r'''
# `google_spanner_backup_schedule`

Refer to the Terraform Registry for docs: [`google_spanner_backup_schedule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule).
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


class SpannerBackupSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule google_spanner_backup_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        instance: builtins.str,
        retention_duration: builtins.str,
        encryption_config: typing.Optional[typing.Union["SpannerBackupScheduleEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        full_backup_spec: typing.Optional[typing.Union["SpannerBackupScheduleFullBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_backup_spec: typing.Optional[typing.Union["SpannerBackupScheduleIncrementalBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["SpannerBackupScheduleSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SpannerBackupScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule google_spanner_backup_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database to create the backup schedule on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#database SpannerBackupSchedule#database}
        :param instance: The instance to create the database on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#instance SpannerBackupSchedule#instance}
        :param retention_duration: At what relative time in the future, compared to its creation time, the backup should be deleted, e.g. keep backups for 7 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. You can set this to a value up to 366 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#retention_duration SpannerBackupSchedule#retention_duration}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#encryption_config SpannerBackupSchedule#encryption_config}
        :param full_backup_spec: full_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#full_backup_spec SpannerBackupSchedule#full_backup_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#id SpannerBackupSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_backup_spec: incremental_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#incremental_backup_spec SpannerBackupSchedule#incremental_backup_spec}
        :param name: A unique identifier for the backup schedule, which cannot be changed after the backup schedule is created. Values are of the form [a-z][-a-z0-9]*[a-z0-9]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#name SpannerBackupSchedule#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#project SpannerBackupSchedule#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#spec SpannerBackupSchedule#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#timeouts SpannerBackupSchedule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa86559058b6f7dbf87964d58adf3f22abf76bd4911c3cd6d0c0ffc27e7c2d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpannerBackupScheduleConfig(
            database=database,
            instance=instance,
            retention_duration=retention_duration,
            encryption_config=encryption_config,
            full_backup_spec=full_backup_spec,
            id=id,
            incremental_backup_spec=incremental_backup_spec,
            name=name,
            project=project,
            spec=spec,
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
        '''Generates CDKTF code for importing a SpannerBackupSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpannerBackupSchedule to import.
        :param import_from_id: The id of the existing SpannerBackupSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpannerBackupSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb16ee2f30b98812fb4a1b88ec449f16ccc8d551e3c0e2fdac358db561d54ea2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        encryption_type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
        kms_key_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param encryption_type: The encryption type of backups created by the backup schedule. Possible values are USE_DATABASE_ENCRYPTION, GOOGLE_DEFAULT_ENCRYPTION, or CUSTOMER_MANAGED_ENCRYPTION. If you use CUSTOMER_MANAGED_ENCRYPTION, you must specify a kmsKeyName. If your backup type is incremental-backup, the encryption type must be GOOGLE_DEFAULT_ENCRYPTION. Possible values: ["USE_DATABASE_ENCRYPTION", "GOOGLE_DEFAULT_ENCRYPTION", "CUSTOMER_MANAGED_ENCRYPTION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#encryption_type SpannerBackupSchedule#encryption_type}
        :param kms_key_name: The resource name of the Cloud KMS key to use for encryption. Format: 'projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#kms_key_name SpannerBackupSchedule#kms_key_name}
        :param kms_key_names: Fully qualified name of the KMS keys to use to encrypt this database. The keys must exist in the same locations as the Spanner Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#kms_key_names SpannerBackupSchedule#kms_key_names}
        '''
        value = SpannerBackupScheduleEncryptionConfig(
            encryption_type=encryption_type,
            kms_key_name=kms_key_name,
            kms_key_names=kms_key_names,
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putFullBackupSpec")
    def put_full_backup_spec(self) -> None:
        value = SpannerBackupScheduleFullBackupSpec()

        return typing.cast(None, jsii.invoke(self, "putFullBackupSpec", [value]))

    @jsii.member(jsii_name="putIncrementalBackupSpec")
    def put_incremental_backup_spec(self) -> None:
        value = SpannerBackupScheduleIncrementalBackupSpec()

        return typing.cast(None, jsii.invoke(self, "putIncrementalBackupSpec", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        cron_spec: typing.Optional[typing.Union["SpannerBackupScheduleSpecCronSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_spec: cron_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#cron_spec SpannerBackupSchedule#cron_spec}
        '''
        value = SpannerBackupScheduleSpec(cron_spec=cron_spec)

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#create SpannerBackupSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#delete SpannerBackupSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#update SpannerBackupSchedule#update}.
        '''
        value = SpannerBackupScheduleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetFullBackupSpec")
    def reset_full_backup_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullBackupSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncrementalBackupSpec")
    def reset_incremental_backup_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncrementalBackupSpec", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

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
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> "SpannerBackupScheduleEncryptionConfigOutputReference":
        return typing.cast("SpannerBackupScheduleEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="fullBackupSpec")
    def full_backup_spec(self) -> "SpannerBackupScheduleFullBackupSpecOutputReference":
        return typing.cast("SpannerBackupScheduleFullBackupSpecOutputReference", jsii.get(self, "fullBackupSpec"))

    @builtins.property
    @jsii.member(jsii_name="incrementalBackupSpec")
    def incremental_backup_spec(
        self,
    ) -> "SpannerBackupScheduleIncrementalBackupSpecOutputReference":
        return typing.cast("SpannerBackupScheduleIncrementalBackupSpecOutputReference", jsii.get(self, "incrementalBackupSpec"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "SpannerBackupScheduleSpecOutputReference":
        return typing.cast("SpannerBackupScheduleSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SpannerBackupScheduleTimeoutsOutputReference":
        return typing.cast("SpannerBackupScheduleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["SpannerBackupScheduleEncryptionConfig"]:
        return typing.cast(typing.Optional["SpannerBackupScheduleEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fullBackupSpecInput")
    def full_backup_spec_input(
        self,
    ) -> typing.Optional["SpannerBackupScheduleFullBackupSpec"]:
        return typing.cast(typing.Optional["SpannerBackupScheduleFullBackupSpec"], jsii.get(self, "fullBackupSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalBackupSpecInput")
    def incremental_backup_spec_input(
        self,
    ) -> typing.Optional["SpannerBackupScheduleIncrementalBackupSpec"]:
        return typing.cast(typing.Optional["SpannerBackupScheduleIncrementalBackupSpec"], jsii.get(self, "incrementalBackupSpecInput"))

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
    @jsii.member(jsii_name="retentionDurationInput")
    def retention_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["SpannerBackupScheduleSpec"]:
        return typing.cast(typing.Optional["SpannerBackupScheduleSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpannerBackupScheduleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpannerBackupScheduleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2193553a95a1261aae3c69c7c27d67152947a491972189a596b4103841110bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6f8457afe5e2b89cb47c52c8758b8120efd5009e083cf349f36cf8aa5d5556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a04b1d5e480a425d324ab328cf9b636a79427c91cef8bc6df7d4b94535f3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41277eb0274e3085feef4c073ec6261fd9a2959c2267eae50bc5bed5abdab27e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0bd780300b6d9fce61a886c2690f26c89b968d13269b7a4c120dfd4c7acdfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDuration")
    def retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionDuration"))

    @retention_duration.setter
    def retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a12768400c392f9f7826f257280115b585d42c20304175a5b56824eda568e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDuration", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "instance": "instance",
        "retention_duration": "retentionDuration",
        "encryption_config": "encryptionConfig",
        "full_backup_spec": "fullBackupSpec",
        "id": "id",
        "incremental_backup_spec": "incrementalBackupSpec",
        "name": "name",
        "project": "project",
        "spec": "spec",
        "timeouts": "timeouts",
    },
)
class SpannerBackupScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        instance: builtins.str,
        retention_duration: builtins.str,
        encryption_config: typing.Optional[typing.Union["SpannerBackupScheduleEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        full_backup_spec: typing.Optional[typing.Union["SpannerBackupScheduleFullBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_backup_spec: typing.Optional[typing.Union["SpannerBackupScheduleIncrementalBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["SpannerBackupScheduleSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SpannerBackupScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database to create the backup schedule on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#database SpannerBackupSchedule#database}
        :param instance: The instance to create the database on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#instance SpannerBackupSchedule#instance}
        :param retention_duration: At what relative time in the future, compared to its creation time, the backup should be deleted, e.g. keep backups for 7 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. You can set this to a value up to 366 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#retention_duration SpannerBackupSchedule#retention_duration}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#encryption_config SpannerBackupSchedule#encryption_config}
        :param full_backup_spec: full_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#full_backup_spec SpannerBackupSchedule#full_backup_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#id SpannerBackupSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_backup_spec: incremental_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#incremental_backup_spec SpannerBackupSchedule#incremental_backup_spec}
        :param name: A unique identifier for the backup schedule, which cannot be changed after the backup schedule is created. Values are of the form [a-z][-a-z0-9]*[a-z0-9]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#name SpannerBackupSchedule#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#project SpannerBackupSchedule#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#spec SpannerBackupSchedule#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#timeouts SpannerBackupSchedule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_config, dict):
            encryption_config = SpannerBackupScheduleEncryptionConfig(**encryption_config)
        if isinstance(full_backup_spec, dict):
            full_backup_spec = SpannerBackupScheduleFullBackupSpec(**full_backup_spec)
        if isinstance(incremental_backup_spec, dict):
            incremental_backup_spec = SpannerBackupScheduleIncrementalBackupSpec(**incremental_backup_spec)
        if isinstance(spec, dict):
            spec = SpannerBackupScheduleSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = SpannerBackupScheduleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ca35640328e0cde1d82c35ff62ab49a1d1706913bd874ddb40253e7139ea43)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument retention_duration", value=retention_duration, expected_type=type_hints["retention_duration"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument full_backup_spec", value=full_backup_spec, expected_type=type_hints["full_backup_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument incremental_backup_spec", value=incremental_backup_spec, expected_type=type_hints["incremental_backup_spec"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "instance": instance,
            "retention_duration": retention_duration,
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
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if full_backup_spec is not None:
            self._values["full_backup_spec"] = full_backup_spec
        if id is not None:
            self._values["id"] = id
        if incremental_backup_spec is not None:
            self._values["incremental_backup_spec"] = incremental_backup_spec
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if spec is not None:
            self._values["spec"] = spec
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
    def database(self) -> builtins.str:
        '''The database to create the backup schedule on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#database SpannerBackupSchedule#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''The instance to create the database on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#instance SpannerBackupSchedule#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_duration(self) -> builtins.str:
        '''At what relative time in the future, compared to its creation time, the backup should be deleted, e.g. keep backups for 7 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. You can set this to a value up to 366 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#retention_duration SpannerBackupSchedule#retention_duration}
        '''
        result = self._values.get("retention_duration")
        assert result is not None, "Required property 'retention_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["SpannerBackupScheduleEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#encryption_config SpannerBackupSchedule#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["SpannerBackupScheduleEncryptionConfig"], result)

    @builtins.property
    def full_backup_spec(
        self,
    ) -> typing.Optional["SpannerBackupScheduleFullBackupSpec"]:
        '''full_backup_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#full_backup_spec SpannerBackupSchedule#full_backup_spec}
        '''
        result = self._values.get("full_backup_spec")
        return typing.cast(typing.Optional["SpannerBackupScheduleFullBackupSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#id SpannerBackupSchedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_backup_spec(
        self,
    ) -> typing.Optional["SpannerBackupScheduleIncrementalBackupSpec"]:
        '''incremental_backup_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#incremental_backup_spec SpannerBackupSchedule#incremental_backup_spec}
        '''
        result = self._values.get("incremental_backup_spec")
        return typing.cast(typing.Optional["SpannerBackupScheduleIncrementalBackupSpec"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the backup schedule, which cannot be changed after the backup schedule is created.

        Values are of the form [a-z][-a-z0-9]*[a-z0-9].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#name SpannerBackupSchedule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#project SpannerBackupSchedule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["SpannerBackupScheduleSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#spec SpannerBackupSchedule#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["SpannerBackupScheduleSpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpannerBackupScheduleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#timeouts SpannerBackupSchedule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpannerBackupScheduleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_type": "encryptionType",
        "kms_key_name": "kmsKeyName",
        "kms_key_names": "kmsKeyNames",
    },
)
class SpannerBackupScheduleEncryptionConfig:
    def __init__(
        self,
        *,
        encryption_type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
        kms_key_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param encryption_type: The encryption type of backups created by the backup schedule. Possible values are USE_DATABASE_ENCRYPTION, GOOGLE_DEFAULT_ENCRYPTION, or CUSTOMER_MANAGED_ENCRYPTION. If you use CUSTOMER_MANAGED_ENCRYPTION, you must specify a kmsKeyName. If your backup type is incremental-backup, the encryption type must be GOOGLE_DEFAULT_ENCRYPTION. Possible values: ["USE_DATABASE_ENCRYPTION", "GOOGLE_DEFAULT_ENCRYPTION", "CUSTOMER_MANAGED_ENCRYPTION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#encryption_type SpannerBackupSchedule#encryption_type}
        :param kms_key_name: The resource name of the Cloud KMS key to use for encryption. Format: 'projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#kms_key_name SpannerBackupSchedule#kms_key_name}
        :param kms_key_names: Fully qualified name of the KMS keys to use to encrypt this database. The keys must exist in the same locations as the Spanner Database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#kms_key_names SpannerBackupSchedule#kms_key_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7563a05c6780132debdab328eb989dbe802a5115dc3b6dda16ca12216dc7bdae)
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument kms_key_names", value=kms_key_names, expected_type=type_hints["kms_key_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_type": encryption_type,
        }
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if kms_key_names is not None:
            self._values["kms_key_names"] = kms_key_names

    @builtins.property
    def encryption_type(self) -> builtins.str:
        '''The encryption type of backups created by the backup schedule.

        Possible values are USE_DATABASE_ENCRYPTION, GOOGLE_DEFAULT_ENCRYPTION, or CUSTOMER_MANAGED_ENCRYPTION.
        If you use CUSTOMER_MANAGED_ENCRYPTION, you must specify a kmsKeyName.
        If your backup type is incremental-backup, the encryption type must be GOOGLE_DEFAULT_ENCRYPTION. Possible values: ["USE_DATABASE_ENCRYPTION", "GOOGLE_DEFAULT_ENCRYPTION", "CUSTOMER_MANAGED_ENCRYPTION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#encryption_type SpannerBackupSchedule#encryption_type}
        '''
        result = self._values.get("encryption_type")
        assert result is not None, "Required property 'encryption_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Cloud KMS key to use for encryption. Format: 'projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#kms_key_name SpannerBackupSchedule#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully qualified name of the KMS keys to use to encrypt this database.

        The keys must exist
        in the same locations as the Spanner Database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#kms_key_names SpannerBackupSchedule#kms_key_names}
        '''
        result = self._values.get("kms_key_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerBackupScheduleEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43f1ee5dbc3b470c05f95905cd35ebcb46b26f2c3178aa6ab629fb33e4ed21c1)
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
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNamesInput")
    def kms_key_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "kmsKeyNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e61bcbe3141c072f6644e0e98b7698de23d15117e37e6c5806857f97f4018f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a8eab876fe7bfc01ca093fd66f236db3424c2e4b4fa1c2a0bd303b72d928dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNames")
    def kms_key_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kmsKeyNames"))

    @kms_key_names.setter
    def kms_key_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2816fc6e1bd6e2df9484a7484822ee26bcf5fe05588921df52d9c06d2f56f55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpannerBackupScheduleEncryptionConfig]:
        return typing.cast(typing.Optional[SpannerBackupScheduleEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerBackupScheduleEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fba7670ee92750f795fed374e4db047b6d11e2459fc119c9d1dbc6316c43966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleFullBackupSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class SpannerBackupScheduleFullBackupSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleFullBackupSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerBackupScheduleFullBackupSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleFullBackupSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44166a51c0c95bb682ef67629d6ea3956444743358ce6e4ebd6d559d46cdc1eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpannerBackupScheduleFullBackupSpec]:
        return typing.cast(typing.Optional[SpannerBackupScheduleFullBackupSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerBackupScheduleFullBackupSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a4e8995ae845cc570645ee94a64d67e0ed081469614165da1bf92a3d0251ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleIncrementalBackupSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class SpannerBackupScheduleIncrementalBackupSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleIncrementalBackupSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerBackupScheduleIncrementalBackupSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleIncrementalBackupSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce155c5e0e0d0bffb3fc9805efee64813153a9b204b6409e85f6afe79be8052e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpannerBackupScheduleIncrementalBackupSpec]:
        return typing.cast(typing.Optional[SpannerBackupScheduleIncrementalBackupSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerBackupScheduleIncrementalBackupSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079d410507109efe08928f37afc5cc9bd6e912171ee93776933ebba0368d4f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleSpec",
    jsii_struct_bases=[],
    name_mapping={"cron_spec": "cronSpec"},
)
class SpannerBackupScheduleSpec:
    def __init__(
        self,
        *,
        cron_spec: typing.Optional[typing.Union["SpannerBackupScheduleSpecCronSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_spec: cron_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#cron_spec SpannerBackupSchedule#cron_spec}
        '''
        if isinstance(cron_spec, dict):
            cron_spec = SpannerBackupScheduleSpecCronSpec(**cron_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bdb6a11284ab5b0428da2c09d55daf6cada7d05027c70f04b26cf35ea9884e)
            check_type(argname="argument cron_spec", value=cron_spec, expected_type=type_hints["cron_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_spec is not None:
            self._values["cron_spec"] = cron_spec

    @builtins.property
    def cron_spec(self) -> typing.Optional["SpannerBackupScheduleSpecCronSpec"]:
        '''cron_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#cron_spec SpannerBackupSchedule#cron_spec}
        '''
        result = self._values.get("cron_spec")
        return typing.cast(typing.Optional["SpannerBackupScheduleSpecCronSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleSpecCronSpec",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class SpannerBackupScheduleSpecCronSpec:
    def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Textual representation of the crontab. User can customize the backup frequency and the backup version time using the cron expression. The version time must be in UTC timzeone. The backup will contain an externally consistent copy of the database at the version time. Allowed frequencies are 12 hour, 1 day, 1 week and 1 month. Examples of valid cron specifications: 0 2/12 * * * : every 12 hours at (2, 14) hours past midnight in UTC. 0 2,14 * * * : every 12 hours at (2,14) hours past midnight in UTC. 0 2 * * * : once a day at 2 past midnight in UTC. 0 2 * * 0 : once a week every Sunday at 2 past midnight in UTC. 0 2 8 * * : once a month on 8th day at 2 past midnight in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#text SpannerBackupSchedule#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0711e4ec53db1f576d1afd7ddb8cc1c6c677901a8b300b55ec30e3d443ddb374)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Textual representation of the crontab.

        User can customize the
        backup frequency and the backup version time using the cron
        expression. The version time must be in UTC timzeone.
        The backup will contain an externally consistent copy of the
        database at the version time. Allowed frequencies are 12 hour, 1 day,
        1 week and 1 month. Examples of valid cron specifications:
        0 2/12 * * * : every 12 hours at (2, 14) hours past midnight in UTC.
        0 2,14 * * * : every 12 hours at (2,14) hours past midnight in UTC.
        0 2 * * *    : once a day at 2 past midnight in UTC.
        0 2 * * 0    : once a week every Sunday at 2 past midnight in UTC.
        0 2 8 * *    : once a month on 8th day at 2 past midnight in UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#text SpannerBackupSchedule#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleSpecCronSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerBackupScheduleSpecCronSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleSpecCronSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d91597f8fef16477b9b1733497ffc695f6acf5d4894d6714ec805363a4eb2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9ea9c55889841db1d650d0fa4fd23fe993b3c65be8f435a8d6800e15ced18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpannerBackupScheduleSpecCronSpec]:
        return typing.cast(typing.Optional[SpannerBackupScheduleSpecCronSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpannerBackupScheduleSpecCronSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd1738df417557e4d9b3112a787ec032fbd885e61e3d85411530b1914b565ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpannerBackupScheduleSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11de7b3e8627a79646f1b4bce3a826a8a55b53e18894d32145c63e43398c05c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCronSpec")
    def put_cron_spec(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Textual representation of the crontab. User can customize the backup frequency and the backup version time using the cron expression. The version time must be in UTC timzeone. The backup will contain an externally consistent copy of the database at the version time. Allowed frequencies are 12 hour, 1 day, 1 week and 1 month. Examples of valid cron specifications: 0 2/12 * * * : every 12 hours at (2, 14) hours past midnight in UTC. 0 2,14 * * * : every 12 hours at (2,14) hours past midnight in UTC. 0 2 * * * : once a day at 2 past midnight in UTC. 0 2 * * 0 : once a week every Sunday at 2 past midnight in UTC. 0 2 8 * * : once a month on 8th day at 2 past midnight in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#text SpannerBackupSchedule#text}
        '''
        value = SpannerBackupScheduleSpecCronSpec(text=text)

        return typing.cast(None, jsii.invoke(self, "putCronSpec", [value]))

    @jsii.member(jsii_name="resetCronSpec")
    def reset_cron_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSpec", []))

    @builtins.property
    @jsii.member(jsii_name="cronSpec")
    def cron_spec(self) -> SpannerBackupScheduleSpecCronSpecOutputReference:
        return typing.cast(SpannerBackupScheduleSpecCronSpecOutputReference, jsii.get(self, "cronSpec"))

    @builtins.property
    @jsii.member(jsii_name="cronSpecInput")
    def cron_spec_input(self) -> typing.Optional[SpannerBackupScheduleSpecCronSpec]:
        return typing.cast(typing.Optional[SpannerBackupScheduleSpecCronSpec], jsii.get(self, "cronSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpannerBackupScheduleSpec]:
        return typing.cast(typing.Optional[SpannerBackupScheduleSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SpannerBackupScheduleSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de38b69b2df612c5aebecd0400669d69207648d326be5ccc6c8232248568da47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SpannerBackupScheduleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#create SpannerBackupSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#delete SpannerBackupSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#update SpannerBackupSchedule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa34c13ece8d75a5060598e2c1928945b34cb303b83f492597f6c050f4c0d04)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#create SpannerBackupSchedule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#delete SpannerBackupSchedule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/spanner_backup_schedule#update SpannerBackupSchedule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpannerBackupScheduleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpannerBackupScheduleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.spannerBackupSchedule.SpannerBackupScheduleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aa328111b4fe81a7c5bcf6a8d696839b252890822cdc60872a0ff0e094ce8e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5f2e210d37c43994e620f9a9aeec58f99c129443f2d2eb2ab3092fee13e5599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea52cfc35ceb4add605c2f19a3bed231da1af9f857523ce4f509199483a719d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93155901c3aed53923f7169a8fe5b019e4955315b77b7e2b26a443a944395347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerBackupScheduleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerBackupScheduleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerBackupScheduleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d3738d010aceff04f55b7a81dd29321f72a440138b6bde96d4e2c1c51c2214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpannerBackupSchedule",
    "SpannerBackupScheduleConfig",
    "SpannerBackupScheduleEncryptionConfig",
    "SpannerBackupScheduleEncryptionConfigOutputReference",
    "SpannerBackupScheduleFullBackupSpec",
    "SpannerBackupScheduleFullBackupSpecOutputReference",
    "SpannerBackupScheduleIncrementalBackupSpec",
    "SpannerBackupScheduleIncrementalBackupSpecOutputReference",
    "SpannerBackupScheduleSpec",
    "SpannerBackupScheduleSpecCronSpec",
    "SpannerBackupScheduleSpecCronSpecOutputReference",
    "SpannerBackupScheduleSpecOutputReference",
    "SpannerBackupScheduleTimeouts",
    "SpannerBackupScheduleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__afa86559058b6f7dbf87964d58adf3f22abf76bd4911c3cd6d0c0ffc27e7c2d8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    instance: builtins.str,
    retention_duration: builtins.str,
    encryption_config: typing.Optional[typing.Union[SpannerBackupScheduleEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    full_backup_spec: typing.Optional[typing.Union[SpannerBackupScheduleFullBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_backup_spec: typing.Optional[typing.Union[SpannerBackupScheduleIncrementalBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[SpannerBackupScheduleSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SpannerBackupScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__eb16ee2f30b98812fb4a1b88ec449f16ccc8d551e3c0e2fdac358db561d54ea2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2193553a95a1261aae3c69c7c27d67152947a491972189a596b4103841110bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6f8457afe5e2b89cb47c52c8758b8120efd5009e083cf349f36cf8aa5d5556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a04b1d5e480a425d324ab328cf9b636a79427c91cef8bc6df7d4b94535f3b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41277eb0274e3085feef4c073ec6261fd9a2959c2267eae50bc5bed5abdab27e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0bd780300b6d9fce61a886c2690f26c89b968d13269b7a4c120dfd4c7acdfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a12768400c392f9f7826f257280115b585d42c20304175a5b56824eda568e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ca35640328e0cde1d82c35ff62ab49a1d1706913bd874ddb40253e7139ea43(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    instance: builtins.str,
    retention_duration: builtins.str,
    encryption_config: typing.Optional[typing.Union[SpannerBackupScheduleEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    full_backup_spec: typing.Optional[typing.Union[SpannerBackupScheduleFullBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_backup_spec: typing.Optional[typing.Union[SpannerBackupScheduleIncrementalBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[SpannerBackupScheduleSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SpannerBackupScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7563a05c6780132debdab328eb989dbe802a5115dc3b6dda16ca12216dc7bdae(
    *,
    encryption_type: builtins.str,
    kms_key_name: typing.Optional[builtins.str] = None,
    kms_key_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f1ee5dbc3b470c05f95905cd35ebcb46b26f2c3178aa6ab629fb33e4ed21c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e61bcbe3141c072f6644e0e98b7698de23d15117e37e6c5806857f97f4018f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a8eab876fe7bfc01ca093fd66f236db3424c2e4b4fa1c2a0bd303b72d928dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2816fc6e1bd6e2df9484a7484822ee26bcf5fe05588921df52d9c06d2f56f55b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fba7670ee92750f795fed374e4db047b6d11e2459fc119c9d1dbc6316c43966(
    value: typing.Optional[SpannerBackupScheduleEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44166a51c0c95bb682ef67629d6ea3956444743358ce6e4ebd6d559d46cdc1eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a4e8995ae845cc570645ee94a64d67e0ed081469614165da1bf92a3d0251ba(
    value: typing.Optional[SpannerBackupScheduleFullBackupSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce155c5e0e0d0bffb3fc9805efee64813153a9b204b6409e85f6afe79be8052e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079d410507109efe08928f37afc5cc9bd6e912171ee93776933ebba0368d4f7f(
    value: typing.Optional[SpannerBackupScheduleIncrementalBackupSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bdb6a11284ab5b0428da2c09d55daf6cada7d05027c70f04b26cf35ea9884e(
    *,
    cron_spec: typing.Optional[typing.Union[SpannerBackupScheduleSpecCronSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0711e4ec53db1f576d1afd7ddb8cc1c6c677901a8b300b55ec30e3d443ddb374(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d91597f8fef16477b9b1733497ffc695f6acf5d4894d6714ec805363a4eb2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9ea9c55889841db1d650d0fa4fd23fe993b3c65be8f435a8d6800e15ced18d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd1738df417557e4d9b3112a787ec032fbd885e61e3d85411530b1914b565ad(
    value: typing.Optional[SpannerBackupScheduleSpecCronSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11de7b3e8627a79646f1b4bce3a826a8a55b53e18894d32145c63e43398c05c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de38b69b2df612c5aebecd0400669d69207648d326be5ccc6c8232248568da47(
    value: typing.Optional[SpannerBackupScheduleSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa34c13ece8d75a5060598e2c1928945b34cb303b83f492597f6c050f4c0d04(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa328111b4fe81a7c5bcf6a8d696839b252890822cdc60872a0ff0e094ce8e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f2e210d37c43994e620f9a9aeec58f99c129443f2d2eb2ab3092fee13e5599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea52cfc35ceb4add605c2f19a3bed231da1af9f857523ce4f509199483a719d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93155901c3aed53923f7169a8fe5b019e4955315b77b7e2b26a443a944395347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d3738d010aceff04f55b7a81dd29321f72a440138b6bde96d4e2c1c51c2214(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpannerBackupScheduleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
