r'''
# `google_dataform_repository_release_config`

Refer to the Terraform Registry for docs: [`google_dataform_repository_release_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config).
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


class GoogleDataformRepositoryReleaseConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config google_dataform_repository_release_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        git_commitish: builtins.str,
        name: builtins.str,
        code_compilation_config: typing.Optional[typing.Union["GoogleDataformRepositoryReleaseConfigCodeCompilationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cron_schedule: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryReleaseConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config google_dataform_repository_release_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param git_commitish: Git commit/tag/branch name at which the repository should be compiled. Must exist in the remote repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#git_commitish GoogleDataformRepositoryReleaseConfig#git_commitish}
        :param name: The release's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#name GoogleDataformRepositoryReleaseConfig#name}
        :param code_compilation_config: code_compilation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#code_compilation_config GoogleDataformRepositoryReleaseConfig#code_compilation_config}
        :param cron_schedule: Optional. Optional schedule (in cron format) for automatic creation of compilation results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#cron_schedule GoogleDataformRepositoryReleaseConfig#cron_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#id GoogleDataformRepositoryReleaseConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#project GoogleDataformRepositoryReleaseConfig#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#region GoogleDataformRepositoryReleaseConfig#region}
        :param repository: A reference to the Dataform repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#repository GoogleDataformRepositoryReleaseConfig#repository}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#timeouts GoogleDataformRepositoryReleaseConfig#timeouts}
        :param time_zone: Optional. Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#time_zone GoogleDataformRepositoryReleaseConfig#time_zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357cab32058dba0b3d509ee33508f94e39f4bb0fe5b53071368460583e565c8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataformRepositoryReleaseConfigConfig(
            git_commitish=git_commitish,
            name=name,
            code_compilation_config=code_compilation_config,
            cron_schedule=cron_schedule,
            id=id,
            project=project,
            region=region,
            repository=repository,
            timeouts=timeouts,
            time_zone=time_zone,
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
        '''Generates CDKTF code for importing a GoogleDataformRepositoryReleaseConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataformRepositoryReleaseConfig to import.
        :param import_from_id: The id of the existing GoogleDataformRepositoryReleaseConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataformRepositoryReleaseConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cd3f4cb5608731b88e543a180e6bde65c47b49d4791c4c5c0763cc199e759e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCodeCompilationConfig")
    def put_code_compilation_config(
        self,
        *,
        assertion_schema: typing.Optional[builtins.str] = None,
        database_suffix: typing.Optional[builtins.str] = None,
        default_database: typing.Optional[builtins.str] = None,
        default_location: typing.Optional[builtins.str] = None,
        default_schema: typing.Optional[builtins.str] = None,
        schema_suffix: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param assertion_schema: Optional. The default schema (BigQuery dataset ID) for assertions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#assertion_schema GoogleDataformRepositoryReleaseConfig#assertion_schema}
        :param database_suffix: Optional. The suffix that should be appended to all database (Google Cloud project ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#database_suffix GoogleDataformRepositoryReleaseConfig#database_suffix}
        :param default_database: Optional. The default database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_database GoogleDataformRepositoryReleaseConfig#default_database}
        :param default_location: Optional. The default BigQuery location to use. Defaults to "US". See the BigQuery docs for a full list of locations: https://cloud.google.com/bigquery/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_location GoogleDataformRepositoryReleaseConfig#default_location}
        :param default_schema: Optional. The default schema (BigQuery dataset ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_schema GoogleDataformRepositoryReleaseConfig#default_schema}
        :param schema_suffix: Optional. The suffix that should be appended to all schema (BigQuery dataset ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#schema_suffix GoogleDataformRepositoryReleaseConfig#schema_suffix}
        :param table_prefix: Optional. The prefix that should be prepended to all table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#table_prefix GoogleDataformRepositoryReleaseConfig#table_prefix}
        :param vars: Optional. User-defined variables that are made available to project code during compilation. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#vars GoogleDataformRepositoryReleaseConfig#vars}
        '''
        value = GoogleDataformRepositoryReleaseConfigCodeCompilationConfig(
            assertion_schema=assertion_schema,
            database_suffix=database_suffix,
            default_database=default_database,
            default_location=default_location,
            default_schema=default_schema,
            schema_suffix=schema_suffix,
            table_prefix=table_prefix,
            vars=vars,
        )

        return typing.cast(None, jsii.invoke(self, "putCodeCompilationConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#create GoogleDataformRepositoryReleaseConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#delete GoogleDataformRepositoryReleaseConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#update GoogleDataformRepositoryReleaseConfig#update}.
        '''
        value = GoogleDataformRepositoryReleaseConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCodeCompilationConfig")
    def reset_code_compilation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeCompilationConfig", []))

    @jsii.member(jsii_name="resetCronSchedule")
    def reset_cron_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSchedule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

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
    @jsii.member(jsii_name="codeCompilationConfig")
    def code_compilation_config(
        self,
    ) -> "GoogleDataformRepositoryReleaseConfigCodeCompilationConfigOutputReference":
        return typing.cast("GoogleDataformRepositoryReleaseConfigCodeCompilationConfigOutputReference", jsii.get(self, "codeCompilationConfig"))

    @builtins.property
    @jsii.member(jsii_name="recentScheduledReleaseRecords")
    def recent_scheduled_release_records(
        self,
    ) -> "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsList":
        return typing.cast("GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsList", jsii.get(self, "recentScheduledReleaseRecords"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDataformRepositoryReleaseConfigTimeoutsOutputReference":
        return typing.cast("GoogleDataformRepositoryReleaseConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="codeCompilationConfigInput")
    def code_compilation_config_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryReleaseConfigCodeCompilationConfig"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryReleaseConfigCodeCompilationConfig"], jsii.get(self, "codeCompilationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cronScheduleInput")
    def cron_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="gitCommitishInput")
    def git_commitish_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitCommitishInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryReleaseConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryReleaseConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="cronSchedule")
    def cron_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSchedule"))

    @cron_schedule.setter
    def cron_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25eba99fad74a7480b599e27dc69f3e5ea08af60074c38b924d2df8ed4a8fd79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitCommitish")
    def git_commitish(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitCommitish"))

    @git_commitish.setter
    def git_commitish(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14433022a33b2a5fd593600966795fb201c89f1635520c200d48011fa70c3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitCommitish", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0d98d09d5ca70fb48823162f6d5876ab546bb6a8ec3cc9bc94a0cd72e2eaff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4700a6cffe41e6dbe16092c3f93d1557a133ad19c066928c593e95a85eb950a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27141e5a9362a0dead790c8fe19256990c3d55a896b19a934f8486b324c74943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f449928715081fce52fa94127d169a5fe004ddd726f72775f8417d1cb939b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c846162db5414fcd2297b956002accd42c7ce1a05528c5e2331d223c2b9e0f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b611ed0c73da08fa34313a7637789c0b0dfaa0600da932d3deada112bee1a37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigCodeCompilationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "assertion_schema": "assertionSchema",
        "database_suffix": "databaseSuffix",
        "default_database": "defaultDatabase",
        "default_location": "defaultLocation",
        "default_schema": "defaultSchema",
        "schema_suffix": "schemaSuffix",
        "table_prefix": "tablePrefix",
        "vars": "vars",
    },
)
class GoogleDataformRepositoryReleaseConfigCodeCompilationConfig:
    def __init__(
        self,
        *,
        assertion_schema: typing.Optional[builtins.str] = None,
        database_suffix: typing.Optional[builtins.str] = None,
        default_database: typing.Optional[builtins.str] = None,
        default_location: typing.Optional[builtins.str] = None,
        default_schema: typing.Optional[builtins.str] = None,
        schema_suffix: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param assertion_schema: Optional. The default schema (BigQuery dataset ID) for assertions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#assertion_schema GoogleDataformRepositoryReleaseConfig#assertion_schema}
        :param database_suffix: Optional. The suffix that should be appended to all database (Google Cloud project ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#database_suffix GoogleDataformRepositoryReleaseConfig#database_suffix}
        :param default_database: Optional. The default database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_database GoogleDataformRepositoryReleaseConfig#default_database}
        :param default_location: Optional. The default BigQuery location to use. Defaults to "US". See the BigQuery docs for a full list of locations: https://cloud.google.com/bigquery/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_location GoogleDataformRepositoryReleaseConfig#default_location}
        :param default_schema: Optional. The default schema (BigQuery dataset ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_schema GoogleDataformRepositoryReleaseConfig#default_schema}
        :param schema_suffix: Optional. The suffix that should be appended to all schema (BigQuery dataset ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#schema_suffix GoogleDataformRepositoryReleaseConfig#schema_suffix}
        :param table_prefix: Optional. The prefix that should be prepended to all table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#table_prefix GoogleDataformRepositoryReleaseConfig#table_prefix}
        :param vars: Optional. User-defined variables that are made available to project code during compilation. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#vars GoogleDataformRepositoryReleaseConfig#vars}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f95cad5f1785310586588b5e48952dec5f8130029d704327f6e0a1c4870714)
            check_type(argname="argument assertion_schema", value=assertion_schema, expected_type=type_hints["assertion_schema"])
            check_type(argname="argument database_suffix", value=database_suffix, expected_type=type_hints["database_suffix"])
            check_type(argname="argument default_database", value=default_database, expected_type=type_hints["default_database"])
            check_type(argname="argument default_location", value=default_location, expected_type=type_hints["default_location"])
            check_type(argname="argument default_schema", value=default_schema, expected_type=type_hints["default_schema"])
            check_type(argname="argument schema_suffix", value=schema_suffix, expected_type=type_hints["schema_suffix"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            check_type(argname="argument vars", value=vars, expected_type=type_hints["vars"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assertion_schema is not None:
            self._values["assertion_schema"] = assertion_schema
        if database_suffix is not None:
            self._values["database_suffix"] = database_suffix
        if default_database is not None:
            self._values["default_database"] = default_database
        if default_location is not None:
            self._values["default_location"] = default_location
        if default_schema is not None:
            self._values["default_schema"] = default_schema
        if schema_suffix is not None:
            self._values["schema_suffix"] = schema_suffix
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix
        if vars is not None:
            self._values["vars"] = vars

    @builtins.property
    def assertion_schema(self) -> typing.Optional[builtins.str]:
        '''Optional. The default schema (BigQuery dataset ID) for assertions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#assertion_schema GoogleDataformRepositoryReleaseConfig#assertion_schema}
        '''
        result = self._values.get("assertion_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_suffix(self) -> typing.Optional[builtins.str]:
        '''Optional. The suffix that should be appended to all database (Google Cloud project ID) names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#database_suffix GoogleDataformRepositoryReleaseConfig#database_suffix}
        '''
        result = self._values.get("database_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_database(self) -> typing.Optional[builtins.str]:
        '''Optional. The default database (Google Cloud project ID).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_database GoogleDataformRepositoryReleaseConfig#default_database}
        '''
        result = self._values.get("default_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The default BigQuery location to use. Defaults to "US".
        See the BigQuery docs for a full list of locations: https://cloud.google.com/bigquery/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_location GoogleDataformRepositoryReleaseConfig#default_location}
        '''
        result = self._values.get("default_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_schema(self) -> typing.Optional[builtins.str]:
        '''Optional. The default schema (BigQuery dataset ID).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#default_schema GoogleDataformRepositoryReleaseConfig#default_schema}
        '''
        result = self._values.get("default_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_suffix(self) -> typing.Optional[builtins.str]:
        '''Optional. The suffix that should be appended to all schema (BigQuery dataset ID) names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#schema_suffix GoogleDataformRepositoryReleaseConfig#schema_suffix}
        '''
        result = self._values.get("schema_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional. The prefix that should be prepended to all table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#table_prefix GoogleDataformRepositoryReleaseConfig#table_prefix}
        '''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vars(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        User-defined variables that are made available to project code during compilation.
        An object containing a list of "key": value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#vars GoogleDataformRepositoryReleaseConfig#vars}
        '''
        result = self._values.get("vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryReleaseConfigCodeCompilationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryReleaseConfigCodeCompilationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigCodeCompilationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee72f89d42a8f6812ff2e1c3d6baa74928f97349c146c15dbd8bd68196a720fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAssertionSchema")
    def reset_assertion_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssertionSchema", []))

    @jsii.member(jsii_name="resetDatabaseSuffix")
    def reset_database_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseSuffix", []))

    @jsii.member(jsii_name="resetDefaultDatabase")
    def reset_default_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDatabase", []))

    @jsii.member(jsii_name="resetDefaultLocation")
    def reset_default_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLocation", []))

    @jsii.member(jsii_name="resetDefaultSchema")
    def reset_default_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSchema", []))

    @jsii.member(jsii_name="resetSchemaSuffix")
    def reset_schema_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaSuffix", []))

    @jsii.member(jsii_name="resetTablePrefix")
    def reset_table_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablePrefix", []))

    @jsii.member(jsii_name="resetVars")
    def reset_vars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVars", []))

    @builtins.property
    @jsii.member(jsii_name="assertionSchemaInput")
    def assertion_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assertionSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseSuffixInput")
    def database_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDatabaseInput")
    def default_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLocationInput")
    def default_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSchemaInput")
    def default_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSuffixInput")
    def schema_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="varsInput")
    def vars_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "varsInput"))

    @builtins.property
    @jsii.member(jsii_name="assertionSchema")
    def assertion_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assertionSchema"))

    @assertion_schema.setter
    def assertion_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7695e1a6d684adf652832d01e0d37703576bf27e515c54d1b51a39d60b47a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertionSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseSuffix")
    def database_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseSuffix"))

    @database_suffix.setter
    def database_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac625c5c94a214816da118babfb291b0ddea1e08ac5ac7b0064d5f390523c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDatabase")
    def default_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDatabase"))

    @default_database.setter
    def default_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf3e04b5ddc9c3a9d596b0bdbf62aa117337f850ec4df2842a3c625bd680b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLocation")
    def default_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLocation"))

    @default_location.setter
    def default_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9c704bcb24e9a98c9fdce3f8e40b5e53624fde19f1e1deacae9f63e7e2ea07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSchema")
    def default_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSchema"))

    @default_schema.setter
    def default_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd028e5e528c4d680ffee5585668ac8c418b72e57680cd128c4aa8851fd0e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaSuffix")
    def schema_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaSuffix"))

    @schema_suffix.setter
    def schema_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fbc9254fab0fa6f96c4f9b32f2fc6d3964a52d0d75c585e7aaa22dd4b3c5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af762e28643f7fc461ccfdd708d39c30cf8e181b5f426536148adc2e3173f976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vars")
    def vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "vars"))

    @vars.setter
    def vars(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2249b4ee4de378508dc56ddf003c5931ef5fa74c84fbcc9a80f7e3926c50d537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d521ce1771d6b1fd3446285ef0c2c911a2363002c68dafa401caccdd05d43df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "git_commitish": "gitCommitish",
        "name": "name",
        "code_compilation_config": "codeCompilationConfig",
        "cron_schedule": "cronSchedule",
        "id": "id",
        "project": "project",
        "region": "region",
        "repository": "repository",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class GoogleDataformRepositoryReleaseConfigConfig(
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
        git_commitish: builtins.str,
        name: builtins.str,
        code_compilation_config: typing.Optional[typing.Union[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cron_schedule: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryReleaseConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param git_commitish: Git commit/tag/branch name at which the repository should be compiled. Must exist in the remote repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#git_commitish GoogleDataformRepositoryReleaseConfig#git_commitish}
        :param name: The release's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#name GoogleDataformRepositoryReleaseConfig#name}
        :param code_compilation_config: code_compilation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#code_compilation_config GoogleDataformRepositoryReleaseConfig#code_compilation_config}
        :param cron_schedule: Optional. Optional schedule (in cron format) for automatic creation of compilation results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#cron_schedule GoogleDataformRepositoryReleaseConfig#cron_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#id GoogleDataformRepositoryReleaseConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#project GoogleDataformRepositoryReleaseConfig#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#region GoogleDataformRepositoryReleaseConfig#region}
        :param repository: A reference to the Dataform repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#repository GoogleDataformRepositoryReleaseConfig#repository}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#timeouts GoogleDataformRepositoryReleaseConfig#timeouts}
        :param time_zone: Optional. Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#time_zone GoogleDataformRepositoryReleaseConfig#time_zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(code_compilation_config, dict):
            code_compilation_config = GoogleDataformRepositoryReleaseConfigCodeCompilationConfig(**code_compilation_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataformRepositoryReleaseConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c975c43f42c6fa7b6e1c10083ccdc9ffd49e61026acc94672cc296ed9bb1cbac)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument git_commitish", value=git_commitish, expected_type=type_hints["git_commitish"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument code_compilation_config", value=code_compilation_config, expected_type=type_hints["code_compilation_config"])
            check_type(argname="argument cron_schedule", value=cron_schedule, expected_type=type_hints["cron_schedule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "git_commitish": git_commitish,
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
        if code_compilation_config is not None:
            self._values["code_compilation_config"] = code_compilation_config
        if cron_schedule is not None:
            self._values["cron_schedule"] = cron_schedule
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if repository is not None:
            self._values["repository"] = repository
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone

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
    def git_commitish(self) -> builtins.str:
        '''Git commit/tag/branch name at which the repository should be compiled. Must exist in the remote repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#git_commitish GoogleDataformRepositoryReleaseConfig#git_commitish}
        '''
        result = self._values.get("git_commitish")
        assert result is not None, "Required property 'git_commitish' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The release's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#name GoogleDataformRepositoryReleaseConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_compilation_config(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig]:
        '''code_compilation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#code_compilation_config GoogleDataformRepositoryReleaseConfig#code_compilation_config}
        '''
        result = self._values.get("code_compilation_config")
        return typing.cast(typing.Optional[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig], result)

    @builtins.property
    def cron_schedule(self) -> typing.Optional[builtins.str]:
        '''Optional. Optional schedule (in cron format) for automatic creation of compilation results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#cron_schedule GoogleDataformRepositoryReleaseConfig#cron_schedule}
        '''
        result = self._values.get("cron_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#id GoogleDataformRepositoryReleaseConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#project GoogleDataformRepositoryReleaseConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#region GoogleDataformRepositoryReleaseConfig#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''A reference to the Dataform repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#repository GoogleDataformRepositoryReleaseConfig#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryReleaseConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#timeouts GoogleDataformRepositoryReleaseConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataformRepositoryReleaseConfigTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). If left unspecified, the default is UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#time_zone GoogleDataformRepositoryReleaseConfig#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryReleaseConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f91e727532e0c042fc02f59a0c103cbf0b035fe9d59d21e0973b5aef8b21c21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1fa28e60087ed7288c6a45044da3e8203c67575955be9520cdb7ee0446fa02)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e062329d81bd39a462ec8449eeee8d78200641a69282acb109faad2522ac53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a118dab2282a30d4bbe1989eb2460b895247dc000f5bae4ea724670bc5f8913)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf3a5688969a2e43eab5757dc3b83969d882b3527bf0528fbcb5903cc41e711c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbb83b8c9d66e0a69709bcf7c8cd12d2fcb72765da0f8fe5074b6c7416bdb121)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e97bc5e76756fc8f1cd4360c58e4a7fe78606cca9cda557271d5578eb02187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ab4d0c944b26ee46be20c7e8338f7f413efd01ca1f4f77c90837a1be61769c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475802f9203aa3ee97c5a3fa4761da3d24ea0ab551dd46965e206bd2636cb253)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c364ae2f445a3f0ca7b8d662062363d29507227ba4186cc301560e38293b8038)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d1868d9739a9ec28c6f82c252c7382800afb46291ad75440cc82445d8605ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fadd4e74c6c626839a91e6ddc8f2c779f70e52127207e30d58f0acfaa10192b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a96351fce45b61a21c629de8ac0024ccb9d7a7bed70798c9f2e59b0196cdb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="compilationResult")
    def compilation_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compilationResult"))

    @builtins.property
    @jsii.member(jsii_name="errorStatus")
    def error_status(
        self,
    ) -> GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusList:
        return typing.cast(GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusList, jsii.get(self, "errorStatus"))

    @builtins.property
    @jsii.member(jsii_name="releaseTime")
    def release_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76692cee92f8b043f5b70f6233ec0841c21828fe37bba8447d8f5c16eb864c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataformRepositoryReleaseConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#create GoogleDataformRepositoryReleaseConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#delete GoogleDataformRepositoryReleaseConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#update GoogleDataformRepositoryReleaseConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a804546189be37d8a422e8346b60f836ae93874d7811a1f167b476e2c9a2c37c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#create GoogleDataformRepositoryReleaseConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#delete GoogleDataformRepositoryReleaseConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_release_config#update GoogleDataformRepositoryReleaseConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryReleaseConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryReleaseConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryReleaseConfig.GoogleDataformRepositoryReleaseConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c3b3c5a754cab099bc8059ced9a6457c30a24ddc845dae5a8f3c885b25b2e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d359e64a3544f992fac46cae7a1283a41cb85c9a285a72bf7b9fde16ed6e9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246008f432ee58213d17fcca386bad5a958d54dc098268869e1e11ed804bf427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23df8f33b5c68c3ed216d48a535e449857e99a4fe9ed22c8ba84a71bfa5ad25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryReleaseConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryReleaseConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryReleaseConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8d89c814d39b244cf2cd5ab622be2a8d317e9da1e6bc22977555c772fedd8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataformRepositoryReleaseConfig",
    "GoogleDataformRepositoryReleaseConfigCodeCompilationConfig",
    "GoogleDataformRepositoryReleaseConfigCodeCompilationConfigOutputReference",
    "GoogleDataformRepositoryReleaseConfigConfig",
    "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords",
    "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus",
    "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusList",
    "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatusOutputReference",
    "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsList",
    "GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsOutputReference",
    "GoogleDataformRepositoryReleaseConfigTimeouts",
    "GoogleDataformRepositoryReleaseConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__357cab32058dba0b3d509ee33508f94e39f4bb0fe5b53071368460583e565c8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    git_commitish: builtins.str,
    name: builtins.str,
    code_compilation_config: typing.Optional[typing.Union[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cron_schedule: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryReleaseConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__82cd3f4cb5608731b88e543a180e6bde65c47b49d4791c4c5c0763cc199e759e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25eba99fad74a7480b599e27dc69f3e5ea08af60074c38b924d2df8ed4a8fd79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14433022a33b2a5fd593600966795fb201c89f1635520c200d48011fa70c3f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0d98d09d5ca70fb48823162f6d5876ab546bb6a8ec3cc9bc94a0cd72e2eaff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4700a6cffe41e6dbe16092c3f93d1557a133ad19c066928c593e95a85eb950a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27141e5a9362a0dead790c8fe19256990c3d55a896b19a934f8486b324c74943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f449928715081fce52fa94127d169a5fe004ddd726f72775f8417d1cb939b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c846162db5414fcd2297b956002accd42c7ce1a05528c5e2331d223c2b9e0f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b611ed0c73da08fa34313a7637789c0b0dfaa0600da932d3deada112bee1a37d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f95cad5f1785310586588b5e48952dec5f8130029d704327f6e0a1c4870714(
    *,
    assertion_schema: typing.Optional[builtins.str] = None,
    database_suffix: typing.Optional[builtins.str] = None,
    default_database: typing.Optional[builtins.str] = None,
    default_location: typing.Optional[builtins.str] = None,
    default_schema: typing.Optional[builtins.str] = None,
    schema_suffix: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
    vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee72f89d42a8f6812ff2e1c3d6baa74928f97349c146c15dbd8bd68196a720fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7695e1a6d684adf652832d01e0d37703576bf27e515c54d1b51a39d60b47a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac625c5c94a214816da118babfb291b0ddea1e08ac5ac7b0064d5f390523c12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf3e04b5ddc9c3a9d596b0bdbf62aa117337f850ec4df2842a3c625bd680b00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9c704bcb24e9a98c9fdce3f8e40b5e53624fde19f1e1deacae9f63e7e2ea07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd028e5e528c4d680ffee5585668ac8c418b72e57680cd128c4aa8851fd0e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fbc9254fab0fa6f96c4f9b32f2fc6d3964a52d0d75c585e7aaa22dd4b3c5b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af762e28643f7fc461ccfdd708d39c30cf8e181b5f426536148adc2e3173f976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2249b4ee4de378508dc56ddf003c5931ef5fa74c84fbcc9a80f7e3926c50d537(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d521ce1771d6b1fd3446285ef0c2c911a2363002c68dafa401caccdd05d43df(
    value: typing.Optional[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c975c43f42c6fa7b6e1c10083ccdc9ffd49e61026acc94672cc296ed9bb1cbac(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    git_commitish: builtins.str,
    name: builtins.str,
    code_compilation_config: typing.Optional[typing.Union[GoogleDataformRepositoryReleaseConfigCodeCompilationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cron_schedule: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryReleaseConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f91e727532e0c042fc02f59a0c103cbf0b035fe9d59d21e0973b5aef8b21c21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1fa28e60087ed7288c6a45044da3e8203c67575955be9520cdb7ee0446fa02(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e062329d81bd39a462ec8449eeee8d78200641a69282acb109faad2522ac53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a118dab2282a30d4bbe1989eb2460b895247dc000f5bae4ea724670bc5f8913(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3a5688969a2e43eab5757dc3b83969d882b3527bf0528fbcb5903cc41e711c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb83b8c9d66e0a69709bcf7c8cd12d2fcb72765da0f8fe5074b6c7416bdb121(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e97bc5e76756fc8f1cd4360c58e4a7fe78606cca9cda557271d5578eb02187(
    value: typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecordsErrorStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ab4d0c944b26ee46be20c7e8338f7f413efd01ca1f4f77c90837a1be61769c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475802f9203aa3ee97c5a3fa4761da3d24ea0ab551dd46965e206bd2636cb253(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c364ae2f445a3f0ca7b8d662062363d29507227ba4186cc301560e38293b8038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d1868d9739a9ec28c6f82c252c7382800afb46291ad75440cc82445d8605ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fadd4e74c6c626839a91e6ddc8f2c779f70e52127207e30d58f0acfaa10192b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a96351fce45b61a21c629de8ac0024ccb9d7a7bed70798c9f2e59b0196cdb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76692cee92f8b043f5b70f6233ec0841c21828fe37bba8447d8f5c16eb864c68(
    value: typing.Optional[GoogleDataformRepositoryReleaseConfigRecentScheduledReleaseRecords],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a804546189be37d8a422e8346b60f836ae93874d7811a1f167b476e2c9a2c37c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c3b3c5a754cab099bc8059ced9a6457c30a24ddc845dae5a8f3c885b25b2e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d359e64a3544f992fac46cae7a1283a41cb85c9a285a72bf7b9fde16ed6e9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246008f432ee58213d17fcca386bad5a958d54dc098268869e1e11ed804bf427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23df8f33b5c68c3ed216d48a535e449857e99a4fe9ed22c8ba84a71bfa5ad25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8d89c814d39b244cf2cd5ab622be2a8d317e9da1e6bc22977555c772fedd8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryReleaseConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
