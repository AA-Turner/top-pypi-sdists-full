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
    Dependency as _Dependency_f510e013,
    GitOptions as _GitOptions_a65916a3,
    IgnoreFileOptions as _IgnoreFileOptions_86c48b91,
    LoggerOptions as _LoggerOptions_eb0f6309,
    Project as _Project_57d89203,
    ProjectType as _ProjectType_fd80c725,
    ProjenrcFile as _ProjenrcFile_50432c7e,
    ProjenrcJsonOptions as _ProjenrcJsonOptions_9c40dd4f,
    RenovatebotOptions as _RenovatebotOptions_18e6b8a1,
    SampleReadmeProps as _SampleReadmeProps_3518b03b,
)
from ..github import (
    AutoApproveOptions as _AutoApproveOptions_dac86cbe,
    AutoMergeOptions as _AutoMergeOptions_d112cd3c,
    GitHubOptions as _GitHubOptions_21553699,
    GitHubProject as _GitHubProject_c48bc7ea,
    GitHubProjectOptions as _GitHubProjectOptions_547f2d08,
    GithubCredentials as _GithubCredentials_ae257072,
    MergifyOptions as _MergifyOptions_a6faaab3,
    StaleOptions as _StaleOptions_929db764,
)


@jsii.enum(jsii_type="projen.java.ChecksumPolicy")
class ChecksumPolicy(enum.Enum):
    '''
    :stability: experimental
    '''

    IGNORE = "IGNORE"
    '''
    :stability: experimental
    '''
    FAIL = "FAIL"
    '''
    :stability: experimental
    '''
    WARN = "WARN"
    '''
    :stability: experimental
    '''


class JavaProject(
    _GitHubProject_c48bc7ea,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.java.JavaProject",
):
    '''(experimental) Java project.

    :stability: experimental
    :pjid: java
    '''

    def __init__(
        self,
        *,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        compile_options: typing.Optional[typing.Union["MavenCompileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        distdir: typing.Optional[builtins.str] = None,
        junit: typing.Optional[builtins.bool] = None,
        junit_options: typing.Optional[typing.Union["JunitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        packaging_options: typing.Optional[typing.Union["MavenPackagingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_java: typing.Optional[builtins.bool] = None,
        projenrc_java_options: typing.Optional[typing.Union["ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_ProjectType_fd80c725] = None,
        projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        artifact_id: builtins.str,
        group_id: builtins.str,
        version: builtins.str,
        description: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        parent_pom: typing.Optional[typing.Union["ParentPom", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_Project_57d89203] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>`` Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param junit: (experimental) Include junit tests. Default: true
        :param junit_options: (experimental) junit options. Default: - defaults
        :param packaging_options: (experimental) Packaging options. Default: - defaults
        :param projenrc_java: (experimental) Use projenrc in java. This will install ``projen`` as a java dependency and will add a ``synth`` task which will compile & execute ``main()`` from ``src/main/java/projenrc.java``. Default: true
        :param projenrc_java_options: (experimental) Options related to projenrc in java. Default: - default options
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>`` Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options

        :stability: experimental
        '''
        options = JavaProjectOptions(
            sample=sample,
            sample_java_package=sample_java_package,
            compile_options=compile_options,
            deps=deps,
            distdir=distdir,
            junit=junit,
            junit_options=junit_options,
            packaging_options=packaging_options,
            projenrc_java=projenrc_java,
            projenrc_java_options=projenrc_java_options,
            test_deps=test_deps,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            clobber=clobber,
            dev_container=dev_container,
            github=github,
            github_options=github_options,
            gitpod=gitpod,
            mergify=mergify,
            mergify_options=mergify_options,
            project_type=project_type,
            projen_credentials=projen_credentials,
            projen_token_secret=projen_token_secret,
            readme=readme,
            stale=stale,
            stale_options=stale_options,
            vscode=vscode,
            artifact_id=artifact_id,
            group_id=group_id,
            version=version,
            description=description,
            packaging=packaging,
            parent_pom=parent_pom,
            url=url,
            name=name,
            commit_generated=commit_generated,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            logging=logging,
            outdir=outdir,
            parent=parent,
            projen_command=projen_command,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, spec: builtins.str) -> None:
        '''(experimental) Adds a runtime dependency.

        :param spec: Format ``<groupId>/<artifactId>@<semver>``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3cde13045b969d2a5e4bfbf540cdcead81b701c879b4079ebdf703d31d185aa)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        return typing.cast(None, jsii.invoke(self, "addDependency", [spec]))

    @jsii.member(jsii_name="addPlugin")
    def add_plugin(
        self,
        spec: builtins.str,
        *,
        configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        executions: typing.Optional[typing.Sequence[typing.Union["PluginExecution", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _Dependency_f510e013:
        '''(experimental) Adds a build plugin to the pom.

        The plug in is also added as a BUILD dep to the project.

        :param spec: dependency spec (``group/artifact@version``).
        :param configuration: (experimental) Plugin key/value configuration. Default: {}
        :param dependencies: (experimental) You could configure the dependencies for the plugin. Dependencies are in ``<groupId>/<artifactId>@<semver>`` format. Default: []
        :param executions: (experimental) Plugin executions. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d82566ec5da4a4ff8c5ec4f7442835fb01d67e916c8cdb64dc6ed08d10a361c)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        options = PluginOptions(
            configuration=configuration,
            dependencies=dependencies,
            executions=executions,
        )

        return typing.cast(_Dependency_f510e013, jsii.invoke(self, "addPlugin", [spec, options]))

    @jsii.member(jsii_name="addTestDependency")
    def add_test_dependency(self, spec: builtins.str) -> None:
        '''(experimental) Adds a test dependency.

        :param spec: Format ``<groupId>/<artifactId>@<semver>``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702d880972766245e6e0ce9d4332f75632d1c9f56321a84f3b10f119ec91dcd0)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        return typing.cast(None, jsii.invoke(self, "addTestDependency", [spec]))

    @builtins.property
    @jsii.member(jsii_name="compile")
    def compile(self) -> "MavenCompile":
        '''(experimental) Compile component.

        :stability: experimental
        '''
        return typing.cast("MavenCompile", jsii.get(self, "compile"))

    @builtins.property
    @jsii.member(jsii_name="distdir")
    def distdir(self) -> builtins.str:
        '''(experimental) Maven artifact output directory.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distdir"))

    @builtins.property
    @jsii.member(jsii_name="packaging")
    def packaging(self) -> "MavenPackaging":
        '''(experimental) Packaging component.

        :stability: experimental
        '''
        return typing.cast("MavenPackaging", jsii.get(self, "packaging"))

    @builtins.property
    @jsii.member(jsii_name="pom")
    def pom(self) -> "Pom":
        '''(experimental) API for managing ``pom.xml``.

        :stability: experimental
        '''
        return typing.cast("Pom", jsii.get(self, "pom"))

    @builtins.property
    @jsii.member(jsii_name="junit")
    def junit(self) -> typing.Optional["Junit"]:
        '''(experimental) JUnit component.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Junit"], jsii.get(self, "junit"))

    @builtins.property
    @jsii.member(jsii_name="projenrc")
    def projenrc(self) -> typing.Optional["Projenrc"]:
        '''(experimental) Projenrc component.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Projenrc"], jsii.get(self, "projenrc"))


class Junit(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.java.Junit",
):
    '''(experimental) Implements JUnit-based testing.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        pom: "Pom",
        sample_java_package: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param pom: (experimental) Java pom.
        :param sample_java_package: (experimental) Java package for test sample. Default: "org.acme"
        :param version: (experimental) Junit version. Default: "5.7.0"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877c5aed063e2ddca6cbb37631bb31564c14fc1f304629ab7adcc662faa0b0da)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = JunitOptions(
            pom=pom, sample_java_package=sample_java_package, version=version
        )

        jsii.create(self.__class__, self, [project, options])


@jsii.data_type(
    jsii_type="projen.java.JunitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "pom": "pom",
        "sample_java_package": "sampleJavaPackage",
        "version": "version",
    },
)
class JunitOptions:
    def __init__(
        self,
        *,
        pom: "Pom",
        sample_java_package: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``Junit``.

        :param pom: (experimental) Java pom.
        :param sample_java_package: (experimental) Java package for test sample. Default: "org.acme"
        :param version: (experimental) Junit version. Default: "5.7.0"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db441a323339ae146e69254287868e3704cd5ee3edbcc272138a4e660f9e4c72)
            check_type(argname="argument pom", value=pom, expected_type=type_hints["pom"])
            check_type(argname="argument sample_java_package", value=sample_java_package, expected_type=type_hints["sample_java_package"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pom": pom,
        }
        if sample_java_package is not None:
            self._values["sample_java_package"] = sample_java_package
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def pom(self) -> "Pom":
        '''(experimental) Java pom.

        :stability: experimental
        '''
        result = self._values.get("pom")
        assert result is not None, "Required property 'pom' is missing"
        return typing.cast("Pom", result)

    @builtins.property
    def sample_java_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) Java package for test sample.

        :default: "org.acme"

        :stability: experimental
        '''
        result = self._values.get("sample_java_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Junit version.

        :default: "5.7.0"

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JunitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MavenCompile(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.java.MavenCompile",
):
    '''(experimental) Adds the maven-compiler plugin to a POM file and the ``compile`` task.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        pom: "Pom",
        *,
        source: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param pom: -
        :param source: (experimental) Source language version. Default: "1.8"
        :param target: (experimental) Target JVM version. Default: "1.8"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f143440a0c274a37fff9c951ad85be29c31b978c6c6d89ee2cbe127b8249b88)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pom", value=pom, expected_type=type_hints["pom"])
        options = MavenCompileOptions(source=source, target=target)

        jsii.create(self.__class__, self, [project, pom, options])


@jsii.data_type(
    jsii_type="projen.java.MavenCompileOptions",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "target": "target"},
)
class MavenCompileOptions:
    def __init__(
        self,
        *,
        source: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``MavenCompile``.

        :param source: (experimental) Source language version. Default: "1.8"
        :param target: (experimental) Target JVM version. Default: "1.8"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abc628703576e622a20aab761493d186a662ac606df5bccb664dfe4f41a9240)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''(experimental) Source language version.

        :default: "1.8"

        :stability: experimental
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target JVM version.

        :default: "1.8"

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MavenCompileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MavenPackaging(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.java.MavenPackaging",
):
    '''(experimental) Configures a maven project to produce a .jar archive with sources and javadocs.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        pom: "Pom",
        *,
        distdir: typing.Optional[builtins.str] = None,
        javadocs: typing.Optional[builtins.bool] = None,
        javadocs_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        sources: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param pom: -
        :param distdir: (experimental) Where to place the package output? Default: "dist/java"
        :param javadocs: (experimental) Include javadocs jar in package. Default: true
        :param javadocs_exclude: (experimental) Exclude source files from docs. Default: []
        :param sources: (experimental) Include sources jar in package. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7f0f4d617b106a57e5b073cf5f51ca4195a66d251926fe0b5b0fa27b2b7612)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pom", value=pom, expected_type=type_hints["pom"])
        options = MavenPackagingOptions(
            distdir=distdir,
            javadocs=javadocs,
            javadocs_exclude=javadocs_exclude,
            sources=sources,
        )

        jsii.create(self.__class__, self, [project, pom, options])

    @builtins.property
    @jsii.member(jsii_name="distdir")
    def distdir(self) -> builtins.str:
        '''(experimental) The directory containing the package output, relative to the project outdir.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distdir"))


@jsii.data_type(
    jsii_type="projen.java.MavenPackagingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "distdir": "distdir",
        "javadocs": "javadocs",
        "javadocs_exclude": "javadocsExclude",
        "sources": "sources",
    },
)
class MavenPackagingOptions:
    def __init__(
        self,
        *,
        distdir: typing.Optional[builtins.str] = None,
        javadocs: typing.Optional[builtins.bool] = None,
        javadocs_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        sources: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``MavenPackage``.

        :param distdir: (experimental) Where to place the package output? Default: "dist/java"
        :param javadocs: (experimental) Include javadocs jar in package. Default: true
        :param javadocs_exclude: (experimental) Exclude source files from docs. Default: []
        :param sources: (experimental) Include sources jar in package. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69d38d3cd60ee77b03f102371324cf8c453ac910fe11ed85622f44a7358057a)
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument javadocs", value=javadocs, expected_type=type_hints["javadocs"])
            check_type(argname="argument javadocs_exclude", value=javadocs_exclude, expected_type=type_hints["javadocs_exclude"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if distdir is not None:
            self._values["distdir"] = distdir
        if javadocs is not None:
            self._values["javadocs"] = javadocs
        if javadocs_exclude is not None:
            self._values["javadocs_exclude"] = javadocs_exclude
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def distdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Where to place the package output?

        :default: "dist/java"

        :stability: experimental
        '''
        result = self._values.get("distdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def javadocs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include javadocs jar in package.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("javadocs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def javadocs_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Exclude source files from docs.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("javadocs_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sources(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include sources jar in package.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MavenPackagingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.java.MavenRepository",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "url": "url",
        "layout": "layout",
        "name": "name",
        "releases": "releases",
        "snapshots": "snapshots",
    },
)
class MavenRepository:
    def __init__(
        self,
        *,
        id: builtins.str,
        url: builtins.str,
        layout: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        releases: typing.Optional[typing.Union["MavenRepositoryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshots: typing.Optional[typing.Union["MavenRepositoryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Represents a Maven repository.

        :param id: (experimental) The identifier for the repository.
        :param url: (experimental) The url of the repository.
        :param layout: (experimental) The layout of the repository.
        :param name: (experimental) The name of the repository.
        :param releases: (experimental) Repository Policy for Releases.
        :param snapshots: (experimental) Repository Policy for Snapshots.

        :see: https://maven.apache.org/guides/introduction/introduction-to-repositories.html
        :stability: experimental
        '''
        if isinstance(releases, dict):
            releases = MavenRepositoryPolicy(**releases)
        if isinstance(snapshots, dict):
            snapshots = MavenRepositoryPolicy(**snapshots)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e8ee88cd330385feef214bd08b3bc44314dc15ddbcd48e4f74c198bda84bde)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument layout", value=layout, expected_type=type_hints["layout"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument releases", value=releases, expected_type=type_hints["releases"])
            check_type(argname="argument snapshots", value=snapshots, expected_type=type_hints["snapshots"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "url": url,
        }
        if layout is not None:
            self._values["layout"] = layout
        if name is not None:
            self._values["name"] = name
        if releases is not None:
            self._values["releases"] = releases
        if snapshots is not None:
            self._values["snapshots"] = snapshots

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) The identifier for the repository.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The url of the repository.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def layout(self) -> typing.Optional[builtins.str]:
        '''(experimental) The layout of the repository.

        :stability: experimental
        '''
        result = self._values.get("layout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def releases(self) -> typing.Optional["MavenRepositoryPolicy"]:
        '''(experimental) Repository Policy for Releases.

        :stability: experimental
        '''
        result = self._values.get("releases")
        return typing.cast(typing.Optional["MavenRepositoryPolicy"], result)

    @builtins.property
    def snapshots(self) -> typing.Optional["MavenRepositoryPolicy"]:
        '''(experimental) Repository Policy for Snapshots.

        :stability: experimental
        '''
        result = self._values.get("snapshots")
        return typing.cast(typing.Optional["MavenRepositoryPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MavenRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.java.MavenRepositoryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "checksum_policy": "checksumPolicy",
        "enabled": "enabled",
        "update_policy": "updatePolicy",
    },
)
class MavenRepositoryPolicy:
    def __init__(
        self,
        *,
        checksum_policy: typing.Optional[ChecksumPolicy] = None,
        enabled: typing.Optional[builtins.bool] = None,
        update_policy: typing.Optional["UpdatePolicy"] = None,
    ) -> None:
        '''(experimental) Represents a Maven Repository Policy.

        :param checksum_policy: (experimental) Checksum Policy When Maven deploys files to the repository, it also deploys corresponding checksum files.
        :param enabled: 
        :param update_policy: (experimental) Update Policy This element specifies how often updates should attempt to occur. Maven will compare the local POM's timestamp (stored in a repository's maven-metadata file) to the remote. Default: UpdatePolicy.DAILY

        :see: https://maven.apache.org/settings.html#repositories
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041e104cddeb68a13d0b79cfdce8653000ee58d2c7cef3088a2c8717d7f02ebf)
            check_type(argname="argument checksum_policy", value=checksum_policy, expected_type=type_hints["checksum_policy"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument update_policy", value=update_policy, expected_type=type_hints["update_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if checksum_policy is not None:
            self._values["checksum_policy"] = checksum_policy
        if enabled is not None:
            self._values["enabled"] = enabled
        if update_policy is not None:
            self._values["update_policy"] = update_policy

    @builtins.property
    def checksum_policy(self) -> typing.Optional[ChecksumPolicy]:
        '''(experimental) Checksum Policy When Maven deploys files to the repository, it also deploys corresponding checksum files.

        :stability: experimental
        '''
        result = self._values.get("checksum_policy")
        return typing.cast(typing.Optional[ChecksumPolicy], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_policy(self) -> typing.Optional["UpdatePolicy"]:
        '''(experimental) Update Policy This element specifies how often updates should attempt to occur.

        Maven will compare the local POM's timestamp (stored in a repository's maven-metadata file) to the remote.

        :default: UpdatePolicy.DAILY

        :stability: experimental
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional["UpdatePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MavenRepositoryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MavenSample(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.java.MavenSample",
):
    '''(experimental) Java code sample.

    :stability: experimental
    '''

    def __init__(self, project: _Project_57d89203, *, package: builtins.str) -> None:
        '''
        :param project: -
        :param package: (experimental) Project root java package.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4190861db7ca6169340394602246875f9668e86624764e5e7279d01f6c2a3017)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = MavenSampleOptions(package=package)

        jsii.create(self.__class__, self, [project, options])


@jsii.data_type(
    jsii_type="projen.java.MavenSampleOptions",
    jsii_struct_bases=[],
    name_mapping={"package": "package"},
)
class MavenSampleOptions:
    def __init__(self, *, package: builtins.str) -> None:
        '''
        :param package: (experimental) Project root java package.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be9d5c5edaace101d0e427b56fb2e89f3b2e6ac01bd59e3cb1d0743d9293524)
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package": package,
        }

    @builtins.property
    def package(self) -> builtins.str:
        '''(experimental) Project root java package.

        :stability: experimental
        '''
        result = self._values.get("package")
        assert result is not None, "Required property 'package' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MavenSampleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.java.ParentPom",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "group_id": "groupId",
        "relative_path": "relativePath",
        "version": "version",
    },
)
class ParentPom:
    def __init__(
        self,
        *,
        artifact_id: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        relative_path: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: (experimental) Parent Pom Artifact ID.
        :param group_id: (experimental) Parent Pom Group ID.
        :param relative_path: (experimental) Parent Pom Relative path from the current pom.
        :param version: (experimental) Parent Pom Version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f47e5dc92031bfaa3a639437d282aedc130d8a3857314c5a71a2ca063798f40)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument relative_path", value=relative_path, expected_type=type_hints["relative_path"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifact_id is not None:
            self._values["artifact_id"] = artifact_id
        if group_id is not None:
            self._values["group_id"] = group_id
        if relative_path is not None:
            self._values["relative_path"] = relative_path
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def artifact_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parent Pom Artifact ID.

        :stability: experimental
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parent Pom Group ID.

        :stability: experimental
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relative_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parent Pom Relative path from the current pom.

        :stability: experimental
        '''
        result = self._values.get("relative_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parent Pom Version.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParentPom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.java.PluginExecution",
    jsii_struct_bases=[],
    name_mapping={
        "goals": "goals",
        "id": "id",
        "configuration": "configuration",
        "phase": "phase",
    },
)
class PluginExecution:
    def __init__(
        self,
        *,
        goals: typing.Sequence[builtins.str],
        id: builtins.str,
        configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        phase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Plugin execution definition.

        :param goals: (experimental) Which Maven goals this plugin should be associated with.
        :param id: (experimental) The ID.
        :param configuration: (experimental) Execution key/value configuration. Default: {}
        :param phase: (experimental) The phase in which the plugin should execute.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b1bc2eb1ab79c9e54c8b62fd341a87dd82eec6a2b2ec76a5fdb6f1c51d5444)
            check_type(argname="argument goals", value=goals, expected_type=type_hints["goals"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument phase", value=phase, expected_type=type_hints["phase"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "goals": goals,
            "id": id,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if phase is not None:
            self._values["phase"] = phase

    @builtins.property
    def goals(self) -> typing.List[builtins.str]:
        '''(experimental) Which Maven goals this plugin should be associated with.

        :stability: experimental
        '''
        result = self._values.get("goals")
        assert result is not None, "Required property 'goals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) The ID.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Execution key/value configuration.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def phase(self) -> typing.Optional[builtins.str]:
        '''(experimental) The phase in which the plugin should execute.

        :stability: experimental
        '''
        result = self._values.get("phase")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PluginExecution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.java.PluginOptions",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "dependencies": "dependencies",
        "executions": "executions",
    },
)
class PluginOptions:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        executions: typing.Optional[typing.Sequence[typing.Union[PluginExecution, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Options for Maven plugins.

        :param configuration: (experimental) Plugin key/value configuration. Default: {}
        :param dependencies: (experimental) You could configure the dependencies for the plugin. Dependencies are in ``<groupId>/<artifactId>@<semver>`` format. Default: []
        :param executions: (experimental) Plugin executions. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf453a5ea3da08b956d0eb1127063e74802cd6e62720cf0f2c1841875bb9f17e)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument executions", value=executions, expected_type=type_hints["executions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if executions is not None:
            self._values["executions"] = executions

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Plugin key/value configuration.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) You could configure the dependencies for the plugin.

        Dependencies are in ``<groupId>/<artifactId>@<semver>`` format.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def executions(self) -> typing.Optional[typing.List[PluginExecution]]:
        '''(experimental) Plugin executions.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("executions")
        return typing.cast(typing.Optional[typing.List[PluginExecution]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PluginOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Pom(_Component_2b0ad27f, metaclass=jsii.JSIIMeta, jsii_type="projen.java.Pom"):
    '''(experimental) A Project Object Model or POM is the fundamental unit of work in Maven.

    It is
    an XML file that contains information about the project and configuration
    details used by Maven to build the project.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        artifact_id: builtins.str,
        group_id: builtins.str,
        version: builtins.str,
        description: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3638a11786e70b5de428bf2064d32761537778501eb3cb189b4457c78aee9d8)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PomOptions(
            artifact_id=artifact_id,
            group_id=group_id,
            version=version,
            description=description,
            packaging=packaging,
            parent_pom=parent_pom,
            url=url,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, spec: builtins.str) -> None:
        '''(experimental) Adds a runtime dependency.

        :param spec: Format ``<groupId>/<artifactId>@<semver>``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babe0c916a881bd5ee39c89fc4aea86a422e404dde7e5bf3a13a1a7430b81baa)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        return typing.cast(None, jsii.invoke(self, "addDependency", [spec]))

    @jsii.member(jsii_name="addPlugin")
    def add_plugin(
        self,
        spec: builtins.str,
        *,
        configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        executions: typing.Optional[typing.Sequence[typing.Union[PluginExecution, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _Dependency_f510e013:
        '''(experimental) Adds a build plugin to the pom.

        The plug in is also added as a BUILD dep to the project.

        :param spec: dependency spec (``group/artifact@version``).
        :param configuration: (experimental) Plugin key/value configuration. Default: {}
        :param dependencies: (experimental) You could configure the dependencies for the plugin. Dependencies are in ``<groupId>/<artifactId>@<semver>`` format. Default: []
        :param executions: (experimental) Plugin executions. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fb4eb690c78d4a220dcb39656037de03d1bc879d6904d08835eb6a2d41de93)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        options = PluginOptions(
            configuration=configuration,
            dependencies=dependencies,
            executions=executions,
        )

        return typing.cast(_Dependency_f510e013, jsii.invoke(self, "addPlugin", [spec, options]))

    @jsii.member(jsii_name="addPluginRepository")
    def add_plugin_repository(
        self,
        *,
        id: builtins.str,
        url: builtins.str,
        layout: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        releases: typing.Optional[typing.Union[MavenRepositoryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        snapshots: typing.Optional[typing.Union[MavenRepositoryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: (experimental) The identifier for the repository.
        :param url: (experimental) The url of the repository.
        :param layout: (experimental) The layout of the repository.
        :param name: (experimental) The name of the repository.
        :param releases: (experimental) Repository Policy for Releases.
        :param snapshots: (experimental) Repository Policy for Snapshots.

        :stability: experimental
        '''
        repository = MavenRepository(
            id=id,
            url=url,
            layout=layout,
            name=name,
            releases=releases,
            snapshots=snapshots,
        )

        return typing.cast(None, jsii.invoke(self, "addPluginRepository", [repository]))

    @jsii.member(jsii_name="addProperty")
    def add_property(self, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) Adds a key/value property to the pom.

        :param key: the key.
        :param value: the value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88917f0eb8cf7f4c02c3fa27ba8f3feaf465d762b92e9d01d91c5ff48859a3c6)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addProperty", [key, value]))

    @jsii.member(jsii_name="addRepository")
    def add_repository(
        self,
        *,
        id: builtins.str,
        url: builtins.str,
        layout: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        releases: typing.Optional[typing.Union[MavenRepositoryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        snapshots: typing.Optional[typing.Union[MavenRepositoryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Adds a repository to the pom.

        :param id: (experimental) The identifier for the repository.
        :param url: (experimental) The url of the repository.
        :param layout: (experimental) The layout of the repository.
        :param name: (experimental) The name of the repository.
        :param releases: (experimental) Repository Policy for Releases.
        :param snapshots: (experimental) Repository Policy for Snapshots.

        :stability: experimental
        '''
        repository = MavenRepository(
            id=id,
            url=url,
            layout=layout,
            name=name,
            releases=releases,
            snapshots=snapshots,
        )

        return typing.cast(None, jsii.invoke(self, "addRepository", [repository]))

    @jsii.member(jsii_name="addTestDependency")
    def add_test_dependency(self, spec: builtins.str) -> None:
        '''(experimental) Adds a test dependency.

        :param spec: Format ``<groupId>/<artifactId>@<semver>``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1671b0ccd8a1185ca40d182b3df573ab75cd69e4085d2a310a227960249ddd)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        return typing.cast(None, jsii.invoke(self, "addTestDependency", [spec]))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        '''(experimental) Maven artifact ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        '''(experimental) The name of the pom file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        '''(experimental) Maven group ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="packaging")
    def packaging(self) -> builtins.str:
        '''(experimental) Maven packaging format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "packaging"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) Project version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project description.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project display name.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project URL.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "url"))


@jsii.data_type(
    jsii_type="projen.java.PomOptions",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "group_id": "groupId",
        "version": "version",
        "description": "description",
        "packaging": "packaging",
        "parent_pom": "parentPom",
        "url": "url",
    },
)
class PomOptions:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        group_id: builtins.str,
        version: builtins.str,
        description: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``Pom``.

        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined

        :stability: experimental
        '''
        if isinstance(parent_pom, dict):
            parent_pom = ParentPom(**parent_pom)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468190ed1f2feac4431fa6e9f5cc22eb8dbb01cd1c5d3bdfdac29f07c4370851)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument parent_pom", value=parent_pom, expected_type=type_hints["parent_pom"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
            "group_id": group_id,
            "version": version,
        }
        if description is not None:
            self._values["description"] = description
        if packaging is not None:
            self._values["packaging"] = packaging
        if parent_pom is not None:
            self._values["parent_pom"] = parent_pom
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''(experimental) The artifactId is generally the name that the project is known by.

        Although
        the groupId is important, people within the group will rarely mention the
        groupId in discussion (they are often all be the same ID, such as the
        MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId,
        creates a key that separates this project from every other project in the
        world (at least, it should :) ). Along with the groupId, the artifactId
        fully defines the artifact's living quarters within the repository. In the
        case of the above project, my-project lives in
        $M2_REPO/org/codehaus/mojo/my-project.

        :default: "my-app"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> builtins.str:
        '''(experimental) This is generally unique amongst an organization or a project.

        For example,
        all core Maven artifacts do (well, should) live under the groupId
        org.apache.maven. Group ID's do not necessarily use the dot notation, for
        example, the junit project. Note that the dot-notated groupId does not have
        to correspond to the package structure that the project contains. It is,
        however, a good practice to follow. When stored within a repository, the
        group acts much like the Java packaging structure does in an operating
        system. The dots are replaced by OS specific directory separators (such as
        '/' in Unix) which becomes a relative directory structure from the base
        repository. In the example given, the org.codehaus.mojo group lives within
        the directory $M2_REPO/org/codehaus/mojo.

        :default: "org.acme"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) This is the last piece of the naming puzzle.

        groupId:artifactId denotes a
        single project but they cannot delineate which incarnation of that project
        we are talking about. Do we want the junit:junit of 2018 (version 4.12), or
        of 2007 (version 3.8.2)? In short: code changes, those changes should be
        versioned, and this element keeps those versions in line. It is also used
        within an artifact's repository to separate versions from each other.
        my-project version 1.0 files live in the directory structure
        $M2_REPO/org/codehaus/mojo/my-project/1.0.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of a project is always good.

        Although this should not replace
        formal documentation, a quick comment to any readers of the POM is always
        helpful.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project packaging format.

        :default: "jar"

        :stability: experimental
        '''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_pom(self) -> typing.Optional[ParentPom]:
        '''(experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("parent_pom")
        return typing.cast(typing.Optional[ParentPom], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL, like the name, is not required.

        This is a nice gesture for
        projects users, however, so that they know where the project lives.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PomOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Projenrc(
    _ProjenrcFile_50432c7e,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.java.Projenrc",
):
    '''(experimental) Allows writing projenrc files in java.

    This will install ``org.projen/projen`` as a Maven dependency and will add a
    ``synth`` task which will compile & execute ``main()`` from
    ``src/main/java/projenrc.java``.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        pom: Pom,
        *,
        class_name: typing.Optional[builtins.str] = None,
        projen_version: typing.Optional[builtins.str] = None,
        test_scope: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param pom: -
        :param class_name: (experimental) The name of the Java class which contains the ``main()`` method for projen. Default: "projenrc"
        :param projen_version: (experimental) The projen version to use. Default: - current version
        :param test_scope: (experimental) Defines projenrc under the test scope instead of the main scope, which is reserved to the app. This means that projenrc will be under ``src/test/java/projenrc.java`` and projen will be defined as a test dependency. This enforces that application code does not take a dependency on projen code. If this is disabled, projenrc should be under ``src/main/java/projenrc.java``. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6120ff9474a63c873f006408943a5ac6d72a57ca356c129fa21e41f897bb072d)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pom", value=pom, expected_type=type_hints["pom"])
        options = ProjenrcOptions(
            class_name=class_name, projen_version=projen_version, test_scope=test_scope
        )

        jsii.create(self.__class__, self, [project, pom, options])

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        '''(experimental) The name of the java class that includes the projen entrypoint.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "className"))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        '''(experimental) The path of the projenrc file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filePath"))


@jsii.data_type(
    jsii_type="projen.java.ProjenrcOptions",
    jsii_struct_bases=[],
    name_mapping={
        "class_name": "className",
        "projen_version": "projenVersion",
        "test_scope": "testScope",
    },
)
class ProjenrcOptions:
    def __init__(
        self,
        *,
        class_name: typing.Optional[builtins.str] = None,
        projen_version: typing.Optional[builtins.str] = None,
        test_scope: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``Projenrc``.

        :param class_name: (experimental) The name of the Java class which contains the ``main()`` method for projen. Default: "projenrc"
        :param projen_version: (experimental) The projen version to use. Default: - current version
        :param test_scope: (experimental) Defines projenrc under the test scope instead of the main scope, which is reserved to the app. This means that projenrc will be under ``src/test/java/projenrc.java`` and projen will be defined as a test dependency. This enforces that application code does not take a dependency on projen code. If this is disabled, projenrc should be under ``src/main/java/projenrc.java``. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae2ae91be40e1fe4218504ad4a0a84a64d14b1c1274575f956490848ab10770)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
            check_type(argname="argument projen_version", value=projen_version, expected_type=type_hints["projen_version"])
            check_type(argname="argument test_scope", value=test_scope, expected_type=type_hints["test_scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if class_name is not None:
            self._values["class_name"] = class_name
        if projen_version is not None:
            self._values["projen_version"] = projen_version
        if test_scope is not None:
            self._values["test_scope"] = test_scope

    @builtins.property
    def class_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Java class which contains the ``main()`` method for projen.

        :default: "projenrc"

        :stability: experimental
        '''
        result = self._values.get("class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The projen version to use.

        :default: - current version

        :stability: experimental
        '''
        result = self._values.get("projen_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_scope(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines projenrc under the test scope instead of the main scope, which is reserved to the app.

        This means that projenrc will be under
        ``src/test/java/projenrc.java`` and projen will be defined as a test
        dependency. This enforces that application code does not take a dependency
        on projen code.

        If this is disabled, projenrc should be under
        ``src/main/java/projenrc.java``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("test_scope")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjenrcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UpdatePolicy(metaclass=jsii.JSIIMeta, jsii_type="projen.java.UpdatePolicy"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="interval")
    @builtins.classmethod
    def interval(cls, minutes: jsii.Number) -> builtins.str:
        '''(experimental) Updates at an interval of X minutes.

        :param minutes: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf8e37b8aa70ecfb764a100f3a50eabbce221f62cf2cc199c929b8132fe42cc)
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "interval", [minutes]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALWAYS")
    def ALWAYS(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ALWAYS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DAILY")
    def DAILY(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DAILY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NEVER")
    def NEVER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NEVER"))


@jsii.data_type(
    jsii_type="projen.java.JavaProjectCommonOptions",
    jsii_struct_bases=[_GitHubProjectOptions_547f2d08, PomOptions],
    name_mapping={
        "name": "name",
        "commit_generated": "commitGenerated",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "logging": "logging",
        "outdir": "outdir",
        "parent": "parent",
        "projen_command": "projenCommand",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "clobber": "clobber",
        "dev_container": "devContainer",
        "github": "github",
        "github_options": "githubOptions",
        "gitpod": "gitpod",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "project_type": "projectType",
        "projen_credentials": "projenCredentials",
        "projen_token_secret": "projenTokenSecret",
        "readme": "readme",
        "stale": "stale",
        "stale_options": "staleOptions",
        "vscode": "vscode",
        "artifact_id": "artifactId",
        "group_id": "groupId",
        "version": "version",
        "description": "description",
        "packaging": "packaging",
        "parent_pom": "parentPom",
        "url": "url",
        "compile_options": "compileOptions",
        "deps": "deps",
        "distdir": "distdir",
        "junit": "junit",
        "junit_options": "junitOptions",
        "packaging_options": "packagingOptions",
        "projenrc_java": "projenrcJava",
        "projenrc_java_options": "projenrcJavaOptions",
        "test_deps": "testDeps",
    },
)
class JavaProjectCommonOptions(_GitHubProjectOptions_547f2d08, PomOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_Project_57d89203] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_ProjectType_fd80c725] = None,
        projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        artifact_id: builtins.str,
        group_id: builtins.str,
        version: builtins.str,
        description: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
        compile_options: typing.Optional[typing.Union[MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        distdir: typing.Optional[builtins.str] = None,
        junit: typing.Optional[builtins.bool] = None,
        junit_options: typing.Optional[typing.Union[JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        packaging_options: typing.Optional[typing.Union[MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_java: typing.Optional[builtins.bool] = None,
        projenrc_java_options: typing.Optional[typing.Union[ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``JavaProject``.

        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>`` Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param junit: (experimental) Include junit tests. Default: true
        :param junit_options: (experimental) junit options. Default: - defaults
        :param packaging_options: (experimental) Packaging options. Default: - defaults
        :param projenrc_java: (experimental) Use projenrc in java. This will install ``projen`` as a java dependency and will add a ``synth`` task which will compile & execute ``main()`` from ``src/main/java/projenrc.java``. Default: true
        :param projenrc_java_options: (experimental) Options related to projenrc in java. Default: - default options
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>`` Additional dependencies can be added via ``project.addTestDependency()``. Default: []

        :stability: experimental
        '''
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _IgnoreFileOptions_86c48b91(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _GitOptions_a65916a3(**git_options)
        if isinstance(logging, dict):
            logging = _LoggerOptions_eb0f6309(**logging)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _ProjenrcJsonOptions_9c40dd4f(**projenrc_json_options)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _RenovatebotOptions_18e6b8a1(**renovatebot_options)
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _AutoApproveOptions_dac86cbe(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _AutoMergeOptions_d112cd3c(**auto_merge_options)
        if isinstance(github_options, dict):
            github_options = _GitHubOptions_21553699(**github_options)
        if isinstance(mergify_options, dict):
            mergify_options = _MergifyOptions_a6faaab3(**mergify_options)
        if isinstance(readme, dict):
            readme = _SampleReadmeProps_3518b03b(**readme)
        if isinstance(stale_options, dict):
            stale_options = _StaleOptions_929db764(**stale_options)
        if isinstance(parent_pom, dict):
            parent_pom = ParentPom(**parent_pom)
        if isinstance(compile_options, dict):
            compile_options = MavenCompileOptions(**compile_options)
        if isinstance(junit_options, dict):
            junit_options = JunitOptions(**junit_options)
        if isinstance(packaging_options, dict):
            packaging_options = MavenPackagingOptions(**packaging_options)
        if isinstance(projenrc_java_options, dict):
            projenrc_java_options = ProjenrcOptions(**projenrc_java_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d1347bcc9244ea45fe2d94ee57536743a6579b8c3cbeefd1a9832f2acb54b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument parent_pom", value=parent_pom, expected_type=type_hints["parent_pom"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument compile_options", value=compile_options, expected_type=type_hints["compile_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument junit", value=junit, expected_type=type_hints["junit"])
            check_type(argname="argument junit_options", value=junit_options, expected_type=type_hints["junit_options"])
            check_type(argname="argument packaging_options", value=packaging_options, expected_type=type_hints["packaging_options"])
            check_type(argname="argument projenrc_java", value=projenrc_java, expected_type=type_hints["projenrc_java"])
            check_type(argname="argument projenrc_java_options", value=projenrc_java_options, expected_type=type_hints["projenrc_java_options"])
            check_type(argname="argument test_deps", value=test_deps, expected_type=type_hints["test_deps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "artifact_id": artifact_id,
            "group_id": group_id,
            "version": version,
        }
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if logging is not None:
            self._values["logging"] = logging
        if outdir is not None:
            self._values["outdir"] = outdir
        if parent is not None:
            self._values["parent"] = parent
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if clobber is not None:
            self._values["clobber"] = clobber
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if readme is not None:
            self._values["readme"] = readme
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if vscode is not None:
            self._values["vscode"] = vscode
        if description is not None:
            self._values["description"] = description
        if packaging is not None:
            self._values["packaging"] = packaging
        if parent_pom is not None:
            self._values["parent_pom"] = parent_pom
        if url is not None:
            self._values["url"] = url
        if compile_options is not None:
            self._values["compile_options"] = compile_options
        if deps is not None:
            self._values["deps"] = deps
        if distdir is not None:
            self._values["distdir"] = distdir
        if junit is not None:
            self._values["junit"] = junit
        if junit_options is not None:
            self._values["junit_options"] = junit_options
        if packaging_options is not None:
            self._values["packaging_options"] = packaging_options
        if projenrc_java is not None:
            self._values["projenrc_java"] = projenrc_java
        if projenrc_java_options is not None:
            self._values["projenrc_java_options"] = projenrc_java_options
        if test_deps is not None:
            self._values["test_deps"] = test_deps

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) This is the name of your project.

        :default: $BASEDIR

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_IgnoreFileOptions_86c48b91]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_IgnoreFileOptions_86c48b91], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_GitOptions_a65916a3]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_GitOptions_a65916a3], result)

    @builtins.property
    def logging(self) -> typing.Optional[_LoggerOptions_eb0f6309]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_LoggerOptions_eb0f6309], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project.

        Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_Project_57d89203]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_Project_57d89203], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(self) -> typing.Optional[_ProjenrcJsonOptions_9c40dd4f]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_ProjenrcJsonOptions_9c40dd4f], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(self) -> typing.Optional[_RenovatebotOptions_18e6b8a1]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_RenovatebotOptions_18e6b8a1], result)

    @builtins.property
    def auto_approve_options(self) -> typing.Optional[_AutoApproveOptions_dac86cbe]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_AutoApproveOptions_dac86cbe], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(self) -> typing.Optional[_AutoMergeOptions_d112cd3c]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_AutoMergeOptions_d112cd3c], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_GitHubOptions_21553699]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_GitHubOptions_21553699], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(self) -> typing.Optional[_MergifyOptions_a6faaab3]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_MergifyOptions_a6faaab3], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_ProjectType_fd80c725]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_ProjectType_fd80c725], result)

    @builtins.property
    def projen_credentials(self) -> typing.Optional[_GithubCredentials_ae257072]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_GithubCredentials_ae257072], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_SampleReadmeProps_3518b03b]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental

        Example::

            "{ filename: 'readme.md', contents: '# title' }"
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_SampleReadmeProps_3518b03b], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_StaleOptions_929db764]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_StaleOptions_929db764], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''(experimental) The artifactId is generally the name that the project is known by.

        Although
        the groupId is important, people within the group will rarely mention the
        groupId in discussion (they are often all be the same ID, such as the
        MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId,
        creates a key that separates this project from every other project in the
        world (at least, it should :) ). Along with the groupId, the artifactId
        fully defines the artifact's living quarters within the repository. In the
        case of the above project, my-project lives in
        $M2_REPO/org/codehaus/mojo/my-project.

        :default: "my-app"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> builtins.str:
        '''(experimental) This is generally unique amongst an organization or a project.

        For example,
        all core Maven artifacts do (well, should) live under the groupId
        org.apache.maven. Group ID's do not necessarily use the dot notation, for
        example, the junit project. Note that the dot-notated groupId does not have
        to correspond to the package structure that the project contains. It is,
        however, a good practice to follow. When stored within a repository, the
        group acts much like the Java packaging structure does in an operating
        system. The dots are replaced by OS specific directory separators (such as
        '/' in Unix) which becomes a relative directory structure from the base
        repository. In the example given, the org.codehaus.mojo group lives within
        the directory $M2_REPO/org/codehaus/mojo.

        :default: "org.acme"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) This is the last piece of the naming puzzle.

        groupId:artifactId denotes a
        single project but they cannot delineate which incarnation of that project
        we are talking about. Do we want the junit:junit of 2018 (version 4.12), or
        of 2007 (version 3.8.2)? In short: code changes, those changes should be
        versioned, and this element keeps those versions in line. It is also used
        within an artifact's repository to separate versions from each other.
        my-project version 1.0 files live in the directory structure
        $M2_REPO/org/codehaus/mojo/my-project/1.0.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of a project is always good.

        Although this should not replace
        formal documentation, a quick comment to any readers of the POM is always
        helpful.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project packaging format.

        :default: "jar"

        :stability: experimental
        '''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_pom(self) -> typing.Optional[ParentPom]:
        '''(experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("parent_pom")
        return typing.cast(typing.Optional[ParentPom], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL, like the name, is not required.

        This is a nice gesture for
        projects users, however, so that they know where the project lives.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compile_options(self) -> typing.Optional[MavenCompileOptions]:
        '''(experimental) Compile options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("compile_options")
        return typing.cast(typing.Optional[MavenCompileOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of runtime dependencies for this project.

        Dependencies use the format: ``<groupId>/<artifactId>@<semver>``

        Additional dependencies can be added via ``project.addDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def distdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Final artifact output directory.

        :default: "dist/java"

        :stability: experimental
        '''
        result = self._values.get("distdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include junit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("junit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def junit_options(self) -> typing.Optional[JunitOptions]:
        '''(experimental) junit options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("junit_options")
        return typing.cast(typing.Optional[JunitOptions], result)

    @builtins.property
    def packaging_options(self) -> typing.Optional[MavenPackagingOptions]:
        '''(experimental) Packaging options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("packaging_options")
        return typing.cast(typing.Optional[MavenPackagingOptions], result)

    @builtins.property
    def projenrc_java(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use projenrc in java.

        This will install ``projen`` as a java dependency and will add a ``synth`` task which
        will compile & execute ``main()`` from ``src/main/java/projenrc.java``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("projenrc_java")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_java_options(self) -> typing.Optional[ProjenrcOptions]:
        '''(experimental) Options related to projenrc in java.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_java_options")
        return typing.cast(typing.Optional[ProjenrcOptions], result)

    @builtins.property
    def test_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of test dependencies for this project.

        Dependencies use the format: ``<groupId>/<artifactId>@<semver>``

        Additional dependencies can be added via ``project.addTestDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("test_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JavaProjectCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.java.JavaProjectOptions",
    jsii_struct_bases=[JavaProjectCommonOptions],
    name_mapping={
        "name": "name",
        "commit_generated": "commitGenerated",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "logging": "logging",
        "outdir": "outdir",
        "parent": "parent",
        "projen_command": "projenCommand",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "clobber": "clobber",
        "dev_container": "devContainer",
        "github": "github",
        "github_options": "githubOptions",
        "gitpod": "gitpod",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "project_type": "projectType",
        "projen_credentials": "projenCredentials",
        "projen_token_secret": "projenTokenSecret",
        "readme": "readme",
        "stale": "stale",
        "stale_options": "staleOptions",
        "vscode": "vscode",
        "artifact_id": "artifactId",
        "group_id": "groupId",
        "version": "version",
        "description": "description",
        "packaging": "packaging",
        "parent_pom": "parentPom",
        "url": "url",
        "compile_options": "compileOptions",
        "deps": "deps",
        "distdir": "distdir",
        "junit": "junit",
        "junit_options": "junitOptions",
        "packaging_options": "packagingOptions",
        "projenrc_java": "projenrcJava",
        "projenrc_java_options": "projenrcJavaOptions",
        "test_deps": "testDeps",
        "sample": "sample",
        "sample_java_package": "sampleJavaPackage",
    },
)
class JavaProjectOptions(JavaProjectCommonOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_Project_57d89203] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_ProjectType_fd80c725] = None,
        projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        artifact_id: builtins.str,
        group_id: builtins.str,
        version: builtins.str,
        description: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
        compile_options: typing.Optional[typing.Union[MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        distdir: typing.Optional[builtins.str] = None,
        junit: typing.Optional[builtins.bool] = None,
        junit_options: typing.Optional[typing.Union[JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        packaging_options: typing.Optional[typing.Union[MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_java: typing.Optional[builtins.bool] = None,
        projenrc_java_options: typing.Optional[typing.Union[ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``JavaProject``.

        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>`` Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param junit: (experimental) Include junit tests. Default: true
        :param junit_options: (experimental) junit options. Default: - defaults
        :param packaging_options: (experimental) Packaging options. Default: - defaults
        :param projenrc_java: (experimental) Use projenrc in java. This will install ``projen`` as a java dependency and will add a ``synth`` task which will compile & execute ``main()`` from ``src/main/java/projenrc.java``. Default: true
        :param projenrc_java_options: (experimental) Options related to projenrc in java. Default: - default options
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>`` Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"

        :stability: experimental
        '''
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _IgnoreFileOptions_86c48b91(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _GitOptions_a65916a3(**git_options)
        if isinstance(logging, dict):
            logging = _LoggerOptions_eb0f6309(**logging)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _ProjenrcJsonOptions_9c40dd4f(**projenrc_json_options)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _RenovatebotOptions_18e6b8a1(**renovatebot_options)
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _AutoApproveOptions_dac86cbe(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _AutoMergeOptions_d112cd3c(**auto_merge_options)
        if isinstance(github_options, dict):
            github_options = _GitHubOptions_21553699(**github_options)
        if isinstance(mergify_options, dict):
            mergify_options = _MergifyOptions_a6faaab3(**mergify_options)
        if isinstance(readme, dict):
            readme = _SampleReadmeProps_3518b03b(**readme)
        if isinstance(stale_options, dict):
            stale_options = _StaleOptions_929db764(**stale_options)
        if isinstance(parent_pom, dict):
            parent_pom = ParentPom(**parent_pom)
        if isinstance(compile_options, dict):
            compile_options = MavenCompileOptions(**compile_options)
        if isinstance(junit_options, dict):
            junit_options = JunitOptions(**junit_options)
        if isinstance(packaging_options, dict):
            packaging_options = MavenPackagingOptions(**packaging_options)
        if isinstance(projenrc_java_options, dict):
            projenrc_java_options = ProjenrcOptions(**projenrc_java_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd204911b78eb490a0ff7d3863868024abfc54a7f5ababba6fe97db2f176861)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument parent_pom", value=parent_pom, expected_type=type_hints["parent_pom"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument compile_options", value=compile_options, expected_type=type_hints["compile_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument junit", value=junit, expected_type=type_hints["junit"])
            check_type(argname="argument junit_options", value=junit_options, expected_type=type_hints["junit_options"])
            check_type(argname="argument packaging_options", value=packaging_options, expected_type=type_hints["packaging_options"])
            check_type(argname="argument projenrc_java", value=projenrc_java, expected_type=type_hints["projenrc_java"])
            check_type(argname="argument projenrc_java_options", value=projenrc_java_options, expected_type=type_hints["projenrc_java_options"])
            check_type(argname="argument test_deps", value=test_deps, expected_type=type_hints["test_deps"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument sample_java_package", value=sample_java_package, expected_type=type_hints["sample_java_package"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "artifact_id": artifact_id,
            "group_id": group_id,
            "version": version,
        }
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if logging is not None:
            self._values["logging"] = logging
        if outdir is not None:
            self._values["outdir"] = outdir
        if parent is not None:
            self._values["parent"] = parent
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if clobber is not None:
            self._values["clobber"] = clobber
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if readme is not None:
            self._values["readme"] = readme
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if vscode is not None:
            self._values["vscode"] = vscode
        if description is not None:
            self._values["description"] = description
        if packaging is not None:
            self._values["packaging"] = packaging
        if parent_pom is not None:
            self._values["parent_pom"] = parent_pom
        if url is not None:
            self._values["url"] = url
        if compile_options is not None:
            self._values["compile_options"] = compile_options
        if deps is not None:
            self._values["deps"] = deps
        if distdir is not None:
            self._values["distdir"] = distdir
        if junit is not None:
            self._values["junit"] = junit
        if junit_options is not None:
            self._values["junit_options"] = junit_options
        if packaging_options is not None:
            self._values["packaging_options"] = packaging_options
        if projenrc_java is not None:
            self._values["projenrc_java"] = projenrc_java
        if projenrc_java_options is not None:
            self._values["projenrc_java_options"] = projenrc_java_options
        if test_deps is not None:
            self._values["test_deps"] = test_deps
        if sample is not None:
            self._values["sample"] = sample
        if sample_java_package is not None:
            self._values["sample_java_package"] = sample_java_package

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) This is the name of your project.

        :default: $BASEDIR

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_IgnoreFileOptions_86c48b91]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_IgnoreFileOptions_86c48b91], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_GitOptions_a65916a3]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_GitOptions_a65916a3], result)

    @builtins.property
    def logging(self) -> typing.Optional[_LoggerOptions_eb0f6309]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_LoggerOptions_eb0f6309], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project.

        Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_Project_57d89203]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_Project_57d89203], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(self) -> typing.Optional[_ProjenrcJsonOptions_9c40dd4f]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_ProjenrcJsonOptions_9c40dd4f], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(self) -> typing.Optional[_RenovatebotOptions_18e6b8a1]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_RenovatebotOptions_18e6b8a1], result)

    @builtins.property
    def auto_approve_options(self) -> typing.Optional[_AutoApproveOptions_dac86cbe]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_AutoApproveOptions_dac86cbe], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(self) -> typing.Optional[_AutoMergeOptions_d112cd3c]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_AutoMergeOptions_d112cd3c], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_GitHubOptions_21553699]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_GitHubOptions_21553699], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(self) -> typing.Optional[_MergifyOptions_a6faaab3]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_MergifyOptions_a6faaab3], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_ProjectType_fd80c725]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_ProjectType_fd80c725], result)

    @builtins.property
    def projen_credentials(self) -> typing.Optional[_GithubCredentials_ae257072]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_GithubCredentials_ae257072], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_SampleReadmeProps_3518b03b]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental

        Example::

            "{ filename: 'readme.md', contents: '# title' }"
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_SampleReadmeProps_3518b03b], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_StaleOptions_929db764]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_StaleOptions_929db764], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''(experimental) The artifactId is generally the name that the project is known by.

        Although
        the groupId is important, people within the group will rarely mention the
        groupId in discussion (they are often all be the same ID, such as the
        MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId,
        creates a key that separates this project from every other project in the
        world (at least, it should :) ). Along with the groupId, the artifactId
        fully defines the artifact's living quarters within the repository. In the
        case of the above project, my-project lives in
        $M2_REPO/org/codehaus/mojo/my-project.

        :default: "my-app"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> builtins.str:
        '''(experimental) This is generally unique amongst an organization or a project.

        For example,
        all core Maven artifacts do (well, should) live under the groupId
        org.apache.maven. Group ID's do not necessarily use the dot notation, for
        example, the junit project. Note that the dot-notated groupId does not have
        to correspond to the package structure that the project contains. It is,
        however, a good practice to follow. When stored within a repository, the
        group acts much like the Java packaging structure does in an operating
        system. The dots are replaced by OS specific directory separators (such as
        '/' in Unix) which becomes a relative directory structure from the base
        repository. In the example given, the org.codehaus.mojo group lives within
        the directory $M2_REPO/org/codehaus/mojo.

        :default: "org.acme"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) This is the last piece of the naming puzzle.

        groupId:artifactId denotes a
        single project but they cannot delineate which incarnation of that project
        we are talking about. Do we want the junit:junit of 2018 (version 4.12), or
        of 2007 (version 3.8.2)? In short: code changes, those changes should be
        versioned, and this element keeps those versions in line. It is also used
        within an artifact's repository to separate versions from each other.
        my-project version 1.0 files live in the directory structure
        $M2_REPO/org/codehaus/mojo/my-project/1.0.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of a project is always good.

        Although this should not replace
        formal documentation, a quick comment to any readers of the POM is always
        helpful.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project packaging format.

        :default: "jar"

        :stability: experimental
        '''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_pom(self) -> typing.Optional[ParentPom]:
        '''(experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("parent_pom")
        return typing.cast(typing.Optional[ParentPom], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL, like the name, is not required.

        This is a nice gesture for
        projects users, however, so that they know where the project lives.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compile_options(self) -> typing.Optional[MavenCompileOptions]:
        '''(experimental) Compile options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("compile_options")
        return typing.cast(typing.Optional[MavenCompileOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of runtime dependencies for this project.

        Dependencies use the format: ``<groupId>/<artifactId>@<semver>``

        Additional dependencies can be added via ``project.addDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def distdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Final artifact output directory.

        :default: "dist/java"

        :stability: experimental
        '''
        result = self._values.get("distdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include junit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("junit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def junit_options(self) -> typing.Optional[JunitOptions]:
        '''(experimental) junit options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("junit_options")
        return typing.cast(typing.Optional[JunitOptions], result)

    @builtins.property
    def packaging_options(self) -> typing.Optional[MavenPackagingOptions]:
        '''(experimental) Packaging options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("packaging_options")
        return typing.cast(typing.Optional[MavenPackagingOptions], result)

    @builtins.property
    def projenrc_java(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use projenrc in java.

        This will install ``projen`` as a java dependency and will add a ``synth`` task which
        will compile & execute ``main()`` from ``src/main/java/projenrc.java``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("projenrc_java")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_java_options(self) -> typing.Optional[ProjenrcOptions]:
        '''(experimental) Options related to projenrc in java.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_java_options")
        return typing.cast(typing.Optional[ProjenrcOptions], result)

    @builtins.property
    def test_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of test dependencies for this project.

        Dependencies use the format: ``<groupId>/<artifactId>@<semver>``

        Additional dependencies can be added via ``project.addTestDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("test_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include sample code and test if the relevant directories don't exist.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sample_java_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The java package to use for the code sample.

        :default: "org.acme"

        :stability: experimental
        '''
        result = self._values.get("sample_java_package")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JavaProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ChecksumPolicy",
    "JavaProject",
    "JavaProjectCommonOptions",
    "JavaProjectOptions",
    "Junit",
    "JunitOptions",
    "MavenCompile",
    "MavenCompileOptions",
    "MavenPackaging",
    "MavenPackagingOptions",
    "MavenRepository",
    "MavenRepositoryPolicy",
    "MavenSample",
    "MavenSampleOptions",
    "ParentPom",
    "PluginExecution",
    "PluginOptions",
    "Pom",
    "PomOptions",
    "Projenrc",
    "ProjenrcOptions",
    "UpdatePolicy",
]

publication.publish()

def _typecheckingstub__c3cde13045b969d2a5e4bfbf540cdcead81b701c879b4079ebdf703d31d185aa(
    spec: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d82566ec5da4a4ff8c5ec4f7442835fb01d67e916c8cdb64dc6ed08d10a361c(
    spec: builtins.str,
    *,
    configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    executions: typing.Optional[typing.Sequence[typing.Union[PluginExecution, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702d880972766245e6e0ce9d4332f75632d1c9f56321a84f3b10f119ec91dcd0(
    spec: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877c5aed063e2ddca6cbb37631bb31564c14fc1f304629ab7adcc662faa0b0da(
    project: _Project_57d89203,
    *,
    pom: Pom,
    sample_java_package: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db441a323339ae146e69254287868e3704cd5ee3edbcc272138a4e660f9e4c72(
    *,
    pom: Pom,
    sample_java_package: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f143440a0c274a37fff9c951ad85be29c31b978c6c6d89ee2cbe127b8249b88(
    project: _Project_57d89203,
    pom: Pom,
    *,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abc628703576e622a20aab761493d186a662ac606df5bccb664dfe4f41a9240(
    *,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7f0f4d617b106a57e5b073cf5f51ca4195a66d251926fe0b5b0fa27b2b7612(
    project: _Project_57d89203,
    pom: Pom,
    *,
    distdir: typing.Optional[builtins.str] = None,
    javadocs: typing.Optional[builtins.bool] = None,
    javadocs_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    sources: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69d38d3cd60ee77b03f102371324cf8c453ac910fe11ed85622f44a7358057a(
    *,
    distdir: typing.Optional[builtins.str] = None,
    javadocs: typing.Optional[builtins.bool] = None,
    javadocs_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    sources: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e8ee88cd330385feef214bd08b3bc44314dc15ddbcd48e4f74c198bda84bde(
    *,
    id: builtins.str,
    url: builtins.str,
    layout: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    releases: typing.Optional[typing.Union[MavenRepositoryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshots: typing.Optional[typing.Union[MavenRepositoryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041e104cddeb68a13d0b79cfdce8653000ee58d2c7cef3088a2c8717d7f02ebf(
    *,
    checksum_policy: typing.Optional[ChecksumPolicy] = None,
    enabled: typing.Optional[builtins.bool] = None,
    update_policy: typing.Optional[UpdatePolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4190861db7ca6169340394602246875f9668e86624764e5e7279d01f6c2a3017(
    project: _Project_57d89203,
    *,
    package: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be9d5c5edaace101d0e427b56fb2e89f3b2e6ac01bd59e3cb1d0743d9293524(
    *,
    package: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f47e5dc92031bfaa3a639437d282aedc130d8a3857314c5a71a2ca063798f40(
    *,
    artifact_id: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    relative_path: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b1bc2eb1ab79c9e54c8b62fd341a87dd82eec6a2b2ec76a5fdb6f1c51d5444(
    *,
    goals: typing.Sequence[builtins.str],
    id: builtins.str,
    configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    phase: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf453a5ea3da08b956d0eb1127063e74802cd6e62720cf0f2c1841875bb9f17e(
    *,
    configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    executions: typing.Optional[typing.Sequence[typing.Union[PluginExecution, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3638a11786e70b5de428bf2064d32761537778501eb3cb189b4457c78aee9d8(
    project: _Project_57d89203,
    *,
    artifact_id: builtins.str,
    group_id: builtins.str,
    version: builtins.str,
    description: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babe0c916a881bd5ee39c89fc4aea86a422e404dde7e5bf3a13a1a7430b81baa(
    spec: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fb4eb690c78d4a220dcb39656037de03d1bc879d6904d08835eb6a2d41de93(
    spec: builtins.str,
    *,
    configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    executions: typing.Optional[typing.Sequence[typing.Union[PluginExecution, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88917f0eb8cf7f4c02c3fa27ba8f3feaf465d762b92e9d01d91c5ff48859a3c6(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1671b0ccd8a1185ca40d182b3df573ab75cd69e4085d2a310a227960249ddd(
    spec: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468190ed1f2feac4431fa6e9f5cc22eb8dbb01cd1c5d3bdfdac29f07c4370851(
    *,
    artifact_id: builtins.str,
    group_id: builtins.str,
    version: builtins.str,
    description: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6120ff9474a63c873f006408943a5ac6d72a57ca356c129fa21e41f897bb072d(
    project: _Project_57d89203,
    pom: Pom,
    *,
    class_name: typing.Optional[builtins.str] = None,
    projen_version: typing.Optional[builtins.str] = None,
    test_scope: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae2ae91be40e1fe4218504ad4a0a84a64d14b1c1274575f956490848ab10770(
    *,
    class_name: typing.Optional[builtins.str] = None,
    projen_version: typing.Optional[builtins.str] = None,
    test_scope: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf8e37b8aa70ecfb764a100f3a50eabbce221f62cf2cc199c929b8132fe42cc(
    minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d1347bcc9244ea45fe2d94ee57536743a6579b8c3cbeefd1a9832f2acb54b0(
    *,
    name: builtins.str,
    commit_generated: typing.Optional[builtins.bool] = None,
    git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_Project_57d89203] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_ProjectType_fd80c725] = None,
    projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
    vscode: typing.Optional[builtins.bool] = None,
    artifact_id: builtins.str,
    group_id: builtins.str,
    version: builtins.str,
    description: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
    compile_options: typing.Optional[typing.Union[MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    distdir: typing.Optional[builtins.str] = None,
    junit: typing.Optional[builtins.bool] = None,
    junit_options: typing.Optional[typing.Union[JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    packaging_options: typing.Optional[typing.Union[MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_java: typing.Optional[builtins.bool] = None,
    projenrc_java_options: typing.Optional[typing.Union[ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd204911b78eb490a0ff7d3863868024abfc54a7f5ababba6fe97db2f176861(
    *,
    name: builtins.str,
    commit_generated: typing.Optional[builtins.bool] = None,
    git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_Project_57d89203] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_ProjectType_fd80c725] = None,
    projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
    vscode: typing.Optional[builtins.bool] = None,
    artifact_id: builtins.str,
    group_id: builtins.str,
    version: builtins.str,
    description: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    parent_pom: typing.Optional[typing.Union[ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
    compile_options: typing.Optional[typing.Union[MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    distdir: typing.Optional[builtins.str] = None,
    junit: typing.Optional[builtins.bool] = None,
    junit_options: typing.Optional[typing.Union[JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    packaging_options: typing.Optional[typing.Union[MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_java: typing.Optional[builtins.bool] = None,
    projenrc_java_options: typing.Optional[typing.Union[ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    sample: typing.Optional[builtins.bool] = None,
    sample_java_package: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
