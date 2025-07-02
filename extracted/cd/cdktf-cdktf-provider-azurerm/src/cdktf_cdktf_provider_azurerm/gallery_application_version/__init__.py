r'''
# `azurerm_gallery_application_version`

Refer to the Terraform Registry for docs: [`azurerm_gallery_application_version`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version).
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


class GalleryApplicationVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version azurerm_gallery_application_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gallery_application_id: builtins.str,
        location: builtins.str,
        manage_action: typing.Union["GalleryApplicationVersionManageAction", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source: typing.Union["GalleryApplicationVersionSource", typing.Dict[builtins.str, typing.Any]],
        target_region: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GalleryApplicationVersionTargetRegion", typing.Dict[builtins.str, typing.Any]]]],
        config_file: typing.Optional[builtins.str] = None,
        enable_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_of_life_date: typing.Optional[builtins.str] = None,
        exclude_from_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        package_file: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GalleryApplicationVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version azurerm_gallery_application_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gallery_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#gallery_application_id GalleryApplicationVersion#gallery_application_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#location GalleryApplicationVersion#location}.
        :param manage_action: manage_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#manage_action GalleryApplicationVersion#manage_action}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#name GalleryApplicationVersion#name}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#source GalleryApplicationVersion#source}
        :param target_region: target_region block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#target_region GalleryApplicationVersion#target_region}
        :param config_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#config_file GalleryApplicationVersion#config_file}.
        :param enable_health_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#enable_health_check GalleryApplicationVersion#enable_health_check}.
        :param end_of_life_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#end_of_life_date GalleryApplicationVersion#end_of_life_date}.
        :param exclude_from_latest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#exclude_from_latest GalleryApplicationVersion#exclude_from_latest}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#id GalleryApplicationVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param package_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#package_file GalleryApplicationVersion#package_file}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#tags GalleryApplicationVersion#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#timeouts GalleryApplicationVersion#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846486a1ab1d2bf6cf1c161431b86adf571d874c66b8f1059026ebe8aea7744d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GalleryApplicationVersionConfig(
            gallery_application_id=gallery_application_id,
            location=location,
            manage_action=manage_action,
            name=name,
            source=source,
            target_region=target_region,
            config_file=config_file,
            enable_health_check=enable_health_check,
            end_of_life_date=end_of_life_date,
            exclude_from_latest=exclude_from_latest,
            id=id,
            package_file=package_file,
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
        '''Generates CDKTF code for importing a GalleryApplicationVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GalleryApplicationVersion to import.
        :param import_from_id: The id of the existing GalleryApplicationVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GalleryApplicationVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b9c35841ea19872d34204019d3695e2adc42c41ffb03861cea8ec4a7f3d499)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putManageAction")
    def put_manage_action(
        self,
        *,
        install: builtins.str,
        remove: builtins.str,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param install: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#install GalleryApplicationVersion#install}.
        :param remove: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#remove GalleryApplicationVersion#remove}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#update GalleryApplicationVersion#update}.
        '''
        value = GalleryApplicationVersionManageAction(
            install=install, remove=remove, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putManageAction", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        media_link: builtins.str,
        default_configuration_link: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param media_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#media_link GalleryApplicationVersion#media_link}.
        :param default_configuration_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#default_configuration_link GalleryApplicationVersion#default_configuration_link}.
        '''
        value = GalleryApplicationVersionSource(
            media_link=media_link,
            default_configuration_link=default_configuration_link,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putTargetRegion")
    def put_target_region(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GalleryApplicationVersionTargetRegion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a9c32c9390cadac12b66f368fbbc1b52ee0e8f778139716ab7957f500c904d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetRegion", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#create GalleryApplicationVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#delete GalleryApplicationVersion#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#read GalleryApplicationVersion#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#update GalleryApplicationVersion#update}.
        '''
        value = GalleryApplicationVersionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfigFile")
    def reset_config_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigFile", []))

    @jsii.member(jsii_name="resetEnableHealthCheck")
    def reset_enable_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHealthCheck", []))

    @jsii.member(jsii_name="resetEndOfLifeDate")
    def reset_end_of_life_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndOfLifeDate", []))

    @jsii.member(jsii_name="resetExcludeFromLatest")
    def reset_exclude_from_latest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeFromLatest", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPackageFile")
    def reset_package_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageFile", []))

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
    @jsii.member(jsii_name="manageAction")
    def manage_action(self) -> "GalleryApplicationVersionManageActionOutputReference":
        return typing.cast("GalleryApplicationVersionManageActionOutputReference", jsii.get(self, "manageAction"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "GalleryApplicationVersionSourceOutputReference":
        return typing.cast("GalleryApplicationVersionSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="targetRegion")
    def target_region(self) -> "GalleryApplicationVersionTargetRegionList":
        return typing.cast("GalleryApplicationVersionTargetRegionList", jsii.get(self, "targetRegion"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GalleryApplicationVersionTimeoutsOutputReference":
        return typing.cast("GalleryApplicationVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configFileInput")
    def config_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configFileInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHealthCheckInput")
    def enable_health_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="endOfLifeDateInput")
    def end_of_life_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endOfLifeDateInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeFromLatestInput")
    def exclude_from_latest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeFromLatestInput"))

    @builtins.property
    @jsii.member(jsii_name="galleryApplicationIdInput")
    def gallery_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "galleryApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="manageActionInput")
    def manage_action_input(
        self,
    ) -> typing.Optional["GalleryApplicationVersionManageAction"]:
        return typing.cast(typing.Optional["GalleryApplicationVersionManageAction"], jsii.get(self, "manageActionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="packageFileInput")
    def package_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packageFileInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["GalleryApplicationVersionSource"]:
        return typing.cast(typing.Optional["GalleryApplicationVersionSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRegionInput")
    def target_region_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GalleryApplicationVersionTargetRegion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GalleryApplicationVersionTargetRegion"]]], jsii.get(self, "targetRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GalleryApplicationVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GalleryApplicationVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="configFile")
    def config_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configFile"))

    @config_file.setter
    def config_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3286bb5135e4e5581f3c6ed2a7845c505d6d09ce44764d7259caecad6f3cf85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableHealthCheck")
    def enable_health_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHealthCheck"))

    @enable_health_check.setter
    def enable_health_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c8c76d286f43fd854bdcaa570c3e7f314e1a29d27ed23dec0f62bc552bccaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHealthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endOfLifeDate")
    def end_of_life_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endOfLifeDate"))

    @end_of_life_date.setter
    def end_of_life_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b22184b4c08ee1c2078fc6acf3f183593a20a55aad3d1eff09d2b6b962fbe4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endOfLifeDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeFromLatest")
    def exclude_from_latest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeFromLatest"))

    @exclude_from_latest.setter
    def exclude_from_latest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc22c1d93fced848d8b1c7ff2053eabeb2757ccf11c9b2fe6d698101d4ed8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeFromLatest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="galleryApplicationId")
    def gallery_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "galleryApplicationId"))

    @gallery_application_id.setter
    def gallery_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deeb8c2d6ffbd69515a9c84b49267f085c7cbaec58153c901452acbbf0be4d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "galleryApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ac56a596e96023b515f8afa27ce272b24c3d6757f18427646c50353b30e06c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7a793741f645f05323abf4da753e634c885a3042967e3da065470b11122713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d1ea75f68b0f892cbaaad00ddd99a795d2c595a451fa91430aac297cd4943b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageFile")
    def package_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packageFile"))

    @package_file.setter
    def package_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d27f58eadde8f64feb77cf0e9cfa8b9751e9bb2b4000be76ac2e2bc6ab97346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f88f6a3015abbfeda45da52485fa455f1deb5c9a1ca14b6148a267429408eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "gallery_application_id": "galleryApplicationId",
        "location": "location",
        "manage_action": "manageAction",
        "name": "name",
        "source": "source",
        "target_region": "targetRegion",
        "config_file": "configFile",
        "enable_health_check": "enableHealthCheck",
        "end_of_life_date": "endOfLifeDate",
        "exclude_from_latest": "excludeFromLatest",
        "id": "id",
        "package_file": "packageFile",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class GalleryApplicationVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gallery_application_id: builtins.str,
        location: builtins.str,
        manage_action: typing.Union["GalleryApplicationVersionManageAction", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source: typing.Union["GalleryApplicationVersionSource", typing.Dict[builtins.str, typing.Any]],
        target_region: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GalleryApplicationVersionTargetRegion", typing.Dict[builtins.str, typing.Any]]]],
        config_file: typing.Optional[builtins.str] = None,
        enable_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_of_life_date: typing.Optional[builtins.str] = None,
        exclude_from_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        package_file: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GalleryApplicationVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param gallery_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#gallery_application_id GalleryApplicationVersion#gallery_application_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#location GalleryApplicationVersion#location}.
        :param manage_action: manage_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#manage_action GalleryApplicationVersion#manage_action}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#name GalleryApplicationVersion#name}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#source GalleryApplicationVersion#source}
        :param target_region: target_region block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#target_region GalleryApplicationVersion#target_region}
        :param config_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#config_file GalleryApplicationVersion#config_file}.
        :param enable_health_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#enable_health_check GalleryApplicationVersion#enable_health_check}.
        :param end_of_life_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#end_of_life_date GalleryApplicationVersion#end_of_life_date}.
        :param exclude_from_latest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#exclude_from_latest GalleryApplicationVersion#exclude_from_latest}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#id GalleryApplicationVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param package_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#package_file GalleryApplicationVersion#package_file}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#tags GalleryApplicationVersion#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#timeouts GalleryApplicationVersion#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(manage_action, dict):
            manage_action = GalleryApplicationVersionManageAction(**manage_action)
        if isinstance(source, dict):
            source = GalleryApplicationVersionSource(**source)
        if isinstance(timeouts, dict):
            timeouts = GalleryApplicationVersionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bbb668d7780b19e8876a4c3a1b7266f103dcb3232301465c4d09a04fbd088a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gallery_application_id", value=gallery_application_id, expected_type=type_hints["gallery_application_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument manage_action", value=manage_action, expected_type=type_hints["manage_action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target_region", value=target_region, expected_type=type_hints["target_region"])
            check_type(argname="argument config_file", value=config_file, expected_type=type_hints["config_file"])
            check_type(argname="argument enable_health_check", value=enable_health_check, expected_type=type_hints["enable_health_check"])
            check_type(argname="argument end_of_life_date", value=end_of_life_date, expected_type=type_hints["end_of_life_date"])
            check_type(argname="argument exclude_from_latest", value=exclude_from_latest, expected_type=type_hints["exclude_from_latest"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument package_file", value=package_file, expected_type=type_hints["package_file"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gallery_application_id": gallery_application_id,
            "location": location,
            "manage_action": manage_action,
            "name": name,
            "source": source,
            "target_region": target_region,
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
        if config_file is not None:
            self._values["config_file"] = config_file
        if enable_health_check is not None:
            self._values["enable_health_check"] = enable_health_check
        if end_of_life_date is not None:
            self._values["end_of_life_date"] = end_of_life_date
        if exclude_from_latest is not None:
            self._values["exclude_from_latest"] = exclude_from_latest
        if id is not None:
            self._values["id"] = id
        if package_file is not None:
            self._values["package_file"] = package_file
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
    def gallery_application_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#gallery_application_id GalleryApplicationVersion#gallery_application_id}.'''
        result = self._values.get("gallery_application_id")
        assert result is not None, "Required property 'gallery_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#location GalleryApplicationVersion#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def manage_action(self) -> "GalleryApplicationVersionManageAction":
        '''manage_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#manage_action GalleryApplicationVersion#manage_action}
        '''
        result = self._values.get("manage_action")
        assert result is not None, "Required property 'manage_action' is missing"
        return typing.cast("GalleryApplicationVersionManageAction", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#name GalleryApplicationVersion#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "GalleryApplicationVersionSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#source GalleryApplicationVersion#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("GalleryApplicationVersionSource", result)

    @builtins.property
    def target_region(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GalleryApplicationVersionTargetRegion"]]:
        '''target_region block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#target_region GalleryApplicationVersion#target_region}
        '''
        result = self._values.get("target_region")
        assert result is not None, "Required property 'target_region' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GalleryApplicationVersionTargetRegion"]], result)

    @builtins.property
    def config_file(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#config_file GalleryApplicationVersion#config_file}.'''
        result = self._values.get("config_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_health_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#enable_health_check GalleryApplicationVersion#enable_health_check}.'''
        result = self._values.get("enable_health_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_of_life_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#end_of_life_date GalleryApplicationVersion#end_of_life_date}.'''
        result = self._values.get("end_of_life_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_from_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#exclude_from_latest GalleryApplicationVersion#exclude_from_latest}.'''
        result = self._values.get("exclude_from_latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#id GalleryApplicationVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_file(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#package_file GalleryApplicationVersion#package_file}.'''
        result = self._values.get("package_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#tags GalleryApplicationVersion#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GalleryApplicationVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#timeouts GalleryApplicationVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GalleryApplicationVersionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GalleryApplicationVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionManageAction",
    jsii_struct_bases=[],
    name_mapping={"install": "install", "remove": "remove", "update": "update"},
)
class GalleryApplicationVersionManageAction:
    def __init__(
        self,
        *,
        install: builtins.str,
        remove: builtins.str,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param install: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#install GalleryApplicationVersion#install}.
        :param remove: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#remove GalleryApplicationVersion#remove}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#update GalleryApplicationVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0391e8ddd8da3785b3219159ee35d7d0d22a2d3915ea540d88bf4bfc03d8705)
            check_type(argname="argument install", value=install, expected_type=type_hints["install"])
            check_type(argname="argument remove", value=remove, expected_type=type_hints["remove"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "install": install,
            "remove": remove,
        }
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def install(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#install GalleryApplicationVersion#install}.'''
        result = self._values.get("install")
        assert result is not None, "Required property 'install' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remove(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#remove GalleryApplicationVersion#remove}.'''
        result = self._values.get("remove")
        assert result is not None, "Required property 'remove' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#update GalleryApplicationVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GalleryApplicationVersionManageAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GalleryApplicationVersionManageActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionManageActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06a1a5b6891f1248ccc1c7f8f8219dd896a960ea70b85d5e55eb75955c570ecf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="installInput")
    def install_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "installInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInput")
    def remove_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "removeInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="install")
    def install(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "install"))

    @install.setter
    def install(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161190880984d5dc9281cf85b1a4a1f74d328713fce5d0942d76975448b0a376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "install", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remove"))

    @remove.setter
    def remove(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca359174dff6d8d4e154a7ff664b00faf0b4d348e05a0cb002e1a1b5f74e0596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e580405f5f7d7cabd31e8b27bdab8ab8fa2aa8cd843373edd784d033d095d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GalleryApplicationVersionManageAction]:
        return typing.cast(typing.Optional[GalleryApplicationVersionManageAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GalleryApplicationVersionManageAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e94bfdf1fbd97dca8ceac75ea9564f955929062f85e3d60d09aa023b10d500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionSource",
    jsii_struct_bases=[],
    name_mapping={
        "media_link": "mediaLink",
        "default_configuration_link": "defaultConfigurationLink",
    },
)
class GalleryApplicationVersionSource:
    def __init__(
        self,
        *,
        media_link: builtins.str,
        default_configuration_link: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param media_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#media_link GalleryApplicationVersion#media_link}.
        :param default_configuration_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#default_configuration_link GalleryApplicationVersion#default_configuration_link}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746bc03053e224da596a0d0e4b69e5811b0564908d96952417143b27e1f839b1)
            check_type(argname="argument media_link", value=media_link, expected_type=type_hints["media_link"])
            check_type(argname="argument default_configuration_link", value=default_configuration_link, expected_type=type_hints["default_configuration_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "media_link": media_link,
        }
        if default_configuration_link is not None:
            self._values["default_configuration_link"] = default_configuration_link

    @builtins.property
    def media_link(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#media_link GalleryApplicationVersion#media_link}.'''
        result = self._values.get("media_link")
        assert result is not None, "Required property 'media_link' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_configuration_link(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#default_configuration_link GalleryApplicationVersion#default_configuration_link}.'''
        result = self._values.get("default_configuration_link")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GalleryApplicationVersionSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GalleryApplicationVersionSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07d71eca364a9c6ef872b69033e8d6d1669d83c4a2aa82b7cb17d01fdcbe1509)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultConfigurationLink")
    def reset_default_configuration_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultConfigurationLink", []))

    @builtins.property
    @jsii.member(jsii_name="defaultConfigurationLinkInput")
    def default_configuration_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultConfigurationLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaLinkInput")
    def media_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultConfigurationLink")
    def default_configuration_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultConfigurationLink"))

    @default_configuration_link.setter
    def default_configuration_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22059c1711d4f9f99d0309fdfc510ab746d4f006ef9e19390fddd3268c05f8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultConfigurationLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mediaLink")
    def media_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaLink"))

    @media_link.setter
    def media_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1f025dc2e3c05a5a06d637c7a29a74b06ca367daac65d656d28cd451c42115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GalleryApplicationVersionSource]:
        return typing.cast(typing.Optional[GalleryApplicationVersionSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GalleryApplicationVersionSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cd100244dd60fa689d9c9edf2f999206a2c71981412bb7e8521c3a48a921b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionTargetRegion",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "regional_replica_count": "regionalReplicaCount",
        "exclude_from_latest": "excludeFromLatest",
        "storage_account_type": "storageAccountType",
    },
)
class GalleryApplicationVersionTargetRegion:
    def __init__(
        self,
        *,
        name: builtins.str,
        regional_replica_count: jsii.Number,
        exclude_from_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_account_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#name GalleryApplicationVersion#name}.
        :param regional_replica_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#regional_replica_count GalleryApplicationVersion#regional_replica_count}.
        :param exclude_from_latest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#exclude_from_latest GalleryApplicationVersion#exclude_from_latest}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#storage_account_type GalleryApplicationVersion#storage_account_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ebc4f76313752704ebf098e410045414f198a700f7c630bc7935f5a760401b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regional_replica_count", value=regional_replica_count, expected_type=type_hints["regional_replica_count"])
            check_type(argname="argument exclude_from_latest", value=exclude_from_latest, expected_type=type_hints["exclude_from_latest"])
            check_type(argname="argument storage_account_type", value=storage_account_type, expected_type=type_hints["storage_account_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "regional_replica_count": regional_replica_count,
        }
        if exclude_from_latest is not None:
            self._values["exclude_from_latest"] = exclude_from_latest
        if storage_account_type is not None:
            self._values["storage_account_type"] = storage_account_type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#name GalleryApplicationVersion#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regional_replica_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#regional_replica_count GalleryApplicationVersion#regional_replica_count}.'''
        result = self._values.get("regional_replica_count")
        assert result is not None, "Required property 'regional_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def exclude_from_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#exclude_from_latest GalleryApplicationVersion#exclude_from_latest}.'''
        result = self._values.get("exclude_from_latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_account_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#storage_account_type GalleryApplicationVersion#storage_account_type}.'''
        result = self._values.get("storage_account_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GalleryApplicationVersionTargetRegion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GalleryApplicationVersionTargetRegionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionTargetRegionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a56944f7c5fd6e690ce57261a1e59d4c2c1a015b6bd7654ec51de3d954196e21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GalleryApplicationVersionTargetRegionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18155e1a98909f79f50a6cad944b8f43c9133362d295bdd4247f37cc28cb3d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GalleryApplicationVersionTargetRegionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de773b49c0157d29f7ff27b2b443f48f2b8587c7481d7f72590f9a7996824f0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d0740077d02dd4deb4e87414bd1c0e7b4202586a448c0714f4b51dd9340d8a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b1c9a82becb199b912627ed5f085879adad62e496cc33ffd1cf0ec352ce794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GalleryApplicationVersionTargetRegion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GalleryApplicationVersionTargetRegion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GalleryApplicationVersionTargetRegion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71839c35028f9356e451d790582c5a49738c516dfba996ebdd2206cd37c78f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GalleryApplicationVersionTargetRegionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionTargetRegionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10590128cac9bb9cc596786f6ea0bc047ae11495468c5c0cf2d583ef2326d6f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExcludeFromLatest")
    def reset_exclude_from_latest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeFromLatest", []))

    @jsii.member(jsii_name="resetStorageAccountType")
    def reset_storage_account_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountType", []))

    @builtins.property
    @jsii.member(jsii_name="excludeFromLatestInput")
    def exclude_from_latest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeFromLatestInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionalReplicaCountInput")
    def regional_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "regionalReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountTypeInput")
    def storage_account_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeFromLatest")
    def exclude_from_latest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeFromLatest"))

    @exclude_from_latest.setter
    def exclude_from_latest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0da0c7042a08961edfb95e7343bd3d42e470b5a5aaacfb2585da7f15ea01c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeFromLatest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c48f77ce28e32912cecb87ef26cda01b95334630f55ef6cd970cfd4d5ba4730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionalReplicaCount")
    def regional_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "regionalReplicaCount"))

    @regional_replica_count.setter
    def regional_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db891f62f5a9501452f5fc2a4dc2136594be28cbbaece84bd610bcbb83a1651b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountType")
    def storage_account_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountType"))

    @storage_account_type.setter
    def storage_account_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc822e06ebad6c46f91d5358f000aa909495fe6808a42be55c58a6fc16e38dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTargetRegion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTargetRegion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTargetRegion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be075f9f0e3f8091ceda6f9974bbe9e4b0011a77e67e273051af251faa15086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class GalleryApplicationVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#create GalleryApplicationVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#delete GalleryApplicationVersion#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#read GalleryApplicationVersion#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#update GalleryApplicationVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6cba481a9b120a16650bfa70976a2aa68e7bfe1628fab96f77aa1fa1396c764)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#create GalleryApplicationVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#delete GalleryApplicationVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#read GalleryApplicationVersion#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/gallery_application_version#update GalleryApplicationVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GalleryApplicationVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GalleryApplicationVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.galleryApplicationVersion.GalleryApplicationVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2b6fff66c2902ea334cc8bf6a5610299ac79da6b7587fd9600e0ff64c7ace1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52612291d2dfcc033e37bd904d0f591d52ec9e87ec0db8d1df5a4c975002b0db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8fb7a5135a91f85e4654e979005db8094caf8f1bf989ea6f75f8c4d0172d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88819e5a43abb96dd09461da26cfe0b71bcbd5aa7e6a6e158bfcd5eea63a91ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1090b6b3f8534c77fdf2498c2e487739b8839f84b7e0c6d565b7e4648b6be8a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c44f7a1aae53475d5c5ab935855411cbc94c3da782a1ad567f7c4303d00603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GalleryApplicationVersion",
    "GalleryApplicationVersionConfig",
    "GalleryApplicationVersionManageAction",
    "GalleryApplicationVersionManageActionOutputReference",
    "GalleryApplicationVersionSource",
    "GalleryApplicationVersionSourceOutputReference",
    "GalleryApplicationVersionTargetRegion",
    "GalleryApplicationVersionTargetRegionList",
    "GalleryApplicationVersionTargetRegionOutputReference",
    "GalleryApplicationVersionTimeouts",
    "GalleryApplicationVersionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__846486a1ab1d2bf6cf1c161431b86adf571d874c66b8f1059026ebe8aea7744d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gallery_application_id: builtins.str,
    location: builtins.str,
    manage_action: typing.Union[GalleryApplicationVersionManageAction, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source: typing.Union[GalleryApplicationVersionSource, typing.Dict[builtins.str, typing.Any]],
    target_region: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GalleryApplicationVersionTargetRegion, typing.Dict[builtins.str, typing.Any]]]],
    config_file: typing.Optional[builtins.str] = None,
    enable_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_of_life_date: typing.Optional[builtins.str] = None,
    exclude_from_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    package_file: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GalleryApplicationVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e5b9c35841ea19872d34204019d3695e2adc42c41ffb03861cea8ec4a7f3d499(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a9c32c9390cadac12b66f368fbbc1b52ee0e8f778139716ab7957f500c904d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GalleryApplicationVersionTargetRegion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3286bb5135e4e5581f3c6ed2a7845c505d6d09ce44764d7259caecad6f3cf85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c8c76d286f43fd854bdcaa570c3e7f314e1a29d27ed23dec0f62bc552bccaf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b22184b4c08ee1c2078fc6acf3f183593a20a55aad3d1eff09d2b6b962fbe4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc22c1d93fced848d8b1c7ff2053eabeb2757ccf11c9b2fe6d698101d4ed8f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deeb8c2d6ffbd69515a9c84b49267f085c7cbaec58153c901452acbbf0be4d77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ac56a596e96023b515f8afa27ce272b24c3d6757f18427646c50353b30e06c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d7a793741f645f05323abf4da753e634c885a3042967e3da065470b11122713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d1ea75f68b0f892cbaaad00ddd99a795d2c595a451fa91430aac297cd4943b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d27f58eadde8f64feb77cf0e9cfa8b9751e9bb2b4000be76ac2e2bc6ab97346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f88f6a3015abbfeda45da52485fa455f1deb5c9a1ca14b6148a267429408eb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bbb668d7780b19e8876a4c3a1b7266f103dcb3232301465c4d09a04fbd088a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gallery_application_id: builtins.str,
    location: builtins.str,
    manage_action: typing.Union[GalleryApplicationVersionManageAction, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source: typing.Union[GalleryApplicationVersionSource, typing.Dict[builtins.str, typing.Any]],
    target_region: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GalleryApplicationVersionTargetRegion, typing.Dict[builtins.str, typing.Any]]]],
    config_file: typing.Optional[builtins.str] = None,
    enable_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_of_life_date: typing.Optional[builtins.str] = None,
    exclude_from_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    package_file: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GalleryApplicationVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0391e8ddd8da3785b3219159ee35d7d0d22a2d3915ea540d88bf4bfc03d8705(
    *,
    install: builtins.str,
    remove: builtins.str,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a1a5b6891f1248ccc1c7f8f8219dd896a960ea70b85d5e55eb75955c570ecf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161190880984d5dc9281cf85b1a4a1f74d328713fce5d0942d76975448b0a376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca359174dff6d8d4e154a7ff664b00faf0b4d348e05a0cb002e1a1b5f74e0596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e580405f5f7d7cabd31e8b27bdab8ab8fa2aa8cd843373edd784d033d095d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e94bfdf1fbd97dca8ceac75ea9564f955929062f85e3d60d09aa023b10d500(
    value: typing.Optional[GalleryApplicationVersionManageAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746bc03053e224da596a0d0e4b69e5811b0564908d96952417143b27e1f839b1(
    *,
    media_link: builtins.str,
    default_configuration_link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d71eca364a9c6ef872b69033e8d6d1669d83c4a2aa82b7cb17d01fdcbe1509(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22059c1711d4f9f99d0309fdfc510ab746d4f006ef9e19390fddd3268c05f8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1f025dc2e3c05a5a06d637c7a29a74b06ca367daac65d656d28cd451c42115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cd100244dd60fa689d9c9edf2f999206a2c71981412bb7e8521c3a48a921b8(
    value: typing.Optional[GalleryApplicationVersionSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ebc4f76313752704ebf098e410045414f198a700f7c630bc7935f5a760401b(
    *,
    name: builtins.str,
    regional_replica_count: jsii.Number,
    exclude_from_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_account_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56944f7c5fd6e690ce57261a1e59d4c2c1a015b6bd7654ec51de3d954196e21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18155e1a98909f79f50a6cad944b8f43c9133362d295bdd4247f37cc28cb3d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de773b49c0157d29f7ff27b2b443f48f2b8587c7481d7f72590f9a7996824f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0740077d02dd4deb4e87414bd1c0e7b4202586a448c0714f4b51dd9340d8a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b1c9a82becb199b912627ed5f085879adad62e496cc33ffd1cf0ec352ce794(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71839c35028f9356e451d790582c5a49738c516dfba996ebdd2206cd37c78f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GalleryApplicationVersionTargetRegion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10590128cac9bb9cc596786f6ea0bc047ae11495468c5c0cf2d583ef2326d6f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0da0c7042a08961edfb95e7343bd3d42e470b5a5aaacfb2585da7f15ea01c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c48f77ce28e32912cecb87ef26cda01b95334630f55ef6cd970cfd4d5ba4730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db891f62f5a9501452f5fc2a4dc2136594be28cbbaece84bd610bcbb83a1651b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc822e06ebad6c46f91d5358f000aa909495fe6808a42be55c58a6fc16e38dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be075f9f0e3f8091ceda6f9974bbe9e4b0011a77e67e273051af251faa15086(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTargetRegion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cba481a9b120a16650bfa70976a2aa68e7bfe1628fab96f77aa1fa1396c764(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b6fff66c2902ea334cc8bf6a5610299ac79da6b7587fd9600e0ff64c7ace1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52612291d2dfcc033e37bd904d0f591d52ec9e87ec0db8d1df5a4c975002b0db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8fb7a5135a91f85e4654e979005db8094caf8f1bf989ea6f75f8c4d0172d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88819e5a43abb96dd09461da26cfe0b71bcbd5aa7e6a6e158bfcd5eea63a91ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1090b6b3f8534c77fdf2498c2e487739b8839f84b7e0c6d565b7e4648b6be8a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c44f7a1aae53475d5c5ab935855411cbc94c3da782a1ad567f7c4303d00603(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GalleryApplicationVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
