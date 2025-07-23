r'''
# `google_spanner_database`

Refer to the Terraform Registry for docs: [`google_spanner_database`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database).
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


class SpannerDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerDatabase.SpannerDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database google_spanner_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance: builtins.str,
        name: builtins.str,
        database_dialect: typing.Optional[builtins.str] = None,
        ddl: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_time_zone: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_drop_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["SpannerDatabaseEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpannerDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_retention_period: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database google_spanner_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance: The instance to create the database on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#instance SpannerDatabase#instance}
        :param name: A unique identifier for the database, which cannot be changed after the instance is created. Values are of the form '[a-z][-_a-z0-9]*[a-z0-9]'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#name SpannerDatabase#name}
        :param database_dialect: The dialect of the Cloud Spanner Database. If it is not provided, "GOOGLE_STANDARD_SQL" will be used. Possible values: ["GOOGLE_STANDARD_SQL", "POSTGRESQL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#database_dialect SpannerDatabase#database_dialect}
        :param ddl: An optional list of DDL statements to run inside the database. Statements can create tables, indexes, etc. During creation these statements execute atomically with the creation of the database and if there is an error in any statement, the database is not created. Terraform does not perform drift detection on this field and assumes that the values recorded in state are accurate. Limited updates to this field are supported, and newly appended DDL statements can be executed in an update. However, modifications to prior statements will create a plan that marks the resource for recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#ddl SpannerDatabase#ddl}
        :param default_time_zone: The default time zone for the database. The default time zone must be a valid name from the tz database. Default value is "America/Los_angeles". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#default_time_zone SpannerDatabase#default_time_zone}
        :param deletion_protection: Whether Terraform will be prevented from destroying the database. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the database, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the database will fail. When the field is set to false, deleting the database is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#deletion_protection SpannerDatabase#deletion_protection}
        :param enable_drop_protection: Whether drop protection is enabled for this database. Defaults to false. Drop protection is different from the "deletion_protection" attribute in the following ways: (1) "deletion_protection" only protects the database from deletions in Terraform. whereas setting “enableDropProtection” to true protects the database from deletions in all interfaces. (2) Setting "enableDropProtection" to true also prevents the deletion of the parent instance containing the database. "deletion_protection" attribute does not provide protection against the deletion of the parent instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#enable_drop_protection SpannerDatabase#enable_drop_protection}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#encryption_config SpannerDatabase#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#id SpannerDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#project SpannerDatabase#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#timeouts SpannerDatabase#timeouts}
        :param version_retention_period: The retention period for the database. The retention period must be between 1 hour and 7 days, and can be specified in days, hours, minutes, or seconds. For example, the values 1d, 24h, 1440m, and 86400s are equivalent. Default value is 1h. If this property is used, you must avoid adding new DDL statements to 'ddl' that update the database's version_retention_period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#version_retention_period SpannerDatabase#version_retention_period}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6aeb5da33457991ffe16bf7f8e1074992333893ea8ae69c4c1e3b97d6c6d15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpannerDatabaseConfig(
            instance=instance,
            name=name,
            database_dialect=database_dialect,
            ddl=ddl,
            default_time_zone=default_time_zone,
            deletion_protection=deletion_protection,
            enable_drop_protection=enable_drop_protection,
            encryption_config=encryption_config,
            id=id,
            project=project,
            timeouts=timeouts,
            version_retention_period=version_retention_period,
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
        '''Generates CDKTF code for importing a SpannerDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpannerDatabase to import.
        :param import_from_id: The id of the existing SpannerDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpannerDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f731bcb64280ebcb2080241f710e31020827136262d6641e2bc4aa05e59f8ca2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        kms_key_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param kms_key_name: Fully qualified name of the KMS key to use to encrypt this database. This key must exist in the same location as the Spanner Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#kms_key_name SpannerDatabase#kms_key_name}
        :param kms_key_names: Fully qualified name of the KMS keys to use to encrypt this database. The keys must exist in the same locations as the Spanner Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#kms_key_names SpannerDatabase#kms_key_names}
        '''
        value = SpannerDatabaseEncryptionConfig(
            kms_key_name=kms_key_name, kms_key_names=kms_key_names
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#create SpannerDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#delete SpannerDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#update SpannerDatabase#update}.
        '''
        value = SpannerDatabaseTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDatabaseDialect")
    def reset_database_dialect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseDialect", []))

    @jsii.member(jsii_name="resetDdl")
    def reset_ddl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDdl", []))

    @jsii.member(jsii_name="resetDefaultTimeZone")
    def reset_default_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTimeZone", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetEnableDropProtection")
    def reset_enable_drop_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDropProtection", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersionRetentionPeriod")
    def reset_version_retention_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionRetentionPeriod", []))

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
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> "SpannerDatabaseEncryptionConfigOutputReference":
        return typing.cast("SpannerDatabaseEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SpannerDatabaseTimeoutsOutputReference":
        return typing.cast("SpannerDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="databaseDialectInput")
    def database_dialect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseDialectInput"))

    @builtins.property
    @jsii.member(jsii_name="ddlInput")
    def ddl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ddlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTimeZoneInput")
    def default_time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTimeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDropProtectionInput")
    def enable_drop_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDropProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["SpannerDatabaseEncryptionConfig"]:
        return typing.cast(typing.Optional["SpannerDatabaseEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpannerDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpannerDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionRetentionPeriodInput")
    def version_retention_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionRetentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseDialect")
    def database_dialect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseDialect"))

    @database_dialect.setter
    def database_dialect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17da1d7b1a1c4193c3257fe9aae9a981befe71a69ddfd736dc249c7a1d19f233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseDialect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ddl")
    def ddl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ddl"))

    @ddl.setter
    def ddl(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9337db51c1a07168d5a9495de3e1b6d5bf10b1bab4bd5586990f0fa1002e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ddl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTimeZone")
    def default_time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTimeZone"))

    @default_time_zone.setter
    def default_time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5998a72e642d16314876e3431750ce49d8bee2bc92256a5f8bcb94d4b8da047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTimeZone", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__340f0063657202e8d59274be83c55b9c667afa52c7dac3c4628ddf080afb66cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDropProtection")
    def enable_drop_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDropProtection"))

    @enable_drop_protection.setter
    def enable_drop_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fee1070a864f046a77394a87d83b75114c41dc37ec86a8b81aed668f2e2d099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDropProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14aac796cd5081c8f4a38e57fce07a6d375c9bdd7bd7eed3ac8234cbb6412cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651eae51134cafde1cff5b98785bc5de93d10bb77b7ad6de54812ff2f48f5992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6362ac69d40a52504163ac2cbcb93a28db68a2b711ce6573cfd37be96032f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfa515d328177bab434e80934cedcc3d0899b035e830352e0d33fb04b6fc634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionRetentionPeriod")
    def version_retention_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionRetentionPeriod"))

    @version_retention_period.setter
    def version_retention_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a878cdecd3180162919dca667d4a76808300801808b589a767fdca6c675f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionRetentionPeriod", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerDatabase.SpannerDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance": "instance",
        "name": "name",
        "database_dialect": "databaseDialect",
        "ddl": "ddl",
        "default_time_zone": "defaultTimeZone",
        "deletion_protection": "deletionProtection",
        "enable_drop_protection": "enableDropProtection",
        "encryption_config": "encryptionConfig",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
        "version_retention_period": "versionRetentionPeriod",
    },
)
class SpannerDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance: builtins.str,
        name: builtins.str,
        database_dialect: typing.Optional[builtins.str] = None,
        ddl: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_time_zone: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_drop_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["SpannerDatabaseEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpannerDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance: The instance to create the database on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#instance SpannerDatabase#instance}
        :param name: A unique identifier for the database, which cannot be changed after the instance is created. Values are of the form '[a-z][-_a-z0-9]*[a-z0-9]'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#name SpannerDatabase#name}
        :param database_dialect: The dialect of the Cloud Spanner Database. If it is not provided, "GOOGLE_STANDARD_SQL" will be used. Possible values: ["GOOGLE_STANDARD_SQL", "POSTGRESQL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#database_dialect SpannerDatabase#database_dialect}
        :param ddl: An optional list of DDL statements to run inside the database. Statements can create tables, indexes, etc. During creation these statements execute atomically with the creation of the database and if there is an error in any statement, the database is not created. Terraform does not perform drift detection on this field and assumes that the values recorded in state are accurate. Limited updates to this field are supported, and newly appended DDL statements can be executed in an update. However, modifications to prior statements will create a plan that marks the resource for recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#ddl SpannerDatabase#ddl}
        :param default_time_zone: The default time zone for the database. The default time zone must be a valid name from the tz database. Default value is "America/Los_angeles". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#default_time_zone SpannerDatabase#default_time_zone}
        :param deletion_protection: Whether Terraform will be prevented from destroying the database. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the database, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the database will fail. When the field is set to false, deleting the database is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#deletion_protection SpannerDatabase#deletion_protection}
        :param enable_drop_protection: Whether drop protection is enabled for this database. Defaults to false. Drop protection is different from the "deletion_protection" attribute in the following ways: (1) "deletion_protection" only protects the database from deletions in Terraform. whereas setting “enableDropProtection” to true protects the database from deletions in all interfaces. (2) Setting "enableDropProtection" to true also prevents the deletion of the parent instance containing the database. "deletion_protection" attribute does not provide protection against the deletion of the parent instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#enable_drop_protection SpannerDatabase#enable_drop_protection}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#encryption_config SpannerDatabase#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#id SpannerDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#project SpannerDatabase#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#timeouts SpannerDatabase#timeouts}
        :param version_retention_period: The retention period for the database. The retention period must be between 1 hour and 7 days, and can be specified in days, hours, minutes, or seconds. For example, the values 1d, 24h, 1440m, and 86400s are equivalent. Default value is 1h. If this property is used, you must avoid adding new DDL statements to 'ddl' that update the database's version_retention_period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#version_retention_period SpannerDatabase#version_retention_period}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_config, dict):
            encryption_config = SpannerDatabaseEncryptionConfig(**encryption_config)
        if isinstance(timeouts, dict):
            timeouts = SpannerDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c43e0ff0a90aae42dfaf2f4fb6ee9952ca81beb04fd0ea7dff7851ab5197257)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument database_dialect", value=database_dialect, expected_type=type_hints["database_dialect"])
            check_type(argname="argument ddl", value=ddl, expected_type=type_hints["ddl"])
            check_type(argname="argument default_time_zone", value=default_time_zone, expected_type=type_hints["default_time_zone"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument enable_drop_protection", value=enable_drop_protection, expected_type=type_hints["enable_drop_protection"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_retention_period", value=version_retention_period, expected_type=type_hints["version_retention_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance": instance,
            "name": name,
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
        if database_dialect is not None:
            self._values["database_dialect"] = database_dialect
        if ddl is not None:
            self._values["ddl"] = ddl
        if default_time_zone is not None:
            self._values["default_time_zone"] = default_time_zone
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enable_drop_protection is not None:
            self._values["enable_drop_protection"] = enable_drop_protection
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_retention_period is not None:
            self._values["version_retention_period"] = version_retention_period

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
    def instance(self) -> builtins.str:
        '''The instance to create the database on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#instance SpannerDatabase#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A unique identifier for the database, which cannot be changed after the instance is created.

        Values are of the form '[a-z][-_a-z0-9]*[a-z0-9]'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#name SpannerDatabase#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_dialect(self) -> typing.Optional[builtins.str]:
        '''The dialect of the Cloud Spanner Database. If it is not provided, "GOOGLE_STANDARD_SQL" will be used. Possible values: ["GOOGLE_STANDARD_SQL", "POSTGRESQL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#database_dialect SpannerDatabase#database_dialect}
        '''
        result = self._values.get("database_dialect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ddl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of DDL statements to run inside the database. Statements can create tables, indexes, etc.

        During creation these statements execute atomically with the creation of the database
        and if there is an error in any statement, the database is not created.

        Terraform does not perform drift detection on this field and assumes that the values
        recorded in state are accurate. Limited updates to this field are supported, and
        newly appended DDL statements can be executed in an update. However, modifications
        to prior statements will create a plan that marks the resource for recreation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#ddl SpannerDatabase#ddl}
        '''
        result = self._values.get("ddl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_time_zone(self) -> typing.Optional[builtins.str]:
        '''The default time zone for the database.

        The default time zone must be a valid name
        from the tz database. Default value is "America/Los_angeles".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#default_time_zone SpannerDatabase#default_time_zone}
        '''
        result = self._values.get("default_time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the database.

        Defaults to true.
        When a'terraform destroy' or 'terraform apply' would delete the database,
        the command will fail if this field is not set to false in Terraform state.
        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the database will fail.
        When the field is set to false, deleting the database is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#deletion_protection SpannerDatabase#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_drop_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether drop protection is enabled for this database.

        Defaults to false.
        Drop protection is different from
        the "deletion_protection" attribute in the following ways:
        (1) "deletion_protection" only protects the database from deletions in Terraform.
        whereas setting “enableDropProtection” to true protects the database from deletions in all interfaces.
        (2) Setting "enableDropProtection" to true also prevents the deletion of the parent instance containing the database.
        "deletion_protection" attribute does not provide protection against the deletion of the parent instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#enable_drop_protection SpannerDatabase#enable_drop_protection}
        '''
        result = self._values.get("enable_drop_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(self) -> typing.Optional["SpannerDatabaseEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#encryption_config SpannerDatabase#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["SpannerDatabaseEncryptionConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#id SpannerDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#project SpannerDatabase#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpannerDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#timeouts SpannerDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpannerDatabaseTimeouts"], result)

    @builtins.property
    def version_retention_period(self) -> typing.Optional[builtins.str]:
        '''The retention period for the database.

        The retention period must be between 1 hour
        and 7 days, and can be specified in days, hours, minutes, or seconds. For example,
        the values 1d, 24h, 1440m, and 86400s are equivalent. Default value is 1h.
        If this property is used, you must avoid adding new DDL statements to 'ddl' that
        update the database's version_retention_period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#version_retention_period SpannerDatabase#version_retention_period}
        '''
        result = self._values.get("version_retention_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerDatabase.SpannerDatabaseEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "kms_key_names": "kmsKeyNames"},
)
class SpannerDatabaseEncryptionConfig:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        kms_key_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param kms_key_name: Fully qualified name of the KMS key to use to encrypt this database. This key must exist in the same location as the Spanner Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#kms_key_name SpannerDatabase#kms_key_name}
        :param kms_key_names: Fully qualified name of the KMS keys to use to encrypt this database. The keys must exist in the same locations as the Spanner Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#kms_key_names SpannerDatabase#kms_key_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02a3db68af0d6314733a36aaf311b8bf30b54e3a374f50cd8f8e04e5c03e2b4)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument kms_key_names", value=kms_key_names, expected_type=type_hints["kms_key_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if kms_key_names is not None:
            self._values["kms_key_names"] = kms_key_names

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Fully qualified name of the KMS key to use to encrypt this database.

        This key must exist
        in the same location as the Spanner Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#kms_key_name SpannerDatabase#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully qualified name of the KMS keys to use to encrypt this database.

        The keys must exist
        in the same locations as the Spanner Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#kms_key_names SpannerDatabase#kms_key_names}
        '''
        result = self._values.get("kms_key_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerDatabaseEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerDatabaseEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerDatabase.SpannerDatabaseEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8d5064bf25727b9abc2c7a68b071789c4507adc5ebf878998eec5f2c3b98913)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetKmsKeyNames")
    def reset_kms_key_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyNames", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNamesInput")
    def kms_key_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "kmsKeyNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f848cdf80bdcc3e3b3f419ba80a28c196fd5d025ddb575245e15845035b7df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNames")
    def kms_key_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kmsKeyNames"))

    @kms_key_names.setter
    def kms_key_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1707b53a58ef5a3ef1c3e976dad7b150c02cbcedf736cbc3f41990bb44472a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpannerDatabaseEncryptionConfig]:
        return typing.cast(typing.Optional[SpannerDatabaseEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerDatabaseEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2737af70dacfc43814650cf4722ccc39ea2eb358f2223fc7ab9e7169615c683c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerDatabase.SpannerDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SpannerDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#create SpannerDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#delete SpannerDatabase#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#update SpannerDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b479327ea65a3cb530bfef310ff53f3e880695c11d074c63f094bd6fbf6b043)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#create SpannerDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#delete SpannerDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_database#update SpannerDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerDatabase.SpannerDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f63e6b4eef3a56af301220aa7f85a7eac596bfcdc36cca1ee4725ed8c3e281c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced2205702ed900c22b3fd0bd502823a58ef972ff03fadd19a3ee0ac1ae06916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a5fb1e897ff2059e7599a14712865c3bf690e0d6dd7877708dabd4e2d841e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbeed6627bf1e3d5abd971cd81bd92f4193c12d863d9da2ecc54239ef573468c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36394b122691de6a0eba98c11fb4f6323dc16c2451adc21b37bee8fe0ed435f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpannerDatabase",
    "SpannerDatabaseConfig",
    "SpannerDatabaseEncryptionConfig",
    "SpannerDatabaseEncryptionConfigOutputReference",
    "SpannerDatabaseTimeouts",
    "SpannerDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7b6aeb5da33457991ffe16bf7f8e1074992333893ea8ae69c4c1e3b97d6c6d15(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance: builtins.str,
    name: builtins.str,
    database_dialect: typing.Optional[builtins.str] = None,
    ddl: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_time_zone: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_drop_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[SpannerDatabaseEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpannerDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_retention_period: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f731bcb64280ebcb2080241f710e31020827136262d6641e2bc4aa05e59f8ca2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17da1d7b1a1c4193c3257fe9aae9a981befe71a69ddfd736dc249c7a1d19f233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9337db51c1a07168d5a9495de3e1b6d5bf10b1bab4bd5586990f0fa1002e87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5998a72e642d16314876e3431750ce49d8bee2bc92256a5f8bcb94d4b8da047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340f0063657202e8d59274be83c55b9c667afa52c7dac3c4628ddf080afb66cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fee1070a864f046a77394a87d83b75114c41dc37ec86a8b81aed668f2e2d099(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14aac796cd5081c8f4a38e57fce07a6d375c9bdd7bd7eed3ac8234cbb6412cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651eae51134cafde1cff5b98785bc5de93d10bb77b7ad6de54812ff2f48f5992(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6362ac69d40a52504163ac2cbcb93a28db68a2b711ce6573cfd37be96032f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfa515d328177bab434e80934cedcc3d0899b035e830352e0d33fb04b6fc634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a878cdecd3180162919dca667d4a76808300801808b589a767fdca6c675f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c43e0ff0a90aae42dfaf2f4fb6ee9952ca81beb04fd0ea7dff7851ab5197257(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance: builtins.str,
    name: builtins.str,
    database_dialect: typing.Optional[builtins.str] = None,
    ddl: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_time_zone: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_drop_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[SpannerDatabaseEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpannerDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_retention_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02a3db68af0d6314733a36aaf311b8bf30b54e3a374f50cd8f8e04e5c03e2b4(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    kms_key_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d5064bf25727b9abc2c7a68b071789c4507adc5ebf878998eec5f2c3b98913(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f848cdf80bdcc3e3b3f419ba80a28c196fd5d025ddb575245e15845035b7df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1707b53a58ef5a3ef1c3e976dad7b150c02cbcedf736cbc3f41990bb44472a45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2737af70dacfc43814650cf4722ccc39ea2eb358f2223fc7ab9e7169615c683c(
    value: typing.Optional[SpannerDatabaseEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b479327ea65a3cb530bfef310ff53f3e880695c11d074c63f094bd6fbf6b043(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f63e6b4eef3a56af301220aa7f85a7eac596bfcdc36cca1ee4725ed8c3e281c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced2205702ed900c22b3fd0bd502823a58ef972ff03fadd19a3ee0ac1ae06916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a5fb1e897ff2059e7599a14712865c3bf690e0d6dd7877708dabd4e2d841e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbeed6627bf1e3d5abd971cd81bd92f4193c12d863d9da2ecc54239ef573468c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36394b122691de6a0eba98c11fb4f6323dc16c2451adc21b37bee8fe0ed435f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
