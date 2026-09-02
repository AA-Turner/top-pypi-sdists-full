from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from .._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import constructs as _constructs_77d1e7e8
    import projen as _projen_04054675
else:

    _constructs_77d1e7e8 = _LazyImport("constructs")
    _projen_04054675 = _LazyImport("projen")


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeCoverageOptions",
    jsii_struct_bases=[],
    name_mapping={"exclusions": "exclusions"},
)
class SonarqubeCoverageOptions:
    def __init__(
        self,
        *,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.coverage.*`` properties.

        :param exclusions: (experimental) Comma-separated file path patterns to exclude from test coverage calculations. Maps to ``sonar.coverage.exclusions``. Default: - no coverage exclusions

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9113540a247617d806eaee98dbc9efcc4ec7ed79504f78650d9e555198783795)
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated file path patterns to exclude from test coverage calculations.

        Maps to ``sonar.coverage.exclusions``.

        :default: - no coverage exclusions

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeCoverageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeCpdOptions",
    jsii_struct_bases=[],
    name_mapping={"exclusions": "exclusions"},
)
class SonarqubeCpdOptions:
    def __init__(
        self,
        *,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.cpd.*`` properties.

        :param exclusions: (experimental) Comma-separated file path patterns to exclude from code duplication detection. Maps to ``sonar.cpd.exclusions``. Default: - no duplication exclusions

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0cf0b7b26cf704d304e8db90268127d3964dc0335fd35c98381a5a687898e593)
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated file path patterns to exclude from code duplication detection.

        Maps to ``sonar.cpd.exclusions``.

        :default: - no duplication exclusions

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeCpdOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeFileOptions",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "committed": "committed",
        "marker": "marker",
        "readonly": "readonly",
    },
)
class SonarqubeFileOptions:
    def __init__(
        self,
        *,
        comment: typing.Optional[typing.Sequence[builtins.str]] = None,
        committed: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) File options for the generated ``sonar-project.properties`` file.

        :param comment: (experimental) A comment to include at the top of the file. Default: - no additional comment
        :param committed: (experimental) Whether the generated file should be committed to git. Default: true
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__783c3c18d13f6c2abbee60deeea0346f3ec9f8ac9c3934296d7bb4c81cb136be)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if committed is not None:
            self._values["committed"] = committed
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly

    @builtins.property
    def comment(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A comment to include at the top of the file.

        :default: - no additional comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be committed to git.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeJavascriptOptions",
    jsii_struct_bases=[],
    name_mapping={"lcov": "lcov"},
)
class SonarqubeJavascriptOptions:
    def __init__(
        self,
        *,
        lcov: typing.Optional[typing.Union["SonarqubeLcovOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.javascript.*`` properties.

        :param lcov: (experimental) Options for ``sonar.javascript.lcov.*``. Default: - no LCOV configuration

        :stability: experimental
        '''
        if isinstance(lcov, dict):
            lcov = SonarqubeLcovOptions(**lcov)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__49f834c072e3e82c664ebf087e9824337838420df13be0ac2466beca64f33bcd)
            check_type(argname="argument lcov", value=lcov, expected_type=type_hints["lcov"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lcov is not None:
            self._values["lcov"] = lcov

    @builtins.property
    def lcov(self) -> typing.Optional["SonarqubeLcovOptions"]:
        '''(experimental) Options for ``sonar.javascript.lcov.*``.

        :default: - no LCOV configuration

        :stability: experimental
        '''
        result = self._values.get("lcov")
        return typing.cast(typing.Optional["SonarqubeLcovOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeJavascriptOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeLcovOptions",
    jsii_struct_bases=[],
    name_mapping={"report_paths": "reportPaths"},
)
class SonarqubeLcovOptions:
    def __init__(
        self,
        *,
        report_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for lcov report paths (shared between languages).

        :param report_paths: (experimental) Comma-separated paths to LCOV coverage report files. Maps to ``sonar.<language>.lcov.reportPaths``. Default: - not set

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d2f1bb64a6068c39051c30b18f7a44a63b48a91ebf8417855ad011e16f450e8d)
            check_type(argname="argument report_paths", value=report_paths, expected_type=type_hints["report_paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if report_paths is not None:
            self._values["report_paths"] = report_paths

    @builtins.property
    def report_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated paths to LCOV coverage report files.

        Maps to ``sonar.<language>.lcov.reportPaths``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("report_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeLcovOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.sonarqube.SonarqubeLogLevel")
class SonarqubeLogLevel(enum.Enum):
    '''(experimental) Log level for SonarQube analysis.

    :stability: experimental
    '''

    INFO = "INFO"
    '''(experimental) Standard logging (default).

    :stability: experimental
    '''
    DEBUG = "DEBUG"
    '''(experimental) Verbose logging.

    :stability: experimental
    '''
    TRACE = "TRACE"
    '''(experimental) Most verbose, includes plugin/library output.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeLogOptions",
    jsii_struct_bases=[],
    name_mapping={"level": "level"},
)
class SonarqubeLogOptions:
    def __init__(self, *, level: typing.Optional["SonarqubeLogLevel"] = None) -> None:
        '''(experimental) Options for ``sonar.log.*`` properties.

        :param level: (experimental) Controls the quantity/level of logs produced during analysis. Maps to ``sonar.log.level``. Default: SonarqubeLogLevel.INFO

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cbae29a71c88e1ea8f1091033076251b5ebe8552cbb2df1357a964fa1aae0945)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if level is not None:
            self._values["level"] = level

    @builtins.property
    def level(self) -> typing.Optional["SonarqubeLogLevel"]:
        '''(experimental) Controls the quantity/level of logs produced during analysis.

        Maps to ``sonar.log.level``.

        :default: SonarqubeLogLevel.INFO

        :stability: experimental
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional["SonarqubeLogLevel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SonarqubeProperties(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.sonarqube.SonarqubeProperties",
):
    '''(experimental) Manages the ``sonar-project.properties`` configuration file for SonarQube analysis.

    This component generates a ``sonar-project.properties`` file at the project
    root with the specified configuration parameters. It provides typed options
    whose structure mirrors the dot-notation property namespaces.

    :see: https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/analysis-parameters/parameters-not-settable-in-ui
    :stability: experimental

    Example::

        new SonarqubeProperties(project, {
          projectKey: 'my-org_my-project',
          organization: 'my-org',
          sources: 'src',
          tests: 'test',
          exclusions: ['*{@literal *}/node_modules/**'],
          coverage: { exclusions: ['*{@literal *}/test/**'] },
          javascript: { lcov: { reportPaths: ['coverage/lcov.info'] } },
          sourceEncoding: 'UTF-8',
        });
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.IConstruct",
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d032a848399835b60247bb0c3958b3727bde6832f2dbf6f72022aafd8eaaf2ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = SonarqubePropertiesOptions(
            project_key=project_key,
            coverage=coverage,
            cpd=cpd,
            exclusions=exclusions,
            extra_properties=extra_properties,
            file_options=file_options,
            javascript=javascript,
            language=language,
            log=log,
            organization=organization,
            profile=profile,
            project_base_dir=project_base_dir,
            project_name=project_name,
            project_version=project_version,
            qualitygate=qualitygate,
            region=region,
            rust=rust,
            scm=scm,
            source_encoding=source_encoding,
            sources=sources,
            tests=tests,
            typescript=typescript,
        )

        jsii.create(self.__class__, self, [scope, options])

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> "_projen_04054675.PropertiesFile":
        '''(experimental) The underlying properties file.

        :stability: experimental
        '''
        return typing.cast("_projen_04054675.PropertiesFile", jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubePropertiesOptions",
    jsii_struct_bases=[],
    name_mapping={
        "project_key": "projectKey",
        "coverage": "coverage",
        "cpd": "cpd",
        "exclusions": "exclusions",
        "extra_properties": "extraProperties",
        "file_options": "fileOptions",
        "javascript": "javascript",
        "language": "language",
        "log": "log",
        "organization": "organization",
        "profile": "profile",
        "project_base_dir": "projectBaseDir",
        "project_name": "projectName",
        "project_version": "projectVersion",
        "qualitygate": "qualitygate",
        "region": "region",
        "rust": "rust",
        "scm": "scm",
        "source_encoding": "sourceEncoding",
        "sources": "sources",
        "tests": "tests",
        "typescript": "typescript",
    },
)
class SonarqubePropertiesOptions:
    def __init__(
        self,
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``SonarqubeProperties``.

        The interface structure mirrors the ``sonar.*`` dot-notation used in
        ``sonar-project.properties``. Nested interfaces map to nested property
        namespaces. For example, ``scm.provider`` maps to ``sonar.scm.provider``.

        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if isinstance(coverage, dict):
            coverage = SonarqubeCoverageOptions(**coverage)
        if isinstance(cpd, dict):
            cpd = SonarqubeCpdOptions(**cpd)
        if isinstance(file_options, dict):
            file_options = SonarqubeFileOptions(**file_options)
        if isinstance(javascript, dict):
            javascript = SonarqubeJavascriptOptions(**javascript)
        if isinstance(log, dict):
            log = SonarqubeLogOptions(**log)
        if isinstance(qualitygate, dict):
            qualitygate = SonarqubeQualityGateOptions(**qualitygate)
        if isinstance(rust, dict):
            rust = SonarqubeRustOptions(**rust)
        if isinstance(scm, dict):
            scm = SonarqubeScmOptions(**scm)
        if isinstance(typescript, dict):
            typescript = SonarqubeTypescriptOptions(**typescript)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a2903e34d199955ec4b3395ac11813643349a6bc12046316b13284cfd461b692)
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument coverage", value=coverage, expected_type=type_hints["coverage"])
            check_type(argname="argument cpd", value=cpd, expected_type=type_hints["cpd"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument extra_properties", value=extra_properties, expected_type=type_hints["extra_properties"])
            check_type(argname="argument file_options", value=file_options, expected_type=type_hints["file_options"])
            check_type(argname="argument javascript", value=javascript, expected_type=type_hints["javascript"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument project_base_dir", value=project_base_dir, expected_type=type_hints["project_base_dir"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument project_version", value=project_version, expected_type=type_hints["project_version"])
            check_type(argname="argument qualitygate", value=qualitygate, expected_type=type_hints["qualitygate"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rust", value=rust, expected_type=type_hints["rust"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
            check_type(argname="argument source_encoding", value=source_encoding, expected_type=type_hints["source_encoding"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tests", value=tests, expected_type=type_hints["tests"])
            check_type(argname="argument typescript", value=typescript, expected_type=type_hints["typescript"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_key": project_key,
        }
        if coverage is not None:
            self._values["coverage"] = coverage
        if cpd is not None:
            self._values["cpd"] = cpd
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if extra_properties is not None:
            self._values["extra_properties"] = extra_properties
        if file_options is not None:
            self._values["file_options"] = file_options
        if javascript is not None:
            self._values["javascript"] = javascript
        if language is not None:
            self._values["language"] = language
        if log is not None:
            self._values["log"] = log
        if organization is not None:
            self._values["organization"] = organization
        if profile is not None:
            self._values["profile"] = profile
        if project_base_dir is not None:
            self._values["project_base_dir"] = project_base_dir
        if project_name is not None:
            self._values["project_name"] = project_name
        if project_version is not None:
            self._values["project_version"] = project_version
        if qualitygate is not None:
            self._values["qualitygate"] = qualitygate
        if region is not None:
            self._values["region"] = region
        if rust is not None:
            self._values["rust"] = rust
        if scm is not None:
            self._values["scm"] = scm
        if source_encoding is not None:
            self._values["source_encoding"] = source_encoding
        if sources is not None:
            self._values["sources"] = sources
        if tests is not None:
            self._values["tests"] = tests
        if typescript is not None:
            self._values["typescript"] = typescript

    @builtins.property
    def project_key(self) -> builtins.str:
        '''(experimental) The project's unique key.

        Can include up to 400 characters. Allowed characters:
        letters, digits, dash, underscore, periods, and colons.

        Maps to ``sonar.projectKey``. This parameter is mandatory.

        :stability: experimental
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def coverage(self) -> typing.Optional["SonarqubeCoverageOptions"]:
        '''(experimental) Coverage-related options (``sonar.coverage.*``).

        :default: - no coverage configuration

        :stability: experimental
        '''
        result = self._values.get("coverage")
        return typing.cast(typing.Optional["SonarqubeCoverageOptions"], result)

    @builtins.property
    def cpd(self) -> typing.Optional["SonarqubeCpdOptions"]:
        '''(experimental) Duplication detection options (``sonar.cpd.*``).

        :default: - no CPD configuration

        :stability: experimental
        '''
        result = self._values.get("cpd")
        return typing.cast(typing.Optional["SonarqubeCpdOptions"], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated file path patterns to exclude from the analysis scope.

        Maps to ``sonar.exclusions``.

        :default: - no exclusions

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extra_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional arbitrary properties to include in the configuration.

        Use this for properties not covered by the typed options.
        Keys use dot-notation (e.g., ``sonar.java.binaries``).

        These are applied as overrides after the typed options above, so a key
        that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces
        that entire subtree rather than merging with it.

        :default: - no additional properties

        :stability: experimental
        '''
        result = self._values.get("extra_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file_options(self) -> typing.Optional["SonarqubeFileOptions"]:
        '''(experimental) Options for the generated properties file.

        :default: - default file options

        :stability: experimental
        '''
        result = self._values.get("file_options")
        return typing.cast(typing.Optional["SonarqubeFileOptions"], result)

    @builtins.property
    def javascript(self) -> typing.Optional["SonarqubeJavascriptOptions"]:
        '''(experimental) JavaScript-specific options (``sonar.javascript.*``).

        :default: - no JavaScript configuration

        :stability: experimental
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["SonarqubeJavascriptOptions"], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''(experimental) The language for analysis.

        Maps to ``sonar.language``.

        :default: - auto-detected

        :stability: experimental
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log(self) -> typing.Optional["SonarqubeLogOptions"]:
        '''(experimental) Logging options (``sonar.log.*``).

        :default: - INFO level

        :stability: experimental
        '''
        result = self._values.get("log")
        return typing.cast(typing.Optional["SonarqubeLogOptions"], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the organization to which the project belongs.

        Maps to ``sonar.organization``. Mandatory for SonarQube Cloud.

        :default: - no organization

        :stability: experimental
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) The quality profile name.

        Maps to ``sonar.profile``.

        :default: - uses the default profile configured on the server

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_base_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started.

        Maps to ``sonar.projectBaseDir``.

        :default: - the directory from which the analysis was started

        :stability: experimental
        '''
        result = self._values.get("project_base_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the project displayed on the web interface.

        Maps to ``sonar.projectName``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project version.

        Maps to ``sonar.projectVersion``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualitygate(self) -> typing.Optional["SonarqubeQualityGateOptions"]:
        '''(experimental) Quality gate options (``sonar.qualitygate.*``).

        :default: - quality gate not awaited

        :stability: experimental
        '''
        result = self._values.get("qualitygate")
        return typing.cast(typing.Optional["SonarqubeQualityGateOptions"], result)

    @builtins.property
    def region(self) -> typing.Optional["SonarqubeRegion"]:
        '''(experimental) The SonarQube Cloud instance's region.

        Maps to ``sonar.region``.

        :default: SonarqubeRegion.EU

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional["SonarqubeRegion"], result)

    @builtins.property
    def rust(self) -> typing.Optional["SonarqubeRustOptions"]:
        '''(experimental) Rust-specific options (``sonar.rust.*``).

        :default: - no Rust configuration

        :stability: experimental
        '''
        result = self._values.get("rust")
        return typing.cast(typing.Optional["SonarqubeRustOptions"], result)

    @builtins.property
    def scm(self) -> typing.Optional["SonarqubeScmOptions"]:
        '''(experimental) SCM-related options (``sonar.scm.*``).

        :default: - no SCM configuration

        :stability: experimental
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional["SonarqubeScmOptions"], result)

    @builtins.property
    def source_encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) Encoding of the source files.

        Maps to ``sonar.sourceEncoding``.

        :default: - system encoding

        :stability: experimental
        '''
        result = self._values.get("source_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing main source code (non-test code).

        Maps to ``sonar.sources``.

        :default: - the project base directory

        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tests(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing test code.

        Maps to ``sonar.tests``.

        :default: - no test code analyzed

        :stability: experimental
        '''
        result = self._values.get("tests")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def typescript(self) -> typing.Optional["SonarqubeTypescriptOptions"]:
        '''(experimental) TypeScript-specific options (``sonar.typescript.*``).

        :default: - no TypeScript configuration

        :stability: experimental
        '''
        result = self._values.get("typescript")
        return typing.cast(typing.Optional["SonarqubeTypescriptOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubePropertiesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeQualityGateOptions",
    jsii_struct_bases=[],
    name_mapping={"timeout": "timeout", "wait": "wait"},
)
class SonarqubeQualityGateOptions:
    def __init__(
        self,
        *,
        timeout: typing.Optional[jsii.Number] = None,
        wait: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.qualitygate.*`` properties.

        :param timeout: (experimental) The number of seconds that the scanner should wait for a report to be processed. Maps to ``sonar.qualitygate.timeout``. Default: 300
        :param wait: (experimental) Forces the analysis step to poll the server and wait for the Quality Gate status. Will fail the pipeline if the quality gate fails. Maps to ``sonar.qualitygate.wait``. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1751ee9928717822a44e53a063c9bd184cbc4ec627b8a8c882e1be83584b80b4)
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if timeout is not None:
            self._values["timeout"] = timeout
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of seconds that the scanner should wait for a report to be processed.

        Maps to ``sonar.qualitygate.timeout``.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Forces the analysis step to poll the server and wait for the Quality Gate status.

        Will fail the pipeline if the quality gate fails.

        Maps to ``sonar.qualitygate.wait``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeQualityGateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.sonarqube.SonarqubeRegion")
class SonarqubeRegion(enum.Enum):
    '''(experimental) SonarQube Cloud region.

    :stability: experimental
    '''

    EU = "EU"
    '''(experimental) EU instance (default).

    :stability: experimental
    '''
    US = "US"
    '''(experimental) US instance.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeRustClippyOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class SonarqubeRustClippyOptions:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for ``sonar.rust.clippy.*`` properties.

        :param enabled: (experimental) Whether Clippy analysis is enabled. Maps to ``sonar.rust.clippy.enabled``. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ec45e69ebbd11008a7827e535a23bd4abd48d8edc4c291f3d0ee7e886a398187)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Clippy analysis is enabled.

        Maps to ``sonar.rust.clippy.enabled``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeRustClippyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeRustClippyReportOptions",
    jsii_struct_bases=[],
    name_mapping={"report_paths": "reportPaths"},
)
class SonarqubeRustClippyReportOptions:
    def __init__(
        self,
        *,
        report_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.rust.clippyReport.*`` properties.

        :param report_paths: (experimental) Paths to Clippy JSON report files. Maps to ``sonar.rust.clippyReport.reportPaths``. Default: - not set

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7b93e70be08a603e21119fcfa30c99dc0ba028ecd5990d8ba06a459ba1ceaff)
            check_type(argname="argument report_paths", value=report_paths, expected_type=type_hints["report_paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if report_paths is not None:
            self._values["report_paths"] = report_paths

    @builtins.property
    def report_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Paths to Clippy JSON report files.

        Maps to ``sonar.rust.clippyReport.reportPaths``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("report_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeRustClippyReportOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeRustOptions",
    jsii_struct_bases=[],
    name_mapping={"clippy": "clippy", "clippy_report": "clippyReport", "lcov": "lcov"},
)
class SonarqubeRustOptions:
    def __init__(
        self,
        *,
        clippy: typing.Optional[typing.Union["SonarqubeRustClippyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        clippy_report: typing.Optional[typing.Union["SonarqubeRustClippyReportOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        lcov: typing.Optional[typing.Union["SonarqubeLcovOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.rust.*`` properties.

        :param clippy: (experimental) Options for ``sonar.rust.clippy.*``. Default: - no clippy configuration
        :param clippy_report: (experimental) Options for ``sonar.rust.clippyReport.*``. Default: - no clippy report configuration
        :param lcov: (experimental) Options for ``sonar.rust.lcov.*``. Default: - no Rust LCOV configuration

        :stability: experimental
        '''
        if isinstance(clippy, dict):
            clippy = SonarqubeRustClippyOptions(**clippy)
        if isinstance(clippy_report, dict):
            clippy_report = SonarqubeRustClippyReportOptions(**clippy_report)
        if isinstance(lcov, dict):
            lcov = SonarqubeLcovOptions(**lcov)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__43b4e9c03fd0a21e993b5a56715a14a484f7092e2942379b10280387e962f6ab)
            check_type(argname="argument clippy", value=clippy, expected_type=type_hints["clippy"])
            check_type(argname="argument clippy_report", value=clippy_report, expected_type=type_hints["clippy_report"])
            check_type(argname="argument lcov", value=lcov, expected_type=type_hints["lcov"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if clippy is not None:
            self._values["clippy"] = clippy
        if clippy_report is not None:
            self._values["clippy_report"] = clippy_report
        if lcov is not None:
            self._values["lcov"] = lcov

    @builtins.property
    def clippy(self) -> typing.Optional["SonarqubeRustClippyOptions"]:
        '''(experimental) Options for ``sonar.rust.clippy.*``.

        :default: - no clippy configuration

        :stability: experimental
        '''
        result = self._values.get("clippy")
        return typing.cast(typing.Optional["SonarqubeRustClippyOptions"], result)

    @builtins.property
    def clippy_report(self) -> typing.Optional["SonarqubeRustClippyReportOptions"]:
        '''(experimental) Options for ``sonar.rust.clippyReport.*``.

        :default: - no clippy report configuration

        :stability: experimental
        '''
        result = self._values.get("clippy_report")
        return typing.cast(typing.Optional["SonarqubeRustClippyReportOptions"], result)

    @builtins.property
    def lcov(self) -> typing.Optional["SonarqubeLcovOptions"]:
        '''(experimental) Options for ``sonar.rust.lcov.*``.

        :default: - no Rust LCOV configuration

        :stability: experimental
        '''
        result = self._values.get("lcov")
        return typing.cast(typing.Optional["SonarqubeLcovOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeRustOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SonarqubeRustProperties(
    SonarqubeProperties,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.sonarqube.SonarqubeRustProperties",
):
    '''(experimental) A SonarQube configuration preset for Rust projects.

    Provides sensible defaults for Rust analysis:

    - ``sonar.language`` = ``rust``
    - ``sonar.sources`` = ``src``
    - ``sonar.tests`` = ``tests``
    - ``sonar.sourceEncoding`` = ``UTF-8``
    - ``sonar.profile`` = ``Sonar Way``
    - ``sonar.scm.provider`` = ``git``
    - Typical exclusions for ``coverage``, test, and ``target`` dirs
    - ``sonar.rust.lcov.reportPaths`` = ``target/lcov.info``
    - ``sonar.rust.clippy.enabled`` = ``false``
    - ``sonar.rust.clippyReport.reportPaths`` = ``target/clippy.json``

    All defaults can be overridden via options. Nested options (e.g. ``coverage``,
    ``rust``) are deep-merged with the defaults, so overriding one nested field
    does not drop the other defaults in that subtree.

    :stability: experimental

    Example::

        new SonarqubeRustProperties(project, {
          projectKey: 'my-org_my-rust-project',
        });
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.IConstruct",
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d3203229f162bdb4a5861a63f3eac5203d5840e2dd887f5ec2aaefb390efb42e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = SonarqubeRustPropertiesOptions(
            project_key=project_key,
            coverage=coverage,
            cpd=cpd,
            exclusions=exclusions,
            extra_properties=extra_properties,
            file_options=file_options,
            javascript=javascript,
            language=language,
            log=log,
            organization=organization,
            profile=profile,
            project_base_dir=project_base_dir,
            project_name=project_name,
            project_version=project_version,
            qualitygate=qualitygate,
            region=region,
            rust=rust,
            scm=scm,
            source_encoding=source_encoding,
            sources=sources,
            tests=tests,
            typescript=typescript,
        )

        jsii.create(self.__class__, self, [scope, options])


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeRustPropertiesOptions",
    jsii_struct_bases=[SonarqubePropertiesOptions],
    name_mapping={
        "project_key": "projectKey",
        "coverage": "coverage",
        "cpd": "cpd",
        "exclusions": "exclusions",
        "extra_properties": "extraProperties",
        "file_options": "fileOptions",
        "javascript": "javascript",
        "language": "language",
        "log": "log",
        "organization": "organization",
        "profile": "profile",
        "project_base_dir": "projectBaseDir",
        "project_name": "projectName",
        "project_version": "projectVersion",
        "qualitygate": "qualitygate",
        "region": "region",
        "rust": "rust",
        "scm": "scm",
        "source_encoding": "sourceEncoding",
        "sources": "sources",
        "tests": "tests",
        "typescript": "typescript",
    },
)
class SonarqubeRustPropertiesOptions(SonarqubePropertiesOptions):
    def __init__(
        self,
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``SonarqubeRustProperties``.

        Extends base options with Rust-specific defaults.

        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if isinstance(coverage, dict):
            coverage = SonarqubeCoverageOptions(**coverage)
        if isinstance(cpd, dict):
            cpd = SonarqubeCpdOptions(**cpd)
        if isinstance(file_options, dict):
            file_options = SonarqubeFileOptions(**file_options)
        if isinstance(javascript, dict):
            javascript = SonarqubeJavascriptOptions(**javascript)
        if isinstance(log, dict):
            log = SonarqubeLogOptions(**log)
        if isinstance(qualitygate, dict):
            qualitygate = SonarqubeQualityGateOptions(**qualitygate)
        if isinstance(rust, dict):
            rust = SonarqubeRustOptions(**rust)
        if isinstance(scm, dict):
            scm = SonarqubeScmOptions(**scm)
        if isinstance(typescript, dict):
            typescript = SonarqubeTypescriptOptions(**typescript)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2ad05c13b54541e0cda8b6d0b5a26b3d9a4bb8bf18df593c22d342077c8f2caa)
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument coverage", value=coverage, expected_type=type_hints["coverage"])
            check_type(argname="argument cpd", value=cpd, expected_type=type_hints["cpd"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument extra_properties", value=extra_properties, expected_type=type_hints["extra_properties"])
            check_type(argname="argument file_options", value=file_options, expected_type=type_hints["file_options"])
            check_type(argname="argument javascript", value=javascript, expected_type=type_hints["javascript"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument project_base_dir", value=project_base_dir, expected_type=type_hints["project_base_dir"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument project_version", value=project_version, expected_type=type_hints["project_version"])
            check_type(argname="argument qualitygate", value=qualitygate, expected_type=type_hints["qualitygate"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rust", value=rust, expected_type=type_hints["rust"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
            check_type(argname="argument source_encoding", value=source_encoding, expected_type=type_hints["source_encoding"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tests", value=tests, expected_type=type_hints["tests"])
            check_type(argname="argument typescript", value=typescript, expected_type=type_hints["typescript"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_key": project_key,
        }
        if coverage is not None:
            self._values["coverage"] = coverage
        if cpd is not None:
            self._values["cpd"] = cpd
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if extra_properties is not None:
            self._values["extra_properties"] = extra_properties
        if file_options is not None:
            self._values["file_options"] = file_options
        if javascript is not None:
            self._values["javascript"] = javascript
        if language is not None:
            self._values["language"] = language
        if log is not None:
            self._values["log"] = log
        if organization is not None:
            self._values["organization"] = organization
        if profile is not None:
            self._values["profile"] = profile
        if project_base_dir is not None:
            self._values["project_base_dir"] = project_base_dir
        if project_name is not None:
            self._values["project_name"] = project_name
        if project_version is not None:
            self._values["project_version"] = project_version
        if qualitygate is not None:
            self._values["qualitygate"] = qualitygate
        if region is not None:
            self._values["region"] = region
        if rust is not None:
            self._values["rust"] = rust
        if scm is not None:
            self._values["scm"] = scm
        if source_encoding is not None:
            self._values["source_encoding"] = source_encoding
        if sources is not None:
            self._values["sources"] = sources
        if tests is not None:
            self._values["tests"] = tests
        if typescript is not None:
            self._values["typescript"] = typescript

    @builtins.property
    def project_key(self) -> builtins.str:
        '''(experimental) The project's unique key.

        Can include up to 400 characters. Allowed characters:
        letters, digits, dash, underscore, periods, and colons.

        Maps to ``sonar.projectKey``. This parameter is mandatory.

        :stability: experimental
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def coverage(self) -> typing.Optional["SonarqubeCoverageOptions"]:
        '''(experimental) Coverage-related options (``sonar.coverage.*``).

        :default: - no coverage configuration

        :stability: experimental
        '''
        result = self._values.get("coverage")
        return typing.cast(typing.Optional["SonarqubeCoverageOptions"], result)

    @builtins.property
    def cpd(self) -> typing.Optional["SonarqubeCpdOptions"]:
        '''(experimental) Duplication detection options (``sonar.cpd.*``).

        :default: - no CPD configuration

        :stability: experimental
        '''
        result = self._values.get("cpd")
        return typing.cast(typing.Optional["SonarqubeCpdOptions"], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated file path patterns to exclude from the analysis scope.

        Maps to ``sonar.exclusions``.

        :default: - no exclusions

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extra_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional arbitrary properties to include in the configuration.

        Use this for properties not covered by the typed options.
        Keys use dot-notation (e.g., ``sonar.java.binaries``).

        These are applied as overrides after the typed options above, so a key
        that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces
        that entire subtree rather than merging with it.

        :default: - no additional properties

        :stability: experimental
        '''
        result = self._values.get("extra_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file_options(self) -> typing.Optional["SonarqubeFileOptions"]:
        '''(experimental) Options for the generated properties file.

        :default: - default file options

        :stability: experimental
        '''
        result = self._values.get("file_options")
        return typing.cast(typing.Optional["SonarqubeFileOptions"], result)

    @builtins.property
    def javascript(self) -> typing.Optional["SonarqubeJavascriptOptions"]:
        '''(experimental) JavaScript-specific options (``sonar.javascript.*``).

        :default: - no JavaScript configuration

        :stability: experimental
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["SonarqubeJavascriptOptions"], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''(experimental) The language for analysis.

        Maps to ``sonar.language``.

        :default: - auto-detected

        :stability: experimental
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log(self) -> typing.Optional["SonarqubeLogOptions"]:
        '''(experimental) Logging options (``sonar.log.*``).

        :default: - INFO level

        :stability: experimental
        '''
        result = self._values.get("log")
        return typing.cast(typing.Optional["SonarqubeLogOptions"], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the organization to which the project belongs.

        Maps to ``sonar.organization``. Mandatory for SonarQube Cloud.

        :default: - no organization

        :stability: experimental
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) The quality profile name.

        Maps to ``sonar.profile``.

        :default: - uses the default profile configured on the server

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_base_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started.

        Maps to ``sonar.projectBaseDir``.

        :default: - the directory from which the analysis was started

        :stability: experimental
        '''
        result = self._values.get("project_base_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the project displayed on the web interface.

        Maps to ``sonar.projectName``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project version.

        Maps to ``sonar.projectVersion``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualitygate(self) -> typing.Optional["SonarqubeQualityGateOptions"]:
        '''(experimental) Quality gate options (``sonar.qualitygate.*``).

        :default: - quality gate not awaited

        :stability: experimental
        '''
        result = self._values.get("qualitygate")
        return typing.cast(typing.Optional["SonarqubeQualityGateOptions"], result)

    @builtins.property
    def region(self) -> typing.Optional["SonarqubeRegion"]:
        '''(experimental) The SonarQube Cloud instance's region.

        Maps to ``sonar.region``.

        :default: SonarqubeRegion.EU

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional["SonarqubeRegion"], result)

    @builtins.property
    def rust(self) -> typing.Optional["SonarqubeRustOptions"]:
        '''(experimental) Rust-specific options (``sonar.rust.*``).

        :default: - no Rust configuration

        :stability: experimental
        '''
        result = self._values.get("rust")
        return typing.cast(typing.Optional["SonarqubeRustOptions"], result)

    @builtins.property
    def scm(self) -> typing.Optional["SonarqubeScmOptions"]:
        '''(experimental) SCM-related options (``sonar.scm.*``).

        :default: - no SCM configuration

        :stability: experimental
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional["SonarqubeScmOptions"], result)

    @builtins.property
    def source_encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) Encoding of the source files.

        Maps to ``sonar.sourceEncoding``.

        :default: - system encoding

        :stability: experimental
        '''
        result = self._values.get("source_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing main source code (non-test code).

        Maps to ``sonar.sources``.

        :default: - the project base directory

        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tests(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing test code.

        Maps to ``sonar.tests``.

        :default: - no test code analyzed

        :stability: experimental
        '''
        result = self._values.get("tests")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def typescript(self) -> typing.Optional["SonarqubeTypescriptOptions"]:
        '''(experimental) TypeScript-specific options (``sonar.typescript.*``).

        :default: - no TypeScript configuration

        :stability: experimental
        '''
        result = self._values.get("typescript")
        return typing.cast(typing.Optional["SonarqubeTypescriptOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeRustPropertiesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeScmExclusionsOptions",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled"},
)
class SonarqubeScmExclusionsOptions:
    def __init__(self, *, disabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for ``sonar.scm.exclusions.*`` properties.

        :param disabled: (experimental) Whether to disable files ignored by the SCM (e.g., files in .gitignore) from being excluded from analysis. Maps to ``sonar.scm.exclusions.disabled``. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__716e6044727f1fa46c3448e8e2712c00d1e863fed1867d1e85ebe4ffa1a3f3be)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to disable files ignored by the SCM (e.g., files in .gitignore) from being excluded from analysis.

        Maps to ``sonar.scm.exclusions.disabled``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeScmExclusionsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeScmOptions",
    jsii_struct_bases=[],
    name_mapping={"exclusions": "exclusions", "provider": "provider"},
)
class SonarqubeScmOptions:
    def __init__(
        self,
        *,
        exclusions: typing.Optional[typing.Union["SonarqubeScmExclusionsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``sonar.scm.*`` properties.

        :param exclusions: (experimental) Options for ``sonar.scm.exclusions.*``. Default: - no exclusion overrides
        :param provider: (experimental) The SCM provider to use. Maps to ``sonar.scm.provider``. Default: - auto-detected

        :stability: experimental
        '''
        if isinstance(exclusions, dict):
            exclusions = SonarqubeScmExclusionsOptions(**exclusions)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__57a0799e1adff2395176aac608256f7abdd0f1292e6ef8f9a5f33a41d61b5c2b)
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def exclusions(self) -> typing.Optional["SonarqubeScmExclusionsOptions"]:
        '''(experimental) Options for ``sonar.scm.exclusions.*``.

        :default: - no exclusion overrides

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional["SonarqubeScmExclusionsOptions"], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''(experimental) The SCM provider to use.

        Maps to ``sonar.scm.provider``.

        :default: - auto-detected

        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeScmOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeTypescriptOptions",
    jsii_struct_bases=[],
    name_mapping={"tsconfig_path": "tsconfigPath"},
)
class SonarqubeTypescriptOptions:
    def __init__(self, *, tsconfig_path: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Options for ``sonar.typescript.*`` properties.

        :param tsconfig_path: (experimental) Path to the TypeScript configuration file. Maps to ``sonar.typescript.tsconfigPath``. Default: - not set

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d239110ecf824c542fa4c6258b08f69d3facda43eb3676199ca490bc1a8a215b)
            check_type(argname="argument tsconfig_path", value=tsconfig_path, expected_type=type_hints["tsconfig_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tsconfig_path is not None:
            self._values["tsconfig_path"] = tsconfig_path

    @builtins.property
    def tsconfig_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the TypeScript configuration file.

        Maps to ``sonar.typescript.tsconfigPath``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("tsconfig_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeTypescriptOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SonarqubeTypescriptProperties(
    SonarqubeProperties,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.sonarqube.SonarqubeTypescriptProperties",
):
    '''(experimental) A SonarQube configuration preset for TypeScript projects.

    Provides sensible defaults for TypeScript analysis:

    - ``sonar.language`` = ``ts``
    - ``sonar.sources`` = ``src``
    - ``sonar.tests`` = ``test``
    - ``sonar.sourceEncoding`` = ``UTF-8``
    - ``sonar.profile`` = ``Sonar Way``
    - ``sonar.scm.provider`` = ``git``
    - ``sonar.typescript.tsconfigPath`` = ``tsconfig.json``
    - Typical exclusions for ``node_modules``, ``coverage``, test files
    - ``sonar.javascript.lcov.reportPaths`` = ``coverage/lcov.info``

    All defaults can be overridden via options. Nested options (e.g. ``coverage``,
    ``javascript``) are deep-merged with the defaults, so overriding one nested
    field does not drop the other defaults in that subtree.

    :stability: experimental

    Example::

        new SonarqubeTypescriptProperties(project, {
          projectKey: 'my-org_my-ts-project',
        });
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.IConstruct",
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8d766f5f1a4b8059fe48532815dc8d56c10063ce0c2f591bbb1b399b4bcfa387)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = SonarqubeTypescriptPropertiesOptions(
            project_key=project_key,
            coverage=coverage,
            cpd=cpd,
            exclusions=exclusions,
            extra_properties=extra_properties,
            file_options=file_options,
            javascript=javascript,
            language=language,
            log=log,
            organization=organization,
            profile=profile,
            project_base_dir=project_base_dir,
            project_name=project_name,
            project_version=project_version,
            qualitygate=qualitygate,
            region=region,
            rust=rust,
            scm=scm,
            source_encoding=source_encoding,
            sources=sources,
            tests=tests,
            typescript=typescript,
        )

        jsii.create(self.__class__, self, [scope, options])


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeTypescriptPropertiesOptions",
    jsii_struct_bases=[SonarqubePropertiesOptions],
    name_mapping={
        "project_key": "projectKey",
        "coverage": "coverage",
        "cpd": "cpd",
        "exclusions": "exclusions",
        "extra_properties": "extraProperties",
        "file_options": "fileOptions",
        "javascript": "javascript",
        "language": "language",
        "log": "log",
        "organization": "organization",
        "profile": "profile",
        "project_base_dir": "projectBaseDir",
        "project_name": "projectName",
        "project_version": "projectVersion",
        "qualitygate": "qualitygate",
        "region": "region",
        "rust": "rust",
        "scm": "scm",
        "source_encoding": "sourceEncoding",
        "sources": "sources",
        "tests": "tests",
        "typescript": "typescript",
    },
)
class SonarqubeTypescriptPropertiesOptions(SonarqubePropertiesOptions):
    def __init__(
        self,
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``SonarqubeTypescriptProperties``.

        Extends base options with TypeScript-specific defaults.

        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if isinstance(coverage, dict):
            coverage = SonarqubeCoverageOptions(**coverage)
        if isinstance(cpd, dict):
            cpd = SonarqubeCpdOptions(**cpd)
        if isinstance(file_options, dict):
            file_options = SonarqubeFileOptions(**file_options)
        if isinstance(javascript, dict):
            javascript = SonarqubeJavascriptOptions(**javascript)
        if isinstance(log, dict):
            log = SonarqubeLogOptions(**log)
        if isinstance(qualitygate, dict):
            qualitygate = SonarqubeQualityGateOptions(**qualitygate)
        if isinstance(rust, dict):
            rust = SonarqubeRustOptions(**rust)
        if isinstance(scm, dict):
            scm = SonarqubeScmOptions(**scm)
        if isinstance(typescript, dict):
            typescript = SonarqubeTypescriptOptions(**typescript)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__88b81e841b21150947356e146bd990dfa855a8142f93c95742a6a38bd899ff70)
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument coverage", value=coverage, expected_type=type_hints["coverage"])
            check_type(argname="argument cpd", value=cpd, expected_type=type_hints["cpd"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument extra_properties", value=extra_properties, expected_type=type_hints["extra_properties"])
            check_type(argname="argument file_options", value=file_options, expected_type=type_hints["file_options"])
            check_type(argname="argument javascript", value=javascript, expected_type=type_hints["javascript"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument project_base_dir", value=project_base_dir, expected_type=type_hints["project_base_dir"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument project_version", value=project_version, expected_type=type_hints["project_version"])
            check_type(argname="argument qualitygate", value=qualitygate, expected_type=type_hints["qualitygate"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rust", value=rust, expected_type=type_hints["rust"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
            check_type(argname="argument source_encoding", value=source_encoding, expected_type=type_hints["source_encoding"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tests", value=tests, expected_type=type_hints["tests"])
            check_type(argname="argument typescript", value=typescript, expected_type=type_hints["typescript"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_key": project_key,
        }
        if coverage is not None:
            self._values["coverage"] = coverage
        if cpd is not None:
            self._values["cpd"] = cpd
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if extra_properties is not None:
            self._values["extra_properties"] = extra_properties
        if file_options is not None:
            self._values["file_options"] = file_options
        if javascript is not None:
            self._values["javascript"] = javascript
        if language is not None:
            self._values["language"] = language
        if log is not None:
            self._values["log"] = log
        if organization is not None:
            self._values["organization"] = organization
        if profile is not None:
            self._values["profile"] = profile
        if project_base_dir is not None:
            self._values["project_base_dir"] = project_base_dir
        if project_name is not None:
            self._values["project_name"] = project_name
        if project_version is not None:
            self._values["project_version"] = project_version
        if qualitygate is not None:
            self._values["qualitygate"] = qualitygate
        if region is not None:
            self._values["region"] = region
        if rust is not None:
            self._values["rust"] = rust
        if scm is not None:
            self._values["scm"] = scm
        if source_encoding is not None:
            self._values["source_encoding"] = source_encoding
        if sources is not None:
            self._values["sources"] = sources
        if tests is not None:
            self._values["tests"] = tests
        if typescript is not None:
            self._values["typescript"] = typescript

    @builtins.property
    def project_key(self) -> builtins.str:
        '''(experimental) The project's unique key.

        Can include up to 400 characters. Allowed characters:
        letters, digits, dash, underscore, periods, and colons.

        Maps to ``sonar.projectKey``. This parameter is mandatory.

        :stability: experimental
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def coverage(self) -> typing.Optional["SonarqubeCoverageOptions"]:
        '''(experimental) Coverage-related options (``sonar.coverage.*``).

        :default: - no coverage configuration

        :stability: experimental
        '''
        result = self._values.get("coverage")
        return typing.cast(typing.Optional["SonarqubeCoverageOptions"], result)

    @builtins.property
    def cpd(self) -> typing.Optional["SonarqubeCpdOptions"]:
        '''(experimental) Duplication detection options (``sonar.cpd.*``).

        :default: - no CPD configuration

        :stability: experimental
        '''
        result = self._values.get("cpd")
        return typing.cast(typing.Optional["SonarqubeCpdOptions"], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated file path patterns to exclude from the analysis scope.

        Maps to ``sonar.exclusions``.

        :default: - no exclusions

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extra_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional arbitrary properties to include in the configuration.

        Use this for properties not covered by the typed options.
        Keys use dot-notation (e.g., ``sonar.java.binaries``).

        These are applied as overrides after the typed options above, so a key
        that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces
        that entire subtree rather than merging with it.

        :default: - no additional properties

        :stability: experimental
        '''
        result = self._values.get("extra_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file_options(self) -> typing.Optional["SonarqubeFileOptions"]:
        '''(experimental) Options for the generated properties file.

        :default: - default file options

        :stability: experimental
        '''
        result = self._values.get("file_options")
        return typing.cast(typing.Optional["SonarqubeFileOptions"], result)

    @builtins.property
    def javascript(self) -> typing.Optional["SonarqubeJavascriptOptions"]:
        '''(experimental) JavaScript-specific options (``sonar.javascript.*``).

        :default: - no JavaScript configuration

        :stability: experimental
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["SonarqubeJavascriptOptions"], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''(experimental) The language for analysis.

        Maps to ``sonar.language``.

        :default: - auto-detected

        :stability: experimental
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log(self) -> typing.Optional["SonarqubeLogOptions"]:
        '''(experimental) Logging options (``sonar.log.*``).

        :default: - INFO level

        :stability: experimental
        '''
        result = self._values.get("log")
        return typing.cast(typing.Optional["SonarqubeLogOptions"], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the organization to which the project belongs.

        Maps to ``sonar.organization``. Mandatory for SonarQube Cloud.

        :default: - no organization

        :stability: experimental
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) The quality profile name.

        Maps to ``sonar.profile``.

        :default: - uses the default profile configured on the server

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_base_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started.

        Maps to ``sonar.projectBaseDir``.

        :default: - the directory from which the analysis was started

        :stability: experimental
        '''
        result = self._values.get("project_base_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the project displayed on the web interface.

        Maps to ``sonar.projectName``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project version.

        Maps to ``sonar.projectVersion``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualitygate(self) -> typing.Optional["SonarqubeQualityGateOptions"]:
        '''(experimental) Quality gate options (``sonar.qualitygate.*``).

        :default: - quality gate not awaited

        :stability: experimental
        '''
        result = self._values.get("qualitygate")
        return typing.cast(typing.Optional["SonarqubeQualityGateOptions"], result)

    @builtins.property
    def region(self) -> typing.Optional["SonarqubeRegion"]:
        '''(experimental) The SonarQube Cloud instance's region.

        Maps to ``sonar.region``.

        :default: SonarqubeRegion.EU

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional["SonarqubeRegion"], result)

    @builtins.property
    def rust(self) -> typing.Optional["SonarqubeRustOptions"]:
        '''(experimental) Rust-specific options (``sonar.rust.*``).

        :default: - no Rust configuration

        :stability: experimental
        '''
        result = self._values.get("rust")
        return typing.cast(typing.Optional["SonarqubeRustOptions"], result)

    @builtins.property
    def scm(self) -> typing.Optional["SonarqubeScmOptions"]:
        '''(experimental) SCM-related options (``sonar.scm.*``).

        :default: - no SCM configuration

        :stability: experimental
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional["SonarqubeScmOptions"], result)

    @builtins.property
    def source_encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) Encoding of the source files.

        Maps to ``sonar.sourceEncoding``.

        :default: - system encoding

        :stability: experimental
        '''
        result = self._values.get("source_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing main source code (non-test code).

        Maps to ``sonar.sources``.

        :default: - the project base directory

        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tests(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing test code.

        Maps to ``sonar.tests``.

        :default: - no test code analyzed

        :stability: experimental
        '''
        result = self._values.get("tests")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def typescript(self) -> typing.Optional["SonarqubeTypescriptOptions"]:
        '''(experimental) TypeScript-specific options (``sonar.typescript.*``).

        :default: - no TypeScript configuration

        :stability: experimental
        '''
        result = self._values.get("typescript")
        return typing.cast(typing.Optional["SonarqubeTypescriptOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeTypescriptPropertiesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SonarqubeJavascriptProperties(
    SonarqubeProperties,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.sonarqube.SonarqubeJavascriptProperties",
):
    '''(experimental) A SonarQube configuration preset for JavaScript projects.

    Provides sensible defaults for JavaScript analysis:

    - ``sonar.language`` = ``js``
    - ``sonar.sources`` = ``src``
    - ``sonar.tests`` = ``test``
    - ``sonar.sourceEncoding`` = ``UTF-8``
    - ``sonar.profile`` = ``Sonar Way``
    - ``sonar.scm.provider`` = ``git``
    - Typical exclusions for ``node_modules``, ``coverage``, and test files
    - ``sonar.javascript.lcov.reportPaths`` = ``coverage/lcov.info``

    All defaults can be overridden via options. Nested options (e.g. ``coverage``,
    ``javascript``) are deep-merged with the defaults, so overriding one nested
    field does not drop the other defaults in that subtree.

    :stability: experimental

    Example::

        new SonarqubeJavascriptProperties(project, {
          projectKey: 'my-org_my-js-project',
        });
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.IConstruct",
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e4c9473567147849552b45d3bb906c7f8af581078455a1214894492fff2ed939)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = SonarqubeJavascriptPropertiesOptions(
            project_key=project_key,
            coverage=coverage,
            cpd=cpd,
            exclusions=exclusions,
            extra_properties=extra_properties,
            file_options=file_options,
            javascript=javascript,
            language=language,
            log=log,
            organization=organization,
            profile=profile,
            project_base_dir=project_base_dir,
            project_name=project_name,
            project_version=project_version,
            qualitygate=qualitygate,
            region=region,
            rust=rust,
            scm=scm,
            source_encoding=source_encoding,
            sources=sources,
            tests=tests,
            typescript=typescript,
        )

        jsii.create(self.__class__, self, [scope, options])


@jsii.data_type(
    jsii_type="projen.sonarqube.SonarqubeJavascriptPropertiesOptions",
    jsii_struct_bases=[SonarqubePropertiesOptions],
    name_mapping={
        "project_key": "projectKey",
        "coverage": "coverage",
        "cpd": "cpd",
        "exclusions": "exclusions",
        "extra_properties": "extraProperties",
        "file_options": "fileOptions",
        "javascript": "javascript",
        "language": "language",
        "log": "log",
        "organization": "organization",
        "profile": "profile",
        "project_base_dir": "projectBaseDir",
        "project_name": "projectName",
        "project_version": "projectVersion",
        "qualitygate": "qualitygate",
        "region": "region",
        "rust": "rust",
        "scm": "scm",
        "source_encoding": "sourceEncoding",
        "sources": "sources",
        "tests": "tests",
        "typescript": "typescript",
    },
)
class SonarqubeJavascriptPropertiesOptions(SonarqubePropertiesOptions):
    def __init__(
        self,
        *,
        project_key: builtins.str,
        coverage: typing.Optional[typing.Union["SonarqubeCoverageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cpd: typing.Optional[typing.Union["SonarqubeCpdOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_options: typing.Optional[typing.Union["SonarqubeFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["SonarqubeJavascriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        language: typing.Optional[builtins.str] = None,
        log: typing.Optional[typing.Union["SonarqubeLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        organization: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        project_base_dir: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        project_version: typing.Optional[builtins.str] = None,
        qualitygate: typing.Optional[typing.Union["SonarqubeQualityGateOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional["SonarqubeRegion"] = None,
        rust: typing.Optional[typing.Union["SonarqubeRustOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        scm: typing.Optional[typing.Union["SonarqubeScmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        source_encoding: typing.Optional[builtins.str] = None,
        sources: typing.Optional[builtins.str] = None,
        tests: typing.Optional[builtins.str] = None,
        typescript: typing.Optional[typing.Union["SonarqubeTypescriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``SonarqubeJavascriptProperties``.

        Extends base options with JavaScript-specific defaults.

        :param project_key: (experimental) The project's unique key. Can include up to 400 characters. Allowed characters: letters, digits, dash, underscore, periods, and colons. Maps to ``sonar.projectKey``. This parameter is mandatory.
        :param coverage: (experimental) Coverage-related options (``sonar.coverage.*``). Default: - no coverage configuration
        :param cpd: (experimental) Duplication detection options (``sonar.cpd.*``). Default: - no CPD configuration
        :param exclusions: (experimental) Comma-separated file path patterns to exclude from the analysis scope. Maps to ``sonar.exclusions``. Default: - no exclusions
        :param extra_properties: (experimental) Additional arbitrary properties to include in the configuration. Use this for properties not covered by the typed options. Keys use dot-notation (e.g., ``sonar.java.binaries``). These are applied as overrides after the typed options above, so a key that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces that entire subtree rather than merging with it. Default: - no additional properties
        :param file_options: (experimental) Options for the generated properties file. Default: - default file options
        :param javascript: (experimental) JavaScript-specific options (``sonar.javascript.*``). Default: - no JavaScript configuration
        :param language: (experimental) The language for analysis. Maps to ``sonar.language``. Default: - auto-detected
        :param log: (experimental) Logging options (``sonar.log.*``). Default: - INFO level
        :param organization: (experimental) The key of the organization to which the project belongs. Maps to ``sonar.organization``. Mandatory for SonarQube Cloud. Default: - no organization
        :param profile: (experimental) The quality profile name. Maps to ``sonar.profile``. Default: - uses the default profile configured on the server
        :param project_base_dir: (experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started. Maps to ``sonar.projectBaseDir``. Default: - the directory from which the analysis was started
        :param project_name: (experimental) Name of the project displayed on the web interface. Maps to ``sonar.projectName``. Default: - not set
        :param project_version: (experimental) The project version. Maps to ``sonar.projectVersion``. Default: - not set
        :param qualitygate: (experimental) Quality gate options (``sonar.qualitygate.*``). Default: - quality gate not awaited
        :param region: (experimental) The SonarQube Cloud instance's region. Maps to ``sonar.region``. Default: SonarqubeRegion.EU
        :param rust: (experimental) Rust-specific options (``sonar.rust.*``). Default: - no Rust configuration
        :param scm: (experimental) SCM-related options (``sonar.scm.*``). Default: - no SCM configuration
        :param source_encoding: (experimental) Encoding of the source files. Maps to ``sonar.sourceEncoding``. Default: - system encoding
        :param sources: (experimental) Comma-separated paths to directories containing main source code (non-test code). Maps to ``sonar.sources``. Default: - the project base directory
        :param tests: (experimental) Comma-separated paths to directories containing test code. Maps to ``sonar.tests``. Default: - no test code analyzed
        :param typescript: (experimental) TypeScript-specific options (``sonar.typescript.*``). Default: - no TypeScript configuration

        :stability: experimental
        '''
        if isinstance(coverage, dict):
            coverage = SonarqubeCoverageOptions(**coverage)
        if isinstance(cpd, dict):
            cpd = SonarqubeCpdOptions(**cpd)
        if isinstance(file_options, dict):
            file_options = SonarqubeFileOptions(**file_options)
        if isinstance(javascript, dict):
            javascript = SonarqubeJavascriptOptions(**javascript)
        if isinstance(log, dict):
            log = SonarqubeLogOptions(**log)
        if isinstance(qualitygate, dict):
            qualitygate = SonarqubeQualityGateOptions(**qualitygate)
        if isinstance(rust, dict):
            rust = SonarqubeRustOptions(**rust)
        if isinstance(scm, dict):
            scm = SonarqubeScmOptions(**scm)
        if isinstance(typescript, dict):
            typescript = SonarqubeTypescriptOptions(**typescript)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f830197b74a3423ab391654e2a5ba39d9669c4adac4a6b1f0a558663212a2fa9)
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument coverage", value=coverage, expected_type=type_hints["coverage"])
            check_type(argname="argument cpd", value=cpd, expected_type=type_hints["cpd"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument extra_properties", value=extra_properties, expected_type=type_hints["extra_properties"])
            check_type(argname="argument file_options", value=file_options, expected_type=type_hints["file_options"])
            check_type(argname="argument javascript", value=javascript, expected_type=type_hints["javascript"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument project_base_dir", value=project_base_dir, expected_type=type_hints["project_base_dir"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument project_version", value=project_version, expected_type=type_hints["project_version"])
            check_type(argname="argument qualitygate", value=qualitygate, expected_type=type_hints["qualitygate"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rust", value=rust, expected_type=type_hints["rust"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
            check_type(argname="argument source_encoding", value=source_encoding, expected_type=type_hints["source_encoding"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tests", value=tests, expected_type=type_hints["tests"])
            check_type(argname="argument typescript", value=typescript, expected_type=type_hints["typescript"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_key": project_key,
        }
        if coverage is not None:
            self._values["coverage"] = coverage
        if cpd is not None:
            self._values["cpd"] = cpd
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if extra_properties is not None:
            self._values["extra_properties"] = extra_properties
        if file_options is not None:
            self._values["file_options"] = file_options
        if javascript is not None:
            self._values["javascript"] = javascript
        if language is not None:
            self._values["language"] = language
        if log is not None:
            self._values["log"] = log
        if organization is not None:
            self._values["organization"] = organization
        if profile is not None:
            self._values["profile"] = profile
        if project_base_dir is not None:
            self._values["project_base_dir"] = project_base_dir
        if project_name is not None:
            self._values["project_name"] = project_name
        if project_version is not None:
            self._values["project_version"] = project_version
        if qualitygate is not None:
            self._values["qualitygate"] = qualitygate
        if region is not None:
            self._values["region"] = region
        if rust is not None:
            self._values["rust"] = rust
        if scm is not None:
            self._values["scm"] = scm
        if source_encoding is not None:
            self._values["source_encoding"] = source_encoding
        if sources is not None:
            self._values["sources"] = sources
        if tests is not None:
            self._values["tests"] = tests
        if typescript is not None:
            self._values["typescript"] = typescript

    @builtins.property
    def project_key(self) -> builtins.str:
        '''(experimental) The project's unique key.

        Can include up to 400 characters. Allowed characters:
        letters, digits, dash, underscore, periods, and colons.

        Maps to ``sonar.projectKey``. This parameter is mandatory.

        :stability: experimental
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def coverage(self) -> typing.Optional["SonarqubeCoverageOptions"]:
        '''(experimental) Coverage-related options (``sonar.coverage.*``).

        :default: - no coverage configuration

        :stability: experimental
        '''
        result = self._values.get("coverage")
        return typing.cast(typing.Optional["SonarqubeCoverageOptions"], result)

    @builtins.property
    def cpd(self) -> typing.Optional["SonarqubeCpdOptions"]:
        '''(experimental) Duplication detection options (``sonar.cpd.*``).

        :default: - no CPD configuration

        :stability: experimental
        '''
        result = self._values.get("cpd")
        return typing.cast(typing.Optional["SonarqubeCpdOptions"], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Comma-separated file path patterns to exclude from the analysis scope.

        Maps to ``sonar.exclusions``.

        :default: - no exclusions

        :stability: experimental
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extra_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional arbitrary properties to include in the configuration.

        Use this for properties not covered by the typed options.
        Keys use dot-notation (e.g., ``sonar.java.binaries``).

        These are applied as overrides after the typed options above, so a key
        that is a prefix of a typed option (e.g. ``"sonar.coverage"``) replaces
        that entire subtree rather than merging with it.

        :default: - no additional properties

        :stability: experimental
        '''
        result = self._values.get("extra_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file_options(self) -> typing.Optional["SonarqubeFileOptions"]:
        '''(experimental) Options for the generated properties file.

        :default: - default file options

        :stability: experimental
        '''
        result = self._values.get("file_options")
        return typing.cast(typing.Optional["SonarqubeFileOptions"], result)

    @builtins.property
    def javascript(self) -> typing.Optional["SonarqubeJavascriptOptions"]:
        '''(experimental) JavaScript-specific options (``sonar.javascript.*``).

        :default: - no JavaScript configuration

        :stability: experimental
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["SonarqubeJavascriptOptions"], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''(experimental) The language for analysis.

        Maps to ``sonar.language``.

        :default: - auto-detected

        :stability: experimental
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log(self) -> typing.Optional["SonarqubeLogOptions"]:
        '''(experimental) Logging options (``sonar.log.*``).

        :default: - INFO level

        :stability: experimental
        '''
        result = self._values.get("log")
        return typing.cast(typing.Optional["SonarqubeLogOptions"], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the organization to which the project belongs.

        Maps to ``sonar.organization``. Mandatory for SonarQube Cloud.

        :default: - no organization

        :stability: experimental
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) The quality profile name.

        Maps to ``sonar.profile``.

        :default: - uses the default profile configured on the server

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_base_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project's base directory when the analysis needs to take place in a directory other than the one from which it was started.

        Maps to ``sonar.projectBaseDir``.

        :default: - the directory from which the analysis was started

        :stability: experimental
        '''
        result = self._values.get("project_base_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the project displayed on the web interface.

        Maps to ``sonar.projectName``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The project version.

        Maps to ``sonar.projectVersion``.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("project_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualitygate(self) -> typing.Optional["SonarqubeQualityGateOptions"]:
        '''(experimental) Quality gate options (``sonar.qualitygate.*``).

        :default: - quality gate not awaited

        :stability: experimental
        '''
        result = self._values.get("qualitygate")
        return typing.cast(typing.Optional["SonarqubeQualityGateOptions"], result)

    @builtins.property
    def region(self) -> typing.Optional["SonarqubeRegion"]:
        '''(experimental) The SonarQube Cloud instance's region.

        Maps to ``sonar.region``.

        :default: SonarqubeRegion.EU

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional["SonarqubeRegion"], result)

    @builtins.property
    def rust(self) -> typing.Optional["SonarqubeRustOptions"]:
        '''(experimental) Rust-specific options (``sonar.rust.*``).

        :default: - no Rust configuration

        :stability: experimental
        '''
        result = self._values.get("rust")
        return typing.cast(typing.Optional["SonarqubeRustOptions"], result)

    @builtins.property
    def scm(self) -> typing.Optional["SonarqubeScmOptions"]:
        '''(experimental) SCM-related options (``sonar.scm.*``).

        :default: - no SCM configuration

        :stability: experimental
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional["SonarqubeScmOptions"], result)

    @builtins.property
    def source_encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) Encoding of the source files.

        Maps to ``sonar.sourceEncoding``.

        :default: - system encoding

        :stability: experimental
        '''
        result = self._values.get("source_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing main source code (non-test code).

        Maps to ``sonar.sources``.

        :default: - the project base directory

        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tests(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-separated paths to directories containing test code.

        Maps to ``sonar.tests``.

        :default: - no test code analyzed

        :stability: experimental
        '''
        result = self._values.get("tests")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def typescript(self) -> typing.Optional["SonarqubeTypescriptOptions"]:
        '''(experimental) TypeScript-specific options (``sonar.typescript.*``).

        :default: - no TypeScript configuration

        :stability: experimental
        '''
        result = self._values.get("typescript")
        return typing.cast(typing.Optional["SonarqubeTypescriptOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarqubeJavascriptPropertiesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SonarqubeCoverageOptions",
    "SonarqubeCpdOptions",
    "SonarqubeFileOptions",
    "SonarqubeJavascriptOptions",
    "SonarqubeJavascriptProperties",
    "SonarqubeJavascriptPropertiesOptions",
    "SonarqubeLcovOptions",
    "SonarqubeLogLevel",
    "SonarqubeLogOptions",
    "SonarqubeProperties",
    "SonarqubePropertiesOptions",
    "SonarqubeQualityGateOptions",
    "SonarqubeRegion",
    "SonarqubeRustClippyOptions",
    "SonarqubeRustClippyReportOptions",
    "SonarqubeRustOptions",
    "SonarqubeRustProperties",
    "SonarqubeRustPropertiesOptions",
    "SonarqubeScmExclusionsOptions",
    "SonarqubeScmOptions",
    "SonarqubeTypescriptOptions",
    "SonarqubeTypescriptProperties",
    "SonarqubeTypescriptPropertiesOptions",
]

publication.publish()

def _typecheckingstub__9113540a247617d806eaee98dbc9efcc4ec7ed79504f78650d9e555198783795(
    *,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf0b7b26cf704d304e8db90268127d3964dc0335fd35c98381a5a687898e593(
    *,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783c3c18d13f6c2abbee60deeea0346f3ec9f8ac9c3934296d7bb4c81cb136be(
    *,
    comment: typing.Optional[typing.Sequence[builtins.str]] = None,
    committed: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f834c072e3e82c664ebf087e9824337838420df13be0ac2466beca64f33bcd(
    *,
    lcov: typing.Optional[typing.Union[SonarqubeLcovOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f1bb64a6068c39051c30b18f7a44a63b48a91ebf8417855ad011e16f450e8d(
    *,
    report_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbae29a71c88e1ea8f1091033076251b5ebe8552cbb2df1357a964fa1aae0945(
    *,
    level: typing.Optional[SonarqubeLogLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d032a848399835b60247bb0c3958b3727bde6832f2dbf6f72022aafd8eaaf2ba(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2903e34d199955ec4b3395ac11813643349a6bc12046316b13284cfd461b692(
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1751ee9928717822a44e53a063c9bd184cbc4ec627b8a8c882e1be83584b80b4(
    *,
    timeout: typing.Optional[jsii.Number] = None,
    wait: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec45e69ebbd11008a7827e535a23bd4abd48d8edc4c291f3d0ee7e886a398187(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b93e70be08a603e21119fcfa30c99dc0ba028ecd5990d8ba06a459ba1ceaff(
    *,
    report_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b4e9c03fd0a21e993b5a56715a14a484f7092e2942379b10280387e962f6ab(
    *,
    clippy: typing.Optional[typing.Union[SonarqubeRustClippyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clippy_report: typing.Optional[typing.Union[SonarqubeRustClippyReportOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    lcov: typing.Optional[typing.Union[SonarqubeLcovOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3203229f162bdb4a5861a63f3eac5203d5840e2dd887f5ec2aaefb390efb42e(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad05c13b54541e0cda8b6d0b5a26b3d9a4bb8bf18df593c22d342077c8f2caa(
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716e6044727f1fa46c3448e8e2712c00d1e863fed1867d1e85ebe4ffa1a3f3be(
    *,
    disabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a0799e1adff2395176aac608256f7abdd0f1292e6ef8f9a5f33a41d61b5c2b(
    *,
    exclusions: typing.Optional[typing.Union[SonarqubeScmExclusionsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d239110ecf824c542fa4c6258b08f69d3facda43eb3676199ca490bc1a8a215b(
    *,
    tsconfig_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d766f5f1a4b8059fe48532815dc8d56c10063ce0c2f591bbb1b399b4bcfa387(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b81e841b21150947356e146bd990dfa855a8142f93c95742a6a38bd899ff70(
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c9473567147849552b45d3bb906c7f8af581078455a1214894492fff2ed939(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f830197b74a3423ab391654e2a5ba39d9669c4adac4a6b1f0a558663212a2fa9(
    *,
    project_key: builtins.str,
    coverage: typing.Optional[typing.Union[SonarqubeCoverageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cpd: typing.Optional[typing.Union[SonarqubeCpdOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file_options: typing.Optional[typing.Union[SonarqubeFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[SonarqubeJavascriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    language: typing.Optional[builtins.str] = None,
    log: typing.Optional[typing.Union[SonarqubeLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    organization: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    project_base_dir: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    project_version: typing.Optional[builtins.str] = None,
    qualitygate: typing.Optional[typing.Union[SonarqubeQualityGateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[SonarqubeRegion] = None,
    rust: typing.Optional[typing.Union[SonarqubeRustOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scm: typing.Optional[typing.Union[SonarqubeScmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    source_encoding: typing.Optional[builtins.str] = None,
    sources: typing.Optional[builtins.str] = None,
    tests: typing.Optional[builtins.str] = None,
    typescript: typing.Optional[typing.Union[SonarqubeTypescriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
