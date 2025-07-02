r'''
# `azurerm_orbital_contact_profile`

Refer to the Terraform Registry for docs: [`azurerm_orbital_contact_profile`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile).
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


class OrbitalContactProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile azurerm_orbital_contact_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auto_tracking: builtins.str,
        links: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        minimum_variable_contact_duration: builtins.str,
        name: builtins.str,
        network_configuration_subnet_id: builtins.str,
        resource_group_name: builtins.str,
        event_hub_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OrbitalContactProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile azurerm_orbital_contact_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auto_tracking: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#auto_tracking OrbitalContactProfile#auto_tracking}.
        :param links: links block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#links OrbitalContactProfile#links}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#location OrbitalContactProfile#location}.
        :param minimum_variable_contact_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#minimum_variable_contact_duration OrbitalContactProfile#minimum_variable_contact_duration}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param network_configuration_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#network_configuration_subnet_id OrbitalContactProfile#network_configuration_subnet_id}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#resource_group_name OrbitalContactProfile#resource_group_name}.
        :param event_hub_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#event_hub_uri OrbitalContactProfile#event_hub_uri}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#id OrbitalContactProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_elevation_degrees: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#minimum_elevation_degrees OrbitalContactProfile#minimum_elevation_degrees}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#tags OrbitalContactProfile#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#timeouts OrbitalContactProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39deff242aa5c6a38243dc3e1fcbacca86de15e35910d701c352dc3db0d6f6c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrbitalContactProfileConfig(
            auto_tracking=auto_tracking,
            links=links,
            location=location,
            minimum_variable_contact_duration=minimum_variable_contact_duration,
            name=name,
            network_configuration_subnet_id=network_configuration_subnet_id,
            resource_group_name=resource_group_name,
            event_hub_uri=event_hub_uri,
            id=id,
            minimum_elevation_degrees=minimum_elevation_degrees,
            tags=tags,
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
        '''Generates CDKTF code for importing a OrbitalContactProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrbitalContactProfile to import.
        :param import_from_id: The id of the existing OrbitalContactProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrbitalContactProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9fcda313c8e3e43d97cc93a1b6a1f2c6fd1575e4e705d1967da74e68cb72256)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLinks")
    def put_links(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6895a0fa03aa1f99619d595a476f5cf0702d6eac481041c9282446b22814f80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLinks", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#create OrbitalContactProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#delete OrbitalContactProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#read OrbitalContactProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#update OrbitalContactProfile#update}.
        '''
        value = OrbitalContactProfileTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEventHubUri")
    def reset_event_hub_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHubUri", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimumElevationDegrees")
    def reset_minimum_elevation_degrees(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumElevationDegrees", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="links")
    def links(self) -> "OrbitalContactProfileLinksList":
        return typing.cast("OrbitalContactProfileLinksList", jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OrbitalContactProfileTimeoutsOutputReference":
        return typing.cast("OrbitalContactProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoTrackingInput")
    def auto_tracking_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoTrackingInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubUriInput")
    def event_hub_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubUriInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linksInput")
    def links_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinks"]]], jsii.get(self, "linksInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumElevationDegreesInput")
    def minimum_elevation_degrees_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumElevationDegreesInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumVariableContactDurationInput")
    def minimum_variable_contact_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumVariableContactDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationSubnetIdInput")
    def network_configuration_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkConfigurationSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OrbitalContactProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OrbitalContactProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoTracking")
    def auto_tracking(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoTracking"))

    @auto_tracking.setter
    def auto_tracking(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac05a98564bb751a68b31dd22f923a6719acf26a9e9fe627d430ad0bf4b140d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoTracking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventHubUri")
    def event_hub_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHubUri"))

    @event_hub_uri.setter
    def event_hub_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55c6ad098aca455b57bc670c85666164fac20a583f4efcf5f0b8b19897216b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHubUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66dbc43d2186b2d903d47d3b416b345b7fb9e31aa29c5ccab521489640d3b1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c7222653c118760ce7499b2ffaeaa8ffa6b5ed543cddddea06ef60bb4294ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumElevationDegrees")
    def minimum_elevation_degrees(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumElevationDegrees"))

    @minimum_elevation_degrees.setter
    def minimum_elevation_degrees(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc2e109a940f78fbd2237acad1c9ce72576e74c46097a2e543f18047b3cf0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumElevationDegrees", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumVariableContactDuration")
    def minimum_variable_contact_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumVariableContactDuration"))

    @minimum_variable_contact_duration.setter
    def minimum_variable_contact_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ad8867b71cadfb1b68fad8d014c45c38a008742f458962370570ae9e594c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumVariableContactDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28bd9b81140cc0e8a1627218abadb66b6f4ac3b6266ccfde2a7ab02abe28c563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationSubnetId")
    def network_configuration_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConfigurationSubnetId"))

    @network_configuration_subnet_id.setter
    def network_configuration_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d848c106141f90d5843c2bd5c3e5211beae874a435f888425e6ab420194f111d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConfigurationSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d49532fe123d0a75bd5a4bdf2ba374bb46b0d868aacf1dd6b2c108714d59d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354f551f319a5e81735f2d7519c136788f11fd843c6b581e802095b7b3e3dfd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auto_tracking": "autoTracking",
        "links": "links",
        "location": "location",
        "minimum_variable_contact_duration": "minimumVariableContactDuration",
        "name": "name",
        "network_configuration_subnet_id": "networkConfigurationSubnetId",
        "resource_group_name": "resourceGroupName",
        "event_hub_uri": "eventHubUri",
        "id": "id",
        "minimum_elevation_degrees": "minimumElevationDegrees",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class OrbitalContactProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auto_tracking: builtins.str,
        links: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        minimum_variable_contact_duration: builtins.str,
        name: builtins.str,
        network_configuration_subnet_id: builtins.str,
        resource_group_name: builtins.str,
        event_hub_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OrbitalContactProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auto_tracking: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#auto_tracking OrbitalContactProfile#auto_tracking}.
        :param links: links block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#links OrbitalContactProfile#links}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#location OrbitalContactProfile#location}.
        :param minimum_variable_contact_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#minimum_variable_contact_duration OrbitalContactProfile#minimum_variable_contact_duration}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param network_configuration_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#network_configuration_subnet_id OrbitalContactProfile#network_configuration_subnet_id}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#resource_group_name OrbitalContactProfile#resource_group_name}.
        :param event_hub_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#event_hub_uri OrbitalContactProfile#event_hub_uri}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#id OrbitalContactProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_elevation_degrees: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#minimum_elevation_degrees OrbitalContactProfile#minimum_elevation_degrees}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#tags OrbitalContactProfile#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#timeouts OrbitalContactProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = OrbitalContactProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f75005285a6add60f72ca34ae53faaef01ae899497a2f85860be8965984afae)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auto_tracking", value=auto_tracking, expected_type=type_hints["auto_tracking"])
            check_type(argname="argument links", value=links, expected_type=type_hints["links"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument minimum_variable_contact_duration", value=minimum_variable_contact_duration, expected_type=type_hints["minimum_variable_contact_duration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration_subnet_id", value=network_configuration_subnet_id, expected_type=type_hints["network_configuration_subnet_id"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument event_hub_uri", value=event_hub_uri, expected_type=type_hints["event_hub_uri"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimum_elevation_degrees", value=minimum_elevation_degrees, expected_type=type_hints["minimum_elevation_degrees"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_tracking": auto_tracking,
            "links": links,
            "location": location,
            "minimum_variable_contact_duration": minimum_variable_contact_duration,
            "name": name,
            "network_configuration_subnet_id": network_configuration_subnet_id,
            "resource_group_name": resource_group_name,
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
        if event_hub_uri is not None:
            self._values["event_hub_uri"] = event_hub_uri
        if id is not None:
            self._values["id"] = id
        if minimum_elevation_degrees is not None:
            self._values["minimum_elevation_degrees"] = minimum_elevation_degrees
        if tags is not None:
            self._values["tags"] = tags
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
    def auto_tracking(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#auto_tracking OrbitalContactProfile#auto_tracking}.'''
        result = self._values.get("auto_tracking")
        assert result is not None, "Required property 'auto_tracking' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def links(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinks"]]:
        '''links block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#links OrbitalContactProfile#links}
        '''
        result = self._values.get("links")
        assert result is not None, "Required property 'links' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinks"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#location OrbitalContactProfile#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def minimum_variable_contact_duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#minimum_variable_contact_duration OrbitalContactProfile#minimum_variable_contact_duration}.'''
        result = self._values.get("minimum_variable_contact_duration")
        assert result is not None, "Required property 'minimum_variable_contact_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_configuration_subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#network_configuration_subnet_id OrbitalContactProfile#network_configuration_subnet_id}.'''
        result = self._values.get("network_configuration_subnet_id")
        assert result is not None, "Required property 'network_configuration_subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#resource_group_name OrbitalContactProfile#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_hub_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#event_hub_uri OrbitalContactProfile#event_hub_uri}.'''
        result = self._values.get("event_hub_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#id OrbitalContactProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_elevation_degrees(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#minimum_elevation_degrees OrbitalContactProfile#minimum_elevation_degrees}.'''
        result = self._values.get("minimum_elevation_degrees")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#tags OrbitalContactProfile#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OrbitalContactProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#timeouts OrbitalContactProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OrbitalContactProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinks",
    jsii_struct_bases=[],
    name_mapping={
        "channels": "channels",
        "direction": "direction",
        "name": "name",
        "polarization": "polarization",
    },
)
class OrbitalContactProfileLinks:
    def __init__(
        self,
        *,
        channels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinksChannels", typing.Dict[builtins.str, typing.Any]]]],
        direction: builtins.str,
        name: builtins.str,
        polarization: builtins.str,
    ) -> None:
        '''
        :param channels: channels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#channels OrbitalContactProfile#channels}
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#direction OrbitalContactProfile#direction}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param polarization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#polarization OrbitalContactProfile#polarization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456ff9b0e6f776a6057481678b8b7f08dac0c2eece07c0bf65f4f8bb25c490fd)
            check_type(argname="argument channels", value=channels, expected_type=type_hints["channels"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument polarization", value=polarization, expected_type=type_hints["polarization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channels": channels,
            "direction": direction,
            "name": name,
            "polarization": polarization,
        }

    @builtins.property
    def channels(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinksChannels"]]:
        '''channels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#channels OrbitalContactProfile#channels}
        '''
        result = self._values.get("channels")
        assert result is not None, "Required property 'channels' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinksChannels"]], result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#direction OrbitalContactProfile#direction}.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def polarization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#polarization OrbitalContactProfile#polarization}.'''
        result = self._values.get("polarization")
        assert result is not None, "Required property 'polarization' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileLinks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannels",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_mhz": "bandwidthMhz",
        "center_frequency_mhz": "centerFrequencyMhz",
        "end_point": "endPoint",
        "name": "name",
        "demodulation_configuration": "demodulationConfiguration",
        "modulation_configuration": "modulationConfiguration",
    },
)
class OrbitalContactProfileLinksChannels:
    def __init__(
        self,
        *,
        bandwidth_mhz: jsii.Number,
        center_frequency_mhz: jsii.Number,
        end_point: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinksChannelsEndPoint", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        demodulation_configuration: typing.Optional[builtins.str] = None,
        modulation_configuration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_mhz: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#bandwidth_mhz OrbitalContactProfile#bandwidth_mhz}.
        :param center_frequency_mhz: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#center_frequency_mhz OrbitalContactProfile#center_frequency_mhz}.
        :param end_point: end_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#end_point OrbitalContactProfile#end_point}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param demodulation_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#demodulation_configuration OrbitalContactProfile#demodulation_configuration}.
        :param modulation_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#modulation_configuration OrbitalContactProfile#modulation_configuration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da9881c5348b59c757ccd7e2075b85a2c13e1bd693227155c3f930ef1a7a574)
            check_type(argname="argument bandwidth_mhz", value=bandwidth_mhz, expected_type=type_hints["bandwidth_mhz"])
            check_type(argname="argument center_frequency_mhz", value=center_frequency_mhz, expected_type=type_hints["center_frequency_mhz"])
            check_type(argname="argument end_point", value=end_point, expected_type=type_hints["end_point"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument demodulation_configuration", value=demodulation_configuration, expected_type=type_hints["demodulation_configuration"])
            check_type(argname="argument modulation_configuration", value=modulation_configuration, expected_type=type_hints["modulation_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth_mhz": bandwidth_mhz,
            "center_frequency_mhz": center_frequency_mhz,
            "end_point": end_point,
            "name": name,
        }
        if demodulation_configuration is not None:
            self._values["demodulation_configuration"] = demodulation_configuration
        if modulation_configuration is not None:
            self._values["modulation_configuration"] = modulation_configuration

    @builtins.property
    def bandwidth_mhz(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#bandwidth_mhz OrbitalContactProfile#bandwidth_mhz}.'''
        result = self._values.get("bandwidth_mhz")
        assert result is not None, "Required property 'bandwidth_mhz' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def center_frequency_mhz(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#center_frequency_mhz OrbitalContactProfile#center_frequency_mhz}.'''
        result = self._values.get("center_frequency_mhz")
        assert result is not None, "Required property 'center_frequency_mhz' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def end_point(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinksChannelsEndPoint"]]:
        '''end_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#end_point OrbitalContactProfile#end_point}
        '''
        result = self._values.get("end_point")
        assert result is not None, "Required property 'end_point' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrbitalContactProfileLinksChannelsEndPoint"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#name OrbitalContactProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def demodulation_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#demodulation_configuration OrbitalContactProfile#demodulation_configuration}.'''
        result = self._values.get("demodulation_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modulation_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#modulation_configuration OrbitalContactProfile#modulation_configuration}.'''
        result = self._values.get("modulation_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileLinksChannels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsEndPoint",
    jsii_struct_bases=[],
    name_mapping={
        "end_point_name": "endPointName",
        "port": "port",
        "protocol": "protocol",
        "ip_address": "ipAddress",
    },
)
class OrbitalContactProfileLinksChannelsEndPoint:
    def __init__(
        self,
        *,
        end_point_name: builtins.str,
        port: builtins.str,
        protocol: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_point_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#end_point_name OrbitalContactProfile#end_point_name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#port OrbitalContactProfile#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#protocol OrbitalContactProfile#protocol}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#ip_address OrbitalContactProfile#ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b623091cdd1eba66e0e07fe4645b546fb819b85a6a9b780fff09c2300b594500)
            check_type(argname="argument end_point_name", value=end_point_name, expected_type=type_hints["end_point_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_point_name": end_point_name,
            "port": port,
            "protocol": protocol,
        }
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def end_point_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#end_point_name OrbitalContactProfile#end_point_name}.'''
        result = self._values.get("end_point_name")
        assert result is not None, "Required property 'end_point_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#port OrbitalContactProfile#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#protocol OrbitalContactProfile#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#ip_address OrbitalContactProfile#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileLinksChannelsEndPoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrbitalContactProfileLinksChannelsEndPointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsEndPointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de5cc00d333f05f027480fecb3d7539ade63369eba90835da01343f33e85aa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrbitalContactProfileLinksChannelsEndPointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab131cbcc41f6616d16ffc9a738c4d4c393f29190ad77a8ebbbe0c60bd35e9ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrbitalContactProfileLinksChannelsEndPointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25f0226188c49e009f22d71eae0d9d459d2ca118d65c6630c8c98660efb879e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1143221d57f1fd598adefebd86399b78138391bc10bc70304f7b607454524ba5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00a02ef204c0640d1bd5cfdbcdaef463e90cb79e7b5918e1ee31fea28c060b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30134c2cdc1acd22bba3628900f63679c370416c505965a7b33bbc77e2a912b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrbitalContactProfileLinksChannelsEndPointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsEndPointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd2a926f1d534a0e661334c380e7a19f5dbc16e11b8a09699239e86aa517f1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="endPointNameInput")
    def end_point_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endPointNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="endPointName")
    def end_point_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endPointName"))

    @end_point_name.setter
    def end_point_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f40dd198aaec340d8f3d1dd0f2f16445f5f22c7a5f644ad7386dee24bb214fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endPointName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189a92dd4bb45906c19077388424e6014180e28aba64101967b30fb83a362fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da129840c04ca0ab2c88457c633772b126984955933909a0045f9c6ec349ec55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e1719e7442d97ee11385b3daeb2aff928a41e4a36101a174d4ab46651db87d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannelsEndPoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannelsEndPoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannelsEndPoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55d4b5e5738501f3c1b6419d77e583a63d6e27c6437e3bca5205a538ffd0b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrbitalContactProfileLinksChannelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b084da7bcc3db586427467519dc0514aff1aa240e18c28cf0a77d04719d1030c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrbitalContactProfileLinksChannelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd1792b1a10265cbc2164e9e40e75d23fdeead359a804e13ef80ceb1d284292)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrbitalContactProfileLinksChannelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4341a92e72f1944bf3593027fe5cf337de20057b388bc7447ff82eea89ab88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__324eb426372039168171c72d049e466a368b6ca3e8daed5fb0705d8bda134c62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4f413c665822955c89ba615bfa8804489fd38e7b7a71662dbb43ecb54cd6ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241c9a8233cd4241ee19e4e6e5cd154b0782e699b51e4ed5caf062fb35178017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrbitalContactProfileLinksChannelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5c67a30be0e35dafd4627f56b5440654d93efdab55903dfc1d91e7a8a79eb6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEndPoint")
    def put_end_point(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05b03cce2c16a692c308bf5451eb771b1f902d922f0b931a86e4fa9c40e1f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEndPoint", [value]))

    @jsii.member(jsii_name="resetDemodulationConfiguration")
    def reset_demodulation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDemodulationConfiguration", []))

    @jsii.member(jsii_name="resetModulationConfiguration")
    def reset_modulation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModulationConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="endPoint")
    def end_point(self) -> OrbitalContactProfileLinksChannelsEndPointList:
        return typing.cast(OrbitalContactProfileLinksChannelsEndPointList, jsii.get(self, "endPoint"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthMhzInput")
    def bandwidth_mhz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthMhzInput"))

    @builtins.property
    @jsii.member(jsii_name="centerFrequencyMhzInput")
    def center_frequency_mhz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "centerFrequencyMhzInput"))

    @builtins.property
    @jsii.member(jsii_name="demodulationConfigurationInput")
    def demodulation_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "demodulationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="endPointInput")
    def end_point_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]], jsii.get(self, "endPointInput"))

    @builtins.property
    @jsii.member(jsii_name="modulationConfigurationInput")
    def modulation_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modulationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthMhz")
    def bandwidth_mhz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthMhz"))

    @bandwidth_mhz.setter
    def bandwidth_mhz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38de3a7a465ad402081830334c66270ec3c6d27ec7d8048ae336b691be4ebb23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthMhz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="centerFrequencyMhz")
    def center_frequency_mhz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "centerFrequencyMhz"))

    @center_frequency_mhz.setter
    def center_frequency_mhz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7565b307169ddf0aef8e8967eb827b6c03b11b4bc2c7c8c9fea4b2cdfe41c4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "centerFrequencyMhz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="demodulationConfiguration")
    def demodulation_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "demodulationConfiguration"))

    @demodulation_configuration.setter
    def demodulation_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56903c196fd0dcc58b13f14e4d083231a1fc95bd3467214ea196e3119f63004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "demodulationConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modulationConfiguration")
    def modulation_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modulationConfiguration"))

    @modulation_configuration.setter
    def modulation_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c6dbae100fb3c8f215dc4587e3085d2f8f4543418da71a8bca76c8bfd3d733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modulationConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44ddc9b1e301fc7db70bfefa7c2c9206bf8f0709b5cc27f763ac5f773d9abbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f679ce42d9c5a0ca9c5e411e876d5968cbe4a7b6d4649646d72ef8c47c223047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrbitalContactProfileLinksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37bcd6240b54f6ae7dd5c0cff62b8ee830015b58420de4cf016de993c5880924)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrbitalContactProfileLinksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfefb0c19869cd50fd59de8b2284a20cdf4c5a63d0034ed04f306dc33c7167c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrbitalContactProfileLinksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a087a87ab96c0527a73424eea856e3a079a2ddb9b3496e4cc718c48b6dcae2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28466590207d511e9018fd0b5cf55e633cfee88d3094396cf78064818e322651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5659844352f8825370a618d6edc2359cd3f1faf744e7f7fe07d540c9605190ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7973395b0232802ec9fb0b4918bd321226f68c0abb414b66bdbee6699b3a3d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrbitalContactProfileLinksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__935b889d80e250b3a5a9cdae2a33ff970016d32f630d1e5209416eadcd5331cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putChannels")
    def put_channels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50db15cccdd7b64acd9a5f94ac1bf64c459ce784dcc391ea8dad0debf7e125cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putChannels", [value]))

    @builtins.property
    @jsii.member(jsii_name="channels")
    def channels(self) -> OrbitalContactProfileLinksChannelsList:
        return typing.cast(OrbitalContactProfileLinksChannelsList, jsii.get(self, "channels"))

    @builtins.property
    @jsii.member(jsii_name="channelsInput")
    def channels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]], jsii.get(self, "channelsInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="polarizationInput")
    def polarization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "polarizationInput"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ebc4889753dc8b9aa2d493575f0158507522729b9cab46c40418889bb2ad76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c48afd85ce11122602c3eee7157b840360d56e61568ccfc4fea32ef8c00a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="polarization")
    def polarization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "polarization"))

    @polarization.setter
    def polarization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee70d718a3c1b8736040055f6c226d7c4e0380ed56166c2d6e21a6cef3540d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "polarization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8ed0c1cedc9ee26518913c33ac7116c859084b97123bbe0b3548388242b46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class OrbitalContactProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#create OrbitalContactProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#delete OrbitalContactProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#read OrbitalContactProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#update OrbitalContactProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4838412be69dff14dbc4adcd6560db50283c9fdf684a5487718171c821603c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#create OrbitalContactProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#delete OrbitalContactProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#read OrbitalContactProfile#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/orbital_contact_profile#update OrbitalContactProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrbitalContactProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eef220e1602e4c8b24578163cf4148cb754f50f6adb48b77e241d14b46823dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ae5560c2dabd740096d9381c4ebd3508c36866a3508c4e6235e9574300fb10b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac96bfb1050dcfc27858d566a52212bd55dd554ae7edc2ebdf5dbbb139235ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69252958f0ac909f0d9588208ad095a364faee6ed0fc11107be6a58e82697208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d783b14c8c77e42f3ab1cdcfe7b9347da22f1d8c8097acf2c47d1ea6c07f76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44aa045b58007e85ad83ce88c7cbd9ba9a921bfbe7ffc638c4f070505736b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OrbitalContactProfile",
    "OrbitalContactProfileConfig",
    "OrbitalContactProfileLinks",
    "OrbitalContactProfileLinksChannels",
    "OrbitalContactProfileLinksChannelsEndPoint",
    "OrbitalContactProfileLinksChannelsEndPointList",
    "OrbitalContactProfileLinksChannelsEndPointOutputReference",
    "OrbitalContactProfileLinksChannelsList",
    "OrbitalContactProfileLinksChannelsOutputReference",
    "OrbitalContactProfileLinksList",
    "OrbitalContactProfileLinksOutputReference",
    "OrbitalContactProfileTimeouts",
    "OrbitalContactProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__39deff242aa5c6a38243dc3e1fcbacca86de15e35910d701c352dc3db0d6f6c2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auto_tracking: builtins.str,
    links: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinks, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    minimum_variable_contact_duration: builtins.str,
    name: builtins.str,
    network_configuration_subnet_id: builtins.str,
    resource_group_name: builtins.str,
    event_hub_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OrbitalContactProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d9fcda313c8e3e43d97cc93a1b6a1f2c6fd1575e4e705d1967da74e68cb72256(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6895a0fa03aa1f99619d595a476f5cf0702d6eac481041c9282446b22814f80d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac05a98564bb751a68b31dd22f923a6719acf26a9e9fe627d430ad0bf4b140d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55c6ad098aca455b57bc670c85666164fac20a583f4efcf5f0b8b19897216b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66dbc43d2186b2d903d47d3b416b345b7fb9e31aa29c5ccab521489640d3b1e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c7222653c118760ce7499b2ffaeaa8ffa6b5ed543cddddea06ef60bb4294ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc2e109a940f78fbd2237acad1c9ce72576e74c46097a2e543f18047b3cf0a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ad8867b71cadfb1b68fad8d014c45c38a008742f458962370570ae9e594c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28bd9b81140cc0e8a1627218abadb66b6f4ac3b6266ccfde2a7ab02abe28c563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d848c106141f90d5843c2bd5c3e5211beae874a435f888425e6ab420194f111d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d49532fe123d0a75bd5a4bdf2ba374bb46b0d868aacf1dd6b2c108714d59d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354f551f319a5e81735f2d7519c136788f11fd843c6b581e802095b7b3e3dfd0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f75005285a6add60f72ca34ae53faaef01ae899497a2f85860be8965984afae(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auto_tracking: builtins.str,
    links: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinks, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    minimum_variable_contact_duration: builtins.str,
    name: builtins.str,
    network_configuration_subnet_id: builtins.str,
    resource_group_name: builtins.str,
    event_hub_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OrbitalContactProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456ff9b0e6f776a6057481678b8b7f08dac0c2eece07c0bf65f4f8bb25c490fd(
    *,
    channels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannels, typing.Dict[builtins.str, typing.Any]]]],
    direction: builtins.str,
    name: builtins.str,
    polarization: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da9881c5348b59c757ccd7e2075b85a2c13e1bd693227155c3f930ef1a7a574(
    *,
    bandwidth_mhz: jsii.Number,
    center_frequency_mhz: jsii.Number,
    end_point: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    demodulation_configuration: typing.Optional[builtins.str] = None,
    modulation_configuration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b623091cdd1eba66e0e07fe4645b546fb819b85a6a9b780fff09c2300b594500(
    *,
    end_point_name: builtins.str,
    port: builtins.str,
    protocol: builtins.str,
    ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de5cc00d333f05f027480fecb3d7539ade63369eba90835da01343f33e85aa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab131cbcc41f6616d16ffc9a738c4d4c393f29190ad77a8ebbbe0c60bd35e9ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25f0226188c49e009f22d71eae0d9d459d2ca118d65c6630c8c98660efb879e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1143221d57f1fd598adefebd86399b78138391bc10bc70304f7b607454524ba5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a02ef204c0640d1bd5cfdbcdaef463e90cb79e7b5918e1ee31fea28c060b33(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30134c2cdc1acd22bba3628900f63679c370416c505965a7b33bbc77e2a912b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd2a926f1d534a0e661334c380e7a19f5dbc16e11b8a09699239e86aa517f1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f40dd198aaec340d8f3d1dd0f2f16445f5f22c7a5f644ad7386dee24bb214fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189a92dd4bb45906c19077388424e6014180e28aba64101967b30fb83a362fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da129840c04ca0ab2c88457c633772b126984955933909a0045f9c6ec349ec55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e1719e7442d97ee11385b3daeb2aff928a41e4a36101a174d4ab46651db87d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55d4b5e5738501f3c1b6419d77e583a63d6e27c6437e3bca5205a538ffd0b69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannelsEndPoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b084da7bcc3db586427467519dc0514aff1aa240e18c28cf0a77d04719d1030c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd1792b1a10265cbc2164e9e40e75d23fdeead359a804e13ef80ceb1d284292(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4341a92e72f1944bf3593027fe5cf337de20057b388bc7447ff82eea89ab88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324eb426372039168171c72d049e466a368b6ca3e8daed5fb0705d8bda134c62(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f413c665822955c89ba615bfa8804489fd38e7b7a71662dbb43ecb54cd6ed2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241c9a8233cd4241ee19e4e6e5cd154b0782e699b51e4ed5caf062fb35178017(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c67a30be0e35dafd4627f56b5440654d93efdab55903dfc1d91e7a8a79eb6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05b03cce2c16a692c308bf5451eb771b1f902d922f0b931a86e4fa9c40e1f01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38de3a7a465ad402081830334c66270ec3c6d27ec7d8048ae336b691be4ebb23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7565b307169ddf0aef8e8967eb827b6c03b11b4bc2c7c8c9fea4b2cdfe41c4c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56903c196fd0dcc58b13f14e4d083231a1fc95bd3467214ea196e3119f63004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c6dbae100fb3c8f215dc4587e3085d2f8f4543418da71a8bca76c8bfd3d733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44ddc9b1e301fc7db70bfefa7c2c9206bf8f0709b5cc27f763ac5f773d9abbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f679ce42d9c5a0ca9c5e411e876d5968cbe4a7b6d4649646d72ef8c47c223047(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinksChannels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bcd6240b54f6ae7dd5c0cff62b8ee830015b58420de4cf016de993c5880924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfefb0c19869cd50fd59de8b2284a20cdf4c5a63d0034ed04f306dc33c7167c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a087a87ab96c0527a73424eea856e3a079a2ddb9b3496e4cc718c48b6dcae2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28466590207d511e9018fd0b5cf55e633cfee88d3094396cf78064818e322651(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5659844352f8825370a618d6edc2359cd3f1faf744e7f7fe07d540c9605190ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7973395b0232802ec9fb0b4918bd321226f68c0abb414b66bdbee6699b3a3d44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrbitalContactProfileLinks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935b889d80e250b3a5a9cdae2a33ff970016d32f630d1e5209416eadcd5331cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50db15cccdd7b64acd9a5f94ac1bf64c459ce784dcc391ea8dad0debf7e125cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ebc4889753dc8b9aa2d493575f0158507522729b9cab46c40418889bb2ad76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c48afd85ce11122602c3eee7157b840360d56e61568ccfc4fea32ef8c00a41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee70d718a3c1b8736040055f6c226d7c4e0380ed56166c2d6e21a6cef3540d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8ed0c1cedc9ee26518913c33ac7116c859084b97123bbe0b3548388242b46f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileLinks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4838412be69dff14dbc4adcd6560db50283c9fdf684a5487718171c821603c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eef220e1602e4c8b24578163cf4148cb754f50f6adb48b77e241d14b46823dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5560c2dabd740096d9381c4ebd3508c36866a3508c4e6235e9574300fb10b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac96bfb1050dcfc27858d566a52212bd55dd554ae7edc2ebdf5dbbb139235ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69252958f0ac909f0d9588208ad095a364faee6ed0fc11107be6a58e82697208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d783b14c8c77e42f3ab1cdcfe7b9347da22f1d8c8097acf2c47d1ea6c07f76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44aa045b58007e85ad83ce88c7cbd9ba9a921bfbe7ffc638c4f070505736b8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrbitalContactProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
