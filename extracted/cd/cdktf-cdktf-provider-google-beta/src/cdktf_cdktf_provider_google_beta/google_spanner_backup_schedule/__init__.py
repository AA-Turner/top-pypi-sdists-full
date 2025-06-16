r'''
# `google_spanner_backup_schedule`

Refer to the Terraform Registry for docs: [`google_spanner_backup_schedule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule).
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


class GoogleSpannerBackupSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule google_spanner_backup_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        instance: builtins.str,
        retention_duration: builtins.str,
        encryption_config: typing.Optional[typing.Union["GoogleSpannerBackupScheduleEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        full_backup_spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleFullBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_backup_spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleIncrementalBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleSpannerBackupScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule google_spanner_backup_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database to create the backup schedule on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#database GoogleSpannerBackupSchedule#database}
        :param instance: The instance to create the database on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#instance GoogleSpannerBackupSchedule#instance}
        :param retention_duration: At what relative time in the future, compared to its creation time, the backup should be deleted, e.g. keep backups for 7 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. You can set this to a value up to 366 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#retention_duration GoogleSpannerBackupSchedule#retention_duration}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#encryption_config GoogleSpannerBackupSchedule#encryption_config}
        :param full_backup_spec: full_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#full_backup_spec GoogleSpannerBackupSchedule#full_backup_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#id GoogleSpannerBackupSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_backup_spec: incremental_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#incremental_backup_spec GoogleSpannerBackupSchedule#incremental_backup_spec}
        :param name: A unique identifier for the backup schedule, which cannot be changed after the backup schedule is created. Values are of the form [a-z][-a-z0-9]*[a-z0-9]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#name GoogleSpannerBackupSchedule#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#project GoogleSpannerBackupSchedule#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#spec GoogleSpannerBackupSchedule#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#timeouts GoogleSpannerBackupSchedule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b5109aaaf350638c84b5f4f89534de6249489b77180b943dc32fc9175d0b7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleSpannerBackupScheduleConfig(
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
        '''Generates CDKTF code for importing a GoogleSpannerBackupSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleSpannerBackupSchedule to import.
        :param import_from_id: The id of the existing GoogleSpannerBackupSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleSpannerBackupSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded714e7f9200e150cf3989f800ff9f4d49102e9b145a6c6ef18eb18947f739a)
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
    ) -> None:
        '''
        :param encryption_type: The encryption type of backups created by the backup schedule. Possible values are USE_DATABASE_ENCRYPTION, GOOGLE_DEFAULT_ENCRYPTION, or CUSTOMER_MANAGED_ENCRYPTION. If you use CUSTOMER_MANAGED_ENCRYPTION, you must specify a kmsKeyName. If your backup type is incremental-backup, the encryption type must be GOOGLE_DEFAULT_ENCRYPTION. Possible values: ["USE_DATABASE_ENCRYPTION", "GOOGLE_DEFAULT_ENCRYPTION", "CUSTOMER_MANAGED_ENCRYPTION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#encryption_type GoogleSpannerBackupSchedule#encryption_type}
        :param kms_key_name: The resource name of the Cloud KMS key to use for encryption. Format: 'projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#kms_key_name GoogleSpannerBackupSchedule#kms_key_name}
        '''
        value = GoogleSpannerBackupScheduleEncryptionConfig(
            encryption_type=encryption_type, kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putFullBackupSpec")
    def put_full_backup_spec(self) -> None:
        value = GoogleSpannerBackupScheduleFullBackupSpec()

        return typing.cast(None, jsii.invoke(self, "putFullBackupSpec", [value]))

    @jsii.member(jsii_name="putIncrementalBackupSpec")
    def put_incremental_backup_spec(self) -> None:
        value = GoogleSpannerBackupScheduleIncrementalBackupSpec()

        return typing.cast(None, jsii.invoke(self, "putIncrementalBackupSpec", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        cron_spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleSpecCronSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_spec: cron_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#cron_spec GoogleSpannerBackupSchedule#cron_spec}
        '''
        value = GoogleSpannerBackupScheduleSpec(cron_spec=cron_spec)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#create GoogleSpannerBackupSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#delete GoogleSpannerBackupSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#update GoogleSpannerBackupSchedule#update}.
        '''
        value = GoogleSpannerBackupScheduleTimeouts(
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
    ) -> "GoogleSpannerBackupScheduleEncryptionConfigOutputReference":
        return typing.cast("GoogleSpannerBackupScheduleEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="fullBackupSpec")
    def full_backup_spec(
        self,
    ) -> "GoogleSpannerBackupScheduleFullBackupSpecOutputReference":
        return typing.cast("GoogleSpannerBackupScheduleFullBackupSpecOutputReference", jsii.get(self, "fullBackupSpec"))

    @builtins.property
    @jsii.member(jsii_name="incrementalBackupSpec")
    def incremental_backup_spec(
        self,
    ) -> "GoogleSpannerBackupScheduleIncrementalBackupSpecOutputReference":
        return typing.cast("GoogleSpannerBackupScheduleIncrementalBackupSpecOutputReference", jsii.get(self, "incrementalBackupSpec"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "GoogleSpannerBackupScheduleSpecOutputReference":
        return typing.cast("GoogleSpannerBackupScheduleSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleSpannerBackupScheduleTimeoutsOutputReference":
        return typing.cast("GoogleSpannerBackupScheduleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["GoogleSpannerBackupScheduleEncryptionConfig"]:
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fullBackupSpecInput")
    def full_backup_spec_input(
        self,
    ) -> typing.Optional["GoogleSpannerBackupScheduleFullBackupSpec"]:
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleFullBackupSpec"], jsii.get(self, "fullBackupSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalBackupSpecInput")
    def incremental_backup_spec_input(
        self,
    ) -> typing.Optional["GoogleSpannerBackupScheduleIncrementalBackupSpec"]:
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleIncrementalBackupSpec"], jsii.get(self, "incrementalBackupSpecInput"))

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
    def spec_input(self) -> typing.Optional["GoogleSpannerBackupScheduleSpec"]:
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSpannerBackupScheduleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSpannerBackupScheduleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bfc00e5270974a14c5017bb07d7561658c819b84ee3b7c9571e4fc164ad76b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed233c37297eaeaed6e34fb9001a598131c90c975605c560626d221775c8dfa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27378ca374faa3ad20d4967426549e407234e2843412980fc51196e606fcb887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6583403c3c99923675c63dc020ed5c5ea9887863120d77afef6bee167ce4f9ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591f28b8af0e4f5cab18f78fc8c4d07515ff4ffa69fa16884107af630f3b2d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDuration")
    def retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionDuration"))

    @retention_duration.setter
    def retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a33a9d1c55ccb2fd7ab1e6dd13cb30c457c377f7bdf14f863ef090ad9f5687c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDuration", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleConfig",
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
class GoogleSpannerBackupScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        encryption_config: typing.Optional[typing.Union["GoogleSpannerBackupScheduleEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        full_backup_spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleFullBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_backup_spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleIncrementalBackupSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleSpannerBackupScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database to create the backup schedule on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#database GoogleSpannerBackupSchedule#database}
        :param instance: The instance to create the database on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#instance GoogleSpannerBackupSchedule#instance}
        :param retention_duration: At what relative time in the future, compared to its creation time, the backup should be deleted, e.g. keep backups for 7 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. You can set this to a value up to 366 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#retention_duration GoogleSpannerBackupSchedule#retention_duration}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#encryption_config GoogleSpannerBackupSchedule#encryption_config}
        :param full_backup_spec: full_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#full_backup_spec GoogleSpannerBackupSchedule#full_backup_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#id GoogleSpannerBackupSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_backup_spec: incremental_backup_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#incremental_backup_spec GoogleSpannerBackupSchedule#incremental_backup_spec}
        :param name: A unique identifier for the backup schedule, which cannot be changed after the backup schedule is created. Values are of the form [a-z][-a-z0-9]*[a-z0-9]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#name GoogleSpannerBackupSchedule#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#project GoogleSpannerBackupSchedule#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#spec GoogleSpannerBackupSchedule#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#timeouts GoogleSpannerBackupSchedule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleSpannerBackupScheduleEncryptionConfig(**encryption_config)
        if isinstance(full_backup_spec, dict):
            full_backup_spec = GoogleSpannerBackupScheduleFullBackupSpec(**full_backup_spec)
        if isinstance(incremental_backup_spec, dict):
            incremental_backup_spec = GoogleSpannerBackupScheduleIncrementalBackupSpec(**incremental_backup_spec)
        if isinstance(spec, dict):
            spec = GoogleSpannerBackupScheduleSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = GoogleSpannerBackupScheduleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d548e826f0cece7874fb16e0b28f0f15447753979d5b9f6407713d58d8b2e66)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#database GoogleSpannerBackupSchedule#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''The instance to create the database on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#instance GoogleSpannerBackupSchedule#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_duration(self) -> builtins.str:
        '''At what relative time in the future, compared to its creation time, the backup should be deleted, e.g. keep backups for 7 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. You can set this to a value up to 366 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#retention_duration GoogleSpannerBackupSchedule#retention_duration}
        '''
        result = self._values.get("retention_duration")
        assert result is not None, "Required property 'retention_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleSpannerBackupScheduleEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#encryption_config GoogleSpannerBackupSchedule#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleEncryptionConfig"], result)

    @builtins.property
    def full_backup_spec(
        self,
    ) -> typing.Optional["GoogleSpannerBackupScheduleFullBackupSpec"]:
        '''full_backup_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#full_backup_spec GoogleSpannerBackupSchedule#full_backup_spec}
        '''
        result = self._values.get("full_backup_spec")
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleFullBackupSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#id GoogleSpannerBackupSchedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_backup_spec(
        self,
    ) -> typing.Optional["GoogleSpannerBackupScheduleIncrementalBackupSpec"]:
        '''incremental_backup_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#incremental_backup_spec GoogleSpannerBackupSchedule#incremental_backup_spec}
        '''
        result = self._values.get("incremental_backup_spec")
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleIncrementalBackupSpec"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the backup schedule, which cannot be changed after the backup schedule is created.

        Values are of the form [a-z][-a-z0-9]*[a-z0-9].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#name GoogleSpannerBackupSchedule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#project GoogleSpannerBackupSchedule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["GoogleSpannerBackupScheduleSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#spec GoogleSpannerBackupSchedule#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleSpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleSpannerBackupScheduleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#timeouts GoogleSpannerBackupSchedule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"encryption_type": "encryptionType", "kms_key_name": "kmsKeyName"},
)
class GoogleSpannerBackupScheduleEncryptionConfig:
    def __init__(
        self,
        *,
        encryption_type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_type: The encryption type of backups created by the backup schedule. Possible values are USE_DATABASE_ENCRYPTION, GOOGLE_DEFAULT_ENCRYPTION, or CUSTOMER_MANAGED_ENCRYPTION. If you use CUSTOMER_MANAGED_ENCRYPTION, you must specify a kmsKeyName. If your backup type is incremental-backup, the encryption type must be GOOGLE_DEFAULT_ENCRYPTION. Possible values: ["USE_DATABASE_ENCRYPTION", "GOOGLE_DEFAULT_ENCRYPTION", "CUSTOMER_MANAGED_ENCRYPTION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#encryption_type GoogleSpannerBackupSchedule#encryption_type}
        :param kms_key_name: The resource name of the Cloud KMS key to use for encryption. Format: 'projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#kms_key_name GoogleSpannerBackupSchedule#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa156e205b3712f7216d6a5d2a0a06ee3d98e76dc67a91e83fd9e6c1b4a6514)
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_type": encryption_type,
        }
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def encryption_type(self) -> builtins.str:
        '''The encryption type of backups created by the backup schedule.

        Possible values are USE_DATABASE_ENCRYPTION, GOOGLE_DEFAULT_ENCRYPTION, or CUSTOMER_MANAGED_ENCRYPTION.
        If you use CUSTOMER_MANAGED_ENCRYPTION, you must specify a kmsKeyName.
        If your backup type is incremental-backup, the encryption type must be GOOGLE_DEFAULT_ENCRYPTION. Possible values: ["USE_DATABASE_ENCRYPTION", "GOOGLE_DEFAULT_ENCRYPTION", "CUSTOMER_MANAGED_ENCRYPTION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#encryption_type GoogleSpannerBackupSchedule#encryption_type}
        '''
        result = self._values.get("encryption_type")
        assert result is not None, "Required property 'encryption_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Cloud KMS key to use for encryption. Format: 'projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#kms_key_name GoogleSpannerBackupSchedule#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSpannerBackupScheduleEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__361d36e28b5d0a5d891aca002c5dede5d8817e81de38dcb5469cfa57b7270f2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e29ef058f8e31f52e99378fe0b97c52e350f29ce05cc69128e703bb1359a60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e473ddf435360c6a91350939c47b7b6797667155d65a00a0e596012119db2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSpannerBackupScheduleEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleSpannerBackupScheduleEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSpannerBackupScheduleEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dc2b681f575da25cbb1c07ca515c0a3418aa954faff7053579a1391e6b2874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleFullBackupSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleSpannerBackupScheduleFullBackupSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleFullBackupSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSpannerBackupScheduleFullBackupSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleFullBackupSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a50d145a9b678f5f9731259aa8f48814051f50a5253819748abd9e0a6c958cb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSpannerBackupScheduleFullBackupSpec]:
        return typing.cast(typing.Optional[GoogleSpannerBackupScheduleFullBackupSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSpannerBackupScheduleFullBackupSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e39c270de7d306eae174631b3c7831d400250d8cf4f1c1f28fe62cc5544086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleIncrementalBackupSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleSpannerBackupScheduleIncrementalBackupSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleIncrementalBackupSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSpannerBackupScheduleIncrementalBackupSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleIncrementalBackupSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71501766f75a696616b3d610e71857166c8eeef4d3c894ce9de4a71e98a5ccd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSpannerBackupScheduleIncrementalBackupSpec]:
        return typing.cast(typing.Optional[GoogleSpannerBackupScheduleIncrementalBackupSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSpannerBackupScheduleIncrementalBackupSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e018ffa8399ee0ce5b4849d18ad03ac8dae663acaaf7fbdef2b7d1798cfc0800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleSpec",
    jsii_struct_bases=[],
    name_mapping={"cron_spec": "cronSpec"},
)
class GoogleSpannerBackupScheduleSpec:
    def __init__(
        self,
        *,
        cron_spec: typing.Optional[typing.Union["GoogleSpannerBackupScheduleSpecCronSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_spec: cron_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#cron_spec GoogleSpannerBackupSchedule#cron_spec}
        '''
        if isinstance(cron_spec, dict):
            cron_spec = GoogleSpannerBackupScheduleSpecCronSpec(**cron_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aed504d7150d620515a85ef887a45c392dbbf62ec0b743cccec899e51079c9)
            check_type(argname="argument cron_spec", value=cron_spec, expected_type=type_hints["cron_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_spec is not None:
            self._values["cron_spec"] = cron_spec

    @builtins.property
    def cron_spec(self) -> typing.Optional["GoogleSpannerBackupScheduleSpecCronSpec"]:
        '''cron_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#cron_spec GoogleSpannerBackupSchedule#cron_spec}
        '''
        result = self._values.get("cron_spec")
        return typing.cast(typing.Optional["GoogleSpannerBackupScheduleSpecCronSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleSpecCronSpec",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class GoogleSpannerBackupScheduleSpecCronSpec:
    def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Textual representation of the crontab. User can customize the backup frequency and the backup version time using the cron expression. The version time must be in UTC timzeone. The backup will contain an externally consistent copy of the database at the version time. Allowed frequencies are 12 hour, 1 day, 1 week and 1 month. Examples of valid cron specifications: 0 2/12 * * * : every 12 hours at (2, 14) hours past midnight in UTC. 0 2,14 * * * : every 12 hours at (2,14) hours past midnight in UTC. 0 2 * * * : once a day at 2 past midnight in UTC. 0 2 * * 0 : once a week every Sunday at 2 past midnight in UTC. 0 2 8 * * : once a month on 8th day at 2 past midnight in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#text GoogleSpannerBackupSchedule#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c06b24f6ea3c1e77f642615db6d675601fa7ea8fa7704c335b1503439e97d10)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#text GoogleSpannerBackupSchedule#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleSpecCronSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSpannerBackupScheduleSpecCronSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleSpecCronSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95094071d7651829bfad9b8650fa3076beeddbe1729d284075f64493e08c602b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caab72c2b3e61d490d045afef4c1c964ac438defb0ea647181a0696d661fccc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSpannerBackupScheduleSpecCronSpec]:
        return typing.cast(typing.Optional[GoogleSpannerBackupScheduleSpecCronSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSpannerBackupScheduleSpecCronSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e81e1f8efbc4a43f8986605d51f461b1476d88361c78ea5ce6420f7078fa931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSpannerBackupScheduleSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12e1b1e7bd655e223dcf901f498bbfd33155830ef3f7eb2df7c442f74959ca65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCronSpec")
    def put_cron_spec(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Textual representation of the crontab. User can customize the backup frequency and the backup version time using the cron expression. The version time must be in UTC timzeone. The backup will contain an externally consistent copy of the database at the version time. Allowed frequencies are 12 hour, 1 day, 1 week and 1 month. Examples of valid cron specifications: 0 2/12 * * * : every 12 hours at (2, 14) hours past midnight in UTC. 0 2,14 * * * : every 12 hours at (2,14) hours past midnight in UTC. 0 2 * * * : once a day at 2 past midnight in UTC. 0 2 * * 0 : once a week every Sunday at 2 past midnight in UTC. 0 2 8 * * : once a month on 8th day at 2 past midnight in UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#text GoogleSpannerBackupSchedule#text}
        '''
        value = GoogleSpannerBackupScheduleSpecCronSpec(text=text)

        return typing.cast(None, jsii.invoke(self, "putCronSpec", [value]))

    @jsii.member(jsii_name="resetCronSpec")
    def reset_cron_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSpec", []))

    @builtins.property
    @jsii.member(jsii_name="cronSpec")
    def cron_spec(self) -> GoogleSpannerBackupScheduleSpecCronSpecOutputReference:
        return typing.cast(GoogleSpannerBackupScheduleSpecCronSpecOutputReference, jsii.get(self, "cronSpec"))

    @builtins.property
    @jsii.member(jsii_name="cronSpecInput")
    def cron_spec_input(
        self,
    ) -> typing.Optional[GoogleSpannerBackupScheduleSpecCronSpec]:
        return typing.cast(typing.Optional[GoogleSpannerBackupScheduleSpecCronSpec], jsii.get(self, "cronSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSpannerBackupScheduleSpec]:
        return typing.cast(typing.Optional[GoogleSpannerBackupScheduleSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSpannerBackupScheduleSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b35413acb12995ba2fffb375bf304133945ac209fa6fe4554a6bf2a324f0c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleSpannerBackupScheduleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#create GoogleSpannerBackupSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#delete GoogleSpannerBackupSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#update GoogleSpannerBackupSchedule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c8461e9aa6607ee6b59b978a6835c06b4376a9add489692c12efc00512a617)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#create GoogleSpannerBackupSchedule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#delete GoogleSpannerBackupSchedule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_spanner_backup_schedule#update GoogleSpannerBackupSchedule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSpannerBackupScheduleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSpannerBackupScheduleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSpannerBackupSchedule.GoogleSpannerBackupScheduleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f09893b1a89d4408485652951ab84e6f94387ad1a688484e223864be64c42502)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f4ad4a837c3e2708134aaa84d4bb45c6cbc7241c45de0a8c862fc603bce38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1805a80cc37da26a05802d8955c792d8e1670ab3e90c2cce9d5a0639ab464b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb834e6694455dea1ca7c14ba2086259e763960e3edf7e237a0c7696f01d7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSpannerBackupScheduleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSpannerBackupScheduleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSpannerBackupScheduleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce8391a7574e152e4793dc37e9a08c8545c9e06ba257612458563683cb9c301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleSpannerBackupSchedule",
    "GoogleSpannerBackupScheduleConfig",
    "GoogleSpannerBackupScheduleEncryptionConfig",
    "GoogleSpannerBackupScheduleEncryptionConfigOutputReference",
    "GoogleSpannerBackupScheduleFullBackupSpec",
    "GoogleSpannerBackupScheduleFullBackupSpecOutputReference",
    "GoogleSpannerBackupScheduleIncrementalBackupSpec",
    "GoogleSpannerBackupScheduleIncrementalBackupSpecOutputReference",
    "GoogleSpannerBackupScheduleSpec",
    "GoogleSpannerBackupScheduleSpecCronSpec",
    "GoogleSpannerBackupScheduleSpecCronSpecOutputReference",
    "GoogleSpannerBackupScheduleSpecOutputReference",
    "GoogleSpannerBackupScheduleTimeouts",
    "GoogleSpannerBackupScheduleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__39b5109aaaf350638c84b5f4f89534de6249489b77180b943dc32fc9175d0b7c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    instance: builtins.str,
    retention_duration: builtins.str,
    encryption_config: typing.Optional[typing.Union[GoogleSpannerBackupScheduleEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    full_backup_spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleFullBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_backup_spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleIncrementalBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleSpannerBackupScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ded714e7f9200e150cf3989f800ff9f4d49102e9b145a6c6ef18eb18947f739a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bfc00e5270974a14c5017bb07d7561658c819b84ee3b7c9571e4fc164ad76b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed233c37297eaeaed6e34fb9001a598131c90c975605c560626d221775c8dfa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27378ca374faa3ad20d4967426549e407234e2843412980fc51196e606fcb887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6583403c3c99923675c63dc020ed5c5ea9887863120d77afef6bee167ce4f9ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591f28b8af0e4f5cab18f78fc8c4d07515ff4ffa69fa16884107af630f3b2d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a33a9d1c55ccb2fd7ab1e6dd13cb30c457c377f7bdf14f863ef090ad9f5687c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d548e826f0cece7874fb16e0b28f0f15447753979d5b9f6407713d58d8b2e66(
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
    encryption_config: typing.Optional[typing.Union[GoogleSpannerBackupScheduleEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    full_backup_spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleFullBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_backup_spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleIncrementalBackupSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleSpannerBackupScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa156e205b3712f7216d6a5d2a0a06ee3d98e76dc67a91e83fd9e6c1b4a6514(
    *,
    encryption_type: builtins.str,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361d36e28b5d0a5d891aca002c5dede5d8817e81de38dcb5469cfa57b7270f2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e29ef058f8e31f52e99378fe0b97c52e350f29ce05cc69128e703bb1359a60a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e473ddf435360c6a91350939c47b7b6797667155d65a00a0e596012119db2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dc2b681f575da25cbb1c07ca515c0a3418aa954faff7053579a1391e6b2874(
    value: typing.Optional[GoogleSpannerBackupScheduleEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50d145a9b678f5f9731259aa8f48814051f50a5253819748abd9e0a6c958cb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e39c270de7d306eae174631b3c7831d400250d8cf4f1c1f28fe62cc5544086(
    value: typing.Optional[GoogleSpannerBackupScheduleFullBackupSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71501766f75a696616b3d610e71857166c8eeef4d3c894ce9de4a71e98a5ccd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e018ffa8399ee0ce5b4849d18ad03ac8dae663acaaf7fbdef2b7d1798cfc0800(
    value: typing.Optional[GoogleSpannerBackupScheduleIncrementalBackupSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aed504d7150d620515a85ef887a45c392dbbf62ec0b743cccec899e51079c9(
    *,
    cron_spec: typing.Optional[typing.Union[GoogleSpannerBackupScheduleSpecCronSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c06b24f6ea3c1e77f642615db6d675601fa7ea8fa7704c335b1503439e97d10(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95094071d7651829bfad9b8650fa3076beeddbe1729d284075f64493e08c602b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caab72c2b3e61d490d045afef4c1c964ac438defb0ea647181a0696d661fccc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e81e1f8efbc4a43f8986605d51f461b1476d88361c78ea5ce6420f7078fa931(
    value: typing.Optional[GoogleSpannerBackupScheduleSpecCronSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e1b1e7bd655e223dcf901f498bbfd33155830ef3f7eb2df7c442f74959ca65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b35413acb12995ba2fffb375bf304133945ac209fa6fe4554a6bf2a324f0c88(
    value: typing.Optional[GoogleSpannerBackupScheduleSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c8461e9aa6607ee6b59b978a6835c06b4376a9add489692c12efc00512a617(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09893b1a89d4408485652951ab84e6f94387ad1a688484e223864be64c42502(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f4ad4a837c3e2708134aaa84d4bb45c6cbc7241c45de0a8c862fc603bce38a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1805a80cc37da26a05802d8955c792d8e1670ab3e90c2cce9d5a0639ab464b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb834e6694455dea1ca7c14ba2086259e763960e3edf7e237a0c7696f01d7d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce8391a7574e152e4793dc37e9a08c8545c9e06ba257612458563683cb9c301(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSpannerBackupScheduleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
