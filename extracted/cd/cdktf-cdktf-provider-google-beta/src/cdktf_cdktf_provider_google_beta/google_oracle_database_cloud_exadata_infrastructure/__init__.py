r'''
# `google_oracle_database_cloud_exadata_infrastructure`

Refer to the Terraform Registry for docs: [`google_oracle_database_cloud_exadata_infrastructure`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure).
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


class GoogleOracleDatabaseCloudExadataInfrastructure(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructure",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure google_oracle_database_cloud_exadata_infrastructure}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cloud_exadata_infrastructure_id: builtins.str,
        location: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gcp_oracle_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructureProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure google_oracle_database_cloud_exadata_infrastructure} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cloud_exadata_infrastructure_id: The ID of the Exadata Infrastructure to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#cloud_exadata_infrastructure_id GoogleOracleDatabaseCloudExadataInfrastructure#cloud_exadata_infrastructure_id}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/DbServer'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#location GoogleOracleDatabaseCloudExadataInfrastructure#location}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#deletion_protection GoogleOracleDatabaseCloudExadataInfrastructure#deletion_protection}
        :param display_name: User friendly name for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#display_name GoogleOracleDatabaseCloudExadataInfrastructure#display_name}
        :param gcp_oracle_zone: GCP location where Oracle Exadata is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#gcp_oracle_zone GoogleOracleDatabaseCloudExadataInfrastructure#gcp_oracle_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#id GoogleOracleDatabaseCloudExadataInfrastructure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels or tags associated with the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#labels GoogleOracleDatabaseCloudExadataInfrastructure#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#project GoogleOracleDatabaseCloudExadataInfrastructure#project}.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#properties GoogleOracleDatabaseCloudExadataInfrastructure#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#timeouts GoogleOracleDatabaseCloudExadataInfrastructure#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5a8004327c6c8ca7b9850389826f3666a03b234d67af7f43d4df9891892324)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOracleDatabaseCloudExadataInfrastructureConfig(
            cloud_exadata_infrastructure_id=cloud_exadata_infrastructure_id,
            location=location,
            deletion_protection=deletion_protection,
            display_name=display_name,
            gcp_oracle_zone=gcp_oracle_zone,
            id=id,
            labels=labels,
            project=project,
            properties=properties,
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
        '''Generates CDKTF code for importing a GoogleOracleDatabaseCloudExadataInfrastructure resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOracleDatabaseCloudExadataInfrastructure to import.
        :param import_from_id: The id of the existing GoogleOracleDatabaseCloudExadataInfrastructure that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOracleDatabaseCloudExadataInfrastructure to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53bfb019f6bc5518228994651988ff859f8da6867728fcbd2cb6b13973c7107)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        shape: builtins.str,
        compute_count: typing.Optional[jsii.Number] = None,
        customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_count: typing.Optional[jsii.Number] = None,
        total_storage_size_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param shape: The shape of the Exadata Infrastructure. The shape determines the amount of CPU, storage, and memory resources allocated to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#shape GoogleOracleDatabaseCloudExadataInfrastructure#shape}
        :param compute_count: The number of compute servers for the Exadata Infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#compute_count GoogleOracleDatabaseCloudExadataInfrastructure#compute_count}
        :param customer_contacts: customer_contacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#customer_contacts GoogleOracleDatabaseCloudExadataInfrastructure#customer_contacts}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#maintenance_window GoogleOracleDatabaseCloudExadataInfrastructure#maintenance_window}
        :param storage_count: The number of Cloud Exadata storage servers for the Exadata Infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#storage_count GoogleOracleDatabaseCloudExadataInfrastructure#storage_count}
        :param total_storage_size_gb: The total storage allocated to the Exadata Infrastructure resource, in gigabytes (GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#total_storage_size_gb GoogleOracleDatabaseCloudExadataInfrastructure#total_storage_size_gb}
        '''
        value = GoogleOracleDatabaseCloudExadataInfrastructureProperties(
            shape=shape,
            compute_count=compute_count,
            customer_contacts=customer_contacts,
            maintenance_window=maintenance_window,
            storage_count=storage_count,
            total_storage_size_gb=total_storage_size_gb,
        )

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#create GoogleOracleDatabaseCloudExadataInfrastructure#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#delete GoogleOracleDatabaseCloudExadataInfrastructure#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#update GoogleOracleDatabaseCloudExadataInfrastructure#update}.
        '''
        value = GoogleOracleDatabaseCloudExadataInfrastructureTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGcpOracleZone")
    def reset_gcp_oracle_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpOracleZone", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="entitlementId")
    def entitlement_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entitlementId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesOutputReference":
        return typing.cast("GoogleOracleDatabaseCloudExadataInfrastructurePropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleOracleDatabaseCloudExadataInfrastructureTimeoutsOutputReference":
        return typing.cast("GoogleOracleDatabaseCloudExadataInfrastructureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureIdInput")
    def cloud_exadata_infrastructure_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudExadataInfrastructureIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpOracleZoneInput")
    def gcp_oracle_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpOracleZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructureProperties"]:
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructureProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOracleDatabaseCloudExadataInfrastructureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOracleDatabaseCloudExadataInfrastructureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureId")
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureId"))

    @cloud_exadata_infrastructure_id.setter
    def cloud_exadata_infrastructure_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75622dba1598b72e853ce8b7ed380b5fb1e534de943e85593d4c7430eea5feba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudExadataInfrastructureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50115feac305ede3ce848cdb03d14fa895ef56b193b23cabb22ff1a07f8ff064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3842c2c52d288aa84c5514d191b2d3c09f98e70ad066b9ff7a6f193f5bd37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpOracleZone")
    def gcp_oracle_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpOracleZone"))

    @gcp_oracle_zone.setter
    def gcp_oracle_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c289b863eb434c2f1b006acefdf3b31f317a3d2287c0a60defce51c0ec225325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpOracleZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524edf8d17dfa6ec93c80dbf57f560e5d59e2e2bd9d4aaf8fd676c5171e16e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1344ed304210014a4b3bad3fe91cf8cd4ecf88ce80c8f6c0514ae42130ea11c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ca8b55e6ace38029338c1ace05b8f5c7c58d62bd61961aa50ebc4fa6c62f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3039b31d6e992d821906cc63edfb0dbafefde64575881094743c7b0cab07d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cloud_exadata_infrastructure_id": "cloudExadataInfrastructureId",
        "location": "location",
        "deletion_protection": "deletionProtection",
        "display_name": "displayName",
        "gcp_oracle_zone": "gcpOracleZone",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "properties": "properties",
        "timeouts": "timeouts",
    },
)
class GoogleOracleDatabaseCloudExadataInfrastructureConfig(
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
        cloud_exadata_infrastructure_id: builtins.str,
        location: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gcp_oracle_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructureProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cloud_exadata_infrastructure_id: The ID of the Exadata Infrastructure to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#cloud_exadata_infrastructure_id GoogleOracleDatabaseCloudExadataInfrastructure#cloud_exadata_infrastructure_id}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/DbServer'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#location GoogleOracleDatabaseCloudExadataInfrastructure#location}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#deletion_protection GoogleOracleDatabaseCloudExadataInfrastructure#deletion_protection}
        :param display_name: User friendly name for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#display_name GoogleOracleDatabaseCloudExadataInfrastructure#display_name}
        :param gcp_oracle_zone: GCP location where Oracle Exadata is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#gcp_oracle_zone GoogleOracleDatabaseCloudExadataInfrastructure#gcp_oracle_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#id GoogleOracleDatabaseCloudExadataInfrastructure#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels or tags associated with the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#labels GoogleOracleDatabaseCloudExadataInfrastructure#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#project GoogleOracleDatabaseCloudExadataInfrastructure#project}.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#properties GoogleOracleDatabaseCloudExadataInfrastructure#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#timeouts GoogleOracleDatabaseCloudExadataInfrastructure#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = GoogleOracleDatabaseCloudExadataInfrastructureProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = GoogleOracleDatabaseCloudExadataInfrastructureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999facddb4f1e1a3483135a22efa6f4269378d6ff36fe7b12bc224fe4c5ed96b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cloud_exadata_infrastructure_id", value=cloud_exadata_infrastructure_id, expected_type=type_hints["cloud_exadata_infrastructure_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gcp_oracle_zone", value=gcp_oracle_zone, expected_type=type_hints["gcp_oracle_zone"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_exadata_infrastructure_id": cloud_exadata_infrastructure_id,
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
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if display_name is not None:
            self._values["display_name"] = display_name
        if gcp_oracle_zone is not None:
            self._values["gcp_oracle_zone"] = gcp_oracle_zone
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if properties is not None:
            self._values["properties"] = properties
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
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        '''The ID of the Exadata Infrastructure to create.

        This value is restricted
        to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63
        characters in length. The value must start with a letter and end with
        a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#cloud_exadata_infrastructure_id GoogleOracleDatabaseCloudExadataInfrastructure#cloud_exadata_infrastructure_id}
        '''
        result = self._values.get("cloud_exadata_infrastructure_id")
        assert result is not None, "Required property 'cloud_exadata_infrastructure_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/DbServer'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#location GoogleOracleDatabaseCloudExadataInfrastructure#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to allow Terraform to destroy the instance.

        Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#deletion_protection GoogleOracleDatabaseCloudExadataInfrastructure#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User friendly name for this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#display_name GoogleOracleDatabaseCloudExadataInfrastructure#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_oracle_zone(self) -> typing.Optional[builtins.str]:
        '''GCP location where Oracle Exadata is hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#gcp_oracle_zone GoogleOracleDatabaseCloudExadataInfrastructure#gcp_oracle_zone}
        '''
        result = self._values.get("gcp_oracle_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#id GoogleOracleDatabaseCloudExadataInfrastructure#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels or tags associated with the resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#labels GoogleOracleDatabaseCloudExadataInfrastructure#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#project GoogleOracleDatabaseCloudExadataInfrastructure#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructureProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#properties GoogleOracleDatabaseCloudExadataInfrastructure#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructureProperties"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#timeouts GoogleOracleDatabaseCloudExadataInfrastructure#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudExadataInfrastructureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructureProperties",
    jsii_struct_bases=[],
    name_mapping={
        "shape": "shape",
        "compute_count": "computeCount",
        "customer_contacts": "customerContacts",
        "maintenance_window": "maintenanceWindow",
        "storage_count": "storageCount",
        "total_storage_size_gb": "totalStorageSizeGb",
    },
)
class GoogleOracleDatabaseCloudExadataInfrastructureProperties:
    def __init__(
        self,
        *,
        shape: builtins.str,
        compute_count: typing.Optional[jsii.Number] = None,
        customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_count: typing.Optional[jsii.Number] = None,
        total_storage_size_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param shape: The shape of the Exadata Infrastructure. The shape determines the amount of CPU, storage, and memory resources allocated to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#shape GoogleOracleDatabaseCloudExadataInfrastructure#shape}
        :param compute_count: The number of compute servers for the Exadata Infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#compute_count GoogleOracleDatabaseCloudExadataInfrastructure#compute_count}
        :param customer_contacts: customer_contacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#customer_contacts GoogleOracleDatabaseCloudExadataInfrastructure#customer_contacts}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#maintenance_window GoogleOracleDatabaseCloudExadataInfrastructure#maintenance_window}
        :param storage_count: The number of Cloud Exadata storage servers for the Exadata Infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#storage_count GoogleOracleDatabaseCloudExadataInfrastructure#storage_count}
        :param total_storage_size_gb: The total storage allocated to the Exadata Infrastructure resource, in gigabytes (GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#total_storage_size_gb GoogleOracleDatabaseCloudExadataInfrastructure#total_storage_size_gb}
        '''
        if isinstance(maintenance_window, dict):
            maintenance_window = GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow(**maintenance_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cbb22b06d1c72636cfbf66b38937905076c4de978a39b3f295f98401e6ec6db)
            check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
            check_type(argname="argument compute_count", value=compute_count, expected_type=type_hints["compute_count"])
            check_type(argname="argument customer_contacts", value=customer_contacts, expected_type=type_hints["customer_contacts"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument storage_count", value=storage_count, expected_type=type_hints["storage_count"])
            check_type(argname="argument total_storage_size_gb", value=total_storage_size_gb, expected_type=type_hints["total_storage_size_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shape": shape,
        }
        if compute_count is not None:
            self._values["compute_count"] = compute_count
        if customer_contacts is not None:
            self._values["customer_contacts"] = customer_contacts
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if storage_count is not None:
            self._values["storage_count"] = storage_count
        if total_storage_size_gb is not None:
            self._values["total_storage_size_gb"] = total_storage_size_gb

    @builtins.property
    def shape(self) -> builtins.str:
        '''The shape of the Exadata Infrastructure.

        The shape determines the
        amount of CPU, storage, and memory resources allocated to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#shape GoogleOracleDatabaseCloudExadataInfrastructure#shape}
        '''
        result = self._values.get("shape")
        assert result is not None, "Required property 'shape' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_count(self) -> typing.Optional[jsii.Number]:
        '''The number of compute servers for the Exadata Infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#compute_count GoogleOracleDatabaseCloudExadataInfrastructure#compute_count}
        '''
        result = self._values.get("compute_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customer_contacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts"]]]:
        '''customer_contacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#customer_contacts GoogleOracleDatabaseCloudExadataInfrastructure#customer_contacts}
        '''
        result = self._values.get("customer_contacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts"]]], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#maintenance_window GoogleOracleDatabaseCloudExadataInfrastructure#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow"], result)

    @builtins.property
    def storage_count(self) -> typing.Optional[jsii.Number]:
        '''The number of Cloud Exadata storage servers for the Exadata Infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#storage_count GoogleOracleDatabaseCloudExadataInfrastructure#storage_count}
        '''
        result = self._values.get("storage_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_storage_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The total storage allocated to the Exadata Infrastructure resource, in gigabytes (GB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#total_storage_size_gb GoogleOracleDatabaseCloudExadataInfrastructure#total_storage_size_gb}
        '''
        result = self._values.get("total_storage_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudExadataInfrastructureProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts",
    jsii_struct_bases=[],
    name_mapping={"email": "email"},
)
class GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts:
    def __init__(self, *, email: builtins.str) -> None:
        '''
        :param email: The email address used by Oracle to send notifications regarding databases and infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#email GoogleOracleDatabaseCloudExadataInfrastructure#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575e9efa8121eac4d7e9a7e64636f3b56e9de039b91d897f8002af7fcb581912)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }

    @builtins.property
    def email(self) -> builtins.str:
        '''The email address used by Oracle to send notifications regarding databases and infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#email GoogleOracleDatabaseCloudExadataInfrastructure#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d063a2cf9daac0ab077d93a16c0bf2886d40eddb16edec7f54d2a665850bfd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9e8098b79369201f3d842bb1e66ef2c76919eb3f07e0fd75b50ceb77d4cc6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db06419427be80740f088634fad8de3f5ff52c1ca1777a7e26719748d50aadbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31462f4e20953d6f6e02f5512e47f3d13f4bcadd9172b2bd1a2025e3b9a247a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e110ba342b5031aedaf0fc3d0fc53ed6d0fec2016ca13827a02423e6ea7b1ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5068cacac9b2355c72d32016c0817ed558eca745945a491aea4ca1698c4afc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce6f1de398c833c00ab73181f6779c391b3a97d7af6c0713aa97735e0d06542b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4a05943adf6bbc9596f2eb31a205f441cbd849c998cd894fdc0e0a4fb8b738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe36f266e90fc58e81ae208bccc39a4de4d1ad4d3907a9cff724d28bc7ae366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "custom_action_timeout_mins": "customActionTimeoutMins",
        "days_of_week": "daysOfWeek",
        "hours_of_day": "hoursOfDay",
        "is_custom_action_timeout_enabled": "isCustomActionTimeoutEnabled",
        "lead_time_week": "leadTimeWeek",
        "months": "months",
        "patching_mode": "patchingMode",
        "preference": "preference",
        "weeks_of_month": "weeksOfMonth",
    },
)
class GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow:
    def __init__(
        self,
        *,
        custom_action_timeout_mins: typing.Optional[jsii.Number] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        hours_of_day: typing.Optional[typing.Sequence[jsii.Number]] = None,
        is_custom_action_timeout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lead_time_week: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Sequence[builtins.str]] = None,
        patching_mode: typing.Optional[builtins.str] = None,
        preference: typing.Optional[builtins.str] = None,
        weeks_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param custom_action_timeout_mins: Determines the amount of time the system will wait before the start of each database server patching operation. Custom action timeout is in minutes and valid value is between 15 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#custom_action_timeout_mins GoogleOracleDatabaseCloudExadataInfrastructure#custom_action_timeout_mins}
        :param days_of_week: Days during the week when maintenance should be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#days_of_week GoogleOracleDatabaseCloudExadataInfrastructure#days_of_week}
        :param hours_of_day: The window of hours during the day when maintenance should be performed. The window is a 4 hour slot. Valid values are: 0 - represents time slot 0:00 - 3:59 UTC 4 - represents time slot 4:00 - 7:59 UTC 8 - represents time slot 8:00 - 11:59 UTC 12 - represents time slot 12:00 - 15:59 UTC 16 - represents time slot 16:00 - 19:59 UTC 20 - represents time slot 20:00 - 23:59 UTC Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#hours_of_day GoogleOracleDatabaseCloudExadataInfrastructure#hours_of_day}
        :param is_custom_action_timeout_enabled: If true, enables the configuration of a custom action timeout (waiting period) between database server patching operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#is_custom_action_timeout_enabled GoogleOracleDatabaseCloudExadataInfrastructure#is_custom_action_timeout_enabled}
        :param lead_time_week: Lead time window allows user to set a lead time to prepare for a down time. The lead time is in weeks and valid value is between 1 to 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#lead_time_week GoogleOracleDatabaseCloudExadataInfrastructure#lead_time_week}
        :param months: Months during the year when maintenance should be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#months GoogleOracleDatabaseCloudExadataInfrastructure#months}
        :param patching_mode: Cloud CloudExadataInfrastructure node patching method, either "ROLLING" or "NONROLLING". Default value is ROLLING. Possible values: PATCHING_MODE_UNSPECIFIED ROLLING NON_ROLLING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#patching_mode GoogleOracleDatabaseCloudExadataInfrastructure#patching_mode}
        :param preference: The maintenance window scheduling preference. Possible values: MAINTENANCE_WINDOW_PREFERENCE_UNSPECIFIED CUSTOM_PREFERENCE NO_PREFERENCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#preference GoogleOracleDatabaseCloudExadataInfrastructure#preference}
        :param weeks_of_month: Weeks during the month when maintenance should be performed. Weeks start on the 1st, 8th, 15th, and 22nd days of the month, and have a duration of 7 days. Weeks start and end based on calendar dates, not days of the week. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#weeks_of_month GoogleOracleDatabaseCloudExadataInfrastructure#weeks_of_month}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7539059840b1ab6f222bda0e1425fb52a2c33cd5b0ac70c0eddcb86203c22c8)
            check_type(argname="argument custom_action_timeout_mins", value=custom_action_timeout_mins, expected_type=type_hints["custom_action_timeout_mins"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument hours_of_day", value=hours_of_day, expected_type=type_hints["hours_of_day"])
            check_type(argname="argument is_custom_action_timeout_enabled", value=is_custom_action_timeout_enabled, expected_type=type_hints["is_custom_action_timeout_enabled"])
            check_type(argname="argument lead_time_week", value=lead_time_week, expected_type=type_hints["lead_time_week"])
            check_type(argname="argument months", value=months, expected_type=type_hints["months"])
            check_type(argname="argument patching_mode", value=patching_mode, expected_type=type_hints["patching_mode"])
            check_type(argname="argument preference", value=preference, expected_type=type_hints["preference"])
            check_type(argname="argument weeks_of_month", value=weeks_of_month, expected_type=type_hints["weeks_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_action_timeout_mins is not None:
            self._values["custom_action_timeout_mins"] = custom_action_timeout_mins
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if hours_of_day is not None:
            self._values["hours_of_day"] = hours_of_day
        if is_custom_action_timeout_enabled is not None:
            self._values["is_custom_action_timeout_enabled"] = is_custom_action_timeout_enabled
        if lead_time_week is not None:
            self._values["lead_time_week"] = lead_time_week
        if months is not None:
            self._values["months"] = months
        if patching_mode is not None:
            self._values["patching_mode"] = patching_mode
        if preference is not None:
            self._values["preference"] = preference
        if weeks_of_month is not None:
            self._values["weeks_of_month"] = weeks_of_month

    @builtins.property
    def custom_action_timeout_mins(self) -> typing.Optional[jsii.Number]:
        '''Determines the amount of time the system will wait before the start of each database server patching operation.

        Custom action timeout is in minutes and
        valid value is between 15 to 120 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#custom_action_timeout_mins GoogleOracleDatabaseCloudExadataInfrastructure#custom_action_timeout_mins}
        '''
        result = self._values.get("custom_action_timeout_mins")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Days during the week when maintenance should be performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#days_of_week GoogleOracleDatabaseCloudExadataInfrastructure#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hours_of_day(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The window of hours during the day when maintenance should be performed.

        The window is a 4 hour slot. Valid values are:
        0 - represents time slot 0:00 - 3:59 UTC
        4 - represents time slot 4:00 - 7:59 UTC
        8 - represents time slot 8:00 - 11:59 UTC
        12 - represents time slot 12:00 - 15:59 UTC
        16 - represents time slot 16:00 - 19:59 UTC
        20 - represents time slot 20:00 - 23:59 UTC

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#hours_of_day GoogleOracleDatabaseCloudExadataInfrastructure#hours_of_day}
        '''
        result = self._values.get("hours_of_day")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def is_custom_action_timeout_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enables the configuration of a custom action timeout (waiting period) between database server patching operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#is_custom_action_timeout_enabled GoogleOracleDatabaseCloudExadataInfrastructure#is_custom_action_timeout_enabled}
        '''
        result = self._values.get("is_custom_action_timeout_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lead_time_week(self) -> typing.Optional[jsii.Number]:
        '''Lead time window allows user to set a lead time to prepare for a down time.

        The lead time is in weeks and valid value is between 1 to 4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#lead_time_week GoogleOracleDatabaseCloudExadataInfrastructure#lead_time_week}
        '''
        result = self._values.get("lead_time_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def months(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Months during the year when maintenance should be performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#months GoogleOracleDatabaseCloudExadataInfrastructure#months}
        '''
        result = self._values.get("months")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def patching_mode(self) -> typing.Optional[builtins.str]:
        '''Cloud CloudExadataInfrastructure node patching method, either "ROLLING"  or "NONROLLING". Default value is ROLLING.   Possible values:  PATCHING_MODE_UNSPECIFIED ROLLING NON_ROLLING.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#patching_mode GoogleOracleDatabaseCloudExadataInfrastructure#patching_mode}
        '''
        result = self._values.get("patching_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preference(self) -> typing.Optional[builtins.str]:
        '''The maintenance window scheduling preference.   Possible values:  MAINTENANCE_WINDOW_PREFERENCE_UNSPECIFIED CUSTOM_PREFERENCE NO_PREFERENCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#preference GoogleOracleDatabaseCloudExadataInfrastructure#preference}
        '''
        result = self._values.get("preference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weeks_of_month(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Weeks during the month when maintenance should be performed.

        Weeks start on
        the 1st, 8th, 15th, and 22nd days of the month, and have a duration of 7
        days. Weeks start and end based on calendar dates, not days of the week.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#weeks_of_month GoogleOracleDatabaseCloudExadataInfrastructure#weeks_of_month}
        '''
        result = self._values.get("weeks_of_month")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35502580ec5bf19cde0afc339321fd2a73a0f5b91277709b4009217406e6e44d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomActionTimeoutMins")
    def reset_custom_action_timeout_mins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomActionTimeoutMins", []))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetHoursOfDay")
    def reset_hours_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoursOfDay", []))

    @jsii.member(jsii_name="resetIsCustomActionTimeoutEnabled")
    def reset_is_custom_action_timeout_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCustomActionTimeoutEnabled", []))

    @jsii.member(jsii_name="resetLeadTimeWeek")
    def reset_lead_time_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeadTimeWeek", []))

    @jsii.member(jsii_name="resetMonths")
    def reset_months(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonths", []))

    @jsii.member(jsii_name="resetPatchingMode")
    def reset_patching_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchingMode", []))

    @jsii.member(jsii_name="resetPreference")
    def reset_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreference", []))

    @jsii.member(jsii_name="resetWeeksOfMonth")
    def reset_weeks_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeksOfMonth", []))

    @builtins.property
    @jsii.member(jsii_name="customActionTimeoutMinsInput")
    def custom_action_timeout_mins_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customActionTimeoutMinsInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursOfDayInput")
    def hours_of_day_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "hoursOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="isCustomActionTimeoutEnabledInput")
    def is_custom_action_timeout_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCustomActionTimeoutEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="leadTimeWeekInput")
    def lead_time_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "leadTimeWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="monthsInput")
    def months_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monthsInput"))

    @builtins.property
    @jsii.member(jsii_name="patchingModeInput")
    def patching_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patchingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="preferenceInput")
    def preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonthInput")
    def weeks_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "weeksOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="customActionTimeoutMins")
    def custom_action_timeout_mins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customActionTimeoutMins"))

    @custom_action_timeout_mins.setter
    def custom_action_timeout_mins(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e8514955d28e39447cb4327ccc8561bcd60ab110f680420f55026fc32110ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customActionTimeoutMins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e5382b144cbb0dd63c33bbbe5da497e0e7ba91935d833f48b6e476c1917d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hoursOfDay")
    def hours_of_day(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "hoursOfDay"))

    @hours_of_day.setter
    def hours_of_day(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff43f2dee7a5014a9b6fae51f3e8c3bbfbf7cd82de05d3c3276f97bb8a5f017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hoursOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isCustomActionTimeoutEnabled")
    def is_custom_action_timeout_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCustomActionTimeoutEnabled"))

    @is_custom_action_timeout_enabled.setter
    def is_custom_action_timeout_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839277e18fe0fc8a279d046445ff3784386119a3f4f35c711fee531035dfd5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCustomActionTimeoutEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="leadTimeWeek")
    def lead_time_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leadTimeWeek"))

    @lead_time_week.setter
    def lead_time_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bd831f874387a3f11b34a80b322f3918bdd3478517148a5b0e49b2d21b1b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leadTimeWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @months.setter
    def months(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91efef122d7fd76b7124a5d8a1a257ff0829e59316b1df31bda1db899ff71773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "months", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patchingMode")
    def patching_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchingMode"))

    @patching_mode.setter
    def patching_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6973cc2b79d8831cd8833c6dead5b6c1dcdf0910fa77c62caa8679b3864234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preference")
    def preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preference"))

    @preference.setter
    def preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652429ec4b80d09c13861efaf3c92164ffbd717c56c5eb2060be4d3f180360bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonth")
    def weeks_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "weeksOfMonth"))

    @weeks_of_month.setter
    def weeks_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4f4198edb87ba5078949bdc791dc532d070564eb6f17f4e8e45d20644cf4bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeksOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9db18c383af1abda49403c3bb559501faf7b701f77ecdbf9eca2fecfa366a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseCloudExadataInfrastructurePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructurePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a81224609e831892e4fa16933d3d86b002515cb555a971bb1ac5207a0495ebd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerContacts")
    def put_customer_contacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bd9f2b9107227f8a04852d78a0ba51d3009cdf604a1c9beb359ae4544b7cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomerContacts", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        custom_action_timeout_mins: typing.Optional[jsii.Number] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        hours_of_day: typing.Optional[typing.Sequence[jsii.Number]] = None,
        is_custom_action_timeout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lead_time_week: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Sequence[builtins.str]] = None,
        patching_mode: typing.Optional[builtins.str] = None,
        preference: typing.Optional[builtins.str] = None,
        weeks_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param custom_action_timeout_mins: Determines the amount of time the system will wait before the start of each database server patching operation. Custom action timeout is in minutes and valid value is between 15 to 120 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#custom_action_timeout_mins GoogleOracleDatabaseCloudExadataInfrastructure#custom_action_timeout_mins}
        :param days_of_week: Days during the week when maintenance should be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#days_of_week GoogleOracleDatabaseCloudExadataInfrastructure#days_of_week}
        :param hours_of_day: The window of hours during the day when maintenance should be performed. The window is a 4 hour slot. Valid values are: 0 - represents time slot 0:00 - 3:59 UTC 4 - represents time slot 4:00 - 7:59 UTC 8 - represents time slot 8:00 - 11:59 UTC 12 - represents time slot 12:00 - 15:59 UTC 16 - represents time slot 16:00 - 19:59 UTC 20 - represents time slot 20:00 - 23:59 UTC Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#hours_of_day GoogleOracleDatabaseCloudExadataInfrastructure#hours_of_day}
        :param is_custom_action_timeout_enabled: If true, enables the configuration of a custom action timeout (waiting period) between database server patching operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#is_custom_action_timeout_enabled GoogleOracleDatabaseCloudExadataInfrastructure#is_custom_action_timeout_enabled}
        :param lead_time_week: Lead time window allows user to set a lead time to prepare for a down time. The lead time is in weeks and valid value is between 1 to 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#lead_time_week GoogleOracleDatabaseCloudExadataInfrastructure#lead_time_week}
        :param months: Months during the year when maintenance should be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#months GoogleOracleDatabaseCloudExadataInfrastructure#months}
        :param patching_mode: Cloud CloudExadataInfrastructure node patching method, either "ROLLING" or "NONROLLING". Default value is ROLLING. Possible values: PATCHING_MODE_UNSPECIFIED ROLLING NON_ROLLING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#patching_mode GoogleOracleDatabaseCloudExadataInfrastructure#patching_mode}
        :param preference: The maintenance window scheduling preference. Possible values: MAINTENANCE_WINDOW_PREFERENCE_UNSPECIFIED CUSTOM_PREFERENCE NO_PREFERENCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#preference GoogleOracleDatabaseCloudExadataInfrastructure#preference}
        :param weeks_of_month: Weeks during the month when maintenance should be performed. Weeks start on the 1st, 8th, 15th, and 22nd days of the month, and have a duration of 7 days. Weeks start and end based on calendar dates, not days of the week. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#weeks_of_month GoogleOracleDatabaseCloudExadataInfrastructure#weeks_of_month}
        '''
        value = GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow(
            custom_action_timeout_mins=custom_action_timeout_mins,
            days_of_week=days_of_week,
            hours_of_day=hours_of_day,
            is_custom_action_timeout_enabled=is_custom_action_timeout_enabled,
            lead_time_week=lead_time_week,
            months=months,
            patching_mode=patching_mode,
            preference=preference,
            weeks_of_month=weeks_of_month,
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="resetComputeCount")
    def reset_compute_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeCount", []))

    @jsii.member(jsii_name="resetCustomerContacts")
    def reset_customer_contacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerContacts", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetStorageCount")
    def reset_storage_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageCount", []))

    @jsii.member(jsii_name="resetTotalStorageSizeGb")
    def reset_total_storage_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalStorageSizeGb", []))

    @builtins.property
    @jsii.member(jsii_name="activatedStorageCount")
    def activated_storage_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "activatedStorageCount"))

    @builtins.property
    @jsii.member(jsii_name="additionalStorageCount")
    def additional_storage_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalStorageCount"))

    @builtins.property
    @jsii.member(jsii_name="availableStorageSizeGb")
    def available_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(
        self,
    ) -> GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsList:
        return typing.cast(GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsList, jsii.get(self, "customerContacts"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTb")
    def data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeGb")
    def db_node_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dbNodeStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="dbServerVersion")
    def db_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindowOutputReference:
        return typing.cast(GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindowOutputReference, jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="maxCpuCount")
    def max_cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCpuCount"))

    @builtins.property
    @jsii.member(jsii_name="maxDataStorageTb")
    def max_data_storage_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDataStorageTb"))

    @builtins.property
    @jsii.member(jsii_name="maxDbNodeStorageSizeGb")
    def max_db_node_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDbNodeStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGb")
    def max_memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemoryGb"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeGb")
    def memory_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeGb"))

    @builtins.property
    @jsii.member(jsii_name="monthlyDbServerVersion")
    def monthly_db_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monthlyDbServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="monthlyStorageServerVersion")
    def monthly_storage_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monthlyStorageServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="nextMaintenanceRunId")
    def next_maintenance_run_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextMaintenanceRunId"))

    @builtins.property
    @jsii.member(jsii_name="nextMaintenanceRunTime")
    def next_maintenance_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextMaintenanceRunTime"))

    @builtins.property
    @jsii.member(jsii_name="nextSecurityMaintenanceRunTime")
    def next_security_maintenance_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextSecurityMaintenanceRunTime"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="storageServerVersion")
    def storage_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="computeCountInput")
    def compute_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="customerContactsInput")
    def customer_contacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]], jsii.get(self, "customerContactsInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="shapeInput")
    def shape_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shapeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageCountInput")
    def storage_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageCountInput"))

    @builtins.property
    @jsii.member(jsii_name="totalStorageSizeGbInput")
    def total_storage_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalStorageSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="computeCount")
    def compute_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeCount"))

    @compute_count.setter
    def compute_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f43768a25d364f91d8ef77cd0dedfb9c65fac91534f774cd8b2e7fcfeac7392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shape")
    def shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shape"))

    @shape.setter
    def shape(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8d94a426a5ccada5e8d5d24eaa537c546780f07353f468345949d7bc1a3169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shape", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageCount")
    def storage_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageCount"))

    @storage_count.setter
    def storage_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c10714c8d7f6421ca052f803953602ae25c509daa8dfb15fe90c6a0c212b73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalStorageSizeGb")
    def total_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalStorageSizeGb"))

    @total_storage_size_gb.setter
    def total_storage_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a279f55601d19e9b07248e6d3c62a57a208aae20d581feb61adc3ab3897b1d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalStorageSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructureProperties]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructureProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructureProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d945f0fcffd2b928626515e25723c626cbaf4d715e3d4b2a7e7f5170bea78e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleOracleDatabaseCloudExadataInfrastructureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#create GoogleOracleDatabaseCloudExadataInfrastructure#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#delete GoogleOracleDatabaseCloudExadataInfrastructure#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#update GoogleOracleDatabaseCloudExadataInfrastructure#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b1a0da5bbaf70815b24480490759bb5402d3e2259c46d7b2c2cb1069e02ae4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#create GoogleOracleDatabaseCloudExadataInfrastructure#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#delete GoogleOracleDatabaseCloudExadataInfrastructure#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_exadata_infrastructure#update GoogleOracleDatabaseCloudExadataInfrastructure#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudExadataInfrastructureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseCloudExadataInfrastructureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudExadataInfrastructure.GoogleOracleDatabaseCloudExadataInfrastructureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__080046536b1d373ce003d3bf3375f326e995c4c3c76efd3a068460655ff69198)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6de6b12cf88682db21de41b8b3fa8c1f64fcb93ea2e4e8ee0d665cdcc23f028f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa79995a9c5af2ceb62d477f1fdd1b5693ce8d7e4dd407f56ccec20051dcb74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8aa6f70049a7101ac62aae4ad199bc94f3d5000df050586beccf44c5c14ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf32f49ff333ad8aa452cb7652cd32ade83ffb3a0fb892a5d49a174859e4808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOracleDatabaseCloudExadataInfrastructure",
    "GoogleOracleDatabaseCloudExadataInfrastructureConfig",
    "GoogleOracleDatabaseCloudExadataInfrastructureProperties",
    "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts",
    "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsList",
    "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContactsOutputReference",
    "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow",
    "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindowOutputReference",
    "GoogleOracleDatabaseCloudExadataInfrastructurePropertiesOutputReference",
    "GoogleOracleDatabaseCloudExadataInfrastructureTimeouts",
    "GoogleOracleDatabaseCloudExadataInfrastructureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fe5a8004327c6c8ca7b9850389826f3666a03b234d67af7f43d4df9891892324(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cloud_exadata_infrastructure_id: builtins.str,
    location: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gcp_oracle_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructureProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e53bfb019f6bc5518228994651988ff859f8da6867728fcbd2cb6b13973c7107(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75622dba1598b72e853ce8b7ed380b5fb1e534de943e85593d4c7430eea5feba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50115feac305ede3ce848cdb03d14fa895ef56b193b23cabb22ff1a07f8ff064(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3842c2c52d288aa84c5514d191b2d3c09f98e70ad066b9ff7a6f193f5bd37a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c289b863eb434c2f1b006acefdf3b31f317a3d2287c0a60defce51c0ec225325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524edf8d17dfa6ec93c80dbf57f560e5d59e2e2bd9d4aaf8fd676c5171e16e48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1344ed304210014a4b3bad3fe91cf8cd4ecf88ce80c8f6c0514ae42130ea11c6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ca8b55e6ace38029338c1ace05b8f5c7c58d62bd61961aa50ebc4fa6c62f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3039b31d6e992d821906cc63edfb0dbafefde64575881094743c7b0cab07d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999facddb4f1e1a3483135a22efa6f4269378d6ff36fe7b12bc224fe4c5ed96b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloud_exadata_infrastructure_id: builtins.str,
    location: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gcp_oracle_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructureProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbb22b06d1c72636cfbf66b38937905076c4de978a39b3f295f98401e6ec6db(
    *,
    shape: builtins.str,
    compute_count: typing.Optional[jsii.Number] = None,
    customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_count: typing.Optional[jsii.Number] = None,
    total_storage_size_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575e9efa8121eac4d7e9a7e64636f3b56e9de039b91d897f8002af7fcb581912(
    *,
    email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d063a2cf9daac0ab077d93a16c0bf2886d40eddb16edec7f54d2a665850bfd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9e8098b79369201f3d842bb1e66ef2c76919eb3f07e0fd75b50ceb77d4cc6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db06419427be80740f088634fad8de3f5ff52c1ca1777a7e26719748d50aadbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31462f4e20953d6f6e02f5512e47f3d13f4bcadd9172b2bd1a2025e3b9a247a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e110ba342b5031aedaf0fc3d0fc53ed6d0fec2016ca13827a02423e6ea7b1ffb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5068cacac9b2355c72d32016c0817ed558eca745945a491aea4ca1698c4afc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6f1de398c833c00ab73181f6779c391b3a97d7af6c0713aa97735e0d06542b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4a05943adf6bbc9596f2eb31a205f441cbd849c998cd894fdc0e0a4fb8b738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe36f266e90fc58e81ae208bccc39a4de4d1ad4d3907a9cff724d28bc7ae366(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7539059840b1ab6f222bda0e1425fb52a2c33cd5b0ac70c0eddcb86203c22c8(
    *,
    custom_action_timeout_mins: typing.Optional[jsii.Number] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    hours_of_day: typing.Optional[typing.Sequence[jsii.Number]] = None,
    is_custom_action_timeout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lead_time_week: typing.Optional[jsii.Number] = None,
    months: typing.Optional[typing.Sequence[builtins.str]] = None,
    patching_mode: typing.Optional[builtins.str] = None,
    preference: typing.Optional[builtins.str] = None,
    weeks_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35502580ec5bf19cde0afc339321fd2a73a0f5b91277709b4009217406e6e44d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e8514955d28e39447cb4327ccc8561bcd60ab110f680420f55026fc32110ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e5382b144cbb0dd63c33bbbe5da497e0e7ba91935d833f48b6e476c1917d01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff43f2dee7a5014a9b6fae51f3e8c3bbfbf7cd82de05d3c3276f97bb8a5f017(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839277e18fe0fc8a279d046445ff3784386119a3f4f35c711fee531035dfd5e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bd831f874387a3f11b34a80b322f3918bdd3478517148a5b0e49b2d21b1b17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91efef122d7fd76b7124a5d8a1a257ff0829e59316b1df31bda1db899ff71773(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6973cc2b79d8831cd8833c6dead5b6c1dcdf0910fa77c62caa8679b3864234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652429ec4b80d09c13861efaf3c92164ffbd717c56c5eb2060be4d3f180360bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4f4198edb87ba5078949bdc791dc532d070564eb6f17f4e8e45d20644cf4bd(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9db18c383af1abda49403c3bb559501faf7b701f77ecdbf9eca2fecfa366a3(
    value: typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81224609e831892e4fa16933d3d86b002515cb555a971bb1ac5207a0495ebd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bd9f2b9107227f8a04852d78a0ba51d3009cdf604a1c9beb359ae4544b7cef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOracleDatabaseCloudExadataInfrastructurePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f43768a25d364f91d8ef77cd0dedfb9c65fac91534f774cd8b2e7fcfeac7392(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8d94a426a5ccada5e8d5d24eaa537c546780f07353f468345949d7bc1a3169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c10714c8d7f6421ca052f803953602ae25c509daa8dfb15fe90c6a0c212b73e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a279f55601d19e9b07248e6d3c62a57a208aae20d581feb61adc3ab3897b1d1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d945f0fcffd2b928626515e25723c626cbaf4d715e3d4b2a7e7f5170bea78e9c(
    value: typing.Optional[GoogleOracleDatabaseCloudExadataInfrastructureProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b1a0da5bbaf70815b24480490759bb5402d3e2259c46d7b2c2cb1069e02ae4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080046536b1d373ce003d3bf3375f326e995c4c3c76efd3a068460655ff69198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de6b12cf88682db21de41b8b3fa8c1f64fcb93ea2e4e8ee0d665cdcc23f028f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa79995a9c5af2ceb62d477f1fdd1b5693ce8d7e4dd407f56ccec20051dcb74a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8aa6f70049a7101ac62aae4ad199bc94f3d5000df050586beccf44c5c14ab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf32f49ff333ad8aa452cb7652cd32ade83ffb3a0fb892a5d49a174859e4808(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudExadataInfrastructureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
