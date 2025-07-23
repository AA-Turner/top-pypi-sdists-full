r'''
# `google_oracle_database_autonomous_database`

Refer to the Terraform Registry for docs: [`google_oracle_database_autonomous_database`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database).
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


class OracleDatabaseAutonomousDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database google_oracle_database_autonomous_database}.'''

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
        properties: typing.Union["OracleDatabaseAutonomousDatabaseProperties", typing.Dict[builtins.str, typing.Any]],
        admin_password: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OracleDatabaseAutonomousDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database google_oracle_database_autonomous_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autonomous_database_id: The ID of the Autonomous Database to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#autonomous_database_id OracleDatabaseAutonomousDatabase#autonomous_database_id}
        :param cidr: The subnet CIDR range for the Autonmous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#cidr OracleDatabaseAutonomousDatabase#cidr}
        :param database: The name of the Autonomous Database. The database name must be unique in the project. The name must begin with a letter and can contain a maximum of 30 alphanumeric characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#database OracleDatabaseAutonomousDatabase#database}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#location OracleDatabaseAutonomousDatabase#location}
        :param network: The name of the VPC network used by the Autonomous Database. Format: projects/{project}/global/networks/{network}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#network OracleDatabaseAutonomousDatabase#network}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#properties OracleDatabaseAutonomousDatabase#properties}
        :param admin_password: The password for the default ADMIN user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#admin_password OracleDatabaseAutonomousDatabase#admin_password}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#deletion_protection OracleDatabaseAutonomousDatabase#deletion_protection}
        :param display_name: The display name for the Autonomous Database. The name does not have to be unique within your project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#display_name OracleDatabaseAutonomousDatabase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#id OracleDatabaseAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels or tags associated with the Autonomous Database. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#labels OracleDatabaseAutonomousDatabase#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#project OracleDatabaseAutonomousDatabase#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#timeouts OracleDatabaseAutonomousDatabase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7efcf65b31f65a12fe5a9f2becbd62daed0f293eb00fceeb63faf5ff6f74508b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OracleDatabaseAutonomousDatabaseConfig(
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
        '''Generates CDKTF code for importing a OracleDatabaseAutonomousDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OracleDatabaseAutonomousDatabase to import.
        :param import_from_id: The id of the existing OracleDatabaseAutonomousDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OracleDatabaseAutonomousDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b648563d89b92bb8503cefa9ff88c3f238ae53033e128dda7d0062f25aa7c2fb)
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
        customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OracleDatabaseAutonomousDatabasePropertiesCustomerContacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param db_workload: Possible values: DB_WORKLOAD_UNSPECIFIED OLTP DW AJD APEX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_workload OracleDatabaseAutonomousDatabase#db_workload}
        :param license_type: The license type used for the Autonomous Database. Possible values: LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#license_type OracleDatabaseAutonomousDatabase#license_type}
        :param backup_retention_period_days: The retention period for the Autonomous Database. This field is specified in days, can range from 1 day to 60 days, and has a default value of 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#backup_retention_period_days OracleDatabaseAutonomousDatabase#backup_retention_period_days}
        :param character_set: The character set for the Autonomous Database. The default is AL32UTF8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#character_set OracleDatabaseAutonomousDatabase#character_set}
        :param compute_count: The number of compute servers for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#compute_count OracleDatabaseAutonomousDatabase#compute_count}
        :param customer_contacts: customer_contacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#customer_contacts OracleDatabaseAutonomousDatabase#customer_contacts}
        :param data_storage_size_gb: The size of the data stored in the database, in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#data_storage_size_gb OracleDatabaseAutonomousDatabase#data_storage_size_gb}
        :param data_storage_size_tb: The size of the data stored in the database, in terabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#data_storage_size_tb OracleDatabaseAutonomousDatabase#data_storage_size_tb}
        :param db_edition: The edition of the Autonomous Databases. Possible values: DATABASE_EDITION_UNSPECIFIED STANDARD_EDITION ENTERPRISE_EDITION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_edition OracleDatabaseAutonomousDatabase#db_edition}
        :param db_version: The Oracle Database version for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_version OracleDatabaseAutonomousDatabase#db_version}
        :param is_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database CPU core count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#is_auto_scaling_enabled OracleDatabaseAutonomousDatabase#is_auto_scaling_enabled}
        :param is_storage_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#is_storage_auto_scaling_enabled OracleDatabaseAutonomousDatabase#is_storage_auto_scaling_enabled}
        :param maintenance_schedule_type: The maintenance schedule of the Autonomous Database. Possible values: MAINTENANCE_SCHEDULE_TYPE_UNSPECIFIED EARLY REGULAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#maintenance_schedule_type OracleDatabaseAutonomousDatabase#maintenance_schedule_type}
        :param mtls_connection_required: This field specifies if the Autonomous Database requires mTLS connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#mtls_connection_required OracleDatabaseAutonomousDatabase#mtls_connection_required}
        :param n_character_set: The national character set for the Autonomous Database. The default is AL16UTF16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#n_character_set OracleDatabaseAutonomousDatabase#n_character_set}
        :param operations_insights_state: Possible values: OPERATIONS_INSIGHTS_STATE_UNSPECIFIED ENABLING ENABLED DISABLING NOT_ENABLED FAILED_ENABLING FAILED_DISABLING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#operations_insights_state OracleDatabaseAutonomousDatabase#operations_insights_state}
        :param private_endpoint_ip: The private endpoint IP address for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#private_endpoint_ip OracleDatabaseAutonomousDatabase#private_endpoint_ip}
        :param private_endpoint_label: The private endpoint label for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#private_endpoint_label OracleDatabaseAutonomousDatabase#private_endpoint_label}
        '''
        value = OracleDatabaseAutonomousDatabaseProperties(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#create OracleDatabaseAutonomousDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#delete OracleDatabaseAutonomousDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#update OracleDatabaseAutonomousDatabase#update}.
        '''
        value = OracleDatabaseAutonomousDatabaseTimeouts(
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
    def properties(self) -> "OracleDatabaseAutonomousDatabasePropertiesOutputReference":
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OracleDatabaseAutonomousDatabaseTimeoutsOutputReference":
        return typing.cast("OracleDatabaseAutonomousDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["OracleDatabaseAutonomousDatabaseProperties"]:
        return typing.cast(typing.Optional["OracleDatabaseAutonomousDatabaseProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OracleDatabaseAutonomousDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OracleDatabaseAutonomousDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5688eab259b2d0056de0fc846bcb4c9bc0535c86f726048dc8039a5ace4579fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autonomousDatabaseId")
    def autonomous_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autonomousDatabaseId"))

    @autonomous_database_id.setter
    def autonomous_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07691ece5e8e039498f4738389ac2dc29c53724f453300e1da13fb959d94cd2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autonomousDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @cidr.setter
    def cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ce7404411545f944ab01cca0bcd7c333843ea8ae625169c62e94a31bade9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660a9a15c6ef822abbc0bcdbb4147b5cff1a4b479688f8cd5a0d2b0746ef8ca3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb482eb30a86446643f44b4cbfecfa15e8d280d3e13beaf6c370d266a0ad294f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6969194d781a454a1be164eda8e5d15a4d85f06e55605aa950577a464d2fc3db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9ce2b6ae1da1fa73474fdf05d77d96b47929b811d94f8ec0e4a767e978ca35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8487c049bed9ffb5a43cff96a15300347d3b70c90e1b264fa4ec2f9976bb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c884f746af22f48e83b9e6acd9ba2498b58847f41263eab17c1a45bc1c4f9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a946ea6962e77924518b465b02589306e28d63a240e4099fd2965c66c4db891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e344ea4b08718e8390f2c19900620e69cb9835a4699303da6eb2dffa0dd8a21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabaseConfig",
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
class OracleDatabaseAutonomousDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        properties: typing.Union["OracleDatabaseAutonomousDatabaseProperties", typing.Dict[builtins.str, typing.Any]],
        admin_password: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OracleDatabaseAutonomousDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autonomous_database_id: The ID of the Autonomous Database to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#autonomous_database_id OracleDatabaseAutonomousDatabase#autonomous_database_id}
        :param cidr: The subnet CIDR range for the Autonmous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#cidr OracleDatabaseAutonomousDatabase#cidr}
        :param database: The name of the Autonomous Database. The database name must be unique in the project. The name must begin with a letter and can contain a maximum of 30 alphanumeric characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#database OracleDatabaseAutonomousDatabase#database}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#location OracleDatabaseAutonomousDatabase#location}
        :param network: The name of the VPC network used by the Autonomous Database. Format: projects/{project}/global/networks/{network}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#network OracleDatabaseAutonomousDatabase#network}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#properties OracleDatabaseAutonomousDatabase#properties}
        :param admin_password: The password for the default ADMIN user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#admin_password OracleDatabaseAutonomousDatabase#admin_password}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#deletion_protection OracleDatabaseAutonomousDatabase#deletion_protection}
        :param display_name: The display name for the Autonomous Database. The name does not have to be unique within your project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#display_name OracleDatabaseAutonomousDatabase#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#id OracleDatabaseAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels or tags associated with the Autonomous Database. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#labels OracleDatabaseAutonomousDatabase#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#project OracleDatabaseAutonomousDatabase#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#timeouts OracleDatabaseAutonomousDatabase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = OracleDatabaseAutonomousDatabaseProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = OracleDatabaseAutonomousDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f29a7687b62a3235eae40c1e9ce139da7bbf885adaf0beadd047a704bdd23a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#autonomous_database_id OracleDatabaseAutonomousDatabase#autonomous_database_id}
        '''
        result = self._values.get("autonomous_database_id")
        assert result is not None, "Required property 'autonomous_database_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr(self) -> builtins.str:
        '''The subnet CIDR range for the Autonmous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#cidr OracleDatabaseAutonomousDatabase#cidr}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#database OracleDatabaseAutonomousDatabase#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#location OracleDatabaseAutonomousDatabase#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The name of the VPC network used by the Autonomous Database. Format: projects/{project}/global/networks/{network}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#network OracleDatabaseAutonomousDatabase#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def properties(self) -> "OracleDatabaseAutonomousDatabaseProperties":
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#properties OracleDatabaseAutonomousDatabase#properties}
        '''
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast("OracleDatabaseAutonomousDatabaseProperties", result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''The password for the default ADMIN user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#admin_password OracleDatabaseAutonomousDatabase#admin_password}
        '''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to allow Terraform to destroy the instance.

        Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#deletion_protection OracleDatabaseAutonomousDatabase#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for the Autonomous Database. The name does not have to be unique within your project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#display_name OracleDatabaseAutonomousDatabase#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#id OracleDatabaseAutonomousDatabase#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#labels OracleDatabaseAutonomousDatabase#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#project OracleDatabaseAutonomousDatabase#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OracleDatabaseAutonomousDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#timeouts OracleDatabaseAutonomousDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OracleDatabaseAutonomousDatabaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabaseProperties",
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
class OracleDatabaseAutonomousDatabaseProperties:
    def __init__(
        self,
        *,
        db_workload: builtins.str,
        license_type: builtins.str,
        backup_retention_period_days: typing.Optional[jsii.Number] = None,
        character_set: typing.Optional[builtins.str] = None,
        compute_count: typing.Optional[jsii.Number] = None,
        customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OracleDatabaseAutonomousDatabasePropertiesCustomerContacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param db_workload: Possible values: DB_WORKLOAD_UNSPECIFIED OLTP DW AJD APEX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_workload OracleDatabaseAutonomousDatabase#db_workload}
        :param license_type: The license type used for the Autonomous Database. Possible values: LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#license_type OracleDatabaseAutonomousDatabase#license_type}
        :param backup_retention_period_days: The retention period for the Autonomous Database. This field is specified in days, can range from 1 day to 60 days, and has a default value of 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#backup_retention_period_days OracleDatabaseAutonomousDatabase#backup_retention_period_days}
        :param character_set: The character set for the Autonomous Database. The default is AL32UTF8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#character_set OracleDatabaseAutonomousDatabase#character_set}
        :param compute_count: The number of compute servers for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#compute_count OracleDatabaseAutonomousDatabase#compute_count}
        :param customer_contacts: customer_contacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#customer_contacts OracleDatabaseAutonomousDatabase#customer_contacts}
        :param data_storage_size_gb: The size of the data stored in the database, in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#data_storage_size_gb OracleDatabaseAutonomousDatabase#data_storage_size_gb}
        :param data_storage_size_tb: The size of the data stored in the database, in terabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#data_storage_size_tb OracleDatabaseAutonomousDatabase#data_storage_size_tb}
        :param db_edition: The edition of the Autonomous Databases. Possible values: DATABASE_EDITION_UNSPECIFIED STANDARD_EDITION ENTERPRISE_EDITION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_edition OracleDatabaseAutonomousDatabase#db_edition}
        :param db_version: The Oracle Database version for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_version OracleDatabaseAutonomousDatabase#db_version}
        :param is_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database CPU core count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#is_auto_scaling_enabled OracleDatabaseAutonomousDatabase#is_auto_scaling_enabled}
        :param is_storage_auto_scaling_enabled: This field indicates if auto scaling is enabled for the Autonomous Database storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#is_storage_auto_scaling_enabled OracleDatabaseAutonomousDatabase#is_storage_auto_scaling_enabled}
        :param maintenance_schedule_type: The maintenance schedule of the Autonomous Database. Possible values: MAINTENANCE_SCHEDULE_TYPE_UNSPECIFIED EARLY REGULAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#maintenance_schedule_type OracleDatabaseAutonomousDatabase#maintenance_schedule_type}
        :param mtls_connection_required: This field specifies if the Autonomous Database requires mTLS connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#mtls_connection_required OracleDatabaseAutonomousDatabase#mtls_connection_required}
        :param n_character_set: The national character set for the Autonomous Database. The default is AL16UTF16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#n_character_set OracleDatabaseAutonomousDatabase#n_character_set}
        :param operations_insights_state: Possible values: OPERATIONS_INSIGHTS_STATE_UNSPECIFIED ENABLING ENABLED DISABLING NOT_ENABLED FAILED_ENABLING FAILED_DISABLING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#operations_insights_state OracleDatabaseAutonomousDatabase#operations_insights_state}
        :param private_endpoint_ip: The private endpoint IP address for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#private_endpoint_ip OracleDatabaseAutonomousDatabase#private_endpoint_ip}
        :param private_endpoint_label: The private endpoint label for the Autonomous Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#private_endpoint_label OracleDatabaseAutonomousDatabase#private_endpoint_label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38281d19f7cdac48260a8abe683f8f6fe34da3269926e34c5e17b98e273dea2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_workload OracleDatabaseAutonomousDatabase#db_workload}
        '''
        result = self._values.get("db_workload")
        assert result is not None, "Required property 'db_workload' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_type(self) -> builtins.str:
        '''The license type used for the Autonomous Database.   Possible values:  LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#license_type OracleDatabaseAutonomousDatabase#license_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#backup_retention_period_days OracleDatabaseAutonomousDatabase#backup_retention_period_days}
        '''
        result = self._values.get("backup_retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def character_set(self) -> typing.Optional[builtins.str]:
        '''The character set for the Autonomous Database. The default is AL32UTF8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#character_set OracleDatabaseAutonomousDatabase#character_set}
        '''
        result = self._values.get("character_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_count(self) -> typing.Optional[jsii.Number]:
        '''The number of compute servers for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#compute_count OracleDatabaseAutonomousDatabase#compute_count}
        '''
        result = self._values.get("compute_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customer_contacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OracleDatabaseAutonomousDatabasePropertiesCustomerContacts"]]]:
        '''customer_contacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#customer_contacts OracleDatabaseAutonomousDatabase#customer_contacts}
        '''
        result = self._values.get("customer_contacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OracleDatabaseAutonomousDatabasePropertiesCustomerContacts"]]], result)

    @builtins.property
    def data_storage_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the data stored in the database, in gigabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#data_storage_size_gb OracleDatabaseAutonomousDatabase#data_storage_size_gb}
        '''
        result = self._values.get("data_storage_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_storage_size_tb(self) -> typing.Optional[jsii.Number]:
        '''The size of the data stored in the database, in terabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#data_storage_size_tb OracleDatabaseAutonomousDatabase#data_storage_size_tb}
        '''
        result = self._values.get("data_storage_size_tb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_edition(self) -> typing.Optional[builtins.str]:
        '''The edition of the Autonomous Databases.   Possible values:  DATABASE_EDITION_UNSPECIFIED STANDARD_EDITION ENTERPRISE_EDITION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_edition OracleDatabaseAutonomousDatabase#db_edition}
        '''
        result = self._values.get("db_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_version(self) -> typing.Optional[builtins.str]:
        '''The Oracle Database version for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#db_version OracleDatabaseAutonomousDatabase#db_version}
        '''
        result = self._values.get("db_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_auto_scaling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field indicates if auto scaling is enabled for the Autonomous Database CPU core count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#is_auto_scaling_enabled OracleDatabaseAutonomousDatabase#is_auto_scaling_enabled}
        '''
        result = self._values.get("is_auto_scaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_storage_auto_scaling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field indicates if auto scaling is enabled for the Autonomous Database storage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#is_storage_auto_scaling_enabled OracleDatabaseAutonomousDatabase#is_storage_auto_scaling_enabled}
        '''
        result = self._values.get("is_storage_auto_scaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maintenance_schedule_type(self) -> typing.Optional[builtins.str]:
        '''The maintenance schedule of the Autonomous Database.   Possible values:  MAINTENANCE_SCHEDULE_TYPE_UNSPECIFIED EARLY REGULAR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#maintenance_schedule_type OracleDatabaseAutonomousDatabase#maintenance_schedule_type}
        '''
        result = self._values.get("maintenance_schedule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtls_connection_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field specifies if the Autonomous Database requires mTLS connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#mtls_connection_required OracleDatabaseAutonomousDatabase#mtls_connection_required}
        '''
        result = self._values.get("mtls_connection_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def n_character_set(self) -> typing.Optional[builtins.str]:
        '''The national character set for the Autonomous Database. The default is AL16UTF16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#n_character_set OracleDatabaseAutonomousDatabase#n_character_set}
        '''
        result = self._values.get("n_character_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations_insights_state(self) -> typing.Optional[builtins.str]:
        '''Possible values:  OPERATIONS_INSIGHTS_STATE_UNSPECIFIED ENABLING ENABLED DISABLING NOT_ENABLED FAILED_ENABLING FAILED_DISABLING.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#operations_insights_state OracleDatabaseAutonomousDatabase#operations_insights_state}
        '''
        result = self._values.get("operations_insights_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_endpoint_ip(self) -> typing.Optional[builtins.str]:
        '''The private endpoint IP address for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#private_endpoint_ip OracleDatabaseAutonomousDatabase#private_endpoint_ip}
        '''
        result = self._values.get("private_endpoint_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_endpoint_label(self) -> typing.Optional[builtins.str]:
        '''The private endpoint label for the Autonomous Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#private_endpoint_label OracleDatabaseAutonomousDatabase#private_endpoint_label}
        '''
        result = self._values.get("private_endpoint_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabaseProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesApexDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesApexDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesApexDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesApexDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesApexDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__929f45df1e48d1af4477dd014433cb7590eee83467160566e0293d7e247a3917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d898ccaa7331be2e4606f7c74111ad39ffd4288fb7213082293a89f811db2cfd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bb13a7c079dad82f8aef46417249f977de62b679c9ab631084d81873ace648)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f89940a831b836b0c950a5d652104905506ca5f43c514eff42923e5216bfcc81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__358202af8f7328a05dd2411b8c6e44ff71d3edf6ebd181e7f28ddbc2f93014f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeaea8483b770b1e26a76d679be535d1b12a1fad096dbcea3702105cc2aa768e)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesApexDetails]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesApexDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesApexDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d46125506d2e66f7ced8b6c93c407efeaf7d76c06cf22c75bd497de93d68064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcfd3a6a4f3ace994993f38848c0fa0a462e1c3f04f9fab0612bf5604ae00748)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f4c53cfd3da3cfdd9275e2353d0d20d3d0ecfd6aa3a9cefdc9c6c3a0c0a9ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691836245dcf653d6e05de040dcc16e2889976072ceb04b417256d3d755a5dbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66f7e99e4c6c521f4fa7a6afe50b2c2a809c92b84298ba3a27ea5f89625023e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aa6fe312faaa0c972baecf3822b9ca1de5ef68ba26893b9749e4aee583a4964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5ed763a1363985c30725725830e31fd93aa00b838d137dc54f4d0bcfd7fdf2)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e2296ff27e43c980e1747de6fb098002db31629ec0a23f0c7effbfe150246f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3152db093a066ce9fe737fe6b4c361d526100c58414797e681e06162dd7fc46c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a3160515d3e3c153a50a37f463c76d83c918c8834fd9ed6dbd4bf7cae092a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b643ae88b663a47eb0b8d997188802bf82292edab09ce4199ef480db3b2ed0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23215bea6bdbcf11b4f3d2768c586aef55d46afefd833e7e6c744e5157da81c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7595ea8f3efdbab0712ffd3272552051e160f4ec4003617dc9a21c6c34d42d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9090e86dd96c4d4938c64e7a1db6c5e41655dab464d922d67b622763b66caffd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allConnectionStrings")
    def all_connection_strings(
        self,
    ) -> OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList:
        return typing.cast(OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList, jsii.get(self, "allConnectionStrings"))

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
    ) -> "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList":
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList", jsii.get(self, "profiles"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStrings]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ff05bd3148e68b58b96065fe134cc184aaad3ee3144eb16c147c239f04db57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a98ba0b0292a4ded862a06b069678c7bb3db70b09e332f26751d46c296e960d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6836cf57be60ca9a586c387f23dbcc5368dccc8b46d9fec1be4a1123815fc488)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3ef1168ace736784f3faa0fca61fb8aa6b5d96d7ce5b3b4c590a509741e4fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc1ac2626fa5dab8e0b82abd433b15c9de79cd77dde43dc06a2ee25689e011b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43bf26611d785f929447f08242ee86419f66bee90608d431ae7bf05c34c6b2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43463b722569ef89e1474b4f19ecd9085e36b2e044652d31ceda4d7560fa434d)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ac78165acaa2dc0ca7403c1e54135249595694f6f6252e7b28f5d96c6b6022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionUrls",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesConnectionUrls:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesConnectionUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2d35ecff1ca3e9355ddf542f59f2ae22812cfeb9c92eae2e04f795817d90b75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebc9b5483747eda4bc44ed4a12588d70b6deba039efaf6bbaa6e1c4d000e7f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7140b8fed8d1f270b3049e7432d2777d0bd09c8caa46b218229508bf7a794b07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f394b2e2694e48e3c8f9f2eac8d2f66ac2f094f0c13a8298922e17f6cb42426)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e802a2319ff8893e312c67642cbcfd976a266f88f6d69782dfd814027b25b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__316d992059065e246da6194118428f012f34e3ce520d59ce76ad3f3ae62b1ef5)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionUrls]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c09cc99d5eb39280979c05bcbce1589ddc39dc4d8689759374cc0601e8fb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesCustomerContacts",
    jsii_struct_bases=[],
    name_mapping={"email": "email"},
)
class OracleDatabaseAutonomousDatabasePropertiesCustomerContacts:
    def __init__(self, *, email: builtins.str) -> None:
        '''
        :param email: The email address used by Oracle to send notifications regarding databases and infrastructure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#email OracleDatabaseAutonomousDatabase#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75afcd8f31884e718a1f9423bb04c068d325ea5595b8a6ad56631b76ec4b639)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }

    @builtins.property
    def email(self) -> builtins.str:
        '''The email address used by Oracle to send notifications regarding databases and infrastructure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#email OracleDatabaseAutonomousDatabase#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesCustomerContacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesCustomerContactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesCustomerContactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__425f6d8bdb97fdace5590a9d423d86d53029259e163951cfa76d8e88c534e184)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d628d5347f816bd1e57f41d0c4b2434a0db82a7c6814af195c84f394968a415)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c532d3602e19b744603b4786446680c9096ca857989aacecf7f654ea4a8ca43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3739dc73beb67f501d22e509db09b9566e49e52d33498e4c85d03f4cbf451d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96f11be3f1f90d7b447f66ce831096f1aedfe8deb2c3c4d29d8209f64c6eb45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f586224a91f0694db68ffaf6826a5725742db70471cf5cff7a60346d3f8eb5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__378fea50e23d2b1c0fa03f0ad05732cf83acd5545833757e12fff09f65965ac4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d80430799194599f895bc2abfc8bbaec114d12818dca1ee455ee21e899e5175f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016bc4faaf81588d7bb1d7a3369ada19daddd6bb8099212c4aa768121e7ddd77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b1e5953943a0401384ff56630b3fdc429be699cca6697da71a50939803532d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382bd8c98fbff611f63e193d629805a7bb33f69fd2dfb89f3f5c220b8288f1ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2451937886ffa57b1c1fcb1493178390dde873a0b64ad1f7558b4c834baa0276)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f562d7aa56d1e236c10f35117cee71f66649918c437e2c3f1821c97dfa6858)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdaef7a2b0a169fbaf5edbc64103101b9b55f83b5dddc186f4cbe835c07e3d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d62c7c5c6c7dea37158c5d199d186b09fe5af0f7b5186cf6f61a374506f9a6a)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe999c6c2e3cf20d50cfa8dc45740bb772d687f4c51f2bdd3aeeac67b9df2006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835f7678f86141be929f2bd4fee8f5939fbc275268a94c8139efc95dc82ab82f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerContacts")
    def put_customer_contacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c469d282ed3ee34e313b230833acdfa33e0f2a623b0040193b3fbeed36f4761f)
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
    def apex_details(self) -> OracleDatabaseAutonomousDatabasePropertiesApexDetailsList:
        return typing.cast(OracleDatabaseAutonomousDatabasePropertiesApexDetailsList, jsii.get(self, "apexDetails"))

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
    ) -> OracleDatabaseAutonomousDatabasePropertiesConnectionStringsList:
        return typing.cast(OracleDatabaseAutonomousDatabasePropertiesConnectionStringsList, jsii.get(self, "connectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrls")
    def connection_urls(
        self,
    ) -> OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList:
        return typing.cast(OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList, jsii.get(self, "connectionUrls"))

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(
        self,
    ) -> OracleDatabaseAutonomousDatabasePropertiesCustomerContactsList:
        return typing.cast(OracleDatabaseAutonomousDatabasePropertiesCustomerContactsList, jsii.get(self, "customerContacts"))

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
    ) -> OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList:
        return typing.cast(OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList, jsii.get(self, "localStandbyDb"))

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
    ) -> "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList":
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList", jsii.get(self, "scheduledOperationDetails"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]], jsii.get(self, "customerContactsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__841c84449a3cb3b199495a950362e6d123ffc2f6617e175c9bcaa67d533655bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="characterSet")
    def character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "characterSet"))

    @character_set.setter
    def character_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4affcf90c03e3597b2c296bc7fa693795a2357d1c31fdfac3dd5b6594b371a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "characterSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeCount")
    def compute_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeCount"))

    @compute_count.setter
    def compute_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6041459e38bd66eb6d633c5a3175e7a397ef475b3b7f39330f01f991ef6e580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeGb")
    def data_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeGb"))

    @data_storage_size_gb.setter
    def data_storage_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185c8771ed28b5d33dad977a003b9489648940489866be6c22916bd784ded1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTb")
    def data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeTb"))

    @data_storage_size_tb.setter
    def data_storage_size_tb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77af7fdf337ce591579870166fb91c01b755c3747f2f9febeb067b429fd670df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeTb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbEdition")
    def db_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbEdition"))

    @db_edition.setter
    def db_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f14753fbb672c0c443262ca09629d87cc2d381e50c7dd0a18d6d586dee5c2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbEdition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbVersion")
    def db_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbVersion"))

    @db_version.setter
    def db_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2bbf7f48c35d6981aebe5b4b844f9e6c97899064941ec517d231670f86231a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbWorkload")
    def db_workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbWorkload"))

    @db_workload.setter
    def db_workload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8cebaa8c172597cbe5a2064486c11a7bee2cd5597374e8dfea4f364ba21a84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b351d249c5c6c074451e09154090e25703141099d2be947595ac4dc66c483f21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e81649a74b4d5f13f4e2d55932e0c390a4fe1179ca30071d3395d861fec1fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isStorageAutoScalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138e57df052f432e599f6a7d73930969ce537029dba3c577220273d448fbda9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceScheduleType")
    def maintenance_schedule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceScheduleType"))

    @maintenance_schedule_type.setter
    def maintenance_schedule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecd45086ea432a8d0cced06106148dff8d066a8b96fae2c8cd3d6279eb4c8fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__926e32c5aa49ba967eedde315bc9769d830b3cc337596c95677a9fb3d66603eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtlsConnectionRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nCharacterSet")
    def n_character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nCharacterSet"))

    @n_character_set.setter
    def n_character_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfbf52575acbc1f5b96e30c2b04a4013958b4bfabd5f2167c196045c0826d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nCharacterSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationsInsightsState")
    def operations_insights_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationsInsightsState"))

    @operations_insights_state.setter
    def operations_insights_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f49fa2aed3221880d9fa9f8ad59a22156d5f1007d34dcd9edcf6df1c170031a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationsInsightsState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateEndpointIp")
    def private_endpoint_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointIp"))

    @private_endpoint_ip.setter
    def private_endpoint_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c605b1d4b649e254bfb22baba697ebd60096ec5f75d1efbce3b945c06adbf5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateEndpointIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateEndpointLabel")
    def private_endpoint_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointLabel"))

    @private_endpoint_label.setter
    def private_endpoint_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7a7bc4138e53f371807b24f11a3098bd1da359231b84a5c39cb65827c0a00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateEndpointLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OracleDatabaseAutonomousDatabaseProperties]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabaseProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabaseProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20707eec19060f5e21b825cf2b94fc69decac1d2972633c2843f366218d2bf17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a85594be3d5b3c4163424813d9539ee5755e45f6ba2476636fa148d3d71964ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a31880db842ae3281d8b1ce1837e06c6df6ae84afcc2bcbbd2d9fc399e536c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992a9ed454f38c23d20eb7eacb30659929fac660b8e285594fdc92137884b43c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66c9bf31f5bf0d3c3ce71b7d9ac9f8906e584f8dcf39ec7bd0b8118789195cd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c950cefaf369a85ecb734148877326a6c25a1b3be27b780adae9d9c2f65714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68b2f374c0261a09974834a5e6007e00e0332105b14d34f984a160286bc66aad)
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
    ) -> "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList":
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="stopTime")
    def stop_time(
        self,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList":
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList", jsii.get(self, "stopTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e4d0a08f64f1086da4044905bd0c2a02a979d5de3f1ba7ca24da4040805f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__145e7825a71436f6567812c9f9a5491af1c70cd6eac4d15ccf305659152836ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7305c3cedaf0dd8eb46dc4da11134d830bb8e76d6399cf2d6b89e8f61eecd02e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae63ec1f8969083046b1655bc4830933c329ab3c453fccc07291ac88b346e1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f077cd0ef2d06fdd304a49e0783789e4879273cda83f79c69f055b78af1550cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bff6fcb91659d1fb5ddd13d038c299d6493310b35a62150ca6bab5121dad3eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5531ff4731de869b6cd3daac6c93847c8d553fbd2c9c49b4c162107b0e40662d)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6bc38fd3e7ba40efefd6936f1fe8d9e5950ded2450f36cab4d24390e7ec6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baa810a9b39d3e445ad1f29bc2504cecbb8c5645b5d4679923ca3f85da3ef739)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f4b55b0798a0060bf1c91a4a1894275ac4708bae6cd5bf42df3e72ba311ed3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4462838782281c35375162198b93cd365435482aeb96a6064354ecd3441d7e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b0c85adf6e548b4d493d6e06e35bf33a1ef89712676412d66462f34372610a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__028c6982f5c185627d50939a01ff01957a9be70e24eba88a6ea144dc5f36cc99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3761d810591074115c7ddba6080c372155e6e052ab18c5c4d71c6d5a210ee7a7)
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
    ) -> typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime]:
        return typing.cast(typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac991a9120bc04baa6f224b356b6aa7e0341bf152d2114769ed2332120ceb49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OracleDatabaseAutonomousDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#create OracleDatabaseAutonomousDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#delete OracleDatabaseAutonomousDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#update OracleDatabaseAutonomousDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d45d970ef7d350cc0609e01dcc82e5107b41b536d4dbe4e3dd2060e9b983b3f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#create OracleDatabaseAutonomousDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#delete OracleDatabaseAutonomousDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/oracle_database_autonomous_database#update OracleDatabaseAutonomousDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleDatabaseAutonomousDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleDatabaseAutonomousDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.oracleDatabaseAutonomousDatabase.OracleDatabaseAutonomousDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f0dcecf18a3f8c197677b74f7bfd64255cd2629d3da8e30c910b3bfa5308757)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7e3da0065ef850d4645c37e07ab6c1611bbc69f732a98bc286d5f9a258db452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f605852128e9d2a86223eb3e4ff45abf303140b40af897666b11db207fe293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74d82efdd0d841da9765b559768ed03b65ec8f91f6e38c3fdaecd88baa05b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823c94b249399628492ae630462b6a5c937dcd21c7f04a0bbf0c068a4e4912c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OracleDatabaseAutonomousDatabase",
    "OracleDatabaseAutonomousDatabaseConfig",
    "OracleDatabaseAutonomousDatabaseProperties",
    "OracleDatabaseAutonomousDatabasePropertiesApexDetails",
    "OracleDatabaseAutonomousDatabasePropertiesApexDetailsList",
    "OracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStrings",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsList",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionUrls",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList",
    "OracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesCustomerContacts",
    "OracleDatabaseAutonomousDatabasePropertiesCustomerContactsList",
    "OracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb",
    "OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList",
    "OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList",
    "OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference",
    "OracleDatabaseAutonomousDatabaseTimeouts",
    "OracleDatabaseAutonomousDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7efcf65b31f65a12fe5a9f2becbd62daed0f293eb00fceeb63faf5ff6f74508b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autonomous_database_id: builtins.str,
    cidr: builtins.str,
    database: builtins.str,
    location: builtins.str,
    network: builtins.str,
    properties: typing.Union[OracleDatabaseAutonomousDatabaseProperties, typing.Dict[builtins.str, typing.Any]],
    admin_password: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OracleDatabaseAutonomousDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b648563d89b92bb8503cefa9ff88c3f238ae53033e128dda7d0062f25aa7c2fb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5688eab259b2d0056de0fc846bcb4c9bc0535c86f726048dc8039a5ace4579fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07691ece5e8e039498f4738389ac2dc29c53724f453300e1da13fb959d94cd2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ce7404411545f944ab01cca0bcd7c333843ea8ae625169c62e94a31bade9b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660a9a15c6ef822abbc0bcdbb4147b5cff1a4b479688f8cd5a0d2b0746ef8ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb482eb30a86446643f44b4cbfecfa15e8d280d3e13beaf6c370d266a0ad294f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6969194d781a454a1be164eda8e5d15a4d85f06e55605aa950577a464d2fc3db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9ce2b6ae1da1fa73474fdf05d77d96b47929b811d94f8ec0e4a767e978ca35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8487c049bed9ffb5a43cff96a15300347d3b70c90e1b264fa4ec2f9976bb53(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c884f746af22f48e83b9e6acd9ba2498b58847f41263eab17c1a45bc1c4f9cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a946ea6962e77924518b465b02589306e28d63a240e4099fd2965c66c4db891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e344ea4b08718e8390f2c19900620e69cb9835a4699303da6eb2dffa0dd8a21f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f29a7687b62a3235eae40c1e9ce139da7bbf885adaf0beadd047a704bdd23a(
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
    properties: typing.Union[OracleDatabaseAutonomousDatabaseProperties, typing.Dict[builtins.str, typing.Any]],
    admin_password: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OracleDatabaseAutonomousDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38281d19f7cdac48260a8abe683f8f6fe34da3269926e34c5e17b98e273dea2(
    *,
    db_workload: builtins.str,
    license_type: builtins.str,
    backup_retention_period_days: typing.Optional[jsii.Number] = None,
    character_set: typing.Optional[builtins.str] = None,
    compute_count: typing.Optional[jsii.Number] = None,
    customer_contacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__929f45df1e48d1af4477dd014433cb7590eee83467160566e0293d7e247a3917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d898ccaa7331be2e4606f7c74111ad39ffd4288fb7213082293a89f811db2cfd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bb13a7c079dad82f8aef46417249f977de62b679c9ab631084d81873ace648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89940a831b836b0c950a5d652104905506ca5f43c514eff42923e5216bfcc81(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358202af8f7328a05dd2411b8c6e44ff71d3edf6ebd181e7f28ddbc2f93014f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeaea8483b770b1e26a76d679be535d1b12a1fad096dbcea3702105cc2aa768e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d46125506d2e66f7ced8b6c93c407efeaf7d76c06cf22c75bd497de93d68064(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesApexDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfd3a6a4f3ace994993f38848c0fa0a462e1c3f04f9fab0612bf5604ae00748(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f4c53cfd3da3cfdd9275e2353d0d20d3d0ecfd6aa3a9cefdc9c6c3a0c0a9ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691836245dcf653d6e05de040dcc16e2889976072ceb04b417256d3d755a5dbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f7e99e4c6c521f4fa7a6afe50b2c2a809c92b84298ba3a27ea5f89625023e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa6fe312faaa0c972baecf3822b9ca1de5ef68ba26893b9749e4aee583a4964(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5ed763a1363985c30725725830e31fd93aa00b838d137dc54f4d0bcfd7fdf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e2296ff27e43c980e1747de6fb098002db31629ec0a23f0c7effbfe150246f(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3152db093a066ce9fe737fe6b4c361d526100c58414797e681e06162dd7fc46c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a3160515d3e3c153a50a37f463c76d83c918c8834fd9ed6dbd4bf7cae092a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b643ae88b663a47eb0b8d997188802bf82292edab09ce4199ef480db3b2ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23215bea6bdbcf11b4f3d2768c586aef55d46afefd833e7e6c744e5157da81c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7595ea8f3efdbab0712ffd3272552051e160f4ec4003617dc9a21c6c34d42d39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9090e86dd96c4d4938c64e7a1db6c5e41655dab464d922d67b622763b66caffd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ff05bd3148e68b58b96065fe134cc184aaad3ee3144eb16c147c239f04db57(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98ba0b0292a4ded862a06b069678c7bb3db70b09e332f26751d46c296e960d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6836cf57be60ca9a586c387f23dbcc5368dccc8b46d9fec1be4a1123815fc488(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3ef1168ace736784f3faa0fca61fb8aa6b5d96d7ce5b3b4c590a509741e4fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1ac2626fa5dab8e0b82abd433b15c9de79cd77dde43dc06a2ee25689e011b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bf26611d785f929447f08242ee86419f66bee90608d431ae7bf05c34c6b2a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43463b722569ef89e1474b4f19ecd9085e36b2e044652d31ceda4d7560fa434d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ac78165acaa2dc0ca7403c1e54135249595694f6f6252e7b28f5d96c6b6022(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d35ecff1ca3e9355ddf542f59f2ae22812cfeb9c92eae2e04f795817d90b75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebc9b5483747eda4bc44ed4a12588d70b6deba039efaf6bbaa6e1c4d000e7f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7140b8fed8d1f270b3049e7432d2777d0bd09c8caa46b218229508bf7a794b07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f394b2e2694e48e3c8f9f2eac8d2f66ac2f094f0c13a8298922e17f6cb42426(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e802a2319ff8893e312c67642cbcfd976a266f88f6d69782dfd814027b25b81(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316d992059065e246da6194118428f012f34e3ce520d59ce76ad3f3ae62b1ef5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c09cc99d5eb39280979c05bcbce1589ddc39dc4d8689759374cc0601e8fb36(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesConnectionUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75afcd8f31884e718a1f9423bb04c068d325ea5595b8a6ad56631b76ec4b639(
    *,
    email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425f6d8bdb97fdace5590a9d423d86d53029259e163951cfa76d8e88c534e184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d628d5347f816bd1e57f41d0c4b2434a0db82a7c6814af195c84f394968a415(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c532d3602e19b744603b4786446680c9096ca857989aacecf7f654ea4a8ca43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3739dc73beb67f501d22e509db09b9566e49e52d33498e4c85d03f4cbf451d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f11be3f1f90d7b447f66ce831096f1aedfe8deb2c3c4d29d8209f64c6eb45e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f586224a91f0694db68ffaf6826a5725742db70471cf5cff7a60346d3f8eb5b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378fea50e23d2b1c0fa03f0ad05732cf83acd5545833757e12fff09f65965ac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80430799194599f895bc2abfc8bbaec114d12818dca1ee455ee21e899e5175f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016bc4faaf81588d7bb1d7a3369ada19daddd6bb8099212c4aa768121e7ddd77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabasePropertiesCustomerContacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1e5953943a0401384ff56630b3fdc429be699cca6697da71a50939803532d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382bd8c98fbff611f63e193d629805a7bb33f69fd2dfb89f3f5c220b8288f1ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2451937886ffa57b1c1fcb1493178390dde873a0b64ad1f7558b4c834baa0276(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f562d7aa56d1e236c10f35117cee71f66649918c437e2c3f1821c97dfa6858(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaef7a2b0a169fbaf5edbc64103101b9b55f83b5dddc186f4cbe835c07e3d0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d62c7c5c6c7dea37158c5d199d186b09fe5af0f7b5186cf6f61a374506f9a6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe999c6c2e3cf20d50cfa8dc45740bb772d687f4c51f2bdd3aeeac67b9df2006(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835f7678f86141be929f2bd4fee8f5939fbc275268a94c8139efc95dc82ab82f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c469d282ed3ee34e313b230833acdfa33e0f2a623b0040193b3fbeed36f4761f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OracleDatabaseAutonomousDatabasePropertiesCustomerContacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841c84449a3cb3b199495a950362e6d123ffc2f6617e175c9bcaa67d533655bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4affcf90c03e3597b2c296bc7fa693795a2357d1c31fdfac3dd5b6594b371a73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6041459e38bd66eb6d633c5a3175e7a397ef475b3b7f39330f01f991ef6e580(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185c8771ed28b5d33dad977a003b9489648940489866be6c22916bd784ded1d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77af7fdf337ce591579870166fb91c01b755c3747f2f9febeb067b429fd670df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f14753fbb672c0c443262ca09629d87cc2d381e50c7dd0a18d6d586dee5c2bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bbf7f48c35d6981aebe5b4b844f9e6c97899064941ec517d231670f86231a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8cebaa8c172597cbe5a2064486c11a7bee2cd5597374e8dfea4f364ba21a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b351d249c5c6c074451e09154090e25703141099d2be947595ac4dc66c483f21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e81649a74b4d5f13f4e2d55932e0c390a4fe1179ca30071d3395d861fec1fdb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138e57df052f432e599f6a7d73930969ce537029dba3c577220273d448fbda9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecd45086ea432a8d0cced06106148dff8d066a8b96fae2c8cd3d6279eb4c8fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926e32c5aa49ba967eedde315bc9769d830b3cc337596c95677a9fb3d66603eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfbf52575acbc1f5b96e30c2b04a4013958b4bfabd5f2167c196045c0826d17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f49fa2aed3221880d9fa9f8ad59a22156d5f1007d34dcd9edcf6df1c170031a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c605b1d4b649e254bfb22baba697ebd60096ec5f75d1efbce3b945c06adbf5bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7a7bc4138e53f371807b24f11a3098bd1da359231b84a5c39cb65827c0a00f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20707eec19060f5e21b825cf2b94fc69decac1d2972633c2843f366218d2bf17(
    value: typing.Optional[OracleDatabaseAutonomousDatabaseProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85594be3d5b3c4163424813d9539ee5755e45f6ba2476636fa148d3d71964ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a31880db842ae3281d8b1ce1837e06c6df6ae84afcc2bcbbd2d9fc399e536c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992a9ed454f38c23d20eb7eacb30659929fac660b8e285594fdc92137884b43c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c9bf31f5bf0d3c3ce71b7d9ac9f8906e584f8dcf39ec7bd0b8118789195cd3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c950cefaf369a85ecb734148877326a6c25a1b3be27b780adae9d9c2f65714(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b2f374c0261a09974834a5e6007e00e0332105b14d34f984a160286bc66aad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e4d0a08f64f1086da4044905bd0c2a02a979d5de3f1ba7ca24da4040805f97(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145e7825a71436f6567812c9f9a5491af1c70cd6eac4d15ccf305659152836ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7305c3cedaf0dd8eb46dc4da11134d830bb8e76d6399cf2d6b89e8f61eecd02e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae63ec1f8969083046b1655bc4830933c329ab3c453fccc07291ac88b346e1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f077cd0ef2d06fdd304a49e0783789e4879273cda83f79c69f055b78af1550cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff6fcb91659d1fb5ddd13d038c299d6493310b35a62150ca6bab5121dad3eac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5531ff4731de869b6cd3daac6c93847c8d553fbd2c9c49b4c162107b0e40662d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6bc38fd3e7ba40efefd6936f1fe8d9e5950ded2450f36cab4d24390e7ec6da(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa810a9b39d3e445ad1f29bc2504cecbb8c5645b5d4679923ca3f85da3ef739(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f4b55b0798a0060bf1c91a4a1894275ac4708bae6cd5bf42df3e72ba311ed3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4462838782281c35375162198b93cd365435482aeb96a6064354ecd3441d7e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0c85adf6e548b4d493d6e06e35bf33a1ef89712676412d66462f34372610a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028c6982f5c185627d50939a01ff01957a9be70e24eba88a6ea144dc5f36cc99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3761d810591074115c7ddba6080c372155e6e052ab18c5c4d71c6d5a210ee7a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac991a9120bc04baa6f224b356b6aa7e0341bf152d2114769ed2332120ceb49(
    value: typing.Optional[OracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d45d970ef7d350cc0609e01dcc82e5107b41b536d4dbe4e3dd2060e9b983b3f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0dcecf18a3f8c197677b74f7bfd64255cd2629d3da8e30c910b3bfa5308757(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e3da0065ef850d4645c37e07ab6c1611bbc69f732a98bc286d5f9a258db452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f605852128e9d2a86223eb3e4ff45abf303140b40af897666b11db207fe293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74d82efdd0d841da9765b559768ed03b65ec8f91f6e38c3fdaecd88baa05b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823c94b249399628492ae630462b6a5c937dcd21c7f04a0bbf0c068a4e4912c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleDatabaseAutonomousDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
