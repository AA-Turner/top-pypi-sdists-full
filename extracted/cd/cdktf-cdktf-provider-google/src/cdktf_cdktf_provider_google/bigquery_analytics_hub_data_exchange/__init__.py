r'''
# `google_bigquery_analytics_hub_data_exchange`

Refer to the Terraform Registry for docs: [`google_bigquery_analytics_hub_data_exchange`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange).
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


class BigqueryAnalyticsHubDataExchange(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchange",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange google_bigquery_analytics_hub_data_exchange}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sharing_environment_config: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange google_bigquery_analytics_hub_data_exchange} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#data_exchange_id BigqueryAnalyticsHubDataExchange#data_exchange_id}
        :param display_name: Human-readable display name of the data exchange. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), and must not start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#display_name BigqueryAnalyticsHubDataExchange#display_name}
        :param location: The name of the location this data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#location BigqueryAnalyticsHubDataExchange#location}
        :param description: Description of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#description BigqueryAnalyticsHubDataExchange#description}
        :param documentation: Documentation describing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#documentation BigqueryAnalyticsHubDataExchange#documentation}
        :param icon: Base64 encoded image representing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#icon BigqueryAnalyticsHubDataExchange#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#id BigqueryAnalyticsHubDataExchange#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_linked_dataset_query_user_email: If true, subscriber email logging is enabled and all queries on the linked dataset will log the email address of the querying user. Once enabled, this setting cannot be turned off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#log_linked_dataset_query_user_email BigqueryAnalyticsHubDataExchange#log_linked_dataset_query_user_email}
        :param primary_contact: Email or URL of the primary point of contact of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#primary_contact BigqueryAnalyticsHubDataExchange#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#project BigqueryAnalyticsHubDataExchange#project}.
        :param sharing_environment_config: sharing_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#sharing_environment_config BigqueryAnalyticsHubDataExchange#sharing_environment_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#timeouts BigqueryAnalyticsHubDataExchange#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c256656e21007196549919e7ffee97758cf5dc1e5a0cc96609b0c09fcbb374)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryAnalyticsHubDataExchangeConfig(
            data_exchange_id=data_exchange_id,
            display_name=display_name,
            location=location,
            description=description,
            documentation=documentation,
            icon=icon,
            id=id,
            log_linked_dataset_query_user_email=log_linked_dataset_query_user_email,
            primary_contact=primary_contact,
            project=project,
            sharing_environment_config=sharing_environment_config,
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
        '''Generates CDKTF code for importing a BigqueryAnalyticsHubDataExchange resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryAnalyticsHubDataExchange to import.
        :param import_from_id: The id of the existing BigqueryAnalyticsHubDataExchange that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryAnalyticsHubDataExchange to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61239ef1a8dbdf99baf768b7552d937615581b929c4b945998625df101ecb76c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSharingEnvironmentConfig")
    def put_sharing_environment_config(
        self,
        *,
        dcr_exchange_config: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_exchange_config: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dcr_exchange_config: dcr_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#dcr_exchange_config BigqueryAnalyticsHubDataExchange#dcr_exchange_config}
        :param default_exchange_config: default_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#default_exchange_config BigqueryAnalyticsHubDataExchange#default_exchange_config}
        '''
        value = BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig(
            dcr_exchange_config=dcr_exchange_config,
            default_exchange_config=default_exchange_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSharingEnvironmentConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#create BigqueryAnalyticsHubDataExchange#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#delete BigqueryAnalyticsHubDataExchange#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#update BigqueryAnalyticsHubDataExchange#update}.
        '''
        value = BigqueryAnalyticsHubDataExchangeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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

    @jsii.member(jsii_name="resetSharingEnvironmentConfig")
    def reset_sharing_environment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharingEnvironmentConfig", []))

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
    @jsii.member(jsii_name="listingCount")
    def listing_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "listingCount"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sharingEnvironmentConfig")
    def sharing_environment_config(
        self,
    ) -> "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference":
        return typing.cast("BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference", jsii.get(self, "sharingEnvironmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryAnalyticsHubDataExchangeTimeoutsOutputReference":
        return typing.cast("BigqueryAnalyticsHubDataExchangeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeIdInput")
    def data_exchange_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataExchangeIdInput"))

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
    @jsii.member(jsii_name="sharingEnvironmentConfigInput")
    def sharing_environment_config_input(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"]:
        return typing.cast(typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"], jsii.get(self, "sharingEnvironmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryAnalyticsHubDataExchangeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryAnalyticsHubDataExchangeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeId")
    def data_exchange_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataExchangeId"))

    @data_exchange_id.setter
    def data_exchange_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9ca14c9ef742882b76f901b2384344908318cbfaae04cb18757a11261cb3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExchangeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f9f633cadff8d669a411525c2d2f0317c63593e2cf712d9f7a1fa7ec7950ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abfd495ab286da2b0b0f1003ef472c439e251031dbbb7c3d4d0a21305797751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentation"))

    @documentation.setter
    def documentation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505a61e5b832c6459801d153836043fc189da115a29c965cc000080d4fe9e810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="icon")
    def icon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icon"))

    @icon.setter
    def icon(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11d1166e8829ca8a3396e721a5c00982a6b02805dc6b4c0afb88fdd5aa2fa81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icon", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d854d30b4540e10cf0afca16146dcafdac83804af03028a7fa3a66c28b7ffb3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adcf8118488bb707d0c72afd8b76e73b1de0ff931b78572106c9500d56ffae00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__846f042fa37a75d251eba1e77207f64330ffffd45febf4e0c05b560669864f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLinkedDatasetQueryUserEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd04d3f501538dbe7c9da5742120bfbc0639ccaf733aeddd28398f399a85629f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a79c7cfe794456b97dcc0610eefee6c4d78f929cef6b680bfb73b4c79127f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeConfig",
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
        "location": "location",
        "description": "description",
        "documentation": "documentation",
        "icon": "icon",
        "id": "id",
        "log_linked_dataset_query_user_email": "logLinkedDatasetQueryUserEmail",
        "primary_contact": "primaryContact",
        "project": "project",
        "sharing_environment_config": "sharingEnvironmentConfig",
        "timeouts": "timeouts",
    },
)
class BigqueryAnalyticsHubDataExchangeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sharing_environment_config: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#data_exchange_id BigqueryAnalyticsHubDataExchange#data_exchange_id}
        :param display_name: Human-readable display name of the data exchange. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), and must not start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#display_name BigqueryAnalyticsHubDataExchange#display_name}
        :param location: The name of the location this data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#location BigqueryAnalyticsHubDataExchange#location}
        :param description: Description of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#description BigqueryAnalyticsHubDataExchange#description}
        :param documentation: Documentation describing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#documentation BigqueryAnalyticsHubDataExchange#documentation}
        :param icon: Base64 encoded image representing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#icon BigqueryAnalyticsHubDataExchange#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#id BigqueryAnalyticsHubDataExchange#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_linked_dataset_query_user_email: If true, subscriber email logging is enabled and all queries on the linked dataset will log the email address of the querying user. Once enabled, this setting cannot be turned off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#log_linked_dataset_query_user_email BigqueryAnalyticsHubDataExchange#log_linked_dataset_query_user_email}
        :param primary_contact: Email or URL of the primary point of contact of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#primary_contact BigqueryAnalyticsHubDataExchange#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#project BigqueryAnalyticsHubDataExchange#project}.
        :param sharing_environment_config: sharing_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#sharing_environment_config BigqueryAnalyticsHubDataExchange#sharing_environment_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#timeouts BigqueryAnalyticsHubDataExchange#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sharing_environment_config, dict):
            sharing_environment_config = BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig(**sharing_environment_config)
        if isinstance(timeouts, dict):
            timeouts = BigqueryAnalyticsHubDataExchangeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f064b665359bf20ab371e7916c39279aefdcf82c89679aa599997f7a0fcea55)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_exchange_id", value=data_exchange_id, expected_type=type_hints["data_exchange_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument icon", value=icon, expected_type=type_hints["icon"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_linked_dataset_query_user_email", value=log_linked_dataset_query_user_email, expected_type=type_hints["log_linked_dataset_query_user_email"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument sharing_environment_config", value=sharing_environment_config, expected_type=type_hints["sharing_environment_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_exchange_id": data_exchange_id,
            "display_name": display_name,
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
        if sharing_environment_config is not None:
            self._values["sharing_environment_config"] = sharing_environment_config
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#data_exchange_id BigqueryAnalyticsHubDataExchange#data_exchange_id}
        '''
        result = self._values.get("data_exchange_id")
        assert result is not None, "Required property 'data_exchange_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Human-readable display name of the data exchange.

        The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), and must not start or end with spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#display_name BigqueryAnalyticsHubDataExchange#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#location BigqueryAnalyticsHubDataExchange#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#description BigqueryAnalyticsHubDataExchange#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional[builtins.str]:
        '''Documentation describing the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#documentation BigqueryAnalyticsHubDataExchange#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded image representing the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#icon BigqueryAnalyticsHubDataExchange#icon}
        '''
        result = self._values.get("icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#id BigqueryAnalyticsHubDataExchange#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#log_linked_dataset_query_user_email BigqueryAnalyticsHubDataExchange#log_linked_dataset_query_user_email}
        '''
        result = self._values.get("log_linked_dataset_query_user_email")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the primary point of contact of the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#primary_contact BigqueryAnalyticsHubDataExchange#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#project BigqueryAnalyticsHubDataExchange#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sharing_environment_config(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"]:
        '''sharing_environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#sharing_environment_config BigqueryAnalyticsHubDataExchange#sharing_environment_config}
        '''
        result = self._values.get("sharing_environment_config")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryAnalyticsHubDataExchangeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#timeouts BigqueryAnalyticsHubDataExchange#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubDataExchangeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubDataExchangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dcr_exchange_config": "dcrExchangeConfig",
        "default_exchange_config": "defaultExchangeConfig",
    },
)
class BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig:
    def __init__(
        self,
        *,
        dcr_exchange_config: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_exchange_config: typing.Optional[typing.Union["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dcr_exchange_config: dcr_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#dcr_exchange_config BigqueryAnalyticsHubDataExchange#dcr_exchange_config}
        :param default_exchange_config: default_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#default_exchange_config BigqueryAnalyticsHubDataExchange#default_exchange_config}
        '''
        if isinstance(dcr_exchange_config, dict):
            dcr_exchange_config = BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig(**dcr_exchange_config)
        if isinstance(default_exchange_config, dict):
            default_exchange_config = BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig(**default_exchange_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2294f1327ce8003118edb8557ab0192fe42be71b1776ba3cb3ce645d3d30d9a5)
            check_type(argname="argument dcr_exchange_config", value=dcr_exchange_config, expected_type=type_hints["dcr_exchange_config"])
            check_type(argname="argument default_exchange_config", value=default_exchange_config, expected_type=type_hints["default_exchange_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dcr_exchange_config is not None:
            self._values["dcr_exchange_config"] = dcr_exchange_config
        if default_exchange_config is not None:
            self._values["default_exchange_config"] = default_exchange_config

    @builtins.property
    def dcr_exchange_config(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig"]:
        '''dcr_exchange_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#dcr_exchange_config BigqueryAnalyticsHubDataExchange#dcr_exchange_config}
        '''
        result = self._values.get("dcr_exchange_config")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig"], result)

    @builtins.property
    def default_exchange_config(
        self,
    ) -> typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig"]:
        '''default_exchange_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#default_exchange_config BigqueryAnalyticsHubDataExchange#default_exchange_config}
        '''
        result = self._values.get("default_exchange_config")
        return typing.cast(typing.Optional["BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fad5d3f3c54c84f85a7e099738bb5123302ce3b592f4ea328a15c758029592f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce31fc0f1ba02bc56b705b497402f9327da8e90e8d8bb872ba5ce4b81b96f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7ddeb30f5c8d1e2b64ccfcc04643c389345898389451a8c9b8f5e01036cd906)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a405827292d6d59f311ed5b6a1edd8f46e455f053bfba2ed64df16eeedc4c8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c93b8d1b96581cfb897af8165dbf60287bc0fc0585ba3f6cb7428a2efb62e3c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDcrExchangeConfig")
    def put_dcr_exchange_config(self) -> None:
        value = BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig()

        return typing.cast(None, jsii.invoke(self, "putDcrExchangeConfig", [value]))

    @jsii.member(jsii_name="putDefaultExchangeConfig")
    def put_default_exchange_config(self) -> None:
        value = BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig()

        return typing.cast(None, jsii.invoke(self, "putDefaultExchangeConfig", [value]))

    @jsii.member(jsii_name="resetDcrExchangeConfig")
    def reset_dcr_exchange_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDcrExchangeConfig", []))

    @jsii.member(jsii_name="resetDefaultExchangeConfig")
    def reset_default_exchange_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultExchangeConfig", []))

    @builtins.property
    @jsii.member(jsii_name="dcrExchangeConfig")
    def dcr_exchange_config(
        self,
    ) -> BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference:
        return typing.cast(BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference, jsii.get(self, "dcrExchangeConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultExchangeConfig")
    def default_exchange_config(
        self,
    ) -> BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference:
        return typing.cast(BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference, jsii.get(self, "defaultExchangeConfig"))

    @builtins.property
    @jsii.member(jsii_name="dcrExchangeConfigInput")
    def dcr_exchange_config_input(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig], jsii.get(self, "dcrExchangeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultExchangeConfigInput")
    def default_exchange_config_input(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig], jsii.get(self, "defaultExchangeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig]:
        return typing.cast(typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bd972ff4909df47a3d2fd10d3fecc41eb165123983e089a3db5a4c863a98ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryAnalyticsHubDataExchangeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#create BigqueryAnalyticsHubDataExchange#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#delete BigqueryAnalyticsHubDataExchange#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#update BigqueryAnalyticsHubDataExchange#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07952a739b7ad2f4ab0a752212ee2483e87fc0cc48df760da3ae411772374b90)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#create BigqueryAnalyticsHubDataExchange#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#delete BigqueryAnalyticsHubDataExchange#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_analytics_hub_data_exchange#update BigqueryAnalyticsHubDataExchange#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryAnalyticsHubDataExchangeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryAnalyticsHubDataExchangeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryAnalyticsHubDataExchange.BigqueryAnalyticsHubDataExchangeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3be965b7818b53749a23a96cb39b5f969edd12ac1eb105402b936981661d609f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f0511c9e5bd390d4bf8c39617304be559810e25c0d9eae535988e4cf5dcec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb38a5b7983539db5581a62fc460c6ab37278c3a5d598135f4026d8e0a12d82f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eeb777b80a0b266ead2d57cc7a4befea6065b15814b83832089cc05d02346c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubDataExchangeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubDataExchangeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubDataExchangeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550c9cd19b6a5144870ba237470b8934e45269c05146781cb896679bb9d6063b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryAnalyticsHubDataExchange",
    "BigqueryAnalyticsHubDataExchangeConfig",
    "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig",
    "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig",
    "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference",
    "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig",
    "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference",
    "BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference",
    "BigqueryAnalyticsHubDataExchangeTimeouts",
    "BigqueryAnalyticsHubDataExchangeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__22c256656e21007196549919e7ffee97758cf5dc1e5a0cc96609b0c09fcbb374(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    sharing_environment_config: typing.Optional[typing.Union[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryAnalyticsHubDataExchangeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__61239ef1a8dbdf99baf768b7552d937615581b929c4b945998625df101ecb76c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9ca14c9ef742882b76f901b2384344908318cbfaae04cb18757a11261cb3d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f9f633cadff8d669a411525c2d2f0317c63593e2cf712d9f7a1fa7ec7950ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abfd495ab286da2b0b0f1003ef472c439e251031dbbb7c3d4d0a21305797751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505a61e5b832c6459801d153836043fc189da115a29c965cc000080d4fe9e810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11d1166e8829ca8a3396e721a5c00982a6b02805dc6b4c0afb88fdd5aa2fa81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d854d30b4540e10cf0afca16146dcafdac83804af03028a7fa3a66c28b7ffb3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adcf8118488bb707d0c72afd8b76e73b1de0ff931b78572106c9500d56ffae00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846f042fa37a75d251eba1e77207f64330ffffd45febf4e0c05b560669864f2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd04d3f501538dbe7c9da5742120bfbc0639ccaf733aeddd28398f399a85629f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a79c7cfe794456b97dcc0610eefee6c4d78f929cef6b680bfb73b4c79127f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f064b665359bf20ab371e7916c39279aefdcf82c89679aa599997f7a0fcea55(
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
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_linked_dataset_query_user_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    sharing_environment_config: typing.Optional[typing.Union[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryAnalyticsHubDataExchangeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2294f1327ce8003118edb8557ab0192fe42be71b1776ba3cb3ce645d3d30d9a5(
    *,
    dcr_exchange_config: typing.Optional[typing.Union[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_exchange_config: typing.Optional[typing.Union[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fad5d3f3c54c84f85a7e099738bb5123302ce3b592f4ea328a15c758029592f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce31fc0f1ba02bc56b705b497402f9327da8e90e8d8bb872ba5ce4b81b96f5a(
    value: typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ddeb30f5c8d1e2b64ccfcc04643c389345898389451a8c9b8f5e01036cd906(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a405827292d6d59f311ed5b6a1edd8f46e455f053bfba2ed64df16eeedc4c8a0(
    value: typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93b8d1b96581cfb897af8165dbf60287bc0fc0585ba3f6cb7428a2efb62e3c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bd972ff4909df47a3d2fd10d3fecc41eb165123983e089a3db5a4c863a98ad(
    value: typing.Optional[BigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07952a739b7ad2f4ab0a752212ee2483e87fc0cc48df760da3ae411772374b90(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be965b7818b53749a23a96cb39b5f969edd12ac1eb105402b936981661d609f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f0511c9e5bd390d4bf8c39617304be559810e25c0d9eae535988e4cf5dcec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb38a5b7983539db5581a62fc460c6ab37278c3a5d598135f4026d8e0a12d82f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eeb777b80a0b266ead2d57cc7a4befea6065b15814b83832089cc05d02346c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550c9cd19b6a5144870ba237470b8934e45269c05146781cb896679bb9d6063b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryAnalyticsHubDataExchangeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
