r'''
# `google_apigee_organization`

Refer to the Terraform Registry for docs: [`google_apigee_organization`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization).
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


class GoogleApigeeOrganization(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganization",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization google_apigee_organization}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project_id: builtins.str,
        analytics_region: typing.Optional[builtins.str] = None,
        api_consumer_data_encryption_key_name: typing.Optional[builtins.str] = None,
        api_consumer_data_location: typing.Optional[builtins.str] = None,
        authorized_network: typing.Optional[builtins.str] = None,
        billing_type: typing.Optional[builtins.str] = None,
        control_plane_encryption_key_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_vpc_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union["GoogleApigeeOrganizationProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        retention: typing.Optional[builtins.str] = None,
        runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
        runtime_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeOrganizationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization google_apigee_organization} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project_id: The project ID associated with the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#project_id GoogleApigeeOrganization#project_id}
        :param analytics_region: Primary GCP region for analytics data storage. For valid values, see `Create an Apigee organization <https://cloud.google.com/apigee/docs/api-platform/get-started/create-org>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#analytics_region GoogleApigeeOrganization#analytics_region}
        :param api_consumer_data_encryption_key_name: Cloud KMS key name used for encrypting API consumer data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#api_consumer_data_encryption_key_name GoogleApigeeOrganization#api_consumer_data_encryption_key_name}
        :param api_consumer_data_location: This field is needed only for customers using non-default data residency regions. Apigee stores some control plane data only in single region. This field determines which single region Apigee should use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#api_consumer_data_location GoogleApigeeOrganization#api_consumer_data_location}
        :param authorized_network: Compute Engine network used for Service Networking to be peered with Apigee runtime instances. See `Getting started with the Service Networking API <https://cloud.google.com/service-infrastructure/docs/service-networking/getting-started>`_. Valid only when 'RuntimeType' is set to CLOUD. The value can be updated only when there are no runtime instances. For example: "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#authorized_network GoogleApigeeOrganization#authorized_network}
        :param billing_type: Billing type of the Apigee organization. See `Apigee pricing <https://cloud.google.com/apigee/pricing>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#billing_type GoogleApigeeOrganization#billing_type}
        :param control_plane_encryption_key_name: Cloud KMS key name used for encrypting control plane data that is stored in a multi region. Only used for the data residency region "US" or "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#control_plane_encryption_key_name GoogleApigeeOrganization#control_plane_encryption_key_name}
        :param description: Description of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#description GoogleApigeeOrganization#description}
        :param disable_vpc_peering: Flag that specifies whether the VPC Peering through Private Google Access should be disabled between the consumer network and Apigee. Required if an 'authorizedNetwork' on the consumer project is not provided, in which case the flag should be set to 'true'. Valid only when 'RuntimeType' is set to CLOUD. The value must be set before the creation of any Apigee runtime instance and can be updated only when there are no runtime instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#disable_vpc_peering GoogleApigeeOrganization#disable_vpc_peering}
        :param display_name: The display name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#display_name GoogleApigeeOrganization#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#id GoogleApigeeOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#properties GoogleApigeeOrganization#properties}
        :param retention: Optional. This setting is applicable only for organizations that are soft-deleted (i.e., BillingType is not EVALUATION). It controls how long Organization data will be retained after the initial delete operation completes. During this period, the Organization may be restored to its last known state. After this period, the Organization will no longer be able to be restored. Default value: "DELETION_RETENTION_UNSPECIFIED" Possible values: ["DELETION_RETENTION_UNSPECIFIED", "MINIMUM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#retention GoogleApigeeOrganization#retention}
        :param runtime_database_encryption_key_name: Cloud KMS key name used for encrypting the data that is stored and replicated across runtime instances. Update is not allowed after the organization is created. If not specified, a Google-Managed encryption key will be used. Valid only when 'RuntimeType' is CLOUD. For example: 'projects/foo/locations/us/keyRings/bar/cryptoKeys/baz'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#runtime_database_encryption_key_name GoogleApigeeOrganization#runtime_database_encryption_key_name}
        :param runtime_type: Runtime type of the Apigee organization based on the Apigee subscription purchased. Default value: "CLOUD" Possible values: ["CLOUD", "HYBRID"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#runtime_type GoogleApigeeOrganization#runtime_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#timeouts GoogleApigeeOrganization#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce68a532787e457a647feb6a997c16276c79740a9702ff79a55059cec502ede)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeOrganizationConfig(
            project_id=project_id,
            analytics_region=analytics_region,
            api_consumer_data_encryption_key_name=api_consumer_data_encryption_key_name,
            api_consumer_data_location=api_consumer_data_location,
            authorized_network=authorized_network,
            billing_type=billing_type,
            control_plane_encryption_key_name=control_plane_encryption_key_name,
            description=description,
            disable_vpc_peering=disable_vpc_peering,
            display_name=display_name,
            id=id,
            properties=properties,
            retention=retention,
            runtime_database_encryption_key_name=runtime_database_encryption_key_name,
            runtime_type=runtime_type,
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
        '''Generates CDKTF code for importing a GoogleApigeeOrganization resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeOrganization to import.
        :param import_from_id: The id of the existing GoogleApigeeOrganization that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeOrganization to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34cf5a78d835c7afe59e40718e4d539383c63068ad70eb2539100cf26606e0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeOrganizationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#property GoogleApigeeOrganization#property}
        '''
        value = GoogleApigeeOrganizationProperties(property=property)

        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#create GoogleApigeeOrganization#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#delete GoogleApigeeOrganization#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#update GoogleApigeeOrganization#update}.
        '''
        value = GoogleApigeeOrganizationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnalyticsRegion")
    def reset_analytics_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticsRegion", []))

    @jsii.member(jsii_name="resetApiConsumerDataEncryptionKeyName")
    def reset_api_consumer_data_encryption_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiConsumerDataEncryptionKeyName", []))

    @jsii.member(jsii_name="resetApiConsumerDataLocation")
    def reset_api_consumer_data_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiConsumerDataLocation", []))

    @jsii.member(jsii_name="resetAuthorizedNetwork")
    def reset_authorized_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedNetwork", []))

    @jsii.member(jsii_name="resetBillingType")
    def reset_billing_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingType", []))

    @jsii.member(jsii_name="resetControlPlaneEncryptionKeyName")
    def reset_control_plane_encryption_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneEncryptionKeyName", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableVpcPeering")
    def reset_disable_vpc_peering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableVpcPeering", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetRetention")
    def reset_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetention", []))

    @jsii.member(jsii_name="resetRuntimeDatabaseEncryptionKeyName")
    def reset_runtime_database_encryption_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeDatabaseEncryptionKeyName", []))

    @jsii.member(jsii_name="resetRuntimeType")
    def reset_runtime_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeType", []))

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
    @jsii.member(jsii_name="apigeeProjectId")
    def apigee_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apigeeProjectId"))

    @builtins.property
    @jsii.member(jsii_name="caCertificate")
    def ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificate"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> "GoogleApigeeOrganizationPropertiesOutputReference":
        return typing.cast("GoogleApigeeOrganizationPropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionType")
    def subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApigeeOrganizationTimeoutsOutputReference":
        return typing.cast("GoogleApigeeOrganizationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="analyticsRegionInput")
    def analytics_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "analyticsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="apiConsumerDataEncryptionKeyNameInput")
    def api_consumer_data_encryption_key_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiConsumerDataEncryptionKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiConsumerDataLocationInput")
    def api_consumer_data_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiConsumerDataLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworkInput")
    def authorized_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="billingTypeInput")
    def billing_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryptionKeyNameInput")
    def control_plane_encryption_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneEncryptionKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableVpcPeeringInput")
    def disable_vpc_peering_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableVpcPeeringInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional["GoogleApigeeOrganizationProperties"]:
        return typing.cast(typing.Optional["GoogleApigeeOrganizationProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionInput")
    def retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeDatabaseEncryptionKeyNameInput")
    def runtime_database_encryption_key_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeDatabaseEncryptionKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeTypeInput")
    def runtime_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeOrganizationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeOrganizationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticsRegion")
    def analytics_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyticsRegion"))

    @analytics_region.setter
    def analytics_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000cb3a31c23035b33e9f8f684fcb0e3c4b97f8c7d75e0117aa0630477372a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyticsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiConsumerDataEncryptionKeyName")
    def api_consumer_data_encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiConsumerDataEncryptionKeyName"))

    @api_consumer_data_encryption_key_name.setter
    def api_consumer_data_encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e32d8a31caa13c1d0b215d74a93e35db6e4e475008002893841680744f6cc8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiConsumerDataEncryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiConsumerDataLocation")
    def api_consumer_data_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiConsumerDataLocation"))

    @api_consumer_data_location.setter
    def api_consumer_data_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4854cdfe1754aba8884961f9a0620bf848259c163642f4db8f7e4d1ee4a8f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiConsumerDataLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizedNetwork")
    def authorized_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedNetwork"))

    @authorized_network.setter
    def authorized_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5474a4b48060ff8154f8afdeb8290a2a8a222d2a505d6b4f8fe7af269f613328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingType")
    def billing_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingType"))

    @billing_type.setter
    def billing_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bd91bc2552dab19425f6b3d0f8c9cd0896ad145959ca4725ee5b961e8dce4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryptionKeyName")
    def control_plane_encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneEncryptionKeyName"))

    @control_plane_encryption_key_name.setter
    def control_plane_encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1d90e777272c778531b55e17b37020c28f7afdb76ddeb84711ca674e65fb16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneEncryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331d09e59c12bba73b438d1d2714be11933716cae7bc4e357a6c63666d8ff55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableVpcPeering")
    def disable_vpc_peering(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableVpcPeering"))

    @disable_vpc_peering.setter
    def disable_vpc_peering(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03451b34cf2b09ecf0a339b167183cc67e8daac265bedfa405df4c7aef5675cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableVpcPeering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef22cb279f7bb2e16d9170dc08236e3d9f07eb4d4c1071cfb7c216a5435a687f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bb4c55897d9f3482e0395b948de72c8c65753dfd8d0fa1596cfd12c13e6fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0de1c006e06c9e9a0043dfaeb9abf26d2db09dc0f07d64fa4d392d911488e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retention")
    def retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retention"))

    @retention.setter
    def retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca694f9e4ddcf35557b0fb4af1e61a5510de742da5f16b64987b92c4be8129c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeDatabaseEncryptionKeyName")
    def runtime_database_encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeDatabaseEncryptionKeyName"))

    @runtime_database_encryption_key_name.setter
    def runtime_database_encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e697085e30950934e4bed25e85e021bdd8536eb6fa6779b153c31a3de4a7529f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeDatabaseEncryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeType")
    def runtime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeType"))

    @runtime_type.setter
    def runtime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81369145b03a26f5c014a75aa2d73b8fba8c38135acd3d38139bc33fa4eb69dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "project_id": "projectId",
        "analytics_region": "analyticsRegion",
        "api_consumer_data_encryption_key_name": "apiConsumerDataEncryptionKeyName",
        "api_consumer_data_location": "apiConsumerDataLocation",
        "authorized_network": "authorizedNetwork",
        "billing_type": "billingType",
        "control_plane_encryption_key_name": "controlPlaneEncryptionKeyName",
        "description": "description",
        "disable_vpc_peering": "disableVpcPeering",
        "display_name": "displayName",
        "id": "id",
        "properties": "properties",
        "retention": "retention",
        "runtime_database_encryption_key_name": "runtimeDatabaseEncryptionKeyName",
        "runtime_type": "runtimeType",
        "timeouts": "timeouts",
    },
)
class GoogleApigeeOrganizationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project_id: builtins.str,
        analytics_region: typing.Optional[builtins.str] = None,
        api_consumer_data_encryption_key_name: typing.Optional[builtins.str] = None,
        api_consumer_data_location: typing.Optional[builtins.str] = None,
        authorized_network: typing.Optional[builtins.str] = None,
        billing_type: typing.Optional[builtins.str] = None,
        control_plane_encryption_key_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_vpc_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union["GoogleApigeeOrganizationProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        retention: typing.Optional[builtins.str] = None,
        runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
        runtime_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeOrganizationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project_id: The project ID associated with the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#project_id GoogleApigeeOrganization#project_id}
        :param analytics_region: Primary GCP region for analytics data storage. For valid values, see `Create an Apigee organization <https://cloud.google.com/apigee/docs/api-platform/get-started/create-org>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#analytics_region GoogleApigeeOrganization#analytics_region}
        :param api_consumer_data_encryption_key_name: Cloud KMS key name used for encrypting API consumer data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#api_consumer_data_encryption_key_name GoogleApigeeOrganization#api_consumer_data_encryption_key_name}
        :param api_consumer_data_location: This field is needed only for customers using non-default data residency regions. Apigee stores some control plane data only in single region. This field determines which single region Apigee should use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#api_consumer_data_location GoogleApigeeOrganization#api_consumer_data_location}
        :param authorized_network: Compute Engine network used for Service Networking to be peered with Apigee runtime instances. See `Getting started with the Service Networking API <https://cloud.google.com/service-infrastructure/docs/service-networking/getting-started>`_. Valid only when 'RuntimeType' is set to CLOUD. The value can be updated only when there are no runtime instances. For example: "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#authorized_network GoogleApigeeOrganization#authorized_network}
        :param billing_type: Billing type of the Apigee organization. See `Apigee pricing <https://cloud.google.com/apigee/pricing>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#billing_type GoogleApigeeOrganization#billing_type}
        :param control_plane_encryption_key_name: Cloud KMS key name used for encrypting control plane data that is stored in a multi region. Only used for the data residency region "US" or "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#control_plane_encryption_key_name GoogleApigeeOrganization#control_plane_encryption_key_name}
        :param description: Description of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#description GoogleApigeeOrganization#description}
        :param disable_vpc_peering: Flag that specifies whether the VPC Peering through Private Google Access should be disabled between the consumer network and Apigee. Required if an 'authorizedNetwork' on the consumer project is not provided, in which case the flag should be set to 'true'. Valid only when 'RuntimeType' is set to CLOUD. The value must be set before the creation of any Apigee runtime instance and can be updated only when there are no runtime instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#disable_vpc_peering GoogleApigeeOrganization#disable_vpc_peering}
        :param display_name: The display name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#display_name GoogleApigeeOrganization#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#id GoogleApigeeOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#properties GoogleApigeeOrganization#properties}
        :param retention: Optional. This setting is applicable only for organizations that are soft-deleted (i.e., BillingType is not EVALUATION). It controls how long Organization data will be retained after the initial delete operation completes. During this period, the Organization may be restored to its last known state. After this period, the Organization will no longer be able to be restored. Default value: "DELETION_RETENTION_UNSPECIFIED" Possible values: ["DELETION_RETENTION_UNSPECIFIED", "MINIMUM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#retention GoogleApigeeOrganization#retention}
        :param runtime_database_encryption_key_name: Cloud KMS key name used for encrypting the data that is stored and replicated across runtime instances. Update is not allowed after the organization is created. If not specified, a Google-Managed encryption key will be used. Valid only when 'RuntimeType' is CLOUD. For example: 'projects/foo/locations/us/keyRings/bar/cryptoKeys/baz'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#runtime_database_encryption_key_name GoogleApigeeOrganization#runtime_database_encryption_key_name}
        :param runtime_type: Runtime type of the Apigee organization based on the Apigee subscription purchased. Default value: "CLOUD" Possible values: ["CLOUD", "HYBRID"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#runtime_type GoogleApigeeOrganization#runtime_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#timeouts GoogleApigeeOrganization#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = GoogleApigeeOrganizationProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeOrganizationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffbfc50f1a72590422c3cf691ee0526238ceed59ff5bd78efae19630d002f4d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument analytics_region", value=analytics_region, expected_type=type_hints["analytics_region"])
            check_type(argname="argument api_consumer_data_encryption_key_name", value=api_consumer_data_encryption_key_name, expected_type=type_hints["api_consumer_data_encryption_key_name"])
            check_type(argname="argument api_consumer_data_location", value=api_consumer_data_location, expected_type=type_hints["api_consumer_data_location"])
            check_type(argname="argument authorized_network", value=authorized_network, expected_type=type_hints["authorized_network"])
            check_type(argname="argument billing_type", value=billing_type, expected_type=type_hints["billing_type"])
            check_type(argname="argument control_plane_encryption_key_name", value=control_plane_encryption_key_name, expected_type=type_hints["control_plane_encryption_key_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_vpc_peering", value=disable_vpc_peering, expected_type=type_hints["disable_vpc_peering"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument runtime_database_encryption_key_name", value=runtime_database_encryption_key_name, expected_type=type_hints["runtime_database_encryption_key_name"])
            check_type(argname="argument runtime_type", value=runtime_type, expected_type=type_hints["runtime_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
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
        if analytics_region is not None:
            self._values["analytics_region"] = analytics_region
        if api_consumer_data_encryption_key_name is not None:
            self._values["api_consumer_data_encryption_key_name"] = api_consumer_data_encryption_key_name
        if api_consumer_data_location is not None:
            self._values["api_consumer_data_location"] = api_consumer_data_location
        if authorized_network is not None:
            self._values["authorized_network"] = authorized_network
        if billing_type is not None:
            self._values["billing_type"] = billing_type
        if control_plane_encryption_key_name is not None:
            self._values["control_plane_encryption_key_name"] = control_plane_encryption_key_name
        if description is not None:
            self._values["description"] = description
        if disable_vpc_peering is not None:
            self._values["disable_vpc_peering"] = disable_vpc_peering
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if properties is not None:
            self._values["properties"] = properties
        if retention is not None:
            self._values["retention"] = retention
        if runtime_database_encryption_key_name is not None:
            self._values["runtime_database_encryption_key_name"] = runtime_database_encryption_key_name
        if runtime_type is not None:
            self._values["runtime_type"] = runtime_type
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
    def project_id(self) -> builtins.str:
        '''The project ID associated with the Apigee organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#project_id GoogleApigeeOrganization#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analytics_region(self) -> typing.Optional[builtins.str]:
        '''Primary GCP region for analytics data storage. For valid values, see `Create an Apigee organization <https://cloud.google.com/apigee/docs/api-platform/get-started/create-org>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#analytics_region GoogleApigeeOrganization#analytics_region}
        '''
        result = self._values.get("analytics_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_consumer_data_encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Cloud KMS key name used for encrypting API consumer data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#api_consumer_data_encryption_key_name GoogleApigeeOrganization#api_consumer_data_encryption_key_name}
        '''
        result = self._values.get("api_consumer_data_encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_consumer_data_location(self) -> typing.Optional[builtins.str]:
        '''This field is needed only for customers using non-default data residency regions.

        Apigee stores some control plane data only in single region.
        This field determines which single region Apigee should use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#api_consumer_data_location GoogleApigeeOrganization#api_consumer_data_location}
        '''
        result = self._values.get("api_consumer_data_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_network(self) -> typing.Optional[builtins.str]:
        '''Compute Engine network used for Service Networking to be peered with Apigee runtime instances.

        See `Getting started with the Service Networking API <https://cloud.google.com/service-infrastructure/docs/service-networking/getting-started>`_.
        Valid only when 'RuntimeType' is set to CLOUD. The value can be updated only when there are no runtime instances. For example: "default".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#authorized_network GoogleApigeeOrganization#authorized_network}
        '''
        result = self._values.get("authorized_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_type(self) -> typing.Optional[builtins.str]:
        '''Billing type of the Apigee organization. See `Apigee pricing <https://cloud.google.com/apigee/pricing>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#billing_type GoogleApigeeOrganization#billing_type}
        '''
        result = self._values.get("billing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Cloud KMS key name used for encrypting control plane data that is stored in a multi region.

        Only used for the data residency region "US" or "EU".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#control_plane_encryption_key_name GoogleApigeeOrganization#control_plane_encryption_key_name}
        '''
        result = self._values.get("control_plane_encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Apigee organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#description GoogleApigeeOrganization#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_vpc_peering(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the VPC Peering through Private Google Access should be disabled between the consumer network and Apigee.

        Required if an 'authorizedNetwork'
        on the consumer project is not provided, in which case the flag should be set to 'true'.
        Valid only when 'RuntimeType' is set to CLOUD. The value must be set before the creation
        of any Apigee runtime instance and can be updated only when there are no runtime instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#disable_vpc_peering GoogleApigeeOrganization#disable_vpc_peering}
        '''
        result = self._values.get("disable_vpc_peering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Apigee organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#display_name GoogleApigeeOrganization#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#id GoogleApigeeOrganization#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional["GoogleApigeeOrganizationProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#properties GoogleApigeeOrganization#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["GoogleApigeeOrganizationProperties"], result)

    @builtins.property
    def retention(self) -> typing.Optional[builtins.str]:
        '''Optional.

        This setting is applicable only for organizations that are soft-deleted (i.e., BillingType
        is not EVALUATION). It controls how long Organization data will be retained after the initial delete
        operation completes. During this period, the Organization may be restored to its last known state.
        After this period, the Organization will no longer be able to be restored. Default value: "DELETION_RETENTION_UNSPECIFIED" Possible values: ["DELETION_RETENTION_UNSPECIFIED", "MINIMUM"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#retention GoogleApigeeOrganization#retention}
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_database_encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Cloud KMS key name used for encrypting the data that is stored and replicated across runtime instances.

        Update is not allowed after the organization is created.
        If not specified, a Google-Managed encryption key will be used.
        Valid only when 'RuntimeType' is CLOUD. For example: 'projects/foo/locations/us/keyRings/bar/cryptoKeys/baz'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#runtime_database_encryption_key_name GoogleApigeeOrganization#runtime_database_encryption_key_name}
        '''
        result = self._values.get("runtime_database_encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_type(self) -> typing.Optional[builtins.str]:
        '''Runtime type of the Apigee organization based on the Apigee subscription purchased. Default value: "CLOUD" Possible values: ["CLOUD", "HYBRID"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#runtime_type GoogleApigeeOrganization#runtime_type}
        '''
        result = self._values.get("runtime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApigeeOrganizationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#timeouts GoogleApigeeOrganization#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeOrganizationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeOrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationProperties",
    jsii_struct_bases=[],
    name_mapping={"property": "property"},
)
class GoogleApigeeOrganizationProperties:
    def __init__(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeOrganizationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#property GoogleApigeeOrganization#property}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96f9d2d898bfbba930c8244fcf81ef16c6e949a42b28290f90c3140ab8ee150)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if property is not None:
            self._values["property"] = property

    @builtins.property
    def property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeOrganizationPropertiesProperty"]]]:
        '''property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#property GoogleApigeeOrganization#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeOrganizationPropertiesProperty"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeOrganizationProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeOrganizationPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c64b45bbb0e07db380ccd07d543ecf30071e55db22b1d20008238831ac9335db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperty")
    def put_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeOrganizationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ed5e8e94e3bf62ee7a5daf4b2d148e8f5d11fbdd2f007c9082db6616025f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperty", [value]))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> "GoogleApigeeOrganizationPropertiesPropertyList":
        return typing.cast("GoogleApigeeOrganizationPropertiesPropertyList", jsii.get(self, "property"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeOrganizationPropertiesProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeOrganizationPropertiesProperty"]]], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeOrganizationProperties]:
        return typing.cast(typing.Optional[GoogleApigeeOrganizationProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeOrganizationProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e787bd4d2550af89a4601368e35401a7915a45582c52adb279606f30a3f72483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationPropertiesProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeOrganizationPropertiesProperty:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#name GoogleApigeeOrganization#name}
        :param value: Value of the property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#value GoogleApigeeOrganization#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02d4c43ac5c12697e1f5a94e1dad66e8c9959768e9abce8a352d6a0afdc3f29)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#name GoogleApigeeOrganization#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#value GoogleApigeeOrganization#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeOrganizationPropertiesProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeOrganizationPropertiesPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationPropertiesPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fe38ac6fbdf3b17b895ce221f01ca796c4a6d553636f5488fc4c73e50a6b760)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeOrganizationPropertiesPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0a86c043f3bd9747df02b506f8c3e21d848f46e84f1e09ea39615d7edd6ef8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeOrganizationPropertiesPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85633c00bf87beb49f5450fa780185c9e33b88838d7d10595712ecf9c212260a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__371b142fa7700baa782eb853c9409503613bead5ceda96f6b986aab6c190c0a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2d4f8514e84fa805f94296582d12e11c80f41a964ab03134ba69b35725bec5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeOrganizationPropertiesProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeOrganizationPropertiesProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeOrganizationPropertiesProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce3c95c06f83e597a7b3da2599f5b257d9ee908a75a72d89c2c843072f994a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeOrganizationPropertiesPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationPropertiesPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__645daea6be1a89e3ca9306a49e38b4ea3f20e53f5e5454946e91a0a8f5890e25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e929f56590ee0e032b605ff34323d0db9ebfaa2902b39199b9f2bbfd8165458a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626efd9aa47965f81a9399a184391ec890a3948608f70390e1fd6e22b1f4776b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationPropertiesProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationPropertiesProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationPropertiesProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4134e9d5a8cee80ef00476e334fc3e4e375f0f3b44a42ffd19c0a97d723d6f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApigeeOrganizationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#create GoogleApigeeOrganization#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#delete GoogleApigeeOrganization#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#update GoogleApigeeOrganization#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2936c10c495b7afb438ccf77921a6a09baf2c8c32d6dee66d8f9a1c97c031f2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#create GoogleApigeeOrganization#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#delete GoogleApigeeOrganization#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_organization#update GoogleApigeeOrganization#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeOrganizationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeOrganizationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeOrganization.GoogleApigeeOrganizationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c03351ce114f7f656fa0f9ea21407c46b58408e064e81def822aeff092743f8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c768915b523c8a11bbbeecdbfe771c26c8ed5e4146234f72650cd73163f49a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d742522960b3bd28d1479d392deb5b726db55d02629996872425c317285413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63173822d40f386e63a39347f2ec151693c6c7e5d5f6b97b428bd82c96a60b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4864c84105d5112ccc4336a04ddd7464b62240b142af098f5f1b446358bd59d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeOrganization",
    "GoogleApigeeOrganizationConfig",
    "GoogleApigeeOrganizationProperties",
    "GoogleApigeeOrganizationPropertiesOutputReference",
    "GoogleApigeeOrganizationPropertiesProperty",
    "GoogleApigeeOrganizationPropertiesPropertyList",
    "GoogleApigeeOrganizationPropertiesPropertyOutputReference",
    "GoogleApigeeOrganizationTimeouts",
    "GoogleApigeeOrganizationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3ce68a532787e457a647feb6a997c16276c79740a9702ff79a55059cec502ede(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project_id: builtins.str,
    analytics_region: typing.Optional[builtins.str] = None,
    api_consumer_data_encryption_key_name: typing.Optional[builtins.str] = None,
    api_consumer_data_location: typing.Optional[builtins.str] = None,
    authorized_network: typing.Optional[builtins.str] = None,
    billing_type: typing.Optional[builtins.str] = None,
    control_plane_encryption_key_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_vpc_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[GoogleApigeeOrganizationProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    retention: typing.Optional[builtins.str] = None,
    runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
    runtime_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeOrganizationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d34cf5a78d835c7afe59e40718e4d539383c63068ad70eb2539100cf26606e0b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000cb3a31c23035b33e9f8f684fcb0e3c4b97f8c7d75e0117aa0630477372a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e32d8a31caa13c1d0b215d74a93e35db6e4e475008002893841680744f6cc8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4854cdfe1754aba8884961f9a0620bf848259c163642f4db8f7e4d1ee4a8f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5474a4b48060ff8154f8afdeb8290a2a8a222d2a505d6b4f8fe7af269f613328(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bd91bc2552dab19425f6b3d0f8c9cd0896ad145959ca4725ee5b961e8dce4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1d90e777272c778531b55e17b37020c28f7afdb76ddeb84711ca674e65fb16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331d09e59c12bba73b438d1d2714be11933716cae7bc4e357a6c63666d8ff55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03451b34cf2b09ecf0a339b167183cc67e8daac265bedfa405df4c7aef5675cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef22cb279f7bb2e16d9170dc08236e3d9f07eb4d4c1071cfb7c216a5435a687f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bb4c55897d9f3482e0395b948de72c8c65753dfd8d0fa1596cfd12c13e6fc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0de1c006e06c9e9a0043dfaeb9abf26d2db09dc0f07d64fa4d392d911488e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca694f9e4ddcf35557b0fb4af1e61a5510de742da5f16b64987b92c4be8129c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e697085e30950934e4bed25e85e021bdd8536eb6fa6779b153c31a3de4a7529f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81369145b03a26f5c014a75aa2d73b8fba8c38135acd3d38139bc33fa4eb69dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffbfc50f1a72590422c3cf691ee0526238ceed59ff5bd78efae19630d002f4d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project_id: builtins.str,
    analytics_region: typing.Optional[builtins.str] = None,
    api_consumer_data_encryption_key_name: typing.Optional[builtins.str] = None,
    api_consumer_data_location: typing.Optional[builtins.str] = None,
    authorized_network: typing.Optional[builtins.str] = None,
    billing_type: typing.Optional[builtins.str] = None,
    control_plane_encryption_key_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_vpc_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[GoogleApigeeOrganizationProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    retention: typing.Optional[builtins.str] = None,
    runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
    runtime_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeOrganizationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96f9d2d898bfbba930c8244fcf81ef16c6e949a42b28290f90c3140ab8ee150(
    *,
    property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeOrganizationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64b45bbb0e07db380ccd07d543ecf30071e55db22b1d20008238831ac9335db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ed5e8e94e3bf62ee7a5daf4b2d148e8f5d11fbdd2f007c9082db6616025f2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeOrganizationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e787bd4d2550af89a4601368e35401a7915a45582c52adb279606f30a3f72483(
    value: typing.Optional[GoogleApigeeOrganizationProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02d4c43ac5c12697e1f5a94e1dad66e8c9959768e9abce8a352d6a0afdc3f29(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe38ac6fbdf3b17b895ce221f01ca796c4a6d553636f5488fc4c73e50a6b760(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0a86c043f3bd9747df02b506f8c3e21d848f46e84f1e09ea39615d7edd6ef8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85633c00bf87beb49f5450fa780185c9e33b88838d7d10595712ecf9c212260a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371b142fa7700baa782eb853c9409503613bead5ceda96f6b986aab6c190c0a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d4f8514e84fa805f94296582d12e11c80f41a964ab03134ba69b35725bec5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce3c95c06f83e597a7b3da2599f5b257d9ee908a75a72d89c2c843072f994a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeOrganizationPropertiesProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645daea6be1a89e3ca9306a49e38b4ea3f20e53f5e5454946e91a0a8f5890e25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e929f56590ee0e032b605ff34323d0db9ebfaa2902b39199b9f2bbfd8165458a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626efd9aa47965f81a9399a184391ec890a3948608f70390e1fd6e22b1f4776b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4134e9d5a8cee80ef00476e334fc3e4e375f0f3b44a42ffd19c0a97d723d6f99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2936c10c495b7afb438ccf77921a6a09baf2c8c32d6dee66d8f9a1c97c031f2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03351ce114f7f656fa0f9ea21407c46b58408e064e81def822aeff092743f8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c768915b523c8a11bbbeecdbfe771c26c8ed5e4146234f72650cd73163f49a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d742522960b3bd28d1479d392deb5b726db55d02629996872425c317285413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63173822d40f386e63a39347f2ec151693c6c7e5d5f6b97b428bd82c96a60b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4864c84105d5112ccc4336a04ddd7464b62240b142af098f5f1b446358bd59d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeOrganizationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
