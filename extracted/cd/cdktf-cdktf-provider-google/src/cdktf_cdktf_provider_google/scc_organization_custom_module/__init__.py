r'''
# `google_scc_organization_custom_module`

Refer to the Terraform Registry for docs: [`google_scc_organization_custom_module`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module).
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


class SccOrganizationCustomModule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module google_scc_organization_custom_module}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        custom_config: typing.Union["SccOrganizationCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: builtins.str,
        enablement_state: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccOrganizationCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module google_scc_organization_custom_module} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#custom_config SccOrganizationCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#display_name SccOrganizationCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#enablement_state SccOrganizationCustomModule#enablement_state}
        :param organization: Numerical ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#organization SccOrganizationCustomModule#organization}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#id SccOrganizationCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#timeouts SccOrganizationCustomModule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64308c015b0dafdafc7eb734b8f9ed7cd6778fe511037a849bcc116ebdcc36e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SccOrganizationCustomModuleConfig(
            custom_config=custom_config,
            display_name=display_name,
            enablement_state=enablement_state,
            organization=organization,
            id=id,
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
        '''Generates CDKTF code for importing a SccOrganizationCustomModule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SccOrganizationCustomModule to import.
        :param import_from_id: The id of the existing SccOrganizationCustomModule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SccOrganizationCustomModule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714e03835f817743d7dc54bb3d0d74a3c55b75c3ee5453e093d8d1cf590a0e3e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomConfig")
    def put_custom_config(
        self,
        *,
        predicate: typing.Union["SccOrganizationCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        recommendation: builtins.str,
        resource_selector: typing.Union["SccOrganizationCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SccOrganizationCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#predicate SccOrganizationCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#recommendation SccOrganizationCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#resource_selector SccOrganizationCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#severity SccOrganizationCustomModule#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#custom_output SccOrganizationCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        '''
        value = SccOrganizationCustomModuleCustomConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#create SccOrganizationCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#delete SccOrganizationCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#update SccOrganizationCustomModule#update}.
        '''
        value = SccOrganizationCustomModuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    def custom_config(self) -> "SccOrganizationCustomModuleCustomConfigOutputReference":
        return typing.cast("SccOrganizationCustomModuleCustomConfigOutputReference", jsii.get(self, "customConfig"))

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
    def timeouts(self) -> "SccOrganizationCustomModuleTimeoutsOutputReference":
        return typing.cast("SccOrganizationCustomModuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="customConfigInput")
    def custom_config_input(
        self,
    ) -> typing.Optional["SccOrganizationCustomModuleCustomConfig"]:
        return typing.cast(typing.Optional["SccOrganizationCustomModuleCustomConfig"], jsii.get(self, "customConfigInput"))

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
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccOrganizationCustomModuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SccOrganizationCustomModuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982e186ba6d8bc958bbc7ade90c93b4a3f4d7b9220ec202389d7a618e07aa77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablementState")
    def enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementState"))

    @enablement_state.setter
    def enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b638b426526ad425fd1c9bb4505ef78801850bdb66d9404e0a2e62ac7d3d07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84cf91601b87250fd7c02d75838d1ff5fb5ccf517e1e7d3e8f69143e5d883cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0ea3c0aa11e473267967b3404a8ce9e0153c772ee8a9e75e2d6032d9a2c10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleConfig",
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
        "organization": "organization",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class SccOrganizationCustomModuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_config: typing.Union["SccOrganizationCustomModuleCustomConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: builtins.str,
        enablement_state: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SccOrganizationCustomModuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_config: custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#custom_config SccOrganizationCustomModule#custom_config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. The display name must be between 1 and 128 characters, start with a lowercase letter, and contain alphanumeric characters or underscores only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#display_name SccOrganizationCustomModule#display_name}
        :param enablement_state: The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#enablement_state SccOrganizationCustomModule#enablement_state}
        :param organization: Numerical ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#organization SccOrganizationCustomModule#organization}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#id SccOrganizationCustomModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#timeouts SccOrganizationCustomModule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_config, dict):
            custom_config = SccOrganizationCustomModuleCustomConfig(**custom_config)
        if isinstance(timeouts, dict):
            timeouts = SccOrganizationCustomModuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca141a49d6d68dd3e56f399d7e07332c2907a3cde915658e772cca39c3e03c3)
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
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_config": custom_config,
            "display_name": display_name,
            "enablement_state": enablement_state,
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
        if id is not None:
            self._values["id"] = id
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
    def custom_config(self) -> "SccOrganizationCustomModuleCustomConfig":
        '''custom_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#custom_config SccOrganizationCustomModule#custom_config}
        '''
        result = self._values.get("custom_config")
        assert result is not None, "Required property 'custom_config' is missing"
        return typing.cast("SccOrganizationCustomModuleCustomConfig", result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the Security Health Analytics custom module.

        This
        display name becomes the finding category for all findings that are
        returned by this custom module. The display name must be between 1 and
        128 characters, start with a lowercase letter, and contain alphanumeric
        characters or underscores only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#display_name SccOrganizationCustomModule#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enablement_state(self) -> builtins.str:
        '''The enablement state of the custom module. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#enablement_state SccOrganizationCustomModule#enablement_state}
        '''
        result = self._values.get("enablement_state")
        assert result is not None, "Required property 'enablement_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Numerical ID of the parent organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#organization SccOrganizationCustomModule#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#id SccOrganizationCustomModule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SccOrganizationCustomModuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#timeouts SccOrganizationCustomModule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SccOrganizationCustomModuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfig",
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
class SccOrganizationCustomModuleCustomConfig:
    def __init__(
        self,
        *,
        predicate: typing.Union["SccOrganizationCustomModuleCustomConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        recommendation: builtins.str,
        resource_selector: typing.Union["SccOrganizationCustomModuleCustomConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SccOrganizationCustomModuleCustomConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#predicate SccOrganizationCustomModule#predicate}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. This explanation is returned with each finding generated by this module in the nextSteps property of the finding JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#recommendation SccOrganizationCustomModule#recommendation}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#resource_selector SccOrganizationCustomModule#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#severity SccOrganizationCustomModule#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#custom_output SccOrganizationCustomModule#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. This explanation is returned with each finding instance to help investigators understand the detected issue. The text must be enclosed in quotation marks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        '''
        if isinstance(predicate, dict):
            predicate = SccOrganizationCustomModuleCustomConfigPredicate(**predicate)
        if isinstance(resource_selector, dict):
            resource_selector = SccOrganizationCustomModuleCustomConfigResourceSelector(**resource_selector)
        if isinstance(custom_output, dict):
            custom_output = SccOrganizationCustomModuleCustomConfigCustomOutput(**custom_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4762f90b21eed230b606fb0d95c540221e57a5a56f4c62b2a6a61bdd0788e2b8)
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
    def predicate(self) -> "SccOrganizationCustomModuleCustomConfigPredicate":
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#predicate SccOrganizationCustomModule#predicate}
        '''
        result = self._values.get("predicate")
        assert result is not None, "Required property 'predicate' is missing"
        return typing.cast("SccOrganizationCustomModuleCustomConfigPredicate", result)

    @builtins.property
    def recommendation(self) -> builtins.str:
        '''An explanation of the recommended steps that security teams can take to resolve the detected issue.

        This explanation is returned with each finding generated by
        this module in the nextSteps property of the finding JSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#recommendation SccOrganizationCustomModule#recommendation}
        '''
        result = self._values.get("recommendation")
        assert result is not None, "Required property 'recommendation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_selector(
        self,
    ) -> "SccOrganizationCustomModuleCustomConfigResourceSelector":
        '''resource_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#resource_selector SccOrganizationCustomModule#resource_selector}
        '''
        result = self._values.get("resource_selector")
        assert result is not None, "Required property 'resource_selector' is missing"
        return typing.cast("SccOrganizationCustomModuleCustomConfigResourceSelector", result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''The severity to assign to findings generated by the module. Possible values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#severity SccOrganizationCustomModule#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_output(
        self,
    ) -> typing.Optional["SccOrganizationCustomModuleCustomConfigCustomOutput"]:
        '''custom_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#custom_output SccOrganizationCustomModule#custom_output}
        '''
        result = self._values.get("custom_output")
        return typing.cast(typing.Optional["SccOrganizationCustomModuleCustomConfigCustomOutput"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text that describes the vulnerability or misconfiguration that the custom module detects.

        This explanation is returned with each finding instance to
        help investigators understand the detected issue. The text must be enclosed in quotation marks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutput",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties"},
)
class SccOrganizationCustomModuleCustomConfigCustomOutput:
    def __init__(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccOrganizationCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#properties SccOrganizationCustomModule#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db202a608d5fa04673e055d09c672cf9153e7d3e3353a9a32bf382e8b31c87e)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccOrganizationCustomModuleCustomConfigCustomOutputProperties"]]]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#properties SccOrganizationCustomModule#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccOrganizationCustomModuleCustomConfigCustomOutputProperties"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleCustomConfigCustomOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccOrganizationCustomModuleCustomConfigCustomOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d6c459fc4b5397533d4977eb1330bb3a323d10036d911ba205ca990922274f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SccOrganizationCustomModuleCustomConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1667251f7fa1351d81092c1980c6e5f429a730abd272f080ca25c4380c51be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesList":
        return typing.cast("SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccOrganizationCustomModuleCustomConfigCustomOutputProperties"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SccOrganizationCustomModuleCustomConfigCustomOutputProperties"]]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9e3a20d2fcbabbefc8e32a24d4ebdc74dfb28407ca971d56848eee2dcee9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutputProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value_expression": "valueExpression"},
)
class SccOrganizationCustomModuleCustomConfigCustomOutputProperties:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value_expression: typing.Optional[typing.Union["SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the property for the custom output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#name SccOrganizationCustomModule#name}
        :param value_expression: value_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#value_expression SccOrganizationCustomModule#value_expression}
        '''
        if isinstance(value_expression, dict):
            value_expression = SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression(**value_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb32a939a802352bd95cf3d1e3a9842dc5def90a0b8991219c7fc88427cc7f0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#name SccOrganizationCustomModule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_expression(
        self,
    ) -> typing.Optional["SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        '''value_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#value_expression SccOrganizationCustomModule#value_expression}
        '''
        result = self._values.get("value_expression")
        return typing.cast(typing.Optional["SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleCustomConfigCustomOutputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd2a5d34cd92ed0eccc1e1b96d83cd97933cd2a2e3550f595441f3c859f28953)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f09e84cec69cc50f5c9997a2dedf9866d39310346c632c0b3d0b1b86e9cd54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9fd356ec9160fcc02317c2ce9142b992c53f8e0ef33d40cc387449ddd754a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4781a2beb20fb94e343905878419c0c5f4f9a3a9fbaf7630d4be7719c6c85c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec21de57f9427443a61d6e1e644b0cb800634ec5cdf936c33d06359dfc0d40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccOrganizationCustomModuleCustomConfigCustomOutputProperties]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccOrganizationCustomModuleCustomConfigCustomOutputProperties]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccOrganizationCustomModuleCustomConfigCustomOutputProperties]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de23dbd6a53759e52d3f6b1964821e37d3aa82b39486950cc7acbd4332cd80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f64621a557a8466a21bed1dff3d2e60e1f64bf47b195ca19f9dd180bb71f3588)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#expression SccOrganizationCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#location SccOrganizationCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#title SccOrganizationCustomModule#title}
        '''
        value = SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression(
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
    ) -> "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference":
        return typing.cast("SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference", jsii.get(self, "valueExpression"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExpressionInput")
    def value_expression_input(
        self,
    ) -> typing.Optional["SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression"]:
        return typing.cast(typing.Optional["SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression"], jsii.get(self, "valueExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fdb3cf6ab105db63a660d1ff29a64c2f14098807401e929f02bf3d6eb7cd7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleCustomConfigCustomOutputProperties]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleCustomConfigCustomOutputProperties]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleCustomConfigCustomOutputProperties]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6ab10146ac0fb0fbc42602f710b54f816011acafc87521ff1f12eb7f66937d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#expression SccOrganizationCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#location SccOrganizationCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#title SccOrganizationCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858390cd54acd9fa20d1395971e1dae775f986b608d95ab39da06c82b9e5444e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#expression SccOrganizationCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#location SccOrganizationCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#title SccOrganizationCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1add531551940ab3f2239be94bee994927bc2a017957f1de36c60f319ddb55cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aadf2663d5bcd321be483be060fa81545c31b8ae1beffd9f299b8cf610720ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67aaa242ea86ef786089fc8db1fc849c63d77cacd7c6c832bd48489ce6c96d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0990c5761bb39645abdde458069f2cbb6e5ffb486dc1766e8b2a99f61e291e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ec980230301eb70f05a0101bc4f7741644fc9845fbb6c6bcd886c192eed15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression]:
        return typing.cast(typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9266e883696c75e2a86114c5837f42ed461a7400b68787249cb5712a8f1ec32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SccOrganizationCustomModuleCustomConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e21890d088324a57ead43d6340c4aa33270b45dbcbad10a29d56c0f18e125f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomOutput")
    def put_custom_output(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccOrganizationCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#properties SccOrganizationCustomModule#properties}
        '''
        value = SccOrganizationCustomModuleCustomConfigCustomOutput(
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#expression SccOrganizationCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#location SccOrganizationCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#title SccOrganizationCustomModule#title}
        '''
        value = SccOrganizationCustomModuleCustomConfigPredicate(
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
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#resource_types SccOrganizationCustomModule#resource_types}
        '''
        value = SccOrganizationCustomModuleCustomConfigResourceSelector(
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
    ) -> SccOrganizationCustomModuleCustomConfigCustomOutputOutputReference:
        return typing.cast(SccOrganizationCustomModuleCustomConfigCustomOutputOutputReference, jsii.get(self, "customOutput"))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "SccOrganizationCustomModuleCustomConfigPredicateOutputReference":
        return typing.cast("SccOrganizationCustomModuleCustomConfigPredicateOutputReference", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelector")
    def resource_selector(
        self,
    ) -> "SccOrganizationCustomModuleCustomConfigResourceSelectorOutputReference":
        return typing.cast("SccOrganizationCustomModuleCustomConfigResourceSelectorOutputReference", jsii.get(self, "resourceSelector"))

    @builtins.property
    @jsii.member(jsii_name="customOutputInput")
    def custom_output_input(
        self,
    ) -> typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutput]:
        return typing.cast(typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutput], jsii.get(self, "customOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional["SccOrganizationCustomModuleCustomConfigPredicate"]:
        return typing.cast(typing.Optional["SccOrganizationCustomModuleCustomConfigPredicate"], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationInput")
    def recommendation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelectorInput")
    def resource_selector_input(
        self,
    ) -> typing.Optional["SccOrganizationCustomModuleCustomConfigResourceSelector"]:
        return typing.cast(typing.Optional["SccOrganizationCustomModuleCustomConfigResourceSelector"], jsii.get(self, "resourceSelectorInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b85351d5f4cd6966f478ed9deafc887aea061fa9938c6ad4d5e8e07c98badf1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @recommendation.setter
    def recommendation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bccf053c72a35851f674d648943a4ad5ff89b70c1ad5e56217e2a0988f0e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37c7b7e62d3f2045e86a6bbece3857c105380e2ad11594ef0e9484479f9fb16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccOrganizationCustomModuleCustomConfig]:
        return typing.cast(typing.Optional[SccOrganizationCustomModuleCustomConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccOrganizationCustomModuleCustomConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d577935bd4775d35da319bfb487e6e728884b7e25ec9186a24d41c7b2dddf71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigPredicate",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SccOrganizationCustomModuleCustomConfigPredicate:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#expression SccOrganizationCustomModule#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#location SccOrganizationCustomModule#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#title SccOrganizationCustomModule#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bffb70e60f5c4ed380b54df2e67a36bb0f87ac5e7a45a11c0185367b8c10c5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#expression SccOrganizationCustomModule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the
        expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#description SccOrganizationCustomModule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#location SccOrganizationCustomModule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#title SccOrganizationCustomModule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleCustomConfigPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccOrganizationCustomModuleCustomConfigPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9fc1e0b0843407b6688cfc729e19f2382906f49c3a095956c88a988c32403ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__595672c7ede8d29f7a5ce046dfec34346a99d5a52ef30d5c7f2aa4efa12c8b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed103a8a7728c06e38a45d5d1bf01dcefb2794681ddbe37253fa291e732f0e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc9b6ec1504c4ebde52a2558d686e684fe3d7732a1ed6559834a03381820035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e569b7c5b4fdc5ebba84a46d72986156fb9c616f66212fdb6f93626787af7cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccOrganizationCustomModuleCustomConfigPredicate]:
        return typing.cast(typing.Optional[SccOrganizationCustomModuleCustomConfigPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccOrganizationCustomModuleCustomConfigPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e1a5afa52f0eb1236a7a4931acdaf3703fa567ce649952a3aae87b072db295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigResourceSelector",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class SccOrganizationCustomModuleCustomConfigResourceSelector:
    def __init__(self, *, resource_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#resource_types SccOrganizationCustomModule#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83c8906c31d2cbe39a8926faa91128c558e624b6380d1269d6ca56164da8a21)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_types": resource_types,
        }

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''The resource types to run the detector on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#resource_types SccOrganizationCustomModule#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleCustomConfigResourceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccOrganizationCustomModuleCustomConfigResourceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleCustomConfigResourceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67d2547d44e6284ffd133ebe08707d705ee2909976f4ce6bdc28b834fb4fbdaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0241337756961551ef943d02f8df9dea21434277bfb55e3e42709c52d4c194fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SccOrganizationCustomModuleCustomConfigResourceSelector]:
        return typing.cast(typing.Optional[SccOrganizationCustomModuleCustomConfigResourceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SccOrganizationCustomModuleCustomConfigResourceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4127ee711e204bd28ffd20c96985f03871c770ef8bbc8efdb94b0dc7b552c11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SccOrganizationCustomModuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#create SccOrganizationCustomModule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#delete SccOrganizationCustomModule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#update SccOrganizationCustomModule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a86b1430b55e704acbfac48ac5f2d5d046433632e95569a3c46a837445f4e2e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#create SccOrganizationCustomModule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#delete SccOrganizationCustomModule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/scc_organization_custom_module#update SccOrganizationCustomModule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SccOrganizationCustomModuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SccOrganizationCustomModuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sccOrganizationCustomModule.SccOrganizationCustomModuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06bbcf9cbe53df80b7bba116a0dca1d787b855d7c511877bd81cf31bca2fa7fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__318f7fc54137fa628b9289759670d18b38f74951acf2408c3b3428ae22f7ede5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03c18005093105544fdf8567bec7f444a11af2115c0e934ee787ba55194cde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f8d713b32b15a11b09ad383083a9952df5cc0fbfb2106727d9a1203eabe088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22e3c90bbd2954211d68dfc6064328d38592eb241e353ad72a644f1faf7fcac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SccOrganizationCustomModule",
    "SccOrganizationCustomModuleConfig",
    "SccOrganizationCustomModuleCustomConfig",
    "SccOrganizationCustomModuleCustomConfigCustomOutput",
    "SccOrganizationCustomModuleCustomConfigCustomOutputOutputReference",
    "SccOrganizationCustomModuleCustomConfigCustomOutputProperties",
    "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesList",
    "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesOutputReference",
    "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression",
    "SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpressionOutputReference",
    "SccOrganizationCustomModuleCustomConfigOutputReference",
    "SccOrganizationCustomModuleCustomConfigPredicate",
    "SccOrganizationCustomModuleCustomConfigPredicateOutputReference",
    "SccOrganizationCustomModuleCustomConfigResourceSelector",
    "SccOrganizationCustomModuleCustomConfigResourceSelectorOutputReference",
    "SccOrganizationCustomModuleTimeouts",
    "SccOrganizationCustomModuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__64308c015b0dafdafc7eb734b8f9ed7cd6778fe511037a849bcc116ebdcc36e3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    custom_config: typing.Union[SccOrganizationCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]],
    display_name: builtins.str,
    enablement_state: builtins.str,
    organization: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccOrganizationCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__714e03835f817743d7dc54bb3d0d74a3c55b75c3ee5453e093d8d1cf590a0e3e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982e186ba6d8bc958bbc7ade90c93b4a3f4d7b9220ec202389d7a618e07aa77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b638b426526ad425fd1c9bb4505ef78801850bdb66d9404e0a2e62ac7d3d07d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cf91601b87250fd7c02d75838d1ff5fb5ccf517e1e7d3e8f69143e5d883cde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0ea3c0aa11e473267967b3404a8ce9e0153c772ee8a9e75e2d6032d9a2c10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca141a49d6d68dd3e56f399d7e07332c2907a3cde915658e772cca39c3e03c3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_config: typing.Union[SccOrganizationCustomModuleCustomConfig, typing.Dict[builtins.str, typing.Any]],
    display_name: builtins.str,
    enablement_state: builtins.str,
    organization: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SccOrganizationCustomModuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4762f90b21eed230b606fb0d95c540221e57a5a56f4c62b2a6a61bdd0788e2b8(
    *,
    predicate: typing.Union[SccOrganizationCustomModuleCustomConfigPredicate, typing.Dict[builtins.str, typing.Any]],
    recommendation: builtins.str,
    resource_selector: typing.Union[SccOrganizationCustomModuleCustomConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
    severity: builtins.str,
    custom_output: typing.Optional[typing.Union[SccOrganizationCustomModuleCustomConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db202a608d5fa04673e055d09c672cf9153e7d3e3353a9a32bf382e8b31c87e(
    *,
    properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccOrganizationCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6c459fc4b5397533d4977eb1330bb3a323d10036d911ba205ca990922274f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1667251f7fa1351d81092c1980c6e5f429a730abd272f080ca25c4380c51be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SccOrganizationCustomModuleCustomConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9e3a20d2fcbabbefc8e32a24d4ebdc74dfb28407ca971d56848eee2dcee9de(
    value: typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb32a939a802352bd95cf3d1e3a9842dc5def90a0b8991219c7fc88427cc7f0(
    *,
    name: typing.Optional[builtins.str] = None,
    value_expression: typing.Optional[typing.Union[SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2a5d34cd92ed0eccc1e1b96d83cd97933cd2a2e3550f595441f3c859f28953(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f09e84cec69cc50f5c9997a2dedf9866d39310346c632c0b3d0b1b86e9cd54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9fd356ec9160fcc02317c2ce9142b992c53f8e0ef33d40cc387449ddd754a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4781a2beb20fb94e343905878419c0c5f4f9a3a9fbaf7630d4be7719c6c85c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec21de57f9427443a61d6e1e644b0cb800634ec5cdf936c33d06359dfc0d40e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de23dbd6a53759e52d3f6b1964821e37d3aa82b39486950cc7acbd4332cd80d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SccOrganizationCustomModuleCustomConfigCustomOutputProperties]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64621a557a8466a21bed1dff3d2e60e1f64bf47b195ca19f9dd180bb71f3588(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fdb3cf6ab105db63a660d1ff29a64c2f14098807401e929f02bf3d6eb7cd7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6ab10146ac0fb0fbc42602f710b54f816011acafc87521ff1f12eb7f66937d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleCustomConfigCustomOutputProperties]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858390cd54acd9fa20d1395971e1dae775f986b608d95ab39da06c82b9e5444e(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1add531551940ab3f2239be94bee994927bc2a017957f1de36c60f319ddb55cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadf2663d5bcd321be483be060fa81545c31b8ae1beffd9f299b8cf610720ba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67aaa242ea86ef786089fc8db1fc849c63d77cacd7c6c832bd48489ce6c96d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0990c5761bb39645abdde458069f2cbb6e5ffb486dc1766e8b2a99f61e291e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ec980230301eb70f05a0101bc4f7741644fc9845fbb6c6bcd886c192eed15b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9266e883696c75e2a86114c5837f42ed461a7400b68787249cb5712a8f1ec32(
    value: typing.Optional[SccOrganizationCustomModuleCustomConfigCustomOutputPropertiesValueExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e21890d088324a57ead43d6340c4aa33270b45dbcbad10a29d56c0f18e125f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85351d5f4cd6966f478ed9deafc887aea061fa9938c6ad4d5e8e07c98badf1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bccf053c72a35851f674d648943a4ad5ff89b70c1ad5e56217e2a0988f0e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37c7b7e62d3f2045e86a6bbece3857c105380e2ad11594ef0e9484479f9fb16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d577935bd4775d35da319bfb487e6e728884b7e25ec9186a24d41c7b2dddf71(
    value: typing.Optional[SccOrganizationCustomModuleCustomConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bffb70e60f5c4ed380b54df2e67a36bb0f87ac5e7a45a11c0185367b8c10c5(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fc1e0b0843407b6688cfc729e19f2382906f49c3a095956c88a988c32403ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595672c7ede8d29f7a5ce046dfec34346a99d5a52ef30d5c7f2aa4efa12c8b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed103a8a7728c06e38a45d5d1bf01dcefb2794681ddbe37253fa291e732f0e3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc9b6ec1504c4ebde52a2558d686e684fe3d7732a1ed6559834a03381820035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e569b7c5b4fdc5ebba84a46d72986156fb9c616f66212fdb6f93626787af7cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e1a5afa52f0eb1236a7a4931acdaf3703fa567ce649952a3aae87b072db295(
    value: typing.Optional[SccOrganizationCustomModuleCustomConfigPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83c8906c31d2cbe39a8926faa91128c558e624b6380d1269d6ca56164da8a21(
    *,
    resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d2547d44e6284ffd133ebe08707d705ee2909976f4ce6bdc28b834fb4fbdaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0241337756961551ef943d02f8df9dea21434277bfb55e3e42709c52d4c194fc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4127ee711e204bd28ffd20c96985f03871c770ef8bbc8efdb94b0dc7b552c11c(
    value: typing.Optional[SccOrganizationCustomModuleCustomConfigResourceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a86b1430b55e704acbfac48ac5f2d5d046433632e95569a3c46a837445f4e2e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bbcf9cbe53df80b7bba116a0dca1d787b855d7c511877bd81cf31bca2fa7fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318f7fc54137fa628b9289759670d18b38f74951acf2408c3b3428ae22f7ede5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03c18005093105544fdf8567bec7f444a11af2115c0e934ee787ba55194cde2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f8d713b32b15a11b09ad383083a9952df5cc0fbfb2106727d9a1203eabe088(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22e3c90bbd2954211d68dfc6064328d38592eb241e353ad72a644f1faf7fcac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SccOrganizationCustomModuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
