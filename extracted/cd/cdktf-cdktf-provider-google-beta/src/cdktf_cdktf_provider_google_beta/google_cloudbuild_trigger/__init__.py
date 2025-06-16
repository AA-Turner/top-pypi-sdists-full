r'''
# `google_cloudbuild_trigger`

Refer to the Terraform Registry for docs: [`google_cloudbuild_trigger`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger).
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


class GoogleCloudbuildTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger google_cloudbuild_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        approval_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerApprovalConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_server_trigger_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerBitbucketServerTriggerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        build_attribute: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        filter: typing.Optional[builtins.str] = None,
        git_file_source: typing.Optional[typing.Union["GoogleCloudbuildTriggerGitFileSource", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["GoogleCloudbuildTriggerGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_build_logs: typing.Optional[builtins.str] = None,
        included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pubsub_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerPubsubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        repository_event_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerRepositoryEventConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_to_build: typing.Optional[typing.Union["GoogleCloudbuildTriggerSourceToBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_template: typing.Optional[typing.Union["GoogleCloudbuildTriggerTriggerTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerWebhookConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger google_cloudbuild_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param approval_config: approval_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#approval_config GoogleCloudbuildTrigger#approval_config}
        :param bitbucket_server_trigger_config: bitbucket_server_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_trigger_config GoogleCloudbuildTrigger#bitbucket_server_trigger_config}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#build GoogleCloudbuildTrigger#build}
        :param description: Human-readable description of the trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#description GoogleCloudbuildTrigger#description}
        :param disabled: Whether the trigger is disabled or not. If true, the trigger will never result in a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#disabled GoogleCloudbuildTrigger#disabled}
        :param filename: Path, from the source root, to a file whose contents is used for the template. Either a filename or build template must be provided. Set this only when using trigger_template or github. When using Pub/Sub, Webhook or Manual set the file name using git_file_source instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#filename GoogleCloudbuildTrigger#filename}
        :param filter: A Common Expression Language string. Used only with Pub/Sub and Webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#filter GoogleCloudbuildTrigger#filter}
        :param git_file_source: git_file_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#git_file_source GoogleCloudbuildTrigger#git_file_source}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github GoogleCloudbuildTrigger#github}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#id GoogleCloudbuildTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignored_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If ignoredFiles and changed files are both empty, then they are not used to determine whether or not to trigger a build. If ignoredFiles is not empty, then we ignore any files that match any of the ignored_file globs. If the change has no files that are outside of the ignoredFiles globs, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#ignored_files GoogleCloudbuildTrigger#ignored_files}
        :param include_build_logs: Build logs will be sent back to GitHub as part of the checkrun result. Values can be INCLUDE_BUILD_LOGS_UNSPECIFIED or INCLUDE_BUILD_LOGS_WITH_STATUS Possible values: ["INCLUDE_BUILD_LOGS_UNSPECIFIED", "INCLUDE_BUILD_LOGS_WITH_STATUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#include_build_logs GoogleCloudbuildTrigger#include_build_logs}
        :param included_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is empty, then as far as this filter is concerned, we should trigger the build. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is not empty, then we make sure that at least one of those files matches a includedFiles glob. If not, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#included_files GoogleCloudbuildTrigger#included_files}
        :param location: The `Cloud Build location <https://cloud.google.com/build/docs/locations>`_ for the trigger. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#location GoogleCloudbuildTrigger#location}
        :param name: Name of the trigger. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project GoogleCloudbuildTrigger#project}.
        :param pubsub_config: pubsub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pubsub_config GoogleCloudbuildTrigger#pubsub_config}
        :param repository_event_config: repository_event_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository_event_config GoogleCloudbuildTrigger#repository_event_config}
        :param service_account: The service account used for all user-controlled operations including triggers.patch, triggers.run, builds.create, and builds.cancel. If no service account is set, then the standard Cloud Build service account ([PROJECT_NUM]@system.gserviceaccount.com) will be used instead. Format: projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_ID_OR_EMAIL} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#service_account GoogleCloudbuildTrigger#service_account}
        :param source_to_build: source_to_build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source_to_build GoogleCloudbuildTrigger#source_to_build}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a BuildTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tags GoogleCloudbuildTrigger#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeouts GoogleCloudbuildTrigger#timeouts}
        :param trigger_template: trigger_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#trigger_template GoogleCloudbuildTrigger#trigger_template}
        :param webhook_config: webhook_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#webhook_config GoogleCloudbuildTrigger#webhook_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79dec4c8b91abe7df451c8a9ff02c42d93070b222a174785345da6681314891c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudbuildTriggerConfig(
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
        '''Generates CDKTF code for importing a GoogleCloudbuildTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudbuildTrigger to import.
        :param import_from_id: The id of the existing GoogleCloudbuildTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudbuildTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070f1d3c370e3e3c9678a2402b1aa86f8ca2466ca67513f63cbd1aad053d1082)
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
        :param approval_required: Whether or not approval is needed. If this is set on a build, it will become pending when run, and will need to be explicitly approved to start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#approval_required GoogleCloudbuildTrigger#approval_required}
        '''
        value = GoogleCloudbuildTriggerApprovalConfig(
            approval_required=approval_required
        )

        return typing.cast(None, jsii.invoke(self, "putApprovalConfig", [value]))

    @jsii.member(jsii_name="putBitbucketServerTriggerConfig")
    def put_bitbucket_server_trigger_config(
        self,
        *,
        bitbucket_server_config_resource: builtins.str,
        project_key: builtins.str,
        repo_slug: builtins.str,
        pull_request: typing.Optional[typing.Union["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bitbucket_server_config_resource: The Bitbucket server config resource that this trigger config maps to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config_resource GoogleCloudbuildTrigger#bitbucket_server_config_resource}
        :param project_key: Key of the project that the repo is in. For example: The key for https://mybitbucket.server/projects/TEST/repos/test-repo is "TEST". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_key GoogleCloudbuildTrigger#project_key}
        :param repo_slug: Slug of the repository. A repository slug is a URL-friendly version of a repository name, automatically generated by Bitbucket for use in the URL. For example, if the repository name is 'test repo', in the URL it would become 'test-repo' as in https://mybitbucket.server/projects/TEST/repos/test-repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_slug GoogleCloudbuildTrigger#repo_slug}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        value = GoogleCloudbuildTriggerBitbucketServerTriggerConfig(
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
        step: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildStep", typing.Dict[builtins.str, typing.Any]]]],
        artifacts: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        available_secrets: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildAvailableSecrets", typing.Dict[builtins.str, typing.Any]]] = None,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        logs_bucket: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        queue_ttl: typing.Optional[builtins.str] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildSource", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param step: step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#step GoogleCloudbuildTrigger#step}
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#artifacts GoogleCloudbuildTrigger#artifacts}
        :param available_secrets: available_secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#available_secrets GoogleCloudbuildTrigger#available_secrets}
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images are pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build status is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#images GoogleCloudbuildTrigger#images}
        :param logs_bucket: Google Cloud Storage bucket where logs should be written. Logs file names will be of the format ${logsBucket}/log-${build_id}.txt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#logs_bucket GoogleCloudbuildTrigger#logs_bucket}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#options GoogleCloudbuildTrigger#options}
        :param queue_ttl: TTL in queue for this build. If provided and the build is enqueued longer than this value, the build will expire and the build status will be EXPIRED. The TTL starts ticking from createTime. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#queue_ttl GoogleCloudbuildTrigger#queue_ttl}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret GoogleCloudbuildTrigger#secret}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source GoogleCloudbuildTrigger#source}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a Build. These are not docker tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tags GoogleCloudbuildTrigger#tags}
        :param timeout: Amount of time that this build should be allowed to run, to second granularity. If this amount of time elapses, work on the build will cease and the build status will be TIMEOUT. This timeout must be equal to or greater than the sum of the timeouts for build steps within the build. The expected format is the number of seconds followed by s. Default time is ten minutes (600s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeout GoogleCloudbuildTrigger#timeout}
        '''
        value = GoogleCloudbuildTriggerBuild(
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
        :param path: The path of the file, with the repo root as the root of the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_type GoogleCloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config GoogleCloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github_enterprise_config GoogleCloudbuildTrigger#github_enterprise_config}
        :param repository: The fully qualified resource name of the Repo API repository. The fully qualified resource name of the Repo API repository. If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        :param revision: The branch, tag, arbitrary ref, or SHA version of the repo to use when resolving the filename (optional). This field respects the same syntax/resolution as described here: https://git-scm.com/docs/gitrevisions If unspecified, the revision from which the trigger invocation originated is assumed to be the revision from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#revision GoogleCloudbuildTrigger#revision}
        :param uri: The URI of the repo (optional). If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#uri GoogleCloudbuildTrigger#uri}
        '''
        value = GoogleCloudbuildTriggerGitFileSource(
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
        pull_request: typing.Optional[typing.Union["GoogleCloudbuildTriggerGithubPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["GoogleCloudbuildTriggerGithubPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enterprise_config_resource_name: The resource name of the github enterprise config that should be applied to this installation. For example: "projects/{$projectId}/locations/{$locationId}/githubEnterpriseConfigs/{$configId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#enterprise_config_resource_name GoogleCloudbuildTrigger#enterprise_config_resource_name}
        :param name: Name of the repository. For example: The name for https://github.com/googlecloudplatform/cloud-builders is "cloud-builders". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param owner: Owner of the repository. For example: The owner for https://github.com/googlecloudplatform/cloud-builders is "googlecloudplatform". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#owner GoogleCloudbuildTrigger#owner}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        value = GoogleCloudbuildTriggerGithub(
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
        :param topic: The name of the topic from which this subscription is receiving messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#topic GoogleCloudbuildTrigger#topic}
        :param service_account_email: Service account that will make the push request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#service_account_email GoogleCloudbuildTrigger#service_account_email}
        '''
        value = GoogleCloudbuildTriggerPubsubConfig(
            topic=topic, service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubConfig", [value]))

    @jsii.member(jsii_name="putRepositoryEventConfig")
    def put_repository_event_config(
        self,
        *,
        pull_request: typing.Optional[typing.Union["GoogleCloudbuildTriggerRepositoryEventConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["GoogleCloudbuildTriggerRepositoryEventConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        :param repository: The resource name of the Repo API resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        value = GoogleCloudbuildTriggerRepositoryEventConfig(
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
        :param ref: The branch or tag to use. Must start with "refs/" (required). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#ref GoogleCloudbuildTrigger#ref}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_type GoogleCloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config GoogleCloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github_enterprise_config GoogleCloudbuildTrigger#github_enterprise_config}
        :param repository: The qualified resource name of the Repo API repository. Either uri or repository can be specified and is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        :param uri: The URI of the repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#uri GoogleCloudbuildTrigger#uri}
        '''
        value = GoogleCloudbuildTriggerSourceToBuild(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#create GoogleCloudbuildTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#delete GoogleCloudbuildTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#update GoogleCloudbuildTrigger#update}.
        '''
        value = GoogleCloudbuildTriggerTimeouts(
            create=create, delete=delete, update=update
        )

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
        :param branch_name: Name of the branch to build. Exactly one a of branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch_name GoogleCloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one of a branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#commit_sha GoogleCloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_id GoogleCloudbuildTrigger#project_id}
        :param repo_name: Name of the Cloud Source Repository. If omitted, the name "default" is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_name GoogleCloudbuildTrigger#repo_name}
        :param tag_name: Name of the tag to build. Exactly one of a branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag_name GoogleCloudbuildTrigger#tag_name}
        '''
        value = GoogleCloudbuildTriggerTriggerTemplate(
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
        :param secret: Resource name for the secret required as a URL parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret GoogleCloudbuildTrigger#secret}
        '''
        value = GoogleCloudbuildTriggerWebhookConfig(secret=secret)

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
    def approval_config(self) -> "GoogleCloudbuildTriggerApprovalConfigOutputReference":
        return typing.cast("GoogleCloudbuildTriggerApprovalConfigOutputReference", jsii.get(self, "approvalConfig"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerTriggerConfig")
    def bitbucket_server_trigger_config(
        self,
    ) -> "GoogleCloudbuildTriggerBitbucketServerTriggerConfigOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBitbucketServerTriggerConfigOutputReference", jsii.get(self, "bitbucketServerTriggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> "GoogleCloudbuildTriggerBuildOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBuildOutputReference", jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="gitFileSource")
    def git_file_source(self) -> "GoogleCloudbuildTriggerGitFileSourceOutputReference":
        return typing.cast("GoogleCloudbuildTriggerGitFileSourceOutputReference", jsii.get(self, "gitFileSource"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> "GoogleCloudbuildTriggerGithubOutputReference":
        return typing.cast("GoogleCloudbuildTriggerGithubOutputReference", jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="pubsubConfig")
    def pubsub_config(self) -> "GoogleCloudbuildTriggerPubsubConfigOutputReference":
        return typing.cast("GoogleCloudbuildTriggerPubsubConfigOutputReference", jsii.get(self, "pubsubConfig"))

    @builtins.property
    @jsii.member(jsii_name="repositoryEventConfig")
    def repository_event_config(
        self,
    ) -> "GoogleCloudbuildTriggerRepositoryEventConfigOutputReference":
        return typing.cast("GoogleCloudbuildTriggerRepositoryEventConfigOutputReference", jsii.get(self, "repositoryEventConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceToBuild")
    def source_to_build(self) -> "GoogleCloudbuildTriggerSourceToBuildOutputReference":
        return typing.cast("GoogleCloudbuildTriggerSourceToBuildOutputReference", jsii.get(self, "sourceToBuild"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudbuildTriggerTimeoutsOutputReference":
        return typing.cast("GoogleCloudbuildTriggerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="triggerId")
    def trigger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerId"))

    @builtins.property
    @jsii.member(jsii_name="triggerTemplate")
    def trigger_template(
        self,
    ) -> "GoogleCloudbuildTriggerTriggerTemplateOutputReference":
        return typing.cast("GoogleCloudbuildTriggerTriggerTemplateOutputReference", jsii.get(self, "triggerTemplate"))

    @builtins.property
    @jsii.member(jsii_name="webhookConfig")
    def webhook_config(self) -> "GoogleCloudbuildTriggerWebhookConfigOutputReference":
        return typing.cast("GoogleCloudbuildTriggerWebhookConfigOutputReference", jsii.get(self, "webhookConfig"))

    @builtins.property
    @jsii.member(jsii_name="approvalConfigInput")
    def approval_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerApprovalConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerApprovalConfig"], jsii.get(self, "approvalConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketServerTriggerConfigInput")
    def bitbucket_server_trigger_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfig"], jsii.get(self, "bitbucketServerTriggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="buildAttributeInput")
    def build_attribute_input(self) -> typing.Optional["GoogleCloudbuildTriggerBuild"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuild"], jsii.get(self, "buildAttributeInput"))

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
    ) -> typing.Optional["GoogleCloudbuildTriggerGitFileSource"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGitFileSource"], jsii.get(self, "gitFileSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(self) -> typing.Optional["GoogleCloudbuildTriggerGithub"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGithub"], jsii.get(self, "githubInput"))

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
    def pubsub_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerPubsubConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerPubsubConfig"], jsii.get(self, "pubsubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryEventConfigInput")
    def repository_event_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfig"], jsii.get(self, "repositoryEventConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceToBuildInput")
    def source_to_build_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerSourceToBuild"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerSourceToBuild"], jsii.get(self, "sourceToBuildInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildTriggerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildTriggerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTemplateInput")
    def trigger_template_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerTriggerTemplate"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerTriggerTemplate"], jsii.get(self, "triggerTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookConfigInput")
    def webhook_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerWebhookConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerWebhookConfig"], jsii.get(self, "webhookConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2c25fd74f6825d1475845dc19d8e022062bd497052f6566f779cb0a8d0c12b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8af35c674795464f09f7aaffbf643171f32f20450a50eeb278ec7f2056c07a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71c958103c8d5e8f8b4156195eeaeb3f595c4d63352970a7a0576eeeb18b2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277f5d893a13f4c391c6dcc2e99125be0b6326bc93b7446a032349426e605ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755116e79189508780fdd5635d01f662d235c06102fea2b3e3976b65ad55b0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoredFiles")
    def ignored_files(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ignoredFiles"))

    @ignored_files.setter
    def ignored_files(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575ab032dd6cbf4b8f721539f9e7c82c9d64c02b6193ce3cf99336cb5b45c450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoredFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeBuildLogs")
    def include_build_logs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includeBuildLogs"))

    @include_build_logs.setter
    def include_build_logs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdeea4f9133576a8ad283e9deec649e7c395391442e5270addc6442634ef83f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeBuildLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedFiles")
    def included_files(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedFiles"))

    @included_files.setter
    def included_files(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ccde23af9c8934727afa043d45a7c563cdc7426d63baa69fcc6fbdd3d4ef5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e85eca937644417bac2543aed62b2e4b8cde7e063f08463abce7c8835a0e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6111c39b7a0c4c5a7341c6ff3b5a99af1c1b7b108fe6876459015d4176aafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9e6f1b06c1adcb7eda28454d43cb7df1d530e839d51c5d84059b0d851d006a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa27b8a2cafc33c478de205423c1434d84f5cd749429f7b608c95f70fa7a92db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutions")
    def substitutions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitutions"))

    @substitutions.setter
    def substitutions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c02f26ba506dd8726fba2670cc2fb16d9897d66e8adcfafec28555cb4ade04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc44e4ea5f33e375faec10a03ef28a1109e6a7f49b704e334492cf520ecd908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerApprovalConfig",
    jsii_struct_bases=[],
    name_mapping={"approval_required": "approvalRequired"},
)
class GoogleCloudbuildTriggerApprovalConfig:
    def __init__(
        self,
        *,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_required: Whether or not approval is needed. If this is set on a build, it will become pending when run, and will need to be explicitly approved to start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#approval_required GoogleCloudbuildTrigger#approval_required}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846c39a89d2e83a47750cbe865ca7e726b9c5f420df72917694722f38fa54605)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#approval_required GoogleCloudbuildTrigger#approval_required}
        '''
        result = self._values.get("approval_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerApprovalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerApprovalConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerApprovalConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f48dd5e2d330334c767e678efcce3a5108f963461d4a4445c4cc15e8562112)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd08c6cb1d9ca9998436aafe3f40e63be5a69c7e03efe9659c9ece0448a4f6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerApprovalConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerApprovalConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerApprovalConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e731c4925a6da26a5298cf6249fe5d40da78158e31580f2c1ece483df4c4338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBitbucketServerTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bitbucket_server_config_resource": "bitbucketServerConfigResource",
        "project_key": "projectKey",
        "repo_slug": "repoSlug",
        "pull_request": "pullRequest",
        "push": "push",
    },
)
class GoogleCloudbuildTriggerBitbucketServerTriggerConfig:
    def __init__(
        self,
        *,
        bitbucket_server_config_resource: builtins.str,
        project_key: builtins.str,
        repo_slug: builtins.str,
        pull_request: typing.Optional[typing.Union["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bitbucket_server_config_resource: The Bitbucket server config resource that this trigger config maps to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config_resource GoogleCloudbuildTrigger#bitbucket_server_config_resource}
        :param project_key: Key of the project that the repo is in. For example: The key for https://mybitbucket.server/projects/TEST/repos/test-repo is "TEST". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_key GoogleCloudbuildTrigger#project_key}
        :param repo_slug: Slug of the repository. A repository slug is a URL-friendly version of a repository name, automatically generated by Bitbucket for use in the URL. For example, if the repository name is 'test repo', in the URL it would become 'test-repo' as in https://mybitbucket.server/projects/TEST/repos/test-repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_slug GoogleCloudbuildTrigger#repo_slug}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        if isinstance(pull_request, dict):
            pull_request = GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest(**pull_request)
        if isinstance(push, dict):
            push = GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush(**push)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16607d103f74ad141e007b065dcf13058da43382078ce031483ca69cef86b378)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config_resource GoogleCloudbuildTrigger#bitbucket_server_config_resource}
        '''
        result = self._values.get("bitbucket_server_config_resource")
        assert result is not None, "Required property 'bitbucket_server_config_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''Key of the project that the repo is in. For example: The key for https://mybitbucket.server/projects/TEST/repos/test-repo is "TEST".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_key GoogleCloudbuildTrigger#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_slug(self) -> builtins.str:
        '''Slug of the repository.

        A repository slug is a URL-friendly version of a repository name, automatically generated by Bitbucket for use in the URL.
        For example, if the repository name is 'test repo', in the URL it would become 'test-repo' as in https://mybitbucket.server/projects/TEST/repos/test-repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_slug GoogleCloudbuildTrigger#repo_slug}
        '''
        result = self._values.get("repo_slug")
        assert result is not None, "Required property 'repo_slug' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pull_request(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest"], result)

    @builtins.property
    def push(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush"]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBitbucketServerTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBitbucketServerTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBitbucketServerTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36e6a6269b7ab19005f0436b48f37e3240f2b22c2a10763599a41001fa536a6d)
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
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment /gcbrun. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        value = GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest(
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
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the gitRef regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        value = GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush(
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
    ) -> "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(
        self,
    ) -> "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference", jsii.get(self, "push"))

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
    ) -> typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush"], jsii.get(self, "pushInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3b803888d1c74d37b3099a023e2c62d7f1050372f64b616b05810a46c13a5374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitbucketServerConfigResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1862cf61f16014dc63540d98932270e113ae24e43d7115d2b04253b84d52b7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoSlug")
    def repo_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoSlug"))

    @repo_slug.setter
    def repo_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b457e5b2af0756fa6149f73b55082ae882d6228a911d1b97b0641b401014fcc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b667e9d5afbeb542daa30dea99251894baf2d5213505c264c33f0a175124fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "comment_control": "commentControl",
        "invert_regex": "invertRegex",
    },
)
class GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest:
    def __init__(
        self,
        *,
        branch: builtins.str,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment /gcbrun. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd491bb8d23824300563e9af0558c38ff2544321f30f08f5c7af90353e8fe12)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment_control(self) -> typing.Optional[builtins.str]:
        '''Configure builds to run whether a repository owner or collaborator need to comment /gcbrun. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        '''
        result = self._values.get("comment_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, branches that do NOT match the git_ref will trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66b7d6b61383b4651c15f4dc94ec50d58c388d67b396a9f2eccbb00a3d6c2a11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5333c4baf8e7fdd09ff68b061170a8b704891cca1e1f46bd9fad005fabbf92eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentControl")
    def comment_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commentControl"))

    @comment_control.setter
    def comment_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175c965aebdb179edb9aae5c6b7088568b52ee79cd365b29a40aee5388cce432)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9318adc3caa83a55c917e085361709383c2c72c405728a9ab8e2d8806b185c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e9c89721f6785b02594e451db41de39cc889105f0587da2b929c944ac3bd6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "invert_regex": "invertRegex", "tag": "tag"},
)
class GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the gitRef regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5464cd118f240ed04c2190115285e98752fed9c93a305bb581e04a3d3caa48e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, only trigger a build if the revision regex does NOT match the gitRef regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Regex of tags to match.  Specify only one of branch or tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4879d370d4eee05f089a8ec7fb77c38007ae228568a5e5b950a40f3066c9123)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0590b4824659bff13abd0d9ab620c03e79fb8e7e2a2f4930a8a25ddecfffeeb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__615fe75e4eaf9b054adb307666949c2f37016629f5f4168ca3d8af52ed71142e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21fa0be4e7584f079257c9019b598c2ae131e7108d25b18014107f0f182d720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f73cef6354fc84d9a7f70ba8e63f12e87a7d3d202a18d102d366aa53382c17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuild",
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
class GoogleCloudbuildTriggerBuild:
    def __init__(
        self,
        *,
        step: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildStep", typing.Dict[builtins.str, typing.Any]]]],
        artifacts: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildArtifacts", typing.Dict[builtins.str, typing.Any]]] = None,
        available_secrets: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildAvailableSecrets", typing.Dict[builtins.str, typing.Any]]] = None,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        logs_bucket: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        queue_ttl: typing.Optional[builtins.str] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildSource", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param step: step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#step GoogleCloudbuildTrigger#step}
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#artifacts GoogleCloudbuildTrigger#artifacts}
        :param available_secrets: available_secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#available_secrets GoogleCloudbuildTrigger#available_secrets}
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images are pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build status is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#images GoogleCloudbuildTrigger#images}
        :param logs_bucket: Google Cloud Storage bucket where logs should be written. Logs file names will be of the format ${logsBucket}/log-${build_id}.txt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#logs_bucket GoogleCloudbuildTrigger#logs_bucket}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#options GoogleCloudbuildTrigger#options}
        :param queue_ttl: TTL in queue for this build. If provided and the build is enqueued longer than this value, the build will expire and the build status will be EXPIRED. The TTL starts ticking from createTime. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#queue_ttl GoogleCloudbuildTrigger#queue_ttl}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret GoogleCloudbuildTrigger#secret}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source GoogleCloudbuildTrigger#source}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a Build. These are not docker tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tags GoogleCloudbuildTrigger#tags}
        :param timeout: Amount of time that this build should be allowed to run, to second granularity. If this amount of time elapses, work on the build will cease and the build status will be TIMEOUT. This timeout must be equal to or greater than the sum of the timeouts for build steps within the build. The expected format is the number of seconds followed by s. Default time is ten minutes (600s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeout GoogleCloudbuildTrigger#timeout}
        '''
        if isinstance(artifacts, dict):
            artifacts = GoogleCloudbuildTriggerBuildArtifacts(**artifacts)
        if isinstance(available_secrets, dict):
            available_secrets = GoogleCloudbuildTriggerBuildAvailableSecrets(**available_secrets)
        if isinstance(options, dict):
            options = GoogleCloudbuildTriggerBuildOptions(**options)
        if isinstance(source, dict):
            source = GoogleCloudbuildTriggerBuildSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77058a7e80dbee84c84792703b9a447dd76b17b5713321109fff772a545654e6)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStep"]]:
        '''step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#step GoogleCloudbuildTrigger#step}
        '''
        result = self._values.get("step")
        assert result is not None, "Required property 'step' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStep"]], result)

    @builtins.property
    def artifacts(self) -> typing.Optional["GoogleCloudbuildTriggerBuildArtifacts"]:
        '''artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#artifacts GoogleCloudbuildTrigger#artifacts}
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildArtifacts"], result)

    @builtins.property
    def available_secrets(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBuildAvailableSecrets"]:
        '''available_secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#available_secrets GoogleCloudbuildTrigger#available_secrets}
        '''
        result = self._values.get("available_secrets")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildAvailableSecrets"], result)

    @builtins.property
    def images(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of images to be pushed upon the successful completion of all build steps.

        The images are pushed using the builder service account's credentials.
        The digests of the pushed images will be stored in the Build resource's results field.
        If any of the images fail to be pushed, the build status is marked FAILURE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#images GoogleCloudbuildTrigger#images}
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logs_bucket(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage bucket where logs should be written. Logs file names will be of the format ${logsBucket}/log-${build_id}.txt.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#logs_bucket GoogleCloudbuildTrigger#logs_bucket}
        '''
        result = self._values.get("logs_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional["GoogleCloudbuildTriggerBuildOptions"]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#options GoogleCloudbuildTrigger#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildOptions"], result)

    @builtins.property
    def queue_ttl(self) -> typing.Optional[builtins.str]:
        '''TTL in queue for this build.

        If provided and the build is enqueued longer than this value,
        the build will expire and the build status will be EXPIRED.
        The TTL starts ticking from createTime.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#queue_ttl GoogleCloudbuildTrigger#queue_ttl}
        '''
        result = self._values.get("queue_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildSecret"]]]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret GoogleCloudbuildTrigger#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildSecret"]]], result)

    @builtins.property
    def source(self) -> typing.Optional["GoogleCloudbuildTriggerBuildSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source GoogleCloudbuildTrigger#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildSource"], result)

    @builtins.property
    def substitutions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Substitutions data for Build resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        '''
        result = self._values.get("substitutions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags for annotation of a Build. These are not docker tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tags GoogleCloudbuildTrigger#tags}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeout GoogleCloudbuildTrigger#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "images": "images",
        "maven_artifacts": "mavenArtifacts",
        "npm_packages": "npmPackages",
        "objects": "objects",
        "python_packages": "pythonPackages",
    },
)
class GoogleCloudbuildTriggerBuildArtifacts:
    def __init__(
        self,
        *,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        maven_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        npm_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildArtifactsNpmPackages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        objects: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildArtifactsObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        python_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildArtifactsPythonPackages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images will be pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#images GoogleCloudbuildTrigger#images}
        :param maven_artifacts: maven_artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#maven_artifacts GoogleCloudbuildTrigger#maven_artifacts}
        :param npm_packages: npm_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#npm_packages GoogleCloudbuildTrigger#npm_packages}
        :param objects: objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#objects GoogleCloudbuildTrigger#objects}
        :param python_packages: python_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#python_packages GoogleCloudbuildTrigger#python_packages}
        '''
        if isinstance(objects, dict):
            objects = GoogleCloudbuildTriggerBuildArtifactsObjects(**objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0570c1678c20dcad77f4596ff00c3fd8867f6a7bb003f6694865ed9bed610b53)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#images GoogleCloudbuildTrigger#images}
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def maven_artifacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts"]]]:
        '''maven_artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#maven_artifacts GoogleCloudbuildTrigger#maven_artifacts}
        '''
        result = self._values.get("maven_artifacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts"]]], result)

    @builtins.property
    def npm_packages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsNpmPackages"]]]:
        '''npm_packages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#npm_packages GoogleCloudbuildTrigger#npm_packages}
        '''
        result = self._values.get("npm_packages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsNpmPackages"]]], result)

    @builtins.property
    def objects(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBuildArtifactsObjects"]:
        '''objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#objects GoogleCloudbuildTrigger#objects}
        '''
        result = self._values.get("objects")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildArtifactsObjects"], result)

    @builtins.property
    def python_packages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsPythonPackages"]]]:
        '''python_packages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#python_packages GoogleCloudbuildTrigger#python_packages}
        '''
        result = self._values.get("python_packages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsPythonPackages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "group_id": "groupId",
        "path": "path",
        "repository": "repository",
        "version": "version",
    },
)
class GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts:
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
        :param artifact_id: Maven artifactId value used when uploading the artifact to Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#artifact_id GoogleCloudbuildTrigger#artifact_id}
        :param group_id: Maven groupId value used when uploading the artifact to Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#group_id GoogleCloudbuildTrigger#group_id}
        :param path: Path to an artifact in the build's workspace to be uploaded to Artifact Registry. This can be either an absolute path, e.g. /workspace/my-app/target/my-app-1.0.SNAPSHOT.jar or a relative path from /workspace, e.g. my-app/target/my-app-1.0.SNAPSHOT.jar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        :param repository: Artifact Registry repository, in the form "https://$REGION-maven.pkg.dev/$PROJECT/$REPOSITORY". Artifact in the workspace specified by path will be uploaded to Artifact Registry with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        :param version: Maven version value used when uploading the artifact to Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#version GoogleCloudbuildTrigger#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c799a80064aa84878ed2ccb1b203e9b7839ac3b0125ed1068416da909421f1c5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#artifact_id GoogleCloudbuildTrigger#artifact_id}
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Maven groupId value used when uploading the artifact to Artifact Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#group_id GoogleCloudbuildTrigger#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to an artifact in the build's workspace to be uploaded to Artifact Registry.

        This can be either an absolute path, e.g. /workspace/my-app/target/my-app-1.0.SNAPSHOT.jar or a relative path from /workspace, e.g. my-app/target/my-app-1.0.SNAPSHOT.jar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry repository, in the form "https://$REGION-maven.pkg.dev/$PROJECT/$REPOSITORY".

        Artifact in the workspace specified by path will be uploaded to Artifact Registry with this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Maven version value used when uploading the artifact to Artifact Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#version GoogleCloudbuildTrigger#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbd9d6f9ead346d1d8d4b55cadf43b299a57390c507b5eadc4f0888ae22f6f6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5dbcdadd5a1a1a9fc9cd42df1f1ca02f66da559c7a82109719ee6dcf3476edf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a813fd27fb3391f11493825e10513bc0645181a5bb869bb4e025774ec82cd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b24b9d7d931eed0d8c5883f5eebbe7e426685f9b63e15940f528d89e7e65bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1425563962e74f57fd34665b872fdc5a515177ad44464d7ea12ab76ab9a1e1f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cbe15ebea15c633349200fcf382e388fceb8227d64b3eb9214ded3b392c11c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b0726101ecb87d8c4f41b1b07adebce418c8d13afd7c458c1413ba578cbf434)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2bbdde86000a559737177b428b52e6d7a26548d24a9c2f6e4af2fbe59406866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d3a4248a8081454ffd900452bf24623ec1418eda29f213470c11d9993f67f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002d432941e526988a29c76d0e1d393e199a0fad16fde020b6c03965bbe52e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826f374be17852aeb2d70feb98be4e2aaede2053dc004f679067d7c6270d8780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f0386a44fce9e23ddc4038467f7985aad399723d6f01f33a869515e903edf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f2b4e54d8b1cf6333c614311e1195b7356c68e056b1897cf0d7b3aeb8859c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsNpmPackages",
    jsii_struct_bases=[],
    name_mapping={"package_path": "packagePath", "repository": "repository"},
)
class GoogleCloudbuildTriggerBuildArtifactsNpmPackages:
    def __init__(
        self,
        *,
        package_path: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param package_path: Path to the package.json. e.g. workspace/path/to/package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#package_path GoogleCloudbuildTrigger#package_path}
        :param repository: Artifact Registry repository, in the form "https://$REGION-npm.pkg.dev/$PROJECT/$REPOSITORY". Npm package in the workspace specified by path will be zipped and uploaded to Artifact Registry with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff45e44225193553091c29a44c71b104c8267ba18a0ef1479501dbd5a5cc393e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#package_path GoogleCloudbuildTrigger#package_path}
        '''
        result = self._values.get("package_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry repository, in the form "https://$REGION-npm.pkg.dev/$PROJECT/$REPOSITORY".

        Npm package in the workspace specified by path will be zipped and uploaded to Artifact Registry with this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildArtifactsNpmPackages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildArtifactsNpmPackagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsNpmPackagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed856e3fbea1088aec5f1502338ad2f5cd9c97fa729b85007f275ecb86cbac4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildArtifactsNpmPackagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4133d10e92379f33168fb4dbc856ce9914e851c1e6621d025dc02667560dc82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildArtifactsNpmPackagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588c8d6512fe3180619ed79b91f2a083a842313e7c7439aad83591fb0383e9ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9cad181ae6f8ec5f85f269ea4c2656170394708bd7c356d128b08e5d24f893f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c0751caa22d2aef3325eb383e34cafc8a2611049e94ec62b109cd6e8540594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc40ce408d9e53a3d5a6831691b3c4f91cc190f6255af9958372449d671752ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildArtifactsNpmPackagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsNpmPackagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1d8a035589c2966fb85d7d18043f952c56bcf6fbf7418b8cc9a0195d602de4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4fe646051efdc2a23309f09c4848b18b92ba0345e455c0e27ce50432a03d81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packagePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8482048d878e40de67fb952ca216653c7350af56897298e9c89bc81bf55c924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsNpmPackages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsNpmPackages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cbbc59a8f42b6f77c1f219cb2e249cc5e713a34cd9a536337ab8abf903d0c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsObjects",
    jsii_struct_bases=[],
    name_mapping={"location": "location", "paths": "paths"},
)
class GoogleCloudbuildTriggerBuildArtifactsObjects:
    def __init__(
        self,
        *,
        location: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: Cloud Storage bucket and optional object path, in the form "gs://bucket/path/to/somewhere/". Files in the workspace matching any path pattern will be uploaded to Cloud Storage with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#location GoogleCloudbuildTrigger#location}
        :param paths: Path globs used to match files in the build's workspace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#paths GoogleCloudbuildTrigger#paths}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9a1c05db32e8dedbdef887ff14d4629822451b63bf27f5c1596d5ed0d2c7e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#location GoogleCloudbuildTrigger#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Path globs used to match files in the build's workspace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#paths GoogleCloudbuildTrigger#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildArtifactsObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildArtifactsObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda1f5b96775dc044c03cedba389807ea171a14089763ede837320a9bac5f8ce)
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
    def timing(self) -> "GoogleCloudbuildTriggerBuildArtifactsObjectsTimingList":
        return typing.cast("GoogleCloudbuildTriggerBuildArtifactsObjectsTimingList", jsii.get(self, "timing"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1a57d243e0562b241cd7ad21ad1901b062f2bbbecd20828b10517d40d115008d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0f4a38c7fbb32194fef87e67328c7a2f196c5b78760e3e95a16afcc36ee1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjects]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38bb576792a1b9087be4fc335341e62e17133dc6bbace9ac0880ce2103f9ad0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsObjectsTiming",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudbuildTriggerBuildArtifactsObjectsTiming:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildArtifactsObjectsTiming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildArtifactsObjectsTimingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsObjectsTimingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34427fde05941cb5a3c66ddcbdbe3917218391c79f62661fff7880d32dfc4d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildArtifactsObjectsTimingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f9d39c97f8ac7574605b6227dad03a81aa7a774a0bffdbc59b2602db57d51c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildArtifactsObjectsTimingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8147b4196e88b4d0d65d76bf4dcd3bfed247f680cb647fe75b4f0a5baeca667a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a8b67d23beecb3ee912069b636848a65c8904f71241e2eb7c47a5881f6454cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b567f6ad3a144ae2edc59deb4821fd4d44f37bb15f79893fd70023ac13a6242f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildArtifactsObjectsTimingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsObjectsTimingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cab724f8e6b2f146b2c4db7a1ec0d1691546d2e080b77abb7c0640623171790)
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
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjectsTiming]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjectsTiming], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjectsTiming],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c61c0873f239298524bf96158ee26ec2360b76e1f25361630d91876963f2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e500529e9e2e489f76af7de6b733fdcfc044ef47b5dbb663aa75395f21fac38c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMavenArtifacts")
    def put_maven_artifacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0243bf6c4deac17289aa4c603fd08217f6819ed0e142e2b676a4b1f8888c60ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMavenArtifacts", [value]))

    @jsii.member(jsii_name="putNpmPackages")
    def put_npm_packages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e1a5cde9dc44a22eae1903950efc8d6d839fcd3b89b7afe474f4f8384679d8)
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
        :param location: Cloud Storage bucket and optional object path, in the form "gs://bucket/path/to/somewhere/". Files in the workspace matching any path pattern will be uploaded to Cloud Storage with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#location GoogleCloudbuildTrigger#location}
        :param paths: Path globs used to match files in the build's workspace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#paths GoogleCloudbuildTrigger#paths}
        '''
        value = GoogleCloudbuildTriggerBuildArtifactsObjects(
            location=location, paths=paths
        )

        return typing.cast(None, jsii.invoke(self, "putObjects", [value]))

    @jsii.member(jsii_name="putPythonPackages")
    def put_python_packages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildArtifactsPythonPackages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bf724484f623c89ac0b65a17dced72fa4558ccba3d0244a4471e6167d6f94e)
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
    def maven_artifacts(
        self,
    ) -> GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsList:
        return typing.cast(GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsList, jsii.get(self, "mavenArtifacts"))

    @builtins.property
    @jsii.member(jsii_name="npmPackages")
    def npm_packages(self) -> GoogleCloudbuildTriggerBuildArtifactsNpmPackagesList:
        return typing.cast(GoogleCloudbuildTriggerBuildArtifactsNpmPackagesList, jsii.get(self, "npmPackages"))

    @builtins.property
    @jsii.member(jsii_name="objects")
    def objects(self) -> GoogleCloudbuildTriggerBuildArtifactsObjectsOutputReference:
        return typing.cast(GoogleCloudbuildTriggerBuildArtifactsObjectsOutputReference, jsii.get(self, "objects"))

    @builtins.property
    @jsii.member(jsii_name="pythonPackages")
    def python_packages(
        self,
    ) -> "GoogleCloudbuildTriggerBuildArtifactsPythonPackagesList":
        return typing.cast("GoogleCloudbuildTriggerBuildArtifactsPythonPackagesList", jsii.get(self, "pythonPackages"))

    @builtins.property
    @jsii.member(jsii_name="imagesInput")
    def images_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "imagesInput"))

    @builtins.property
    @jsii.member(jsii_name="mavenArtifactsInput")
    def maven_artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]], jsii.get(self, "mavenArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="npmPackagesInput")
    def npm_packages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]], jsii.get(self, "npmPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectsInput")
    def objects_input(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjects]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjects], jsii.get(self, "objectsInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonPackagesInput")
    def python_packages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsPythonPackages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildArtifactsPythonPackages"]]], jsii.get(self, "pythonPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "images"))

    @images.setter
    def images(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918d203435d4f20694ed998c2d76adf5add1c50bebf31e16c94f99a9a7b9820e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "images", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerBuildArtifacts]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildArtifacts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildArtifacts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aac08d9f6f73a8eb94f12b948a84c7aebf11ccaaae8c343c76c32555edd4631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsPythonPackages",
    jsii_struct_bases=[],
    name_mapping={"paths": "paths", "repository": "repository"},
)
class GoogleCloudbuildTriggerBuildArtifactsPythonPackages:
    def __init__(
        self,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param paths: Path globs used to match files in the build's workspace. For Python/ Twine, this is usually dist/*, and sometimes additionally an .asc file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#paths GoogleCloudbuildTrigger#paths}
        :param repository: Artifact Registry repository, in the form "https://$REGION-python.pkg.dev/$PROJECT/$REPOSITORY". Files in the workspace matching any path pattern will be uploaded to Artifact Registry with this location as a prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c1c6ae08f384e60252d9b27dc5b2806e8c553edc24f6113be3a5df4105655f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#paths GoogleCloudbuildTrigger#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry repository, in the form "https://$REGION-python.pkg.dev/$PROJECT/$REPOSITORY".

        Files in the workspace matching any path pattern will be uploaded to Artifact Registry with this location as a prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildArtifactsPythonPackages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildArtifactsPythonPackagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsPythonPackagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a37085f8499941cfc867456f70af8c2dc776170de4489d8223b534a5206b1bfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildArtifactsPythonPackagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d14da43dd77b8731a3383abc12dfb7ea6ca7303dce6b24c3ac12f7fef95f4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildArtifactsPythonPackagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be582e2946e7d032dc245b4eca79345a8463c59d96d33df359ff9ec842d30b38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a91a9c34a1f77c0cf38a57f5d4ceafe10d37cbd032e5d5e437fb1b4e9ff09f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34e90ecd9a5d4faf30759f42410a6c79ebfe78dc28a0d9120024602e2b02e606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsPythonPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsPythonPackages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsPythonPackages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6a39cadfd3fdc2862ebf37a4a4ba445d9abf71694c7faac576c6ab42338d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildArtifactsPythonPackagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildArtifactsPythonPackagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d82cdcef61ef3f4671b53199ece75e4631b53c491603d58f4db7e606b5a0eab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79f569965acca4b64d53e46fafd1c3d4f92a9eca3bf7e63e82f651d45ac1444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33be15a1ea65d6b2e27ec5699741e93fc92a4fabcfa5f045c79bcce88332a32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsPythonPackages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsPythonPackages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsPythonPackages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836c2f389046e5a78ce59b85e26a34bb7f98387f081da844a9f3279e718d8bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildAvailableSecrets",
    jsii_struct_bases=[],
    name_mapping={"secret_manager": "secretManager"},
)
class GoogleCloudbuildTriggerBuildAvailableSecrets:
    def __init__(
        self,
        *,
        secret_manager: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param secret_manager: secret_manager block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_manager GoogleCloudbuildTrigger#secret_manager}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794e2578215992257c9bbea92c88ba325368239d30fba749033f28d295031d96)
            check_type(argname="argument secret_manager", value=secret_manager, expected_type=type_hints["secret_manager"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_manager": secret_manager,
        }

    @builtins.property
    def secret_manager(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager"]]:
        '''secret_manager block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_manager GoogleCloudbuildTrigger#secret_manager}
        '''
        result = self._values.get("secret_manager")
        assert result is not None, "Required property 'secret_manager' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildAvailableSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildAvailableSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildAvailableSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__887a5c25ea1ef5c68170f832c0e3ba5b0b9c7387eb8e19017f5e696913c7307d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretManager")
    def put_secret_manager(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1593bd2282bccef7aaf925cb3a4867c7b88ab1eaae473589fa0cade68e6b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretManager", [value]))

    @builtins.property
    @jsii.member(jsii_name="secretManager")
    def secret_manager(
        self,
    ) -> "GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerList":
        return typing.cast("GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerList", jsii.get(self, "secretManager"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerInput")
    def secret_manager_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager"]]], jsii.get(self, "secretManagerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildAvailableSecrets]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildAvailableSecrets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildAvailableSecrets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0531197abffa43798e651f214222eabd6b073da48096ccec8df7581433a779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "version_name": "versionName"},
)
class GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager:
    def __init__(self, *, env: builtins.str, version_name: builtins.str) -> None:
        '''
        :param env: Environment variable name to associate with the secret. Secret environment variables must be unique across all of a build's secrets, and must be used by at least one build step. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        :param version_name: Resource name of the SecretVersion. In format: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#version_name GoogleCloudbuildTrigger#version_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3036f7c31629509a182caf256b97a90f9d7dbd06d104eb46ca141fefc033b39f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        '''
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_name(self) -> builtins.str:
        '''Resource name of the SecretVersion. In format: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#version_name GoogleCloudbuildTrigger#version_name}

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
        return "GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55a6cd296ec140d209ae07e588790a0229b54c1721ced4c306db468233426ad4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0034b53a6e0bda4245265d623cc1dce3a15f7383299cd95352b419627c0abf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93275adaf8d00d3f06772eb7423d01a9e6b78bf67d04cba3c978b48a3d7caeea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a8e8ab556f07641c3d2038ef60a400d94a714f80bed3c9bc540d0a02bcfecb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15cc94fb1cb05a7bc36f7be246eb0e6b343ad469781b8eec3e8a5d27fb8873db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ff5df089e770b988298ea962f963673edbb253949a16cb378c34a6b9eb1ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1ca9fdc477835e46e3ff97130ec53be1e992336326595079dd0254160e228b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dbc4957a5ba90d30aa1be27361b79a5e5e1985eaf0475039a81df28282bc9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionName")
    def version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionName"))

    @version_name.setter
    def version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c68dc858e3237b1c985eb9a50f2f80c730177eea76ef9d3e287f1f1f67b2197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a060666f502f90ad84eed6c4bc31d7af3fc1f68a2612a409ddcf17cf32a3d62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildOptions",
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
class GoogleCloudbuildTriggerBuildOptions:
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
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildOptionsVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: Requested disk size for the VM that runs the build. Note that this is NOT "disk free"; some of the space will be used by the operating system and build utilities. Also note that this is the minimum disk size that will be allocated for the build -- the build may run with a larger disk than requested. At present, the maximum disk size is 1000GB; builds that request more than the maximum are rejected with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#disk_size_gb GoogleCloudbuildTrigger#disk_size_gb}
        :param dynamic_substitutions: Option to specify whether or not to apply bash style string operations to the substitutions. NOTE this is always enabled for triggered builds and cannot be overridden in the build configuration file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dynamic_substitutions GoogleCloudbuildTrigger#dynamic_substitutions}
        :param env: A list of global environment variable definitions that will exist for all build steps in this build. If a variable is defined in both globally and in a build step, the variable will use the build step value. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        :param logging: Option to specify the logging mode, which determines if and where build logs are stored. Possible values: ["LOGGING_UNSPECIFIED", "LEGACY", "GCS_ONLY", "STACKDRIVER_ONLY", "CLOUD_LOGGING_ONLY", "NONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#logging GoogleCloudbuildTrigger#logging}
        :param log_streaming_option: Option to define build log streaming behavior to Google Cloud Storage. Possible values: ["STREAM_DEFAULT", "STREAM_ON", "STREAM_OFF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#log_streaming_option GoogleCloudbuildTrigger#log_streaming_option}
        :param machine_type: Compute Engine machine type on which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#machine_type GoogleCloudbuildTrigger#machine_type}
        :param requested_verify_option: Requested verifiability options. Possible values: ["NOT_VERIFIED", "VERIFIED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#requested_verify_option GoogleCloudbuildTrigger#requested_verify_option}
        :param secret_env: A list of global environment variables, which are encrypted using a Cloud Key Management Service crypto key. These values must be specified in the build's Secret. These variables will be available to all build steps in this build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
        :param source_provenance_hash: Requested hash for SourceProvenance. Possible values: ["NONE", "SHA256", "MD5"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source_provenance_hash GoogleCloudbuildTrigger#source_provenance_hash}
        :param substitution_option: Option to specify behavior when there is an error in the substitution checks. NOTE this is always set to ALLOW_LOOSE for triggered builds and cannot be overridden in the build configuration file. Possible values: ["MUST_MATCH", "ALLOW_LOOSE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitution_option GoogleCloudbuildTrigger#substitution_option}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#volumes GoogleCloudbuildTrigger#volumes}
        :param worker_pool: Option to specify a WorkerPool for the build. Format projects/{project}/workerPools/{workerPool}. This field is experimental. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#worker_pool GoogleCloudbuildTrigger#worker_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac39e564704fcf45006bcec93ec5ebc04d9328bc9c7c32fc2e54ff9f2b252188)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#disk_size_gb GoogleCloudbuildTrigger#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dynamic_substitutions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to specify whether or not to apply bash style string operations to the substitutions.

        NOTE this is always enabled for triggered builds and cannot be overridden in the build configuration file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dynamic_substitutions GoogleCloudbuildTrigger#dynamic_substitutions}
        '''
        result = self._values.get("dynamic_substitutions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of global environment variable definitions that will exist for all build steps in this build.

        If a variable is defined in both globally and in a build step,
        the variable will use the build step value.

        The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.str]:
        '''Option to specify the logging mode, which determines if and where build logs are stored.

        Possible values: ["LOGGING_UNSPECIFIED", "LEGACY", "GCS_ONLY", "STACKDRIVER_ONLY", "CLOUD_LOGGING_ONLY", "NONE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#logging GoogleCloudbuildTrigger#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_streaming_option(self) -> typing.Optional[builtins.str]:
        '''Option to define build log streaming behavior to Google Cloud Storage. Possible values: ["STREAM_DEFAULT", "STREAM_ON", "STREAM_OFF"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#log_streaming_option GoogleCloudbuildTrigger#log_streaming_option}
        '''
        result = self._values.get("log_streaming_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Compute Engine machine type on which to run the build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#machine_type GoogleCloudbuildTrigger#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requested_verify_option(self) -> typing.Optional[builtins.str]:
        '''Requested verifiability options. Possible values: ["NOT_VERIFIED", "VERIFIED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#requested_verify_option GoogleCloudbuildTrigger#requested_verify_option}
        '''
        result = self._values.get("requested_verify_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of global environment variables, which are encrypted using a Cloud Key Management Service crypto key.

        These values must be specified in the build's Secret. These variables
        will be available to all build steps in this build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
        '''
        result = self._values.get("secret_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_provenance_hash(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Requested hash for SourceProvenance. Possible values: ["NONE", "SHA256", "MD5"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source_provenance_hash GoogleCloudbuildTrigger#source_provenance_hash}
        '''
        result = self._values.get("source_provenance_hash")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def substitution_option(self) -> typing.Optional[builtins.str]:
        '''Option to specify behavior when there is an error in the substitution checks.

        NOTE this is always set to ALLOW_LOOSE for triggered builds and cannot be overridden
        in the build configuration file. Possible values: ["MUST_MATCH", "ALLOW_LOOSE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitution_option GoogleCloudbuildTrigger#substitution_option}
        '''
        result = self._values.get("substitution_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildOptionsVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#volumes GoogleCloudbuildTrigger#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildOptionsVolumes"]]], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Option to specify a WorkerPool for the build. Format projects/{project}/workerPools/{workerPool}.

        This field is experimental.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#worker_pool GoogleCloudbuildTrigger#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b4c8244b2c3154101608de9851ea0270125049be15b1164bf857c34c702d84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildOptionsVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bd1a9194c1a07c88a85d840a4eafe91cabcde8e588fb03243a8b9a487f7d76)
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
    def volumes(self) -> "GoogleCloudbuildTriggerBuildOptionsVolumesList":
        return typing.cast("GoogleCloudbuildTriggerBuildOptionsVolumesList", jsii.get(self, "volumes"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildOptionsVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildOptionsVolumes"]]], jsii.get(self, "volumesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6298847ec3e52cbb3d27c2ba940cb562e1e8c384423139ed896dad5358fb6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d17cc68ec65a38352c0cbbbba4ef361570317b19d4ad99f2b768d5dfced88db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicSubstitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c05b214a4905975cd441773fd75639d8f34ca06999f08630c55c2ce6e5bc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logging"))

    @logging.setter
    def logging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17f2fe82cbde6889570141e91fed49f1ce07a38ff5c6b4fbea98a982ff61d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamingOption")
    def log_streaming_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamingOption"))

    @log_streaming_option.setter
    def log_streaming_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57831bd8f86fcb849e85d1b913860fe6769ac3875075efe507781be9241bbcf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamingOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23246d9155c565edb16ae3d0eb003e2026e0869583224ab12c44a425a4a6891e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedVerifyOption")
    def requested_verify_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestedVerifyOption"))

    @requested_verify_option.setter
    def requested_verify_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db176da57f5798f114f7966ed5e47ff1ba90ab4984d5bde72b6f86aca003a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedVerifyOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretEnv")
    def secret_env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "secretEnv"))

    @secret_env.setter
    def secret_env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc960b2da8872de8ae4367dd576f62efe065a0419011d470d89349fc1ab3bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceProvenanceHash")
    def source_provenance_hash(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceProvenanceHash"))

    @source_provenance_hash.setter
    def source_provenance_hash(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12881fe6ce45db64aadfc3a3f781d1dfe59424a608f75007541fb8a3be01edb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceProvenanceHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutionOption")
    def substitution_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "substitutionOption"))

    @substitution_option.setter
    def substitution_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e949983de4fbb420bd7ba6f1ef24a2c0f923f24c745b53fa1d79915b01ffd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutionOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51a3a771f163fdf2f0755ea78e4b5e5b48adf2e7be3c339cebed87efd976e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerBuildOptions]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fad9251cf13c78cd5cf1a5fb1afb9efd382f9f32af9eacc2f2a75551e478e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildOptionsVolumes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class GoogleCloudbuildTriggerBuildOptionsVolumes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the volume to mount. Volume names must be unique per build step and must be valid names for Docker volumes. Each named volume must be used by at least two build steps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param path: Path at which to mount the volume. Paths must be absolute and cannot conflict with other volume paths on the same build step or with certain reserved volume paths. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e74f8bf678bfa4b56d20809a9c98f19ce6cd23a87982ee93121d8986623978a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path at which to mount the volume.

        Paths must be absolute and cannot conflict with other volume paths on the same
        build step or with certain reserved volume paths.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildOptionsVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildOptionsVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildOptionsVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a91ff9162b8d3dcb571a79701b97815baf1e06b8408885f8e9a8727e48e89ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildOptionsVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2deeff7ca226a1a5ffa255b63a0142422416193b123aea1b0ce93cb89a40ef3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildOptionsVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfef56b62046e4ba1b16960c0d55ba408fe91fedf1c75bcf8787b15bb30da6c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__110079901bce1467c5adbc3d81c7cad6168b0362662148c6d5d3fda7177a1c44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b832f1b63739087d99394a9800dd5b3566f2c2d56dd51f3301dd64425b1770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildOptionsVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildOptionsVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildOptionsVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb96a9a0db5eec621780cb687140bcaaee99b877bde500eed88e96dc3dd6469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildOptionsVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildOptionsVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8546256480817ef28153028dfcb5a67e11ba3cdc5002805650a4797d8efc9feb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dc682fb00786dde4376a4d28fda3aebe98c25dc95ff4c3c0cdd088978ae61c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca3c1152d8a7ed06f871b41dbc0dc43bd51ea6d72d39a1745bed27970190ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildOptionsVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildOptionsVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildOptionsVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e668642d71fdf27a27c6196918df0d42fb927999a0cbecc2376f196108424eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca8f34ccdbcacbc4e21e84f2b9b8da383a64918938cd52f52921e743d2fb9c00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArtifacts")
    def put_artifacts(
        self,
        *,
        images: typing.Optional[typing.Sequence[builtins.str]] = None,
        maven_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        npm_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
        objects: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildArtifactsObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        python_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsPythonPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param images: A list of images to be pushed upon the successful completion of all build steps. The images will be pushed using the builder service account's credentials. The digests of the pushed images will be stored in the Build resource's results field. If any of the images fail to be pushed, the build is marked FAILURE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#images GoogleCloudbuildTrigger#images}
        :param maven_artifacts: maven_artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#maven_artifacts GoogleCloudbuildTrigger#maven_artifacts}
        :param npm_packages: npm_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#npm_packages GoogleCloudbuildTrigger#npm_packages}
        :param objects: objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#objects GoogleCloudbuildTrigger#objects}
        :param python_packages: python_packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#python_packages GoogleCloudbuildTrigger#python_packages}
        '''
        value = GoogleCloudbuildTriggerBuildArtifacts(
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
        secret_manager: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param secret_manager: secret_manager block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_manager GoogleCloudbuildTrigger#secret_manager}
        '''
        value = GoogleCloudbuildTriggerBuildAvailableSecrets(
            secret_manager=secret_manager
        )

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
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildOptionsVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: Requested disk size for the VM that runs the build. Note that this is NOT "disk free"; some of the space will be used by the operating system and build utilities. Also note that this is the minimum disk size that will be allocated for the build -- the build may run with a larger disk than requested. At present, the maximum disk size is 1000GB; builds that request more than the maximum are rejected with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#disk_size_gb GoogleCloudbuildTrigger#disk_size_gb}
        :param dynamic_substitutions: Option to specify whether or not to apply bash style string operations to the substitutions. NOTE this is always enabled for triggered builds and cannot be overridden in the build configuration file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dynamic_substitutions GoogleCloudbuildTrigger#dynamic_substitutions}
        :param env: A list of global environment variable definitions that will exist for all build steps in this build. If a variable is defined in both globally and in a build step, the variable will use the build step value. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        :param logging: Option to specify the logging mode, which determines if and where build logs are stored. Possible values: ["LOGGING_UNSPECIFIED", "LEGACY", "GCS_ONLY", "STACKDRIVER_ONLY", "CLOUD_LOGGING_ONLY", "NONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#logging GoogleCloudbuildTrigger#logging}
        :param log_streaming_option: Option to define build log streaming behavior to Google Cloud Storage. Possible values: ["STREAM_DEFAULT", "STREAM_ON", "STREAM_OFF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#log_streaming_option GoogleCloudbuildTrigger#log_streaming_option}
        :param machine_type: Compute Engine machine type on which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#machine_type GoogleCloudbuildTrigger#machine_type}
        :param requested_verify_option: Requested verifiability options. Possible values: ["NOT_VERIFIED", "VERIFIED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#requested_verify_option GoogleCloudbuildTrigger#requested_verify_option}
        :param secret_env: A list of global environment variables, which are encrypted using a Cloud Key Management Service crypto key. These values must be specified in the build's Secret. These variables will be available to all build steps in this build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
        :param source_provenance_hash: Requested hash for SourceProvenance. Possible values: ["NONE", "SHA256", "MD5"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source_provenance_hash GoogleCloudbuildTrigger#source_provenance_hash}
        :param substitution_option: Option to specify behavior when there is an error in the substitution checks. NOTE this is always set to ALLOW_LOOSE for triggered builds and cannot be overridden in the build configuration file. Possible values: ["MUST_MATCH", "ALLOW_LOOSE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitution_option GoogleCloudbuildTrigger#substitution_option}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#volumes GoogleCloudbuildTrigger#volumes}
        :param worker_pool: Option to specify a WorkerPool for the build. Format projects/{project}/workerPools/{workerPool}. This field is experimental. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#worker_pool GoogleCloudbuildTrigger#worker_pool}
        '''
        value = GoogleCloudbuildTriggerBuildOptions(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildSecret", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4597671facbd0c5a71353bec32e1ba0c4be5eef2138014379142068e26da1302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        repo_source: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_source GoogleCloudbuildTrigger#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#storage_source GoogleCloudbuildTrigger#storage_source}
        '''
        value = GoogleCloudbuildTriggerBuildSource(
            repo_source=repo_source, storage_source=storage_source
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putStep")
    def put_step(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildStep", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96960f914e4b9fb1579817e2fa8238309f17f87940564b729208b18e2f26475c)
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
    def artifacts(self) -> GoogleCloudbuildTriggerBuildArtifactsOutputReference:
        return typing.cast(GoogleCloudbuildTriggerBuildArtifactsOutputReference, jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="availableSecrets")
    def available_secrets(
        self,
    ) -> GoogleCloudbuildTriggerBuildAvailableSecretsOutputReference:
        return typing.cast(GoogleCloudbuildTriggerBuildAvailableSecretsOutputReference, jsii.get(self, "availableSecrets"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> GoogleCloudbuildTriggerBuildOptionsOutputReference:
        return typing.cast(GoogleCloudbuildTriggerBuildOptionsOutputReference, jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "GoogleCloudbuildTriggerBuildSecretList":
        return typing.cast("GoogleCloudbuildTriggerBuildSecretList", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "GoogleCloudbuildTriggerBuildSourceOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBuildSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="step")
    def step(self) -> "GoogleCloudbuildTriggerBuildStepList":
        return typing.cast("GoogleCloudbuildTriggerBuildStepList", jsii.get(self, "step"))

    @builtins.property
    @jsii.member(jsii_name="artifactsInput")
    def artifacts_input(self) -> typing.Optional[GoogleCloudbuildTriggerBuildArtifacts]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildArtifacts], jsii.get(self, "artifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="availableSecretsInput")
    def available_secrets_input(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildAvailableSecrets]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildAvailableSecrets], jsii.get(self, "availableSecretsInput"))

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
    def options_input(self) -> typing.Optional[GoogleCloudbuildTriggerBuildOptions]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildOptions], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueTtlInput")
    def queue_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildSecret"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildSecret"]]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["GoogleCloudbuildTriggerBuildSource"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="stepInput")
    def step_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStep"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStep"]]], jsii.get(self, "stepInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__378eb6d0bf4e2bf44013e1724bcd9db72f09ecdd0c3220a66d7d10390734ec9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "images", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logsBucket")
    def logs_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logsBucket"))

    @logs_bucket.setter
    def logs_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1997818173213a1c96d0335ca3156868bb91657b95c383c52a445dc6764a98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logsBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueTtl")
    def queue_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueTtl"))

    @queue_ttl.setter
    def queue_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09d535e18b178fd7e53e60502291c64d1b41232c7dffcaaf92b2de9815e5a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutions")
    def substitutions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitutions"))

    @substitutions.setter
    def substitutions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69523da307f42e8966b07782f60ea073846e3ba081432b70010846ff216c3509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72e2a21fe3bdeb24748075c19b509e5677649bf0504909b31dd53a649f75d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598b3a1e3a6a483c27971bc27ff018942bea9d0a0c94feb932e2a6f749aad4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerBuild]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuild],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b1c6dfdbc71a1697b1b71a7a197dc0796232be7a7e823014ad822f141d7277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSecret",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "secret_env": "secretEnv"},
)
class GoogleCloudbuildTriggerBuildSecret:
    def __init__(
        self,
        *,
        kms_key_name: builtins.str,
        secret_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param kms_key_name: Cloud KMS key name to use to decrypt these envs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#kms_key_name GoogleCloudbuildTrigger#kms_key_name}
        :param secret_env: Map of environment variable name to its encrypted value. Secret environment variables must be unique across all of a build's secrets, and must be used by at least one build step. Values can be at most 64 KB in size. There can be at most 100 secret values across all of a build's secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da97e109f5bc16f1f421db3a28874efc8e4354ede7e69369b0c107b1cedeba9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#kms_key_name GoogleCloudbuildTrigger#kms_key_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
        '''
        result = self._values.get("secret_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildSecretList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSecretList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6522ef376f22447a7921f9b841a128abeb67506108ad5ecf3aa86db4c6c11793)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildSecretOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c41b22bdffdc8ffd241ccd1e7262a20f4f38b2456b60876b247e2e4cd913e1d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildSecretOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374585a21b313091cb00b14b86c60cb14abd8d2246770ae5b3bb8d5939dc1066)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cd68f161f72951aa7a9d08a87a91773ee706942853fca6bc4b6cd42b0387c2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb6c3a010bb6eda2c8c7cb04a5f2595a60114e36188b3ce1ebcbb877d78219d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildSecret]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildSecret]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildSecret]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a9f38ae615bf1152e7bd924ef5162c4c6fa77d4896d5538b5239c85e1c1311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e109987e125ad278899cdea80a671603f974390349c2c72703247c1cb9b3b36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb56eb5e0c78cb45ae22f7dcf23aafdc33c9068eb628bef6adf885e61294c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretEnv")
    def secret_env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "secretEnv"))

    @secret_env.setter
    def secret_env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30420db1c01a29bd1fa1c6b5674060848f667e581a5be8ab73fe5f3fdd94036e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05f44c3a7d981e60f2b774ebf3dc748661b44ce4125155c9c4a5bf8c72e457f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSource",
    jsii_struct_bases=[],
    name_mapping={"repo_source": "repoSource", "storage_source": "storageSource"},
)
class GoogleCloudbuildTriggerBuildSource:
    def __init__(
        self,
        *,
        repo_source: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["GoogleCloudbuildTriggerBuildSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_source GoogleCloudbuildTrigger#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#storage_source GoogleCloudbuildTrigger#storage_source}
        '''
        if isinstance(repo_source, dict):
            repo_source = GoogleCloudbuildTriggerBuildSourceRepoSource(**repo_source)
        if isinstance(storage_source, dict):
            storage_source = GoogleCloudbuildTriggerBuildSourceStorageSource(**storage_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686afdd6442066d4e4da7047cf7eda50ecf186257da2d63b3c36455ba324b978)
            check_type(argname="argument repo_source", value=repo_source, expected_type=type_hints["repo_source"])
            check_type(argname="argument storage_source", value=storage_source, expected_type=type_hints["storage_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if repo_source is not None:
            self._values["repo_source"] = repo_source
        if storage_source is not None:
            self._values["storage_source"] = storage_source

    @builtins.property
    def repo_source(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBuildSourceRepoSource"]:
        '''repo_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_source GoogleCloudbuildTrigger#repo_source}
        '''
        result = self._values.get("repo_source")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildSourceRepoSource"], result)

    @builtins.property
    def storage_source(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBuildSourceStorageSource"]:
        '''storage_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#storage_source GoogleCloudbuildTrigger#storage_source}
        '''
        result = self._values.get("storage_source")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildSourceStorageSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b45917536a509ea0edc88344293785af6baf9b7dbe7824dd2f18d6b23f5c91ea)
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
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_name GoogleCloudbuildTrigger#repo_name}
        :param branch_name: Regex matching branches to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch_name GoogleCloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one a of branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#commit_sha GoogleCloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_id GoogleCloudbuildTrigger#project_id}
        :param substitutions: Substitutions to use in a triggered build. Should only be used with triggers.run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        :param tag_name: Regex matching tags to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag_name GoogleCloudbuildTrigger#tag_name}
        '''
        value = GoogleCloudbuildTriggerBuildSourceRepoSource(
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
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bucket GoogleCloudbuildTrigger#bucket}
        :param object: Google Cloud Storage object containing the source. This object must be a gzipped archive file (.tar.gz) containing source to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#object GoogleCloudbuildTrigger#object}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#generation GoogleCloudbuildTrigger#generation}
        '''
        value = GoogleCloudbuildTriggerBuildSourceStorageSource(
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
    def repo_source(
        self,
    ) -> "GoogleCloudbuildTriggerBuildSourceRepoSourceOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBuildSourceRepoSourceOutputReference", jsii.get(self, "repoSource"))

    @builtins.property
    @jsii.member(jsii_name="storageSource")
    def storage_source(
        self,
    ) -> "GoogleCloudbuildTriggerBuildSourceStorageSourceOutputReference":
        return typing.cast("GoogleCloudbuildTriggerBuildSourceStorageSourceOutputReference", jsii.get(self, "storageSource"))

    @builtins.property
    @jsii.member(jsii_name="repoSourceInput")
    def repo_source_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBuildSourceRepoSource"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildSourceRepoSource"], jsii.get(self, "repoSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSourceInput")
    def storage_source_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerBuildSourceStorageSource"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerBuildSourceStorageSource"], jsii.get(self, "storageSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerBuildSource]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c44079d4f11d7149da1c3bcd0a5bfd0518be7fec7a7ca3f689a3a143b032809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSourceRepoSource",
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
class GoogleCloudbuildTriggerBuildSourceRepoSource:
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
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_name GoogleCloudbuildTrigger#repo_name}
        :param branch_name: Regex matching branches to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch_name GoogleCloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one a of branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#commit_sha GoogleCloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_id GoogleCloudbuildTrigger#project_id}
        :param substitutions: Substitutions to use in a triggered build. Should only be used with triggers.run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        :param tag_name: Regex matching tags to build. Exactly one a of branch name, tag, or commit SHA must be provided. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag_name GoogleCloudbuildTrigger#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96334d07ffb9cb5bd493e362c3b97c4ad0095093db608fb597abc174b869e85)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_name GoogleCloudbuildTrigger#repo_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch_name GoogleCloudbuildTrigger#branch_name}
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''Explicit commit SHA to build. Exactly one a of branch name, tag, or commit SHA must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#commit_sha GoogleCloudbuildTrigger#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Directory, relative to the source root, in which to run the build.

        This must be a relative path. If a step's dir is specified and is an absolute path,
        this value is ignored for that step's execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger a build if the revision regex does NOT match the revision regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_id GoogleCloudbuildTrigger#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def substitutions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Substitutions to use in a triggered build. Should only be used with triggers.run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        '''
        result = self._values.get("substitutions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Regex matching tags to build.

        Exactly one a of branch name, tag, or commit SHA must be provided.
        The syntax of the regular expressions accepted is the syntax accepted by RE2 and
        described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag_name GoogleCloudbuildTrigger#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildSourceRepoSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildSourceRepoSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSourceRepoSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f2f917c36f3888d8c851b49de08194d74ccc11a4445237acce09120409fa47c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d89975f625cd500dbb5a1615abc1dd6c1d000eeef45135c0e9bb545e1443156e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29295b34e4f5a35f502daf9b5135641a17b030f99087e6fd2a1fab379e00cdd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5240383b67193ded7dbc8e64540adce606c03af90c9f158d9ae820bd1396e477)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c841462d3913ff8990c9a6fc8789031749b96a47a89f64ebd3760d595e6b7e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5b201046e121dc32530f1422ceb692953c718e0e1782828bb6052d152b75d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ba46af8fad3fe4e705b545d9f59f76ceecbf734327be37dd54173ee1b7fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="substitutions")
    def substitutions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "substitutions"))

    @substitutions.setter
    def substitutions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685e5a73654f75628f4907fdcb8218444aa575f21400da9c6b9e7ef4e3454395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substitutions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a8d1d0c0211960c078bb1aba8764cb414781b345a08e37436f28518a7f81c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildSourceRepoSource]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildSourceRepoSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildSourceRepoSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b094cf73f1b4162758f55812bb8c21b40e0f67d81b82310c227b244126b11004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSourceStorageSource",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleCloudbuildTriggerBuildSourceStorageSource:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bucket GoogleCloudbuildTrigger#bucket}
        :param object: Google Cloud Storage object containing the source. This object must be a gzipped archive file (.tar.gz) containing source to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#object GoogleCloudbuildTrigger#object}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#generation GoogleCloudbuildTrigger#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cb35e08dc9459fa5edb6c2d3520c95ddf3d5d5b91b0dcdc010eacfc9d26e29)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bucket GoogleCloudbuildTrigger#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Google Cloud Storage object containing the source. This object must be a gzipped archive file (.tar.gz) containing source to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#object GoogleCloudbuildTrigger#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#generation GoogleCloudbuildTrigger#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildSourceStorageSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildSourceStorageSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildSourceStorageSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa4073da998216861522ce87a764f29721f72f5036662d666f19cf45eb618013)
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
            type_hints = typing.get_type_hints(_typecheckingstub__250432fc45d164276a40359d8e50697a4f152abde00320c6467021e333b8ed54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e11b0df327f6f7fc0b2437241d8f147aa6f854cf728126a1db51b4788028a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae33c4d4257bdf9412b3a5713c53a192f4120a537fae15678058d37d7af6e597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBuildSourceStorageSource]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuildSourceStorageSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerBuildSourceStorageSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2bd29cea07472ca11355aa4393dfa3344ceaed19bef412301b23b556d092ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildStep",
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
class GoogleCloudbuildTriggerBuildStep:
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
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildStepVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the container image that will run this particular build step. If the image is available in the host's Docker daemon's cache, it will be run directly. If not, the host will attempt to pull the image first, using the builder service account's credentials if necessary. The Docker daemon's cache will already have the latest versions of all of the officially supported build steps (see https://github.com/GoogleCloudPlatform/cloud-builders for images and examples). The Docker daemon will also have cached many of the layers for some popular images, like "ubuntu", "debian", but they will be refreshed at the time you attempt to use them. If you built an image in a previous build step, it will be stored in the host's Docker daemon's cache and is available to use as the name for a later build step. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param allow_exit_codes: Allow this build step to fail without failing the entire build if and only if the exit code is one of the specified codes. If 'allowFailure' is also specified, this field will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#allow_exit_codes GoogleCloudbuildTrigger#allow_exit_codes}
        :param allow_failure: Allow this build step to fail without failing the entire build. If false, the entire build will fail if this step fails. Otherwise, the build will succeed, but this step will still have a failure status. Error information will be reported in the 'failureDetail' field. 'allowExitCodes' takes precedence over this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#allow_failure GoogleCloudbuildTrigger#allow_failure}
        :param args: A list of arguments that will be presented to the step when it is started. If the image used to run the step's container has an entrypoint, the args are used as arguments to that entrypoint. If the image does not define an entrypoint, the first element in args is used as the entrypoint, and the remainder will be used as arguments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#args GoogleCloudbuildTrigger#args}
        :param dir: Working directory to use when running this step's container. If this value is a relative path, it is relative to the build's working directory. If this value is absolute, it may be outside the build's working directory, in which case the contents of the path may not be persisted across build step executions, unless a 'volume' for that path is specified. If the build specifies a 'RepoSource' with 'dir' and a step with a 'dir', which specifies an absolute path, the 'RepoSource' 'dir' is ignored for the step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        :param entrypoint: Entrypoint to be used instead of the build step image's default entrypoint. If unset, the image's default entrypoint is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#entrypoint GoogleCloudbuildTrigger#entrypoint}
        :param env: A list of environment variable definitions to be used when running a step. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        :param id: Unique identifier for this build step, used in 'wait_for' to reference this build step as a dependency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#id GoogleCloudbuildTrigger#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param script: A shell script to be executed in the step. When script is provided, the user cannot specify the entrypoint or args. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#script GoogleCloudbuildTrigger#script}
        :param secret_env: A list of environment variables which are encrypted using a Cloud Key Management Service crypto key. These values must be specified in the build's 'Secret'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
        :param timeout: Time limit for executing this build step. If not defined, the step has no time limit and will be allowed to continue to run until either it completes or the build itself times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeout GoogleCloudbuildTrigger#timeout}
        :param timing: Output only. Stores timing information for executing this build step. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timing GoogleCloudbuildTrigger#timing}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#volumes GoogleCloudbuildTrigger#volumes}
        :param wait_for: The ID(s) of the step(s) that this build step depends on. This build step will not start until all the build steps in 'wait_for' have completed successfully. If 'wait_for' is empty, this build step will start when all previous build steps in the 'Build.Steps' list have completed successfully. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#wait_for GoogleCloudbuildTrigger#wait_for}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a5882e5783e8d59c26355e4264a745fcf664696f39922e0adb6939035b6158)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Allow this build step to fail without failing the entire build if and only if the exit code is one of the specified codes.

        If 'allowFailure' is also specified, this field will take precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#allow_exit_codes GoogleCloudbuildTrigger#allow_exit_codes}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#allow_failure GoogleCloudbuildTrigger#allow_failure}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#args GoogleCloudbuildTrigger#args}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''Entrypoint to be used instead of the build step image's default entrypoint. If unset, the image's default entrypoint is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#entrypoint GoogleCloudbuildTrigger#entrypoint}
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of environment variable definitions to be used when running a step.

        The elements are of the form "KEY=VALUE" for the environment variable
        "KEY" being given the value "VALUE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#env GoogleCloudbuildTrigger#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for this build step, used in 'wait_for' to reference this build step as a dependency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#id GoogleCloudbuildTrigger#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''A shell script to be executed in the step.

        When script is provided, the user cannot specify the entrypoint or args.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#script GoogleCloudbuildTrigger#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of environment variables which are encrypted using a Cloud Key Management Service crypto key.

        These values must be specified in
        the build's 'Secret'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret_env GoogleCloudbuildTrigger#secret_env}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeout GoogleCloudbuildTrigger#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timing(self) -> typing.Optional[builtins.str]:
        '''Output only. Stores timing information for executing this build step.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timing GoogleCloudbuildTrigger#timing}
        '''
        result = self._values.get("timing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStepVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#volumes GoogleCloudbuildTrigger#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStepVolumes"]]], result)

    @builtins.property
    def wait_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID(s) of the step(s) that this build step depends on.

        This build step will not start until all the build steps in 'wait_for'
        have completed successfully. If 'wait_for' is empty, this build step
        will start when all previous build steps in the 'Build.Steps' list
        have completed successfully.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#wait_for GoogleCloudbuildTrigger#wait_for}
        '''
        result = self._values.get("wait_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildStepList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildStepList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68ee51a55a085c0d6446d6a4cef47794715808e9ccfca19af5360d3972033802)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildStepOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ead7be91d90cca9c53a37b26574ad9b5ed5b5ca8ca747acea09223595a57d35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildStepOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8216aaaade147150e101197900644bef7e4e643361ed6c43f09fc3a78ac86e05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a94bcfb758d276e3bd756d389b06da520bb27a8d66f5632860e79e691fea6135)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3bf794a4494011a21b6c7943ce0c5ef5e167f004f60e119bee24f4c1b980ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStep]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStep]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStep]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a22a2d52fbb4260e6e1313b22afec1644ef2a7c0f17618f38999737b19e2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b90825de1ba56ebf27a5ab0786dd1682cc1dc0ced818f1dca19361913f38c99b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildTriggerBuildStepVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49835e55c852e390531eb8b8bd28b7b0b76acda3b499c33f8230c25608ef943)
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
    def volumes(self) -> "GoogleCloudbuildTriggerBuildStepVolumesList":
        return typing.cast("GoogleCloudbuildTriggerBuildStepVolumesList", jsii.get(self, "volumes"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStepVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildTriggerBuildStepVolumes"]]], jsii.get(self, "volumesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c119e917441af7d8238477cff96b5ecb2341e7a3e7d5a0960be6ceef08436d63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8112993125914b563433fd1285e68fbf87522097fca3a70d8e1811e48244f908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a16d3694f37a2e47e504b7d5a7f619bcf646dc25622c325e22acc206ed9b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2cc6327ee641990b4b600b8f8b422f317effeef5ec3b44f85661fc5013341a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entrypoint"))

    @entrypoint.setter
    def entrypoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf5f76a9b0e82a665cb93da5d6ee4220a5c23868329357d3f25a175f8796990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entrypoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa24758842f2b339c122ca35e5ebcf28a11b031271983be9c9e1e1901afbe2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa23e18879ee9554da09af3d8fe23c634709bc9511cc8e99837c64084ea5978c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cddbc37da3d392513ec3641dcb25c9ee55d2375244ded0d280e3cbf5ac33b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36093233a0ce7e5ecd4869c65705ae14bf2200db83610bb15db49dfbd571de58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretEnv")
    def secret_env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "secretEnv"))

    @secret_env.setter
    def secret_env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e2ddc0766b7ba453cebeb50260dd347a6d49aa92a34baa5e933dfd616c2f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5676a9c3655d18abe356e2347383ea32f7555dd7c1c30ba0a84312c949dc97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timing")
    def timing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timing"))

    @timing.setter
    def timing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76237d926ff8e7570735b2f5579034170ec203282f82ddda98ad2b5c2fcae70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitFor")
    def wait_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "waitFor"))

    @wait_for.setter
    def wait_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba0958f291293b4e27330762cc1df36338fa7dfd825b9206bf21fa817fa87a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitFor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStep]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStep]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStep]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fac8da5bf77974f9c141b7fa763a3f5a025303d847dbe91ba90aac574345f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildStepVolumes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class GoogleCloudbuildTriggerBuildStepVolumes:
    def __init__(self, *, name: builtins.str, path: builtins.str) -> None:
        '''
        :param name: Name of the volume to mount. Volume names must be unique per build step and must be valid names for Docker volumes. Each named volume must be used by at least two build steps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param path: Path at which to mount the volume. Paths must be absolute and cannot conflict with other volume paths on the same build step or with certain reserved volume paths. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1492c214aef87ceddc21c02d098a21fa52a9fec67679d4281013204cedf7c1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Path at which to mount the volume.

        Paths must be absolute and cannot conflict with other volume paths on
        the same build step or with certain reserved volume paths.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerBuildStepVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerBuildStepVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildStepVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ede88056726e0c50ab7d21f58b514f9c524c9e53a9cfb72eaca5cad37a0701)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildTriggerBuildStepVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ad239ce751eb1e77643673809157cc753aa75fc5e49a88a4fb4e852d0c60fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildTriggerBuildStepVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2033aaaf09fb2d68f91e3b38e177818bd0de3f3417be7175958412bb7fa80d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9fc2834809ea76b3932daea5733d5e3ac7c71197e491be01dc58ee19c2f7ddf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__addeaace2a9cf33c99577bc85ac5a996b472390f7bf89a3a3900849b57c5cdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStepVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStepVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStepVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3058d25f45450cdc514770e4624824474c6b7746244c6a84ede9d671a163356f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildTriggerBuildStepVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerBuildStepVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__274e4caf1bffa8ccde0ab2ad8d72867510bd1731d0772002d4ce0fab8ea65252)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc7fc81241ed8fc2d5edffe8f17231e0ff45f78a882b7d3f8254d48e9502430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d375b9fb846a2eba4b7962efe40fdcb7242f2a041b58c7bcc90dd8a266ad19be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStepVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStepVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStepVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de50844f2582a56e6b3ccdc58be5671677d460ad03f2108fcbddbb23886a104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerConfig",
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
class GoogleCloudbuildTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        approval_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerApprovalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_server_trigger_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerBitbucketServerTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        build_attribute: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuild, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        filter: typing.Optional[builtins.str] = None,
        git_file_source: typing.Optional[typing.Union["GoogleCloudbuildTriggerGitFileSource", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["GoogleCloudbuildTriggerGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_build_logs: typing.Optional[builtins.str] = None,
        included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pubsub_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerPubsubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        repository_event_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerRepositoryEventConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_to_build: typing.Optional[typing.Union["GoogleCloudbuildTriggerSourceToBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_template: typing.Optional[typing.Union["GoogleCloudbuildTriggerTriggerTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_config: typing.Optional[typing.Union["GoogleCloudbuildTriggerWebhookConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param approval_config: approval_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#approval_config GoogleCloudbuildTrigger#approval_config}
        :param bitbucket_server_trigger_config: bitbucket_server_trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_trigger_config GoogleCloudbuildTrigger#bitbucket_server_trigger_config}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#build GoogleCloudbuildTrigger#build}
        :param description: Human-readable description of the trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#description GoogleCloudbuildTrigger#description}
        :param disabled: Whether the trigger is disabled or not. If true, the trigger will never result in a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#disabled GoogleCloudbuildTrigger#disabled}
        :param filename: Path, from the source root, to a file whose contents is used for the template. Either a filename or build template must be provided. Set this only when using trigger_template or github. When using Pub/Sub, Webhook or Manual set the file name using git_file_source instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#filename GoogleCloudbuildTrigger#filename}
        :param filter: A Common Expression Language string. Used only with Pub/Sub and Webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#filter GoogleCloudbuildTrigger#filter}
        :param git_file_source: git_file_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#git_file_source GoogleCloudbuildTrigger#git_file_source}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github GoogleCloudbuildTrigger#github}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#id GoogleCloudbuildTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignored_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If ignoredFiles and changed files are both empty, then they are not used to determine whether or not to trigger a build. If ignoredFiles is not empty, then we ignore any files that match any of the ignored_file globs. If the change has no files that are outside of the ignoredFiles globs, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#ignored_files GoogleCloudbuildTrigger#ignored_files}
        :param include_build_logs: Build logs will be sent back to GitHub as part of the checkrun result. Values can be INCLUDE_BUILD_LOGS_UNSPECIFIED or INCLUDE_BUILD_LOGS_WITH_STATUS Possible values: ["INCLUDE_BUILD_LOGS_UNSPECIFIED", "INCLUDE_BUILD_LOGS_WITH_STATUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#include_build_logs GoogleCloudbuildTrigger#include_build_logs}
        :param included_files: ignoredFiles and includedFiles are file glob matches using https://golang.org/pkg/path/filepath/#Match extended with support for '**'. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is empty, then as far as this filter is concerned, we should trigger the build. If any of the files altered in the commit pass the ignoredFiles filter and includedFiles is not empty, then we make sure that at least one of those files matches a includedFiles glob. If not, then we do not trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#included_files GoogleCloudbuildTrigger#included_files}
        :param location: The `Cloud Build location <https://cloud.google.com/build/docs/locations>`_ for the trigger. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#location GoogleCloudbuildTrigger#location}
        :param name: Name of the trigger. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project GoogleCloudbuildTrigger#project}.
        :param pubsub_config: pubsub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pubsub_config GoogleCloudbuildTrigger#pubsub_config}
        :param repository_event_config: repository_event_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository_event_config GoogleCloudbuildTrigger#repository_event_config}
        :param service_account: The service account used for all user-controlled operations including triggers.patch, triggers.run, builds.create, and builds.cancel. If no service account is set, then the standard Cloud Build service account ([PROJECT_NUM]@system.gserviceaccount.com) will be used instead. Format: projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_ID_OR_EMAIL} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#service_account GoogleCloudbuildTrigger#service_account}
        :param source_to_build: source_to_build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source_to_build GoogleCloudbuildTrigger#source_to_build}
        :param substitutions: Substitutions data for Build resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        :param tags: Tags for annotation of a BuildTrigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tags GoogleCloudbuildTrigger#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeouts GoogleCloudbuildTrigger#timeouts}
        :param trigger_template: trigger_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#trigger_template GoogleCloudbuildTrigger#trigger_template}
        :param webhook_config: webhook_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#webhook_config GoogleCloudbuildTrigger#webhook_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(approval_config, dict):
            approval_config = GoogleCloudbuildTriggerApprovalConfig(**approval_config)
        if isinstance(bitbucket_server_trigger_config, dict):
            bitbucket_server_trigger_config = GoogleCloudbuildTriggerBitbucketServerTriggerConfig(**bitbucket_server_trigger_config)
        if isinstance(build_attribute, dict):
            build_attribute = GoogleCloudbuildTriggerBuild(**build_attribute)
        if isinstance(git_file_source, dict):
            git_file_source = GoogleCloudbuildTriggerGitFileSource(**git_file_source)
        if isinstance(github, dict):
            github = GoogleCloudbuildTriggerGithub(**github)
        if isinstance(pubsub_config, dict):
            pubsub_config = GoogleCloudbuildTriggerPubsubConfig(**pubsub_config)
        if isinstance(repository_event_config, dict):
            repository_event_config = GoogleCloudbuildTriggerRepositoryEventConfig(**repository_event_config)
        if isinstance(source_to_build, dict):
            source_to_build = GoogleCloudbuildTriggerSourceToBuild(**source_to_build)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudbuildTriggerTimeouts(**timeouts)
        if isinstance(trigger_template, dict):
            trigger_template = GoogleCloudbuildTriggerTriggerTemplate(**trigger_template)
        if isinstance(webhook_config, dict):
            webhook_config = GoogleCloudbuildTriggerWebhookConfig(**webhook_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc7ae934ff6b279c84bf79dd5c54f23506860b2ced887338c8142616354e657)
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
    def approval_config(self) -> typing.Optional[GoogleCloudbuildTriggerApprovalConfig]:
        '''approval_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#approval_config GoogleCloudbuildTrigger#approval_config}
        '''
        result = self._values.get("approval_config")
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerApprovalConfig], result)

    @builtins.property
    def bitbucket_server_trigger_config(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfig]:
        '''bitbucket_server_trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_trigger_config GoogleCloudbuildTrigger#bitbucket_server_trigger_config}
        '''
        result = self._values.get("bitbucket_server_trigger_config")
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfig], result)

    @builtins.property
    def build_attribute(self) -> typing.Optional[GoogleCloudbuildTriggerBuild]:
        '''build block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#build GoogleCloudbuildTrigger#build}
        '''
        result = self._values.get("build_attribute")
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerBuild], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human-readable description of the trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#description GoogleCloudbuildTrigger#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the trigger is disabled or not. If true, the trigger will never result in a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#disabled GoogleCloudbuildTrigger#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Path, from the source root, to a file whose contents is used for the template.

        Either a filename or build template must be provided. Set this only when using trigger_template or github.
        When using Pub/Sub, Webhook or Manual set the file name using git_file_source instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#filename GoogleCloudbuildTrigger#filename}
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A Common Expression Language string. Used only with Pub/Sub and Webhook.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#filter GoogleCloudbuildTrigger#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_file_source(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerGitFileSource"]:
        '''git_file_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#git_file_source GoogleCloudbuildTrigger#git_file_source}
        '''
        result = self._values.get("git_file_source")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGitFileSource"], result)

    @builtins.property
    def github(self) -> typing.Optional["GoogleCloudbuildTriggerGithub"]:
        '''github block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github GoogleCloudbuildTrigger#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGithub"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#id GoogleCloudbuildTrigger#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#ignored_files GoogleCloudbuildTrigger#ignored_files}
        '''
        result = self._values.get("ignored_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_build_logs(self) -> typing.Optional[builtins.str]:
        '''Build logs will be sent back to GitHub as part of the checkrun result.

        Values can be INCLUDE_BUILD_LOGS_UNSPECIFIED or
        INCLUDE_BUILD_LOGS_WITH_STATUS Possible values: ["INCLUDE_BUILD_LOGS_UNSPECIFIED", "INCLUDE_BUILD_LOGS_WITH_STATUS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#include_build_logs GoogleCloudbuildTrigger#include_build_logs}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#included_files GoogleCloudbuildTrigger#included_files}
        '''
        result = self._values.get("included_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The `Cloud Build location <https://cloud.google.com/build/docs/locations>`_ for the trigger. If not specified, "global" is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#location GoogleCloudbuildTrigger#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the trigger. Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project GoogleCloudbuildTrigger#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_config(self) -> typing.Optional["GoogleCloudbuildTriggerPubsubConfig"]:
        '''pubsub_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pubsub_config GoogleCloudbuildTrigger#pubsub_config}
        '''
        result = self._values.get("pubsub_config")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerPubsubConfig"], result)

    @builtins.property
    def repository_event_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfig"]:
        '''repository_event_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository_event_config GoogleCloudbuildTrigger#repository_event_config}
        '''
        result = self._values.get("repository_event_config")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfig"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for all user-controlled operations including triggers.patch, triggers.run, builds.create, and builds.cancel.

        If no service account is set, then the standard Cloud Build service account
        ([PROJECT_NUM]@system.gserviceaccount.com) will be used instead.

        Format: projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_ID_OR_EMAIL}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#service_account GoogleCloudbuildTrigger#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_to_build(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerSourceToBuild"]:
        '''source_to_build block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#source_to_build GoogleCloudbuildTrigger#source_to_build}
        '''
        result = self._values.get("source_to_build")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerSourceToBuild"], result)

    @builtins.property
    def substitutions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Substitutions data for Build resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#substitutions GoogleCloudbuildTrigger#substitutions}
        '''
        result = self._values.get("substitutions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags for annotation of a BuildTrigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tags GoogleCloudbuildTrigger#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudbuildTriggerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#timeouts GoogleCloudbuildTrigger#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerTimeouts"], result)

    @builtins.property
    def trigger_template(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerTriggerTemplate"]:
        '''trigger_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#trigger_template GoogleCloudbuildTrigger#trigger_template}
        '''
        result = self._values.get("trigger_template")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerTriggerTemplate"], result)

    @builtins.property
    def webhook_config(self) -> typing.Optional["GoogleCloudbuildTriggerWebhookConfig"]:
        '''webhook_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#webhook_config GoogleCloudbuildTrigger#webhook_config}
        '''
        result = self._values.get("webhook_config")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerWebhookConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGitFileSource",
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
class GoogleCloudbuildTriggerGitFileSource:
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
        :param path: The path of the file, with the repo root as the root of the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_type GoogleCloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config GoogleCloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github_enterprise_config GoogleCloudbuildTrigger#github_enterprise_config}
        :param repository: The fully qualified resource name of the Repo API repository. The fully qualified resource name of the Repo API repository. If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        :param revision: The branch, tag, arbitrary ref, or SHA version of the repo to use when resolving the filename (optional). This field respects the same syntax/resolution as described here: https://git-scm.com/docs/gitrevisions If unspecified, the revision from which the trigger invocation originated is assumed to be the revision from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#revision GoogleCloudbuildTrigger#revision}
        :param uri: The URI of the repo (optional). If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#uri GoogleCloudbuildTrigger#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620971bada7a8b771c285cc73370646f4877c037d1df3e9ca46067610dc95b59)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#path GoogleCloudbuildTrigger#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_type(self) -> builtins.str:
        '''The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_type GoogleCloudbuildTrigger#repo_type}
        '''
        result = self._values.get("repo_type")
        assert result is not None, "Required property 'repo_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bitbucket_server_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config GoogleCloudbuildTrigger#bitbucket_server_config}
        '''
        result = self._values.get("bitbucket_server_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_enterprise_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github_enterprise_config GoogleCloudbuildTrigger#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The fully qualified resource name of the Repo API repository.

        The fully qualified resource name of the Repo API repository.
        If unspecified, the repo from which the trigger invocation originated is assumed to be the repo from which to read the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''The branch, tag, arbitrary ref, or SHA version of the repo to use when resolving the filename (optional).

        This field respects the same syntax/resolution as described here: https://git-scm.com/docs/gitrevisions
        If unspecified, the revision from which the trigger invocation originated is assumed to be the revision from which to read the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#revision GoogleCloudbuildTrigger#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the repo (optional).

        If unspecified, the repo from which the trigger
        invocation originated is assumed to be the repo from which to read the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#uri GoogleCloudbuildTrigger#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerGitFileSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerGitFileSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGitFileSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__227aa0a89bc50af626c6f79bdc06642b618bd5144aba3b5ea1acaf51d816766b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8bcdd67a551cb8f81d7c53fee36f00a4802e4dd59e0b1c4fdb7d3161df8e7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitbucketServerConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubEnterpriseConfig"))

    @github_enterprise_config.setter
    def github_enterprise_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbaa2e81e73dbdcd582aeffb4322da0889d8db126acc1720ad9ea76800b65dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubEnterpriseConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae30307281c258134c0746c38038f5075bf1bf20ed0698d32784859f4269447c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5543c4d4dd7380d84ee4f872abac6c713176fd7ec23cb4470ef76137818a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoType")
    def repo_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoType"))

    @repo_type.setter
    def repo_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d2ff72f8ac3e09bb54d8b20d6f822beadf70c36456e917dea42dce7aedd1d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d948918cd57eaeb1fe220eb9cefffeb1147398d928e9e068841f4c86fdc5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11762be46f3a8233a1272b6562c3c5f249fb2228ee5ee4bae5dc667d0b053c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerGitFileSource]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerGitFileSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerGitFileSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565a8a97c4efba066fcca272767fe422a83dbce996303acfbf6b63be8dea0257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGithub",
    jsii_struct_bases=[],
    name_mapping={
        "enterprise_config_resource_name": "enterpriseConfigResourceName",
        "name": "name",
        "owner": "owner",
        "pull_request": "pullRequest",
        "push": "push",
    },
)
class GoogleCloudbuildTriggerGithub:
    def __init__(
        self,
        *,
        enterprise_config_resource_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        pull_request: typing.Optional[typing.Union["GoogleCloudbuildTriggerGithubPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["GoogleCloudbuildTriggerGithubPush", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enterprise_config_resource_name: The resource name of the github enterprise config that should be applied to this installation. For example: "projects/{$projectId}/locations/{$locationId}/githubEnterpriseConfigs/{$configId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#enterprise_config_resource_name GoogleCloudbuildTrigger#enterprise_config_resource_name}
        :param name: Name of the repository. For example: The name for https://github.com/googlecloudplatform/cloud-builders is "cloud-builders". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        :param owner: Owner of the repository. For example: The owner for https://github.com/googlecloudplatform/cloud-builders is "googlecloudplatform". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#owner GoogleCloudbuildTrigger#owner}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        if isinstance(pull_request, dict):
            pull_request = GoogleCloudbuildTriggerGithubPullRequest(**pull_request)
        if isinstance(push, dict):
            push = GoogleCloudbuildTriggerGithubPush(**push)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06eb966280749e1d431369e4346d691d511bf65f4c578fdaa3842d59a6a073f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#enterprise_config_resource_name GoogleCloudbuildTrigger#enterprise_config_resource_name}
        '''
        result = self._values.get("enterprise_config_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the repository. For example: The name for https://github.com/googlecloudplatform/cloud-builders is "cloud-builders".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#name GoogleCloudbuildTrigger#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Owner of the repository. For example: The owner for https://github.com/googlecloudplatform/cloud-builders is "googlecloudplatform".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#owner GoogleCloudbuildTrigger#owner}
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerGithubPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGithubPullRequest"], result)

    @builtins.property
    def push(self) -> typing.Optional["GoogleCloudbuildTriggerGithubPush"]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGithubPush"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8260a749f7749c5a0e738fdbdfe132699087fab452fa8bb7636d60c266ac0737)
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
        :param branch: Regex of branches to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param comment_control: Whether to block builds on a "/gcbrun" comment from a repository owner or collaborator. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        value = GoogleCloudbuildTriggerGithubPullRequest(
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
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        value = GoogleCloudbuildTriggerGithubPush(
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
    def pull_request(self) -> "GoogleCloudbuildTriggerGithubPullRequestOutputReference":
        return typing.cast("GoogleCloudbuildTriggerGithubPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(self) -> "GoogleCloudbuildTriggerGithubPushOutputReference":
        return typing.cast("GoogleCloudbuildTriggerGithubPushOutputReference", jsii.get(self, "push"))

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
    ) -> typing.Optional["GoogleCloudbuildTriggerGithubPullRequest"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGithubPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(self) -> typing.Optional["GoogleCloudbuildTriggerGithubPush"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerGithubPush"], jsii.get(self, "pushInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseConfigResourceName")
    def enterprise_config_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseConfigResourceName"))

    @enterprise_config_resource_name.setter
    def enterprise_config_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4cfcb5ced00454c19621504ad8e5539edee7c844add7b822577a88585d964f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseConfigResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2eeeba2a996f63c84b7aa626dd46695e0fd74056670e8576527f579d45a3594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9806af5fce30aa3337fe5212879e99522c30aef8b484e9a714f8552cfdc79b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerGithub]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerGithub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerGithub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4109ba4b755a7bcc3cfd4985c55920d5fb7bece4c9b44febcd35bd6d63a431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGithubPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "comment_control": "commentControl",
        "invert_regex": "invertRegex",
    },
)
class GoogleCloudbuildTriggerGithubPullRequest:
    def __init__(
        self,
        *,
        branch: builtins.str,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param comment_control: Whether to block builds on a "/gcbrun" comment from a repository owner or collaborator. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef9dafa2a3619955140cf9e6e51ca2404063b2b2daaef6905ef6baf513e1f5f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment_control(self) -> typing.Optional[builtins.str]:
        '''Whether to block builds on a "/gcbrun" comment from a repository owner or collaborator. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        '''
        result = self._values.get("comment_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, branches that do NOT match the git_ref will trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerGithubPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerGithubPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGithubPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0cf2041730e5c5238084edb7b046a2ae2c0c324cdfe6b2a3ee7091e752eaed0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc81e4fc783da30f5206770358a1c4dcaf4ab8d2be9486c14d72f1cca707e2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentControl")
    def comment_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commentControl"))

    @comment_control.setter
    def comment_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9655cc7b8c1a1ddd3f1871ad980f48b9ee33aac176feb53a1c7865faddd660a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b7bca5ef831f5dd85e7d477b8b180dbc0e484c7948747159a75b87e7125510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerGithubPullRequest]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerGithubPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerGithubPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580a43ab5c3a06b0f0b5baf6eb05511146c84ff044e5cafad1c9d2cbe6ca6cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGithubPush",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "invert_regex": "invertRegex", "tag": "tag"},
)
class GoogleCloudbuildTriggerGithubPush:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param invert_regex: When true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. Specify only one of branch or tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d13506b1bae74a6bde47d706c8698e8951e34f3985f13f0d367bb87813fec2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, only trigger a build if the revision regex does NOT match the git_ref regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Regex of tags to match.  Specify only one of branch or tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerGithubPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerGithubPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerGithubPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6cb801e31b7928d5dfdac0c0383ea0fdb85247e407eb2ae8df3584ba1e22bd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef7429519e42babacbe4de9d157715a4fbbec6ccb4b772f58d8adb75f5f3e162)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae1169f5ea69dfe319608d46af3b440e43b2bdd3138452af26340a9a8e1bba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352aa9ccef0f6188c1a8fa329da6c1931ca05822dea7b90d5ec54632b37889c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerGithubPush]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerGithubPush], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerGithubPush],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e77f0ee567da85be7d5cae351a7e0d524057f1738a625d61495f49d8484d8a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerPubsubConfig",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "service_account_email": "serviceAccountEmail"},
)
class GoogleCloudbuildTriggerPubsubConfig:
    def __init__(
        self,
        *,
        topic: builtins.str,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the topic from which this subscription is receiving messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#topic GoogleCloudbuildTrigger#topic}
        :param service_account_email: Service account that will make the push request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#service_account_email GoogleCloudbuildTrigger#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad423adee13af901d9b2e000208dbcdf30a59d1e6762c2cfb58ea4e4e35c98a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#topic GoogleCloudbuildTrigger#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''Service account that will make the push request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#service_account_email GoogleCloudbuildTrigger#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerPubsubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerPubsubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerPubsubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ee20761c2ec5bad0b41276cf412ce94854029f1a9ca218fe22833f9e2176051)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7733d6179f34f0e2ed7d55bc7bd02ef102206ad120462241ed6a2c904a1d2098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075d730733257e80e2ff054005826a059c22e362ca30c0a8201c09c3b5e12032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerPubsubConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerPubsubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerPubsubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1bb48f82fa9b9820e3c5634f5584df9542496dd5ec928c8021be276db689a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerRepositoryEventConfig",
    jsii_struct_bases=[],
    name_mapping={
        "pull_request": "pullRequest",
        "push": "push",
        "repository": "repository",
    },
)
class GoogleCloudbuildTriggerRepositoryEventConfig:
    def __init__(
        self,
        *,
        pull_request: typing.Optional[typing.Union["GoogleCloudbuildTriggerRepositoryEventConfigPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union["GoogleCloudbuildTriggerRepositoryEventConfigPush", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        :param repository: The resource name of the Repo API resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        if isinstance(pull_request, dict):
            pull_request = GoogleCloudbuildTriggerRepositoryEventConfigPullRequest(**pull_request)
        if isinstance(push, dict):
            push = GoogleCloudbuildTriggerRepositoryEventConfigPush(**push)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01cb76d163e73e58ab1ca3bec77c8d176920536d007b0a08b99ae137f6c90039)
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
    ) -> typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#pull_request GoogleCloudbuildTrigger#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPullRequest"], result)

    @builtins.property
    def push(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPush"]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#push GoogleCloudbuildTrigger#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPush"], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Repo API resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerRepositoryEventConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerRepositoryEventConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerRepositoryEventConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__716cd5403c85644199850c1c17c3fbf4c185aa536f5bdf1bbecd83184b4221df)
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
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment '/gcbrun'. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        value = GoogleCloudbuildTriggerRepositoryEventConfigPullRequest(
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
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param invert_regex: If true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        value = GoogleCloudbuildTriggerRepositoryEventConfigPush(
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
    ) -> "GoogleCloudbuildTriggerRepositoryEventConfigPullRequestOutputReference":
        return typing.cast("GoogleCloudbuildTriggerRepositoryEventConfigPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(self) -> "GoogleCloudbuildTriggerRepositoryEventConfigPushOutputReference":
        return typing.cast("GoogleCloudbuildTriggerRepositoryEventConfigPushOutputReference", jsii.get(self, "push"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestInput")
    def pull_request_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPullRequest"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPush"]:
        return typing.cast(typing.Optional["GoogleCloudbuildTriggerRepositoryEventConfigPush"], jsii.get(self, "pushInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__749880dc185db599f2de22ab1c5356751014999736619ab26245c29acdc0f225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097d5dd47ceb8fdd69897bdbc8ebbe6270fcc32982d2f57273f663d820a5c40d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerRepositoryEventConfigPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "comment_control": "commentControl",
        "invert_regex": "invertRegex",
    },
)
class GoogleCloudbuildTriggerRepositoryEventConfigPullRequest:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        comment_control: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param comment_control: Configure builds to run whether a repository owner or collaborator need to comment '/gcbrun'. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        :param invert_regex: If true, branches that do NOT match the git_ref will trigger a build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d97a54ab89cf71c943b124e825dd9dca99ac74acf0acc08d9389de3aa123ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment_control(self) -> typing.Optional[builtins.str]:
        '''Configure builds to run whether a repository owner or collaborator need to comment '/gcbrun'. Possible values: ["COMMENTS_DISABLED", "COMMENTS_ENABLED", "COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#comment_control GoogleCloudbuildTrigger#comment_control}
        '''
        result = self._values.get("comment_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, branches that do NOT match the git_ref will trigger a build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerRepositoryEventConfigPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerRepositoryEventConfigPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerRepositoryEventConfigPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0c0e3aa1ad266d2c59c0616b5c3789608b723cbf1e5461e1ddbe72fc13d8426)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4894d9b7e0abbb643cf64a480eee62cb477e94985f507673de43d49b6459bd21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentControl")
    def comment_control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commentControl"))

    @comment_control.setter
    def comment_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57a13af460cab17c605a7d4160cfd198cac63dbe575c983dc832195ecbc37fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afcaf8c63958858004268b94e6316741ed827f92d8c6ab18df1dae182b54a04e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPullRequest]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b93906aac1cb9164b63517ad1d9f0a718cfd3bfc92779fcccc898445db741e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerRepositoryEventConfigPush",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "invert_regex": "invertRegex", "tag": "tag"},
)
class GoogleCloudbuildTriggerRepositoryEventConfigPush:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: Regex of branches to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        :param invert_regex: If true, only trigger a build if the revision regex does NOT match the git_ref regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param tag: Regex of tags to match. The syntax of the regular expressions accepted is the syntax accepted by RE2 and described at https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2f897fedf8f1163864ac6f46522e19fe18b3df781caa5bc45db4183938a37c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch GoogleCloudbuildTrigger#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, only trigger a build if the revision regex does NOT match the git_ref regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Regex of tags to match.

        The syntax of the regular expressions accepted is the syntax accepted by
        RE2 and described at https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag GoogleCloudbuildTrigger#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerRepositoryEventConfigPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerRepositoryEventConfigPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerRepositoryEventConfigPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4ce761906e2bd333a711ec9ea5a40ef29dc21eac324d28d6a5f25b616c18c00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fea00d3732d1f5708a8b6af1f93e306c04696d36315d82f514a57a6feb7b7dc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87dab6b79f00fb6434c55a11977bd9aee5340b29c745011adf63b7efabd02fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2742f8c124a46ef0466b42db0e271f851b8835eae2f7b0b2f384ff744ab051b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPush]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPush], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPush],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b328ee97bfaa3904dfcd36489dd3f0e51f75eb5da15a03d0aa8869a70db58738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerSourceToBuild",
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
class GoogleCloudbuildTriggerSourceToBuild:
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
        :param ref: The branch or tag to use. Must start with "refs/" (required). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#ref GoogleCloudbuildTrigger#ref}
        :param repo_type: The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_type GoogleCloudbuildTrigger#repo_type}
        :param bitbucket_server_config: The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config GoogleCloudbuildTrigger#bitbucket_server_config}
        :param github_enterprise_config: The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github_enterprise_config GoogleCloudbuildTrigger#github_enterprise_config}
        :param repository: The qualified resource name of the Repo API repository. Either uri or repository can be specified and is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        :param uri: The URI of the repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#uri GoogleCloudbuildTrigger#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c46307ad54e21310817bcfce6e897d9a9e44a5c800bf0ebc51cf911c028da4d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#ref GoogleCloudbuildTrigger#ref}
        '''
        result = self._values.get("ref")
        assert result is not None, "Required property 'ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_type(self) -> builtins.str:
        '''The type of the repo, since it may not be explicit from the repo field (e.g from a URL). Values can be UNKNOWN, CLOUD_SOURCE_REPOSITORIES, GITHUB, BITBUCKET_SERVER Possible values: ["UNKNOWN", "CLOUD_SOURCE_REPOSITORIES", "GITHUB", "BITBUCKET_SERVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_type GoogleCloudbuildTrigger#repo_type}
        '''
        result = self._values.get("repo_type")
        assert result is not None, "Required property 'repo_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bitbucket_server_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the bitbucket server config. Format: projects/{project}/locations/{location}/bitbucketServerConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#bitbucket_server_config GoogleCloudbuildTrigger#bitbucket_server_config}
        '''
        result = self._values.get("bitbucket_server_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_enterprise_config(self) -> typing.Optional[builtins.str]:
        '''The full resource name of the github enterprise config. Format: projects/{project}/locations/{location}/githubEnterpriseConfigs/{id}. projects/{project}/githubEnterpriseConfigs/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#github_enterprise_config GoogleCloudbuildTrigger#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The qualified resource name of the Repo API repository. Either uri or repository can be specified and is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repository GoogleCloudbuildTrigger#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#uri GoogleCloudbuildTrigger#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerSourceToBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerSourceToBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerSourceToBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb6b9919c18b0a6cc6fb91b8b13bc8c79a7ff8427a85e8aa0b4d2e55a665edf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88bf52285c7115874bc444cfc33f465e5e1c103b113d1d686a3338f49878e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitbucketServerConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubEnterpriseConfig"))

    @github_enterprise_config.setter
    def github_enterprise_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4294265063eb0ce004af72e6cb744a0ad3a93c340935312323b25910bcfcbe4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubEnterpriseConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54730a178f5e531433b85fdfa022556cfe31ba0240e2678ab9362032b0e31582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759a83e71057ac694406c282cf30ec7dc5d6d279d4a606535e68ca18b5667675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoType")
    def repo_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoType"))

    @repo_type.setter
    def repo_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1f909f9f3d1e5d6ece31fff82e6c4bb1757e1e2fdf29a51d3fb2402506d099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a32777f7a9712257acb0d05bc62252dfbda9e81ea6e274b25cc762c6c0e6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerSourceToBuild]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerSourceToBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerSourceToBuild],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c014fd936e022291a37c649dadb717e03e3036843c0c91c7a7b8fddde6a01a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudbuildTriggerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#create GoogleCloudbuildTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#delete GoogleCloudbuildTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#update GoogleCloudbuildTrigger#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061a6626cb17091e0d8aad294dba6c1ff1b8faeaf65d63dd369d6ba6a31d4862)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#create GoogleCloudbuildTrigger#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#delete GoogleCloudbuildTrigger#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#update GoogleCloudbuildTrigger#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8a9b725f95705ae46b293d4e6273e5b67df7613413ecdd615a8ea9f5328cee9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e229fe8d0b8a04582646abc48c14ba430f6818a2a06ee78c7ac0fa045172f896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b8673364d0b64868beb3c25861e5ba0027bfb22358a32c4ee1daa823940e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45595d5c9622e3d34b9e9d8e1a3f789a64c8d05087686981161c4e8dbd0b9e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57b05d955813d987c12d75ff15f68f6e6f914a071e02250e6d86613d5004aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerTriggerTemplate",
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
class GoogleCloudbuildTriggerTriggerTemplate:
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
        :param branch_name: Name of the branch to build. Exactly one a of branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch_name GoogleCloudbuildTrigger#branch_name}
        :param commit_sha: Explicit commit SHA to build. Exactly one of a branch name, tag, or commit SHA must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#commit_sha GoogleCloudbuildTrigger#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. This must be a relative path. If a step's dir is specified and is an absolute path, this value is ignored for that step's execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_id GoogleCloudbuildTrigger#project_id}
        :param repo_name: Name of the Cloud Source Repository. If omitted, the name "default" is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_name GoogleCloudbuildTrigger#repo_name}
        :param tag_name: Name of the tag to build. Exactly one of a branch name, tag, or commit SHA must be provided. This field is a regular expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag_name GoogleCloudbuildTrigger#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f40fa513d480f05e95943e27f5d4872237a0bbe465e64d6b3bf6ba6df3e90a0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#branch_name GoogleCloudbuildTrigger#branch_name}
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''Explicit commit SHA to build. Exactly one of a branch name, tag, or commit SHA must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#commit_sha GoogleCloudbuildTrigger#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Directory, relative to the source root, in which to run the build.

        This must be a relative path. If a step's dir is specified and
        is an absolute path, this value is ignored for that step's
        execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#dir GoogleCloudbuildTrigger#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger a build if the revision regex does NOT match the revision regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#invert_regex GoogleCloudbuildTrigger#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#project_id GoogleCloudbuildTrigger#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Source Repository. If omitted, the name "default" is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#repo_name GoogleCloudbuildTrigger#repo_name}
        '''
        result = self._values.get("repo_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Name of the tag to build.

        Exactly one of a branch name, tag, or commit SHA must be provided.
        This field is a regular expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#tag_name GoogleCloudbuildTrigger#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerTriggerTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerTriggerTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerTriggerTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc9a930582db54540280793d64fb684f07def5a8adf9c9aeebaf564192fca92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61ecb32c8ae736a13f1bd5d4ccda52e3c7a4295021ecd625f3cc58b4a249c719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5d2d37b9da37ec4001c76b550a652ef963da4d23b530998ab9de18a749521a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8738364f9e0e73eb6acf1c90580befbf72b7bcf51dbf53db987e6e6f749b7a39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1474b6f1a584fe57ced7da3a57a7867d4378a7133724c51a4d823b2d6908db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c92bd083c2a0d239e941757f0f911c053ba291a22fd818a4f15c1c28dd1c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dded37aae367a07938cad959b44857180beee7ff314ff15196657944de74a0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc87a4474874992a36c2f635d2a21f1eaa21da9f8c715cc5ea0d773431207df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerTriggerTemplate]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerTriggerTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerTriggerTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13614c7401877df88455fc37ba71be1c8bc6993448e4720b99737a593f11952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerWebhookConfig",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class GoogleCloudbuildTriggerWebhookConfig:
    def __init__(self, *, secret: builtins.str) -> None:
        '''
        :param secret: Resource name for the secret required as a URL parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret GoogleCloudbuildTrigger#secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10102f58e4413dd3def0401f4f9b81955a879b9bdec4d6b66217c735822eca6b)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> builtins.str:
        '''Resource name for the secret required as a URL parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_trigger#secret GoogleCloudbuildTrigger#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildTriggerWebhookConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildTriggerWebhookConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildTrigger.GoogleCloudbuildTriggerWebhookConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__867d9895095296543d8b1b8bc7b1ba7bb6f536891b413b96fd1de55f2d23f31d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a33795e8a759228c11ad070d76387ecdea401db0086896c8171821124d7b2345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildTriggerWebhookConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildTriggerWebhookConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildTriggerWebhookConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34880e8412b293240fda98f8d13d46437faeb9abe87b05b3b809dafd598889b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudbuildTrigger",
    "GoogleCloudbuildTriggerApprovalConfig",
    "GoogleCloudbuildTriggerApprovalConfigOutputReference",
    "GoogleCloudbuildTriggerBitbucketServerTriggerConfig",
    "GoogleCloudbuildTriggerBitbucketServerTriggerConfigOutputReference",
    "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest",
    "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequestOutputReference",
    "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush",
    "GoogleCloudbuildTriggerBitbucketServerTriggerConfigPushOutputReference",
    "GoogleCloudbuildTriggerBuild",
    "GoogleCloudbuildTriggerBuildArtifacts",
    "GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts",
    "GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsList",
    "GoogleCloudbuildTriggerBuildArtifactsMavenArtifactsOutputReference",
    "GoogleCloudbuildTriggerBuildArtifactsNpmPackages",
    "GoogleCloudbuildTriggerBuildArtifactsNpmPackagesList",
    "GoogleCloudbuildTriggerBuildArtifactsNpmPackagesOutputReference",
    "GoogleCloudbuildTriggerBuildArtifactsObjects",
    "GoogleCloudbuildTriggerBuildArtifactsObjectsOutputReference",
    "GoogleCloudbuildTriggerBuildArtifactsObjectsTiming",
    "GoogleCloudbuildTriggerBuildArtifactsObjectsTimingList",
    "GoogleCloudbuildTriggerBuildArtifactsObjectsTimingOutputReference",
    "GoogleCloudbuildTriggerBuildArtifactsOutputReference",
    "GoogleCloudbuildTriggerBuildArtifactsPythonPackages",
    "GoogleCloudbuildTriggerBuildArtifactsPythonPackagesList",
    "GoogleCloudbuildTriggerBuildArtifactsPythonPackagesOutputReference",
    "GoogleCloudbuildTriggerBuildAvailableSecrets",
    "GoogleCloudbuildTriggerBuildAvailableSecretsOutputReference",
    "GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager",
    "GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerList",
    "GoogleCloudbuildTriggerBuildAvailableSecretsSecretManagerOutputReference",
    "GoogleCloudbuildTriggerBuildOptions",
    "GoogleCloudbuildTriggerBuildOptionsOutputReference",
    "GoogleCloudbuildTriggerBuildOptionsVolumes",
    "GoogleCloudbuildTriggerBuildOptionsVolumesList",
    "GoogleCloudbuildTriggerBuildOptionsVolumesOutputReference",
    "GoogleCloudbuildTriggerBuildOutputReference",
    "GoogleCloudbuildTriggerBuildSecret",
    "GoogleCloudbuildTriggerBuildSecretList",
    "GoogleCloudbuildTriggerBuildSecretOutputReference",
    "GoogleCloudbuildTriggerBuildSource",
    "GoogleCloudbuildTriggerBuildSourceOutputReference",
    "GoogleCloudbuildTriggerBuildSourceRepoSource",
    "GoogleCloudbuildTriggerBuildSourceRepoSourceOutputReference",
    "GoogleCloudbuildTriggerBuildSourceStorageSource",
    "GoogleCloudbuildTriggerBuildSourceStorageSourceOutputReference",
    "GoogleCloudbuildTriggerBuildStep",
    "GoogleCloudbuildTriggerBuildStepList",
    "GoogleCloudbuildTriggerBuildStepOutputReference",
    "GoogleCloudbuildTriggerBuildStepVolumes",
    "GoogleCloudbuildTriggerBuildStepVolumesList",
    "GoogleCloudbuildTriggerBuildStepVolumesOutputReference",
    "GoogleCloudbuildTriggerConfig",
    "GoogleCloudbuildTriggerGitFileSource",
    "GoogleCloudbuildTriggerGitFileSourceOutputReference",
    "GoogleCloudbuildTriggerGithub",
    "GoogleCloudbuildTriggerGithubOutputReference",
    "GoogleCloudbuildTriggerGithubPullRequest",
    "GoogleCloudbuildTriggerGithubPullRequestOutputReference",
    "GoogleCloudbuildTriggerGithubPush",
    "GoogleCloudbuildTriggerGithubPushOutputReference",
    "GoogleCloudbuildTriggerPubsubConfig",
    "GoogleCloudbuildTriggerPubsubConfigOutputReference",
    "GoogleCloudbuildTriggerRepositoryEventConfig",
    "GoogleCloudbuildTriggerRepositoryEventConfigOutputReference",
    "GoogleCloudbuildTriggerRepositoryEventConfigPullRequest",
    "GoogleCloudbuildTriggerRepositoryEventConfigPullRequestOutputReference",
    "GoogleCloudbuildTriggerRepositoryEventConfigPush",
    "GoogleCloudbuildTriggerRepositoryEventConfigPushOutputReference",
    "GoogleCloudbuildTriggerSourceToBuild",
    "GoogleCloudbuildTriggerSourceToBuildOutputReference",
    "GoogleCloudbuildTriggerTimeouts",
    "GoogleCloudbuildTriggerTimeoutsOutputReference",
    "GoogleCloudbuildTriggerTriggerTemplate",
    "GoogleCloudbuildTriggerTriggerTemplateOutputReference",
    "GoogleCloudbuildTriggerWebhookConfig",
    "GoogleCloudbuildTriggerWebhookConfigOutputReference",
]

publication.publish()

def _typecheckingstub__79dec4c8b91abe7df451c8a9ff02c42d93070b222a174785345da6681314891c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    approval_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerApprovalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_server_trigger_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerBitbucketServerTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    build_attribute: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filename: typing.Optional[builtins.str] = None,
    filter: typing.Optional[builtins.str] = None,
    git_file_source: typing.Optional[typing.Union[GoogleCloudbuildTriggerGitFileSource, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[GoogleCloudbuildTriggerGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_build_logs: typing.Optional[builtins.str] = None,
    included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pubsub_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerPubsubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_event_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerRepositoryEventConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    source_to_build: typing.Optional[typing.Union[GoogleCloudbuildTriggerSourceToBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_template: typing.Optional[typing.Union[GoogleCloudbuildTriggerTriggerTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerWebhookConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__070f1d3c370e3e3c9678a2402b1aa86f8ca2466ca67513f63cbd1aad053d1082(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2c25fd74f6825d1475845dc19d8e022062bd497052f6566f779cb0a8d0c12b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8af35c674795464f09f7aaffbf643171f32f20450a50eeb278ec7f2056c07a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71c958103c8d5e8f8b4156195eeaeb3f595c4d63352970a7a0576eeeb18b2cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277f5d893a13f4c391c6dcc2e99125be0b6326bc93b7446a032349426e605ada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755116e79189508780fdd5635d01f662d235c06102fea2b3e3976b65ad55b0e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575ab032dd6cbf4b8f721539f9e7c82c9d64c02b6193ce3cf99336cb5b45c450(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdeea4f9133576a8ad283e9deec649e7c395391442e5270addc6442634ef83f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ccde23af9c8934727afa043d45a7c563cdc7426d63baa69fcc6fbdd3d4ef5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e85eca937644417bac2543aed62b2e4b8cde7e063f08463abce7c8835a0e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6111c39b7a0c4c5a7341c6ff3b5a99af1c1b7b108fe6876459015d4176aafa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9e6f1b06c1adcb7eda28454d43cb7df1d530e839d51c5d84059b0d851d006a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa27b8a2cafc33c478de205423c1434d84f5cd749429f7b608c95f70fa7a92db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c02f26ba506dd8726fba2670cc2fb16d9897d66e8adcfafec28555cb4ade04(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc44e4ea5f33e375faec10a03ef28a1109e6a7f49b704e334492cf520ecd908(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846c39a89d2e83a47750cbe865ca7e726b9c5f420df72917694722f38fa54605(
    *,
    approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f48dd5e2d330334c767e678efcce3a5108f963461d4a4445c4cc15e8562112(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd08c6cb1d9ca9998436aafe3f40e63be5a69c7e03efe9659c9ece0448a4f6c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e731c4925a6da26a5298cf6249fe5d40da78158e31580f2c1ece483df4c4338(
    value: typing.Optional[GoogleCloudbuildTriggerApprovalConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16607d103f74ad141e007b065dcf13058da43382078ce031483ca69cef86b378(
    *,
    bitbucket_server_config_resource: builtins.str,
    project_key: builtins.str,
    repo_slug: builtins.str,
    pull_request: typing.Optional[typing.Union[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e6a6269b7ab19005f0436b48f37e3240f2b22c2a10763599a41001fa536a6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b803888d1c74d37b3099a023e2c62d7f1050372f64b616b05810a46c13a5374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1862cf61f16014dc63540d98932270e113ae24e43d7115d2b04253b84d52b7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b457e5b2af0756fa6149f73b55082ae882d6228a911d1b97b0641b401014fcc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b667e9d5afbeb542daa30dea99251894baf2d5213505c264c33f0a175124fc6(
    value: typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd491bb8d23824300563e9af0558c38ff2544321f30f08f5c7af90353e8fe12(
    *,
    branch: builtins.str,
    comment_control: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b7d6b61383b4651c15f4dc94ec50d58c388d67b396a9f2eccbb00a3d6c2a11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5333c4baf8e7fdd09ff68b061170a8b704891cca1e1f46bd9fad005fabbf92eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175c965aebdb179edb9aae5c6b7088568b52ee79cd365b29a40aee5388cce432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9318adc3caa83a55c917e085361709383c2c72c405728a9ab8e2d8806b185c4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e9c89721f6785b02594e451db41de39cc889105f0587da2b929c944ac3bd6c(
    value: typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5464cd118f240ed04c2190115285e98752fed9c93a305bb581e04a3d3caa48e(
    *,
    branch: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4879d370d4eee05f089a8ec7fb77c38007ae228568a5e5b950a40f3066c9123(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0590b4824659bff13abd0d9ab620c03e79fb8e7e2a2f4930a8a25ddecfffeeb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615fe75e4eaf9b054adb307666949c2f37016629f5f4168ca3d8af52ed71142e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21fa0be4e7584f079257c9019b598c2ae131e7108d25b18014107f0f182d720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f73cef6354fc84d9a7f70ba8e63f12e87a7d3d202a18d102d366aa53382c17c(
    value: typing.Optional[GoogleCloudbuildTriggerBitbucketServerTriggerConfigPush],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77058a7e80dbee84c84792703b9a447dd76b17b5713321109fff772a545654e6(
    *,
    step: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildStep, typing.Dict[builtins.str, typing.Any]]]],
    artifacts: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildArtifacts, typing.Dict[builtins.str, typing.Any]]] = None,
    available_secrets: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildAvailableSecrets, typing.Dict[builtins.str, typing.Any]]] = None,
    images: typing.Optional[typing.Sequence[builtins.str]] = None,
    logs_bucket: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    queue_ttl: typing.Optional[builtins.str] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildSource, typing.Dict[builtins.str, typing.Any]]] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0570c1678c20dcad77f4596ff00c3fd8867f6a7bb003f6694865ed9bed610b53(
    *,
    images: typing.Optional[typing.Sequence[builtins.str]] = None,
    maven_artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    npm_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    objects: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildArtifactsObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    python_packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsPythonPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c799a80064aa84878ed2ccb1b203e9b7839ac3b0125ed1068416da909421f1c5(
    *,
    artifact_id: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd9d6f9ead346d1d8d4b55cadf43b299a57390c507b5eadc4f0888ae22f6f6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5dbcdadd5a1a1a9fc9cd42df1f1ca02f66da559c7a82109719ee6dcf3476edf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a813fd27fb3391f11493825e10513bc0645181a5bb869bb4e025774ec82cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b24b9d7d931eed0d8c5883f5eebbe7e426685f9b63e15940f528d89e7e65bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1425563962e74f57fd34665b872fdc5a515177ad44464d7ea12ab76ab9a1e1f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbe15ebea15c633349200fcf382e388fceb8227d64b3eb9214ded3b392c11c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0726101ecb87d8c4f41b1b07adebce418c8d13afd7c458c1413ba578cbf434(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bbdde86000a559737177b428b52e6d7a26548d24a9c2f6e4af2fbe59406866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d3a4248a8081454ffd900452bf24623ec1418eda29f213470c11d9993f67f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002d432941e526988a29c76d0e1d393e199a0fad16fde020b6c03965bbe52e91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826f374be17852aeb2d70feb98be4e2aaede2053dc004f679067d7c6270d8780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f0386a44fce9e23ddc4038467f7985aad399723d6f01f33a869515e903edf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f2b4e54d8b1cf6333c614311e1195b7356c68e056b1897cf0d7b3aeb8859c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff45e44225193553091c29a44c71b104c8267ba18a0ef1479501dbd5a5cc393e(
    *,
    package_path: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed856e3fbea1088aec5f1502338ad2f5cd9c97fa729b85007f275ecb86cbac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4133d10e92379f33168fb4dbc856ce9914e851c1e6621d025dc02667560dc82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588c8d6512fe3180619ed79b91f2a083a842313e7c7439aad83591fb0383e9ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cad181ae6f8ec5f85f269ea4c2656170394708bd7c356d128b08e5d24f893f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c0751caa22d2aef3325eb383e34cafc8a2611049e94ec62b109cd6e8540594(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc40ce408d9e53a3d5a6831691b3c4f91cc190f6255af9958372449d671752ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsNpmPackages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1d8a035589c2966fb85d7d18043f952c56bcf6fbf7418b8cc9a0195d602de4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fe646051efdc2a23309f09c4848b18b92ba0345e455c0e27ce50432a03d81a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8482048d878e40de67fb952ca216653c7350af56897298e9c89bc81bf55c924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cbbc59a8f42b6f77c1f219cb2e249cc5e713a34cd9a536337ab8abf903d0c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsNpmPackages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9a1c05db32e8dedbdef887ff14d4629822451b63bf27f5c1596d5ed0d2c7e7(
    *,
    location: typing.Optional[builtins.str] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda1f5b96775dc044c03cedba389807ea171a14089763ede837320a9bac5f8ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a57d243e0562b241cd7ad21ad1901b062f2bbbecd20828b10517d40d115008d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0f4a38c7fbb32194fef87e67328c7a2f196c5b78760e3e95a16afcc36ee1f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38bb576792a1b9087be4fc335341e62e17133dc6bbace9ac0880ce2103f9ad0b(
    value: typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34427fde05941cb5a3c66ddcbdbe3917218391c79f62661fff7880d32dfc4d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f9d39c97f8ac7574605b6227dad03a81aa7a774a0bffdbc59b2602db57d51c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8147b4196e88b4d0d65d76bf4dcd3bfed247f680cb647fe75b4f0a5baeca667a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8b67d23beecb3ee912069b636848a65c8904f71241e2eb7c47a5881f6454cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b567f6ad3a144ae2edc59deb4821fd4d44f37bb15f79893fd70023ac13a6242f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cab724f8e6b2f146b2c4db7a1ec0d1691546d2e080b77abb7c0640623171790(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c61c0873f239298524bf96158ee26ec2360b76e1f25361630d91876963f2be(
    value: typing.Optional[GoogleCloudbuildTriggerBuildArtifactsObjectsTiming],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e500529e9e2e489f76af7de6b733fdcfc044ef47b5dbb663aa75395f21fac38c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0243bf6c4deac17289aa4c603fd08217f6819ed0e142e2b676a4b1f8888c60ad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsMavenArtifacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e1a5cde9dc44a22eae1903950efc8d6d839fcd3b89b7afe474f4f8384679d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsNpmPackages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bf724484f623c89ac0b65a17dced72fa4558ccba3d0244a4471e6167d6f94e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildArtifactsPythonPackages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918d203435d4f20694ed998c2d76adf5add1c50bebf31e16c94f99a9a7b9820e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aac08d9f6f73a8eb94f12b948a84c7aebf11ccaaae8c343c76c32555edd4631(
    value: typing.Optional[GoogleCloudbuildTriggerBuildArtifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c1c6ae08f384e60252d9b27dc5b2806e8c553edc24f6113be3a5df4105655f(
    *,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37085f8499941cfc867456f70af8c2dc776170de4489d8223b534a5206b1bfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d14da43dd77b8731a3383abc12dfb7ea6ca7303dce6b24c3ac12f7fef95f4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be582e2946e7d032dc245b4eca79345a8463c59d96d33df359ff9ec842d30b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a91a9c34a1f77c0cf38a57f5d4ceafe10d37cbd032e5d5e437fb1b4e9ff09f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e90ecd9a5d4faf30759f42410a6c79ebfe78dc28a0d9120024602e2b02e606(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6a39cadfd3fdc2862ebf37a4a4ba445d9abf71694c7faac576c6ab42338d22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildArtifactsPythonPackages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d82cdcef61ef3f4671b53199ece75e4631b53c491603d58f4db7e606b5a0eab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79f569965acca4b64d53e46fafd1c3d4f92a9eca3bf7e63e82f651d45ac1444(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33be15a1ea65d6b2e27ec5699741e93fc92a4fabcfa5f045c79bcce88332a32c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836c2f389046e5a78ce59b85e26a34bb7f98387f081da844a9f3279e718d8bd3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildArtifactsPythonPackages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794e2578215992257c9bbea92c88ba325368239d30fba749033f28d295031d96(
    *,
    secret_manager: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887a5c25ea1ef5c68170f832c0e3ba5b0b9c7387eb8e19017f5e696913c7307d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1593bd2282bccef7aaf925cb3a4867c7b88ab1eaae473589fa0cade68e6b9a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0531197abffa43798e651f214222eabd6b073da48096ccec8df7581433a779(
    value: typing.Optional[GoogleCloudbuildTriggerBuildAvailableSecrets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3036f7c31629509a182caf256b97a90f9d7dbd06d104eb46ca141fefc033b39f(
    *,
    env: builtins.str,
    version_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a6cd296ec140d209ae07e588790a0229b54c1721ced4c306db468233426ad4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0034b53a6e0bda4245265d623cc1dce3a15f7383299cd95352b419627c0abf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93275adaf8d00d3f06772eb7423d01a9e6b78bf67d04cba3c978b48a3d7caeea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8e8ab556f07641c3d2038ef60a400d94a714f80bed3c9bc540d0a02bcfecb7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cc94fb1cb05a7bc36f7be246eb0e6b343ad469781b8eec3e8a5d27fb8873db(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ff5df089e770b988298ea962f963673edbb253949a16cb378c34a6b9eb1ffc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1ca9fdc477835e46e3ff97130ec53be1e992336326595079dd0254160e228b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbc4957a5ba90d30aa1be27361b79a5e5e1985eaf0475039a81df28282bc9e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c68dc858e3237b1c985eb9a50f2f80c730177eea76ef9d3e287f1f1f67b2197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a060666f502f90ad84eed6c4bc31d7af3fc1f68a2612a409ddcf17cf32a3d62f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildAvailableSecretsSecretManager]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac39e564704fcf45006bcec93ec5ebc04d9328bc9c7c32fc2e54ff9f2b252188(
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
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildOptionsVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b4c8244b2c3154101608de9851ea0270125049be15b1164bf857c34c702d84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bd1a9194c1a07c88a85d840a4eafe91cabcde8e588fb03243a8b9a487f7d76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildOptionsVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6298847ec3e52cbb3d27c2ba940cb562e1e8c384423139ed896dad5358fb6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17cc68ec65a38352c0cbbbba4ef361570317b19d4ad99f2b768d5dfced88db1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c05b214a4905975cd441773fd75639d8f34ca06999f08630c55c2ce6e5bc37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17f2fe82cbde6889570141e91fed49f1ce07a38ff5c6b4fbea98a982ff61d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57831bd8f86fcb849e85d1b913860fe6769ac3875075efe507781be9241bbcf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23246d9155c565edb16ae3d0eb003e2026e0869583224ab12c44a425a4a6891e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db176da57f5798f114f7966ed5e47ff1ba90ab4984d5bde72b6f86aca003a86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc960b2da8872de8ae4367dd576f62efe065a0419011d470d89349fc1ab3bba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12881fe6ce45db64aadfc3a3f781d1dfe59424a608f75007541fb8a3be01edb9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e949983de4fbb420bd7ba6f1ef24a2c0f923f24c745b53fa1d79915b01ffd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51a3a771f163fdf2f0755ea78e4b5e5b48adf2e7be3c339cebed87efd976e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fad9251cf13c78cd5cf1a5fb1afb9efd382f9f32af9eacc2f2a75551e478e49(
    value: typing.Optional[GoogleCloudbuildTriggerBuildOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e74f8bf678bfa4b56d20809a9c98f19ce6cd23a87982ee93121d8986623978a(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a91ff9162b8d3dcb571a79701b97815baf1e06b8408885f8e9a8727e48e89ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2deeff7ca226a1a5ffa255b63a0142422416193b123aea1b0ce93cb89a40ef3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfef56b62046e4ba1b16960c0d55ba408fe91fedf1c75bcf8787b15bb30da6c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110079901bce1467c5adbc3d81c7cad6168b0362662148c6d5d3fda7177a1c44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b832f1b63739087d99394a9800dd5b3566f2c2d56dd51f3301dd64425b1770(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb96a9a0db5eec621780cb687140bcaaee99b877bde500eed88e96dc3dd6469(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildOptionsVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8546256480817ef28153028dfcb5a67e11ba3cdc5002805650a4797d8efc9feb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc682fb00786dde4376a4d28fda3aebe98c25dc95ff4c3c0cdd088978ae61c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca3c1152d8a7ed06f871b41dbc0dc43bd51ea6d72d39a1745bed27970190ac1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e668642d71fdf27a27c6196918df0d42fb927999a0cbecc2376f196108424eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildOptionsVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8f34ccdbcacbc4e21e84f2b9b8da383a64918938cd52f52921e743d2fb9c00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4597671facbd0c5a71353bec32e1ba0c4be5eef2138014379142068e26da1302(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildSecret, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96960f914e4b9fb1579817e2fa8238309f17f87940564b729208b18e2f26475c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildStep, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378eb6d0bf4e2bf44013e1724bcd9db72f09ecdd0c3220a66d7d10390734ec9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1997818173213a1c96d0335ca3156868bb91657b95c383c52a445dc6764a98d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09d535e18b178fd7e53e60502291c64d1b41232c7dffcaaf92b2de9815e5a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69523da307f42e8966b07782f60ea073846e3ba081432b70010846ff216c3509(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72e2a21fe3bdeb24748075c19b509e5677649bf0504909b31dd53a649f75d1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598b3a1e3a6a483c27971bc27ff018942bea9d0a0c94feb932e2a6f749aad4f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b1c6dfdbc71a1697b1b71a7a197dc0796232be7a7e823014ad822f141d7277(
    value: typing.Optional[GoogleCloudbuildTriggerBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da97e109f5bc16f1f421db3a28874efc8e4354ede7e69369b0c107b1cedeba9(
    *,
    kms_key_name: builtins.str,
    secret_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6522ef376f22447a7921f9b841a128abeb67506108ad5ecf3aa86db4c6c11793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c41b22bdffdc8ffd241ccd1e7262a20f4f38b2456b60876b247e2e4cd913e1d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374585a21b313091cb00b14b86c60cb14abd8d2246770ae5b3bb8d5939dc1066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd68f161f72951aa7a9d08a87a91773ee706942853fca6bc4b6cd42b0387c2e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6c3a010bb6eda2c8c7cb04a5f2595a60114e36188b3ce1ebcbb877d78219d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a9f38ae615bf1152e7bd924ef5162c4c6fa77d4896d5538b5239c85e1c1311(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildSecret]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e109987e125ad278899cdea80a671603f974390349c2c72703247c1cb9b3b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb56eb5e0c78cb45ae22f7dcf23aafdc33c9068eb628bef6adf885e61294c81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30420db1c01a29bd1fa1c6b5674060848f667e581a5be8ab73fe5f3fdd94036e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05f44c3a7d981e60f2b774ebf3dc748661b44ce4125155c9c4a5bf8c72e457f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686afdd6442066d4e4da7047cf7eda50ecf186257da2d63b3c36455ba324b978(
    *,
    repo_source: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildSourceRepoSource, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_source: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuildSourceStorageSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45917536a509ea0edc88344293785af6baf9b7dbe7824dd2f18d6b23f5c91ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c44079d4f11d7149da1c3bcd0a5bfd0518be7fec7a7ca3f689a3a143b032809(
    value: typing.Optional[GoogleCloudbuildTriggerBuildSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96334d07ffb9cb5bd493e362c3b97c4ad0095093db608fb597abc174b869e85(
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

def _typecheckingstub__0f2f917c36f3888d8c851b49de08194d74ccc11a4445237acce09120409fa47c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89975f625cd500dbb5a1615abc1dd6c1d000eeef45135c0e9bb545e1443156e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29295b34e4f5a35f502daf9b5135641a17b030f99087e6fd2a1fab379e00cdd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5240383b67193ded7dbc8e64540adce606c03af90c9f158d9ae820bd1396e477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c841462d3913ff8990c9a6fc8789031749b96a47a89f64ebd3760d595e6b7e51(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5b201046e121dc32530f1422ceb692953c718e0e1782828bb6052d152b75d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ba46af8fad3fe4e705b545d9f59f76ceecbf734327be37dd54173ee1b7fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685e5a73654f75628f4907fdcb8218444aa575f21400da9c6b9e7ef4e3454395(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a8d1d0c0211960c078bb1aba8764cb414781b345a08e37436f28518a7f81c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b094cf73f1b4162758f55812bb8c21b40e0f67d81b82310c227b244126b11004(
    value: typing.Optional[GoogleCloudbuildTriggerBuildSourceRepoSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cb35e08dc9459fa5edb6c2d3520c95ddf3d5d5b91b0dcdc010eacfc9d26e29(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4073da998216861522ce87a764f29721f72f5036662d666f19cf45eb618013(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250432fc45d164276a40359d8e50697a4f152abde00320c6467021e333b8ed54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e11b0df327f6f7fc0b2437241d8f147aa6f854cf728126a1db51b4788028a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae33c4d4257bdf9412b3a5713c53a192f4120a537fae15678058d37d7af6e597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2bd29cea07472ca11355aa4393dfa3344ceaed19bef412301b23b556d092ac(
    value: typing.Optional[GoogleCloudbuildTriggerBuildSourceStorageSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a5882e5783e8d59c26355e4264a745fcf664696f39922e0adb6939035b6158(
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
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildStepVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait_for: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ee51a55a085c0d6446d6a4cef47794715808e9ccfca19af5360d3972033802(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ead7be91d90cca9c53a37b26574ad9b5ed5b5ca8ca747acea09223595a57d35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8216aaaade147150e101197900644bef7e4e643361ed6c43f09fc3a78ac86e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94bcfb758d276e3bd756d389b06da520bb27a8d66f5632860e79e691fea6135(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bf794a4494011a21b6c7943ce0c5ef5e167f004f60e119bee24f4c1b980ebc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a22a2d52fbb4260e6e1313b22afec1644ef2a7c0f17618f38999737b19e2bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStep]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90825de1ba56ebf27a5ab0786dd1682cc1dc0ced818f1dca19361913f38c99b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49835e55c852e390531eb8b8bd28b7b0b76acda3b499c33f8230c25608ef943(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildTriggerBuildStepVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c119e917441af7d8238477cff96b5ecb2341e7a3e7d5a0960be6ceef08436d63(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8112993125914b563433fd1285e68fbf87522097fca3a70d8e1811e48244f908(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a16d3694f37a2e47e504b7d5a7f619bcf646dc25622c325e22acc206ed9b0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2cc6327ee641990b4b600b8f8b422f317effeef5ec3b44f85661fc5013341a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf5f76a9b0e82a665cb93da5d6ee4220a5c23868329357d3f25a175f8796990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa24758842f2b339c122ca35e5ebcf28a11b031271983be9c9e1e1901afbe2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa23e18879ee9554da09af3d8fe23c634709bc9511cc8e99837c64084ea5978c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cddbc37da3d392513ec3641dcb25c9ee55d2375244ded0d280e3cbf5ac33b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36093233a0ce7e5ecd4869c65705ae14bf2200db83610bb15db49dfbd571de58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e2ddc0766b7ba453cebeb50260dd347a6d49aa92a34baa5e933dfd616c2f9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5676a9c3655d18abe356e2347383ea32f7555dd7c1c30ba0a84312c949dc97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76237d926ff8e7570735b2f5579034170ec203282f82ddda98ad2b5c2fcae70c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba0958f291293b4e27330762cc1df36338fa7dfd825b9206bf21fa817fa87a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fac8da5bf77974f9c141b7fa763a3f5a025303d847dbe91ba90aac574345f9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStep]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1492c214aef87ceddc21c02d098a21fa52a9fec67679d4281013204cedf7c1(
    *,
    name: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ede88056726e0c50ab7d21f58b514f9c524c9e53a9cfb72eaca5cad37a0701(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ad239ce751eb1e77643673809157cc753aa75fc5e49a88a4fb4e852d0c60fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2033aaaf09fb2d68f91e3b38e177818bd0de3f3417be7175958412bb7fa80d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fc2834809ea76b3932daea5733d5e3ac7c71197e491be01dc58ee19c2f7ddf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addeaace2a9cf33c99577bc85ac5a996b472390f7bf89a3a3900849b57c5cdc0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3058d25f45450cdc514770e4624824474c6b7746244c6a84ede9d671a163356f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildTriggerBuildStepVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274e4caf1bffa8ccde0ab2ad8d72867510bd1731d0772002d4ce0fab8ea65252(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc7fc81241ed8fc2d5edffe8f17231e0ff45f78a882b7d3f8254d48e9502430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d375b9fb846a2eba4b7962efe40fdcb7242f2a041b58c7bcc90dd8a266ad19be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de50844f2582a56e6b3ccdc58be5671677d460ad03f2108fcbddbb23886a104(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerBuildStepVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc7ae934ff6b279c84bf79dd5c54f23506860b2ced887338c8142616354e657(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    approval_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerApprovalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_server_trigger_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerBitbucketServerTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    build_attribute: typing.Optional[typing.Union[GoogleCloudbuildTriggerBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filename: typing.Optional[builtins.str] = None,
    filter: typing.Optional[builtins.str] = None,
    git_file_source: typing.Optional[typing.Union[GoogleCloudbuildTriggerGitFileSource, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[GoogleCloudbuildTriggerGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ignored_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_build_logs: typing.Optional[builtins.str] = None,
    included_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pubsub_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerPubsubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_event_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerRepositoryEventConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    source_to_build: typing.Optional[typing.Union[GoogleCloudbuildTriggerSourceToBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    substitutions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_template: typing.Optional[typing.Union[GoogleCloudbuildTriggerTriggerTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_config: typing.Optional[typing.Union[GoogleCloudbuildTriggerWebhookConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620971bada7a8b771c285cc73370646f4877c037d1df3e9ca46067610dc95b59(
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

def _typecheckingstub__227aa0a89bc50af626c6f79bdc06642b618bd5144aba3b5ea1acaf51d816766b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bcdd67a551cb8f81d7c53fee36f00a4802e4dd59e0b1c4fdb7d3161df8e7eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbaa2e81e73dbdcd582aeffb4322da0889d8db126acc1720ad9ea76800b65dfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae30307281c258134c0746c38038f5075bf1bf20ed0698d32784859f4269447c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5543c4d4dd7380d84ee4f872abac6c713176fd7ec23cb4470ef76137818a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d2ff72f8ac3e09bb54d8b20d6f822beadf70c36456e917dea42dce7aedd1d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d948918cd57eaeb1fe220eb9cefffeb1147398d928e9e068841f4c86fdc5d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11762be46f3a8233a1272b6562c3c5f249fb2228ee5ee4bae5dc667d0b053c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565a8a97c4efba066fcca272767fe422a83dbce996303acfbf6b63be8dea0257(
    value: typing.Optional[GoogleCloudbuildTriggerGitFileSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06eb966280749e1d431369e4346d691d511bf65f4c578fdaa3842d59a6a073f(
    *,
    enterprise_config_resource_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    pull_request: typing.Optional[typing.Union[GoogleCloudbuildTriggerGithubPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[GoogleCloudbuildTriggerGithubPush, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8260a749f7749c5a0e738fdbdfe132699087fab452fa8bb7636d60c266ac0737(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4cfcb5ced00454c19621504ad8e5539edee7c844add7b822577a88585d964f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2eeeba2a996f63c84b7aa626dd46695e0fd74056670e8576527f579d45a3594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9806af5fce30aa3337fe5212879e99522c30aef8b484e9a714f8552cfdc79b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4109ba4b755a7bcc3cfd4985c55920d5fb7bece4c9b44febcd35bd6d63a431(
    value: typing.Optional[GoogleCloudbuildTriggerGithub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef9dafa2a3619955140cf9e6e51ca2404063b2b2daaef6905ef6baf513e1f5f(
    *,
    branch: builtins.str,
    comment_control: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cf2041730e5c5238084edb7b046a2ae2c0c324cdfe6b2a3ee7091e752eaed0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc81e4fc783da30f5206770358a1c4dcaf4ab8d2be9486c14d72f1cca707e2b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9655cc7b8c1a1ddd3f1871ad980f48b9ee33aac176feb53a1c7865faddd660a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b7bca5ef831f5dd85e7d477b8b180dbc0e484c7948747159a75b87e7125510(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580a43ab5c3a06b0f0b5baf6eb05511146c84ff044e5cafad1c9d2cbe6ca6cad(
    value: typing.Optional[GoogleCloudbuildTriggerGithubPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d13506b1bae74a6bde47d706c8698e8951e34f3985f13f0d367bb87813fec2(
    *,
    branch: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cb801e31b7928d5dfdac0c0383ea0fdb85247e407eb2ae8df3584ba1e22bd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7429519e42babacbe4de9d157715a4fbbec6ccb4b772f58d8adb75f5f3e162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae1169f5ea69dfe319608d46af3b440e43b2bdd3138452af26340a9a8e1bba0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352aa9ccef0f6188c1a8fa329da6c1931ca05822dea7b90d5ec54632b37889c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e77f0ee567da85be7d5cae351a7e0d524057f1738a625d61495f49d8484d8a5(
    value: typing.Optional[GoogleCloudbuildTriggerGithubPush],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad423adee13af901d9b2e000208dbcdf30a59d1e6762c2cfb58ea4e4e35c98a(
    *,
    topic: builtins.str,
    service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee20761c2ec5bad0b41276cf412ce94854029f1a9ca218fe22833f9e2176051(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7733d6179f34f0e2ed7d55bc7bd02ef102206ad120462241ed6a2c904a1d2098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075d730733257e80e2ff054005826a059c22e362ca30c0a8201c09c3b5e12032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1bb48f82fa9b9820e3c5634f5584df9542496dd5ec928c8021be276db689a5(
    value: typing.Optional[GoogleCloudbuildTriggerPubsubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01cb76d163e73e58ab1ca3bec77c8d176920536d007b0a08b99ae137f6c90039(
    *,
    pull_request: typing.Optional[typing.Union[GoogleCloudbuildTriggerRepositoryEventConfigPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[GoogleCloudbuildTriggerRepositoryEventConfigPush, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716cd5403c85644199850c1c17c3fbf4c185aa536f5bdf1bbecd83184b4221df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749880dc185db599f2de22ab1c5356751014999736619ab26245c29acdc0f225(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097d5dd47ceb8fdd69897bdbc8ebbe6270fcc32982d2f57273f663d820a5c40d(
    value: typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d97a54ab89cf71c943b124e825dd9dca99ac74acf0acc08d9389de3aa123ee(
    *,
    branch: typing.Optional[builtins.str] = None,
    comment_control: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c0e3aa1ad266d2c59c0616b5c3789608b723cbf1e5461e1ddbe72fc13d8426(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4894d9b7e0abbb643cf64a480eee62cb477e94985f507673de43d49b6459bd21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57a13af460cab17c605a7d4160cfd198cac63dbe575c983dc832195ecbc37fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afcaf8c63958858004268b94e6316741ed827f92d8c6ab18df1dae182b54a04e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b93906aac1cb9164b63517ad1d9f0a718cfd3bfc92779fcccc898445db741e(
    value: typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2f897fedf8f1163864ac6f46522e19fe18b3df781caa5bc45db4183938a37c(
    *,
    branch: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ce761906e2bd333a711ec9ea5a40ef29dc21eac324d28d6a5f25b616c18c00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea00d3732d1f5708a8b6af1f93e306c04696d36315d82f514a57a6feb7b7dc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dab6b79f00fb6434c55a11977bd9aee5340b29c745011adf63b7efabd02fec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2742f8c124a46ef0466b42db0e271f851b8835eae2f7b0b2f384ff744ab051b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b328ee97bfaa3904dfcd36489dd3f0e51f75eb5da15a03d0aa8869a70db58738(
    value: typing.Optional[GoogleCloudbuildTriggerRepositoryEventConfigPush],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c46307ad54e21310817bcfce6e897d9a9e44a5c800bf0ebc51cf911c028da4d(
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

def _typecheckingstub__5bb6b9919c18b0a6cc6fb91b8b13bc8c79a7ff8427a85e8aa0b4d2e55a665edf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88bf52285c7115874bc444cfc33f465e5e1c103b113d1d686a3338f49878e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4294265063eb0ce004af72e6cb744a0ad3a93c340935312323b25910bcfcbe4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54730a178f5e531433b85fdfa022556cfe31ba0240e2678ab9362032b0e31582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759a83e71057ac694406c282cf30ec7dc5d6d279d4a606535e68ca18b5667675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1f909f9f3d1e5d6ece31fff82e6c4bb1757e1e2fdf29a51d3fb2402506d099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a32777f7a9712257acb0d05bc62252dfbda9e81ea6e274b25cc762c6c0e6d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c014fd936e022291a37c649dadb717e03e3036843c0c91c7a7b8fddde6a01a50(
    value: typing.Optional[GoogleCloudbuildTriggerSourceToBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061a6626cb17091e0d8aad294dba6c1ff1b8faeaf65d63dd369d6ba6a31d4862(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a9b725f95705ae46b293d4e6273e5b67df7613413ecdd615a8ea9f5328cee9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e229fe8d0b8a04582646abc48c14ba430f6818a2a06ee78c7ac0fa045172f896(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b8673364d0b64868beb3c25861e5ba0027bfb22358a32c4ee1daa823940e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45595d5c9622e3d34b9e9d8e1a3f789a64c8d05087686981161c4e8dbd0b9e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57b05d955813d987c12d75ff15f68f6e6f914a071e02250e6d86613d5004aa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildTriggerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f40fa513d480f05e95943e27f5d4872237a0bbe465e64d6b3bf6ba6df3e90a0(
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

def _typecheckingstub__0fc9a930582db54540280793d64fb684f07def5a8adf9c9aeebaf564192fca92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ecb32c8ae736a13f1bd5d4ccda52e3c7a4295021ecd625f3cc58b4a249c719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5d2d37b9da37ec4001c76b550a652ef963da4d23b530998ab9de18a749521a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8738364f9e0e73eb6acf1c90580befbf72b7bcf51dbf53db987e6e6f749b7a39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1474b6f1a584fe57ced7da3a57a7867d4378a7133724c51a4d823b2d6908db6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c92bd083c2a0d239e941757f0f911c053ba291a22fd818a4f15c1c28dd1c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dded37aae367a07938cad959b44857180beee7ff314ff15196657944de74a0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc87a4474874992a36c2f635d2a21f1eaa21da9f8c715cc5ea0d773431207df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13614c7401877df88455fc37ba71be1c8bc6993448e4720b99737a593f11952(
    value: typing.Optional[GoogleCloudbuildTriggerTriggerTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10102f58e4413dd3def0401f4f9b81955a879b9bdec4d6b66217c735822eca6b(
    *,
    secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867d9895095296543d8b1b8bc7b1ba7bb6f536891b413b96fd1de55f2d23f31d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33795e8a759228c11ad070d76387ecdea401db0086896c8171821124d7b2345(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34880e8412b293240fda98f8d13d46437faeb9abe87b05b3b809dafd598889b2(
    value: typing.Optional[GoogleCloudbuildTriggerWebhookConfig],
) -> None:
    """Type checking stubs"""
    pass
