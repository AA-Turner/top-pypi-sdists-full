r'''
# `google_data_loss_prevention_discovery_config`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_discovery_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config).
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


class GoogleDataLossPreventionDiscoveryConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config google_data_loss_prevention_discovery_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        parent: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_config: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigOrgConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config google_data_loss_prevention_discovery_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location to create the discovery config in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#location GoogleDataLossPreventionDiscoveryConfig#location}
        :param parent: The parent of the discovery config in any of the following formats:. - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#parent GoogleDataLossPreventionDiscoveryConfig#parent}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#actions GoogleDataLossPreventionDiscoveryConfig#actions}
        :param display_name: Display Name (max 1000 Chars). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#display_name GoogleDataLossPreventionDiscoveryConfig#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#id GoogleDataLossPreventionDiscoveryConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_templates: Detection logic for profile generation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_templates GoogleDataLossPreventionDiscoveryConfig#inspect_templates}
        :param org_config: org_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#org_config GoogleDataLossPreventionDiscoveryConfig#org_config}
        :param status: Required. A status for this configuration Possible values: ["RUNNING", "PAUSED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#status GoogleDataLossPreventionDiscoveryConfig#status}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#targets GoogleDataLossPreventionDiscoveryConfig#targets}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#timeouts GoogleDataLossPreventionDiscoveryConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17017175cbbef6972d623750c69242c970f50dbb50c2940e1de991c8c2b72a4d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataLossPreventionDiscoveryConfigConfig(
            location=location,
            parent=parent,
            actions=actions,
            display_name=display_name,
            id=id,
            inspect_templates=inspect_templates,
            org_config=org_config,
            status=status,
            targets=targets,
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
        '''Generates CDKTF code for importing a GoogleDataLossPreventionDiscoveryConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataLossPreventionDiscoveryConfig to import.
        :param import_from_id: The id of the existing GoogleDataLossPreventionDiscoveryConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataLossPreventionDiscoveryConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396bf6890e8f32ee43377e279335bb63c222c870c500376ac777701791d46700)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025dc68f8d8e990f8256577d65d9e0ebf194d23252a9d3ec1bafafab8140b5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putOrgConfig")
    def put_org_config(
        self,
        *,
        location: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#location GoogleDataLossPreventionDiscoveryConfig#location}
        :param project_id: The project that will run the scan. The DLP service account that exists within this project must have access to all resources that are profiled, and the cloud DLP API must be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigOrgConfig(
            location=location, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putOrgConfig", [value]))

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2688ad8e96b3ede07d4fb752a13f993f5682af1bdf5c6db1b120aa56d79d7251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#create GoogleDataLossPreventionDiscoveryConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#delete GoogleDataLossPreventionDiscoveryConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#update GoogleDataLossPreventionDiscoveryConfig#update}.
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInspectTemplates")
    def reset_inspect_templates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplates", []))

    @jsii.member(jsii_name="resetOrgConfig")
    def reset_org_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgConfig", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTargets")
    def reset_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargets", []))

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> "GoogleDataLossPreventionDiscoveryConfigActionsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsList", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="errors")
    def errors(self) -> "GoogleDataLossPreventionDiscoveryConfigErrorsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigErrorsList", jsii.get(self, "errors"))

    @builtins.property
    @jsii.member(jsii_name="lastRunTime")
    def last_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastRunTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="orgConfig")
    def org_config(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigOrgConfigOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigOrgConfigOutputReference", jsii.get(self, "orgConfig"))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "GoogleDataLossPreventionDiscoveryConfigTargetsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTimeoutsOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActions"]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplatesInput")
    def inspect_templates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inspectTemplatesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="orgConfigInput")
    def org_config_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigOrgConfig"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigOrgConfig"], jsii.get(self, "orgConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionDiscoveryConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionDiscoveryConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d20a8ce0b992d592ffa03b5e58355b5e04e5bf843981974529b64e52e34d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4ee45e7051891ae8c4ac546dd267d354b294647945768b5ab7a8c137e6d995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplates")
    def inspect_templates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inspectTemplates"))

    @inspect_templates.setter
    def inspect_templates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1731eeceebecbbf7f6ba238bda4f756462fa3d63f4865aacdac5b33c97664c04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2503974cb27d7856acbf9178314ea5ad136d297f776f02cccd77ec08658b90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa13cb30a97a943fe4930faa021be5942702eb685bf2ab8d0a4315e788843de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a2d62b500a92dec261ce2bef4beb945903f099fc3363de99352e9dcca59686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActions",
    jsii_struct_bases=[],
    name_mapping={
        "export_data": "exportData",
        "pub_sub_notification": "pubSubNotification",
        "tag_resources": "tagResources",
    },
)
class GoogleDataLossPreventionDiscoveryConfigActions:
    def __init__(
        self,
        *,
        export_data: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsExportData", typing.Dict[builtins.str, typing.Any]]] = None,
        pub_sub_notification: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_resources: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsTagResources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param export_data: export_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#export_data GoogleDataLossPreventionDiscoveryConfig#export_data}
        :param pub_sub_notification: pub_sub_notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#pub_sub_notification GoogleDataLossPreventionDiscoveryConfig#pub_sub_notification}
        :param tag_resources: tag_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag_resources GoogleDataLossPreventionDiscoveryConfig#tag_resources}
        '''
        if isinstance(export_data, dict):
            export_data = GoogleDataLossPreventionDiscoveryConfigActionsExportData(**export_data)
        if isinstance(pub_sub_notification, dict):
            pub_sub_notification = GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification(**pub_sub_notification)
        if isinstance(tag_resources, dict):
            tag_resources = GoogleDataLossPreventionDiscoveryConfigActionsTagResources(**tag_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027e9ea63e657620bea93ba5742d1f1bd90598b2bb40b10dabced1b2cdfac788)
            check_type(argname="argument export_data", value=export_data, expected_type=type_hints["export_data"])
            check_type(argname="argument pub_sub_notification", value=pub_sub_notification, expected_type=type_hints["pub_sub_notification"])
            check_type(argname="argument tag_resources", value=tag_resources, expected_type=type_hints["tag_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if export_data is not None:
            self._values["export_data"] = export_data
        if pub_sub_notification is not None:
            self._values["pub_sub_notification"] = pub_sub_notification
        if tag_resources is not None:
            self._values["tag_resources"] = tag_resources

    @builtins.property
    def export_data(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsExportData"]:
        '''export_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#export_data GoogleDataLossPreventionDiscoveryConfig#export_data}
        '''
        result = self._values.get("export_data")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsExportData"], result)

    @builtins.property
    def pub_sub_notification(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification"]:
        '''pub_sub_notification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#pub_sub_notification GoogleDataLossPreventionDiscoveryConfig#pub_sub_notification}
        '''
        result = self._values.get("pub_sub_notification")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification"], result)

    @builtins.property
    def tag_resources(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResources"]:
        '''tag_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag_resources GoogleDataLossPreventionDiscoveryConfig#tag_resources}
        '''
        result = self._values.get("tag_resources")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResources"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsExportData",
    jsii_struct_bases=[],
    name_mapping={"profile_table": "profileTable"},
)
class GoogleDataLossPreventionDiscoveryConfigActionsExportData:
    def __init__(
        self,
        *,
        profile_table: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param profile_table: profile_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#profile_table GoogleDataLossPreventionDiscoveryConfig#profile_table}
        '''
        if isinstance(profile_table, dict):
            profile_table = GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable(**profile_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605398ab72b03d1be3597aa5511c6606bd671e7f0f219b4750ff79c3e14d6cd3)
            check_type(argname="argument profile_table", value=profile_table, expected_type=type_hints["profile_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if profile_table is not None:
            self._values["profile_table"] = profile_table

    @builtins.property
    def profile_table(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable"]:
        '''profile_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#profile_table GoogleDataLossPreventionDiscoveryConfig#profile_table}
        '''
        result = self._values.get("profile_table")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsExportData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsExportDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsExportDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b916796605b608851182ce08f0a38366a51c4ba3f27693fe4dff49a0f7ffa208)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProfileTable")
    def put_profile_table(
        self,
        *,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset Id of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id GoogleDataLossPreventionDiscoveryConfig#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. If omitted, the project ID is inferred from the API call. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        :param table_id: Name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id GoogleDataLossPreventionDiscoveryConfig#table_id}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putProfileTable", [value]))

    @jsii.member(jsii_name="resetProfileTable")
    def reset_profile_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileTable", []))

    @builtins.property
    @jsii.member(jsii_name="profileTable")
    def profile_table(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference", jsii.get(self, "profileTable"))

    @builtins.property
    @jsii.member(jsii_name="profileTableInput")
    def profile_table_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable"], jsii.get(self, "profileTableInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportData]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a0296fb6b0e074d1d3b66f09b976e1b2e69aa61bc18eb3d28688fb17988f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable:
    def __init__(
        self,
        *,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset Id of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id GoogleDataLossPreventionDiscoveryConfig#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. If omitted, the project ID is inferred from the API call. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        :param table_id: Name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id GoogleDataLossPreventionDiscoveryConfig#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5abf469657807d1956c463be195ee28585c443cf949c9424cc6bebe00e3042)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id
        if table_id is not None:
            self._values["table_id"] = table_id

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''Dataset Id of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id GoogleDataLossPreventionDiscoveryConfig#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform project ID of the project containing the table.

        If omitted, the project ID is inferred from the API call.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_id(self) -> typing.Optional[builtins.str]:
        '''Name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id GoogleDataLossPreventionDiscoveryConfig#table_id}
        '''
        result = self._values.get("table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fced3533cf5f388d768cd858ddc20f3fcbf5bd73cefa449e7372107ed6a1b7c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetTableId")
    def reset_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableId", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9463abd9c1e36bed633ad47f97093e1f77e503575731bd588ee63e71e92f81ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423e4064bc4d6f87d4ab03af128271b7a2b637a6825a34427a1b1937e6f6771d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d3755a331829b041f439e2ac8091d48a2cd4598e3df643ff42e87cdba15abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c20a3f4f2d1b301ed7333040f894eaac965a5ca0328a89b3affbe66d377731d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d3ba9cf9503456a9a8723a0b1a40a54109fa49c5a8ead442ee66e7b28d4bddf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c8eae36d0ecf38dc93d3c2e8af96f2ed5081d35d3d6c8380bf96ff672742f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e39df8629be0c359a52d73bd29adf1da89f88070e2e64ed178e13b84fb8df44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32604be0e07583a86efa187d64b3cf89d0036498db2a546b9429215191ee0572)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5c4327f7416efb1ea188a32766e2dae8febe57fd368513973acc87a71937fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29afbd3df522b1aac6fa0f30e671957b98b5d5e39e8ab3f3a46c2ac083f7d4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aec5e1582659fc389092fdca06134b264863b3564e27da04f862ffa64aa73db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExportData")
    def put_export_data(
        self,
        *,
        profile_table: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param profile_table: profile_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#profile_table GoogleDataLossPreventionDiscoveryConfig#profile_table}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsExportData(
            profile_table=profile_table
        )

        return typing.cast(None, jsii.invoke(self, "putExportData", [value]))

    @jsii.member(jsii_name="putPubSubNotification")
    def put_pub_sub_notification(
        self,
        *,
        detail_of_message: typing.Optional[builtins.str] = None,
        event: typing.Optional[builtins.str] = None,
        pubsub_condition: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_of_message: How much data to include in the pub/sub message. Possible values: ["TABLE_PROFILE", "RESOURCE_NAME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#detail_of_message GoogleDataLossPreventionDiscoveryConfig#detail_of_message}
        :param event: The type of event that triggers a Pub/Sub. At most one PubSubNotification per EventType is permitted. Possible values: ["NEW_PROFILE", "CHANGED_PROFILE", "SCORE_INCREASED", "ERROR_CHANGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#event GoogleDataLossPreventionDiscoveryConfig#event}
        :param pubsub_condition: pubsub_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#pubsub_condition GoogleDataLossPreventionDiscoveryConfig#pubsub_condition}
        :param topic: Cloud Pub/Sub topic to send notifications to. Format is projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#topic GoogleDataLossPreventionDiscoveryConfig#topic}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification(
            detail_of_message=detail_of_message,
            event=event,
            pubsub_condition=pubsub_condition,
            topic=topic,
        )

        return typing.cast(None, jsii.invoke(self, "putPubSubNotification", [value]))

    @jsii.member(jsii_name="putTagResources")
    def put_tag_resources(
        self,
        *,
        lower_data_risk_to_low: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        profile_generations_to_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param lower_data_risk_to_low: Whether applying a tag to a resource should lower the risk of the profile for that resource. For example, in conjunction with an `IAM deny policy <https://cloud.google.com/iam/docs/deny-overview>`_, you can deny all principals a permission if a tag value is present, mitigating the risk of the resource. This also lowers the data risk of resources at the lower levels of the resource hierarchy. For example, reducing the data risk of a table data profile also reduces the data risk of the constituent column data profiles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#lower_data_risk_to_low GoogleDataLossPreventionDiscoveryConfig#lower_data_risk_to_low}
        :param profile_generations_to_tag: The profile generations for which the tag should be attached to resources. If you attach a tag to only new profiles, then if the sensitivity score of a profile subsequently changes, its tag doesn't change. By default, this field includes only new profiles. To include both new and updated profiles for tagging, this field should explicitly include both 'PROFILE_GENERATION_NEW' and 'PROFILE_GENERATION_UPDATE'. Possible values: ["PROFILE_GENERATION_NEW", "PROFILE_GENERATION_UPDATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#profile_generations_to_tag GoogleDataLossPreventionDiscoveryConfig#profile_generations_to_tag}
        :param tag_conditions: tag_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag_conditions GoogleDataLossPreventionDiscoveryConfig#tag_conditions}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsTagResources(
            lower_data_risk_to_low=lower_data_risk_to_low,
            profile_generations_to_tag=profile_generations_to_tag,
            tag_conditions=tag_conditions,
        )

        return typing.cast(None, jsii.invoke(self, "putTagResources", [value]))

    @jsii.member(jsii_name="resetExportData")
    def reset_export_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportData", []))

    @jsii.member(jsii_name="resetPubSubNotification")
    def reset_pub_sub_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubSubNotification", []))

    @jsii.member(jsii_name="resetTagResources")
    def reset_tag_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagResources", []))

    @builtins.property
    @jsii.member(jsii_name="exportData")
    def export_data(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigActionsExportDataOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigActionsExportDataOutputReference, jsii.get(self, "exportData"))

    @builtins.property
    @jsii.member(jsii_name="pubSubNotification")
    def pub_sub_notification(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference", jsii.get(self, "pubSubNotification"))

    @builtins.property
    @jsii.member(jsii_name="tagResources")
    def tag_resources(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesOutputReference", jsii.get(self, "tagResources"))

    @builtins.property
    @jsii.member(jsii_name="exportDataInput")
    def export_data_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportData]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportData], jsii.get(self, "exportDataInput"))

    @builtins.property
    @jsii.member(jsii_name="pubSubNotificationInput")
    def pub_sub_notification_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification"], jsii.get(self, "pubSubNotificationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagResourcesInput")
    def tag_resources_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResources"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResources"], jsii.get(self, "tagResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d07ff24f708f3f87edccb049c57541f6ed1836bcc09e14f7a9f8b924030ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification",
    jsii_struct_bases=[],
    name_mapping={
        "detail_of_message": "detailOfMessage",
        "event": "event",
        "pubsub_condition": "pubsubCondition",
        "topic": "topic",
    },
)
class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification:
    def __init__(
        self,
        *,
        detail_of_message: typing.Optional[builtins.str] = None,
        event: typing.Optional[builtins.str] = None,
        pubsub_condition: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_of_message: How much data to include in the pub/sub message. Possible values: ["TABLE_PROFILE", "RESOURCE_NAME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#detail_of_message GoogleDataLossPreventionDiscoveryConfig#detail_of_message}
        :param event: The type of event that triggers a Pub/Sub. At most one PubSubNotification per EventType is permitted. Possible values: ["NEW_PROFILE", "CHANGED_PROFILE", "SCORE_INCREASED", "ERROR_CHANGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#event GoogleDataLossPreventionDiscoveryConfig#event}
        :param pubsub_condition: pubsub_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#pubsub_condition GoogleDataLossPreventionDiscoveryConfig#pubsub_condition}
        :param topic: Cloud Pub/Sub topic to send notifications to. Format is projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#topic GoogleDataLossPreventionDiscoveryConfig#topic}
        '''
        if isinstance(pubsub_condition, dict):
            pubsub_condition = GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition(**pubsub_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d6f6263f9c37012a447f45e65a822fec2f96d1f086590d65b81cf0712a69be)
            check_type(argname="argument detail_of_message", value=detail_of_message, expected_type=type_hints["detail_of_message"])
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
            check_type(argname="argument pubsub_condition", value=pubsub_condition, expected_type=type_hints["pubsub_condition"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detail_of_message is not None:
            self._values["detail_of_message"] = detail_of_message
        if event is not None:
            self._values["event"] = event
        if pubsub_condition is not None:
            self._values["pubsub_condition"] = pubsub_condition
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def detail_of_message(self) -> typing.Optional[builtins.str]:
        '''How much data to include in the pub/sub message. Possible values: ["TABLE_PROFILE", "RESOURCE_NAME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#detail_of_message GoogleDataLossPreventionDiscoveryConfig#detail_of_message}
        '''
        result = self._values.get("detail_of_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event(self) -> typing.Optional[builtins.str]:
        '''The type of event that triggers a Pub/Sub.

        At most one PubSubNotification per EventType is permitted. Possible values: ["NEW_PROFILE", "CHANGED_PROFILE", "SCORE_INCREASED", "ERROR_CHANGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#event GoogleDataLossPreventionDiscoveryConfig#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_condition(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"]:
        '''pubsub_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#pubsub_condition GoogleDataLossPreventionDiscoveryConfig#pubsub_condition}
        '''
        result = self._values.get("pubsub_condition")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Cloud Pub/Sub topic to send notifications to. Format is projects/{project}/topics/{topic}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#topic GoogleDataLossPreventionDiscoveryConfig#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc4aff9bb3ef3f226990bdcf35986e2e573a374ec860cb8187b49ab10f0a184c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsubCondition")
    def put_pubsub_condition(
        self,
        *,
        expressions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param expressions: expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#expressions GoogleDataLossPreventionDiscoveryConfig#expressions}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition(
            expressions=expressions
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubCondition", [value]))

    @jsii.member(jsii_name="resetDetailOfMessage")
    def reset_detail_of_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetailOfMessage", []))

    @jsii.member(jsii_name="resetEvent")
    def reset_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvent", []))

    @jsii.member(jsii_name="resetPubsubCondition")
    def reset_pubsub_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubCondition", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="pubsubCondition")
    def pubsub_condition(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference", jsii.get(self, "pubsubCondition"))

    @builtins.property
    @jsii.member(jsii_name="detailOfMessageInput")
    def detail_of_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detailOfMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubConditionInput")
    def pubsub_condition_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"], jsii.get(self, "pubsubConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="detailOfMessage")
    def detail_of_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detailOfMessage"))

    @detail_of_message.setter
    def detail_of_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5f138555fb8060db9e7cb939fc371b011f0473904f3acd856a9cb5de2555da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detailOfMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @event.setter
    def event(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe04f32c9d095c057f9ced3c13fa98be681df84506f84f96cd9dbfb2b87cfad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0eb75436b90c40f9d0ac38f991b0f59ee029cc86cd10cb18076191fa54a18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07dbd143496a1e14a602f5e07b0dfd42b9c6bc620b473b07d7198f85ee834396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition",
    jsii_struct_bases=[],
    name_mapping={"expressions": "expressions"},
)
class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition:
    def __init__(
        self,
        *,
        expressions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param expressions: expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#expressions GoogleDataLossPreventionDiscoveryConfig#expressions}
        '''
        if isinstance(expressions, dict):
            expressions = GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions(**expressions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca98b08cb349b93c98914f4d35d221514e89442aad3f9dcd4bb451485f00431)
            check_type(argname="argument expressions", value=expressions, expected_type=type_hints["expressions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expressions is not None:
            self._values["expressions"] = expressions

    @builtins.property
    def expressions(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions"]:
        '''expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#expressions GoogleDataLossPreventionDiscoveryConfig#expressions}
        '''
        result = self._values.get("expressions")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions",
    jsii_struct_bases=[],
    name_mapping={"conditions": "conditions", "logical_operator": "logicalOperator"},
)
class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions:
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logical_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param logical_operator: The operator to apply to the collection of conditions Possible values: ["OR", "AND"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#logical_operator GoogleDataLossPreventionDiscoveryConfig#logical_operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cd8627633e0f07e4f086b4a3a619ec22c801ea5f6853fea1970b1afecbb683)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument logical_operator", value=logical_operator, expected_type=type_hints["logical_operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if logical_operator is not None:
            self._values["logical_operator"] = logical_operator

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions"]]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions"]]], result)

    @builtins.property
    def logical_operator(self) -> typing.Optional[builtins.str]:
        '''The operator to apply to the collection of conditions Possible values: ["OR", "AND"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#logical_operator GoogleDataLossPreventionDiscoveryConfig#logical_operator}
        '''
        result = self._values.get("logical_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions",
    jsii_struct_bases=[],
    name_mapping={
        "minimum_risk_score": "minimumRiskScore",
        "minimum_sensitivity_score": "minimumSensitivityScore",
    },
)
class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions:
    def __init__(
        self,
        *,
        minimum_risk_score: typing.Optional[builtins.str] = None,
        minimum_sensitivity_score: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimum_risk_score: The minimum data risk score that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#minimum_risk_score GoogleDataLossPreventionDiscoveryConfig#minimum_risk_score}
        :param minimum_sensitivity_score: The minimum sensitivity level that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#minimum_sensitivity_score GoogleDataLossPreventionDiscoveryConfig#minimum_sensitivity_score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f39dd53c0be842d7543c1a3d14f52b87bd27c1f4944b96c0a1ba77bf1273db)
            check_type(argname="argument minimum_risk_score", value=minimum_risk_score, expected_type=type_hints["minimum_risk_score"])
            check_type(argname="argument minimum_sensitivity_score", value=minimum_sensitivity_score, expected_type=type_hints["minimum_sensitivity_score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minimum_risk_score is not None:
            self._values["minimum_risk_score"] = minimum_risk_score
        if minimum_sensitivity_score is not None:
            self._values["minimum_sensitivity_score"] = minimum_sensitivity_score

    @builtins.property
    def minimum_risk_score(self) -> typing.Optional[builtins.str]:
        '''The minimum data risk score that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#minimum_risk_score GoogleDataLossPreventionDiscoveryConfig#minimum_risk_score}
        '''
        result = self._values.get("minimum_risk_score")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_sensitivity_score(self) -> typing.Optional[builtins.str]:
        '''The minimum sensitivity level that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#minimum_sensitivity_score GoogleDataLossPreventionDiscoveryConfig#minimum_sensitivity_score}
        '''
        result = self._values.get("minimum_sensitivity_score")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69f97e760bbcae69df4a64106c999c6cbe1049755be07cc4d6447fbb59e8adfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0812c123805e7e6030a4cd6001bce8be9ffd721fee3373c144b160762037b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b77d0e16f15ce5de305f0b5e4db719d1cb7a46099c73a56dc4c2d152c1b7eac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8ff2e0cd469a2e825700c38f972c7ea7e163fbf6b95cf44f65876d2f47d8da2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f0db5c264020bc7ff7cee7c82f7f54a8985ef1167a7d0aff43c66d5da11351c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75eff58f0c1db52c7730503c365c70056a3374603cd93fc3a6eb48ec9ccc9bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c076addbe945d3e05c6224193adbc2f6c7f9a79dd072788767ae31644b69dc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMinimumRiskScore")
    def reset_minimum_risk_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumRiskScore", []))

    @jsii.member(jsii_name="resetMinimumSensitivityScore")
    def reset_minimum_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumSensitivityScore", []))

    @builtins.property
    @jsii.member(jsii_name="minimumRiskScoreInput")
    def minimum_risk_score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumRiskScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumSensitivityScoreInput")
    def minimum_sensitivity_score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumSensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumRiskScore")
    def minimum_risk_score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumRiskScore"))

    @minimum_risk_score.setter
    def minimum_risk_score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a1517187399c05268ca54bcea12c0e0a57b128da8e72d8c39058780e94f6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumRiskScore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumSensitivityScore")
    def minimum_sensitivity_score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumSensitivityScore"))

    @minimum_sensitivity_score.setter
    def minimum_sensitivity_score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4765d151ec5e759e334a8808e4b53f134ce92fb9b56c5bd7d998822a4d2a53fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumSensitivityScore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d54c5d1e625d464d9b86f323358c95d91e0f3cab33cc6b95815c8a53b17089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff994d44a17edf6adeb2e9c8fd3e08d1cb8641160144bc126a7b0c33ec141cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f33998ed93ec60203e7584bac9d1ba1dd71e8c1ce5293e912bff4376f4c9186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetLogicalOperator")
    def reset_logical_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicalOperator", []))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalOperatorInput")
    def logical_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalOperator")
    def logical_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicalOperator"))

    @logical_operator.setter
    def logical_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dffec1d813c9ac8adcd164b8d0c694557424c3a2599857ea96720495fdd0139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicalOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfe4ac80f167dc5b0392e7c20ade692409cbd9149132ea6bec1f130f4490cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da0e53e72aa48615369733b7e294dce4ee0b15e9ed217164226432cbd661a52e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExpressions")
    def put_expressions(
        self,
        *,
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        logical_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param logical_operator: The operator to apply to the collection of conditions Possible values: ["OR", "AND"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#logical_operator GoogleDataLossPreventionDiscoveryConfig#logical_operator}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions(
            conditions=conditions, logical_operator=logical_operator
        )

        return typing.cast(None, jsii.invoke(self, "putExpressions", [value]))

    @jsii.member(jsii_name="resetExpressions")
    def reset_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressions", []))

    @builtins.property
    @jsii.member(jsii_name="expressions")
    def expressions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference, jsii.get(self, "expressions"))

    @builtins.property
    @jsii.member(jsii_name="expressionsInput")
    def expressions_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions], jsii.get(self, "expressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889c399a1381733a943276a1539f53982c7c55a70f43b02d11bba7a755d5c20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResources",
    jsii_struct_bases=[],
    name_mapping={
        "lower_data_risk_to_low": "lowerDataRiskToLow",
        "profile_generations_to_tag": "profileGenerationsToTag",
        "tag_conditions": "tagConditions",
    },
)
class GoogleDataLossPreventionDiscoveryConfigActionsTagResources:
    def __init__(
        self,
        *,
        lower_data_risk_to_low: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        profile_generations_to_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param lower_data_risk_to_low: Whether applying a tag to a resource should lower the risk of the profile for that resource. For example, in conjunction with an `IAM deny policy <https://cloud.google.com/iam/docs/deny-overview>`_, you can deny all principals a permission if a tag value is present, mitigating the risk of the resource. This also lowers the data risk of resources at the lower levels of the resource hierarchy. For example, reducing the data risk of a table data profile also reduces the data risk of the constituent column data profiles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#lower_data_risk_to_low GoogleDataLossPreventionDiscoveryConfig#lower_data_risk_to_low}
        :param profile_generations_to_tag: The profile generations for which the tag should be attached to resources. If you attach a tag to only new profiles, then if the sensitivity score of a profile subsequently changes, its tag doesn't change. By default, this field includes only new profiles. To include both new and updated profiles for tagging, this field should explicitly include both 'PROFILE_GENERATION_NEW' and 'PROFILE_GENERATION_UPDATE'. Possible values: ["PROFILE_GENERATION_NEW", "PROFILE_GENERATION_UPDATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#profile_generations_to_tag GoogleDataLossPreventionDiscoveryConfig#profile_generations_to_tag}
        :param tag_conditions: tag_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag_conditions GoogleDataLossPreventionDiscoveryConfig#tag_conditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af34b6b750babd0d545a40e6353b474f812226b9d1fc8aeb5254c8cfb576e2f)
            check_type(argname="argument lower_data_risk_to_low", value=lower_data_risk_to_low, expected_type=type_hints["lower_data_risk_to_low"])
            check_type(argname="argument profile_generations_to_tag", value=profile_generations_to_tag, expected_type=type_hints["profile_generations_to_tag"])
            check_type(argname="argument tag_conditions", value=tag_conditions, expected_type=type_hints["tag_conditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lower_data_risk_to_low is not None:
            self._values["lower_data_risk_to_low"] = lower_data_risk_to_low
        if profile_generations_to_tag is not None:
            self._values["profile_generations_to_tag"] = profile_generations_to_tag
        if tag_conditions is not None:
            self._values["tag_conditions"] = tag_conditions

    @builtins.property
    def lower_data_risk_to_low(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether applying a tag to a resource should lower the risk of the profile for that resource.

        For example, in conjunction with an `IAM deny policy <https://cloud.google.com/iam/docs/deny-overview>`_, you can deny all principals a permission if a tag value is present, mitigating the risk of the resource. This also lowers the data risk of resources at the lower levels of the resource hierarchy. For example, reducing the data risk of a table data profile also reduces the data risk of the constituent column data profiles.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#lower_data_risk_to_low GoogleDataLossPreventionDiscoveryConfig#lower_data_risk_to_low}
        '''
        result = self._values.get("lower_data_risk_to_low")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def profile_generations_to_tag(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The profile generations for which the tag should be attached to resources.

        If you attach a tag to only new profiles, then if the sensitivity score of a profile subsequently changes, its tag doesn't change. By default, this field includes only new profiles. To include both new and updated profiles for tagging, this field should explicitly include both 'PROFILE_GENERATION_NEW' and 'PROFILE_GENERATION_UPDATE'. Possible values: ["PROFILE_GENERATION_NEW", "PROFILE_GENERATION_UPDATE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#profile_generations_to_tag GoogleDataLossPreventionDiscoveryConfig#profile_generations_to_tag}
        '''
        result = self._values.get("profile_generations_to_tag")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_conditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions"]]]:
        '''tag_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag_conditions GoogleDataLossPreventionDiscoveryConfig#tag_conditions}
        '''
        result = self._values.get("tag_conditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsTagResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47110645cf2a512881a437d304a46971ae53385288a41d7053b75a092ee4e3f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagConditions")
    def put_tag_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0e65e806d74fdcd3b89c38693b8df5af4f59c1af7a4420126e689e74cfb04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagConditions", [value]))

    @jsii.member(jsii_name="resetLowerDataRiskToLow")
    def reset_lower_data_risk_to_low(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLowerDataRiskToLow", []))

    @jsii.member(jsii_name="resetProfileGenerationsToTag")
    def reset_profile_generations_to_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileGenerationsToTag", []))

    @jsii.member(jsii_name="resetTagConditions")
    def reset_tag_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagConditions", []))

    @builtins.property
    @jsii.member(jsii_name="tagConditions")
    def tag_conditions(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsList", jsii.get(self, "tagConditions"))

    @builtins.property
    @jsii.member(jsii_name="lowerDataRiskToLowInput")
    def lower_data_risk_to_low_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lowerDataRiskToLowInput"))

    @builtins.property
    @jsii.member(jsii_name="profileGenerationsToTagInput")
    def profile_generations_to_tag_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "profileGenerationsToTagInput"))

    @builtins.property
    @jsii.member(jsii_name="tagConditionsInput")
    def tag_conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions"]]], jsii.get(self, "tagConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="lowerDataRiskToLow")
    def lower_data_risk_to_low(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lowerDataRiskToLow"))

    @lower_data_risk_to_low.setter
    def lower_data_risk_to_low(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf102a1d91c596c594061ed71e753d294b000a8a51218187297f82d2bdc6cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lowerDataRiskToLow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileGenerationsToTag")
    def profile_generations_to_tag(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "profileGenerationsToTag"))

    @profile_generations_to_tag.setter
    def profile_generations_to_tag(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd559062063b634345afc33ef94a0b67158dfe07e9356c4b6ea10a1398665b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileGenerationsToTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResources]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee046015e47932585d714100391cd7ff5d67375459041e9eae456eb79fad7cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions",
    jsii_struct_bases=[],
    name_mapping={"sensitivity_score": "sensitivityScore", "tag": "tag"},
)
class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions:
    def __init__(
        self,
        *,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#sensitivity_score GoogleDataLossPreventionDiscoveryConfig#sensitivity_score}
        :param tag: tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag GoogleDataLossPreventionDiscoveryConfig#tag}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore(**sensitivity_score)
        if isinstance(tag, dict):
            tag = GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag(**tag)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6edc4f410f641ef8aba974f645d6aebabce9ac8892aaea6a5667a1ae9395e8)
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#sensitivity_score GoogleDataLossPreventionDiscoveryConfig#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore"], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag"]:
        '''tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tag GoogleDataLossPreventionDiscoveryConfig#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e487093abedc3ad89f7bc0d58c794078f05795cbc6817dd8f7d19c48c27f1a90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df17977296d3a101033b3c667e8f489e6675864c96ae4d13008f3811ed558e81)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbbcf7b2510cdc6a5cce9acc44f350db59d14bf7a3380905de7704607d9bafa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7115c5fa04d0c9a01d7e9b3cbd243949f6a8a2063d0df5e5a02eb3fb621def2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49d78d3a90bbd3591a20716aa41b337c6108c9212784b25b13f90c1efb95db1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482b43c087b2f51b2dc975c1c5b998e54bc2af5777984b26f35ba3dd915a3360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61a9acc9519343cc73bb19f7466a88a31339b1806d4bda1b1af702904a4114af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#score GoogleDataLossPreventionDiscoveryConfig#score}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        *,
        namespaced_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespaced_value: The namespaced name for the tag value to attach to resources. Must be in the format '{parent_id}/{tag_key_short_name}/{short_name}', for example, "123456/environment/prod". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#namespaced_value GoogleDataLossPreventionDiscoveryConfig#namespaced_value}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag(
            namespaced_value=namespaced_value
        )

        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTagOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTagOutputReference", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag"], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ec7f31086fcdd6583b7724a4a79839dee47257571a880abcfa0dbdc6d2cd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#score GoogleDataLossPreventionDiscoveryConfig#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c863a884b8a56244f0b60ad25783991fb7e78b9325c6f7cfdca313bfe78626)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#score GoogleDataLossPreventionDiscoveryConfig#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e3bb57b8dc1b8114224b4b04477e1598c3b56054f8047499a7a4f06cfbc35a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4686eada06998015887a01114ec0a47568e6e909edb7e914385d492a4988e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9f50ca15526ffaaa53203d31479a6f1817de8d1bead42f07991f22c0308642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag",
    jsii_struct_bases=[],
    name_mapping={"namespaced_value": "namespacedValue"},
)
class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag:
    def __init__(
        self,
        *,
        namespaced_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespaced_value: The namespaced name for the tag value to attach to resources. Must be in the format '{parent_id}/{tag_key_short_name}/{short_name}', for example, "123456/environment/prod". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#namespaced_value GoogleDataLossPreventionDiscoveryConfig#namespaced_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3134418b4025f8646ad5f281f9d8a8b1985a170584be7ccc6cd33cc9911dde9)
            check_type(argname="argument namespaced_value", value=namespaced_value, expected_type=type_hints["namespaced_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespaced_value is not None:
            self._values["namespaced_value"] = namespaced_value

    @builtins.property
    def namespaced_value(self) -> typing.Optional[builtins.str]:
        '''The namespaced name for the tag value to attach to resources.

        Must be in the format '{parent_id}/{tag_key_short_name}/{short_name}', for example, "123456/environment/prod".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#namespaced_value GoogleDataLossPreventionDiscoveryConfig#namespaced_value}
        '''
        result = self._values.get("namespaced_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f64a75fd16dd29cb1454a9d0577507b571004101da5f73f92bd07f693a8f8a6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespacedValue")
    def reset_namespaced_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespacedValue", []))

    @builtins.property
    @jsii.member(jsii_name="namespacedValueInput")
    def namespaced_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespacedValueInput"))

    @builtins.property
    @jsii.member(jsii_name="namespacedValue")
    def namespaced_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespacedValue"))

    @namespaced_value.setter
    def namespaced_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5cbb2c9e8d43ce68f6bfa5de39e0af75c2f724d72d33dd43bf98781938fc88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespacedValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646be84fa9bcf4fd942ad39b64be02d976e4f0c8fe47514eb826be1b90ce34c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigConfig",
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
        "parent": "parent",
        "actions": "actions",
        "display_name": "displayName",
        "id": "id",
        "inspect_templates": "inspectTemplates",
        "org_config": "orgConfig",
        "status": "status",
        "targets": "targets",
        "timeouts": "timeouts",
    },
)
class GoogleDataLossPreventionDiscoveryConfigConfig(
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
        location: builtins.str,
        parent: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_config: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigOrgConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location to create the discovery config in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#location GoogleDataLossPreventionDiscoveryConfig#location}
        :param parent: The parent of the discovery config in any of the following formats:. - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#parent GoogleDataLossPreventionDiscoveryConfig#parent}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#actions GoogleDataLossPreventionDiscoveryConfig#actions}
        :param display_name: Display Name (max 1000 Chars). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#display_name GoogleDataLossPreventionDiscoveryConfig#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#id GoogleDataLossPreventionDiscoveryConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_templates: Detection logic for profile generation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_templates GoogleDataLossPreventionDiscoveryConfig#inspect_templates}
        :param org_config: org_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#org_config GoogleDataLossPreventionDiscoveryConfig#org_config}
        :param status: Required. A status for this configuration Possible values: ["RUNNING", "PAUSED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#status GoogleDataLossPreventionDiscoveryConfig#status}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#targets GoogleDataLossPreventionDiscoveryConfig#targets}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#timeouts GoogleDataLossPreventionDiscoveryConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(org_config, dict):
            org_config = GoogleDataLossPreventionDiscoveryConfigOrgConfig(**org_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataLossPreventionDiscoveryConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a81cf1b45206eb7d29f082c785a8970d7012ce60f735f4e111887928321284)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inspect_templates", value=inspect_templates, expected_type=type_hints["inspect_templates"])
            check_type(argname="argument org_config", value=org_config, expected_type=type_hints["org_config"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "parent": parent,
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
        if actions is not None:
            self._values["actions"] = actions
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if inspect_templates is not None:
            self._values["inspect_templates"] = inspect_templates
        if org_config is not None:
            self._values["org_config"] = org_config
        if status is not None:
            self._values["status"] = status
        if targets is not None:
            self._values["targets"] = targets
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
        '''Location to create the discovery config in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#location GoogleDataLossPreventionDiscoveryConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the discovery config in any of the following formats:.

        - 'projects/{{project}}/locations/{{location}}'
        - 'organizations/{{organization_id}}/locations/{{location}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#parent GoogleDataLossPreventionDiscoveryConfig#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActions]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#actions GoogleDataLossPreventionDiscoveryConfig#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActions]]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display Name (max 1000 Chars).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#display_name GoogleDataLossPreventionDiscoveryConfig#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#id GoogleDataLossPreventionDiscoveryConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_templates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Detection logic for profile generation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_templates GoogleDataLossPreventionDiscoveryConfig#inspect_templates}
        '''
        result = self._values.get("inspect_templates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def org_config(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigOrgConfig"]:
        '''org_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#org_config GoogleDataLossPreventionDiscoveryConfig#org_config}
        '''
        result = self._values.get("org_config")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigOrgConfig"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Required. A status for this configuration Possible values: ["RUNNING", "PAUSED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#status GoogleDataLossPreventionDiscoveryConfig#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargets"]]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#targets GoogleDataLossPreventionDiscoveryConfig#targets}
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargets"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#timeouts GoogleDataLossPreventionDiscoveryConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigErrorsDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigErrorsDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigErrorsDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigErrorsDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigErrorsDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31e59f346e02f4df2556c315d06fb3011561751abb90eeff1eb2161a1c8a9506)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigErrorsDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2af8d10aea6f4177570718a58952d05749a1c792b3297734a087a6208c237f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigErrorsDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2b380654f34df34d42f80926b836629028e2bc1f29cf5cb411768c78ddc711)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d579fcc537276fab8b987d676b0c2576b9c18ef649e6b3d33b1eeb2af27c91d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db67b59683d0c644ae0c68d9921bdea2ff6fc91f85d0c65de86b0e741ffc5ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigErrorsDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigErrorsDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c41b5d1757f25b015f3b5c02272854e3c702d80e73e57cbb8d3bb3ab8d3c8964)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrorsDetails]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrorsDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrorsDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb62ac1a4f7cfa611e43618ff477b1e690fa1f68f801653583a60075fdd4441e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigErrorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acb373634e36479240e14eab566dd8d3b334762b219171fd7c4cd64335f48323)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d35a60dc76fcb17e486e5df6926da290f39c2afd1e60c6aa7e8139116be8fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3775bafb60f85fbac50389be81213b5829f55e35deb48be46770da5ec5e8bc69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f37c79c56fa23c56b4febd0e47f66c61d34939eabc473a6d5dadce1522ad0b85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__446ed8f919b57fded2feb208af43c52cda3ab4b3bd2fe72ffd4635e0a65d2544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigErrorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c16612a7865edbd5bd73fe463528054510a36d782db3355c23329b8bc0ca085)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> GoogleDataLossPreventionDiscoveryConfigErrorsDetailsList:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigErrorsDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrors]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf104d9a8a9c02f352290fe7e74489fd9e35894cc8fbcee61409ea2ff0a6280c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigOrgConfig",
    jsii_struct_bases=[],
    name_mapping={"location": "location", "project_id": "projectId"},
)
class GoogleDataLossPreventionDiscoveryConfigOrgConfig:
    def __init__(
        self,
        *,
        location: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#location GoogleDataLossPreventionDiscoveryConfig#location}
        :param project_id: The project that will run the scan. The DLP service account that exists within this project must have access to all resources that are profiled, and the cloud DLP API must be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        if isinstance(location, dict):
            location = GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation(**location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f67d99bda50030abc58cdcb6a0550ace7cfe5158ffd3e42add1be9910263e93)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location is not None:
            self._values["location"] = location
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def location(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation"]:
        '''location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#location GoogleDataLossPreventionDiscoveryConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The project that will run the scan.

        The DLP service account that exists within this project must have access to all resources that are profiled, and the cloud DLP API must be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigOrgConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation",
    jsii_struct_bases=[],
    name_mapping={"folder_id": "folderId", "organization_id": "organizationId"},
)
class GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation:
    def __init__(
        self,
        *,
        folder_id: typing.Optional[builtins.str] = None,
        organization_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param folder_id: The ID for the folder within an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#folder_id GoogleDataLossPreventionDiscoveryConfig#folder_id}
        :param organization_id: The ID of an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#organization_id GoogleDataLossPreventionDiscoveryConfig#organization_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bf0e9bca5932049b338f501450e14c45f9a7cb75899f928d5bc971dad6ed31)
            check_type(argname="argument folder_id", value=folder_id, expected_type=type_hints["folder_id"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if folder_id is not None:
            self._values["folder_id"] = folder_id
        if organization_id is not None:
            self._values["organization_id"] = organization_id

    @builtins.property
    def folder_id(self) -> typing.Optional[builtins.str]:
        '''The ID for the folder within an organization to scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#folder_id GoogleDataLossPreventionDiscoveryConfig#folder_id}
        '''
        result = self._values.get("folder_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an organization to scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#organization_id GoogleDataLossPreventionDiscoveryConfig#organization_id}
        '''
        result = self._values.get("organization_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1428d2ca0c06d17e709e2a9379bb737534053a17aff31e1684f4333d9f454fd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFolderId")
    def reset_folder_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolderId", []))

    @jsii.member(jsii_name="resetOrganizationId")
    def reset_organization_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationId", []))

    @builtins.property
    @jsii.member(jsii_name="folderIdInput")
    def folder_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationIdInput")
    def organization_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="folderId")
    def folder_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folderId"))

    @folder_id.setter
    def folder_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f022a00b1f6e11a23583e6aff80bbcc429c7b06ed6c8e3905bbc116cac098d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @organization_id.setter
    def organization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48121cdbd82fd1bf1fe4da0aabbc9d25580d154f5fd93e414b321dafaff1928d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73731032b78ce88923373e23fe23d5096c19a0fee5fd21de4e6652405db54cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigOrgConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigOrgConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da57abbc48ce002418cc96441456b9f34490cd599e09e5d405e64e96d9cae583)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocation")
    def put_location(
        self,
        *,
        folder_id: typing.Optional[builtins.str] = None,
        organization_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param folder_id: The ID for the folder within an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#folder_id GoogleDataLossPreventionDiscoveryConfig#folder_id}
        :param organization_id: The ID of an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#organization_id GoogleDataLossPreventionDiscoveryConfig#organization_id}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation(
            folder_id=folder_id, organization_id=organization_id
        )

        return typing.cast(None, jsii.invoke(self, "putLocation", [value]))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29bdd211671dd6efac17d8ca42b6df12c8cc93477337463a6182fd2a98b488a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6e4bb06ea512c7725cab37c015375641d6841c9eb727ad844b59c3eafba5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargets",
    jsii_struct_bases=[],
    name_mapping={
        "big_query_target": "bigQueryTarget",
        "cloud_sql_target": "cloudSqlTarget",
        "cloud_storage_target": "cloudStorageTarget",
        "secrets_target": "secretsTarget",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargets:
    def __init__(
        self,
        *,
        big_query_target: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_sql_target: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_storage_target: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        secrets_target: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param big_query_target: big_query_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#big_query_target GoogleDataLossPreventionDiscoveryConfig#big_query_target}
        :param cloud_sql_target: cloud_sql_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_sql_target GoogleDataLossPreventionDiscoveryConfig#cloud_sql_target}
        :param cloud_storage_target: cloud_storage_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_target GoogleDataLossPreventionDiscoveryConfig#cloud_storage_target}
        :param secrets_target: secrets_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#secrets_target GoogleDataLossPreventionDiscoveryConfig#secrets_target}
        '''
        if isinstance(big_query_target, dict):
            big_query_target = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget(**big_query_target)
        if isinstance(cloud_sql_target, dict):
            cloud_sql_target = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget(**cloud_sql_target)
        if isinstance(cloud_storage_target, dict):
            cloud_storage_target = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget(**cloud_storage_target)
        if isinstance(secrets_target, dict):
            secrets_target = GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget(**secrets_target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f677bae5f06a2996439afe124ea28848249066838ff483751222f3956bbb4fc0)
            check_type(argname="argument big_query_target", value=big_query_target, expected_type=type_hints["big_query_target"])
            check_type(argname="argument cloud_sql_target", value=cloud_sql_target, expected_type=type_hints["cloud_sql_target"])
            check_type(argname="argument cloud_storage_target", value=cloud_storage_target, expected_type=type_hints["cloud_storage_target"])
            check_type(argname="argument secrets_target", value=secrets_target, expected_type=type_hints["secrets_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if big_query_target is not None:
            self._values["big_query_target"] = big_query_target
        if cloud_sql_target is not None:
            self._values["cloud_sql_target"] = cloud_sql_target
        if cloud_storage_target is not None:
            self._values["cloud_storage_target"] = cloud_storage_target
        if secrets_target is not None:
            self._values["secrets_target"] = secrets_target

    @builtins.property
    def big_query_target(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget"]:
        '''big_query_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#big_query_target GoogleDataLossPreventionDiscoveryConfig#big_query_target}
        '''
        result = self._values.get("big_query_target")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget"], result)

    @builtins.property
    def cloud_sql_target(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget"]:
        '''cloud_sql_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_sql_target GoogleDataLossPreventionDiscoveryConfig#cloud_sql_target}
        '''
        result = self._values.get("cloud_sql_target")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget"], result)

    @builtins.property
    def cloud_storage_target(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget"]:
        '''cloud_storage_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_target GoogleDataLossPreventionDiscoveryConfig#cloud_storage_target}
        '''
        result = self._values.get("cloud_storage_target")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget"], result)

    @builtins.property
    def secrets_target(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget"]:
        '''secrets_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#secrets_target GoogleDataLossPreventionDiscoveryConfig#secrets_target}
        '''
        result = self._values.get("secrets_target")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget",
    jsii_struct_bases=[],
    name_mapping={
        "cadence": "cadence",
        "conditions": "conditions",
        "disabled": "disabled",
        "filter": "filter",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget:
    def __init__(
        self,
        *,
        cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        conditions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cadence: cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cadence GoogleDataLossPreventionDiscoveryConfig#cadence}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        '''
        if isinstance(cadence, dict):
            cadence = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence(**cadence)
        if isinstance(conditions, dict):
            conditions = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions(**conditions)
        if isinstance(disabled, dict):
            disabled = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled(**disabled)
        if isinstance(filter, dict):
            filter = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a568d873e30a04bf48b8e044dde0d7f02f43b451a4c7c51d0903b8056e1c0d)
            check_type(argname="argument cadence", value=cadence, expected_type=type_hints["cadence"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cadence is not None:
            self._values["cadence"] = cadence
        if conditions is not None:
            self._values["conditions"] = conditions
        if disabled is not None:
            self._values["disabled"] = disabled
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence"]:
        '''cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cadence GoogleDataLossPreventionDiscoveryConfig#cadence}
        '''
        result = self._values.get("cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence"], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions"]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions"], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled"]:
        '''disabled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled"], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence",
    jsii_struct_bases=[],
    name_mapping={
        "inspect_template_modified_cadence": "inspectTemplateModifiedCadence",
        "schema_modified_cadence": "schemaModifiedCadence",
        "table_modified_cadence": "tableModifiedCadence",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence:
    def __init__(
        self,
        *,
        inspect_template_modified_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_modified_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        table_modified_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param inspect_template_modified_cadence: inspect_template_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        :param schema_modified_cadence: schema_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#schema_modified_cadence GoogleDataLossPreventionDiscoveryConfig#schema_modified_cadence}
        :param table_modified_cadence: table_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_modified_cadence GoogleDataLossPreventionDiscoveryConfig#table_modified_cadence}
        '''
        if isinstance(inspect_template_modified_cadence, dict):
            inspect_template_modified_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence(**inspect_template_modified_cadence)
        if isinstance(schema_modified_cadence, dict):
            schema_modified_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence(**schema_modified_cadence)
        if isinstance(table_modified_cadence, dict):
            table_modified_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence(**table_modified_cadence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989fe62fd9bba6ace4e40815a0452a00d40b25bfa87ed600abb11ea4a5f0a1ff)
            check_type(argname="argument inspect_template_modified_cadence", value=inspect_template_modified_cadence, expected_type=type_hints["inspect_template_modified_cadence"])
            check_type(argname="argument schema_modified_cadence", value=schema_modified_cadence, expected_type=type_hints["schema_modified_cadence"])
            check_type(argname="argument table_modified_cadence", value=table_modified_cadence, expected_type=type_hints["table_modified_cadence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inspect_template_modified_cadence is not None:
            self._values["inspect_template_modified_cadence"] = inspect_template_modified_cadence
        if schema_modified_cadence is not None:
            self._values["schema_modified_cadence"] = schema_modified_cadence
        if table_modified_cadence is not None:
            self._values["table_modified_cadence"] = table_modified_cadence

    @builtins.property
    def inspect_template_modified_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence"]:
        '''inspect_template_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        '''
        result = self._values.get("inspect_template_modified_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence"], result)

    @builtins.property
    def schema_modified_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"]:
        '''schema_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#schema_modified_cadence GoogleDataLossPreventionDiscoveryConfig#schema_modified_cadence}
        '''
        result = self._values.get("schema_modified_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"], result)

    @builtins.property
    def table_modified_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"]:
        '''table_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_modified_cadence GoogleDataLossPreventionDiscoveryConfig#table_modified_cadence}
        '''
        result = self._values.get("table_modified_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence:
    def __init__(self, *, frequency: typing.Optional[builtins.str] = None) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when the template is modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3511b5d80bca40e3a3fcd91ddb868fbc352d19f00b9a01ef18db97a13e2d8b8c)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently data profiles can be updated when the template is modified.

        Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5881cc540119e8c63372bae78699084b7c2d5a7f4b1173176bd500e60a3bc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a81ea3779a67e9f13c427e342dc5b5b7b89478e6ad6428861550da6813e35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab17eae24c6c791f48189e0507fa0a981f1b8531e4f699a9f6bdf744edf24f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc58fc329c3d7b3a70ebb825fb490a2e04ea2d36515d0e5f7b79d645f87e25f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInspectTemplateModifiedCadence")
    def put_inspect_template_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when the template is modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence(
            frequency=frequency
        )

        return typing.cast(None, jsii.invoke(self, "putInspectTemplateModifiedCadence", [value]))

    @jsii.member(jsii_name="putSchemaModifiedCadence")
    def put_schema_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently profiles may be updated when schemas are modified. Default to monthly Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table's schema has been modified and should have the profile updated. Defaults to NEW_COLUMN. Possible values: ["SCHEMA_NEW_COLUMNS", "SCHEMA_REMOVED_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence(
            frequency=frequency, types=types
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaModifiedCadence", [value]))

    @jsii.member(jsii_name="putTableModifiedCadence")
    def put_table_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when tables are modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table has been modified and should have the profile updated. Defaults to MODIFIED_TIMESTAMP Possible values: ["TABLE_MODIFIED_TIMESTAMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence(
            frequency=frequency, types=types
        )

        return typing.cast(None, jsii.invoke(self, "putTableModifiedCadence", [value]))

    @jsii.member(jsii_name="resetInspectTemplateModifiedCadence")
    def reset_inspect_template_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplateModifiedCadence", []))

    @jsii.member(jsii_name="resetSchemaModifiedCadence")
    def reset_schema_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaModifiedCadence", []))

    @jsii.member(jsii_name="resetTableModifiedCadence")
    def reset_table_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableModifiedCadence", []))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateModifiedCadence")
    def inspect_template_modified_cadence(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadenceOutputReference, jsii.get(self, "inspectTemplateModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="schemaModifiedCadence")
    def schema_modified_cadence(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference", jsii.get(self, "schemaModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="tableModifiedCadence")
    def table_modified_cadence(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference", jsii.get(self, "tableModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateModifiedCadenceInput")
    def inspect_template_modified_cadence_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence], jsii.get(self, "inspectTemplateModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaModifiedCadenceInput")
    def schema_modified_cadence_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"], jsii.get(self, "schemaModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="tableModifiedCadenceInput")
    def table_modified_cadence_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"], jsii.get(self, "tableModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5efe721785d6154bcbd4a70c496c124d2f286d8365276730e6299585b9e50c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "types": "types"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently profiles may be updated when schemas are modified. Default to monthly Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table's schema has been modified and should have the profile updated. Defaults to NEW_COLUMN. Possible values: ["SCHEMA_NEW_COLUMNS", "SCHEMA_REMOVED_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ca09e0beaa6d9ebf272e6b417d5738ce441fa61a50c4415a6173faa20ad10e)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently profiles may be updated when schemas are modified. Default to monthly Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The type of events to consider when deciding if the table's schema has been modified and should have the profile updated.

        Defaults to NEW_COLUMN. Possible values: ["SCHEMA_NEW_COLUMNS", "SCHEMA_REMOVED_COLUMNS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abeca3338176c54105814c3409e0b17ae9b3ca60d4f663e539e580a1f61dab7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525560a19d18902a3a648bb34bf99051be71004db8a6b6cef8b5d298ce554401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a9c96fda350e29ad8c6b6ebbcf1d0ea6e4ef092bac3881219514c44b9b6384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716a40e39af0d8d36980c490ecdf92fb153462b80a087ba7978b7edf5702c0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "types": "types"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when tables are modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table has been modified and should have the profile updated. Defaults to MODIFIED_TIMESTAMP Possible values: ["TABLE_MODIFIED_TIMESTAMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262d78d98be5b48b820a0ef71d39269fe72d32c3033dbbb05b19ab61211ec0ea)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently data profiles can be updated when tables are modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The type of events to consider when deciding if the table has been modified and should have the profile updated.

        Defaults to MODIFIED_TIMESTAMP Possible values: ["TABLE_MODIFIED_TIMESTAMP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45a72037140bea37e5044040186995854d7eaa53bb3ccfd112fd2e7e264bc403)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a2a0b7f4296dc0edc6056dad71c0e44cdf15ae8c8bd73d82b695114002207e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ee2521a00e475653b3613b35c749ab8310716f9e5b60b2a8aa4b41f3b086c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32bfa7e632d499d3820ad25dac843cb3130bb2127c94b6f2ebc02875de00a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions",
    jsii_struct_bases=[],
    name_mapping={
        "created_after": "createdAfter",
        "or_conditions": "orConditions",
        "type_collection": "typeCollection",
        "types": "types",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions:
    def __init__(
        self,
        *,
        created_after: typing.Optional[builtins.str] = None,
        or_conditions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        type_collection: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param created_after: A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#created_after GoogleDataLossPreventionDiscoveryConfig#created_after}
        :param or_conditions: or_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#or_conditions GoogleDataLossPreventionDiscoveryConfig#or_conditions}
        :param type_collection: Restrict discovery to categories of table types. Currently view, materialized view, snapshot and non-biglake external tables are supported. Possible values: ["BIG_QUERY_COLLECTION_ALL_TYPES", "BIG_QUERY_COLLECTION_ONLY_SUPPORTED_TYPES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#type_collection GoogleDataLossPreventionDiscoveryConfig#type_collection}
        :param types: types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        if isinstance(or_conditions, dict):
            or_conditions = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions(**or_conditions)
        if isinstance(types, dict):
            types = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes(**types)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5bb45cb5ea98893ae54c30f21b26ec9524dcc8cd063a69886a3a1a160f6a53)
            check_type(argname="argument created_after", value=created_after, expected_type=type_hints["created_after"])
            check_type(argname="argument or_conditions", value=or_conditions, expected_type=type_hints["or_conditions"])
            check_type(argname="argument type_collection", value=type_collection, expected_type=type_hints["type_collection"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if created_after is not None:
            self._values["created_after"] = created_after
        if or_conditions is not None:
            self._values["or_conditions"] = or_conditions
        if type_collection is not None:
            self._values["type_collection"] = type_collection
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def created_after(self) -> typing.Optional[builtins.str]:
        '''A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#created_after GoogleDataLossPreventionDiscoveryConfig#created_after}
        '''
        result = self._values.get("created_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def or_conditions(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions"]:
        '''or_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#or_conditions GoogleDataLossPreventionDiscoveryConfig#or_conditions}
        '''
        result = self._values.get("or_conditions")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions"], result)

    @builtins.property
    def type_collection(self) -> typing.Optional[builtins.str]:
        '''Restrict discovery to categories of table types.

        Currently view, materialized view, snapshot and non-biglake external tables are supported. Possible values: ["BIG_QUERY_COLLECTION_ALL_TYPES", "BIG_QUERY_COLLECTION_ONLY_SUPPORTED_TYPES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#type_collection GoogleDataLossPreventionDiscoveryConfig#type_collection}
        '''
        result = self._values.get("type_collection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"]:
        '''types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions",
    jsii_struct_bases=[],
    name_mapping={"min_age": "minAge", "min_row_count": "minRowCount"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions:
    def __init__(
        self,
        *,
        min_age: typing.Optional[builtins.str] = None,
        min_row_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_age: Duration format. The minimum age a table must have before Cloud DLP can profile it. Value greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_age GoogleDataLossPreventionDiscoveryConfig#min_age}
        :param min_row_count: Minimum number of rows that should be present before Cloud DLP profiles as a table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_row_count GoogleDataLossPreventionDiscoveryConfig#min_row_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f17164d74bef34aa85bdca0a41fe5025aa311dbbe6950584be27fd6efc04baa)
            check_type(argname="argument min_age", value=min_age, expected_type=type_hints["min_age"])
            check_type(argname="argument min_row_count", value=min_row_count, expected_type=type_hints["min_row_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if min_age is not None:
            self._values["min_age"] = min_age
        if min_row_count is not None:
            self._values["min_row_count"] = min_row_count

    @builtins.property
    def min_age(self) -> typing.Optional[builtins.str]:
        '''Duration format. The minimum age a table must have before Cloud DLP can profile it. Value greater than 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_age GoogleDataLossPreventionDiscoveryConfig#min_age}
        '''
        result = self._values.get("min_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_row_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of rows that should be present before Cloud DLP profiles as a table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_row_count GoogleDataLossPreventionDiscoveryConfig#min_row_count}
        '''
        result = self._values.get("min_row_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bf5dcb56fd0a2e7c4485b87138ca6dc980fe0daca5cca58e939185f6c409744)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinAge")
    def reset_min_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAge", []))

    @jsii.member(jsii_name="resetMinRowCount")
    def reset_min_row_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRowCount", []))

    @builtins.property
    @jsii.member(jsii_name="minAgeInput")
    def min_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="minRowCountInput")
    def min_row_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRowCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minAge")
    def min_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minAge"))

    @min_age.setter
    def min_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8feab055971f57e17188e4f004bbb0a33bf9e8362d9489c2600ad6bec43b89a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRowCount")
    def min_row_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRowCount"))

    @min_row_count.setter
    def min_row_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cab2cbfa722e5d7ebfe946db609bb72ffaa996ced1e5ec57a71fffc21d73827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRowCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e425c555a843e1ae137f3d0b4c51e9f873020abb7fc360032b7c61eac6030084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ade237e3877c9635d4da6d970c7234fbcc02d0524ca3d6e996aa6d4c68ee5323)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOrConditions")
    def put_or_conditions(
        self,
        *,
        min_age: typing.Optional[builtins.str] = None,
        min_row_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_age: Duration format. The minimum age a table must have before Cloud DLP can profile it. Value greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_age GoogleDataLossPreventionDiscoveryConfig#min_age}
        :param min_row_count: Minimum number of rows that should be present before Cloud DLP profiles as a table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_row_count GoogleDataLossPreventionDiscoveryConfig#min_row_count}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions(
            min_age=min_age, min_row_count=min_row_count
        )

        return typing.cast(None, jsii.invoke(self, "putOrConditions", [value]))

    @jsii.member(jsii_name="putTypes")
    def put_types(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param types: A set of BiqQuery table types Possible values: ["BIG_QUERY_TABLE_TYPE_TABLE", "BIG_QUERY_TABLE_TYPE_EXTERNAL_BIG_LAKE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes(
            types=types
        )

        return typing.cast(None, jsii.invoke(self, "putTypes", [value]))

    @jsii.member(jsii_name="resetCreatedAfter")
    def reset_created_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAfter", []))

    @jsii.member(jsii_name="resetOrConditions")
    def reset_or_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrConditions", []))

    @jsii.member(jsii_name="resetTypeCollection")
    def reset_type_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeCollection", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="orConditions")
    def or_conditions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference, jsii.get(self, "orConditions"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference", jsii.get(self, "types"))

    @builtins.property
    @jsii.member(jsii_name="createdAfterInput")
    def created_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="orConditionsInput")
    def or_conditions_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions], jsii.get(self, "orConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeCollectionInput")
    def type_collection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAfter")
    def created_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAfter"))

    @created_after.setter
    def created_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774bea999310d976a6661575c250f083251e516912ecb1a8fe47f89f09e2f4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="typeCollection")
    def type_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeCollection"))

    @type_collection.setter
    def type_collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeaff3a51f7e902515b67559cf826d821918d443284d547bd822d3b6093e0dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40698823796dc965aef335d63577f8c3b90f00c995600aa12979215bf6cc4fb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param types: A set of BiqQuery table types Possible values: ["BIG_QUERY_TABLE_TYPE_TABLE", "BIG_QUERY_TABLE_TYPE_EXTERNAL_BIG_LAKE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc9b6804cd75ee37f2a54a0d8ffd961c24cec5eb676ac778d399f3bd9de05f0)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of BiqQuery table types Possible values: ["BIG_QUERY_TABLE_TYPE_TABLE", "BIG_QUERY_TABLE_TYPE_EXTERNAL_BIG_LAKE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ff35395b4b12cb3d3e81ced9d99ecff2f3cc74f859b7891943d14ca0397f74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70175d37bb90b71f7e03224acd25a91206f0abe8db8b4ba0c5ed15e92785e31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b4c58f1b9b1634ff14fcf1aaa1e8233fb31dd0f4ec7fd3ae5e7bc2cc8165af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c498df72fd641b21fc7db952e9a7815696d6fb9bf0b684025672946b09c55146)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5b01a1e25d5c9e6f69ef76efa2025616b8a10f1915bbff15bd7b8542249a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter",
    jsii_struct_bases=[],
    name_mapping={
        "other_tables": "otherTables",
        "table_reference": "tableReference",
        "tables": "tables",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter:
    def __init__(
        self,
        *,
        other_tables: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables", typing.Dict[builtins.str, typing.Any]]] = None,
        table_reference: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference", typing.Dict[builtins.str, typing.Any]]] = None,
        tables: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param other_tables: other_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#other_tables GoogleDataLossPreventionDiscoveryConfig#other_tables}
        :param table_reference: table_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_reference GoogleDataLossPreventionDiscoveryConfig#table_reference}
        :param tables: tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tables GoogleDataLossPreventionDiscoveryConfig#tables}
        '''
        if isinstance(other_tables, dict):
            other_tables = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables(**other_tables)
        if isinstance(table_reference, dict):
            table_reference = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference(**table_reference)
        if isinstance(tables, dict):
            tables = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables(**tables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db3fcc37fcd0ce19189e8bf3d2991767ba95b282e26e314bf1a458ce46d812d)
            check_type(argname="argument other_tables", value=other_tables, expected_type=type_hints["other_tables"])
            check_type(argname="argument table_reference", value=table_reference, expected_type=type_hints["table_reference"])
            check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if other_tables is not None:
            self._values["other_tables"] = other_tables
        if table_reference is not None:
            self._values["table_reference"] = table_reference
        if tables is not None:
            self._values["tables"] = tables

    @builtins.property
    def other_tables(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables"]:
        '''other_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#other_tables GoogleDataLossPreventionDiscoveryConfig#other_tables}
        '''
        result = self._values.get("other_tables")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables"], result)

    @builtins.property
    def table_reference(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference"]:
        '''table_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_reference GoogleDataLossPreventionDiscoveryConfig#table_reference}
        '''
        result = self._values.get("table_reference")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference"], result)

    @builtins.property
    def tables(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"]:
        '''tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tables GoogleDataLossPreventionDiscoveryConfig#tables}
        '''
        result = self._values.get("tables")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3296be49cadb2845f4ed079a79a2ce6f4ec07ea95897c388427df3aee40ee4dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983e31e205a9e2a23fa20c2ed088014592d4e60070d5d6590870368ca0bcf9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcddd13933f6f1ad2a11244d0f5a8167337349c49b9ad6ca0f8c8b1b04df6a34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOtherTables")
    def put_other_tables(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables()

        return typing.cast(None, jsii.invoke(self, "putOtherTables", [value]))

    @jsii.member(jsii_name="putTableReference")
    def put_table_reference(
        self,
        *,
        dataset_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: Dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id GoogleDataLossPreventionDiscoveryConfig#dataset_id}
        :param table_id: Name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id GoogleDataLossPreventionDiscoveryConfig#table_id}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference(
            dataset_id=dataset_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putTableReference", [value]))

    @jsii.member(jsii_name="putTables")
    def put_tables(
        self,
        *,
        include_regexes: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables(
            include_regexes=include_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putTables", [value]))

    @jsii.member(jsii_name="resetOtherTables")
    def reset_other_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOtherTables", []))

    @jsii.member(jsii_name="resetTableReference")
    def reset_table_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableReference", []))

    @jsii.member(jsii_name="resetTables")
    def reset_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTables", []))

    @builtins.property
    @jsii.member(jsii_name="otherTables")
    def other_tables(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference, jsii.get(self, "otherTables"))

    @builtins.property
    @jsii.member(jsii_name="tableReference")
    def table_reference(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReferenceOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReferenceOutputReference", jsii.get(self, "tableReference"))

    @builtins.property
    @jsii.member(jsii_name="tables")
    def tables(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference", jsii.get(self, "tables"))

    @builtins.property
    @jsii.member(jsii_name="otherTablesInput")
    def other_tables_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables], jsii.get(self, "otherTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="tableReferenceInput")
    def table_reference_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference"], jsii.get(self, "tableReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesInput")
    def tables_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"], jsii.get(self, "tablesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9424a8c456515094da2ac4b0bd7bee952019cf5e1f87da82c0aec6605ce3202a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference",
    jsii_struct_bases=[],
    name_mapping={"dataset_id": "datasetId", "table_id": "tableId"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference:
    def __init__(self, *, dataset_id: builtins.str, table_id: builtins.str) -> None:
        '''
        :param dataset_id: Dataset ID of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id GoogleDataLossPreventionDiscoveryConfig#dataset_id}
        :param table_id: Name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id GoogleDataLossPreventionDiscoveryConfig#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725d768e974f25c014066fc8b909aeea4bb0e3554d6af0f3080ffd356e67870d)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "table_id": table_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''Dataset ID of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id GoogleDataLossPreventionDiscoveryConfig#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''Name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id GoogleDataLossPreventionDiscoveryConfig#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0c6f87a085a15cd1b3ebe66c44ab1e0c37b09e91d113bb5326286ee3e3ddd7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f74cabe6431dc648f03e86556f8804dbf84a41b6393e3532c9b6011afb546b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428dabfeadcdcdd91fab4aedeb4753741bcb33aa00169eb3776b2cdaf397b814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e5699ae711ad5488975df269a083456e35edc3a01ef80c9766cc94bda42fac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables",
    jsii_struct_bases=[],
    name_mapping={"include_regexes": "includeRegexes"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables:
    def __init__(
        self,
        *,
        include_regexes: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        if isinstance(include_regexes, dict):
            include_regexes = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes(**include_regexes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4d286c83b07b2c23a5acd8e4ea49e531ddce637df745d94e05f8e676ad53a2)
            check_type(argname="argument include_regexes", value=include_regexes, expected_type=type_hints["include_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_regexes is not None:
            self._values["include_regexes"] = include_regexes

    @builtins.property
    def include_regexes(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes"]:
        '''include_regexes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        result = self._values.get("include_regexes")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes",
    jsii_struct_bases=[],
    name_mapping={"patterns": "patterns"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes:
    def __init__(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91cbfc772ee82c960e8a414e72c63338396573eb656b08e9de5c82f16bb2a73c)
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if patterns is not None:
            self._values["patterns"] = patterns

    @builtins.property
    def patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]]:
        '''patterns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bd6b65cc124f3f7d4f6d0f27d61cbbfa237ce0940094b6b78234517b734b57a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPatterns")
    def put_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fa9d67b28f3864769888c28bfadd6db32c048601114ad0445f7dbdd4940904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPatterns", [value]))

    @jsii.member(jsii_name="resetPatterns")
    def reset_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="patterns")
    def patterns(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList", jsii.get(self, "patterns"))

    @builtins.property
    @jsii.member(jsii_name="patternsInput")
    def patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]], jsii.get(self, "patternsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a121bedb4ce4b27d1e7a5cb3f45e3c3a671806e0d9118fec61e607b97af6f774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id_regex": "datasetIdRegex",
        "project_id_regex": "projectIdRegex",
        "table_id_regex": "tableIdRegex",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns:
    def __init__(
        self,
        *,
        dataset_id_regex: typing.Optional[builtins.str] = None,
        project_id_regex: typing.Optional[builtins.str] = None,
        table_id_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id_regex: if unset, this property matches all datasets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id_regex GoogleDataLossPreventionDiscoveryConfig#dataset_id_regex}
        :param project_id_regex: For organizations, if unset, will match all projects. Has no effect for data profile configurations created within a project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        :param table_id_regex: if unset, this property matches all tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id_regex GoogleDataLossPreventionDiscoveryConfig#table_id_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0778416aee23d1f8571d5fc023141f7e508114263b767b8cae9782781bb497f)
            check_type(argname="argument dataset_id_regex", value=dataset_id_regex, expected_type=type_hints["dataset_id_regex"])
            check_type(argname="argument project_id_regex", value=project_id_regex, expected_type=type_hints["project_id_regex"])
            check_type(argname="argument table_id_regex", value=table_id_regex, expected_type=type_hints["table_id_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_id_regex is not None:
            self._values["dataset_id_regex"] = dataset_id_regex
        if project_id_regex is not None:
            self._values["project_id_regex"] = project_id_regex
        if table_id_regex is not None:
            self._values["table_id_regex"] = table_id_regex

    @builtins.property
    def dataset_id_regex(self) -> typing.Optional[builtins.str]:
        '''if unset, this property matches all datasets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#dataset_id_regex GoogleDataLossPreventionDiscoveryConfig#dataset_id_regex}
        '''
        result = self._values.get("dataset_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id_regex(self) -> typing.Optional[builtins.str]:
        '''For organizations, if unset, will match all projects. Has no effect for data profile configurations created within a project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        result = self._values.get("project_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_id_regex(self) -> typing.Optional[builtins.str]:
        '''if unset, this property matches all tables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_id_regex GoogleDataLossPreventionDiscoveryConfig#table_id_regex}
        '''
        result = self._values.get("table_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35a9b57bd46b2c27af8439acecc5a23e32c3634315a0cf4e0c4ebcf9866210aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fdb0efdacafbe5a075872d9362248cf481716cfac91ea6969e1fe5dcc8eaf6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358662f19880c0b40c526cdb804708c66a5163dd850f2014c5b4965a58337396)
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
            type_hints = typing.get_type_hints(_typecheckingstub__258da9903e4d2e1a3b5971d601644427b1c4afa41c3cf2815f32c1743c7a47de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a560de17a3bf3983b7a0b0bc661c70131e7e52a806a7d779e3b6943c510c4966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88b49a2cfe73ab585e8fa2ef7bcbdf08efde25d30c0e259ba3950fe7fad5de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c3c3fabdd89275d62f276cb9498b9cea7a340c2db876f4b87117f2e9a6dddd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatasetIdRegex")
    def reset_dataset_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetIdRegex", []))

    @jsii.member(jsii_name="resetProjectIdRegex")
    def reset_project_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectIdRegex", []))

    @jsii.member(jsii_name="resetTableIdRegex")
    def reset_table_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableIdRegex", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdRegexInput")
    def dataset_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdRegexInput")
    def project_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdRegexInput")
    def table_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdRegex")
    def dataset_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetIdRegex"))

    @dataset_id_regex.setter
    def dataset_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0726279db8249a466136fc4cdcc4df94e5ee798165657cb19039d202fa21e413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetIdRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectIdRegex")
    def project_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectIdRegex"))

    @project_id_regex.setter
    def project_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc1a342e5ba6c3b0ee4877435a637abbef123713016631cc3a60160908e9f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectIdRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableIdRegex")
    def table_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableIdRegex"))

    @table_id_regex.setter
    def table_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43afde8ad4e700022edd1a728cffff441733e8b65d3687d90402235b5f936052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableIdRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b877252149621d298b69470bf55e79173b84af95dcb20ce762ed9fe604e1d942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f66960264acfd2a2edc53dd022c167da0dcd1ccd90f442820b96955b4d343bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludeRegexes")
    def put_include_regexes(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes(
            patterns=patterns
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeRegexes", [value]))

    @jsii.member(jsii_name="resetIncludeRegexes")
    def reset_include_regexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRegexes", []))

    @builtins.property
    @jsii.member(jsii_name="includeRegexes")
    def include_regexes(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference, jsii.get(self, "includeRegexes"))

    @builtins.property
    @jsii.member(jsii_name="includeRegexesInput")
    def include_regexes_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes], jsii.get(self, "includeRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282dfc73bb837b9c49693b13ebf1c4d6bbf674b12ff024d8a9819832c9686285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dfd6fc542be97edc3604455c5f3d38453a7eb4e5eba33c53bbd47e6ba5fcebc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCadence")
    def put_cadence(
        self,
        *,
        inspect_template_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        schema_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        table_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param inspect_template_modified_cadence: inspect_template_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        :param schema_modified_cadence: schema_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#schema_modified_cadence GoogleDataLossPreventionDiscoveryConfig#schema_modified_cadence}
        :param table_modified_cadence: table_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_modified_cadence GoogleDataLossPreventionDiscoveryConfig#table_modified_cadence}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence(
            inspect_template_modified_cadence=inspect_template_modified_cadence,
            schema_modified_cadence=schema_modified_cadence,
            table_modified_cadence=table_modified_cadence,
        )

        return typing.cast(None, jsii.invoke(self, "putCadence", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        created_after: typing.Optional[builtins.str] = None,
        or_conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        type_collection: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param created_after: A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#created_after GoogleDataLossPreventionDiscoveryConfig#created_after}
        :param or_conditions: or_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#or_conditions GoogleDataLossPreventionDiscoveryConfig#or_conditions}
        :param type_collection: Restrict discovery to categories of table types. Currently view, materialized view, snapshot and non-biglake external tables are supported. Possible values: ["BIG_QUERY_COLLECTION_ALL_TYPES", "BIG_QUERY_COLLECTION_ONLY_SUPPORTED_TYPES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#type_collection GoogleDataLossPreventionDiscoveryConfig#type_collection}
        :param types: types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions(
            created_after=created_after,
            or_conditions=or_conditions,
            type_collection=type_collection,
            types=types,
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putDisabled")
    def put_disabled(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled()

        return typing.cast(None, jsii.invoke(self, "putDisabled", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        other_tables: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables, typing.Dict[builtins.str, typing.Any]]] = None,
        table_reference: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference, typing.Dict[builtins.str, typing.Any]]] = None,
        tables: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param other_tables: other_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#other_tables GoogleDataLossPreventionDiscoveryConfig#other_tables}
        :param table_reference: table_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#table_reference GoogleDataLossPreventionDiscoveryConfig#table_reference}
        :param tables: tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#tables GoogleDataLossPreventionDiscoveryConfig#tables}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter(
            other_tables=other_tables, table_reference=table_reference, tables=tables
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetCadence")
    def reset_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCadence", []))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="cadence")
    def cadence(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference, jsii.get(self, "cadence"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="cadenceInput")
    def cadence_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence], jsii.get(self, "cadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf69c1d222fd7c06ebfb320f00524797a2826d81a8ee87f95a86b185a7fa71f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget",
    jsii_struct_bases=[],
    name_mapping={
        "filter": "filter",
        "conditions": "conditions",
        "disabled": "disabled",
        "generation_cadence": "generationCadence",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget:
    def __init__(
        self,
        *,
        filter: typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter", typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled", typing.Dict[builtins.str, typing.Any]]] = None,
        generation_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        :param generation_cadence: generation_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#generation_cadence GoogleDataLossPreventionDiscoveryConfig#generation_cadence}
        '''
        if isinstance(filter, dict):
            filter = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter(**filter)
        if isinstance(conditions, dict):
            conditions = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions(**conditions)
        if isinstance(disabled, dict):
            disabled = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled(**disabled)
        if isinstance(generation_cadence, dict):
            generation_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence(**generation_cadence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f007967582d4a65ff83c942926aa53410a85187cf1f9a98a603a941606eed001)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument generation_cadence", value=generation_cadence, expected_type=type_hints["generation_cadence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if disabled is not None:
            self._values["disabled"] = disabled
        if generation_cadence is not None:
            self._values["generation_cadence"] = generation_cadence

    @builtins.property
    def filter(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter", result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions"]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions"], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled"]:
        '''disabled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled"], result)

    @builtins.property
    def generation_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence"]:
        '''generation_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#generation_cadence GoogleDataLossPreventionDiscoveryConfig#generation_cadence}
        '''
        result = self._values.get("generation_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions",
    jsii_struct_bases=[],
    name_mapping={"database_engines": "databaseEngines", "types": "types"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions:
    def __init__(
        self,
        *,
        database_engines: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param database_engines: Database engines that should be profiled. Optional. Defaults to ALL_SUPPORTED_DATABASE_ENGINES if unspecified. Possible values: ["ALL_SUPPORTED_DATABASE_ENGINES", "MYSQL", "POSTGRES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_engines GoogleDataLossPreventionDiscoveryConfig#database_engines}
        :param types: Data profiles will only be generated for the database resource types specified in this field. If not specified, defaults to [DATABASE_RESOURCE_TYPE_ALL_SUPPORTED_TYPES]. Possible values: ["DATABASE_RESOURCE_TYPE_ALL_SUPPORTED_TYPES", "DATABASE_RESOURCE_TYPE_TABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8633ed03271c4d685dfde297e830ab680d1f584fe2e8ee28b9513847749320ea)
            check_type(argname="argument database_engines", value=database_engines, expected_type=type_hints["database_engines"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_engines is not None:
            self._values["database_engines"] = database_engines
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def database_engines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Database engines that should be profiled. Optional. Defaults to ALL_SUPPORTED_DATABASE_ENGINES if unspecified. Possible values: ["ALL_SUPPORTED_DATABASE_ENGINES", "MYSQL", "POSTGRES"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_engines GoogleDataLossPreventionDiscoveryConfig#database_engines}
        '''
        result = self._values.get("database_engines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Data profiles will only be generated for the database resource types specified in this field.

        If not specified, defaults to [DATABASE_RESOURCE_TYPE_ALL_SUPPORTED_TYPES]. Possible values: ["DATABASE_RESOURCE_TYPE_ALL_SUPPORTED_TYPES", "DATABASE_RESOURCE_TYPE_TABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dbdfc2874e15fd4698476cde0490e14d627fe19941ff4d00090724ffc19a2d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatabaseEngines")
    def reset_database_engines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseEngines", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="databaseEnginesInput")
    def database_engines_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "databaseEnginesInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseEngines")
    def database_engines(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "databaseEngines"))

    @database_engines.setter
    def database_engines(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e8556f9d578c7936e0e4a30a8aebf75a2b8725477fb935fb21996343ec9258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseEngines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58fe8f52519e4578861f77423c818d1e77fa6430b0f670d547cc25151aa15269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3c3c57593a0e1152dfdc8c3e2b2e33ae41deb53a4ae401d4b27eefdb73030f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04082c3aa15b3cd7063b9bb770b522e0c9d52704837533c068cf69156f372264)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9f1d91a9c13df8ed81340e7996272a20aad05c2b52667e72a1cc26a9035b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter",
    jsii_struct_bases=[],
    name_mapping={
        "collection": "collection",
        "database_resource_reference": "databaseResourceReference",
        "others": "others",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter:
    def __init__(
        self,
        *,
        collection: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection", typing.Dict[builtins.str, typing.Any]]] = None,
        database_resource_reference: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference", typing.Dict[builtins.str, typing.Any]]] = None,
        others: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param collection: collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#collection GoogleDataLossPreventionDiscoveryConfig#collection}
        :param database_resource_reference: database_resource_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource_reference GoogleDataLossPreventionDiscoveryConfig#database_resource_reference}
        :param others: others block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#others GoogleDataLossPreventionDiscoveryConfig#others}
        '''
        if isinstance(collection, dict):
            collection = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection(**collection)
        if isinstance(database_resource_reference, dict):
            database_resource_reference = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference(**database_resource_reference)
        if isinstance(others, dict):
            others = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers(**others)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a96776277121b2a3f16e77e20fdb45f1f140677b7a7cb8b0a6b0fcb516cd2e5)
            check_type(argname="argument collection", value=collection, expected_type=type_hints["collection"])
            check_type(argname="argument database_resource_reference", value=database_resource_reference, expected_type=type_hints["database_resource_reference"])
            check_type(argname="argument others", value=others, expected_type=type_hints["others"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collection is not None:
            self._values["collection"] = collection
        if database_resource_reference is not None:
            self._values["database_resource_reference"] = database_resource_reference
        if others is not None:
            self._values["others"] = others

    @builtins.property
    def collection(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection"]:
        '''collection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#collection GoogleDataLossPreventionDiscoveryConfig#collection}
        '''
        result = self._values.get("collection")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection"], result)

    @builtins.property
    def database_resource_reference(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference"]:
        '''database_resource_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource_reference GoogleDataLossPreventionDiscoveryConfig#database_resource_reference}
        '''
        result = self._values.get("database_resource_reference")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference"], result)

    @builtins.property
    def others(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers"]:
        '''others block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#others GoogleDataLossPreventionDiscoveryConfig#others}
        '''
        result = self._values.get("others")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection",
    jsii_struct_bases=[],
    name_mapping={"include_regexes": "includeRegexes"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection:
    def __init__(
        self,
        *,
        include_regexes: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        if isinstance(include_regexes, dict):
            include_regexes = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes(**include_regexes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb6b5c9a59492de5827e77366fd2561547f5c884f88eac2529d1883b152d5db)
            check_type(argname="argument include_regexes", value=include_regexes, expected_type=type_hints["include_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_regexes is not None:
            self._values["include_regexes"] = include_regexes

    @builtins.property
    def include_regexes(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes"]:
        '''include_regexes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        result = self._values.get("include_regexes")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes",
    jsii_struct_bases=[],
    name_mapping={"patterns": "patterns"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes:
    def __init__(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dfe570c7a7dd1f0cd06709f77b58c3e3fb9df76e23ac543e771c422d48e03b7)
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if patterns is not None:
            self._values["patterns"] = patterns

    @builtins.property
    def patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns"]]]:
        '''patterns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a23bb900a245f1232eadf0eb6dfa1596ddd76d945409933c21b7f046d31b895e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPatterns")
    def put_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e69385fb57651a4a82dfa437af65a28a3774a195d8735c413b0ae61748a0286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPatterns", [value]))

    @jsii.member(jsii_name="resetPatterns")
    def reset_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="patterns")
    def patterns(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsList", jsii.get(self, "patterns"))

    @builtins.property
    @jsii.member(jsii_name="patternsInput")
    def patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns"]]], jsii.get(self, "patternsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbc0cc3570a63aabfb1c3bd95383709b6b7d8fffdd3f8bea46a487f025809ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns",
    jsii_struct_bases=[],
    name_mapping={
        "database_regex": "databaseRegex",
        "database_resource_name_regex": "databaseResourceNameRegex",
        "instance_regex": "instanceRegex",
        "project_id_regex": "projectIdRegex",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns:
    def __init__(
        self,
        *,
        database_regex: typing.Optional[builtins.str] = None,
        database_resource_name_regex: typing.Optional[builtins.str] = None,
        instance_regex: typing.Optional[builtins.str] = None,
        project_id_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_regex: Regex to test the database name against. If empty, all databases match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_regex GoogleDataLossPreventionDiscoveryConfig#database_regex}
        :param database_resource_name_regex: Regex to test the database resource's name against. An example of a database resource name is a table's name. Other database resource names like view names could be included in the future. If empty, all database resources match.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource_name_regex GoogleDataLossPreventionDiscoveryConfig#database_resource_name_regex}
        :param instance_regex: Regex to test the instance name against. If empty, all instances match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#instance_regex GoogleDataLossPreventionDiscoveryConfig#instance_regex}
        :param project_id_regex: For organizations, if unset, will match all projects. Has no effect for data profile configurations created within a project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cd2cae3bd966d7d7618c8e083454dec4dd179ab0213b57f429ee9db5455584)
            check_type(argname="argument database_regex", value=database_regex, expected_type=type_hints["database_regex"])
            check_type(argname="argument database_resource_name_regex", value=database_resource_name_regex, expected_type=type_hints["database_resource_name_regex"])
            check_type(argname="argument instance_regex", value=instance_regex, expected_type=type_hints["instance_regex"])
            check_type(argname="argument project_id_regex", value=project_id_regex, expected_type=type_hints["project_id_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_regex is not None:
            self._values["database_regex"] = database_regex
        if database_resource_name_regex is not None:
            self._values["database_resource_name_regex"] = database_resource_name_regex
        if instance_regex is not None:
            self._values["instance_regex"] = instance_regex
        if project_id_regex is not None:
            self._values["project_id_regex"] = project_id_regex

    @builtins.property
    def database_regex(self) -> typing.Optional[builtins.str]:
        '''Regex to test the database name against. If empty, all databases match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_regex GoogleDataLossPreventionDiscoveryConfig#database_regex}
        '''
        result = self._values.get("database_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_resource_name_regex(self) -> typing.Optional[builtins.str]:
        '''Regex to test the database resource's name against.

        An example of a database resource name is a table's name. Other database resource names like view names could be included in the future. If empty, all database resources match.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource_name_regex GoogleDataLossPreventionDiscoveryConfig#database_resource_name_regex}
        '''
        result = self._values.get("database_resource_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_regex(self) -> typing.Optional[builtins.str]:
        '''Regex to test the instance name against. If empty, all instances match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#instance_regex GoogleDataLossPreventionDiscoveryConfig#instance_regex}
        '''
        result = self._values.get("instance_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id_regex(self) -> typing.Optional[builtins.str]:
        '''For organizations, if unset, will match all projects. Has no effect for data profile configurations created within a project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        result = self._values.get("project_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47fcebf64c73f3567702b2bdfc333bfdfe784bf72894fb8e1bea772e442ab53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8acc6739b96512fa03ffdd60205d573623d25c95c6bac09ab76d17d3b8f09180)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80047867519a66eb08a13d3e331c869bc96ef744e603e366a133916830a55cb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e9ac3dff21a4ebb763df9aecc9365d9afde6926059f824b8c561d453a785da3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c011d36c4b4382ee30a6c3995399cc5fe49703b1efd81703e162eb13786ded08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c62c84bc90487e4af31eda794c6e7eeb1feb1ea80385766cbfdb57578e015c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e40660266264934365e4823df5a6ffb5d6dc71cfaa4e1a6d66184d85ad95b4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatabaseRegex")
    def reset_database_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseRegex", []))

    @jsii.member(jsii_name="resetDatabaseResourceNameRegex")
    def reset_database_resource_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseResourceNameRegex", []))

    @jsii.member(jsii_name="resetInstanceRegex")
    def reset_instance_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceRegex", []))

    @jsii.member(jsii_name="resetProjectIdRegex")
    def reset_project_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectIdRegex", []))

    @builtins.property
    @jsii.member(jsii_name="databaseRegexInput")
    def database_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseResourceNameRegexInput")
    def database_resource_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseResourceNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceRegexInput")
    def instance_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdRegexInput")
    def project_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseRegex")
    def database_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseRegex"))

    @database_regex.setter
    def database_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0954a3b881f199a7c2e81ae4d5fad3291ca2b0a0d5670c7920f4ffa183e342c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseResourceNameRegex")
    def database_resource_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseResourceNameRegex"))

    @database_resource_name_regex.setter
    def database_resource_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e57ba30a807e9329751ea037e5fd06a2bfc9dd226d3b99d5ad14504a21692a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseResourceNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceRegex")
    def instance_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceRegex"))

    @instance_regex.setter
    def instance_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4976da4791fd033d223b846bf70d0fa42ca7d654b74c2c4997a4355a3c159882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectIdRegex")
    def project_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectIdRegex"))

    @project_id_regex.setter
    def project_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25468de6f7de97ee57e82e7845fc64e73570a5fd3e547192e624cd3a8f9c923b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectIdRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d653f6e00fafd6e0e40a578a9d2175d0008ee246d108f1971c8a572b715f3eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77e606d0cafe0bc85d83d9e135a03b7e82427659ffb031ef6c79c10ea3fa0747)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludeRegexes")
    def put_include_regexes(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes(
            patterns=patterns
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeRegexes", [value]))

    @jsii.member(jsii_name="resetIncludeRegexes")
    def reset_include_regexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRegexes", []))

    @builtins.property
    @jsii.member(jsii_name="includeRegexes")
    def include_regexes(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesOutputReference, jsii.get(self, "includeRegexes"))

    @builtins.property
    @jsii.member(jsii_name="includeRegexesInput")
    def include_regexes_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes], jsii.get(self, "includeRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf43506d4e0f4674def50a240b2431ae9a4160d028197ab0568de2c7e4ec800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "database_resource": "databaseResource",
        "instance": "instance",
        "project_id": "projectId",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference:
    def __init__(
        self,
        *,
        database: builtins.str,
        database_resource: builtins.str,
        instance: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param database: Required. Name of a database within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database GoogleDataLossPreventionDiscoveryConfig#database}
        :param database_resource: Required. Name of a database resource, for example, a table within the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource GoogleDataLossPreventionDiscoveryConfig#database_resource}
        :param instance: Required. The instance where this resource is located. For example: Cloud SQL instance ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#instance GoogleDataLossPreventionDiscoveryConfig#instance}
        :param project_id: Required. If within a project-level config, then this must match the config's project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f7d27da1f3745009821ed1e6c32209a8c60fabf176d08a079bfc4c5620ae4a)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument database_resource", value=database_resource, expected_type=type_hints["database_resource"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "database_resource": database_resource,
            "instance": instance,
            "project_id": project_id,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Required. Name of a database within the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database GoogleDataLossPreventionDiscoveryConfig#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_resource(self) -> builtins.str:
        '''Required. Name of a database resource, for example, a table within the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource GoogleDataLossPreventionDiscoveryConfig#database_resource}
        '''
        result = self._values.get("database_resource")
        assert result is not None, "Required property 'database_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''Required. The instance where this resource is located. For example: Cloud SQL instance ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#instance GoogleDataLossPreventionDiscoveryConfig#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Required. If within a project-level config, then this must match the config's project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19caa61ecd962eec5aa390639ded27a8e5ec6911c412a5b8df2a6837d5ddbb5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseResourceInput")
    def database_resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cacb371e026610b8c1d41e0cb37717d77b5a1915df596639b383af86f41eb08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseResource")
    def database_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseResource"))

    @database_resource.setter
    def database_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1772f1384560b8a5c7c6f8b3748913159e93560b88db2ed167a59d8e2b161996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cdbfb0e70e7a1a665311f35a2b620142086895f353663eb3b071d99da3f1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a678074f0001ca122ac44707853f0f283305bc95a7b280d85ad9eda0f011014e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778c5e654d21569b0954ab8621d84ea2d1da8976c458c2981aaed37459b7cf93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5afc56a18a9d66fae34ffe45a2ebcb89aad3ea5f7b378af028015053648003f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67b1f2258d47b1b40110d805e0126f37a677c408548c198491b8b48ac533ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__816656631e49b5f77a34773e192b994f6982768da86cc9bb433c9b61e1cc51c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCollection")
    def put_collection(
        self,
        *,
        include_regexes: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection(
            include_regexes=include_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putCollection", [value]))

    @jsii.member(jsii_name="putDatabaseResourceReference")
    def put_database_resource_reference(
        self,
        *,
        database: builtins.str,
        database_resource: builtins.str,
        instance: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param database: Required. Name of a database within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database GoogleDataLossPreventionDiscoveryConfig#database}
        :param database_resource: Required. Name of a database resource, for example, a table within the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource GoogleDataLossPreventionDiscoveryConfig#database_resource}
        :param instance: Required. The instance where this resource is located. For example: Cloud SQL instance ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#instance GoogleDataLossPreventionDiscoveryConfig#instance}
        :param project_id: Required. If within a project-level config, then this must match the config's project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference(
            database=database,
            database_resource=database_resource,
            instance=instance,
            project_id=project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseResourceReference", [value]))

    @jsii.member(jsii_name="putOthers")
    def put_others(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers()

        return typing.cast(None, jsii.invoke(self, "putOthers", [value]))

    @jsii.member(jsii_name="resetCollection")
    def reset_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollection", []))

    @jsii.member(jsii_name="resetDatabaseResourceReference")
    def reset_database_resource_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseResourceReference", []))

    @jsii.member(jsii_name="resetOthers")
    def reset_others(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOthers", []))

    @builtins.property
    @jsii.member(jsii_name="collection")
    def collection(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionOutputReference, jsii.get(self, "collection"))

    @builtins.property
    @jsii.member(jsii_name="databaseResourceReference")
    def database_resource_reference(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReferenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReferenceOutputReference, jsii.get(self, "databaseResourceReference"))

    @builtins.property
    @jsii.member(jsii_name="others")
    def others(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthersOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthersOutputReference, jsii.get(self, "others"))

    @builtins.property
    @jsii.member(jsii_name="collectionInput")
    def collection_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection], jsii.get(self, "collectionInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseResourceReferenceInput")
    def database_resource_reference_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference], jsii.get(self, "databaseResourceReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="othersInput")
    def others_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers], jsii.get(self, "othersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcef39956edc31124d5805a5c8f2e83989ef35f4c75000f1ff4b0fc7f2d0fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence",
    jsii_struct_bases=[],
    name_mapping={
        "inspect_template_modified_cadence": "inspectTemplateModifiedCadence",
        "refresh_frequency": "refreshFrequency",
        "schema_modified_cadence": "schemaModifiedCadence",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence:
    def __init__(
        self,
        *,
        inspect_template_modified_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_frequency: typing.Optional[builtins.str] = None,
        schema_modified_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param inspect_template_modified_cadence: inspect_template_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        :param refresh_frequency: Data changes (non-schema changes) in Cloud SQL tables can't trigger reprofiling. If you set this field, profiles are refreshed at this frequency regardless of whether the underlying tables have changes. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#refresh_frequency GoogleDataLossPreventionDiscoveryConfig#refresh_frequency}
        :param schema_modified_cadence: schema_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#schema_modified_cadence GoogleDataLossPreventionDiscoveryConfig#schema_modified_cadence}
        '''
        if isinstance(inspect_template_modified_cadence, dict):
            inspect_template_modified_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence(**inspect_template_modified_cadence)
        if isinstance(schema_modified_cadence, dict):
            schema_modified_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence(**schema_modified_cadence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d6363db822313e1d8ef47bf5526b19de8d53a5067888fa67ada0d84d6b0126)
            check_type(argname="argument inspect_template_modified_cadence", value=inspect_template_modified_cadence, expected_type=type_hints["inspect_template_modified_cadence"])
            check_type(argname="argument refresh_frequency", value=refresh_frequency, expected_type=type_hints["refresh_frequency"])
            check_type(argname="argument schema_modified_cadence", value=schema_modified_cadence, expected_type=type_hints["schema_modified_cadence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inspect_template_modified_cadence is not None:
            self._values["inspect_template_modified_cadence"] = inspect_template_modified_cadence
        if refresh_frequency is not None:
            self._values["refresh_frequency"] = refresh_frequency
        if schema_modified_cadence is not None:
            self._values["schema_modified_cadence"] = schema_modified_cadence

    @builtins.property
    def inspect_template_modified_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence"]:
        '''inspect_template_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        '''
        result = self._values.get("inspect_template_modified_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence"], result)

    @builtins.property
    def refresh_frequency(self) -> typing.Optional[builtins.str]:
        '''Data changes (non-schema changes) in Cloud SQL tables can't trigger reprofiling.

        If you set this field, profiles are refreshed at this frequency regardless of whether the underlying tables have changes. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#refresh_frequency GoogleDataLossPreventionDiscoveryConfig#refresh_frequency}
        '''
        result = self._values.get("refresh_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_modified_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence"]:
        '''schema_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#schema_modified_cadence GoogleDataLossPreventionDiscoveryConfig#schema_modified_cadence}
        '''
        result = self._values.get("schema_modified_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence:
    def __init__(self, *, frequency: builtins.str) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when the template is modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b26c74b95b5aea6f6ac57040e7e839b35d6bc524e2b054b2a767774ba272c48)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
        }

    @builtins.property
    def frequency(self) -> builtins.str:
        '''How frequently data profiles can be updated when the template is modified.

        Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06ccd8e881d41574578aee7472bd72835161505c65e4a4456126470575445b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0268852cb7f603d2ee86b5800ec26acef85cc7b5f54caec5fde393251f657bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0f0080eb875e3504cad7899c8d2876d9ef4bf79f15f2e053b817ee39e05bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c917f066697c323fbb86f3deaa5de0374ac3107c18283a5f9bc8d4b10f13dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInspectTemplateModifiedCadence")
    def put_inspect_template_modified_cadence(self, *, frequency: builtins.str) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when the template is modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence(
            frequency=frequency
        )

        return typing.cast(None, jsii.invoke(self, "putInspectTemplateModifiedCadence", [value]))

    @jsii.member(jsii_name="putSchemaModifiedCadence")
    def put_schema_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: Frequency to regenerate data profiles when the schema is modified. Defaults to monthly. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        :param types: The types of schema modifications to consider. Defaults to NEW_COLUMNS. Possible values: ["NEW_COLUMNS", "REMOVED_COLUMNS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence(
            frequency=frequency, types=types
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaModifiedCadence", [value]))

    @jsii.member(jsii_name="resetInspectTemplateModifiedCadence")
    def reset_inspect_template_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplateModifiedCadence", []))

    @jsii.member(jsii_name="resetRefreshFrequency")
    def reset_refresh_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshFrequency", []))

    @jsii.member(jsii_name="resetSchemaModifiedCadence")
    def reset_schema_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaModifiedCadence", []))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateModifiedCadence")
    def inspect_template_modified_cadence(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference, jsii.get(self, "inspectTemplateModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="schemaModifiedCadence")
    def schema_modified_cadence(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadenceOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadenceOutputReference", jsii.get(self, "schemaModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateModifiedCadenceInput")
    def inspect_template_modified_cadence_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence], jsii.get(self, "inspectTemplateModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshFrequencyInput")
    def refresh_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaModifiedCadenceInput")
    def schema_modified_cadence_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence"], jsii.get(self, "schemaModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshFrequency")
    def refresh_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshFrequency"))

    @refresh_frequency.setter
    def refresh_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa552a0fa7fb89ae7712127db31130aa68e55cc2d11d0b33749ac2dee745e02f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec86e4dad99150d5d9f0506a20b63f553f7ee3b33fd69ad1e767e8cf68ad848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "types": "types"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: Frequency to regenerate data profiles when the schema is modified. Defaults to monthly. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        :param types: The types of schema modifications to consider. Defaults to NEW_COLUMNS. Possible values: ["NEW_COLUMNS", "REMOVED_COLUMNS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ccb7621682c160bfb340f75e711c12df83d52064fe458edb4ad8d3bba08cb8)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''Frequency to regenerate data profiles when the schema is modified. Defaults to monthly. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The types of schema modifications to consider. Defaults to NEW_COLUMNS. Possible values: ["NEW_COLUMNS", "REMOVED_COLUMNS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca6e1f2c26b65f021ae9be62e4042a4c187dedcad45690ea5035a34885f3ee29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d041ad58e2f06ae9568238b52afb50cfbb5ec282f32b9a4095056ac559a48b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f42f54993274695554b537987b13b24aea3021d56382b79ad8c01624b38643d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087b56a508154c58bb460739c2cea9ad4ccc0244afa4114e039542a4233ffb30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__452805636f74515cf69f53ac503964b4c0d83b18c1da016f1a65c8d6a39fcc20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        database_engines: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param database_engines: Database engines that should be profiled. Optional. Defaults to ALL_SUPPORTED_DATABASE_ENGINES if unspecified. Possible values: ["ALL_SUPPORTED_DATABASE_ENGINES", "MYSQL", "POSTGRES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_engines GoogleDataLossPreventionDiscoveryConfig#database_engines}
        :param types: Data profiles will only be generated for the database resource types specified in this field. If not specified, defaults to [DATABASE_RESOURCE_TYPE_ALL_SUPPORTED_TYPES]. Possible values: ["DATABASE_RESOURCE_TYPE_ALL_SUPPORTED_TYPES", "DATABASE_RESOURCE_TYPE_TABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#types GoogleDataLossPreventionDiscoveryConfig#types}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions(
            database_engines=database_engines, types=types
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putDisabled")
    def put_disabled(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled()

        return typing.cast(None, jsii.invoke(self, "putDisabled", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        collection: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection, typing.Dict[builtins.str, typing.Any]]] = None,
        database_resource_reference: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference, typing.Dict[builtins.str, typing.Any]]] = None,
        others: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param collection: collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#collection GoogleDataLossPreventionDiscoveryConfig#collection}
        :param database_resource_reference: database_resource_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#database_resource_reference GoogleDataLossPreventionDiscoveryConfig#database_resource_reference}
        :param others: others block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#others GoogleDataLossPreventionDiscoveryConfig#others}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter(
            collection=collection,
            database_resource_reference=database_resource_reference,
            others=others,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putGenerationCadence")
    def put_generation_cadence(
        self,
        *,
        inspect_template_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_frequency: typing.Optional[builtins.str] = None,
        schema_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param inspect_template_modified_cadence: inspect_template_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        :param refresh_frequency: Data changes (non-schema changes) in Cloud SQL tables can't trigger reprofiling. If you set this field, profiles are refreshed at this frequency regardless of whether the underlying tables have changes. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#refresh_frequency GoogleDataLossPreventionDiscoveryConfig#refresh_frequency}
        :param schema_modified_cadence: schema_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#schema_modified_cadence GoogleDataLossPreventionDiscoveryConfig#schema_modified_cadence}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence(
            inspect_template_modified_cadence=inspect_template_modified_cadence,
            refresh_frequency=refresh_frequency,
            schema_modified_cadence=schema_modified_cadence,
        )

        return typing.cast(None, jsii.invoke(self, "putGenerationCadence", [value]))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetGenerationCadence")
    def reset_generation_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerationCadence", []))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditionsOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditionsOutputReference, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabledOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabledOutputReference, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="generationCadence")
    def generation_cadence(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceOutputReference, jsii.get(self, "generationCadence"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="generationCadenceInput")
    def generation_cadence_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence], jsii.get(self, "generationCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebbfaf0d56e71e5933dbae3ef227b52bcf2b858b1e454852d717e821f210469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget",
    jsii_struct_bases=[],
    name_mapping={
        "filter": "filter",
        "conditions": "conditions",
        "disabled": "disabled",
        "generation_cadence": "generationCadence",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget:
    def __init__(
        self,
        *,
        filter: typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter", typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled", typing.Dict[builtins.str, typing.Any]]] = None,
        generation_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        :param generation_cadence: generation_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#generation_cadence GoogleDataLossPreventionDiscoveryConfig#generation_cadence}
        '''
        if isinstance(filter, dict):
            filter = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter(**filter)
        if isinstance(conditions, dict):
            conditions = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions(**conditions)
        if isinstance(disabled, dict):
            disabled = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled(**disabled)
        if isinstance(generation_cadence, dict):
            generation_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence(**generation_cadence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96f9017eaedf31ec3e05e3adea7569ac267ba4e6d3947d28c1cbd8c5aed5d08)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument generation_cadence", value=generation_cadence, expected_type=type_hints["generation_cadence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if disabled is not None:
            self._values["disabled"] = disabled
        if generation_cadence is not None:
            self._values["generation_cadence"] = generation_cadence

    @builtins.property
    def filter(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter", result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions"]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions"], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled"]:
        '''disabled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled"], result)

    @builtins.property
    def generation_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence"]:
        '''generation_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#generation_cadence GoogleDataLossPreventionDiscoveryConfig#generation_cadence}
        '''
        result = self._values.get("generation_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_storage_conditions": "cloudStorageConditions",
        "created_after": "createdAfter",
        "min_age": "minAge",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions:
    def __init__(
        self,
        *,
        cloud_storage_conditions: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        created_after: typing.Optional[builtins.str] = None,
        min_age: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_storage_conditions: cloud_storage_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_conditions GoogleDataLossPreventionDiscoveryConfig#cloud_storage_conditions}
        :param created_after: File store must have been created after this date. Used to avoid backfilling. A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#created_after GoogleDataLossPreventionDiscoveryConfig#created_after}
        :param min_age: Duration format. Minimum age a file store must have. If set, the value must be 1 hour or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_age GoogleDataLossPreventionDiscoveryConfig#min_age}
        '''
        if isinstance(cloud_storage_conditions, dict):
            cloud_storage_conditions = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions(**cloud_storage_conditions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b477e5a28edf420a04381fdb2f8914d513ffddb34c588d387b93a925d7b2fba)
            check_type(argname="argument cloud_storage_conditions", value=cloud_storage_conditions, expected_type=type_hints["cloud_storage_conditions"])
            check_type(argname="argument created_after", value=created_after, expected_type=type_hints["created_after"])
            check_type(argname="argument min_age", value=min_age, expected_type=type_hints["min_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_conditions is not None:
            self._values["cloud_storage_conditions"] = cloud_storage_conditions
        if created_after is not None:
            self._values["created_after"] = created_after
        if min_age is not None:
            self._values["min_age"] = min_age

    @builtins.property
    def cloud_storage_conditions(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions"]:
        '''cloud_storage_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_conditions GoogleDataLossPreventionDiscoveryConfig#cloud_storage_conditions}
        '''
        result = self._values.get("cloud_storage_conditions")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions"], result)

    @builtins.property
    def created_after(self) -> typing.Optional[builtins.str]:
        '''File store must have been created after this date.

        Used to avoid backfilling. A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#created_after GoogleDataLossPreventionDiscoveryConfig#created_after}
        '''
        result = self._values.get("created_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_age(self) -> typing.Optional[builtins.str]:
        '''Duration format. Minimum age a file store must have. If set, the value must be 1 hour or greater.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_age GoogleDataLossPreventionDiscoveryConfig#min_age}
        '''
        result = self._values.get("min_age")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions",
    jsii_struct_bases=[],
    name_mapping={
        "included_bucket_attributes": "includedBucketAttributes",
        "included_object_attributes": "includedObjectAttributes",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions:
    def __init__(
        self,
        *,
        included_bucket_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_object_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_bucket_attributes: Only objects with the specified attributes will be scanned. Defaults to [ALL_SUPPORTED_BUCKETS] if unset. Possible values: ["ALL_SUPPORTED_BUCKETS", "AUTOCLASS_DISABLED", "AUTOCLASS_ENABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#included_bucket_attributes GoogleDataLossPreventionDiscoveryConfig#included_bucket_attributes}
        :param included_object_attributes: Only objects with the specified attributes will be scanned. If an object has one of the specified attributes but is inside an excluded bucket, it will not be scanned. Defaults to [ALL_SUPPORTED_OBJECTS]. A profile will be created even if no objects match the included_object_attributes. Possible values: ["ALL_SUPPORTED_OBJECTS", "STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE", "REGIONAL", "MULTI_REGIONAL", "DURABLE_REDUCED_AVAILABILITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#included_object_attributes GoogleDataLossPreventionDiscoveryConfig#included_object_attributes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fc0f2c151fd9848e40b12dffee5efd62e66e8f29f039adc4574cef838a3243)
            check_type(argname="argument included_bucket_attributes", value=included_bucket_attributes, expected_type=type_hints["included_bucket_attributes"])
            check_type(argname="argument included_object_attributes", value=included_object_attributes, expected_type=type_hints["included_object_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_bucket_attributes is not None:
            self._values["included_bucket_attributes"] = included_bucket_attributes
        if included_object_attributes is not None:
            self._values["included_object_attributes"] = included_object_attributes

    @builtins.property
    def included_bucket_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Only objects with the specified attributes will be scanned. Defaults to [ALL_SUPPORTED_BUCKETS] if unset. Possible values: ["ALL_SUPPORTED_BUCKETS", "AUTOCLASS_DISABLED", "AUTOCLASS_ENABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#included_bucket_attributes GoogleDataLossPreventionDiscoveryConfig#included_bucket_attributes}
        '''
        result = self._values.get("included_bucket_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_object_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Only objects with the specified attributes will be scanned.

        If an object has one of the specified attributes but is inside an excluded bucket, it will not be scanned. Defaults to [ALL_SUPPORTED_OBJECTS]. A profile will be created even if no objects match the included_object_attributes. Possible values: ["ALL_SUPPORTED_OBJECTS", "STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE", "REGIONAL", "MULTI_REGIONAL", "DURABLE_REDUCED_AVAILABILITY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#included_object_attributes GoogleDataLossPreventionDiscoveryConfig#included_object_attributes}
        '''
        result = self._values.get("included_object_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b61e27eaa10ce8989a8ae7a9aadc381b1c10102889d70b07ee6f1edc8f3402)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludedBucketAttributes")
    def reset_included_bucket_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedBucketAttributes", []))

    @jsii.member(jsii_name="resetIncludedObjectAttributes")
    def reset_included_object_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedObjectAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="includedBucketAttributesInput")
    def included_bucket_attributes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedBucketAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedObjectAttributesInput")
    def included_object_attributes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedObjectAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedBucketAttributes")
    def included_bucket_attributes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedBucketAttributes"))

    @included_bucket_attributes.setter
    def included_bucket_attributes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758dd5439c8111740b9614511557eb2fdc5fd33252dd73849ac616da0b90aa12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedBucketAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedObjectAttributes")
    def included_object_attributes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedObjectAttributes"))

    @included_object_attributes.setter
    def included_object_attributes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1150bde177a4985e3f85c588e6187ddd1e4ebb7b8159761d533a13feea0b146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedObjectAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da82ce9787e679c479c0275327e42fa471ec47142a0d47f8033ffd8619465a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__108138c613647f38ec0f901065eff716b639e5c28f0b47f9ff1a868b4f4608f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStorageConditions")
    def put_cloud_storage_conditions(
        self,
        *,
        included_bucket_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_object_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_bucket_attributes: Only objects with the specified attributes will be scanned. Defaults to [ALL_SUPPORTED_BUCKETS] if unset. Possible values: ["ALL_SUPPORTED_BUCKETS", "AUTOCLASS_DISABLED", "AUTOCLASS_ENABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#included_bucket_attributes GoogleDataLossPreventionDiscoveryConfig#included_bucket_attributes}
        :param included_object_attributes: Only objects with the specified attributes will be scanned. If an object has one of the specified attributes but is inside an excluded bucket, it will not be scanned. Defaults to [ALL_SUPPORTED_OBJECTS]. A profile will be created even if no objects match the included_object_attributes. Possible values: ["ALL_SUPPORTED_OBJECTS", "STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE", "REGIONAL", "MULTI_REGIONAL", "DURABLE_REDUCED_AVAILABILITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#included_object_attributes GoogleDataLossPreventionDiscoveryConfig#included_object_attributes}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions(
            included_bucket_attributes=included_bucket_attributes,
            included_object_attributes=included_object_attributes,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageConditions", [value]))

    @jsii.member(jsii_name="resetCloudStorageConditions")
    def reset_cloud_storage_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageConditions", []))

    @jsii.member(jsii_name="resetCreatedAfter")
    def reset_created_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAfter", []))

    @jsii.member(jsii_name="resetMinAge")
    def reset_min_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAge", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageConditions")
    def cloud_storage_conditions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditionsOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditionsOutputReference, jsii.get(self, "cloudStorageConditions"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageConditionsInput")
    def cloud_storage_conditions_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions], jsii.get(self, "cloudStorageConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAfterInput")
    def created_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="minAgeInput")
    def min_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAfter")
    def created_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAfter"))

    @created_after.setter
    def created_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0e21418d7ce5cb8fd478bc6b6bc8322fbf63a6f659986ba0a3ca2e64a56ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minAge")
    def min_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minAge"))

    @min_age.setter
    def min_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efebd95fbf756de27e0436ec8ca3fea1da78a9aca356bbd9c7e0413e2c4319fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851011406d9324e03f5f2bf2e117a82e6854f91d7e5b8fd956bf90977e58ef08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__516fd5cae23a1867c481631dc7c86c0ca8513d2bfd66ee4947bb10f6864028ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27e9c323fff64502d588b8a33c1d8ebed092050c3a0a58e80aec82f95f9a777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_storage_resource_reference": "cloudStorageResourceReference",
        "collection": "collection",
        "others": "others",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter:
    def __init__(
        self,
        *,
        cloud_storage_resource_reference: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference", typing.Dict[builtins.str, typing.Any]]] = None,
        collection: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection", typing.Dict[builtins.str, typing.Any]]] = None,
        others: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_resource_reference: cloud_storage_resource_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_resource_reference GoogleDataLossPreventionDiscoveryConfig#cloud_storage_resource_reference}
        :param collection: collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#collection GoogleDataLossPreventionDiscoveryConfig#collection}
        :param others: others block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#others GoogleDataLossPreventionDiscoveryConfig#others}
        '''
        if isinstance(cloud_storage_resource_reference, dict):
            cloud_storage_resource_reference = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference(**cloud_storage_resource_reference)
        if isinstance(collection, dict):
            collection = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection(**collection)
        if isinstance(others, dict):
            others = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers(**others)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3ff4197b8b62f0d730cc63ece750b72e772f2dc6e3b785687e6018bac76ae1)
            check_type(argname="argument cloud_storage_resource_reference", value=cloud_storage_resource_reference, expected_type=type_hints["cloud_storage_resource_reference"])
            check_type(argname="argument collection", value=collection, expected_type=type_hints["collection"])
            check_type(argname="argument others", value=others, expected_type=type_hints["others"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_resource_reference is not None:
            self._values["cloud_storage_resource_reference"] = cloud_storage_resource_reference
        if collection is not None:
            self._values["collection"] = collection
        if others is not None:
            self._values["others"] = others

    @builtins.property
    def cloud_storage_resource_reference(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference"]:
        '''cloud_storage_resource_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_resource_reference GoogleDataLossPreventionDiscoveryConfig#cloud_storage_resource_reference}
        '''
        result = self._values.get("cloud_storage_resource_reference")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference"], result)

    @builtins.property
    def collection(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection"]:
        '''collection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#collection GoogleDataLossPreventionDiscoveryConfig#collection}
        '''
        result = self._values.get("collection")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection"], result)

    @builtins.property
    def others(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers"]:
        '''others block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#others GoogleDataLossPreventionDiscoveryConfig#others}
        '''
        result = self._values.get("others")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "project_id": "projectId"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The bucket to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#bucket_name GoogleDataLossPreventionDiscoveryConfig#bucket_name}
        :param project_id: If within a project-level config, then this must match the config's project id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0900d81418252780698338f20b2271bdb8b4967128d715e6475700d5f1df5697)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The bucket to scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#bucket_name GoogleDataLossPreventionDiscoveryConfig#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''If within a project-level config, then this must match the config's project id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__369f5a77043c3e55e1e212cc7e13b44e5fa52f2fbe0d6d4be68b700895f225fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07a73be561340e66ca83ac8b3ba418407df65ba909a1166f0e4e223f1ec7eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2796069f30c64654af9d561dda740957d86fcfbf5a080c6e154265cdd98adccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff12b25917dca010b2972b948ca779174c9f2dacdf17a9e1625107acc0e847f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection",
    jsii_struct_bases=[],
    name_mapping={"include_regexes": "includeRegexes"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection:
    def __init__(
        self,
        *,
        include_regexes: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        if isinstance(include_regexes, dict):
            include_regexes = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes(**include_regexes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9e92edb10641eb709b8032fb6198ec8671ff0a5434f4b8f998681804ef9352)
            check_type(argname="argument include_regexes", value=include_regexes, expected_type=type_hints["include_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_regexes is not None:
            self._values["include_regexes"] = include_regexes

    @builtins.property
    def include_regexes(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes"]:
        '''include_regexes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        result = self._values.get("include_regexes")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes",
    jsii_struct_bases=[],
    name_mapping={"patterns": "patterns"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes:
    def __init__(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516449f6f6e1b40f72105cc449f60c3547e03d0a91fbe34b13b8168845f80099)
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if patterns is not None:
            self._values["patterns"] = patterns

    @builtins.property
    def patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns"]]]:
        '''patterns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4806ff96541d4db54354087178838634f271a5f9fb76f5981ece5decd4ca7275)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPatterns")
    def put_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e099aa55256801c132f9912934d921d1d2a56c53362f9bf35874686142a11b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPatterns", [value]))

    @jsii.member(jsii_name="resetPatterns")
    def reset_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="patterns")
    def patterns(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsList":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsList", jsii.get(self, "patterns"))

    @builtins.property
    @jsii.member(jsii_name="patternsInput")
    def patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns"]]], jsii.get(self, "patternsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55453ae35abe547d39052fe5e34477f5762931cd23253719c4ff4c97fc57b35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_regex": "cloudStorageRegex"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns:
    def __init__(
        self,
        *,
        cloud_storage_regex: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_regex: cloud_storage_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_regex GoogleDataLossPreventionDiscoveryConfig#cloud_storage_regex}
        '''
        if isinstance(cloud_storage_regex, dict):
            cloud_storage_regex = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex(**cloud_storage_regex)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2538f2e73dee3bdad77425d048bfc2c5e3a79680661ee216515da52422aac596)
            check_type(argname="argument cloud_storage_regex", value=cloud_storage_regex, expected_type=type_hints["cloud_storage_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_regex is not None:
            self._values["cloud_storage_regex"] = cloud_storage_regex

    @builtins.property
    def cloud_storage_regex(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex"]:
        '''cloud_storage_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_regex GoogleDataLossPreventionDiscoveryConfig#cloud_storage_regex}
        '''
        result = self._values.get("cloud_storage_regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name_regex": "bucketNameRegex",
        "project_id_regex": "projectIdRegex",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex:
    def __init__(
        self,
        *,
        bucket_name_regex: typing.Optional[builtins.str] = None,
        project_id_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name_regex: Regex to test the bucket name against. If empty, all buckets match. Example: "marketing2021" or "(marketing)\\d{4}" will both match the bucket gs://marketing2021 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#bucket_name_regex GoogleDataLossPreventionDiscoveryConfig#bucket_name_regex}
        :param project_id_regex: For organizations, if unset, will match all projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f135e1b11cab34b046889146531169f08fcdd9a6a69d6c626da31080df21c5c3)
            check_type(argname="argument bucket_name_regex", value=bucket_name_regex, expected_type=type_hints["bucket_name_regex"])
            check_type(argname="argument project_id_regex", value=project_id_regex, expected_type=type_hints["project_id_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name_regex is not None:
            self._values["bucket_name_regex"] = bucket_name_regex
        if project_id_regex is not None:
            self._values["project_id_regex"] = project_id_regex

    @builtins.property
    def bucket_name_regex(self) -> typing.Optional[builtins.str]:
        '''Regex to test the bucket name against.

        If empty, all buckets match. Example: "marketing2021" or "(marketing)\\d{4}" will both match the bucket gs://marketing2021

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#bucket_name_regex GoogleDataLossPreventionDiscoveryConfig#bucket_name_regex}
        '''
        result = self._values.get("bucket_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id_regex(self) -> typing.Optional[builtins.str]:
        '''For organizations, if unset, will match all projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        result = self._values.get("project_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cdd7ddbcaac16740ca105335d689b1469b2af1404f67511b6b2b1302e475754)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketNameRegex")
    def reset_bucket_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketNameRegex", []))

    @jsii.member(jsii_name="resetProjectIdRegex")
    def reset_project_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectIdRegex", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameRegexInput")
    def bucket_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdRegexInput")
    def project_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameRegex")
    def bucket_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketNameRegex"))

    @bucket_name_regex.setter
    def bucket_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92486ae3b3b40273de6c4975b13624c9eabaceb0a1cdc27c0df1487d74e1612b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectIdRegex")
    def project_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectIdRegex"))

    @project_id_regex.setter
    def project_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cf22da293de2d31b8993ca1eb8edb68916f5cf150451781859ccef473148f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectIdRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d4de8a3b3c74af46b8c08cb01db3d0f91967a18ec760fce6d47e390eedfc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__219657d870ff66131309ffe15531329d874ba52f969f37bd812c1a15d6033d67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27282426f39f72536423dfb1cddf84c396d6db3f82df54d956f07a9c99d7ccf9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61f9c4bce590ee93874585f402262e3596e946efc6c8b9a3ef1f3ef30cbe701)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c29bc200395056bc218e528000d8b132c41787028b0b0fbb2e3069aafd8adbcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d348859a97677c89bb7cf28f08368160883e34d381af836039ddc056907dfcc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b9f67c45748f1f267fe767a835b89464088ddbd7b5d017f2eaa76a01322e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96a692e8c26b6e4d818b41628fdb85149813a606418b881d7167e4209a220c36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCloudStorageRegex")
    def put_cloud_storage_regex(
        self,
        *,
        bucket_name_regex: typing.Optional[builtins.str] = None,
        project_id_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name_regex: Regex to test the bucket name against. If empty, all buckets match. Example: "marketing2021" or "(marketing)\\d{4}" will both match the bucket gs://marketing2021 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#bucket_name_regex GoogleDataLossPreventionDiscoveryConfig#bucket_name_regex}
        :param project_id_regex: For organizations, if unset, will match all projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id_regex GoogleDataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex(
            bucket_name_regex=bucket_name_regex, project_id_regex=project_id_regex
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageRegex", [value]))

    @jsii.member(jsii_name="resetCloudStorageRegex")
    def reset_cloud_storage_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageRegex", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageRegex")
    def cloud_storage_regex(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegexOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegexOutputReference, jsii.get(self, "cloudStorageRegex"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageRegexInput")
    def cloud_storage_regex_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex], jsii.get(self, "cloudStorageRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85353cca78caaf8c093a1fbbf40020311d62b4822d47d28e4167428b5e363e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__146b2c7919342dd8c4ef32296fd8be7cbad123c31d640459612c65ab51dca31d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludeRegexes")
    def put_include_regexes(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#patterns GoogleDataLossPreventionDiscoveryConfig#patterns}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes(
            patterns=patterns
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeRegexes", [value]))

    @jsii.member(jsii_name="resetIncludeRegexes")
    def reset_include_regexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRegexes", []))

    @builtins.property
    @jsii.member(jsii_name="includeRegexes")
    def include_regexes(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesOutputReference, jsii.get(self, "includeRegexes"))

    @builtins.property
    @jsii.member(jsii_name="includeRegexesInput")
    def include_regexes_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes], jsii.get(self, "includeRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ad08627900afd1ab881b7694c098e0f48b607976ac0685306521c58ed17c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b92df40694937d1406d53cc597eafa12df099fd113647de3eb67a05bd32ef513)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47dac4f57f16dc6eb8891072bbf0cfd2358bbb23ae6068a27180e45a19b9699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07a698560648e46d39b09d669f079adae257c7c433782f8c117bdf26e508b770)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStorageResourceReference")
    def put_cloud_storage_resource_reference(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: The bucket to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#bucket_name GoogleDataLossPreventionDiscoveryConfig#bucket_name}
        :param project_id: If within a project-level config, then this must match the config's project id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#project_id GoogleDataLossPreventionDiscoveryConfig#project_id}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference(
            bucket_name=bucket_name, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageResourceReference", [value]))

    @jsii.member(jsii_name="putCollection")
    def put_collection(
        self,
        *,
        include_regexes: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#include_regexes GoogleDataLossPreventionDiscoveryConfig#include_regexes}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection(
            include_regexes=include_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putCollection", [value]))

    @jsii.member(jsii_name="putOthers")
    def put_others(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers()

        return typing.cast(None, jsii.invoke(self, "putOthers", [value]))

    @jsii.member(jsii_name="resetCloudStorageResourceReference")
    def reset_cloud_storage_resource_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageResourceReference", []))

    @jsii.member(jsii_name="resetCollection")
    def reset_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollection", []))

    @jsii.member(jsii_name="resetOthers")
    def reset_others(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOthers", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageResourceReference")
    def cloud_storage_resource_reference(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReferenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReferenceOutputReference, jsii.get(self, "cloudStorageResourceReference"))

    @builtins.property
    @jsii.member(jsii_name="collection")
    def collection(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionOutputReference, jsii.get(self, "collection"))

    @builtins.property
    @jsii.member(jsii_name="others")
    def others(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthersOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthersOutputReference, jsii.get(self, "others"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageResourceReferenceInput")
    def cloud_storage_resource_reference_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference], jsii.get(self, "cloudStorageResourceReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionInput")
    def collection_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection], jsii.get(self, "collectionInput"))

    @builtins.property
    @jsii.member(jsii_name="othersInput")
    def others_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers], jsii.get(self, "othersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7763328ef3f3aa32b70001c86fc437cad9959b5b302c77c1cb1e86f49149f175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence",
    jsii_struct_bases=[],
    name_mapping={
        "inspect_template_modified_cadence": "inspectTemplateModifiedCadence",
        "refresh_frequency": "refreshFrequency",
    },
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence:
    def __init__(
        self,
        *,
        inspect_template_modified_cadence: typing.Optional[typing.Union["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_frequency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inspect_template_modified_cadence: inspect_template_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        :param refresh_frequency: Data changes in Cloud Storage can't trigger reprofiling. If you set this field, profiles are refreshed at this frequency regardless of whether the underlying buckets have changes. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#refresh_frequency GoogleDataLossPreventionDiscoveryConfig#refresh_frequency}
        '''
        if isinstance(inspect_template_modified_cadence, dict):
            inspect_template_modified_cadence = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence(**inspect_template_modified_cadence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca62bb21f20aee07e047f5c026a03091937654a0d3506c17a08b7db8bb91392)
            check_type(argname="argument inspect_template_modified_cadence", value=inspect_template_modified_cadence, expected_type=type_hints["inspect_template_modified_cadence"])
            check_type(argname="argument refresh_frequency", value=refresh_frequency, expected_type=type_hints["refresh_frequency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inspect_template_modified_cadence is not None:
            self._values["inspect_template_modified_cadence"] = inspect_template_modified_cadence
        if refresh_frequency is not None:
            self._values["refresh_frequency"] = refresh_frequency

    @builtins.property
    def inspect_template_modified_cadence(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence"]:
        '''inspect_template_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        '''
        result = self._values.get("inspect_template_modified_cadence")
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence"], result)

    @builtins.property
    def refresh_frequency(self) -> typing.Optional[builtins.str]:
        '''Data changes in Cloud Storage can't trigger reprofiling.

        If you set this field, profiles are refreshed at this frequency regardless of whether the underlying buckets have changes. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#refresh_frequency GoogleDataLossPreventionDiscoveryConfig#refresh_frequency}
        '''
        result = self._values.get("refresh_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency"},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence:
    def __init__(self, *, frequency: typing.Optional[builtins.str] = None) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when the template is modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52185909ef41b9a1a3532482ddd3e4aa90ff44c82437616c47744e79b55ea0d1)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently data profiles can be updated when the template is modified.

        Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b1c8268ac4b75ecc1665d11baa97f6f6c97697e10fe39460f07d80a5e1c9f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1410cab40e94f9961b3d4f4acd64a45195c54cf0d37321310b325bb6060173a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9a8dd7e4088d77d0e66edd723793c6873983612fc4060f18c54d7e282dd8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb417eaddcea96149697c9d5b78c540caa713894356338f4a12c55f236a8bbe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInspectTemplateModifiedCadence")
    def put_inspect_template_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when the template is modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#frequency GoogleDataLossPreventionDiscoveryConfig#frequency}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence(
            frequency=frequency
        )

        return typing.cast(None, jsii.invoke(self, "putInspectTemplateModifiedCadence", [value]))

    @jsii.member(jsii_name="resetInspectTemplateModifiedCadence")
    def reset_inspect_template_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplateModifiedCadence", []))

    @jsii.member(jsii_name="resetRefreshFrequency")
    def reset_refresh_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshFrequency", []))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateModifiedCadence")
    def inspect_template_modified_cadence(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference, jsii.get(self, "inspectTemplateModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateModifiedCadenceInput")
    def inspect_template_modified_cadence_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence], jsii.get(self, "inspectTemplateModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshFrequencyInput")
    def refresh_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshFrequency")
    def refresh_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshFrequency"))

    @refresh_frequency.setter
    def refresh_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31385362c013476ace3bb75e96b3d8096f8cc8c2ba0bb15d0cd61c0c5e0a2668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fd392154c6b3e7dead277b4eab9f53fa6cf993bb4783d683ebc6f97afa647b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3dad2d52574e083359e311cbfbe6ad8d92a2a8c6925da1e498a7f52aa17950)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        cloud_storage_conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        created_after: typing.Optional[builtins.str] = None,
        min_age: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_storage_conditions: cloud_storage_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_conditions GoogleDataLossPreventionDiscoveryConfig#cloud_storage_conditions}
        :param created_after: File store must have been created after this date. Used to avoid backfilling. A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#created_after GoogleDataLossPreventionDiscoveryConfig#created_after}
        :param min_age: Duration format. Minimum age a file store must have. If set, the value must be 1 hour or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#min_age GoogleDataLossPreventionDiscoveryConfig#min_age}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions(
            cloud_storage_conditions=cloud_storage_conditions,
            created_after=created_after,
            min_age=min_age,
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putDisabled")
    def put_disabled(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled()

        return typing.cast(None, jsii.invoke(self, "putDisabled", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        cloud_storage_resource_reference: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference, typing.Dict[builtins.str, typing.Any]]] = None,
        collection: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection, typing.Dict[builtins.str, typing.Any]]] = None,
        others: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_resource_reference: cloud_storage_resource_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cloud_storage_resource_reference GoogleDataLossPreventionDiscoveryConfig#cloud_storage_resource_reference}
        :param collection: collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#collection GoogleDataLossPreventionDiscoveryConfig#collection}
        :param others: others block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#others GoogleDataLossPreventionDiscoveryConfig#others}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter(
            cloud_storage_resource_reference=cloud_storage_resource_reference,
            collection=collection,
            others=others,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putGenerationCadence")
    def put_generation_cadence(
        self,
        *,
        inspect_template_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_frequency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inspect_template_modified_cadence: inspect_template_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#inspect_template_modified_cadence GoogleDataLossPreventionDiscoveryConfig#inspect_template_modified_cadence}
        :param refresh_frequency: Data changes in Cloud Storage can't trigger reprofiling. If you set this field, profiles are refreshed at this frequency regardless of whether the underlying buckets have changes. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#refresh_frequency GoogleDataLossPreventionDiscoveryConfig#refresh_frequency}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence(
            inspect_template_modified_cadence=inspect_template_modified_cadence,
            refresh_frequency=refresh_frequency,
        )

        return typing.cast(None, jsii.invoke(self, "putGenerationCadence", [value]))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetGenerationCadence")
    def reset_generation_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerationCadence", []))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsOutputReference, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabledOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabledOutputReference, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="generationCadence")
    def generation_cadence(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceOutputReference, jsii.get(self, "generationCadence"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="generationCadenceInput")
    def generation_cadence_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence], jsii.get(self, "generationCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4e8c4df01b63aff4f8e5a6b5bc49c089754a4fba9ce9ed154877b81ae01e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c4b92a7343c9ff692b73ade8323da5bde3744571432a89ea57608191eccf1c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c20183f6a62524b6b040feeda0124461a38d4ad27f945a3ac68f52e61ecc0b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a4253d5d74e8006ed4c85d3df8213a3fe6b53f1f1de373697ae0eddc2550bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cfda5044e614f35ef71381495e2f9ed9cc6efe0bf1b7b91c31cca832df5b8b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a3640700bb63dde13b84fd68832133a5fdbebe26ddbf9920256ac81377cbfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d21f86975db9500aa9ca994d2c74c1b663000cd55f3dc7d176d80af447355f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionDiscoveryConfigTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c228652eacde274e58e9658a7151f5d8e3cfe78dd6e3140e298fdf3bcf8dd3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBigQueryTarget")
    def put_big_query_target(
        self,
        *,
        cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cadence: cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#cadence GoogleDataLossPreventionDiscoveryConfig#cadence}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget(
            cadence=cadence, conditions=conditions, disabled=disabled, filter=filter
        )

        return typing.cast(None, jsii.invoke(self, "putBigQueryTarget", [value]))

    @jsii.member(jsii_name="putCloudSqlTarget")
    def put_cloud_sql_target(
        self,
        *,
        filter: typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter, typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
        generation_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        :param generation_cadence: generation_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#generation_cadence GoogleDataLossPreventionDiscoveryConfig#generation_cadence}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget(
            filter=filter,
            conditions=conditions,
            disabled=disabled,
            generation_cadence=generation_cadence,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudSqlTarget", [value]))

    @jsii.member(jsii_name="putCloudStorageTarget")
    def put_cloud_storage_target(
        self,
        *,
        filter: typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter, typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
        generation_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#filter GoogleDataLossPreventionDiscoveryConfig#filter}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#conditions GoogleDataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#disabled GoogleDataLossPreventionDiscoveryConfig#disabled}
        :param generation_cadence: generation_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#generation_cadence GoogleDataLossPreventionDiscoveryConfig#generation_cadence}
        '''
        value = GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget(
            filter=filter,
            conditions=conditions,
            disabled=disabled,
            generation_cadence=generation_cadence,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStorageTarget", [value]))

    @jsii.member(jsii_name="putSecretsTarget")
    def put_secrets_target(self) -> None:
        value = GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget()

        return typing.cast(None, jsii.invoke(self, "putSecretsTarget", [value]))

    @jsii.member(jsii_name="resetBigQueryTarget")
    def reset_big_query_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQueryTarget", []))

    @jsii.member(jsii_name="resetCloudSqlTarget")
    def reset_cloud_sql_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlTarget", []))

    @jsii.member(jsii_name="resetCloudStorageTarget")
    def reset_cloud_storage_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStorageTarget", []))

    @jsii.member(jsii_name="resetSecretsTarget")
    def reset_secrets_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsTarget", []))

    @builtins.property
    @jsii.member(jsii_name="bigQueryTarget")
    def big_query_target(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference, jsii.get(self, "bigQueryTarget"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlTarget")
    def cloud_sql_target(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetOutputReference, jsii.get(self, "cloudSqlTarget"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageTarget")
    def cloud_storage_target(
        self,
    ) -> GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetOutputReference:
        return typing.cast(GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetOutputReference, jsii.get(self, "cloudStorageTarget"))

    @builtins.property
    @jsii.member(jsii_name="secretsTarget")
    def secrets_target(
        self,
    ) -> "GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTargetOutputReference":
        return typing.cast("GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTargetOutputReference", jsii.get(self, "secretsTarget"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryTargetInput")
    def big_query_target_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget], jsii.get(self, "bigQueryTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlTargetInput")
    def cloud_sql_target_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget], jsii.get(self, "cloudSqlTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudStorageTargetInput")
    def cloud_storage_target_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget], jsii.get(self, "cloudStorageTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsTargetInput")
    def secrets_target_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget"], jsii.get(self, "secretsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c670c2cd08772a8c7676cb76415de6aafcf808887a58a1af76740edc39f8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe357628b17fe0ae6c9c07e8711dd32c89540aeecd914e8fa4588c95ec476be8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a32b3a3a43c0da4d9494a60e21837e041e70f033dc09fae2eb11077d0242c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataLossPreventionDiscoveryConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#create GoogleDataLossPreventionDiscoveryConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#delete GoogleDataLossPreventionDiscoveryConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#update GoogleDataLossPreventionDiscoveryConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b816fc5875210e2a79a0ee964d8d61f0184d7fc17cd3db8e853c7fbceb96cd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#create GoogleDataLossPreventionDiscoveryConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#delete GoogleDataLossPreventionDiscoveryConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_discovery_config#update GoogleDataLossPreventionDiscoveryConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionDiscoveryConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionDiscoveryConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionDiscoveryConfig.GoogleDataLossPreventionDiscoveryConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d45cba7b910baebdf822b1eee5b6d7eed0cf6863a04a899d2ff44c79b242969c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__934401c3b84eec3c69bd6fb6e885a41af20f22be30543ab40b43cb8da273b2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c9769fc133e34c3a92aeec4da9e96a82f6caf5b1c64eaaada2870e1679202b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751f30aeb4d8ce622ec890e019f35fa523206f26e6032ab349afeeda5adfa97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b003c5e5cb651c7980c5287a815514487f93b9978f06f13f458d760f1ab587c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataLossPreventionDiscoveryConfig",
    "GoogleDataLossPreventionDiscoveryConfigActions",
    "GoogleDataLossPreventionDiscoveryConfigActionsExportData",
    "GoogleDataLossPreventionDiscoveryConfigActionsExportDataOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable",
    "GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsList",
    "GoogleDataLossPreventionDiscoveryConfigActionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResources",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsList",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScoreOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag",
    "GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTagOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigConfig",
    "GoogleDataLossPreventionDiscoveryConfigErrors",
    "GoogleDataLossPreventionDiscoveryConfigErrorsDetails",
    "GoogleDataLossPreventionDiscoveryConfigErrorsDetailsList",
    "GoogleDataLossPreventionDiscoveryConfigErrorsDetailsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigErrorsList",
    "GoogleDataLossPreventionDiscoveryConfigErrorsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigOrgConfig",
    "GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation",
    "GoogleDataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigOrgConfigOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargets",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReferenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabledOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsList",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatternsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReferenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthersOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabledOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReferenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegexOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsList",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthersOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsList",
    "GoogleDataLossPreventionDiscoveryConfigTargetsOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget",
    "GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTargetOutputReference",
    "GoogleDataLossPreventionDiscoveryConfigTimeouts",
    "GoogleDataLossPreventionDiscoveryConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__17017175cbbef6972d623750c69242c970f50dbb50c2940e1de991c8c2b72a4d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    parent: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
    org_config: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigOrgConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__396bf6890e8f32ee43377e279335bb63c222c870c500376ac777701791d46700(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025dc68f8d8e990f8256577d65d9e0ebf194d23252a9d3ec1bafafab8140b5da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2688ad8e96b3ede07d4fb752a13f993f5682af1bdf5c6db1b120aa56d79d7251(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d20a8ce0b992d592ffa03b5e58355b5e04e5bf843981974529b64e52e34d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4ee45e7051891ae8c4ac546dd267d354b294647945768b5ab7a8c137e6d995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1731eeceebecbbf7f6ba238bda4f756462fa3d63f4865aacdac5b33c97664c04(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2503974cb27d7856acbf9178314ea5ad136d297f776f02cccd77ec08658b90a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa13cb30a97a943fe4930faa021be5942702eb685bf2ab8d0a4315e788843de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a2d62b500a92dec261ce2bef4beb945903f099fc3363de99352e9dcca59686(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027e9ea63e657620bea93ba5742d1f1bd90598b2bb40b10dabced1b2cdfac788(
    *,
    export_data: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsExportData, typing.Dict[builtins.str, typing.Any]]] = None,
    pub_sub_notification: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_resources: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsTagResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605398ab72b03d1be3597aa5511c6606bd671e7f0f219b4750ff79c3e14d6cd3(
    *,
    profile_table: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b916796605b608851182ce08f0a38366a51c4ba3f27693fe4dff49a0f7ffa208(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a0296fb6b0e074d1d3b66f09b976e1b2e69aa61bc18eb3d28688fb17988f39(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5abf469657807d1956c463be195ee28585c443cf949c9424cc6bebe00e3042(
    *,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fced3533cf5f388d768cd858ddc20f3fcbf5bd73cefa449e7372107ed6a1b7c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9463abd9c1e36bed633ad47f97093e1f77e503575731bd588ee63e71e92f81ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423e4064bc4d6f87d4ab03af128271b7a2b637a6825a34427a1b1937e6f6771d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d3755a331829b041f439e2ac8091d48a2cd4598e3df643ff42e87cdba15abc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c20a3f4f2d1b301ed7333040f894eaac965a5ca0328a89b3affbe66d377731d(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsExportDataProfileTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3ba9cf9503456a9a8723a0b1a40a54109fa49c5a8ead442ee66e7b28d4bddf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c8eae36d0ecf38dc93d3c2e8af96f2ed5081d35d3d6c8380bf96ff672742f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e39df8629be0c359a52d73bd29adf1da89f88070e2e64ed178e13b84fb8df44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32604be0e07583a86efa187d64b3cf89d0036498db2a546b9429215191ee0572(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c4327f7416efb1ea188a32766e2dae8febe57fd368513973acc87a71937fe4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29afbd3df522b1aac6fa0f30e671957b98b5d5e39e8ab3f3a46c2ac083f7d4db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aec5e1582659fc389092fdca06134b264863b3564e27da04f862ffa64aa73db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d07ff24f708f3f87edccb049c57541f6ed1836bcc09e14f7a9f8b924030ebc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d6f6263f9c37012a447f45e65a822fec2f96d1f086590d65b81cf0712a69be(
    *,
    detail_of_message: typing.Optional[builtins.str] = None,
    event: typing.Optional[builtins.str] = None,
    pubsub_condition: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4aff9bb3ef3f226990bdcf35986e2e573a374ec860cb8187b49ab10f0a184c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5f138555fb8060db9e7cb939fc371b011f0473904f3acd856a9cb5de2555da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe04f32c9d095c057f9ced3c13fa98be681df84506f84f96cd9dbfb2b87cfad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0eb75436b90c40f9d0ac38f991b0f59ee029cc86cd10cb18076191fa54a18f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07dbd143496a1e14a602f5e07b0dfd42b9c6bc620b473b07d7198f85ee834396(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca98b08cb349b93c98914f4d35d221514e89442aad3f9dcd4bb451485f00431(
    *,
    expressions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cd8627633e0f07e4f086b4a3a619ec22c801ea5f6853fea1970b1afecbb683(
    *,
    conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logical_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f39dd53c0be842d7543c1a3d14f52b87bd27c1f4944b96c0a1ba77bf1273db(
    *,
    minimum_risk_score: typing.Optional[builtins.str] = None,
    minimum_sensitivity_score: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f97e760bbcae69df4a64106c999c6cbe1049755be07cc4d6447fbb59e8adfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0812c123805e7e6030a4cd6001bce8be9ffd721fee3373c144b160762037b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b77d0e16f15ce5de305f0b5e4db719d1cb7a46099c73a56dc4c2d152c1b7eac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ff2e0cd469a2e825700c38f972c7ea7e163fbf6b95cf44f65876d2f47d8da2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0db5c264020bc7ff7cee7c82f7f54a8985ef1167a7d0aff43c66d5da11351c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75eff58f0c1db52c7730503c365c70056a3374603cd93fc3a6eb48ec9ccc9bf2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c076addbe945d3e05c6224193adbc2f6c7f9a79dd072788767ae31644b69dc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a1517187399c05268ca54bcea12c0e0a57b128da8e72d8c39058780e94f6e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4765d151ec5e759e334a8808e4b53f134ce92fb9b56c5bd7d998822a4d2a53fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d54c5d1e625d464d9b86f323358c95d91e0f3cab33cc6b95815c8a53b17089(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff994d44a17edf6adeb2e9c8fd3e08d1cb8641160144bc126a7b0c33ec141cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f33998ed93ec60203e7584bac9d1ba1dd71e8c1ce5293e912bff4376f4c9186(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dffec1d813c9ac8adcd164b8d0c694557424c3a2599857ea96720495fdd0139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfe4ac80f167dc5b0392e7c20ade692409cbd9149132ea6bec1f130f4490cc7(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0e53e72aa48615369733b7e294dce4ee0b15e9ed217164226432cbd661a52e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889c399a1381733a943276a1539f53982c7c55a70f43b02d11bba7a755d5c20d(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af34b6b750babd0d545a40e6353b474f812226b9d1fc8aeb5254c8cfb576e2f(
    *,
    lower_data_risk_to_low: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    profile_generations_to_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47110645cf2a512881a437d304a46971ae53385288a41d7053b75a092ee4e3f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0e65e806d74fdcd3b89c38693b8df5af4f59c1af7a4420126e689e74cfb04d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf102a1d91c596c594061ed71e753d294b000a8a51218187297f82d2bdc6cc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd559062063b634345afc33ef94a0b67158dfe07e9356c4b6ea10a1398665b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee046015e47932585d714100391cd7ff5d67375459041e9eae456eb79fad7cae(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6edc4f410f641ef8aba974f645d6aebabce9ac8892aaea6a5667a1ae9395e8(
    *,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    tag: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e487093abedc3ad89f7bc0d58c794078f05795cbc6817dd8f7d19c48c27f1a90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df17977296d3a101033b3c667e8f489e6675864c96ae4d13008f3811ed558e81(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbbcf7b2510cdc6a5cce9acc44f350db59d14bf7a3380905de7704607d9bafa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7115c5fa04d0c9a01d7e9b3cbd243949f6a8a2063d0df5e5a02eb3fb621def2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d78d3a90bbd3591a20716aa41b337c6108c9212784b25b13f90c1efb95db1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482b43c087b2f51b2dc975c1c5b998e54bc2af5777984b26f35ba3dd915a3360(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a9acc9519343cc73bb19f7466a88a31339b1806d4bda1b1af702904a4114af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ec7f31086fcdd6583b7724a4a79839dee47257571a880abcfa0dbdc6d2cd7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c863a884b8a56244f0b60ad25783991fb7e78b9325c6f7cfdca313bfe78626(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e3bb57b8dc1b8114224b4b04477e1598c3b56054f8047499a7a4f06cfbc35a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4686eada06998015887a01114ec0a47568e6e909edb7e914385d492a4988e67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9f50ca15526ffaaa53203d31479a6f1817de8d1bead42f07991f22c0308642(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3134418b4025f8646ad5f281f9d8a8b1985a170584be7ccc6cd33cc9911dde9(
    *,
    namespaced_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64a75fd16dd29cb1454a9d0577507b571004101da5f73f92bd07f693a8f8a6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5cbb2c9e8d43ce68f6bfa5de39e0af75c2f724d72d33dd43bf98781938fc88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646be84fa9bcf4fd942ad39b64be02d976e4f0c8fe47514eb826be1b90ce34c7(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigActionsTagResourcesTagConditionsTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a81cf1b45206eb7d29f082c785a8970d7012ce60f735f4e111887928321284(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    parent: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
    org_config: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigOrgConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e59f346e02f4df2556c315d06fb3011561751abb90eeff1eb2161a1c8a9506(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2af8d10aea6f4177570718a58952d05749a1c792b3297734a087a6208c237f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2b380654f34df34d42f80926b836629028e2bc1f29cf5cb411768c78ddc711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d579fcc537276fab8b987d676b0c2576b9c18ef649e6b3d33b1eeb2af27c91d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db67b59683d0c644ae0c68d9921bdea2ff6fc91f85d0c65de86b0e741ffc5ef6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41b5d1757f25b015f3b5c02272854e3c702d80e73e57cbb8d3bb3ab8d3c8964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb62ac1a4f7cfa611e43618ff477b1e690fa1f68f801653583a60075fdd4441e(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrorsDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb373634e36479240e14eab566dd8d3b334762b219171fd7c4cd64335f48323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d35a60dc76fcb17e486e5df6926da290f39c2afd1e60c6aa7e8139116be8fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3775bafb60f85fbac50389be81213b5829f55e35deb48be46770da5ec5e8bc69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37c79c56fa23c56b4febd0e47f66c61d34939eabc473a6d5dadce1522ad0b85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446ed8f919b57fded2feb208af43c52cda3ab4b3bd2fe72ffd4635e0a65d2544(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c16612a7865edbd5bd73fe463528054510a36d782db3355c23329b8bc0ca085(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf104d9a8a9c02f352290fe7e74489fd9e35894cc8fbcee61409ea2ff0a6280c(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f67d99bda50030abc58cdcb6a0550ace7cfe5158ffd3e42add1be9910263e93(
    *,
    location: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bf0e9bca5932049b338f501450e14c45f9a7cb75899f928d5bc971dad6ed31(
    *,
    folder_id: typing.Optional[builtins.str] = None,
    organization_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1428d2ca0c06d17e709e2a9379bb737534053a17aff31e1684f4333d9f454fd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f022a00b1f6e11a23583e6aff80bbcc429c7b06ed6c8e3905bbc116cac098d8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48121cdbd82fd1bf1fe4da0aabbc9d25580d154f5fd93e414b321dafaff1928d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73731032b78ce88923373e23fe23d5096c19a0fee5fd21de4e6652405db54cb(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfigLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da57abbc48ce002418cc96441456b9f34490cd599e09e5d405e64e96d9cae583(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29bdd211671dd6efac17d8ca42b6df12c8cc93477337463a6182fd2a98b488a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6e4bb06ea512c7725cab37c015375641d6841c9eb727ad844b59c3eafba5aa(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigOrgConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f677bae5f06a2996439afe124ea28848249066838ff483751222f3956bbb4fc0(
    *,
    big_query_target: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_sql_target: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_storage_target: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    secrets_target: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a568d873e30a04bf48b8e044dde0d7f02f43b451a4c7c51d0903b8056e1c0d(
    *,
    cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989fe62fd9bba6ace4e40815a0452a00d40b25bfa87ed600abb11ea4a5f0a1ff(
    *,
    inspect_template_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    schema_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    table_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3511b5d80bca40e3a3fcd91ddb868fbc352d19f00b9a01ef18db97a13e2d8b8c(
    *,
    frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5881cc540119e8c63372bae78699084b7c2d5a7f4b1173176bd500e60a3bc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a81ea3779a67e9f13c427e342dc5b5b7b89478e6ad6428861550da6813e35d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab17eae24c6c791f48189e0507fa0a981f1b8531e4f699a9f6bdf744edf24f2a(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceInspectTemplateModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc58fc329c3d7b3a70ebb825fb490a2e04ea2d36515d0e5f7b79d645f87e25f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5efe721785d6154bcbd4a70c496c124d2f286d8365276730e6299585b9e50c1(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ca09e0beaa6d9ebf272e6b417d5738ce441fa61a50c4415a6173faa20ad10e(
    *,
    frequency: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeca3338176c54105814c3409e0b17ae9b3ca60d4f663e539e580a1f61dab7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525560a19d18902a3a648bb34bf99051be71004db8a6b6cef8b5d298ce554401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a9c96fda350e29ad8c6b6ebbcf1d0ea6e4ef092bac3881219514c44b9b6384(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716a40e39af0d8d36980c490ecdf92fb153462b80a087ba7978b7edf5702c0f0(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262d78d98be5b48b820a0ef71d39269fe72d32c3033dbbb05b19ab61211ec0ea(
    *,
    frequency: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a72037140bea37e5044040186995854d7eaa53bb3ccfd112fd2e7e264bc403(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a2a0b7f4296dc0edc6056dad71c0e44cdf15ae8c8bd73d82b695114002207e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ee2521a00e475653b3613b35c749ab8310716f9e5b60b2a8aa4b41f3b086c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32bfa7e632d499d3820ad25dac843cb3130bb2127c94b6f2ebc02875de00a6e(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5bb45cb5ea98893ae54c30f21b26ec9524dcc8cd063a69886a3a1a160f6a53(
    *,
    created_after: typing.Optional[builtins.str] = None,
    or_conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    type_collection: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f17164d74bef34aa85bdca0a41fe5025aa311dbbe6950584be27fd6efc04baa(
    *,
    min_age: typing.Optional[builtins.str] = None,
    min_row_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf5dcb56fd0a2e7c4485b87138ca6dc980fe0daca5cca58e939185f6c409744(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8feab055971f57e17188e4f004bbb0a33bf9e8362d9489c2600ad6bec43b89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cab2cbfa722e5d7ebfe946db609bb72ffaa996ced1e5ec57a71fffc21d73827(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e425c555a843e1ae137f3d0b4c51e9f873020abb7fc360032b7c61eac6030084(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade237e3877c9635d4da6d970c7234fbcc02d0524ca3d6e996aa6d4c68ee5323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774bea999310d976a6661575c250f083251e516912ecb1a8fe47f89f09e2f4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeaff3a51f7e902515b67559cf826d821918d443284d547bd822d3b6093e0dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40698823796dc965aef335d63577f8c3b90f00c995600aa12979215bf6cc4fb6(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc9b6804cd75ee37f2a54a0d8ffd961c24cec5eb676ac778d399f3bd9de05f0(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ff35395b4b12cb3d3e81ced9d99ecff2f3cc74f859b7891943d14ca0397f74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70175d37bb90b71f7e03224acd25a91206f0abe8db8b4ba0c5ed15e92785e31c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b4c58f1b9b1634ff14fcf1aaa1e8233fb31dd0f4ec7fd3ae5e7bc2cc8165af(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c498df72fd641b21fc7db952e9a7815696d6fb9bf0b684025672946b09c55146(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5b01a1e25d5c9e6f69ef76efa2025616b8a10f1915bbff15bd7b8542249a28(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db3fcc37fcd0ce19189e8bf3d2991767ba95b282e26e314bf1a458ce46d812d(
    *,
    other_tables: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables, typing.Dict[builtins.str, typing.Any]]] = None,
    table_reference: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference, typing.Dict[builtins.str, typing.Any]]] = None,
    tables: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3296be49cadb2845f4ed079a79a2ce6f4ec07ea95897c388427df3aee40ee4dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983e31e205a9e2a23fa20c2ed088014592d4e60070d5d6590870368ca0bcf9f4(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcddd13933f6f1ad2a11244d0f5a8167337349c49b9ad6ca0f8c8b1b04df6a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9424a8c456515094da2ac4b0bd7bee952019cf5e1f87da82c0aec6605ce3202a(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725d768e974f25c014066fc8b909aeea4bb0e3554d6af0f3080ffd356e67870d(
    *,
    dataset_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0c6f87a085a15cd1b3ebe66c44ab1e0c37b09e91d113bb5326286ee3e3ddd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f74cabe6431dc648f03e86556f8804dbf84a41b6393e3532c9b6011afb546b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428dabfeadcdcdd91fab4aedeb4753741bcb33aa00169eb3776b2cdaf397b814(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e5699ae711ad5488975df269a083456e35edc3a01ef80c9766cc94bda42fac(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTableReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4d286c83b07b2c23a5acd8e4ea49e531ddce637df745d94e05f8e676ad53a2(
    *,
    include_regexes: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cbfc772ee82c960e8a414e72c63338396573eb656b08e9de5c82f16bb2a73c(
    *,
    patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd6b65cc124f3f7d4f6d0f27d61cbbfa237ce0940094b6b78234517b734b57a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fa9d67b28f3864769888c28bfadd6db32c048601114ad0445f7dbdd4940904(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a121bedb4ce4b27d1e7a5cb3f45e3c3a671806e0d9118fec61e607b97af6f774(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0778416aee23d1f8571d5fc023141f7e508114263b767b8cae9782781bb497f(
    *,
    dataset_id_regex: typing.Optional[builtins.str] = None,
    project_id_regex: typing.Optional[builtins.str] = None,
    table_id_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a9b57bd46b2c27af8439acecc5a23e32c3634315a0cf4e0c4ebcf9866210aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fdb0efdacafbe5a075872d9362248cf481716cfac91ea6969e1fe5dcc8eaf6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358662f19880c0b40c526cdb804708c66a5163dd850f2014c5b4965a58337396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258da9903e4d2e1a3b5971d601644427b1c4afa41c3cf2815f32c1743c7a47de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a560de17a3bf3983b7a0b0bc661c70131e7e52a806a7d779e3b6943c510c4966(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88b49a2cfe73ab585e8fa2ef7bcbdf08efde25d30c0e259ba3950fe7fad5de9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3c3fabdd89275d62f276cb9498b9cea7a340c2db876f4b87117f2e9a6dddd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0726279db8249a466136fc4cdcc4df94e5ee798165657cb19039d202fa21e413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc1a342e5ba6c3b0ee4877435a637abbef123713016631cc3a60160908e9f8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43afde8ad4e700022edd1a728cffff441733e8b65d3687d90402235b5f936052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b877252149621d298b69470bf55e79173b84af95dcb20ce762ed9fe604e1d942(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f66960264acfd2a2edc53dd022c167da0dcd1ccd90f442820b96955b4d343bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282dfc73bb837b9c49693b13ebf1c4d6bbf674b12ff024d8a9819832c9686285(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfd6fc542be97edc3604455c5f3d38453a7eb4e5eba33c53bbd47e6ba5fcebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf69c1d222fd7c06ebfb320f00524797a2826d81a8ee87f95a86b185a7fa71f1(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsBigQueryTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f007967582d4a65ff83c942926aa53410a85187cf1f9a98a603a941606eed001(
    *,
    filter: typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter, typing.Dict[builtins.str, typing.Any]],
    conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
    generation_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8633ed03271c4d685dfde297e830ab680d1f584fe2e8ee28b9513847749320ea(
    *,
    database_engines: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbdfc2874e15fd4698476cde0490e14d627fe19941ff4d00090724ffc19a2d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e8556f9d578c7936e0e4a30a8aebf75a2b8725477fb935fb21996343ec9258(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fe8f52519e4578861f77423c818d1e77fa6430b0f670d547cc25151aa15269(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3c3c57593a0e1152dfdc8c3e2b2e33ae41deb53a4ae401d4b27eefdb73030f(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04082c3aa15b3cd7063b9bb770b522e0c9d52704837533c068cf69156f372264(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9f1d91a9c13df8ed81340e7996272a20aad05c2b52667e72a1cc26a9035b95(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetDisabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a96776277121b2a3f16e77e20fdb45f1f140677b7a7cb8b0a6b0fcb516cd2e5(
    *,
    collection: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection, typing.Dict[builtins.str, typing.Any]]] = None,
    database_resource_reference: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference, typing.Dict[builtins.str, typing.Any]]] = None,
    others: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb6b5c9a59492de5827e77366fd2561547f5c884f88eac2529d1883b152d5db(
    *,
    include_regexes: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dfe570c7a7dd1f0cd06709f77b58c3e3fb9df76e23ac543e771c422d48e03b7(
    *,
    patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23bb900a245f1232eadf0eb6dfa1596ddd76d945409933c21b7f046d31b895e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e69385fb57651a4a82dfa437af65a28a3774a195d8735c413b0ae61748a0286(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbc0cc3570a63aabfb1c3bd95383709b6b7d8fffdd3f8bea46a487f025809ee(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cd2cae3bd966d7d7618c8e083454dec4dd179ab0213b57f429ee9db5455584(
    *,
    database_regex: typing.Optional[builtins.str] = None,
    database_resource_name_regex: typing.Optional[builtins.str] = None,
    instance_regex: typing.Optional[builtins.str] = None,
    project_id_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47fcebf64c73f3567702b2bdfc333bfdfe784bf72894fb8e1bea772e442ab53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8acc6739b96512fa03ffdd60205d573623d25c95c6bac09ab76d17d3b8f09180(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80047867519a66eb08a13d3e331c869bc96ef744e603e366a133916830a55cb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9ac3dff21a4ebb763df9aecc9365d9afde6926059f824b8c561d453a785da3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c011d36c4b4382ee30a6c3995399cc5fe49703b1efd81703e162eb13786ded08(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c62c84bc90487e4af31eda794c6e7eeb1feb1ea80385766cbfdb57578e015c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e40660266264934365e4823df5a6ffb5d6dc71cfaa4e1a6d66184d85ad95b4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0954a3b881f199a7c2e81ae4d5fad3291ca2b0a0d5670c7920f4ffa183e342c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e57ba30a807e9329751ea037e5fd06a2bfc9dd226d3b99d5ad14504a21692a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4976da4791fd033d223b846bf70d0fa42ca7d654b74c2c4997a4355a3c159882(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25468de6f7de97ee57e82e7845fc64e73570a5fd3e547192e624cd3a8f9c923b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d653f6e00fafd6e0e40a578a9d2175d0008ee246d108f1971c8a572b715f3eb7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollectionIncludeRegexesPatterns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e606d0cafe0bc85d83d9e135a03b7e82427659ffb031ef6c79c10ea3fa0747(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf43506d4e0f4674def50a240b2431ae9a4160d028197ab0568de2c7e4ec800(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterCollection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f7d27da1f3745009821ed1e6c32209a8c60fabf176d08a079bfc4c5620ae4a(
    *,
    database: builtins.str,
    database_resource: builtins.str,
    instance: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19caa61ecd962eec5aa390639ded27a8e5ec6911c412a5b8df2a6837d5ddbb5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cacb371e026610b8c1d41e0cb37717d77b5a1915df596639b383af86f41eb08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1772f1384560b8a5c7c6f8b3748913159e93560b88db2ed167a59d8e2b161996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cdbfb0e70e7a1a665311f35a2b620142086895f353663eb3b071d99da3f1e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a678074f0001ca122ac44707853f0f283305bc95a7b280d85ad9eda0f011014e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778c5e654d21569b0954ab8621d84ea2d1da8976c458c2981aaed37459b7cf93(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterDatabaseResourceReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5afc56a18a9d66fae34ffe45a2ebcb89aad3ea5f7b378af028015053648003f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67b1f2258d47b1b40110d805e0126f37a677c408548c198491b8b48ac533ee6(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilterOthers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816656631e49b5f77a34773e192b994f6982768da86cc9bb433c9b61e1cc51c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcef39956edc31124d5805a5c8f2e83989ef35f4c75000f1ff4b0fc7f2d0fc2(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d6363db822313e1d8ef47bf5526b19de8d53a5067888fa67ada0d84d6b0126(
    *,
    inspect_template_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_frequency: typing.Optional[builtins.str] = None,
    schema_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b26c74b95b5aea6f6ac57040e7e839b35d6bc524e2b054b2a767774ba272c48(
    *,
    frequency: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06ccd8e881d41574578aee7472bd72835161505c65e4a4456126470575445b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0268852cb7f603d2ee86b5800ec26acef85cc7b5f54caec5fde393251f657bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0f0080eb875e3504cad7899c8d2876d9ef4bf79f15f2e053b817ee39e05bb1(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceInspectTemplateModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c917f066697c323fbb86f3deaa5de0374ac3107c18283a5f9bc8d4b10f13dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa552a0fa7fb89ae7712127db31130aa68e55cc2d11d0b33749ac2dee745e02f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec86e4dad99150d5d9f0506a20b63f553f7ee3b33fd69ad1e767e8cf68ad848(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ccb7621682c160bfb340f75e711c12df83d52064fe458edb4ad8d3bba08cb8(
    *,
    frequency: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6e1f2c26b65f021ae9be62e4042a4c187dedcad45690ea5035a34885f3ee29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d041ad58e2f06ae9568238b52afb50cfbb5ec282f32b9a4095056ac559a48b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f42f54993274695554b537987b13b24aea3021d56382b79ad8c01624b38643d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087b56a508154c58bb460739c2cea9ad4ccc0244afa4114e039542a4233ffb30(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTargetGenerationCadenceSchemaModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452805636f74515cf69f53ac503964b4c0d83b18c1da016f1a65c8d6a39fcc20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebbfaf0d56e71e5933dbae3ef227b52bcf2b858b1e454852d717e821f210469(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudSqlTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96f9017eaedf31ec3e05e3adea7569ac267ba4e6d3947d28c1cbd8c5aed5d08(
    *,
    filter: typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter, typing.Dict[builtins.str, typing.Any]],
    conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
    generation_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b477e5a28edf420a04381fdb2f8914d513ffddb34c588d387b93a925d7b2fba(
    *,
    cloud_storage_conditions: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    created_after: typing.Optional[builtins.str] = None,
    min_age: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fc0f2c151fd9848e40b12dffee5efd62e66e8f29f039adc4574cef838a3243(
    *,
    included_bucket_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_object_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b61e27eaa10ce8989a8ae7a9aadc381b1c10102889d70b07ee6f1edc8f3402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758dd5439c8111740b9614511557eb2fdc5fd33252dd73849ac616da0b90aa12(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1150bde177a4985e3f85c588e6187ddd1e4ebb7b8159761d533a13feea0b146(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da82ce9787e679c479c0275327e42fa471ec47142a0d47f8033ffd8619465a6(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditionsCloudStorageConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108138c613647f38ec0f901065eff716b639e5c28f0b47f9ff1a868b4f4608f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0e21418d7ce5cb8fd478bc6b6bc8322fbf63a6f659986ba0a3ca2e64a56ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efebd95fbf756de27e0436ec8ca3fea1da78a9aca356bbd9c7e0413e2c4319fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851011406d9324e03f5f2bf2e117a82e6854f91d7e5b8fd956bf90977e58ef08(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516fd5cae23a1867c481631dc7c86c0ca8513d2bfd66ee4947bb10f6864028ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27e9c323fff64502d588b8a33c1d8ebed092050c3a0a58e80aec82f95f9a777(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetDisabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3ff4197b8b62f0d730cc63ece750b72e772f2dc6e3b785687e6018bac76ae1(
    *,
    cloud_storage_resource_reference: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference, typing.Dict[builtins.str, typing.Any]]] = None,
    collection: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection, typing.Dict[builtins.str, typing.Any]]] = None,
    others: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0900d81418252780698338f20b2271bdb8b4967128d715e6475700d5f1df5697(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369f5a77043c3e55e1e212cc7e13b44e5fa52f2fbe0d6d4be68b700895f225fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07a73be561340e66ca83ac8b3ba418407df65ba909a1166f0e4e223f1ec7eb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2796069f30c64654af9d561dda740957d86fcfbf5a080c6e154265cdd98adccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff12b25917dca010b2972b948ca779174c9f2dacdf17a9e1625107acc0e847f4(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCloudStorageResourceReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9e92edb10641eb709b8032fb6198ec8671ff0a5434f4b8f998681804ef9352(
    *,
    include_regexes: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516449f6f6e1b40f72105cc449f60c3547e03d0a91fbe34b13b8168845f80099(
    *,
    patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4806ff96541d4db54354087178838634f271a5f9fb76f5981ece5decd4ca7275(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e099aa55256801c132f9912934d921d1d2a56c53362f9bf35874686142a11b8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55453ae35abe547d39052fe5e34477f5762931cd23253719c4ff4c97fc57b35c(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2538f2e73dee3bdad77425d048bfc2c5e3a79680661ee216515da52422aac596(
    *,
    cloud_storage_regex: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f135e1b11cab34b046889146531169f08fcdd9a6a69d6c626da31080df21c5c3(
    *,
    bucket_name_regex: typing.Optional[builtins.str] = None,
    project_id_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdd7ddbcaac16740ca105335d689b1469b2af1404f67511b6b2b1302e475754(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92486ae3b3b40273de6c4975b13624c9eabaceb0a1cdc27c0df1487d74e1612b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cf22da293de2d31b8993ca1eb8edb68916f5cf150451781859ccef473148f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d4de8a3b3c74af46b8c08cb01db3d0f91967a18ec760fce6d47e390eedfc0d(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatternsCloudStorageRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219657d870ff66131309ffe15531329d874ba52f969f37bd812c1a15d6033d67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27282426f39f72536423dfb1cddf84c396d6db3f82df54d956f07a9c99d7ccf9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61f9c4bce590ee93874585f402262e3596e946efc6c8b9a3ef1f3ef30cbe701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29bc200395056bc218e528000d8b132c41787028b0b0fbb2e3069aafd8adbcc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d348859a97677c89bb7cf28f08368160883e34d381af836039ddc056907dfcc9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b9f67c45748f1f267fe767a835b89464088ddbd7b5d017f2eaa76a01322e7e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a692e8c26b6e4d818b41628fdb85149813a606418b881d7167e4209a220c36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85353cca78caaf8c093a1fbbf40020311d62b4822d47d28e4167428b5e363e9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollectionIncludeRegexesPatterns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146b2c7919342dd8c4ef32296fd8be7cbad123c31d640459612c65ab51dca31d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ad08627900afd1ab881b7694c098e0f48b607976ac0685306521c58ed17c24(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterCollection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92df40694937d1406d53cc597eafa12df099fd113647de3eb67a05bd32ef513(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47dac4f57f16dc6eb8891072bbf0cfd2358bbb23ae6068a27180e45a19b9699(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilterOthers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a698560648e46d39b09d669f079adae257c7c433782f8c117bdf26e508b770(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7763328ef3f3aa32b70001c86fc437cad9959b5b302c77c1cb1e86f49149f175(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca62bb21f20aee07e047f5c026a03091937654a0d3506c17a08b7db8bb91392(
    *,
    inspect_template_modified_cadence: typing.Optional[typing.Union[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52185909ef41b9a1a3532482ddd3e4aa90ff44c82437616c47744e79b55ea0d1(
    *,
    frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b1c8268ac4b75ecc1665d11baa97f6f6c97697e10fe39460f07d80a5e1c9f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1410cab40e94f9961b3d4f4acd64a45195c54cf0d37321310b325bb6060173a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9a8dd7e4088d77d0e66edd723793c6873983612fc4060f18c54d7e282dd8f6(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadenceInspectTemplateModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb417eaddcea96149697c9d5b78c540caa713894356338f4a12c55f236a8bbe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31385362c013476ace3bb75e96b3d8096f8cc8c2ba0bb15d0cd61c0c5e0a2668(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fd392154c6b3e7dead277b4eab9f53fa6cf993bb4783d683ebc6f97afa647b(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTargetGenerationCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3dad2d52574e083359e311cbfbe6ad8d92a2a8c6925da1e498a7f52aa17950(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4e8c4df01b63aff4f8e5a6b5bc49c089754a4fba9ce9ed154877b81ae01e37(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsCloudStorageTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4b92a7343c9ff692b73ade8323da5bde3744571432a89ea57608191eccf1c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c20183f6a62524b6b040feeda0124461a38d4ad27f945a3ac68f52e61ecc0b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a4253d5d74e8006ed4c85d3df8213a3fe6b53f1f1de373697ae0eddc2550bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cfda5044e614f35ef71381495e2f9ed9cc6efe0bf1b7b91c31cca832df5b8b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a3640700bb63dde13b84fd68832133a5fdbebe26ddbf9920256ac81377cbfe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d21f86975db9500aa9ca994d2c74c1b663000cd55f3dc7d176d80af447355f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionDiscoveryConfigTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c228652eacde274e58e9658a7151f5d8e3cfe78dd6e3140e298fdf3bcf8dd3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c670c2cd08772a8c7676cb76415de6aafcf808887a58a1af76740edc39f8b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe357628b17fe0ae6c9c07e8711dd32c89540aeecd914e8fa4588c95ec476be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a32b3a3a43c0da4d9494a60e21837e041e70f033dc09fae2eb11077d0242c55(
    value: typing.Optional[GoogleDataLossPreventionDiscoveryConfigTargetsSecretsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b816fc5875210e2a79a0ee964d8d61f0184d7fc17cd3db8e853c7fbceb96cd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45cba7b910baebdf822b1eee5b6d7eed0cf6863a04a899d2ff44c79b242969c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934401c3b84eec3c69bd6fb6e885a41af20f22be30543ab40b43cb8da273b2b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c9769fc133e34c3a92aeec4da9e96a82f6caf5b1c64eaaada2870e1679202b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751f30aeb4d8ce622ec890e019f35fa523206f26e6032ab349afeeda5adfa97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b003c5e5cb651c7980c5287a815514487f93b9978f06f13f458d760f1ab587c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionDiscoveryConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
