r'''
# `google_scc_management_folder_security_health_analytics_custom_module`

Refer to the Terraform Registry for docs: [`google_scc_management_folder_security_health_analytics_custom_module`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module).
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


class SccManagementFolderSecurityHealthAnalyticsCustomModule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module google_scc_management_folder_security_health_analytics_custom_module}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        folder: builtins.str,
        custom_config: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enablement_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module google_scc_management_folder_security_health_analytics_custom_module} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param folder: Numerical ID of the parent folder. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#folder SccManagementFolderSecurityHealthAnalyticsCustomModule#folder}
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#custom_config SccManagementFolderSecurityHealthAnalyticsCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#display_name SccManagementFolderSecurityHealthAnalyticsCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#enablement_state SccManagementFolderSecurityHealthAnalyticsCustomModule#enablement_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#id SccManagementFolderSecurityHealthAnalyticsCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: Location ID of the parent organization. If not provided, 'global' will be used as the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#timeouts SccManagementFolderSecurityHealthAnalyticsCustomModule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3ff6e225a23b16e58ef07f16ad1893aa09f30328e589360ae87ab08afc2682)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SccManagementFolderSecurityHealthAnalyticsCustomModuleConfig(
            folder=folder,
            custom_config=custom_config,
            display_name=display_name,
            enablement_state=enablement_state,
            id=id,
            location=location,
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
        '''Generates CDKTF code for importing a SccManagementFolderSecurityHealthAnalyticsCustomModule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SccManagementFolderSecurityHealthAnalyticsCustomModule to import.
        :param import_from_id: The id of the existing SccManagementFolderSecurityHealthAnalyticsCustomModule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SccManagementFolderSecurityHealthAnalyticsCustomModule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd98fe447a94b43d204ae9bb0713322209b728aa450d55fa7d3f08b3c376f09)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomConfig")
    def put_custom_config(
        self,
        *,
        custom_output: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        predicate: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]]] = None,
        recommendation: typing.Optional[builtins.str] = None,
        resource_selector: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#custom_output SccManagementFolderSecurityHealthAnalyticsCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#predicate SccManagementFolderSecurityHealthAnalyticsCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#recommendation SccManagementFolderSecurityHealthAnalyticsCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#resource_selector SccManagementFolderSecurityHealthAnalyticsCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#severity SccManagementFolderSecurityHealthAnalyticsCustomModule#severity}
        '''
        value = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig(
            custom_output=custom_output,
            description=description,
            predicate=predicate,
            recommendation=recommendation,
            resource_selector=resource_selector,
            severity=severity,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#create SccManagementFolderSecurityHealthAnalyticsCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#delete SccManagementFolderSecurityHealthAnalyticsCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#update SccManagementFolderSecurityHealthAnalyticsCustomModule#update}.
        '''
        value = SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomConfig")
    def reset_custom_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConfig", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnablementState")
    def reset_enablement_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablementState", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

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
    @jsii.member(jsii_name="ancestorModule")
    def ancestor_module(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ancestorModule"))

    @builtins.property
    @jsii.member(jsii_name="customConfig")
    def custom_config(
        self,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference":
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference", jsii.get(self, "customConfig"))

    @builtins.property
    @jsii.member(jsii_name="lastEditor")
    def last_editor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastEditor"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference":
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="customConfigInput")
    def custom_config_input(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig"]:
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig"], jsii.get(self, "customConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enablementStateInput")
    def enablement_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enablementStateInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14686e3a64a40c2ef7482fc261f00f6afcb02a5021fab557afec42a00e7a5f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablementState")
    def enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementState"))

    @enablement_state.setter
    def enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c30fa17c92df150f7aa5410cec64337035be9dffc24c9e48fd0a9e5deead703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4157664dfe5d6ae6a1bde63e1ec2ef9957866c45078f5582476b659b2a68e725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cefc62eff58f67d5d15933046f8a881814ec937d99b9835449f1bc0ca4fcf6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab867e187da368f6a5e6a510a0747ab0d60896fc851c45ba4b000b9dbb61c27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "folder": "folder",
        "custom_config": "customConfig",
        "display_name": "displayName",
        "enablement_state": "enablementState",
        "id": "id",
        "location": "location",
        "timeouts": "timeouts",
    },
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        folder: builtins.str,
        custom_config: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enablement_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param folder: Numerical ID of the parent folder. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#folder SccManagementFolderSecurityHealthAnalyticsCustomModule#folder}
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#custom_config SccManagementFolderSecurityHealthAnalyticsCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#display_name SccManagementFolderSecurityHealthAnalyticsCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#enablement_state SccManagementFolderSecurityHealthAnalyticsCustomModule#enablement_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#id SccManagementFolderSecurityHealthAnalyticsCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: Location ID of the parent organization. If not provided, 'global' will be used as the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#timeouts SccManagementFolderSecurityHealthAnalyticsCustomModule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_config, dict):
            custom_config = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig(**custom_config)
        if isinstance(timeouts, dict):
            timeouts = SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c611217105fa8677759fc5b6751361507157e1b24ef29de46704ec5156bd2144)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enablement_state", value=enablement_state, expected_type=type_hints["enablement_state"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "folder": folder,
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
        if custom_config is not None:
            self._values["custom_config"] = custom_config
        if display_name is not None:
            self._values["display_name"] = display_name
        if enablement_state is not None:
            self._values["enablement_state"] = enablement_state
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
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
    def folder(self) -> builtins.str:
        '''Numerical ID of the parent folder.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#folder SccManagementFolderSecurityHealthAnalyticsCustomModule#folder}
        '''
        result = self._values.get("folder")
        assert result is not None, "Required property 'folder' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_config(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig"]:
        '''custom_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#custom_config SccManagementFolderSecurityHealthAnalyticsCustomModule#custom_config}
        '''
        result = self._values.get("custom_config")
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Security Health Analytics custom module.

        This
        display name becomes the finding category for all findings that are
        returned by this custom module. The display name must be between 1 and
        128 characters, start with a lowercase letter, and contain alphanumeric
        characters or underscores only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#display_name SccManagementFolderSecurityHealthAnalyticsCustomModule#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enablement_state(self) -> typing.Optional[builtins.str]:
        '''The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#enablement_state SccManagementFolderSecurityHealthAnalyticsCustomModule#enablement_state}
        '''
        result = self._values.get("enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#id SccManagementFolderSecurityHealthAnalyticsCustomModule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location ID of the parent organization. If not provided, 'global' will be used as the default location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#timeouts SccManagementFolderSecurityHealthAnalyticsCustomModule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig",
    jsii_struct_bases=[],
    name_mapping={
        "custom_output": "customOutput",
        "description": "description",
        "predicate": "predicate",
        "recommendation": "recommendation",
        "resource_selector": "resourceSelector",
        "severity": "severity",
    },
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig:
    def __init__(
        self,
        *,
        custom_output: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        predicate: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]]] = None,
        recommendation: typing.Optional[builtins.str] = None,
        resource_selector: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#custom_output SccManagementFolderSecurityHealthAnalyticsCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#predicate SccManagementFolderSecurityHealthAnalyticsCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#recommendation SccManagementFolderSecurityHealthAnalyticsCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#resource_selector SccManagementFolderSecurityHealthAnalyticsCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#severity SccManagementFolderSecurityHealthAnalyticsCustomModule#severity}
        '''
        if isinstance(custom_output, dict):
            custom_output = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(**custom_output)
        if isinstance(predicate, dict):
            predicate = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(**predicate)
        if isinstance(resource_selector, dict):
            resource_selector = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(**resource_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abafd8d172ea102ffe90826f9facb0058e3b317137ae199f2cf8471891133ca)
            check_type(argname="argument custom_output", value=custom_output, expected_type=type_hints["custom_output"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
            check_type(argname="argument resource_selector", value=resource_selector, expected_type=type_hints["resource_selector"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_output is not None:
            self._values["custom_output"] = custom_output
        if description is not None:
            self._values["description"] = description
        if predicate is not None:
            self._values["predicate"] = predicate
        if recommendation is not None:
            self._values["recommendation"] = recommendation
        if resource_selector is not None:
            self._values["resource_selector"] = resource_selector
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def custom_output(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput"]:
        '''custom_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#custom_output SccManagementFolderSecurityHealthAnalyticsCustomModule#custom_output}
        '''
        result = self._values.get("custom_output")
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text that describes the vulnerability or misconfiguration that the custom module detects.

        This explanation is returned with each finding instance to
        help investigators understand the detected issue. The text must be enclosed in quotation marks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predicate(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"]:
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#predicate SccManagementFolderSecurityHealthAnalyticsCustomModule#predicate}
        '''
        result = self._values.get("predicate")
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"], result)

    @builtins.property
    def recommendation(self) -> typing.Optional[builtins.str]:
        '''An explanation of the recommended steps that security teams can take to resolve the detected issue.

        This explanation is returned with each finding generated by
        this module in the nextSteps property of the finding JSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#recommendation SccManagementFolderSecurityHealthAnalyticsCustomModule#recommendation}
        '''
        result = self._values.get("recommendation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_selector(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"]:
        '''resource_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#resource_selector SccManagementFolderSecurityHealthAnalyticsCustomModule#resource_selector}
        '''
        result = self._values.get("resource_selector")
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#severity SccManagementFolderSecurityHealthAnalyticsCustomModule#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties"},
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput:
    def __init__(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#properties SccManagementFolderSecurityHealthAnalyticsCustomModule#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cb34afd9afa30f55ba368ea23b2d440126a3da05c65017e2e63131b950666d)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#properties SccManagementFolderSecurityHealthAnalyticsCustomModule#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd8c4dc89007e13d919e3ca2f417a388abeac7585b6312e00bf4d879431a7bcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85588fc8b5c9bfaa59e937541fc3ca66e79c72e828698cda6c10a01f1be299dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList":
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df898d8c70dcda28609aceb0f54b612fbbe25ccc5057425bce5d257294dcc702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value_expression": "valueExpression"},
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value_expression: typing.Optional[typing.Union["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the property for the custom output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#name SccManagementFolderSecurityHealthAnalyticsCustomModule#name}
        :param value_expression: value_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#value_expression SccManagementFolderSecurityHealthAnalyticsCustomModule#value_expression}
        '''
        if isinstance(value_expression, dict):
            value_expression = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(**value_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf924e28e5121ea494031523e5c17ea12ff04d1cbd83bf463c06bc7cae3e79ae)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value_expression", value=value_expression, expected_type=type_hints["value_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value_expression is not None:
            self._values["value_expression"] = value_expression

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the property for the custom output.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#name SccManagementFolderSecurityHealthAnalyticsCustomModule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_expression(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        '''value_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#value_expression SccManagementFolderSecurityHealthAnalyticsCustomModule#value_expression}
        '''
        result = self._values.get("value_expression")
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__479492fd5307b56c3f9e984570443a0ba851e6349d5d7657611d1c9b16ae501f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc558a2657f85622dabb4440e97f7c46ec4083bc494dc7424390d852ad6f024e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0a9f1da100e4c3cb2af8077a47293cf1934eced9522b0f4ed055d36a7be88e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e5bc97fd3b3be9bb7f246b8915f2bbce4215e4646391255f1054de1bf66c8b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__193a6f31573418b0d414273f0159be957eca4f371c171bc98d1ddc154365b292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8f738c9cdbb14e4e3f3a7978e8df77b075ede3b0b60f487955614a57669b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ede1b69d50169641d0d574db2c111d67e5f8703f51498d8d5e50ed572894ebf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueExpression")
    def put_value_expression(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#expression SccManagementFolderSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#title SccManagementFolderSecurityHealthAnalyticsCustomModule#title}
        '''
        value = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putValueExpression", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValueExpression")
    def reset_value_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueExpression", []))

    @builtins.property
    @jsii.member(jsii_name="valueExpression")
    def value_expression(
        self,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference":
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference", jsii.get(self, "valueExpression"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExpressionInput")
    def value_expression_input(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], jsii.get(self, "valueExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c260fb3aedea07477be5c57f24e8c7b10f48f9cb2203c782375676b6f4727ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c7c487db90c2f3154bb0c121feb66b7fb0f341807b21d43a844374eba1a053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#expression SccManagementFolderSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#title SccManagementFolderSecurityHealthAnalyticsCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8bd5eaab060cbeb8cb6ae43f0e9328cf383a55d085963f946a90cd78e557fa)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#expression SccManagementFolderSecurityHealthAnalyticsCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#title SccManagementFolderSecurityHealthAnalyticsCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a481849dc4f413f75cb89622a14ca6bbc5f830d7b66044388e8ba09131baf2e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d92c88f8a4a3ee7eedba3ed7647e02671547596640c55db966f382fd9c5e389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975cffb5ba2e90cb872fe1a468710e04adc1b1e9237f99c8cefcdfe01b78b730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd9acedaaddd5582c61f26d99b286be0fdf85dd9f3c40833218297b9688dc84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e58f26030d71036b8ac23153eefcbb8499d57f7b7770e7fe214069be4af0c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression]:
        return typing.cast(typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f9c1fb1d3c9388f670c8c476a759a3710d9062b6331fa7802045642f50934e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5b381f3e551c1c603785cb367677dad77665eadf752e128beb03a2a35500696)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomOutput")
    def put_custom_output(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#properties SccManagementFolderSecurityHealthAnalyticsCustomModule#properties}
        '''
        value = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(
            properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomOutput", [value]))

    @jsii.member(jsii_name="putPredicate")
    def put_predicate(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#expression SccManagementFolderSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#title SccManagementFolderSecurityHealthAnalyticsCustomModule#title}
        '''
        value = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putPredicate", [value]))

    @jsii.member(jsii_name="putResourceSelector")
    def put_resource_selector(
        self,
        *,
        resource_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#resource_types SccManagementFolderSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        value = SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(
            resource_types=resource_types
        )

        return typing.cast(None, jsii.invoke(self, "putResourceSelector", [value]))

    @jsii.member(jsii_name="resetCustomOutput")
    def reset_custom_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOutput", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetPredicate")
    def reset_predicate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredicate", []))

    @jsii.member(jsii_name="resetRecommendation")
    def reset_recommendation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendation", []))

    @jsii.member(jsii_name="resetResourceSelector")
    def reset_resource_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceSelector", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @builtins.property
    @jsii.member(jsii_name="customOutput")
    def custom_output(
        self,
    ) -> SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference:
        return typing.cast(SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference, jsii.get(self, "customOutput"))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference":
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelector")
    def resource_selector(
        self,
    ) -> "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference":
        return typing.cast("SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference", jsii.get(self, "resourceSelector"))

    @builtins.property
    @jsii.member(jsii_name="customOutputInput")
    def custom_output_input(
        self,
    ) -> typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput], jsii.get(self, "customOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"]:
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationInput")
    def recommendation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelectorInput")
    def resource_selector_input(
        self,
    ) -> typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"]:
        return typing.cast(typing.Optional["SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"], jsii.get(self, "resourceSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6bb14e52b2f847827a57b336a04273b769b6f0b85885959ab203acce9835c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @recommendation.setter
    def recommendation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc65602a2dd127323eb765b881327aea542214c401267db30d3ac2079b480ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8ceffc291fea60ac41251d1fb76c85e62ebf70dbcff463ab0ddbe2e3e9dbb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig]:
        return typing.cast(typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367cde732cd677f8b589af6e002ef9fd80234ec914638241f9c9b4fef1b47365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#expression SccManagementFolderSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#title SccManagementFolderSecurityHealthAnalyticsCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2a7344aa505190e824965db8162bc0fc01693b6246c7430d76400f3a986675)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#expression SccManagementFolderSecurityHealthAnalyticsCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#description SccManagementFolderSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#location SccManagementFolderSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#title SccManagementFolderSecurityHealthAnalyticsCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93ed68337519d69630daabcb1e35c34f959a4d488a2749875763287b07ceea7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de526d75b4e9cde60440a3129ef0eec6489a057bf40b8c0ff4af43ece485887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b0c2fcf7d7d903a90f8ce16a269a694713304a9443fdc06b17841c3b0608cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96eaf7404a2f6e61dffa87422b4234172df95ab49d4174e10619446f28622c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0acb5bfb3bd96524501d87939f57150b12e3b9c1c4066a29017737a713d47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate]:
        return typing.cast(typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9134a59061b1332fa7019836cf05abcfa9db51c053d23d323ee538bf87d9d031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector:
    def __init__(self, *, resource_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#resource_types SccManagementFolderSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd33fe7a543c1d86bea527c5531632f8afdcd7dc4594bc275953321fb0c74dbc)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_types": resource_types,
        }

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''The resource types to run the detector on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#resource_types SccManagementFolderSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e989ec8d8d20bcb618ac267ed42014c6a367a6c1bc8db2c26cd5c7ee3909051f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0365797d30050952f45fdee97e5702afef4c859755e388a3a0ed3507289d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector]:
        return typing.cast(typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f79d28cdf3b0f62b445213932e75c059312bd017a6937d4650341f45d3e5d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#create SccManagementFolderSecurityHealthAnalyticsCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#delete SccManagementFolderSecurityHealthAnalyticsCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#update SccManagementFolderSecurityHealthAnalyticsCustomModule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f61039c6437c96f87240ac2b0dd853034eb9ecac27e2466007c4369b3a03d7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#create SccManagementFolderSecurityHealthAnalyticsCustomModule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#delete SccManagementFolderSecurityHealthAnalyticsCustomModule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_folder_security_health_analytics_custom_module#update SccManagementFolderSecurityHealthAnalyticsCustomModule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementFolderSecurityHealthAnalyticsCustomModule.SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e3514504926bd27edd5c270bb61c47de884eab97e4da2874e4821a60c6a94c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32086029f2e8d43b9321567da5925f534e4cd24f2d0dcf6e7e10995983a7286a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37bd68a0183edc7ef64394ce0546b0b4adfeb669ea854b070940648ac80d5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ee227f7ada3426bf8568feaf6c6d2fbb600dbef526c57c035ec76bc8949e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8583ae12c8bae888ca8e1c529d2ebf4ae60afb31adccadce971c5c0024275a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SccManagementFolderSecurityHealthAnalyticsCustomModule",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleConfig",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts",
    "SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8e3ff6e225a23b16e58ef07f16ad1893aa09f30328e589360ae87ab08afc2682(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    folder: builtins.str,
    custom_config: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enablement_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8bd98fe447a94b43d204ae9bb0713322209b728aa450d55fa7d3f08b3c376f09(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14686e3a64a40c2ef7482fc261f00f6afcb02a5021fab557afec42a00e7a5f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c30fa17c92df150f7aa5410cec64337035be9dffc24c9e48fd0a9e5deead703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4157664dfe5d6ae6a1bde63e1ec2ef9957866c45078f5582476b659b2a68e725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cefc62eff58f67d5d15933046f8a881814ec937d99b9835449f1bc0ca4fcf6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab867e187da368f6a5e6a510a0747ab0d60896fc851c45ba4b000b9dbb61c27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c611217105fa8677759fc5b6751361507157e1b24ef29de46704ec5156bd2144(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    folder: builtins.str,
    custom_config: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enablement_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abafd8d172ea102ffe90826f9facb0058e3b317137ae199f2cf8471891133ca(
    *,
    custom_output: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    predicate: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate, typing.Dict[builtins.str, typing.Any]]] = None,
    recommendation: typing.Optional[builtins.str] = None,
    resource_selector: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cb34afd9afa30f55ba368ea23b2d440126a3da05c65017e2e63131b950666d(
    *,
    properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8c4dc89007e13d919e3ca2f417a388abeac7585b6312e00bf4d879431a7bcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85588fc8b5c9bfaa59e937541fc3ca66e79c72e828698cda6c10a01f1be299dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df898d8c70dcda28609aceb0f54b612fbbe25ccc5057425bce5d257294dcc702(
    value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf924e28e5121ea494031523e5c17ea12ff04d1cbd83bf463c06bc7cae3e79ae(
    *,
    name: typing.Optional[builtins.str] = None,
    value_expression: typing.Optional[typing.Union[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479492fd5307b56c3f9e984570443a0ba851e6349d5d7657611d1c9b16ae501f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc558a2657f85622dabb4440e97f7c46ec4083bc494dc7424390d852ad6f024e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0a9f1da100e4c3cb2af8077a47293cf1934eced9522b0f4ed055d36a7be88e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5bc97fd3b3be9bb7f246b8915f2bbce4215e4646391255f1054de1bf66c8b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193a6f31573418b0d414273f0159be957eca4f371c171bc98d1ddc154365b292(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8f738c9cdbb14e4e3f3a7978e8df77b075ede3b0b60f487955614a57669b22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ede1b69d50169641d0d574db2c111d67e5f8703f51498d8d5e50ed572894ebf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c260fb3aedea07477be5c57f24e8c7b10f48f9cb2203c782375676b6f4727ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c7c487db90c2f3154bb0c121feb66b7fb0f341807b21d43a844374eba1a053(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8bd5eaab060cbeb8cb6ae43f0e9328cf383a55d085963f946a90cd78e557fa(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a481849dc4f413f75cb89622a14ca6bbc5f830d7b66044388e8ba09131baf2e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d92c88f8a4a3ee7eedba3ed7647e02671547596640c55db966f382fd9c5e389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975cffb5ba2e90cb872fe1a468710e04adc1b1e9237f99c8cefcdfe01b78b730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd9acedaaddd5582c61f26d99b286be0fdf85dd9f3c40833218297b9688dc84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e58f26030d71036b8ac23153eefcbb8499d57f7b7770e7fe214069be4af0c77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f9c1fb1d3c9388f670c8c476a759a3710d9062b6331fa7802045642f50934e(
    value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b381f3e551c1c603785cb367677dad77665eadf752e128beb03a2a35500696(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6bb14e52b2f847827a57b336a04273b769b6f0b85885959ab203acce9835c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc65602a2dd127323eb765b881327aea542214c401267db30d3ac2079b480ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8ceffc291fea60ac41251d1fb76c85e62ebf70dbcff463ab0ddbe2e3e9dbb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367cde732cd677f8b589af6e002ef9fd80234ec914638241f9c9b4fef1b47365(
    value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2a7344aa505190e824965db8162bc0fc01693b6246c7430d76400f3a986675(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ed68337519d69630daabcb1e35c34f959a4d488a2749875763287b07ceea7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de526d75b4e9cde60440a3129ef0eec6489a057bf40b8c0ff4af43ece485887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b0c2fcf7d7d903a90f8ce16a269a694713304a9443fdc06b17841c3b0608cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96eaf7404a2f6e61dffa87422b4234172df95ab49d4174e10619446f28622c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0acb5bfb3bd96524501d87939f57150b12e3b9c1c4066a29017737a713d47d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9134a59061b1332fa7019836cf05abcfa9db51c053d23d323ee538bf87d9d031(
    value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd33fe7a543c1d86bea527c5531632f8afdcd7dc4594bc275953321fb0c74dbc(
    *,
    resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e989ec8d8d20bcb618ac267ed42014c6a367a6c1bc8db2c26cd5c7ee3909051f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0365797d30050952f45fdee97e5702afef4c859755e388a3a0ed3507289d45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f79d28cdf3b0f62b445213932e75c059312bd017a6937d4650341f45d3e5d5a(
    value: typing.Optional[SccManagementFolderSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f61039c6437c96f87240ac2b0dd853034eb9ecac27e2466007c4369b3a03d7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e3514504926bd27edd5c270bb61c47de884eab97e4da2874e4821a60c6a94c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32086029f2e8d43b9321567da5925f534e4cd24f2d0dcf6e7e10995983a7286a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37bd68a0183edc7ef64394ce0546b0b4adfeb669ea854b070940648ac80d5c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ee227f7ada3426bf8568feaf6c6d2fbb600dbef526c57c035ec76bc8949e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8583ae12c8bae888ca8e1c529d2ebf4ae60afb31adccadce971c5c0024275a2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementFolderSecurityHealthAnalyticsCustomModuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
