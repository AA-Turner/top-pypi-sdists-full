r'''
# `google_apigee_organization`

Refer to the Terraform Registry for docs: [`google_apigee_organization`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization).
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


class ApigeeOrganization(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganization",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization google_apigee_organization}.'''

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
        properties: typing.Optional[typing.Union["ApigeeOrganizationProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        retention: typing.Optional[builtins.str] = None,
        runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
        runtime_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeOrganizationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization google_apigee_organization} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project_id: The project ID associated with the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#project_id ApigeeOrganization#project_id}
        :param analytics_region: Primary GCP region for analytics data storage. For valid values, see `Create an Apigee organization <https://cloud.google.com/apigee/docs/api-platform/get-started/create-org>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#analytics_region ApigeeOrganization#analytics_region}
        :param api_consumer_data_encryption_key_name: Cloud KMS key name used for encrypting API consumer data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#api_consumer_data_encryption_key_name ApigeeOrganization#api_consumer_data_encryption_key_name}
        :param api_consumer_data_location: This field is needed only for customers using non-default data residency regions. Apigee stores some control plane data only in single region. This field determines which single region Apigee should use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#api_consumer_data_location ApigeeOrganization#api_consumer_data_location}
        :param authorized_network: Compute Engine network used for Service Networking to be peered with Apigee runtime instances. See `Getting started with the Service Networking API <https://cloud.google.com/service-infrastructure/docs/service-networking/getting-started>`_. Valid only when 'RuntimeType' is set to CLOUD. The value can be updated only when there are no runtime instances. For example: "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#authorized_network ApigeeOrganization#authorized_network}
        :param billing_type: Billing type of the Apigee organization. See `Apigee pricing <https://cloud.google.com/apigee/pricing>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#billing_type ApigeeOrganization#billing_type}
        :param control_plane_encryption_key_name: Cloud KMS key name used for encrypting control plane data that is stored in a multi region. Only used for the data residency region "US" or "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#control_plane_encryption_key_name ApigeeOrganization#control_plane_encryption_key_name}
        :param description: Description of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#description ApigeeOrganization#description}
        :param disable_vpc_peering: Flag that specifies whether the VPC Peering through Private Google Access should be disabled between the consumer network and Apigee. Required if an 'authorizedNetwork' on the consumer project is not provided, in which case the flag should be set to 'true'. Valid only when 'RuntimeType' is set to CLOUD. The value must be set before the creation of any Apigee runtime instance and can be updated only when there are no runtime instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#disable_vpc_peering ApigeeOrganization#disable_vpc_peering}
        :param display_name: The display name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#display_name ApigeeOrganization#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#id ApigeeOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#properties ApigeeOrganization#properties}
        :param retention: Optional. This setting is applicable only for organizations that are soft-deleted (i.e., BillingType is not EVALUATION). It controls how long Organization data will be retained after the initial delete operation completes. During this period, the Organization may be restored to its last known state. After this period, the Organization will no longer be able to be restored. Default value: "DELETION_RETENTION_UNSPECIFIED" Possible values: ["DELETION_RETENTION_UNSPECIFIED", "MINIMUM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#retention ApigeeOrganization#retention}
        :param runtime_database_encryption_key_name: Cloud KMS key name used for encrypting the data that is stored and replicated across runtime instances. Update is not allowed after the organization is created. If not specified, a Google-Managed encryption key will be used. Valid only when 'RuntimeType' is CLOUD. For example: 'projects/foo/locations/us/keyRings/bar/cryptoKeys/baz'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#runtime_database_encryption_key_name ApigeeOrganization#runtime_database_encryption_key_name}
        :param runtime_type: Runtime type of the Apigee organization based on the Apigee subscription purchased. Default value: "CLOUD" Possible values: ["CLOUD", "HYBRID"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#runtime_type ApigeeOrganization#runtime_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#timeouts ApigeeOrganization#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc693692124bfb8eef2b8e79f6153733295d773ad662f4fbb7637cd9e79b68a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeOrganizationConfig(
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
        '''Generates CDKTF code for importing a ApigeeOrganization resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeOrganization to import.
        :param import_from_id: The id of the existing ApigeeOrganization that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeOrganization to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488239657759dc1562501f92c0ec6d86f9ba606ccfa3911219f2636124dbbd21)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeOrganizationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#property ApigeeOrganization#property}
        '''
        value = ApigeeOrganizationProperties(property=property)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#create ApigeeOrganization#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#delete ApigeeOrganization#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#update ApigeeOrganization#update}.
        '''
        value = ApigeeOrganizationTimeouts(create=create, delete=delete, update=update)

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
    def properties(self) -> "ApigeeOrganizationPropertiesOutputReference":
        return typing.cast("ApigeeOrganizationPropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionType")
    def subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeOrganizationTimeoutsOutputReference":
        return typing.cast("ApigeeOrganizationTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def properties_input(self) -> typing.Optional["ApigeeOrganizationProperties"]:
        return typing.cast(typing.Optional["ApigeeOrganizationProperties"], jsii.get(self, "propertiesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeOrganizationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeOrganizationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticsRegion")
    def analytics_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyticsRegion"))

    @analytics_region.setter
    def analytics_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37bcbe3616be9475ce56b742af0a32a00a3642b593c8f5096b7ed6c19c939bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyticsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiConsumerDataEncryptionKeyName")
    def api_consumer_data_encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiConsumerDataEncryptionKeyName"))

    @api_consumer_data_encryption_key_name.setter
    def api_consumer_data_encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155973c879131bdd93d54e7a15543270c5cf22aa209908de70a64cbd5b84bb19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiConsumerDataEncryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiConsumerDataLocation")
    def api_consumer_data_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiConsumerDataLocation"))

    @api_consumer_data_location.setter
    def api_consumer_data_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16317c012a36f005a83f52b0b2b77c4776f223506d1639317af2ee97b36c4095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiConsumerDataLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizedNetwork")
    def authorized_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedNetwork"))

    @authorized_network.setter
    def authorized_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babb2f23512fd0cfe95ebf5abbf04957cb116462eb0e84f380301cb03973a50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingType")
    def billing_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingType"))

    @billing_type.setter
    def billing_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6b2ca1c1b595a5b985aa3ee73149570a308f2817ecd39c9b4b86f7b5f1f4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryptionKeyName")
    def control_plane_encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneEncryptionKeyName"))

    @control_plane_encryption_key_name.setter
    def control_plane_encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916fa8a671698188e2021fded40a2f628f0d6f808bb131a5f5a048bbb9429572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneEncryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdeea77289fb985a9d51bdf703ea7481b73b5a3337f23082dd752d7934f53bf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5938e9f4f39d6a4a5aeb5543e15b052ed087e31e43396d7376d17761f65f078d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableVpcPeering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a00b53fe3f3f6faebae883c22f893e9b64a2219b4fa79863970c6d74aa4b9c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf0d9d0db81f8f7a72d3810f02abe7d2cda2254659c0ba61af35bf33b5eac8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03eb3ed5028aa13611dbfe267700411a7787ec4703bbb2186c9403861fbe3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retention")
    def retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retention"))

    @retention.setter
    def retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc82a9ab90a9a899b03dd4dc60bba22ead78285b6dd0cfc8a48456c9b4f9adea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeDatabaseEncryptionKeyName")
    def runtime_database_encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeDatabaseEncryptionKeyName"))

    @runtime_database_encryption_key_name.setter
    def runtime_database_encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ceb29179af25680ecea212333008c8c662e3156fed39c46bff0c248b766d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeDatabaseEncryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeType")
    def runtime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeType"))

    @runtime_type.setter
    def runtime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75375a117107bc3304e68ce6a6ffcd47f4a49740bed764fc5b6983bd3d793b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationConfig",
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
class ApigeeOrganizationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        properties: typing.Optional[typing.Union["ApigeeOrganizationProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        retention: typing.Optional[builtins.str] = None,
        runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
        runtime_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeOrganizationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project_id: The project ID associated with the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#project_id ApigeeOrganization#project_id}
        :param analytics_region: Primary GCP region for analytics data storage. For valid values, see `Create an Apigee organization <https://cloud.google.com/apigee/docs/api-platform/get-started/create-org>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#analytics_region ApigeeOrganization#analytics_region}
        :param api_consumer_data_encryption_key_name: Cloud KMS key name used for encrypting API consumer data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#api_consumer_data_encryption_key_name ApigeeOrganization#api_consumer_data_encryption_key_name}
        :param api_consumer_data_location: This field is needed only for customers using non-default data residency regions. Apigee stores some control plane data only in single region. This field determines which single region Apigee should use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#api_consumer_data_location ApigeeOrganization#api_consumer_data_location}
        :param authorized_network: Compute Engine network used for Service Networking to be peered with Apigee runtime instances. See `Getting started with the Service Networking API <https://cloud.google.com/service-infrastructure/docs/service-networking/getting-started>`_. Valid only when 'RuntimeType' is set to CLOUD. The value can be updated only when there are no runtime instances. For example: "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#authorized_network ApigeeOrganization#authorized_network}
        :param billing_type: Billing type of the Apigee organization. See `Apigee pricing <https://cloud.google.com/apigee/pricing>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#billing_type ApigeeOrganization#billing_type}
        :param control_plane_encryption_key_name: Cloud KMS key name used for encrypting control plane data that is stored in a multi region. Only used for the data residency region "US" or "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#control_plane_encryption_key_name ApigeeOrganization#control_plane_encryption_key_name}
        :param description: Description of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#description ApigeeOrganization#description}
        :param disable_vpc_peering: Flag that specifies whether the VPC Peering through Private Google Access should be disabled between the consumer network and Apigee. Required if an 'authorizedNetwork' on the consumer project is not provided, in which case the flag should be set to 'true'. Valid only when 'RuntimeType' is set to CLOUD. The value must be set before the creation of any Apigee runtime instance and can be updated only when there are no runtime instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#disable_vpc_peering ApigeeOrganization#disable_vpc_peering}
        :param display_name: The display name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#display_name ApigeeOrganization#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#id ApigeeOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#properties ApigeeOrganization#properties}
        :param retention: Optional. This setting is applicable only for organizations that are soft-deleted (i.e., BillingType is not EVALUATION). It controls how long Organization data will be retained after the initial delete operation completes. During this period, the Organization may be restored to its last known state. After this period, the Organization will no longer be able to be restored. Default value: "DELETION_RETENTION_UNSPECIFIED" Possible values: ["DELETION_RETENTION_UNSPECIFIED", "MINIMUM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#retention ApigeeOrganization#retention}
        :param runtime_database_encryption_key_name: Cloud KMS key name used for encrypting the data that is stored and replicated across runtime instances. Update is not allowed after the organization is created. If not specified, a Google-Managed encryption key will be used. Valid only when 'RuntimeType' is CLOUD. For example: 'projects/foo/locations/us/keyRings/bar/cryptoKeys/baz'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#runtime_database_encryption_key_name ApigeeOrganization#runtime_database_encryption_key_name}
        :param runtime_type: Runtime type of the Apigee organization based on the Apigee subscription purchased. Default value: "CLOUD" Possible values: ["CLOUD", "HYBRID"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#runtime_type ApigeeOrganization#runtime_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#timeouts ApigeeOrganization#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = ApigeeOrganizationProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = ApigeeOrganizationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0490556b513064e3e78720410f98d159a1c92ab2fb4e5611bfbb66918ea97da5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#project_id ApigeeOrganization#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analytics_region(self) -> typing.Optional[builtins.str]:
        '''Primary GCP region for analytics data storage. For valid values, see `Create an Apigee organization <https://cloud.google.com/apigee/docs/api-platform/get-started/create-org>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#analytics_region ApigeeOrganization#analytics_region}
        '''
        result = self._values.get("analytics_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_consumer_data_encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Cloud KMS key name used for encrypting API consumer data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#api_consumer_data_encryption_key_name ApigeeOrganization#api_consumer_data_encryption_key_name}
        '''
        result = self._values.get("api_consumer_data_encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_consumer_data_location(self) -> typing.Optional[builtins.str]:
        '''This field is needed only for customers using non-default data residency regions.

        Apigee stores some control plane data only in single region.
        This field determines which single region Apigee should use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#api_consumer_data_location ApigeeOrganization#api_consumer_data_location}
        '''
        result = self._values.get("api_consumer_data_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_network(self) -> typing.Optional[builtins.str]:
        '''Compute Engine network used for Service Networking to be peered with Apigee runtime instances.

        See `Getting started with the Service Networking API <https://cloud.google.com/service-infrastructure/docs/service-networking/getting-started>`_.
        Valid only when 'RuntimeType' is set to CLOUD. The value can be updated only when there are no runtime instances. For example: "default".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#authorized_network ApigeeOrganization#authorized_network}
        '''
        result = self._values.get("authorized_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_type(self) -> typing.Optional[builtins.str]:
        '''Billing type of the Apigee organization. See `Apigee pricing <https://cloud.google.com/apigee/pricing>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#billing_type ApigeeOrganization#billing_type}
        '''
        result = self._values.get("billing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Cloud KMS key name used for encrypting control plane data that is stored in a multi region.

        Only used for the data residency region "US" or "EU".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#control_plane_encryption_key_name ApigeeOrganization#control_plane_encryption_key_name}
        '''
        result = self._values.get("control_plane_encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Apigee organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#description ApigeeOrganization#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#disable_vpc_peering ApigeeOrganization#disable_vpc_peering}
        '''
        result = self._values.get("disable_vpc_peering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Apigee organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#display_name ApigeeOrganization#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#id ApigeeOrganization#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional["ApigeeOrganizationProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#properties ApigeeOrganization#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["ApigeeOrganizationProperties"], result)

    @builtins.property
    def retention(self) -> typing.Optional[builtins.str]:
        '''Optional.

        This setting is applicable only for organizations that are soft-deleted (i.e., BillingType
        is not EVALUATION). It controls how long Organization data will be retained after the initial delete
        operation completes. During this period, the Organization may be restored to its last known state.
        After this period, the Organization will no longer be able to be restored. Default value: "DELETION_RETENTION_UNSPECIFIED" Possible values: ["DELETION_RETENTION_UNSPECIFIED", "MINIMUM"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#retention ApigeeOrganization#retention}
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_database_encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Cloud KMS key name used for encrypting the data that is stored and replicated across runtime instances.

        Update is not allowed after the organization is created.
        If not specified, a Google-Managed encryption key will be used.
        Valid only when 'RuntimeType' is CLOUD. For example: 'projects/foo/locations/us/keyRings/bar/cryptoKeys/baz'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#runtime_database_encryption_key_name ApigeeOrganization#runtime_database_encryption_key_name}
        '''
        result = self._values.get("runtime_database_encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_type(self) -> typing.Optional[builtins.str]:
        '''Runtime type of the Apigee organization based on the Apigee subscription purchased. Default value: "CLOUD" Possible values: ["CLOUD", "HYBRID"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#runtime_type ApigeeOrganization#runtime_type}
        '''
        result = self._values.get("runtime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeOrganizationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#timeouts ApigeeOrganization#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeOrganizationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeOrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationProperties",
    jsii_struct_bases=[],
    name_mapping={"property": "property"},
)
class ApigeeOrganizationProperties:
    def __init__(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeOrganizationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#property ApigeeOrganization#property}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6bb6cb064e8ab88b9327e5513f3aed105f520f2fb3b2baa96da89a1c339cd31)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if property is not None:
            self._values["property"] = property

    @builtins.property
    def property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeOrganizationPropertiesProperty"]]]:
        '''property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#property ApigeeOrganization#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeOrganizationPropertiesProperty"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeOrganizationProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeOrganizationPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7f6d42e873f57389a98790081b641dadb57f59f81d003b17073607ee52cc220)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperty")
    def put_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeOrganizationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edab703f53fbe68fe610abd63df69637e260dc77305a30f9b00b91ddd7a37bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperty", [value]))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> "ApigeeOrganizationPropertiesPropertyList":
        return typing.cast("ApigeeOrganizationPropertiesPropertyList", jsii.get(self, "property"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeOrganizationPropertiesProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeOrganizationPropertiesProperty"]]], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeOrganizationProperties]:
        return typing.cast(typing.Optional[ApigeeOrganizationProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeOrganizationProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a491b54317c5be7fb099f195e33f17fdf3cce1e41b61bf628e4eaa2eaae25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationPropertiesProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeOrganizationPropertiesProperty:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#name ApigeeOrganization#name}
        :param value: Value of the property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#value ApigeeOrganization#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1714bc0f710bbc98fc284927d1917380c46b5eaa35217c65a09a0907b4fe7ed5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#name ApigeeOrganization#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#value ApigeeOrganization#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeOrganizationPropertiesProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeOrganizationPropertiesPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationPropertiesPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ceacc9c4740f90bab97139e8a0981275a7aa7f3b73f08c855f59b7508c87519)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeOrganizationPropertiesPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb047d391d753094d4b3f710ae8f73d302b84a33595e05a496d8623de463340)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeOrganizationPropertiesPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11685ebede8410180a735672aad67f001ce1fb503b599892eb4951669e1f884)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8befccf92316171bc4247e5f8fa9f97655c375024a8f2e8646124765a024702b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6687672f7384f095949401bceb54105380e1be6e14d8c66e85738a672f77a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeOrganizationPropertiesProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeOrganizationPropertiesProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeOrganizationPropertiesProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e795bb6b6919796ebfc17b878193110757002a7624f2c63f50424d3e1ae547e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeOrganizationPropertiesPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationPropertiesPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b52b2068a519a32e6976b2a0027b582f577e0fa778bb3d6aefebb7cdcf4548)
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
            type_hints = typing.get_type_hints(_typecheckingstub__275f29ea02b2f8afcd97101de19f994a38f1ea5f3b2a563fe701b960accb3209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fd9a241054b82e80f74560b49da0dfe93265e1ddb8fbef7e3299a0849af0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationPropertiesProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationPropertiesProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationPropertiesProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4092c811461506a9bc5acc52ac4c4edca6e03e80bac82ab92ccba8702a9263d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApigeeOrganizationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#create ApigeeOrganization#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#delete ApigeeOrganization#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#update ApigeeOrganization#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0779e5dcf0d6e2f283835682f08fd2b3a9f285046c6f4f7578e73a74e3d22e03)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#create ApigeeOrganization#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#delete ApigeeOrganization#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_organization#update ApigeeOrganization#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeOrganizationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeOrganizationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeOrganization.ApigeeOrganizationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__633ad5811d661cb6727abeeaa1cd638620b47c8e3255fc71408106efc526dd9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccc6f041dcb23a03eb35456b9fdc3ea2a47070e58f69adbbcd711d94fca0c8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3148a56ac18c1e6372c65f0506cbe2c8dda718a59241f9d645c06cf165f030cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473338306bd9b6e0a2407565291306b2fdacc70c96560a0fe79ec0820db756be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88608279a4ad09d1b1f2b2866e9c98a9aa50987eb4dc949ac887e22ce2ec3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeOrganization",
    "ApigeeOrganizationConfig",
    "ApigeeOrganizationProperties",
    "ApigeeOrganizationPropertiesOutputReference",
    "ApigeeOrganizationPropertiesProperty",
    "ApigeeOrganizationPropertiesPropertyList",
    "ApigeeOrganizationPropertiesPropertyOutputReference",
    "ApigeeOrganizationTimeouts",
    "ApigeeOrganizationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9dc693692124bfb8eef2b8e79f6153733295d773ad662f4fbb7637cd9e79b68a(
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
    properties: typing.Optional[typing.Union[ApigeeOrganizationProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    retention: typing.Optional[builtins.str] = None,
    runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
    runtime_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeOrganizationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__488239657759dc1562501f92c0ec6d86f9ba606ccfa3911219f2636124dbbd21(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37bcbe3616be9475ce56b742af0a32a00a3642b593c8f5096b7ed6c19c939bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155973c879131bdd93d54e7a15543270c5cf22aa209908de70a64cbd5b84bb19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16317c012a36f005a83f52b0b2b77c4776f223506d1639317af2ee97b36c4095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babb2f23512fd0cfe95ebf5abbf04957cb116462eb0e84f380301cb03973a50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6b2ca1c1b595a5b985aa3ee73149570a308f2817ecd39c9b4b86f7b5f1f4ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916fa8a671698188e2021fded40a2f628f0d6f808bb131a5f5a048bbb9429572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdeea77289fb985a9d51bdf703ea7481b73b5a3337f23082dd752d7934f53bf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5938e9f4f39d6a4a5aeb5543e15b052ed087e31e43396d7376d17761f65f078d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a00b53fe3f3f6faebae883c22f893e9b64a2219b4fa79863970c6d74aa4b9c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf0d9d0db81f8f7a72d3810f02abe7d2cda2254659c0ba61af35bf33b5eac8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03eb3ed5028aa13611dbfe267700411a7787ec4703bbb2186c9403861fbe3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc82a9ab90a9a899b03dd4dc60bba22ead78285b6dd0cfc8a48456c9b4f9adea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ceb29179af25680ecea212333008c8c662e3156fed39c46bff0c248b766d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75375a117107bc3304e68ce6a6ffcd47f4a49740bed764fc5b6983bd3d793b76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0490556b513064e3e78720410f98d159a1c92ab2fb4e5611bfbb66918ea97da5(
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
    properties: typing.Optional[typing.Union[ApigeeOrganizationProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    retention: typing.Optional[builtins.str] = None,
    runtime_database_encryption_key_name: typing.Optional[builtins.str] = None,
    runtime_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeOrganizationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bb6cb064e8ab88b9327e5513f3aed105f520f2fb3b2baa96da89a1c339cd31(
    *,
    property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeOrganizationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f6d42e873f57389a98790081b641dadb57f59f81d003b17073607ee52cc220(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edab703f53fbe68fe610abd63df69637e260dc77305a30f9b00b91ddd7a37bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeOrganizationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a491b54317c5be7fb099f195e33f17fdf3cce1e41b61bf628e4eaa2eaae25c(
    value: typing.Optional[ApigeeOrganizationProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1714bc0f710bbc98fc284927d1917380c46b5eaa35217c65a09a0907b4fe7ed5(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ceacc9c4740f90bab97139e8a0981275a7aa7f3b73f08c855f59b7508c87519(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb047d391d753094d4b3f710ae8f73d302b84a33595e05a496d8623de463340(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11685ebede8410180a735672aad67f001ce1fb503b599892eb4951669e1f884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8befccf92316171bc4247e5f8fa9f97655c375024a8f2e8646124765a024702b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6687672f7384f095949401bceb54105380e1be6e14d8c66e85738a672f77a59(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e795bb6b6919796ebfc17b878193110757002a7624f2c63f50424d3e1ae547e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeOrganizationPropertiesProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b52b2068a519a32e6976b2a0027b582f577e0fa778bb3d6aefebb7cdcf4548(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275f29ea02b2f8afcd97101de19f994a38f1ea5f3b2a563fe701b960accb3209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fd9a241054b82e80f74560b49da0dfe93265e1ddb8fbef7e3299a0849af0ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4092c811461506a9bc5acc52ac4c4edca6e03e80bac82ab92ccba8702a9263d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0779e5dcf0d6e2f283835682f08fd2b3a9f285046c6f4f7578e73a74e3d22e03(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633ad5811d661cb6727abeeaa1cd638620b47c8e3255fc71408106efc526dd9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc6f041dcb23a03eb35456b9fdc3ea2a47070e58f69adbbcd711d94fca0c8f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3148a56ac18c1e6372c65f0506cbe2c8dda718a59241f9d645c06cf165f030cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473338306bd9b6e0a2407565291306b2fdacc70c96560a0fe79ec0820db756be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88608279a4ad09d1b1f2b2866e9c98a9aa50987eb4dc949ac887e22ce2ec3ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeOrganizationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
