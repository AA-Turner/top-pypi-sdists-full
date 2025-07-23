r'''
# `google_bigquery_analytics_hub_listing`

Refer to the Terraform Registry for docs: [`google_bigquery_analytics_hub_listing`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing).
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


class BigqueryAnalyticsHubListing(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListing",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        bigquery_dataset: typing.Optional[typing.Union["BigqueryAnalyticsHubListingBigqueryDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["BigqueryAnalyticsHubListingDataProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["BigqueryAnalyticsHubListingPublisher", typing.Dict[builtins.str, typing.Any]]] = None,
        pubsub_topic: typing.Optional[typing.Union["BigqueryAnalyticsHubListingPubsubTopic", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        restricted_export_config: typing.Optional[typing.Union["BigqueryAnalyticsHubListingRestrictedExportConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryAnalyticsHubListingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_exchange_id BigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#display_name BigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#listing_id BigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#location BigqueryAnalyticsHubListing#location}
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#bigquery_dataset BigqueryAnalyticsHubListing#bigquery_dataset}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#categories BigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_provider BigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#description BigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#documentation BigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#icon BigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#id BigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_linked_dataset_query_user_email: If true, subscriber email logging is enabled and all queries on the linked dataset will log the email address of the querying user. Once enabled, this setting cannot be turned off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#log_linked_dataset_query_user_email BigqueryAnalyticsHubListing#log_linked_dataset_query_user_email}
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#project BigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#publisher BigqueryAnalyticsHubListing#publisher}
        :param pubsub_topic: pubsub_topic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#pubsub_topic BigqueryAnalyticsHubListing#pubsub_topic}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#request_access BigqueryAnalyticsHubListing#request_access}
        :param restricted_export_config: restricted_export_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#restricted_export_config BigqueryAnalyticsHubListing#restricted_export_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#timeouts BigqueryAnalyticsHubListing#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d505263e565ae87a235e5746b84245a6aa58cdaaf3167594a151569437cbdd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryAnalyticsHubListingConfig(
            data_exchange_id=data_exchange_id,
            display_name=display_name,
            listing_id=listing_id,
            location=location,
            bigquery_dataset=bigquery_dataset,
            categories=categories,
            data_provider=data_provider,
            description=description,
            documentation=documentation,
            icon=icon,
            id=id,
            log_linked_dataset_query_user_email=log_linked_dataset_query_user_email,
            primary_contact=primary_contact,
            project=project,
            publisher=publisher,
            pubsub_topic=pubsub_topic,
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
        '''Generates CDKTF code for importing a BigqueryAnalyticsHubListing resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryAnalyticsHubListing to import.
        :param import_from_id: The id of the existing BigqueryAnalyticsHubListing that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryAnalyticsHubListing to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f3ab8faf00477e3989a1b6fcfa321c6c53019d11f74a17bc180c2d073ab42b)
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
        selected_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#dataset BigqueryAnalyticsHubListing#dataset}
        :param selected_resources: selected_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#selected_resources BigqueryAnalyticsHubListing#selected_resources}
        '''
        value = BigqueryAnalyticsHubListingBigqueryDataset(
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
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        value = BigqueryAnalyticsHubListingDataProvider(
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
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        value = BigqueryAnalyticsHubListingPublisher(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putPublisher", [value]))

    @jsii.member(jsii_name="putPubsubTopic")
    def put_pubsub_topic(
        self,
        *,
        topic: builtins.str,
        data_affinity_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param topic: Resource name of the Pub/Sub topic source for this listing. e.g. projects/myproject/topics/topicId. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#topic BigqueryAnalyticsHubListing#topic}
        :param data_affinity_regions: Region hint on where the data might be published. Data affinity regions are modifiable. See https://cloud.google.com/about/locations for full listing of possible Cloud regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_affinity_regions BigqueryAnalyticsHubListing#data_affinity_regions}
        '''
        value = BigqueryAnalyticsHubListingPubsubTopic(
            topic=topic, data_affinity_regions=data_affinity_regions
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubTopic", [value]))

    @jsii.member(jsii_name="putRestrictedExportConfig")
    def put_restricted_export_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_query_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: If true, enable restricted export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#enabled BigqueryAnalyticsHubListing#enabled}
        :param restrict_query_result: If true, restrict export of query result derived from restricted linked dataset table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#restrict_query_result BigqueryAnalyticsHubListing#restrict_query_result}
        '''
        value = BigqueryAnalyticsHubListingRestrictedExportConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#create BigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#delete BigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#update BigqueryAnalyticsHubListing#update}.
        '''
        value = BigqueryAnalyticsHubListingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBigqueryDataset")
    def reset_bigquery_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryDataset", []))

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

    @jsii.member(jsii_name="resetLogLinkedDatasetQueryUserEmail")
    def reset_log_linked_dataset_query_user_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLinkedDatasetQueryUserEmail", []))

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetPubsubTopic")
    def reset_pubsub_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubTopic", []))

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
    ) -> "BigqueryAnalyticsHubListingBigqueryDatasetOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingBigqueryDatasetOutputReference", jsii.get(self, "bigqueryDataset"))

    @builtins.property
    @jsii.member(jsii_name="dataProvider")
    def data_provider(self) -> "BigqueryAnalyticsHubListingDataProviderOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingDataProviderOutputReference", jsii.get(self, "dataProvider"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> "BigqueryAnalyticsHubListingPublisherOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingPublisherOutputReference", jsii.get(self, "publisher"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> "BigqueryAnalyticsHubListingPubsubTopicOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingPubsubTopicOutputReference", jsii.get(self, "pubsubTopic"))

    @builtins.property
    @jsii.member(jsii_name="restrictedExportConfig")
    def restricted_export_config(
        self,
    ) -> "BigqueryAnalyticsHubListingRestrictedExportConfigOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingRestrictedExportConfigOutputReference", jsii.get(self, "restrictedExportConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryAnalyticsHubListingTimeoutsOutputReference":
        return typing.cast("BigqueryAnalyticsHubListingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDatasetInput")
    def bigquery_dataset_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingBigqueryDataset"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingBigqueryDataset"], jsii.get(self, "bigqueryDatasetInput"))

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
    ) -> typing.Optional["BigqueryAnalyticsHubListingDataProvider"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingDataProvider"], jsii.get(self, "dataProviderInput"))

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
    @jsii.member(jsii_name="logLinkedDatasetQueryUserEmailInput")
    def log_linked_dataset_query_user_email_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logLinkedDatasetQueryUserEmailInput"))

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
    ) -> typing.Optional["BigqueryAnalyticsHubListingPublisher"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingPublisher"], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingPubsubTopic"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingPubsubTopic"], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessInput")
    def request_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedExportConfigInput")
    def restricted_export_config_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingRestrictedExportConfig"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingRestrictedExportConfig"], jsii.get(self, "restrictedExportConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryAnalyticsHubListingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryAnalyticsHubListingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e13729b1fe33a1103014155577db943cd7077452ccee34ad12ff7f8aa539dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataExchangeId")
    def data_exchange_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataExchangeId"))

    @data_exchange_id.setter
    def data_exchange_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5966941064b6688cebd225dab799d3147f29d68fcf74598505eccf11338ec81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExchangeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229bd9e3965b65c8326caa0307a2b2dc527db1077dd1962449221d0a3383434f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1caf99206298147f08d878bf956c7c151498936f0a43b7c1072b4252d07e6d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentation"))

    @documentation.setter
    def documentation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771ebe67fbf25fa0b15a4eda36ac30cd15e68a0ed7d4aff4b0cdc9b54f1a9ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="icon")
    def icon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icon"))

    @icon.setter
    def icon(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fcccb3edaf2c368cbd0ef3e7153a776d072798577d0dd60970e3d989d44959a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icon", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f487389f9fc68224fdc653db4b148d6f1de6f6c9a7da8008b51c9e711f606384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listingId")
    def listing_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listingId"))

    @listing_id.setter
    def listing_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0df29d60b767eec0d9cb041547e6cbbe70a160cc45ad568475eaa10bfd79f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listingId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468ef073a6d95dc0ac33c31691432c4544f32a6d69cf6e98d6c6502e3e1caff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLinkedDatasetQueryUserEmail")
    def log_linked_dataset_query_user_email(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logLinkedDatasetQueryUserEmail"))

    @log_linked_dataset_query_user_email.setter
    def log_linked_dataset_query_user_email(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6fd47346b5d1aee985d940163220ecf39a292db324ea6a59f253f9d1297b54c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLinkedDatasetQueryUserEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c80fef065b198266853236179401ec9beda5da479633fc412e2a808b34ea61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2cb85aa29dfdfbb1328e0266438d3faa5c03a4b0d5aa5909d7ca74432631cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestAccess")
    def request_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestAccess"))

    @request_access.setter
    def request_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da58a59fc41b931af5714891bb62fdb4f4e0119e15b4e58cec937bc72c1ecc77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestAccess", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset", "selected_resources": "selectedResources"},
)
class BigqueryAnalyticsHubListingBigqueryDataset:
    def __init__(
        self,
        *,
        dataset: builtins.str,
        selected_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#dataset BigqueryAnalyticsHubListing#dataset}
        :param selected_resources: selected_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#selected_resources BigqueryAnalyticsHubListing#selected_resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196ab1dceb2f13f773cbc5ca03a3a10de415e193f9e22aaac3cf4f33c3ac5ad0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#dataset BigqueryAnalyticsHubListing#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selected_resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]]:
        '''selected_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#selected_resources BigqueryAnalyticsHubListing#selected_resources}
        '''
        result = self._values.get("selected_resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingBigqueryDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingBigqueryDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df05494ac707cc137894a81781410b9a9edabf9c469bbe098296f936decce907)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectedResources")
    def put_selected_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fa6a1367ef87520061e6a03b60c0050ad9d20caec50d523e9c4197bdfaa668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectedResources", [value]))

    @jsii.member(jsii_name="resetSelectedResources")
    def reset_selected_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedResources", []))

    @builtins.property
    @jsii.member(jsii_name="selectedResources")
    def selected_resources(
        self,
    ) -> "BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList":
        return typing.cast("BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList", jsii.get(self, "selectedResources"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedResourcesInput")
    def selected_resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources"]]], jsii.get(self, "selectedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f9e1a79e5514de52fa687c44ece7ba231d99ab1cf432c3b8a981ea5e805d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0c78ea848bc2e21fdd8e80aa19679e13aacb4850fa0d5ada9d96de13a4be57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources",
    jsii_struct_bases=[],
    name_mapping={"table": "table"},
)
class BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources:
    def __init__(self, *, table: typing.Optional[builtins.str] = None) -> None:
        '''
        :param table: Format: For table: projects/{projectId}/datasets/{datasetId}/tables/{tableId} Example:"projects/test_project/datasets/test_dataset/tables/test_table". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#table BigqueryAnalyticsHubListing#table}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fbc215c2f61d52df9636fc8b4c5d3f8fd1095c6cbfcf5057652e24716d7910)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if table is not None:
            self._values["table"] = table

    @builtins.property
    def table(self) -> typing.Optional[builtins.str]:
        '''Format: For table: projects/{projectId}/datasets/{datasetId}/tables/{tableId} Example:"projects/test_project/datasets/test_dataset/tables/test_table".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#table BigqueryAnalyticsHubListing#table}
        '''
        result = self._values.get("table")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b48224500eccb2568125f5a365ab18a0029d59540b0aab9e428cbc628c19ca5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f71073b0357fa452468e8bad14ed87c3c06c4d671d9da4a4a385747e330c94f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01434a1423711d31f6dca860800bfdb88c5160d28ff32455854a8c602779ad54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5104c2265791ef5bd040f65c1b2e9daffbee9dd6426a1da67e24e6d2e7425d5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9047ebadd672d25ed1b147a5daf9cb3e77c473dfd5179f669f601490e9c972e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ef7387256e70c8e6cdfa6dc2baf2da3dbcdab543ca8f68b16ec1e986ebe3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4ee89da930d97265446457680c55cc32dd74576eb4bba13def2a24bd9c69be3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82cd631cd82172d5522aae4e2ee2a493c4784f119692d47d42228bf2ec54bc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3bcb074562fc67b9549e0286c43db4621ae172d5491760396706adf7ab9795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_exchange_id": "dataExchangeId",
        "display_name": "displayName",
        "listing_id": "listingId",
        "location": "location",
        "bigquery_dataset": "bigqueryDataset",
        "categories": "categories",
        "data_provider": "dataProvider",
        "description": "description",
        "documentation": "documentation",
        "icon": "icon",
        "id": "id",
        "log_linked_dataset_query_user_email": "logLinkedDatasetQueryUserEmail",
        "primary_contact": "primaryContact",
        "project": "project",
        "publisher": "publisher",
        "pubsub_topic": "pubsubTopic",
        "request_access": "requestAccess",
        "restricted_export_config": "restrictedExportConfig",
        "timeouts": "timeouts",
    },
)
class BigqueryAnalyticsHubListingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        bigquery_dataset: typing.Optional[typing.Union[BigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]]] = None,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["BigqueryAnalyticsHubListingDataProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["BigqueryAnalyticsHubListingPublisher", typing.Dict[builtins.str, typing.Any]]] = None,
        pubsub_topic: typing.Optional[typing.Union["BigqueryAnalyticsHubListingPubsubTopic", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        restricted_export_config: typing.Optional[typing.Union["BigqueryAnalyticsHubListingRestrictedExportConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryAnalyticsHubListingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_exchange_id BigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#display_name BigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#listing_id BigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#location BigqueryAnalyticsHubListing#location}
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#bigquery_dataset BigqueryAnalyticsHubListing#bigquery_dataset}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#categories BigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_provider BigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#description BigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#documentation BigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#icon BigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#id BigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_linked_dataset_query_user_email: If true, subscriber email logging is enabled and all queries on the linked dataset will log the email address of the querying user. Once enabled, this setting cannot be turned off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#log_linked_dataset_query_user_email BigqueryAnalyticsHubListing#log_linked_dataset_query_user_email}
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#project BigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#publisher BigqueryAnalyticsHubListing#publisher}
        :param pubsub_topic: pubsub_topic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#pubsub_topic BigqueryAnalyticsHubListing#pubsub_topic}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#request_access BigqueryAnalyticsHubListing#request_access}
        :param restricted_export_config: restricted_export_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#restricted_export_config BigqueryAnalyticsHubListing#restricted_export_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#timeouts BigqueryAnalyticsHubListing#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_dataset, dict):
            bigquery_dataset = BigqueryAnalyticsHubListingBigqueryDataset(**bigquery_dataset)
        if isinstance(data_provider, dict):
            data_provider = BigqueryAnalyticsHubListingDataProvider(**data_provider)
        if isinstance(publisher, dict):
            publisher = BigqueryAnalyticsHubListingPublisher(**publisher)
        if isinstance(pubsub_topic, dict):
            pubsub_topic = BigqueryAnalyticsHubListingPubsubTopic(**pubsub_topic)
        if isinstance(restricted_export_config, dict):
            restricted_export_config = BigqueryAnalyticsHubListingRestrictedExportConfig(**restricted_export_config)
        if isinstance(timeouts, dict):
            timeouts = BigqueryAnalyticsHubListingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20118a18a5faabaed81067e337785772e52a3f731755be5ccf7c990c1d01b07)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_exchange_id", value=data_exchange_id, expected_type=type_hints["data_exchange_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument listing_id", value=listing_id, expected_type=type_hints["listing_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument bigquery_dataset", value=bigquery_dataset, expected_type=type_hints["bigquery_dataset"])
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument data_provider", value=data_provider, expected_type=type_hints["data_provider"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument icon", value=icon, expected_type=type_hints["icon"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_linked_dataset_query_user_email", value=log_linked_dataset_query_user_email, expected_type=type_hints["log_linked_dataset_query_user_email"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument request_access", value=request_access, expected_type=type_hints["request_access"])
            check_type(argname="argument restricted_export_config", value=restricted_export_config, expected_type=type_hints["restricted_export_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if bigquery_dataset is not None:
            self._values["bigquery_dataset"] = bigquery_dataset
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
        if log_linked_dataset_query_user_email is not None:
            self._values["log_linked_dataset_query_user_email"] = log_linked_dataset_query_user_email
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact
        if project is not None:
            self._values["project"] = project
        if publisher is not None:
            self._values["publisher"] = publisher
        if pubsub_topic is not None:
            self._values["pubsub_topic"] = pubsub_topic
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
    def data_exchange_id(self) -> builtins.str:
        '''The ID of the data exchange.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_exchange_id BigqueryAnalyticsHubListing#data_exchange_id}
        '''
        result = self._values.get("data_exchange_id")
        assert result is not None, "Required property 'data_exchange_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Human-readable display name of the listing.

        The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#display_name BigqueryAnalyticsHubListing#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listing_id(self) -> builtins.str:
        '''The ID of the listing.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#listing_id BigqueryAnalyticsHubListing#listing_id}
        '''
        result = self._values.get("listing_id")
        assert result is not None, "Required property 'listing_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this data exchange listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#location BigqueryAnalyticsHubListing#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigquery_dataset(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset]:
        '''bigquery_dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#bigquery_dataset BigqueryAnalyticsHubListing#bigquery_dataset}
        '''
        result = self._values.get("bigquery_dataset")
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset], result)

    @builtins.property
    def categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Categories of the listing. Up to two categories are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#categories BigqueryAnalyticsHubListing#categories}
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_provider(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingDataProvider"]:
        '''data_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_provider BigqueryAnalyticsHubListing#data_provider}
        '''
        result = self._values.get("data_provider")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingDataProvider"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Short description of the listing.

        The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#description BigqueryAnalyticsHubListing#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional[builtins.str]:
        '''Documentation describing the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#documentation BigqueryAnalyticsHubListing#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded image representing the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#icon BigqueryAnalyticsHubListing#icon}
        '''
        result = self._values.get("icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#id BigqueryAnalyticsHubListing#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_linked_dataset_query_user_email(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, subscriber email logging is enabled and all queries on the linked dataset will log the email address of the querying user.

        Once enabled, this setting cannot be turned off.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#log_linked_dataset_query_user_email BigqueryAnalyticsHubListing#log_linked_dataset_query_user_email}
        '''
        result = self._values.get("log_linked_dataset_query_user_email")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the primary point of contact of the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#project BigqueryAnalyticsHubListing#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional["BigqueryAnalyticsHubListingPublisher"]:
        '''publisher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#publisher BigqueryAnalyticsHubListing#publisher}
        '''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingPublisher"], result)

    @builtins.property
    def pubsub_topic(self) -> typing.Optional["BigqueryAnalyticsHubListingPubsubTopic"]:
        '''pubsub_topic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#pubsub_topic BigqueryAnalyticsHubListing#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingPubsubTopic"], result)

    @builtins.property
    def request_access(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the request access of the listing. Subscribers can use this reference to request access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#request_access BigqueryAnalyticsHubListing#request_access}
        '''
        result = self._values.get("request_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restricted_export_config(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubListingRestrictedExportConfig"]:
        '''restricted_export_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#restricted_export_config BigqueryAnalyticsHubListing#restricted_export_config}
        '''
        result = self._values.get("restricted_export_config")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingRestrictedExportConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryAnalyticsHubListingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#timeouts BigqueryAnalyticsHubListing#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubListingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingDataProvider",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class BigqueryAnalyticsHubListingDataProvider:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9477abaa2020cebbd71c7498b48e8ef2ab1321a07ce4d5b37e911cc8bf089175)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the data provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingDataProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingDataProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingDataProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3a760e9e504eb60e851dc7875d47145013ab62d45bf4b300df04e227d5c7c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc870329b34291a5cd024c3d81bc3a42e1186299abb6ecd92f309af9ec280eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ea6f3bb7db73886e4f2b4c05cea514ded44522ba2b8a1d5bc6dde5be9e58eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubListingDataProvider]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingDataProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingDataProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a81e06a8d79b404d9c5bafa21b9a25fc4e64c5d9a0d04f0edae4603485fcb4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingPublisher",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class BigqueryAnalyticsHubListingPublisher:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c10fa2c9ae8ea3a96c2f89bc63e148fc8801f0f27161bf5eb98b0f3533da74)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#name BigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the listing publisher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#primary_contact BigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingPublisher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingPublisherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingPublisherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1471827598b2f4a5ac33f0f93b040f01e0053c78b78a19f960f1a5261375209d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__617377a16650c7a77da4a3128217d78bfeeba32e2ad79f18fd58bd92147fc28c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b735594f5c9683fdd36cee17f3386b6c44ddf231623bc8545dafbb316466b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryAnalyticsHubListingPublisher]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingPublisher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingPublisher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d91a7479e780d3d9c0fb641973d037c718e1265a0f4a7cff80f1c329a68ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingPubsubTopic",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "data_affinity_regions": "dataAffinityRegions"},
)
class BigqueryAnalyticsHubListingPubsubTopic:
    def __init__(
        self,
        *,
        topic: builtins.str,
        data_affinity_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param topic: Resource name of the Pub/Sub topic source for this listing. e.g. projects/myproject/topics/topicId. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#topic BigqueryAnalyticsHubListing#topic}
        :param data_affinity_regions: Region hint on where the data might be published. Data affinity regions are modifiable. See https://cloud.google.com/about/locations for full listing of possible Cloud regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_affinity_regions BigqueryAnalyticsHubListing#data_affinity_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309db13b9c142dfd44628bdb63ec7e36909e852ad3c0e1a8e3199ac75cdd4b82)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument data_affinity_regions", value=data_affinity_regions, expected_type=type_hints["data_affinity_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if data_affinity_regions is not None:
            self._values["data_affinity_regions"] = data_affinity_regions

    @builtins.property
    def topic(self) -> builtins.str:
        '''Resource name of the Pub/Sub topic source for this listing. e.g. projects/myproject/topics/topicId.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#topic BigqueryAnalyticsHubListing#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_affinity_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region hint on where the data might be published.

        Data affinity regions are modifiable.
        See https://cloud.google.com/about/locations for full listing of possible Cloud regions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#data_affinity_regions BigqueryAnalyticsHubListing#data_affinity_regions}
        '''
        result = self._values.get("data_affinity_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingPubsubTopic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingPubsubTopicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingPubsubTopicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4255f45ac6a556c38e8d42ed02bf83d6286de43333cbfe0fdf1e3ee87623a4d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataAffinityRegions")
    def reset_data_affinity_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataAffinityRegions", []))

    @builtins.property
    @jsii.member(jsii_name="dataAffinityRegionsInput")
    def data_affinity_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dataAffinityRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAffinityRegions")
    def data_affinity_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataAffinityRegions"))

    @data_affinity_regions.setter
    def data_affinity_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bd9d11e57b7b73b872707e46e3f5a4d62648bf40e0373ee5b0a896753bac7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAffinityRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17979f1ba413c2690ca020eeb024906b6f6305a7fa34e2442ca11edd20c7d2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryAnalyticsHubListingPubsubTopic]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingPubsubTopic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingPubsubTopic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0223129518062400a0660f5facd009f553da4f31a96321756b0c195c1ed1ac95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingRestrictedExportConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "restrict_query_result": "restrictQueryResult",
    },
)
class BigqueryAnalyticsHubListingRestrictedExportConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_query_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: If true, enable restricted export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#enabled BigqueryAnalyticsHubListing#enabled}
        :param restrict_query_result: If true, restrict export of query result derived from restricted linked dataset table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#restrict_query_result BigqueryAnalyticsHubListing#restrict_query_result}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5495be373c89b313bcb962fcdbe9bdbc66f4b3e7faa8bbac1b9d1dbdfae1903c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#enabled BigqueryAnalyticsHubListing#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrict_query_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, restrict export of query result derived from restricted linked dataset table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#restrict_query_result BigqueryAnalyticsHubListing#restrict_query_result}
        '''
        result = self._values.get("restrict_query_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingRestrictedExportConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingRestrictedExportConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingRestrictedExportConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6b4d447ba5998d1a309fce3dd09d42a7b895bcdf3f0778b9541af6c107efcaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd6a6098a34d5d036443cc13d4e7008f6c8b7a9a9b8e9a9c0c69fb141204735d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37069953ab053938dbd9cc2bd744a75e231efe92fb140bd5193b79025a87de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictQueryResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubListingRestrictedExportConfig]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubListingRestrictedExportConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubListingRestrictedExportConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ee1625ad3feaad2040ac25e756ee12bf8faabd849f9b274df94ae843f9318e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryAnalyticsHubListingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#create BigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#delete BigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#update BigqueryAnalyticsHubListing#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8522b90a34ded34fe39ca074307cc4c98a764bfc9eaafa0cc3be6ccf6366b730)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#create BigqueryAnalyticsHubListing#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#delete BigqueryAnalyticsHubListing#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_listing#update BigqueryAnalyticsHubListing#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubListingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubListingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubListing.BigqueryAnalyticsHubListingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec07cbc9f72023382039a8e3b3dc924bc4f9984e08d09f200b2da2b012c5ecba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfbfa607b47d964f458866c96dea3800cbb8ed5a2952410767dc4a8713389531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f46ba78b2cc7d4dd27f8480580a7c6230b6bc4d14d6a8f0d894a35275084d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe78bfc898e2cb9ae8a6519312d40bde485226d92a112073fa9836ffb3e9bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02970ef3c8194b2b5c3dc5275006d640c5f3abd2ed9009bc30f9cce13b4e7280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryAnalyticsHubListing",
    "BigqueryAnalyticsHubListingBigqueryDataset",
    "BigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
    "BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources",
    "BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesList",
    "BigqueryAnalyticsHubListingBigqueryDatasetSelectedResourcesOutputReference",
    "BigqueryAnalyticsHubListingConfig",
    "BigqueryAnalyticsHubListingDataProvider",
    "BigqueryAnalyticsHubListingDataProviderOutputReference",
    "BigqueryAnalyticsHubListingPublisher",
    "BigqueryAnalyticsHubListingPublisherOutputReference",
    "BigqueryAnalyticsHubListingPubsubTopic",
    "BigqueryAnalyticsHubListingPubsubTopicOutputReference",
    "BigqueryAnalyticsHubListingRestrictedExportConfig",
    "BigqueryAnalyticsHubListingRestrictedExportConfigOutputReference",
    "BigqueryAnalyticsHubListingTimeouts",
    "BigqueryAnalyticsHubListingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__14d505263e565ae87a235e5746b84245a6aa58cdaaf3167594a151569437cbdd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    listing_id: builtins.str,
    location: builtins.str,
    bigquery_dataset: typing.Optional[typing.Union[BigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_provider: typing.Optional[typing.Union[BigqueryAnalyticsHubListingDataProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[typing.Union[BigqueryAnalyticsHubListingPublisher, typing.Dict[builtins.str, typing.Any]]] = None,
    pubsub_topic: typing.Optional[typing.Union[BigqueryAnalyticsHubListingPubsubTopic, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access: typing.Optional[builtins.str] = None,
    restricted_export_config: typing.Optional[typing.Union[BigqueryAnalyticsHubListingRestrictedExportConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__31f3ab8faf00477e3989a1b6fcfa321c6c53019d11f74a17bc180c2d073ab42b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e13729b1fe33a1103014155577db943cd7077452ccee34ad12ff7f8aa539dd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5966941064b6688cebd225dab799d3147f29d68fcf74598505eccf11338ec81a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229bd9e3965b65c8326caa0307a2b2dc527db1077dd1962449221d0a3383434f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1caf99206298147f08d878bf956c7c151498936f0a43b7c1072b4252d07e6d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771ebe67fbf25fa0b15a4eda36ac30cd15e68a0ed7d4aff4b0cdc9b54f1a9ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcccb3edaf2c368cbd0ef3e7153a776d072798577d0dd60970e3d989d44959a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f487389f9fc68224fdc653db4b148d6f1de6f6c9a7da8008b51c9e711f606384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0df29d60b767eec0d9cb041547e6cbbe70a160cc45ad568475eaa10bfd79f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468ef073a6d95dc0ac33c31691432c4544f32a6d69cf6e98d6c6502e3e1caff7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fd47346b5d1aee985d940163220ecf39a292db324ea6a59f253f9d1297b54c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c80fef065b198266853236179401ec9beda5da479633fc412e2a808b34ea61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2cb85aa29dfdfbb1328e0266438d3faa5c03a4b0d5aa5909d7ca74432631cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da58a59fc41b931af5714891bb62fdb4f4e0119e15b4e58cec937bc72c1ecc77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196ab1dceb2f13f773cbc5ca03a3a10de415e193f9e22aaac3cf4f33c3ac5ad0(
    *,
    dataset: builtins.str,
    selected_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df05494ac707cc137894a81781410b9a9edabf9c469bbe098296f936decce907(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fa6a1367ef87520061e6a03b60c0050ad9d20caec50d523e9c4197bdfaa668(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f9e1a79e5514de52fa687c44ece7ba231d99ab1cf432c3b8a981ea5e805d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0c78ea848bc2e21fdd8e80aa19679e13aacb4850fa0d5ada9d96de13a4be57(
    value: typing.Optional[BigqueryAnalyticsHubListingBigqueryDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fbc215c2f61d52df9636fc8b4c5d3f8fd1095c6cbfcf5057652e24716d7910(
    *,
    table: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b48224500eccb2568125f5a365ab18a0029d59540b0aab9e428cbc628c19ca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f71073b0357fa452468e8bad14ed87c3c06c4d671d9da4a4a385747e330c94f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01434a1423711d31f6dca860800bfdb88c5160d28ff32455854a8c602779ad54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5104c2265791ef5bd040f65c1b2e9daffbee9dd6426a1da67e24e6d2e7425d5a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9047ebadd672d25ed1b147a5daf9cb3e77c473dfd5179f669f601490e9c972e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ef7387256e70c8e6cdfa6dc2baf2da3dbcdab543ca8f68b16ec1e986ebe3aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ee89da930d97265446457680c55cc32dd74576eb4bba13def2a24bd9c69be3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cd631cd82172d5522aae4e2ee2a493c4784f119692d47d42228bf2ec54bc1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3bcb074562fc67b9549e0286c43db4621ae172d5491760396706adf7ab9795(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingBigqueryDatasetSelectedResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20118a18a5faabaed81067e337785772e52a3f731755be5ccf7c990c1d01b07(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    listing_id: builtins.str,
    location: builtins.str,
    bigquery_dataset: typing.Optional[typing.Union[BigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_provider: typing.Optional[typing.Union[BigqueryAnalyticsHubListingDataProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[typing.Union[BigqueryAnalyticsHubListingPublisher, typing.Dict[builtins.str, typing.Any]]] = None,
    pubsub_topic: typing.Optional[typing.Union[BigqueryAnalyticsHubListingPubsubTopic, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access: typing.Optional[builtins.str] = None,
    restricted_export_config: typing.Optional[typing.Union[BigqueryAnalyticsHubListingRestrictedExportConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryAnalyticsHubListingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9477abaa2020cebbd71c7498b48e8ef2ab1321a07ce4d5b37e911cc8bf089175(
    *,
    name: builtins.str,
    primary_contact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3a760e9e504eb60e851dc7875d47145013ab62d45bf4b300df04e227d5c7c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc870329b34291a5cd024c3d81bc3a42e1186299abb6ecd92f309af9ec280eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ea6f3bb7db73886e4f2b4c05cea514ded44522ba2b8a1d5bc6dde5be9e58eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a81e06a8d79b404d9c5bafa21b9a25fc4e64c5d9a0d04f0edae4603485fcb4c(
    value: typing.Optional[BigqueryAnalyticsHubListingDataProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c10fa2c9ae8ea3a96c2f89bc63e148fc8801f0f27161bf5eb98b0f3533da74(
    *,
    name: builtins.str,
    primary_contact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1471827598b2f4a5ac33f0f93b040f01e0053c78b78a19f960f1a5261375209d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617377a16650c7a77da4a3128217d78bfeeba32e2ad79f18fd58bd92147fc28c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b735594f5c9683fdd36cee17f3386b6c44ddf231623bc8545dafbb316466b1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d91a7479e780d3d9c0fb641973d037c718e1265a0f4a7cff80f1c329a68ff8(
    value: typing.Optional[BigqueryAnalyticsHubListingPublisher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309db13b9c142dfd44628bdb63ec7e36909e852ad3c0e1a8e3199ac75cdd4b82(
    *,
    topic: builtins.str,
    data_affinity_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4255f45ac6a556c38e8d42ed02bf83d6286de43333cbfe0fdf1e3ee87623a4d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bd9d11e57b7b73b872707e46e3f5a4d62648bf40e0373ee5b0a896753bac7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17979f1ba413c2690ca020eeb024906b6f6305a7fa34e2442ca11edd20c7d2c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0223129518062400a0660f5facd009f553da4f31a96321756b0c195c1ed1ac95(
    value: typing.Optional[BigqueryAnalyticsHubListingPubsubTopic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5495be373c89b313bcb962fcdbe9bdbc66f4b3e7faa8bbac1b9d1dbdfae1903c(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_query_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b4d447ba5998d1a309fce3dd09d42a7b895bcdf3f0778b9541af6c107efcaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6a6098a34d5d036443cc13d4e7008f6c8b7a9a9b8e9a9c0c69fb141204735d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37069953ab053938dbd9cc2bd744a75e231efe92fb140bd5193b79025a87de2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ee1625ad3feaad2040ac25e756ee12bf8faabd849f9b274df94ae843f9318e(
    value: typing.Optional[BigqueryAnalyticsHubListingRestrictedExportConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8522b90a34ded34fe39ca074307cc4c98a764bfc9eaafa0cc3be6ccf6366b730(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec07cbc9f72023382039a8e3b3dc924bc4f9984e08d09f200b2da2b012c5ecba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbfa607b47d964f458866c96dea3800cbb8ed5a2952410767dc4a8713389531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f46ba78b2cc7d4dd27f8480580a7c6230b6bc4d14d6a8f0d894a35275084d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe78bfc898e2cb9ae8a6519312d40bde485226d92a112073fa9836ffb3e9bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02970ef3c8194b2b5c3dc5275006d640c5f3abd2ed9009bc30f9cce13b4e7280(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubListingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
