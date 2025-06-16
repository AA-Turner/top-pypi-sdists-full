r'''
# `google_clouddeploy_custom_target_type`

Refer to the Terraform Registry for docs: [`google_clouddeploy_custom_target_type`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type).
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


class GoogleClouddeployCustomTargetType(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetType",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type google_clouddeploy_custom_target_type}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_actions: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeCustomActions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type google_clouddeploy_custom_target_type} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#location GoogleClouddeployCustomTargetType#location}
        :param name: Name of the 'CustomTargetType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#name GoogleClouddeployCustomTargetType#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#annotations GoogleClouddeployCustomTargetType#annotations}
        :param custom_actions: custom_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#custom_actions GoogleClouddeployCustomTargetType#custom_actions}
        :param description: Description of the 'CustomTargetType'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#description GoogleClouddeployCustomTargetType#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#id GoogleClouddeployCustomTargetType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#labels GoogleClouddeployCustomTargetType#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#project GoogleClouddeployCustomTargetType#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#timeouts GoogleClouddeployCustomTargetType#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edac1cad5dd15419b77612d8f011289912c52bc90afc7693b81cf6a78ff5f4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleClouddeployCustomTargetTypeConfig(
            location=location,
            name=name,
            annotations=annotations,
            custom_actions=custom_actions,
            description=description,
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
        '''Generates CDKTF code for importing a GoogleClouddeployCustomTargetType resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleClouddeployCustomTargetType to import.
        :param import_from_id: The id of the existing GoogleClouddeployCustomTargetType that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleClouddeployCustomTargetType to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5108fcf4baccbb0224fcdcadafbe4a146ab547597f2600f69780623498e6496f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomActions")
    def put_custom_actions(
        self,
        *,
        deploy_action: builtins.str,
        include_skaffold_modules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        render_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deploy_action: The Skaffold custom action responsible for deploy operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#deploy_action GoogleClouddeployCustomTargetType#deploy_action}
        :param include_skaffold_modules: include_skaffold_modules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#include_skaffold_modules GoogleClouddeployCustomTargetType#include_skaffold_modules}
        :param render_action: The Skaffold custom action responsible for render operations. If not provided then Cloud Deploy will perform the render operations via 'skaffold render'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#render_action GoogleClouddeployCustomTargetType#render_action}
        '''
        value = GoogleClouddeployCustomTargetTypeCustomActions(
            deploy_action=deploy_action,
            include_skaffold_modules=include_skaffold_modules,
            render_action=render_action,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomActions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#create GoogleClouddeployCustomTargetType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#delete GoogleClouddeployCustomTargetType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#update GoogleClouddeployCustomTargetType#update}.
        '''
        value = GoogleClouddeployCustomTargetTypeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetCustomActions")
    def reset_custom_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomActions", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="customActions")
    def custom_actions(
        self,
    ) -> "GoogleClouddeployCustomTargetTypeCustomActionsOutputReference":
        return typing.cast("GoogleClouddeployCustomTargetTypeCustomActionsOutputReference", jsii.get(self, "customActions"))

    @builtins.property
    @jsii.member(jsii_name="customTargetTypeId")
    def custom_target_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customTargetTypeId"))

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
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleClouddeployCustomTargetTypeTimeoutsOutputReference":
        return typing.cast("GoogleClouddeployCustomTargetTypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="customActionsInput")
    def custom_actions_input(
        self,
    ) -> typing.Optional["GoogleClouddeployCustomTargetTypeCustomActions"]:
        return typing.cast(typing.Optional["GoogleClouddeployCustomTargetTypeCustomActions"], jsii.get(self, "customActionsInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployCustomTargetTypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployCustomTargetTypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10efc9c3c1035484da326112583889ced76878fa2c1df3361999e61f295b18d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a46ceb35613aa21784cb3ebd75171484c4a2d31487f68208a712c961277ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f4d32c9d76e1f77702d651dc97c15eab0be96af9aa2638deb40c9663cfc95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b2a6f38c573cefc597ff8da6a7a0e4b59af0723e8e120a7ec51d488e6a02fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7ff61bf1a8a4f9a7701de80fd870edd3efc909834c9c42ee7ea06cc7a7181f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0299282a3f6fc26c9f375c54a9a6dbb109bfafffa00a2c3100a1011c4315780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbe1845b1570180c72ee783dc048bc4e7065f38294c73534ca7d4dc2b0d6676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeConfig",
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
        "custom_actions": "customActions",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleClouddeployCustomTargetTypeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_actions: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeCustomActions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#location GoogleClouddeployCustomTargetType#location}
        :param name: Name of the 'CustomTargetType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#name GoogleClouddeployCustomTargetType#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#annotations GoogleClouddeployCustomTargetType#annotations}
        :param custom_actions: custom_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#custom_actions GoogleClouddeployCustomTargetType#custom_actions}
        :param description: Description of the 'CustomTargetType'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#description GoogleClouddeployCustomTargetType#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#id GoogleClouddeployCustomTargetType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#labels GoogleClouddeployCustomTargetType#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#project GoogleClouddeployCustomTargetType#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#timeouts GoogleClouddeployCustomTargetType#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_actions, dict):
            custom_actions = GoogleClouddeployCustomTargetTypeCustomActions(**custom_actions)
        if isinstance(timeouts, dict):
            timeouts = GoogleClouddeployCustomTargetTypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af94e88d6819d9e97f287380b70995928c7fbeab1d158993d8a0b829b2b4f17)
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
            check_type(argname="argument custom_actions", value=custom_actions, expected_type=type_hints["custom_actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
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
        if custom_actions is not None:
            self._values["custom_actions"] = custom_actions
        if description is not None:
            self._values["description"] = description
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
    def location(self) -> builtins.str:
        '''The location of the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#location GoogleClouddeployCustomTargetType#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the 'CustomTargetType'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#name GoogleClouddeployCustomTargetType#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User annotations.

        These attributes can only be set and used by the user, and not by Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#annotations GoogleClouddeployCustomTargetType#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def custom_actions(
        self,
    ) -> typing.Optional["GoogleClouddeployCustomTargetTypeCustomActions"]:
        '''custom_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#custom_actions GoogleClouddeployCustomTargetType#custom_actions}
        '''
        result = self._values.get("custom_actions")
        return typing.cast(typing.Optional["GoogleClouddeployCustomTargetTypeCustomActions"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the 'CustomTargetType'. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#description GoogleClouddeployCustomTargetType#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#id GoogleClouddeployCustomTargetType#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are attributes that can be set and used by both the user and by Cloud Deploy.

        Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#labels GoogleClouddeployCustomTargetType#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#project GoogleClouddeployCustomTargetType#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleClouddeployCustomTargetTypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#timeouts GoogleClouddeployCustomTargetType#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleClouddeployCustomTargetTypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActions",
    jsii_struct_bases=[],
    name_mapping={
        "deploy_action": "deployAction",
        "include_skaffold_modules": "includeSkaffoldModules",
        "render_action": "renderAction",
    },
)
class GoogleClouddeployCustomTargetTypeCustomActions:
    def __init__(
        self,
        *,
        deploy_action: builtins.str,
        include_skaffold_modules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        render_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deploy_action: The Skaffold custom action responsible for deploy operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#deploy_action GoogleClouddeployCustomTargetType#deploy_action}
        :param include_skaffold_modules: include_skaffold_modules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#include_skaffold_modules GoogleClouddeployCustomTargetType#include_skaffold_modules}
        :param render_action: The Skaffold custom action responsible for render operations. If not provided then Cloud Deploy will perform the render operations via 'skaffold render'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#render_action GoogleClouddeployCustomTargetType#render_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2367ce98c3c3e275146251aab62ab146ee967bd9dc544fc3a3d8444882c319e)
            check_type(argname="argument deploy_action", value=deploy_action, expected_type=type_hints["deploy_action"])
            check_type(argname="argument include_skaffold_modules", value=include_skaffold_modules, expected_type=type_hints["include_skaffold_modules"])
            check_type(argname="argument render_action", value=render_action, expected_type=type_hints["render_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deploy_action": deploy_action,
        }
        if include_skaffold_modules is not None:
            self._values["include_skaffold_modules"] = include_skaffold_modules
        if render_action is not None:
            self._values["render_action"] = render_action

    @builtins.property
    def deploy_action(self) -> builtins.str:
        '''The Skaffold custom action responsible for deploy operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#deploy_action GoogleClouddeployCustomTargetType#deploy_action}
        '''
        result = self._values.get("deploy_action")
        assert result is not None, "Required property 'deploy_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_skaffold_modules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules"]]]:
        '''include_skaffold_modules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#include_skaffold_modules GoogleClouddeployCustomTargetType#include_skaffold_modules}
        '''
        result = self._values.get("include_skaffold_modules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules"]]], result)

    @builtins.property
    def render_action(self) -> typing.Optional[builtins.str]:
        '''The Skaffold custom action responsible for render operations.

        If not provided then Cloud Deploy will perform the render operations via 'skaffold render'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#render_action GoogleClouddeployCustomTargetType#render_action}
        '''
        result = self._values.get("render_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeCustomActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules",
    jsii_struct_bases=[],
    name_mapping={
        "configs": "configs",
        "git": "git",
        "google_cloud_build_repo": "googleCloudBuildRepo",
        "google_cloud_storage": "googleCloudStorage",
    },
)
class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules:
    def __init__(
        self,
        *,
        configs: typing.Optional[typing.Sequence[builtins.str]] = None,
        git: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit", typing.Dict[builtins.str, typing.Any]]] = None,
        google_cloud_build_repo: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo", typing.Dict[builtins.str, typing.Any]]] = None,
        google_cloud_storage: typing.Optional[typing.Union["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configs: The Skaffold Config modules to use from the specified source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#configs GoogleClouddeployCustomTargetType#configs}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#git GoogleClouddeployCustomTargetType#git}
        :param google_cloud_build_repo: google_cloud_build_repo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#google_cloud_build_repo GoogleClouddeployCustomTargetType#google_cloud_build_repo}
        :param google_cloud_storage: google_cloud_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#google_cloud_storage GoogleClouddeployCustomTargetType#google_cloud_storage}
        '''
        if isinstance(git, dict):
            git = GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit(**git)
        if isinstance(google_cloud_build_repo, dict):
            google_cloud_build_repo = GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo(**google_cloud_build_repo)
        if isinstance(google_cloud_storage, dict):
            google_cloud_storage = GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage(**google_cloud_storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93188b7ecb7e3adecc7481c965440409830537a6f17779dc3b8ce2e495882fba)
            check_type(argname="argument configs", value=configs, expected_type=type_hints["configs"])
            check_type(argname="argument git", value=git, expected_type=type_hints["git"])
            check_type(argname="argument google_cloud_build_repo", value=google_cloud_build_repo, expected_type=type_hints["google_cloud_build_repo"])
            check_type(argname="argument google_cloud_storage", value=google_cloud_storage, expected_type=type_hints["google_cloud_storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configs is not None:
            self._values["configs"] = configs
        if git is not None:
            self._values["git"] = git
        if google_cloud_build_repo is not None:
            self._values["google_cloud_build_repo"] = google_cloud_build_repo
        if google_cloud_storage is not None:
            self._values["google_cloud_storage"] = google_cloud_storage

    @builtins.property
    def configs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Skaffold Config modules to use from the specified source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#configs GoogleClouddeployCustomTargetType#configs}
        '''
        result = self._values.get("configs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#git GoogleClouddeployCustomTargetType#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit"], result)

    @builtins.property
    def google_cloud_build_repo(
        self,
    ) -> typing.Optional["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo"]:
        '''google_cloud_build_repo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#google_cloud_build_repo GoogleClouddeployCustomTargetType#google_cloud_build_repo}
        '''
        result = self._values.get("google_cloud_build_repo")
        return typing.cast(typing.Optional["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo"], result)

    @builtins.property
    def google_cloud_storage(
        self,
    ) -> typing.Optional["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage"]:
        '''google_cloud_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#google_cloud_storage GoogleClouddeployCustomTargetType#google_cloud_storage}
        '''
        result = self._values.get("google_cloud_storage")
        return typing.cast(typing.Optional["GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit",
    jsii_struct_bases=[],
    name_mapping={"repo": "repo", "path": "path", "ref": "ref"},
)
class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit:
    def __init__(
        self,
        *,
        repo: builtins.str,
        path: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repo: Git repository the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#repo GoogleClouddeployCustomTargetType#repo}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        :param ref: Git ref the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#ref GoogleClouddeployCustomTargetType#ref}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e77eadaea8bc812e38d8a7f02d03c9363c8b522bd7a8758fba58137af95250)
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repo": repo,
        }
        if path is not None:
            self._values["path"] = path
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def repo(self) -> builtins.str:
        '''Git repository the package should be cloned from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#repo GoogleClouddeployCustomTargetType#repo}
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Relative path from the repository root to the Skaffold file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''Git ref the package should be cloned from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#ref GoogleClouddeployCustomTargetType#ref}
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb25c983b720ab9df1f5e7d1a745cd6af363bcda118e53f5d13434ddae1580d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRef")
    def reset_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRef", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="refInput")
    def ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refInput"))

    @builtins.property
    @jsii.member(jsii_name="repoInput")
    def repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb2d90e7b45bcc566cf34ea4e5d72eba799a435a6f32590d8d7603f727f5065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5f8739ea8d706630106ad94d05cf4dad6d8439263456020065db3a5b865cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repo"))

    @repo.setter
    def repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2901192e279414b17086f53add36ec94a830da9d2f37132e32ed5192b992d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17aafa8e9966d35487140012ff48b8bd0a82800b7c199f114e9c2d8a2b075bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "path": "path", "ref": "ref"},
)
class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo:
    def __init__(
        self,
        *,
        repository: builtins.str,
        path: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: Cloud Build 2nd gen repository in the format of 'projects//locations//connections//repositories/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#repository GoogleClouddeployCustomTargetType#repository}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        :param ref: Branch or tag to use when cloning the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#ref GoogleClouddeployCustomTargetType#ref}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7021479b3b3bb882b640a7a25f5405a5b3d145a857b228eb925f678c0602db83)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if path is not None:
            self._values["path"] = path
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def repository(self) -> builtins.str:
        '''Cloud Build 2nd gen repository in the format of 'projects//locations//connections//repositories/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#repository GoogleClouddeployCustomTargetType#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Relative path from the repository root to the Skaffold file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''Branch or tag to use when cloning the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#ref GoogleClouddeployCustomTargetType#ref}
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c1effe2b977604ab8baea9fc47f297fbfc88757b8d7b4f4e0d151b339deddc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRef")
    def reset_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRef", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="refInput")
    def ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265820f2fb7bc995276e3eb1b23395b72031b3d7c322fbfd187a009a6027255c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ed75c49e792bec4336c3ed79c9066d69e44ec0ecda5736ac21523fb8f6fc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c1654ffddd1db0f4b797e5eb3ec7e9b4a2467feec6bbd409b59b02fba5370c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662eae7c54010b746589cf992e6b77af2c10b6806570421bba66dfdcc08d760a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "path": "path"},
)
class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage:
    def __init__(
        self,
        *,
        source: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: Cloud Storage source paths to copy recursively. For example, providing 'gs://my-bucket/dir/configs/*' will result in Skaffold copying all files within the 'dir/configs' directory in the bucket 'my-bucket'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#source GoogleClouddeployCustomTargetType#source}
        :param path: Relative path from the source to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828e0d1a85f9f9eaf18ea0f6bee83e9b2fa3420c1145b40ee181c95077c90a39)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def source(self) -> builtins.str:
        '''Cloud Storage source paths to copy recursively.

        For example, providing 'gs://my-bucket/dir/configs/*' will result in Skaffold copying all files within the 'dir/configs' directory in the bucket 'my-bucket'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#source GoogleClouddeployCustomTargetType#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Relative path from the source to the Skaffold file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d64b6a57fdc0d5233dc9745cad2c956bd094f37b25c9511ff2a1f15b38087900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492db1bdbe2f731fa701e5e1eeafa8acedfa7b09dda859e77d9dd1e486408796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab15a5dc45ab64935c600f3af319076e8e208697efbf3e9ccf6cfb8718de9f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91836bfc2002faaeaf587f4711a169fbb368dde410d1935c1ed16eccfb2a0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c30b208cabb70c7ed8cdca91cec54beedf58dde9608e69cc2dc196eef2887a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914c71f2e5dfec03edf416ed5ee071ef053413fda4fe11b7918f3e7220d073fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ed9919e32c50367d11baf7627015a7c6c8a71f9b0ea34e34cac79115e12124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57276125b88e064283799f65000328f8143ffd6862daad3d90cfcc64b18cc589)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c1fd4fd0918abecf5067693226fa93a261cbcf4aa37ddec278ded35df477d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf6d0e944a66f04d839948e4f249a94b792c485f909408e5310f012e0af5309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0513c635cc92a13c2e6942e51986e67deb77494c76ab5e795e4b1415b4a76c1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGit")
    def put_git(
        self,
        *,
        repo: builtins.str,
        path: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repo: Git repository the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#repo GoogleClouddeployCustomTargetType#repo}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        :param ref: Git ref the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#ref GoogleClouddeployCustomTargetType#ref}
        '''
        value = GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit(
            repo=repo, path=path, ref=ref
        )

        return typing.cast(None, jsii.invoke(self, "putGit", [value]))

    @jsii.member(jsii_name="putGoogleCloudBuildRepo")
    def put_google_cloud_build_repo(
        self,
        *,
        repository: builtins.str,
        path: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: Cloud Build 2nd gen repository in the format of 'projects//locations//connections//repositories/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#repository GoogleClouddeployCustomTargetType#repository}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        :param ref: Branch or tag to use when cloning the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#ref GoogleClouddeployCustomTargetType#ref}
        '''
        value = GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo(
            repository=repository, path=path, ref=ref
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleCloudBuildRepo", [value]))

    @jsii.member(jsii_name="putGoogleCloudStorage")
    def put_google_cloud_storage(
        self,
        *,
        source: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: Cloud Storage source paths to copy recursively. For example, providing 'gs://my-bucket/dir/configs/*' will result in Skaffold copying all files within the 'dir/configs' directory in the bucket 'my-bucket'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#source GoogleClouddeployCustomTargetType#source}
        :param path: Relative path from the source to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#path GoogleClouddeployCustomTargetType#path}
        '''
        value = GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage(
            source=source, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleCloudStorage", [value]))

    @jsii.member(jsii_name="resetConfigs")
    def reset_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigs", []))

    @jsii.member(jsii_name="resetGit")
    def reset_git(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGit", []))

    @jsii.member(jsii_name="resetGoogleCloudBuildRepo")
    def reset_google_cloud_build_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleCloudBuildRepo", []))

    @jsii.member(jsii_name="resetGoogleCloudStorage")
    def reset_google_cloud_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleCloudStorage", []))

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(
        self,
    ) -> GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference:
        return typing.cast(GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudBuildRepo")
    def google_cloud_build_repo(
        self,
    ) -> GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference:
        return typing.cast(GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference, jsii.get(self, "googleCloudBuildRepo"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudStorage")
    def google_cloud_storage(
        self,
    ) -> GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference:
        return typing.cast(GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference, jsii.get(self, "googleCloudStorage"))

    @builtins.property
    @jsii.member(jsii_name="configsInput")
    def configs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "configsInput"))

    @builtins.property
    @jsii.member(jsii_name="gitInput")
    def git_input(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudBuildRepoInput")
    def google_cloud_build_repo_input(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo], jsii.get(self, "googleCloudBuildRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudStorageInput")
    def google_cloud_storage_input(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage], jsii.get(self, "googleCloudStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="configs")
    def configs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "configs"))

    @configs.setter
    def configs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4084ee922a08ad3d61231c1e0b1cad38a711fb522c55dbfea6a98300b73e6fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75ba06a144021ecefac3dabaa924199c227b04aa3c69325b516ae1084ecc90e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployCustomTargetTypeCustomActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeCustomActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1cd40c3a8dbf1a9b879a300530a176063c91f47942dde4e879a81646b33ebd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludeSkaffoldModules")
    def put_include_skaffold_modules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec40d40ff4fb1b97f57d0ba53f3a5b9ac726f3831e1bf22e8ba4e58063bf19ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncludeSkaffoldModules", [value]))

    @jsii.member(jsii_name="resetIncludeSkaffoldModules")
    def reset_include_skaffold_modules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSkaffoldModules", []))

    @jsii.member(jsii_name="resetRenderAction")
    def reset_render_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenderAction", []))

    @builtins.property
    @jsii.member(jsii_name="includeSkaffoldModules")
    def include_skaffold_modules(
        self,
    ) -> GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList:
        return typing.cast(GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList, jsii.get(self, "includeSkaffoldModules"))

    @builtins.property
    @jsii.member(jsii_name="deployActionInput")
    def deploy_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployActionInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSkaffoldModulesInput")
    def include_skaffold_modules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]], jsii.get(self, "includeSkaffoldModulesInput"))

    @builtins.property
    @jsii.member(jsii_name="renderActionInput")
    def render_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "renderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="deployAction")
    def deploy_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployAction"))

    @deploy_action.setter
    def deploy_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29031ee06d0ba752870a653fdd010663b0176544b55f0ca0be5c8bcd39bd2f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renderAction")
    def render_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renderAction"))

    @render_action.setter
    def render_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ecd37618c792a440b22c8c3630b136c0770c42141b381292e1295bb20e47c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renderAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployCustomTargetTypeCustomActions]:
        return typing.cast(typing.Optional[GoogleClouddeployCustomTargetTypeCustomActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4541af1c5ea654d10e9e924cd5bb8a69560f2bd60212a7bf648d283095aa2cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleClouddeployCustomTargetTypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#create GoogleClouddeployCustomTargetType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#delete GoogleClouddeployCustomTargetType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#update GoogleClouddeployCustomTargetType#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9f6a195cbad7a0cf8185585ef5f60a40281e18423153bca2f4898606d54a6b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#create GoogleClouddeployCustomTargetType#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#delete GoogleClouddeployCustomTargetType#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_custom_target_type#update GoogleClouddeployCustomTargetType#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployCustomTargetTypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployCustomTargetTypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployCustomTargetType.GoogleClouddeployCustomTargetTypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8be2ead6e3e23822a0ee082255e490c3d69b5f8dc721fc89397794a23e6c8a62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4acf47c56475d1f4c50288fb35fb51af30af5f0189771b87a61a3e1f6de8e832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1350b8432000f4aa2226acc48d3ab356c2192be4bed3190df40aa2a82ff789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b75ad28a8af87083695546ee8b98100bbdef813af13998732c498bcb4d2d2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24220ad5bb93f3f1a1ef1ec95f39e18ee102f9b93af5569471b18f49a7f3076d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleClouddeployCustomTargetType",
    "GoogleClouddeployCustomTargetTypeConfig",
    "GoogleClouddeployCustomTargetTypeCustomActions",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList",
    "GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference",
    "GoogleClouddeployCustomTargetTypeCustomActionsOutputReference",
    "GoogleClouddeployCustomTargetTypeTimeouts",
    "GoogleClouddeployCustomTargetTypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8edac1cad5dd15419b77612d8f011289912c52bc90afc7693b81cf6a78ff5f4a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    custom_actions: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeCustomActions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5108fcf4baccbb0224fcdcadafbe4a146ab547597f2600f69780623498e6496f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10efc9c3c1035484da326112583889ced76878fa2c1df3361999e61f295b18d3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a46ceb35613aa21784cb3ebd75171484c4a2d31487f68208a712c961277ae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f4d32c9d76e1f77702d651dc97c15eab0be96af9aa2638deb40c9663cfc95c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b2a6f38c573cefc597ff8da6a7a0e4b59af0723e8e120a7ec51d488e6a02fd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7ff61bf1a8a4f9a7701de80fd870edd3efc909834c9c42ee7ea06cc7a7181f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0299282a3f6fc26c9f375c54a9a6dbb109bfafffa00a2c3100a1011c4315780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbe1845b1570180c72ee783dc048bc4e7065f38294c73534ca7d4dc2b0d6676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af94e88d6819d9e97f287380b70995928c7fbeab1d158993d8a0b829b2b4f17(
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
    custom_actions: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeCustomActions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2367ce98c3c3e275146251aab62ab146ee967bd9dc544fc3a3d8444882c319e(
    *,
    deploy_action: builtins.str,
    include_skaffold_modules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    render_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93188b7ecb7e3adecc7481c965440409830537a6f17779dc3b8ce2e495882fba(
    *,
    configs: typing.Optional[typing.Sequence[builtins.str]] = None,
    git: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit, typing.Dict[builtins.str, typing.Any]]] = None,
    google_cloud_build_repo: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo, typing.Dict[builtins.str, typing.Any]]] = None,
    google_cloud_storage: typing.Optional[typing.Union[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e77eadaea8bc812e38d8a7f02d03c9363c8b522bd7a8758fba58137af95250(
    *,
    repo: builtins.str,
    path: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb25c983b720ab9df1f5e7d1a745cd6af363bcda118e53f5d13434ddae1580d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb2d90e7b45bcc566cf34ea4e5d72eba799a435a6f32590d8d7603f727f5065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5f8739ea8d706630106ad94d05cf4dad6d8439263456020065db3a5b865cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2901192e279414b17086f53add36ec94a830da9d2f37132e32ed5192b992d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aafa8e9966d35487140012ff48b8bd0a82800b7c199f114e9c2d8a2b075bac(
    value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7021479b3b3bb882b640a7a25f5405a5b3d145a857b228eb925f678c0602db83(
    *,
    repository: builtins.str,
    path: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c1effe2b977604ab8baea9fc47f297fbfc88757b8d7b4f4e0d151b339deddc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265820f2fb7bc995276e3eb1b23395b72031b3d7c322fbfd187a009a6027255c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ed75c49e792bec4336c3ed79c9066d69e44ec0ecda5736ac21523fb8f6fc42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c1654ffddd1db0f4b797e5eb3ec7e9b4a2467feec6bbd409b59b02fba5370c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662eae7c54010b746589cf992e6b77af2c10b6806570421bba66dfdcc08d760a(
    value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828e0d1a85f9f9eaf18ea0f6bee83e9b2fa3420c1145b40ee181c95077c90a39(
    *,
    source: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64b6a57fdc0d5233dc9745cad2c956bd094f37b25c9511ff2a1f15b38087900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492db1bdbe2f731fa701e5e1eeafa8acedfa7b09dda859e77d9dd1e486408796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab15a5dc45ab64935c600f3af319076e8e208697efbf3e9ccf6cfb8718de9f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91836bfc2002faaeaf587f4711a169fbb368dde410d1935c1ed16eccfb2a0f5(
    value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c30b208cabb70c7ed8cdca91cec54beedf58dde9608e69cc2dc196eef2887a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914c71f2e5dfec03edf416ed5ee071ef053413fda4fe11b7918f3e7220d073fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ed9919e32c50367d11baf7627015a7c6c8a71f9b0ea34e34cac79115e12124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57276125b88e064283799f65000328f8143ffd6862daad3d90cfcc64b18cc589(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c1fd4fd0918abecf5067693226fa93a261cbcf4aa37ddec278ded35df477d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf6d0e944a66f04d839948e4f249a94b792c485f909408e5310f012e0af5309(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0513c635cc92a13c2e6942e51986e67deb77494c76ab5e795e4b1415b4a76c1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4084ee922a08ad3d61231c1e0b1cad38a711fb522c55dbfea6a98300b73e6fbe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75ba06a144021ecefac3dabaa924199c227b04aa3c69325b516ae1084ecc90e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cd40c3a8dbf1a9b879a300530a176063c91f47942dde4e879a81646b33ebd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec40d40ff4fb1b97f57d0ba53f3a5b9ac726f3831e1bf22e8ba4e58063bf19ac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29031ee06d0ba752870a653fdd010663b0176544b55f0ca0be5c8bcd39bd2f59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ecd37618c792a440b22c8c3630b136c0770c42141b381292e1295bb20e47c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4541af1c5ea654d10e9e924cd5bb8a69560f2bd60212a7bf648d283095aa2cac(
    value: typing.Optional[GoogleClouddeployCustomTargetTypeCustomActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9f6a195cbad7a0cf8185585ef5f60a40281e18423153bca2f4898606d54a6b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be2ead6e3e23822a0ee082255e490c3d69b5f8dc721fc89397794a23e6c8a62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acf47c56475d1f4c50288fb35fb51af30af5f0189771b87a61a3e1f6de8e832(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1350b8432000f4aa2226acc48d3ab356c2192be4bed3190df40aa2a82ff789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b75ad28a8af87083695546ee8b98100bbdef813af13998732c498bcb4d2d2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24220ad5bb93f3f1a1ef1ec95f39e18ee102f9b93af5569471b18f49a7f3076d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployCustomTargetTypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
