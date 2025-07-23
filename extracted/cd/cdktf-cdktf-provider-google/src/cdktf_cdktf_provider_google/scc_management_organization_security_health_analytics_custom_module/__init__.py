r'''
# `google_scc_management_organization_security_health_analytics_custom_module`

Refer to the Terraform Registry for docs: [`google_scc_management_organization_security_health_analytics_custom_module`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module).
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


class SccManagementOrganizationSecurityHealthAnalyticsCustomModule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module google_scc_management_organization_security_health_analytics_custom_module}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        organization: builtins.str,
        custom_config: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enablement_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module google_scc_management_organization_security_health_analytics_custom_module} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param organization: Numerical ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#organization SccManagementOrganizationSecurityHealthAnalyticsCustomModule#organization}
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#custom_config SccManagementOrganizationSecurityHealthAnalyticsCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#display_name SccManagementOrganizationSecurityHealthAnalyticsCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#enablement_state SccManagementOrganizationSecurityHealthAnalyticsCustomModule#enablement_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#id SccManagementOrganizationSecurityHealthAnalyticsCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: Location ID of the parent organization. If not provided, 'global' will be used as the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#timeouts SccManagementOrganizationSecurityHealthAnalyticsCustomModule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271f6680a494e567ddf911110f007f0bdecbe5627bc0a65c49f78930c983c49d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleConfig(
            organization=organization,
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
        '''Generates CDKTF code for importing a SccManagementOrganizationSecurityHealthAnalyticsCustomModule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SccManagementOrganizationSecurityHealthAnalyticsCustomModule to import.
        :param import_from_id: The id of the existing SccManagementOrganizationSecurityHealthAnalyticsCustomModule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SccManagementOrganizationSecurityHealthAnalyticsCustomModule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab511a2a4d852758f55611c204d25d251831cd074fb2b029778e5b2879df21c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomConfig")
    def put_custom_config(
        self,
        *,
        predicate: typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        recommendation: builtins.str,
        resource_selector: typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#predicate SccManagementOrganizationSecurityHealthAnalyticsCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#recommendation SccManagementOrganizationSecurityHealthAnalyticsCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#resource_selector SccManagementOrganizationSecurityHealthAnalyticsCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#severity SccManagementOrganizationSecurityHealthAnalyticsCustomModule#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#custom_output SccManagementOrganizationSecurityHealthAnalyticsCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        '''
        value = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#create SccManagementOrganizationSecurityHealthAnalyticsCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#delete SccManagementOrganizationSecurityHealthAnalyticsCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#update SccManagementOrganizationSecurityHealthAnalyticsCustomModule#update}.
        '''
        value = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts(
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
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference":
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference", jsii.get(self, "customConfig"))

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
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference":
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="customConfigInput")
    def custom_config_input(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig"]:
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig"], jsii.get(self, "customConfigInput"))

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
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f166569fa0ce1c5babaf2a87673e1e7ffc2733b372e26de62bdae5fecf9a6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablementState")
    def enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementState"))

    @enablement_state.setter
    def enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d36633d0ec200b9917b040b8640809ac86541947de7c2801d8a1b883de85995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ecaf8d367103ee129f098abd2fe46caf36ba382ab21dd81529cb87d25a16d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ebecdd81578f24ad560298b703955f26153aa5cc4e544b9aedde9ca414179a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58946ca98cb5179b9b4421606881ea9b40dc1a9e669c3e889cf1053627ad47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "organization": "organization",
        "custom_config": "customConfig",
        "display_name": "displayName",
        "enablement_state": "enablementState",
        "id": "id",
        "location": "location",
        "timeouts": "timeouts",
    },
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleConfig(
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
        organization: builtins.str,
        custom_config: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enablement_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param organization: Numerical ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#organization SccManagementOrganizationSecurityHealthAnalyticsCustomModule#organization}
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#custom_config SccManagementOrganizationSecurityHealthAnalyticsCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#display_name SccManagementOrganizationSecurityHealthAnalyticsCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#enablement_state SccManagementOrganizationSecurityHealthAnalyticsCustomModule#enablement_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#id SccManagementOrganizationSecurityHealthAnalyticsCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: Location ID of the parent organization. If not provided, 'global' will be used as the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#timeouts SccManagementOrganizationSecurityHealthAnalyticsCustomModule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_config, dict):
            custom_config = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig(**custom_config)
        if isinstance(timeouts, dict):
            timeouts = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186824b47fce89303cdbc41352224093289af416cc0bf26929f6bda415a5664c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument custom_config", value=custom_config, expected_type=type_hints["custom_config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enablement_state", value=enablement_state, expected_type=type_hints["enablement_state"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "organization": organization,
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
    def organization(self) -> builtins.str:
        '''Numerical ID of the parent organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#organization SccManagementOrganizationSecurityHealthAnalyticsCustomModule#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_config(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig"]:
        '''custom_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#custom_config SccManagementOrganizationSecurityHealthAnalyticsCustomModule#custom_config}
        '''
        result = self._values.get("custom_config")
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Security Health Analytics custom module.

        This
        display name becomes the finding category for all findings that are
        returned by this custom module. The display name must be between 1 and
        128 characters, start with a lowercase letter, and contain alphanumeric
        characters or underscores only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#display_name SccManagementOrganizationSecurityHealthAnalyticsCustomModule#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enablement_state(self) -> typing.Optional[builtins.str]:
        '''The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#enablement_state SccManagementOrganizationSecurityHealthAnalyticsCustomModule#enablement_state}
        '''
        result = self._values.get("enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#id SccManagementOrganizationSecurityHealthAnalyticsCustomModule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location ID of the parent organization. If not provided, 'global' will be used as the default location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#timeouts SccManagementOrganizationSecurityHealthAnalyticsCustomModule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig",
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
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig:
    def __init__(
        self,
        *,
        predicate: typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        recommendation: builtins.str,
        resource_selector: typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#predicate SccManagementOrganizationSecurityHealthAnalyticsCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#recommendation SccManagementOrganizationSecurityHealthAnalyticsCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#resource_selector SccManagementOrganizationSecurityHealthAnalyticsCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#severity SccManagementOrganizationSecurityHealthAnalyticsCustomModule#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#custom_output SccManagementOrganizationSecurityHealthAnalyticsCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        '''
        if isinstance(predicate, dict):
            predicate = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(**predicate)
        if isinstance(resource_selector, dict):
            resource_selector = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(**resource_selector)
        if isinstance(custom_output, dict):
            custom_output = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(**custom_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d525965f00f96810f45b4d559d4912a9c7223cf0ba881c5066a44cfc552c48e0)
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
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate":
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#predicate SccManagementOrganizationSecurityHealthAnalyticsCustomModule#predicate}
        '''
        result = self._values.get("predicate")
        assert result is not None, "Required property 'predicate' is missing"
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate", result)

    @builtins.property
    def recommendation(self) -> builtins.str:
        '''An explanation of the recommended steps that security teams can take to resolve the detected issue.

        This explanation is returned with each finding generated by
        this module in the nextSteps property of the finding JSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#recommendation SccManagementOrganizationSecurityHealthAnalyticsCustomModule#recommendation}
        '''
        result = self._values.get("recommendation")
        assert result is not None, "Required property 'recommendation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_selector(
        self,
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector":
        '''resource_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#resource_selector SccManagementOrganizationSecurityHealthAnalyticsCustomModule#resource_selector}
        '''
        result = self._values.get("resource_selector")
        assert result is not None, "Required property 'resource_selector' is missing"
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector", result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#severity SccManagementOrganizationSecurityHealthAnalyticsCustomModule#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_output(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput"]:
        '''custom_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#custom_output SccManagementOrganizationSecurityHealthAnalyticsCustomModule#custom_output}
        '''
        result = self._values.get("custom_output")
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text that describes the vulnerability or misconfiguration that the custom module detects.

        This explanation is returned with each finding instance to
        help investigators understand the detected issue. The text must be enclosed in quotation marks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties"},
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput:
    def __init__(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#properties SccManagementOrganizationSecurityHealthAnalyticsCustomModule#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1923441eda58d9ccf79f8931b2de7899016848b8f3492f153b8000d68e8d4f)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#properties SccManagementOrganizationSecurityHealthAnalyticsCustomModule#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9f47dbfe1dfe47c520e3597e738064311d84ce0bf42376f36a58f486c88d210)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c431043184260f180374477890fab481eb0ee95892ac41d30010967f700b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList":
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties"]]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c852eccb64fca7a9481f63d06b3aca131517b022c2ac7719f85b017825469f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value_expression": "valueExpression"},
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value_expression: typing.Optional[typing.Union["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the property for the custom output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#name SccManagementOrganizationSecurityHealthAnalyticsCustomModule#name}
        :param value_expression: value_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#value_expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#value_expression}
        '''
        if isinstance(value_expression, dict):
            value_expression = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(**value_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b483142553c5726f257ad4e8bb6cd3ba3d61c2029829df88ddd00690643667)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#name SccManagementOrganizationSecurityHealthAnalyticsCustomModule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_expression(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        '''value_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#value_expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#value_expression}
        '''
        result = self._values.get("value_expression")
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8cfee6d1804566a292846fb27a55b1acdcfce2bf34c439edace3830f4a3ecf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eeace414ac734b52945674242da729aa244a8e757fa959529b6d99f554b75ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb2c6358daf7c9783cff879edf2eacb2a6c852ffd4f899ea6af90b43b073731)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8161fa0e1aeb7d41e58c225a3943ab32e2f111879969442d5460f9099c7770c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b969a3cb7ab3bfe47968b68b13e2e5ccb1ffef26dc870cb30382527a052993a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b7d0b458b979f841c8416a8a8f0c793da712a457f729827c02f7617552ec6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__400efd91f7708dc75de8e5b19dfb9afa483ca62eef1c7c7d3ceed4296f9356df)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#title SccManagementOrganizationSecurityHealthAnalyticsCustomModule#title}
        '''
        value = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(
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
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference":
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference", jsii.get(self, "valueExpression"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExpressionInput")
    def value_expression_input(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], jsii.get(self, "valueExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22067759beb467e274960800cb4fd7968ff5363f603d30ec8ed19c4db0c4d265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586bbbc436ff7193605fa3a650ffdf4445c8802f9d8e25822c909fffdb427a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#title SccManagementOrganizationSecurityHealthAnalyticsCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71609bd3da79fbb609a84228cc1ce4c7d802607f93e0a9bdcb6d3d73784889f0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#title SccManagementOrganizationSecurityHealthAnalyticsCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8394f7fb6ca7fe66382fc751960374d02ae4c7771ad59ece22fd42727beac942)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7867b8d558bcf9615c8b00b39ca846e408e52656900522627547e94767f52c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ca3dfc6c6dd34303c2e5d8c32c319da7817cb2ba941696a08633264a4d846c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca5e1982dfa2e2b9b0c8eca6cf1641e62619b90f68225f19ce6640a2a62f00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a661e18bb72c0a713afc22653be09a01e8ce7e5bd3a6275f7384eab3bfdec182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression]:
        return typing.cast(typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce043dbdd64e8369a19260bba81a036ba1acf0b708ef3f2f4a26f90807670290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f600411ddb35e3a11fafcaef8abc23a363d643ad9803900d3f577b479de58e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomOutput")
    def put_custom_output(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#properties SccManagementOrganizationSecurityHealthAnalyticsCustomModule#properties}
        '''
        value = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput(
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#title SccManagementOrganizationSecurityHealthAnalyticsCustomModule#title}
        '''
        value = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(
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
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#resource_types SccManagementOrganizationSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        value = SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(
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
    ) -> SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference:
        return typing.cast(SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference, jsii.get(self, "customOutput"))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference":
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelector")
    def resource_selector(
        self,
    ) -> "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference":
        return typing.cast("SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference", jsii.get(self, "resourceSelector"))

    @builtins.property
    @jsii.member(jsii_name="customOutputInput")
    def custom_output_input(
        self,
    ) -> typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput], jsii.get(self, "customOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"]:
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate"], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationInput")
    def recommendation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelectorInput")
    def resource_selector_input(
        self,
    ) -> typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"]:
        return typing.cast(typing.Optional["SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector"], jsii.get(self, "resourceSelectorInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cf1ef1380603d4050dc67b174ecba4e588284278fa000cab4e374850df7f868c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @recommendation.setter
    def recommendation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a24c075e4dadd398b43455fd9b6f6889da2ad68bddb2681463d6d7f3a74f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67756fd8e71332971b867286912a78fef1109e92c743f5efd7d796244aaadf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig]:
        return typing.cast(typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358d595c1bf4296003b0707e7f4deb4d848012bcface97b3fd04877adb7bcb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#title SccManagementOrganizationSecurityHealthAnalyticsCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578f3d14b671f7f74c45abb594d1455b05e6826baae8a689da8187c7dcc3f0a9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#expression SccManagementOrganizationSecurityHealthAnalyticsCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#description SccManagementOrganizationSecurityHealthAnalyticsCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#location SccManagementOrganizationSecurityHealthAnalyticsCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#title SccManagementOrganizationSecurityHealthAnalyticsCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f927824445b40e5b9a772db9dd0225ec91e66865457bdc9bd8d58b0f60ef20c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__753009f376faadda19d7e49eb8162f17c5bd8a07d880913d5ea7da7aad84f988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f235c6756785fb305d663168b45356d4d1784b697c38b8fb9b5d00df0b9822a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3ed4835ccfd646e5361fee3f02c5e79480219706af8a2e05cea5acde52bdff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498f04b685213fbe9c1c6d58aa4c8387dc236586b2a2a4b8b79b29ee6d9d6104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate]:
        return typing.cast(typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee259a0d40f05b5c4809eeeabc41beeb7fe133c3609f17511d9f9370eefb61cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector:
    def __init__(self, *, resource_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#resource_types SccManagementOrganizationSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b883b0e8fc910a3100fd554231923018f71809a4aeaed15a2bd72b7fe2eb5e48)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_types": resource_types,
        }

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''The resource types to run the detector on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#resource_types SccManagementOrganizationSecurityHealthAnalyticsCustomModule#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01219a86eb07c72800ee8617b158855019b0f08d9f1a7a216c7f29a93c88388)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4cfd8a82d9a0efab1ec4503c5b0180d29554b9ec1f86d681d877c3a33c5627b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector]:
        return typing.cast(typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e726ff2f95e474c63ea1f5443cebdfaacc3c8bb65258843de486a36cb226a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#create SccManagementOrganizationSecurityHealthAnalyticsCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#delete SccManagementOrganizationSecurityHealthAnalyticsCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#update SccManagementOrganizationSecurityHealthAnalyticsCustomModule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485e028e52ec8cb6e1e6ad760c1c7f02953d38a374429c56062d0e8751e24468)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#create SccManagementOrganizationSecurityHealthAnalyticsCustomModule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#delete SccManagementOrganizationSecurityHealthAnalyticsCustomModule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_management_organization_security_health_analytics_custom_module#update SccManagementOrganizationSecurityHealthAnalyticsCustomModule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccManagementOrganizationSecurityHealthAnalyticsCustomModule.SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35ab6d0218780662a12ca416e13873a1c9373ce22c8d3ca0cde14f2a6a104c7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da3dbb6268e5ed4a3810624eecbb55800108ac9f9854f5729ec24c0b0a4ed675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8128655e907906753ecd07959d73e7b8b4cce499365d8041ef4c5eac84ae89f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eef54998a1d8026dd6337c1c35bf1552ab57710a046ece3179939f25de358f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1525e0a13ce1790b7a506201ccceecafd92df04caa8cf8d8a193bb38af8f481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModule",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleConfig",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputOutputReference",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesList",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigOutputReference",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicateOutputReference",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelectorOutputReference",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts",
    "SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__271f6680a494e567ddf911110f007f0bdecbe5627bc0a65c49f78930c983c49d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    organization: builtins.str,
    custom_config: typing.Optional[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enablement_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ab511a2a4d852758f55611c204d25d251831cd074fb2b029778e5b2879df21c6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f166569fa0ce1c5babaf2a87673e1e7ffc2733b372e26de62bdae5fecf9a6ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d36633d0ec200b9917b040b8640809ac86541947de7c2801d8a1b883de85995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ecaf8d367103ee129f098abd2fe46caf36ba382ab21dd81529cb87d25a16d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ebecdd81578f24ad560298b703955f26153aa5cc4e544b9aedde9ca414179a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58946ca98cb5179b9b4421606881ea9b40dc1a9e669c3e889cf1053627ad47b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186824b47fce89303cdbc41352224093289af416cc0bf26929f6bda415a5664c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    organization: builtins.str,
    custom_config: typing.Optional[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enablement_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d525965f00f96810f45b4d559d4912a9c7223cf0ba881c5066a44cfc552c48e0(
    *,
    predicate: typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate, typing.Dict[builtins.str, typing.Any]],
    recommendation: builtins.str,
    resource_selector: typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
    severity: builtins.str,
    custom_output: typing.Optional[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1923441eda58d9ccf79f8931b2de7899016848b8f3492f153b8000d68e8d4f(
    *,
    properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f47dbfe1dfe47c520e3597e738064311d84ce0bf42376f36a58f486c88d210(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c431043184260f180374477890fab481eb0ee95892ac41d30010967f700b33(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c852eccb64fca7a9481f63d06b3aca131517b022c2ac7719f85b017825469f3(
    value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b483142553c5726f257ad4e8bb6cd3ba3d61c2029829df88ddd00690643667(
    *,
    name: typing.Optional[builtins.str] = None,
    value_expression: typing.Optional[typing.Union[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8cfee6d1804566a292846fb27a55b1acdcfce2bf34c439edace3830f4a3ecf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eeace414ac734b52945674242da729aa244a8e757fa959529b6d99f554b75ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb2c6358daf7c9783cff879edf2eacb2a6c852ffd4f899ea6af90b43b073731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8161fa0e1aeb7d41e58c225a3943ab32e2f111879969442d5460f9099c7770c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b969a3cb7ab3bfe47968b68b13e2e5ccb1ffef26dc870cb30382527a052993a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b7d0b458b979f841c8416a8a8f0c793da712a457f729827c02f7617552ec6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400efd91f7708dc75de8e5b19dfb9afa483ca62eef1c7c7d3ceed4296f9356df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22067759beb467e274960800cb4fd7968ff5363f603d30ec8ed19c4db0c4d265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586bbbc436ff7193605fa3a650ffdf4445c8802f9d8e25822c909fffdb427a28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputProperties]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71609bd3da79fbb609a84228cc1ce4c7d802607f93e0a9bdcb6d3d73784889f0(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8394f7fb6ca7fe66382fc751960374d02ae4c7771ad59ece22fd42727beac942(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7867b8d558bcf9615c8b00b39ca846e408e52656900522627547e94767f52c8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ca3dfc6c6dd34303c2e5d8c32c319da7817cb2ba941696a08633264a4d846c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca5e1982dfa2e2b9b0c8eca6cf1641e62619b90f68225f19ce6640a2a62f00a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a661e18bb72c0a713afc22653be09a01e8ce7e5bd3a6275f7384eab3bfdec182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce043dbdd64e8369a19260bba81a036ba1acf0b708ef3f2f4a26f90807670290(
    value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f600411ddb35e3a11fafcaef8abc23a363d643ad9803900d3f577b479de58e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1ef1380603d4050dc67b174ecba4e588284278fa000cab4e374850df7f868c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a24c075e4dadd398b43455fd9b6f6889da2ad68bddb2681463d6d7f3a74f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67756fd8e71332971b867286912a78fef1109e92c743f5efd7d796244aaadf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358d595c1bf4296003b0707e7f4deb4d848012bcface97b3fd04877adb7bcb71(
    value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578f3d14b671f7f74c45abb594d1455b05e6826baae8a689da8187c7dcc3f0a9(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f927824445b40e5b9a772db9dd0225ec91e66865457bdc9bd8d58b0f60ef20c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753009f376faadda19d7e49eb8162f17c5bd8a07d880913d5ea7da7aad84f988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f235c6756785fb305d663168b45356d4d1784b697c38b8fb9b5d00df0b9822a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3ed4835ccfd646e5361fee3f02c5e79480219706af8a2e05cea5acde52bdff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498f04b685213fbe9c1c6d58aa4c8387dc236586b2a2a4b8b79b29ee6d9d6104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee259a0d40f05b5c4809eeeabc41beeb7fe133c3609f17511d9f9370eefb61cb(
    value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b883b0e8fc910a3100fd554231923018f71809a4aeaed15a2bd72b7fe2eb5e48(
    *,
    resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01219a86eb07c72800ee8617b158855019b0f08d9f1a7a216c7f29a93c88388(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cfd8a82d9a0efab1ec4503c5b0180d29554b9ec1f86d681d877c3a33c5627b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e726ff2f95e474c63ea1f5443cebdfaacc3c8bb65258843de486a36cb226a3(
    value: typing.Optional[SccManagementOrganizationSecurityHealthAnalyticsCustomModuleCustomConfigResourceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485e028e52ec8cb6e1e6ad760c1c7f02953d38a374429c56062d0e8751e24468(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ab6d0218780662a12ca416e13873a1c9373ce22c8d3ca0cde14f2a6a104c7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3dbb6268e5ed4a3810624eecbb55800108ac9f9854f5729ec24c0b0a4ed675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8128655e907906753ecd07959d73e7b8b4cce499365d8041ef4c5eac84ae89f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eef54998a1d8026dd6337c1c35bf1552ab57710a046ece3179939f25de358f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1525e0a13ce1790b7a506201ccceecafd92df04caa8cf8d8a193bb38af8f481(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccManagementOrganizationSecurityHealthAnalyticsCustomModuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
