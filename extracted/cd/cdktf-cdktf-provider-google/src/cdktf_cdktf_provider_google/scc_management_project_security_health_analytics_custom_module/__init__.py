r'''
# `google_scc_management_project_security_health_analytics_custom_module`

Refer to the Terraform Registry for docs: [`google_scc_management_project_security_health_analytics_custom_module`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module).
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


class SccManagementProjectSecurityHealthAnalyticsCustomModule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module google_scc_management_project_security_health_analytics_custom_module}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        custom_config: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enablement_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module google_scc_management_project_security_health_analytics_custom_module} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#custom_config SccManagementProjectSecurityHealthAnalyticsCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#display_name SccManagementProjectSecurityHealthAnalyticsCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#enablement_state SccManagementProjectSecurityHealthAnalyticsCustomModule#enablement_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#id SccManagementProjectSecurityHealthAnalyticsCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: Location ID of the parent organization. If not provided, 'global' will be used as the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#project SccManagementProjectSecurityHealthAnalyticsCustomModule#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#timeouts SccManagementProjectSecurityHealthAnalyticsCustomModule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c31e16854382e44113d37a49bc252eb5ce855c9fd5caa799e5e2f847a15e6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SccManagementProjectSecurityHealthAnalyticsCustomModuleConfig(
            custom_config=custom_config,
            display_name=display_name,
            enablement_state=enablement_state,
            id=id,
            location=location,
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
        '''Generates CDKTF code for importing a SccManagementProjectSecurityHealthAnalyticsCustomModule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SccManagementProjectSecurityHealthAnalyticsCustomModule to import.
        :param import_from_id: The id of the existing SccManagementProjectSecurityHealthAnalyticsCustomModule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SccManagementProjectSecurityHealthAnalyticsCustomModule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5958827ee0700b1519529dcbe198373954fb621cbc8ebaf1907cb1f3288fe482)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomConfig")
    def put_custom_config(
        self,
        *,
        predicate: typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        recommendation: builtins.str,
        resource_selector: typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#predicate SccManagementProjectSecurityHealthAnalyticsCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#recommendation SccManagementProjectSecurityHealthAnalyticsCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#resource_selector SccManagementProjectSecurityHealthAnalyticsCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#severity SccManagementProjectSecurityHealthAnalyticsCustomModule#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#custom_output SccManagementProjectSecurityHealthAnalyticsCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        '''
        value = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig(
            predicate=predicate,
            recommendation=recommendation,
            resource_selector=resource_selector,
            severity=severity,
            custom_output=custom_output,
            description=description,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#create SccManagementProjectSecurityHealthAnalyticsCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#delete SccManagementProjectSecurityHealthAnalyticsCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#update SccManagementProjectSecurityHealthAnalyticsCustomModule#update}.
        '''
        value = SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts(
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
    @jsii.member(jsii_name="ancestorModule")
    def ancestor_module(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ancestorModule"))

    @builtins.property
    @jsii.member(jsii_name="customConfig")
    def custom_config(
        self,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference":
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference", jsii.get(self, "customConfig"))

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
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference":
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="customConfigInput")
    def custom_config_input(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig"]:
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig"], jsii.get(self, "customConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enablementStateInput")
    def enablement_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enablementStateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3e71b50534c6a1835abd29e9615665cceab8624ac67081f552a2b31712e726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablementState")
    def enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementState"))

    @enablement_state.setter
    def enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5daed4d3905f19c7c98661750d5b53316ae987d9753727b4cf5a322a619096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb16cd14d91e6c7cbd600b14a81161e2a71cd9c6b759d1d36a653bee0fd998c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aefecc699851519354d0daa0b874b08a1c2f9e032d3f89348032ff696923df37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac47664210b336b866d4908352f5f187845b27f8d67147e9c671a535d0caa4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "custom_config": "customConfig",
        "display_name": "displayName",
        "enablement_state": "enablementState",
        "id": "id",
        "location": "location",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleConfig(
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
        custom_config: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enablement_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#custom_config SccManagementProjectSecurityHealthAnalyticsCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#display_name SccManagementProjectSecurityHealthAnalyticsCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#enablement_state SccManagementProjectSecurityHealthAnalyticsCustomModule#enablement_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#id SccManagementProjectSecurityHealthAnalyticsCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: Location ID of the parent organization. If not provided, 'global' will be used as the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#project SccManagementProjectSecurityHealthAnalyticsCustomModule#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#timeouts SccManagementProjectSecurityHealthAnalyticsCustomModule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_config, dict):
            custom_config = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig(**custom_config)
        if isinstance(timeouts, dict):
            timeouts = SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af685055858ffe2a2b1cbf5601da892978c30a8468a9b38211942e12d489fb05)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enablement_state", value=enablement_state, expected_type=type_hints["enablement_state"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
    def custom_config(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig"]:
        '''custom_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#custom_config SccManagementProjectSecurityHealthAnalyticsCustomModule#custom_config}
        '''
        result = self._values.get("custom_config")
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Security Health Analytics custom module.

        This
        display name becomes the finding category for all findings that are
        returned by this custom module. The display name must be between 1 and
        128 characters, start with a lowercase letter, and contain alphanumeric
        characters or underscores only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#display_name SccManagementProjectSecurityHealthAnalyticsCustomModule#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enablement_state(self) -> typing.Optional[builtins.str]:
        '''The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#enablement_state SccManagementProjectSecurityHealthAnalyticsCustomModule#enablement_state}
        '''
        result = self._values.get("enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#id SccManagementProjectSecurityHealthAnalyticsCustomModule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location ID of the parent organization. If not provided, 'global' will be used as the default location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#project SccManagementProjectSecurityHealthAnalyticsCustomModule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#timeouts SccManagementProjectSecurityHealthAnalyticsCustomModule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig",
    jsii_struct_bases=[],
    name_mapping={
        "predicate": "predicate",
        "recommendation": "recommendation",
        "resource_selector": "resourceSelector",
        "severity": "severity",
        "custom_output": "customOutput",
        "description": "description",
    },
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig:
    def __init__(
        self,
        *,
        predicate: typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        recommendation: builtins.str,
        resource_selector: typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#predicate SccManagementProjectSecurityHealthAnalyticsCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#recommendation SccManagementProjectSecurityHealthAnalyticsCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#resource_selector SccManagementProjectSecurityHealthAnalyticsCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#severity SccManagementProjectSecurityHealthAnalyticsCustomModule#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#custom_output SccManagementProjectSecurityHealthAnalyticsCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        '''
        if isinstance(predicate, dict):
            predicate = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(**predicate)
        if isinstance(resource_selector, dict):
            resource_selector = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(**resource_selector)
        if isinstance(custom_output, dict):
            custom_output = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(**custom_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a79522ce9520214eb3154252ada235f7c08f02b7b20959c7db59caa68039a9)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
            check_type(argname="argument resource_selector", value=resource_selector, expected_type=type_hints["resource_selector"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument custom_output", value=custom_output, expected_type=type_hints["custom_output"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "predicate": predicate,
            "recommendation": recommendation,
            "resource_selector": resource_selector,
            "severity": severity,
        }
        if custom_output is not None:
            self._values["custom_output"] = custom_output
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def predicate(
        self,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate":
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#predicate SccManagementProjectSecurityHealthAnalyticsCustomModule#predicate}
        '''
        result = self._values.get("predicate")
        assert result is not None, "Required property 'predicate' is missing"
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", result)

    @builtins.property
    def recommendation(self) -> builtins.str:
        '''An explanation of the recommended steps that security teams can take to resolve the detected issue.

        This explanation is returned with each finding generated by
        this module in the nextSteps property of the finding JSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#recommendation SccManagementProjectSecurityHealthAnalyticsCustomModule#recommendation}
        '''
        result = self._values.get("recommendation")
        assert result is not None, "Required property 'recommendation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_selector(
        self,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector":
        '''resource_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#resource_selector SccManagementProjectSecurityHealthAnalyticsCustomModule#resource_selector}
        '''
        result = self._values.get("resource_selector")
        assert result is not None, "Required property 'resource_selector' is missing"
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#severity SccManagementProjectSecurityHealthAnalyticsCustomModule#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_output(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput"]:
        '''custom_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#custom_output SccManagementProjectSecurityHealthAnalyticsCustomModule#custom_output}
        '''
        result = self._values.get("custom_output")
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text that describes the vulnerability or misconfiguration that the custom module detects.

        This explanation is returned with each finding instance to
        help investigators understand the detected issue. The text must be enclosed in quotation marks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties"},
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput:
    def __init__(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#properties SccManagementProjectSecurityHealthAnalyticsCustomModule#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eae29d871bc4904563261e9752c30f6667b3a065e8542904fb48e82f9d1c168)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#properties SccManagementProjectSecurityHealthAnalyticsCustomModule#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74909efe4e8beadedf393b7c6874be07730b813b76122750a78c5b3c6fffbec1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a5773db0c9fcd328c15d7b0a46f5313738726ea6dd4dfc648c4dea07a41bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList":
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af7c12c9a210a3ae61f3cb622863a38cb60f26a23f3a6635dbffead771312b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value_expression": "valueExpression"},
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value_expression: typing.Optional[typing.Union["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the property for the custom output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#name SccManagementProjectSecurityHealthAnalyticsCustomModule#name}
        :param value_expression: value_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#value_expression SccManagementProjectSecurityHealthAnalyticsCustomModule#value_expression}
        '''
        if isinstance(value_expression, dict):
            value_expression = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(**value_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b431ab987ce5f124bbe90eb438cd4f47d894060168cabdfd10fa7c4d2b698df)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#name SccManagementProjectSecurityHealthAnalyticsCustomModule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_expression(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        '''value_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#value_expression SccManagementProjectSecurityHealthAnalyticsCustomModule#value_expression}
        '''
        result = self._values.get("value_expression")
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b27cdacabe3f7ae0c8265c81d30f6c2bf9887ba319922bed7088b1a40800a83b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad316cbdc9a19bc11a36bd170a8c4bf36388efcbaf33a71dc08190f9c6fac020)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5290978257e416ab8b249ee7a8856b4f52c47946f36ae946d8f169d77c7d6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__962f63a38bb3a8205bd56ff3a0ac999ae730cf55f4d500caeebc5021485613ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__424ee515af063dae3d056a228347234eac10148fee881559cca874973f5bf132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f98ce05aa5b001284b0f318592eaf672087f511bf9383e094e33911d3d3380f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13c16316e992b7bbe3c7c8b7c539275bb57a77aa9b2c8a4ba17e24c57c1e3379)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#expression SccManagementProjectSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#title SccManagementProjectSecurityHealthAnalyticsCustomModule#title}
        '''
        value = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(
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
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference":
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference", jsii.get(self, "valueExpression"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExpressionInput")
    def value_expression_input(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], jsii.get(self, "valueExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af24818a6b0066e566be102a4c7ad040b356173d331424d3edb4aee3ca166765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de70ced8e6f25c7c0bf70420bc44a4203d84ccacb77778fcdf7cfaabab3f4b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#expression SccManagementProjectSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#title SccManagementProjectSecurityHealthAnalyticsCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33637510aefca2f555a9902422c2ac77951c4cdde767837c31a460a6dc044f4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#expression SccManagementProjectSecurityHealthAnalyticsCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#title SccManagementProjectSecurityHealthAnalyticsCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__262235aeccc45f943e98b9a652130fb88f58581523ba5b2f610f90f320f31ef2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ec6d9060f4f8a93a879da745e8b9c05e31c8d2aa3ac7074daa227a0a86f30f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44be6c322648aa66b3aed9332035c84d7d02c58cb183db8f28b32cc48e7de14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd1c027661fbbf9f88d5e08ae51427088118fd046564a06d7d98d1a11a20f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627ac44f48f29716b615843260ccbe7a6d231d69450565c61c30a893acbf554e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression]:
        return typing.cast(typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ec82e0ef3b4c7899ff846a95663c44e80682e5fe74add9a14c6c3bedc630ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fe2508d092f5ff0f17393a6cfad3ad9010ecaf862a58e3bc16bef4915006ee8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomOutput")
    def put_custom_output(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#properties SccManagementProjectSecurityHealthAnalyticsCustomModule#properties}
        '''
        value = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#expression SccManagementProjectSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#title SccManagementProjectSecurityHealthAnalyticsCustomModule#title}
        '''
        value = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(
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
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#resource_types SccManagementProjectSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        value = SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(
            resource_types=resource_types
        )

        return typing.cast(None, jsii.invoke(self, "putResourceSelector", [value]))

    @jsii.member(jsii_name="resetCustomOutput")
    def reset_custom_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOutput", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="customOutput")
    def custom_output(
        self,
    ) -> SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference:
        return typing.cast(SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference, jsii.get(self, "customOutput"))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference":
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelector")
    def resource_selector(
        self,
    ) -> "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference":
        return typing.cast("SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference", jsii.get(self, "resourceSelector"))

    @builtins.property
    @jsii.member(jsii_name="customOutputInput")
    def custom_output_input(
        self,
    ) -> typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput], jsii.get(self, "customOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"]:
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationInput")
    def recommendation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelectorInput")
    def resource_selector_input(
        self,
    ) -> typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"]:
        return typing.cast(typing.Optional["SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"], jsii.get(self, "resourceSelectorInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__21a5e576b53ee5f6096b17a47b5e4bd394313d43d4d9cde29b2608e64c1550f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @recommendation.setter
    def recommendation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245b4f0473ddb162f19663e10606d218935d4902f80cd54d5e4926214d8191bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1403bfa0bbb015ee45f23bac9dd07ea1848bd877a395ce7730dbe027c1d4d631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig]:
        return typing.cast(typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4917e82d63879e105d6e3950048867d4946fa8e0ffa3a0ace24d386cd02b131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#expression SccManagementProjectSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#title SccManagementProjectSecurityHealthAnalyticsCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9dc0e783d1526011ab25ce55e2d7bd838e6a8879d6e7af77bff56ebe8e0fb44)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#expression SccManagementProjectSecurityHealthAnalyticsCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#description SccManagementProjectSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#location SccManagementProjectSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#title SccManagementProjectSecurityHealthAnalyticsCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3b8a0548cabd262d40e0b73376a8e516e97d8284613bbdfb90fd92c51a5e6dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c6c6da78d812b1601fd9f6b2916517620e41e9673c9b3c2275d2b371b1e53e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e906269d9dc1d35ec6decf76ab06fb2c41479db928d11c2f588954809bd80b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1565a42c250c76ae37ba7f9ff339d1356166784691ff83dd367e2d9792e7c1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3809d967ae3831547a4c5404339032ca03cd03e5be13410c26fcac2cfa4bb02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate]:
        return typing.cast(typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be88d448fa71683fffb9782abbf7f459ab95ad7c8cf4f75566576665c398453e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector:
    def __init__(self, *, resource_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#resource_types SccManagementProjectSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580102bfc59bc09f8e10372de064ab07655ef665ad6a4e1155d783962def7e9a)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_types": resource_types,
        }

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''The resource types to run the detector on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#resource_types SccManagementProjectSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56daabffd043b3474be6a3513c02eea975f850c483592420a50aa113b1ec6f21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75142fad28ee3bbda048e0899ac2ebe9514378698ca6e0bef6602fee192d8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector]:
        return typing.cast(typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171f54d710ad8d624b93498d581cd42b579cad11e9296b571d6ee53cc1ab7037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#create SccManagementProjectSecurityHealthAnalyticsCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#delete SccManagementProjectSecurityHealthAnalyticsCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#update SccManagementProjectSecurityHealthAnalyticsCustomModule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a07a1495949e491091092527f65c36be6c70febb4cd249c023bc08674388cfa)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#create SccManagementProjectSecurityHealthAnalyticsCustomModule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#delete SccManagementProjectSecurityHealthAnalyticsCustomModule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_project_security_health_analytics_custom_module#update SccManagementProjectSecurityHealthAnalyticsCustomModule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementProjectSecurityHealthAnalyticsCustomModule.SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae679c6fef7c4e5e05eaf303a82bc0166ac81bec91a715e9250683bb66458ddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c0a8a5cf5dc7ed6bf2c28ba398616b0787f97b85ac116c0116687aef328b74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24e8213027723e63dfbac85c18763e3a6ccc07b499390b5033886e88857e1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0904881309521b7a0109104e66b1945c0e15f1ad5a2c61a024aa662c10b73e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445d26d858ff76e3924ad47cbf78671cc855e2cfeef318ae014781d91522134c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SccManagementProjectSecurityHealthAnalyticsCustomModule",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleConfig",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts",
    "SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__61c31e16854382e44113d37a49bc252eb5ce855c9fd5caa799e5e2f847a15e6f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    custom_config: typing.Optional[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enablement_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5958827ee0700b1519529dcbe198373954fb621cbc8ebaf1907cb1f3288fe482(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3e71b50534c6a1835abd29e9615665cceab8624ac67081f552a2b31712e726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5daed4d3905f19c7c98661750d5b53316ae987d9753727b4cf5a322a619096(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb16cd14d91e6c7cbd600b14a81161e2a71cd9c6b759d1d36a653bee0fd998c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefecc699851519354d0daa0b874b08a1c2f9e032d3f89348032ff696923df37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac47664210b336b866d4908352f5f187845b27f8d67147e9c671a535d0caa4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af685055858ffe2a2b1cbf5601da892978c30a8468a9b38211942e12d489fb05(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_config: typing.Optional[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enablement_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a79522ce9520214eb3154252ada235f7c08f02b7b20959c7db59caa68039a9(
    *,
    predicate: typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate, typing.Dict[builtins.str, typing.Any]],
    recommendation: builtins.str,
    resource_selector: typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
    severity: builtins.str,
    custom_output: typing.Optional[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eae29d871bc4904563261e9752c30f6667b3a065e8542904fb48e82f9d1c168(
    *,
    properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74909efe4e8beadedf393b7c6874be07730b813b76122750a78c5b3c6fffbec1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a5773db0c9fcd328c15d7b0a46f5313738726ea6dd4dfc648c4dea07a41bc0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af7c12c9a210a3ae61f3cb622863a38cb60f26a23f3a6635dbffead771312b4(
    value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b431ab987ce5f124bbe90eb438cd4f47d894060168cabdfd10fa7c4d2b698df(
    *,
    name: typing.Optional[builtins.str] = None,
    value_expression: typing.Optional[typing.Union[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27cdacabe3f7ae0c8265c81d30f6c2bf9887ba319922bed7088b1a40800a83b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad316cbdc9a19bc11a36bd170a8c4bf36388efcbaf33a71dc08190f9c6fac020(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5290978257e416ab8b249ee7a8856b4f52c47946f36ae946d8f169d77c7d6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962f63a38bb3a8205bd56ff3a0ac999ae730cf55f4d500caeebc5021485613ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424ee515af063dae3d056a228347234eac10148fee881559cca874973f5bf132(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f98ce05aa5b001284b0f318592eaf672087f511bf9383e094e33911d3d3380f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c16316e992b7bbe3c7c8b7c539275bb57a77aa9b2c8a4ba17e24c57c1e3379(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af24818a6b0066e566be102a4c7ad040b356173d331424d3edb4aee3ca166765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de70ced8e6f25c7c0bf70420bc44a4203d84ccacb77778fcdf7cfaabab3f4b9e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33637510aefca2f555a9902422c2ac77951c4cdde767837c31a460a6dc044f4(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262235aeccc45f943e98b9a652130fb88f58581523ba5b2f610f90f320f31ef2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ec6d9060f4f8a93a879da745e8b9c05e31c8d2aa3ac7074daa227a0a86f30f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44be6c322648aa66b3aed9332035c84d7d02c58cb183db8f28b32cc48e7de14c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd1c027661fbbf9f88d5e08ae51427088118fd046564a06d7d98d1a11a20f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627ac44f48f29716b615843260ccbe7a6d231d69450565c61c30a893acbf554e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ec82e0ef3b4c7899ff846a95663c44e80682e5fe74add9a14c6c3bedc630ac(
    value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe2508d092f5ff0f17393a6cfad3ad9010ecaf862a58e3bc16bef4915006ee8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a5e576b53ee5f6096b17a47b5e4bd394313d43d4d9cde29b2608e64c1550f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245b4f0473ddb162f19663e10606d218935d4902f80cd54d5e4926214d8191bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1403bfa0bbb015ee45f23bac9dd07ea1848bd877a395ce7730dbe027c1d4d631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4917e82d63879e105d6e3950048867d4946fa8e0ffa3a0ace24d386cd02b131(
    value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9dc0e783d1526011ab25ce55e2d7bd838e6a8879d6e7af77bff56ebe8e0fb44(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b8a0548cabd262d40e0b73376a8e516e97d8284613bbdfb90fd92c51a5e6dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6c6da78d812b1601fd9f6b2916517620e41e9673c9b3c2275d2b371b1e53e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e906269d9dc1d35ec6decf76ab06fb2c41479db928d11c2f588954809bd80b45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1565a42c250c76ae37ba7f9ff339d1356166784691ff83dd367e2d9792e7c1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3809d967ae3831547a4c5404339032ca03cd03e5be13410c26fcac2cfa4bb02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be88d448fa71683fffb9782abbf7f459ab95ad7c8cf4f75566576665c398453e(
    value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580102bfc59bc09f8e10372de064ab07655ef665ad6a4e1155d783962def7e9a(
    *,
    resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56daabffd043b3474be6a3513c02eea975f850c483592420a50aa113b1ec6f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75142fad28ee3bbda048e0899ac2ebe9514378698ca6e0bef6602fee192d8a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171f54d710ad8d624b93498d581cd42b579cad11e9296b571d6ee53cc1ab7037(
    value: typing.Optional[SccManagementProjectSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a07a1495949e491091092527f65c36be6c70febb4cd249c023bc08674388cfa(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae679c6fef7c4e5e05eaf303a82bc0166ac81bec91a715e9250683bb66458ddc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0a8a5cf5dc7ed6bf2c28ba398616b0787f97b85ac116c0116687aef328b74b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24e8213027723e63dfbac85c18763e3a6ccc07b499390b5033886e88857e1f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0904881309521b7a0109104e66b1945c0e15f1ad5a2c61a024aa662c10b73e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445d26d858ff76e3924ad47cbf78671cc855e2cfeef318ae014781d91522134c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementProjectSecurityHealthAnalyticsCustomModuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
