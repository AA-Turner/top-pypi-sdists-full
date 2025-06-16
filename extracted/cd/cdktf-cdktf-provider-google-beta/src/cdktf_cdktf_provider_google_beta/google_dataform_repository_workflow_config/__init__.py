r'''
# `google_dataform_repository_workflow_config`

Refer to the Terraform Registry for docs: [`google_dataform_repository_workflow_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config).
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


class GoogleDataformRepositoryWorkflowConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config google_dataform_repository_workflow_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        release_config: builtins.str,
        cron_schedule: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        invocation_config: typing.Optional[typing.Union["GoogleDataformRepositoryWorkflowConfigInvocationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryWorkflowConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config google_dataform_repository_workflow_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The workflow's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#name GoogleDataformRepositoryWorkflowConfig#name}
        :param release_config: The name of the release config whose releaseCompilationResult should be executed. Must be in the format projects/* /locations/* /repositories/* /releaseConfigs/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#release_config GoogleDataformRepositoryWorkflowConfig#release_config} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param cron_schedule: Optional. Optional schedule (in cron format) for automatic creation of compilation results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#cron_schedule GoogleDataformRepositoryWorkflowConfig#cron_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#id GoogleDataformRepositoryWorkflowConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param invocation_config: invocation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#invocation_config GoogleDataformRepositoryWorkflowConfig#invocation_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#project GoogleDataformRepositoryWorkflowConfig#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#region GoogleDataformRepositoryWorkflowConfig#region}
        :param repository: A reference to the Dataform repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#repository GoogleDataformRepositoryWorkflowConfig#repository}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#timeouts GoogleDataformRepositoryWorkflowConfig#timeouts}
        :param time_zone: Optional. Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#time_zone GoogleDataformRepositoryWorkflowConfig#time_zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cfaf83194182dd78b0b49332f5157194bfc626ba9635e9154f630f2abb9e506)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataformRepositoryWorkflowConfigConfig(
            name=name,
            release_config=release_config,
            cron_schedule=cron_schedule,
            id=id,
            invocation_config=invocation_config,
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
        '''Generates CDKTF code for importing a GoogleDataformRepositoryWorkflowConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataformRepositoryWorkflowConfig to import.
        :param import_from_id: The id of the existing GoogleDataformRepositoryWorkflowConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataformRepositoryWorkflowConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7249fea934438dc026301c864630a1b52b553f6a2e81128ba1d0355c42a57e58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInvocationConfig")
    def put_invocation_config(
        self,
        *,
        fully_refresh_incremental_tables_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        included_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        transitive_dependencies_included: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transitive_dependents_included: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param fully_refresh_incremental_tables_enabled: Optional. When set to true, any incremental tables will be fully refreshed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#fully_refresh_incremental_tables_enabled GoogleDataformRepositoryWorkflowConfig#fully_refresh_incremental_tables_enabled}
        :param included_tags: Optional. The set of tags to include. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#included_tags GoogleDataformRepositoryWorkflowConfig#included_tags}
        :param included_targets: included_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#included_targets GoogleDataformRepositoryWorkflowConfig#included_targets}
        :param service_account: Optional. The service account to run workflow invocations under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#service_account GoogleDataformRepositoryWorkflowConfig#service_account}
        :param transitive_dependencies_included: Optional. When set to true, transitive dependencies of included actions will be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#transitive_dependencies_included GoogleDataformRepositoryWorkflowConfig#transitive_dependencies_included}
        :param transitive_dependents_included: Optional. When set to true, transitive dependents of included actions will be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#transitive_dependents_included GoogleDataformRepositoryWorkflowConfig#transitive_dependents_included}
        '''
        value = GoogleDataformRepositoryWorkflowConfigInvocationConfig(
            fully_refresh_incremental_tables_enabled=fully_refresh_incremental_tables_enabled,
            included_tags=included_tags,
            included_targets=included_targets,
            service_account=service_account,
            transitive_dependencies_included=transitive_dependencies_included,
            transitive_dependents_included=transitive_dependents_included,
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#create GoogleDataformRepositoryWorkflowConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#delete GoogleDataformRepositoryWorkflowConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#update GoogleDataformRepositoryWorkflowConfig#update}.
        '''
        value = GoogleDataformRepositoryWorkflowConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCronSchedule")
    def reset_cron_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSchedule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInvocationConfig")
    def reset_invocation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationConfig", []))

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
    @jsii.member(jsii_name="invocationConfig")
    def invocation_config(
        self,
    ) -> "GoogleDataformRepositoryWorkflowConfigInvocationConfigOutputReference":
        return typing.cast("GoogleDataformRepositoryWorkflowConfigInvocationConfigOutputReference", jsii.get(self, "invocationConfig"))

    @builtins.property
    @jsii.member(jsii_name="recentScheduledExecutionRecords")
    def recent_scheduled_execution_records(
        self,
    ) -> "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsList":
        return typing.cast("GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsList", jsii.get(self, "recentScheduledExecutionRecords"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDataformRepositoryWorkflowConfigTimeoutsOutputReference":
        return typing.cast("GoogleDataformRepositoryWorkflowConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cronScheduleInput")
    def cron_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationConfigInput")
    def invocation_config_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkflowConfigInvocationConfig"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkflowConfigInvocationConfig"], jsii.get(self, "invocationConfigInput"))

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
    @jsii.member(jsii_name="releaseConfigInput")
    def release_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryWorkflowConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryWorkflowConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__94a4fcd40e52077eb3b890ef343086c234ccff7fd063d7921ff753928fdb3f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000e82608478bdf4be76b506312714e33f867263c405271df19de46d2c42e876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a569d6b83135d77d723f446d2ba5ede2ef0032016b35bed3af98b623ec368b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa462e98b924f9e6e0f6afe8aab0efddfe417d980ae171c47c175fba9c0124b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bec8e33766532d8b75904dea1fe7f4ea3de94e72b83b98a708a3c4d2eae06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseConfig")
    def release_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseConfig"))

    @release_config.setter
    def release_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71d82413f6228a9bf213a93b884a07356532d895610a0552f0bb4f43a9d0308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e035246dcc5d4298a78d220f2c4585d2afc0f045fa50df42d6e3cad28fcad48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1ee326a7ab1bc7d30744e083c2e062fb0823b49e0dd0b2394dacb9ad764dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "release_config": "releaseConfig",
        "cron_schedule": "cronSchedule",
        "id": "id",
        "invocation_config": "invocationConfig",
        "project": "project",
        "region": "region",
        "repository": "repository",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class GoogleDataformRepositoryWorkflowConfigConfig(
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
        name: builtins.str,
        release_config: builtins.str,
        cron_schedule: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        invocation_config: typing.Optional[typing.Union["GoogleDataformRepositoryWorkflowConfigInvocationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryWorkflowConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: The workflow's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#name GoogleDataformRepositoryWorkflowConfig#name}
        :param release_config: The name of the release config whose releaseCompilationResult should be executed. Must be in the format projects/* /locations/* /repositories/* /releaseConfigs/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#release_config GoogleDataformRepositoryWorkflowConfig#release_config} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param cron_schedule: Optional. Optional schedule (in cron format) for automatic creation of compilation results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#cron_schedule GoogleDataformRepositoryWorkflowConfig#cron_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#id GoogleDataformRepositoryWorkflowConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param invocation_config: invocation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#invocation_config GoogleDataformRepositoryWorkflowConfig#invocation_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#project GoogleDataformRepositoryWorkflowConfig#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#region GoogleDataformRepositoryWorkflowConfig#region}
        :param repository: A reference to the Dataform repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#repository GoogleDataformRepositoryWorkflowConfig#repository}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#timeouts GoogleDataformRepositoryWorkflowConfig#timeouts}
        :param time_zone: Optional. Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#time_zone GoogleDataformRepositoryWorkflowConfig#time_zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(invocation_config, dict):
            invocation_config = GoogleDataformRepositoryWorkflowConfigInvocationConfig(**invocation_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataformRepositoryWorkflowConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454ba9824936dc68086b121d657e2ee298ad72fc343eaf0a6366059bce4d14c5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument release_config", value=release_config, expected_type=type_hints["release_config"])
            check_type(argname="argument cron_schedule", value=cron_schedule, expected_type=type_hints["cron_schedule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument invocation_config", value=invocation_config, expected_type=type_hints["invocation_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "release_config": release_config,
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
        if cron_schedule is not None:
            self._values["cron_schedule"] = cron_schedule
        if id is not None:
            self._values["id"] = id
        if invocation_config is not None:
            self._values["invocation_config"] = invocation_config
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
    def name(self) -> builtins.str:
        '''The workflow's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#name GoogleDataformRepositoryWorkflowConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_config(self) -> builtins.str:
        '''The name of the release config whose releaseCompilationResult should be executed.

        Must be in the format projects/* /locations/* /repositories/* /releaseConfigs/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#release_config GoogleDataformRepositoryWorkflowConfig#release_config}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("release_config")
        assert result is not None, "Required property 'release_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cron_schedule(self) -> typing.Optional[builtins.str]:
        '''Optional. Optional schedule (in cron format) for automatic creation of compilation results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#cron_schedule GoogleDataformRepositoryWorkflowConfig#cron_schedule}
        '''
        result = self._values.get("cron_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#id GoogleDataformRepositoryWorkflowConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_config(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkflowConfigInvocationConfig"]:
        '''invocation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#invocation_config GoogleDataformRepositoryWorkflowConfig#invocation_config}
        '''
        result = self._values.get("invocation_config")
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkflowConfigInvocationConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#project GoogleDataformRepositoryWorkflowConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#region GoogleDataformRepositoryWorkflowConfig#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''A reference to the Dataform repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#repository GoogleDataformRepositoryWorkflowConfig#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkflowConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#timeouts GoogleDataformRepositoryWorkflowConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkflowConfigTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). If left unspecified, the default is UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#time_zone GoogleDataformRepositoryWorkflowConfig#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkflowConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigInvocationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fully_refresh_incremental_tables_enabled": "fullyRefreshIncrementalTablesEnabled",
        "included_tags": "includedTags",
        "included_targets": "includedTargets",
        "service_account": "serviceAccount",
        "transitive_dependencies_included": "transitiveDependenciesIncluded",
        "transitive_dependents_included": "transitiveDependentsIncluded",
    },
)
class GoogleDataformRepositoryWorkflowConfigInvocationConfig:
    def __init__(
        self,
        *,
        fully_refresh_incremental_tables_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        included_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        transitive_dependencies_included: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transitive_dependents_included: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param fully_refresh_incremental_tables_enabled: Optional. When set to true, any incremental tables will be fully refreshed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#fully_refresh_incremental_tables_enabled GoogleDataformRepositoryWorkflowConfig#fully_refresh_incremental_tables_enabled}
        :param included_tags: Optional. The set of tags to include. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#included_tags GoogleDataformRepositoryWorkflowConfig#included_tags}
        :param included_targets: included_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#included_targets GoogleDataformRepositoryWorkflowConfig#included_targets}
        :param service_account: Optional. The service account to run workflow invocations under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#service_account GoogleDataformRepositoryWorkflowConfig#service_account}
        :param transitive_dependencies_included: Optional. When set to true, transitive dependencies of included actions will be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#transitive_dependencies_included GoogleDataformRepositoryWorkflowConfig#transitive_dependencies_included}
        :param transitive_dependents_included: Optional. When set to true, transitive dependents of included actions will be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#transitive_dependents_included GoogleDataformRepositoryWorkflowConfig#transitive_dependents_included}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17053658bbdb9acadb46b1fc9589da441dff4e8c970c4c80f2e04265512f3b30)
            check_type(argname="argument fully_refresh_incremental_tables_enabled", value=fully_refresh_incremental_tables_enabled, expected_type=type_hints["fully_refresh_incremental_tables_enabled"])
            check_type(argname="argument included_tags", value=included_tags, expected_type=type_hints["included_tags"])
            check_type(argname="argument included_targets", value=included_targets, expected_type=type_hints["included_targets"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument transitive_dependencies_included", value=transitive_dependencies_included, expected_type=type_hints["transitive_dependencies_included"])
            check_type(argname="argument transitive_dependents_included", value=transitive_dependents_included, expected_type=type_hints["transitive_dependents_included"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fully_refresh_incremental_tables_enabled is not None:
            self._values["fully_refresh_incremental_tables_enabled"] = fully_refresh_incremental_tables_enabled
        if included_tags is not None:
            self._values["included_tags"] = included_tags
        if included_targets is not None:
            self._values["included_targets"] = included_targets
        if service_account is not None:
            self._values["service_account"] = service_account
        if transitive_dependencies_included is not None:
            self._values["transitive_dependencies_included"] = transitive_dependencies_included
        if transitive_dependents_included is not None:
            self._values["transitive_dependents_included"] = transitive_dependents_included

    @builtins.property
    def fully_refresh_incremental_tables_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When set to true, any incremental tables will be fully refreshed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#fully_refresh_incremental_tables_enabled GoogleDataformRepositoryWorkflowConfig#fully_refresh_incremental_tables_enabled}
        '''
        result = self._values.get("fully_refresh_incremental_tables_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def included_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. The set of tags to include.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#included_tags GoogleDataformRepositoryWorkflowConfig#included_tags}
        '''
        result = self._values.get("included_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets"]]]:
        '''included_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#included_targets GoogleDataformRepositoryWorkflowConfig#included_targets}
        '''
        result = self._values.get("included_targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets"]]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Optional. The service account to run workflow invocations under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#service_account GoogleDataformRepositoryWorkflowConfig#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transitive_dependencies_included(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When set to true, transitive dependencies of included actions will be executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#transitive_dependencies_included GoogleDataformRepositoryWorkflowConfig#transitive_dependencies_included}
        '''
        result = self._values.get("transitive_dependencies_included")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transitive_dependents_included(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When set to true, transitive dependents of included actions will be executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#transitive_dependents_included GoogleDataformRepositoryWorkflowConfig#transitive_dependents_included}
        '''
        result = self._values.get("transitive_dependents_included")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkflowConfigInvocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "name": "name", "schema": "schema"},
)
class GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets:
    def __init__(
        self,
        *,
        database: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: The action's database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#database GoogleDataformRepositoryWorkflowConfig#database}
        :param name: The action's name, within database and schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#name GoogleDataformRepositoryWorkflowConfig#name}
        :param schema: The action's schema (BigQuery dataset ID), within database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#schema GoogleDataformRepositoryWorkflowConfig#schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495daadbc489fae9837f8920910f975e30e39838395b27be9b8e1554dda613ca)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database is not None:
            self._values["database"] = database
        if name is not None:
            self._values["name"] = name
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''The action's database (Google Cloud project ID).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#database GoogleDataformRepositoryWorkflowConfig#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The action's name, within database and schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#name GoogleDataformRepositoryWorkflowConfig#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''The action's schema (BigQuery dataset ID), within database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#schema GoogleDataformRepositoryWorkflowConfig#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8f675e3e615fabc4a707f32608cd5eeba20ce96961faae1834d8e194616cc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e15e872b62479bf4b4313e1eb22c7d6112440fd9ee15976f5f421a871aa9dca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2266433ccf3ebe51d76922424fe1ebb60ca358a4e5c56b01ed287ee79fb4c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52232f137833a9a10718844e861f4d259ed6c410885e8db4617a78e39f74bdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__333e70a56be0e6be022de6f36bfb9bf293d5f6462900bcdfb8389ad7508e8c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c412251ef0361a0f9f36e9360b6a192975ec3612a7deb3eefac67a3d6c0fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94b1163cc7059b1a30d6a380dafdeafa968c2c47627b542db0cb58b4eda8f1a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24807e05ed34ce2b8a247dcaa20b020d5b2051e31d57fc8f4a53f7dfe556dd8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ea90e4a596f5a74aa384080f86d6a13b0b4cf2001ec1ddd75f6490d01ba9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5affa5fe8ecd27f3ba34a50b2d3855a67e335542238288f37096e82054b41a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18263f9d65b6cd60715ecbef02942fce23e35049091bf111aa91a33e3de2d71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryWorkflowConfigInvocationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigInvocationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__532ee704d4aa535da99d1eb0db9358c6cddc017add23c7747a313931c1d5be91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludedTargets")
    def put_included_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43216fa2c4544a9bb636fbf509485581e87af0c309e860b6133439c8c3d4cd28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncludedTargets", [value]))

    @jsii.member(jsii_name="resetFullyRefreshIncrementalTablesEnabled")
    def reset_fully_refresh_incremental_tables_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullyRefreshIncrementalTablesEnabled", []))

    @jsii.member(jsii_name="resetIncludedTags")
    def reset_included_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedTags", []))

    @jsii.member(jsii_name="resetIncludedTargets")
    def reset_included_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedTargets", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetTransitiveDependenciesIncluded")
    def reset_transitive_dependencies_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitiveDependenciesIncluded", []))

    @jsii.member(jsii_name="resetTransitiveDependentsIncluded")
    def reset_transitive_dependents_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitiveDependentsIncluded", []))

    @builtins.property
    @jsii.member(jsii_name="includedTargets")
    def included_targets(
        self,
    ) -> GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsList:
        return typing.cast(GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsList, jsii.get(self, "includedTargets"))

    @builtins.property
    @jsii.member(jsii_name="fullyRefreshIncrementalTablesEnabledInput")
    def fully_refresh_incremental_tables_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fullyRefreshIncrementalTablesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="includedTagsInput")
    def included_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedTargetsInput")
    def included_targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]], jsii.get(self, "includedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="transitiveDependenciesIncludedInput")
    def transitive_dependencies_included_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "transitiveDependenciesIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="transitiveDependentsIncludedInput")
    def transitive_dependents_included_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "transitiveDependentsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="fullyRefreshIncrementalTablesEnabled")
    def fully_refresh_incremental_tables_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fullyRefreshIncrementalTablesEnabled"))

    @fully_refresh_incremental_tables_enabled.setter
    def fully_refresh_incremental_tables_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1775f87fc90e1e6b7f5679087049c6b7f512aaa11dbbc0b8e61f4d90517a90e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullyRefreshIncrementalTablesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedTags")
    def included_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedTags"))

    @included_tags.setter
    def included_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c161595df42492807a91081a30a27c8631d77e8fd3c16b410be2c61d362228d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6210580f71b089c8f708866f0aed51a6224e4538cd14ee777ce27e85cc7b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitiveDependenciesIncluded")
    def transitive_dependencies_included(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "transitiveDependenciesIncluded"))

    @transitive_dependencies_included.setter
    def transitive_dependencies_included(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96f71b5ba805946159e03250fd3e96efddbf45d9d5a60b907265fd5147e094d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitiveDependenciesIncluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitiveDependentsIncluded")
    def transitive_dependents_included(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "transitiveDependentsIncluded"))

    @transitive_dependents_included.setter
    def transitive_dependents_included(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d162eaaa0f12e7f6bbf732f6a58f794ae69cbf388280b856f741d5d2d4b7590d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitiveDependentsIncluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryWorkflowConfigInvocationConfig]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryWorkflowConfigInvocationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryWorkflowConfigInvocationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757a38d162c20d855f1cf14b307f8f54ec12563ac4350ce751b2d1179ce6a46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59d6af0cd6aeadd90e8ae6959ef304370d0bb51299b34558d31a6a63a7ce0015)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ad37ceb1efb77cae8ffdfbe023b2e290e962863d62e6c631997bf531b12691)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce35a092a3d6108f0eb7f5da51ce4763c00fefbcb9fc15be1694aa1471acd3e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__875386cac17cdddcdb89056fff9ba4cc15e063debe7b0f3def956716c946baaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f8cc9a444d43134ffbed12d8b349dacb2cfc5dcd623d3c38fa4e0b753ef75e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c873e26d1aeef42b4de76dadce28bc967b9ef01503abe22664ebf2c33939ef1)
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
    ) -> typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa51b6103319211c27dcef2692a5c824c1aa7a92f57c6e6abd69b3cd22a9ef79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be61c57c4d5bea141ba28b868c4c0dd7a5156218992c2a95d8ba3dabc14fe87b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76e787ecb0e06bc333a32d91319e422aa84464c14d501559de38004807d175b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2c450257e85c227062e12610735cfc5edf3c50b207bc7ea0fe8efa5a64694e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7bdd815f6b00903947476553d088baa34e7e6a4f2fdfb197e2717c87d45a9d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__530ab31d5547e2cf4cbeabddf38a9cadbac94ef4fd417a51115c9c6a813ee032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47105efd052121bfa313bf0af2d521cacf9dd36ea82c43c4d422aed4822f32e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="errorStatus")
    def error_status(
        self,
    ) -> GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusList:
        return typing.cast(GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusList, jsii.get(self, "errorStatus"))

    @builtins.property
    @jsii.member(jsii_name="executionTime")
    def execution_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTime"))

    @builtins.property
    @jsii.member(jsii_name="workflowInvocation")
    def workflow_invocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowInvocation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0f00797d1ce990b6e6596592cceeef5a0f09a42d6be11678d9ed87a7415b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataformRepositoryWorkflowConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#create GoogleDataformRepositoryWorkflowConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#delete GoogleDataformRepositoryWorkflowConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#update GoogleDataformRepositoryWorkflowConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864a87195cb0c707480e74515e0d1279bd72e2b5d61cdb450108e4b55b2fd20d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#create GoogleDataformRepositoryWorkflowConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#delete GoogleDataformRepositoryWorkflowConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository_workflow_config#update GoogleDataformRepositoryWorkflowConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkflowConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryWorkflowConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepositoryWorkflowConfig.GoogleDataformRepositoryWorkflowConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7247d7a8d86a7a337da91fd85a3da6085d614b766f95cd9b0f69e4e8a8de0b4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c921a6a887bb1b18a71cda00704235a8edd51e65e0a7f4b6dc1862e387f949a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9a9c3a72d931d9f6e8068957a48cbfb3eb8da841d6176b9fde8b2635dfbb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191c4aeacb05d134acdb761c9b1a9043b56ce51c466e041772829203a144fbc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629233a9d9f26a7b0b6fca181014dc2186ef9b8a8077041746f676c77cc942e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataformRepositoryWorkflowConfig",
    "GoogleDataformRepositoryWorkflowConfigConfig",
    "GoogleDataformRepositoryWorkflowConfigInvocationConfig",
    "GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets",
    "GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsList",
    "GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargetsOutputReference",
    "GoogleDataformRepositoryWorkflowConfigInvocationConfigOutputReference",
    "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords",
    "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus",
    "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusList",
    "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatusOutputReference",
    "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsList",
    "GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsOutputReference",
    "GoogleDataformRepositoryWorkflowConfigTimeouts",
    "GoogleDataformRepositoryWorkflowConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7cfaf83194182dd78b0b49332f5157194bfc626ba9635e9154f630f2abb9e506(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    release_config: builtins.str,
    cron_schedule: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    invocation_config: typing.Optional[typing.Union[GoogleDataformRepositoryWorkflowConfigInvocationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryWorkflowConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7249fea934438dc026301c864630a1b52b553f6a2e81128ba1d0355c42a57e58(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a4fcd40e52077eb3b890ef343086c234ccff7fd063d7921ff753928fdb3f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000e82608478bdf4be76b506312714e33f867263c405271df19de46d2c42e876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a569d6b83135d77d723f446d2ba5ede2ef0032016b35bed3af98b623ec368b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa462e98b924f9e6e0f6afe8aab0efddfe417d980ae171c47c175fba9c0124b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bec8e33766532d8b75904dea1fe7f4ea3de94e72b83b98a708a3c4d2eae06a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71d82413f6228a9bf213a93b884a07356532d895610a0552f0bb4f43a9d0308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e035246dcc5d4298a78d220f2c4585d2afc0f045fa50df42d6e3cad28fcad48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1ee326a7ab1bc7d30744e083c2e062fb0823b49e0dd0b2394dacb9ad764dd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454ba9824936dc68086b121d657e2ee298ad72fc343eaf0a6366059bce4d14c5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    release_config: builtins.str,
    cron_schedule: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    invocation_config: typing.Optional[typing.Union[GoogleDataformRepositoryWorkflowConfigInvocationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryWorkflowConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17053658bbdb9acadb46b1fc9589da441dff4e8c970c4c80f2e04265512f3b30(
    *,
    fully_refresh_incremental_tables_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    included_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    transitive_dependencies_included: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transitive_dependents_included: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495daadbc489fae9837f8920910f975e30e39838395b27be9b8e1554dda613ca(
    *,
    database: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8f675e3e615fabc4a707f32608cd5eeba20ce96961faae1834d8e194616cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e15e872b62479bf4b4313e1eb22c7d6112440fd9ee15976f5f421a871aa9dca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2266433ccf3ebe51d76922424fe1ebb60ca358a4e5c56b01ed287ee79fb4c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52232f137833a9a10718844e861f4d259ed6c410885e8db4617a78e39f74bdc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333e70a56be0e6be022de6f36bfb9bf293d5f6462900bcdfb8389ad7508e8c45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c412251ef0361a0f9f36e9360b6a192975ec3612a7deb3eefac67a3d6c0fb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b1163cc7059b1a30d6a380dafdeafa968c2c47627b542db0cb58b4eda8f1a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24807e05ed34ce2b8a247dcaa20b020d5b2051e31d57fc8f4a53f7dfe556dd8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ea90e4a596f5a74aa384080f86d6a13b0b4cf2001ec1ddd75f6490d01ba9fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5affa5fe8ecd27f3ba34a50b2d3855a67e335542238288f37096e82054b41a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18263f9d65b6cd60715ecbef02942fce23e35049091bf111aa91a33e3de2d71c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532ee704d4aa535da99d1eb0db9358c6cddc017add23c7747a313931c1d5be91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43216fa2c4544a9bb636fbf509485581e87af0c309e860b6133439c8c3d4cd28(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataformRepositoryWorkflowConfigInvocationConfigIncludedTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1775f87fc90e1e6b7f5679087049c6b7f512aaa11dbbc0b8e61f4d90517a90e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c161595df42492807a91081a30a27c8631d77e8fd3c16b410be2c61d362228d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6210580f71b089c8f708866f0aed51a6224e4538cd14ee777ce27e85cc7b2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96f71b5ba805946159e03250fd3e96efddbf45d9d5a60b907265fd5147e094d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d162eaaa0f12e7f6bbf732f6a58f794ae69cbf388280b856f741d5d2d4b7590d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757a38d162c20d855f1cf14b307f8f54ec12563ac4350ce751b2d1179ce6a46c(
    value: typing.Optional[GoogleDataformRepositoryWorkflowConfigInvocationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d6af0cd6aeadd90e8ae6959ef304370d0bb51299b34558d31a6a63a7ce0015(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ad37ceb1efb77cae8ffdfbe023b2e290e962863d62e6c631997bf531b12691(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce35a092a3d6108f0eb7f5da51ce4763c00fefbcb9fc15be1694aa1471acd3e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875386cac17cdddcdb89056fff9ba4cc15e063debe7b0f3def956716c946baaa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8cc9a444d43134ffbed12d8b349dacb2cfc5dcd623d3c38fa4e0b753ef75e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c873e26d1aeef42b4de76dadce28bc967b9ef01503abe22664ebf2c33939ef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa51b6103319211c27dcef2692a5c824c1aa7a92f57c6e6abd69b3cd22a9ef79(
    value: typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecordsErrorStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be61c57c4d5bea141ba28b868c4c0dd7a5156218992c2a95d8ba3dabc14fe87b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76e787ecb0e06bc333a32d91319e422aa84464c14d501559de38004807d175b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2c450257e85c227062e12610735cfc5edf3c50b207bc7ea0fe8efa5a64694e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bdd815f6b00903947476553d088baa34e7e6a4f2fdfb197e2717c87d45a9d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530ab31d5547e2cf4cbeabddf38a9cadbac94ef4fd417a51115c9c6a813ee032(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47105efd052121bfa313bf0af2d521cacf9dd36ea82c43c4d422aed4822f32e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0f00797d1ce990b6e6596592cceeef5a0f09a42d6be11678d9ed87a7415b25(
    value: typing.Optional[GoogleDataformRepositoryWorkflowConfigRecentScheduledExecutionRecords],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864a87195cb0c707480e74515e0d1279bd72e2b5d61cdb450108e4b55b2fd20d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7247d7a8d86a7a337da91fd85a3da6085d614b766f95cd9b0f69e4e8a8de0b4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c921a6a887bb1b18a71cda00704235a8edd51e65e0a7f4b6dc1862e387f949a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9a9c3a72d931d9f6e8068957a48cbfb3eb8da841d6176b9fde8b2635dfbb2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191c4aeacb05d134acdb761c9b1a9043b56ce51c466e041772829203a144fbc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629233a9d9f26a7b0b6fca181014dc2186ef9b8a8077041746f676c77cc942e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryWorkflowConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
