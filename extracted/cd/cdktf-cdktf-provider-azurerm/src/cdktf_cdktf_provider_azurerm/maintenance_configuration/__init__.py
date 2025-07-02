r'''
# `azurerm_maintenance_configuration`

Refer to the Terraform Registry for docs: [`azurerm_maintenance_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration).
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


class MaintenanceConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration azurerm_maintenance_configuration}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        scope: builtins.str,
        id: typing.Optional[builtins.str] = None,
        in_guest_user_patch_mode: typing.Optional[builtins.str] = None,
        install_patches: typing.Optional[typing.Union["MaintenanceConfigurationInstallPatches", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MaintenanceConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["MaintenanceConfigurationWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration azurerm_maintenance_configuration} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#location MaintenanceConfiguration#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#name MaintenanceConfiguration#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#resource_group_name MaintenanceConfiguration#resource_group_name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#scope MaintenanceConfiguration#scope}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#id MaintenanceConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_guest_user_patch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#in_guest_user_patch_mode MaintenanceConfiguration#in_guest_user_patch_mode}.
        :param install_patches: install_patches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#install_patches MaintenanceConfiguration#install_patches}
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#properties MaintenanceConfiguration#properties}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#tags MaintenanceConfiguration#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#timeouts MaintenanceConfiguration#timeouts}
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#visibility MaintenanceConfiguration#visibility}.
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#window MaintenanceConfiguration#window}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acbde05bdbea78d90f7f26b79f50ddb62fc8efe07d93df5d53c70dcafbc1d708)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MaintenanceConfigurationConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            scope=scope,
            id=id,
            in_guest_user_patch_mode=in_guest_user_patch_mode,
            install_patches=install_patches,
            properties=properties,
            tags=tags,
            timeouts=timeouts,
            visibility=visibility,
            window=window,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a MaintenanceConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MaintenanceConfiguration to import.
        :param import_from_id: The id of the existing MaintenanceConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MaintenanceConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85783ab9c72c37eae8cc93fa014ee2bbaf82408a3a2a03478781fc9b93466ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstallPatches")
    def put_install_patches(
        self,
        *,
        linux: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MaintenanceConfigurationInstallPatchesLinux", typing.Dict[builtins.str, typing.Any]]]]] = None,
        reboot: typing.Optional[builtins.str] = None,
        windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MaintenanceConfigurationInstallPatchesWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param linux: linux block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#linux MaintenanceConfiguration#linux}
        :param reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#reboot MaintenanceConfiguration#reboot}.
        :param windows: windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#windows MaintenanceConfiguration#windows}
        '''
        value = MaintenanceConfigurationInstallPatches(
            linux=linux, reboot=reboot, windows=windows
        )

        return typing.cast(None, jsii.invoke(self, "putInstallPatches", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#create MaintenanceConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#delete MaintenanceConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#read MaintenanceConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#update MaintenanceConfiguration#update}.
        '''
        value = MaintenanceConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWindow")
    def put_window(
        self,
        *,
        start_date_time: builtins.str,
        time_zone: builtins.str,
        duration: typing.Optional[builtins.str] = None,
        expiration_date_time: typing.Optional[builtins.str] = None,
        recur_every: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_date_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#start_date_time MaintenanceConfiguration#start_date_time}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#time_zone MaintenanceConfiguration#time_zone}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#duration MaintenanceConfiguration#duration}.
        :param expiration_date_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#expiration_date_time MaintenanceConfiguration#expiration_date_time}.
        :param recur_every: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#recur_every MaintenanceConfiguration#recur_every}.
        '''
        value = MaintenanceConfigurationWindow(
            start_date_time=start_date_time,
            time_zone=time_zone,
            duration=duration,
            expiration_date_time=expiration_date_time,
            recur_every=recur_every,
        )

        return typing.cast(None, jsii.invoke(self, "putWindow", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInGuestUserPatchMode")
    def reset_in_guest_user_patch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInGuestUserPatchMode", []))

    @jsii.member(jsii_name="resetInstallPatches")
    def reset_install_patches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallPatches", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="resetWindow")
    def reset_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindow", []))

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
    @jsii.member(jsii_name="installPatches")
    def install_patches(
        self,
    ) -> "MaintenanceConfigurationInstallPatchesOutputReference":
        return typing.cast("MaintenanceConfigurationInstallPatchesOutputReference", jsii.get(self, "installPatches"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MaintenanceConfigurationTimeoutsOutputReference":
        return typing.cast("MaintenanceConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(self) -> "MaintenanceConfigurationWindowOutputReference":
        return typing.cast("MaintenanceConfigurationWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inGuestUserPatchModeInput")
    def in_guest_user_patch_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inGuestUserPatchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="installPatchesInput")
    def install_patches_input(
        self,
    ) -> typing.Optional["MaintenanceConfigurationInstallPatches"]:
        return typing.cast(typing.Optional["MaintenanceConfigurationInstallPatches"], jsii.get(self, "installPatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MaintenanceConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MaintenanceConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(self) -> typing.Optional["MaintenanceConfigurationWindow"]:
        return typing.cast(typing.Optional["MaintenanceConfigurationWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cb18e2c6957e03eb72c0709a605a62c449efdf0022e207fd2874b4468d239e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inGuestUserPatchMode")
    def in_guest_user_patch_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inGuestUserPatchMode"))

    @in_guest_user_patch_mode.setter
    def in_guest_user_patch_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58c949cadfe3668a8aecd115359c03524e9ca12e2039ae90181faf486b424f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inGuestUserPatchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca0d48a49638a361cf7efd238ae46c5197f5b442c81779000be0209b95170b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4133f6e1baf97e9ee4ace399211d6321cd0e1df5e6d7425738cc899d70ceba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03a8ba158c65b9013aaa0e0ad2a1c80c061a5c043ba72ed5fa2e50c02d7002d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bfee459bfa1d2f2e43d04f49e9420719aa489fce2ec0dc79eaa8cbd17fdcfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b35bc3fa2299eeb6ccd597d934d138f1abf71787efb2b817b6e1b9b3b2617ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e9768e894bbfe48d1621baae1414482c1d0deb25c24c1c898b90b51bfe5520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075b5b37353c225560d2c77258e4be7c1d24ae14bc8e8478f3d1e80ed3f9e189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationConfig",
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
        "resource_group_name": "resourceGroupName",
        "scope": "scope",
        "id": "id",
        "in_guest_user_patch_mode": "inGuestUserPatchMode",
        "install_patches": "installPatches",
        "properties": "properties",
        "tags": "tags",
        "timeouts": "timeouts",
        "visibility": "visibility",
        "window": "window",
    },
)
class MaintenanceConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resource_group_name: builtins.str,
        scope: builtins.str,
        id: typing.Optional[builtins.str] = None,
        in_guest_user_patch_mode: typing.Optional[builtins.str] = None,
        install_patches: typing.Optional[typing.Union["MaintenanceConfigurationInstallPatches", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MaintenanceConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["MaintenanceConfigurationWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#location MaintenanceConfiguration#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#name MaintenanceConfiguration#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#resource_group_name MaintenanceConfiguration#resource_group_name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#scope MaintenanceConfiguration#scope}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#id MaintenanceConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_guest_user_patch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#in_guest_user_patch_mode MaintenanceConfiguration#in_guest_user_patch_mode}.
        :param install_patches: install_patches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#install_patches MaintenanceConfiguration#install_patches}
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#properties MaintenanceConfiguration#properties}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#tags MaintenanceConfiguration#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#timeouts MaintenanceConfiguration#timeouts}
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#visibility MaintenanceConfiguration#visibility}.
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#window MaintenanceConfiguration#window}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(install_patches, dict):
            install_patches = MaintenanceConfigurationInstallPatches(**install_patches)
        if isinstance(timeouts, dict):
            timeouts = MaintenanceConfigurationTimeouts(**timeouts)
        if isinstance(window, dict):
            window = MaintenanceConfigurationWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89eafd8c13899e7ab108d943344e9b71b6340090b4ab31bd202c89cc119fbce4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument in_guest_user_patch_mode", value=in_guest_user_patch_mode, expected_type=type_hints["in_guest_user_patch_mode"])
            check_type(argname="argument install_patches", value=install_patches, expected_type=type_hints["install_patches"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "scope": scope,
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
        if in_guest_user_patch_mode is not None:
            self._values["in_guest_user_patch_mode"] = in_guest_user_patch_mode
        if install_patches is not None:
            self._values["install_patches"] = install_patches
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if visibility is not None:
            self._values["visibility"] = visibility
        if window is not None:
            self._values["window"] = window

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#location MaintenanceConfiguration#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#name MaintenanceConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#resource_group_name MaintenanceConfiguration#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#scope MaintenanceConfiguration#scope}.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#id MaintenanceConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_guest_user_patch_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#in_guest_user_patch_mode MaintenanceConfiguration#in_guest_user_patch_mode}.'''
        result = self._values.get("in_guest_user_patch_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_patches(
        self,
    ) -> typing.Optional["MaintenanceConfigurationInstallPatches"]:
        '''install_patches block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#install_patches MaintenanceConfiguration#install_patches}
        '''
        result = self._values.get("install_patches")
        return typing.cast(typing.Optional["MaintenanceConfigurationInstallPatches"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#properties MaintenanceConfiguration#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#tags MaintenanceConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MaintenanceConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#timeouts MaintenanceConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MaintenanceConfigurationTimeouts"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#visibility MaintenanceConfiguration#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window(self) -> typing.Optional["MaintenanceConfigurationWindow"]:
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#window MaintenanceConfiguration#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional["MaintenanceConfigurationWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MaintenanceConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatches",
    jsii_struct_bases=[],
    name_mapping={"linux": "linux", "reboot": "reboot", "windows": "windows"},
)
class MaintenanceConfigurationInstallPatches:
    def __init__(
        self,
        *,
        linux: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MaintenanceConfigurationInstallPatchesLinux", typing.Dict[builtins.str, typing.Any]]]]] = None,
        reboot: typing.Optional[builtins.str] = None,
        windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MaintenanceConfigurationInstallPatchesWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param linux: linux block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#linux MaintenanceConfiguration#linux}
        :param reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#reboot MaintenanceConfiguration#reboot}.
        :param windows: windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#windows MaintenanceConfiguration#windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db1f5c833e5f8f62a84411116a51be754faa81a575b317d5dc9f7ddf80c91fe)
            check_type(argname="argument linux", value=linux, expected_type=type_hints["linux"])
            check_type(argname="argument reboot", value=reboot, expected_type=type_hints["reboot"])
            check_type(argname="argument windows", value=windows, expected_type=type_hints["windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if linux is not None:
            self._values["linux"] = linux
        if reboot is not None:
            self._values["reboot"] = reboot
        if windows is not None:
            self._values["windows"] = windows

    @builtins.property
    def linux(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MaintenanceConfigurationInstallPatchesLinux"]]]:
        '''linux block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#linux MaintenanceConfiguration#linux}
        '''
        result = self._values.get("linux")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MaintenanceConfigurationInstallPatchesLinux"]]], result)

    @builtins.property
    def reboot(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#reboot MaintenanceConfiguration#reboot}.'''
        result = self._values.get("reboot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MaintenanceConfigurationInstallPatchesWindows"]]]:
        '''windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#windows MaintenanceConfiguration#windows}
        '''
        result = self._values.get("windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MaintenanceConfigurationInstallPatchesWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MaintenanceConfigurationInstallPatches(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesLinux",
    jsii_struct_bases=[],
    name_mapping={
        "classifications_to_include": "classificationsToInclude",
        "package_names_mask_to_exclude": "packageNamesMaskToExclude",
        "package_names_mask_to_include": "packageNamesMaskToInclude",
    },
)
class MaintenanceConfigurationInstallPatchesLinux:
    def __init__(
        self,
        *,
        classifications_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        package_names_mask_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        package_names_mask_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param classifications_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#classifications_to_include MaintenanceConfiguration#classifications_to_include}.
        :param package_names_mask_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#package_names_mask_to_exclude MaintenanceConfiguration#package_names_mask_to_exclude}.
        :param package_names_mask_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#package_names_mask_to_include MaintenanceConfiguration#package_names_mask_to_include}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0661cdfcaf86619540b88ec96e6e5b7d15a8dfd7dbf199fdd39df03a6fa3b2)
            check_type(argname="argument classifications_to_include", value=classifications_to_include, expected_type=type_hints["classifications_to_include"])
            check_type(argname="argument package_names_mask_to_exclude", value=package_names_mask_to_exclude, expected_type=type_hints["package_names_mask_to_exclude"])
            check_type(argname="argument package_names_mask_to_include", value=package_names_mask_to_include, expected_type=type_hints["package_names_mask_to_include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if classifications_to_include is not None:
            self._values["classifications_to_include"] = classifications_to_include
        if package_names_mask_to_exclude is not None:
            self._values["package_names_mask_to_exclude"] = package_names_mask_to_exclude
        if package_names_mask_to_include is not None:
            self._values["package_names_mask_to_include"] = package_names_mask_to_include

    @builtins.property
    def classifications_to_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#classifications_to_include MaintenanceConfiguration#classifications_to_include}.'''
        result = self._values.get("classifications_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def package_names_mask_to_exclude(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#package_names_mask_to_exclude MaintenanceConfiguration#package_names_mask_to_exclude}.'''
        result = self._values.get("package_names_mask_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def package_names_mask_to_include(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#package_names_mask_to_include MaintenanceConfiguration#package_names_mask_to_include}.'''
        result = self._values.get("package_names_mask_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MaintenanceConfigurationInstallPatchesLinux(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MaintenanceConfigurationInstallPatchesLinuxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesLinuxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea57494e56ac47344919b551032e1b14068cc1cab83c6578bfb209b5a0f5223a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MaintenanceConfigurationInstallPatchesLinuxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a607ccdf777ccf1f2ffa24d9fd4999152868a418bf5cca5d571f482b3c9de1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MaintenanceConfigurationInstallPatchesLinuxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06ca0ffd3af519d0e3a2615fa70cd144f2cc89b73db45dc64b000d510d4a4aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e8ee63fb218aa509eda40c4c2b7d229a49ea6a83a325eefdb691f47bf6ac3e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ebe09980344fae756de0627b1162d9f77a87fcb5d02321d984101c09c4b00b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesLinux]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesLinux]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesLinux]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f909901410f4f07256d548f03a7f976dcda4b395520b41791776c9705443fb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MaintenanceConfigurationInstallPatchesLinuxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesLinuxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7853643bd5d87cc4a5f7602b8e4d1dc2bffd473fe017704521178f7c7b782f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetClassificationsToInclude")
    def reset_classifications_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassificationsToInclude", []))

    @jsii.member(jsii_name="resetPackageNamesMaskToExclude")
    def reset_package_names_mask_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageNamesMaskToExclude", []))

    @jsii.member(jsii_name="resetPackageNamesMaskToInclude")
    def reset_package_names_mask_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageNamesMaskToInclude", []))

    @builtins.property
    @jsii.member(jsii_name="classificationsToIncludeInput")
    def classifications_to_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classificationsToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="packageNamesMaskToExcludeInput")
    def package_names_mask_to_exclude_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "packageNamesMaskToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="packageNamesMaskToIncludeInput")
    def package_names_mask_to_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "packageNamesMaskToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationsToInclude")
    def classifications_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classificationsToInclude"))

    @classifications_to_include.setter
    def classifications_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf85bc5684d59dd7ab8782458989d1adeef934f05a089ada67bfb256bf30a06b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationsToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageNamesMaskToExclude")
    def package_names_mask_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packageNamesMaskToExclude"))

    @package_names_mask_to_exclude.setter
    def package_names_mask_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab9793b1755d90fd8445dd07790432d0cbc99ab034f559e1dd2ec23a83e88ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageNamesMaskToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageNamesMaskToInclude")
    def package_names_mask_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packageNamesMaskToInclude"))

    @package_names_mask_to_include.setter
    def package_names_mask_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c6e4ddb39bbb8ffd0cc805905d45178b7f2a9450e7a5c1f75c5a412233fb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageNamesMaskToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesLinux]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesLinux]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesLinux]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40f7227ae1e5aa175308bc042a81cc37978ddc1c02f0cb8e8f68fba7a4579bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MaintenanceConfigurationInstallPatchesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ced917c1e8c8a7a30802711dcd86a02f949a03f3e375853fc1d91082035fab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLinux")
    def put_linux(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MaintenanceConfigurationInstallPatchesLinux, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712913ae14a805617e70364e5c374d2a39e4ed5754da2ba4292cd4030e6409e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLinux", [value]))

    @jsii.member(jsii_name="putWindows")
    def put_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MaintenanceConfigurationInstallPatchesWindows", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246b78fe4e1b581ab021f32be4539e1a4db0d4a285c39dabc853f34bd58c481f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWindows", [value]))

    @jsii.member(jsii_name="resetLinux")
    def reset_linux(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinux", []))

    @jsii.member(jsii_name="resetReboot")
    def reset_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReboot", []))

    @jsii.member(jsii_name="resetWindows")
    def reset_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindows", []))

    @builtins.property
    @jsii.member(jsii_name="linux")
    def linux(self) -> MaintenanceConfigurationInstallPatchesLinuxList:
        return typing.cast(MaintenanceConfigurationInstallPatchesLinuxList, jsii.get(self, "linux"))

    @builtins.property
    @jsii.member(jsii_name="windows")
    def windows(self) -> "MaintenanceConfigurationInstallPatchesWindowsList":
        return typing.cast("MaintenanceConfigurationInstallPatchesWindowsList", jsii.get(self, "windows"))

    @builtins.property
    @jsii.member(jsii_name="linuxInput")
    def linux_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesLinux]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesLinux]]], jsii.get(self, "linuxInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootInput")
    def reboot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rebootInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsInput")
    def windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MaintenanceConfigurationInstallPatchesWindows"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MaintenanceConfigurationInstallPatchesWindows"]]], jsii.get(self, "windowsInput"))

    @builtins.property
    @jsii.member(jsii_name="reboot")
    def reboot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reboot"))

    @reboot.setter
    def reboot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693ff17166014cd5b4ee0d539f6d999ed8ea7502f461cb933f7d1462a1ce48d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reboot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MaintenanceConfigurationInstallPatches]:
        return typing.cast(typing.Optional[MaintenanceConfigurationInstallPatches], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MaintenanceConfigurationInstallPatches],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bf6561a9b44cb611cd69fa46e7a785711daba88c05fc6feaa241541655d5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesWindows",
    jsii_struct_bases=[],
    name_mapping={
        "classifications_to_include": "classificationsToInclude",
        "kb_numbers_to_exclude": "kbNumbersToExclude",
        "kb_numbers_to_include": "kbNumbersToInclude",
    },
)
class MaintenanceConfigurationInstallPatchesWindows:
    def __init__(
        self,
        *,
        classifications_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        kb_numbers_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        kb_numbers_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param classifications_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#classifications_to_include MaintenanceConfiguration#classifications_to_include}.
        :param kb_numbers_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#kb_numbers_to_exclude MaintenanceConfiguration#kb_numbers_to_exclude}.
        :param kb_numbers_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#kb_numbers_to_include MaintenanceConfiguration#kb_numbers_to_include}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d09c13b1e26a4308449eea6a81781e4636f500edf6d773a6350c0b51570a5c)
            check_type(argname="argument classifications_to_include", value=classifications_to_include, expected_type=type_hints["classifications_to_include"])
            check_type(argname="argument kb_numbers_to_exclude", value=kb_numbers_to_exclude, expected_type=type_hints["kb_numbers_to_exclude"])
            check_type(argname="argument kb_numbers_to_include", value=kb_numbers_to_include, expected_type=type_hints["kb_numbers_to_include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if classifications_to_include is not None:
            self._values["classifications_to_include"] = classifications_to_include
        if kb_numbers_to_exclude is not None:
            self._values["kb_numbers_to_exclude"] = kb_numbers_to_exclude
        if kb_numbers_to_include is not None:
            self._values["kb_numbers_to_include"] = kb_numbers_to_include

    @builtins.property
    def classifications_to_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#classifications_to_include MaintenanceConfiguration#classifications_to_include}.'''
        result = self._values.get("classifications_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kb_numbers_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#kb_numbers_to_exclude MaintenanceConfiguration#kb_numbers_to_exclude}.'''
        result = self._values.get("kb_numbers_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kb_numbers_to_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#kb_numbers_to_include MaintenanceConfiguration#kb_numbers_to_include}.'''
        result = self._values.get("kb_numbers_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MaintenanceConfigurationInstallPatchesWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MaintenanceConfigurationInstallPatchesWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e567674f0e43d3b3fea0275570669d165090746deeca6767ecded0c2cde3cb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MaintenanceConfigurationInstallPatchesWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd021162090b50838469c20a5cbbcba68dc4d45f8bbfc5f2bf0332e6be826ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MaintenanceConfigurationInstallPatchesWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc744c2b39719666e4d6ef69eb4a27dc4e75d3f05ae4a96755efe121da5247f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82172e3c86b8b4c6f63d2c08b24f1ddde30e8b023918b6a5ca160461e67f80d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da72356f7fc00c866928797671fc542353effe94d33db8e391b101a3592a5a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04305acf7c0c33ea411955640502702e5e0f1133e427da2488cfe240dbc23482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MaintenanceConfigurationInstallPatchesWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationInstallPatchesWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91be851dd63493eb4aeb9a0e2782394eb47b13e378f75e84223568875a75130)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetClassificationsToInclude")
    def reset_classifications_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassificationsToInclude", []))

    @jsii.member(jsii_name="resetKbNumbersToExclude")
    def reset_kb_numbers_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKbNumbersToExclude", []))

    @jsii.member(jsii_name="resetKbNumbersToInclude")
    def reset_kb_numbers_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKbNumbersToInclude", []))

    @builtins.property
    @jsii.member(jsii_name="classificationsToIncludeInput")
    def classifications_to_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classificationsToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="kbNumbersToExcludeInput")
    def kb_numbers_to_exclude_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "kbNumbersToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="kbNumbersToIncludeInput")
    def kb_numbers_to_include_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "kbNumbersToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationsToInclude")
    def classifications_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classificationsToInclude"))

    @classifications_to_include.setter
    def classifications_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c663f89396016ffbabf897abeee99267dbef91d4427536b732e6096bd817beec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationsToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kbNumbersToExclude")
    def kb_numbers_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kbNumbersToExclude"))

    @kb_numbers_to_exclude.setter
    def kb_numbers_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c80fa7cf97173c4afac61918ee3f169de431c9899971699d5df9220c243f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kbNumbersToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kbNumbersToInclude")
    def kb_numbers_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kbNumbersToInclude"))

    @kb_numbers_to_include.setter
    def kb_numbers_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a950305f779f5f67b473e385e0d87bc1ce5712961d5913c2eb3998ba51fa88ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kbNumbersToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e83a466cb4fe6ee4bc1f1bb1c320f349060aeb0cae192633929a1179ef995b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MaintenanceConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#create MaintenanceConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#delete MaintenanceConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#read MaintenanceConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#update MaintenanceConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122f12c93059f22f81579bd416583da2a55fd031cdcafc3515ef8f5f9e127318)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#create MaintenanceConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#delete MaintenanceConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#read MaintenanceConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#update MaintenanceConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MaintenanceConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MaintenanceConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3e631d210af08a6b98fd45d0a7bd530568e88ea2b3fb6bcd23eacaf5603c69d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__406511247400ed31d24892a065de713d49d0a4e8376850640c527d5f6ef0de6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613e7c4e24c12c5c580d476e390ef291d4dab383958af253caec152b7130cc40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa7536b6f2f8b6960075769939cfe702b7f449e893740ea1a0da05e7b9dfeb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9b4c3af76694c3678c1eb80ae67aef31f29912e293be66d5a0920e2c683e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a460c8574ecc4068cfaf949676e05301dc28434ca58e5c73aefcccf249f72e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationWindow",
    jsii_struct_bases=[],
    name_mapping={
        "start_date_time": "startDateTime",
        "time_zone": "timeZone",
        "duration": "duration",
        "expiration_date_time": "expirationDateTime",
        "recur_every": "recurEvery",
    },
)
class MaintenanceConfigurationWindow:
    def __init__(
        self,
        *,
        start_date_time: builtins.str,
        time_zone: builtins.str,
        duration: typing.Optional[builtins.str] = None,
        expiration_date_time: typing.Optional[builtins.str] = None,
        recur_every: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_date_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#start_date_time MaintenanceConfiguration#start_date_time}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#time_zone MaintenanceConfiguration#time_zone}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#duration MaintenanceConfiguration#duration}.
        :param expiration_date_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#expiration_date_time MaintenanceConfiguration#expiration_date_time}.
        :param recur_every: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#recur_every MaintenanceConfiguration#recur_every}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813fcec526839bf486e484e118c36fe1658c91fd4566995c18c7fb902611a4d9)
            check_type(argname="argument start_date_time", value=start_date_time, expected_type=type_hints["start_date_time"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument expiration_date_time", value=expiration_date_time, expected_type=type_hints["expiration_date_time"])
            check_type(argname="argument recur_every", value=recur_every, expected_type=type_hints["recur_every"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_date_time": start_date_time,
            "time_zone": time_zone,
        }
        if duration is not None:
            self._values["duration"] = duration
        if expiration_date_time is not None:
            self._values["expiration_date_time"] = expiration_date_time
        if recur_every is not None:
            self._values["recur_every"] = recur_every

    @builtins.property
    def start_date_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#start_date_time MaintenanceConfiguration#start_date_time}.'''
        result = self._values.get("start_date_time")
        assert result is not None, "Required property 'start_date_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#time_zone MaintenanceConfiguration#time_zone}.'''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#duration MaintenanceConfiguration#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration_date_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#expiration_date_time MaintenanceConfiguration#expiration_date_time}.'''
        result = self._values.get("expiration_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recur_every(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/maintenance_configuration#recur_every MaintenanceConfiguration#recur_every}.'''
        result = self._values.get("recur_every")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MaintenanceConfigurationWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MaintenanceConfigurationWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.maintenanceConfiguration.MaintenanceConfigurationWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd350efca4d94e54749e168da1a690aee4ed528c5e70d2e4546e4cda1a90eb3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetExpirationDateTime")
    def reset_expiration_date_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationDateTime", []))

    @jsii.member(jsii_name="resetRecurEvery")
    def reset_recur_every(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurEvery", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationDateTimeInput")
    def expiration_date_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationDateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="recurEveryInput")
    def recur_every_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurEveryInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateTimeInput")
    def start_date_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5037b7ce2e6b8865cd39e6d685d34e9650c6528d245bdbf82bda6165e953985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationDateTime")
    def expiration_date_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationDateTime"))

    @expiration_date_time.setter
    def expiration_date_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e6410de76f9844f12696881eca5ab4767bd1600872804c820b24df79499ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationDateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurEvery")
    def recur_every(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurEvery"))

    @recur_every.setter
    def recur_every(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e7877851b2cfe3895ab193d8b64c4a8bb8743471ade29e3bf0793a0bd3d3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurEvery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDateTime")
    def start_date_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDateTime"))

    @start_date_time.setter
    def start_date_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ca26c78132036022ff9c1079b39d96c7efaa6d7082187853b798e590ff83fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e89e3f9b14bafc90043876b483626ec5fb4038510444f997450078d05ba0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MaintenanceConfigurationWindow]:
        return typing.cast(typing.Optional[MaintenanceConfigurationWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MaintenanceConfigurationWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f137c461a972868238d62548e406615d71931e77fad89b075e7a197a895f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MaintenanceConfiguration",
    "MaintenanceConfigurationConfig",
    "MaintenanceConfigurationInstallPatches",
    "MaintenanceConfigurationInstallPatchesLinux",
    "MaintenanceConfigurationInstallPatchesLinuxList",
    "MaintenanceConfigurationInstallPatchesLinuxOutputReference",
    "MaintenanceConfigurationInstallPatchesOutputReference",
    "MaintenanceConfigurationInstallPatchesWindows",
    "MaintenanceConfigurationInstallPatchesWindowsList",
    "MaintenanceConfigurationInstallPatchesWindowsOutputReference",
    "MaintenanceConfigurationTimeouts",
    "MaintenanceConfigurationTimeoutsOutputReference",
    "MaintenanceConfigurationWindow",
    "MaintenanceConfigurationWindowOutputReference",
]

publication.publish()

def _typecheckingstub__acbde05bdbea78d90f7f26b79f50ddb62fc8efe07d93df5d53c70dcafbc1d708(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    scope: builtins.str,
    id: typing.Optional[builtins.str] = None,
    in_guest_user_patch_mode: typing.Optional[builtins.str] = None,
    install_patches: typing.Optional[typing.Union[MaintenanceConfigurationInstallPatches, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MaintenanceConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[MaintenanceConfigurationWindow, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d85783ab9c72c37eae8cc93fa014ee2bbaf82408a3a2a03478781fc9b93466ee(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cb18e2c6957e03eb72c0709a605a62c449efdf0022e207fd2874b4468d239e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58c949cadfe3668a8aecd115359c03524e9ca12e2039ae90181faf486b424f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca0d48a49638a361cf7efd238ae46c5197f5b442c81779000be0209b95170b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4133f6e1baf97e9ee4ace399211d6321cd0e1df5e6d7425738cc899d70ceba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03a8ba158c65b9013aaa0e0ad2a1c80c061a5c043ba72ed5fa2e50c02d7002d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bfee459bfa1d2f2e43d04f49e9420719aa489fce2ec0dc79eaa8cbd17fdcfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b35bc3fa2299eeb6ccd597d934d138f1abf71787efb2b817b6e1b9b3b2617ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e9768e894bbfe48d1621baae1414482c1d0deb25c24c1c898b90b51bfe5520(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075b5b37353c225560d2c77258e4be7c1d24ae14bc8e8478f3d1e80ed3f9e189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89eafd8c13899e7ab108d943344e9b71b6340090b4ab31bd202c89cc119fbce4(
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
    resource_group_name: builtins.str,
    scope: builtins.str,
    id: typing.Optional[builtins.str] = None,
    in_guest_user_patch_mode: typing.Optional[builtins.str] = None,
    install_patches: typing.Optional[typing.Union[MaintenanceConfigurationInstallPatches, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MaintenanceConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[MaintenanceConfigurationWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db1f5c833e5f8f62a84411116a51be754faa81a575b317d5dc9f7ddf80c91fe(
    *,
    linux: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MaintenanceConfigurationInstallPatchesLinux, typing.Dict[builtins.str, typing.Any]]]]] = None,
    reboot: typing.Optional[builtins.str] = None,
    windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MaintenanceConfigurationInstallPatchesWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0661cdfcaf86619540b88ec96e6e5b7d15a8dfd7dbf199fdd39df03a6fa3b2(
    *,
    classifications_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    package_names_mask_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    package_names_mask_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea57494e56ac47344919b551032e1b14068cc1cab83c6578bfb209b5a0f5223a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a607ccdf777ccf1f2ffa24d9fd4999152868a418bf5cca5d571f482b3c9de1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06ca0ffd3af519d0e3a2615fa70cd144f2cc89b73db45dc64b000d510d4a4aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8ee63fb218aa509eda40c4c2b7d229a49ea6a83a325eefdb691f47bf6ac3e1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebe09980344fae756de0627b1162d9f77a87fcb5d02321d984101c09c4b00b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f909901410f4f07256d548f03a7f976dcda4b395520b41791776c9705443fb0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesLinux]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7853643bd5d87cc4a5f7602b8e4d1dc2bffd473fe017704521178f7c7b782f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf85bc5684d59dd7ab8782458989d1adeef934f05a089ada67bfb256bf30a06b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab9793b1755d90fd8445dd07790432d0cbc99ab034f559e1dd2ec23a83e88ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c6e4ddb39bbb8ffd0cc805905d45178b7f2a9450e7a5c1f75c5a412233fb27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40f7227ae1e5aa175308bc042a81cc37978ddc1c02f0cb8e8f68fba7a4579bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesLinux]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ced917c1e8c8a7a30802711dcd86a02f949a03f3e375853fc1d91082035fab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712913ae14a805617e70364e5c374d2a39e4ed5754da2ba4292cd4030e6409e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MaintenanceConfigurationInstallPatchesLinux, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246b78fe4e1b581ab021f32be4539e1a4db0d4a285c39dabc853f34bd58c481f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MaintenanceConfigurationInstallPatchesWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693ff17166014cd5b4ee0d539f6d999ed8ea7502f461cb933f7d1462a1ce48d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bf6561a9b44cb611cd69fa46e7a785711daba88c05fc6feaa241541655d5d3(
    value: typing.Optional[MaintenanceConfigurationInstallPatches],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d09c13b1e26a4308449eea6a81781e4636f500edf6d773a6350c0b51570a5c(
    *,
    classifications_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    kb_numbers_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    kb_numbers_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e567674f0e43d3b3fea0275570669d165090746deeca6767ecded0c2cde3cb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd021162090b50838469c20a5cbbcba68dc4d45f8bbfc5f2bf0332e6be826ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc744c2b39719666e4d6ef69eb4a27dc4e75d3f05ae4a96755efe121da5247f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82172e3c86b8b4c6f63d2c08b24f1ddde30e8b023918b6a5ca160461e67f80d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da72356f7fc00c866928797671fc542353effe94d33db8e391b101a3592a5a58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04305acf7c0c33ea411955640502702e5e0f1133e427da2488cfe240dbc23482(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MaintenanceConfigurationInstallPatchesWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91be851dd63493eb4aeb9a0e2782394eb47b13e378f75e84223568875a75130(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c663f89396016ffbabf897abeee99267dbef91d4427536b732e6096bd817beec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c80fa7cf97173c4afac61918ee3f169de431c9899971699d5df9220c243f11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a950305f779f5f67b473e385e0d87bc1ce5712961d5913c2eb3998ba51fa88ad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e83a466cb4fe6ee4bc1f1bb1c320f349060aeb0cae192633929a1179ef995b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationInstallPatchesWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122f12c93059f22f81579bd416583da2a55fd031cdcafc3515ef8f5f9e127318(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e631d210af08a6b98fd45d0a7bd530568e88ea2b3fb6bcd23eacaf5603c69d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406511247400ed31d24892a065de713d49d0a4e8376850640c527d5f6ef0de6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613e7c4e24c12c5c580d476e390ef291d4dab383958af253caec152b7130cc40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa7536b6f2f8b6960075769939cfe702b7f449e893740ea1a0da05e7b9dfeb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9b4c3af76694c3678c1eb80ae67aef31f29912e293be66d5a0920e2c683e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a460c8574ecc4068cfaf949676e05301dc28434ca58e5c73aefcccf249f72e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MaintenanceConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813fcec526839bf486e484e118c36fe1658c91fd4566995c18c7fb902611a4d9(
    *,
    start_date_time: builtins.str,
    time_zone: builtins.str,
    duration: typing.Optional[builtins.str] = None,
    expiration_date_time: typing.Optional[builtins.str] = None,
    recur_every: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd350efca4d94e54749e168da1a690aee4ed528c5e70d2e4546e4cda1a90eb3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5037b7ce2e6b8865cd39e6d685d34e9650c6528d245bdbf82bda6165e953985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e6410de76f9844f12696881eca5ab4767bd1600872804c820b24df79499ce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e7877851b2cfe3895ab193d8b64c4a8bb8743471ade29e3bf0793a0bd3d3a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ca26c78132036022ff9c1079b39d96c7efaa6d7082187853b798e590ff83fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e89e3f9b14bafc90043876b483626ec5fb4038510444f997450078d05ba0ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f137c461a972868238d62548e406615d71931e77fad89b075e7a197a895f81(
    value: typing.Optional[MaintenanceConfigurationWindow],
) -> None:
    """Type checking stubs"""
    pass
