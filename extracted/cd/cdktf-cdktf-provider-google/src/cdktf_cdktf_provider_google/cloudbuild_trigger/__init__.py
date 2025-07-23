r'''
# `google_cloudbuild_trigger`

Refer to the Terraform Registry for docs: [`google_cloudbuild_trigger`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger).
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


class CloudbuildTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger google_cloudbuild_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        approval_config: typing.Optional[typing.Union["CloudbuildTriggerApprovalConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_server_trigger_config: typing.Optional[typing.Union["CloudbuildTriggerBitbucketServerTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        build_attribute: typing.Optional[typing.Union["CloudbuildTriggerBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        filter: typing.Optional[builtins.str] = None,
        git_file_source: typing.Optional[typing.Union["CloudbuildTriggerGitFileSource", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["CloudbuildTriggerGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_build_logs: typing.Optional[builtins.str] = None,
        included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pubsub_config: typing.Optional[typing.Union["CloudbuildTriggerPubsubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        repository_event_config: typing.Optional[typing.Union["CloudbuildTriggerRepositoryEventConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_to_build: typing.Optional[typing.Union["CloudbuildTriggerSourceToBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CloudbuildTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_template: typing.Optional[typing.Union["CloudbuildTriggerTriggerTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_config: typing.Optional[typing.Union["CloudbuildTriggerWebhookConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger google_cloudbuild_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param approval_config: approval_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#approval_config CloudbuildTrigger#approval_config}
        :param bitbucket_server_trigger_config: bitbucket_server_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_trigger_config CloudbuildTrigger#bitbucket_server_trigger_config}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#build CloudbuildTrigger#build}
        :param description: Human-readable description of the trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#description CloudbuildTrigger#description}
        :param disabled: Whether the trigger is disabled or not. If true, the trigger will never result in a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#disabled CloudbuildTrigger#disabled}
        :param filename: Path, from the source root, to a file whose contents is used for the template. Either a filename or build template must be provided. Set this only when using trigger_template or github. When using Pub/Sub, Webhook or Manual set the file name using git_file_source instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#filename CloudbuildTrigger#filename}
        :param filter: A Common Expression Language string. Used only with Pub/Sub and Webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#filter CloudbuildTrigger#filter}
        :param git_file_source: git_file_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#git_file_source CloudbuildTrigger#git_file_source}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github CloudbuildTrigger#github}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#id CloudbuildTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignored_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If ignoredFiles and changed files are both empty, then they are not used to determine whether or not to trigger a build. If ignoredFiles is not empty, then we ignore any files that match any of the ignored_file globs. If the change has no files that are outside of the ignoredFiles globs, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#ignored_files CloudbuildTrigger#ignored_files}
        :param include_build_logs: Build logs will be sent back to GitHub as part of the checkrun result. Values can be INCLUDE_BUILD_LOGS_UNSPECIFIED or INCLUDE_BUILD_LOGS_WITH_STATUS Possible values: ["INCLUDE_BUILD_LOGS_UNSPECIFIED", "INCLUDE_BUILD_LOGS_WITH_STATUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#include_build_logs CloudbuildTrigger#include_build_logs}
        :param included_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is empty, then as far as this filter is concerned, we should trigger the build. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is not empty, then we make sure that at least one of those files matches a includedFiles glob. If not, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#included_files CloudbuildTrigger#included_files}
        :param location: The `Cloud Build location <https://cloud.google.com/build/docs/locations>`_ for the trigger. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#location CloudbuildTrigger#location}
        :param name: Name of the trigger. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project CloudbuildTrigger#project}.
        :param pubsub_config: pubsub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pubsub_config CloudbuildTrigger#pubsub_config}
        :param repository_event_config: repository_event_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository_event_config CloudbuildTrigger#repository_event_config}
        :param service_account: The service account used for all user-controlled operations including triggers.patch, triggers.run, builds.create, and builds.cancel. If no service account is set, then the standard Cloud Build service account ([PROJECT_NUM]@system.gserviceaccount.com) will be used instead. Format: projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_ID_OR_EMAIL} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#service_account CloudbuildTrigger#service_account}
        :param source_to_build: source_to_build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source_to_build CloudbuildTrigger#source_to_build}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a BuildTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tags CloudbuildTrigger#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeouts CloudbuildTrigger#timeouts}
        :param trigger_template: trigger_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#trigger_template CloudbuildTrigger#trigger_template}
        :param webhook_config: webhook_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#webhook_config CloudbuildTrigger#webhook_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d0fc7ab845b08d8ac8cc27beffa7a97fb1fc9be14f813bd9fac42e8bf39abb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudbuildTriggerConfig(
            approval_config=approval_config,
            bitbucket_server_trigger_config=bitbucket_server_trigger_config,
            build_attribute=build_attribute,
            description=description,
            disabled=disabled,
            filename=filename,
            filter=filter,
            git_file_source=git_file_source,
            github=github,
            id=id,
            ignored_files=ignored_files,
            include_build_logs=include_build_logs,
            included_files=included_files,
            location=location,
            name=name,
            project=project,
            pubsub_config=pubsub_config,
            repository_event_config=repository_event_config,
            service_account=service_account,
            source_to_build=source_to_build,
            substitutions=substitutions,
            tags=tags,
            timeouts=timeouts,
            trigger_template=trigger_template,
            webhook_config=webhook_config,
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
        '''Generates CDKTF code for importing a CloudbuildTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudbuildTrigger to import.
        :param import_from_id: The id of the existing CloudbuildTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudbuildTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3810ea2d04f6b88cda1cecf165c64d2b6892d21884b63d25e1e5cae1451fd5e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApprovalConfig")
    def put_approval_config(
        self,
        *,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_required: Whether or not approval is needed. If this is set on a build, it will become pending when run, and will need to be explicitly approved to start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#approval_required CloudbuildTrigger#approval_required}
        '''
        value = CloudbuildTriggerApprovalConfig(approval_required=approval_required)

        return typing.cast(None, jsii.invoke(self, "putApprovalConfig", [value]))

    @jsii.member(jsii_name="putBitbucketServerTriggerConfig")
    def put_bitbucket_server_trigger_config(
        self,
        *,
        bitbucket_server_config_resource: builtins.str,
        project_key: builtins.str,
        repo_slug: builtins.str,
        pull_request: typing.Optional[typing.Union["CloudbuildTriggerBitbucketServerTriggerConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["CloudbuildTriggerBitbucketServerTriggerConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bitbucket_server_config_resource: The Bitbucket server config resource that this trigger config maps to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config_resource CloudbuildTrigger#bitbucket_server_config_resource}
        :param project_key: Key of the project that the repo is in. For example: The key for https://mybitbucket.server/projects/TEST/repos/test-repo is "TEST". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_key CloudbuildTrigger#project_key}
        :param repo_slug: Slug of the repository. A repository slug is a URL-friendly version of a repository name, automatically generated by Bitbucket for use in the URL. For example, if the repository name is 'test repo', in the URL it would become 'test-repo' as in https://mybitbucket.server/projects/TEST/repos/test-repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_slug CloudbuildTrigger#repo_slug}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        value = CloudbuildTriggerBitbucketServerTriggerConfig(
            bitbucket_server_config_resource=bitbucket_server_config_resource,
            project_key=project_key,
            repo_slug=repo_slug,
            pull_request=pull_request,
            push=push,
        )

        return typing.cast(None, jsii.invoke(self, "putBitbucketServerTriggerConfig", [value]))

    @jsii.member(jsii_name="putBuildAttribute")
    def put_build_attribute(
        self,
        *,
        step: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildStep", typing.Dict[builtins.str, typing.Any]]]],
        artifacts: typing.Optional[typing.Union["CloudbuildTriggerBuildArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        available_secrets: typing.Optional[typing.Union["CloudbuildTriggerBuildAvailableSecrets", typing.Dict[builtins.str, typing.Any]]] = None,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        logs_bucket: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["CloudbuildTriggerBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        queue_ttl: typing.Optional[builtins.str] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union["CloudbuildTriggerBuildSource", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param step: step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#step CloudbuildTrigger#step}
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#artifacts CloudbuildTrigger#artifacts}
        :param available_secrets: available_secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#available_secrets CloudbuildTrigger#available_secrets}
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images are pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build status is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#images CloudbuildTrigger#images}
        :param logs_bucket: Google Cloud Storage bucket where logs should be written. Logs file names will be of the format ${logsBucket}/log-${build_id}.txt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#logs_bucket CloudbuildTrigger#logs_bucket}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#options CloudbuildTrigger#options}
        :param queue_ttl: TTL in queue for this build. If provided and the build is enqueued longer than this value, the build will expire and the build status will be EXPIRED. The TTL starts ticking from createTime. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#queue_ttl CloudbuildTrigger#queue_ttl}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret CloudbuildTrigger#secret}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source CloudbuildTrigger#source}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a Build. These are not docker tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tags CloudbuildTrigger#tags}
        :param timeout: Amount of time that this build should be allowed to run, to second granularity. If this amount of time elapses, work on the build will cease and the build status will be TIMEOUT. This timeout must be equal to or greater than the sum of the timeouts for build steps within the build. The expected format is the number of seconds followed by s. Default time is ten minutes (600s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeout CloudbuildTrigger#timeout}
        '''
        value = CloudbuildTriggerBuild(
            step=step,
            artifacts=artifacts,
            available_secrets=available_secrets,
            images=images,
            logs_bucket=logs_bucket,
            options=options,
            queue_ttl=queue_ttl,
            secret=secret,
            source=source,
            substitutions=substitutions,
            tags=tags,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildAttribute", [value]))

    @jsii.member(jsii_name="putGitFileSource")
    def put_git_file_source(
        self,
        *,
        path: builtins.str,
        repo_type: builtins.str,
        bitbucket_server_config: typing.Optional[builtins.str] = None,
        github_enterprise_config: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        revision: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The path of the file, with the repo root as the root of the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_type CloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config CloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github_enterprise_config CloudbuildTrigger#github_enterprise_config}
        :param repository: The fully qualified resource name of the Repo API repository. The fully qualified resource name of the Repo API repository. If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        :param revision: The branch, tag, arbitrary ref, or SHA version of the repo to use when resolving the filename (optional). This field respects the same syntax/resolution as described here: https://git-scm.com/docs/gitrevisions If unspecified, the revision from which the trigger invocation originated is assumed to be the revision from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#revision CloudbuildTrigger#revision}
        :param uri: The URI of the repo (optional). If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#uri CloudbuildTrigger#uri}
        '''
        value = CloudbuildTriggerGitFileSource(
            path=path,
            repo_type=repo_type,
            bitbucket_server_config=bitbucket_server_config,
            github_enterprise_config=github_enterprise_config,
            repository=repository,
            revision=revision,
            uri=uri,
        )

        return typing.cast(None, jsii.invoke(self, "putGitFileSource", [value]))

    @jsii.member(jsii_name="putGithub")
    def put_github(
        self,
        *,
        enterprise_config_resource_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        pull_request: typing.Optional[typing.Union["CloudbuildTriggerGithubPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["CloudbuildTriggerGithubPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enterprise_config_resource_name: The resource name of the github enterprise config that should be applied to this installation. For example: "projects/{$projectId}/locations/{$locationId}/githubEnterpriseConfigs/{$configId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#enterprise_config_resource_name CloudbuildTrigger#enterprise_config_resource_name}
        :param name: Name of the repository. For example: The name for https://github.com/googlecloudplatform/cloud-builders is "cloud-builders". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param owner: Owner of the repository. For example: The owner for https://github.com/googlecloudplatform/cloud-builders is "googlecloudplatform". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#owner CloudbuildTrigger#owner}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        value = CloudbuildTriggerGithub(
            enterprise_config_resource_name=enterprise_config_resource_name,
            name=name,
            owner=owner,
            pull_request=pull_request,
            push=push,
        )

        return typing.cast(None, jsii.invoke(self, "putGithub", [value]))

    @jsii.member(jsii_name="putPubsubConfig")
    def put_pubsub_config(
        self,
        *,
        topic: builtins.str,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the topic from which this subscription is receiving messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#topic CloudbuildTrigger#topic}
        :param service_account_email: Service account that will make the push request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#service_account_email CloudbuildTrigger#service_account_email}
        '''
        value = CloudbuildTriggerPubsubConfig(
            topic=topic, service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubConfig", [value]))

    @jsii.member(jsii_name="putRepositoryEventConfig")
    def put_repository_event_config(
        self,
        *,
        pull_request: typing.Optional[typing.Union["CloudbuildTriggerRepositoryEventConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["CloudbuildTriggerRepositoryEventConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        :param repository: The resource name of the Repo API resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        value = CloudbuildTriggerRepositoryEventConfig(
            pull_request=pull_request, push=push, repository=repository
        )

        return typing.cast(None, jsii.invoke(self, "putRepositoryEventConfig", [value]))

    @jsii.member(jsii_name="putSourceToBuild")
    def put_source_to_build(
        self,
        *,
        ref: builtins.str,
        repo_type: builtins.str,
        bitbucket_server_config: typing.Optional[builtins.str] = None,
        github_enterprise_config: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ref: The branch or tag to use. Must start with "refs/" (required). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#ref CloudbuildTrigger#ref}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_type CloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config CloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github_enterprise_config CloudbuildTrigger#github_enterprise_config}
        :param repository: The qualified resource name of the Repo API repository. Either uri or repository can be specified and is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        :param uri: The URI of the repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#uri CloudbuildTrigger#uri}
        '''
        value = CloudbuildTriggerSourceToBuild(
            ref=ref,
            repo_type=repo_type,
            bitbucket_server_config=bitbucket_server_config,
            github_enterprise_config=github_enterprise_config,
            repository=repository,
            uri=uri,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceToBuild", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#create CloudbuildTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#delete CloudbuildTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#update CloudbuildTrigger#update}.
        '''
        value = CloudbuildTriggerTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTriggerTemplate")
    def put_trigger_template(
        self,
        *,
        branch_name: typing.Optional[builtins.str] = None,
        commit_sha: typing.Optional[builtins.str] = None,
        dir: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_id: typing.Optional[builtins.str] = None,
        repo_name: typing.Optional[builtins.str] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch_name: Name of the branch to build. Exactly one a of branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch_name CloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one of a branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#commit_sha CloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_id CloudbuildTrigger#project_id}
        :param repo_name: Name of the Cloud Source Repository. If omitted, the name "default" is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_name CloudbuildTrigger#repo_name}
        :param tag_name: Name of the tag to build. Exactly one of a branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag_name CloudbuildTrigger#tag_name}
        '''
        value = CloudbuildTriggerTriggerTemplate(
            branch_name=branch_name,
            commit_sha=commit_sha,
            dir=dir,
            invert_regex=invert_regex,
            project_id=project_id,
            repo_name=repo_name,
            tag_name=tag_name,
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerTemplate", [value]))

    @jsii.member(jsii_name="putWebhookConfig")
    def put_webhook_config(self, *, secret: builtins.str) -> None:
        '''
        :param secret: Resource name for the secret required as a URL parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret CloudbuildTrigger#secret}
        '''
        value = CloudbuildTriggerWebhookConfig(secret=secret)

        return typing.cast(None, jsii.invoke(self, "putWebhookConfig", [value]))

    @jsii.member(jsii_name="resetApprovalConfig")
    def reset_approval_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalConfig", []))

    @jsii.member(jsii_name="resetBitbucketServerTriggerConfig")
    def reset_bitbucket_server_trigger_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitbucketServerTriggerConfig", []))

    @jsii.member(jsii_name="resetBuildAttribute")
    def reset_build_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildAttribute", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetGitFileSource")
    def reset_git_file_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitFileSource", []))

    @jsii.member(jsii_name="resetGithub")
    def reset_github(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithub", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoredFiles")
    def reset_ignored_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoredFiles", []))

    @jsii.member(jsii_name="resetIncludeBuildLogs")
    def reset_include_build_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeBuildLogs", []))

    @jsii.member(jsii_name="resetIncludedFiles")
    def reset_included_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedFiles", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPubsubConfig")
    def reset_pubsub_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubConfig", []))

    @jsii.member(jsii_name="resetRepositoryEventConfig")
    def reset_repository_event_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryEventConfig", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSourceToBuild")
    def reset_source_to_build(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceToBuild", []))

    @jsii.member(jsii_name="resetSubstitutions")
    def reset_substitutions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstitutions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTriggerTemplate")
    def reset_trigger_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerTemplate", []))

    @jsii.member(jsii_name="resetWebhookConfig")
    def reset_webhook_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookConfig", []))

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
    @jsii.member(jsii_name="approvalConfig")
    def approval_config(self) -> "CloudbuildTriggerApprovalConfigOutputReference":
        return typing.cast("CloudbuildTriggerApprovalConfigOutputReference", jsii.get(self, "approvalConfig"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerTriggerConfig")
    def bitbucket_server_trigger_config(
        self,
    ) -> "CloudbuildTriggerBitbucketServerTriggerConfigOutputReference":
        return typing.cast("CloudbuildTriggerBitbucketServerTriggerConfigOutputReference", jsii.get(self, "bitbucketServerTriggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> "CloudbuildTriggerBuildOutputReference":
        return typing.cast("CloudbuildTriggerBuildOutputReference", jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="gitFileSource")
    def git_file_source(self) -> "CloudbuildTriggerGitFileSourceOutputReference":
        return typing.cast("CloudbuildTriggerGitFileSourceOutputReference", jsii.get(self, "gitFileSource"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> "CloudbuildTriggerGithubOutputReference":
        return typing.cast("CloudbuildTriggerGithubOutputReference", jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="pubsubConfig")
    def pubsub_config(self) -> "CloudbuildTriggerPubsubConfigOutputReference":
        return typing.cast("CloudbuildTriggerPubsubConfigOutputReference", jsii.get(self, "pubsubConfig"))

    @builtins.property
    @jsii.member(jsii_name="repositoryEventConfig")
    def repository_event_config(
        self,
    ) -> "CloudbuildTriggerRepositoryEventConfigOutputReference":
        return typing.cast("CloudbuildTriggerRepositoryEventConfigOutputReference", jsii.get(self, "repositoryEventConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceToBuild")
    def source_to_build(self) -> "CloudbuildTriggerSourceToBuildOutputReference":
        return typing.cast("CloudbuildTriggerSourceToBuildOutputReference", jsii.get(self, "sourceToBuild"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudbuildTriggerTimeoutsOutputReference":
        return typing.cast("CloudbuildTriggerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="triggerId")
    def trigger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerId"))

    @builtins.property
    @jsii.member(jsii_name="triggerTemplate")
    def trigger_template(self) -> "CloudbuildTriggerTriggerTemplateOutputReference":
        return typing.cast("CloudbuildTriggerTriggerTemplateOutputReference", jsii.get(self, "triggerTemplate"))

    @builtins.property
    @jsii.member(jsii_name="webhookConfig")
    def webhook_config(self) -> "CloudbuildTriggerWebhookConfigOutputReference":
        return typing.cast("CloudbuildTriggerWebhookConfigOutputReference", jsii.get(self, "webhookConfig"))

    @builtins.property
    @jsii.member(jsii_name="approvalConfigInput")
    def approval_config_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerApprovalConfig"]:
        return typing.cast(typing.Optional["CloudbuildTriggerApprovalConfig"], jsii.get(self, "approvalConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerTriggerConfigInput")
    def bitbucket_server_trigger_config_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfig"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfig"], jsii.get(self, "bitbucketServerTriggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="buildAttributeInput")
    def build_attribute_input(self) -> typing.Optional["CloudbuildTriggerBuild"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBuild"], jsii.get(self, "buildAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="gitFileSourceInput")
    def git_file_source_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerGitFileSource"]:
        return typing.cast(typing.Optional["CloudbuildTriggerGitFileSource"], jsii.get(self, "gitFileSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(self) -> typing.Optional["CloudbuildTriggerGithub"]:
        return typing.cast(typing.Optional["CloudbuildTriggerGithub"], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoredFilesInput")
    def ignored_files_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignoredFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeBuildLogsInput")
    def include_build_logs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeBuildLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedFilesInput")
    def included_files_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubConfigInput")
    def pubsub_config_input(self) -> typing.Optional["CloudbuildTriggerPubsubConfig"]:
        return typing.cast(typing.Optional["CloudbuildTriggerPubsubConfig"], jsii.get(self, "pubsubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryEventConfigInput")
    def repository_event_config_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerRepositoryEventConfig"]:
        return typing.cast(typing.Optional["CloudbuildTriggerRepositoryEventConfig"], jsii.get(self, "repositoryEventConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceToBuildInput")
    def source_to_build_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerSourceToBuild"]:
        return typing.cast(typing.Optional["CloudbuildTriggerSourceToBuild"], jsii.get(self, "sourceToBuildInput"))

    @builtins.property
    @jsii.member(jsii_name="substitutionsInput")
    def substitutions_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "substitutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudbuildTriggerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudbuildTriggerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTemplateInput")
    def trigger_template_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerTriggerTemplate"]:
        return typing.cast(typing.Optional["CloudbuildTriggerTriggerTemplate"], jsii.get(self, "triggerTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookConfigInput")
    def webhook_config_input(self) -> typing.Optional["CloudbuildTriggerWebhookConfig"]:
        return typing.cast(typing.Optional["CloudbuildTriggerWebhookConfig"], jsii.get(self, "webhookConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaff1c6f5bbf9d67a6ed97c3dcb4b48bedaf0d2abc434e487c2de9120cd3ea8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f41d2ede926b7f8bc85da18071bc2494b0fc39b8d54d2d997f7c1239fdf799b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5a3b44164e142d47c17baa865b670ee186d30dace45b16fa82974c7db30ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be27be8662ee255dbc2564e6d31baae3db0b694464c1e4f91232b74e446a634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d732bb4c1ff5ec3f7a1e32b0df09678672d801b8866ef2e90d858880be116e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoredFiles")
    def ignored_files(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ignoredFiles"))

    @ignored_files.setter
    def ignored_files(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cc653b744fec770cfdede44370a9c6666a199a92ac3552cbdc4706890627b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoredFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeBuildLogs")
    def include_build_logs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includeBuildLogs"))

    @include_build_logs.setter
    def include_build_logs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15de7566268587465c4dbb72474a3fede438489702f12bdcea72c73a2904a6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeBuildLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedFiles")
    def included_files(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedFiles"))

    @included_files.setter
    def included_files(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928d8b13415c7b0463e3ccf76d51539cd2b510df417202539c93916d0b2f4664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08000509c9038210b7c67096005c6c4459dac47d5f699205507f40044a025d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfaa1bc7258db05dd34f9c02549f240f6c6ff6cff5c8d02f4b3559faad0b8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a883dd14345e7dc81921feef0e5dcf24b415995f0fbb05beaf416c675279af0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a229bbc14e61a0d7f0a3b0a79f8618dce6e64164e1381fddb983e40455ef335e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutions")
    def substitutions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitutions"))

    @substitutions.setter
    def substitutions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53916dbfd55bae4d459d62ebc515a4156197b3bd4407a60fbe448f79377f3503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd3b7a555eecda4d4515bdb069df10f609f568b521fa2934d10d58c5840c56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerApprovalConfig",
    jsii_struct_bases=[],
    name_mapping={"approval_required": "approvalRequired"},
)
class CloudbuildTriggerApprovalConfig:
    def __init__(
        self,
        *,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_required: Whether or not approval is needed. If this is set on a build, it will become pending when run, and will need to be explicitly approved to start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#approval_required CloudbuildTrigger#approval_required}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3de77cdb1e8fc27cf964d9a3d6dfa80906445748fa9580baa5fdcc1eae621db)
            check_type(argname="argument approval_required", value=approval_required, expected_type=type_hints["approval_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if approval_required is not None:
            self._values["approval_required"] = approval_required

    @builtins.property
    def approval_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not approval is needed.

        If this is set on a build, it will become pending when run,
        and will need to be explicitly approved to start.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#approval_required CloudbuildTrigger#approval_required}
        '''
        result = self._values.get("approval_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerApprovalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerApprovalConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerApprovalConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04110b611627cfe8a9ee234736d82bc24a8e5475124e910aa2205d96110bc498)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApprovalRequired")
    def reset_approval_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalRequired", []))

    @builtins.property
    @jsii.member(jsii_name="approvalRequiredInput")
    def approval_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "approvalRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalRequired")
    def approval_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "approvalRequired"))

    @approval_required.setter
    def approval_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af91fdde7161c07912fc27572d4c4e835b7807b1d710702d18eb9c837ec05f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerApprovalConfig]:
        return typing.cast(typing.Optional[CloudbuildTriggerApprovalConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerApprovalConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555e081f68cb55d9a30174f1c74fd3d4c8224b86986197a423512d17e0523eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBitbucketServerTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bitbucket_server_config_resource": "bitbucketServerConfigResource",
        "project_key": "projectKey",
        "repo_slug": "repoSlug",
        "pull_request": "pullRequest",
        "push": "push",
    },
)
class CloudbuildTriggerBitbucketServerTriggerConfig:
    def __init__(
        self,
        *,
        bitbucket_server_config_resource: builtins.str,
        project_key: builtins.str,
        repo_slug: builtins.str,
        pull_request: typing.Optional[typing.Union["CloudbuildTriggerBitbucketServerTriggerConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["CloudbuildTriggerBitbucketServerTriggerConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bitbucket_server_config_resource: The Bitbucket server config resource that this trigger config maps to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config_resource CloudbuildTrigger#bitbucket_server_config_resource}
        :param project_key: Key of the project that the repo is in. For example: The key for https://mybitbucket.server/projects/TEST/repos/test-repo is "TEST". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_key CloudbuildTrigger#project_key}
        :param repo_slug: Slug of the repository. A repository slug is a URL-friendly version of a repository name, automatically generated by Bitbucket for use in the URL. For example, if the repository name is 'test repo', in the URL it would become 'test-repo' as in https://mybitbucket.server/projects/TEST/repos/test-repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_slug CloudbuildTrigger#repo_slug}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        if isinstance(pull_request, dict):
            pull_request = CloudbuildTriggerBitbucketServerTriggerConfigPullRequest(**pull_request)
        if isinstance(push, dict):
            push = CloudbuildTriggerBitbucketServerTriggerConfigPush(**push)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d74d67d5094e75eaa8d5de697d6f6127aa2556f28117a54f1ab61d5974cbc40)
            check_type(argname="argument bitbucket_server_config_resource", value=bitbucket_server_config_resource, expected_type=type_hints["bitbucket_server_config_resource"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument repo_slug", value=repo_slug, expected_type=type_hints["repo_slug"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bitbucket_server_config_resource": bitbucket_server_config_resource,
            "project_key": project_key,
            "repo_slug": repo_slug,
        }
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if push is not None:
            self._values["push"] = push

    @builtins.property
    def bitbucket_server_config_resource(self) -> builtins.str:
        '''The Bitbucket server config resource that this trigger config maps to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config_resource CloudbuildTrigger#bitbucket_server_config_resource}
        '''
        result = self._values.get("bitbucket_server_config_resource")
        assert result is not None, "Required property 'bitbucket_server_config_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''Key of the project that the repo is in. For example: The key for https://mybitbucket.server/projects/TEST/repos/test-repo is "TEST".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_key CloudbuildTrigger#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_slug(self) -> builtins.str:
        '''Slug of the repository.

        A repository slug is a URL-friendly version of a repository name, automatically generated by Bitbucket for use in the URL.
        For example, if the repository name is 'test repo', in the URL it would become 'test-repo' as in https://mybitbucket.server/projects/TEST/repos/test-repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_slug CloudbuildTrigger#repo_slug}
        '''
        result = self._values.get("repo_slug")
        assert result is not None, "Required property 'repo_slug' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pull_request(
        self,
    ) -> typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPullRequest"], result)

    @builtins.property
    def push(
        self,
    ) -> typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPush"]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPush"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBitbucketServerTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBitbucketServerTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBitbucketServerTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b09debc590369e1cb77f26e69b6e0c7dfd74392c96a0495463914e24e26c7b2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPullRequest")
    def put_pull_request(
        self,
        *,
        branch: builtins.str,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment /gcbrun. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        value = CloudbuildTriggerBitbucketServerTriggerConfigPullRequest(
            branch=branch, comment_control=comment_control, invert_regex=invert_regex
        )

        return typing.cast(None, jsii.invoke(self, "putPullRequest", [value]))

    @jsii.member(jsii_name="putPush")
    def put_push(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the gitRef regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        value = CloudbuildTriggerBitbucketServerTriggerConfigPush(
            branch=branch, invert_regex=invert_regex, tag=tag
        )

        return typing.cast(None, jsii.invoke(self, "putPush", [value]))

    @jsii.member(jsii_name="resetPullRequest")
    def reset_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequest", []))

    @jsii.member(jsii_name="resetPush")
    def reset_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPush", []))

    @builtins.property
    @jsii.member(jsii_name="pullRequest")
    def pull_request(
        self,
    ) -> "CloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference":
        return typing.cast("CloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(
        self,
    ) -> "CloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference":
        return typing.cast("CloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference", jsii.get(self, "push"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerConfigResourceInput")
    def bitbucket_server_config_resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitbucketServerConfigResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestInput")
    def pull_request_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPullRequest"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPush"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBitbucketServerTriggerConfigPush"], jsii.get(self, "pushInput"))

    @builtins.property
    @jsii.member(jsii_name="repoSlugInput")
    def repo_slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoSlugInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerConfigResource")
    def bitbucket_server_config_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitbucketServerConfigResource"))

    @bitbucket_server_config_resource.setter
    def bitbucket_server_config_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58fb8ca44a63d0f6d36615cd634ea9d1528e818f8bada2ee73913ff91d5277c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitbucketServerConfigResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc0d707f98dc7d9554f8ed31177294928b693bb02f3baf97091828e8d6e0965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoSlug")
    def repo_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoSlug"))

    @repo_slug.setter
    def repo_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7816e52d2ee311f55d5ededfa9d004a5e4d7a212415432c350147e1aa174fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfig]:
        return typing.cast(typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774a9f5db01134ade503f810008a88409a1d6920fc06339b7840a4e7920aa941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBitbucketServerTriggerConfigPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "comment_control": "commentControl",
        "invert_regex": "invertRegex",
    },
)
class CloudbuildTriggerBitbucketServerTriggerConfigPullRequest:
    def __init__(
        self,
        *,
        branch: builtins.str,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment /gcbrun. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cfbe5c47fca65fb28975f6bacef041b0be64b3f8424e75be554ad0e9685fa07)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument comment_control", value=comment_control, expected_type=type_hints["comment_control"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
        }
        if comment_control is not None:
            self._values["comment_control"] = comment_control
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex

    @builtins.property
    def branch(self) -> builtins.str:
        '''Regex of branches to match.

        The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment_control(self) -> typing.Optional[builtins.str]:
        '''Configure builds to run whether a repository owner or collaborator need to comment /gcbrun. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        '''
        result = self._values.get("comment_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, branches that do NOT match the git_ref will trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBitbucketServerTriggerConfigPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19059f58712f1c524c832f550c926169bafff220df14c739e977dced58d2735a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommentControl")
    def reset_comment_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommentControl", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="commentControlInput")
    def comment_control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentControlInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b106bbb738563442422734f13351e9f5d3b5946c0f4d9a25d1c3ee498ba2599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentControl")
    def comment_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commentControl"))

    @comment_control.setter
    def comment_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddd79b2a296589b0427adea853dc51ea0ebad1efe0f3a7070149ff85e1250b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a0fb0f8f82b2a3f9e058e347058a912b56e42900a2b28feae4425405dadc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPullRequest]:
        return typing.cast(typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e7396eb7365e9e556fd5b9b2d81a1eba4b69d4a81b0bb1055cb7b2b5ce2786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBitbucketServerTriggerConfigPush",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "invert_regex": "invertRegex", "tag": "tag"},
)
class CloudbuildTriggerBitbucketServerTriggerConfigPush:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the gitRef regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee112fd6a2a3e4713b80dc25f9798c6dd325ee616cb4d57fb797a7838a235193)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Regex of branches to match.  Specify only one of branch or tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, only trigger a build if the revision regex does NOT match the gitRef regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Regex of tags to match.  Specify only one of branch or tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBitbucketServerTriggerConfigPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__385993c252e7edbdb2db708f60cd35c753d3f9290ed112410fc63c39cd24d517)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e90e2c80cac1450b6dab4ed9d82f54e3ea9f71f7980d90013441236f71320f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d394815551349644343e242e57637644512940edcd184aa4c8f4a2b18662aa92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c6d1939bf57e5c8ae46b5554a56f816d1f6495ed46268888e43eeeb2908cc9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPush]:
        return typing.cast(typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPush], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPush],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b6d21bfaefc44d3e1aa5afe7768918cd83eeefb90fcbc2a016023159f8b823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuild",
    jsii_struct_bases=[],
    name_mapping={
        "step": "step",
        "artifacts": "artifacts",
        "available_secrets": "availableSecrets",
        "images": "images",
        "logs_bucket": "logsBucket",
        "options": "options",
        "queue_ttl": "queueTtl",
        "secret": "secret",
        "source": "source",
        "substitutions": "substitutions",
        "tags": "tags",
        "timeout": "timeout",
    },
)
class CloudbuildTriggerBuild:
    def __init__(
        self,
        *,
        step: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildStep", typing.Dict[builtins.str, typing.Any]]]],
        artifacts: typing.Optional[typing.Union["CloudbuildTriggerBuildArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        available_secrets: typing.Optional[typing.Union["CloudbuildTriggerBuildAvailableSecrets", typing.Dict[builtins.str, typing.Any]]] = None,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        logs_bucket: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["CloudbuildTriggerBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        queue_ttl: typing.Optional[builtins.str] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union["CloudbuildTriggerBuildSource", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param step: step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#step CloudbuildTrigger#step}
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#artifacts CloudbuildTrigger#artifacts}
        :param available_secrets: available_secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#available_secrets CloudbuildTrigger#available_secrets}
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images are pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build status is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#images CloudbuildTrigger#images}
        :param logs_bucket: Google Cloud Storage bucket where logs should be written. Logs file names will be of the format ${logsBucket}/log-${build_id}.txt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#logs_bucket CloudbuildTrigger#logs_bucket}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#options CloudbuildTrigger#options}
        :param queue_ttl: TTL in queue for this build. If provided and the build is enqueued longer than this value, the build will expire and the build status will be EXPIRED. The TTL starts ticking from createTime. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#queue_ttl CloudbuildTrigger#queue_ttl}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret CloudbuildTrigger#secret}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source CloudbuildTrigger#source}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a Build. These are not docker tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tags CloudbuildTrigger#tags}
        :param timeout: Amount of time that this build should be allowed to run, to second granularity. If this amount of time elapses, work on the build will cease and the build status will be TIMEOUT. This timeout must be equal to or greater than the sum of the timeouts for build steps within the build. The expected format is the number of seconds followed by s. Default time is ten minutes (600s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeout CloudbuildTrigger#timeout}
        '''
        if isinstance(artifacts, dict):
            artifacts = CloudbuildTriggerBuildArtifacts(**artifacts)
        if isinstance(available_secrets, dict):
            available_secrets = CloudbuildTriggerBuildAvailableSecrets(**available_secrets)
        if isinstance(options, dict):
            options = CloudbuildTriggerBuildOptions(**options)
        if isinstance(source, dict):
            source = CloudbuildTriggerBuildSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0254e3eff0c4eb03082410acf57109ba975934519d630a276f633e4401a597bb)
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument available_secrets", value=available_secrets, expected_type=type_hints["available_secrets"])
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument logs_bucket", value=logs_bucket, expected_type=type_hints["logs_bucket"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument queue_ttl", value=queue_ttl, expected_type=type_hints["queue_ttl"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument substitutions", value=substitutions, expected_type=type_hints["substitutions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "step": step,
        }
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if available_secrets is not None:
            self._values["available_secrets"] = available_secrets
        if images is not None:
            self._values["images"] = images
        if logs_bucket is not None:
            self._values["logs_bucket"] = logs_bucket
        if options is not None:
            self._values["options"] = options
        if queue_ttl is not None:
            self._values["queue_ttl"] = queue_ttl
        if secret is not None:
            self._values["secret"] = secret
        if source is not None:
            self._values["source"] = source
        if substitutions is not None:
            self._values["substitutions"] = substitutions
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def step(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStep"]]:
        '''step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#step CloudbuildTrigger#step}
        '''
        result = self._values.get("step")
        assert result is not None, "Required property 'step' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStep"]], result)

    @builtins.property
    def artifacts(self) -> typing.Optional["CloudbuildTriggerBuildArtifacts"]:
        '''artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#artifacts CloudbuildTrigger#artifacts}
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildArtifacts"], result)

    @builtins.property
    def available_secrets(
        self,
    ) -> typing.Optional["CloudbuildTriggerBuildAvailableSecrets"]:
        '''available_secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#available_secrets CloudbuildTrigger#available_secrets}
        '''
        result = self._values.get("available_secrets")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildAvailableSecrets"], result)

    @builtins.property
    def images(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of images to be pushed upon the successful completion of all build steps.

        The images are pushed using the builder service account's credentials.
        The digests of the pushed images will be stored in the Build resource's results field.
        If any of the images fail to be pushed, the build status is marked FAILURE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#images CloudbuildTrigger#images}
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logs_bucket(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage bucket where logs should be written. Logs file names will be of the format ${logsBucket}/log-${build_id}.txt.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#logs_bucket CloudbuildTrigger#logs_bucket}
        '''
        result = self._values.get("logs_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional["CloudbuildTriggerBuildOptions"]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#options CloudbuildTrigger#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildOptions"], result)

    @builtins.property
    def queue_ttl(self) -> typing.Optional[builtins.str]:
        '''TTL in queue for this build.

        If provided and the build is enqueued longer than this value,
        the build will expire and the build status will be EXPIRED.
        The TTL starts ticking from createTime.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#queue_ttl CloudbuildTrigger#queue_ttl}
        '''
        result = self._values.get("queue_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildSecret"]]]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret CloudbuildTrigger#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildSecret"]]], result)

    @builtins.property
    def source(self) -> typing.Optional["CloudbuildTriggerBuildSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source CloudbuildTrigger#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildSource"], result)

    @builtins.property
    def substitutions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Substitutions data for Build resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        '''
        result = self._values.get("substitutions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags for annotation of a Build. These are not docker tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tags CloudbuildTrigger#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Amount of time that this build should be allowed to run, to second granularity.

        If this amount of time elapses, work on the build will cease and the build status will be TIMEOUT.
        This timeout must be equal to or greater than the sum of the timeouts for build steps within the build.
        The expected format is the number of seconds followed by s.
        Default time is ten minutes (600s).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeout CloudbuildTrigger#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "images": "images",
        "maven_artifacts": "mavenArtifacts",
        "npm_packages": "npmPackages",
        "objects": "objects",
        "python_packages": "pythonPackages",
    },
)
class CloudbuildTriggerBuildArtifacts:
    def __init__(
        self,
        *,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        maven_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildArtifactsMavenArtifacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        npm_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildArtifactsNpmPackages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        objects: typing.Optional[typing.Union["CloudbuildTriggerBuildArtifactsObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        python_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildArtifactsPythonPackages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images will be pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#images CloudbuildTrigger#images}
        :param maven_artifacts: maven_artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#maven_artifacts CloudbuildTrigger#maven_artifacts}
        :param npm_packages: npm_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#npm_packages CloudbuildTrigger#npm_packages}
        :param objects: objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#objects CloudbuildTrigger#objects}
        :param python_packages: python_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#python_packages CloudbuildTrigger#python_packages}
        '''
        if isinstance(objects, dict):
            objects = CloudbuildTriggerBuildArtifactsObjects(**objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b540c13286c7a330ca51201ca60dd1bb1673f6dbf5437d4338308cec9d8b83)
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument maven_artifacts", value=maven_artifacts, expected_type=type_hints["maven_artifacts"])
            check_type(argname="argument npm_packages", value=npm_packages, expected_type=type_hints["npm_packages"])
            check_type(argname="argument objects", value=objects, expected_type=type_hints["objects"])
            check_type(argname="argument python_packages", value=python_packages, expected_type=type_hints["python_packages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if images is not None:
            self._values["images"] = images
        if maven_artifacts is not None:
            self._values["maven_artifacts"] = maven_artifacts
        if npm_packages is not None:
            self._values["npm_packages"] = npm_packages
        if objects is not None:
            self._values["objects"] = objects
        if python_packages is not None:
            self._values["python_packages"] = python_packages

    @builtins.property
    def images(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of images to be pushed upon the successful completion of all build steps.

        The images will be pushed using the builder service account's credentials.

        The digests of the pushed images will be stored in the Build resource's results field.

        If any of the images fail to be pushed, the build is marked FAILURE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#images CloudbuildTrigger#images}
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def maven_artifacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsMavenArtifacts"]]]:
        '''maven_artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#maven_artifacts CloudbuildTrigger#maven_artifacts}
        '''
        result = self._values.get("maven_artifacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsMavenArtifacts"]]], result)

    @builtins.property
    def npm_packages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsNpmPackages"]]]:
        '''npm_packages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#npm_packages CloudbuildTrigger#npm_packages}
        '''
        result = self._values.get("npm_packages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsNpmPackages"]]], result)

    @builtins.property
    def objects(self) -> typing.Optional["CloudbuildTriggerBuildArtifactsObjects"]:
        '''objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#objects CloudbuildTrigger#objects}
        '''
        result = self._values.get("objects")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildArtifactsObjects"], result)

    @builtins.property
    def python_packages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsPythonPackages"]]]:
        '''python_packages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#python_packages CloudbuildTrigger#python_packages}
        '''
        result = self._values.get("python_packages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsPythonPackages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsMavenArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "group_id": "groupId",
        "path": "path",
        "repository": "repository",
        "version": "version",
    },
)
class CloudbuildTriggerBuildArtifactsMavenArtifacts:
    def __init__(
        self,
        *,
        artifact_id: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: Maven artifactId value used when uploading the artifact to Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#artifact_id CloudbuildTrigger#artifact_id}
        :param group_id: Maven groupId value used when uploading the artifact to Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#group_id CloudbuildTrigger#group_id}
        :param path: Path to an artifact in the build's workspace to be uploaded to Artifact Registry. This can be either an absolute path, e.g. /workspace/my-app/target/my-app-1.0.SNAPSHOT.jar or a relative path from /workspace, e.g. my-app/target/my-app-1.0.SNAPSHOT.jar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        :param repository: Artifact Registry repository, in the form "https://$REGION-maven.pkg.dev/$PROJECT/$REPOSITORY". Artifact in the workspace specified by path will be uploaded to Artifact Registry with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        :param version: Maven version value used when uploading the artifact to Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#version CloudbuildTrigger#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b03984ffdae9a1f8a9ad00af72ec547db607818e298946682eff53835285b0)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifact_id is not None:
            self._values["artifact_id"] = artifact_id
        if group_id is not None:
            self._values["group_id"] = group_id
        if path is not None:
            self._values["path"] = path
        if repository is not None:
            self._values["repository"] = repository
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def artifact_id(self) -> typing.Optional[builtins.str]:
        '''Maven artifactId value used when uploading the artifact to Artifact Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#artifact_id CloudbuildTrigger#artifact_id}
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Maven groupId value used when uploading the artifact to Artifact Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#group_id CloudbuildTrigger#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to an artifact in the build's workspace to be uploaded to Artifact Registry.

        This can be either an absolute path, e.g. /workspace/my-app/target/my-app-1.0.SNAPSHOT.jar or a relative path from /workspace, e.g. my-app/target/my-app-1.0.SNAPSHOT.jar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry repository, in the form "https://$REGION-maven.pkg.dev/$PROJECT/$REPOSITORY".

        Artifact in the workspace specified by path will be uploaded to Artifact Registry with this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Maven version value used when uploading the artifact to Artifact Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#version CloudbuildTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildArtifactsMavenArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildArtifactsMavenArtifactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsMavenArtifactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e4ee23c5d0076d90a4b31225dc25b86e8c4b34f11e606bcae1f2bd0a3aa63c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be7b096ce27bb292d34c0eb70753250278354f68eaf0b0190088ee1b7babcd8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc73282e32fc59c37a3296e5664c13e052cf29fd7936c1cc79de08001ba8c28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6db03298f782cec272e724a44653260cff5e81b54c11665925afb94d399fa333)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c30acea698c59b175113818f902186559cd0feb560938000fc2ebaa77651fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsMavenArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsMavenArtifacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsMavenArtifacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0052065116ed5af987e84221d3cb6e517f873a00ec18c9d225f261e6eadcb62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d0b3e3f878a90313070dc69d8e8ba42d5d42e9cab7f93c227431284c9942a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArtifactId")
    def reset_artifact_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactId", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e170477b1413ac0c496c8e2849e133e32d352d9323bc45e09508138fb3b2590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e8afd63dc0d25a3dcfccbfa349d278c3eabee6f510dd480bb47933ae9ad4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf78fca30cfe845872f93c9f5fed7d3a927331dc29b462bcf870d3dd3cb3890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fddb92874da4467b6c1f377218f402f48f37fb870b04aee136ccddf2a91a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c46cdee66619f59b20fd05202c3fa97a4d849973424db93656ea3a5aaefaeb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsMavenArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsMavenArtifacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsMavenArtifacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ccc141017a901de53c395756e8ee8878f1c15a0abdb0821729316518b7b76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsNpmPackages",
    jsii_struct_bases=[],
    name_mapping={"package_path": "packagePath", "repository": "repository"},
)
class CloudbuildTriggerBuildArtifactsNpmPackages:
    def __init__(
        self,
        *,
        package_path: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param package_path: Path to the package.json. e.g. workspace/path/to/package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#package_path CloudbuildTrigger#package_path}
        :param repository: Artifact Registry repository, in the form "https://$REGION-npm.pkg.dev/$PROJECT/$REPOSITORY". Npm package in the workspace specified by path will be zipped and uploaded to Artifact Registry with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385a85f99baec2d5b42381550f6c1dec820a36489f1cbb4950f3486689241a4c)
            check_type(argname="argument package_path", value=package_path, expected_type=type_hints["package_path"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if package_path is not None:
            self._values["package_path"] = package_path
        if repository is not None:
            self._values["repository"] = repository

    @builtins.property
    def package_path(self) -> typing.Optional[builtins.str]:
        '''Path to the package.json. e.g. workspace/path/to/package.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#package_path CloudbuildTrigger#package_path}
        '''
        result = self._values.get("package_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry repository, in the form "https://$REGION-npm.pkg.dev/$PROJECT/$REPOSITORY".

        Npm package in the workspace specified by path will be zipped and uploaded to Artifact Registry with this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildArtifactsNpmPackages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildArtifactsNpmPackagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsNpmPackagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__436f25c2ce997db76dd329ae9b6bda9cd8fcf3d233f3293651d83e9b4e870e9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildArtifactsNpmPackagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c2b3f85e2a65899bb2a60c630c8d39f936c6f4bc44acca07b4e9d823b9bae3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildArtifactsNpmPackagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef78d37d2f1dfcbee4e92032f3633172459399ff0f091e5fb1aec5c6732b3874)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93cbdc34728b9fb505be8e5c0b99895cb49254f28cc89027bfd67ecee283273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c732a8c5f7a4d8d915817b621df200c445bd6af341b8875d4e7dbbebda05777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsNpmPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsNpmPackages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsNpmPackages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed98b25d278196f59a13f2305b8ceb0307af8485c79a800c2bde1bbc62697881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildArtifactsNpmPackagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsNpmPackagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff3de44c6655a23a29bb81a03d8e06793d2f92e225d4e44c0818a64438a810db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPackagePath")
    def reset_package_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackagePath", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @builtins.property
    @jsii.member(jsii_name="packagePathInput")
    def package_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packagePathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="packagePath")
    def package_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packagePath"))

    @package_path.setter
    def package_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc40f34033cf75467d70babf09f054f6bfcc06f0a01ba5e6a18a6f3547406aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packagePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bb4cc5b5bedc47556e87debfe6b1d1b346d0ee6eba5aceffd351f88e78d892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsNpmPackages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsNpmPackages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsNpmPackages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5db3de4b755d78ffea611ce35f7efdf7be78f68d7e1dcdab5b492ffb5eb9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsObjects",
    jsii_struct_bases=[],
    name_mapping={"location": "location", "paths": "paths"},
)
class CloudbuildTriggerBuildArtifactsObjects:
    def __init__(
        self,
        *,
        location: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: Cloud Storage bucket and optional object path, in the form "gs://bucket/path/to/somewhere/". Files in the workspace matching any path pattern will be uploaded to Cloud Storage with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#location CloudbuildTrigger#location}
        :param paths: Path globs used to match files in the build's workspace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#paths CloudbuildTrigger#paths}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3a1f281add22166e681f678ce2c9e8ddebaaffb2e6578b95e891f989aae955)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location is not None:
            self._values["location"] = location
        if paths is not None:
            self._values["paths"] = paths

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Cloud Storage bucket and optional object path, in the form "gs://bucket/path/to/somewhere/".

        Files in the workspace matching any path pattern will be uploaded to Cloud Storage with
        this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#location CloudbuildTrigger#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Path globs used to match files in the build's workspace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#paths CloudbuildTrigger#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildArtifactsObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildArtifactsObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82b0208164bd1cffbb2593dce11bd415e7e299bd64c0e82c67fb5c559b8df47f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @builtins.property
    @jsii.member(jsii_name="timing")
    def timing(self) -> "CloudbuildTriggerBuildArtifactsObjectsTimingList":
        return typing.cast("CloudbuildTriggerBuildArtifactsObjectsTimingList", jsii.get(self, "timing"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0633d4c44c9ddf6ac3da1c7a29cd57b9e1ca527e335915e916a20a7a1c99ac6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec885b94486b764979236273dcc9c2c89b9eb7e4f0492aeccdb892f9a76e032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuildArtifactsObjects]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildArtifactsObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildArtifactsObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f32dc56c76c8e2c9d4353e5190e61f14a6a727f5b533673b697e44700606157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsObjectsTiming",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudbuildTriggerBuildArtifactsObjectsTiming:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildArtifactsObjectsTiming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildArtifactsObjectsTimingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsObjectsTimingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa376a43430cb123116e5fe81b3124b92601dc27d1e135ce68e98bb76c7a2b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildArtifactsObjectsTimingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5037667761618e9799b4dfdac200de78917f335a6cc675ecbde750afb606ab7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildArtifactsObjectsTimingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80e5bc22f2653c935c920dacb5d9db5ebe3b9fe6280c74f5cf4886e6de18372)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa1b91191d307ac154c591d29a423a22ed194810760b5e12832175cffc698fe3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__811ba882bb20b02a94caf452d98b64b38f3399abdaf66969cd4af0950f239516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildArtifactsObjectsTimingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsObjectsTimingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce7c526aef295deaebeba0fd3369ba8e855b4312fa68bf32864ad8a57008cd85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerBuildArtifactsObjectsTiming]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildArtifactsObjectsTiming], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildArtifactsObjectsTiming],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4dffcbd11e57a6f0f037713c7818a9996f34e5d97b8daca0eee79085cbc6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5917202b4b3a272ef3fcefcfbe7960261f426e17c882c751cda5a8bdccc7a39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMavenArtifacts")
    def put_maven_artifacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5cb013d85a217a128cba25afa149914681f441458ba0352aeb56cb17b11559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMavenArtifacts", [value]))

    @jsii.member(jsii_name="putNpmPackages")
    def put_npm_packages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6fafe611587e866f5644e7f753e21568b45def6882aa3a3cf95629cbe4c4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNpmPackages", [value]))

    @jsii.member(jsii_name="putObjects")
    def put_objects(
        self,
        *,
        location: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: Cloud Storage bucket and optional object path, in the form "gs://bucket/path/to/somewhere/". Files in the workspace matching any path pattern will be uploaded to Cloud Storage with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#location CloudbuildTrigger#location}
        :param paths: Path globs used to match files in the build's workspace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#paths CloudbuildTrigger#paths}
        '''
        value = CloudbuildTriggerBuildArtifactsObjects(location=location, paths=paths)

        return typing.cast(None, jsii.invoke(self, "putObjects", [value]))

    @jsii.member(jsii_name="putPythonPackages")
    def put_python_packages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildArtifactsPythonPackages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fd14739e192a8655fdb7784e44e2e423af5239f5dfb97f88fe9aa72fbc9aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPythonPackages", [value]))

    @jsii.member(jsii_name="resetImages")
    def reset_images(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImages", []))

    @jsii.member(jsii_name="resetMavenArtifacts")
    def reset_maven_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMavenArtifacts", []))

    @jsii.member(jsii_name="resetNpmPackages")
    def reset_npm_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNpmPackages", []))

    @jsii.member(jsii_name="resetObjects")
    def reset_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjects", []))

    @jsii.member(jsii_name="resetPythonPackages")
    def reset_python_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonPackages", []))

    @builtins.property
    @jsii.member(jsii_name="mavenArtifacts")
    def maven_artifacts(self) -> CloudbuildTriggerBuildArtifactsMavenArtifactsList:
        return typing.cast(CloudbuildTriggerBuildArtifactsMavenArtifactsList, jsii.get(self, "mavenArtifacts"))

    @builtins.property
    @jsii.member(jsii_name="npmPackages")
    def npm_packages(self) -> CloudbuildTriggerBuildArtifactsNpmPackagesList:
        return typing.cast(CloudbuildTriggerBuildArtifactsNpmPackagesList, jsii.get(self, "npmPackages"))

    @builtins.property
    @jsii.member(jsii_name="objects")
    def objects(self) -> CloudbuildTriggerBuildArtifactsObjectsOutputReference:
        return typing.cast(CloudbuildTriggerBuildArtifactsObjectsOutputReference, jsii.get(self, "objects"))

    @builtins.property
    @jsii.member(jsii_name="pythonPackages")
    def python_packages(self) -> "CloudbuildTriggerBuildArtifactsPythonPackagesList":
        return typing.cast("CloudbuildTriggerBuildArtifactsPythonPackagesList", jsii.get(self, "pythonPackages"))

    @builtins.property
    @jsii.member(jsii_name="imagesInput")
    def images_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "imagesInput"))

    @builtins.property
    @jsii.member(jsii_name="mavenArtifactsInput")
    def maven_artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsMavenArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsMavenArtifacts]]], jsii.get(self, "mavenArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="npmPackagesInput")
    def npm_packages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsNpmPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsNpmPackages]]], jsii.get(self, "npmPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectsInput")
    def objects_input(self) -> typing.Optional[CloudbuildTriggerBuildArtifactsObjects]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildArtifactsObjects], jsii.get(self, "objectsInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonPackagesInput")
    def python_packages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsPythonPackages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildArtifactsPythonPackages"]]], jsii.get(self, "pythonPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "images"))

    @images.setter
    def images(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c346284bc4a0e9ed389ba0e2346095a4f1723c53f3899894a76920468646600a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "images", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuildArtifacts]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildArtifacts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildArtifacts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93014f3a602c207c298ffca9385517c42c509646647fa5e6311508de5884ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsPythonPackages",
    jsii_struct_bases=[],
    name_mapping={"paths": "paths", "repository": "repository"},
)
class CloudbuildTriggerBuildArtifactsPythonPackages:
    def __init__(
        self,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param paths: Path globs used to match files in the build's workspace. For Python/ Twine, this is usually dist/*, and sometimes additionally an .asc file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#paths CloudbuildTrigger#paths}
        :param repository: Artifact Registry repository, in the form "https://$REGION-python.pkg.dev/$PROJECT/$REPOSITORY". Files in the workspace matching any path pattern will be uploaded to Artifact Registry with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fcb46752b42388b13f587af96cfe72f38621e926402658caaa4ac17c95a389)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if paths is not None:
            self._values["paths"] = paths
        if repository is not None:
            self._values["repository"] = repository

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Path globs used to match files in the build's workspace.

        For Python/ Twine, this is usually dist/*, and sometimes additionally an .asc file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#paths CloudbuildTrigger#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry repository, in the form "https://$REGION-python.pkg.dev/$PROJECT/$REPOSITORY".

        Files in the workspace matching any path pattern will be uploaded to Artifact Registry with this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildArtifactsPythonPackages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildArtifactsPythonPackagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsPythonPackagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2bfe29217d497e93f2561efaa9e8d57cbe1d27a2fc718192985c32fd774f997)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildArtifactsPythonPackagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba5335dc228591443b01e7d99cb5536093bd5da7a27525f9fc4743b216042ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildArtifactsPythonPackagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603e62ea66288a2f861c20919fb4809ff9dc8b804a00d4a480ff484dc9c25c61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382c22a938c51e56d89626e5158b03f79af653d6a980375db786e1d74e7afa52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebccb337961323e1896b32e434cf93d429492cc0b0f0354969521d05e8f7a132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsPythonPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsPythonPackages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsPythonPackages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16cfd72c3f08eef1ecb9e7a7686e618c80d2b85910a9a0448b1140b34b2e5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildArtifactsPythonPackagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildArtifactsPythonPackagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9639a2d685a2c80ca15b73f2e6a97974d7fe9a68d510ad79b53083806c13bf15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7221ebbe2641f3a1d04a3ebadc7a73790e9ae72493c0be48a30e4544ee162b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ace4a5167b0d1de7369fecb4399bdc3c2087b0437e097a2361b5994e937ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsPythonPackages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsPythonPackages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsPythonPackages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdfc4b31d060c2752d33306527cd88f264319b072375c79d0f90b5ffd38b3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildAvailableSecrets",
    jsii_struct_bases=[],
    name_mapping={"secret_manager": "secretManager"},
)
class CloudbuildTriggerBuildAvailableSecrets:
    def __init__(
        self,
        *,
        secret_manager: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildAvailableSecretsSecretManager", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param secret_manager: secret_manager block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_manager CloudbuildTrigger#secret_manager}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f888a277e9a41970509da9d63fa38b59ff6b88acedce818455c07585eee5d6)
            check_type(argname="argument secret_manager", value=secret_manager, expected_type=type_hints["secret_manager"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_manager": secret_manager,
        }

    @builtins.property
    def secret_manager(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildAvailableSecretsSecretManager"]]:
        '''secret_manager block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_manager CloudbuildTrigger#secret_manager}
        '''
        result = self._values.get("secret_manager")
        assert result is not None, "Required property 'secret_manager' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildAvailableSecretsSecretManager"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildAvailableSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildAvailableSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildAvailableSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c040f2b809fc0c6e6bae3445e06b8a4ddf36a79f65d62f68429f80f2d5ec42ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretManager")
    def put_secret_manager(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildAvailableSecretsSecretManager", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f550a1d50b0f30ee1d4b2c1b6c3e6198b5561f8a31590255ddd7242b14a2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretManager", [value]))

    @builtins.property
    @jsii.member(jsii_name="secretManager")
    def secret_manager(
        self,
    ) -> "CloudbuildTriggerBuildAvailableSecretsSecretManagerList":
        return typing.cast("CloudbuildTriggerBuildAvailableSecretsSecretManagerList", jsii.get(self, "secretManager"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerInput")
    def secret_manager_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildAvailableSecretsSecretManager"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildAvailableSecretsSecretManager"]]], jsii.get(self, "secretManagerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuildAvailableSecrets]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildAvailableSecrets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildAvailableSecrets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9272f035c266a8668f4e0a062f67bb690a0e24ebe2c0486f867daf85886a20d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildAvailableSecretsSecretManager",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "version_name": "versionName"},
)
class CloudbuildTriggerBuildAvailableSecretsSecretManager:
    def __init__(self, *, env: builtins.str, version_name: builtins.str) -> None:
        '''
        :param env: Environment variable name to associate with the secret. Secret environment variables must be unique across all of a build's secrets, and must be used by at least one build step. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        :param version_name: Resource name of the SecretVersion. In format: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#version_name CloudbuildTrigger#version_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0c00b71658784f02706e15ad876b6ffd36de0f9d0583def13b3549a150df34)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument version_name", value=version_name, expected_type=type_hints["version_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env": env,
            "version_name": version_name,
        }

    @builtins.property
    def env(self) -> builtins.str:
        '''Environment variable name to associate with the secret.

        Secret environment
        variables must be unique across all of a build's secrets, and must be used
        by at least one build step.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        '''
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_name(self) -> builtins.str:
        '''Resource name of the SecretVersion. In format: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#version_name CloudbuildTrigger#version_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("version_name")
        assert result is not None, "Required property 'version_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildAvailableSecretsSecretManager(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildAvailableSecretsSecretManagerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildAvailableSecretsSecretManagerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38766b751587c68e026b3edd8192d3836a43b7789f3f430cc4f01c1cacf70010)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090ac6f523ec580c66b571e90562b21f0e5002580b407b8f1c414bab5d6cd5b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e319fa2045c2abc7e649131583e2b44c6e785005b947f50ec102f6feb48bfa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__157d4c1e066d052f9a4b745cb8a15008a8729010451274a26397844103e1dec6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e136e74865445c2543e3332a82d70f577e7df459623d4d1e58a67c7b42f6f684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildAvailableSecretsSecretManager]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildAvailableSecretsSecretManager]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildAvailableSecretsSecretManager]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225663e066a35987735209bbca1091d09a3bedb35579bc70da894b3740980beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ff76b4e00e8fca5acf72b0a25c29a5a6e7d0c34ca6ff827bdd28f60b8a0b87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="versionNameInput")
    def version_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "env"))

    @env.setter
    def env(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d841f93832d11cc5431d357236ea70368139662c76e251744ff0d9e55a3b928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionName")
    def version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionName"))

    @version_name.setter
    def version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fdb016249172d6ddd1c837d625cf5e0061d77ace75eec2cbdf292913fca398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildAvailableSecretsSecretManager]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildAvailableSecretsSecretManager]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildAvailableSecretsSecretManager]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80017f0d10621f28b8a0205fd77f87ef9dc4df8a65c7e28e18bd95e485c52810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildOptions",
    jsii_struct_bases=[],
    name_mapping={
        "disk_size_gb": "diskSizeGb",
        "dynamic_substitutions": "dynamicSubstitutions",
        "env": "env",
        "logging": "logging",
        "log_streaming_option": "logStreamingOption",
        "machine_type": "machineType",
        "requested_verify_option": "requestedVerifyOption",
        "secret_env": "secretEnv",
        "source_provenance_hash": "sourceProvenanceHash",
        "substitution_option": "substitutionOption",
        "volumes": "volumes",
        "worker_pool": "workerPool",
    },
)
class CloudbuildTriggerBuildOptions:
    def __init__(
        self,
        *,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        dynamic_substitutions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging: typing.Optional[builtins.str] = None,
        log_streaming_option: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        requested_verify_option: typing.Optional[builtins.str] = None,
        secret_env: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_provenance_hash: typing.Optional[typing.Sequence[builtins.str]] = None,
        substitution_option: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildOptionsVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: Requested disk size for the VM that runs the build. Note that this is NOT "disk free"; some of the space will be used by the operating system and build utilities. Also note that this is the minimum disk size that will be allocated for the build -- the build may run with a larger disk than requested. At present, the maximum disk size is 1000GB; builds that request more than the maximum are rejected with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#disk_size_gb CloudbuildTrigger#disk_size_gb}
        :param dynamic_substitutions: Option to specify whether or not to apply bash style string operations to the substitutions. NOTE this is always enabled for triggered builds and cannot be overridden in the build configuration file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dynamic_substitutions CloudbuildTrigger#dynamic_substitutions}
        :param env: A list of global environment variable definitions that will exist for all build steps in this build. If a variable is defined in both globally and in a build step, the variable will use the build step value. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        :param logging: Option to specify the logging mode, which determines if and where build logs are stored. Possible values: ["LOGGING_UNSPECIFIED", "LEGACY", "GCS_ONLY", "STACKDRIVER_ONLY", "CLOUD_LOGGING_ONLY", "NONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#logging CloudbuildTrigger#logging}
        :param log_streaming_option: Option to define build log streaming behavior to Google Cloud Storage. Possible values: ["STREAM_DEFAULT", "STREAM_ON", "STREAM_OFF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#log_streaming_option CloudbuildTrigger#log_streaming_option}
        :param machine_type: Compute Engine machine type on which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#machine_type CloudbuildTrigger#machine_type}
        :param requested_verify_option: Requested verifiability options. Possible values: ["NOT_VERIFIED", "VERIFIED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#requested_verify_option CloudbuildTrigger#requested_verify_option}
        :param secret_env: A list of global environment variables, which are encrypted using a Cloud Key Management Service crypto key. These values must be specified in the build's Secret. These variables will be available to all build steps in this build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        :param source_provenance_hash: Requested hash for SourceProvenance. Possible values: ["NONE", "SHA256", "MD5"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source_provenance_hash CloudbuildTrigger#source_provenance_hash}
        :param substitution_option: Option to specify behavior when there is an error in the substitution checks. NOTE this is always set to ALLOW_LOOSE for triggered builds and cannot be overridden in the build configuration file. Possible values: ["MUST_MATCH", "ALLOW_LOOSE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitution_option CloudbuildTrigger#substitution_option}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#volumes CloudbuildTrigger#volumes}
        :param worker_pool: Option to specify a WorkerPool for the build. Format projects/{project}/workerPools/{workerPool}. This field is experimental. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#worker_pool CloudbuildTrigger#worker_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9999d74eba2b15df3130a30ba5107516e720a91c2ec69a23b55ae348bd823ab7)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument dynamic_substitutions", value=dynamic_substitutions, expected_type=type_hints["dynamic_substitutions"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument log_streaming_option", value=log_streaming_option, expected_type=type_hints["log_streaming_option"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument requested_verify_option", value=requested_verify_option, expected_type=type_hints["requested_verify_option"])
            check_type(argname="argument secret_env", value=secret_env, expected_type=type_hints["secret_env"])
            check_type(argname="argument source_provenance_hash", value=source_provenance_hash, expected_type=type_hints["source_provenance_hash"])
            check_type(argname="argument substitution_option", value=substitution_option, expected_type=type_hints["substitution_option"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument worker_pool", value=worker_pool, expected_type=type_hints["worker_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if dynamic_substitutions is not None:
            self._values["dynamic_substitutions"] = dynamic_substitutions
        if env is not None:
            self._values["env"] = env
        if logging is not None:
            self._values["logging"] = logging
        if log_streaming_option is not None:
            self._values["log_streaming_option"] = log_streaming_option
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if requested_verify_option is not None:
            self._values["requested_verify_option"] = requested_verify_option
        if secret_env is not None:
            self._values["secret_env"] = secret_env
        if source_provenance_hash is not None:
            self._values["source_provenance_hash"] = source_provenance_hash
        if substitution_option is not None:
            self._values["substitution_option"] = substitution_option
        if volumes is not None:
            self._values["volumes"] = volumes
        if worker_pool is not None:
            self._values["worker_pool"] = worker_pool

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Requested disk size for the VM that runs the build.

        Note that this is NOT "disk free";
        some of the space will be used by the operating system and build utilities.
        Also note that this is the minimum disk size that will be allocated for the build --
        the build may run with a larger disk than requested. At present, the maximum disk size
        is 1000GB; builds that request more than the maximum are rejected with an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#disk_size_gb CloudbuildTrigger#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dynamic_substitutions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to specify whether or not to apply bash style string operations to the substitutions.

        NOTE this is always enabled for triggered builds and cannot be overridden in the build configuration file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dynamic_substitutions CloudbuildTrigger#dynamic_substitutions}
        '''
        result = self._values.get("dynamic_substitutions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of global environment variable definitions that will exist for all build steps in this build.

        If a variable is defined in both globally and in a build step,
        the variable will use the build step value.

        The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.str]:
        '''Option to specify the logging mode, which determines if and where build logs are stored.

        Possible values: ["LOGGING_UNSPECIFIED", "LEGACY", "GCS_ONLY", "STACKDRIVER_ONLY", "CLOUD_LOGGING_ONLY", "NONE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#logging CloudbuildTrigger#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_streaming_option(self) -> typing.Optional[builtins.str]:
        '''Option to define build log streaming behavior to Google Cloud Storage. Possible values: ["STREAM_DEFAULT", "STREAM_ON", "STREAM_OFF"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#log_streaming_option CloudbuildTrigger#log_streaming_option}
        '''
        result = self._values.get("log_streaming_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Compute Engine machine type on which to run the build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#machine_type CloudbuildTrigger#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requested_verify_option(self) -> typing.Optional[builtins.str]:
        '''Requested verifiability options. Possible values: ["NOT_VERIFIED", "VERIFIED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#requested_verify_option CloudbuildTrigger#requested_verify_option}
        '''
        result = self._values.get("requested_verify_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of global environment variables, which are encrypted using a Cloud Key Management Service crypto key.

        These values must be specified in the build's Secret. These variables
        will be available to all build steps in this build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        '''
        result = self._values.get("secret_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_provenance_hash(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Requested hash for SourceProvenance. Possible values: ["NONE", "SHA256", "MD5"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source_provenance_hash CloudbuildTrigger#source_provenance_hash}
        '''
        result = self._values.get("source_provenance_hash")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def substitution_option(self) -> typing.Optional[builtins.str]:
        '''Option to specify behavior when there is an error in the substitution checks.

        NOTE this is always set to ALLOW_LOOSE for triggered builds and cannot be overridden
        in the build configuration file. Possible values: ["MUST_MATCH", "ALLOW_LOOSE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitution_option CloudbuildTrigger#substitution_option}
        '''
        result = self._values.get("substitution_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildOptionsVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#volumes CloudbuildTrigger#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildOptionsVolumes"]]], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Option to specify a WorkerPool for the build. Format projects/{project}/workerPools/{workerPool}.

        This field is experimental.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#worker_pool CloudbuildTrigger#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f90b16556f10b9f2cf6f7ee89034496c403002dd2743a0457bd9fbccf66e576)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildOptionsVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d98942d8b1f8067d00389ccb818209e8b9b1c1b62fdc6bb45b6feade4a54824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDynamicSubstitutions")
    def reset_dynamic_substitutions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicSubstitutions", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetLogStreamingOption")
    def reset_log_streaming_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamingOption", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetRequestedVerifyOption")
    def reset_requested_verify_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedVerifyOption", []))

    @jsii.member(jsii_name="resetSecretEnv")
    def reset_secret_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretEnv", []))

    @jsii.member(jsii_name="resetSourceProvenanceHash")
    def reset_source_provenance_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceProvenanceHash", []))

    @jsii.member(jsii_name="resetSubstitutionOption")
    def reset_substitution_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstitutionOption", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetWorkerPool")
    def reset_worker_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerPool", []))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "CloudbuildTriggerBuildOptionsVolumesList":
        return typing.cast("CloudbuildTriggerBuildOptionsVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicSubstitutionsInput")
    def dynamic_substitutions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicSubstitutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamingOptionInput")
    def log_streaming_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamingOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedVerifyOptionInput")
    def requested_verify_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestedVerifyOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvInput")
    def secret_env_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "secretEnvInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceProvenanceHashInput")
    def source_provenance_hash_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceProvenanceHashInput"))

    @builtins.property
    @jsii.member(jsii_name="substitutionOptionInput")
    def substitution_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "substitutionOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildOptionsVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildOptionsVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="workerPoolInput")
    def worker_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73435b4fa2eae7de494937870bbe1484942a3f2a69770a89663ff42bdb34b62b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicSubstitutions")
    def dynamic_substitutions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicSubstitutions"))

    @dynamic_substitutions.setter
    def dynamic_substitutions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc14aa292cae86d0cbe7b95bf5185a5c8de79b93ae27fdfceef668469d09702f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicSubstitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e971dffb3e864a0c72b1651391249c38942ece2d0953278acd8c34d33958aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logging"))

    @logging.setter
    def logging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a266c2185f10dd97dbe9c19e6aa4d3c74bc0aba25761179231324cb4bf758a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamingOption")
    def log_streaming_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamingOption"))

    @log_streaming_option.setter
    def log_streaming_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c3134c13d93a212999a7c88267a0fcf22d7c62c177db66747b5b17373caf960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamingOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade00fdc941efecd2eb53d4f4226656f913c9e2e553f796373f80b56114aa066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedVerifyOption")
    def requested_verify_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestedVerifyOption"))

    @requested_verify_option.setter
    def requested_verify_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca3d24a69ff389caa9280208c6fb1f865cad739098c41e1bfd057a60def485b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedVerifyOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretEnv")
    def secret_env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "secretEnv"))

    @secret_env.setter
    def secret_env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e91a65b23f4a3bd94f6864667a1575031663dbdf023245a853ea1de83d8a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceProvenanceHash")
    def source_provenance_hash(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceProvenanceHash"))

    @source_provenance_hash.setter
    def source_provenance_hash(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8e6def8f04ff5e0fb32dec373d438d235a37bcfd2f0090d9afdc79a77e04a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceProvenanceHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutionOption")
    def substitution_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "substitutionOption"))

    @substitution_option.setter
    def substitution_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d697d02a394ba7e6e8561182cbd68edf4f2a6ff4188607072dd884c9dddc1663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutionOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231e2066205378ffd2a5279c8aabac5fcb8c55b26e68fbff57a9320a61462485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuildOptions]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3010e16fea3d153a2eec3fd451aeb247e53e8851bad4dc5ac2906f2cdaa46bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildOptionsVolumes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class CloudbuildTriggerBuildOptionsVolumes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the volume to mount. Volume names must be unique per build step and must be valid names for Docker volumes. Each named volume must be used by at least two build steps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param path: Path at which to mount the volume. Paths must be absolute and cannot conflict with other volume paths on the same build step or with certain reserved volume paths. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccfcca6a9d9ed0dcc9bb39ecfc08badf143293ee989fd0bd947c37d9122e2fe)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the volume to mount.

        Volume names must be unique per build step and must be valid names for Docker volumes.
        Each named volume must be used by at least two build steps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path at which to mount the volume.

        Paths must be absolute and cannot conflict with other volume paths on the same
        build step or with certain reserved volume paths.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildOptionsVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildOptionsVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildOptionsVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b19758746cb8642eea00b8a9fbb1ff7d0140b785a68a764519d8c1f4b363ae47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildOptionsVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f2c21512890226342628911143e26936178f48c4fc73ab184b74834d6022cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildOptionsVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ff1b89d5ff5b13fd0ba6deb5340532135f6f52b59ecb0ba71bd359fc8be105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5081e79881371429fa77fd49733c1b85d4fd376bd89a8fed7506448a3913499b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65e2d261e219636ddb2505282e1953437d924ab7c7a74cddd21b45f06cfaa14d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildOptionsVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildOptionsVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildOptionsVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad0405ae15648127f7e3ac615375c947f2d290619b2ddec84ee88bab38639b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildOptionsVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildOptionsVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eadd6fa2882974f37c49d431049ee19944a4bbb10c8f305b950968aab8b8961)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b11562971c1b102bba9c93e6bc3f4ff7e14cc5d8ab5084a5351f546a239e562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b68b9079b084cced8eaf8b8a5fd820d562cdc4de04bb2177fd6a139486ef81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildOptionsVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildOptionsVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildOptionsVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa38e0f66b8cd5ce0f70dfd7b132247becccf2b97aa532c4ec1649813c97aa13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fd4bb3b9fb966928fa050ee6fefa379748a0ee0ec63631f6fbf6aeddf072aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArtifacts")
    def put_artifacts(
        self,
        *,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        maven_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        npm_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
        objects: typing.Optional[typing.Union[CloudbuildTriggerBuildArtifactsObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        python_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsPythonPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images will be pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#images CloudbuildTrigger#images}
        :param maven_artifacts: maven_artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#maven_artifacts CloudbuildTrigger#maven_artifacts}
        :param npm_packages: npm_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#npm_packages CloudbuildTrigger#npm_packages}
        :param objects: objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#objects CloudbuildTrigger#objects}
        :param python_packages: python_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#python_packages CloudbuildTrigger#python_packages}
        '''
        value = CloudbuildTriggerBuildArtifacts(
            images=images,
            maven_artifacts=maven_artifacts,
            npm_packages=npm_packages,
            objects=objects,
            python_packages=python_packages,
        )

        return typing.cast(None, jsii.invoke(self, "putArtifacts", [value]))

    @jsii.member(jsii_name="putAvailableSecrets")
    def put_available_secrets(
        self,
        *,
        secret_manager: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildAvailableSecretsSecretManager, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param secret_manager: secret_manager block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_manager CloudbuildTrigger#secret_manager}
        '''
        value = CloudbuildTriggerBuildAvailableSecrets(secret_manager=secret_manager)

        return typing.cast(None, jsii.invoke(self, "putAvailableSecrets", [value]))

    @jsii.member(jsii_name="putOptions")
    def put_options(
        self,
        *,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        dynamic_substitutions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging: typing.Optional[builtins.str] = None,
        log_streaming_option: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        requested_verify_option: typing.Optional[builtins.str] = None,
        secret_env: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_provenance_hash: typing.Optional[typing.Sequence[builtins.str]] = None,
        substitution_option: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildOptionsVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: Requested disk size for the VM that runs the build. Note that this is NOT "disk free"; some of the space will be used by the operating system and build utilities. Also note that this is the minimum disk size that will be allocated for the build -- the build may run with a larger disk than requested. At present, the maximum disk size is 1000GB; builds that request more than the maximum are rejected with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#disk_size_gb CloudbuildTrigger#disk_size_gb}
        :param dynamic_substitutions: Option to specify whether or not to apply bash style string operations to the substitutions. NOTE this is always enabled for triggered builds and cannot be overridden in the build configuration file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dynamic_substitutions CloudbuildTrigger#dynamic_substitutions}
        :param env: A list of global environment variable definitions that will exist for all build steps in this build. If a variable is defined in both globally and in a build step, the variable will use the build step value. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        :param logging: Option to specify the logging mode, which determines if and where build logs are stored. Possible values: ["LOGGING_UNSPECIFIED", "LEGACY", "GCS_ONLY", "STACKDRIVER_ONLY", "CLOUD_LOGGING_ONLY", "NONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#logging CloudbuildTrigger#logging}
        :param log_streaming_option: Option to define build log streaming behavior to Google Cloud Storage. Possible values: ["STREAM_DEFAULT", "STREAM_ON", "STREAM_OFF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#log_streaming_option CloudbuildTrigger#log_streaming_option}
        :param machine_type: Compute Engine machine type on which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#machine_type CloudbuildTrigger#machine_type}
        :param requested_verify_option: Requested verifiability options. Possible values: ["NOT_VERIFIED", "VERIFIED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#requested_verify_option CloudbuildTrigger#requested_verify_option}
        :param secret_env: A list of global environment variables, which are encrypted using a Cloud Key Management Service crypto key. These values must be specified in the build's Secret. These variables will be available to all build steps in this build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        :param source_provenance_hash: Requested hash for SourceProvenance. Possible values: ["NONE", "SHA256", "MD5"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source_provenance_hash CloudbuildTrigger#source_provenance_hash}
        :param substitution_option: Option to specify behavior when there is an error in the substitution checks. NOTE this is always set to ALLOW_LOOSE for triggered builds and cannot be overridden in the build configuration file. Possible values: ["MUST_MATCH", "ALLOW_LOOSE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitution_option CloudbuildTrigger#substitution_option}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#volumes CloudbuildTrigger#volumes}
        :param worker_pool: Option to specify a WorkerPool for the build. Format projects/{project}/workerPools/{workerPool}. This field is experimental. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#worker_pool CloudbuildTrigger#worker_pool}
        '''
        value = CloudbuildTriggerBuildOptions(
            disk_size_gb=disk_size_gb,
            dynamic_substitutions=dynamic_substitutions,
            env=env,
            logging=logging,
            log_streaming_option=log_streaming_option,
            machine_type=machine_type,
            requested_verify_option=requested_verify_option,
            secret_env=secret_env,
            source_provenance_hash=source_provenance_hash,
            substitution_option=substitution_option,
            volumes=volumes,
            worker_pool=worker_pool,
        )

        return typing.cast(None, jsii.invoke(self, "putOptions", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildSecret", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe49d69baed25889f095629eb90cb6a9c9b9c9777fd58a91873f4f8c42c7c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        repo_source: typing.Optional[typing.Union["CloudbuildTriggerBuildSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["CloudbuildTriggerBuildSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_source CloudbuildTrigger#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#storage_source CloudbuildTrigger#storage_source}
        '''
        value = CloudbuildTriggerBuildSource(
            repo_source=repo_source, storage_source=storage_source
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putStep")
    def put_step(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildStep", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c44d6cb7541ce631ec3ebac8d83683ea88ffffa4b39f502a8f1d9620b85f3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStep", [value]))

    @jsii.member(jsii_name="resetArtifacts")
    def reset_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifacts", []))

    @jsii.member(jsii_name="resetAvailableSecrets")
    def reset_available_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableSecrets", []))

    @jsii.member(jsii_name="resetImages")
    def reset_images(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImages", []))

    @jsii.member(jsii_name="resetLogsBucket")
    def reset_logs_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogsBucket", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetQueueTtl")
    def reset_queue_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueTtl", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetSubstitutions")
    def reset_substitutions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstitutions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> CloudbuildTriggerBuildArtifactsOutputReference:
        return typing.cast(CloudbuildTriggerBuildArtifactsOutputReference, jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="availableSecrets")
    def available_secrets(
        self,
    ) -> CloudbuildTriggerBuildAvailableSecretsOutputReference:
        return typing.cast(CloudbuildTriggerBuildAvailableSecretsOutputReference, jsii.get(self, "availableSecrets"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> CloudbuildTriggerBuildOptionsOutputReference:
        return typing.cast(CloudbuildTriggerBuildOptionsOutputReference, jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "CloudbuildTriggerBuildSecretList":
        return typing.cast("CloudbuildTriggerBuildSecretList", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "CloudbuildTriggerBuildSourceOutputReference":
        return typing.cast("CloudbuildTriggerBuildSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="step")
    def step(self) -> "CloudbuildTriggerBuildStepList":
        return typing.cast("CloudbuildTriggerBuildStepList", jsii.get(self, "step"))

    @builtins.property
    @jsii.member(jsii_name="artifactsInput")
    def artifacts_input(self) -> typing.Optional[CloudbuildTriggerBuildArtifacts]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildArtifacts], jsii.get(self, "artifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="availableSecretsInput")
    def available_secrets_input(
        self,
    ) -> typing.Optional[CloudbuildTriggerBuildAvailableSecrets]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildAvailableSecrets], jsii.get(self, "availableSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="imagesInput")
    def images_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "imagesInput"))

    @builtins.property
    @jsii.member(jsii_name="logsBucketInput")
    def logs_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logsBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(self) -> typing.Optional[CloudbuildTriggerBuildOptions]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildOptions], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueTtlInput")
    def queue_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildSecret"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildSecret"]]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["CloudbuildTriggerBuildSource"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBuildSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="stepInput")
    def step_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStep"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStep"]]], jsii.get(self, "stepInput"))

    @builtins.property
    @jsii.member(jsii_name="substitutionsInput")
    def substitutions_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "substitutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "images"))

    @images.setter
    def images(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e89a1ea9c9a8b448e6c6023f2fbe136224345537e7d45d3476137699e391f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "images", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logsBucket")
    def logs_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logsBucket"))

    @logs_bucket.setter
    def logs_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be466adf02c4ce57f4ae97afe608163baa987752abaf7125ed9df5132542fd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logsBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueTtl")
    def queue_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueTtl"))

    @queue_ttl.setter
    def queue_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236f9bd183801fa3d3f9faeadee4ca53d406749ae33fe1c492d6b8f360af4b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutions")
    def substitutions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitutions"))

    @substitutions.setter
    def substitutions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29525b6fb93fa377c4f20379a3dfb32d57d84c4341530d2a4c2c20da276a0602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ca778ce102c8203f83b0e715d26890ade68b8ff854e17bd0b736c06af170ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e1f1f0af887bbab571784a455796da66f1d22c315539a4a0f4cb7052693a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuild]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudbuildTriggerBuild]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c571dbb11ebaf2fe84b8f2a1947ef5d1c31bfd3db1fd4958edd2a8329115ae11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSecret",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "secret_env": "secretEnv"},
)
class CloudbuildTriggerBuildSecret:
    def __init__(
        self,
        *,
        kms_key_name: builtins.str,
        secret_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param kms_key_name: Cloud KMS key name to use to decrypt these envs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#kms_key_name CloudbuildTrigger#kms_key_name}
        :param secret_env: Map of environment variable name to its encrypted value. Secret environment variables must be unique across all of a build's secrets, and must be used by at least one build step. Values can be at most 64 KB in size. There can be at most 100 secret values across all of a build's secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72c8280adc0efeb3372003f683fb944ae6042602cd360d01eeaf9aa6ddd910d)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument secret_env", value=secret_env, expected_type=type_hints["secret_env"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }
        if secret_env is not None:
            self._values["secret_env"] = secret_env

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Cloud KMS key name to use to decrypt these envs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#kms_key_name CloudbuildTrigger#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of environment variable name to its encrypted value.

        Secret environment variables must be unique across all of a build's secrets,
        and must be used by at least one build step. Values can be at most 64 KB in size.
        There can be at most 100 secret values across all of a build's secrets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        '''
        result = self._values.get("secret_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildSecretList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSecretList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dfa73855ca8ad2d97319d993b43cf8db12e889587331544b1791fdfbbb7eda7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudbuildTriggerBuildSecretOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__452c21c95c2cddfc00c423dbb9c190b0010bfe1719056f612d32891a548941de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildSecretOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7893705d12efa677863ae0f68b7ebd4513452e70dda7d8155788fd56b36f2725)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0487f7d239ddefd77f359bc243f7ba6754452418e757fa48f4fb624d6c6d60dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78917190377b8fd3ee99429dec22596c015c9b8a2685a648b4af3517e9e7d82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildSecret]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildSecret]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildSecret]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2e56516516814045b9b4be9b929ae253001e5b32b9f76cde9a2405df9fbe10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c0f806cac754990912be482e7a7f41ec44be670decd2f752b4b60ef6f9ba092)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecretEnv")
    def reset_secret_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretEnv", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvInput")
    def secret_env_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "secretEnvInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2644e92e3b5df4a208b06ca2e8562928c2a361b5b8e69680e9746f5712eb3f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretEnv")
    def secret_env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "secretEnv"))

    @secret_env.setter
    def secret_env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e03b84a752a2f0ba5b47f92a544157e09b850aa2b34485df96f555872167b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134010ac601c78dd0bc616e7dec2dd2c9a1ab917dcfe89c7f7ffdc9874af041e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSource",
    jsii_struct_bases=[],
    name_mapping={"repo_source": "repoSource", "storage_source": "storageSource"},
)
class CloudbuildTriggerBuildSource:
    def __init__(
        self,
        *,
        repo_source: typing.Optional[typing.Union["CloudbuildTriggerBuildSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["CloudbuildTriggerBuildSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_source CloudbuildTrigger#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#storage_source CloudbuildTrigger#storage_source}
        '''
        if isinstance(repo_source, dict):
            repo_source = CloudbuildTriggerBuildSourceRepoSource(**repo_source)
        if isinstance(storage_source, dict):
            storage_source = CloudbuildTriggerBuildSourceStorageSource(**storage_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209bba23fb837e1d55590c1f8557b342a636ebd74af22e2605eda7cbc1ccb474)
            check_type(argname="argument repo_source", value=repo_source, expected_type=type_hints["repo_source"])
            check_type(argname="argument storage_source", value=storage_source, expected_type=type_hints["storage_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if repo_source is not None:
            self._values["repo_source"] = repo_source
        if storage_source is not None:
            self._values["storage_source"] = storage_source

    @builtins.property
    def repo_source(self) -> typing.Optional["CloudbuildTriggerBuildSourceRepoSource"]:
        '''repo_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_source CloudbuildTrigger#repo_source}
        '''
        result = self._values.get("repo_source")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildSourceRepoSource"], result)

    @builtins.property
    def storage_source(
        self,
    ) -> typing.Optional["CloudbuildTriggerBuildSourceStorageSource"]:
        '''storage_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#storage_source CloudbuildTrigger#storage_source}
        '''
        result = self._values.get("storage_source")
        return typing.cast(typing.Optional["CloudbuildTriggerBuildSourceStorageSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2b2a26a6dd335504c1d7d944e36156f0e11305e13c8bff65037dfe553961b99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepoSource")
    def put_repo_source(
        self,
        *,
        repo_name: builtins.str,
        branch_name: typing.Optional[builtins.str] = None,
        commit_sha: typing.Optional[builtins.str] = None,
        dir: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_id: typing.Optional[builtins.str] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_name CloudbuildTrigger#repo_name}
        :param branch_name: Regex matching branches to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch_name CloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one a of branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#commit_sha CloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_id CloudbuildTrigger#project_id}
        :param substitutions: Substitutions to use in a triggered build. Should only be used with triggers.run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        :param tag_name: Regex matching tags to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag_name CloudbuildTrigger#tag_name}
        '''
        value = CloudbuildTriggerBuildSourceRepoSource(
            repo_name=repo_name,
            branch_name=branch_name,
            commit_sha=commit_sha,
            dir=dir,
            invert_regex=invert_regex,
            project_id=project_id,
            substitutions=substitutions,
            tag_name=tag_name,
        )

        return typing.cast(None, jsii.invoke(self, "putRepoSource", [value]))

    @jsii.member(jsii_name="putStorageSource")
    def put_storage_source(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bucket CloudbuildTrigger#bucket}
        :param object: Google Cloud Storage object containing the source. This object must be a gzipped archive file (.tar.gz) containing source to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#object CloudbuildTrigger#object}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#generation CloudbuildTrigger#generation}
        '''
        value = CloudbuildTriggerBuildSourceStorageSource(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putStorageSource", [value]))

    @jsii.member(jsii_name="resetRepoSource")
    def reset_repo_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepoSource", []))

    @jsii.member(jsii_name="resetStorageSource")
    def reset_storage_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageSource", []))

    @builtins.property
    @jsii.member(jsii_name="repoSource")
    def repo_source(self) -> "CloudbuildTriggerBuildSourceRepoSourceOutputReference":
        return typing.cast("CloudbuildTriggerBuildSourceRepoSourceOutputReference", jsii.get(self, "repoSource"))

    @builtins.property
    @jsii.member(jsii_name="storageSource")
    def storage_source(
        self,
    ) -> "CloudbuildTriggerBuildSourceStorageSourceOutputReference":
        return typing.cast("CloudbuildTriggerBuildSourceStorageSourceOutputReference", jsii.get(self, "storageSource"))

    @builtins.property
    @jsii.member(jsii_name="repoSourceInput")
    def repo_source_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerBuildSourceRepoSource"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBuildSourceRepoSource"], jsii.get(self, "repoSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSourceInput")
    def storage_source_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerBuildSourceStorageSource"]:
        return typing.cast(typing.Optional["CloudbuildTriggerBuildSourceStorageSource"], jsii.get(self, "storageSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuildSource]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5bd008d8acce957c103b6d6b39b13f3cef5e0ca36691909c099c5dfe090a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSourceRepoSource",
    jsii_struct_bases=[],
    name_mapping={
        "repo_name": "repoName",
        "branch_name": "branchName",
        "commit_sha": "commitSha",
        "dir": "dir",
        "invert_regex": "invertRegex",
        "project_id": "projectId",
        "substitutions": "substitutions",
        "tag_name": "tagName",
    },
)
class CloudbuildTriggerBuildSourceRepoSource:
    def __init__(
        self,
        *,
        repo_name: builtins.str,
        branch_name: typing.Optional[builtins.str] = None,
        commit_sha: typing.Optional[builtins.str] = None,
        dir: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_id: typing.Optional[builtins.str] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_name CloudbuildTrigger#repo_name}
        :param branch_name: Regex matching branches to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch_name CloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one a of branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#commit_sha CloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_id CloudbuildTrigger#project_id}
        :param substitutions: Substitutions to use in a triggered build. Should only be used with triggers.run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        :param tag_name: Regex matching tags to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag_name CloudbuildTrigger#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e2e61a32d6f192cbee7746278848ace9fe64506b9ff98b9f5477ff3bf508b1)
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument commit_sha", value=commit_sha, expected_type=type_hints["commit_sha"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument substitutions", value=substitutions, expected_type=type_hints["substitutions"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repo_name": repo_name,
        }
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if commit_sha is not None:
            self._values["commit_sha"] = commit_sha
        if dir is not None:
            self._values["dir"] = dir
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex
        if project_id is not None:
            self._values["project_id"] = project_id
        if substitutions is not None:
            self._values["substitutions"] = substitutions
        if tag_name is not None:
            self._values["tag_name"] = tag_name

    @builtins.property
    def repo_name(self) -> builtins.str:
        '''Name of the Cloud Source Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_name CloudbuildTrigger#repo_name}
        '''
        result = self._values.get("repo_name")
        assert result is not None, "Required property 'repo_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''Regex matching branches to build.

        Exactly one a of branch name, tag, or commit SHA must be provided.
        The syntax of the regular expressions accepted is the syntax accepted by RE2 and
        described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch_name CloudbuildTrigger#branch_name}
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''Explicit commit SHA to build. Exactly one a of branch name, tag, or commit SHA must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#commit_sha CloudbuildTrigger#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Directory, relative to the source root, in which to run the build.

        This must be a relative path. If a step's dir is specified and is an absolute path,
        this value is ignored for that step's execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger a build if the revision regex does NOT match the revision regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_id CloudbuildTrigger#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def substitutions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Substitutions to use in a triggered build. Should only be used with triggers.run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        '''
        result = self._values.get("substitutions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Regex matching tags to build.

        Exactly one a of branch name, tag, or commit SHA must be provided.
        The syntax of the regular expressions accepted is the syntax accepted by RE2 and
        described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag_name CloudbuildTrigger#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildSourceRepoSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildSourceRepoSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSourceRepoSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c51c5fc28582b3248bb100d9203c2920f8fc6ac285f9010ec504c56001d7b7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranchName")
    def reset_branch_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchName", []))

    @jsii.member(jsii_name="resetCommitSha")
    def reset_commit_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitSha", []))

    @jsii.member(jsii_name="resetDir")
    def reset_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDir", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetSubstitutions")
    def reset_substitutions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstitutions", []))

    @jsii.member(jsii_name="resetTagName")
    def reset_tag_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagName", []))

    @builtins.property
    @jsii.member(jsii_name="branchNameInput")
    def branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commitShaInput")
    def commit_sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitShaInput"))

    @builtins.property
    @jsii.member(jsii_name="dirInput")
    def dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="repoNameInput")
    def repo_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoNameInput"))

    @builtins.property
    @jsii.member(jsii_name="substitutionsInput")
    def substitutions_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "substitutionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNameInput")
    def tag_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagNameInput"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd91dc7d0f8ec7b0174b6906aab93a614473c3c900e0270bae4a4318975b8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca8304595d57b1a7533d823c961cb719344ca12788eb456e301d08d8d61e9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb15e16e850762c8af8e431f2c178e9030c6b5782763eebbd70f692f3d61eafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9947a6d331b3109c0b90422a8e7185af60d06d5b4dfaa43b7a42c9e1b1651490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbda5a17a476d5875c2020e91ce8053f74ec03a316b9211ce33a9abcc6809aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cce332843f403c9ceab2ca1dec417db10d2bbbbadc48e4d804d55961afafc3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutions")
    def substitutions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitutions"))

    @substitutions.setter
    def substitutions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c44c7ad3329727d69bd9ca7b29e87a270be57aa42c65492cdd28beae32ed2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b117faba023b30c1bd4c85453d4fe8ae2bca944d445550fb71329e246de32f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerBuildSourceRepoSource]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildSourceRepoSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildSourceRepoSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef000a953d9bc1f2360cbb848a202b180b0168b0359dfd95e672e7e20b7e775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSourceStorageSource",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class CloudbuildTriggerBuildSourceStorageSource:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bucket CloudbuildTrigger#bucket}
        :param object: Google Cloud Storage object containing the source. This object must be a gzipped archive file (.tar.gz) containing source to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#object CloudbuildTrigger#object}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#generation CloudbuildTrigger#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb75dd2f826ec9b61f2dcc51fb10acd4e38d608712f6af6e62daf5de230cac7b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Google Cloud Storage bucket containing the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bucket CloudbuildTrigger#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Google Cloud Storage object containing the source. This object must be a gzipped archive file (.tar.gz) containing source to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#object CloudbuildTrigger#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#generation CloudbuildTrigger#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildSourceStorageSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildSourceStorageSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildSourceStorageSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15c2f09219d67ccc6c7911f4e8f594494f07758533ed06fcb88d470bd7b0951b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030eb673d384c49440f81c2557a07ddbb6883eee6c1d6e2be044e8d8eba12f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd30cd01d34b9ff369166188490f78f52c2b5d9a77e0657231381f31a102929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5244ea5465e3cc5930018ab1f9f65d4265c47ee7654d1f96ac827d2d31984a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerBuildSourceStorageSource]:
        return typing.cast(typing.Optional[CloudbuildTriggerBuildSourceStorageSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerBuildSourceStorageSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cb664c297704c4571dce0005cb5f20bf58634b4c9bcdc10ba85b1978546df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildStep",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_exit_codes": "allowExitCodes",
        "allow_failure": "allowFailure",
        "args": "args",
        "dir": "dir",
        "entrypoint": "entrypoint",
        "env": "env",
        "id": "id",
        "script": "script",
        "secret_env": "secretEnv",
        "timeout": "timeout",
        "timing": "timing",
        "volumes": "volumes",
        "wait_for": "waitFor",
    },
)
class CloudbuildTriggerBuildStep:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        allow_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        dir: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
        secret_env: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timing: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildStepVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the container image that will run this particular build step. If the image is available in the host's Docker daemon's cache, it will be run directly. If not, the host will attempt to pull the image first, using the builder service account's credentials if necessary. The Docker daemon's cache will already have the latest versions of all of the officially supported build steps (see https://github.com/GoogleCloudPlatform/cloud-builders for images and examples). The Docker daemon will also have cached many of the layers for some popular images, like "ubuntu", "debian", but they will be refreshed at the time you attempt to use them. If you built an image in a previous build step, it will be stored in the host's Docker daemon's cache and is available to use as the name for a later build step. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param allow_exit_codes: Allow this build step to fail without failing the entire build if and only if the exit code is one of the specified codes. If 'allowFailure' is also specified, this field will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#allow_exit_codes CloudbuildTrigger#allow_exit_codes}
        :param allow_failure: Allow this build step to fail without failing the entire build. If false, the entire build will fail if this step fails. Otherwise, the build will succeed, but this step will still have a failure status. Error information will be reported in the 'failureDetail' field. 'allowExitCodes' takes precedence over this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#allow_failure CloudbuildTrigger#allow_failure}
        :param args: A list of arguments that will be presented to the step when it is started. If the image used to run the step's container has an entrypoint, the args are used as arguments to that entrypoint. If the image does not define an entrypoint, the first element in args is used as the entrypoint, and the remainder will be used as arguments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#args CloudbuildTrigger#args}
        :param dir: Working directory to use when running this step's container. If this value is a relative path, it is relative to the build's working directory. If this value is absolute, it may be outside the build's working directory, in which case the contents of the path may not be persisted across build step executions, unless a 'volume' for that path is specified. If the build specifies a 'RepoSource' with 'dir' and a step with a 'dir', which specifies an absolute path, the 'RepoSource' 'dir' is ignored for the step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        :param entrypoint: Entrypoint to be used instead of the build step image's default entrypoint. If unset, the image's default entrypoint is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#entrypoint CloudbuildTrigger#entrypoint}
        :param env: A list of environment variable definitions to be used when running a step. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        :param id: Unique identifier for this build step, used in 'wait_for' to reference this build step as a dependency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#id CloudbuildTrigger#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param script: A shell script to be executed in the step. When script is provided, the user cannot specify the entrypoint or args. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#script CloudbuildTrigger#script}
        :param secret_env: A list of environment variables which are encrypted using a Cloud Key Management Service crypto key. These values must be specified in the build's 'Secret'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        :param timeout: Time limit for executing this build step. If not defined, the step has no time limit and will be allowed to continue to run until either it completes or the build itself times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeout CloudbuildTrigger#timeout}
        :param timing: Output only. Stores timing information for executing this build step. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timing CloudbuildTrigger#timing}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#volumes CloudbuildTrigger#volumes}
        :param wait_for: The ID(s) of the step(s) that this build step depends on. This build step will not start until all the build steps in 'wait_for' have completed successfully. If 'wait_for' is empty, this build step will start when all previous build steps in the 'Build.Steps' list have completed successfully. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#wait_for CloudbuildTrigger#wait_for}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1328f48eddeae1f91dab097d9431aa798faa37dfb88523d0f82866e3674941ec)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_exit_codes", value=allow_exit_codes, expected_type=type_hints["allow_exit_codes"])
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument secret_env", value=secret_env, expected_type=type_hints["secret_env"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timing", value=timing, expected_type=type_hints["timing"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument wait_for", value=wait_for, expected_type=type_hints["wait_for"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_exit_codes is not None:
            self._values["allow_exit_codes"] = allow_exit_codes
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if args is not None:
            self._values["args"] = args
        if dir is not None:
            self._values["dir"] = dir
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if script is not None:
            self._values["script"] = script
        if secret_env is not None:
            self._values["secret_env"] = secret_env
        if timeout is not None:
            self._values["timeout"] = timeout
        if timing is not None:
            self._values["timing"] = timing
        if volumes is not None:
            self._values["volumes"] = volumes
        if wait_for is not None:
            self._values["wait_for"] = wait_for

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the container image that will run this particular build step.

        If the image is available in the host's Docker daemon's cache, it will be
        run directly. If not, the host will attempt to pull the image first, using
        the builder service account's credentials if necessary.

        The Docker daemon's cache will already have the latest versions of all of
        the officially supported build steps (see https://github.com/GoogleCloudPlatform/cloud-builders
        for images and examples).
        The Docker daemon will also have cached many of the layers for some popular
        images, like "ubuntu", "debian", but they will be refreshed at the time
        you attempt to use them.

        If you built an image in a previous build step, it will be stored in the
        host's Docker daemon's cache and is available to use as the name for a
        later build step.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Allow this build step to fail without failing the entire build if and only if the exit code is one of the specified codes.

        If 'allowFailure' is also specified, this field will take precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#allow_exit_codes CloudbuildTrigger#allow_exit_codes}
        '''
        result = self._values.get("allow_exit_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def allow_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow this build step to fail without failing the entire build.

        If false, the entire build will fail if this step fails. Otherwise, the
        build will succeed, but this step will still have a failure status.
        Error information will be reported in the 'failureDetail' field.

        'allowExitCodes' takes precedence over this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#allow_failure CloudbuildTrigger#allow_failure}
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of arguments that will be presented to the step when it is started.

        If the image used to run the step's container has an entrypoint, the args
        are used as arguments to that entrypoint. If the image does not define an
        entrypoint, the first element in args is used as the entrypoint, and the
        remainder will be used as arguments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#args CloudbuildTrigger#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Working directory to use when running this step's container.

        If this value is a relative path, it is relative to the build's working
        directory. If this value is absolute, it may be outside the build's working
        directory, in which case the contents of the path may not be persisted
        across build step executions, unless a 'volume' for that path is specified.

        If the build specifies a 'RepoSource' with 'dir' and a step with a
        'dir',
        which specifies an absolute path, the 'RepoSource' 'dir' is ignored
        for the step's execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''Entrypoint to be used instead of the build step image's default entrypoint. If unset, the image's default entrypoint is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#entrypoint CloudbuildTrigger#entrypoint}
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of environment variable definitions to be used when running a step.

        The elements are of the form "KEY=VALUE" for the environment variable
        "KEY" being given the value "VALUE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#env CloudbuildTrigger#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for this build step, used in 'wait_for' to reference this build step as a dependency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#id CloudbuildTrigger#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''A shell script to be executed in the step.

        When script is provided, the user cannot specify the entrypoint or args.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#script CloudbuildTrigger#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of environment variables which are encrypted using a Cloud Key Management Service crypto key.

        These values must be specified in
        the build's 'Secret'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret_env CloudbuildTrigger#secret_env}
        '''
        result = self._values.get("secret_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Time limit for executing this build step.

        If not defined,
        the step has no
        time limit and will be allowed to continue to run until either it
        completes or the build itself times out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeout CloudbuildTrigger#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timing(self) -> typing.Optional[builtins.str]:
        '''Output only. Stores timing information for executing this build step.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timing CloudbuildTrigger#timing}
        '''
        result = self._values.get("timing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStepVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#volumes CloudbuildTrigger#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStepVolumes"]]], result)

    @builtins.property
    def wait_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID(s) of the step(s) that this build step depends on.

        This build step will not start until all the build steps in 'wait_for'
        have completed successfully. If 'wait_for' is empty, this build step
        will start when all previous build steps in the 'Build.Steps' list
        have completed successfully.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#wait_for CloudbuildTrigger#wait_for}
        '''
        result = self._values.get("wait_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildStepList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildStepList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7adb5ed400e04c33c9f89675e4877e01e2c8b8803bb90f7930975adde2ef976b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudbuildTriggerBuildStepOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4192bd00720e1f5ef65f10168d6131ca258583252ca905c66e6f6462fb7b132d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildStepOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae6fb708fadda048ead333e35974c12504a6bfabb555336f5bbeb616adff445)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b293a0a239fdf510ee6abaa9382566cbc29452da551506acab37cab50e0888)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80d5ff20072d6180ec4a3a49bc7b117afaa9cb5ad481f880c9fa4e7df30370d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStep]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStep]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStep]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fcedb422b7eeea06a54973fd0e5d884c10f6aee363111ef00cf5be3955dffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__724a5bb49966b10347812c1501d1d90c9f9ae7f3a7ebf8f9bed84fd4a0eafb99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildTriggerBuildStepVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56d1fb92d69e95d92c3eec423253daab33d29acb6e2b778da50005f42ac614d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="resetAllowExitCodes")
    def reset_allow_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowExitCodes", []))

    @jsii.member(jsii_name="resetAllowFailure")
    def reset_allow_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowFailure", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetDir")
    def reset_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDir", []))

    @jsii.member(jsii_name="resetEntrypoint")
    def reset_entrypoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntrypoint", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @jsii.member(jsii_name="resetSecretEnv")
    def reset_secret_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretEnv", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTiming")
    def reset_timing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTiming", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetWaitFor")
    def reset_wait_for(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitFor", []))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "CloudbuildTriggerBuildStepVolumesList":
        return typing.cast("CloudbuildTriggerBuildStepVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="allowExitCodesInput")
    def allow_exit_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowFailureInput")
    def allow_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="dirInput")
    def dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirInput"))

    @builtins.property
    @jsii.member(jsii_name="entrypointInput")
    def entrypoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entrypointInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvInput")
    def secret_env_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "secretEnvInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timingInput")
    def timing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timingInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStepVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildTriggerBuildStepVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForInput")
    def wait_for_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "waitForInput"))

    @builtins.property
    @jsii.member(jsii_name="allowExitCodes")
    def allow_exit_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowExitCodes"))

    @allow_exit_codes.setter
    def allow_exit_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba86489bef01e38e1797c13fc3efa661eec72fce869b6f97fa5e1f5a2237115e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowFailure")
    def allow_failure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowFailure"))

    @allow_failure.setter
    def allow_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32099ab206f3723f5bac9707a01de4061d25a93b9234bc1c8b1aaa1f4ee7f6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596f8afca763173083bf65043cdd3d66893ecc4310024962b84396565f46e833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd4a6db277aa7fae924d9e40d60efaf3c6c13e43d44bfe48f8d68c397ed688f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entrypoint"))

    @entrypoint.setter
    def entrypoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5a38e845cfcbb36b6fdde03300e51597b6e43516803b52b4a2857ef9b6a8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entrypoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33650829a4437dea5dfff356758162585c598e20f77bb367e2407adc75f8a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2867462ae3cbeb5ffd0b579a18930102bbb4587f69cce9560f71ccfe45d388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce1d574a778dcfaaff152d6904ddbfd2a52d29bf76487b3575470de4447ce53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f219e0433cdc1eb2310fe1dbda8b85f0c7de821ff0ec23b262f6bc2bc353c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretEnv")
    def secret_env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "secretEnv"))

    @secret_env.setter
    def secret_env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2fcfd545d5baf36578ad70268b48902477637f9984f3da0853c46f68bd9199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cceb1e0f719d97cd34f9db6df9caff97dfab99c1d8f1db6062a6775df55f35e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timing")
    def timing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timing"))

    @timing.setter
    def timing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248fa49cd04ac3de54817afd165297307e37930850cb9c97c63adfaa923f13c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitFor")
    def wait_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "waitFor"))

    @wait_for.setter
    def wait_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67062dbe91f67594b590872e4494d158975edf96994a389fee0fe4266db8d760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitFor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStep]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStep]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStep]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffa33efd7acd0fd96db240e87cabd26f8b807c0121e1aaa0e419bbb70c0b1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildStepVolumes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class CloudbuildTriggerBuildStepVolumes:
    def __init__(self, *, name: builtins.str, path: builtins.str) -> None:
        '''
        :param name: Name of the volume to mount. Volume names must be unique per build step and must be valid names for Docker volumes. Each named volume must be used by at least two build steps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param path: Path at which to mount the volume. Paths must be absolute and cannot conflict with other volume paths on the same build step or with certain reserved volume paths. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3cd059d89c13a70e004df203e4cb67585102aba2cae961b9c2c0bac87d04096)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the volume to mount.

        Volume names must be unique per build step and must be valid names for
        Docker volumes. Each named volume must be used by at least two build steps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Path at which to mount the volume.

        Paths must be absolute and cannot conflict with other volume paths on
        the same build step or with certain reserved volume paths.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerBuildStepVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerBuildStepVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildStepVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__924effedd68c580955b65321b7c05ed2af730e261eee0ebc54044fc57e911655)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildTriggerBuildStepVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f2eca506e981ce898c7973d5eeec75dd63f896f68df439bd416a3578a174d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildTriggerBuildStepVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b667331faeb6dfe84ba4e968fa0f581591a87d13371af74527fcf791eaac46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b92f14c88e9d55175ce5452f4f0a1c2a4e3880020ca8bb5b35124592df082c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a763cffebb2eaf36e0516e63f7e9d81028ccb3a2f8d277c6dcf1a34db5d01584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStepVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStepVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStepVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0192567d210a8ef2b2464c8e224daf0a79f4c05f914671aa914a01f5b3627b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildTriggerBuildStepVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerBuildStepVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa3c80bf805abaa3118bbee0380f6559361774b5716fb6f5aa7731a301aae49d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38087e8cfe3cff4e18da4d3e4c02971fdb7b6d5e496e575984e73acfa7631a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2a4048f0f901dcddab15a91a980c8dadc6b91c266625c973261b4e3361592a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStepVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStepVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStepVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f36830ccfc369732906f2c25400c7df5b1b3559eb27e53c80b672585d4a2901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "approval_config": "approvalConfig",
        "bitbucket_server_trigger_config": "bitbucketServerTriggerConfig",
        "build_attribute": "buildAttribute",
        "description": "description",
        "disabled": "disabled",
        "filename": "filename",
        "filter": "filter",
        "git_file_source": "gitFileSource",
        "github": "github",
        "id": "id",
        "ignored_files": "ignoredFiles",
        "include_build_logs": "includeBuildLogs",
        "included_files": "includedFiles",
        "location": "location",
        "name": "name",
        "project": "project",
        "pubsub_config": "pubsubConfig",
        "repository_event_config": "repositoryEventConfig",
        "service_account": "serviceAccount",
        "source_to_build": "sourceToBuild",
        "substitutions": "substitutions",
        "tags": "tags",
        "timeouts": "timeouts",
        "trigger_template": "triggerTemplate",
        "webhook_config": "webhookConfig",
    },
)
class CloudbuildTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        approval_config: typing.Optional[typing.Union[CloudbuildTriggerApprovalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_server_trigger_config: typing.Optional[typing.Union[CloudbuildTriggerBitbucketServerTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        build_attribute: typing.Optional[typing.Union[CloudbuildTriggerBuild, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        filter: typing.Optional[builtins.str] = None,
        git_file_source: typing.Optional[typing.Union["CloudbuildTriggerGitFileSource", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["CloudbuildTriggerGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_build_logs: typing.Optional[builtins.str] = None,
        included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pubsub_config: typing.Optional[typing.Union["CloudbuildTriggerPubsubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        repository_event_config: typing.Optional[typing.Union["CloudbuildTriggerRepositoryEventConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_to_build: typing.Optional[typing.Union["CloudbuildTriggerSourceToBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CloudbuildTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_template: typing.Optional[typing.Union["CloudbuildTriggerTriggerTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_config: typing.Optional[typing.Union["CloudbuildTriggerWebhookConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param approval_config: approval_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#approval_config CloudbuildTrigger#approval_config}
        :param bitbucket_server_trigger_config: bitbucket_server_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_trigger_config CloudbuildTrigger#bitbucket_server_trigger_config}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#build CloudbuildTrigger#build}
        :param description: Human-readable description of the trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#description CloudbuildTrigger#description}
        :param disabled: Whether the trigger is disabled or not. If true, the trigger will never result in a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#disabled CloudbuildTrigger#disabled}
        :param filename: Path, from the source root, to a file whose contents is used for the template. Either a filename or build template must be provided. Set this only when using trigger_template or github. When using Pub/Sub, Webhook or Manual set the file name using git_file_source instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#filename CloudbuildTrigger#filename}
        :param filter: A Common Expression Language string. Used only with Pub/Sub and Webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#filter CloudbuildTrigger#filter}
        :param git_file_source: git_file_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#git_file_source CloudbuildTrigger#git_file_source}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github CloudbuildTrigger#github}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#id CloudbuildTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignored_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If ignoredFiles and changed files are both empty, then they are not used to determine whether or not to trigger a build. If ignoredFiles is not empty, then we ignore any files that match any of the ignored_file globs. If the change has no files that are outside of the ignoredFiles globs, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#ignored_files CloudbuildTrigger#ignored_files}
        :param include_build_logs: Build logs will be sent back to GitHub as part of the checkrun result. Values can be INCLUDE_BUILD_LOGS_UNSPECIFIED or INCLUDE_BUILD_LOGS_WITH_STATUS Possible values: ["INCLUDE_BUILD_LOGS_UNSPECIFIED", "INCLUDE_BUILD_LOGS_WITH_STATUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#include_build_logs CloudbuildTrigger#include_build_logs}
        :param included_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is empty, then as far as this filter is concerned, we should trigger the build. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is not empty, then we make sure that at least one of those files matches a includedFiles glob. If not, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#included_files CloudbuildTrigger#included_files}
        :param location: The `Cloud Build location <https://cloud.google.com/build/docs/locations>`_ for the trigger. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#location CloudbuildTrigger#location}
        :param name: Name of the trigger. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project CloudbuildTrigger#project}.
        :param pubsub_config: pubsub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pubsub_config CloudbuildTrigger#pubsub_config}
        :param repository_event_config: repository_event_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository_event_config CloudbuildTrigger#repository_event_config}
        :param service_account: The service account used for all user-controlled operations including triggers.patch, triggers.run, builds.create, and builds.cancel. If no service account is set, then the standard Cloud Build service account ([PROJECT_NUM]@system.gserviceaccount.com) will be used instead. Format: projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_ID_OR_EMAIL} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#service_account CloudbuildTrigger#service_account}
        :param source_to_build: source_to_build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source_to_build CloudbuildTrigger#source_to_build}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a BuildTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tags CloudbuildTrigger#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeouts CloudbuildTrigger#timeouts}
        :param trigger_template: trigger_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#trigger_template CloudbuildTrigger#trigger_template}
        :param webhook_config: webhook_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#webhook_config CloudbuildTrigger#webhook_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(approval_config, dict):
            approval_config = CloudbuildTriggerApprovalConfig(**approval_config)
        if isinstance(bitbucket_server_trigger_config, dict):
            bitbucket_server_trigger_config = CloudbuildTriggerBitbucketServerTriggerConfig(**bitbucket_server_trigger_config)
        if isinstance(build_attribute, dict):
            build_attribute = CloudbuildTriggerBuild(**build_attribute)
        if isinstance(git_file_source, dict):
            git_file_source = CloudbuildTriggerGitFileSource(**git_file_source)
        if isinstance(github, dict):
            github = CloudbuildTriggerGithub(**github)
        if isinstance(pubsub_config, dict):
            pubsub_config = CloudbuildTriggerPubsubConfig(**pubsub_config)
        if isinstance(repository_event_config, dict):
            repository_event_config = CloudbuildTriggerRepositoryEventConfig(**repository_event_config)
        if isinstance(source_to_build, dict):
            source_to_build = CloudbuildTriggerSourceToBuild(**source_to_build)
        if isinstance(timeouts, dict):
            timeouts = CloudbuildTriggerTimeouts(**timeouts)
        if isinstance(trigger_template, dict):
            trigger_template = CloudbuildTriggerTriggerTemplate(**trigger_template)
        if isinstance(webhook_config, dict):
            webhook_config = CloudbuildTriggerWebhookConfig(**webhook_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438f5ec09a4f7e318450a40224b923ee729fc1adc18edabf3f543d513b944fb2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument approval_config", value=approval_config, expected_type=type_hints["approval_config"])
            check_type(argname="argument bitbucket_server_trigger_config", value=bitbucket_server_trigger_config, expected_type=type_hints["bitbucket_server_trigger_config"])
            check_type(argname="argument build_attribute", value=build_attribute, expected_type=type_hints["build_attribute"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument git_file_source", value=git_file_source, expected_type=type_hints["git_file_source"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignored_files", value=ignored_files, expected_type=type_hints["ignored_files"])
            check_type(argname="argument include_build_logs", value=include_build_logs, expected_type=type_hints["include_build_logs"])
            check_type(argname="argument included_files", value=included_files, expected_type=type_hints["included_files"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pubsub_config", value=pubsub_config, expected_type=type_hints["pubsub_config"])
            check_type(argname="argument repository_event_config", value=repository_event_config, expected_type=type_hints["repository_event_config"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument source_to_build", value=source_to_build, expected_type=type_hints["source_to_build"])
            check_type(argname="argument substitutions", value=substitutions, expected_type=type_hints["substitutions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trigger_template", value=trigger_template, expected_type=type_hints["trigger_template"])
            check_type(argname="argument webhook_config", value=webhook_config, expected_type=type_hints["webhook_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if approval_config is not None:
            self._values["approval_config"] = approval_config
        if bitbucket_server_trigger_config is not None:
            self._values["bitbucket_server_trigger_config"] = bitbucket_server_trigger_config
        if build_attribute is not None:
            self._values["build_attribute"] = build_attribute
        if description is not None:
            self._values["description"] = description
        if disabled is not None:
            self._values["disabled"] = disabled
        if filename is not None:
            self._values["filename"] = filename
        if filter is not None:
            self._values["filter"] = filter
        if git_file_source is not None:
            self._values["git_file_source"] = git_file_source
        if github is not None:
            self._values["github"] = github
        if id is not None:
            self._values["id"] = id
        if ignored_files is not None:
            self._values["ignored_files"] = ignored_files
        if include_build_logs is not None:
            self._values["include_build_logs"] = include_build_logs
        if included_files is not None:
            self._values["included_files"] = included_files
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if pubsub_config is not None:
            self._values["pubsub_config"] = pubsub_config
        if repository_event_config is not None:
            self._values["repository_event_config"] = repository_event_config
        if service_account is not None:
            self._values["service_account"] = service_account
        if source_to_build is not None:
            self._values["source_to_build"] = source_to_build
        if substitutions is not None:
            self._values["substitutions"] = substitutions
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trigger_template is not None:
            self._values["trigger_template"] = trigger_template
        if webhook_config is not None:
            self._values["webhook_config"] = webhook_config

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
    def approval_config(self) -> typing.Optional[CloudbuildTriggerApprovalConfig]:
        '''approval_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#approval_config CloudbuildTrigger#approval_config}
        '''
        result = self._values.get("approval_config")
        return typing.cast(typing.Optional[CloudbuildTriggerApprovalConfig], result)

    @builtins.property
    def bitbucket_server_trigger_config(
        self,
    ) -> typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfig]:
        '''bitbucket_server_trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_trigger_config CloudbuildTrigger#bitbucket_server_trigger_config}
        '''
        result = self._values.get("bitbucket_server_trigger_config")
        return typing.cast(typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfig], result)

    @builtins.property
    def build_attribute(self) -> typing.Optional[CloudbuildTriggerBuild]:
        '''build block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#build CloudbuildTrigger#build}
        '''
        result = self._values.get("build_attribute")
        return typing.cast(typing.Optional[CloudbuildTriggerBuild], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human-readable description of the trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#description CloudbuildTrigger#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the trigger is disabled or not. If true, the trigger will never result in a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#disabled CloudbuildTrigger#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Path, from the source root, to a file whose contents is used for the template.

        Either a filename or build template must be provided. Set this only when using trigger_template or github.
        When using Pub/Sub, Webhook or Manual set the file name using git_file_source instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#filename CloudbuildTrigger#filename}
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A Common Expression Language string. Used only with Pub/Sub and Webhook.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#filter CloudbuildTrigger#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_file_source(self) -> typing.Optional["CloudbuildTriggerGitFileSource"]:
        '''git_file_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#git_file_source CloudbuildTrigger#git_file_source}
        '''
        result = self._values.get("git_file_source")
        return typing.cast(typing.Optional["CloudbuildTriggerGitFileSource"], result)

    @builtins.property
    def github(self) -> typing.Optional["CloudbuildTriggerGithub"]:
        '''github block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github CloudbuildTrigger#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional["CloudbuildTriggerGithub"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#id CloudbuildTrigger#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignored_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'.

        If ignoredFiles and changed files are both empty, then they are not
        used to determine whether or not to trigger a build.

        If ignoredFiles is not empty, then we ignore any files that match any
        of the ignored_file globs. If the change has no files that are outside
        of the ignoredFiles globs, then we do not trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#ignored_files CloudbuildTrigger#ignored_files}
        '''
        result = self._values.get("ignored_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_build_logs(self) -> typing.Optional[builtins.str]:
        '''Build logs will be sent back to GitHub as part of the checkrun result.

        Values can be INCLUDE_BUILD_LOGS_UNSPECIFIED or
        INCLUDE_BUILD_LOGS_WITH_STATUS Possible values: ["INCLUDE_BUILD_LOGS_UNSPECIFIED", "INCLUDE_BUILD_LOGS_WITH_STATUS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#include_build_logs CloudbuildTrigger#include_build_logs}
        '''
        result = self._values.get("include_build_logs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'.

        If any of the files altered in the commit pass the ignoredFiles filter
        and includedFiles is empty, then as far as this filter is concerned, we
        should trigger the build.

        If any of the files altered in the commit pass the ignoredFiles filter
        and includedFiles is not empty, then we make sure that at least one of
        those files matches a includedFiles glob. If not, then we do not trigger
        a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#included_files CloudbuildTrigger#included_files}
        '''
        result = self._values.get("included_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The `Cloud Build location <https://cloud.google.com/build/docs/locations>`_ for the trigger. If not specified, "global" is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#location CloudbuildTrigger#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the trigger. Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project CloudbuildTrigger#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_config(self) -> typing.Optional["CloudbuildTriggerPubsubConfig"]:
        '''pubsub_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pubsub_config CloudbuildTrigger#pubsub_config}
        '''
        result = self._values.get("pubsub_config")
        return typing.cast(typing.Optional["CloudbuildTriggerPubsubConfig"], result)

    @builtins.property
    def repository_event_config(
        self,
    ) -> typing.Optional["CloudbuildTriggerRepositoryEventConfig"]:
        '''repository_event_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository_event_config CloudbuildTrigger#repository_event_config}
        '''
        result = self._values.get("repository_event_config")
        return typing.cast(typing.Optional["CloudbuildTriggerRepositoryEventConfig"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for all user-controlled operations including triggers.patch, triggers.run, builds.create, and builds.cancel.

        If no service account is set, then the standard Cloud Build service account
        ([PROJECT_NUM]@system.gserviceaccount.com) will be used instead.

        Format: projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_ID_OR_EMAIL}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#service_account CloudbuildTrigger#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_to_build(self) -> typing.Optional["CloudbuildTriggerSourceToBuild"]:
        '''source_to_build block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#source_to_build CloudbuildTrigger#source_to_build}
        '''
        result = self._values.get("source_to_build")
        return typing.cast(typing.Optional["CloudbuildTriggerSourceToBuild"], result)

    @builtins.property
    def substitutions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Substitutions data for Build resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#substitutions CloudbuildTrigger#substitutions}
        '''
        result = self._values.get("substitutions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags for annotation of a BuildTrigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tags CloudbuildTrigger#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudbuildTriggerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#timeouts CloudbuildTrigger#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudbuildTriggerTimeouts"], result)

    @builtins.property
    def trigger_template(self) -> typing.Optional["CloudbuildTriggerTriggerTemplate"]:
        '''trigger_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#trigger_template CloudbuildTrigger#trigger_template}
        '''
        result = self._values.get("trigger_template")
        return typing.cast(typing.Optional["CloudbuildTriggerTriggerTemplate"], result)

    @builtins.property
    def webhook_config(self) -> typing.Optional["CloudbuildTriggerWebhookConfig"]:
        '''webhook_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#webhook_config CloudbuildTrigger#webhook_config}
        '''
        result = self._values.get("webhook_config")
        return typing.cast(typing.Optional["CloudbuildTriggerWebhookConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGitFileSource",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "repo_type": "repoType",
        "bitbucket_server_config": "bitbucketServerConfig",
        "github_enterprise_config": "githubEnterpriseConfig",
        "repository": "repository",
        "revision": "revision",
        "uri": "uri",
    },
)
class CloudbuildTriggerGitFileSource:
    def __init__(
        self,
        *,
        path: builtins.str,
        repo_type: builtins.str,
        bitbucket_server_config: typing.Optional[builtins.str] = None,
        github_enterprise_config: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        revision: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The path of the file, with the repo root as the root of the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_type CloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config CloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github_enterprise_config CloudbuildTrigger#github_enterprise_config}
        :param repository: The fully qualified resource name of the Repo API repository. The fully qualified resource name of the Repo API repository. If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        :param revision: The branch, tag, arbitrary ref, or SHA version of the repo to use when resolving the filename (optional). This field respects the same syntax/resolution as described here: https://git-scm.com/docs/gitrevisions If unspecified, the revision from which the trigger invocation originated is assumed to be the revision from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#revision CloudbuildTrigger#revision}
        :param uri: The URI of the repo (optional). If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#uri CloudbuildTrigger#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e5f0aa8c545ec0d6329c7a393cb10ab92853a360e02cbbb65dc1dbcf77a51d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument repo_type", value=repo_type, expected_type=type_hints["repo_type"])
            check_type(argname="argument bitbucket_server_config", value=bitbucket_server_config, expected_type=type_hints["bitbucket_server_config"])
            check_type(argname="argument github_enterprise_config", value=github_enterprise_config, expected_type=type_hints["github_enterprise_config"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "repo_type": repo_type,
        }
        if bitbucket_server_config is not None:
            self._values["bitbucket_server_config"] = bitbucket_server_config
        if github_enterprise_config is not None:
            self._values["github_enterprise_config"] = github_enterprise_config
        if repository is not None:
            self._values["repository"] = repository
        if revision is not None:
            self._values["revision"] = revision
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def path(self) -> builtins.str:
        '''The path of the file, with the repo root as the root of the path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#path CloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_type(self) -> builtins.str:
        '''The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_type CloudbuildTrigger#repo_type}
        '''
        result = self._values.get("repo_type")
        assert result is not None, "Required property 'repo_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bitbucket_server_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config CloudbuildTrigger#bitbucket_server_config}
        '''
        result = self._values.get("bitbucket_server_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_enterprise_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github_enterprise_config CloudbuildTrigger#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The fully qualified resource name of the Repo API repository.

        The fully qualified resource name of the Repo API repository.
        If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''The branch, tag, arbitrary ref, or SHA version of the repo to use when resolving the filename (optional).

        This field respects the same syntax/resolution as described here: https://git-scm.com/docs/gitrevisions
        If unspecified, the revision from which the trigger invocation originated is assumed to be the revision from which to read the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#revision CloudbuildTrigger#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the repo (optional).

        If unspecified, the repo from which the trigger
        invocation originated is assumed to be the repo from which to read the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#uri CloudbuildTrigger#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerGitFileSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerGitFileSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGitFileSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7f72fe9efa37e227595f86833ca89329c655a8ff146e4f8bc136fbaf2679414)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBitbucketServerConfig")
    def reset_bitbucket_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitbucketServerConfig", []))

    @jsii.member(jsii_name="resetGithubEnterpriseConfig")
    def reset_github_enterprise_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubEnterpriseConfig", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @jsii.member(jsii_name="resetRevision")
    def reset_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevision", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerConfigInput")
    def bitbucket_server_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitbucketServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfigInput")
    def github_enterprise_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="repoTypeInput")
    def repo_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerConfig")
    def bitbucket_server_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitbucketServerConfig"))

    @bitbucket_server_config.setter
    def bitbucket_server_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d98f7da8bbbe193ac349737d2103c9222b12212c5c7265d8ee85e38f19c035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitbucketServerConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubEnterpriseConfig"))

    @github_enterprise_config.setter
    def github_enterprise_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b0aaf598c43b5cf28f045ed89f8d52482edd6e0f856ecb644588735415a6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubEnterpriseConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6818af2dc1722ca3c0df439c1520663bcc3728c1ce2f4b246acba65d18447f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85601af3c06517e43250c7840277e136c6c30b965856fbd6e38ed587db3074e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoType")
    def repo_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoType"))

    @repo_type.setter
    def repo_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa827c9b31abd37c6ca68df2abc289388b409273e1a52a160d371d7c9afc73f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ff592349bba7bea0b3d44b4289c3f996e7bfce05de5a2ac3a8bfd155ea1bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a52eaa0b5cc13f4158dee281786a321d866e26d9c12e8853493a26e3bd11bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerGitFileSource]:
        return typing.cast(typing.Optional[CloudbuildTriggerGitFileSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerGitFileSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb45b99847ed5f74ef000df8eb45b0394a4529de3ca43c3cb9d0df9aa06564fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGithub",
    jsii_struct_bases=[],
    name_mapping={
        "enterprise_config_resource_name": "enterpriseConfigResourceName",
        "name": "name",
        "owner": "owner",
        "pull_request": "pullRequest",
        "push": "push",
    },
)
class CloudbuildTriggerGithub:
    def __init__(
        self,
        *,
        enterprise_config_resource_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        pull_request: typing.Optional[typing.Union["CloudbuildTriggerGithubPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["CloudbuildTriggerGithubPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enterprise_config_resource_name: The resource name of the github enterprise config that should be applied to this installation. For example: "projects/{$projectId}/locations/{$locationId}/githubEnterpriseConfigs/{$configId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#enterprise_config_resource_name CloudbuildTrigger#enterprise_config_resource_name}
        :param name: Name of the repository. For example: The name for https://github.com/googlecloudplatform/cloud-builders is "cloud-builders". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        :param owner: Owner of the repository. For example: The owner for https://github.com/googlecloudplatform/cloud-builders is "googlecloudplatform". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#owner CloudbuildTrigger#owner}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        if isinstance(pull_request, dict):
            pull_request = CloudbuildTriggerGithubPullRequest(**pull_request)
        if isinstance(push, dict):
            push = CloudbuildTriggerGithubPush(**push)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67715daadff33e93a7e587dd520e51c456e201b8783df04f41514e097834fc81)
            check_type(argname="argument enterprise_config_resource_name", value=enterprise_config_resource_name, expected_type=type_hints["enterprise_config_resource_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enterprise_config_resource_name is not None:
            self._values["enterprise_config_resource_name"] = enterprise_config_resource_name
        if name is not None:
            self._values["name"] = name
        if owner is not None:
            self._values["owner"] = owner
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if push is not None:
            self._values["push"] = push

    @builtins.property
    def enterprise_config_resource_name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the github enterprise config that should be applied to this installation. For example: "projects/{$projectId}/locations/{$locationId}/githubEnterpriseConfigs/{$configId}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#enterprise_config_resource_name CloudbuildTrigger#enterprise_config_resource_name}
        '''
        result = self._values.get("enterprise_config_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the repository. For example: The name for https://github.com/googlecloudplatform/cloud-builders is "cloud-builders".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#name CloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Owner of the repository. For example: The owner for https://github.com/googlecloudplatform/cloud-builders is "googlecloudplatform".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#owner CloudbuildTrigger#owner}
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request(self) -> typing.Optional["CloudbuildTriggerGithubPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["CloudbuildTriggerGithubPullRequest"], result)

    @builtins.property
    def push(self) -> typing.Optional["CloudbuildTriggerGithubPush"]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional["CloudbuildTriggerGithubPush"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce274279d4ad6d5ad4808c07a81e2e807abd102fda70c5c3c6bd9e9b2883121)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPullRequest")
    def put_pull_request(
        self,
        *,
        branch: builtins.str,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param comment_control: Whether to block builds on a "/gcbrun" comment from a repository owner or collaborator. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        value = CloudbuildTriggerGithubPullRequest(
            branch=branch, comment_control=comment_control, invert_regex=invert_regex
        )

        return typing.cast(None, jsii.invoke(self, "putPullRequest", [value]))

    @jsii.member(jsii_name="putPush")
    def put_push(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        value = CloudbuildTriggerGithubPush(
            branch=branch, invert_regex=invert_regex, tag=tag
        )

        return typing.cast(None, jsii.invoke(self, "putPush", [value]))

    @jsii.member(jsii_name="resetEnterpriseConfigResourceName")
    def reset_enterprise_config_resource_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseConfigResourceName", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetPullRequest")
    def reset_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequest", []))

    @jsii.member(jsii_name="resetPush")
    def reset_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPush", []))

    @builtins.property
    @jsii.member(jsii_name="pullRequest")
    def pull_request(self) -> "CloudbuildTriggerGithubPullRequestOutputReference":
        return typing.cast("CloudbuildTriggerGithubPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(self) -> "CloudbuildTriggerGithubPushOutputReference":
        return typing.cast("CloudbuildTriggerGithubPushOutputReference", jsii.get(self, "push"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseConfigResourceNameInput")
    def enterprise_config_resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseConfigResourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestInput")
    def pull_request_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerGithubPullRequest"]:
        return typing.cast(typing.Optional["CloudbuildTriggerGithubPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(self) -> typing.Optional["CloudbuildTriggerGithubPush"]:
        return typing.cast(typing.Optional["CloudbuildTriggerGithubPush"], jsii.get(self, "pushInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseConfigResourceName")
    def enterprise_config_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseConfigResourceName"))

    @enterprise_config_resource_name.setter
    def enterprise_config_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daadb2605afad70549bfc276aad9ef0baae83b6d43ae24563cfaf7dbd01ba1b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseConfigResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2232f45d32ce5580489a89919dc4e9023dbdeafde0b7d052358a5dd45615bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b62d84c656793fa4744e678716b91217df9be515f303e559ba8495c42dd124b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerGithub]:
        return typing.cast(typing.Optional[CloudbuildTriggerGithub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudbuildTriggerGithub]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e62bfa90078d54eb2afd680c99c18827bd0c5249dd17c1eb641df8f62f3749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGithubPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "comment_control": "commentControl",
        "invert_regex": "invertRegex",
    },
)
class CloudbuildTriggerGithubPullRequest:
    def __init__(
        self,
        *,
        branch: builtins.str,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param comment_control: Whether to block builds on a "/gcbrun" comment from a repository owner or collaborator. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc2c0c9505a30d34cf709f2bc50527c638ee08db2ed095c592cd40ad6bdc20e)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument comment_control", value=comment_control, expected_type=type_hints["comment_control"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
        }
        if comment_control is not None:
            self._values["comment_control"] = comment_control
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex

    @builtins.property
    def branch(self) -> builtins.str:
        '''Regex of branches to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment_control(self) -> typing.Optional[builtins.str]:
        '''Whether to block builds on a "/gcbrun" comment from a repository owner or collaborator. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        '''
        result = self._values.get("comment_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, branches that do NOT match the git_ref will trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerGithubPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerGithubPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGithubPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb673d4a927ff2205069cb37e467b2d0a6356ed6522c662aec683c0eff291c6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommentControl")
    def reset_comment_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommentControl", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="commentControlInput")
    def comment_control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentControlInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2fed4419f79df35d28b40e5427f5fe3e25804a0dee2e433d8b1ab0f3c2cc80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentControl")
    def comment_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commentControl"))

    @comment_control.setter
    def comment_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b015c7c2ac2546227de7887b4bda46dc0610c7170f0ffbae2d28bafe9acf6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477f49193b24f7ac5ee1f3d032e407c9c3031499dae68a0b7a00aa115104178b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerGithubPullRequest]:
        return typing.cast(typing.Optional[CloudbuildTriggerGithubPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerGithubPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c9d17bba8b1369ee1dc79d05381011e897e14c5ebd974d6287cc4c94c81248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGithubPush",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "invert_regex": "invertRegex", "tag": "tag"},
)
class CloudbuildTriggerGithubPush:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96098449450845ea95987866995251203d0fca81809e40a30df15e6cc66bac98)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Regex of branches to match.  Specify only one of branch or tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, only trigger a build if the revision regex does NOT match the git_ref regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Regex of tags to match.  Specify only one of branch or tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerGithubPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerGithubPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerGithubPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a0a5bd47375122be083af89170cc746407ef45e400e0b816a283dad9a09c039)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae1a3f01463abd9f065f79a78ec5c52ca509f5b60ce9e9f9615d23130741696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0407e25faf3dc75e30cc737a9e7fb977f2ea52dbcbefd8f7068b2a57ea79aeec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79a76ab6aaebfd5727e76cb713c6df9c950ad39552a05ec815932b27c5a54d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerGithubPush]:
        return typing.cast(typing.Optional[CloudbuildTriggerGithubPush], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerGithubPush],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa183950bd19c6f5c50e6b9ba06edfda712d09fa0a3fa4a625b783acbe4849c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerPubsubConfig",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "service_account_email": "serviceAccountEmail"},
)
class CloudbuildTriggerPubsubConfig:
    def __init__(
        self,
        *,
        topic: builtins.str,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the topic from which this subscription is receiving messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#topic CloudbuildTrigger#topic}
        :param service_account_email: Service account that will make the push request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#service_account_email CloudbuildTrigger#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1c5e24ecc9498d94fed62e0f918b7cad29fcfad5837af61a313ac7c6327e77)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email

    @builtins.property
    def topic(self) -> builtins.str:
        '''The name of the topic from which this subscription is receiving messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#topic CloudbuildTrigger#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''Service account that will make the push request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#service_account_email CloudbuildTrigger#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerPubsubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerPubsubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerPubsubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__685ad3b5b1294e962d448aec0500c34d25722487439d4b4a36a04dc437aef5e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="subscription")
    def subscription(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscription"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24914bb866cf6929a38f9d59994cc6e02d4a09ae3ecf7e73222ac6488cbf64e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366baad77451b538db5dcb57f48e717f5608e399987e289092d867ce9c2c87e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerPubsubConfig]:
        return typing.cast(typing.Optional[CloudbuildTriggerPubsubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerPubsubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68bd728b801412ac52a80ba1b68f5133615f255811a9f19161956a2929d1bc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerRepositoryEventConfig",
    jsii_struct_bases=[],
    name_mapping={
        "pull_request": "pullRequest",
        "push": "push",
        "repository": "repository",
    },
)
class CloudbuildTriggerRepositoryEventConfig:
    def __init__(
        self,
        *,
        pull_request: typing.Optional[typing.Union["CloudbuildTriggerRepositoryEventConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["CloudbuildTriggerRepositoryEventConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        :param repository: The resource name of the Repo API resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        if isinstance(pull_request, dict):
            pull_request = CloudbuildTriggerRepositoryEventConfigPullRequest(**pull_request)
        if isinstance(push, dict):
            push = CloudbuildTriggerRepositoryEventConfigPush(**push)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf328daf3e8539b9336fc1df83a498131d423d918095ebe18c73c6f2307f49d)
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if push is not None:
            self._values["push"] = push
        if repository is not None:
            self._values["repository"] = repository

    @builtins.property
    def pull_request(
        self,
    ) -> typing.Optional["CloudbuildTriggerRepositoryEventConfigPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#pull_request CloudbuildTrigger#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["CloudbuildTriggerRepositoryEventConfigPullRequest"], result)

    @builtins.property
    def push(self) -> typing.Optional["CloudbuildTriggerRepositoryEventConfigPush"]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#push CloudbuildTrigger#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional["CloudbuildTriggerRepositoryEventConfigPush"], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Repo API resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerRepositoryEventConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerRepositoryEventConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerRepositoryEventConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b90d18203e83a5a15e498cd5b79ace4240fbc9bee9e9a836469ff7703e919f4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPullRequest")
    def put_pull_request(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment '/gcbrun'. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        value = CloudbuildTriggerRepositoryEventConfigPullRequest(
            branch=branch, comment_control=comment_control, invert_regex=invert_regex
        )

        return typing.cast(None, jsii.invoke(self, "putPullRequest", [value]))

    @jsii.member(jsii_name="putPush")
    def put_push(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param invert_regex: If true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        value = CloudbuildTriggerRepositoryEventConfigPush(
            branch=branch, invert_regex=invert_regex, tag=tag
        )

        return typing.cast(None, jsii.invoke(self, "putPush", [value]))

    @jsii.member(jsii_name="resetPullRequest")
    def reset_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequest", []))

    @jsii.member(jsii_name="resetPush")
    def reset_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPush", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @builtins.property
    @jsii.member(jsii_name="pullRequest")
    def pull_request(
        self,
    ) -> "CloudbuildTriggerRepositoryEventConfigPullRequestOutputReference":
        return typing.cast("CloudbuildTriggerRepositoryEventConfigPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(self) -> "CloudbuildTriggerRepositoryEventConfigPushOutputReference":
        return typing.cast("CloudbuildTriggerRepositoryEventConfigPushOutputReference", jsii.get(self, "push"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestInput")
    def pull_request_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerRepositoryEventConfigPullRequest"]:
        return typing.cast(typing.Optional["CloudbuildTriggerRepositoryEventConfigPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(
        self,
    ) -> typing.Optional["CloudbuildTriggerRepositoryEventConfigPush"]:
        return typing.cast(typing.Optional["CloudbuildTriggerRepositoryEventConfigPush"], jsii.get(self, "pushInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e116e1234e544442a53e2f9eb4ebd886069d82e25a500e9a72cd04e8dad6e1e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerRepositoryEventConfig]:
        return typing.cast(typing.Optional[CloudbuildTriggerRepositoryEventConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerRepositoryEventConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c1dddef793b83dbb13269922dfe75e029b60979844bd4bbe5e78ec6140f2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerRepositoryEventConfigPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "comment_control": "commentControl",
        "invert_regex": "invertRegex",
    },
)
class CloudbuildTriggerRepositoryEventConfigPullRequest:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment '/gcbrun'. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268c1fb3b08bd992bfe98951cbbd9a9e214a9ca8f8e5074093423f70c50b74a6)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument comment_control", value=comment_control, expected_type=type_hints["comment_control"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if comment_control is not None:
            self._values["comment_control"] = comment_control
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Regex of branches to match.

        The syntax of the regular expressions accepted is the syntax accepted by
        RE2 and described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment_control(self) -> typing.Optional[builtins.str]:
        '''Configure builds to run whether a repository owner or collaborator need to comment '/gcbrun'. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#comment_control CloudbuildTrigger#comment_control}
        '''
        result = self._values.get("comment_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, branches that do NOT match the git_ref will trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerRepositoryEventConfigPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerRepositoryEventConfigPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerRepositoryEventConfigPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1448dd8d81eae947b59eabac5c0dcd7407b744a5b0658238721c1af90d5c5904)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetCommentControl")
    def reset_comment_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommentControl", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="commentControlInput")
    def comment_control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentControlInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a141ca4f8ccb66b3b09cbccca036556f5b24b102eaef4f3676fea872d89767c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentControl")
    def comment_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commentControl"))

    @comment_control.setter
    def comment_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e5d64cf090e4ce97641c81e5eb7f24b57139a0512b93e597bbce2e5ed887f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d65e489968112d7f33db0a0cbdcca37cfc9a416e8d530b0de6219625437d1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerRepositoryEventConfigPullRequest]:
        return typing.cast(typing.Optional[CloudbuildTriggerRepositoryEventConfigPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerRepositoryEventConfigPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441d296526d78640b461cf402dc88f8923e024c5c69b8987e8df22a37c03c91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerRepositoryEventConfigPush",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "invert_regex": "invertRegex", "tag": "tag"},
)
class CloudbuildTriggerRepositoryEventConfigPush:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        :param invert_regex: If true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ddefb982b7d126a096a40a662cd9c1511613113cabb5573bc18339e5544f63)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Regex of branches to match.

        The syntax of the regular expressions accepted is the syntax accepted by
        RE2 and described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch CloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, only trigger a build if the revision regex does NOT match the git_ref regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Regex of tags to match.

        The syntax of the regular expressions accepted is the syntax accepted by
        RE2 and described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag CloudbuildTrigger#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerRepositoryEventConfigPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerRepositoryEventConfigPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerRepositoryEventConfigPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab95019944ba110b704d2cc27d6b3916d993628d9a3cf87468c5c87c52021623)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6655af4abdb4d9b11c20aa81f821d879b63a1a7ac1f8fae6728f67d57dbc90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c6da31e971b10b30bbd59f6fecb8b8b94bcd9bd4da7c73dc0f25235881a1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2c84c08b2f6cee4dd144a8e7ce903127dea590bb22221eae25ec8366cd970b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildTriggerRepositoryEventConfigPush]:
        return typing.cast(typing.Optional[CloudbuildTriggerRepositoryEventConfigPush], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerRepositoryEventConfigPush],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578465e3ce6e6c038a78172ba48d08da0d01fa400fd610a1a7870a24e7d4b25e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerSourceToBuild",
    jsii_struct_bases=[],
    name_mapping={
        "ref": "ref",
        "repo_type": "repoType",
        "bitbucket_server_config": "bitbucketServerConfig",
        "github_enterprise_config": "githubEnterpriseConfig",
        "repository": "repository",
        "uri": "uri",
    },
)
class CloudbuildTriggerSourceToBuild:
    def __init__(
        self,
        *,
        ref: builtins.str,
        repo_type: builtins.str,
        bitbucket_server_config: typing.Optional[builtins.str] = None,
        github_enterprise_config: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ref: The branch or tag to use. Must start with "refs/" (required). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#ref CloudbuildTrigger#ref}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_type CloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config CloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github_enterprise_config CloudbuildTrigger#github_enterprise_config}
        :param repository: The qualified resource name of the Repo API repository. Either uri or repository can be specified and is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        :param uri: The URI of the repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#uri CloudbuildTrigger#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36af2a45ef400e63c5065c0871332fcb9964f910ddda837dc8a6379947b9bce4)
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument repo_type", value=repo_type, expected_type=type_hints["repo_type"])
            check_type(argname="argument bitbucket_server_config", value=bitbucket_server_config, expected_type=type_hints["bitbucket_server_config"])
            check_type(argname="argument github_enterprise_config", value=github_enterprise_config, expected_type=type_hints["github_enterprise_config"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ref": ref,
            "repo_type": repo_type,
        }
        if bitbucket_server_config is not None:
            self._values["bitbucket_server_config"] = bitbucket_server_config
        if github_enterprise_config is not None:
            self._values["github_enterprise_config"] = github_enterprise_config
        if repository is not None:
            self._values["repository"] = repository
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def ref(self) -> builtins.str:
        '''The branch or tag to use. Must start with "refs/" (required).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#ref CloudbuildTrigger#ref}
        '''
        result = self._values.get("ref")
        assert result is not None, "Required property 'ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_type(self) -> builtins.str:
        '''The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_type CloudbuildTrigger#repo_type}
        '''
        result = self._values.get("repo_type")
        assert result is not None, "Required property 'repo_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bitbucket_server_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#bitbucket_server_config CloudbuildTrigger#bitbucket_server_config}
        '''
        result = self._values.get("bitbucket_server_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_enterprise_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#github_enterprise_config CloudbuildTrigger#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The qualified resource name of the Repo API repository. Either uri or repository can be specified and is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repository CloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#uri CloudbuildTrigger#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerSourceToBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerSourceToBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerSourceToBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__120e9a71c3b7b22a834b4e251860b6c4c632bcaddc3ba0e9db7613da3f26e80a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBitbucketServerConfig")
    def reset_bitbucket_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitbucketServerConfig", []))

    @jsii.member(jsii_name="resetGithubEnterpriseConfig")
    def reset_github_enterprise_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubEnterpriseConfig", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerConfigInput")
    def bitbucket_server_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bitbucketServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfigInput")
    def github_enterprise_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="refInput")
    def ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="repoTypeInput")
    def repo_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerConfig")
    def bitbucket_server_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bitbucketServerConfig"))

    @bitbucket_server_config.setter
    def bitbucket_server_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c505eff19ce7086549625c219f1efce6ab8a170ec135d42445c7bb1e58c37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitbucketServerConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubEnterpriseConfig"))

    @github_enterprise_config.setter
    def github_enterprise_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f8f6b466dc0e99433ae8249018650cf764c1d89498ed45be967f122463112a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubEnterpriseConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabfe439a4f036fb87522446ec4403d322ff4bef732d9d8d1d9fa2d3b3c8f748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e76bbb612a47a8360e426114dfedfdda99841b2caccb0662a18c6c2567b3622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoType")
    def repo_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoType"))

    @repo_type.setter
    def repo_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acaae0178d1a7be22ee162ada7bb2acace2a8666b34aa611e2cc547c70623764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa4d4fca3474bd2002a204fe633cf54b4f6e349071826fe525494e47b8c0987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerSourceToBuild]:
        return typing.cast(typing.Optional[CloudbuildTriggerSourceToBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerSourceToBuild],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b31c30c76c29d58d540208502ceaa45a4958d6ad399baf7c6fcd17c31da067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudbuildTriggerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#create CloudbuildTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#delete CloudbuildTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#update CloudbuildTrigger#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7289dee5f472ab494107798a893a17426c47b390cc3bb4d9428a5574e3fa2283)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#create CloudbuildTrigger#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#delete CloudbuildTrigger#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#update CloudbuildTrigger#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8a40b5451499b5a7a60bde68195f68b8ed759775ebcb05b03c46539805f1338)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3ccc2b1d34a4637bb2ef382f0888fec0870f080f804d808ddd4901cfe9c57ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1140e71eb77fab0955c77890dc2a14bc2478cba849c1571b0def40ef2057418d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a687f4debf69dc4c2717111689041b56fff2dff650b50e11e05e786028a9554f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddd9a3b18efea93fa06e0dd98253043dd81b7d887896f686679aca63cc03a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerTriggerTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "branch_name": "branchName",
        "commit_sha": "commitSha",
        "dir": "dir",
        "invert_regex": "invertRegex",
        "project_id": "projectId",
        "repo_name": "repoName",
        "tag_name": "tagName",
    },
)
class CloudbuildTriggerTriggerTemplate:
    def __init__(
        self,
        *,
        branch_name: typing.Optional[builtins.str] = None,
        commit_sha: typing.Optional[builtins.str] = None,
        dir: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_id: typing.Optional[builtins.str] = None,
        repo_name: typing.Optional[builtins.str] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch_name: Name of the branch to build. Exactly one a of branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch_name CloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one of a branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#commit_sha CloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_id CloudbuildTrigger#project_id}
        :param repo_name: Name of the Cloud Source Repository. If omitted, the name "default" is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_name CloudbuildTrigger#repo_name}
        :param tag_name: Name of the tag to build. Exactly one of a branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag_name CloudbuildTrigger#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26001b4c6c39c9e1cce3157704b9d1f20a15992a96362144be044153304475f8)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument commit_sha", value=commit_sha, expected_type=type_hints["commit_sha"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if commit_sha is not None:
            self._values["commit_sha"] = commit_sha
        if dir is not None:
            self._values["dir"] = dir
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex
        if project_id is not None:
            self._values["project_id"] = project_id
        if repo_name is not None:
            self._values["repo_name"] = repo_name
        if tag_name is not None:
            self._values["tag_name"] = tag_name

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''Name of the branch to build.

        Exactly one a of branch name, tag, or commit SHA must be provided.
        This field is a regular expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#branch_name CloudbuildTrigger#branch_name}
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''Explicit commit SHA to build. Exactly one of a branch name, tag, or commit SHA must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#commit_sha CloudbuildTrigger#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Directory, relative to the source root, in which to run the build.

        This must be a relative path. If a step's dir is specified and
        is an absolute path, this value is ignored for that step's
        execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#dir CloudbuildTrigger#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger a build if the revision regex does NOT match the revision regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#invert_regex CloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#project_id CloudbuildTrigger#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Source Repository. If omitted, the name "default" is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#repo_name CloudbuildTrigger#repo_name}
        '''
        result = self._values.get("repo_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Name of the tag to build.

        Exactly one of a branch name, tag, or commit SHA must be provided.
        This field is a regular expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#tag_name CloudbuildTrigger#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerTriggerTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerTriggerTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerTriggerTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2b15680c8ea710989ee48fdaf459eccac3990bd79c1c000020b880de2a3c101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranchName")
    def reset_branch_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchName", []))

    @jsii.member(jsii_name="resetCommitSha")
    def reset_commit_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitSha", []))

    @jsii.member(jsii_name="resetDir")
    def reset_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDir", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRepoName")
    def reset_repo_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepoName", []))

    @jsii.member(jsii_name="resetTagName")
    def reset_tag_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagName", []))

    @builtins.property
    @jsii.member(jsii_name="branchNameInput")
    def branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commitShaInput")
    def commit_sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitShaInput"))

    @builtins.property
    @jsii.member(jsii_name="dirInput")
    def dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="repoNameInput")
    def repo_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNameInput")
    def tag_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagNameInput"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5408e03b709db1971296c7fd71a71793e7a72a2c7535d85dc7f49edecafca7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31454cee50aca497e3d84e0a4dc4328133862918b3626275cd1b1e4d1ba7e587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bf7446cda1b9abf25d85e64f560c80e408cf2e0546b640d7ddc4a9f4d24407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db76baf5ad154ef6127f027529cc09add2653def2b0a090061e8d668336d1bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c34980463e0312229ac31f342169232c397838b8d4b8af85d5139547b112d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726e552c8300c261f8b0191b98fd4ecd4bb21410bd499fbd8cebe2e0b11fc6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dd852d16ac875dcef1fe018fe42d1d9ab4f5dc2e184ebfc3cf3f95ee39b08f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerTriggerTemplate]:
        return typing.cast(typing.Optional[CloudbuildTriggerTriggerTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerTriggerTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77628e0d8239a58ef7f01ce07c3dca632d606f156dd99c82e3a403a008f6652f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerWebhookConfig",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class CloudbuildTriggerWebhookConfig:
    def __init__(self, *, secret: builtins.str) -> None:
        '''
        :param secret: Resource name for the secret required as a URL parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret CloudbuildTrigger#secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bafc34c9259c5564428314cf9aefc3fdc03c0033b0206ac6acaa64937d08045)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> builtins.str:
        '''Resource name for the secret required as a URL parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_trigger#secret CloudbuildTrigger#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildTriggerWebhookConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildTriggerWebhookConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildTrigger.CloudbuildTriggerWebhookConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c15f9be34fdc0ac6db53f4a0615099dc50c46553c5209ac7249736e8c7d5075)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfedda6ccd86d3c16f9e40b751ad594ac5277f7df7a4e780e87879a1e7460184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildTriggerWebhookConfig]:
        return typing.cast(typing.Optional[CloudbuildTriggerWebhookConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildTriggerWebhookConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced5d3f6ea29983501694415317d62f899986cd6b12bf607345bac560f14009b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudbuildTrigger",
    "CloudbuildTriggerApprovalConfig",
    "CloudbuildTriggerApprovalConfigOutputReference",
    "CloudbuildTriggerBitbucketServerTriggerConfig",
    "CloudbuildTriggerBitbucketServerTriggerConfigOutputReference",
    "CloudbuildTriggerBitbucketServerTriggerConfigPullRequest",
    "CloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference",
    "CloudbuildTriggerBitbucketServerTriggerConfigPush",
    "CloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference",
    "CloudbuildTriggerBuild",
    "CloudbuildTriggerBuildArtifacts",
    "CloudbuildTriggerBuildArtifactsMavenArtifacts",
    "CloudbuildTriggerBuildArtifactsMavenArtifactsList",
    "CloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference",
    "CloudbuildTriggerBuildArtifactsNpmPackages",
    "CloudbuildTriggerBuildArtifactsNpmPackagesList",
    "CloudbuildTriggerBuildArtifactsNpmPackagesOutputReference",
    "CloudbuildTriggerBuildArtifactsObjects",
    "CloudbuildTriggerBuildArtifactsObjectsOutputReference",
    "CloudbuildTriggerBuildArtifactsObjectsTiming",
    "CloudbuildTriggerBuildArtifactsObjectsTimingList",
    "CloudbuildTriggerBuildArtifactsObjectsTimingOutputReference",
    "CloudbuildTriggerBuildArtifactsOutputReference",
    "CloudbuildTriggerBuildArtifactsPythonPackages",
    "CloudbuildTriggerBuildArtifactsPythonPackagesList",
    "CloudbuildTriggerBuildArtifactsPythonPackagesOutputReference",
    "CloudbuildTriggerBuildAvailableSecrets",
    "CloudbuildTriggerBuildAvailableSecretsOutputReference",
    "CloudbuildTriggerBuildAvailableSecretsSecretManager",
    "CloudbuildTriggerBuildAvailableSecretsSecretManagerList",
    "CloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference",
    "CloudbuildTriggerBuildOptions",
    "CloudbuildTriggerBuildOptionsOutputReference",
    "CloudbuildTriggerBuildOptionsVolumes",
    "CloudbuildTriggerBuildOptionsVolumesList",
    "CloudbuildTriggerBuildOptionsVolumesOutputReference",
    "CloudbuildTriggerBuildOutputReference",
    "CloudbuildTriggerBuildSecret",
    "CloudbuildTriggerBuildSecretList",
    "CloudbuildTriggerBuildSecretOutputReference",
    "CloudbuildTriggerBuildSource",
    "CloudbuildTriggerBuildSourceOutputReference",
    "CloudbuildTriggerBuildSourceRepoSource",
    "CloudbuildTriggerBuildSourceRepoSourceOutputReference",
    "CloudbuildTriggerBuildSourceStorageSource",
    "CloudbuildTriggerBuildSourceStorageSourceOutputReference",
    "CloudbuildTriggerBuildStep",
    "CloudbuildTriggerBuildStepList",
    "CloudbuildTriggerBuildStepOutputReference",
    "CloudbuildTriggerBuildStepVolumes",
    "CloudbuildTriggerBuildStepVolumesList",
    "CloudbuildTriggerBuildStepVolumesOutputReference",
    "CloudbuildTriggerConfig",
    "CloudbuildTriggerGitFileSource",
    "CloudbuildTriggerGitFileSourceOutputReference",
    "CloudbuildTriggerGithub",
    "CloudbuildTriggerGithubOutputReference",
    "CloudbuildTriggerGithubPullRequest",
    "CloudbuildTriggerGithubPullRequestOutputReference",
    "CloudbuildTriggerGithubPush",
    "CloudbuildTriggerGithubPushOutputReference",
    "CloudbuildTriggerPubsubConfig",
    "CloudbuildTriggerPubsubConfigOutputReference",
    "CloudbuildTriggerRepositoryEventConfig",
    "CloudbuildTriggerRepositoryEventConfigOutputReference",
    "CloudbuildTriggerRepositoryEventConfigPullRequest",
    "CloudbuildTriggerRepositoryEventConfigPullRequestOutputReference",
    "CloudbuildTriggerRepositoryEventConfigPush",
    "CloudbuildTriggerRepositoryEventConfigPushOutputReference",
    "CloudbuildTriggerSourceToBuild",
    "CloudbuildTriggerSourceToBuildOutputReference",
    "CloudbuildTriggerTimeouts",
    "CloudbuildTriggerTimeoutsOutputReference",
    "CloudbuildTriggerTriggerTemplate",
    "CloudbuildTriggerTriggerTemplateOutputReference",
    "CloudbuildTriggerWebhookConfig",
    "CloudbuildTriggerWebhookConfigOutputReference",
]

publication.publish()

def _typecheckingstub__11d0fc7ab845b08d8ac8cc27beffa7a97fb1fc9be14f813bd9fac42e8bf39abb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    approval_config: typing.Optional[typing.Union[CloudbuildTriggerApprovalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_server_trigger_config: typing.Optional[typing.Union[CloudbuildTriggerBitbucketServerTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    build_attribute: typing.Optional[typing.Union[CloudbuildTriggerBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filename: typing.Optional[builtins.str] = None,
    filter: typing.Optional[builtins.str] = None,
    git_file_source: typing.Optional[typing.Union[CloudbuildTriggerGitFileSource, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[CloudbuildTriggerGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_build_logs: typing.Optional[builtins.str] = None,
    included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pubsub_config: typing.Optional[typing.Union[CloudbuildTriggerPubsubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_event_config: typing.Optional[typing.Union[CloudbuildTriggerRepositoryEventConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    source_to_build: typing.Optional[typing.Union[CloudbuildTriggerSourceToBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CloudbuildTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_template: typing.Optional[typing.Union[CloudbuildTriggerTriggerTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_config: typing.Optional[typing.Union[CloudbuildTriggerWebhookConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3810ea2d04f6b88cda1cecf165c64d2b6892d21884b63d25e1e5cae1451fd5e8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaff1c6f5bbf9d67a6ed97c3dcb4b48bedaf0d2abc434e487c2de9120cd3ea8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f41d2ede926b7f8bc85da18071bc2494b0fc39b8d54d2d997f7c1239fdf799b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5a3b44164e142d47c17baa865b670ee186d30dace45b16fa82974c7db30ba6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be27be8662ee255dbc2564e6d31baae3db0b694464c1e4f91232b74e446a634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d732bb4c1ff5ec3f7a1e32b0df09678672d801b8866ef2e90d858880be116e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cc653b744fec770cfdede44370a9c6666a199a92ac3552cbdc4706890627b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15de7566268587465c4dbb72474a3fede438489702f12bdcea72c73a2904a6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928d8b13415c7b0463e3ccf76d51539cd2b510df417202539c93916d0b2f4664(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08000509c9038210b7c67096005c6c4459dac47d5f699205507f40044a025d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfaa1bc7258db05dd34f9c02549f240f6c6ff6cff5c8d02f4b3559faad0b8f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a883dd14345e7dc81921feef0e5dcf24b415995f0fbb05beaf416c675279af0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a229bbc14e61a0d7f0a3b0a79f8618dce6e64164e1381fddb983e40455ef335e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53916dbfd55bae4d459d62ebc515a4156197b3bd4407a60fbe448f79377f3503(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd3b7a555eecda4d4515bdb069df10f609f568b521fa2934d10d58c5840c56f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3de77cdb1e8fc27cf964d9a3d6dfa80906445748fa9580baa5fdcc1eae621db(
    *,
    approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04110b611627cfe8a9ee234736d82bc24a8e5475124e910aa2205d96110bc498(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af91fdde7161c07912fc27572d4c4e835b7807b1d710702d18eb9c837ec05f01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555e081f68cb55d9a30174f1c74fd3d4c8224b86986197a423512d17e0523eff(
    value: typing.Optional[CloudbuildTriggerApprovalConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d74d67d5094e75eaa8d5de697d6f6127aa2556f28117a54f1ab61d5974cbc40(
    *,
    bitbucket_server_config_resource: builtins.str,
    project_key: builtins.str,
    repo_slug: builtins.str,
    pull_request: typing.Optional[typing.Union[CloudbuildTriggerBitbucketServerTriggerConfigPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[CloudbuildTriggerBitbucketServerTriggerConfigPush, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09debc590369e1cb77f26e69b6e0c7dfd74392c96a0495463914e24e26c7b2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fb8ca44a63d0f6d36615cd634ea9d1528e818f8bada2ee73913ff91d5277c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc0d707f98dc7d9554f8ed31177294928b693bb02f3baf97091828e8d6e0965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7816e52d2ee311f55d5ededfa9d004a5e4d7a212415432c350147e1aa174fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774a9f5db01134ade503f810008a88409a1d6920fc06339b7840a4e7920aa941(
    value: typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfbe5c47fca65fb28975f6bacef041b0be64b3f8424e75be554ad0e9685fa07(
    *,
    branch: builtins.str,
    comment_control: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19059f58712f1c524c832f550c926169bafff220df14c739e977dced58d2735a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b106bbb738563442422734f13351e9f5d3b5946c0f4d9a25d1c3ee498ba2599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddd79b2a296589b0427adea853dc51ea0ebad1efe0f3a7070149ff85e1250b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a0fb0f8f82b2a3f9e058e347058a912b56e42900a2b28feae4425405dadc28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e7396eb7365e9e556fd5b9b2d81a1eba4b69d4a81b0bb1055cb7b2b5ce2786(
    value: typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee112fd6a2a3e4713b80dc25f9798c6dd325ee616cb4d57fb797a7838a235193(
    *,
    branch: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385993c252e7edbdb2db708f60cd35c753d3f9290ed112410fc63c39cd24d517(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e90e2c80cac1450b6dab4ed9d82f54e3ea9f71f7980d90013441236f71320f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d394815551349644343e242e57637644512940edcd184aa4c8f4a2b18662aa92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6d1939bf57e5c8ae46b5554a56f816d1f6495ed46268888e43eeeb2908cc9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b6d21bfaefc44d3e1aa5afe7768918cd83eeefb90fcbc2a016023159f8b823(
    value: typing.Optional[CloudbuildTriggerBitbucketServerTriggerConfigPush],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0254e3eff0c4eb03082410acf57109ba975934519d630a276f633e4401a597bb(
    *,
    step: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildStep, typing.Dict[builtins.str, typing.Any]]]],
    artifacts: typing.Optional[typing.Union[CloudbuildTriggerBuildArtifacts, typing.Dict[builtins.str, typing.Any]]] = None,
    available_secrets: typing.Optional[typing.Union[CloudbuildTriggerBuildAvailableSecrets, typing.Dict[builtins.str, typing.Any]]] = None,
    images: typing.Optional[typing.Sequence[builtins.str]] = None,
    logs_bucket: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[CloudbuildTriggerBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    queue_ttl: typing.Optional[builtins.str] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source: typing.Optional[typing.Union[CloudbuildTriggerBuildSource, typing.Dict[builtins.str, typing.Any]]] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b540c13286c7a330ca51201ca60dd1bb1673f6dbf5437d4338308cec9d8b83(
    *,
    images: typing.Optional[typing.Sequence[builtins.str]] = None,
    maven_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    npm_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    objects: typing.Optional[typing.Union[CloudbuildTriggerBuildArtifactsObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    python_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsPythonPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b03984ffdae9a1f8a9ad00af72ec547db607818e298946682eff53835285b0(
    *,
    artifact_id: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e4ee23c5d0076d90a4b31225dc25b86e8c4b34f11e606bcae1f2bd0a3aa63c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be7b096ce27bb292d34c0eb70753250278354f68eaf0b0190088ee1b7babcd8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc73282e32fc59c37a3296e5664c13e052cf29fd7936c1cc79de08001ba8c28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db03298f782cec272e724a44653260cff5e81b54c11665925afb94d399fa333(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c30acea698c59b175113818f902186559cd0feb560938000fc2ebaa77651fc9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0052065116ed5af987e84221d3cb6e517f873a00ec18c9d225f261e6eadcb62c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsMavenArtifacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d0b3e3f878a90313070dc69d8e8ba42d5d42e9cab7f93c227431284c9942a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e170477b1413ac0c496c8e2849e133e32d352d9323bc45e09508138fb3b2590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e8afd63dc0d25a3dcfccbfa349d278c3eabee6f510dd480bb47933ae9ad4ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf78fca30cfe845872f93c9f5fed7d3a927331dc29b462bcf870d3dd3cb3890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fddb92874da4467b6c1f377218f402f48f37fb870b04aee136ccddf2a91a86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c46cdee66619f59b20fd05202c3fa97a4d849973424db93656ea3a5aaefaeb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ccc141017a901de53c395756e8ee8878f1c15a0abdb0821729316518b7b76c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsMavenArtifacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385a85f99baec2d5b42381550f6c1dec820a36489f1cbb4950f3486689241a4c(
    *,
    package_path: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436f25c2ce997db76dd329ae9b6bda9cd8fcf3d233f3293651d83e9b4e870e9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c2b3f85e2a65899bb2a60c630c8d39f936c6f4bc44acca07b4e9d823b9bae3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef78d37d2f1dfcbee4e92032f3633172459399ff0f091e5fb1aec5c6732b3874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93cbdc34728b9fb505be8e5c0b99895cb49254f28cc89027bfd67ecee283273(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c732a8c5f7a4d8d915817b621df200c445bd6af341b8875d4e7dbbebda05777(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed98b25d278196f59a13f2305b8ceb0307af8485c79a800c2bde1bbc62697881(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsNpmPackages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3de44c6655a23a29bb81a03d8e06793d2f92e225d4e44c0818a64438a810db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc40f34033cf75467d70babf09f054f6bfcc06f0a01ba5e6a18a6f3547406aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bb4cc5b5bedc47556e87debfe6b1d1b346d0ee6eba5aceffd351f88e78d892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5db3de4b755d78ffea611ce35f7efdf7be78f68d7e1dcdab5b492ffb5eb9a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsNpmPackages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3a1f281add22166e681f678ce2c9e8ddebaaffb2e6578b95e891f989aae955(
    *,
    location: typing.Optional[builtins.str] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b0208164bd1cffbb2593dce11bd415e7e299bd64c0e82c67fb5c559b8df47f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0633d4c44c9ddf6ac3da1c7a29cd57b9e1ca527e335915e916a20a7a1c99ac6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec885b94486b764979236273dcc9c2c89b9eb7e4f0492aeccdb892f9a76e032(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f32dc56c76c8e2c9d4353e5190e61f14a6a727f5b533673b697e44700606157(
    value: typing.Optional[CloudbuildTriggerBuildArtifactsObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa376a43430cb123116e5fe81b3124b92601dc27d1e135ce68e98bb76c7a2b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5037667761618e9799b4dfdac200de78917f335a6cc675ecbde750afb606ab7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80e5bc22f2653c935c920dacb5d9db5ebe3b9fe6280c74f5cf4886e6de18372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1b91191d307ac154c591d29a423a22ed194810760b5e12832175cffc698fe3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811ba882bb20b02a94caf452d98b64b38f3399abdaf66969cd4af0950f239516(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7c526aef295deaebeba0fd3369ba8e855b4312fa68bf32864ad8a57008cd85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4dffcbd11e57a6f0f037713c7818a9996f34e5d97b8daca0eee79085cbc6b6(
    value: typing.Optional[CloudbuildTriggerBuildArtifactsObjectsTiming],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5917202b4b3a272ef3fcefcfbe7960261f426e17c882c751cda5a8bdccc7a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5cb013d85a217a128cba25afa149914681f441458ba0352aeb56cb17b11559(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6fafe611587e866f5644e7f753e21568b45def6882aa3a3cf95629cbe4c4ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fd14739e192a8655fdb7784e44e2e423af5239f5dfb97f88fe9aa72fbc9aed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildArtifactsPythonPackages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c346284bc4a0e9ed389ba0e2346095a4f1723c53f3899894a76920468646600a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93014f3a602c207c298ffca9385517c42c509646647fa5e6311508de5884ee9(
    value: typing.Optional[CloudbuildTriggerBuildArtifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fcb46752b42388b13f587af96cfe72f38621e926402658caaa4ac17c95a389(
    *,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bfe29217d497e93f2561efaa9e8d57cbe1d27a2fc718192985c32fd774f997(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba5335dc228591443b01e7d99cb5536093bd5da7a27525f9fc4743b216042ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603e62ea66288a2f861c20919fb4809ff9dc8b804a00d4a480ff484dc9c25c61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382c22a938c51e56d89626e5158b03f79af653d6a980375db786e1d74e7afa52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebccb337961323e1896b32e434cf93d429492cc0b0f0354969521d05e8f7a132(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16cfd72c3f08eef1ecb9e7a7686e618c80d2b85910a9a0448b1140b34b2e5a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildArtifactsPythonPackages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9639a2d685a2c80ca15b73f2e6a97974d7fe9a68d510ad79b53083806c13bf15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7221ebbe2641f3a1d04a3ebadc7a73790e9ae72493c0be48a30e4544ee162b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ace4a5167b0d1de7369fecb4399bdc3c2087b0437e097a2361b5994e937ea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdfc4b31d060c2752d33306527cd88f264319b072375c79d0f90b5ffd38b3ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildArtifactsPythonPackages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f888a277e9a41970509da9d63fa38b59ff6b88acedce818455c07585eee5d6(
    *,
    secret_manager: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildAvailableSecretsSecretManager, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c040f2b809fc0c6e6bae3445e06b8a4ddf36a79f65d62f68429f80f2d5ec42ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f550a1d50b0f30ee1d4b2c1b6c3e6198b5561f8a31590255ddd7242b14a2b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildAvailableSecretsSecretManager, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9272f035c266a8668f4e0a062f67bb690a0e24ebe2c0486f867daf85886a20d9(
    value: typing.Optional[CloudbuildTriggerBuildAvailableSecrets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0c00b71658784f02706e15ad876b6ffd36de0f9d0583def13b3549a150df34(
    *,
    env: builtins.str,
    version_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38766b751587c68e026b3edd8192d3836a43b7789f3f430cc4f01c1cacf70010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090ac6f523ec580c66b571e90562b21f0e5002580b407b8f1c414bab5d6cd5b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e319fa2045c2abc7e649131583e2b44c6e785005b947f50ec102f6feb48bfa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157d4c1e066d052f9a4b745cb8a15008a8729010451274a26397844103e1dec6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e136e74865445c2543e3332a82d70f577e7df459623d4d1e58a67c7b42f6f684(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225663e066a35987735209bbca1091d09a3bedb35579bc70da894b3740980beb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildAvailableSecretsSecretManager]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ff76b4e00e8fca5acf72b0a25c29a5a6e7d0c34ca6ff827bdd28f60b8a0b87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d841f93832d11cc5431d357236ea70368139662c76e251744ff0d9e55a3b928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fdb016249172d6ddd1c837d625cf5e0061d77ace75eec2cbdf292913fca398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80017f0d10621f28b8a0205fd77f87ef9dc4df8a65c7e28e18bd95e485c52810(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildAvailableSecretsSecretManager]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9999d74eba2b15df3130a30ba5107516e720a91c2ec69a23b55ae348bd823ab7(
    *,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    dynamic_substitutions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    env: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging: typing.Optional[builtins.str] = None,
    log_streaming_option: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    requested_verify_option: typing.Optional[builtins.str] = None,
    secret_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_provenance_hash: typing.Optional[typing.Sequence[builtins.str]] = None,
    substitution_option: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildOptionsVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f90b16556f10b9f2cf6f7ee89034496c403002dd2743a0457bd9fbccf66e576(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d98942d8b1f8067d00389ccb818209e8b9b1c1b62fdc6bb45b6feade4a54824(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildOptionsVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73435b4fa2eae7de494937870bbe1484942a3f2a69770a89663ff42bdb34b62b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc14aa292cae86d0cbe7b95bf5185a5c8de79b93ae27fdfceef668469d09702f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e971dffb3e864a0c72b1651391249c38942ece2d0953278acd8c34d33958aa7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a266c2185f10dd97dbe9c19e6aa4d3c74bc0aba25761179231324cb4bf758a79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3134c13d93a212999a7c88267a0fcf22d7c62c177db66747b5b17373caf960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade00fdc941efecd2eb53d4f4226656f913c9e2e553f796373f80b56114aa066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca3d24a69ff389caa9280208c6fb1f865cad739098c41e1bfd057a60def485b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e91a65b23f4a3bd94f6864667a1575031663dbdf023245a853ea1de83d8a65(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8e6def8f04ff5e0fb32dec373d438d235a37bcfd2f0090d9afdc79a77e04a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d697d02a394ba7e6e8561182cbd68edf4f2a6ff4188607072dd884c9dddc1663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231e2066205378ffd2a5279c8aabac5fcb8c55b26e68fbff57a9320a61462485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3010e16fea3d153a2eec3fd451aeb247e53e8851bad4dc5ac2906f2cdaa46bc2(
    value: typing.Optional[CloudbuildTriggerBuildOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccfcca6a9d9ed0dcc9bb39ecfc08badf143293ee989fd0bd947c37d9122e2fe(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19758746cb8642eea00b8a9fbb1ff7d0140b785a68a764519d8c1f4b363ae47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f2c21512890226342628911143e26936178f48c4fc73ab184b74834d6022cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ff1b89d5ff5b13fd0ba6deb5340532135f6f52b59ecb0ba71bd359fc8be105(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5081e79881371429fa77fd49733c1b85d4fd376bd89a8fed7506448a3913499b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e2d261e219636ddb2505282e1953437d924ab7c7a74cddd21b45f06cfaa14d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad0405ae15648127f7e3ac615375c947f2d290619b2ddec84ee88bab38639b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildOptionsVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eadd6fa2882974f37c49d431049ee19944a4bbb10c8f305b950968aab8b8961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b11562971c1b102bba9c93e6bc3f4ff7e14cc5d8ab5084a5351f546a239e562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b68b9079b084cced8eaf8b8a5fd820d562cdc4de04bb2177fd6a139486ef81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa38e0f66b8cd5ce0f70dfd7b132247becccf2b97aa532c4ec1649813c97aa13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildOptionsVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fd4bb3b9fb966928fa050ee6fefa379748a0ee0ec63631f6fbf6aeddf072aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe49d69baed25889f095629eb90cb6a9c9b9c9777fd58a91873f4f8c42c7c81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildSecret, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c44d6cb7541ce631ec3ebac8d83683ea88ffffa4b39f502a8f1d9620b85f3b6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildStep, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e89a1ea9c9a8b448e6c6023f2fbe136224345537e7d45d3476137699e391f29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be466adf02c4ce57f4ae97afe608163baa987752abaf7125ed9df5132542fd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236f9bd183801fa3d3f9faeadee4ca53d406749ae33fe1c492d6b8f360af4b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29525b6fb93fa377c4f20379a3dfb32d57d84c4341530d2a4c2c20da276a0602(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ca778ce102c8203f83b0e715d26890ade68b8ff854e17bd0b736c06af170ea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e1f1f0af887bbab571784a455796da66f1d22c315539a4a0f4cb7052693a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c571dbb11ebaf2fe84b8f2a1947ef5d1c31bfd3db1fd4958edd2a8329115ae11(
    value: typing.Optional[CloudbuildTriggerBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72c8280adc0efeb3372003f683fb944ae6042602cd360d01eeaf9aa6ddd910d(
    *,
    kms_key_name: builtins.str,
    secret_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dfa73855ca8ad2d97319d993b43cf8db12e889587331544b1791fdfbbb7eda7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452c21c95c2cddfc00c423dbb9c190b0010bfe1719056f612d32891a548941de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7893705d12efa677863ae0f68b7ebd4513452e70dda7d8155788fd56b36f2725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0487f7d239ddefd77f359bc243f7ba6754452418e757fa48f4fb624d6c6d60dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78917190377b8fd3ee99429dec22596c015c9b8a2685a648b4af3517e9e7d82e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2e56516516814045b9b4be9b929ae253001e5b32b9f76cde9a2405df9fbe10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildSecret]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0f806cac754990912be482e7a7f41ec44be670decd2f752b4b60ef6f9ba092(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2644e92e3b5df4a208b06ca2e8562928c2a361b5b8e69680e9746f5712eb3f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e03b84a752a2f0ba5b47f92a544157e09b850aa2b34485df96f555872167b7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134010ac601c78dd0bc616e7dec2dd2c9a1ab917dcfe89c7f7ffdc9874af041e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209bba23fb837e1d55590c1f8557b342a636ebd74af22e2605eda7cbc1ccb474(
    *,
    repo_source: typing.Optional[typing.Union[CloudbuildTriggerBuildSourceRepoSource, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_source: typing.Optional[typing.Union[CloudbuildTriggerBuildSourceStorageSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b2a26a6dd335504c1d7d944e36156f0e11305e13c8bff65037dfe553961b99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5bd008d8acce957c103b6d6b39b13f3cef5e0ca36691909c099c5dfe090a4a(
    value: typing.Optional[CloudbuildTriggerBuildSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e2e61a32d6f192cbee7746278848ace9fe64506b9ff98b9f5477ff3bf508b1(
    *,
    repo_name: builtins.str,
    branch_name: typing.Optional[builtins.str] = None,
    commit_sha: typing.Optional[builtins.str] = None,
    dir: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_id: typing.Optional[builtins.str] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tag_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c51c5fc28582b3248bb100d9203c2920f8fc6ac285f9010ec504c56001d7b7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd91dc7d0f8ec7b0174b6906aab93a614473c3c900e0270bae4a4318975b8fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca8304595d57b1a7533d823c961cb719344ca12788eb456e301d08d8d61e9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb15e16e850762c8af8e431f2c178e9030c6b5782763eebbd70f692f3d61eafa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9947a6d331b3109c0b90422a8e7185af60d06d5b4dfaa43b7a42c9e1b1651490(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbda5a17a476d5875c2020e91ce8053f74ec03a316b9211ce33a9abcc6809aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cce332843f403c9ceab2ca1dec417db10d2bbbbadc48e4d804d55961afafc3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c44c7ad3329727d69bd9ca7b29e87a270be57aa42c65492cdd28beae32ed2ab(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b117faba023b30c1bd4c85453d4fe8ae2bca944d445550fb71329e246de32f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef000a953d9bc1f2360cbb848a202b180b0168b0359dfd95e672e7e20b7e775(
    value: typing.Optional[CloudbuildTriggerBuildSourceRepoSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb75dd2f826ec9b61f2dcc51fb10acd4e38d608712f6af6e62daf5de230cac7b(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c2f09219d67ccc6c7911f4e8f594494f07758533ed06fcb88d470bd7b0951b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030eb673d384c49440f81c2557a07ddbb6883eee6c1d6e2be044e8d8eba12f86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd30cd01d34b9ff369166188490f78f52c2b5d9a77e0657231381f31a102929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5244ea5465e3cc5930018ab1f9f65d4265c47ee7654d1f96ac827d2d31984a80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cb664c297704c4571dce0005cb5f20bf58634b4c9bcdc10ba85b1978546df1(
    value: typing.Optional[CloudbuildTriggerBuildSourceStorageSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1328f48eddeae1f91dab097d9431aa798faa37dfb88523d0f82866e3674941ec(
    *,
    name: builtins.str,
    allow_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    allow_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    dir: typing.Optional[builtins.str] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
    secret_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timing: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildStepVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait_for: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adb5ed400e04c33c9f89675e4877e01e2c8b8803bb90f7930975adde2ef976b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4192bd00720e1f5ef65f10168d6131ca258583252ca905c66e6f6462fb7b132d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae6fb708fadda048ead333e35974c12504a6bfabb555336f5bbeb616adff445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b293a0a239fdf510ee6abaa9382566cbc29452da551506acab37cab50e0888(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80d5ff20072d6180ec4a3a49bc7b117afaa9cb5ad481f880c9fa4e7df30370d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fcedb422b7eeea06a54973fd0e5d884c10f6aee363111ef00cf5be3955dffd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStep]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724a5bb49966b10347812c1501d1d90c9f9ae7f3a7ebf8f9bed84fd4a0eafb99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56d1fb92d69e95d92c3eec423253daab33d29acb6e2b778da50005f42ac614d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildTriggerBuildStepVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba86489bef01e38e1797c13fc3efa661eec72fce869b6f97fa5e1f5a2237115e(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32099ab206f3723f5bac9707a01de4061d25a93b9234bc1c8b1aaa1f4ee7f6f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596f8afca763173083bf65043cdd3d66893ecc4310024962b84396565f46e833(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd4a6db277aa7fae924d9e40d60efaf3c6c13e43d44bfe48f8d68c397ed688f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5a38e845cfcbb36b6fdde03300e51597b6e43516803b52b4a2857ef9b6a8ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33650829a4437dea5dfff356758162585c598e20f77bb367e2407adc75f8a7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2867462ae3cbeb5ffd0b579a18930102bbb4587f69cce9560f71ccfe45d388(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce1d574a778dcfaaff152d6904ddbfd2a52d29bf76487b3575470de4447ce53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f219e0433cdc1eb2310fe1dbda8b85f0c7de821ff0ec23b262f6bc2bc353c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2fcfd545d5baf36578ad70268b48902477637f9984f3da0853c46f68bd9199(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cceb1e0f719d97cd34f9db6df9caff97dfab99c1d8f1db6062a6775df55f35e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248fa49cd04ac3de54817afd165297307e37930850cb9c97c63adfaa923f13c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67062dbe91f67594b590872e4494d158975edf96994a389fee0fe4266db8d760(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffa33efd7acd0fd96db240e87cabd26f8b807c0121e1aaa0e419bbb70c0b1d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStep]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cd059d89c13a70e004df203e4cb67585102aba2cae961b9c2c0bac87d04096(
    *,
    name: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924effedd68c580955b65321b7c05ed2af730e261eee0ebc54044fc57e911655(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f2eca506e981ce898c7973d5eeec75dd63f896f68df439bd416a3578a174d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b667331faeb6dfe84ba4e968fa0f581591a87d13371af74527fcf791eaac46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b92f14c88e9d55175ce5452f4f0a1c2a4e3880020ca8bb5b35124592df082c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a763cffebb2eaf36e0516e63f7e9d81028ccb3a2f8d277c6dcf1a34db5d01584(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0192567d210a8ef2b2464c8e224daf0a79f4c05f914671aa914a01f5b3627b90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildTriggerBuildStepVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3c80bf805abaa3118bbee0380f6559361774b5716fb6f5aa7731a301aae49d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38087e8cfe3cff4e18da4d3e4c02971fdb7b6d5e496e575984e73acfa7631a86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2a4048f0f901dcddab15a91a980c8dadc6b91c266625c973261b4e3361592a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f36830ccfc369732906f2c25400c7df5b1b3559eb27e53c80b672585d4a2901(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerBuildStepVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438f5ec09a4f7e318450a40224b923ee729fc1adc18edabf3f543d513b944fb2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    approval_config: typing.Optional[typing.Union[CloudbuildTriggerApprovalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_server_trigger_config: typing.Optional[typing.Union[CloudbuildTriggerBitbucketServerTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    build_attribute: typing.Optional[typing.Union[CloudbuildTriggerBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filename: typing.Optional[builtins.str] = None,
    filter: typing.Optional[builtins.str] = None,
    git_file_source: typing.Optional[typing.Union[CloudbuildTriggerGitFileSource, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[CloudbuildTriggerGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_build_logs: typing.Optional[builtins.str] = None,
    included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pubsub_config: typing.Optional[typing.Union[CloudbuildTriggerPubsubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_event_config: typing.Optional[typing.Union[CloudbuildTriggerRepositoryEventConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    source_to_build: typing.Optional[typing.Union[CloudbuildTriggerSourceToBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CloudbuildTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_template: typing.Optional[typing.Union[CloudbuildTriggerTriggerTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_config: typing.Optional[typing.Union[CloudbuildTriggerWebhookConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e5f0aa8c545ec0d6329c7a393cb10ab92853a360e02cbbb65dc1dbcf77a51d(
    *,
    path: builtins.str,
    repo_type: builtins.str,
    bitbucket_server_config: typing.Optional[builtins.str] = None,
    github_enterprise_config: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    revision: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f72fe9efa37e227595f86833ca89329c655a8ff146e4f8bc136fbaf2679414(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d98f7da8bbbe193ac349737d2103c9222b12212c5c7265d8ee85e38f19c035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b0aaf598c43b5cf28f045ed89f8d52482edd6e0f856ecb644588735415a6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6818af2dc1722ca3c0df439c1520663bcc3728c1ce2f4b246acba65d18447f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85601af3c06517e43250c7840277e136c6c30b965856fbd6e38ed587db3074e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa827c9b31abd37c6ca68df2abc289388b409273e1a52a160d371d7c9afc73f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ff592349bba7bea0b3d44b4289c3f996e7bfce05de5a2ac3a8bfd155ea1bfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a52eaa0b5cc13f4158dee281786a321d866e26d9c12e8853493a26e3bd11bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb45b99847ed5f74ef000df8eb45b0394a4529de3ca43c3cb9d0df9aa06564fa(
    value: typing.Optional[CloudbuildTriggerGitFileSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67715daadff33e93a7e587dd520e51c456e201b8783df04f41514e097834fc81(
    *,
    enterprise_config_resource_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    pull_request: typing.Optional[typing.Union[CloudbuildTriggerGithubPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[CloudbuildTriggerGithubPush, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce274279d4ad6d5ad4808c07a81e2e807abd102fda70c5c3c6bd9e9b2883121(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daadb2605afad70549bfc276aad9ef0baae83b6d43ae24563cfaf7dbd01ba1b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2232f45d32ce5580489a89919dc4e9023dbdeafde0b7d052358a5dd45615bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b62d84c656793fa4744e678716b91217df9be515f303e559ba8495c42dd124b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e62bfa90078d54eb2afd680c99c18827bd0c5249dd17c1eb641df8f62f3749(
    value: typing.Optional[CloudbuildTriggerGithub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc2c0c9505a30d34cf709f2bc50527c638ee08db2ed095c592cd40ad6bdc20e(
    *,
    branch: builtins.str,
    comment_control: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb673d4a927ff2205069cb37e467b2d0a6356ed6522c662aec683c0eff291c6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2fed4419f79df35d28b40e5427f5fe3e25804a0dee2e433d8b1ab0f3c2cc80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b015c7c2ac2546227de7887b4bda46dc0610c7170f0ffbae2d28bafe9acf6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477f49193b24f7ac5ee1f3d032e407c9c3031499dae68a0b7a00aa115104178b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c9d17bba8b1369ee1dc79d05381011e897e14c5ebd974d6287cc4c94c81248(
    value: typing.Optional[CloudbuildTriggerGithubPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96098449450845ea95987866995251203d0fca81809e40a30df15e6cc66bac98(
    *,
    branch: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0a5bd47375122be083af89170cc746407ef45e400e0b816a283dad9a09c039(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae1a3f01463abd9f065f79a78ec5c52ca509f5b60ce9e9f9615d23130741696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0407e25faf3dc75e30cc737a9e7fb977f2ea52dbcbefd8f7068b2a57ea79aeec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79a76ab6aaebfd5727e76cb713c6df9c950ad39552a05ec815932b27c5a54d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa183950bd19c6f5c50e6b9ba06edfda712d09fa0a3fa4a625b783acbe4849c6(
    value: typing.Optional[CloudbuildTriggerGithubPush],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1c5e24ecc9498d94fed62e0f918b7cad29fcfad5837af61a313ac7c6327e77(
    *,
    topic: builtins.str,
    service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685ad3b5b1294e962d448aec0500c34d25722487439d4b4a36a04dc437aef5e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24914bb866cf6929a38f9d59994cc6e02d4a09ae3ecf7e73222ac6488cbf64e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366baad77451b538db5dcb57f48e717f5608e399987e289092d867ce9c2c87e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bd728b801412ac52a80ba1b68f5133615f255811a9f19161956a2929d1bc3a(
    value: typing.Optional[CloudbuildTriggerPubsubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf328daf3e8539b9336fc1df83a498131d423d918095ebe18c73c6f2307f49d(
    *,
    pull_request: typing.Optional[typing.Union[CloudbuildTriggerRepositoryEventConfigPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[CloudbuildTriggerRepositoryEventConfigPush, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90d18203e83a5a15e498cd5b79ace4240fbc9bee9e9a836469ff7703e919f4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e116e1234e544442a53e2f9eb4ebd886069d82e25a500e9a72cd04e8dad6e1e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c1dddef793b83dbb13269922dfe75e029b60979844bd4bbe5e78ec6140f2e0(
    value: typing.Optional[CloudbuildTriggerRepositoryEventConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268c1fb3b08bd992bfe98951cbbd9a9e214a9ca8f8e5074093423f70c50b74a6(
    *,
    branch: typing.Optional[builtins.str] = None,
    comment_control: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1448dd8d81eae947b59eabac5c0dcd7407b744a5b0658238721c1af90d5c5904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a141ca4f8ccb66b3b09cbccca036556f5b24b102eaef4f3676fea872d89767c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e5d64cf090e4ce97641c81e5eb7f24b57139a0512b93e597bbce2e5ed887f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d65e489968112d7f33db0a0cbdcca37cfc9a416e8d530b0de6219625437d1a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441d296526d78640b461cf402dc88f8923e024c5c69b8987e8df22a37c03c91b(
    value: typing.Optional[CloudbuildTriggerRepositoryEventConfigPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ddefb982b7d126a096a40a662cd9c1511613113cabb5573bc18339e5544f63(
    *,
    branch: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab95019944ba110b704d2cc27d6b3916d993628d9a3cf87468c5c87c52021623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6655af4abdb4d9b11c20aa81f821d879b63a1a7ac1f8fae6728f67d57dbc90d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c6da31e971b10b30bbd59f6fecb8b8b94bcd9bd4da7c73dc0f25235881a1ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2c84c08b2f6cee4dd144a8e7ce903127dea590bb22221eae25ec8366cd970b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578465e3ce6e6c038a78172ba48d08da0d01fa400fd610a1a7870a24e7d4b25e(
    value: typing.Optional[CloudbuildTriggerRepositoryEventConfigPush],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36af2a45ef400e63c5065c0871332fcb9964f910ddda837dc8a6379947b9bce4(
    *,
    ref: builtins.str,
    repo_type: builtins.str,
    bitbucket_server_config: typing.Optional[builtins.str] = None,
    github_enterprise_config: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120e9a71c3b7b22a834b4e251860b6c4c632bcaddc3ba0e9db7613da3f26e80a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c505eff19ce7086549625c219f1efce6ab8a170ec135d42445c7bb1e58c37e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f8f6b466dc0e99433ae8249018650cf764c1d89498ed45be967f122463112a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabfe439a4f036fb87522446ec4403d322ff4bef732d9d8d1d9fa2d3b3c8f748(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e76bbb612a47a8360e426114dfedfdda99841b2caccb0662a18c6c2567b3622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acaae0178d1a7be22ee162ada7bb2acace2a8666b34aa611e2cc547c70623764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa4d4fca3474bd2002a204fe633cf54b4f6e349071826fe525494e47b8c0987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b31c30c76c29d58d540208502ceaa45a4958d6ad399baf7c6fcd17c31da067(
    value: typing.Optional[CloudbuildTriggerSourceToBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7289dee5f472ab494107798a893a17426c47b390cc3bb4d9428a5574e3fa2283(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a40b5451499b5a7a60bde68195f68b8ed759775ebcb05b03c46539805f1338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ccc2b1d34a4637bb2ef382f0888fec0870f080f804d808ddd4901cfe9c57ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1140e71eb77fab0955c77890dc2a14bc2478cba849c1571b0def40ef2057418d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a687f4debf69dc4c2717111689041b56fff2dff650b50e11e05e786028a9554f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddd9a3b18efea93fa06e0dd98253043dd81b7d887896f686679aca63cc03a45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildTriggerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26001b4c6c39c9e1cce3157704b9d1f20a15992a96362144be044153304475f8(
    *,
    branch_name: typing.Optional[builtins.str] = None,
    commit_sha: typing.Optional[builtins.str] = None,
    dir: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_id: typing.Optional[builtins.str] = None,
    repo_name: typing.Optional[builtins.str] = None,
    tag_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b15680c8ea710989ee48fdaf459eccac3990bd79c1c000020b880de2a3c101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5408e03b709db1971296c7fd71a71793e7a72a2c7535d85dc7f49edecafca7d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31454cee50aca497e3d84e0a4dc4328133862918b3626275cd1b1e4d1ba7e587(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bf7446cda1b9abf25d85e64f560c80e408cf2e0546b640d7ddc4a9f4d24407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db76baf5ad154ef6127f027529cc09add2653def2b0a090061e8d668336d1bea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c34980463e0312229ac31f342169232c397838b8d4b8af85d5139547b112d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726e552c8300c261f8b0191b98fd4ecd4bb21410bd499fbd8cebe2e0b11fc6a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dd852d16ac875dcef1fe018fe42d1d9ab4f5dc2e184ebfc3cf3f95ee39b08f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77628e0d8239a58ef7f01ce07c3dca632d606f156dd99c82e3a403a008f6652f(
    value: typing.Optional[CloudbuildTriggerTriggerTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bafc34c9259c5564428314cf9aefc3fdc03c0033b0206ac6acaa64937d08045(
    *,
    secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c15f9be34fdc0ac6db53f4a0615099dc50c46553c5209ac7249736e8c7d5075(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfedda6ccd86d3c16f9e40b751ad594ac5277f7df7a4e780e87879a1e7460184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced5d3f6ea29983501694415317d62f899986cd6b12bf607345bac560f14009b(
    value: typing.Optional[CloudbuildTriggerWebhookConfig],
) -> None:
    """Type checking stubs"""
    pass
