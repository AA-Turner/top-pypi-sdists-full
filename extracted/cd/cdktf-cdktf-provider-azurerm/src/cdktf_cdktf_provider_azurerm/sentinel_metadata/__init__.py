r'''
# `azurerm_sentinel_metadata`

Refer to the Terraform Registry for docs: [`azurerm_sentinel_metadata`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata).
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


class SentinelMetadata(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadata",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata azurerm_sentinel_metadata}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        content_id: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        parent_id: builtins.str,
        workspace_id: builtins.str,
        author: typing.Optional[typing.Union["SentinelMetadataAuthor", typing.Dict[builtins.str, typing.Any]]] = None,
        category: typing.Optional[typing.Union["SentinelMetadataCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        content_schema_version: typing.Optional[builtins.str] = None,
        custom_version: typing.Optional[builtins.str] = None,
        dependency: typing.Optional[builtins.str] = None,
        first_publish_date: typing.Optional[builtins.str] = None,
        icon_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_publish_date: typing.Optional[builtins.str] = None,
        preview_images: typing.Optional[typing.Sequence[builtins.str]] = None,
        preview_images_dark: typing.Optional[typing.Sequence[builtins.str]] = None,
        providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[typing.Union["SentinelMetadataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        support: typing.Optional[typing.Union["SentinelMetadataSupport", typing.Dict[builtins.str, typing.Any]]] = None,
        threat_analysis_tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
        threat_analysis_techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SentinelMetadataTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata azurerm_sentinel_metadata} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param content_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#content_id SentinelMetadata#content_id}.
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#kind SentinelMetadata#kind}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        :param parent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#parent_id SentinelMetadata#parent_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#workspace_id SentinelMetadata#workspace_id}.
        :param author: author block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#author SentinelMetadata#author}
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#category SentinelMetadata#category}
        :param content_schema_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#content_schema_version SentinelMetadata#content_schema_version}.
        :param custom_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#custom_version SentinelMetadata#custom_version}.
        :param dependency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#dependency SentinelMetadata#dependency}.
        :param first_publish_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#first_publish_date SentinelMetadata#first_publish_date}.
        :param icon_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#icon_id SentinelMetadata#icon_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#id SentinelMetadata#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_publish_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#last_publish_date SentinelMetadata#last_publish_date}.
        :param preview_images: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#preview_images SentinelMetadata#preview_images}.
        :param preview_images_dark: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#preview_images_dark SentinelMetadata#preview_images_dark}.
        :param providers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#providers SentinelMetadata#providers}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#source SentinelMetadata#source}
        :param support: support block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#support SentinelMetadata#support}
        :param threat_analysis_tactics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#threat_analysis_tactics SentinelMetadata#threat_analysis_tactics}.
        :param threat_analysis_techniques: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#threat_analysis_techniques SentinelMetadata#threat_analysis_techniques}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#timeouts SentinelMetadata#timeouts}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#version SentinelMetadata#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb7b0869e58477772edef655345453a35bca208a06e79978c98b40c8bde5c86)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SentinelMetadataConfig(
            content_id=content_id,
            kind=kind,
            name=name,
            parent_id=parent_id,
            workspace_id=workspace_id,
            author=author,
            category=category,
            content_schema_version=content_schema_version,
            custom_version=custom_version,
            dependency=dependency,
            first_publish_date=first_publish_date,
            icon_id=icon_id,
            id=id,
            last_publish_date=last_publish_date,
            preview_images=preview_images,
            preview_images_dark=preview_images_dark,
            providers=providers,
            source=source,
            support=support,
            threat_analysis_tactics=threat_analysis_tactics,
            threat_analysis_techniques=threat_analysis_techniques,
            timeouts=timeouts,
            version=version,
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
        '''Generates CDKTF code for importing a SentinelMetadata resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SentinelMetadata to import.
        :param import_from_id: The id of the existing SentinelMetadata that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SentinelMetadata to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1476ef4ffc3392d6b5c5bc2b3410a8d97e05dafa9e575158f7201a96652b168)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthor")
    def put_author(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        link: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#email SentinelMetadata#email}.
        :param link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#link SentinelMetadata#link}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        '''
        value = SentinelMetadataAuthor(email=email, link=link, name=name)

        return typing.cast(None, jsii.invoke(self, "putAuthor", [value]))

    @jsii.member(jsii_name="putCategory")
    def put_category(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        verticals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param domains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#domains SentinelMetadata#domains}.
        :param verticals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#verticals SentinelMetadata#verticals}.
        '''
        value = SentinelMetadataCategory(domains=domains, verticals=verticals)

        return typing.cast(None, jsii.invoke(self, "putCategory", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        kind: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#kind SentinelMetadata#kind}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#id SentinelMetadata#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        '''
        value = SentinelMetadataSource(kind=kind, id=id, name=name)

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putSupport")
    def put_support(
        self,
        *,
        tier: builtins.str,
        email: typing.Optional[builtins.str] = None,
        link: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#tier SentinelMetadata#tier}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#email SentinelMetadata#email}.
        :param link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#link SentinelMetadata#link}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        '''
        value = SentinelMetadataSupport(tier=tier, email=email, link=link, name=name)

        return typing.cast(None, jsii.invoke(self, "putSupport", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#create SentinelMetadata#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#delete SentinelMetadata#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#read SentinelMetadata#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#update SentinelMetadata#update}.
        '''
        value = SentinelMetadataTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthor")
    def reset_author(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthor", []))

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetContentSchemaVersion")
    def reset_content_schema_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentSchemaVersion", []))

    @jsii.member(jsii_name="resetCustomVersion")
    def reset_custom_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomVersion", []))

    @jsii.member(jsii_name="resetDependency")
    def reset_dependency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependency", []))

    @jsii.member(jsii_name="resetFirstPublishDate")
    def reset_first_publish_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstPublishDate", []))

    @jsii.member(jsii_name="resetIconId")
    def reset_icon_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIconId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLastPublishDate")
    def reset_last_publish_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastPublishDate", []))

    @jsii.member(jsii_name="resetPreviewImages")
    def reset_preview_images(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewImages", []))

    @jsii.member(jsii_name="resetPreviewImagesDark")
    def reset_preview_images_dark(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewImagesDark", []))

    @jsii.member(jsii_name="resetProviders")
    def reset_providers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviders", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetSupport")
    def reset_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupport", []))

    @jsii.member(jsii_name="resetThreatAnalysisTactics")
    def reset_threat_analysis_tactics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatAnalysisTactics", []))

    @jsii.member(jsii_name="resetThreatAnalysisTechniques")
    def reset_threat_analysis_techniques(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatAnalysisTechniques", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="author")
    def author(self) -> "SentinelMetadataAuthorOutputReference":
        return typing.cast("SentinelMetadataAuthorOutputReference", jsii.get(self, "author"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> "SentinelMetadataCategoryOutputReference":
        return typing.cast("SentinelMetadataCategoryOutputReference", jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "SentinelMetadataSourceOutputReference":
        return typing.cast("SentinelMetadataSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="support")
    def support(self) -> "SentinelMetadataSupportOutputReference":
        return typing.cast("SentinelMetadataSupportOutputReference", jsii.get(self, "support"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SentinelMetadataTimeoutsOutputReference":
        return typing.cast("SentinelMetadataTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authorInput")
    def author_input(self) -> typing.Optional["SentinelMetadataAuthor"]:
        return typing.cast(typing.Optional["SentinelMetadataAuthor"], jsii.get(self, "authorInput"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional["SentinelMetadataCategory"]:
        return typing.cast(typing.Optional["SentinelMetadataCategory"], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="contentIdInput")
    def content_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="contentSchemaVersionInput")
    def content_schema_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentSchemaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="customVersionInput")
    def custom_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="dependencyInput")
    def dependency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dependencyInput"))

    @builtins.property
    @jsii.member(jsii_name="firstPublishDateInput")
    def first_publish_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstPublishDateInput"))

    @builtins.property
    @jsii.member(jsii_name="iconIdInput")
    def icon_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="lastPublishDateInput")
    def last_publish_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastPublishDateInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentIdInput")
    def parent_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="previewImagesDarkInput")
    def preview_images_dark_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previewImagesDarkInput"))

    @builtins.property
    @jsii.member(jsii_name="previewImagesInput")
    def preview_images_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previewImagesInput"))

    @builtins.property
    @jsii.member(jsii_name="providersInput")
    def providers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "providersInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["SentinelMetadataSource"]:
        return typing.cast(typing.Optional["SentinelMetadataSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="supportInput")
    def support_input(self) -> typing.Optional["SentinelMetadataSupport"]:
        return typing.cast(typing.Optional["SentinelMetadataSupport"], jsii.get(self, "supportInput"))

    @builtins.property
    @jsii.member(jsii_name="threatAnalysisTacticsInput")
    def threat_analysis_tactics_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "threatAnalysisTacticsInput"))

    @builtins.property
    @jsii.member(jsii_name="threatAnalysisTechniquesInput")
    def threat_analysis_techniques_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "threatAnalysisTechniquesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelMetadataTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SentinelMetadataTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="contentId")
    def content_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentId"))

    @content_id.setter
    def content_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb5249399217972ff2b7856a99283e4f7e30b0edb539c4dc2d6f139b578baf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentSchemaVersion")
    def content_schema_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentSchemaVersion"))

    @content_schema_version.setter
    def content_schema_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a279769fce5aeef63196b2ad7797bde2ed7320f07a941956f273edac74720b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentSchemaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customVersion")
    def custom_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customVersion"))

    @custom_version.setter
    def custom_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a097ace864dabff32fe7b5fb071cec7cd457ceb13fc02b900b46c851a9e4c9cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependency")
    def dependency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dependency"))

    @dependency.setter
    def dependency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6337b1791a7f4b0903202199791c507e23cf9c8e118602931e69c1895d90cc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstPublishDate")
    def first_publish_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstPublishDate"))

    @first_publish_date.setter
    def first_publish_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793327fb06b15b83f45ea87ea86de2520b39f46774d9e546125d655b7a913a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstPublishDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iconId")
    def icon_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iconId"))

    @icon_id.setter
    def icon_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd991aaf680e5e67e4498bc2c963728d5550ca7dc1ca4083e7fa0fff5bf4e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iconId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5903fa3a75a115a4a70478ca168595f17b93e7095439c8dc744384bb64edfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505b61c9047786eacccbeb6cf48f5cd38f8945002a4abb5d6cc38cd5fbf9100a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastPublishDate")
    def last_publish_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastPublishDate"))

    @last_publish_date.setter
    def last_publish_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee910699e9794a5da40f53456642bfa6c45ece296682528e81f8e3093841e8a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastPublishDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767fc6d2c38085317a25eea6fdcacfb192e7122f99598adafbada471c3c08c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentId")
    def parent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentId"))

    @parent_id.setter
    def parent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4afa216540053b5489ee4043195264955d51549c21cfbbdde5a1c6891f70db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="previewImages")
    def preview_images(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "previewImages"))

    @preview_images.setter
    def preview_images(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e268e8ae7c999328d7125d3e1a95c8e61935a193ded4779a3e5f6e41f1e66c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewImages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="previewImagesDark")
    def preview_images_dark(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "previewImagesDark"))

    @preview_images_dark.setter
    def preview_images_dark(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624ab8f2aa5c613a0eddf1979d069ce358bc2ed7b53f017a7e2c65ba6ebd9a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewImagesDark", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providers")
    def providers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "providers"))

    @providers.setter
    def providers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbd146648d126015b745b012ef6c5b26bb4c4b00f5cb95f3b12e286051326d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threatAnalysisTactics")
    def threat_analysis_tactics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "threatAnalysisTactics"))

    @threat_analysis_tactics.setter
    def threat_analysis_tactics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809acf614df550574e7c7130542c3eaf170607bbf93d5d0c2cfafd16e9111d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threatAnalysisTactics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threatAnalysisTechniques")
    def threat_analysis_techniques(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "threatAnalysisTechniques"))

    @threat_analysis_techniques.setter
    def threat_analysis_techniques(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd017740c646a54d582bdf44bf7ac46eb231e05d923e539d89f08cbc6f821e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threatAnalysisTechniques", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ef3ff02f1dd5324defdb38e5d8a12395f367fc441c059fa6d15e5253792e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a70bf250d29859c592ec1623a27b0508821762380a49c910fe08d5b8d5390e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataAuthor",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "link": "link", "name": "name"},
)
class SentinelMetadataAuthor:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        link: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#email SentinelMetadata#email}.
        :param link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#link SentinelMetadata#link}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b3aae49093ac4fc2d0333f657975845ee35ceec4bcb4878c650d1eebe8542f)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if link is not None:
            self._values["link"] = link
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#email SentinelMetadata#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#link SentinelMetadata#link}.'''
        result = self._values.get("link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelMetadataAuthor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelMetadataAuthorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataAuthorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6af91aeb17b5ba15f0a76c3f20dc979aa77d7151fe0c3c6d17dd336c920063cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetLink")
    def reset_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLink", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="linkInput")
    def link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7171cb7ce1e0aa12a780281e5d9cebb2e9c43885fa46ae20c442239877ed14b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="link")
    def link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "link"))

    @link.setter
    def link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f6490c30243f39c343056919af9c1c77379fdd078908e6c75b6add01c663c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "link", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25489aeb509877f2317cc2b25e5d8ffd4b901360a783e319afb502e04da6a636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelMetadataAuthor]:
        return typing.cast(typing.Optional[SentinelMetadataAuthor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SentinelMetadataAuthor]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec678b2ae70fef1cb12202b7ae08cd6ab1a86a5691936c3cea7d9ca3283d97ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataCategory",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "verticals": "verticals"},
)
class SentinelMetadataCategory:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        verticals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param domains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#domains SentinelMetadata#domains}.
        :param verticals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#verticals SentinelMetadata#verticals}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972d16e71549b5578afa20c7d4f95d65804a19d8523b4b626114c70c606eab50)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument verticals", value=verticals, expected_type=type_hints["verticals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domains is not None:
            self._values["domains"] = domains
        if verticals is not None:
            self._values["verticals"] = verticals

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#domains SentinelMetadata#domains}.'''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verticals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#verticals SentinelMetadata#verticals}.'''
        result = self._values.get("verticals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelMetadataCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelMetadataCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d713adcbf868673d166c35255eb99bce3e969e715e7f82fc7d381c73fab0f303)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomains")
    def reset_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomains", []))

    @jsii.member(jsii_name="resetVerticals")
    def reset_verticals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerticals", []))

    @builtins.property
    @jsii.member(jsii_name="domainsInput")
    def domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainsInput"))

    @builtins.property
    @jsii.member(jsii_name="verticalsInput")
    def verticals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "verticalsInput"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda0428242a9db2de9f15a4baae5e4967b95b270b774ace465b02b40cc425d24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verticals")
    def verticals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "verticals"))

    @verticals.setter
    def verticals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a06574baa795b934639a7bad872150170dd23dcd2c2fd221a5b74e0e2e9370a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verticals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelMetadataCategory]:
        return typing.cast(typing.Optional[SentinelMetadataCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SentinelMetadataCategory]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0127decb8470782693675decec27004a04cfd03f089834103e39e01476254308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "content_id": "contentId",
        "kind": "kind",
        "name": "name",
        "parent_id": "parentId",
        "workspace_id": "workspaceId",
        "author": "author",
        "category": "category",
        "content_schema_version": "contentSchemaVersion",
        "custom_version": "customVersion",
        "dependency": "dependency",
        "first_publish_date": "firstPublishDate",
        "icon_id": "iconId",
        "id": "id",
        "last_publish_date": "lastPublishDate",
        "preview_images": "previewImages",
        "preview_images_dark": "previewImagesDark",
        "providers": "providers",
        "source": "source",
        "support": "support",
        "threat_analysis_tactics": "threatAnalysisTactics",
        "threat_analysis_techniques": "threatAnalysisTechniques",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class SentinelMetadataConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        content_id: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        parent_id: builtins.str,
        workspace_id: builtins.str,
        author: typing.Optional[typing.Union[SentinelMetadataAuthor, typing.Dict[builtins.str, typing.Any]]] = None,
        category: typing.Optional[typing.Union[SentinelMetadataCategory, typing.Dict[builtins.str, typing.Any]]] = None,
        content_schema_version: typing.Optional[builtins.str] = None,
        custom_version: typing.Optional[builtins.str] = None,
        dependency: typing.Optional[builtins.str] = None,
        first_publish_date: typing.Optional[builtins.str] = None,
        icon_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_publish_date: typing.Optional[builtins.str] = None,
        preview_images: typing.Optional[typing.Sequence[builtins.str]] = None,
        preview_images_dark: typing.Optional[typing.Sequence[builtins.str]] = None,
        providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[typing.Union["SentinelMetadataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        support: typing.Optional[typing.Union["SentinelMetadataSupport", typing.Dict[builtins.str, typing.Any]]] = None,
        threat_analysis_tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
        threat_analysis_techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SentinelMetadataTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param content_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#content_id SentinelMetadata#content_id}.
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#kind SentinelMetadata#kind}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        :param parent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#parent_id SentinelMetadata#parent_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#workspace_id SentinelMetadata#workspace_id}.
        :param author: author block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#author SentinelMetadata#author}
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#category SentinelMetadata#category}
        :param content_schema_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#content_schema_version SentinelMetadata#content_schema_version}.
        :param custom_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#custom_version SentinelMetadata#custom_version}.
        :param dependency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#dependency SentinelMetadata#dependency}.
        :param first_publish_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#first_publish_date SentinelMetadata#first_publish_date}.
        :param icon_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#icon_id SentinelMetadata#icon_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#id SentinelMetadata#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_publish_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#last_publish_date SentinelMetadata#last_publish_date}.
        :param preview_images: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#preview_images SentinelMetadata#preview_images}.
        :param preview_images_dark: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#preview_images_dark SentinelMetadata#preview_images_dark}.
        :param providers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#providers SentinelMetadata#providers}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#source SentinelMetadata#source}
        :param support: support block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#support SentinelMetadata#support}
        :param threat_analysis_tactics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#threat_analysis_tactics SentinelMetadata#threat_analysis_tactics}.
        :param threat_analysis_techniques: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#threat_analysis_techniques SentinelMetadata#threat_analysis_techniques}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#timeouts SentinelMetadata#timeouts}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#version SentinelMetadata#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(author, dict):
            author = SentinelMetadataAuthor(**author)
        if isinstance(category, dict):
            category = SentinelMetadataCategory(**category)
        if isinstance(source, dict):
            source = SentinelMetadataSource(**source)
        if isinstance(support, dict):
            support = SentinelMetadataSupport(**support)
        if isinstance(timeouts, dict):
            timeouts = SentinelMetadataTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd55705d8dde92f38bd847f0af1134933b9bf4292bca4472d7ff5f999d07bb03)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument content_id", value=content_id, expected_type=type_hints["content_id"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_id", value=parent_id, expected_type=type_hints["parent_id"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument author", value=author, expected_type=type_hints["author"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument content_schema_version", value=content_schema_version, expected_type=type_hints["content_schema_version"])
            check_type(argname="argument custom_version", value=custom_version, expected_type=type_hints["custom_version"])
            check_type(argname="argument dependency", value=dependency, expected_type=type_hints["dependency"])
            check_type(argname="argument first_publish_date", value=first_publish_date, expected_type=type_hints["first_publish_date"])
            check_type(argname="argument icon_id", value=icon_id, expected_type=type_hints["icon_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument last_publish_date", value=last_publish_date, expected_type=type_hints["last_publish_date"])
            check_type(argname="argument preview_images", value=preview_images, expected_type=type_hints["preview_images"])
            check_type(argname="argument preview_images_dark", value=preview_images_dark, expected_type=type_hints["preview_images_dark"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument support", value=support, expected_type=type_hints["support"])
            check_type(argname="argument threat_analysis_tactics", value=threat_analysis_tactics, expected_type=type_hints["threat_analysis_tactics"])
            check_type(argname="argument threat_analysis_techniques", value=threat_analysis_techniques, expected_type=type_hints["threat_analysis_techniques"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_id": content_id,
            "kind": kind,
            "name": name,
            "parent_id": parent_id,
            "workspace_id": workspace_id,
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
        if author is not None:
            self._values["author"] = author
        if category is not None:
            self._values["category"] = category
        if content_schema_version is not None:
            self._values["content_schema_version"] = content_schema_version
        if custom_version is not None:
            self._values["custom_version"] = custom_version
        if dependency is not None:
            self._values["dependency"] = dependency
        if first_publish_date is not None:
            self._values["first_publish_date"] = first_publish_date
        if icon_id is not None:
            self._values["icon_id"] = icon_id
        if id is not None:
            self._values["id"] = id
        if last_publish_date is not None:
            self._values["last_publish_date"] = last_publish_date
        if preview_images is not None:
            self._values["preview_images"] = preview_images
        if preview_images_dark is not None:
            self._values["preview_images_dark"] = preview_images_dark
        if providers is not None:
            self._values["providers"] = providers
        if source is not None:
            self._values["source"] = source
        if support is not None:
            self._values["support"] = support
        if threat_analysis_tactics is not None:
            self._values["threat_analysis_tactics"] = threat_analysis_tactics
        if threat_analysis_techniques is not None:
            self._values["threat_analysis_techniques"] = threat_analysis_techniques
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version

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
    def content_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#content_id SentinelMetadata#content_id}.'''
        result = self._values.get("content_id")
        assert result is not None, "Required property 'content_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#kind SentinelMetadata#kind}.'''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#parent_id SentinelMetadata#parent_id}.'''
        result = self._values.get("parent_id")
        assert result is not None, "Required property 'parent_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#workspace_id SentinelMetadata#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def author(self) -> typing.Optional[SentinelMetadataAuthor]:
        '''author block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#author SentinelMetadata#author}
        '''
        result = self._values.get("author")
        return typing.cast(typing.Optional[SentinelMetadataAuthor], result)

    @builtins.property
    def category(self) -> typing.Optional[SentinelMetadataCategory]:
        '''category block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#category SentinelMetadata#category}
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional[SentinelMetadataCategory], result)

    @builtins.property
    def content_schema_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#content_schema_version SentinelMetadata#content_schema_version}.'''
        result = self._values.get("content_schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#custom_version SentinelMetadata#custom_version}.'''
        result = self._values.get("custom_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#dependency SentinelMetadata#dependency}.'''
        result = self._values.get("dependency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_publish_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#first_publish_date SentinelMetadata#first_publish_date}.'''
        result = self._values.get("first_publish_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#icon_id SentinelMetadata#icon_id}.'''
        result = self._values.get("icon_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#id SentinelMetadata#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_publish_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#last_publish_date SentinelMetadata#last_publish_date}.'''
        result = self._values.get("last_publish_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preview_images(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#preview_images SentinelMetadata#preview_images}.'''
        result = self._values.get("preview_images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preview_images_dark(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#preview_images_dark SentinelMetadata#preview_images_dark}.'''
        result = self._values.get("preview_images_dark")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def providers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#providers SentinelMetadata#providers}.'''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional["SentinelMetadataSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#source SentinelMetadata#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["SentinelMetadataSource"], result)

    @builtins.property
    def support(self) -> typing.Optional["SentinelMetadataSupport"]:
        '''support block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#support SentinelMetadata#support}
        '''
        result = self._values.get("support")
        return typing.cast(typing.Optional["SentinelMetadataSupport"], result)

    @builtins.property
    def threat_analysis_tactics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#threat_analysis_tactics SentinelMetadata#threat_analysis_tactics}.'''
        result = self._values.get("threat_analysis_tactics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def threat_analysis_techniques(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#threat_analysis_techniques SentinelMetadata#threat_analysis_techniques}.'''
        result = self._values.get("threat_analysis_techniques")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SentinelMetadataTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#timeouts SentinelMetadata#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SentinelMetadataTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#version SentinelMetadata#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelMetadataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataSource",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "id": "id", "name": "name"},
)
class SentinelMetadataSource:
    def __init__(
        self,
        *,
        kind: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#kind SentinelMetadata#kind}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#id SentinelMetadata#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebfe8a78cf73e7ab50cdf6ac5d2b9840c4b0ef49212743bdc002bb73b5fae26)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
        }
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def kind(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#kind SentinelMetadata#kind}.'''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#id SentinelMetadata#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelMetadataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelMetadataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87e99219d6052507660e1794990131ea9346fd98aa01bf1d51e91913a2876629)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04625acecd62f25cda9c566890d43121f0ddc3b3148b732735dffec6dea89117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e623b7c310ed197236a79961183da8ecff53573b347181b07e5d777052ab999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e84ccbfd4d8c6fcfeedd12b3dfbe5b779f8c24ba66f1c80c09d3245a33408b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelMetadataSource]:
        return typing.cast(typing.Optional[SentinelMetadataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SentinelMetadataSource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67b9a64843280bd49016f73e6e530a4e24d853068b30383bfa14bfe3b13972b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataSupport",
    jsii_struct_bases=[],
    name_mapping={"tier": "tier", "email": "email", "link": "link", "name": "name"},
)
class SentinelMetadataSupport:
    def __init__(
        self,
        *,
        tier: builtins.str,
        email: typing.Optional[builtins.str] = None,
        link: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#tier SentinelMetadata#tier}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#email SentinelMetadata#email}.
        :param link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#link SentinelMetadata#link}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543483fe3d0fae3b6e4fa15850e40cf55c4f4be1447087865929bedf0557d3ee)
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tier": tier,
        }
        if email is not None:
            self._values["email"] = email
        if link is not None:
            self._values["link"] = link
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#tier SentinelMetadata#tier}.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#email SentinelMetadata#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#link SentinelMetadata#link}.'''
        result = self._values.get("link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#name SentinelMetadata#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelMetadataSupport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelMetadataSupportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataSupportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3119842fc8437fcea5bf951eb71a1f388122385165d0faad25d741ad63b52e74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetLink")
    def reset_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLink", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="linkInput")
    def link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862769994bc726c13c8862b3ce0fdec27ab01bf69cdd6658b1529caeef94c99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="link")
    def link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "link"))

    @link.setter
    def link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8928c58c173aa8cbb2237e9f388efb7ecfe1b58bd6aa4f0c2d7645a061715003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "link", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f5414e65b50cef1b0a3b7ff9ef59256ddcdc3268b42414d476528e40e47998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93841d59eb5d780c449e4d0169de9d053dc3bd010a76190a1d0f077b72719de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SentinelMetadataSupport]:
        return typing.cast(typing.Optional[SentinelMetadataSupport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SentinelMetadataSupport]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2397ab48ddee24133c04e19f2972eead40e98c68c1194c0c52d20b5f095e82ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SentinelMetadataTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#create SentinelMetadata#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#delete SentinelMetadata#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#read SentinelMetadata#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#update SentinelMetadata#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a93f50856031bdf91142b70a03d7673f222a0bb01ec65fff6d55262750ce882)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#create SentinelMetadata#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#delete SentinelMetadata#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#read SentinelMetadata#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/sentinel_metadata#update SentinelMetadata#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelMetadataTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelMetadataTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sentinelMetadata.SentinelMetadataTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6a509e6f52f37eadf15b607c51deef5de44a6e7d4354a29412f18777e71a3d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfecade18fd906f7e612b632fde0311ccbac65e0768725b71d694203f26a521f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef54505e7bc8d11ddfa18aee61e5ee84d02acc6a87ed72bdabc6dea01d964adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456e36f617b6d116d2e792cab63427487987c6ccf1be5a61c3683ac6ae4d2038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb9ec24ea6c56ea984f46ab349c6f1f3da4dc3b87b1e9c972487798acee4e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelMetadataTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelMetadataTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelMetadataTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb88a6d1d6fac66f53a6ce6409cd37494f64dfe1c4d791e4d061751965b4bc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SentinelMetadata",
    "SentinelMetadataAuthor",
    "SentinelMetadataAuthorOutputReference",
    "SentinelMetadataCategory",
    "SentinelMetadataCategoryOutputReference",
    "SentinelMetadataConfig",
    "SentinelMetadataSource",
    "SentinelMetadataSourceOutputReference",
    "SentinelMetadataSupport",
    "SentinelMetadataSupportOutputReference",
    "SentinelMetadataTimeouts",
    "SentinelMetadataTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__eeb7b0869e58477772edef655345453a35bca208a06e79978c98b40c8bde5c86(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    content_id: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    parent_id: builtins.str,
    workspace_id: builtins.str,
    author: typing.Optional[typing.Union[SentinelMetadataAuthor, typing.Dict[builtins.str, typing.Any]]] = None,
    category: typing.Optional[typing.Union[SentinelMetadataCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    content_schema_version: typing.Optional[builtins.str] = None,
    custom_version: typing.Optional[builtins.str] = None,
    dependency: typing.Optional[builtins.str] = None,
    first_publish_date: typing.Optional[builtins.str] = None,
    icon_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_publish_date: typing.Optional[builtins.str] = None,
    preview_images: typing.Optional[typing.Sequence[builtins.str]] = None,
    preview_images_dark: typing.Optional[typing.Sequence[builtins.str]] = None,
    providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[typing.Union[SentinelMetadataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    support: typing.Optional[typing.Union[SentinelMetadataSupport, typing.Dict[builtins.str, typing.Any]]] = None,
    threat_analysis_tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_analysis_techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SentinelMetadataTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e1476ef4ffc3392d6b5c5bc2b3410a8d97e05dafa9e575158f7201a96652b168(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb5249399217972ff2b7856a99283e4f7e30b0edb539c4dc2d6f139b578baf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a279769fce5aeef63196b2ad7797bde2ed7320f07a941956f273edac74720b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a097ace864dabff32fe7b5fb071cec7cd457ceb13fc02b900b46c851a9e4c9cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6337b1791a7f4b0903202199791c507e23cf9c8e118602931e69c1895d90cc36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793327fb06b15b83f45ea87ea86de2520b39f46774d9e546125d655b7a913a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd991aaf680e5e67e4498bc2c963728d5550ca7dc1ca4083e7fa0fff5bf4e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5903fa3a75a115a4a70478ca168595f17b93e7095439c8dc744384bb64edfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505b61c9047786eacccbeb6cf48f5cd38f8945002a4abb5d6cc38cd5fbf9100a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee910699e9794a5da40f53456642bfa6c45ece296682528e81f8e3093841e8a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767fc6d2c38085317a25eea6fdcacfb192e7122f99598adafbada471c3c08c81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4afa216540053b5489ee4043195264955d51549c21cfbbdde5a1c6891f70db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e268e8ae7c999328d7125d3e1a95c8e61935a193ded4779a3e5f6e41f1e66c8c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624ab8f2aa5c613a0eddf1979d069ce358bc2ed7b53f017a7e2c65ba6ebd9a2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbd146648d126015b745b012ef6c5b26bb4c4b00f5cb95f3b12e286051326d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809acf614df550574e7c7130542c3eaf170607bbf93d5d0c2cfafd16e9111d21(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd017740c646a54d582bdf44bf7ac46eb231e05d923e539d89f08cbc6f821e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ef3ff02f1dd5324defdb38e5d8a12395f367fc441c059fa6d15e5253792e85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a70bf250d29859c592ec1623a27b0508821762380a49c910fe08d5b8d5390e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b3aae49093ac4fc2d0333f657975845ee35ceec4bcb4878c650d1eebe8542f(
    *,
    email: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af91aeb17b5ba15f0a76c3f20dc979aa77d7151fe0c3c6d17dd336c920063cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7171cb7ce1e0aa12a780281e5d9cebb2e9c43885fa46ae20c442239877ed14b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f6490c30243f39c343056919af9c1c77379fdd078908e6c75b6add01c663c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25489aeb509877f2317cc2b25e5d8ffd4b901360a783e319afb502e04da6a636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec678b2ae70fef1cb12202b7ae08cd6ab1a86a5691936c3cea7d9ca3283d97ae(
    value: typing.Optional[SentinelMetadataAuthor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972d16e71549b5578afa20c7d4f95d65804a19d8523b4b626114c70c606eab50(
    *,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    verticals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d713adcbf868673d166c35255eb99bce3e969e715e7f82fc7d381c73fab0f303(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda0428242a9db2de9f15a4baae5e4967b95b270b774ace465b02b40cc425d24(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a06574baa795b934639a7bad872150170dd23dcd2c2fd221a5b74e0e2e9370a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0127decb8470782693675decec27004a04cfd03f089834103e39e01476254308(
    value: typing.Optional[SentinelMetadataCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd55705d8dde92f38bd847f0af1134933b9bf4292bca4472d7ff5f999d07bb03(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_id: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    parent_id: builtins.str,
    workspace_id: builtins.str,
    author: typing.Optional[typing.Union[SentinelMetadataAuthor, typing.Dict[builtins.str, typing.Any]]] = None,
    category: typing.Optional[typing.Union[SentinelMetadataCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    content_schema_version: typing.Optional[builtins.str] = None,
    custom_version: typing.Optional[builtins.str] = None,
    dependency: typing.Optional[builtins.str] = None,
    first_publish_date: typing.Optional[builtins.str] = None,
    icon_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_publish_date: typing.Optional[builtins.str] = None,
    preview_images: typing.Optional[typing.Sequence[builtins.str]] = None,
    preview_images_dark: typing.Optional[typing.Sequence[builtins.str]] = None,
    providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[typing.Union[SentinelMetadataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    support: typing.Optional[typing.Union[SentinelMetadataSupport, typing.Dict[builtins.str, typing.Any]]] = None,
    threat_analysis_tactics: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_analysis_techniques: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SentinelMetadataTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebfe8a78cf73e7ab50cdf6ac5d2b9840c4b0ef49212743bdc002bb73b5fae26(
    *,
    kind: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e99219d6052507660e1794990131ea9346fd98aa01bf1d51e91913a2876629(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04625acecd62f25cda9c566890d43121f0ddc3b3148b732735dffec6dea89117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e623b7c310ed197236a79961183da8ecff53573b347181b07e5d777052ab999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e84ccbfd4d8c6fcfeedd12b3dfbe5b779f8c24ba66f1c80c09d3245a33408b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67b9a64843280bd49016f73e6e530a4e24d853068b30383bfa14bfe3b13972b(
    value: typing.Optional[SentinelMetadataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543483fe3d0fae3b6e4fa15850e40cf55c4f4be1447087865929bedf0557d3ee(
    *,
    tier: builtins.str,
    email: typing.Optional[builtins.str] = None,
    link: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3119842fc8437fcea5bf951eb71a1f388122385165d0faad25d741ad63b52e74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862769994bc726c13c8862b3ce0fdec27ab01bf69cdd6658b1529caeef94c99c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8928c58c173aa8cbb2237e9f388efb7ecfe1b58bd6aa4f0c2d7645a061715003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f5414e65b50cef1b0a3b7ff9ef59256ddcdc3268b42414d476528e40e47998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93841d59eb5d780c449e4d0169de9d053dc3bd010a76190a1d0f077b72719de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2397ab48ddee24133c04e19f2972eead40e98c68c1194c0c52d20b5f095e82ab(
    value: typing.Optional[SentinelMetadataSupport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a93f50856031bdf91142b70a03d7673f222a0bb01ec65fff6d55262750ce882(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a509e6f52f37eadf15b607c51deef5de44a6e7d4354a29412f18777e71a3d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfecade18fd906f7e612b632fde0311ccbac65e0768725b71d694203f26a521f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef54505e7bc8d11ddfa18aee61e5ee84d02acc6a87ed72bdabc6dea01d964adf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456e36f617b6d116d2e792cab63427487987c6ccf1be5a61c3683ac6ae4d2038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb9ec24ea6c56ea984f46ab349c6f1f3da4dc3b87b1e9c972487798acee4e2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb88a6d1d6fac66f53a6ce6409cd37494f64dfe1c4d791e4d061751965b4bc67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SentinelMetadataTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
