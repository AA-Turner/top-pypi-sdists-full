r'''
# `google_clouddeploy_custom_target_type`

Refer to the Terraform Registry for docs: [`google_clouddeploy_custom_target_type`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type).
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


class ClouddeployCustomTargetType(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetType",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type google_clouddeploy_custom_target_type}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_actions: typing.Optional[typing.Union["ClouddeployCustomTargetTypeCustomActions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployCustomTargetTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type google_clouddeploy_custom_target_type} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#location ClouddeployCustomTargetType#location}
        :param name: Name of the 'CustomTargetType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#name ClouddeployCustomTargetType#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#annotations ClouddeployCustomTargetType#annotations}
        :param custom_actions: custom_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#custom_actions ClouddeployCustomTargetType#custom_actions}
        :param description: Description of the 'CustomTargetType'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#description ClouddeployCustomTargetType#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#id ClouddeployCustomTargetType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#labels ClouddeployCustomTargetType#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#project ClouddeployCustomTargetType#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#timeouts ClouddeployCustomTargetType#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa1ec464c2aa508b894d125c0b78bbad568b5e699ff5315a28ae8dda14ebaf1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddeployCustomTargetTypeConfig(
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
        '''Generates CDKTF code for importing a ClouddeployCustomTargetType resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ClouddeployCustomTargetType to import.
        :param import_from_id: The id of the existing ClouddeployCustomTargetType that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ClouddeployCustomTargetType to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dcc730c89feb5ca8d5260b0a0bab5310d55c4d1754818546c75c37773b194c4)
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
        include_skaffold_modules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        render_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deploy_action: The Skaffold custom action responsible for deploy operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#deploy_action ClouddeployCustomTargetType#deploy_action}
        :param include_skaffold_modules: include_skaffold_modules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#include_skaffold_modules ClouddeployCustomTargetType#include_skaffold_modules}
        :param render_action: The Skaffold custom action responsible for render operations. If not provided then Cloud Deploy will perform the render operations via 'skaffold render'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#render_action ClouddeployCustomTargetType#render_action}
        '''
        value = ClouddeployCustomTargetTypeCustomActions(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#create ClouddeployCustomTargetType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#delete ClouddeployCustomTargetType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#update ClouddeployCustomTargetType#update}.
        '''
        value = ClouddeployCustomTargetTypeTimeouts(
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
    ) -> "ClouddeployCustomTargetTypeCustomActionsOutputReference":
        return typing.cast("ClouddeployCustomTargetTypeCustomActionsOutputReference", jsii.get(self, "customActions"))

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
    def timeouts(self) -> "ClouddeployCustomTargetTypeTimeoutsOutputReference":
        return typing.cast("ClouddeployCustomTargetTypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ClouddeployCustomTargetTypeCustomActions"]:
        return typing.cast(typing.Optional["ClouddeployCustomTargetTypeCustomActions"], jsii.get(self, "customActionsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployCustomTargetTypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployCustomTargetTypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06637541af7d9e26c5d702c1cb63adbbd3d842d96b067127db5777a807e5f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f36c79bd435f340a08f2d021fc0475e7533175bd19041e2218fc0c336471ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befae9f9b956c64c0906c8df1c3973103f6c77494f04cb76bbf8d4d6cc2e67f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9c7fc16a8ed1ec1a6a95775f0ba2d0c2205704fd7e6aecf09ef020253db583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe9741133c4325630d794bb29caa96bbe5d6e56dedcc6981fc804bff309e14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7b4aaf89a53b018d92aa8703761b29811d9d375d3feac88ea4ec9383ee4b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fca04e4b415b32e67f3274c73493f78cfd9503f45e1610d2de3de69c2c927c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeConfig",
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
class ClouddeployCustomTargetTypeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_actions: typing.Optional[typing.Union["ClouddeployCustomTargetTypeCustomActions", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployCustomTargetTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#location ClouddeployCustomTargetType#location}
        :param name: Name of the 'CustomTargetType'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#name ClouddeployCustomTargetType#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#annotations ClouddeployCustomTargetType#annotations}
        :param custom_actions: custom_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#custom_actions ClouddeployCustomTargetType#custom_actions}
        :param description: Description of the 'CustomTargetType'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#description ClouddeployCustomTargetType#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#id ClouddeployCustomTargetType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#labels ClouddeployCustomTargetType#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#project ClouddeployCustomTargetType#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#timeouts ClouddeployCustomTargetType#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_actions, dict):
            custom_actions = ClouddeployCustomTargetTypeCustomActions(**custom_actions)
        if isinstance(timeouts, dict):
            timeouts = ClouddeployCustomTargetTypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca61641658d3d12d2f3696d58bf35b71612eb406b021bc1718f749ec2f5913b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#location ClouddeployCustomTargetType#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the 'CustomTargetType'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#name ClouddeployCustomTargetType#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#annotations ClouddeployCustomTargetType#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def custom_actions(
        self,
    ) -> typing.Optional["ClouddeployCustomTargetTypeCustomActions"]:
        '''custom_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#custom_actions ClouddeployCustomTargetType#custom_actions}
        '''
        result = self._values.get("custom_actions")
        return typing.cast(typing.Optional["ClouddeployCustomTargetTypeCustomActions"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the 'CustomTargetType'. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#description ClouddeployCustomTargetType#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#id ClouddeployCustomTargetType#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#labels ClouddeployCustomTargetType#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#project ClouddeployCustomTargetType#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddeployCustomTargetTypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#timeouts ClouddeployCustomTargetType#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddeployCustomTargetTypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActions",
    jsii_struct_bases=[],
    name_mapping={
        "deploy_action": "deployAction",
        "include_skaffold_modules": "includeSkaffoldModules",
        "render_action": "renderAction",
    },
)
class ClouddeployCustomTargetTypeCustomActions:
    def __init__(
        self,
        *,
        deploy_action: builtins.str,
        include_skaffold_modules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        render_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deploy_action: The Skaffold custom action responsible for deploy operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#deploy_action ClouddeployCustomTargetType#deploy_action}
        :param include_skaffold_modules: include_skaffold_modules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#include_skaffold_modules ClouddeployCustomTargetType#include_skaffold_modules}
        :param render_action: The Skaffold custom action responsible for render operations. If not provided then Cloud Deploy will perform the render operations via 'skaffold render'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#render_action ClouddeployCustomTargetType#render_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87476d58dcc6947e0fa64926640269db1ecc5e34b04fdee5add648c52fa18c62)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#deploy_action ClouddeployCustomTargetType#deploy_action}
        '''
        result = self._values.get("deploy_action")
        assert result is not None, "Required property 'deploy_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_skaffold_modules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules"]]]:
        '''include_skaffold_modules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#include_skaffold_modules ClouddeployCustomTargetType#include_skaffold_modules}
        '''
        result = self._values.get("include_skaffold_modules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules"]]], result)

    @builtins.property
    def render_action(self) -> typing.Optional[builtins.str]:
        '''The Skaffold custom action responsible for render operations.

        If not provided then Cloud Deploy will perform the render operations via 'skaffold render'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#render_action ClouddeployCustomTargetType#render_action}
        '''
        result = self._values.get("render_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeCustomActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules",
    jsii_struct_bases=[],
    name_mapping={
        "configs": "configs",
        "git": "git",
        "google_cloud_build_repo": "googleCloudBuildRepo",
        "google_cloud_storage": "googleCloudStorage",
    },
)
class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules:
    def __init__(
        self,
        *,
        configs: typing.Optional[typing.Sequence[builtins.str]] = None,
        git: typing.Optional[typing.Union["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit", typing.Dict[builtins.str, typing.Any]]] = None,
        google_cloud_build_repo: typing.Optional[typing.Union["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo", typing.Dict[builtins.str, typing.Any]]] = None,
        google_cloud_storage: typing.Optional[typing.Union["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configs: The Skaffold Config modules to use from the specified source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#configs ClouddeployCustomTargetType#configs}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#git ClouddeployCustomTargetType#git}
        :param google_cloud_build_repo: google_cloud_build_repo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#google_cloud_build_repo ClouddeployCustomTargetType#google_cloud_build_repo}
        :param google_cloud_storage: google_cloud_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#google_cloud_storage ClouddeployCustomTargetType#google_cloud_storage}
        '''
        if isinstance(git, dict):
            git = ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit(**git)
        if isinstance(google_cloud_build_repo, dict):
            google_cloud_build_repo = ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo(**google_cloud_build_repo)
        if isinstance(google_cloud_storage, dict):
            google_cloud_storage = ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage(**google_cloud_storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84530c39f024e1a9bb0327ce6aa5c9624a95764f629e9a62c4f8a3774cc005c9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#configs ClouddeployCustomTargetType#configs}
        '''
        result = self._values.get("configs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#git ClouddeployCustomTargetType#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit"], result)

    @builtins.property
    def google_cloud_build_repo(
        self,
    ) -> typing.Optional["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo"]:
        '''google_cloud_build_repo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#google_cloud_build_repo ClouddeployCustomTargetType#google_cloud_build_repo}
        '''
        result = self._values.get("google_cloud_build_repo")
        return typing.cast(typing.Optional["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo"], result)

    @builtins.property
    def google_cloud_storage(
        self,
    ) -> typing.Optional["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage"]:
        '''google_cloud_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#google_cloud_storage ClouddeployCustomTargetType#google_cloud_storage}
        '''
        result = self._values.get("google_cloud_storage")
        return typing.cast(typing.Optional["ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit",
    jsii_struct_bases=[],
    name_mapping={"repo": "repo", "path": "path", "ref": "ref"},
)
class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit:
    def __init__(
        self,
        *,
        repo: builtins.str,
        path: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repo: Git repository the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#repo ClouddeployCustomTargetType#repo}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        :param ref: Git ref the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#ref ClouddeployCustomTargetType#ref}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c7003b27244ea168b630acaed42d42c496e72d94b4ac49ac86699883b307f3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#repo ClouddeployCustomTargetType#repo}
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Relative path from the repository root to the Skaffold file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''Git ref the package should be cloned from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#ref ClouddeployCustomTargetType#ref}
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3033612fa0e9777f89693f42ef80f95176bd626c0911347a2299d813bedd6ca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8486cbff7f12bef752efdc5cdac8c407b693aa62d57da34804c1a32c839cc842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56bf189b33ca1fc7d2f49cc11cffd2a06d031f35e89ee8aefd2607bc33a53864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repo"))

    @repo.setter
    def repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e71d83aa59f04090ddde63b10f6caea1aafa6616ad91ae218e6ce817b8017d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6d2d4f4b663879001fbac6868581ec7756965adfead612ccd0eefa6107136b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "path": "path", "ref": "ref"},
)
class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo:
    def __init__(
        self,
        *,
        repository: builtins.str,
        path: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: Cloud Build 2nd gen repository in the format of 'projects//locations//connections//repositories/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#repository ClouddeployCustomTargetType#repository}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        :param ref: Branch or tag to use when cloning the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#ref ClouddeployCustomTargetType#ref}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3167ae979cbc597c32dfac3b126f1d33b2f0a36cbb4fc5ddcee1b3f7b5a739da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#repository ClouddeployCustomTargetType#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Relative path from the repository root to the Skaffold file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''Branch or tag to use when cloning the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#ref ClouddeployCustomTargetType#ref}
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1396d94676b7d00dcebf41cbd2b1da447c19e96fe64fad703804684c96b53b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0da0ef1af05299cd5c78f6f77d219b5de44cca7f89781519851eccf18da0831f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622907c30979f4f2134f7ee2e84cb21c9c3caff7541af583e08c5ad39d47242b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae2722caf2cd542506e3ea8da15155111c1f6b3218b53cb54a85fe5d3f05877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f62282412631197d2b7854ee2681f211246863087fb77b1ec3a7bd8ea554d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "path": "path"},
)
class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage:
    def __init__(
        self,
        *,
        source: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: Cloud Storage source paths to copy recursively. For example, providing 'gs://my-bucket/dir/configs/*' will result in Skaffold copying all files within the 'dir/configs' directory in the bucket 'my-bucket'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#source ClouddeployCustomTargetType#source}
        :param path: Relative path from the source to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b42d11f3407ff2a2134f22877c385efe93a68ea863ed50e2a1634977fe601ef)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#source ClouddeployCustomTargetType#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Relative path from the source to the Skaffold file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab2aab4344ce156d38dcf4a99e209c66bc0ced5b8c53486e99ce5fa553054e29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3d155d4a7428012831452d8113ebc8ebb85b19fdbfd1cc61b945e6ce1da1c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cd7e4e72fb6651e78f24f2847385292f6e3e2af2a84c6ff4a8f93e181c9347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a0ac8fa14659db3a5f7917d79fb89e38c14365766d5cf95aa22871f845c779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__258f99b1bd70f0d8e19b601c08e8588b44a85b8fca48871c43fcbea85933621e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee340d03492a19c9fda60953772b39e9b413768da8153da1aab4feb6b4147a65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8b28cdc01fb464cea7077e209d8908c13c02846907ff9db99dbcc31e51d0db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd7c9b71827682cef168a96567098b32f13f9b600aac00d943af13545c0310e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3994ba7e5a931475c13520c23567af1d054ed0ff2d7e35ad02c61f7df26de35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88094977c408b5612f77f2bc28caeaff7777be5152c2727c449736d21a0ca13f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c690dfaee2ae24145eecd0e9bcebe638cb98f1397ff6d075061f1e2c5fc2c941)
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
        :param repo: Git repository the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#repo ClouddeployCustomTargetType#repo}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        :param ref: Git ref the package should be cloned from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#ref ClouddeployCustomTargetType#ref}
        '''
        value = ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit(
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
        :param repository: Cloud Build 2nd gen repository in the format of 'projects//locations//connections//repositories/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#repository ClouddeployCustomTargetType#repository}
        :param path: Relative path from the repository root to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        :param ref: Branch or tag to use when cloning the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#ref ClouddeployCustomTargetType#ref}
        '''
        value = ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo(
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
        :param source: Cloud Storage source paths to copy recursively. For example, providing 'gs://my-bucket/dir/configs/*' will result in Skaffold copying all files within the 'dir/configs' directory in the bucket 'my-bucket'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#source ClouddeployCustomTargetType#source}
        :param path: Relative path from the source to the Skaffold file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#path ClouddeployCustomTargetType#path}
        '''
        value = ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage(
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
    ) -> ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference:
        return typing.cast(ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudBuildRepo")
    def google_cloud_build_repo(
        self,
    ) -> ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference:
        return typing.cast(ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference, jsii.get(self, "googleCloudBuildRepo"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudStorage")
    def google_cloud_storage(
        self,
    ) -> ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference:
        return typing.cast(ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference, jsii.get(self, "googleCloudStorage"))

    @builtins.property
    @jsii.member(jsii_name="configsInput")
    def configs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "configsInput"))

    @builtins.property
    @jsii.member(jsii_name="gitInput")
    def git_input(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudBuildRepoInput")
    def google_cloud_build_repo_input(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo], jsii.get(self, "googleCloudBuildRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="googleCloudStorageInput")
    def google_cloud_storage_input(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage], jsii.get(self, "googleCloudStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="configs")
    def configs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "configs"))

    @configs.setter
    def configs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b3f7c5bd8799b422750ab7b66243781f3ccb3f7696875984cb4b00a3480a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e1b3b083c91e7c1a82039ff228b7ada2e0dbfe16366108472a3a457922b2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployCustomTargetTypeCustomActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeCustomActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f7f4b039e27203df12a861b86e093889367f96242e3b9b8425d73c06f2b4cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludeSkaffoldModules")
    def put_include_skaffold_modules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5935b8374f2d9149ecb7ff9c157f11839eea3ce598a9d7a19657d02adefc2a4e)
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
    ) -> ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList:
        return typing.cast(ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList, jsii.get(self, "includeSkaffoldModules"))

    @builtins.property
    @jsii.member(jsii_name="deployActionInput")
    def deploy_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployActionInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSkaffoldModulesInput")
    def include_skaffold_modules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]], jsii.get(self, "includeSkaffoldModulesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f76079da3ad47ecafa54aee8ff38c1e1201bee12d745cf38f282b085d295772e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renderAction")
    def render_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renderAction"))

    @render_action.setter
    def render_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c1e662b92cde2c756bb8a0304b9f3662b2116c01c413094810c4d71527de28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renderAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployCustomTargetTypeCustomActions]:
        return typing.cast(typing.Optional[ClouddeployCustomTargetTypeCustomActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployCustomTargetTypeCustomActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a722b9f6c73f16e7f3a9bfa718ea6cc03c1d10f6d4e88753a8601850feb39feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddeployCustomTargetTypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#create ClouddeployCustomTargetType#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#delete ClouddeployCustomTargetType#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#update ClouddeployCustomTargetType#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c0aba7b970159fd689d011e77d0b9388ff615942d3b4094a3fb42274cc7008)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#create ClouddeployCustomTargetType#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#delete ClouddeployCustomTargetType#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_custom_target_type#update ClouddeployCustomTargetType#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployCustomTargetTypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployCustomTargetTypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployCustomTargetType.ClouddeployCustomTargetTypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d97648c7b518da7ef214df847b8d89a9be068d8156e83a940c9795ca655e86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b2b9e321b5fc6e942eeaf242036e57e1bc3979956a5cdbe1712e33557d88591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0042e101c65e92a81c6a2e4529e3be2aca49e282fa63bc6821d8d0243d4a8ff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413745419426906c5e317fe6b7ef7ecc06d0d0a94b467bfbc6ef5a15ba82c804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eef08f224026c7f13ca53d47a902972a0f621aba504f9ed98d357a73dd05c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ClouddeployCustomTargetType",
    "ClouddeployCustomTargetTypeConfig",
    "ClouddeployCustomTargetTypeCustomActions",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGitOutputReference",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepoOutputReference",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorageOutputReference",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesList",
    "ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesOutputReference",
    "ClouddeployCustomTargetTypeCustomActionsOutputReference",
    "ClouddeployCustomTargetTypeTimeouts",
    "ClouddeployCustomTargetTypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9aa1ec464c2aa508b894d125c0b78bbad568b5e699ff5315a28ae8dda14ebaf1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    custom_actions: typing.Optional[typing.Union[ClouddeployCustomTargetTypeCustomActions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployCustomTargetTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4dcc730c89feb5ca8d5260b0a0bab5310d55c4d1754818546c75c37773b194c4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06637541af7d9e26c5d702c1cb63adbbd3d842d96b067127db5777a807e5f83(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f36c79bd435f340a08f2d021fc0475e7533175bd19041e2218fc0c336471ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befae9f9b956c64c0906c8df1c3973103f6c77494f04cb76bbf8d4d6cc2e67f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9c7fc16a8ed1ec1a6a95775f0ba2d0c2205704fd7e6aecf09ef020253db583(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe9741133c4325630d794bb29caa96bbe5d6e56dedcc6981fc804bff309e14a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7b4aaf89a53b018d92aa8703761b29811d9d375d3feac88ea4ec9383ee4b84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fca04e4b415b32e67f3274c73493f78cfd9503f45e1610d2de3de69c2c927c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca61641658d3d12d2f3696d58bf35b71612eb406b021bc1718f749ec2f5913b(
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
    custom_actions: typing.Optional[typing.Union[ClouddeployCustomTargetTypeCustomActions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployCustomTargetTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87476d58dcc6947e0fa64926640269db1ecc5e34b04fdee5add648c52fa18c62(
    *,
    deploy_action: builtins.str,
    include_skaffold_modules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    render_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84530c39f024e1a9bb0327ce6aa5c9624a95764f629e9a62c4f8a3774cc005c9(
    *,
    configs: typing.Optional[typing.Sequence[builtins.str]] = None,
    git: typing.Optional[typing.Union[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit, typing.Dict[builtins.str, typing.Any]]] = None,
    google_cloud_build_repo: typing.Optional[typing.Union[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo, typing.Dict[builtins.str, typing.Any]]] = None,
    google_cloud_storage: typing.Optional[typing.Union[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c7003b27244ea168b630acaed42d42c496e72d94b4ac49ac86699883b307f3(
    *,
    repo: builtins.str,
    path: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3033612fa0e9777f89693f42ef80f95176bd626c0911347a2299d813bedd6ca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8486cbff7f12bef752efdc5cdac8c407b693aa62d57da34804c1a32c839cc842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bf189b33ca1fc7d2f49cc11cffd2a06d031f35e89ee8aefd2607bc33a53864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e71d83aa59f04090ddde63b10f6caea1aafa6616ad91ae218e6ce817b8017d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6d2d4f4b663879001fbac6868581ec7756965adfead612ccd0eefa6107136b(
    value: typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3167ae979cbc597c32dfac3b126f1d33b2f0a36cbb4fc5ddcee1b3f7b5a739da(
    *,
    repository: builtins.str,
    path: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1396d94676b7d00dcebf41cbd2b1da447c19e96fe64fad703804684c96b53b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da0ef1af05299cd5c78f6f77d219b5de44cca7f89781519851eccf18da0831f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622907c30979f4f2134f7ee2e84cb21c9c3caff7541af583e08c5ad39d47242b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae2722caf2cd542506e3ea8da15155111c1f6b3218b53cb54a85fe5d3f05877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f62282412631197d2b7854ee2681f211246863087fb77b1ec3a7bd8ea554d5(
    value: typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudBuildRepo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b42d11f3407ff2a2134f22877c385efe93a68ea863ed50e2a1634977fe601ef(
    *,
    source: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2aab4344ce156d38dcf4a99e209c66bc0ced5b8c53486e99ce5fa553054e29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d155d4a7428012831452d8113ebc8ebb85b19fdbfd1cc61b945e6ce1da1c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cd7e4e72fb6651e78f24f2847385292f6e3e2af2a84c6ff4a8f93e181c9347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a0ac8fa14659db3a5f7917d79fb89e38c14365766d5cf95aa22871f845c779(
    value: typing.Optional[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModulesGoogleCloudStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258f99b1bd70f0d8e19b601c08e8588b44a85b8fca48871c43fcbea85933621e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee340d03492a19c9fda60953772b39e9b413768da8153da1aab4feb6b4147a65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8b28cdc01fb464cea7077e209d8908c13c02846907ff9db99dbcc31e51d0db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd7c9b71827682cef168a96567098b32f13f9b600aac00d943af13545c0310e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3994ba7e5a931475c13520c23567af1d054ed0ff2d7e35ad02c61f7df26de35e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88094977c408b5612f77f2bc28caeaff7777be5152c2727c449736d21a0ca13f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c690dfaee2ae24145eecd0e9bcebe638cb98f1397ff6d075061f1e2c5fc2c941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b3f7c5bd8799b422750ab7b66243781f3ccb3f7696875984cb4b00a3480a74(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e1b3b083c91e7c1a82039ff228b7ada2e0dbfe16366108472a3a457922b2ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f7f4b039e27203df12a861b86e093889367f96242e3b9b8425d73c06f2b4cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5935b8374f2d9149ecb7ff9c157f11839eea3ce598a9d7a19657d02adefc2a4e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployCustomTargetTypeCustomActionsIncludeSkaffoldModules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76079da3ad47ecafa54aee8ff38c1e1201bee12d745cf38f282b085d295772e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c1e662b92cde2c756bb8a0304b9f3662b2116c01c413094810c4d71527de28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a722b9f6c73f16e7f3a9bfa718ea6cc03c1d10f6d4e88753a8601850feb39feb(
    value: typing.Optional[ClouddeployCustomTargetTypeCustomActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c0aba7b970159fd689d011e77d0b9388ff615942d3b4094a3fb42274cc7008(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d97648c7b518da7ef214df847b8d89a9be068d8156e83a940c9795ca655e86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2b9e321b5fc6e942eeaf242036e57e1bc3979956a5cdbe1712e33557d88591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0042e101c65e92a81c6a2e4529e3be2aca49e282fa63bc6821d8d0243d4a8ff9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413745419426906c5e317fe6b7ef7ecc06d0d0a94b467bfbc6ef5a15ba82c804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eef08f224026c7f13ca53d47a902972a0f621aba504f9ed98d357a73dd05c47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployCustomTargetTypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
