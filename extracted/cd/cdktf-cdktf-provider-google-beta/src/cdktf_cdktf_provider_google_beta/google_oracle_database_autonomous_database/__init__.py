r'''
# `google_oracle_database_autonomous_database`

Refer to the Terraform Registry for docs: [`google_oracle_database_autonomous_database`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database).
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


class GoogleOracleDatabaseAutonomousDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database google_oracle_database_autonomous_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autonomous_database_id: builtins.str,
        cidr: builtins.str,
        database: builtins.str,
        location: builtins.str,
        network: builtins.str,
        properties: typing.Union["GoogleOracleDatabaseAutonomousDatabaseProperties", typing.Dict[builtins.str, typing.Any]],
        admin_password: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleOracleDatabaseAutonomousDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database google_oracle_database_autonomous_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autonomous_database_id: The ID of the Autonomous Database to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#autonomous_database_id GoogleOracleDatabaseAutonomousDatabase#autonomous_database_id}
        :param cidr: The subnet CIDR range for the Autonmous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#cidr GoogleOracleDatabaseAutonomousDatabase#cidr}
        :param database: The name of the Autonomous Database. The database name must be unique in the project. The name must begin with a letter and can contain a maximum of 30 alphanumeric characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#database GoogleOracleDatabaseAutonomousDatabase#database}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#location GoogleOracleDatabaseAutonomousDatabase#location}
        :param network: The name of the VPC network used by the Autonomous Database. Format: projects/{project}/global/networks/{network}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#network GoogleOracleDatabaseAutonomousDatabase#network}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#properties GoogleOracleDatabaseAutonomousDatabase#properties}
        :param admin_password: The password for the default ADMIN user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#admin_password GoogleOracleDatabaseAutonomousDatabase#admin_password}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#deletion_protection GoogleOracleDatabaseAutonomousDatabase#deletion_protection}
        :param display_name: The display name for the Autonomous Database. The name does not have to be unique within your project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#display_name GoogleOracleDatabaseAutonomousDatabase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#id GoogleOracleDatabaseAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels or tags associated with the Autonomous Database. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#labels GoogleOracleDatabaseAutonomousDatabase#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#project GoogleOracleDatabaseAutonomousDatabase#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#timeouts GoogleOracleDatabaseAutonomousDatabase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df6840c5a346efe5ddde54ed947ea88a715108175451ad89d637e5554fad40b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOracleDatabaseAutonomousDatabaseConfig(
            autonomous_database_id=autonomous_database_id,
            cidr=cidr,
            database=database,
            location=location,
            network=network,
            properties=properties,
            admin_password=admin_password,
            deletion_protection=deletion_protection,
            display_name=display_name,
            id=id,
            labels=labels,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleOracleDatabaseAutonomousDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOracleDatabaseAutonomousDatabase to import.
        :param import_from_id: The id of the existing GoogleOracleDatabaseAutonomousDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOracleDatabaseAutonomousDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76db30ddaf92c0e2960ae38538264d1356bb54a4c99887fb7a50f477e8775b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        db_workload: builtins.str,
        license_type: builtins.str,
        backup_retention_period_days: typing.Optional[jsii.Number] = None,
        character_set: typing.Optional[builtins.str] = None,
        compute_count: typing.Optional[jsii.Number] = None,
        customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_storage_size_gb: typing.Optional[jsii.Number] = None,
        data_storage_size_tb: typing.Optional[jsii.Number] = None,
        db_edition: typing.Optional[builtins.str] = None,
        db_version: typing.Optional[builtins.str] = None,
        is_auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_storage_auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintenance_schedule_type: typing.Optional[builtins.str] = None,
        mtls_connection_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        n_character_set: typing.Optional[builtins.str] = None,
        operations_insights_state: typing.Optional[builtins.str] = None,
        private_endpoint_ip: typing.Optional[builtins.str] = None,
        private_endpoint_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param db_workload: Possible values: DB_WORKLOAD_UNSPECIFIED OLTP DW AJD APEX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_workload GoogleOracleDatabaseAutonomousDatabase#db_workload}
        :param license_type: The license type used for the Autonomous Database. Possible values: LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#license_type GoogleOracleDatabaseAutonomousDatabase#license_type}
        :param backup_retention_period_days: The retention period for the Autonomous Database. This field is specified in days, can range from 1 day to 60 days, and has a default value of 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#backup_retention_period_days GoogleOracleDatabaseAutonomousDatabase#backup_retention_period_days}
        :param character_set: The character set for the Autonomous Database. The default is AL32UTF8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#character_set GoogleOracleDatabaseAutonomousDatabase#character_set}
        :param compute_count: The number of compute servers for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#compute_count GoogleOracleDatabaseAutonomousDatabase#compute_count}
        :param customer_contacts: customer_contacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#customer_contacts GoogleOracleDatabaseAutonomousDatabase#customer_contacts}
        :param data_storage_size_gb: The size of the data stored in the database, in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#data_storage_size_gb GoogleOracleDatabaseAutonomousDatabase#data_storage_size_gb}
        :param data_storage_size_tb: The size of the data stored in the database, in terabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#data_storage_size_tb GoogleOracleDatabaseAutonomousDatabase#data_storage_size_tb}
        :param db_edition: The edition of the Autonomous Databases. Possible values: DATABASE_EDITION_UNSPECIFIED STANDARD_EDITION ENTERPRISE_EDITION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_edition GoogleOracleDatabaseAutonomousDatabase#db_edition}
        :param db_version: The Oracle Database version for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_version GoogleOracleDatabaseAutonomousDatabase#db_version}
        :param is_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database CPU core count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#is_auto_scaling_enabled GoogleOracleDatabaseAutonomousDatabase#is_auto_scaling_enabled}
        :param is_storage_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#is_storage_auto_scaling_enabled GoogleOracleDatabaseAutonomousDatabase#is_storage_auto_scaling_enabled}
        :param maintenance_schedule_type: The maintenance schedule of the Autonomous Database. Possible values: MAINTENANCE_SCHEDULE_TYPE_UNSPECIFIED EARLY REGULAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#maintenance_schedule_type GoogleOracleDatabaseAutonomousDatabase#maintenance_schedule_type}
        :param mtls_connection_required: This field specifies if the Autonomous Database requires mTLS connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#mtls_connection_required GoogleOracleDatabaseAutonomousDatabase#mtls_connection_required}
        :param n_character_set: The national character set for the Autonomous Database. The default is AL16UTF16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#n_character_set GoogleOracleDatabaseAutonomousDatabase#n_character_set}
        :param operations_insights_state: Possible values: OPERATIONS_INSIGHTS_STATE_UNSPECIFIED ENABLING ENABLED DISABLING NOT_ENABLED FAILED_ENABLING FAILED_DISABLING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#operations_insights_state GoogleOracleDatabaseAutonomousDatabase#operations_insights_state}
        :param private_endpoint_ip: The private endpoint IP address for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#private_endpoint_ip GoogleOracleDatabaseAutonomousDatabase#private_endpoint_ip}
        :param private_endpoint_label: The private endpoint label for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#private_endpoint_label GoogleOracleDatabaseAutonomousDatabase#private_endpoint_label}
        '''
        value = GoogleOracleDatabaseAutonomousDatabaseProperties(
            db_workload=db_workload,
            license_type=license_type,
            backup_retention_period_days=backup_retention_period_days,
            character_set=character_set,
            compute_count=compute_count,
            customer_contacts=customer_contacts,
            data_storage_size_gb=data_storage_size_gb,
            data_storage_size_tb=data_storage_size_tb,
            db_edition=db_edition,
            db_version=db_version,
            is_auto_scaling_enabled=is_auto_scaling_enabled,
            is_storage_auto_scaling_enabled=is_storage_auto_scaling_enabled,
            maintenance_schedule_type=maintenance_schedule_type,
            mtls_connection_required=mtls_connection_required,
            n_character_set=n_character_set,
            operations_insights_state=operations_insights_state,
            private_endpoint_ip=private_endpoint_ip,
            private_endpoint_label=private_endpoint_label,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#create GoogleOracleDatabaseAutonomousDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#delete GoogleOracleDatabaseAutonomousDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#update GoogleOracleDatabaseAutonomousDatabase#update}.
        '''
        value = GoogleOracleDatabaseAutonomousDatabaseTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference":
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleOracleDatabaseAutonomousDatabaseTimeoutsOutputReference":
        return typing.cast("GoogleOracleDatabaseAutonomousDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="autonomousDatabaseIdInput")
    def autonomous_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autonomousDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrInput")
    def cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

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
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseAutonomousDatabaseProperties"]:
        return typing.cast(typing.Optional["GoogleOracleDatabaseAutonomousDatabaseProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOracleDatabaseAutonomousDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOracleDatabaseAutonomousDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379b3de4ba90e87589007e8846c7339615e01840a9d1b2a4330ca5247a723651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autonomousDatabaseId")
    def autonomous_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autonomousDatabaseId"))

    @autonomous_database_id.setter
    def autonomous_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d136c5fe2d50e0c7c4373ccb510405e9002926260477c494f6b232e39480c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autonomousDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @cidr.setter
    def cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0e3fba230131de426f8af2916756c537665ac15adc040a98d1857d68bb9511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad1c949c6fa9deb4cc4d0209b29f6ac97504c5b73ca27d14d0877b62840bfa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__684df4e65410f4aa8a720db1b9e78958d686667e52d8ba53e32ece1537c78313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63d7599adce77835faf16b8028add82913a80efec317d763ae21aee81e1d778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bf46dc84e35314fb516b54c99c4a677ac78fa0f93b867fe8bb97f82bcf48ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04fd155e26add47f59d62a85152739837308d738b4a2bd05548ea3100c798495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1a0aae7f1437ca4c30615e132fda0f3b4ac075f693f8db5f510b4087ebf4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260ab77e987cdfce3bdc6afb7118453902d58e418c7cbbac92fc5919ed7c18df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780c48dbf731d6f6dccc32a97e70c10235dd5ac1fa8b605d1d73e617eb864dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "autonomous_database_id": "autonomousDatabaseId",
        "cidr": "cidr",
        "database": "database",
        "location": "location",
        "network": "network",
        "properties": "properties",
        "admin_password": "adminPassword",
        "deletion_protection": "deletionProtection",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleOracleDatabaseAutonomousDatabaseConfig(
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
        autonomous_database_id: builtins.str,
        cidr: builtins.str,
        database: builtins.str,
        location: builtins.str,
        network: builtins.str,
        properties: typing.Union["GoogleOracleDatabaseAutonomousDatabaseProperties", typing.Dict[builtins.str, typing.Any]],
        admin_password: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleOracleDatabaseAutonomousDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autonomous_database_id: The ID of the Autonomous Database to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#autonomous_database_id GoogleOracleDatabaseAutonomousDatabase#autonomous_database_id}
        :param cidr: The subnet CIDR range for the Autonmous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#cidr GoogleOracleDatabaseAutonomousDatabase#cidr}
        :param database: The name of the Autonomous Database. The database name must be unique in the project. The name must begin with a letter and can contain a maximum of 30 alphanumeric characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#database GoogleOracleDatabaseAutonomousDatabase#database}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#location GoogleOracleDatabaseAutonomousDatabase#location}
        :param network: The name of the VPC network used by the Autonomous Database. Format: projects/{project}/global/networks/{network}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#network GoogleOracleDatabaseAutonomousDatabase#network}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#properties GoogleOracleDatabaseAutonomousDatabase#properties}
        :param admin_password: The password for the default ADMIN user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#admin_password GoogleOracleDatabaseAutonomousDatabase#admin_password}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#deletion_protection GoogleOracleDatabaseAutonomousDatabase#deletion_protection}
        :param display_name: The display name for the Autonomous Database. The name does not have to be unique within your project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#display_name GoogleOracleDatabaseAutonomousDatabase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#id GoogleOracleDatabaseAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels or tags associated with the Autonomous Database. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#labels GoogleOracleDatabaseAutonomousDatabase#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#project GoogleOracleDatabaseAutonomousDatabase#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#timeouts GoogleOracleDatabaseAutonomousDatabase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = GoogleOracleDatabaseAutonomousDatabaseProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = GoogleOracleDatabaseAutonomousDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd56d1144d8a6f7bc5d501b03c78b5344469f0fc9511e122394e53a172d6c7cc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument autonomous_database_id", value=autonomous_database_id, expected_type=type_hints["autonomous_database_id"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autonomous_database_id": autonomous_database_id,
            "cidr": cidr,
            "database": database,
            "location": location,
            "network": network,
            "properties": properties,
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
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
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
    def autonomous_database_id(self) -> builtins.str:
        '''The ID of the Autonomous Database to create.

        This value is restricted
        to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63
        characters in length. The value must start with a letter and end with
        a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#autonomous_database_id GoogleOracleDatabaseAutonomousDatabase#autonomous_database_id}
        '''
        result = self._values.get("autonomous_database_id")
        assert result is not None, "Required property 'autonomous_database_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr(self) -> builtins.str:
        '''The subnet CIDR range for the Autonmous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#cidr GoogleOracleDatabaseAutonomousDatabase#cidr}
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(self) -> builtins.str:
        '''The name of the Autonomous Database.

        The database name must be unique in
        the project. The name must begin with a letter and can
        contain a maximum of 30 alphanumeric characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#database GoogleOracleDatabaseAutonomousDatabase#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#location GoogleOracleDatabaseAutonomousDatabase#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The name of the VPC network used by the Autonomous Database. Format: projects/{project}/global/networks/{network}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#network GoogleOracleDatabaseAutonomousDatabase#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def properties(self) -> "GoogleOracleDatabaseAutonomousDatabaseProperties":
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#properties GoogleOracleDatabaseAutonomousDatabase#properties}
        '''
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast("GoogleOracleDatabaseAutonomousDatabaseProperties", result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''The password for the default ADMIN user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#admin_password GoogleOracleDatabaseAutonomousDatabase#admin_password}
        '''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to allow Terraform to destroy the instance.

        Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#deletion_protection GoogleOracleDatabaseAutonomousDatabase#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for the Autonomous Database. The name does not have to be unique within your project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#display_name GoogleOracleDatabaseAutonomousDatabase#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#id GoogleOracleDatabaseAutonomousDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels or tags associated with the Autonomous Database.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#labels GoogleOracleDatabaseAutonomousDatabase#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#project GoogleOracleDatabaseAutonomousDatabase#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseAutonomousDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#timeouts GoogleOracleDatabaseAutonomousDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOracleDatabaseAutonomousDatabaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabaseProperties",
    jsii_struct_bases=[],
    name_mapping={
        "db_workload": "dbWorkload",
        "license_type": "licenseType",
        "backup_retention_period_days": "backupRetentionPeriodDays",
        "character_set": "characterSet",
        "compute_count": "computeCount",
        "customer_contacts": "customerContacts",
        "data_storage_size_gb": "dataStorageSizeGb",
        "data_storage_size_tb": "dataStorageSizeTb",
        "db_edition": "dbEdition",
        "db_version": "dbVersion",
        "is_auto_scaling_enabled": "isAutoScalingEnabled",
        "is_storage_auto_scaling_enabled": "isStorageAutoScalingEnabled",
        "maintenance_schedule_type": "maintenanceScheduleType",
        "mtls_connection_required": "mtlsConnectionRequired",
        "n_character_set": "nCharacterSet",
        "operations_insights_state": "operationsInsightsState",
        "private_endpoint_ip": "privateEndpointIp",
        "private_endpoint_label": "privateEndpointLabel",
    },
)
class GoogleOracleDatabaseAutonomousDatabaseProperties:
    def __init__(
        self,
        *,
        db_workload: builtins.str,
        license_type: builtins.str,
        backup_retention_period_days: typing.Optional[jsii.Number] = None,
        character_set: typing.Optional[builtins.str] = None,
        compute_count: typing.Optional[jsii.Number] = None,
        customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_storage_size_gb: typing.Optional[jsii.Number] = None,
        data_storage_size_tb: typing.Optional[jsii.Number] = None,
        db_edition: typing.Optional[builtins.str] = None,
        db_version: typing.Optional[builtins.str] = None,
        is_auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_storage_auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintenance_schedule_type: typing.Optional[builtins.str] = None,
        mtls_connection_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        n_character_set: typing.Optional[builtins.str] = None,
        operations_insights_state: typing.Optional[builtins.str] = None,
        private_endpoint_ip: typing.Optional[builtins.str] = None,
        private_endpoint_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param db_workload: Possible values: DB_WORKLOAD_UNSPECIFIED OLTP DW AJD APEX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_workload GoogleOracleDatabaseAutonomousDatabase#db_workload}
        :param license_type: The license type used for the Autonomous Database. Possible values: LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#license_type GoogleOracleDatabaseAutonomousDatabase#license_type}
        :param backup_retention_period_days: The retention period for the Autonomous Database. This field is specified in days, can range from 1 day to 60 days, and has a default value of 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#backup_retention_period_days GoogleOracleDatabaseAutonomousDatabase#backup_retention_period_days}
        :param character_set: The character set for the Autonomous Database. The default is AL32UTF8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#character_set GoogleOracleDatabaseAutonomousDatabase#character_set}
        :param compute_count: The number of compute servers for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#compute_count GoogleOracleDatabaseAutonomousDatabase#compute_count}
        :param customer_contacts: customer_contacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#customer_contacts GoogleOracleDatabaseAutonomousDatabase#customer_contacts}
        :param data_storage_size_gb: The size of the data stored in the database, in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#data_storage_size_gb GoogleOracleDatabaseAutonomousDatabase#data_storage_size_gb}
        :param data_storage_size_tb: The size of the data stored in the database, in terabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#data_storage_size_tb GoogleOracleDatabaseAutonomousDatabase#data_storage_size_tb}
        :param db_edition: The edition of the Autonomous Databases. Possible values: DATABASE_EDITION_UNSPECIFIED STANDARD_EDITION ENTERPRISE_EDITION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_edition GoogleOracleDatabaseAutonomousDatabase#db_edition}
        :param db_version: The Oracle Database version for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_version GoogleOracleDatabaseAutonomousDatabase#db_version}
        :param is_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database CPU core count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#is_auto_scaling_enabled GoogleOracleDatabaseAutonomousDatabase#is_auto_scaling_enabled}
        :param is_storage_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#is_storage_auto_scaling_enabled GoogleOracleDatabaseAutonomousDatabase#is_storage_auto_scaling_enabled}
        :param maintenance_schedule_type: The maintenance schedule of the Autonomous Database. Possible values: MAINTENANCE_SCHEDULE_TYPE_UNSPECIFIED EARLY REGULAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#maintenance_schedule_type GoogleOracleDatabaseAutonomousDatabase#maintenance_schedule_type}
        :param mtls_connection_required: This field specifies if the Autonomous Database requires mTLS connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#mtls_connection_required GoogleOracleDatabaseAutonomousDatabase#mtls_connection_required}
        :param n_character_set: The national character set for the Autonomous Database. The default is AL16UTF16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#n_character_set GoogleOracleDatabaseAutonomousDatabase#n_character_set}
        :param operations_insights_state: Possible values: OPERATIONS_INSIGHTS_STATE_UNSPECIFIED ENABLING ENABLED DISABLING NOT_ENABLED FAILED_ENABLING FAILED_DISABLING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#operations_insights_state GoogleOracleDatabaseAutonomousDatabase#operations_insights_state}
        :param private_endpoint_ip: The private endpoint IP address for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#private_endpoint_ip GoogleOracleDatabaseAutonomousDatabase#private_endpoint_ip}
        :param private_endpoint_label: The private endpoint label for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#private_endpoint_label GoogleOracleDatabaseAutonomousDatabase#private_endpoint_label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6d6674f71eb34cfba0a6f5be7a8f33ebac826b74793b51aab72221dffc16c80)
            check_type(argname="argument db_workload", value=db_workload, expected_type=type_hints["db_workload"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument backup_retention_period_days", value=backup_retention_period_days, expected_type=type_hints["backup_retention_period_days"])
            check_type(argname="argument character_set", value=character_set, expected_type=type_hints["character_set"])
            check_type(argname="argument compute_count", value=compute_count, expected_type=type_hints["compute_count"])
            check_type(argname="argument customer_contacts", value=customer_contacts, expected_type=type_hints["customer_contacts"])
            check_type(argname="argument data_storage_size_gb", value=data_storage_size_gb, expected_type=type_hints["data_storage_size_gb"])
            check_type(argname="argument data_storage_size_tb", value=data_storage_size_tb, expected_type=type_hints["data_storage_size_tb"])
            check_type(argname="argument db_edition", value=db_edition, expected_type=type_hints["db_edition"])
            check_type(argname="argument db_version", value=db_version, expected_type=type_hints["db_version"])
            check_type(argname="argument is_auto_scaling_enabled", value=is_auto_scaling_enabled, expected_type=type_hints["is_auto_scaling_enabled"])
            check_type(argname="argument is_storage_auto_scaling_enabled", value=is_storage_auto_scaling_enabled, expected_type=type_hints["is_storage_auto_scaling_enabled"])
            check_type(argname="argument maintenance_schedule_type", value=maintenance_schedule_type, expected_type=type_hints["maintenance_schedule_type"])
            check_type(argname="argument mtls_connection_required", value=mtls_connection_required, expected_type=type_hints["mtls_connection_required"])
            check_type(argname="argument n_character_set", value=n_character_set, expected_type=type_hints["n_character_set"])
            check_type(argname="argument operations_insights_state", value=operations_insights_state, expected_type=type_hints["operations_insights_state"])
            check_type(argname="argument private_endpoint_ip", value=private_endpoint_ip, expected_type=type_hints["private_endpoint_ip"])
            check_type(argname="argument private_endpoint_label", value=private_endpoint_label, expected_type=type_hints["private_endpoint_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db_workload": db_workload,
            "license_type": license_type,
        }
        if backup_retention_period_days is not None:
            self._values["backup_retention_period_days"] = backup_retention_period_days
        if character_set is not None:
            self._values["character_set"] = character_set
        if compute_count is not None:
            self._values["compute_count"] = compute_count
        if customer_contacts is not None:
            self._values["customer_contacts"] = customer_contacts
        if data_storage_size_gb is not None:
            self._values["data_storage_size_gb"] = data_storage_size_gb
        if data_storage_size_tb is not None:
            self._values["data_storage_size_tb"] = data_storage_size_tb
        if db_edition is not None:
            self._values["db_edition"] = db_edition
        if db_version is not None:
            self._values["db_version"] = db_version
        if is_auto_scaling_enabled is not None:
            self._values["is_auto_scaling_enabled"] = is_auto_scaling_enabled
        if is_storage_auto_scaling_enabled is not None:
            self._values["is_storage_auto_scaling_enabled"] = is_storage_auto_scaling_enabled
        if maintenance_schedule_type is not None:
            self._values["maintenance_schedule_type"] = maintenance_schedule_type
        if mtls_connection_required is not None:
            self._values["mtls_connection_required"] = mtls_connection_required
        if n_character_set is not None:
            self._values["n_character_set"] = n_character_set
        if operations_insights_state is not None:
            self._values["operations_insights_state"] = operations_insights_state
        if private_endpoint_ip is not None:
            self._values["private_endpoint_ip"] = private_endpoint_ip
        if private_endpoint_label is not None:
            self._values["private_endpoint_label"] = private_endpoint_label

    @builtins.property
    def db_workload(self) -> builtins.str:
        '''Possible values:  DB_WORKLOAD_UNSPECIFIED OLTP DW AJD APEX.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_workload GoogleOracleDatabaseAutonomousDatabase#db_workload}
        '''
        result = self._values.get("db_workload")
        assert result is not None, "Required property 'db_workload' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_type(self) -> builtins.str:
        '''The license type used for the Autonomous Database.   Possible values:  LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#license_type GoogleOracleDatabaseAutonomousDatabase#license_type}
        '''
        result = self._values.get("license_type")
        assert result is not None, "Required property 'license_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_retention_period_days(self) -> typing.Optional[jsii.Number]:
        '''The retention period for the Autonomous Database.

        This field is specified
        in days, can range from 1 day to 60 days, and has a default value of
        60 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#backup_retention_period_days GoogleOracleDatabaseAutonomousDatabase#backup_retention_period_days}
        '''
        result = self._values.get("backup_retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def character_set(self) -> typing.Optional[builtins.str]:
        '''The character set for the Autonomous Database. The default is AL32UTF8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#character_set GoogleOracleDatabaseAutonomousDatabase#character_set}
        '''
        result = self._values.get("character_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_count(self) -> typing.Optional[jsii.Number]:
        '''The number of compute servers for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#compute_count GoogleOracleDatabaseAutonomousDatabase#compute_count}
        '''
        result = self._values.get("compute_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customer_contacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts"]]]:
        '''customer_contacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#customer_contacts GoogleOracleDatabaseAutonomousDatabase#customer_contacts}
        '''
        result = self._values.get("customer_contacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts"]]], result)

    @builtins.property
    def data_storage_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the data stored in the database, in gigabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#data_storage_size_gb GoogleOracleDatabaseAutonomousDatabase#data_storage_size_gb}
        '''
        result = self._values.get("data_storage_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_storage_size_tb(self) -> typing.Optional[jsii.Number]:
        '''The size of the data stored in the database, in terabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#data_storage_size_tb GoogleOracleDatabaseAutonomousDatabase#data_storage_size_tb}
        '''
        result = self._values.get("data_storage_size_tb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_edition(self) -> typing.Optional[builtins.str]:
        '''The edition of the Autonomous Databases.   Possible values:  DATABASE_EDITION_UNSPECIFIED STANDARD_EDITION ENTERPRISE_EDITION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_edition GoogleOracleDatabaseAutonomousDatabase#db_edition}
        '''
        result = self._values.get("db_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_version(self) -> typing.Optional[builtins.str]:
        '''The Oracle Database version for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#db_version GoogleOracleDatabaseAutonomousDatabase#db_version}
        '''
        result = self._values.get("db_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_auto_scaling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field indicates if auto scaling is enabled for the Autonomous Database CPU core count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#is_auto_scaling_enabled GoogleOracleDatabaseAutonomousDatabase#is_auto_scaling_enabled}
        '''
        result = self._values.get("is_auto_scaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_storage_auto_scaling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field indicates if auto scaling is enabled for the Autonomous Database storage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#is_storage_auto_scaling_enabled GoogleOracleDatabaseAutonomousDatabase#is_storage_auto_scaling_enabled}
        '''
        result = self._values.get("is_storage_auto_scaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maintenance_schedule_type(self) -> typing.Optional[builtins.str]:
        '''The maintenance schedule of the Autonomous Database.   Possible values:  MAINTENANCE_SCHEDULE_TYPE_UNSPECIFIED EARLY REGULAR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#maintenance_schedule_type GoogleOracleDatabaseAutonomousDatabase#maintenance_schedule_type}
        '''
        result = self._values.get("maintenance_schedule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtls_connection_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field specifies if the Autonomous Database requires mTLS connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#mtls_connection_required GoogleOracleDatabaseAutonomousDatabase#mtls_connection_required}
        '''
        result = self._values.get("mtls_connection_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def n_character_set(self) -> typing.Optional[builtins.str]:
        '''The national character set for the Autonomous Database. The default is AL16UTF16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#n_character_set GoogleOracleDatabaseAutonomousDatabase#n_character_set}
        '''
        result = self._values.get("n_character_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations_insights_state(self) -> typing.Optional[builtins.str]:
        '''Possible values:  OPERATIONS_INSIGHTS_STATE_UNSPECIFIED ENABLING ENABLED DISABLING NOT_ENABLED FAILED_ENABLING FAILED_DISABLING.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#operations_insights_state GoogleOracleDatabaseAutonomousDatabase#operations_insights_state}
        '''
        result = self._values.get("operations_insights_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_endpoint_ip(self) -> typing.Optional[builtins.str]:
        '''The private endpoint IP address for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#private_endpoint_ip GoogleOracleDatabaseAutonomousDatabase#private_endpoint_ip}
        '''
        result = self._values.get("private_endpoint_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_endpoint_label(self) -> typing.Optional[builtins.str]:
        '''The private endpoint label for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#private_endpoint_label GoogleOracleDatabaseAutonomousDatabase#private_endpoint_label}
        '''
        result = self._values.get("private_endpoint_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabaseProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d16465ded872632a23708b5f9c94e1e9d99d2648b0a9b1b184204fe6ceb89f77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8cdfecf15cb6c611fecebf8c770eb9773ffa526c94d7bfaaf8a83ee0887312)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e49e09fd044d151db114520dbb857567eecabe2735f01252c859e3ddf1ba66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeaa2f28675b23819f9aa117c6446fedfc6afd2ef89d4a7214e492f7d4f4601c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce1b87b883345f065a2667749c53ddd280e1f38b41e13558268f080a4edadc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__218d9bb45e97c15889ed65eeceb8b0412455fc480dbd07a257769db5c06e925d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="apexVersion")
    def apex_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apexVersion"))

    @builtins.property
    @jsii.member(jsii_name="ordsVersion")
    def ords_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ordsVersion"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd846e56a762df843f2ba5dc55f8fa622baa3cd600ba68a07c68aceb234c3c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e3cbc9c50736ece685f087d36d6b4c7d62d9eb6a680635669eb087e66f906d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25021ddbfe531922f159731b3992b798a4aae7e900aec119727cf273d8c747b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2dae74e9bb0580b607997cc69d7e4d2af0883a693c5f81773ab3d12849c3555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2aca666ac78f471e51b1493ec942c85a3798991764ff89e038a54b83a4a08c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__807a6df4b38616448b54150c8120bce2be988c46f0656b878840692db0cbc417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f0e09863579822561842356e154f977507ab48557e8f01b351a4dd23339184b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="high")
    def high(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "high"))

    @builtins.property
    @jsii.member(jsii_name="low")
    def low(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "low"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8335efa0ded1b2cc2aeb66bceb77572c88ae5f925380dc4a6d1696093310c2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__601831023bf7f7bbb4fc21fbdbad04a80c4905fb01e63281bb23f88b961e9b13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98999dceee77f9c76735f9c8bba7779864eea8172f5fe2fa11df9aaddc11dfe1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7e9a32e59c02a726cb2cf4a90e8d6b4fa85bbc961315eddb9a95f1e3592415)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aa1bb15837216ee80f67741de789f4c567ba88e438653a00409c483773ca428)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b9ddbef488c161499325af8cae51a8418749a2de70645dd80cd25a534398980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe4c05495b19a308f26ca217ed44a7cdb56ad7b9887f8625f164a878ad207d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allConnectionStrings")
    def all_connection_strings(
        self,
    ) -> GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList:
        return typing.cast(GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList, jsii.get(self, "allConnectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="dedicated")
    def dedicated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicated"))

    @builtins.property
    @jsii.member(jsii_name="high")
    def high(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "high"))

    @builtins.property
    @jsii.member(jsii_name="low")
    def low(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "low"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @builtins.property
    @jsii.member(jsii_name="profiles")
    def profiles(
        self,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList":
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList", jsii.get(self, "profiles"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729fb44449ac82e44a312b7f2164d7482cd49ef93575d1d2ba17835f5740d35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b941318744acbd9bc2a9d54d3dc4ec18680f998d3c1c79d8ae73b5aac6834dcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80c15ca010e8479cb8d263101dc07906af7328caa250db15f6ed48e7885e05a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ece19f94e35e584471ffd9d8f4facc1d6adc23677eb164bc607b5053cc490e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d2867843ddb03ed3854ecb53d449be40313ec9341bee44b2bca3290abee7778)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6ab45e8294d649ca923c3196fc326bd12a7a2a76378d0e7dff17721eae4ca0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c8466452f95c820381c8271646319d5140cad6bfff4aa73d25f603d01cb7328)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="consumerGroup")
    def consumer_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroup"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="hostFormat")
    def host_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostFormat"))

    @builtins.property
    @jsii.member(jsii_name="isRegional")
    def is_regional(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isRegional"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="sessionMode")
    def session_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionMode"))

    @builtins.property
    @jsii.member(jsii_name="syntaxFormat")
    def syntax_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syntaxFormat"))

    @builtins.property
    @jsii.member(jsii_name="tlsAuthentication")
    def tls_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1ea12f062ff37bedeb235e632aebf6d60de2da8ad2ccfe20cafe65d2faaaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2b952df438e10b6e8e98e65e0b12a62b075af04687e60d783a2336c911a9536)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396b25ad9a34a22dbe5f9b42e68622d24bf0c7cccdf52680ab2c2b9402f518b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cf0fbaed21043cc0f7cda178eb6cb604a7334880956f1a28a9a4d3208899c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e3213e8f89f89edaf837372d195618c25f1bf230006d359b8e58084ba61a611)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ee823dd0b65dd18a3d5dfda8d316e1fd440219497e0c6eb7068da9308ea74c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73098ad8bedf85fe6103ec548d45bd7cc96de720de9f23be4581d13b8f2a47f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="apexUri")
    def apex_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apexUri"))

    @builtins.property
    @jsii.member(jsii_name="databaseTransformsUri")
    def database_transforms_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseTransformsUri"))

    @builtins.property
    @jsii.member(jsii_name="graphStudioUri")
    def graph_studio_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "graphStudioUri"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningNotebookUri")
    def machine_learning_notebook_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineLearningNotebookUri"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningUserManagementUri")
    def machine_learning_user_management_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineLearningUserManagementUri"))

    @builtins.property
    @jsii.member(jsii_name="mongoDbUri")
    def mongo_db_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mongoDbUri"))

    @builtins.property
    @jsii.member(jsii_name="ordsUri")
    def ords_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ordsUri"))

    @builtins.property
    @jsii.member(jsii_name="sqlDevWebUri")
    def sql_dev_web_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlDevWebUri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d10ccb75f03d844de8de97e8f7ea6597320ea838c7cbd6d79977099a725ffa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts",
    jsii_struct_bases=[],
    name_mapping={"email": "email"},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts:
    def __init__(self, *, email: builtins.str) -> None:
        '''
        :param email: The email address used by Oracle to send notifications regarding databases and infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#email GoogleOracleDatabaseAutonomousDatabase#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f517a4625a4ec92093c4858a3b10e415af63da8edbd12f19612d991c26b3a6)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }

    @builtins.property
    def email(self) -> builtins.str:
        '''The email address used by Oracle to send notifications regarding databases and infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#email GoogleOracleDatabaseAutonomousDatabase#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deaa0629f6a959dfc63ee812d81402ecbc67f225e1de423dc470c693058ebe15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdcf17d559e67af4fbfc5e7991cbc983ee7f4cb9c14dc0c6578d9e9c51e6772)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31053e0bf761a6316e6b1801025f34bc490c1ca7670f1eb1227b0c6abd16b440)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad648c1ad0b2602db3f869cb9ced1e37a0a66fbef47e1b5c357aa4ac81c01818)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c39a25c8618d924e29e594be875e6d117701c6ba8a75b524df8ea1a132f8b227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c589472dba983ac6e4f278d4ba8ba7105636bd927238a505c20299ef1cc75cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b323a36d43a17e4b584857677d7787d337a79501e08a267320b600272de459c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a210cbe59967bb9fc9094c6f5d99f047b2961360e0fff96d9eb981d7c9407ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3c1bd46c076267ad0ed4e6a5a0526fb71e13a2ab4a965bcba7d0e05ed5d713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69e6f8d716fc4d3fac68c359e756f79eee62c41413b26e675485fa70b68656a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32697bbc06e2748d5c3f425c2faf7343cc2893d089d795e477f25afabbe11e7d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5588f997a9177fc7286ff39da1e0039cd400166ed168817a1a70053d5a36717)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd79cb0f12d8bdf0fdf19618aa5497c59b32282582a0521070e3517f1692eb01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5dd3972416e00fdb7e95ca709f5bd545360c678a90b76d3b6f0ba5587588805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__163aad53121b84783e74a853a5aa4ed48abd0b9ae8c0f204b51eca0fdaff3224)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataGuardRoleChangedTime")
    def data_guard_role_changed_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataGuardRoleChangedTime"))

    @builtins.property
    @jsii.member(jsii_name="disasterRecoveryRoleChangedTime")
    def disaster_recovery_role_changed_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disasterRecoveryRoleChangedTime"))

    @builtins.property
    @jsii.member(jsii_name="lagTimeDuration")
    def lag_time_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lagTimeDuration"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleDetails")
    def lifecycle_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleDetails"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc08fa4adf5cb221e131db00e30dce66243482d060c7b3ebc4a1d0ef019ad852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00247a98775bcd8bdef506e044d240835f0e70a3deac9ca15cb73240d21adfda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerContacts")
    def put_customer_contacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a13a7c1c32c46bd2db7f088c8bf5bcf188ec20a634da057f900ed49ceb995b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomerContacts", [value]))

    @jsii.member(jsii_name="resetBackupRetentionPeriodDays")
    def reset_backup_retention_period_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRetentionPeriodDays", []))

    @jsii.member(jsii_name="resetCharacterSet")
    def reset_character_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCharacterSet", []))

    @jsii.member(jsii_name="resetComputeCount")
    def reset_compute_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeCount", []))

    @jsii.member(jsii_name="resetCustomerContacts")
    def reset_customer_contacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerContacts", []))

    @jsii.member(jsii_name="resetDataStorageSizeGb")
    def reset_data_storage_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStorageSizeGb", []))

    @jsii.member(jsii_name="resetDataStorageSizeTb")
    def reset_data_storage_size_tb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStorageSizeTb", []))

    @jsii.member(jsii_name="resetDbEdition")
    def reset_db_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbEdition", []))

    @jsii.member(jsii_name="resetDbVersion")
    def reset_db_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbVersion", []))

    @jsii.member(jsii_name="resetIsAutoScalingEnabled")
    def reset_is_auto_scaling_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsAutoScalingEnabled", []))

    @jsii.member(jsii_name="resetIsStorageAutoScalingEnabled")
    def reset_is_storage_auto_scaling_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsStorageAutoScalingEnabled", []))

    @jsii.member(jsii_name="resetMaintenanceScheduleType")
    def reset_maintenance_schedule_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceScheduleType", []))

    @jsii.member(jsii_name="resetMtlsConnectionRequired")
    def reset_mtls_connection_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtlsConnectionRequired", []))

    @jsii.member(jsii_name="resetNCharacterSet")
    def reset_n_character_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNCharacterSet", []))

    @jsii.member(jsii_name="resetOperationsInsightsState")
    def reset_operations_insights_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationsInsightsState", []))

    @jsii.member(jsii_name="resetPrivateEndpointIp")
    def reset_private_endpoint_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateEndpointIp", []))

    @jsii.member(jsii_name="resetPrivateEndpointLabel")
    def reset_private_endpoint_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateEndpointLabel", []))

    @builtins.property
    @jsii.member(jsii_name="actualUsedDataStorageSizeTb")
    def actual_used_data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "actualUsedDataStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="allocatedStorageSizeTb")
    def allocated_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocatedStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="apexDetails")
    def apex_details(
        self,
    ) -> GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList:
        return typing.cast(GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList, jsii.get(self, "apexDetails"))

    @builtins.property
    @jsii.member(jsii_name="arePrimaryAllowlistedIpsUsed")
    def are_primary_allowlisted_ips_used(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "arePrimaryAllowlistedIpsUsed"))

    @builtins.property
    @jsii.member(jsii_name="autonomousContainerDatabaseId")
    def autonomous_container_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autonomousContainerDatabaseId"))

    @builtins.property
    @jsii.member(jsii_name="availableUpgradeVersions")
    def available_upgrade_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableUpgradeVersions"))

    @builtins.property
    @jsii.member(jsii_name="connectionStrings")
    def connection_strings(
        self,
    ) -> GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList:
        return typing.cast(GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList, jsii.get(self, "connectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrls")
    def connection_urls(
        self,
    ) -> GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList:
        return typing.cast(GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList, jsii.get(self, "connectionUrls"))

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(
        self,
    ) -> GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList:
        return typing.cast(GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList, jsii.get(self, "customerContacts"))

    @builtins.property
    @jsii.member(jsii_name="databaseManagementState")
    def database_management_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseManagementState"))

    @builtins.property
    @jsii.member(jsii_name="dataSafeState")
    def data_safe_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSafeState"))

    @builtins.property
    @jsii.member(jsii_name="failedDataRecoveryDuration")
    def failed_data_recovery_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failedDataRecoveryDuration"))

    @builtins.property
    @jsii.member(jsii_name="isLocalDataGuardEnabled")
    def is_local_data_guard_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isLocalDataGuardEnabled"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleDetails")
    def lifecycle_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleDetails"))

    @builtins.property
    @jsii.member(jsii_name="localAdgAutoFailoverMaxDataLossLimit")
    def local_adg_auto_failover_max_data_loss_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localAdgAutoFailoverMaxDataLossLimit"))

    @builtins.property
    @jsii.member(jsii_name="localDisasterRecoveryType")
    def local_disaster_recovery_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localDisasterRecoveryType"))

    @builtins.property
    @jsii.member(jsii_name="localStandbyDb")
    def local_standby_db(
        self,
    ) -> GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList:
        return typing.cast(GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList, jsii.get(self, "localStandbyDb"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceBeginTime")
    def maintenance_begin_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceBeginTime"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceEndTime")
    def maintenance_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceEndTime"))

    @builtins.property
    @jsii.member(jsii_name="memoryPerOracleComputeUnitGbs")
    def memory_per_oracle_compute_unit_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryPerOracleComputeUnitGbs"))

    @builtins.property
    @jsii.member(jsii_name="memoryTableGbs")
    def memory_table_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryTableGbs"))

    @builtins.property
    @jsii.member(jsii_name="nextLongTermBackupTime")
    def next_long_term_backup_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextLongTermBackupTime"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="openMode")
    def open_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openMode"))

    @builtins.property
    @jsii.member(jsii_name="peerDbIds")
    def peer_db_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "peerDbIds"))

    @builtins.property
    @jsii.member(jsii_name="permissionLevel")
    def permission_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionLevel"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpoint")
    def private_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="refreshableMode")
    def refreshable_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshableMode"))

    @builtins.property
    @jsii.member(jsii_name="refreshableState")
    def refreshable_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshableState"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="scheduledOperationDetails")
    def scheduled_operation_details(
        self,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList":
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList", jsii.get(self, "scheduledOperationDetails"))

    @builtins.property
    @jsii.member(jsii_name="sqlWebDeveloperUrl")
    def sql_web_developer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlWebDeveloperUrl"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="supportedCloneRegions")
    def supported_clone_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedCloneRegions"))

    @builtins.property
    @jsii.member(jsii_name="totalAutoBackupStorageSizeGbs")
    def total_auto_backup_storage_size_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalAutoBackupStorageSizeGbs"))

    @builtins.property
    @jsii.member(jsii_name="usedDataStorageSizeTbs")
    def used_data_storage_size_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedDataStorageSizeTbs"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriodDaysInput")
    def backup_retention_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="characterSetInput")
    def character_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "characterSetInput"))

    @builtins.property
    @jsii.member(jsii_name="computeCountInput")
    def compute_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="customerContactsInput")
    def customer_contacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]], jsii.get(self, "customerContactsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeGbInput")
    def data_storage_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStorageSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTbInput")
    def data_storage_size_tb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStorageSizeTbInput"))

    @builtins.property
    @jsii.member(jsii_name="dbEditionInput")
    def db_edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbEditionInput"))

    @builtins.property
    @jsii.member(jsii_name="dbVersionInput")
    def db_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="dbWorkloadInput")
    def db_workload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbWorkloadInput"))

    @builtins.property
    @jsii.member(jsii_name="isAutoScalingEnabledInput")
    def is_auto_scaling_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isAutoScalingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isStorageAutoScalingEnabledInput")
    def is_storage_auto_scaling_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isStorageAutoScalingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceScheduleTypeInput")
    def maintenance_schedule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceScheduleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mtlsConnectionRequiredInput")
    def mtls_connection_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mtlsConnectionRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="nCharacterSetInput")
    def n_character_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nCharacterSetInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInsightsStateInput")
    def operations_insights_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationsInsightsStateInput"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpointIpInput")
    def private_endpoint_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateEndpointIpInput"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpointLabelInput")
    def private_endpoint_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateEndpointLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriodDays")
    def backup_retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionPeriodDays"))

    @backup_retention_period_days.setter
    def backup_retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd94596eaf46704295625f25c84b7f3da2bbd2d3a600296e373055b2eb653dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="characterSet")
    def character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "characterSet"))

    @character_set.setter
    def character_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e072dbb731ca5cad55fb7f1e683321a593a07d19481cafb936ac50863adf8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "characterSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeCount")
    def compute_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeCount"))

    @compute_count.setter
    def compute_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58b5f5469d5763cffa6a84cea1b7c3fe04ac56aad157a875d1ecd91a126ffcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeGb")
    def data_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeGb"))

    @data_storage_size_gb.setter
    def data_storage_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddd850bf3c56b1e3615aec04b57086263506603149ea08262d4316e157f0127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTb")
    def data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeTb"))

    @data_storage_size_tb.setter
    def data_storage_size_tb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e300153fa51ad59ba6027d1226cb51ccd727b8270997d12b4aecabda7e6a613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeTb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbEdition")
    def db_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbEdition"))

    @db_edition.setter
    def db_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8385434641c59ce5cd89cf67be8f955702bb61e246876bc4f1347060bc5f00dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbEdition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbVersion")
    def db_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbVersion"))

    @db_version.setter
    def db_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887d759d1d15bfa9e59d6dc0c1a900f6481141c348ec2dd168ab8534114af564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbWorkload")
    def db_workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbWorkload"))

    @db_workload.setter
    def db_workload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7786c96913f15ee81919e64257d223d840b35075e26a95578cdbd73ce57475bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbWorkload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isAutoScalingEnabled")
    def is_auto_scaling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isAutoScalingEnabled"))

    @is_auto_scaling_enabled.setter
    def is_auto_scaling_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7a6196869194b75d03762786ea13caaf1890f00e525918169e59be5a533c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isAutoScalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isStorageAutoScalingEnabled")
    def is_storage_auto_scaling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isStorageAutoScalingEnabled"))

    @is_storage_auto_scaling_enabled.setter
    def is_storage_auto_scaling_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c328a626aa9fb03af572efd7deac25f183fd362ccaf62fc799caced9ab333eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isStorageAutoScalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe05df376711563637151b6c9589c131ec8da31c718cccd80f840f089050a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceScheduleType")
    def maintenance_schedule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceScheduleType"))

    @maintenance_schedule_type.setter
    def maintenance_schedule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c8e406c5ef31f0a2b16a00cd5d0c836569374a6b98ff9ff426b97662c666d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceScheduleType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtlsConnectionRequired")
    def mtls_connection_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mtlsConnectionRequired"))

    @mtls_connection_required.setter
    def mtls_connection_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5e2797b73a688059d9acaf0f4417394b2f130a6d171fa09fd29320e40f1c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtlsConnectionRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nCharacterSet")
    def n_character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nCharacterSet"))

    @n_character_set.setter
    def n_character_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca918fcd34f4548b87db5e29c98a74b8566055ba9af13b75231f9733f3a87cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nCharacterSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationsInsightsState")
    def operations_insights_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationsInsightsState"))

    @operations_insights_state.setter
    def operations_insights_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b268decbd09ac54d139a531d48662481d70f407dff33dc37b569172d348ae555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationsInsightsState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateEndpointIp")
    def private_endpoint_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointIp"))

    @private_endpoint_ip.setter
    def private_endpoint_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8916746c5c391af5c7ad74dec5a0a4befa650e12485454430d29848f40019acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateEndpointIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateEndpointLabel")
    def private_endpoint_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointLabel"))

    @private_endpoint_label.setter
    def private_endpoint_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f489b319995d1421fca83ed6730d512ff0706a26f40b3376acb8ff1cd04a5cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateEndpointLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabaseProperties]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabaseProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabaseProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04147fa30d16a69a938fa96dc1abf186a1afaa4ebed41e49a99a5dd6da622c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f230f382d0c4e01b33271630bf068f38c0b94da2cb9885f493841e3919086af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ca899cd96346cd3fef090b48f494bd62d788ce2cef09373b487c0aab12502d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cc792def9c89f68aaf86e0147d42c816fc91016523fcafbebe30e2b12b8001)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccdea0bd6bb19089bcdb4dc546520370611980d599f7e82e31fdd36c4613f197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__005f08015c47f27b8d72c211c4c36f1d1a9353b4e9796303aa2ae989c8fd8c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__839c7d7dab79e27b3419814bb03c8a826aa0a881a175cc5a10f592a88815aa91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList":
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="stopTime")
    def stop_time(
        self,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList":
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList", jsii.get(self, "stopTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeabcad474e8de239538f4a389f0207e2ac8134ffe3a52328c86140ead16c00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bda1c44ce1142bf1bdc52ed2056d11ba914b83b8904375526875e559865334f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e684b8d7664b69d3d632e76870786c3aeac902d6bfe8407560176d89638b3a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5421f5eae56beb434a5aab45bafcfcc9f01e98528941c01baa96138d3c6aaf7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__154c00a3d30cb3c61765beb9cf98ba7a0cc818b72d80094c7156a6e833ab287a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30f356d4bcfed949041e57aa2d856611b35d832bcf19030d7294543433f19923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9367a1d811683216613404645cc2903fae598e94cd132a7f303b3f52503bc6d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9619c9285820b2f30956f6e18e2695334e22f51a6a02e146b5d8ec084bf7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35bbe0e91de6dfae1e39c1e33a4e677a02b27cb6c761d0ec4454a3d0a0b288d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493178328650c8a5e663b574d105bea37abfaef8db325875b5a2cf6be4af1fa8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363b9db4810383f1808a5e6f0acc72198b16692906a90e7a1cea427b9afb690f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b02663a5f1897c5c72432a7fb836fcd0f8a1604ad2f96934af39481deaaaf3e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4739e213eebae791bfe4a78f34b4f1e49902b3b87499f632ba696e8729aac14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2df2cbc12d33720fde9b76229e72f519a9301f8380078cfdb37b3c582d6cfdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4fccacc45fd6d65891c45bc0ac4f8cb28e80e682f037836141cd7804b95133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleOracleDatabaseAutonomousDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#create GoogleOracleDatabaseAutonomousDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#delete GoogleOracleDatabaseAutonomousDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#update GoogleOracleDatabaseAutonomousDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3d817ad942677ba2f5dc58d5681fab00a73e487b94e6f874b5ae5e69dc870d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#create GoogleOracleDatabaseAutonomousDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#delete GoogleOracleDatabaseAutonomousDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_autonomous_database#update GoogleOracleDatabaseAutonomousDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseAutonomousDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseAutonomousDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseAutonomousDatabase.GoogleOracleDatabaseAutonomousDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26bd1f2a6cf5790f0881b4b773173c05bc351d78976715be85ea77f708d4bdf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d43e9281457c8419e32491eff498b12c82a481047c44f7e5acc01b01c9d7753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70edee8d314fcf7772d6202da184da96cbdda5e77173e9ad6e4c7d46198d485d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445d22dec7b6ce46e1ca0f162eb62399ba17b2e31df0dd2d36cf9fa5189954fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72022b4ddbfd6488baecbfafba5bbf8188263538a44066601988d2fd2ea289b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOracleDatabaseAutonomousDatabase",
    "GoogleOracleDatabaseAutonomousDatabaseConfig",
    "GoogleOracleDatabaseAutonomousDatabaseProperties",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList",
    "GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference",
    "GoogleOracleDatabaseAutonomousDatabaseTimeouts",
    "GoogleOracleDatabaseAutonomousDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3df6840c5a346efe5ddde54ed947ea88a715108175451ad89d637e5554fad40b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autonomous_database_id: builtins.str,
    cidr: builtins.str,
    database: builtins.str,
    location: builtins.str,
    network: builtins.str,
    properties: typing.Union[GoogleOracleDatabaseAutonomousDatabaseProperties, typing.Dict[builtins.str, typing.Any]],
    admin_password: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleOracleDatabaseAutonomousDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e76db30ddaf92c0e2960ae38538264d1356bb54a4c99887fb7a50f477e8775b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379b3de4ba90e87589007e8846c7339615e01840a9d1b2a4330ca5247a723651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d136c5fe2d50e0c7c4373ccb510405e9002926260477c494f6b232e39480c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0e3fba230131de426f8af2916756c537665ac15adc040a98d1857d68bb9511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad1c949c6fa9deb4cc4d0209b29f6ac97504c5b73ca27d14d0877b62840bfa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684df4e65410f4aa8a720db1b9e78958d686667e52d8ba53e32ece1537c78313(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63d7599adce77835faf16b8028add82913a80efec317d763ae21aee81e1d778(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bf46dc84e35314fb516b54c99c4a677ac78fa0f93b867fe8bb97f82bcf48ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04fd155e26add47f59d62a85152739837308d738b4a2bd05548ea3100c798495(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1a0aae7f1437ca4c30615e132fda0f3b4ac075f693f8db5f510b4087ebf4e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260ab77e987cdfce3bdc6afb7118453902d58e418c7cbbac92fc5919ed7c18df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780c48dbf731d6f6dccc32a97e70c10235dd5ac1fa8b605d1d73e617eb864dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd56d1144d8a6f7bc5d501b03c78b5344469f0fc9511e122394e53a172d6c7cc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autonomous_database_id: builtins.str,
    cidr: builtins.str,
    database: builtins.str,
    location: builtins.str,
    network: builtins.str,
    properties: typing.Union[GoogleOracleDatabaseAutonomousDatabaseProperties, typing.Dict[builtins.str, typing.Any]],
    admin_password: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleOracleDatabaseAutonomousDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d6674f71eb34cfba0a6f5be7a8f33ebac826b74793b51aab72221dffc16c80(
    *,
    db_workload: builtins.str,
    license_type: builtins.str,
    backup_retention_period_days: typing.Optional[jsii.Number] = None,
    character_set: typing.Optional[builtins.str] = None,
    compute_count: typing.Optional[jsii.Number] = None,
    customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_storage_size_gb: typing.Optional[jsii.Number] = None,
    data_storage_size_tb: typing.Optional[jsii.Number] = None,
    db_edition: typing.Optional[builtins.str] = None,
    db_version: typing.Optional[builtins.str] = None,
    is_auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_storage_auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintenance_schedule_type: typing.Optional[builtins.str] = None,
    mtls_connection_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    n_character_set: typing.Optional[builtins.str] = None,
    operations_insights_state: typing.Optional[builtins.str] = None,
    private_endpoint_ip: typing.Optional[builtins.str] = None,
    private_endpoint_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16465ded872632a23708b5f9c94e1e9d99d2648b0a9b1b184204fe6ceb89f77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8cdfecf15cb6c611fecebf8c770eb9773ffa526c94d7bfaaf8a83ee0887312(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e49e09fd044d151db114520dbb857567eecabe2735f01252c859e3ddf1ba66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaa2f28675b23819f9aa117c6446fedfc6afd2ef89d4a7214e492f7d4f4601c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce1b87b883345f065a2667749c53ddd280e1f38b41e13558268f080a4edadc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218d9bb45e97c15889ed65eeceb8b0412455fc480dbd07a257769db5c06e925d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd846e56a762df843f2ba5dc55f8fa622baa3cd600ba68a07c68aceb234c3c4(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3cbc9c50736ece685f087d36d6b4c7d62d9eb6a680635669eb087e66f906d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25021ddbfe531922f159731b3992b798a4aae7e900aec119727cf273d8c747b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dae74e9bb0580b607997cc69d7e4d2af0883a693c5f81773ab3d12849c3555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2aca666ac78f471e51b1493ec942c85a3798991764ff89e038a54b83a4a08c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a6df4b38616448b54150c8120bce2be988c46f0656b878840692db0cbc417(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0e09863579822561842356e154f977507ab48557e8f01b351a4dd23339184b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8335efa0ded1b2cc2aeb66bceb77572c88ae5f925380dc4a6d1696093310c2f2(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601831023bf7f7bbb4fc21fbdbad04a80c4905fb01e63281bb23f88b961e9b13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98999dceee77f9c76735f9c8bba7779864eea8172f5fe2fa11df9aaddc11dfe1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7e9a32e59c02a726cb2cf4a90e8d6b4fa85bbc961315eddb9a95f1e3592415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa1bb15837216ee80f67741de789f4c567ba88e438653a00409c483773ca428(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9ddbef488c161499325af8cae51a8418749a2de70645dd80cd25a534398980(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe4c05495b19a308f26ca217ed44a7cdb56ad7b9887f8625f164a878ad207d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729fb44449ac82e44a312b7f2164d7482cd49ef93575d1d2ba17835f5740d35e(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b941318744acbd9bc2a9d54d3dc4ec18680f998d3c1c79d8ae73b5aac6834dcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80c15ca010e8479cb8d263101dc07906af7328caa250db15f6ed48e7885e05a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ece19f94e35e584471ffd9d8f4facc1d6adc23677eb164bc607b5053cc490e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2867843ddb03ed3854ecb53d449be40313ec9341bee44b2bca3290abee7778(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ab45e8294d649ca923c3196fc326bd12a7a2a76378d0e7dff17721eae4ca0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8466452f95c820381c8271646319d5140cad6bfff4aa73d25f603d01cb7328(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1ea12f062ff37bedeb235e632aebf6d60de2da8ad2ccfe20cafe65d2faaaa9(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b952df438e10b6e8e98e65e0b12a62b075af04687e60d783a2336c911a9536(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396b25ad9a34a22dbe5f9b42e68622d24bf0c7cccdf52680ab2c2b9402f518b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cf0fbaed21043cc0f7cda178eb6cb604a7334880956f1a28a9a4d3208899c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3213e8f89f89edaf837372d195618c25f1bf230006d359b8e58084ba61a611(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee823dd0b65dd18a3d5dfda8d316e1fd440219497e0c6eb7068da9308ea74c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73098ad8bedf85fe6103ec548d45bd7cc96de720de9f23be4581d13b8f2a47f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d10ccb75f03d844de8de97e8f7ea6597320ea838c7cbd6d79977099a725ffa7(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f517a4625a4ec92093c4858a3b10e415af63da8edbd12f19612d991c26b3a6(
    *,
    email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deaa0629f6a959dfc63ee812d81402ecbc67f225e1de423dc470c693058ebe15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdcf17d559e67af4fbfc5e7991cbc983ee7f4cb9c14dc0c6578d9e9c51e6772(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31053e0bf761a6316e6b1801025f34bc490c1ca7670f1eb1227b0c6abd16b440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad648c1ad0b2602db3f869cb9ced1e37a0a66fbef47e1b5c357aa4ac81c01818(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39a25c8618d924e29e594be875e6d117701c6ba8a75b524df8ea1a132f8b227(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c589472dba983ac6e4f278d4ba8ba7105636bd927238a505c20299ef1cc75cb3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b323a36d43a17e4b584857677d7787d337a79501e08a267320b600272de459c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a210cbe59967bb9fc9094c6f5d99f047b2961360e0fff96d9eb981d7c9407ea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3c1bd46c076267ad0ed4e6a5a0526fb71e13a2ab4a965bcba7d0e05ed5d713(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e6f8d716fc4d3fac68c359e756f79eee62c41413b26e675485fa70b68656a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32697bbc06e2748d5c3f425c2faf7343cc2893d089d795e477f25afabbe11e7d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5588f997a9177fc7286ff39da1e0039cd400166ed168817a1a70053d5a36717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd79cb0f12d8bdf0fdf19618aa5497c59b32282582a0521070e3517f1692eb01(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5dd3972416e00fdb7e95ca709f5bd545360c678a90b76d3b6f0ba5587588805(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163aad53121b84783e74a853a5aa4ed48abd0b9ae8c0f204b51eca0fdaff3224(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc08fa4adf5cb221e131db00e30dce66243482d060c7b3ebc4a1d0ef019ad852(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00247a98775bcd8bdef506e044d240835f0e70a3deac9ca15cb73240d21adfda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a13a7c1c32c46bd2db7f088c8bf5bcf188ec20a634da057f900ed49ceb995b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd94596eaf46704295625f25c84b7f3da2bbd2d3a600296e373055b2eb653dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e072dbb731ca5cad55fb7f1e683321a593a07d19481cafb936ac50863adf8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58b5f5469d5763cffa6a84cea1b7c3fe04ac56aad157a875d1ecd91a126ffcf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddd850bf3c56b1e3615aec04b57086263506603149ea08262d4316e157f0127(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e300153fa51ad59ba6027d1226cb51ccd727b8270997d12b4aecabda7e6a613(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8385434641c59ce5cd89cf67be8f955702bb61e246876bc4f1347060bc5f00dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887d759d1d15bfa9e59d6dc0c1a900f6481141c348ec2dd168ab8534114af564(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7786c96913f15ee81919e64257d223d840b35075e26a95578cdbd73ce57475bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7a6196869194b75d03762786ea13caaf1890f00e525918169e59be5a533c18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c328a626aa9fb03af572efd7deac25f183fd362ccaf62fc799caced9ab333eae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe05df376711563637151b6c9589c131ec8da31c718cccd80f840f089050a41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c8e406c5ef31f0a2b16a00cd5d0c836569374a6b98ff9ff426b97662c666d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5e2797b73a688059d9acaf0f4417394b2f130a6d171fa09fd29320e40f1c9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca918fcd34f4548b87db5e29c98a74b8566055ba9af13b75231f9733f3a87cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b268decbd09ac54d139a531d48662481d70f407dff33dc37b569172d348ae555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8916746c5c391af5c7ad74dec5a0a4befa650e12485454430d29848f40019acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f489b319995d1421fca83ed6730d512ff0706a26f40b3376acb8ff1cd04a5cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04147fa30d16a69a938fa96dc1abf186a1afaa4ebed41e49a99a5dd6da622c80(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabaseProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f230f382d0c4e01b33271630bf068f38c0b94da2cb9885f493841e3919086af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ca899cd96346cd3fef090b48f494bd62d788ce2cef09373b487c0aab12502d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cc792def9c89f68aaf86e0147d42c816fc91016523fcafbebe30e2b12b8001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdea0bd6bb19089bcdb4dc546520370611980d599f7e82e31fdd36c4613f197(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005f08015c47f27b8d72c211c4c36f1d1a9353b4e9796303aa2ae989c8fd8c00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839c7d7dab79e27b3419814bb03c8a826aa0a881a175cc5a10f592a88815aa91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeabcad474e8de239538f4a389f0207e2ac8134ffe3a52328c86140ead16c00f(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bda1c44ce1142bf1bdc52ed2056d11ba914b83b8904375526875e559865334f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e684b8d7664b69d3d632e76870786c3aeac902d6bfe8407560176d89638b3a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5421f5eae56beb434a5aab45bafcfcc9f01e98528941c01baa96138d3c6aaf7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154c00a3d30cb3c61765beb9cf98ba7a0cc818b72d80094c7156a6e833ab287a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f356d4bcfed949041e57aa2d856611b35d832bcf19030d7294543433f19923(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9367a1d811683216613404645cc2903fae598e94cd132a7f303b3f52503bc6d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9619c9285820b2f30956f6e18e2695334e22f51a6a02e146b5d8ec084bf7fd(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bbe0e91de6dfae1e39c1e33a4e677a02b27cb6c761d0ec4454a3d0a0b288d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493178328650c8a5e663b574d105bea37abfaef8db325875b5a2cf6be4af1fa8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363b9db4810383f1808a5e6f0acc72198b16692906a90e7a1cea427b9afb690f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02663a5f1897c5c72432a7fb836fcd0f8a1604ad2f96934af39481deaaaf3e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4739e213eebae791bfe4a78f34b4f1e49902b3b87499f632ba696e8729aac14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2df2cbc12d33720fde9b76229e72f519a9301f8380078cfdb37b3c582d6cfdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4fccacc45fd6d65891c45bc0ac4f8cb28e80e682f037836141cd7804b95133(
    value: typing.Optional[GoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3d817ad942677ba2f5dc58d5681fab00a73e487b94e6f874b5ae5e69dc870d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bd1f2a6cf5790f0881b4b773173c05bc351d78976715be85ea77f708d4bdf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d43e9281457c8419e32491eff498b12c82a481047c44f7e5acc01b01c9d7753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70edee8d314fcf7772d6202da184da96cbdda5e77173e9ad6e4c7d46198d485d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445d22dec7b6ce46e1ca0f162eb62399ba17b2e31df0dd2d36cf9fa5189954fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72022b4ddbfd6488baecbfafba5bbf8188263538a44066601988d2fd2ea289b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseAutonomousDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
