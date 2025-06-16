r'''
# `google_bigquery_analytics_hub_listing`

Refer to the Terraform Registry for docs: [`google_bigquery_analytics_hub_listing`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing).
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


class GoogleBigqueryAnalyticsHubListing(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListing",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bigquery_dataset: typing.Union["GoogleBigqueryAnalyticsHubListingBigqueryDataset", typing.Dict[builtins.str, typing.Any]],
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingDataProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingPublisher", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        restricted_export_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingRestrictedExportConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#bigquery_dataset GoogleBigqueryAnalyticsHubListing#bigquery_dataset}
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#data_exchange_id GoogleBigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#display_name GoogleBigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#listing_id GoogleBigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#location GoogleBigqueryAnalyticsHubListing#location}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#categories GoogleBigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#data_provider GoogleBigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#description GoogleBigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#documentation GoogleBigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#icon GoogleBigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#id GoogleBigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#project GoogleBigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#publisher GoogleBigqueryAnalyticsHubListing#publisher}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#request_access GoogleBigqueryAnalyticsHubListing#request_access}
        :param restricted_export_config: restricted_export_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#restricted_export_config GoogleBigqueryAnalyticsHubListing#restricted_export_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#timeouts GoogleBigqueryAnalyticsHubListing#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f1f2677cbe3d7372e4162c32a922d59f80ad350f54b4f5717154c71af05ad8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigqueryAnalyticsHubListingConfig(
            bigquery_dataset=bigquery_dataset,
            data_exchange_id=data_exchange_id,
            display_name=display_name,
            listing_id=listing_id,
            location=location,
            categories=categories,
            data_provider=data_provider,
            description=description,
            documentation=documentation,
            icon=icon,
            id=id,
            primary_contact=primary_contact,
            project=project,
            publisher=publisher,
            request_access=request_access,
            restricted_export_config=restricted_export_config,
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
        '''Generates CDKTF code for importing a GoogleBigqueryAnalyticsHubListing resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBigqueryAnalyticsHubListing to import.
        :param import_from_id: The id of the existing GoogleBigqueryAnalyticsHubListing that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBigqueryAnalyticsHubListing to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72efec56cf9258f2ebe141dd9cd51d4d2279c0a930da9cc99c74db607f5b6b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigqueryDataset")
    def put_bigquery_dataset(
        self,
        *,
        dataset: builtins.str,
        selected_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#dataset GoogleBigqueryAnalyticsHubListing#dataset}
        :param selected_resources: selected_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#selected_resources GoogleBigqueryAnalyticsHubListing#selected_resources}
        '''
        value = GoogleBigqueryAnalyticsHubListingBigqueryDataset(
            dataset=dataset, selected_resources=selected_resources
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryDataset", [value]))

    @jsii.member(jsii_name="putDataProvider")
    def put_data_provider(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        value = GoogleBigqueryAnalyticsHubListingDataProvider(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putDataProvider", [value]))

    @jsii.member(jsii_name="putPublisher")
    def put_publisher(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        value = GoogleBigqueryAnalyticsHubListingPublisher(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putPublisher", [value]))

    @jsii.member(jsii_name="putRestrictedExportConfig")
    def put_restricted_export_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_query_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: If true, enable restricted export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#enabled GoogleBigqueryAnalyticsHubListing#enabled}
        :param restrict_query_result: If true, restrict export of query result derived from restricted linked dataset table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#restrict_query_result GoogleBigqueryAnalyticsHubListing#restrict_query_result}
        '''
        value = GoogleBigqueryAnalyticsHubListingRestrictedExportConfig(
            enabled=enabled, restrict_query_result=restrict_query_result
        )

        return typing.cast(None, jsii.invoke(self, "putRestrictedExportConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#create GoogleBigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#delete GoogleBigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#update GoogleBigqueryAnalyticsHubListing#update}.
        '''
        value = GoogleBigqueryAnalyticsHubListingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCategories")
    def reset_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategories", []))

    @jsii.member(jsii_name="resetDataProvider")
    def reset_data_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProvider", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentation")
    def reset_documentation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentation", []))

    @jsii.member(jsii_name="resetIcon")
    def reset_icon(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcon", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetRequestAccess")
    def reset_request_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestAccess", []))

    @jsii.member(jsii_name="resetRestrictedExportConfig")
    def reset_restricted_export_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedExportConfig", []))

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
    @jsii.member(jsii_name="bigqueryDataset")
    def bigquery_dataset(
        self,
    ) -> "GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference", jsii.get(self, "bigqueryDataset"))

    @builtins.property
    @jsii.member(jsii_name="dataProvider")
    def data_provider(
        self,
    ) -> "GoogleBigqueryAnalyticsHubListingDataProviderOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingDataProviderOutputReference", jsii.get(self, "dataProvider"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> "GoogleBigqueryAnalyticsHubListingPublisherOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingPublisherOutputReference", jsii.get(self, "publisher"))

    @builtins.property
    @jsii.member(jsii_name="restrictedExportConfig")
    def restricted_export_config(
        self,
    ) -> "GoogleBigqueryAnalyticsHubListingRestrictedExportConfigOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingRestrictedExportConfigOutputReference", jsii.get(self, "restrictedExportConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDatasetInput")
    def bigquery_dataset_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingBigqueryDataset"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingBigqueryDataset"], jsii.get(self, "bigqueryDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="categoriesInput")
    def categories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "categoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeIdInput")
    def data_exchange_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataExchangeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProviderInput")
    def data_provider_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"], jsii.get(self, "dataProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationInput")
    def documentation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentationInput"))

    @builtins.property
    @jsii.member(jsii_name="iconInput")
    def icon_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="listingIdInput")
    def listing_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessInput")
    def request_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedExportConfigInput")
    def restricted_export_config_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingRestrictedExportConfig"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingRestrictedExportConfig"], jsii.get(self, "restrictedExportConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryAnalyticsHubListingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryAnalyticsHubListingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c47140d8f889b0c9f274330d749b69074ba5e0c9f8aa03e9f374769e98795a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataExchangeId")
    def data_exchange_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataExchangeId"))

    @data_exchange_id.setter
    def data_exchange_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06e2d312321a9ecc662ceefe6c4ca80d3d97d1ca24b63f983d2ed14941fdd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExchangeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543a5417ca58049205ebe3c11a77d18219fe46b69a03f038f87b02261c924266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676c80bd8fcc45d14203edc3bc0c3a501d7d16d0ffa90e10e203a4b0b7dfe5df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentation"))

    @documentation.setter
    def documentation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8995ccf7e5c997d1aa065257604d36c1468c1791e9fe2586c43eb310de401f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="icon")
    def icon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icon"))

    @icon.setter
    def icon(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a57bd256d505c218123a3427ef2ccab9241c824c3c228dc92e70555c1d5da2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icon", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af712e1a318ea2d85d6badb3a2ff4ac04e9322b05144fc8c66eaf96e7f799325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listingId")
    def listing_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listingId"))

    @listing_id.setter
    def listing_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78516182e4643e21fe38f3948e97158ca8842e6722b8f1dd361dad1329c63ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listingId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001eb1733bcd8934d836909fab0ee71a9e922f78ea9c62bd63a1091ed6fbd4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fec1bc3f8bb8af1bd53476ae2203c81e77a1f6f6ce34b213040e3f81cf3e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a269c38f8627b4120973bb3cc444986b9c07486d661e82d4c2bfbefdc308f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestAccess")
    def request_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestAccess"))

    @request_access.setter
    def request_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec38b8dcbe50f1957c7715772d946b5a3ff01149f671e2f759ba1e9ced671ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestAccess", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset", "selected_resources": "selectedResources"},
)
class GoogleBigqueryAnalyticsHubListingBigqueryDataset:
    def __init__(
        self,
        *,
        dataset: builtins.str,
        selected_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#dataset GoogleBigqueryAnalyticsHubListing#dataset}
        :param selected_resources: selected_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#selected_resources GoogleBigqueryAnalyticsHubListing#selected_resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba5184b6f5dac8efba253aa46a3de2fb7d90a8c6f444fbe8dc7938f2bb1fbc8)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument selected_resources", value=selected_resources, expected_type=type_hints["selected_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
        }
        if selected_resources is not None:
            self._values["selected_resources"] = selected_resources

    @builtins.property
    def dataset(self) -> builtins.str:
        '''Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#dataset GoogleBigqueryAnalyticsHubListing#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selected_resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]]:
        '''selected_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#selected_resources GoogleBigqueryAnalyticsHubListing#selected_resources}
        '''
        result = self._values.get("selected_resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingBigqueryDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b29b0b17c081b01c914964a9ee6493d3c2bef13ab8e62ebe9c95688b5d093b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectedResources")
    def put_selected_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab00de1257008130f44bd6dfb05b2fca35bcfa8a53fcca0ca1036dae0cee443b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectedResources", [value]))

    @jsii.member(jsii_name="resetSelectedResources")
    def reset_selected_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedResources", []))

    @builtins.property
    @jsii.member(jsii_name="selectedResources")
    def selected_resources(
        self,
    ) -> "GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList":
        return typing.cast("GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList", jsii.get(self, "selectedResources"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedResourcesInput")
    def selected_resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]], jsii.get(self, "selectedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e235878681bf8aed65ac945482c9d78c64f6990b8604ece55d40ded90bf6c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b5d05ec5dc40d8b6988fd480828c7218ddd81823abe8092ea64b0210e1a0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources",
    jsii_struct_bases=[],
    name_mapping={"table": "table"},
)
class GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources:
    def __init__(self, *, table: typing.Optional[builtins.str] = None) -> None:
        '''
        :param table: Format: For table: projects/{projectId}/datasets/{datasetId}/tables/{tableId} Example:"projects/test_project/datasets/test_dataset/tables/test_table". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#table GoogleBigqueryAnalyticsHubListing#table}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcda91e78009bffa5b393ba6a54ffe04beefc4d1eb02793b70c62bac4cf26f11)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if table is not None:
            self._values["table"] = table

    @builtins.property
    def table(self) -> typing.Optional[builtins.str]:
        '''Format: For table: projects/{projectId}/datasets/{datasetId}/tables/{tableId} Example:"projects/test_project/datasets/test_dataset/tables/test_table".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#table GoogleBigqueryAnalyticsHubListing#table}
        '''
        result = self._values.get("table")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f239990632e213691cd7c5f0200a3a9fd6b7267db8e104a6dfbf96064e52f1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999b1cb8cbbb867119138d25114eb9ebdca8216b8229e9f0eb7c04e02bc45648)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b495736944b1c0eef21b1be4c0d5d2705b649426fdf122c8d81e066a279afcd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__803d4dfa39f4d936ba00390fee6865e28bc42be964d9fbf5972831254befb2a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d9736464a41c882eb3db73af462d28905bc0ce2899cb64706c948247cb1eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7400d14383b174bfe46ae0df1f9c07bcfe1e3e73bbc89cc373b053da109614d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9509eec1a9990bd4c2ffb103122f4a91e6510b7987682285e9b722b2fa3dcf4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTable")
    def reset_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTable", []))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ef9c25103e75231d75e6b775a9bdbac821ac6c86c963d2fec6cfc6b1338ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ac6272a7301af975a2301a1a17bf244493401cb499e11cf35589ccbe47297c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bigquery_dataset": "bigqueryDataset",
        "data_exchange_id": "dataExchangeId",
        "display_name": "displayName",
        "listing_id": "listingId",
        "location": "location",
        "categories": "categories",
        "data_provider": "dataProvider",
        "description": "description",
        "documentation": "documentation",
        "icon": "icon",
        "id": "id",
        "primary_contact": "primaryContact",
        "project": "project",
        "publisher": "publisher",
        "request_access": "requestAccess",
        "restricted_export_config": "restrictedExportConfig",
        "timeouts": "timeouts",
    },
)
class GoogleBigqueryAnalyticsHubListingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bigquery_dataset: typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]],
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingDataProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingPublisher", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        restricted_export_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingRestrictedExportConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#bigquery_dataset GoogleBigqueryAnalyticsHubListing#bigquery_dataset}
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#data_exchange_id GoogleBigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#display_name GoogleBigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#listing_id GoogleBigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#location GoogleBigqueryAnalyticsHubListing#location}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#categories GoogleBigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#data_provider GoogleBigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#description GoogleBigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#documentation GoogleBigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#icon GoogleBigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#id GoogleBigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#project GoogleBigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#publisher GoogleBigqueryAnalyticsHubListing#publisher}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#request_access GoogleBigqueryAnalyticsHubListing#request_access}
        :param restricted_export_config: restricted_export_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#restricted_export_config GoogleBigqueryAnalyticsHubListing#restricted_export_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#timeouts GoogleBigqueryAnalyticsHubListing#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_dataset, dict):
            bigquery_dataset = GoogleBigqueryAnalyticsHubListingBigqueryDataset(**bigquery_dataset)
        if isinstance(data_provider, dict):
            data_provider = GoogleBigqueryAnalyticsHubListingDataProvider(**data_provider)
        if isinstance(publisher, dict):
            publisher = GoogleBigqueryAnalyticsHubListingPublisher(**publisher)
        if isinstance(restricted_export_config, dict):
            restricted_export_config = GoogleBigqueryAnalyticsHubListingRestrictedExportConfig(**restricted_export_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigqueryAnalyticsHubListingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b367299b584303edcf955004e12a3ce60a97c165fef439299e059ab9e25c76a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bigquery_dataset", value=bigquery_dataset, expected_type=type_hints["bigquery_dataset"])
            check_type(argname="argument data_exchange_id", value=data_exchange_id, expected_type=type_hints["data_exchange_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument listing_id", value=listing_id, expected_type=type_hints["listing_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument data_provider", value=data_provider, expected_type=type_hints["data_provider"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument icon", value=icon, expected_type=type_hints["icon"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument request_access", value=request_access, expected_type=type_hints["request_access"])
            check_type(argname="argument restricted_export_config", value=restricted_export_config, expected_type=type_hints["restricted_export_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bigquery_dataset": bigquery_dataset,
            "data_exchange_id": data_exchange_id,
            "display_name": display_name,
            "listing_id": listing_id,
            "location": location,
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
        if categories is not None:
            self._values["categories"] = categories
        if data_provider is not None:
            self._values["data_provider"] = data_provider
        if description is not None:
            self._values["description"] = description
        if documentation is not None:
            self._values["documentation"] = documentation
        if icon is not None:
            self._values["icon"] = icon
        if id is not None:
            self._values["id"] = id
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact
        if project is not None:
            self._values["project"] = project
        if publisher is not None:
            self._values["publisher"] = publisher
        if request_access is not None:
            self._values["request_access"] = request_access
        if restricted_export_config is not None:
            self._values["restricted_export_config"] = restricted_export_config
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
    def bigquery_dataset(self) -> GoogleBigqueryAnalyticsHubListingBigqueryDataset:
        '''bigquery_dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#bigquery_dataset GoogleBigqueryAnalyticsHubListing#bigquery_dataset}
        '''
        result = self._values.get("bigquery_dataset")
        assert result is not None, "Required property 'bigquery_dataset' is missing"
        return typing.cast(GoogleBigqueryAnalyticsHubListingBigqueryDataset, result)

    @builtins.property
    def data_exchange_id(self) -> builtins.str:
        '''The ID of the data exchange.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#data_exchange_id GoogleBigqueryAnalyticsHubListing#data_exchange_id}
        '''
        result = self._values.get("data_exchange_id")
        assert result is not None, "Required property 'data_exchange_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Human-readable display name of the listing.

        The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#display_name GoogleBigqueryAnalyticsHubListing#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listing_id(self) -> builtins.str:
        '''The ID of the listing.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#listing_id GoogleBigqueryAnalyticsHubListing#listing_id}
        '''
        result = self._values.get("listing_id")
        assert result is not None, "Required property 'listing_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this data exchange listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#location GoogleBigqueryAnalyticsHubListing#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Categories of the listing. Up to two categories are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#categories GoogleBigqueryAnalyticsHubListing#categories}
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_provider(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"]:
        '''data_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#data_provider GoogleBigqueryAnalyticsHubListing#data_provider}
        '''
        result = self._values.get("data_provider")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Short description of the listing.

        The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#description GoogleBigqueryAnalyticsHubListing#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional[builtins.str]:
        '''Documentation describing the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#documentation GoogleBigqueryAnalyticsHubListing#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded image representing the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#icon GoogleBigqueryAnalyticsHubListing#icon}
        '''
        result = self._values.get("icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#id GoogleBigqueryAnalyticsHubListing#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the primary point of contact of the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#project GoogleBigqueryAnalyticsHubListing#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"]:
        '''publisher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#publisher GoogleBigqueryAnalyticsHubListing#publisher}
        '''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"], result)

    @builtins.property
    def request_access(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the request access of the listing. Subscribers can use this reference to request access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#request_access GoogleBigqueryAnalyticsHubListing#request_access}
        '''
        result = self._values.get("request_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restricted_export_config(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingRestrictedExportConfig"]:
        '''restricted_export_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#restricted_export_config GoogleBigqueryAnalyticsHubListing#restricted_export_config}
        '''
        result = self._values.get("restricted_export_config")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingRestrictedExportConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBigqueryAnalyticsHubListingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#timeouts GoogleBigqueryAnalyticsHubListing#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingDataProvider",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class GoogleBigqueryAnalyticsHubListingDataProvider:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a6fd7afc595083d937c8fd2af6eae161bfd7b8b442798e093deb4b6d960e57)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the data provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the data provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingDataProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingDataProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingDataProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0528f306788e22964c863aebdcb350eb374fe24bbad257b3039bb8215c51ee3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff735ac4ddc9adc7f7ceec7aa97163414d722f381dbd9a3e4b2e1fb6e30b77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0267d3df4e933f0870d0b7cc8076c0abf648c49c0c1cf8885278cf27022b637b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cf04f82c031d5483df95e986049ced2c59954397c0d23ae85ce62fbded9b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingPublisher",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class GoogleBigqueryAnalyticsHubListingPublisher:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6855c91baed0b582ed75d400bdf30f6dc374cfa623188fd8324cdf1b48dbb7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the listing publisher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the listing publisher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingPublisher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingPublisherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingPublisherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__797601595df7f568440444b6bbde19522a2a2d798be1173927fd8917074c52e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df9310129f54ce34c18115cd0bb295aa56478f26902e7bdc7ce4781a54d7867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99861882318dce7832326de652d0d717f974e3185bee0445068d35b01176bf0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b47b9776facae2fddbea909028572c1d0f11077ca666e00966ef30de0ded31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingRestrictedExportConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "restrict_query_result": "restrictQueryResult",
    },
)
class GoogleBigqueryAnalyticsHubListingRestrictedExportConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_query_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: If true, enable restricted export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#enabled GoogleBigqueryAnalyticsHubListing#enabled}
        :param restrict_query_result: If true, restrict export of query result derived from restricted linked dataset table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#restrict_query_result GoogleBigqueryAnalyticsHubListing#restrict_query_result}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ade80ac6cac36e30dc717aaab22a84764b1b957cd955666efe81685812ac982)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument restrict_query_result", value=restrict_query_result, expected_type=type_hints["restrict_query_result"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if restrict_query_result is not None:
            self._values["restrict_query_result"] = restrict_query_result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable restricted export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#enabled GoogleBigqueryAnalyticsHubListing#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrict_query_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, restrict export of query result derived from restricted linked dataset table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#restrict_query_result GoogleBigqueryAnalyticsHubListing#restrict_query_result}
        '''
        result = self._values.get("restrict_query_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingRestrictedExportConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingRestrictedExportConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingRestrictedExportConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d786f44c748805e32b0acc4251454c0eb11e904caadaed1aac169ab09f08ee60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetRestrictQueryResult")
    def reset_restrict_query_result(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictQueryResult", []))

    @builtins.property
    @jsii.member(jsii_name="restrictDirectTableAccess")
    def restrict_direct_table_access(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "restrictDirectTableAccess"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictQueryResultInput")
    def restrict_query_result_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "restrictQueryResultInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3a62516a952fcbac339a16402836bbf8fcb3f411dec3d42d61c23ba9c5d52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictQueryResult")
    def restrict_query_result(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "restrictQueryResult"))

    @restrict_query_result.setter
    def restrict_query_result(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3102913ee4c605aacfc8cb6b8b9f2ab9ff9a598ae9a2ab36425c110e2b1687a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictQueryResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingRestrictedExportConfig]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingRestrictedExportConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingRestrictedExportConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d86ec380f44c150b7738e30403019aaeda5d895f138ed2e242a243deb8194d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigqueryAnalyticsHubListingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#create GoogleBigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#delete GoogleBigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#update GoogleBigqueryAnalyticsHubListing#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5097e4d0b563172304dd6c1fc502e2d4bd880701da5c2bf2e9300d0ffb10e12a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#create GoogleBigqueryAnalyticsHubListing#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#delete GoogleBigqueryAnalyticsHubListing#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_listing#update GoogleBigqueryAnalyticsHubListing#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbed192342f7e49d37b0a0fca04b982f226ee25e041ed5939a8e3dc1ff67dc28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce256c167438ac30daa25309dab39812d3701aa1263061dd57409a9ae0bd3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1af8fd02bc79208ec79f4bf8343796921809447abd5ac89ae86a21bed3a2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2c264f95b6b9bc0d5587414ec6464c200a2b532dae77edd59bb985981b652c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ebc74d43b8cb89cd4f9c2933d453784491f9deb388b6a0ca3833d2ca3528a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBigqueryAnalyticsHubListing",
    "GoogleBigqueryAnalyticsHubListingBigqueryDataset",
    "GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
    "GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources",
    "GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList",
    "GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference",
    "GoogleBigqueryAnalyticsHubListingConfig",
    "GoogleBigqueryAnalyticsHubListingDataProvider",
    "GoogleBigqueryAnalyticsHubListingDataProviderOutputReference",
    "GoogleBigqueryAnalyticsHubListingPublisher",
    "GoogleBigqueryAnalyticsHubListingPublisherOutputReference",
    "GoogleBigqueryAnalyticsHubListingRestrictedExportConfig",
    "GoogleBigqueryAnalyticsHubListingRestrictedExportConfigOutputReference",
    "GoogleBigqueryAnalyticsHubListingTimeouts",
    "GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__74f1f2677cbe3d7372e4162c32a922d59f80ad350f54b4f5717154c71af05ad8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bigquery_dataset: typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]],
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    listing_id: builtins.str,
    location: builtins.str,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_provider: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingDataProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingPublisher, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access: typing.Optional[builtins.str] = None,
    restricted_export_config: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingRestrictedExportConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b72efec56cf9258f2ebe141dd9cd51d4d2279c0a930da9cc99c74db607f5b6b4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c47140d8f889b0c9f274330d749b69074ba5e0c9f8aa03e9f374769e98795a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06e2d312321a9ecc662ceefe6c4ca80d3d97d1ca24b63f983d2ed14941fdd7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543a5417ca58049205ebe3c11a77d18219fe46b69a03f038f87b02261c924266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676c80bd8fcc45d14203edc3bc0c3a501d7d16d0ffa90e10e203a4b0b7dfe5df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8995ccf7e5c997d1aa065257604d36c1468c1791e9fe2586c43eb310de401f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a57bd256d505c218123a3427ef2ccab9241c824c3c228dc92e70555c1d5da2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af712e1a318ea2d85d6badb3a2ff4ac04e9322b05144fc8c66eaf96e7f799325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78516182e4643e21fe38f3948e97158ca8842e6722b8f1dd361dad1329c63ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001eb1733bcd8934d836909fab0ee71a9e922f78ea9c62bd63a1091ed6fbd4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fec1bc3f8bb8af1bd53476ae2203c81e77a1f6f6ce34b213040e3f81cf3e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a269c38f8627b4120973bb3cc444986b9c07486d661e82d4c2bfbefdc308f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec38b8dcbe50f1957c7715772d946b5a3ff01149f671e2f759ba1e9ced671ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba5184b6f5dac8efba253aa46a3de2fb7d90a8c6f444fbe8dc7938f2bb1fbc8(
    *,
    dataset: builtins.str,
    selected_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b29b0b17c081b01c914964a9ee6493d3c2bef13ab8e62ebe9c95688b5d093b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab00de1257008130f44bd6dfb05b2fca35bcfa8a53fcca0ca1036dae0cee443b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e235878681bf8aed65ac945482c9d78c64f6990b8604ece55d40ded90bf6c25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b5d05ec5dc40d8b6988fd480828c7218ddd81823abe8092ea64b0210e1a0ed(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcda91e78009bffa5b393ba6a54ffe04beefc4d1eb02793b70c62bac4cf26f11(
    *,
    table: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f239990632e213691cd7c5f0200a3a9fd6b7267db8e104a6dfbf96064e52f1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999b1cb8cbbb867119138d25114eb9ebdca8216b8229e9f0eb7c04e02bc45648(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b495736944b1c0eef21b1be4c0d5d2705b649426fdf122c8d81e066a279afcd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803d4dfa39f4d936ba00390fee6865e28bc42be964d9fbf5972831254befb2a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d9736464a41c882eb3db73af462d28905bc0ce2899cb64706c948247cb1eff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7400d14383b174bfe46ae0df1f9c07bcfe1e3e73bbc89cc373b053da109614d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9509eec1a9990bd4c2ffb103122f4a91e6510b7987682285e9b722b2fa3dcf4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ef9c25103e75231d75e6b775a9bdbac821ac6c86c963d2fec6cfc6b1338ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ac6272a7301af975a2301a1a17bf244493401cb499e11cf35589ccbe47297c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b367299b584303edcf955004e12a3ce60a97c165fef439299e059ab9e25c76a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bigquery_dataset: typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]],
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    listing_id: builtins.str,
    location: builtins.str,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_provider: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingDataProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingPublisher, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access: typing.Optional[builtins.str] = None,
    restricted_export_config: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingRestrictedExportConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a6fd7afc595083d937c8fd2af6eae161bfd7b8b442798e093deb4b6d960e57(
    *,
    name: builtins.str,
    primary_contact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0528f306788e22964c863aebdcb350eb374fe24bbad257b3039bb8215c51ee3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff735ac4ddc9adc7f7ceec7aa97163414d722f381dbd9a3e4b2e1fb6e30b77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0267d3df4e933f0870d0b7cc8076c0abf648c49c0c1cf8885278cf27022b637b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cf04f82c031d5483df95e986049ced2c59954397c0d23ae85ce62fbded9b3a(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6855c91baed0b582ed75d400bdf30f6dc374cfa623188fd8324cdf1b48dbb7(
    *,
    name: builtins.str,
    primary_contact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797601595df7f568440444b6bbde19522a2a2d798be1173927fd8917074c52e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df9310129f54ce34c18115cd0bb295aa56478f26902e7bdc7ce4781a54d7867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99861882318dce7832326de652d0d717f974e3185bee0445068d35b01176bf0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b47b9776facae2fddbea909028572c1d0f11077ca666e00966ef30de0ded31b(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ade80ac6cac36e30dc717aaab22a84764b1b957cd955666efe81685812ac982(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_query_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d786f44c748805e32b0acc4251454c0eb11e904caadaed1aac169ab09f08ee60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3a62516a952fcbac339a16402836bbf8fcb3f411dec3d42d61c23ba9c5d52f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3102913ee4c605aacfc8cb6b8b9f2ab9ff9a598ae9a2ab36425c110e2b1687a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d86ec380f44c150b7738e30403019aaeda5d895f138ed2e242a243deb8194d(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingRestrictedExportConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5097e4d0b563172304dd6c1fc502e2d4bd880701da5c2bf2e9300d0ffb10e12a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbed192342f7e49d37b0a0fca04b982f226ee25e041ed5939a8e3dc1ff67dc28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce256c167438ac30daa25309dab39812d3701aa1263061dd57409a9ae0bd3fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1af8fd02bc79208ec79f4bf8343796921809447abd5ac89ae86a21bed3a2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2c264f95b6b9bc0d5587414ec6464c200a2b532dae77edd59bb985981b652c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ebc74d43b8cb89cd4f9c2933d453784491f9deb388b6a0ca3833d2ca3528a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
