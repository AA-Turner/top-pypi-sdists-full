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

from .. import (
    Component as _Component_2b0ad27f,
    Project as _Project_57d89203,
    YamlFile as _YamlFile_909731b0,
)


@jsii.enum(jsii_type="projen.gitlab.Action")
class Action(enum.Enum):
    '''(experimental) Specifies what this job will do.

    'start' (default) indicates the job will start the
    deployment. 'prepare' indicates this will not affect the deployment. 'stop' indicates
    this will stop the deployment.

    :stability: experimental
    '''

    PREPARE = "PREPARE"
    '''
    :stability: experimental
    '''
    START = "START"
    '''
    :stability: experimental
    '''
    STOP = "STOP"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.AllowFailure",
    jsii_struct_bases=[],
    name_mapping={"exit_codes": "exitCodes"},
)
class AllowFailure:
    def __init__(
        self,
        *,
        exit_codes: typing.Union[jsii.Number, typing.Sequence[jsii.Number]],
    ) -> None:
        '''(experimental) Exit code that are not considered failure.

        The job fails for any other exit code.
        You can list which exit codes are not considered failures. The job fails for any other
        exit code.

        :param exit_codes: 

        :see: https://docs.gitlab.com/ee/ci/yaml/#allow_failure
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f2c30cde1aebaa83de097243717ad8dd6d1c2617b47a4352cbe7e3f351e8b2)
            check_type(argname="argument exit_codes", value=exit_codes, expected_type=type_hints["exit_codes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exit_codes": exit_codes,
        }

    @builtins.property
    def exit_codes(self) -> typing.Union[jsii.Number, typing.List[jsii.Number]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("exit_codes")
        assert result is not None, "Required property 'exit_codes' is missing"
        return typing.cast(typing.Union[jsii.Number, typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AllowFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Artifacts",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "expire_in": "expireIn",
        "expose_as": "exposeAs",
        "name": "name",
        "paths": "paths",
        "reports": "reports",
        "untracked": "untracked",
        "when": "when",
    },
)
class Artifacts:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        expire_in: typing.Optional[builtins.str] = None,
        expose_as: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        reports: typing.Optional[typing.Union["Reports", typing.Dict[builtins.str, typing.Any]]] = None,
        untracked: typing.Optional[builtins.bool] = None,
        when: typing.Optional["CacheWhen"] = None,
    ) -> None:
        '''(experimental) Used to specify a list of files and directories that should be attached to the job if it succeeds.

        Artifacts are sent to Gitlab where they can be downloaded.

        :param exclude: (experimental) A list of paths to files/folders that should be excluded in the artifact.
        :param expire_in: (experimental) How long artifacts should be kept. They are saved 30 days by default. Artifacts that have expired are removed periodically via cron job. Supports a wide variety of formats, e.g. '1 week', '3 mins 4 sec', '2 hrs 20 min', '2h20min', '6 mos 1 day', '47 yrs 6 mos and 4d', '3 weeks and 2 days'.
        :param expose_as: (experimental) Can be used to expose job artifacts in the merge request UI. GitLab will add a link <expose_as> to the relevant merge request that points to the artifact.
        :param name: (experimental) Name for the archive created on job success. Can use variables in the name, e.g. '$CI_JOB_NAME'
        :param paths: (experimental) A list of paths to files/folders that should be included in the artifact.
        :param reports: (experimental) Reports will be uploaded as artifacts, and often displayed in the Gitlab UI, such as in Merge Requests.
        :param untracked: (experimental) Whether to add all untracked files (along with 'artifacts.paths') to the artifact.
        :param when: (experimental) Configure when artifacts are uploaded depended on job status.

        :see: https://docs.gitlab.com/ee/ci/yaml/#artifacts
        :stability: experimental
        '''
        if isinstance(reports, dict):
            reports = Reports(**reports)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d84c68910ff0d2af18be53491f5cbfd0be88648ace2dce10c35c510d498acc)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument expire_in", value=expire_in, expected_type=type_hints["expire_in"])
            check_type(argname="argument expose_as", value=expose_as, expected_type=type_hints["expose_as"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument reports", value=reports, expected_type=type_hints["reports"])
            check_type(argname="argument untracked", value=untracked, expected_type=type_hints["untracked"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if expire_in is not None:
            self._values["expire_in"] = expire_in
        if expose_as is not None:
            self._values["expose_as"] = expose_as
        if name is not None:
            self._values["name"] = name
        if paths is not None:
            self._values["paths"] = paths
        if reports is not None:
            self._values["reports"] = reports
        if untracked is not None:
            self._values["untracked"] = untracked
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to files/folders that should be excluded in the artifact.

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expire_in(self) -> typing.Optional[builtins.str]:
        '''(experimental) How long artifacts should be kept.

        They are saved 30 days by default. Artifacts that have expired are removed periodically via cron job. Supports a wide variety of formats, e.g. '1 week', '3 mins 4 sec', '2 hrs 20 min', '2h20min', '6 mos 1 day', '47 yrs 6 mos and 4d', '3 weeks and 2 days'.

        :stability: experimental
        '''
        result = self._values.get("expire_in")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expose_as(self) -> typing.Optional[builtins.str]:
        '''(experimental) Can be used to expose job artifacts in the merge request UI.

        GitLab will add a link <expose_as> to the relevant merge request that points to the artifact.

        :stability: experimental
        '''
        result = self._values.get("expose_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the archive created on job success.

        Can use variables in the name, e.g. '$CI_JOB_NAME'

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to files/folders that should be included in the artifact.

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reports(self) -> typing.Optional["Reports"]:
        '''(experimental) Reports will be uploaded as artifacts, and often displayed in the Gitlab UI, such as in Merge Requests.

        :stability: experimental
        '''
        result = self._values.get("reports")
        return typing.cast(typing.Optional["Reports"], result)

    @builtins.property
    def untracked(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add all untracked files (along with 'artifacts.paths') to the artifact.

        :stability: experimental
        '''
        result = self._values.get("untracked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def when(self) -> typing.Optional["CacheWhen"]:
        '''(experimental) Configure when artifacts are uploaded depended on job status.

        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["CacheWhen"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Artifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Assets",
    jsii_struct_bases=[],
    name_mapping={"links": "links"},
)
class Assets:
    def __init__(
        self,
        *,
        links: typing.Sequence[typing.Union["Link", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Asset configuration for a release.

        :param links: (experimental) Include asset links in the release.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad15c870fe49288bda1a98e1bfc9db5f862289de2ad5ad62e4c59ce4aab4c73)
            check_type(argname="argument links", value=links, expected_type=type_hints["links"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "links": links,
        }

    @builtins.property
    def links(self) -> typing.List["Link"]:
        '''(experimental) Include asset links in the release.

        :stability: experimental
        '''
        result = self._values.get("links")
        assert result is not None, "Required property 'links' is missing"
        return typing.cast(typing.List["Link"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Assets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Cache",
    jsii_struct_bases=[],
    name_mapping={
        "fallback_keys": "fallbackKeys",
        "key": "key",
        "paths": "paths",
        "policy": "policy",
        "untracked": "untracked",
        "when": "when",
    },
)
class Cache:
    def __init__(
        self,
        *,
        fallback_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[typing.Union[builtins.str, typing.Union["CacheKeyFiles", typing.Dict[builtins.str, typing.Any]]]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy: typing.Optional["CachePolicy"] = None,
        untracked: typing.Optional[builtins.bool] = None,
        when: typing.Optional["CacheWhen"] = None,
    ) -> None:
        '''(experimental) Cache Definition.

        :param fallback_keys: (experimental) Use cache:fallback_keys to specify a list of keys to try to restore cache from if there is no cache found for the cache:key. Caches are retrieved in the order specified in the fallback_keys section.
        :param key: (experimental) Used the to give each cache a unique identifying key. All jobs that use the same cache key use the same cache.
        :param paths: (experimental) Defines which files or directories to cache.
        :param policy: (experimental) Defines the upload and download behaviour of the cache.
        :param untracked: (experimental) If set to true all files that are untracked in your Git repository will be cached.
        :param when: (experimental) Defines when to save the cache, based on the status of the job (Default: Job Success).

        :see: https://docs.gitlab.com/ee/ci/yaml/#cache
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f049681df3dccf35653843c544e06258271520db12493e48ac936a96ecedad)
            check_type(argname="argument fallback_keys", value=fallback_keys, expected_type=type_hints["fallback_keys"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument untracked", value=untracked, expected_type=type_hints["untracked"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fallback_keys is not None:
            self._values["fallback_keys"] = fallback_keys
        if key is not None:
            self._values["key"] = key
        if paths is not None:
            self._values["paths"] = paths
        if policy is not None:
            self._values["policy"] = policy
        if untracked is not None:
            self._values["untracked"] = untracked
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def fallback_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Use cache:fallback_keys to specify a list of keys to try to restore cache from if there is no cache found for the cache:key.

        Caches are retrieved in the order specified in the fallback_keys section.

        :stability: experimental
        '''
        result = self._values.get("fallback_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key(self) -> typing.Optional[typing.Union[builtins.str, "CacheKeyFiles"]]:
        '''(experimental) Used the to give each cache a unique identifying key.

        All jobs that use the same cache key use the same cache.

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CacheKeyFiles"]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Defines which files or directories to cache.

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def policy(self) -> typing.Optional["CachePolicy"]:
        '''(experimental) Defines the upload and download behaviour of the cache.

        :stability: experimental
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional["CachePolicy"], result)

    @builtins.property
    def untracked(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to true all files that are untracked in your Git repository will be cached.

        :stability: experimental
        '''
        result = self._values.get("untracked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def when(self) -> typing.Optional["CacheWhen"]:
        '''(experimental) Defines when to save the cache, based on the status of the job (Default: Job Success).

        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["CacheWhen"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.CacheKeyFiles",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "prefix": "prefix"},
)
class CacheKeyFiles:
    def __init__(
        self,
        *,
        files: typing.Sequence[builtins.str],
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Use this construct to generate a new key when one or two specific files change.

        :param files: (experimental) The files that are checked against. If the SHA checksum changes, the cache becomes invalid.
        :param prefix: (experimental) Adds a custom prefix to the checksums computed.

        :see: https://docs.gitlab.com/ee/ci/yaml/#cachekeyfiles
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fa76bc1e2253fd95df81fb7b93982051b240cea93ead52d9d95535eeb6f760)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "files": files,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def files(self) -> typing.List[builtins.str]:
        '''(experimental) The files that are checked against.

        If the SHA checksum changes, the cache becomes invalid.

        :stability: experimental
        '''
        result = self._values.get("files")
        assert result is not None, "Required property 'files' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Adds a custom prefix to the checksums computed.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CacheKeyFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.CachePolicy")
class CachePolicy(enum.Enum):
    '''(experimental) Configure the upload and download behaviour of a cache.

    :see: https://docs.gitlab.com/ee/ci/yaml/#cachepolicy
    :stability: experimental
    '''

    PULL = "PULL"
    '''(experimental) Only download the cache when the job starts, but never upload changes when the job finishes.

    :stability: experimental
    '''
    PUSH = "PUSH"
    '''(experimental) Only upload a cache when the job finishes, but never download the cache when the job starts.

    :stability: experimental
    '''
    PULL_PUSH = "PULL_PUSH"
    '''(experimental) The job downloads the cache when the job starts, and uploads changes to the cache when the job ends.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.gitlab.CacheWhen")
class CacheWhen(enum.Enum):
    '''(experimental) Configure when artifacts are uploaded depended on job status.

    :see: https://docs.gitlab.com/ee/ci/yaml/#cachewhen
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) Upload artifacts regardless of job status.

    :stability: experimental
    '''
    ON_FAILURE = "ON_FAILURE"
    '''(experimental) Upload artifacts only when the job fails.

    :stability: experimental
    '''
    ON_SUCCESS = "ON_SUCCESS"
    '''(experimental) Upload artifacts only when the job succeeds (this is the default).

    :stability: experimental
    '''


class CiConfiguration(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.gitlab.CiConfiguration",
):
    '''(experimental) CI for GitLab.

    A CI is a configurable automated process made up of one or more stages/jobs.

    :see: https://docs.gitlab.com/ee/ci/yaml/
    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        name: builtins.str,
        *,
        default: typing.Optional[typing.Union["Default", typing.Dict[builtins.str, typing.Any]]] = None,
        jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union["Job", typing.Dict[builtins.str, typing.Any]]]] = None,
        pages: typing.Optional[typing.Union["Job", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow: typing.Optional[typing.Union["Workflow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param name: -
        :param default: (experimental) Default settings for the CI Configuration. Jobs that do not define one or more of the listed keywords use the value defined in the default section.
        :param jobs: (experimental) An initial set of jobs to add to the configuration.
        :param pages: (experimental) A special job used to upload static sites to Gitlab pages. Requires a ``public/`` directory with ``artifacts.path`` pointing to it.
        :param path: (experimental) The path of the file to generate.
        :param stages: (experimental) Groups jobs into stages. All jobs in one stage must complete before next stage is executed. If no stages are specified. Defaults to ['build', 'test', 'deploy'].
        :param variables: (experimental) Global variables that are passed to jobs. If the job already has that variable defined, the job-level variable takes precedence.
        :param workflow: (experimental) Used to control pipeline behavior.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231c30bc513f8e09e345dd63392e7c50f479df9f480fc36e03e88fc4a5e8cd68)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = CiConfigurationOptions(
            default=default,
            jobs=jobs,
            pages=pages,
            path=path,
            stages=stages,
            variables=variables,
            workflow=workflow,
        )

        jsii.create(self.__class__, self, [project, name, options])

    @jsii.member(jsii_name="addDefaultCaches")
    def add_default_caches(
        self,
        caches: typing.Sequence[typing.Union[Cache, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Adds up to 4 default caches configuration to the CI configuration.

        :param caches: Caches to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8dc83f6ed2c3927eac45893c863050843bdea6a919dceda0aeb811aab6b03a)
            check_type(argname="argument caches", value=caches, expected_type=type_hints["caches"])
        return typing.cast(None, jsii.invoke(self, "addDefaultCaches", [caches]))

    @jsii.member(jsii_name="addGlobalVariables")
    def add_global_variables(
        self,
        variables: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''(experimental) Add a globally defined variable to the CI configuration.

        :param variables: The variables to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a532b9d3becbdcec0a292538a067f3ddc6a037abdf523500485dc53041825c03)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast(None, jsii.invoke(self, "addGlobalVariables", [variables]))

    @jsii.member(jsii_name="addIncludes")
    def add_includes(self, *includes: "Include") -> None:
        '''(experimental) Add additional yml/yaml files to the CI includes.

        :param includes: The includes to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bca3189ad53bb4a2659a3c4be7c233788dfd0d6d0e32255e52d6e6d46261ebd)
            check_type(argname="argument includes", value=includes, expected_type=typing.Tuple[type_hints["includes"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addIncludes", [*includes]))

    @jsii.member(jsii_name="addJobs")
    def add_jobs(
        self,
        jobs: typing.Mapping[builtins.str, typing.Union["Job", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Add jobs and their stages to the CI configuration.

        :param jobs: Jobs to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f426ddc0c125aabe74a08ecc4ad008c2d2b5b44ef9240f0a0e99c04a9680ae18)
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
        return typing.cast(None, jsii.invoke(self, "addJobs", [jobs]))

    @jsii.member(jsii_name="addServices")
    def add_services(self, *services: "Service") -> None:
        '''(experimental) Add additional services.

        :param services: The services to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee886ab66358cc25f75eaff5dcbeba2e03d5f72db8d7d299360af81453428f9b)
            check_type(argname="argument services", value=services, expected_type=typing.Tuple[type_hints["services"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addServices", [*services]))

    @jsii.member(jsii_name="addStages")
    def add_stages(self, *stages: builtins.str) -> None:
        '''(experimental) Add stages to the CI configuration if not already present.

        :param stages: stages to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37256713bb8d361966f0b39f4dba8aac446f1eea7da27fabd8e9ea6833933c6)
            check_type(argname="argument stages", value=stages, expected_type=typing.Tuple[type_hints["stages"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStages", [*stages]))

    @builtins.property
    @jsii.member(jsii_name="defaultAfterScript")
    def default_after_script(self) -> typing.List[builtins.str]:
        '''(experimental) Defines default scripts that should run *after* all jobs.

        Can be overriden by the job level ``afterScript``.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultAfterScript"))

    @builtins.property
    @jsii.member(jsii_name="defaultBeforeScript")
    def default_before_script(self) -> typing.List[builtins.str]:
        '''(experimental) Defines default scripts that should run *before* all jobs.

        Can be overriden by the job level ``afterScript``.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultBeforeScript"))

    @builtins.property
    @jsii.member(jsii_name="defaultTags")
    def default_tags(self) -> typing.List[builtins.str]:
        '''(experimental) Used to select a specific runner from the list of all runners that are available for the project.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultTags"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _YamlFile_909731b0:
        '''(experimental) The workflow YAML file.

        :stability: experimental
        '''
        return typing.cast(_YamlFile_909731b0, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> typing.Mapping[builtins.str, "Job"]:
        '''(experimental) The jobs in the CI configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "Job"], jsii.get(self, "jobs"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) Path to CI file generated by the configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List[builtins.str]:
        '''(experimental) Groups jobs into stages.

        All jobs in one stage must complete before next stage is
        executed. Defaults to ['build', 'test', 'deploy'].

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, "VariableConfig"]]:
        '''(experimental) Global variables that are passed to jobs.

        If the job already has that variable defined, the job-level variable takes precedence.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, "VariableConfig"]], jsii.get(self, "variables"))

    @builtins.property
    @jsii.member(jsii_name="defaultArtifacts")
    def default_artifacts(self) -> typing.Optional[Artifacts]:
        '''(experimental) Default list of files and directories that should be attached to the job if it succeeds.

        Artifacts are sent to Gitlab where they can be downloaded.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[Artifacts], jsii.get(self, "defaultArtifacts"))

    @builtins.property
    @jsii.member(jsii_name="defaultCache")
    def default_cache(self) -> typing.Optional[typing.List[Cache]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[Cache]], jsii.get(self, "defaultCache"))

    @builtins.property
    @jsii.member(jsii_name="defaultIdTokens")
    def default_id_tokens(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "IDToken"]]:
        '''(experimental) Default ID tokens (JSON Web Tokens) that are used for CI/CD authentication to use globally for all jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "IDToken"]], jsii.get(self, "defaultIdTokens"))

    @builtins.property
    @jsii.member(jsii_name="defaultImage")
    def default_image(self) -> typing.Optional["Image"]:
        '''(experimental) Specifies the default docker image to use globally for all jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Image"], jsii.get(self, "defaultImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultInterruptible")
    def default_interruptible(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The default behavior for whether a job should be canceled when a newer pipeline starts before the job completes (Default: false).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "defaultInterruptible"))

    @builtins.property
    @jsii.member(jsii_name="defaultRetry")
    def default_retry(self) -> typing.Optional["Retry"]:
        '''(experimental) How many times a job is retried if it fails.

        If not defined, defaults to 0 and jobs do not retry.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Retry"], jsii.get(self, "defaultRetry"))

    @builtins.property
    @jsii.member(jsii_name="defaultTimeout")
    def default_timeout(self) -> typing.Optional[builtins.str]:
        '''(experimental) A default timeout job written in natural language (Ex.

        one hour, 3600 seconds, 60 minutes).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTimeout"))

    @builtins.property
    @jsii.member(jsii_name="pages")
    def pages(self) -> typing.Optional["Job"]:
        '''(experimental) A special job used to upload static sites to Gitlab pages.

        Requires a ``public/`` directory
        with ``artifacts.path`` pointing to it.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Job"], jsii.get(self, "pages"))

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> typing.Optional["Workflow"]:
        '''(experimental) Used to control pipeline behavior.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Workflow"], jsii.get(self, "workflow"))


@jsii.data_type(
    jsii_type="projen.gitlab.CiConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "default": "default",
        "jobs": "jobs",
        "pages": "pages",
        "path": "path",
        "stages": "stages",
        "variables": "variables",
        "workflow": "workflow",
    },
)
class CiConfigurationOptions:
    def __init__(
        self,
        *,
        default: typing.Optional[typing.Union["Default", typing.Dict[builtins.str, typing.Any]]] = None,
        jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union["Job", typing.Dict[builtins.str, typing.Any]]]] = None,
        pages: typing.Optional[typing.Union["Job", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow: typing.Optional[typing.Union["Workflow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``CiConfiguration``.

        :param default: (experimental) Default settings for the CI Configuration. Jobs that do not define one or more of the listed keywords use the value defined in the default section.
        :param jobs: (experimental) An initial set of jobs to add to the configuration.
        :param pages: (experimental) A special job used to upload static sites to Gitlab pages. Requires a ``public/`` directory with ``artifacts.path`` pointing to it.
        :param path: (experimental) The path of the file to generate.
        :param stages: (experimental) Groups jobs into stages. All jobs in one stage must complete before next stage is executed. If no stages are specified. Defaults to ['build', 'test', 'deploy'].
        :param variables: (experimental) Global variables that are passed to jobs. If the job already has that variable defined, the job-level variable takes precedence.
        :param workflow: (experimental) Used to control pipeline behavior.

        :stability: experimental
        '''
        if isinstance(default, dict):
            default = Default(**default)
        if isinstance(pages, dict):
            pages = Job(**pages)
        if isinstance(workflow, dict):
            workflow = Workflow(**workflow)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad6204d94421a2493e44c6131e44e9ac2175546be72d0e655df762520673c9e)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument pages", value=pages, expected_type=type_hints["pages"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default is not None:
            self._values["default"] = default
        if jobs is not None:
            self._values["jobs"] = jobs
        if pages is not None:
            self._values["pages"] = pages
        if path is not None:
            self._values["path"] = path
        if stages is not None:
            self._values["stages"] = stages
        if variables is not None:
            self._values["variables"] = variables
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def default(self) -> typing.Optional["Default"]:
        '''(experimental) Default settings for the CI Configuration.

        Jobs that do not define one or more of the listed keywords use the value defined in the default section.

        :stability: experimental
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional["Default"], result)

    @builtins.property
    def jobs(self) -> typing.Optional[typing.Mapping[builtins.str, "Job"]]:
        '''(experimental) An initial set of jobs to add to the configuration.

        :stability: experimental
        '''
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Job"]], result)

    @builtins.property
    def pages(self) -> typing.Optional["Job"]:
        '''(experimental) A special job used to upload static sites to Gitlab pages.

        Requires a ``public/`` directory
        with ``artifacts.path`` pointing to it.

        :stability: experimental
        '''
        result = self._values.get("pages")
        return typing.cast(typing.Optional["Job"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path of the file to generate.

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Groups jobs into stages.

        All jobs in one stage must complete before next stage is
        executed. If no stages are specified. Defaults to ['build', 'test', 'deploy'].

        :stability: experimental
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Global variables that are passed to jobs.

        If the job already has that variable defined, the job-level variable takes precedence.

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workflow(self) -> typing.Optional["Workflow"]:
        '''(experimental) Used to control pipeline behavior.

        :stability: experimental
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional["Workflow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CiConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.CoverageReport",
    jsii_struct_bases=[],
    name_mapping={"coverage_format": "coverageFormat", "path": "path"},
)
class CoverageReport:
    def __init__(self, *, coverage_format: builtins.str, path: builtins.str) -> None:
        '''(experimental) Code coverage report interface.

        :param coverage_format: 
        :param path: 

        :stability: experimental
        :link: https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html#artifactsreportscoverage_report
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fb846daac000cdcb6374acd70ebc7323f86761a31c2ebb2ef0d1b49a3f0652)
            check_type(argname="argument coverage_format", value=coverage_format, expected_type=type_hints["coverage_format"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "coverage_format": coverage_format,
            "path": path,
        }

    @builtins.property
    def coverage_format(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("coverage_format")
        assert result is not None, "Required property 'coverage_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoverageReport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Default",
    jsii_struct_bases=[],
    name_mapping={
        "after_script": "afterScript",
        "artifacts": "artifacts",
        "before_script": "beforeScript",
        "cache": "cache",
        "id_tokens": "idTokens",
        "image": "image",
        "interruptible": "interruptible",
        "retry": "retry",
        "services": "services",
        "tags": "tags",
        "timeout": "timeout",
    },
)
class Default:
    def __init__(
        self,
        *,
        after_script: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifacts: typing.Optional[typing.Union[Artifacts, typing.Dict[builtins.str, typing.Any]]] = None,
        before_script: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache: typing.Optional[typing.Sequence[typing.Union[Cache, typing.Dict[builtins.str, typing.Any]]]] = None,
        id_tokens: typing.Optional[typing.Mapping[builtins.str, "IDToken"]] = None,
        image: typing.Optional[typing.Union["Image", typing.Dict[builtins.str, typing.Any]]] = None,
        interruptible: typing.Optional[builtins.bool] = None,
        retry: typing.Optional[typing.Union["Retry", typing.Dict[builtins.str, typing.Any]]] = None,
        services: typing.Optional[typing.Sequence[typing.Union["Service", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Default settings for the CI Configuration.

        Jobs that do not define one or more of the listed keywords use the value defined in the default section.

        :param after_script: 
        :param artifacts: 
        :param before_script: 
        :param cache: 
        :param id_tokens: (experimental) Specifies the default ID tokens (JSON Web Tokens) that are used for CI/CD authentication to use globally for all jobs.
        :param image: 
        :param interruptible: 
        :param retry: 
        :param services: 
        :param tags: 
        :param timeout: 

        :see: https://docs.gitlab.com/ee/ci/yaml/#default
        :stability: experimental
        '''
        if isinstance(artifacts, dict):
            artifacts = Artifacts(**artifacts)
        if isinstance(image, dict):
            image = Image(**image)
        if isinstance(retry, dict):
            retry = Retry(**retry)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e71d01eda90297db6af675f51033414546212b06d49c00c218dee2071d1ed1)
            check_type(argname="argument after_script", value=after_script, expected_type=type_hints["after_script"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument before_script", value=before_script, expected_type=type_hints["before_script"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument id_tokens", value=id_tokens, expected_type=type_hints["id_tokens"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument interruptible", value=interruptible, expected_type=type_hints["interruptible"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if after_script is not None:
            self._values["after_script"] = after_script
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if before_script is not None:
            self._values["before_script"] = before_script
        if cache is not None:
            self._values["cache"] = cache
        if id_tokens is not None:
            self._values["id_tokens"] = id_tokens
        if image is not None:
            self._values["image"] = image
        if interruptible is not None:
            self._values["interruptible"] = interruptible
        if retry is not None:
            self._values["retry"] = retry
        if services is not None:
            self._values["services"] = services
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def after_script(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("after_script")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def artifacts(self) -> typing.Optional[Artifacts]:
        '''
        :stability: experimental
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[Artifacts], result)

    @builtins.property
    def before_script(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("before_script")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache(self) -> typing.Optional[typing.List[Cache]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[typing.List[Cache]], result)

    @builtins.property
    def id_tokens(self) -> typing.Optional[typing.Mapping[builtins.str, "IDToken"]]:
        '''(experimental) Specifies the default ID tokens (JSON Web Tokens) that are used for CI/CD authentication to use globally for all jobs.

        :stability: experimental
        '''
        result = self._values.get("id_tokens")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "IDToken"]], result)

    @builtins.property
    def image(self) -> typing.Optional["Image"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional["Image"], result)

    @builtins.property
    def interruptible(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("interruptible")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry(self) -> typing.Optional["Retry"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["Retry"], result)

    @builtins.property
    def services(self) -> typing.Optional[typing.List["Service"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.List["Service"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Default(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.DefaultElement")
class DefaultElement(enum.Enum):
    '''
    :stability: experimental
    '''

    AFTER_SCRIPT = "AFTER_SCRIPT"
    '''
    :stability: experimental
    '''
    ARTIFACTS = "ARTIFACTS"
    '''
    :stability: experimental
    '''
    BEFORE_SCRIPT = "BEFORE_SCRIPT"
    '''
    :stability: experimental
    '''
    CACHE = "CACHE"
    '''
    :stability: experimental
    '''
    IMAGE = "IMAGE"
    '''
    :stability: experimental
    '''
    INTERRUPTIBLE = "INTERRUPTIBLE"
    '''
    :stability: experimental
    '''
    RETRY = "RETRY"
    '''
    :stability: experimental
    '''
    SERVICES = "SERVICES"
    '''
    :stability: experimental
    '''
    TAGS = "TAGS"
    '''
    :stability: experimental
    '''
    TIMEOUT = "TIMEOUT"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.gitlab.DeploymentTier")
class DeploymentTier(enum.Enum):
    '''(experimental) Explicitly specifies the tier of the deployment environment if non-standard environment name is used.

    :stability: experimental
    '''

    DEVELOPMENT = "DEVELOPMENT"
    '''
    :stability: experimental
    '''
    OTHER = "OTHER"
    '''
    :stability: experimental
    '''
    PRODUCTION = "PRODUCTION"
    '''
    :stability: experimental
    '''
    STAGING = "STAGING"
    '''
    :stability: experimental
    '''
    TESTING = "TESTING"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.Engine",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class Engine:
    def __init__(self, *, name: builtins.str, path: builtins.str) -> None:
        '''(experimental) The engine configuration for a secret.

        :param name: (experimental) Name of the secrets engine.
        :param path: (experimental) Path to the secrets engine.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4574deb50cf9019e113c67d714da29685143324fc4e1df06c5ea08a874de8223)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the secrets engine.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Path to the secrets engine.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Engine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Environment",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "action": "action",
        "auto_stop_in": "autoStopIn",
        "deployment_tier": "deploymentTier",
        "kubernetes": "kubernetes",
        "on_stop": "onStop",
        "url": "url",
    },
)
class Environment:
    def __init__(
        self,
        *,
        name: builtins.str,
        action: typing.Optional[Action] = None,
        auto_stop_in: typing.Optional[builtins.str] = None,
        deployment_tier: typing.Optional[DeploymentTier] = None,
        kubernetes: typing.Optional[typing.Union["KubernetesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        on_stop: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The environment that a job deploys to.

        :param name: (experimental) The name of the environment, e.g. 'qa', 'staging', 'production'.
        :param action: (experimental) Specifies what this job will do. 'start' (default) indicates the job will start the deployment. 'prepare' indicates this will not affect the deployment. 'stop' indicates this will stop the deployment.
        :param auto_stop_in: (experimental) The amount of time it should take before Gitlab will automatically stop the environment. Supports a wide variety of formats, e.g. '1 week', '3 mins 4 sec', '2 hrs 20 min', '2h20min', '6 mos 1 day', '47 yrs 6 mos and 4d', '3 weeks and 2 days'.
        :param deployment_tier: (experimental) Explicitly specifies the tier of the deployment environment if non-standard environment name is used.
        :param kubernetes: (experimental) Used to configure the kubernetes deployment for this environment. This is currently not supported for kubernetes clusters that are managed by Gitlab.
        :param on_stop: (experimental) The name of a job to execute when the environment is about to be stopped.
        :param url: (experimental) When set, this will expose buttons in various places for the current environment in Gitlab, that will take you to the defined URL.

        :stability: experimental
        '''
        if isinstance(kubernetes, dict):
            kubernetes = KubernetesConfig(**kubernetes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dacf066520edebcaf1914cf8b47a539d32b601c728c745a9821da18fc61c311)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument auto_stop_in", value=auto_stop_in, expected_type=type_hints["auto_stop_in"])
            check_type(argname="argument deployment_tier", value=deployment_tier, expected_type=type_hints["deployment_tier"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument on_stop", value=on_stop, expected_type=type_hints["on_stop"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if action is not None:
            self._values["action"] = action
        if auto_stop_in is not None:
            self._values["auto_stop_in"] = auto_stop_in
        if deployment_tier is not None:
            self._values["deployment_tier"] = deployment_tier
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if on_stop is not None:
            self._values["on_stop"] = on_stop
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the environment, e.g. 'qa', 'staging', 'production'.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[Action]:
        '''(experimental) Specifies what this job will do.

        'start' (default) indicates the job will start the deployment. 'prepare' indicates this will not affect the deployment. 'stop' indicates this will stop the deployment.

        :stability: experimental
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[Action], result)

    @builtins.property
    def auto_stop_in(self) -> typing.Optional[builtins.str]:
        '''(experimental) The amount of time it should take before Gitlab will automatically stop the environment.

        Supports a wide variety of formats, e.g. '1 week', '3 mins 4 sec', '2 hrs 20 min', '2h20min', '6 mos 1 day', '47 yrs 6 mos and 4d', '3 weeks and 2 days'.

        :stability: experimental
        '''
        result = self._values.get("auto_stop_in")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_tier(self) -> typing.Optional[DeploymentTier]:
        '''(experimental) Explicitly specifies the tier of the deployment environment if non-standard environment name is used.

        :stability: experimental
        '''
        result = self._values.get("deployment_tier")
        return typing.cast(typing.Optional[DeploymentTier], result)

    @builtins.property
    def kubernetes(self) -> typing.Optional["KubernetesConfig"]:
        '''(experimental) Used to configure the kubernetes deployment for this environment.

        This is currently not supported for kubernetes clusters that are managed by Gitlab.

        :stability: experimental
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["KubernetesConfig"], result)

    @builtins.property
    def on_stop(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of a job to execute when the environment is about to be stopped.

        :stability: experimental
        '''
        result = self._values.get("on_stop")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) When set, this will expose buttons in various places for the current environment in Gitlab, that will take you to the defined URL.

        :stability: experimental
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Environment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Filter",
    jsii_struct_bases=[],
    name_mapping={
        "changes": "changes",
        "kubernetes": "kubernetes",
        "refs": "refs",
        "variables": "variables",
    },
)
class Filter:
    def __init__(
        self,
        *,
        changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        kubernetes: typing.Optional["KubernetesEnum"] = None,
        refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Filtering options for when a job will run.

        :param changes: (experimental) Filter job creation based on files that were modified in a git push.
        :param kubernetes: (experimental) Filter job based on if Kubernetes integration is active.
        :param refs: (experimental) Control when to add jobs to a pipeline based on branch names or pipeline types.
        :param variables: (experimental) Filter job by checking comparing values of environment variables. Read more about variable expressions: https://docs.gitlab.com/ee/ci/variables/README.html#variables-expressions

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db895e6728876de5be75625df8be94a8c86846327b2443ff1fd7c8c09dc4d6f2)
            check_type(argname="argument changes", value=changes, expected_type=type_hints["changes"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument refs", value=refs, expected_type=type_hints["refs"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if changes is not None:
            self._values["changes"] = changes
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if refs is not None:
            self._values["refs"] = refs
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def changes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Filter job creation based on files that were modified in a git push.

        :stability: experimental
        '''
        result = self._values.get("changes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kubernetes(self) -> typing.Optional["KubernetesEnum"]:
        '''(experimental) Filter job based on if Kubernetes integration is active.

        :stability: experimental
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["KubernetesEnum"], result)

    @builtins.property
    def refs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Control when to add jobs to a pipeline based on branch names or pipeline types.

        :stability: experimental
        '''
        result = self._values.get("refs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Filter job by checking comparing values of environment variables.

        Read more about variable expressions: https://docs.gitlab.com/ee/ci/variables/README.html#variables-expressions

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Filter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitlabConfiguration(
    CiConfiguration,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.gitlab.GitlabConfiguration",
):
    '''(experimental) A GitLab CI for the main ``.gitlab-ci.yml`` file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        default: typing.Optional[typing.Union[Default, typing.Dict[builtins.str, typing.Any]]] = None,
        jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union["Job", typing.Dict[builtins.str, typing.Any]]]] = None,
        pages: typing.Optional[typing.Union["Job", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow: typing.Optional[typing.Union["Workflow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param default: (experimental) Default settings for the CI Configuration. Jobs that do not define one or more of the listed keywords use the value defined in the default section.
        :param jobs: (experimental) An initial set of jobs to add to the configuration.
        :param pages: (experimental) A special job used to upload static sites to Gitlab pages. Requires a ``public/`` directory with ``artifacts.path`` pointing to it.
        :param path: (experimental) The path of the file to generate.
        :param stages: (experimental) Groups jobs into stages. All jobs in one stage must complete before next stage is executed. If no stages are specified. Defaults to ['build', 'test', 'deploy'].
        :param variables: (experimental) Global variables that are passed to jobs. If the job already has that variable defined, the job-level variable takes precedence.
        :param workflow: (experimental) Used to control pipeline behavior.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7c22b752837d5c419877611c3664caa886539ab5209465bbfe27372b51e714)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = CiConfigurationOptions(
            default=default,
            jobs=jobs,
            pages=pages,
            path=path,
            stages=stages,
            variables=variables,
            workflow=workflow,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="createNestedTemplates")
    def create_nested_templates(
        self,
        config: typing.Mapping[builtins.str, typing.Union[CiConfigurationOptions, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Creates and adds nested templates to the includes of the main CI.

        Additionally adds their stages to the main CI if they are not already present.
        You can futher customize nested templates through the ``nestedTemplates`` property.
        E.g. gitlabConfig.nestedTemplates['templateName']?.addStages('stageName')

        :param config: a record the names and configuraitons of the templates.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e89c004dae5dc8a66477f9e05d4202e2de25b397ad58439158d4d0e311fa46)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        return typing.cast(None, jsii.invoke(self, "createNestedTemplates", [config]))

    @builtins.property
    @jsii.member(jsii_name="nestedTemplates")
    def nested_templates(self) -> typing.Mapping[builtins.str, "NestedConfiguration"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "NestedConfiguration"], jsii.get(self, "nestedTemplates"))


@jsii.interface(jsii_type="projen.gitlab.IDToken")
class IDToken(typing_extensions.Protocol):
    '''(experimental) id_tokens Definition.

    :see: https://docs.gitlab.com/ee/ci/yaml/#id_tokens
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="aud")
    def aud(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''(experimental) The required aud sub-keyword is used to configure the aud claim for the JWT.

        :stability: experimental
        '''
        ...

    @aud.setter
    def aud(self, value: typing.Union[builtins.str, typing.List[builtins.str]]) -> None:
        ...


class _IDTokenProxy:
    '''(experimental) id_tokens Definition.

    :see: https://docs.gitlab.com/ee/ci/yaml/#id_tokens
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.gitlab.IDToken"

    @builtins.property
    @jsii.member(jsii_name="aud")
    def aud(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''(experimental) The required aud sub-keyword is used to configure the aud claim for the JWT.

        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], jsii.get(self, "aud"))

    @aud.setter
    def aud(self, value: typing.Union[builtins.str, typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e6bbd7c1d3e16ffa82367cdd5ca16ce06a42726f4193639790a39bb2eadef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aud", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDToken).__jsii_proxy_class__ = lambda : _IDTokenProxy


@jsii.data_type(
    jsii_type="projen.gitlab.Image",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "entrypoint": "entrypoint"},
)
class Image:
    def __init__(
        self,
        *,
        name: builtins.str,
        entrypoint: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''(experimental) Specifies the docker image to use for the job or globally for all jobs.

        Job configuration
        takes precedence over global setting. Requires a certain kind of Gitlab runner executor.

        :param name: (experimental) Full name of the image that should be used. It should contain the Registry part if needed.
        :param entrypoint: (experimental) Command or script that should be executed as the container's entrypoint. It will be translated to Docker's --entrypoint option while creating the container. The syntax is similar to Dockerfile's ENTRYPOINT directive, where each shell token is a separate string in the array.

        :see: https://docs.gitlab.com/ee/ci/yaml/#image
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db043de1bfd971cf362a1d5015d39fcfec9ce12a8564e12b3dc83c2766f5e7f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Full name of the image that should be used.

        It should contain the Registry part if needed.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) Command or script that should be executed as the container's entrypoint.

        It will be translated to Docker's --entrypoint option while creating the container. The syntax is similar to Dockerfile's ENTRYPOINT directive, where each shell token is a separate string in the array.

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Image(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Include",
    jsii_struct_bases=[],
    name_mapping={
        "file": "file",
        "local": "local",
        "project": "project",
        "ref": "ref",
        "remote": "remote",
        "rules": "rules",
        "template": "template",
    },
)
class Include:
    def __init__(
        self,
        *,
        file: typing.Optional[typing.Sequence[builtins.str]] = None,
        local: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
        remote: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["IncludeRule", typing.Dict[builtins.str, typing.Any]]]] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) An included YAML file.

        :param file: (experimental) Files from another private project on the same GitLab instance. You can use ``file`` in combination with ``project`` only.
        :param local: (experimental) Relative path from local repository root (``/``) to the ``yaml``/``yml`` file template. The file must be on the same branch, and does not work across git submodules.
        :param project: (experimental) Path to the project, e.g. ``group/project``, or ``group/sub-group/project``.
        :param ref: (experimental) Branch/Tag/Commit-hash for the target project.
        :param remote: (experimental) URL to a ``yaml``/``yml`` template file using HTTP/HTTPS.
        :param rules: (experimental) Rules allows for an array of individual rule objects to be evaluated in order, until one matches and dynamically provides attributes to the job.
        :param template: (experimental) Use a ``.gitlab-ci.yml`` template as a base, e.g. ``Nodejs.gitlab-ci.yml``.

        :see: https://docs.gitlab.com/ee/ci/yaml/#include
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b4b33f824dede3c51f8491f23c1b24aa99de8902ab2b0adb792fbc13ddf8fe)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if local is not None:
            self._values["local"] = local
        if project is not None:
            self._values["project"] = project
        if ref is not None:
            self._values["ref"] = ref
        if remote is not None:
            self._values["remote"] = remote
        if rules is not None:
            self._values["rules"] = rules
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def file(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Files from another private project on the same GitLab instance.

        You can use ``file`` in combination with ``project`` only.

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local(self) -> typing.Optional[builtins.str]:
        '''(experimental) Relative path from local repository root (``/``) to the ``yaml``/``yml`` file template.

        The file must be on the same branch, and does not work across git submodules.

        :stability: experimental
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the project, e.g. ``group/project``, or ``group/sub-group/project``.

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''(experimental) Branch/Tag/Commit-hash for the target project.

        :stability: experimental
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL to a ``yaml``/``yml`` template file using HTTP/HTTPS.

        :stability: experimental
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["IncludeRule"]]:
        '''(experimental) Rules allows for an array of individual rule objects to be evaluated in order, until one matches and dynamically provides attributes to the job.

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["IncludeRule"]], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use a ``.gitlab-ci.yml`` template as a base, e.g. ``Nodejs.gitlab-ci.yml``.

        :stability: experimental
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Include(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.IncludeRule",
    jsii_struct_bases=[],
    name_mapping={
        "allow_failure": "allowFailure",
        "changes": "changes",
        "exists": "exists",
        "if_": "if",
        "needs": "needs",
        "start_in": "startIn",
        "variables": "variables",
        "when": "when",
    },
)
class IncludeRule:
    def __init__(
        self,
        *,
        allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Union[AllowFailure, typing.Dict[builtins.str, typing.Any]]]] = None,
        changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exists: typing.Optional[typing.Sequence[builtins.str]] = None,
        if_: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_in: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        when: typing.Optional["JobWhen"] = None,
    ) -> None:
        '''(experimental) Rules allows for an array of individual rule objects to be evaluated in order, until one matches and dynamically provides attributes to the job.

        :param allow_failure: 
        :param changes: 
        :param exists: 
        :param if_: 
        :param needs: 
        :param start_in: 
        :param variables: 
        :param when: 

        :see: https://docs.gitlab.com/ee/ci/yaml/includes.html#use-rules-with-include
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5547025bbe422124f59e782b7141894ba37dbf0049070c73b17f39de1d1843a1)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument changes", value=changes, expected_type=type_hints["changes"])
            check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument start_in", value=start_in, expected_type=type_hints["start_in"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if changes is not None:
            self._values["changes"] = changes
        if exists is not None:
            self._values["exists"] = exists
        if if_ is not None:
            self._values["if_"] = if_
        if needs is not None:
            self._values["needs"] = needs
        if start_in is not None:
            self._values["start_in"] = start_in
        if variables is not None:
            self._values["variables"] = variables
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def allow_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, AllowFailure]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, AllowFailure]], result)

    @builtins.property
    def changes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("changes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("exists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def start_in(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("start_in")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def when(self) -> typing.Optional["JobWhen"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["JobWhen"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Inherit",
    jsii_struct_bases=[],
    name_mapping={"default": "default", "variables": "variables"},
)
class Inherit:
    def __init__(
        self,
        *,
        default: typing.Optional[typing.Union[builtins.bool, typing.Sequence[DefaultElement]]] = None,
        variables: typing.Optional[typing.Union[builtins.bool, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Controls inheritance of globally-defined defaults and variables.

        Boolean values control
        inheritance of all default: or variables: keywords. To inherit only a subset of default:
        or variables: keywords, specify what you wish to inherit. Anything not listed is not
        inherited.

        :param default: (experimental) Whether to inherit all globally-defined defaults or not. Or subset of inherited defaults
        :param variables: (experimental) Whether to inherit all globally-defined variables or not. Or subset of inherited variables

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e202056f8d0ee046415cdd0eeba7b03d414bbd38fc367909020c4d2d2766cf)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default is not None:
            self._values["default"] = default
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, typing.List[DefaultElement]]]:
        '''(experimental) Whether to inherit all globally-defined defaults or not.

        Or subset of inherited defaults

        :stability: experimental
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, typing.List[DefaultElement]]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, typing.List[builtins.str]]]:
        '''(experimental) Whether to inherit all globally-defined variables or not.

        Or subset of inherited variables

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, typing.List[builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Inherit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Job",
    jsii_struct_bases=[],
    name_mapping={
        "after_script": "afterScript",
        "allow_failure": "allowFailure",
        "artifacts": "artifacts",
        "before_script": "beforeScript",
        "cache": "cache",
        "coverage": "coverage",
        "dependencies": "dependencies",
        "environment": "environment",
        "except_": "except",
        "extends": "extends",
        "id_tokens": "idTokens",
        "image": "image",
        "inherit": "inherit",
        "interruptible": "interruptible",
        "needs": "needs",
        "only": "only",
        "parallel": "parallel",
        "release": "release",
        "resource_group": "resourceGroup",
        "retry": "retry",
        "rules": "rules",
        "script": "script",
        "secrets": "secrets",
        "services": "services",
        "stage": "stage",
        "start_in": "startIn",
        "tags": "tags",
        "timeout": "timeout",
        "trigger": "trigger",
        "variables": "variables",
        "when": "when",
    },
)
class Job:
    def __init__(
        self,
        *,
        after_script: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Union[AllowFailure, typing.Dict[builtins.str, typing.Any]]]] = None,
        artifacts: typing.Optional[typing.Union[Artifacts, typing.Dict[builtins.str, typing.Any]]] = None,
        before_script: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache: typing.Optional[typing.Sequence[typing.Union[Cache, typing.Dict[builtins.str, typing.Any]]]] = None,
        coverage: typing.Optional[builtins.str] = None,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[builtins.str, typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]]] = None,
        except_: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Union[Filter, typing.Dict[builtins.str, typing.Any]]]] = None,
        extends: typing.Optional[typing.Sequence[builtins.str]] = None,
        id_tokens: typing.Optional[typing.Mapping[builtins.str, IDToken]] = None,
        image: typing.Optional[typing.Union[Image, typing.Dict[builtins.str, typing.Any]]] = None,
        inherit: typing.Optional[typing.Union[Inherit, typing.Dict[builtins.str, typing.Any]]] = None,
        interruptible: typing.Optional[builtins.bool] = None,
        needs: typing.Optional[typing.Sequence[typing.Union[builtins.str, typing.Union["Need", typing.Dict[builtins.str, typing.Any]]]]] = None,
        only: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Union[Filter, typing.Dict[builtins.str, typing.Any]]]] = None,
        parallel: typing.Optional[typing.Union[jsii.Number, typing.Union["Parallel", typing.Dict[builtins.str, typing.Any]]]] = None,
        release: typing.Optional[typing.Union["Release", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_group: typing.Optional[builtins.str] = None,
        retry: typing.Optional[typing.Union["Retry", typing.Dict[builtins.str, typing.Any]]] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[IncludeRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        script: typing.Optional[typing.Sequence[builtins.str]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Union["Secret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        services: typing.Optional[typing.Sequence[typing.Union["Service", typing.Dict[builtins.str, typing.Any]]]] = None,
        stage: typing.Optional[builtins.str] = None,
        start_in: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[typing.Union[builtins.str, typing.Union["Trigger", typing.Dict[builtins.str, typing.Any]]]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        when: typing.Optional["JobWhen"] = None,
    ) -> None:
        '''(experimental) Jobs are the most fundamental element of a .gitlab-ci.yml file.

        :param after_script: 
        :param allow_failure: (experimental) Whether to allow the pipeline to continue running on job failure (Default: false).
        :param artifacts: 
        :param before_script: 
        :param cache: 
        :param coverage: (experimental) Must be a regular expression, optionally but recommended to be quoted, and must be surrounded with '/'. Example: '/Code coverage: \\d+.\\d+/'
        :param dependencies: (experimental) Specify a list of job names from earlier stages from which artifacts should be loaded. By default, all previous artifacts are passed. Use an empty array to skip downloading artifacts.
        :param environment: (experimental) Used to associate environment metadata with a deploy. Environment can have a name and URL attached to it, and will be displayed under /environments under the project.
        :param except_: (experimental) Job will run *except* for when these filtering options match.
        :param extends: (experimental) The name of one or more jobs to inherit configuration from.
        :param id_tokens: (experimental) Configurable ID tokens (JSON Web Tokens) that are used for CI/CD authentication.
        :param image: 
        :param inherit: (experimental) Controls inheritance of globally-defined defaults and variables. Boolean values control inheritance of all default: or variables: keywords. To inherit only a subset of default: or variables: keywords, specify what you wish to inherit. Anything not listed is not inherited.
        :param interruptible: 
        :param needs: (experimental) The list of jobs in previous stages whose sole completion is needed to start the current job.
        :param only: (experimental) Job will run *only* when these filtering options match.
        :param parallel: (experimental) Parallel will split up a single job into several, and provide ``CI_NODE_INDEX`` and ``CI_NODE_TOTAL`` environment variables for the running jobs.
        :param release: (experimental) Indicates that the job creates a Release.
        :param resource_group: (experimental) Limit job concurrency. Can be used to ensure that the Runner will not run certain jobs simultaneously.
        :param retry: 
        :param rules: (experimental) Rules allows for an array of individual rule objects to be evaluated in order, until one matches and dynamically provides attributes to the job.
        :param script: (experimental) Shell scripts executed by the Runner. The only required property of jobs. Be careful with special characters (e.g. ``:``, ``{``, ``}``, ``&``) and use single or double quotes to avoid issues.
        :param secrets: (experimental) CI/CD secrets.
        :param services: 
        :param stage: (experimental) Define what stage the job will run in.
        :param start_in: 
        :param tags: 
        :param timeout: 
        :param trigger: (experimental) Trigger allows you to define downstream pipeline trigger. When a job created from trigger definition is started by GitLab, a downstream pipeline gets created. Read more: https://docs.gitlab.com/ee/ci/yaml/README.html#trigger
        :param variables: (experimental) Configurable values that are passed to the Job.
        :param when: (experimental) Describes the conditions for when to run the job. Defaults to 'on_success'.

        :see: https://docs.gitlab.com/ee/ci/jobs/
        :stability: experimental
        '''
        if isinstance(artifacts, dict):
            artifacts = Artifacts(**artifacts)
        if isinstance(image, dict):
            image = Image(**image)
        if isinstance(inherit, dict):
            inherit = Inherit(**inherit)
        if isinstance(release, dict):
            release = Release(**release)
        if isinstance(retry, dict):
            retry = Retry(**retry)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485afb8ca4cf12bdaab3c3455c7b90f3ea9d549eb87ec6fd05eae046f3f38bd6)
            check_type(argname="argument after_script", value=after_script, expected_type=type_hints["after_script"])
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument before_script", value=before_script, expected_type=type_hints["before_script"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument coverage", value=coverage, expected_type=type_hints["coverage"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument except_", value=except_, expected_type=type_hints["except_"])
            check_type(argname="argument extends", value=extends, expected_type=type_hints["extends"])
            check_type(argname="argument id_tokens", value=id_tokens, expected_type=type_hints["id_tokens"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument inherit", value=inherit, expected_type=type_hints["inherit"])
            check_type(argname="argument interruptible", value=interruptible, expected_type=type_hints["interruptible"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument only", value=only, expected_type=type_hints["only"])
            check_type(argname="argument parallel", value=parallel, expected_type=type_hints["parallel"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument start_in", value=start_in, expected_type=type_hints["start_in"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if after_script is not None:
            self._values["after_script"] = after_script
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if before_script is not None:
            self._values["before_script"] = before_script
        if cache is not None:
            self._values["cache"] = cache
        if coverage is not None:
            self._values["coverage"] = coverage
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if environment is not None:
            self._values["environment"] = environment
        if except_ is not None:
            self._values["except_"] = except_
        if extends is not None:
            self._values["extends"] = extends
        if id_tokens is not None:
            self._values["id_tokens"] = id_tokens
        if image is not None:
            self._values["image"] = image
        if inherit is not None:
            self._values["inherit"] = inherit
        if interruptible is not None:
            self._values["interruptible"] = interruptible
        if needs is not None:
            self._values["needs"] = needs
        if only is not None:
            self._values["only"] = only
        if parallel is not None:
            self._values["parallel"] = parallel
        if release is not None:
            self._values["release"] = release
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if retry is not None:
            self._values["retry"] = retry
        if rules is not None:
            self._values["rules"] = rules
        if script is not None:
            self._values["script"] = script
        if secrets is not None:
            self._values["secrets"] = secrets
        if services is not None:
            self._values["services"] = services
        if stage is not None:
            self._values["stage"] = stage
        if start_in is not None:
            self._values["start_in"] = start_in
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if trigger is not None:
            self._values["trigger"] = trigger
        if variables is not None:
            self._values["variables"] = variables
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def after_script(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("after_script")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, AllowFailure]]:
        '''(experimental) Whether to allow the pipeline to continue running on job failure (Default: false).

        :stability: experimental
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, AllowFailure]], result)

    @builtins.property
    def artifacts(self) -> typing.Optional[Artifacts]:
        '''
        :stability: experimental
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[Artifacts], result)

    @builtins.property
    def before_script(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("before_script")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache(self) -> typing.Optional[typing.List[Cache]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[typing.List[Cache]], result)

    @builtins.property
    def coverage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Must be a regular expression, optionally but recommended to be quoted, and must be surrounded with '/'.

        Example: '/Code coverage: \\d+.\\d+/'

        :stability: experimental
        '''
        result = self._values.get("coverage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specify a list of job names from earlier stages from which artifacts should be loaded.

        By default, all previous artifacts are passed. Use an empty array to skip downloading artifacts.

        :stability: experimental
        '''
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[typing.Union[builtins.str, Environment]]:
        '''(experimental) Used to associate environment metadata with a deploy.

        Environment can have a name and URL attached to it, and will be displayed under /environments under the project.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[builtins.str, Environment]], result)

    @builtins.property
    def except_(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], Filter]]:
        '''(experimental) Job will run *except* for when these filtering options match.

        :stability: experimental
        '''
        result = self._values.get("except_")
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], Filter]], result)

    @builtins.property
    def extends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The name of one or more jobs to inherit configuration from.

        :stability: experimental
        '''
        result = self._values.get("extends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id_tokens(self) -> typing.Optional[typing.Mapping[builtins.str, IDToken]]:
        '''(experimental) Configurable ID tokens (JSON Web Tokens) that are used for CI/CD authentication.

        :stability: experimental
        '''
        result = self._values.get("id_tokens")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, IDToken]], result)

    @builtins.property
    def image(self) -> typing.Optional[Image]:
        '''
        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[Image], result)

    @builtins.property
    def inherit(self) -> typing.Optional[Inherit]:
        '''(experimental) Controls inheritance of globally-defined defaults and variables.

        Boolean values control inheritance of all default: or variables: keywords. To inherit only a subset of default: or variables: keywords, specify what you wish to inherit. Anything not listed is not inherited.

        :stability: experimental
        '''
        result = self._values.get("inherit")
        return typing.cast(typing.Optional[Inherit], result)

    @builtins.property
    def interruptible(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("interruptible")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[typing.Union[builtins.str, "Need"]]]:
        '''(experimental) The list of jobs in previous stages whose sole completion is needed to start the current job.

        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[typing.Union[builtins.str, "Need"]]], result)

    @builtins.property
    def only(self) -> typing.Optional[typing.Union[typing.List[builtins.str], Filter]]:
        '''(experimental) Job will run *only* when these filtering options match.

        :stability: experimental
        '''
        result = self._values.get("only")
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], Filter]], result)

    @builtins.property
    def parallel(self) -> typing.Optional[typing.Union[jsii.Number, "Parallel"]]:
        '''(experimental) Parallel will split up a single job into several, and provide ``CI_NODE_INDEX`` and ``CI_NODE_TOTAL`` environment variables for the running jobs.

        :stability: experimental
        '''
        result = self._values.get("parallel")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, "Parallel"]], result)

    @builtins.property
    def release(self) -> typing.Optional["Release"]:
        '''(experimental) Indicates that the job creates a Release.

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional["Release"], result)

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Limit job concurrency.

        Can be used to ensure that the Runner will not run certain jobs simultaneously.

        :stability: experimental
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry(self) -> typing.Optional["Retry"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["Retry"], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List[IncludeRule]]:
        '''(experimental) Rules allows for an array of individual rule objects to be evaluated in order, until one matches and dynamically provides attributes to the job.

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[IncludeRule]], result)

    @builtins.property
    def script(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Shell scripts executed by the Runner.

        The only required property of jobs. Be careful with special characters (e.g. ``:``, ``{``, ``}``, ``&``) and use single or double quotes to avoid issues.

        :stability: experimental
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, "Secret"]]]:
        '''(experimental) CI/CD secrets.

        :stability: experimental
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, "Secret"]]], result)

    @builtins.property
    def services(self) -> typing.Optional[typing.List["Service"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.List["Service"]], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Define what stage the job will run in.

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_in(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("start_in")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger(self) -> typing.Optional[typing.Union[builtins.str, "Trigger"]]:
        '''(experimental) Trigger allows you to define downstream pipeline trigger.

        When a job created from trigger definition is started by GitLab, a downstream pipeline gets created. Read more: https://docs.gitlab.com/ee/ci/yaml/README.html#trigger

        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "Trigger"]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Configurable values that are passed to the Job.

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def when(self) -> typing.Optional["JobWhen"]:
        '''(experimental) Describes the conditions for when to run the job.

        Defaults to 'on_success'.

        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["JobWhen"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Job(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.JobWhen")
class JobWhen(enum.Enum):
    '''(experimental) Describes the conditions for when to run the job.

    Defaults to 'on_success'.

    :see: https://docs.gitlab.com/ee/ci/yaml/#when
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''
    :stability: experimental
    '''
    DELAYED = "DELAYED"
    '''
    :stability: experimental
    '''
    MANUAL = "MANUAL"
    '''
    :stability: experimental
    '''
    NEVER = "NEVER"
    '''
    :stability: experimental
    '''
    ON_FAILURE = "ON_FAILURE"
    '''
    :stability: experimental
    '''
    ON_SUCCESS = "ON_SUCCESS"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.KubernetesConfig",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace"},
)
class KubernetesConfig:
    def __init__(self, *, namespace: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Used to configure the kubernetes deployment for this environment.

        This is currently not
        supported for kubernetes clusters that are managed by Gitlab.

        :param namespace: (experimental) The kubernetes namespace where this environment should be deployed to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5135e122b0fb90c5ae5d8c65626715c279ba6c8bb4103d4bd7a12969d1f5ad)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kubernetes namespace where this environment should be deployed to.

        :stability: experimental
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.KubernetesEnum")
class KubernetesEnum(enum.Enum):
    '''(experimental) Filter job based on if Kubernetes integration is active.

    :stability: experimental
    '''

    ACTIVE = "ACTIVE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.Link",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "url": "url",
        "filepath": "filepath",
        "link_type": "linkType",
    },
)
class Link:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        filepath: typing.Optional[builtins.str] = None,
        link_type: typing.Optional["LinkType"] = None,
    ) -> None:
        '''(experimental) Link configuration for an asset.

        :param name: (experimental) The name of the link.
        :param url: (experimental) The URL to download a file.
        :param filepath: (experimental) The redirect link to the url.
        :param link_type: (experimental) The content kind of what users can download via url.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003677e3874ed26747f048e8b5c08a32b87f0226f3522c10b0844ade2521966c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument link_type", value=link_type, expected_type=type_hints["link_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }
        if filepath is not None:
            self._values["filepath"] = filepath
        if link_type is not None:
            self._values["link_type"] = link_type

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the link.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The URL to download a file.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filepath(self) -> typing.Optional[builtins.str]:
        '''(experimental) The redirect link to the url.

        :stability: experimental
        '''
        result = self._values.get("filepath")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_type(self) -> typing.Optional["LinkType"]:
        '''(experimental) The content kind of what users can download via url.

        :stability: experimental
        '''
        result = self._values.get("link_type")
        return typing.cast(typing.Optional["LinkType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Link(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.LinkType")
class LinkType(enum.Enum):
    '''(experimental) The content kind of what users can download via url.

    :stability: experimental
    '''

    IMAGE = "IMAGE"
    '''
    :stability: experimental
    '''
    OTHER = "OTHER"
    '''
    :stability: experimental
    '''
    PACKAGE = "PACKAGE"
    '''
    :stability: experimental
    '''
    RUNBOOK = "RUNBOOK"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.Need",
    jsii_struct_bases=[],
    name_mapping={
        "job": "job",
        "artifacts": "artifacts",
        "optional": "optional",
        "pipeline": "pipeline",
        "project": "project",
        "ref": "ref",
    },
)
class Need:
    def __init__(
        self,
        *,
        job: builtins.str,
        artifacts: typing.Optional[builtins.bool] = None,
        optional: typing.Optional[builtins.bool] = None,
        pipeline: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A jobs in a previous stage whose sole completion is needed to start the current job.

        :param job: 
        :param artifacts: 
        :param optional: 
        :param pipeline: 
        :param project: 
        :param ref: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62a8b5d59de20d0811a6eb2ae8ef5a38099d2a9da0ebfd9c9ce8d1406ce4f8e)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job": job,
        }
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if optional is not None:
            self._values["optional"] = optional
        if pipeline is not None:
            self._values["pipeline"] = pipeline
        if project is not None:
            self._values["project"] = project
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def job(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("job")
        assert result is not None, "Required property 'job' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifacts(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Need(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NestedConfiguration(
    CiConfiguration,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.gitlab.NestedConfiguration",
):
    '''(experimental) A GitLab CI for templates that are created and included in the ``.gitlab-ci.yml`` file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        parent: GitlabConfiguration,
        name: builtins.str,
        *,
        default: typing.Optional[typing.Union[Default, typing.Dict[builtins.str, typing.Any]]] = None,
        jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union[Job, typing.Dict[builtins.str, typing.Any]]]] = None,
        pages: typing.Optional[typing.Union[Job, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow: typing.Optional[typing.Union["Workflow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param parent: -
        :param name: The name of the configuration.
        :param default: (experimental) Default settings for the CI Configuration. Jobs that do not define one or more of the listed keywords use the value defined in the default section.
        :param jobs: (experimental) An initial set of jobs to add to the configuration.
        :param pages: (experimental) A special job used to upload static sites to Gitlab pages. Requires a ``public/`` directory with ``artifacts.path`` pointing to it.
        :param path: (experimental) The path of the file to generate.
        :param stages: (experimental) Groups jobs into stages. All jobs in one stage must complete before next stage is executed. If no stages are specified. Defaults to ['build', 'test', 'deploy'].
        :param variables: (experimental) Global variables that are passed to jobs. If the job already has that variable defined, the job-level variable takes precedence.
        :param workflow: (experimental) Used to control pipeline behavior.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d7f1d8d243fb7e275a0eeba3f1419822bf2c274e47641e553a5675c002a437)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = CiConfigurationOptions(
            default=default,
            jobs=jobs,
            pages=pages,
            path=path,
            stages=stages,
            variables=variables,
            workflow=workflow,
        )

        jsii.create(self.__class__, self, [project, parent, name, options])

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> GitlabConfiguration:
        '''
        :stability: experimental
        '''
        return typing.cast(GitlabConfiguration, jsii.get(self, "parent"))


@jsii.data_type(
    jsii_type="projen.gitlab.Parallel",
    jsii_struct_bases=[],
    name_mapping={"matrix": "matrix"},
)
class Parallel:
    def __init__(
        self,
        *,
        matrix: typing.Sequence[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]],
    ) -> None:
        '''(experimental) Used to run a job multiple times in parallel in a single pipeline.

        :param matrix: (experimental) Defines different variables for jobs that are running in parallel.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27837ae5c9e058eb0806d1abd6557c3fa362e2df59dcab8ce1db5416c00525e1)
            check_type(argname="argument matrix", value=matrix, expected_type=type_hints["matrix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matrix": matrix,
        }

    @builtins.property
    def matrix(
        self,
    ) -> typing.List[typing.Mapping[builtins.str, typing.List[typing.Any]]]:
        '''(experimental) Defines different variables for jobs that are running in parallel.

        :stability: experimental
        '''
        result = self._values.get("matrix")
        assert result is not None, "Required property 'matrix' is missing"
        return typing.cast(typing.List[typing.Mapping[builtins.str, typing.List[typing.Any]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Parallel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.PullPolicy")
class PullPolicy(enum.Enum):
    '''(experimental) Describes the conditions for when to pull an image.

    :see: https://docs.gitlab.com/ee/ci/yaml/#servicepull_policy
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''
    :stability: experimental
    '''
    NEVER = "NEVER"
    '''
    :stability: experimental
    '''
    IF_NOT_PRESENT = "IF_NOT_PRESENT"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.Release",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "tag_name": "tagName",
        "assets": "assets",
        "milestones": "milestones",
        "name": "name",
        "ref": "ref",
        "released_at": "releasedAt",
    },
)
class Release:
    def __init__(
        self,
        *,
        description: builtins.str,
        tag_name: builtins.str,
        assets: typing.Optional[typing.Union[Assets, typing.Dict[builtins.str, typing.Any]]] = None,
        milestones: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
        released_at: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Indicates that the job creates a Release.

        :param description: (experimental) Specifies the longer description of the Release.
        :param tag_name: (experimental) The tag_name must be specified. It can refer to an existing Git tag or can be specified by the user.
        :param assets: 
        :param milestones: (experimental) The title of each milestone the release is associated with.
        :param name: (experimental) The Release name. If omitted, it is populated with the value of release: tag_name.
        :param ref: (experimental) If the release: tag_name doesn’t exist yet, the release is created from ref. ref can be a commit SHA, another tag name, or a branch name.
        :param released_at: (experimental) The date and time when the release is ready. Defaults to the current date and time if not defined. Should be enclosed in quotes and expressed in ISO 8601 format.

        :stability: experimental
        '''
        if isinstance(assets, dict):
            assets = Assets(**assets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38e7545caf21650d3fd8d9c8672f7ac49978e130308eff721d262f5ca861d93)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument milestones", value=milestones, expected_type=type_hints["milestones"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument released_at", value=released_at, expected_type=type_hints["released_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "tag_name": tag_name,
        }
        if assets is not None:
            self._values["assets"] = assets
        if milestones is not None:
            self._values["milestones"] = milestones
        if name is not None:
            self._values["name"] = name
        if ref is not None:
            self._values["ref"] = ref
        if released_at is not None:
            self._values["released_at"] = released_at

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) Specifies the longer description of the Release.

        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_name(self) -> builtins.str:
        '''(experimental) The tag_name must be specified.

        It can refer to an existing Git tag or can be specified by the user.

        :stability: experimental
        '''
        result = self._values.get("tag_name")
        assert result is not None, "Required property 'tag_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assets(self) -> typing.Optional[Assets]:
        '''
        :stability: experimental
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[Assets], result)

    @builtins.property
    def milestones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The title of each milestone the release is associated with.

        :stability: experimental
        '''
        result = self._values.get("milestones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Release name.

        If omitted, it is populated with the value of release: tag_name.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the release: tag_name doesn’t exist yet, the release is created from ref.

        ref can be a commit SHA, another tag name, or a branch name.

        :stability: experimental
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def released_at(self) -> typing.Optional[builtins.str]:
        '''(experimental) The date and time when the release is ready.

        Defaults to the current date and time if not defined. Should be enclosed in quotes and expressed in ISO 8601 format.

        :stability: experimental
        '''
        result = self._values.get("released_at")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Release(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Reports",
    jsii_struct_bases=[],
    name_mapping={
        "cobertura": "cobertura",
        "codequality": "codequality",
        "container_scanning": "containerScanning",
        "coverage_report": "coverageReport",
        "dast": "dast",
        "dependency_scanning": "dependencyScanning",
        "dotenv": "dotenv",
        "junit": "junit",
        "license_management": "licenseManagement",
        "license_scanning": "licenseScanning",
        "lsif": "lsif",
        "metrics": "metrics",
        "performance": "performance",
        "requirements": "requirements",
        "sast": "sast",
        "secret_detection": "secretDetection",
        "terraform": "terraform",
    },
)
class Reports:
    def __init__(
        self,
        *,
        cobertura: typing.Optional[typing.Sequence[builtins.str]] = None,
        codequality: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_scanning: typing.Optional[typing.Sequence[builtins.str]] = None,
        coverage_report: typing.Optional[typing.Union[CoverageReport, typing.Dict[builtins.str, typing.Any]]] = None,
        dast: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_scanning: typing.Optional[typing.Sequence[builtins.str]] = None,
        dotenv: typing.Optional[typing.Sequence[builtins.str]] = None,
        junit: typing.Optional[typing.Sequence[builtins.str]] = None,
        license_management: typing.Optional[typing.Sequence[builtins.str]] = None,
        license_scanning: typing.Optional[typing.Sequence[builtins.str]] = None,
        lsif: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
        performance: typing.Optional[typing.Sequence[builtins.str]] = None,
        requirements: typing.Optional[typing.Sequence[builtins.str]] = None,
        sast: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_detection: typing.Optional[typing.Sequence[builtins.str]] = None,
        terraform: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Reports will be uploaded as artifacts, and often displayed in the Gitlab UI, such as in Merge Requests.

        :param cobertura: (deprecated) Path for file(s) that should be parsed as Cobertura XML coverage report.
        :param codequality: (experimental) Path to file or list of files with code quality report(s) (such as Code Climate).
        :param container_scanning: (experimental) Path to file or list of files with Container scanning vulnerabilities report(s).
        :param coverage_report: (experimental) Code coverage report information.
        :param dast: (experimental) Path to file or list of files with DAST vulnerabilities report(s).
        :param dependency_scanning: (experimental) Path to file or list of files with Dependency scanning vulnerabilities report(s).
        :param dotenv: (experimental) Path to file or list of files containing runtime-created variables for this job.
        :param junit: (experimental) Path for file(s) that should be parsed as JUnit XML result.
        :param license_management: (experimental) Deprecated in 12.8: Path to file or list of files with license report(s).
        :param license_scanning: (experimental) Path to file or list of files with license report(s).
        :param lsif: (experimental) Path to file or list of files containing code intelligence (Language Server Index Format).
        :param metrics: (experimental) Path to file or list of files with custom metrics report(s).
        :param performance: (experimental) Path to file or list of files with performance metrics report(s).
        :param requirements: (experimental) Path to file or list of files with requirements report(s).
        :param sast: (experimental) Path to file or list of files with SAST vulnerabilities report(s).
        :param secret_detection: (experimental) Path to file or list of files with secret detection report(s).
        :param terraform: (experimental) Path to file or list of files with terraform plan(s).

        :see: https://docs.gitlab.com/ee/ci/yaml/#artifactsreports
        :stability: experimental
        '''
        if isinstance(coverage_report, dict):
            coverage_report = CoverageReport(**coverage_report)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f4030cd6e6d9c8988080afe12341d674a6d0751da1c7937dd3901c9d6062c)
            check_type(argname="argument cobertura", value=cobertura, expected_type=type_hints["cobertura"])
            check_type(argname="argument codequality", value=codequality, expected_type=type_hints["codequality"])
            check_type(argname="argument container_scanning", value=container_scanning, expected_type=type_hints["container_scanning"])
            check_type(argname="argument coverage_report", value=coverage_report, expected_type=type_hints["coverage_report"])
            check_type(argname="argument dast", value=dast, expected_type=type_hints["dast"])
            check_type(argname="argument dependency_scanning", value=dependency_scanning, expected_type=type_hints["dependency_scanning"])
            check_type(argname="argument dotenv", value=dotenv, expected_type=type_hints["dotenv"])
            check_type(argname="argument junit", value=junit, expected_type=type_hints["junit"])
            check_type(argname="argument license_management", value=license_management, expected_type=type_hints["license_management"])
            check_type(argname="argument license_scanning", value=license_scanning, expected_type=type_hints["license_scanning"])
            check_type(argname="argument lsif", value=lsif, expected_type=type_hints["lsif"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument performance", value=performance, expected_type=type_hints["performance"])
            check_type(argname="argument requirements", value=requirements, expected_type=type_hints["requirements"])
            check_type(argname="argument sast", value=sast, expected_type=type_hints["sast"])
            check_type(argname="argument secret_detection", value=secret_detection, expected_type=type_hints["secret_detection"])
            check_type(argname="argument terraform", value=terraform, expected_type=type_hints["terraform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cobertura is not None:
            self._values["cobertura"] = cobertura
        if codequality is not None:
            self._values["codequality"] = codequality
        if container_scanning is not None:
            self._values["container_scanning"] = container_scanning
        if coverage_report is not None:
            self._values["coverage_report"] = coverage_report
        if dast is not None:
            self._values["dast"] = dast
        if dependency_scanning is not None:
            self._values["dependency_scanning"] = dependency_scanning
        if dotenv is not None:
            self._values["dotenv"] = dotenv
        if junit is not None:
            self._values["junit"] = junit
        if license_management is not None:
            self._values["license_management"] = license_management
        if license_scanning is not None:
            self._values["license_scanning"] = license_scanning
        if lsif is not None:
            self._values["lsif"] = lsif
        if metrics is not None:
            self._values["metrics"] = metrics
        if performance is not None:
            self._values["performance"] = performance
        if requirements is not None:
            self._values["requirements"] = requirements
        if sast is not None:
            self._values["sast"] = sast
        if secret_detection is not None:
            self._values["secret_detection"] = secret_detection
        if terraform is not None:
            self._values["terraform"] = terraform

    @builtins.property
    def cobertura(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Path for file(s) that should be parsed as Cobertura XML coverage report.

        :deprecated: per {@link https://docs.gitlab.com/ee/update/deprecations.html#artifactsreportscobertura-keyword} use {@link coverageReport } instead

        :stability: deprecated
        '''
        result = self._values.get("cobertura")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def codequality(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with code quality report(s) (such as Code Climate).

        :stability: experimental
        '''
        result = self._values.get("codequality")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_scanning(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with Container scanning vulnerabilities report(s).

        :stability: experimental
        '''
        result = self._values.get("container_scanning")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def coverage_report(self) -> typing.Optional[CoverageReport]:
        '''(experimental) Code coverage report information.

        :stability: experimental
        '''
        result = self._values.get("coverage_report")
        return typing.cast(typing.Optional[CoverageReport], result)

    @builtins.property
    def dast(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with DAST vulnerabilities report(s).

        :stability: experimental
        '''
        result = self._values.get("dast")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dependency_scanning(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with Dependency scanning vulnerabilities report(s).

        :stability: experimental
        '''
        result = self._values.get("dependency_scanning")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dotenv(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files containing runtime-created variables for this job.

        :stability: experimental
        '''
        result = self._values.get("dotenv")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def junit(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path for file(s) that should be parsed as JUnit XML result.

        :stability: experimental
        '''
        result = self._values.get("junit")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license_management(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Deprecated in 12.8: Path to file or list of files with license report(s).

        :stability: experimental
        '''
        result = self._values.get("license_management")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license_scanning(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with license report(s).

        :stability: experimental
        '''
        result = self._values.get("license_scanning")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lsif(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files containing code intelligence (Language Server Index Format).

        :stability: experimental
        '''
        result = self._values.get("lsif")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with custom metrics report(s).

        :stability: experimental
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def performance(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with performance metrics report(s).

        :stability: experimental
        '''
        result = self._values.get("performance")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def requirements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with requirements report(s).

        :stability: experimental
        '''
        result = self._values.get("requirements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sast(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with SAST vulnerabilities report(s).

        :stability: experimental
        '''
        result = self._values.get("sast")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_detection(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with secret detection report(s).

        :stability: experimental
        '''
        result = self._values.get("secret_detection")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def terraform(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Path to file or list of files with terraform plan(s).

        :stability: experimental
        '''
        result = self._values.get("terraform")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Reports(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Retry",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "when": "when"},
)
class Retry:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        when: typing.Any = None,
    ) -> None:
        '''(experimental) How many times a job is retried if it fails.

        If not defined, defaults to 0 and jobs do not retry.

        :param max: (experimental) 0 (default), 1, or 2.
        :param when: (experimental) Either a single or array of error types to trigger job retry.

        :see: https://docs.gitlab.com/ee/ci/yaml/#retry
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbb57c0c914d3fe61ad0fc30c66b1fa89242257ae2e7fbd309e5819250ac25e)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) 0 (default), 1, or 2.

        :stability: experimental
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def when(self) -> typing.Any:
        '''(experimental) Either a single or array of error types to trigger job retry.

        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Retry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Secret",
    jsii_struct_bases=[],
    name_mapping={"vault": "vault"},
)
class Secret:
    def __init__(
        self,
        *,
        vault: typing.Union["VaultConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) A CI/CD secret.

        :param vault: 

        :stability: experimental
        '''
        if isinstance(vault, dict):
            vault = VaultConfig(**vault)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789ab87a937f7529123f7dfe15f4731fb2ba2cd3529681a1c5b7c2766ac518ed)
            check_type(argname="argument vault", value=vault, expected_type=type_hints["vault"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vault": vault,
        }

    @builtins.property
    def vault(self) -> "VaultConfig":
        '''
        :stability: experimental
        '''
        result = self._values.get("vault")
        assert result is not None, "Required property 'vault' is missing"
        return typing.cast("VaultConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Secret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Service",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "alias": "alias",
        "command": "command",
        "entrypoint": "entrypoint",
        "pull_policy": "pullPolicy",
        "variables": "variables",
    },
)
class Service:
    def __init__(
        self,
        *,
        name: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_policy: typing.Optional[typing.Sequence[PullPolicy]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Used to specify an additional Docker image to run scripts in.

        The service image is linked to the image specified in the

        :param name: (experimental) Full name of the image that should be used. It should contain the Registry part if needed.
        :param alias: (experimental) Additional alias that can be used to access the service from the job's container. Read Accessing the services for more information.
        :param command: (experimental) Command or script that should be used as the container's command. It will be translated to arguments passed to Docker after the image's name. The syntax is similar to Dockerfile's CMD directive, where each shell token is a separate string in the array.
        :param entrypoint: (experimental) Command or script that should be executed as the container's entrypoint. It will be translated to Docker's --entrypoint option while creating the container. The syntax is similar to Dockerfile's ENTRYPOINT directive, where each shell token is a separate string in the array.
        :param pull_policy: (experimental) The pull policy that the runner uses to fetch the Docker image.
        :param variables: (experimental) Additional environment variables that are passed exclusively to the service..

        :see: https://docs.gitlab.com/ee/ci/yaml/#services
        :stability: experimental
        :Default: image keyword.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e209468a3f9aab6f0542611bc5e2b756bac42461413eaead1786a1b83ed3d27)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument pull_policy", value=pull_policy, expected_type=type_hints["pull_policy"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if alias is not None:
            self._values["alias"] = alias
        if command is not None:
            self._values["command"] = command
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if pull_policy is not None:
            self._values["pull_policy"] = pull_policy
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Full name of the image that should be used.

        It should contain the Registry part if needed.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''(experimental) Additional alias that can be used to access the service from the job's container.

        Read Accessing the services for more information.

        :stability: experimental
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Command or script that should be used as the container's command.

        It will be translated to arguments passed to Docker after the image's name. The syntax is similar to Dockerfile's CMD directive, where each shell token is a separate string in the array.

        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Command or script that should be executed as the container's entrypoint.

        It will be translated to Docker's --entrypoint option while creating the container. The syntax is similar to Dockerfile's ENTRYPOINT directive, where each shell token is a separate string in the array.

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pull_policy(self) -> typing.Optional[typing.List[PullPolicy]]:
        '''(experimental) The pull policy that the runner uses to fetch the Docker image.

        :stability: experimental
        '''
        result = self._values.get("pull_policy")
        return typing.cast(typing.Optional[typing.List[PullPolicy]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional environment variables that are passed exclusively to the service..

        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Service(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.Strategy")
class Strategy(enum.Enum):
    '''(experimental) You can mirror the pipeline status from the triggered pipeline to the source bridge job by using strategy: depend.

    :see: https://docs.gitlab.com/ee/ci/yaml/#triggerstrategy
    :stability: experimental
    '''

    DEPEND = "DEPEND"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.gitlab.Trigger",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "include": "include",
        "project": "project",
        "strategy": "strategy",
    },
)
class Trigger:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        include: typing.Optional[typing.Sequence[typing.Union["TriggerInclude", typing.Dict[builtins.str, typing.Any]]]] = None,
        project: typing.Optional[builtins.str] = None,
        strategy: typing.Optional[Strategy] = None,
    ) -> None:
        '''(experimental) Trigger a multi-project or a child pipeline.

        Read more:

        :param branch: (experimental) The branch name that a downstream pipeline will use.
        :param include: (experimental) A list of local files or artifacts from other jobs to define the pipeline.
        :param project: (experimental) Path to the project, e.g. ``group/project``, or ``group/sub-group/project``.
        :param strategy: (experimental) You can mirror the pipeline status from the triggered pipeline to the source bridge job by using strategy: depend.

        :see: https://docs.gitlab.com/ee/ci/yaml/README.html#trigger-syntax-for-child-pipeline
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aec6a6c462331cffb8d8af511a7a04ea96a7e260e03f8d857ba57103b6c89f)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if include is not None:
            self._values["include"] = include
        if project is not None:
            self._values["project"] = project
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch name that a downstream pipeline will use.

        :stability: experimental
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include(self) -> typing.Optional[typing.List["TriggerInclude"]]:
        '''(experimental) A list of local files or artifacts from other jobs to define the pipeline.

        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List["TriggerInclude"]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the project, e.g. ``group/project``, or ``group/sub-group/project``.

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strategy(self) -> typing.Optional[Strategy]:
        '''(experimental) You can mirror the pipeline status from the triggered pipeline to the source bridge job by using strategy: depend.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[Strategy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Trigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.TriggerInclude",
    jsii_struct_bases=[],
    name_mapping={
        "artifact": "artifact",
        "file": "file",
        "job": "job",
        "local": "local",
        "project": "project",
        "ref": "ref",
        "template": "template",
    },
)
class TriggerInclude:
    def __init__(
        self,
        *,
        artifact: typing.Optional[builtins.str] = None,
        file: typing.Optional[builtins.str] = None,
        job: typing.Optional[builtins.str] = None,
        local: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) References a local file or an artifact from another job to define the pipeline configuration.

        :param artifact: (experimental) Relative path to the generated YAML file which is extracted from the artifacts and used as the configuration for triggering the child pipeline.
        :param file: (experimental) Relative path from repository root (``/``) to the pipeline configuration YAML file.
        :param job: (experimental) Job name which generates the artifact.
        :param local: (experimental) Relative path from local repository root (``/``) to the local YAML file to define the pipeline configuration.
        :param project: (experimental) Path to another private project under the same GitLab instance, like ``group/project`` or ``group/sub-group/project``.
        :param ref: (experimental) Branch/Tag/Commit hash for the target project.
        :param template: (experimental) Name of the template YAML file to use in the pipeline configuration.

        :see: https://docs.gitlab.com/ee/ci/yaml/#triggerinclude
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf49e8ccbe3154c742f6f10df60e39266fb9481b0c26582426590bf8cd03e4b)
            check_type(argname="argument artifact", value=artifact, expected_type=type_hints["artifact"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifact is not None:
            self._values["artifact"] = artifact
        if file is not None:
            self._values["file"] = file
        if job is not None:
            self._values["job"] = job
        if local is not None:
            self._values["local"] = local
        if project is not None:
            self._values["project"] = project
        if ref is not None:
            self._values["ref"] = ref
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def artifact(self) -> typing.Optional[builtins.str]:
        '''(experimental) Relative path to the generated YAML file which is extracted from the artifacts and used as the configuration for triggering the child pipeline.

        :stability: experimental
        '''
        result = self._values.get("artifact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Relative path from repository root (``/``) to the pipeline configuration YAML file.

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job(self) -> typing.Optional[builtins.str]:
        '''(experimental) Job name which generates the artifact.

        :stability: experimental
        '''
        result = self._values.get("job")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local(self) -> typing.Optional[builtins.str]:
        '''(experimental) Relative path from local repository root (``/``) to the local YAML file to define the pipeline configuration.

        :stability: experimental
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to another private project under the same GitLab instance, like ``group/project`` or ``group/sub-group/project``.

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''(experimental) Branch/Tag/Commit hash for the target project.

        :stability: experimental
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the template YAML file to use in the pipeline configuration.

        :stability: experimental
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TriggerInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.VariableConfig",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "value": "value"},
)
class VariableConfig:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Explains what the global variable is used for, what the acceptable values are.

        :param description: (experimental) Define a global variable that is prefilled when running a pipeline manually. Must be used with value.
        :param value: (experimental) The variable value.

        :see: https://docs.gitlab.com/ee/ci/yaml/#variables
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270d3442d2c5b9f18e475ba2c945ca5765ee61ed94c5ea28d4395b9c3952df58)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Define a global variable that is prefilled when running a pipeline manually.

        Must be used with value.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The variable value.

        :stability: experimental
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VariableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.VaultConfig",
    jsii_struct_bases=[],
    name_mapping={"engine": "engine", "field": "field", "path": "path"},
)
class VaultConfig:
    def __init__(
        self,
        *,
        engine: typing.Union[Engine, typing.Dict[builtins.str, typing.Any]],
        field: builtins.str,
        path: builtins.str,
    ) -> None:
        '''(experimental) Specification for a secret provided by a HashiCorp Vault.

        :param engine: 
        :param field: 
        :param path: (experimental) Path to the secret.

        :see: https://www.vaultproject.io/
        :stability: experimental
        '''
        if isinstance(engine, dict):
            engine = Engine(**engine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf8b88995e7b236e0548afd560041fc8de683c71708218ce1af2818efd3b248)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
            "field": field,
            "path": path,
        }

    @builtins.property
    def engine(self) -> Engine:
        '''
        :stability: experimental
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(Engine, result)

    @builtins.property
    def field(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Path to the secret.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.Workflow",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rules": "rules"},
)
class Workflow:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["WorkflowRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Used to control pipeline behavior.

        :param name: (experimental) You can use name to define a name for pipelines.
        :param rules: (experimental) Used to control whether or not a whole pipeline is created.

        :see: https://docs.gitlab.com/ee/ci/yaml/#workflow
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b75047f6bf7eb788b08fc007a66573480a38e913bde351acaac05347d467b1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use name to define a name for pipelines.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["WorkflowRule"]]:
        '''(experimental) Used to control whether or not a whole pipeline is created.

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["WorkflowRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Workflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.gitlab.WorkflowRule",
    jsii_struct_bases=[],
    name_mapping={
        "changes": "changes",
        "exists": "exists",
        "if_": "if",
        "variables": "variables",
        "when": "when",
    },
)
class WorkflowRule:
    def __init__(
        self,
        *,
        changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exists: typing.Optional[typing.Sequence[builtins.str]] = None,
        if_: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]] = None,
        when: typing.Optional["WorkflowWhen"] = None,
    ) -> None:
        '''(experimental) Used to control whether or not a whole pipeline is created.

        :param changes: 
        :param exists: 
        :param if_: 
        :param variables: 
        :param when: 

        :see: https://docs.gitlab.com/ee/ci/yaml/#workflowrules
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a2cf4c2a982a749d12511d9e43468f3b4a9cca16d6c56d9a2cfd1154720d63)
            check_type(argname="argument changes", value=changes, expected_type=type_hints["changes"])
            check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if changes is not None:
            self._values["changes"] = changes
        if exists is not None:
            self._values["exists"] = exists
        if if_ is not None:
            self._values["if_"] = if_
        if variables is not None:
            self._values["variables"] = variables
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def changes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("changes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("exists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]], result)

    @builtins.property
    def when(self) -> typing.Optional["WorkflowWhen"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["WorkflowWhen"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.gitlab.WorkflowWhen")
class WorkflowWhen(enum.Enum):
    '''(experimental) Describes the conditions for when to run the job.

    Defaults to 'on_success'.
    The value can only be 'always' or 'never' when used with workflow.

    :see: https://docs.gitlab.com/ee/ci/yaml/#workflowrules
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''
    :stability: experimental
    '''
    NEVER = "NEVER"
    '''
    :stability: experimental
    '''


__all__ = [
    "Action",
    "AllowFailure",
    "Artifacts",
    "Assets",
    "Cache",
    "CacheKeyFiles",
    "CachePolicy",
    "CacheWhen",
    "CiConfiguration",
    "CiConfigurationOptions",
    "CoverageReport",
    "Default",
    "DefaultElement",
    "DeploymentTier",
    "Engine",
    "Environment",
    "Filter",
    "GitlabConfiguration",
    "IDToken",
    "Image",
    "Include",
    "IncludeRule",
    "Inherit",
    "Job",
    "JobWhen",
    "KubernetesConfig",
    "KubernetesEnum",
    "Link",
    "LinkType",
    "Need",
    "NestedConfiguration",
    "Parallel",
    "PullPolicy",
    "Release",
    "Reports",
    "Retry",
    "Secret",
    "Service",
    "Strategy",
    "Trigger",
    "TriggerInclude",
    "VariableConfig",
    "VaultConfig",
    "Workflow",
    "WorkflowRule",
    "WorkflowWhen",
]

publication.publish()

def _typecheckingstub__33f2c30cde1aebaa83de097243717ad8dd6d1c2617b47a4352cbe7e3f351e8b2(
    *,
    exit_codes: typing.Union[jsii.Number, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d84c68910ff0d2af18be53491f5cbfd0be88648ace2dce10c35c510d498acc(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    expire_in: typing.Optional[builtins.str] = None,
    expose_as: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    reports: typing.Optional[typing.Union[Reports, typing.Dict[builtins.str, typing.Any]]] = None,
    untracked: typing.Optional[builtins.bool] = None,
    when: typing.Optional[CacheWhen] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad15c870fe49288bda1a98e1bfc9db5f862289de2ad5ad62e4c59ce4aab4c73(
    *,
    links: typing.Sequence[typing.Union[Link, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f049681df3dccf35653843c544e06258271520db12493e48ac936a96ecedad(
    *,
    fallback_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Union[builtins.str, typing.Union[CacheKeyFiles, typing.Dict[builtins.str, typing.Any]]]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy: typing.Optional[CachePolicy] = None,
    untracked: typing.Optional[builtins.bool] = None,
    when: typing.Optional[CacheWhen] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fa76bc1e2253fd95df81fb7b93982051b240cea93ead52d9d95535eeb6f760(
    *,
    files: typing.Sequence[builtins.str],
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231c30bc513f8e09e345dd63392e7c50f479df9f480fc36e03e88fc4a5e8cd68(
    project: _Project_57d89203,
    name: builtins.str,
    *,
    default: typing.Optional[typing.Union[Default, typing.Dict[builtins.str, typing.Any]]] = None,
    jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union[Job, typing.Dict[builtins.str, typing.Any]]]] = None,
    pages: typing.Optional[typing.Union[Job, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow: typing.Optional[typing.Union[Workflow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8dc83f6ed2c3927eac45893c863050843bdea6a919dceda0aeb811aab6b03a(
    caches: typing.Sequence[typing.Union[Cache, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a532b9d3becbdcec0a292538a067f3ddc6a037abdf523500485dc53041825c03(
    variables: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bca3189ad53bb4a2659a3c4be7c233788dfd0d6d0e32255e52d6e6d46261ebd(
    *includes: Include,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f426ddc0c125aabe74a08ecc4ad008c2d2b5b44ef9240f0a0e99c04a9680ae18(
    jobs: typing.Mapping[builtins.str, typing.Union[Job, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee886ab66358cc25f75eaff5dcbeba2e03d5f72db8d7d299360af81453428f9b(
    *services: Service,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37256713bb8d361966f0b39f4dba8aac446f1eea7da27fabd8e9ea6833933c6(
    *stages: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad6204d94421a2493e44c6131e44e9ac2175546be72d0e655df762520673c9e(
    *,
    default: typing.Optional[typing.Union[Default, typing.Dict[builtins.str, typing.Any]]] = None,
    jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union[Job, typing.Dict[builtins.str, typing.Any]]]] = None,
    pages: typing.Optional[typing.Union[Job, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow: typing.Optional[typing.Union[Workflow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fb846daac000cdcb6374acd70ebc7323f86761a31c2ebb2ef0d1b49a3f0652(
    *,
    coverage_format: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e71d01eda90297db6af675f51033414546212b06d49c00c218dee2071d1ed1(
    *,
    after_script: typing.Optional[typing.Sequence[builtins.str]] = None,
    artifacts: typing.Optional[typing.Union[Artifacts, typing.Dict[builtins.str, typing.Any]]] = None,
    before_script: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache: typing.Optional[typing.Sequence[typing.Union[Cache, typing.Dict[builtins.str, typing.Any]]]] = None,
    id_tokens: typing.Optional[typing.Mapping[builtins.str, IDToken]] = None,
    image: typing.Optional[typing.Union[Image, typing.Dict[builtins.str, typing.Any]]] = None,
    interruptible: typing.Optional[builtins.bool] = None,
    retry: typing.Optional[typing.Union[Retry, typing.Dict[builtins.str, typing.Any]]] = None,
    services: typing.Optional[typing.Sequence[typing.Union[Service, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4574deb50cf9019e113c67d714da29685143324fc4e1df06c5ea08a874de8223(
    *,
    name: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dacf066520edebcaf1914cf8b47a539d32b601c728c745a9821da18fc61c311(
    *,
    name: builtins.str,
    action: typing.Optional[Action] = None,
    auto_stop_in: typing.Optional[builtins.str] = None,
    deployment_tier: typing.Optional[DeploymentTier] = None,
    kubernetes: typing.Optional[typing.Union[KubernetesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    on_stop: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db895e6728876de5be75625df8be94a8c86846327b2443ff1fd7c8c09dc4d6f2(
    *,
    changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    kubernetes: typing.Optional[KubernetesEnum] = None,
    refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    variables: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7c22b752837d5c419877611c3664caa886539ab5209465bbfe27372b51e714(
    project: _Project_57d89203,
    *,
    default: typing.Optional[typing.Union[Default, typing.Dict[builtins.str, typing.Any]]] = None,
    jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union[Job, typing.Dict[builtins.str, typing.Any]]]] = None,
    pages: typing.Optional[typing.Union[Job, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow: typing.Optional[typing.Union[Workflow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e89c004dae5dc8a66477f9e05d4202e2de25b397ad58439158d4d0e311fa46(
    config: typing.Mapping[builtins.str, typing.Union[CiConfigurationOptions, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e6bbd7c1d3e16ffa82367cdd5ca16ce06a42726f4193639790a39bb2eadef9(
    value: typing.Union[builtins.str, typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db043de1bfd971cf362a1d5015d39fcfec9ce12a8564e12b3dc83c2766f5e7f(
    *,
    name: builtins.str,
    entrypoint: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b4b33f824dede3c51f8491f23c1b24aa99de8902ab2b0adb792fbc13ddf8fe(
    *,
    file: typing.Optional[typing.Sequence[builtins.str]] = None,
    local: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
    remote: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[IncludeRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5547025bbe422124f59e782b7141894ba37dbf0049070c73b17f39de1d1843a1(
    *,
    allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Union[AllowFailure, typing.Dict[builtins.str, typing.Any]]]] = None,
    changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exists: typing.Optional[typing.Sequence[builtins.str]] = None,
    if_: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_in: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    when: typing.Optional[JobWhen] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e202056f8d0ee046415cdd0eeba7b03d414bbd38fc367909020c4d2d2766cf(
    *,
    default: typing.Optional[typing.Union[builtins.bool, typing.Sequence[DefaultElement]]] = None,
    variables: typing.Optional[typing.Union[builtins.bool, typing.Sequence[builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485afb8ca4cf12bdaab3c3455c7b90f3ea9d549eb87ec6fd05eae046f3f38bd6(
    *,
    after_script: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Union[AllowFailure, typing.Dict[builtins.str, typing.Any]]]] = None,
    artifacts: typing.Optional[typing.Union[Artifacts, typing.Dict[builtins.str, typing.Any]]] = None,
    before_script: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache: typing.Optional[typing.Sequence[typing.Union[Cache, typing.Dict[builtins.str, typing.Any]]]] = None,
    coverage: typing.Optional[builtins.str] = None,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[builtins.str, typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]]] = None,
    except_: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Union[Filter, typing.Dict[builtins.str, typing.Any]]]] = None,
    extends: typing.Optional[typing.Sequence[builtins.str]] = None,
    id_tokens: typing.Optional[typing.Mapping[builtins.str, IDToken]] = None,
    image: typing.Optional[typing.Union[Image, typing.Dict[builtins.str, typing.Any]]] = None,
    inherit: typing.Optional[typing.Union[Inherit, typing.Dict[builtins.str, typing.Any]]] = None,
    interruptible: typing.Optional[builtins.bool] = None,
    needs: typing.Optional[typing.Sequence[typing.Union[builtins.str, typing.Union[Need, typing.Dict[builtins.str, typing.Any]]]]] = None,
    only: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Union[Filter, typing.Dict[builtins.str, typing.Any]]]] = None,
    parallel: typing.Optional[typing.Union[jsii.Number, typing.Union[Parallel, typing.Dict[builtins.str, typing.Any]]]] = None,
    release: typing.Optional[typing.Union[Release, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_group: typing.Optional[builtins.str] = None,
    retry: typing.Optional[typing.Union[Retry, typing.Dict[builtins.str, typing.Any]]] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[IncludeRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    script: typing.Optional[typing.Sequence[builtins.str]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Union[Secret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    services: typing.Optional[typing.Sequence[typing.Union[Service, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage: typing.Optional[builtins.str] = None,
    start_in: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[typing.Union[builtins.str, typing.Union[Trigger, typing.Dict[builtins.str, typing.Any]]]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    when: typing.Optional[JobWhen] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5135e122b0fb90c5ae5d8c65626715c279ba6c8bb4103d4bd7a12969d1f5ad(
    *,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003677e3874ed26747f048e8b5c08a32b87f0226f3522c10b0844ade2521966c(
    *,
    name: builtins.str,
    url: builtins.str,
    filepath: typing.Optional[builtins.str] = None,
    link_type: typing.Optional[LinkType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62a8b5d59de20d0811a6eb2ae8ef5a38099d2a9da0ebfd9c9ce8d1406ce4f8e(
    *,
    job: builtins.str,
    artifacts: typing.Optional[builtins.bool] = None,
    optional: typing.Optional[builtins.bool] = None,
    pipeline: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d7f1d8d243fb7e275a0eeba3f1419822bf2c274e47641e553a5675c002a437(
    project: _Project_57d89203,
    parent: GitlabConfiguration,
    name: builtins.str,
    *,
    default: typing.Optional[typing.Union[Default, typing.Dict[builtins.str, typing.Any]]] = None,
    jobs: typing.Optional[typing.Mapping[builtins.str, typing.Union[Job, typing.Dict[builtins.str, typing.Any]]]] = None,
    pages: typing.Optional[typing.Union[Job, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow: typing.Optional[typing.Union[Workflow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27837ae5c9e058eb0806d1abd6557c3fa362e2df59dcab8ce1db5416c00525e1(
    *,
    matrix: typing.Sequence[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38e7545caf21650d3fd8d9c8672f7ac49978e130308eff721d262f5ca861d93(
    *,
    description: builtins.str,
    tag_name: builtins.str,
    assets: typing.Optional[typing.Union[Assets, typing.Dict[builtins.str, typing.Any]]] = None,
    milestones: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
    released_at: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f4030cd6e6d9c8988080afe12341d674a6d0751da1c7937dd3901c9d6062c(
    *,
    cobertura: typing.Optional[typing.Sequence[builtins.str]] = None,
    codequality: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_scanning: typing.Optional[typing.Sequence[builtins.str]] = None,
    coverage_report: typing.Optional[typing.Union[CoverageReport, typing.Dict[builtins.str, typing.Any]]] = None,
    dast: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_scanning: typing.Optional[typing.Sequence[builtins.str]] = None,
    dotenv: typing.Optional[typing.Sequence[builtins.str]] = None,
    junit: typing.Optional[typing.Sequence[builtins.str]] = None,
    license_management: typing.Optional[typing.Sequence[builtins.str]] = None,
    license_scanning: typing.Optional[typing.Sequence[builtins.str]] = None,
    lsif: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    performance: typing.Optional[typing.Sequence[builtins.str]] = None,
    requirements: typing.Optional[typing.Sequence[builtins.str]] = None,
    sast: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_detection: typing.Optional[typing.Sequence[builtins.str]] = None,
    terraform: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbb57c0c914d3fe61ad0fc30c66b1fa89242257ae2e7fbd309e5819250ac25e(
    *,
    max: typing.Optional[jsii.Number] = None,
    when: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789ab87a937f7529123f7dfe15f4731fb2ba2cd3529681a1c5b7c2766ac518ed(
    *,
    vault: typing.Union[VaultConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e209468a3f9aab6f0542611bc5e2b756bac42461413eaead1786a1b83ed3d27(
    *,
    name: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_policy: typing.Optional[typing.Sequence[PullPolicy]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aec6a6c462331cffb8d8af511a7a04ea96a7e260e03f8d857ba57103b6c89f(
    *,
    branch: typing.Optional[builtins.str] = None,
    include: typing.Optional[typing.Sequence[typing.Union[TriggerInclude, typing.Dict[builtins.str, typing.Any]]]] = None,
    project: typing.Optional[builtins.str] = None,
    strategy: typing.Optional[Strategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf49e8ccbe3154c742f6f10df60e39266fb9481b0c26582426590bf8cd03e4b(
    *,
    artifact: typing.Optional[builtins.str] = None,
    file: typing.Optional[builtins.str] = None,
    job: typing.Optional[builtins.str] = None,
    local: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270d3442d2c5b9f18e475ba2c945ca5765ee61ed94c5ea28d4395b9c3952df58(
    *,
    description: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf8b88995e7b236e0548afd560041fc8de683c71708218ce1af2818efd3b248(
    *,
    engine: typing.Union[Engine, typing.Dict[builtins.str, typing.Any]],
    field: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b75047f6bf7eb788b08fc007a66573480a38e913bde351acaac05347d467b1(
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[WorkflowRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a2cf4c2a982a749d12511d9e43468f3b4a9cca16d6c56d9a2cfd1154720d63(
    *,
    changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exists: typing.Optional[typing.Sequence[builtins.str]] = None,
    if_: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number]]] = None,
    when: typing.Optional[WorkflowWhen] = None,
) -> None:
    """Type checking stubs"""
    pass
