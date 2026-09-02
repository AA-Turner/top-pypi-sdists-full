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

    import projen as _projen_04054675
else:

    _projen_04054675 = _LazyImport("projen")


@jsii.data_type(
    jsii_type="projen.polaris.AnalysisConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "aggressiveness_level": "aggressivenessLevel",
        "callgraph_metrics": "callgraphMetrics",
        "c_cpp_fnptr": "cCppFnptr",
        "c_cpp_virtual": "cCppVirtual",
        "checkers": "checkers",
        "coding_standards": "codingStandards",
        "connect": "connect",
        "constraint_fpp": "constraintFpp",
        "cov_analyze_args": "covAnalyzeArgs",
        "cov_collect_models_args": "covCollectModelsArgs",
        "directives": "directives",
        "files": "files",
        "jobs": "jobs",
        "location": "location",
        "mode": "mode",
        "model_file": "modelFile",
        "one_tu_per_psf": "oneTuPerPsf",
        "output_model_file": "outputModelFile",
        "parse_warnings": "parseWarnings",
        "scan_transparency": "scanTransparency",
        "sigma": "sigma",
        "trust": "trust",
    },
)
class AnalysisConfiguration:
    def __init__(
        self,
        *,
        aggressiveness_level: typing.Optional["AnalysisConfigurationAggressivenessLevel"] = None,
        callgraph_metrics: typing.Optional[builtins.bool] = None,
        c_cpp_fnptr: typing.Optional[builtins.bool] = None,
        c_cpp_virtual: typing.Optional[builtins.bool] = None,
        checkers: typing.Optional[typing.Union["CheckerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        coding_standards: typing.Optional[typing.Union["CodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connect: typing.Optional[typing.Union["AnalyzeConnectConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        constraint_fpp: typing.Optional[builtins.bool] = None,
        cov_analyze_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        cov_collect_models_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        directives: typing.Optional[typing.Sequence[typing.Union["DirectivesConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
        files: typing.Optional[typing.Union["AnalyzeFilesConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        jobs: typing.Optional[typing.Sequence[typing.Union["JobsConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
        location: typing.Optional["AnalysisConfigurationLocation"] = None,
        mode: typing.Optional["AnalysisConfigurationMode"] = None,
        model_file: typing.Optional[builtins.str] = None,
        one_tu_per_psf: typing.Optional[builtins.bool] = None,
        output_model_file: typing.Optional[builtins.str] = None,
        parse_warnings: typing.Optional[typing.Union["ParseWarningsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        scan_transparency: typing.Optional[builtins.bool] = None,
        sigma: typing.Optional[typing.Union["SigmaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        trust: typing.Any = None,
    ) -> None:
        '''(experimental) Specifies how the project should be analyzed.

        :param aggressiveness_level: (experimental) Specifies the aggressiveness level for the analysis. The aggressiveness level causes the analysis to make more or less aggressive assumptions during the analysis where the higher the aggressiveness level the more defects are reported.
        :param callgraph_metrics: (experimental) Enables callgraph metrics output in the intermediate directory.
        :param c_cpp_fnptr: (experimental) Enables analysis of calls to function pointers for defects.
        :param c_cpp_virtual: (experimental) Enables full virtual-call resolution for C++.
        :param checkers: (experimental) If no checker configuration is specified, the CLI will enable a set of checkers based on the files that were captured.
        :param coding_standards: (experimental) If specified, the analysis will scan the code for compliance according to the given coding standard configuration. If this configuration is present, the capture "emit-complementary-info" flag will be set to true.
        :param connect: (experimental) Coverity Connect configuration to use when performing analysis in Coverity Connect.
        :param constraint_fpp: (experimental) Enables additional filtering of defects by using an additional false-path pruner. If set to true, the constraint FPP is enabled.
        :param cov_analyze_args: (experimental) Additional arguments to pass to cov-analyze when doing analysis.
        :param cov_collect_models_args: (experimental) Additional arguments to pass to cov-collect-models following analysis when "output-model-file" is specified.
        :param directives: (experimental) Specifies directives to use for the analysis, including for web application security analysis.
        :param files: (experimental) Specifies which files to analyze when the "analyze.mode" setting is "hfi". Analysis will be performed for only these files.
        :param jobs: (experimental) Specifies analysis worker parallelism.
        :param location: (experimental) Specifies whether the analysis should be done locally, in Coverity Connect, or in Software Risk Manager. The possible values are as follows: connect - Run the analysis in the Coverity Connect job farm; srm - Run the analysis in the Software Risk Manager job farm; local - Run the analysis locally
        :param mode: (experimental) Analysis mode: "pfi" (perfect fidelity incremental) for complete analysis; or "hfi" (high fidelity incremental) for analysis of only specific files specified by analyze.files settings, omitting any other files which may have been incidentally captured by the build. An "hfi" analysis can be faster but may produce results which are incomplete or inconsistent, due to the lack of context, and should be used only when speed is more important than accuracy.
        :param model_file: (experimental) File containing function models. This overrides models specified in the default location of "config/user_models.xmldb".
        :param one_tu_per_psf: (experimental) If set to to true, only one TU (translation unit) will be analyzed per source file name. If set to false, all translation units will be analyzed.
        :param output_model_file: (experimental) Output file to which function models for the project should be written following analysis.
        :param parse_warnings: (experimental) Specifies how parse warnings are handled.
        :param scan_transparency: (experimental) Specifies whether to enable the collection of scan transparency data for analysis. This setting must be enabled if the Coverity Connect instance has 'scan.transparency.enabled=true' in its configuration.
        :param sigma: (experimental) Specifies options for Sigma analysis.
        :param trust: (experimental) This is a map from trust option name to boolean to indicate whether the particular trust property should be trusted or distrusted. The trust option "all" controls whether all trust options should be trusted or distrusted.

        :stability: experimental
        :schema: analysis-configuration
        '''
        if isinstance(checkers, dict):
            checkers = CheckerConfiguration(**checkers)
        if isinstance(coding_standards, dict):
            coding_standards = CodingStandardConfiguration(**coding_standards)
        if isinstance(connect, dict):
            connect = AnalyzeConnectConfiguration(**connect)
        if isinstance(files, dict):
            files = AnalyzeFilesConfiguration(**files)
        if isinstance(parse_warnings, dict):
            parse_warnings = ParseWarningsConfiguration(**parse_warnings)
        if isinstance(sigma, dict):
            sigma = SigmaConfiguration(**sigma)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5b1b87f9b43ed84e0acc43840a145366632715b3ccf8365068e62aff7e8b39ce)
            check_type(argname="argument aggressiveness_level", value=aggressiveness_level, expected_type=type_hints["aggressiveness_level"])
            check_type(argname="argument callgraph_metrics", value=callgraph_metrics, expected_type=type_hints["callgraph_metrics"])
            check_type(argname="argument c_cpp_fnptr", value=c_cpp_fnptr, expected_type=type_hints["c_cpp_fnptr"])
            check_type(argname="argument c_cpp_virtual", value=c_cpp_virtual, expected_type=type_hints["c_cpp_virtual"])
            check_type(argname="argument checkers", value=checkers, expected_type=type_hints["checkers"])
            check_type(argname="argument coding_standards", value=coding_standards, expected_type=type_hints["coding_standards"])
            check_type(argname="argument connect", value=connect, expected_type=type_hints["connect"])
            check_type(argname="argument constraint_fpp", value=constraint_fpp, expected_type=type_hints["constraint_fpp"])
            check_type(argname="argument cov_analyze_args", value=cov_analyze_args, expected_type=type_hints["cov_analyze_args"])
            check_type(argname="argument cov_collect_models_args", value=cov_collect_models_args, expected_type=type_hints["cov_collect_models_args"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument model_file", value=model_file, expected_type=type_hints["model_file"])
            check_type(argname="argument one_tu_per_psf", value=one_tu_per_psf, expected_type=type_hints["one_tu_per_psf"])
            check_type(argname="argument output_model_file", value=output_model_file, expected_type=type_hints["output_model_file"])
            check_type(argname="argument parse_warnings", value=parse_warnings, expected_type=type_hints["parse_warnings"])
            check_type(argname="argument scan_transparency", value=scan_transparency, expected_type=type_hints["scan_transparency"])
            check_type(argname="argument sigma", value=sigma, expected_type=type_hints["sigma"])
            check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggressiveness_level is not None:
            self._values["aggressiveness_level"] = aggressiveness_level
        if callgraph_metrics is not None:
            self._values["callgraph_metrics"] = callgraph_metrics
        if c_cpp_fnptr is not None:
            self._values["c_cpp_fnptr"] = c_cpp_fnptr
        if c_cpp_virtual is not None:
            self._values["c_cpp_virtual"] = c_cpp_virtual
        if checkers is not None:
            self._values["checkers"] = checkers
        if coding_standards is not None:
            self._values["coding_standards"] = coding_standards
        if connect is not None:
            self._values["connect"] = connect
        if constraint_fpp is not None:
            self._values["constraint_fpp"] = constraint_fpp
        if cov_analyze_args is not None:
            self._values["cov_analyze_args"] = cov_analyze_args
        if cov_collect_models_args is not None:
            self._values["cov_collect_models_args"] = cov_collect_models_args
        if directives is not None:
            self._values["directives"] = directives
        if files is not None:
            self._values["files"] = files
        if jobs is not None:
            self._values["jobs"] = jobs
        if location is not None:
            self._values["location"] = location
        if mode is not None:
            self._values["mode"] = mode
        if model_file is not None:
            self._values["model_file"] = model_file
        if one_tu_per_psf is not None:
            self._values["one_tu_per_psf"] = one_tu_per_psf
        if output_model_file is not None:
            self._values["output_model_file"] = output_model_file
        if parse_warnings is not None:
            self._values["parse_warnings"] = parse_warnings
        if scan_transparency is not None:
            self._values["scan_transparency"] = scan_transparency
        if sigma is not None:
            self._values["sigma"] = sigma
        if trust is not None:
            self._values["trust"] = trust

    @builtins.property
    def aggressiveness_level(
        self,
    ) -> typing.Optional["AnalysisConfigurationAggressivenessLevel"]:
        '''(experimental) Specifies the aggressiveness level for the analysis.

        The aggressiveness level causes the analysis to make more or less aggressive assumptions during the analysis where the higher the aggressiveness level the more defects are reported.

        :stability: experimental
        :schema: analysis-configuration#aggressiveness-level
        '''
        result = self._values.get("aggressiveness_level")
        return typing.cast(typing.Optional["AnalysisConfigurationAggressivenessLevel"], result)

    @builtins.property
    def callgraph_metrics(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables callgraph metrics output in the intermediate directory.

        :stability: experimental
        :schema: analysis-configuration#callgraph-metrics
        '''
        result = self._values.get("callgraph_metrics")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def c_cpp_fnptr(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables analysis of calls to function pointers for defects.

        :stability: experimental
        :schema: analysis-configuration#c-cpp-fnptr
        '''
        result = self._values.get("c_cpp_fnptr")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def c_cpp_virtual(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables full virtual-call resolution for C++.

        :stability: experimental
        :schema: analysis-configuration#c-cpp-virtual
        '''
        result = self._values.get("c_cpp_virtual")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def checkers(self) -> typing.Optional["CheckerConfiguration"]:
        '''(experimental) If no checker configuration is specified, the CLI will enable a set of checkers based on the files that were captured.

        :stability: experimental
        :schema: analysis-configuration#checkers
        '''
        result = self._values.get("checkers")
        return typing.cast(typing.Optional["CheckerConfiguration"], result)

    @builtins.property
    def coding_standards(self) -> typing.Optional["CodingStandardConfiguration"]:
        '''(experimental) If specified, the analysis will scan the code for compliance according to the given coding standard configuration.

        If this configuration is present, the capture "emit-complementary-info" flag will be set to true.

        :stability: experimental
        :schema: analysis-configuration#coding-standards
        '''
        result = self._values.get("coding_standards")
        return typing.cast(typing.Optional["CodingStandardConfiguration"], result)

    @builtins.property
    def connect(self) -> typing.Optional["AnalyzeConnectConfiguration"]:
        '''(experimental) Coverity Connect configuration to use when performing analysis in Coverity Connect.

        :stability: experimental
        :schema: analysis-configuration#connect
        '''
        result = self._values.get("connect")
        return typing.cast(typing.Optional["AnalyzeConnectConfiguration"], result)

    @builtins.property
    def constraint_fpp(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables additional filtering of defects by using an additional false-path pruner.

        If set to true, the constraint FPP is enabled.

        :stability: experimental
        :schema: analysis-configuration#constraint-fpp
        '''
        result = self._values.get("constraint_fpp")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cov_analyze_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional arguments to pass to cov-analyze when doing analysis.

        :stability: experimental
        :schema: analysis-configuration#cov-analyze-args
        '''
        result = self._values.get("cov_analyze_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cov_collect_models_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional arguments to pass to cov-collect-models following analysis when "output-model-file" is specified.

        :stability: experimental
        :schema: analysis-configuration#cov-collect-models-args
        '''
        result = self._values.get("cov_collect_models_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List["DirectivesConfiguration"]]:
        '''(experimental) Specifies directives to use for the analysis, including for web application security analysis.

        :stability: experimental
        :schema: analysis-configuration#directives
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List["DirectivesConfiguration"]], result)

    @builtins.property
    def files(self) -> typing.Optional["AnalyzeFilesConfiguration"]:
        '''(experimental) Specifies which files to analyze when the "analyze.mode" setting is "hfi". Analysis will be performed for only these files.

        :stability: experimental
        :schema: analysis-configuration#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional["AnalyzeFilesConfiguration"], result)

    @builtins.property
    def jobs(self) -> typing.Optional[typing.List["JobsConfiguration"]]:
        '''(experimental) Specifies analysis worker parallelism.

        :stability: experimental
        :schema: analysis-configuration#jobs
        '''
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.List["JobsConfiguration"]], result)

    @builtins.property
    def location(self) -> typing.Optional["AnalysisConfigurationLocation"]:
        '''(experimental) Specifies whether the analysis should be done locally, in Coverity Connect, or in Software Risk Manager.

        The possible values are as follows: connect - Run the analysis in the Coverity Connect job farm; srm - Run the analysis in the Software Risk Manager job farm; local - Run the analysis locally

        :stability: experimental
        :schema: analysis-configuration#location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional["AnalysisConfigurationLocation"], result)

    @builtins.property
    def mode(self) -> typing.Optional["AnalysisConfigurationMode"]:
        '''(experimental) Analysis mode: "pfi" (perfect fidelity incremental) for complete analysis;

        or "hfi" (high fidelity incremental) for analysis of only specific files specified by analyze.files settings, omitting any other files which may have been incidentally captured by the build. An "hfi" analysis can be faster but may produce results which are incomplete or inconsistent, due to the lack of context, and should be used only when speed is more important than accuracy.

        :stability: experimental
        :schema: analysis-configuration#mode
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["AnalysisConfigurationMode"], result)

    @builtins.property
    def model_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing function models.

        This overrides models specified in the default location of "config/user_models.xmldb".

        :stability: experimental
        :schema: analysis-configuration#model-file
        '''
        result = self._values.get("model_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def one_tu_per_psf(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to to true, only one TU (translation unit) will be analyzed per source file name.

        If set to false, all translation units will be analyzed.

        :stability: experimental
        :schema: analysis-configuration#one-tu-per-psf
        '''
        result = self._values.get("one_tu_per_psf")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def output_model_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Output file to which function models for the project should be written following analysis.

        :stability: experimental
        :schema: analysis-configuration#output-model-file
        '''
        result = self._values.get("output_model_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parse_warnings(self) -> typing.Optional["ParseWarningsConfiguration"]:
        '''(experimental) Specifies how parse warnings are handled.

        :stability: experimental
        :schema: analysis-configuration#parse-warnings
        '''
        result = self._values.get("parse_warnings")
        return typing.cast(typing.Optional["ParseWarningsConfiguration"], result)

    @builtins.property
    def scan_transparency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable the collection of scan transparency data for analysis.

        This setting must be enabled if the Coverity Connect instance has 'scan.transparency.enabled=true' in its configuration.

        :stability: experimental
        :schema: analysis-configuration#scan-transparency
        '''
        result = self._values.get("scan_transparency")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sigma(self) -> typing.Optional["SigmaConfiguration"]:
        '''(experimental) Specifies options for Sigma analysis.

        :stability: experimental
        :schema: analysis-configuration#sigma
        '''
        result = self._values.get("sigma")
        return typing.cast(typing.Optional["SigmaConfiguration"], result)

    @builtins.property
    def trust(self) -> typing.Any:
        '''(experimental) This is a map from trust option name to boolean to indicate whether the particular trust property should be trusted or distrusted.

        The trust option "all" controls whether all trust options should be trusted or distrusted.

        :stability: experimental
        :schema: analysis-configuration#trust
        '''
        result = self._values.get("trust")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AnalysisConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.AnalysisConfigurationAggressivenessLevel")
class AnalysisConfigurationAggressivenessLevel(enum.Enum):
    '''(experimental) Specifies the aggressiveness level for the analysis.

    The aggressiveness level causes the analysis to make more or less aggressive assumptions during the analysis where the higher the aggressiveness level the more defects are reported.

    :stability: experimental
    :schema: AnalysisConfigurationAggressivenessLevel
    '''

    LOW = "LOW"
    '''(experimental) low.

    :stability: experimental
    '''
    MEDIUM = "MEDIUM"
    '''(experimental) medium.

    :stability: experimental
    '''
    HIGH = "HIGH"
    '''(experimental) high.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.polaris.AnalysisConfigurationLocation")
class AnalysisConfigurationLocation(enum.Enum):
    '''(experimental) Specifies whether the analysis should be done locally, in Coverity Connect, or in Software Risk Manager.

    The possible values are as follows: connect - Run the analysis in the Coverity Connect job farm; srm - Run the analysis in the Software Risk Manager job farm; local - Run the analysis locally

    :stability: experimental
    :schema: AnalysisConfigurationLocation
    '''

    LOCAL = "LOCAL"
    '''(experimental) local.

    :stability: experimental
    '''
    CONNECT = "CONNECT"
    '''(experimental) connect.

    :stability: experimental
    '''
    SRM = "SRM"
    '''(experimental) srm.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.polaris.AnalysisConfigurationMode")
class AnalysisConfigurationMode(enum.Enum):
    '''(experimental) Analysis mode: "pfi" (perfect fidelity incremental) for complete analysis;

    or "hfi" (high fidelity incremental) for analysis of only specific files specified by analyze.files settings, omitting any other files which may have been incidentally captured by the build. An "hfi" analysis can be faster but may produce results which are incomplete or inconsistent, due to the lack of context, and should be used only when speed is more important than accuracy.

    :stability: experimental
    :schema: AnalysisConfigurationMode
    '''

    HFI = "HFI"
    '''(experimental) hfi.

    :stability: experimental
    '''
    PFI = "PFI"
    '''(experimental) pfi.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.AnalyzeConnectConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "auth_key_file": "authKeyFile",
        "ca_certs_file": "caCertsFile",
        "proxy_client_cert_file": "proxyClientCertFile",
        "proxy_client_key_file": "proxyClientKeyFile",
        "proxy_url": "proxyUrl",
        "upload_artifacts": "uploadArtifacts",
    },
)
class AnalyzeConnectConfiguration:
    def __init__(
        self,
        *,
        url: builtins.str,
        auth_key_file: typing.Optional[builtins.str] = None,
        ca_certs_file: typing.Optional[builtins.str] = None,
        proxy_client_cert_file: typing.Optional[builtins.str] = None,
        proxy_client_key_file: typing.Optional[builtins.str] = None,
        proxy_url: typing.Optional[builtins.str] = None,
        upload_artifacts: typing.Optional["AnalyzeConnectConfigurationUploadArtifacts"] = None,
    ) -> None:
        '''
        :param url: (experimental) Absolute URL of where to perform Coverity Connect analysis.
        :param auth_key_file: (experimental) The authentication key file to use when authenticating to Coverity Connect to perform analysis. By default, the file located at $HOME/.coverity/ak-- is used.
        :param ca_certs_file: (experimental) File containing additional certificates to trust in addition to the ones in the system certificate store and the Coverity TFT store. By default system CA certificates are used.
        :param proxy_client_cert_file: (experimental) File containing the client certificate in PEM format, that should be presented to the proxy when making a request.
        :param proxy_client_key_file: (experimental) File containing the client certificate private key in PEM format, for the proxy-client-cert-file.
        :param proxy_url: (experimental) URL for a forward proxy to use when communicating with Coverity Connect. Must be an https URL.
        :param upload_artifacts: (experimental) Artifacts to upload following analysis when the analysis location is Connect.

        :stability: experimental
        :schema: analyze-connect-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__459a713d78e38fd614ae50c9a5552f868863f0b6099fc83bd2ae1ec8d0b3cddb)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument auth_key_file", value=auth_key_file, expected_type=type_hints["auth_key_file"])
            check_type(argname="argument ca_certs_file", value=ca_certs_file, expected_type=type_hints["ca_certs_file"])
            check_type(argname="argument proxy_client_cert_file", value=proxy_client_cert_file, expected_type=type_hints["proxy_client_cert_file"])
            check_type(argname="argument proxy_client_key_file", value=proxy_client_key_file, expected_type=type_hints["proxy_client_key_file"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
            check_type(argname="argument upload_artifacts", value=upload_artifacts, expected_type=type_hints["upload_artifacts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if auth_key_file is not None:
            self._values["auth_key_file"] = auth_key_file
        if ca_certs_file is not None:
            self._values["ca_certs_file"] = ca_certs_file
        if proxy_client_cert_file is not None:
            self._values["proxy_client_cert_file"] = proxy_client_cert_file
        if proxy_client_key_file is not None:
            self._values["proxy_client_key_file"] = proxy_client_key_file
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url
        if upload_artifacts is not None:
            self._values["upload_artifacts"] = upload_artifacts

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) Absolute URL of where to perform Coverity Connect analysis.

        :stability: experimental
        :schema: analyze-connect-configuration#url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_key_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authentication key file to use when authenticating to Coverity Connect to perform analysis.

        By default, the file located at $HOME/.coverity/ak-- is used.

        :stability: experimental
        :schema: analyze-connect-configuration#auth-key-file
        '''
        result = self._values.get("auth_key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certs_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing additional certificates to trust in addition to the ones in the system certificate store and the Coverity TFT store.

        By default system CA certificates are used.

        :stability: experimental
        :schema: analyze-connect-configuration#ca-certs-file
        '''
        result = self._values.get("ca_certs_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_client_cert_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the client certificate in PEM format, that should be presented to the proxy when making a request.

        :stability: experimental
        :schema: analyze-connect-configuration#proxy-client-cert-file
        '''
        result = self._values.get("proxy_client_cert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_client_key_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the client certificate private key in PEM format, for the proxy-client-cert-file.

        :stability: experimental
        :schema: analyze-connect-configuration#proxy-client-key-file
        '''
        result = self._values.get("proxy_client_key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL for a forward proxy to use when communicating with Coverity Connect.

        Must be an https URL.

        :stability: experimental
        :schema: analyze-connect-configuration#proxy-url
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_artifacts(
        self,
    ) -> typing.Optional["AnalyzeConnectConfigurationUploadArtifacts"]:
        '''(experimental) Artifacts to upload following analysis when the analysis location is Connect.

        :stability: experimental
        :schema: analyze-connect-configuration#upload-artifacts
        '''
        result = self._values.get("upload_artifacts")
        return typing.cast(typing.Optional["AnalyzeConnectConfigurationUploadArtifacts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AnalyzeConnectConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.AnalyzeConnectConfigurationUploadArtifacts")
class AnalyzeConnectConfigurationUploadArtifacts(enum.Enum):
    '''(experimental) Artifacts to upload following analysis when the analysis location is Connect.

    :stability: experimental
    :schema: AnalyzeConnectConfigurationUploadArtifacts
    '''

    ALL = "ALL"
    '''(experimental) All.

    :stability: experimental
    '''
    LOGS_ONLY = "LOGS_ONLY"
    '''(experimental) LogsOnly.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) None.

    :stability: experimental
    '''
    ON_FAILURE = "ON_FAILURE"
    '''(experimental) OnFailure.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.AnalyzeFilesConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_glob": "excludeGlob",
        "exclude_regex": "excludeRegex",
        "include_files": "includeFiles",
        "include_glob": "includeGlob",
        "include_list_file": "includeListFile",
        "include_regex": "includeRegex",
    },
)
class AnalyzeFilesConfiguration:
    def __init__(
        self,
        *,
        exclude_glob: typing.Optional[builtins.str] = None,
        exclude_regex: typing.Optional[builtins.str] = None,
        include_files: typing.Optional[builtins.str] = None,
        include_glob: typing.Optional[builtins.str] = None,
        include_list_file: typing.Optional[builtins.str] = None,
        include_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_glob: (experimental) Glob pattern that specifies the set of source files to exclude from analysis. Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.
        :param exclude_regex: (experimental) Regular expression that specifies the set of source files to exclude from analysis. Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.
        :param include_files: (experimental) Paths of source files to analyze. Include and exclude glob patterns and regular expressions are applied to determine which of these files are actually analyzed.
        :param include_glob: (experimental) Glob pattern that specifies the set of source files to analyze.
        :param include_list_file: (experimental) File containing the paths of source files to analyze, one per line. Include and exclude glob patterns and regular expressions are applied to determine which of these files are actually analyzed.
        :param include_regex: (experimental) Regular expression that specifies the set of source files to analyze.

        :stability: experimental
        :schema: analyze-files-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__de9daf461f16912944b8d5c944b16a274a24af7a4f202700d0315191ac0a7b16)
            check_type(argname="argument exclude_glob", value=exclude_glob, expected_type=type_hints["exclude_glob"])
            check_type(argname="argument exclude_regex", value=exclude_regex, expected_type=type_hints["exclude_regex"])
            check_type(argname="argument include_files", value=include_files, expected_type=type_hints["include_files"])
            check_type(argname="argument include_glob", value=include_glob, expected_type=type_hints["include_glob"])
            check_type(argname="argument include_list_file", value=include_list_file, expected_type=type_hints["include_list_file"])
            check_type(argname="argument include_regex", value=include_regex, expected_type=type_hints["include_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_glob is not None:
            self._values["exclude_glob"] = exclude_glob
        if exclude_regex is not None:
            self._values["exclude_regex"] = exclude_regex
        if include_files is not None:
            self._values["include_files"] = include_files
        if include_glob is not None:
            self._values["include_glob"] = include_glob
        if include_list_file is not None:
            self._values["include_list_file"] = include_list_file
        if include_regex is not None:
            self._values["include_regex"] = include_regex

    @builtins.property
    def exclude_glob(self) -> typing.Optional[builtins.str]:
        '''(experimental) Glob pattern that specifies the set of source files to exclude from analysis.

        Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.

        :stability: experimental
        :schema: analyze-files-configuration#exclude-glob
        '''
        result = self._values.get("exclude_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression that specifies the set of source files to exclude from analysis.

        Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.

        :stability: experimental
        :schema: analyze-files-configuration#exclude-regex
        '''
        result = self._values.get("exclude_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_files(self) -> typing.Optional[builtins.str]:
        '''(experimental) Paths of source files to analyze.

        Include and exclude glob patterns and regular expressions are applied to determine which of these files are actually analyzed.

        :stability: experimental
        :schema: analyze-files-configuration#include-files
        '''
        result = self._values.get("include_files")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_glob(self) -> typing.Optional[builtins.str]:
        '''(experimental) Glob pattern that specifies the set of source files to analyze.

        :stability: experimental
        :schema: analyze-files-configuration#include-glob
        '''
        result = self._values.get("include_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_list_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the paths of source files to analyze, one per line.

        Include and exclude glob patterns and regular expressions are applied to determine which of these files are actually analyzed.

        :stability: experimental
        :schema: analyze-files-configuration#include-list-file
        '''
        result = self._values.get("include_list_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression that specifies the set of source files to analyze.

        :stability: experimental
        :schema: analyze-files-configuration#include-regex
        '''
        result = self._values.get("include_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AnalyzeFilesConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.BuildConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "build_command": "buildCommand",
        "aspnet_compiler": "aspnetCompiler",
        "bazel": "bazel",
        "clean_command": "cleanCommand",
        "cov_build_args": "covBuildArgs",
        "defer_decomp": "deferDecomp",
        "instrument": "instrument",
        "parallel_translate": "parallelTranslate",
        "scan_transparency": "scanTransparency",
    },
)
class BuildConfiguration:
    def __init__(
        self,
        *,
        build_command: builtins.str,
        aspnet_compiler: typing.Optional[builtins.bool] = None,
        bazel: typing.Optional[builtins.bool] = None,
        clean_command: typing.Optional[builtins.str] = None,
        cov_build_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        defer_decomp: typing.Optional[builtins.bool] = None,
        instrument: typing.Optional[builtins.bool] = None,
        parallel_translate: typing.Optional[typing.Union["ParallelTranslateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        scan_transparency: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Specifies that build capture should be used to capture the project and provides the build configuration to use.

        If not specified and the project directory contains compiled source files then automatic build capture will be used to capture compiled source files in the project directory.

        :param build_command: (experimental) The build command will be invoked to use build capture to capture the project. A build command specified on the command-line will override this setting.
        :param aspnet_compiler: (experimental) Specifies whether to enable or disable the automatic invocation of Aspnet_compiler.exe for any ASP.NET 4 and earlier Web applications that are detected in the build. The output of Aspnet_compiler.exe is required by the C# and Visual Basic security checkers.
        :param bazel: (experimental) Specifies whether to enable Bazel capture.
        :param clean_command: (experimental) The clean command will be invoked prior to doing build capture to capture the project.
        :param cov_build_args: (experimental) Additional arguments to pass to cov-build when doing build capture.
        :param defer_decomp: (experimental) Specifies whether the build should only record the decompilations of byte code during the build and not attempt to decompile and emit the byte code. During the analysis phase, cov-build will be rerun with --replay-decomp to decompile and emit the byte code.
        :param instrument: (experimental) Specifies whether to use the instrumentation mode instead of the debugger. For certain builds, this configuration can significantly improve build times. This setting is applicable only on Windows.
        :param parallel_translate: (experimental) Specifies how to parallelize translation of C and C++ code.
        :param scan_transparency: (experimental) Specifies whether to enable the collection of scan transparency data for build capture. This setting must be enabled if the Coverity Connect instance has 'scan.transparency.enabled=true' in its configuration.

        :stability: experimental
        :schema: build-configuration
        '''
        if isinstance(parallel_translate, dict):
            parallel_translate = ParallelTranslateConfiguration(**parallel_translate)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b758dad2d938ef8d86e6197414de189afa576eb5a6f03b29fe130fd3a4b779af)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument aspnet_compiler", value=aspnet_compiler, expected_type=type_hints["aspnet_compiler"])
            check_type(argname="argument bazel", value=bazel, expected_type=type_hints["bazel"])
            check_type(argname="argument clean_command", value=clean_command, expected_type=type_hints["clean_command"])
            check_type(argname="argument cov_build_args", value=cov_build_args, expected_type=type_hints["cov_build_args"])
            check_type(argname="argument defer_decomp", value=defer_decomp, expected_type=type_hints["defer_decomp"])
            check_type(argname="argument instrument", value=instrument, expected_type=type_hints["instrument"])
            check_type(argname="argument parallel_translate", value=parallel_translate, expected_type=type_hints["parallel_translate"])
            check_type(argname="argument scan_transparency", value=scan_transparency, expected_type=type_hints["scan_transparency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "build_command": build_command,
        }
        if aspnet_compiler is not None:
            self._values["aspnet_compiler"] = aspnet_compiler
        if bazel is not None:
            self._values["bazel"] = bazel
        if clean_command is not None:
            self._values["clean_command"] = clean_command
        if cov_build_args is not None:
            self._values["cov_build_args"] = cov_build_args
        if defer_decomp is not None:
            self._values["defer_decomp"] = defer_decomp
        if instrument is not None:
            self._values["instrument"] = instrument
        if parallel_translate is not None:
            self._values["parallel_translate"] = parallel_translate
        if scan_transparency is not None:
            self._values["scan_transparency"] = scan_transparency

    @builtins.property
    def build_command(self) -> builtins.str:
        '''(experimental) The build command will be invoked to use build capture to capture the project.

        A build command specified on the command-line will override this setting.

        :stability: experimental
        :schema: build-configuration#build-command
        '''
        result = self._values.get("build_command")
        assert result is not None, "Required property 'build_command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspnet_compiler(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable or disable the automatic invocation of Aspnet_compiler.exe for any ASP.NET 4 and earlier Web applications that are detected in the build. The output of Aspnet_compiler.exe is required by the C# and Visual Basic security checkers.

        :stability: experimental
        :schema: build-configuration#aspnet-compiler
        '''
        result = self._values.get("aspnet_compiler")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bazel(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable Bazel capture.

        :stability: experimental
        :schema: build-configuration#bazel
        '''
        result = self._values.get("bazel")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def clean_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The clean command will be invoked prior to doing build capture to capture the project.

        :stability: experimental
        :schema: build-configuration#clean-command
        '''
        result = self._values.get("clean_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cov_build_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional arguments to pass to cov-build when doing build capture.

        :stability: experimental
        :schema: build-configuration#cov-build-args
        '''
        result = self._values.get("cov_build_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def defer_decomp(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the build should only record the decompilations of byte code during the build and not attempt to decompile and emit the byte code.

        During the analysis phase, cov-build will be rerun with --replay-decomp to decompile and emit the byte code.

        :stability: experimental
        :schema: build-configuration#defer-decomp
        '''
        result = self._values.get("defer_decomp")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instrument(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to use the instrumentation mode instead of the debugger.

        For certain builds, this configuration can significantly improve build times. This setting is applicable only on Windows.

        :stability: experimental
        :schema: build-configuration#instrument
        '''
        result = self._values.get("instrument")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parallel_translate(self) -> typing.Optional["ParallelTranslateConfiguration"]:
        '''(experimental) Specifies how to parallelize translation of C and C++ code.

        :stability: experimental
        :schema: build-configuration#parallel-translate
        '''
        result = self._values.get("parallel_translate")
        return typing.cast(typing.Optional["ParallelTranslateConfiguration"], result)

    @builtins.property
    def scan_transparency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable the collection of scan transparency data for build capture.

        This setting must be enabled if the Coverity Connect instance has 'scan.transparency.enabled=true' in its configuration.

        :stability: experimental
        :schema: build-configuration#scan-transparency
        '''
        result = self._values.get("scan_transparency")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CachingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CachingConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Specifies how the CLI should handle caching when performing capture/analysis.

        :param enabled: (experimental) A true value indicates caching will be used when performing remote analysis.

        :stability: experimental
        :schema: caching-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3f0b433d7ebb00cc93576ab8200b34f77607aae46ff169416465fb293a5a4cb1)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A true value indicates caching will be used when performing remote analysis.

        :stability: experimental
        :schema: caching-configuration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CachingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CaptureConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "build_capture": "buildCapture",
        "build_command_inference": "buildCommandInference",
        "compiler_configuration": "compilerConfiguration",
        "cov_translate": "covTranslate",
        "emit_complementary_info": "emitComplementaryInfo",
        "encoding": "encoding",
        "failure_threshold_percent": "failureThresholdPercent",
        "files": "files",
        "force_dependency_resolution": "forceDependencyResolution",
        "import_scm": "importScm",
        "languages": "languages",
        "minimal_classpath_emit": "minimalClasspathEmit",
        "record_with_source": "recordWithSource",
        "security_da": "securityDa",
    },
)
class CaptureConfiguration:
    def __init__(
        self,
        *,
        build_capture: typing.Optional[typing.Union["BuildConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        build_command_inference: typing.Optional[builtins.bool] = None,
        compiler_configuration: typing.Optional[typing.Union["CompilerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        cov_translate: typing.Optional[typing.Union["CovTranslateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        emit_complementary_info: typing.Optional[builtins.bool] = None,
        encoding: typing.Optional[builtins.str] = None,
        failure_threshold_percent: typing.Optional[jsii.Number] = None,
        files: typing.Optional[typing.Union["FilesConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        force_dependency_resolution: typing.Optional[builtins.bool] = None,
        import_scm: typing.Optional[typing.Union["ImportScmConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        languages: typing.Optional[typing.Union["LanguagesConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        minimal_classpath_emit: typing.Optional[builtins.bool] = None,
        record_with_source: typing.Optional[builtins.bool] = None,
        security_da: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Specifies how the project should be captured.

        :param build_capture: 
        :param build_command_inference: (experimental) Specifies whether to enable or disable build command inference. If build command inference is disabled and no build command is provided then no attempt at build capture will be made.
        :param compiler_configuration: (experimental) Specifies which compilers to configure. By default, template compilers are configured.
        :param cov_translate: 
        :param emit_complementary_info: (experimental) Records additional information during the emit process needed for the compliance checkers. If a "coding-standards" configuration is present then this flag will automatically be set to true.
        :param encoding: (experimental) Specifies the encoding to use when parsing and emitting the source files.
        :param failure_threshold_percent: (experimental) Specifies the minimum percentage of files that must be captured in order to proceed with the analysis.
        :param files: (experimental) Specifies which non-compiled files to capture. By default, all files are captured.
        :param force_dependency_resolution: (experimental) Force resolution of Maven, Gradle and MSBuild dependencies even if this is not needed based on the detected source languages in the project.
        :param import_scm: (experimental) Specifies how to import data about source file changes from the source control management system.
        :param languages: (experimental) Specifies which languages to include or exclude for capture. By default, all languages are captured.
        :param minimal_classpath_emit: (experimental) Specifies whether to limit the group of emitted JAR files to those needed for compilation of the Java files. The default behavior without this option is to emit all the JAR files in the classpath regardless of whether they are referenced by a Java file in the compilation.
        :param record_with_source: (experimental) Specifies whether to do a complete capture or a record with source capture.
        :param security_da: (experimental) Enables or disables security dynamic analysis. If set to true (the default), security dynamic analysis is run as part of the capture step. If set to false, security dynamic analysis is not run.

        :stability: experimental
        :schema: capture-configuration
        '''
        if isinstance(build_capture, dict):
            build_capture = BuildConfiguration(**build_capture)
        if isinstance(compiler_configuration, dict):
            compiler_configuration = CompilerConfiguration(**compiler_configuration)
        if isinstance(cov_translate, dict):
            cov_translate = CovTranslateConfiguration(**cov_translate)
        if isinstance(files, dict):
            files = FilesConfiguration(**files)
        if isinstance(import_scm, dict):
            import_scm = ImportScmConfiguration(**import_scm)
        if isinstance(languages, dict):
            languages = LanguagesConfiguration(**languages)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8de5dfcfda282391d183474360405466b889cca5ccc239d1e268f01a81936d8d)
            check_type(argname="argument build_capture", value=build_capture, expected_type=type_hints["build_capture"])
            check_type(argname="argument build_command_inference", value=build_command_inference, expected_type=type_hints["build_command_inference"])
            check_type(argname="argument compiler_configuration", value=compiler_configuration, expected_type=type_hints["compiler_configuration"])
            check_type(argname="argument cov_translate", value=cov_translate, expected_type=type_hints["cov_translate"])
            check_type(argname="argument emit_complementary_info", value=emit_complementary_info, expected_type=type_hints["emit_complementary_info"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument failure_threshold_percent", value=failure_threshold_percent, expected_type=type_hints["failure_threshold_percent"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument force_dependency_resolution", value=force_dependency_resolution, expected_type=type_hints["force_dependency_resolution"])
            check_type(argname="argument import_scm", value=import_scm, expected_type=type_hints["import_scm"])
            check_type(argname="argument languages", value=languages, expected_type=type_hints["languages"])
            check_type(argname="argument minimal_classpath_emit", value=minimal_classpath_emit, expected_type=type_hints["minimal_classpath_emit"])
            check_type(argname="argument record_with_source", value=record_with_source, expected_type=type_hints["record_with_source"])
            check_type(argname="argument security_da", value=security_da, expected_type=type_hints["security_da"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_capture is not None:
            self._values["build_capture"] = build_capture
        if build_command_inference is not None:
            self._values["build_command_inference"] = build_command_inference
        if compiler_configuration is not None:
            self._values["compiler_configuration"] = compiler_configuration
        if cov_translate is not None:
            self._values["cov_translate"] = cov_translate
        if emit_complementary_info is not None:
            self._values["emit_complementary_info"] = emit_complementary_info
        if encoding is not None:
            self._values["encoding"] = encoding
        if failure_threshold_percent is not None:
            self._values["failure_threshold_percent"] = failure_threshold_percent
        if files is not None:
            self._values["files"] = files
        if force_dependency_resolution is not None:
            self._values["force_dependency_resolution"] = force_dependency_resolution
        if import_scm is not None:
            self._values["import_scm"] = import_scm
        if languages is not None:
            self._values["languages"] = languages
        if minimal_classpath_emit is not None:
            self._values["minimal_classpath_emit"] = minimal_classpath_emit
        if record_with_source is not None:
            self._values["record_with_source"] = record_with_source
        if security_da is not None:
            self._values["security_da"] = security_da

    @builtins.property
    def build_capture(self) -> typing.Optional["BuildConfiguration"]:
        '''
        :stability: experimental
        :schema: capture-configuration#build-capture
        '''
        result = self._values.get("build_capture")
        return typing.cast(typing.Optional["BuildConfiguration"], result)

    @builtins.property
    def build_command_inference(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable or disable build command inference.

        If build command inference is disabled and no build command is provided then no attempt at build capture will be made.

        :stability: experimental
        :schema: capture-configuration#build-command-inference
        '''
        result = self._values.get("build_command_inference")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compiler_configuration(self) -> typing.Optional["CompilerConfiguration"]:
        '''(experimental) Specifies which compilers to configure.

        By default, template compilers are configured.

        :stability: experimental
        :schema: capture-configuration#compiler-configuration
        '''
        result = self._values.get("compiler_configuration")
        return typing.cast(typing.Optional["CompilerConfiguration"], result)

    @builtins.property
    def cov_translate(self) -> typing.Optional["CovTranslateConfiguration"]:
        '''
        :stability: experimental
        :schema: capture-configuration#cov-translate
        '''
        result = self._values.get("cov_translate")
        return typing.cast(typing.Optional["CovTranslateConfiguration"], result)

    @builtins.property
    def emit_complementary_info(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Records additional information during the emit process needed for the compliance checkers.

        If a "coding-standards" configuration is present then this flag will automatically be set to true.

        :stability: experimental
        :schema: capture-configuration#emit-complementary-info
        '''
        result = self._values.get("emit_complementary_info")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the encoding to use when parsing and emitting the source files.

        :stability: experimental
        :schema: capture-configuration#encoding
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the minimum percentage of files that must be captured in order to proceed with the analysis.

        :stability: experimental
        :schema: capture-configuration#failure-threshold-percent
        '''
        result = self._values.get("failure_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def files(self) -> typing.Optional["FilesConfiguration"]:
        '''(experimental) Specifies which non-compiled files to capture.

        By default, all files are captured.

        :stability: experimental
        :schema: capture-configuration#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional["FilesConfiguration"], result)

    @builtins.property
    def force_dependency_resolution(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force resolution of Maven, Gradle and MSBuild dependencies even if this is not needed based on the detected source languages in the project.

        :stability: experimental
        :schema: capture-configuration#force-dependency-resolution
        '''
        result = self._values.get("force_dependency_resolution")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def import_scm(self) -> typing.Optional["ImportScmConfiguration"]:
        '''(experimental) Specifies how to import data about source file changes from the source control management system.

        :stability: experimental
        :schema: capture-configuration#import-scm
        '''
        result = self._values.get("import_scm")
        return typing.cast(typing.Optional["ImportScmConfiguration"], result)

    @builtins.property
    def languages(self) -> typing.Optional["LanguagesConfiguration"]:
        '''(experimental) Specifies which languages to include or exclude for capture.

        By default, all languages are captured.

        :stability: experimental
        :schema: capture-configuration#languages
        '''
        result = self._values.get("languages")
        return typing.cast(typing.Optional["LanguagesConfiguration"], result)

    @builtins.property
    def minimal_classpath_emit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to limit the group of emitted JAR files to those needed for compilation of the Java files.

        The default behavior without this option is to emit all the JAR files in the classpath regardless of whether they are referenced by a Java file in the compilation.

        :stability: experimental
        :schema: capture-configuration#minimal-classpath-emit
        '''
        result = self._values.get("minimal_classpath_emit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_with_source(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to do a complete capture or a record with source capture.

        :stability: experimental
        :schema: capture-configuration#record-with-source
        '''
        result = self._values.get("record_with_source")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_da(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables security dynamic analysis.

        If set to true (the default), security dynamic analysis is run as part of the capture step. If set to false, security dynamic analysis is not run.

        :stability: experimental
        :schema: capture-configuration#security-da
        '''
        result = self._values.get("security_da")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CaptureConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CheckerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "all_security": "allSecurity",
        "android_security": "androidSecurity",
        "audit": "audit",
        "brakeman": "brakeman",
        "c_family_security": "cFamilySecurity",
        "checker_config": "checkerConfig",
        "codexm": "codexm",
        "concurrency": "concurrency",
        "default": "default",
        "pmd": "pmd",
        "recommended_security_checkers": "recommendedSecurityCheckers",
        "rule": "rule",
        "webapp_security": "webappSecurity",
    },
)
class CheckerConfiguration:
    def __init__(
        self,
        *,
        all: typing.Optional[builtins.bool] = None,
        all_security: typing.Optional[builtins.bool] = None,
        android_security: typing.Optional[builtins.bool] = None,
        audit: typing.Optional[builtins.bool] = None,
        brakeman: typing.Optional[builtins.bool] = None,
        c_family_security: typing.Optional[builtins.bool] = None,
        checker_config: typing.Any = None,
        codexm: typing.Optional[typing.Sequence[builtins.str]] = None,
        concurrency: typing.Optional[builtins.bool] = None,
        default: typing.Optional[builtins.bool] = None,
        pmd: typing.Optional[builtins.bool] = None,
        recommended_security_checkers: typing.Optional[builtins.bool] = None,
        rule: typing.Optional[builtins.bool] = None,
        webapp_security: typing.Optional[typing.Union["CheckerConfigurationWebappSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param all: (experimental) Indicates whether all checkers should be enabled.
        :param all_security: (experimental) Indicates whether all security checkers should be enabled. This includes the Security, Android Security, and Web App Security categories, and other security checkers that require explicit enablement.
        :param android_security: (experimental) If set to true, enables android security checkers.
        :param audit: (experimental) Enables audit checkers.
        :param brakeman: (experimental) Indicates whether the brakeman checkers should be enabled or disabled.
        :param c_family_security: (experimental) Enables C, C++, Objective-C, Objective-C++ security-related checkers that are disabled by default.
        :param checker_config: (experimental) Map from checker name to configuration for the checker. The configuration indicates whether the checker should be enabled or not and allows users to set options used to configure the checker.
        :param codexm: (experimental) Specifies CodeXM (.cxm) files to use in the analysis.
        :param concurrency: (experimental) Enables C, C++ concurrency checkers that are disabled by default.
        :param default: (experimental) Specifies whether to enable the default set of checkers. If set to true, the default set of checkers is enabled. Set to false to get more control over which checkers are enabled.
        :param pmd: (experimental) Enables or disables PMD for Apex analysis.
        :param recommended_security_checkers: (experimental) Enables or disables recommended security checkers.
        :param rule: (experimental) Enables C, C++ rule checkers.
        :param webapp_security: (experimental) Specifies how web application security analysis should be done.

        :stability: experimental
        :schema: checker-configuration
        '''
        if isinstance(webapp_security, dict):
            webapp_security = CheckerConfigurationWebappSecurity(**webapp_security)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__20118a538bd2f0c6222fa6c379224b2d866df17d41c1f5ad837f0a235c928a66)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument all_security", value=all_security, expected_type=type_hints["all_security"])
            check_type(argname="argument android_security", value=android_security, expected_type=type_hints["android_security"])
            check_type(argname="argument audit", value=audit, expected_type=type_hints["audit"])
            check_type(argname="argument brakeman", value=brakeman, expected_type=type_hints["brakeman"])
            check_type(argname="argument c_family_security", value=c_family_security, expected_type=type_hints["c_family_security"])
            check_type(argname="argument checker_config", value=checker_config, expected_type=type_hints["checker_config"])
            check_type(argname="argument codexm", value=codexm, expected_type=type_hints["codexm"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument pmd", value=pmd, expected_type=type_hints["pmd"])
            check_type(argname="argument recommended_security_checkers", value=recommended_security_checkers, expected_type=type_hints["recommended_security_checkers"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument webapp_security", value=webapp_security, expected_type=type_hints["webapp_security"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if all_security is not None:
            self._values["all_security"] = all_security
        if android_security is not None:
            self._values["android_security"] = android_security
        if audit is not None:
            self._values["audit"] = audit
        if brakeman is not None:
            self._values["brakeman"] = brakeman
        if c_family_security is not None:
            self._values["c_family_security"] = c_family_security
        if checker_config is not None:
            self._values["checker_config"] = checker_config
        if codexm is not None:
            self._values["codexm"] = codexm
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if default is not None:
            self._values["default"] = default
        if pmd is not None:
            self._values["pmd"] = pmd
        if recommended_security_checkers is not None:
            self._values["recommended_security_checkers"] = recommended_security_checkers
        if rule is not None:
            self._values["rule"] = rule
        if webapp_security is not None:
            self._values["webapp_security"] = webapp_security

    @builtins.property
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether all checkers should be enabled.

        :stability: experimental
        :schema: checker-configuration#all
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def all_security(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether all security checkers should be enabled.

        This includes the Security, Android Security, and Web App Security categories, and other security checkers that require explicit enablement.

        :stability: experimental
        :schema: checker-configuration#all-security
        '''
        result = self._values.get("all_security")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def android_security(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to true, enables android security checkers.

        :stability: experimental
        :schema: checker-configuration#android-security
        '''
        result = self._values.get("android_security")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def audit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables audit checkers.

        :stability: experimental
        :schema: checker-configuration#audit
        '''
        result = self._values.get("audit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def brakeman(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the brakeman checkers should be enabled or disabled.

        :stability: experimental
        :schema: checker-configuration#brakeman
        '''
        result = self._values.get("brakeman")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def c_family_security(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables C, C++, Objective-C, Objective-C++ security-related checkers that are disabled by default.

        :stability: experimental
        :schema: checker-configuration#c-family-security
        '''
        result = self._values.get("c_family_security")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def checker_config(self) -> typing.Any:
        '''(experimental) Map from checker name to configuration for the checker.

        The configuration indicates whether the checker should be enabled or not and allows users to set options used to configure the checker.

        :stability: experimental
        :schema: checker-configuration#checker-config
        '''
        result = self._values.get("checker_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def codexm(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specifies CodeXM (.cxm) files to use in the analysis.

        :stability: experimental
        :schema: checker-configuration#codexm
        '''
        result = self._values.get("codexm")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def concurrency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables C, C++ concurrency checkers that are disabled by default.

        :stability: experimental
        :schema: checker-configuration#concurrency
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable the default set of checkers.

        If set to true, the default set of checkers is enabled. Set to false to get more control over which checkers are enabled.

        :stability: experimental
        :schema: checker-configuration#default
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pmd(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables PMD for Apex analysis.

        :stability: experimental
        :schema: checker-configuration#pmd
        '''
        result = self._values.get("pmd")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def recommended_security_checkers(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables recommended security checkers.

        :stability: experimental
        :schema: checker-configuration#recommended-security-checkers
        '''
        result = self._values.get("recommended_security_checkers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables C, C++ rule checkers.

        :stability: experimental
        :schema: checker-configuration#rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def webapp_security(self) -> typing.Optional["CheckerConfigurationWebappSecurity"]:
        '''(experimental) Specifies how web application security analysis should be done.

        :stability: experimental
        :schema: checker-configuration#webapp-security
        '''
        result = self._values.get("webapp_security")
        return typing.cast(typing.Optional["CheckerConfigurationWebappSecurity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CheckerConfigurationWebappSecurity",
    jsii_struct_bases=[],
    name_mapping={"aggressiveness_level": "aggressivenessLevel", "enabled": "enabled"},
)
class CheckerConfigurationWebappSecurity:
    def __init__(
        self,
        *,
        aggressiveness_level: typing.Optional["CheckerConfigurationWebappSecurityAggressivenessLevel"] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Specifies how web application security analysis should be done.

        :param aggressiveness_level: (experimental) Sets the web application checkers aggressiveness level.
        :param enabled: (experimental) Enables the checkers that are used for web application security analysis.

        :stability: experimental
        :schema: CheckerConfigurationWebappSecurity
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__846d906367a3a82580d316c7a445a95e059c18dc8ea53adca4a04d0c958decc2)
            check_type(argname="argument aggressiveness_level", value=aggressiveness_level, expected_type=type_hints["aggressiveness_level"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggressiveness_level is not None:
            self._values["aggressiveness_level"] = aggressiveness_level
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def aggressiveness_level(
        self,
    ) -> typing.Optional["CheckerConfigurationWebappSecurityAggressivenessLevel"]:
        '''(experimental) Sets the web application checkers aggressiveness level.

        :stability: experimental
        :schema: CheckerConfigurationWebappSecurity#aggressiveness-level
        '''
        result = self._values.get("aggressiveness_level")
        return typing.cast(typing.Optional["CheckerConfigurationWebappSecurityAggressivenessLevel"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the checkers that are used for web application security analysis.

        :stability: experimental
        :schema: CheckerConfigurationWebappSecurity#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckerConfigurationWebappSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="projen.polaris.CheckerConfigurationWebappSecurityAggressivenessLevel"
)
class CheckerConfigurationWebappSecurityAggressivenessLevel(enum.Enum):
    '''(experimental) Sets the web application checkers aggressiveness level.

    :stability: experimental
    :schema: CheckerConfigurationWebappSecurityAggressivenessLevel
    '''

    LOW = "LOW"
    '''(experimental) low.

    :stability: experimental
    '''
    MEDIUM = "MEDIUM"
    '''(experimental) medium.

    :stability: experimental
    '''
    HIGH = "HIGH"
    '''(experimental) high.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.CodingStandardConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "autosarcpp14": "autosarcpp14",
        "cert_c": "certC",
        "cert_cpp": "certCpp",
        "cert_c_recommendation": "certCRecommendation",
        "cert_java": "certJava",
        "hyundai_c": "hyundaiC",
        "hyundai_cpp": "hyundaiCpp",
        "hyundai_java": "hyundaiJava",
        "ignore_deviated_findings": "ignoreDeviatedFindings",
        "iso_ts17961": "isoTs17961",
        "misrac2004": "misrac2004",
        "misrac2012": "misrac2012",
        "misrac2023": "misrac2023",
        "misracpp2008": "misracpp2008",
        "misracpp2023": "misracpp2023",
    },
)
class CodingStandardConfiguration:
    def __init__(
        self,
        *,
        autosarcpp14: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        cert_c: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        cert_cpp: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        cert_c_recommendation: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        cert_java: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        hyundai_c: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        hyundai_cpp: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        hyundai_java: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_deviated_findings: typing.Optional[builtins.bool] = None,
        iso_ts17961: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        misrac2004: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        misrac2012: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        misrac2023: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        misracpp2008: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        misracpp2023: typing.Optional[typing.Union["SpecificCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autosarcpp14: (experimental) Enables AUTOSAR code compliance checking according to the given configuration.
        :param cert_c: (experimental) Enables CERT-C code compliance checking according to the given configuration.
        :param cert_cpp: (experimental) Enables CERT-CPP code compliance checking according to the given configuration.
        :param cert_c_recommendation: (experimental) Enables CERT-C Recommendation code compliance checking according to the given configuration.
        :param cert_java: (experimental) Enables CERT-Java code compliance checking according to the given configuration.
        :param hyundai_c: (experimental) Enables HYUNDAI-C code compliance checking according to the given configuration.
        :param hyundai_cpp: (experimental) Enables HYUNDAI-CPP code compliance checking according to the given configuration.
        :param hyundai_java: (experimental) Enables HYUNDAI-Java code compliance checking according to the given configuration.
        :param ignore_deviated_findings: (experimental) If set to true, any defects found in code annotated using the #pragma Coverity compliance directive will not be reported in Coverity Connect. Information about the defects that were suppressed can then be found in two files: deviations.txt deviations-warnings.txt
        :param iso_ts17961: (experimental) Enables ISO TS 17961 code compliance checking according to the given configuration.
        :param misrac2004: (experimental) Enables MISRA C 2004 code compliance checking according to the given configuration.
        :param misrac2012: (experimental) Enables MISRA C 2012 code compliance checking according to the given configuration.
        :param misrac2023: (experimental) Enables MISRA C 2023 code compliance checking according to the given configuration.
        :param misracpp2008: (experimental) Enables MISRA C++ 2008 code compliance checking according to the given configuration.
        :param misracpp2023: (experimental) Enables MISRA C++ 2023 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration
        '''
        if isinstance(autosarcpp14, dict):
            autosarcpp14 = SpecificCodingStandardConfiguration(**autosarcpp14)
        if isinstance(cert_c, dict):
            cert_c = SpecificCodingStandardConfiguration(**cert_c)
        if isinstance(cert_cpp, dict):
            cert_cpp = SpecificCodingStandardConfiguration(**cert_cpp)
        if isinstance(cert_c_recommendation, dict):
            cert_c_recommendation = SpecificCodingStandardConfiguration(**cert_c_recommendation)
        if isinstance(cert_java, dict):
            cert_java = SpecificCodingStandardConfiguration(**cert_java)
        if isinstance(hyundai_c, dict):
            hyundai_c = SpecificCodingStandardConfiguration(**hyundai_c)
        if isinstance(hyundai_cpp, dict):
            hyundai_cpp = SpecificCodingStandardConfiguration(**hyundai_cpp)
        if isinstance(hyundai_java, dict):
            hyundai_java = SpecificCodingStandardConfiguration(**hyundai_java)
        if isinstance(iso_ts17961, dict):
            iso_ts17961 = SpecificCodingStandardConfiguration(**iso_ts17961)
        if isinstance(misrac2004, dict):
            misrac2004 = SpecificCodingStandardConfiguration(**misrac2004)
        if isinstance(misrac2012, dict):
            misrac2012 = SpecificCodingStandardConfiguration(**misrac2012)
        if isinstance(misrac2023, dict):
            misrac2023 = SpecificCodingStandardConfiguration(**misrac2023)
        if isinstance(misracpp2008, dict):
            misracpp2008 = SpecificCodingStandardConfiguration(**misracpp2008)
        if isinstance(misracpp2023, dict):
            misracpp2023 = SpecificCodingStandardConfiguration(**misracpp2023)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e8d746461fb5b288993834907d57557d631e8a7e2b2aefb9659029516fce68eb)
            check_type(argname="argument autosarcpp14", value=autosarcpp14, expected_type=type_hints["autosarcpp14"])
            check_type(argname="argument cert_c", value=cert_c, expected_type=type_hints["cert_c"])
            check_type(argname="argument cert_cpp", value=cert_cpp, expected_type=type_hints["cert_cpp"])
            check_type(argname="argument cert_c_recommendation", value=cert_c_recommendation, expected_type=type_hints["cert_c_recommendation"])
            check_type(argname="argument cert_java", value=cert_java, expected_type=type_hints["cert_java"])
            check_type(argname="argument hyundai_c", value=hyundai_c, expected_type=type_hints["hyundai_c"])
            check_type(argname="argument hyundai_cpp", value=hyundai_cpp, expected_type=type_hints["hyundai_cpp"])
            check_type(argname="argument hyundai_java", value=hyundai_java, expected_type=type_hints["hyundai_java"])
            check_type(argname="argument ignore_deviated_findings", value=ignore_deviated_findings, expected_type=type_hints["ignore_deviated_findings"])
            check_type(argname="argument iso_ts17961", value=iso_ts17961, expected_type=type_hints["iso_ts17961"])
            check_type(argname="argument misrac2004", value=misrac2004, expected_type=type_hints["misrac2004"])
            check_type(argname="argument misrac2012", value=misrac2012, expected_type=type_hints["misrac2012"])
            check_type(argname="argument misrac2023", value=misrac2023, expected_type=type_hints["misrac2023"])
            check_type(argname="argument misracpp2008", value=misracpp2008, expected_type=type_hints["misracpp2008"])
            check_type(argname="argument misracpp2023", value=misracpp2023, expected_type=type_hints["misracpp2023"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autosarcpp14 is not None:
            self._values["autosarcpp14"] = autosarcpp14
        if cert_c is not None:
            self._values["cert_c"] = cert_c
        if cert_cpp is not None:
            self._values["cert_cpp"] = cert_cpp
        if cert_c_recommendation is not None:
            self._values["cert_c_recommendation"] = cert_c_recommendation
        if cert_java is not None:
            self._values["cert_java"] = cert_java
        if hyundai_c is not None:
            self._values["hyundai_c"] = hyundai_c
        if hyundai_cpp is not None:
            self._values["hyundai_cpp"] = hyundai_cpp
        if hyundai_java is not None:
            self._values["hyundai_java"] = hyundai_java
        if ignore_deviated_findings is not None:
            self._values["ignore_deviated_findings"] = ignore_deviated_findings
        if iso_ts17961 is not None:
            self._values["iso_ts17961"] = iso_ts17961
        if misrac2004 is not None:
            self._values["misrac2004"] = misrac2004
        if misrac2012 is not None:
            self._values["misrac2012"] = misrac2012
        if misrac2023 is not None:
            self._values["misrac2023"] = misrac2023
        if misracpp2008 is not None:
            self._values["misracpp2008"] = misracpp2008
        if misracpp2023 is not None:
            self._values["misracpp2023"] = misracpp2023

    @builtins.property
    def autosarcpp14(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables AUTOSAR code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#autosarcpp14
        '''
        result = self._values.get("autosarcpp14")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def cert_c(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables CERT-C code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#cert-c
        '''
        result = self._values.get("cert_c")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def cert_cpp(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables CERT-CPP code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#cert-cpp
        '''
        result = self._values.get("cert_cpp")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def cert_c_recommendation(
        self,
    ) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables CERT-C Recommendation code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#cert-c-recommendation
        '''
        result = self._values.get("cert_c_recommendation")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def cert_java(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables CERT-Java code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#cert-java
        '''
        result = self._values.get("cert_java")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def hyundai_c(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables HYUNDAI-C code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#hyundai-c
        '''
        result = self._values.get("hyundai_c")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def hyundai_cpp(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables HYUNDAI-CPP code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#hyundai-cpp
        '''
        result = self._values.get("hyundai_cpp")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def hyundai_java(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables HYUNDAI-Java code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#hyundai-java
        '''
        result = self._values.get("hyundai_java")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def ignore_deviated_findings(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to true, any defects found in code annotated using the #pragma Coverity compliance directive will not be reported in Coverity Connect.

        Information about the defects that were suppressed can then be found in two files: deviations.txt deviations-warnings.txt

        :stability: experimental
        :schema: coding-standard-configuration#ignore-deviated-findings
        '''
        result = self._values.get("ignore_deviated_findings")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iso_ts17961(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables ISO TS 17961 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#iso-ts17961
        '''
        result = self._values.get("iso_ts17961")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def misrac2004(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables MISRA C 2004 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#misrac2004
        '''
        result = self._values.get("misrac2004")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def misrac2012(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables MISRA C 2012 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#misrac2012
        '''
        result = self._values.get("misrac2012")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def misrac2023(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables MISRA C 2023 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#misrac2023
        '''
        result = self._values.get("misrac2023")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def misracpp2008(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables MISRA C++ 2008 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#misracpp2008
        '''
        result = self._values.get("misracpp2008")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    @builtins.property
    def misracpp2023(self) -> typing.Optional["SpecificCodingStandardConfiguration"]:
        '''(experimental) Enables MISRA C++ 2023 code compliance checking according to the given configuration.

        :stability: experimental
        :schema: coding-standard-configuration#misracpp2023
        '''
        result = self._values.get("misracpp2023")
        return typing.cast(typing.Optional["SpecificCodingStandardConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodingStandardConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CodingStandardDeviation",
    jsii_struct_bases=[],
    name_mapping={"deviation": "deviation", "reason": "reason"},
)
class CodingStandardDeviation:
    def __init__(self, *, deviation: builtins.str, reason: builtins.str) -> None:
        '''
        :param deviation: (experimental) The name of the rule to deviate from.
        :param reason: (experimental) The reason that the rule is being deviated from.

        :stability: experimental
        :schema: coding-standard-deviation
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__093a59ecfe140bbb066a4c2ce8ec4e051c97545feaddca5c4422d6edf24d2a89)
            check_type(argname="argument deviation", value=deviation, expected_type=type_hints["deviation"])
            check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deviation": deviation,
            "reason": reason,
        }

    @builtins.property
    def deviation(self) -> builtins.str:
        '''(experimental) The name of the rule to deviate from.

        :stability: experimental
        :schema: coding-standard-deviation#deviation
        '''
        result = self._values.get("deviation")
        assert result is not None, "Required property 'deviation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reason(self) -> builtins.str:
        '''(experimental) The reason that the rule is being deviated from.

        :stability: experimental
        :schema: coding-standard-deviation#reason
        '''
        result = self._values.get("reason")
        assert result is not None, "Required property 'reason' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodingStandardDeviation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CommitConfiguration",
    jsii_struct_bases=[],
    name_mapping={"connect": "connect", "local": "local", "srm": "srm"},
)
class CommitConfiguration:
    def __init__(
        self,
        *,
        connect: typing.Optional[typing.Union["CommitConfigurationConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        local: typing.Optional[typing.Union["CommitConfigurationLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        srm: typing.Optional[typing.Union["CommitConfigurationSrm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Specifies where the analysis results should be sent.

        :param connect: (experimental) Coverity Connect configuration to use when committing defects to Coverity Connect.
        :param local: (experimental) Local configuration to use when saving defects to the local file system.
        :param srm: (experimental) Software Risk Manager configuration to use when storing defects in Software Risk Manager.

        :stability: experimental
        :schema: commit-configuration
        '''
        if isinstance(connect, dict):
            connect = CommitConfigurationConnect(**connect)
        if isinstance(local, dict):
            local = CommitConfigurationLocal(**local)
        if isinstance(srm, dict):
            srm = CommitConfigurationSrm(**srm)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__29574609a2ede742a8d684fbf27d054f7005af44af80d1a5533394d600d082bc)
            check_type(argname="argument connect", value=connect, expected_type=type_hints["connect"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument srm", value=srm, expected_type=type_hints["srm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connect is not None:
            self._values["connect"] = connect
        if local is not None:
            self._values["local"] = local
        if srm is not None:
            self._values["srm"] = srm

    @builtins.property
    def connect(self) -> typing.Optional["CommitConfigurationConnect"]:
        '''(experimental) Coverity Connect configuration to use when committing defects to Coverity Connect.

        :stability: experimental
        :schema: commit-configuration#connect
        '''
        result = self._values.get("connect")
        return typing.cast(typing.Optional["CommitConfigurationConnect"], result)

    @builtins.property
    def local(self) -> typing.Optional["CommitConfigurationLocal"]:
        '''(experimental) Local configuration to use when saving defects to the local file system.

        :stability: experimental
        :schema: commit-configuration#local
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional["CommitConfigurationLocal"], result)

    @builtins.property
    def srm(self) -> typing.Optional["CommitConfigurationSrm"]:
        '''(experimental) Software Risk Manager configuration to use when storing defects in Software Risk Manager.

        :stability: experimental
        :schema: commit-configuration#srm
        '''
        result = self._values.get("srm")
        return typing.cast(typing.Optional["CommitConfigurationSrm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommitConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CommitConfigurationConnect",
    jsii_struct_bases=[],
    name_mapping={
        "stream": "stream",
        "url": "url",
        "auth_key_file": "authKeyFile",
        "ca_certs_file": "caCertsFile",
        "comparison_only": "comparisonOnly",
        "comparison_report": "comparisonReport",
        "cov_commit_defects_args": "covCommitDefectsArgs",
        "description": "description",
        "on_new_cert": "onNewCert",
        "project": "project",
        "proxy_client_cert_file": "proxyClientCertFile",
        "proxy_client_key_file": "proxyClientKeyFile",
        "proxy_url": "proxyUrl",
        "scm": "scm",
        "snapshot": "snapshot",
        "triage": "triage",
        "upload_artifacts": "uploadArtifacts",
        "version": "version",
    },
)
class CommitConfigurationConnect:
    def __init__(
        self,
        *,
        stream: builtins.str,
        url: builtins.str,
        auth_key_file: typing.Optional[builtins.str] = None,
        ca_certs_file: typing.Optional[builtins.str] = None,
        comparison_only: typing.Optional[builtins.bool] = None,
        comparison_report: typing.Optional[builtins.str] = None,
        cov_commit_defects_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        on_new_cert: typing.Optional["CommitConfigurationConnectOnNewCert"] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_client_cert_file: typing.Optional[builtins.str] = None,
        proxy_client_key_file: typing.Optional[builtins.str] = None,
        proxy_url: typing.Optional[builtins.str] = None,
        scm: typing.Optional["CommitConfigurationConnectScm"] = None,
        snapshot: typing.Optional[typing.Union["SnapshotConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        triage: typing.Optional[typing.Union["CommitConfigurationConnectTriage", typing.Dict[builtins.str, typing.Any]]] = None,
        upload_artifacts: typing.Optional["CommitConfigurationConnectUploadArtifacts"] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Coverity Connect configuration to use when committing defects to Coverity Connect.

        :param stream: (experimental) The name of the stream to commit the results to.
        :param url: (experimental) Absolute URL of where to commit the Coverity Connect results.
        :param auth_key_file: (experimental) The authentication key file to use when authenticating to Coverity Connect to commit defects. By default, the file located at $HOME/.coverity/ak-- is used.
        :param ca_certs_file: (experimental) File containing additional certificates to trust in addition to the ones in the system certificate store and the Coverity TFT store. By default system CA certificates are used.
        :param comparison_only: (experimental) If true, analysis results will not be committed to Coverity Connect. Instead, results compared to a reference snapshot may be saved locally as specified by the "commit.local" settings.
        :param comparison_report: (experimental) Output file to which analysis results should be written instead of being committed to Coverity Connect. The output includes a comparison against the latest snapshot for the specified stream.
        :param cov_commit_defects_args: (experimental) Additional arguments to pass to "cov-commit-defects" during the commit phase.
        :param description: (experimental) A description for the committed snapshot.
        :param on_new_cert: (experimental) Indicates whether to trust self-signed certificates presented by Coverity Connect that are not currently trusted.
        :param project: (experimental) The name of the project to use when creating a new stream. Ignored when stream creation is not needed. By default the stream name is used.
        :param proxy_client_cert_file: (experimental) File containing the client certificate in PEM format, that should be presented to the proxy when making a request.
        :param proxy_client_key_file: (experimental) File containing the client certificate private key in PEM format, for the proxy-client-cert-file.
        :param proxy_url: (experimental) URL for a forward proxy to use when communicating with Coverity Connect. Must be an https URL.
        :param scm: (experimental) The name of the source control management system.
        :param snapshot: (experimental) Specifies how to select a reference snapshot to use for a comparison report.
        :param triage: (experimental) Specifies how new defects should be handled.
        :param upload_artifacts: (experimental) Artifacts to upload following analysis when the analysis location is Connect.
        :param version: (experimental) A project version for the committed snapshot.

        :stability: experimental
        :schema: CommitConfigurationConnect
        '''
        if isinstance(snapshot, dict):
            snapshot = SnapshotConfiguration(**snapshot)
        if isinstance(triage, dict):
            triage = CommitConfigurationConnectTriage(**triage)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ed61ca990a2803b1dc8f189dde3a89fbb0438fa571a9d4245ff52892ab62713f)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument auth_key_file", value=auth_key_file, expected_type=type_hints["auth_key_file"])
            check_type(argname="argument ca_certs_file", value=ca_certs_file, expected_type=type_hints["ca_certs_file"])
            check_type(argname="argument comparison_only", value=comparison_only, expected_type=type_hints["comparison_only"])
            check_type(argname="argument comparison_report", value=comparison_report, expected_type=type_hints["comparison_report"])
            check_type(argname="argument cov_commit_defects_args", value=cov_commit_defects_args, expected_type=type_hints["cov_commit_defects_args"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument on_new_cert", value=on_new_cert, expected_type=type_hints["on_new_cert"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument proxy_client_cert_file", value=proxy_client_cert_file, expected_type=type_hints["proxy_client_cert_file"])
            check_type(argname="argument proxy_client_key_file", value=proxy_client_key_file, expected_type=type_hints["proxy_client_key_file"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument triage", value=triage, expected_type=type_hints["triage"])
            check_type(argname="argument upload_artifacts", value=upload_artifacts, expected_type=type_hints["upload_artifacts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stream": stream,
            "url": url,
        }
        if auth_key_file is not None:
            self._values["auth_key_file"] = auth_key_file
        if ca_certs_file is not None:
            self._values["ca_certs_file"] = ca_certs_file
        if comparison_only is not None:
            self._values["comparison_only"] = comparison_only
        if comparison_report is not None:
            self._values["comparison_report"] = comparison_report
        if cov_commit_defects_args is not None:
            self._values["cov_commit_defects_args"] = cov_commit_defects_args
        if description is not None:
            self._values["description"] = description
        if on_new_cert is not None:
            self._values["on_new_cert"] = on_new_cert
        if project is not None:
            self._values["project"] = project
        if proxy_client_cert_file is not None:
            self._values["proxy_client_cert_file"] = proxy_client_cert_file
        if proxy_client_key_file is not None:
            self._values["proxy_client_key_file"] = proxy_client_key_file
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url
        if scm is not None:
            self._values["scm"] = scm
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if triage is not None:
            self._values["triage"] = triage
        if upload_artifacts is not None:
            self._values["upload_artifacts"] = upload_artifacts
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def stream(self) -> builtins.str:
        '''(experimental) The name of the stream to commit the results to.

        :stability: experimental
        :schema: CommitConfigurationConnect#stream
        '''
        result = self._values.get("stream")
        assert result is not None, "Required property 'stream' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) Absolute URL of where to commit the Coverity Connect results.

        :stability: experimental
        :schema: CommitConfigurationConnect#url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_key_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authentication key file to use when authenticating to Coverity Connect to commit defects.

        By default, the file located at $HOME/.coverity/ak-- is used.

        :stability: experimental
        :schema: CommitConfigurationConnect#auth-key-file
        '''
        result = self._values.get("auth_key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certs_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing additional certificates to trust in addition to the ones in the system certificate store and the Coverity TFT store.

        By default system CA certificates are used.

        :stability: experimental
        :schema: CommitConfigurationConnect#ca-certs-file
        '''
        result = self._values.get("ca_certs_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comparison_only(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, analysis results will not be committed to Coverity Connect.

        Instead, results compared to a reference snapshot may be saved locally as specified by the "commit.local" settings.

        :stability: experimental
        :schema: CommitConfigurationConnect#comparison-only
        '''
        result = self._values.get("comparison_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def comparison_report(self) -> typing.Optional[builtins.str]:
        '''(experimental) Output file to which analysis results should be written instead of being committed to Coverity Connect.

        The output includes a comparison against the latest snapshot for the specified stream.

        :stability: experimental
        :schema: CommitConfigurationConnect#comparison-report
        '''
        result = self._values.get("comparison_report")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cov_commit_defects_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional arguments to pass to "cov-commit-defects" during the commit phase.

        :stability: experimental
        :schema: CommitConfigurationConnect#cov-commit-defects-args
        '''
        result = self._values.get("cov_commit_defects_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the committed snapshot.

        :stability: experimental
        :schema: CommitConfigurationConnect#description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_new_cert(self) -> typing.Optional["CommitConfigurationConnectOnNewCert"]:
        '''(experimental) Indicates whether to trust self-signed certificates presented by Coverity Connect that are not currently trusted.

        :stability: experimental
        :schema: CommitConfigurationConnect#on-new-cert
        '''
        result = self._values.get("on_new_cert")
        return typing.cast(typing.Optional["CommitConfigurationConnectOnNewCert"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the project to use when creating a new stream.

        Ignored when stream creation is not needed. By default the stream name is used.

        :stability: experimental
        :schema: CommitConfigurationConnect#project
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_client_cert_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the client certificate in PEM format, that should be presented to the proxy when making a request.

        :stability: experimental
        :schema: CommitConfigurationConnect#proxy-client-cert-file
        '''
        result = self._values.get("proxy_client_cert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_client_key_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the client certificate private key in PEM format, for the proxy-client-cert-file.

        :stability: experimental
        :schema: CommitConfigurationConnect#proxy-client-key-file
        '''
        result = self._values.get("proxy_client_key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL for a forward proxy to use when communicating with Coverity Connect.

        Must be an https URL.

        :stability: experimental
        :schema: CommitConfigurationConnect#proxy-url
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scm(self) -> typing.Optional["CommitConfigurationConnectScm"]:
        '''(experimental) The name of the source control management system.

        :stability: experimental
        :schema: CommitConfigurationConnect#scm
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional["CommitConfigurationConnectScm"], result)

    @builtins.property
    def snapshot(self) -> typing.Optional["SnapshotConfiguration"]:
        '''(experimental) Specifies how to select a reference snapshot to use for a comparison report.

        :stability: experimental
        :schema: CommitConfigurationConnect#snapshot
        '''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional["SnapshotConfiguration"], result)

    @builtins.property
    def triage(self) -> typing.Optional["CommitConfigurationConnectTriage"]:
        '''(experimental) Specifies how new defects should be handled.

        :stability: experimental
        :schema: CommitConfigurationConnect#triage
        '''
        result = self._values.get("triage")
        return typing.cast(typing.Optional["CommitConfigurationConnectTriage"], result)

    @builtins.property
    def upload_artifacts(
        self,
    ) -> typing.Optional["CommitConfigurationConnectUploadArtifacts"]:
        '''(experimental) Artifacts to upload following analysis when the analysis location is Connect.

        :stability: experimental
        :schema: CommitConfigurationConnect#upload-artifacts
        '''
        result = self._values.get("upload_artifacts")
        return typing.cast(typing.Optional["CommitConfigurationConnectUploadArtifacts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) A project version for the committed snapshot.

        :stability: experimental
        :schema: CommitConfigurationConnect#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommitConfigurationConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.CommitConfigurationConnectOnNewCert")
class CommitConfigurationConnectOnNewCert(enum.Enum):
    '''(experimental) Indicates whether to trust self-signed certificates presented by Coverity Connect that are not currently trusted.

    :stability: experimental
    :schema: CommitConfigurationConnectOnNewCert
    '''

    TRUST = "TRUST"
    '''(experimental) trust.

    :stability: experimental
    '''
    DISTRUST = "DISTRUST"
    '''(experimental) distrust.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.polaris.CommitConfigurationConnectScm")
class CommitConfigurationConnectScm(enum.Enum):
    '''(experimental) The name of the source control management system.

    :stability: experimental
    :schema: CommitConfigurationConnectScm
    '''

    ADS = "ADS"
    '''(experimental) ads.

    :stability: experimental
    '''
    CLEARCASE = "CLEARCASE"
    '''(experimental) clearcase.

    :stability: experimental
    '''
    CVS = "CVS"
    '''(experimental) cvs.

    :stability: experimental
    '''
    GIT = "GIT"
    '''(experimental) git.

    :stability: experimental
    '''
    HG = "HG"
    '''(experimental) hg.

    :stability: experimental
    '''
    PERFORCE = "PERFORCE"
    '''(experimental) perforce.

    :stability: experimental
    '''
    PLASTIC = "PLASTIC"
    '''(experimental) plastic.

    :stability: experimental
    '''
    PLASTIC_HYPHEN_DISTRIBUTED = "PLASTIC_HYPHEN_DISTRIBUTED"
    '''(experimental) plastic-distributed.

    :stability: experimental
    '''
    SVN = "SVN"
    '''(experimental) svn.

    :stability: experimental
    '''
    TFS = "TFS"
    '''(experimental) tfs.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.CommitConfigurationConnectTriage",
    jsii_struct_bases=[],
    name_mapping={
        "new_defect_owner": "newDefectOwner",
        "new_defect_owner_limit": "newDefectOwnerLimit",
        "set_new_defect_owner": "setNewDefectOwner",
    },
)
class CommitConfigurationConnectTriage:
    def __init__(
        self,
        *,
        new_defect_owner: typing.Optional[builtins.str] = None,
        new_defect_owner_limit: typing.Optional[jsii.Number] = None,
        set_new_defect_owner: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Specifies how new defects should be handled.

        :param new_defect_owner: (experimental) User to whom any new defects will be assigned. The specified user must already exist in the Coverity Connect database. The default is the current user.
        :param new_defect_owner_limit: (experimental) Limit on the number of defects to assign to the specified user. If the number of discovered defects is more than the limit, then no assignment is done.
        :param set_new_defect_owner: (experimental) If true, the owner for newly detected defects that exist locally is set to the specified user.

        :stability: experimental
        :schema: CommitConfigurationConnectTriage
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0ca8942001713bf2b024f8c7d8f36592448f130bf302c4a48be012f6e42f1c6f)
            check_type(argname="argument new_defect_owner", value=new_defect_owner, expected_type=type_hints["new_defect_owner"])
            check_type(argname="argument new_defect_owner_limit", value=new_defect_owner_limit, expected_type=type_hints["new_defect_owner_limit"])
            check_type(argname="argument set_new_defect_owner", value=set_new_defect_owner, expected_type=type_hints["set_new_defect_owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if new_defect_owner is not None:
            self._values["new_defect_owner"] = new_defect_owner
        if new_defect_owner_limit is not None:
            self._values["new_defect_owner_limit"] = new_defect_owner_limit
        if set_new_defect_owner is not None:
            self._values["set_new_defect_owner"] = set_new_defect_owner

    @builtins.property
    def new_defect_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) User to whom any new defects will be assigned.

        The specified user must already exist in the Coverity Connect database. The default is the current user.

        :stability: experimental
        :schema: CommitConfigurationConnectTriage#new-defect-owner
        '''
        result = self._values.get("new_defect_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def new_defect_owner_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Limit on the number of defects to assign to the specified user.

        If the number of discovered defects is more than the limit, then no assignment is done.

        :stability: experimental
        :schema: CommitConfigurationConnectTriage#new-defect-owner-limit
        '''
        result = self._values.get("new_defect_owner_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def set_new_defect_owner(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, the owner for newly detected defects that exist locally is set to the specified user.

        :stability: experimental
        :schema: CommitConfigurationConnectTriage#set-new-defect-owner
        '''
        result = self._values.get("set_new_defect_owner")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommitConfigurationConnectTriage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.CommitConfigurationConnectUploadArtifacts")
class CommitConfigurationConnectUploadArtifacts(enum.Enum):
    '''(experimental) Artifacts to upload following analysis when the analysis location is Connect.

    :stability: experimental
    :schema: CommitConfigurationConnectUploadArtifacts
    '''

    ALL = "ALL"
    '''(experimental) All.

    :stability: experimental
    '''
    LOGS_ONLY = "LOGS_ONLY"
    '''(experimental) LogsOnly.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) None.

    :stability: experimental
    '''
    ON_FAILURE = "ON_FAILURE"
    '''(experimental) OnFailure.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.CommitConfigurationLocal",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "format": "format"},
)
class CommitConfigurationLocal:
    def __init__(
        self,
        *,
        path: builtins.str,
        format: typing.Optional["CommitConfigurationLocalFormat"] = None,
    ) -> None:
        '''(experimental) Local configuration to use when saving defects to the local file system.

        :param path: (experimental) Directory (for "html" format) or file (for "json" format) in which to save defects.
        :param format: (experimental) Format in which to save defects. Either "html" or "json".

        :stability: experimental
        :schema: CommitConfigurationLocal
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__441cf9fe31389f57447c8fff4013df705305b2ff8a2dec14ec84bfdea342d10f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if format is not None:
            self._values["format"] = format

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Directory (for "html" format) or file (for "json" format) in which to save defects.

        :stability: experimental
        :schema: CommitConfigurationLocal#path
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> typing.Optional["CommitConfigurationLocalFormat"]:
        '''(experimental) Format in which to save defects.

        Either "html" or "json".

        :stability: experimental
        :schema: CommitConfigurationLocal#format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional["CommitConfigurationLocalFormat"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommitConfigurationLocal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.CommitConfigurationLocalFormat")
class CommitConfigurationLocalFormat(enum.Enum):
    '''(experimental) Format in which to save defects.

    Either "html" or "json".

    :stability: experimental
    :schema: CommitConfigurationLocalFormat
    '''

    HTML = "HTML"
    '''(experimental) html.

    :stability: experimental
    '''
    JSON = "JSON"
    '''(experimental) json.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.CommitConfigurationSrm",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "branch": "branch",
        "parent_branch": "parentBranch",
        "project_id": "projectId",
        "project_name": "projectName",
        "token_file": "tokenFile",
    },
)
class CommitConfigurationSrm:
    def __init__(
        self,
        *,
        url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        parent_branch: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[jsii.Number] = None,
        project_name: typing.Optional[builtins.str] = None,
        token_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Software Risk Manager configuration to use when storing defects in Software Risk Manager.

        :param url: (experimental) The URL of the Software Risk Manager to use for the analysis (if doing a remote analysis) and the analysis results.
        :param branch: (experimental) The name of the branch to associate the analysis results with in Software Risk Manager.
        :param parent_branch: (experimental) The name of the parent branch of the actual branch.
        :param project_id: (experimental) The ID of the project to associate the analysis results with in Software Risk Manager.
        :param project_name: (experimental) The name of the project to associate the analysis results with in Software Risk Manager.
        :param token_file: (experimental) The name of the file to read the Software Risk Manager API key from. By default, the file located at $HOME/.bridge/srm-token.txt is used.

        :stability: experimental
        :schema: CommitConfigurationSrm
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7719cef67abaafefdfae79698844a772a5114f09ff2e8da55d3c796e31a50958)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument parent_branch", value=parent_branch, expected_type=type_hints["parent_branch"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument token_file", value=token_file, expected_type=type_hints["token_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if branch is not None:
            self._values["branch"] = branch
        if parent_branch is not None:
            self._values["parent_branch"] = parent_branch
        if project_id is not None:
            self._values["project_id"] = project_id
        if project_name is not None:
            self._values["project_name"] = project_name
        if token_file is not None:
            self._values["token_file"] = token_file

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The URL of the Software Risk Manager to use for the analysis (if doing a remote analysis) and the analysis results.

        :stability: experimental
        :schema: CommitConfigurationSrm#url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch to associate the analysis results with in Software Risk Manager.

        :stability: experimental
        :schema: CommitConfigurationSrm#branch
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the parent branch of the actual branch.

        :stability: experimental
        :schema: CommitConfigurationSrm#parent-branch
        '''
        result = self._values.get("parent_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The ID of the project to associate the analysis results with in Software Risk Manager.

        :stability: experimental
        :schema: CommitConfigurationSrm#project-id
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the project to associate the analysis results with in Software Risk Manager.

        :stability: experimental
        :schema: CommitConfigurationSrm#project-name
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the file to read the Software Risk Manager API key from.

        By default, the file located at $HOME/.bridge/srm-token.txt is used.

        :stability: experimental
        :schema: CommitConfigurationSrm#token-file
        '''
        result = self._values.get("token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommitConfigurationSrm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CompilerConfiguration",
    jsii_struct_bases=[],
    name_mapping={"cov_configure": "covConfigure", "file": "file"},
)
class CompilerConfiguration:
    def __init__(
        self,
        *,
        cov_configure: typing.Optional[typing.Sequence[typing.Sequence[builtins.str]]] = None,
        file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cov_configure: (experimental) Specifies a list of arguments to pass to "cov-configure" to generate the compiler configuration to use during capture. This key is mutually exclusive with the "file" key.
        :param file: (experimental) Specifies a pre-generated compiler configuration file to use. This key is mutually exclusive with the "cov-configure" key.

        :stability: experimental
        :schema: compiler-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2a94af515c2d1f0d4abeac655dd05070f012477b1be355b386870709ac204356)
            check_type(argname="argument cov_configure", value=cov_configure, expected_type=type_hints["cov_configure"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cov_configure is not None:
            self._values["cov_configure"] = cov_configure
        if file is not None:
            self._values["file"] = file

    @builtins.property
    def cov_configure(self) -> typing.Optional[typing.List[typing.List[builtins.str]]]:
        '''(experimental) Specifies a list of arguments to pass to "cov-configure" to generate the compiler configuration to use during capture.

        This key is mutually exclusive with the "file" key.

        :stability: experimental
        :schema: compiler-configuration#cov-configure
        '''
        result = self._values.get("cov_configure")
        return typing.cast(typing.Optional[typing.List[typing.List[builtins.str]]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies a pre-generated compiler configuration file to use.

        This key is mutually exclusive with the "cov-configure" key.

        :stability: experimental
        :schema: compiler-configuration#file
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompilerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.CovTranslateConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "cov_build_args": "covBuildArgs",
        "defer_decomp": "deferDecomp",
        "parallel_translate": "parallelTranslate",
        "scan_transparency": "scanTransparency",
    },
)
class CovTranslateConfiguration:
    def __init__(
        self,
        *,
        command: builtins.str,
        cov_build_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        defer_decomp: typing.Optional[builtins.bool] = None,
        parallel_translate: typing.Optional[typing.Union["ParallelTranslateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        scan_transparency: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Command to invoke that will invoke "cov-translate" to capture the project.

        :param command: (experimental) This key specifies a command to invoke that will invoke "cov-translate" in the case where the user is doing a "cov-translate" capture.
        :param cov_build_args: (experimental) Additional arguments to pass to cov-build when invoking the provided command.
        :param defer_decomp: (experimental) Specifies whether the build should only record the decompilations of byte code during the build and not attempt to decompile and emit the byte code. During the analysis phase, cov-build will be rerun with --replay-decomp to decompile and emit the byte code.
        :param parallel_translate: (experimental) Specifies how to parallelize translation of C and C++ code.
        :param scan_transparency: (experimental) Specifies whether to enable the collection of scan transparency data for cov-translate capture. This setting must be enabled if the Coverity Connect instance has 'scan.transparency.enabled=true' in its configuration.

        :stability: experimental
        :schema: cov-translate-configuration
        '''
        if isinstance(parallel_translate, dict):
            parallel_translate = ParallelTranslateConfiguration(**parallel_translate)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0fc20d36229af30b2db04b009de30659d54e39db473f44cd58d65ee8a14d1be9)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cov_build_args", value=cov_build_args, expected_type=type_hints["cov_build_args"])
            check_type(argname="argument defer_decomp", value=defer_decomp, expected_type=type_hints["defer_decomp"])
            check_type(argname="argument parallel_translate", value=parallel_translate, expected_type=type_hints["parallel_translate"])
            check_type(argname="argument scan_transparency", value=scan_transparency, expected_type=type_hints["scan_transparency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command": command,
        }
        if cov_build_args is not None:
            self._values["cov_build_args"] = cov_build_args
        if defer_decomp is not None:
            self._values["defer_decomp"] = defer_decomp
        if parallel_translate is not None:
            self._values["parallel_translate"] = parallel_translate
        if scan_transparency is not None:
            self._values["scan_transparency"] = scan_transparency

    @builtins.property
    def command(self) -> builtins.str:
        '''(experimental) This key specifies a command to invoke that will invoke "cov-translate" in the case where the user is doing a "cov-translate" capture.

        :stability: experimental
        :schema: cov-translate-configuration#command
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cov_build_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional arguments to pass to cov-build when invoking the provided command.

        :stability: experimental
        :schema: cov-translate-configuration#cov-build-args
        '''
        result = self._values.get("cov_build_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def defer_decomp(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the build should only record the decompilations of byte code during the build and not attempt to decompile and emit the byte code.

        During the analysis phase, cov-build will be rerun with --replay-decomp to decompile and emit the byte code.

        :stability: experimental
        :schema: cov-translate-configuration#defer-decomp
        '''
        result = self._values.get("defer_decomp")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parallel_translate(self) -> typing.Optional["ParallelTranslateConfiguration"]:
        '''(experimental) Specifies how to parallelize translation of C and C++ code.

        :stability: experimental
        :schema: cov-translate-configuration#parallel-translate
        '''
        result = self._values.get("parallel_translate")
        return typing.cast(typing.Optional["ParallelTranslateConfiguration"], result)

    @builtins.property
    def scan_transparency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable the collection of scan transparency data for cov-translate capture.

        This setting must be enabled if the Coverity Connect instance has 'scan.transparency.enabled=true' in its configuration.

        :stability: experimental
        :schema: cov-translate-configuration#scan-transparency
        '''
        result = self._values.get("scan_transparency")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CovTranslateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.DirectivesConfiguration",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "file": "file"},
)
class DirectivesConfiguration:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["DirectivesConfigurationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: (experimental) Security directives configuration to use during the analysis. This key is mutually exclusive with the "file" key and is specified in the case where the user wants to in-line the security directives configuration in the file.
        :param file: (experimental) File containing security directives to use during the analysis. This key is mutually exclusive with the "config" key.

        :stability: experimental
        :schema: directives-configuration
        '''
        if isinstance(config, dict):
            config = DirectivesConfigurationConfig(**config)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__04394952de531f5747c84a1edc1f57889db3866770b7c415cb58d6f04f072ad1)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if file is not None:
            self._values["file"] = file

    @builtins.property
    def config(self) -> typing.Optional["DirectivesConfigurationConfig"]:
        '''(experimental) Security directives configuration to use during the analysis.

        This key is mutually exclusive with the "file" key and is specified in the case where the user wants to in-line the security directives configuration in the file.

        :stability: experimental
        :schema: directives-configuration#config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["DirectivesConfigurationConfig"], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing security directives to use during the analysis.

        This key is mutually exclusive with the "config" key.

        :stability: experimental
        :schema: directives-configuration#file
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectivesConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.DirectivesConfigurationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "directives": "directives",
        "language": "language",
        "format_version": "formatVersion",
        "type": "type",
    },
)
class DirectivesConfigurationConfig:
    def __init__(
        self,
        *,
        directives: typing.Sequence[typing.Any],
        language: builtins.str,
        format_version: typing.Optional[jsii.Number] = None,
        type: typing.Optional["DirectivesConfigurationConfigType"] = None,
    ) -> None:
        '''(experimental) Security directives configuration to use during the analysis.

        This key is mutually exclusive with the "file" key and is specified in the case where the user wants to in-line the security directives configuration in the file.

        :param directives: (experimental) Specify a particular analysis behavior.
        :param language: (experimental) Language or language family to which directives apply.
        :param format_version: (experimental) Version of the directives format.
        :param type: (experimental) Must be the string "Coverity analysis configuration".

        :stability: experimental
        :schema: DirectivesConfigurationConfig
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fc7a4ee187ba693efb70331c8d4e7e9030f409b205c3261ce10d4ae77a5a689f)
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directives": directives,
            "language": language,
        }
        if format_version is not None:
            self._values["format_version"] = format_version
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def directives(self) -> typing.List[typing.Any]:
        '''(experimental) Specify a particular analysis behavior.

        :stability: experimental
        :schema: DirectivesConfigurationConfig#directives
        '''
        result = self._values.get("directives")
        assert result is not None, "Required property 'directives' is missing"
        return typing.cast(typing.List[typing.Any], result)

    @builtins.property
    def language(self) -> builtins.str:
        '''(experimental) Language or language family to which directives apply.

        :stability: experimental
        :schema: DirectivesConfigurationConfig#language
        '''
        result = self._values.get("language")
        assert result is not None, "Required property 'language' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Version of the directives format.

        :stability: experimental
        :schema: DirectivesConfigurationConfig#format_version
        '''
        result = self._values.get("format_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional["DirectivesConfigurationConfigType"]:
        '''(experimental) Must be the string "Coverity analysis configuration".

        :stability: experimental
        :schema: DirectivesConfigurationConfig#type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["DirectivesConfigurationConfigType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectivesConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.DirectivesConfigurationConfigType")
class DirectivesConfigurationConfigType(enum.Enum):
    '''(experimental) Must be the string "Coverity analysis configuration".

    :stability: experimental
    :schema: DirectivesConfigurationConfigType
    '''

    COVERITY_ANALYSIS_CONFIGURATION = "COVERITY_ANALYSIS_CONFIGURATION"
    '''(experimental) Coverity analysis configuration.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.FilesConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "emit_minified_js": "emitMinifiedJs",
        "exclude_glob": "excludeGlob",
        "exclude_regex": "excludeRegex",
        "include_dirs": "includeDirs",
        "include_glob": "includeGlob",
        "include_list_file": "includeListFile",
        "include_regex": "includeRegex",
        "java_version": "javaVersion",
        "library_dirs": "libraryDirs",
        "library_files": "libraryFiles",
        "webapp_archives": "webappArchives",
    },
)
class FilesConfiguration:
    def __init__(
        self,
        *,
        emit_minified_js: typing.Optional[builtins.bool] = None,
        exclude_glob: typing.Optional[builtins.str] = None,
        exclude_regex: typing.Optional[builtins.str] = None,
        include_dirs: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_glob: typing.Optional[builtins.str] = None,
        include_list_file: typing.Optional[builtins.str] = None,
        include_regex: typing.Optional[builtins.str] = None,
        java_version: typing.Optional[builtins.str] = None,
        library_dirs: typing.Optional[typing.Sequence[builtins.str]] = None,
        library_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        webapp_archives: typing.Optional[typing.Sequence[typing.Union["WebappArchiveConfiguration", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param emit_minified_js: (experimental) Specifies whether to enable capture of minified JavaScript files.
        :param exclude_glob: (experimental) Glob pattern that specifies the set of source files to exclude from capture. Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.
        :param exclude_regex: (experimental) Regular expression that specifies the set of source files to exclude from capture. Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.
        :param include_dirs: (experimental) List of directory basenames to include for capture, which would normally have been excluded. By default, directories named "vendor" or "node_modules" are excluded, as are directories whose names begin with "."
        :param include_glob: (experimental) Glob pattern that specifies the set of source files to capture.
        :param include_list_file: (experimental) File containing the paths of source files to capture, one per line. Include and exclude glob patterns and regular expressions are applied to determine which of these files are actually captured.
        :param include_regex: (experimental) Regular expression that specifies the set of source files to capture.
        :param java_version: (experimental) Specifies the Java version to use when parsing and emitting Java source files with buildless capture.
        :param library_dirs: (experimental) List of directories to look in for dependencies to use during capture.
        :param library_files: (experimental) List of file dependencies to use during capture.
        :param webapp_archives: (experimental) Specifies information about which web-application archives should be captured. By default all webapp archives are captured.

        :stability: experimental
        :schema: files-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9e21a938b0cd3f7f78413617cac3b659e5e592f27b0b1b359dbec52aa1065c4a)
            check_type(argname="argument emit_minified_js", value=emit_minified_js, expected_type=type_hints["emit_minified_js"])
            check_type(argname="argument exclude_glob", value=exclude_glob, expected_type=type_hints["exclude_glob"])
            check_type(argname="argument exclude_regex", value=exclude_regex, expected_type=type_hints["exclude_regex"])
            check_type(argname="argument include_dirs", value=include_dirs, expected_type=type_hints["include_dirs"])
            check_type(argname="argument include_glob", value=include_glob, expected_type=type_hints["include_glob"])
            check_type(argname="argument include_list_file", value=include_list_file, expected_type=type_hints["include_list_file"])
            check_type(argname="argument include_regex", value=include_regex, expected_type=type_hints["include_regex"])
            check_type(argname="argument java_version", value=java_version, expected_type=type_hints["java_version"])
            check_type(argname="argument library_dirs", value=library_dirs, expected_type=type_hints["library_dirs"])
            check_type(argname="argument library_files", value=library_files, expected_type=type_hints["library_files"])
            check_type(argname="argument webapp_archives", value=webapp_archives, expected_type=type_hints["webapp_archives"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emit_minified_js is not None:
            self._values["emit_minified_js"] = emit_minified_js
        if exclude_glob is not None:
            self._values["exclude_glob"] = exclude_glob
        if exclude_regex is not None:
            self._values["exclude_regex"] = exclude_regex
        if include_dirs is not None:
            self._values["include_dirs"] = include_dirs
        if include_glob is not None:
            self._values["include_glob"] = include_glob
        if include_list_file is not None:
            self._values["include_list_file"] = include_list_file
        if include_regex is not None:
            self._values["include_regex"] = include_regex
        if java_version is not None:
            self._values["java_version"] = java_version
        if library_dirs is not None:
            self._values["library_dirs"] = library_dirs
        if library_files is not None:
            self._values["library_files"] = library_files
        if webapp_archives is not None:
            self._values["webapp_archives"] = webapp_archives

    @builtins.property
    def emit_minified_js(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable capture of minified JavaScript files.

        :stability: experimental
        :schema: files-configuration#emit-minified-js
        '''
        result = self._values.get("emit_minified_js")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclude_glob(self) -> typing.Optional[builtins.str]:
        '''(experimental) Glob pattern that specifies the set of source files to exclude from capture.

        Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.

        :stability: experimental
        :schema: files-configuration#exclude-glob
        '''
        result = self._values.get("exclude_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression that specifies the set of source files to exclude from capture.

        Note that any include glob patterns and regular expressions are processed prior to handling exclude glob patterns and regular expressions.

        :stability: experimental
        :schema: files-configuration#exclude-regex
        '''
        result = self._values.get("exclude_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_dirs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of directory basenames to include for capture, which would normally have been excluded.

        By default, directories named "vendor" or "node_modules" are excluded, as are directories whose names begin with "."

        :stability: experimental
        :schema: files-configuration#include-dirs
        '''
        result = self._values.get("include_dirs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_glob(self) -> typing.Optional[builtins.str]:
        '''(experimental) Glob pattern that specifies the set of source files to capture.

        :stability: experimental
        :schema: files-configuration#include-glob
        '''
        result = self._values.get("include_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_list_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the paths of source files to capture, one per line.

        Include and exclude glob patterns and regular expressions are applied to determine which of these files are actually captured.

        :stability: experimental
        :schema: files-configuration#include-list-file
        '''
        result = self._values.get("include_list_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression that specifies the set of source files to capture.

        :stability: experimental
        :schema: files-configuration#include-regex
        '''
        result = self._values.get("include_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the Java version to use when parsing and emitting Java source files with buildless capture.

        :stability: experimental
        :schema: files-configuration#java-version
        '''
        result = self._values.get("java_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def library_dirs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of directories to look in for dependencies to use during capture.

        :stability: experimental
        :schema: files-configuration#library-dirs
        '''
        result = self._values.get("library_dirs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def library_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of file dependencies to use during capture.

        :stability: experimental
        :schema: files-configuration#library-files
        '''
        result = self._values.get("library_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def webapp_archives(
        self,
    ) -> typing.Optional[typing.List["WebappArchiveConfiguration"]]:
        '''(experimental) Specifies information about which web-application archives should be captured.

        By default all webapp archives are captured.

        :stability: experimental
        :schema: files-configuration#webapp-archives
        '''
        result = self._values.get("webapp_archives")
        return typing.cast(typing.Optional[typing.List["WebappArchiveConfiguration"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilesConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.ImportScmConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cov_import_scm_args": "covImportScmArgs",
        "filename_regex": "filenameRegex",
        "ms_delay": "msDelay",
        "scm": "scm",
    },
)
class ImportScmConfiguration:
    def __init__(
        self,
        *,
        cov_import_scm_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        filename_regex: typing.Optional[builtins.str] = None,
        ms_delay: typing.Optional[jsii.Number] = None,
        scm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cov_import_scm_args: (experimental) Additional arguments to pass to cov-import-scm following capture.
        :param filename_regex: (experimental) Regular expression that specifies the set of files for which to import change information.
        :param ms_delay: (experimental) Delay in milliseconds between calls to the underlying SCM.
        :param scm: (experimental) The name of the source control management system.

        :stability: experimental
        :schema: import-scm-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5555fb5552ef0b1d1251be5a69c8c4999e25d70fc0ae2dfe513d0ffc56a08a0c)
            check_type(argname="argument cov_import_scm_args", value=cov_import_scm_args, expected_type=type_hints["cov_import_scm_args"])
            check_type(argname="argument filename_regex", value=filename_regex, expected_type=type_hints["filename_regex"])
            check_type(argname="argument ms_delay", value=ms_delay, expected_type=type_hints["ms_delay"])
            check_type(argname="argument scm", value=scm, expected_type=type_hints["scm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cov_import_scm_args is not None:
            self._values["cov_import_scm_args"] = cov_import_scm_args
        if filename_regex is not None:
            self._values["filename_regex"] = filename_regex
        if ms_delay is not None:
            self._values["ms_delay"] = ms_delay
        if scm is not None:
            self._values["scm"] = scm

    @builtins.property
    def cov_import_scm_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional arguments to pass to cov-import-scm following capture.

        :stability: experimental
        :schema: import-scm-configuration#cov-import-scm-args
        '''
        result = self._values.get("cov_import_scm_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def filename_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression that specifies the set of files for which to import change information.

        :stability: experimental
        :schema: import-scm-configuration#filename-regex
        '''
        result = self._values.get("filename_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ms_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay in milliseconds between calls to the underlying SCM.

        :stability: experimental
        :schema: import-scm-configuration#ms-delay
        '''
        result = self._values.get("ms_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scm(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the source control management system.

        :stability: experimental
        :schema: import-scm-configuration#scm
        '''
        result = self._values.get("scm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImportScmConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.JobsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "auto": "auto",
        "count": "count",
        "max": "max",
        "override_worker_limit": "overrideWorkerLimit",
    },
)
class JobsConfiguration:
    def __init__(
        self,
        *,
        auto: typing.Optional[builtins.bool] = None,
        count: typing.Optional[jsii.Number] = None,
        max: typing.Optional[jsii.Number] = None,
        override_worker_limit: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param auto: (experimental) If true, the number of analysis workers to run in parallel is based on the amount of memory and number of logical processors in the machine. This is the default for a non-Flexnet license. This key is mutually exclusive with the "count" and "max" keys.
        :param count: (experimental) Number of analysis workers to run in parallel. This key is mutually exclusive with the "auto" and "max" keys.
        :param max: (experimental) Maximum number of analysis worker to run in parallel, subject to limits on the amount of memory and number of logical processors in the machine. A value of 8 is the default for a Flexnet license. This key is mutually exclusive with the "auto" and "count" keys.
        :param override_worker_limit: (experimental) Allows the number of analysis workers to exceed the recommended value. This key may only be used with the "count" key.

        :stability: experimental
        :schema: jobs-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d8db274644be63f71290f71e698f60a1d541bd5ff8d1be025629919de82a8dd5)
            check_type(argname="argument auto", value=auto, expected_type=type_hints["auto"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument override_worker_limit", value=override_worker_limit, expected_type=type_hints["override_worker_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto is not None:
            self._values["auto"] = auto
        if count is not None:
            self._values["count"] = count
        if max is not None:
            self._values["max"] = max
        if override_worker_limit is not None:
            self._values["override_worker_limit"] = override_worker_limit

    @builtins.property
    def auto(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, the number of analysis workers to run in parallel is based on the amount of memory and number of logical processors in the machine.

        This is the default for a non-Flexnet license. This key is mutually exclusive with the "count" and "max" keys.

        :stability: experimental
        :schema: jobs-configuration#auto
        '''
        result = self._values.get("auto")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of analysis workers to run in parallel.

        This key is mutually exclusive with the "auto" and "max" keys.

        :stability: experimental
        :schema: jobs-configuration#count
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of analysis worker to run in parallel, subject to limits on the amount of memory and number of logical processors in the machine.

        A value of 8 is the default for a Flexnet license. This key is mutually exclusive with the "auto" and "count" keys.

        :stability: experimental
        :schema: jobs-configuration#max
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def override_worker_limit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows the number of analysis workers to exceed the recommended value.

        This key may only be used with the "count" key.

        :stability: experimental
        :schema: jobs-configuration#override-worker-limit
        '''
        result = self._values.get("override_worker_limit")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.LanguagesConfiguration",
    jsii_struct_bases=[],
    name_mapping={"exclude": "exclude", "include": "include"},
)
class LanguagesConfiguration:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence["LanguagesConfigurationExclude"]] = None,
        include: typing.Optional[typing.Sequence["LanguagesConfigurationInclude"]] = None,
    ) -> None:
        '''
        :param exclude: (experimental) Specifies the languages for which the source code should be excluded in the capture. This key is mutually exclusive with the "include" key.
        :param include: (experimental) Specifies the languages for which the source code should be included in the capture. This key is mutually exclusive with the "exclude" key.

        :stability: experimental
        :schema: languages-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ee84483a641935f1dfe18312eca06dcb545ad1d67e6ae2806221553c2db2fbc7)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List["LanguagesConfigurationExclude"]]:
        '''(experimental) Specifies the languages for which the source code should be excluded in the capture.

        This key is mutually exclusive with the "include" key.

        :stability: experimental
        :schema: languages-configuration#exclude
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List["LanguagesConfigurationExclude"]], result)

    @builtins.property
    def include(self) -> typing.Optional[typing.List["LanguagesConfigurationInclude"]]:
        '''(experimental) Specifies the languages for which the source code should be included in the capture.

        This key is mutually exclusive with the "exclude" key.

        :stability: experimental
        :schema: languages-configuration#include
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List["LanguagesConfigurationInclude"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LanguagesConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.LanguagesConfigurationExclude")
class LanguagesConfigurationExclude(enum.Enum):
    '''
    :stability: experimental
    :schema: LanguagesConfigurationExclude
    '''

    APEX = "APEX"
    '''(experimental) apex.

    :stability: experimental
    '''
    C_HYPHEN_FAMILY = "C_HYPHEN_FAMILY"
    '''(experimental) c-family.

    :stability: experimental
    '''
    CSHARP = "CSHARP"
    '''(experimental) csharp.

    :stability: experimental
    '''
    DART = "DART"
    '''(experimental) dart.

    :stability: experimental
    '''
    GO = "GO"
    '''(experimental) go.

    :stability: experimental
    '''
    JAVA = "JAVA"
    '''(experimental) java.

    :stability: experimental
    '''
    JAVASCRIPT = "JAVASCRIPT"
    '''(experimental) javascript.

    :stability: experimental
    '''
    KOTLIN = "KOTLIN"
    '''(experimental) kotlin.

    :stability: experimental
    '''
    PHP = "PHP"
    '''(experimental) php.

    :stability: experimental
    '''
    PYTHON = "PYTHON"
    '''(experimental) python.

    :stability: experimental
    '''
    RUBY = "RUBY"
    '''(experimental) ruby.

    :stability: experimental
    '''
    SWIFT = "SWIFT"
    '''(experimental) swift.

    :stability: experimental
    '''
    VB = "VB"
    '''(experimental) vb.

    :stability: experimental
    '''
    CONFIGURATION = "CONFIGURATION"
    '''(experimental) configuration.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.polaris.LanguagesConfigurationInclude")
class LanguagesConfigurationInclude(enum.Enum):
    '''
    :stability: experimental
    :schema: LanguagesConfigurationInclude
    '''

    APEX = "APEX"
    '''(experimental) apex.

    :stability: experimental
    '''
    C_HYPHEN_FAMILY = "C_HYPHEN_FAMILY"
    '''(experimental) c-family.

    :stability: experimental
    '''
    CSHARP = "CSHARP"
    '''(experimental) csharp.

    :stability: experimental
    '''
    DART = "DART"
    '''(experimental) dart.

    :stability: experimental
    '''
    GO = "GO"
    '''(experimental) go.

    :stability: experimental
    '''
    JAVA = "JAVA"
    '''(experimental) java.

    :stability: experimental
    '''
    JAVASCRIPT = "JAVASCRIPT"
    '''(experimental) javascript.

    :stability: experimental
    '''
    KOTLIN = "KOTLIN"
    '''(experimental) kotlin.

    :stability: experimental
    '''
    PHP = "PHP"
    '''(experimental) php.

    :stability: experimental
    '''
    PYTHON = "PYTHON"
    '''(experimental) python.

    :stability: experimental
    '''
    RUBY = "RUBY"
    '''(experimental) ruby.

    :stability: experimental
    '''
    SWIFT = "SWIFT"
    '''(experimental) swift.

    :stability: experimental
    '''
    VB = "VB"
    '''(experimental) vb.

    :stability: experimental
    '''
    CONFIGURATION = "CONFIGURATION"
    '''(experimental) configuration.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.ParallelTranslateConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processes": "processes"},
)
class ParallelTranslateConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        processes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: (experimental) Specifies whether cov-translate parallelization should be enabled.
        :param processes: (experimental) Specifies the number of cov-emit processes to be run in parallel by cov-translate when multiple files are seen on a single native compiler invocation. A value of 0 will use the number of logical processors in the machine.

        :stability: experimental
        :schema: parallel-translate-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__53feeef20f3b05f5c93a14a5eef5c7c4946e0110a45c85fc4a4631da319c2f58)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processes", value=processes, expected_type=type_hints["processes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processes is not None:
            self._values["processes"] = processes

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether cov-translate parallelization should be enabled.

        :stability: experimental
        :schema: parallel-translate-configuration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def processes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the number of cov-emit processes to be run in parallel by cov-translate when multiple files are seen on a single native compiler invocation.

        A value of 0 will use the number of logical processors in the machine.

        :stability: experimental
        :schema: parallel-translate-configuration#processes
        '''
        result = self._values.get("processes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParallelTranslateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.ParseWarningsConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ParseWarningsConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param enabled: (experimental) Enables parse warnings, recovery warnings, and semantic warnings that are produced by the cov-build command so that they appear as defects in Coverity Connect. By default, this is disabled if the aggressiveness level is low, and enabled if the aggressiveness level is medium or high.

        :stability: experimental
        :schema: parse-warnings-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2dcbf188f45310736039810da3f534c75ed3411f5ff12d48dc33afa270b3e373)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parse warnings, recovery warnings, and semantic warnings that are produced by the cov-build command so that they appear as defects in Coverity Connect.

        By default, this is disabled if the aggressiveness level is low, and enabled if the aggressiveness level is medium or high.

        :stability: experimental
        :schema: parse-warnings-configuration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParseWarningsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolarisCoverity(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.polaris.PolarisCoverity",
):
    '''(experimental) Manages ``coverity.yml``, the configuration file for Coverity on Polaris (Black Duck's SAST scanning tool).

    :see: https://docs.blackduck.com/r/cov_polaris/latest/coverity-on-polaris/configuration-file-schema.html
    :stability: experimental
    '''

    def __init__(
        self,
        project: "_projen_04054675.Project",
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param project: -
        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ee4c24407e00a34ed4c70234d7e25620c34f55d5e47791d87b198acbededa434)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PolarisCoverityOptions(
            commit=commit,
            analyze=analyze,
            caching=caching,
            capture=capture,
            version=version,
        )

        jsii.create(self.__class__, self, [project, options])

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> "_projen_04054675.YamlFile":
        '''(experimental) The YAML file for the Coverity on Polaris configuration.

        :stability: experimental
        '''
        return typing.cast("_projen_04054675.YamlFile", jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="projen.polaris.PolarisCoveritySchema",
    jsii_struct_bases=[],
    name_mapping={
        "commit": "commit",
        "analyze": "analyze",
        "caching": "caching",
        "capture": "capture",
        "version": "version",
    },
)
class PolarisCoveritySchema:
    def __init__(
        self,
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        :schema: PolarisCoveritySchema
        '''
        if isinstance(commit, dict):
            commit = CommitConfiguration(**commit)
        if isinstance(analyze, dict):
            analyze = AnalysisConfiguration(**analyze)
        if isinstance(caching, dict):
            caching = CachingConfiguration(**caching)
        if isinstance(capture, dict):
            capture = CaptureConfiguration(**capture)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5882a46d0d2414e8d78d86c82171084bcc091f8af0592a2fbf2e9482f42bafdb)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument analyze", value=analyze, expected_type=type_hints["analyze"])
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
        }
        if analyze is not None:
            self._values["analyze"] = analyze
        if caching is not None:
            self._values["caching"] = caching
        if capture is not None:
            self._values["capture"] = capture
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def commit(self) -> "CommitConfiguration":
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#commit
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast("CommitConfiguration", result)

    @builtins.property
    def analyze(self) -> typing.Optional["AnalysisConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#analyze
        '''
        result = self._values.get("analyze")
        return typing.cast(typing.Optional["AnalysisConfiguration"], result)

    @builtins.property
    def caching(self) -> typing.Optional["CachingConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#caching
        '''
        result = self._values.get("caching")
        return typing.cast(typing.Optional["CachingConfiguration"], result)

    @builtins.property
    def capture(self) -> typing.Optional["CaptureConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#capture
        '''
        result = self._values.get("capture")
        return typing.cast(typing.Optional["CaptureConfiguration"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        :schema: PolarisCoveritySchema#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolarisCoveritySchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolarisGoCoverity(
    PolarisCoverity,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.polaris.PolarisGoCoverity",
):
    '''(experimental) A Coverity on Polaris configuration preset for Go projects.

    Provides sensible defaults for Go analysis:

    - ``capture.languages.include`` = ``[go]``
    - ``capture.buildCapture.buildCommand`` = ``go build .``
    - ``capture.compilerConfiguration.covConfigure`` = ``[["--go"]]``
    - ``capture.files.excludeRegex`` excludes ``vendor``, ``bin`` and other
      conventional Go build artifacts

    All defaults can be overridden via options. Nested options (e.g.
    ``capture``) are deep-merged with the defaults, so overriding one nested
    field does not drop the other defaults in that subtree.

    :stability: experimental

    Example::

        new PolarisGoCoverity(project, {
          commit: {},
        });
    '''

    def __init__(
        self,
        project: "_projen_04054675.Project",
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param project: -
        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0acc879fddf1b7a5f1d4f7ee74c841099f637cf40a5656f85fa56adcf1ed57f3)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PolarisCoverityGoOptions(
            commit=commit,
            analyze=analyze,
            caching=caching,
            capture=capture,
            version=version,
        )

        jsii.create(self.__class__, self, [project, options])


class PolarisJavaCoverity(
    PolarisCoverity,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.polaris.PolarisJavaCoverity",
):
    '''(experimental) A Coverity on Polaris configuration preset for Java projects.

    Provides sensible defaults for Java analysis:

    - ``capture.languages.include`` = ``[java]``
    - ``capture.buildCapture.buildCommand`` = ``mvn package``
    - ``capture.buildCapture.cleanCommand`` = ``mvn clean``
    - ``capture.compilerConfiguration.covConfigure`` = ``[["--java"]]``
    - ``capture.files.excludeRegex`` excludes ``target``, ``dist/java`` and other
      conventional Maven/Gradle build artifacts

    All defaults can be overridden via options. Nested options (e.g.
    ``capture``) are deep-merged with the defaults, so overriding one nested
    field does not drop the other defaults in that subtree.

    :stability: experimental

    Example::

        new PolarisJavaCoverity(project, {
          commit: {},
        });
    '''

    def __init__(
        self,
        project: "_projen_04054675.Project",
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param project: -
        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8839e24f68d014f3a20ab2e7a51a34763a500502d8f6cdcfec178447bc94e1eb)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PolarisCoverityJavaOptions(
            commit=commit,
            analyze=analyze,
            caching=caching,
            capture=capture,
            version=version,
        )

        jsii.create(self.__class__, self, [project, options])


class PolarisJavascriptCoverity(
    PolarisCoverity,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.polaris.PolarisJavascriptCoverity",
):
    '''(experimental) A Coverity on Polaris configuration preset for JavaScript/TypeScript projects.

    Provides sensible defaults for JavaScript/TypeScript analysis:

    - ``capture.languages.include`` = ``[javascript]``
    - ``capture.files.excludeRegex`` excludes ``node_modules``, ``lib``, ``dist``,
      ``coverage`` and other build artifacts, based on the paths projen's
      ``TypeScriptProject`` excludes from git by default

    All defaults can be overridden via options. Nested options (e.g.
    ``capture``) are deep-merged with the defaults, so overriding one nested
    field does not drop the other defaults in that subtree.

    :stability: experimental

    Example::

        new PolarisJavascriptCoverity(project, {
          commit: {},
        });
    '''

    def __init__(
        self,
        project: "_projen_04054675.Project",
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param project: -
        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bf36697ef10b94b77c64a209132aed9ad4344145e79ca8f137be0d16e6cb30a5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PolarisCoverityJavascriptOptions(
            commit=commit,
            analyze=analyze,
            caching=caching,
            capture=capture,
            version=version,
        )

        jsii.create(self.__class__, self, [project, options])


@jsii.data_type(
    jsii_type="projen.polaris.ResolvedCodingStandardConfiguration",
    jsii_struct_bases=[],
    name_mapping={"title": "title", "deviations": "deviations", "version": "version"},
)
class ResolvedCodingStandardConfiguration:
    def __init__(
        self,
        *,
        title: builtins.str,
        deviations: typing.Optional[typing.Sequence[typing.Union["CodingStandardDeviation", typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param title: (experimental) Name of this code compliance configuration.
        :param deviations: (experimental) List of deviations for this standard.
        :param version: (experimental) Version of this code compliance configuration.

        :stability: experimental
        :schema: resolved-coding-standard-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f776076c15568425956f38645c9dab8701fe2f9f2ec7df2bd73c6125bbe76274)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument deviations", value=deviations, expected_type=type_hints["deviations"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "title": title,
        }
        if deviations is not None:
            self._values["deviations"] = deviations
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def title(self) -> builtins.str:
        '''(experimental) Name of this code compliance configuration.

        :stability: experimental
        :schema: resolved-coding-standard-configuration#title
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deviations(self) -> typing.Optional[typing.List["CodingStandardDeviation"]]:
        '''(experimental) List of deviations for this standard.

        :stability: experimental
        :schema: resolved-coding-standard-configuration#deviations
        '''
        result = self._values.get("deviations")
        return typing.cast(typing.Optional[typing.List["CodingStandardDeviation"]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of this code compliance configuration.

        :stability: experimental
        :schema: resolved-coding-standard-configuration#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolvedCodingStandardConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.SigmaConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enable_check_set": "enableCheckSet",
        "malicious_url_patterns_file": "maliciousUrlPatternsFile",
    },
)
class SigmaConfiguration:
    def __init__(
        self,
        *,
        enable_check_set: typing.Optional[typing.Sequence["SigmaConfigurationEnableCheckSet"]] = None,
        malicious_url_patterns_file: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_check_set: (experimental) List of check sets to enable.
        :param malicious_url_patterns_file: (experimental) List of files containing malicious URL patterns.

        :stability: experimental
        :schema: sigma-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__452ba86b55e09c8a885946c42ff660af53ba63df0071499ecfed2b0d1918e013)
            check_type(argname="argument enable_check_set", value=enable_check_set, expected_type=type_hints["enable_check_set"])
            check_type(argname="argument malicious_url_patterns_file", value=malicious_url_patterns_file, expected_type=type_hints["malicious_url_patterns_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_check_set is not None:
            self._values["enable_check_set"] = enable_check_set
        if malicious_url_patterns_file is not None:
            self._values["malicious_url_patterns_file"] = malicious_url_patterns_file

    @builtins.property
    def enable_check_set(
        self,
    ) -> typing.Optional[typing.List["SigmaConfigurationEnableCheckSet"]]:
        '''(experimental) List of check sets to enable.

        :stability: experimental
        :schema: sigma-configuration#enable-check-set
        '''
        result = self._values.get("enable_check_set")
        return typing.cast(typing.Optional[typing.List["SigmaConfigurationEnableCheckSet"]], result)

    @builtins.property
    def malicious_url_patterns_file(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of files containing malicious URL patterns.

        :stability: experimental
        :schema: sigma-configuration#malicious-url-patterns-file
        '''
        result = self._values.get("malicious_url_patterns_file")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SigmaConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.polaris.SigmaConfigurationEnableCheckSet")
class SigmaConfigurationEnableCheckSet(enum.Enum):
    '''
    :stability: experimental
    :schema: SigmaConfigurationEnableCheckSet
    '''

    ALL = "ALL"
    '''(experimental) all.

    :stability: experimental
    '''
    CIS = "CIS"
    '''(experimental) cis.

    :stability: experimental
    '''
    DEFAULT = "DEFAULT"
    '''(experimental) default.

    :stability: experimental
    '''
    EMPTY = "EMPTY"
    '''(experimental) empty.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.polaris.SnapshotConfiguration",
    jsii_struct_bases=[],
    name_mapping={"date": "date", "id": "id", "reference": "reference"},
)
class SnapshotConfiguration:
    def __init__(
        self,
        *,
        date: typing.Optional[builtins.str] = None,
        id: typing.Optional[jsii.Number] = None,
        reference: typing.Any = None,
    ) -> None:
        '''
        :param date: (experimental) Date and time of snapshot to use for comparison report. The value should be of the form "YYYY-MM-DDThh:mm:ss" where date and time are separated by a "T", optionally followed by a time zone specification consisting of either "Z" denoting UTC or a "+" or "-" character followed by colon-separated hours and minutes east of UTC. Example: "2023-12-27T13:21:05-08:00". If no time zone is specified, the local time zone is assumed. This key is mutually exclusive with the "id" and "reference" keys.
        :param id: (experimental) ID of snapshot to use for comparison report. This key is mutually exclusive with the "date" and "reference" keys.
        :param reference: (experimental) One of "idir", "latest", or "scm". "idir" will use the snapshot created closest to, but not after, the creation date of the intermediate directory. "latest" will use the snapshot with the latest code-version date in the specified stream. "scm" will query the SCM to determine the version that was most recently checked out or updated, and then use the closest snapshot. This key is mutually exclusive with the "date" and "id" keys.

        :stability: experimental
        :schema: snapshot-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3befdb2cff755168850b75cef14a0badf619654302171b70d71fb38dc515f28b)
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date is not None:
            self._values["date"] = date
        if id is not None:
            self._values["id"] = id
        if reference is not None:
            self._values["reference"] = reference

    @builtins.property
    def date(self) -> typing.Optional[builtins.str]:
        '''(experimental) Date and time of snapshot to use for comparison report.

        The value should be of the form "YYYY-MM-DDThh:mm:ss" where date and time are separated by a "T", optionally followed by a time zone specification consisting of either "Z" denoting UTC or a "+" or "-" character followed by colon-separated hours and minutes east of UTC. Example: "2023-12-27T13:21:05-08:00". If no time zone is specified, the local time zone is assumed. This key is mutually exclusive with the "id" and "reference" keys.

        :stability: experimental
        :schema: snapshot-configuration#date
        '''
        result = self._values.get("date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) ID of snapshot to use for comparison report.

        This key is mutually exclusive with the "date" and "reference" keys.

        :stability: experimental
        :schema: snapshot-configuration#id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reference(self) -> typing.Any:
        '''(experimental) One of "idir", "latest", or "scm".

        "idir" will use the snapshot created closest to, but not after, the creation date of the intermediate directory. "latest" will use the snapshot with the latest code-version date in the specified stream. "scm" will query the SCM to determine the version that was most recently checked out or updated, and then use the closest snapshot. This key is mutually exclusive with the "date" and "id" keys.

        :stability: experimental
        :schema: snapshot-configuration#reference
        '''
        result = self._values.get("reference")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnapshotConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.SpecificCodingStandardConfiguration",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "file": "file", "pre_canned": "preCanned"},
)
class SpecificCodingStandardConfiguration:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["ResolvedCodingStandardConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[builtins.str] = None,
        pre_canned: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: (experimental) This key specifies the coding standard configuration for the given coding standard. The actual type of this key is specific to the particular coding standard. This key is mutually exclusive with the "file" key. A temporary configuration file will be generated containing the in-line configuration and then passed to "cov-analyze" using the "--coding-standard-config <config_file>" option.
        :param file: (experimental) This specifies the filename containing the configuration to use for the corresponding coding standard. This key is mutually exclusive with the "config" key.
        :param pre_canned: (experimental) This key specifies the name of a "pre-canned" coding standard configuration to use. The available pre-canned coding standard configurations depend on the coding standard in question. Refer to Coverity's documentation for details on the "pre-canned" configurations.

        :stability: experimental
        :schema: specific-coding-standard-configuration
        '''
        if isinstance(config, dict):
            config = ResolvedCodingStandardConfiguration(**config)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f5d78e52b734bea55549d850df5440d10efbc39969b85c4e4ade87e09f0aa31)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument pre_canned", value=pre_canned, expected_type=type_hints["pre_canned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if file is not None:
            self._values["file"] = file
        if pre_canned is not None:
            self._values["pre_canned"] = pre_canned

    @builtins.property
    def config(self) -> typing.Optional["ResolvedCodingStandardConfiguration"]:
        '''(experimental) This key specifies the coding standard configuration for the given coding standard.

        The actual type of this key is specific to the particular coding standard. This key is mutually exclusive with the "file" key. A temporary configuration file will be generated containing the in-line configuration and then passed to "cov-analyze" using the "--coding-standard-config <config_file>" option.

        :stability: experimental
        :schema: specific-coding-standard-configuration#config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ResolvedCodingStandardConfiguration"], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) This specifies the filename containing the configuration to use for the corresponding coding standard.

        This key is mutually exclusive with the "config" key.

        :stability: experimental
        :schema: specific-coding-standard-configuration#file
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_canned(self) -> typing.Optional[builtins.str]:
        '''(experimental) This key specifies the name of a "pre-canned" coding standard configuration to use.

        The available pre-canned coding standard configurations depend on the coding standard in question. Refer to Coverity's documentation for details on the "pre-canned" configurations.

        :stability: experimental
        :schema: specific-coding-standard-configuration#pre-canned
        '''
        result = self._values.get("pre_canned")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpecificCodingStandardConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.WebappArchiveConfiguration",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "validate_webapp": "validateWebapp"},
)
class WebappArchiveConfiguration:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        validate_webapp: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param path: (experimental) Specifies the path to the web application archive file or path to the directory containing the exploded web application.
        :param validate_webapp: (experimental) Indicates whether the web-app should be checked to see if it is valid during capture. The validation check checks that there is a "/WEB-INF/web.xml" file and that > 20% of classes for the web application were captured.

        :stability: experimental
        :schema: webapp-archive-configuration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aeda477dfccef585e14b6b5daaae99162b9ea695d60eb89108c537d67caea425)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument validate_webapp", value=validate_webapp, expected_type=type_hints["validate_webapp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if validate_webapp is not None:
            self._values["validate_webapp"] = validate_webapp

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the path to the web application archive file or path to the directory containing the exploded web application.

        :stability: experimental
        :schema: webapp-archive-configuration#path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_webapp(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the web-app should be checked to see if it is valid during capture.

        The validation check checks that there is a "/WEB-INF/web.xml" file and that > 20% of classes for the web application were captured.

        :stability: experimental
        :schema: webapp-archive-configuration#validate-webapp
        '''
        result = self._values.get("validate_webapp")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebappArchiveConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.PolarisCoverityOptions",
    jsii_struct_bases=[PolarisCoveritySchema],
    name_mapping={
        "commit": "commit",
        "analyze": "analyze",
        "caching": "caching",
        "capture": "capture",
        "version": "version",
    },
)
class PolarisCoverityOptions(PolarisCoveritySchema):
    def __init__(
        self,
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for ``PolarisCoverity``.

        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if isinstance(commit, dict):
            commit = CommitConfiguration(**commit)
        if isinstance(analyze, dict):
            analyze = AnalysisConfiguration(**analyze)
        if isinstance(caching, dict):
            caching = CachingConfiguration(**caching)
        if isinstance(capture, dict):
            capture = CaptureConfiguration(**capture)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f35e2e35bb0be5548bfe99d568501cecf320cc743a85523b183b1aa2910b9d8a)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument analyze", value=analyze, expected_type=type_hints["analyze"])
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
        }
        if analyze is not None:
            self._values["analyze"] = analyze
        if caching is not None:
            self._values["caching"] = caching
        if capture is not None:
            self._values["capture"] = capture
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def commit(self) -> "CommitConfiguration":
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#commit
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast("CommitConfiguration", result)

    @builtins.property
    def analyze(self) -> typing.Optional["AnalysisConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#analyze
        '''
        result = self._values.get("analyze")
        return typing.cast(typing.Optional["AnalysisConfiguration"], result)

    @builtins.property
    def caching(self) -> typing.Optional["CachingConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#caching
        '''
        result = self._values.get("caching")
        return typing.cast(typing.Optional["CachingConfiguration"], result)

    @builtins.property
    def capture(self) -> typing.Optional["CaptureConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#capture
        '''
        result = self._values.get("capture")
        return typing.cast(typing.Optional["CaptureConfiguration"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        :schema: PolarisCoveritySchema#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolarisCoverityOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.PolarisCoverityGoOptions",
    jsii_struct_bases=[PolarisCoverityOptions],
    name_mapping={
        "commit": "commit",
        "analyze": "analyze",
        "caching": "caching",
        "capture": "capture",
        "version": "version",
    },
)
class PolarisCoverityGoOptions(PolarisCoverityOptions):
    def __init__(
        self,
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for ``PolarisCoverityGo``.

        Extends base options with Go-specific defaults.

        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if isinstance(commit, dict):
            commit = CommitConfiguration(**commit)
        if isinstance(analyze, dict):
            analyze = AnalysisConfiguration(**analyze)
        if isinstance(caching, dict):
            caching = CachingConfiguration(**caching)
        if isinstance(capture, dict):
            capture = CaptureConfiguration(**capture)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__99765d77ecc4e7a0974dd639ba8a0d03979799d650010da78d894df08890f404)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument analyze", value=analyze, expected_type=type_hints["analyze"])
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
        }
        if analyze is not None:
            self._values["analyze"] = analyze
        if caching is not None:
            self._values["caching"] = caching
        if capture is not None:
            self._values["capture"] = capture
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def commit(self) -> "CommitConfiguration":
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#commit
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast("CommitConfiguration", result)

    @builtins.property
    def analyze(self) -> typing.Optional["AnalysisConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#analyze
        '''
        result = self._values.get("analyze")
        return typing.cast(typing.Optional["AnalysisConfiguration"], result)

    @builtins.property
    def caching(self) -> typing.Optional["CachingConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#caching
        '''
        result = self._values.get("caching")
        return typing.cast(typing.Optional["CachingConfiguration"], result)

    @builtins.property
    def capture(self) -> typing.Optional["CaptureConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#capture
        '''
        result = self._values.get("capture")
        return typing.cast(typing.Optional["CaptureConfiguration"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        :schema: PolarisCoveritySchema#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolarisCoverityGoOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.PolarisCoverityJavaOptions",
    jsii_struct_bases=[PolarisCoverityOptions],
    name_mapping={
        "commit": "commit",
        "analyze": "analyze",
        "caching": "caching",
        "capture": "capture",
        "version": "version",
    },
)
class PolarisCoverityJavaOptions(PolarisCoverityOptions):
    def __init__(
        self,
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for ``PolarisCoverityJava``.

        Extends base options with Java-specific defaults.

        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if isinstance(commit, dict):
            commit = CommitConfiguration(**commit)
        if isinstance(analyze, dict):
            analyze = AnalysisConfiguration(**analyze)
        if isinstance(caching, dict):
            caching = CachingConfiguration(**caching)
        if isinstance(capture, dict):
            capture = CaptureConfiguration(**capture)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2ac76d5fd48c764ffb1bf6d271a1b3f5bd1ecf9b140c1a85f3b112bdcca52d59)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument analyze", value=analyze, expected_type=type_hints["analyze"])
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
        }
        if analyze is not None:
            self._values["analyze"] = analyze
        if caching is not None:
            self._values["caching"] = caching
        if capture is not None:
            self._values["capture"] = capture
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def commit(self) -> "CommitConfiguration":
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#commit
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast("CommitConfiguration", result)

    @builtins.property
    def analyze(self) -> typing.Optional["AnalysisConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#analyze
        '''
        result = self._values.get("analyze")
        return typing.cast(typing.Optional["AnalysisConfiguration"], result)

    @builtins.property
    def caching(self) -> typing.Optional["CachingConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#caching
        '''
        result = self._values.get("caching")
        return typing.cast(typing.Optional["CachingConfiguration"], result)

    @builtins.property
    def capture(self) -> typing.Optional["CaptureConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#capture
        '''
        result = self._values.get("capture")
        return typing.cast(typing.Optional["CaptureConfiguration"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        :schema: PolarisCoveritySchema#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolarisCoverityJavaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.polaris.PolarisCoverityJavascriptOptions",
    jsii_struct_bases=[PolarisCoverityOptions],
    name_mapping={
        "commit": "commit",
        "analyze": "analyze",
        "caching": "caching",
        "capture": "capture",
        "version": "version",
    },
)
class PolarisCoverityJavascriptOptions(PolarisCoverityOptions):
    def __init__(
        self,
        *,
        commit: typing.Union["CommitConfiguration", typing.Dict[builtins.str, typing.Any]],
        analyze: typing.Optional[typing.Union["AnalysisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        caching: typing.Optional[typing.Union["CachingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        capture: typing.Optional[typing.Union["CaptureConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for ``PolarisCoverityJavascript``.

        Extends base options with JavaScript/TypeScript-specific defaults.

        :param commit: 
        :param analyze: 
        :param caching: 
        :param capture: 
        :param version: (experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        '''
        if isinstance(commit, dict):
            commit = CommitConfiguration(**commit)
        if isinstance(analyze, dict):
            analyze = AnalysisConfiguration(**analyze)
        if isinstance(caching, dict):
            caching = CachingConfiguration(**caching)
        if isinstance(capture, dict):
            capture = CaptureConfiguration(**capture)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3a716860f9840a2f8643522f9c278650861c7f627216f7aff1d6da1451455b16)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument analyze", value=analyze, expected_type=type_hints["analyze"])
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
        }
        if analyze is not None:
            self._values["analyze"] = analyze
        if caching is not None:
            self._values["caching"] = caching
        if capture is not None:
            self._values["capture"] = capture
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def commit(self) -> "CommitConfiguration":
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#commit
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast("CommitConfiguration", result)

    @builtins.property
    def analyze(self) -> typing.Optional["AnalysisConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#analyze
        '''
        result = self._values.get("analyze")
        return typing.cast(typing.Optional["AnalysisConfiguration"], result)

    @builtins.property
    def caching(self) -> typing.Optional["CachingConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#caching
        '''
        result = self._values.get("caching")
        return typing.cast(typing.Optional["CachingConfiguration"], result)

    @builtins.property
    def capture(self) -> typing.Optional["CaptureConfiguration"]:
        '''
        :stability: experimental
        :schema: PolarisCoveritySchema#capture
        '''
        result = self._values.get("capture")
        return typing.cast(typing.Optional["CaptureConfiguration"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Specifies the version of the configuration file in use.

        :stability: experimental
        :schema: PolarisCoveritySchema#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolarisCoverityJavascriptOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AnalysisConfiguration",
    "AnalysisConfigurationAggressivenessLevel",
    "AnalysisConfigurationLocation",
    "AnalysisConfigurationMode",
    "AnalyzeConnectConfiguration",
    "AnalyzeConnectConfigurationUploadArtifacts",
    "AnalyzeFilesConfiguration",
    "BuildConfiguration",
    "CachingConfiguration",
    "CaptureConfiguration",
    "CheckerConfiguration",
    "CheckerConfigurationWebappSecurity",
    "CheckerConfigurationWebappSecurityAggressivenessLevel",
    "CodingStandardConfiguration",
    "CodingStandardDeviation",
    "CommitConfiguration",
    "CommitConfigurationConnect",
    "CommitConfigurationConnectOnNewCert",
    "CommitConfigurationConnectScm",
    "CommitConfigurationConnectTriage",
    "CommitConfigurationConnectUploadArtifacts",
    "CommitConfigurationLocal",
    "CommitConfigurationLocalFormat",
    "CommitConfigurationSrm",
    "CompilerConfiguration",
    "CovTranslateConfiguration",
    "DirectivesConfiguration",
    "DirectivesConfigurationConfig",
    "DirectivesConfigurationConfigType",
    "FilesConfiguration",
    "ImportScmConfiguration",
    "JobsConfiguration",
    "LanguagesConfiguration",
    "LanguagesConfigurationExclude",
    "LanguagesConfigurationInclude",
    "ParallelTranslateConfiguration",
    "ParseWarningsConfiguration",
    "PolarisCoverity",
    "PolarisCoverityGoOptions",
    "PolarisCoverityJavaOptions",
    "PolarisCoverityJavascriptOptions",
    "PolarisCoverityOptions",
    "PolarisCoveritySchema",
    "PolarisGoCoverity",
    "PolarisJavaCoverity",
    "PolarisJavascriptCoverity",
    "ResolvedCodingStandardConfiguration",
    "SigmaConfiguration",
    "SigmaConfigurationEnableCheckSet",
    "SnapshotConfiguration",
    "SpecificCodingStandardConfiguration",
    "WebappArchiveConfiguration",
]

publication.publish()

def _typecheckingstub__5b1b87f9b43ed84e0acc43840a145366632715b3ccf8365068e62aff7e8b39ce(
    *,
    aggressiveness_level: typing.Optional[AnalysisConfigurationAggressivenessLevel] = None,
    callgraph_metrics: typing.Optional[builtins.bool] = None,
    c_cpp_fnptr: typing.Optional[builtins.bool] = None,
    c_cpp_virtual: typing.Optional[builtins.bool] = None,
    checkers: typing.Optional[typing.Union[CheckerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    coding_standards: typing.Optional[typing.Union[CodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    connect: typing.Optional[typing.Union[AnalyzeConnectConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    constraint_fpp: typing.Optional[builtins.bool] = None,
    cov_analyze_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    cov_collect_models_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    directives: typing.Optional[typing.Sequence[typing.Union[DirectivesConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    files: typing.Optional[typing.Union[AnalyzeFilesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    jobs: typing.Optional[typing.Sequence[typing.Union[JobsConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    location: typing.Optional[AnalysisConfigurationLocation] = None,
    mode: typing.Optional[AnalysisConfigurationMode] = None,
    model_file: typing.Optional[builtins.str] = None,
    one_tu_per_psf: typing.Optional[builtins.bool] = None,
    output_model_file: typing.Optional[builtins.str] = None,
    parse_warnings: typing.Optional[typing.Union[ParseWarningsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    scan_transparency: typing.Optional[builtins.bool] = None,
    sigma: typing.Optional[typing.Union[SigmaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    trust: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459a713d78e38fd614ae50c9a5552f868863f0b6099fc83bd2ae1ec8d0b3cddb(
    *,
    url: builtins.str,
    auth_key_file: typing.Optional[builtins.str] = None,
    ca_certs_file: typing.Optional[builtins.str] = None,
    proxy_client_cert_file: typing.Optional[builtins.str] = None,
    proxy_client_key_file: typing.Optional[builtins.str] = None,
    proxy_url: typing.Optional[builtins.str] = None,
    upload_artifacts: typing.Optional[AnalyzeConnectConfigurationUploadArtifacts] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9daf461f16912944b8d5c944b16a274a24af7a4f202700d0315191ac0a7b16(
    *,
    exclude_glob: typing.Optional[builtins.str] = None,
    exclude_regex: typing.Optional[builtins.str] = None,
    include_files: typing.Optional[builtins.str] = None,
    include_glob: typing.Optional[builtins.str] = None,
    include_list_file: typing.Optional[builtins.str] = None,
    include_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b758dad2d938ef8d86e6197414de189afa576eb5a6f03b29fe130fd3a4b779af(
    *,
    build_command: builtins.str,
    aspnet_compiler: typing.Optional[builtins.bool] = None,
    bazel: typing.Optional[builtins.bool] = None,
    clean_command: typing.Optional[builtins.str] = None,
    cov_build_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    defer_decomp: typing.Optional[builtins.bool] = None,
    instrument: typing.Optional[builtins.bool] = None,
    parallel_translate: typing.Optional[typing.Union[ParallelTranslateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    scan_transparency: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0b433d7ebb00cc93576ab8200b34f77607aae46ff169416465fb293a5a4cb1(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de5dfcfda282391d183474360405466b889cca5ccc239d1e268f01a81936d8d(
    *,
    build_capture: typing.Optional[typing.Union[BuildConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command_inference: typing.Optional[builtins.bool] = None,
    compiler_configuration: typing.Optional[typing.Union[CompilerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    cov_translate: typing.Optional[typing.Union[CovTranslateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    emit_complementary_info: typing.Optional[builtins.bool] = None,
    encoding: typing.Optional[builtins.str] = None,
    failure_threshold_percent: typing.Optional[jsii.Number] = None,
    files: typing.Optional[typing.Union[FilesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    force_dependency_resolution: typing.Optional[builtins.bool] = None,
    import_scm: typing.Optional[typing.Union[ImportScmConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    languages: typing.Optional[typing.Union[LanguagesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    minimal_classpath_emit: typing.Optional[builtins.bool] = None,
    record_with_source: typing.Optional[builtins.bool] = None,
    security_da: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20118a538bd2f0c6222fa6c379224b2d866df17d41c1f5ad837f0a235c928a66(
    *,
    all: typing.Optional[builtins.bool] = None,
    all_security: typing.Optional[builtins.bool] = None,
    android_security: typing.Optional[builtins.bool] = None,
    audit: typing.Optional[builtins.bool] = None,
    brakeman: typing.Optional[builtins.bool] = None,
    c_family_security: typing.Optional[builtins.bool] = None,
    checker_config: typing.Any = None,
    codexm: typing.Optional[typing.Sequence[builtins.str]] = None,
    concurrency: typing.Optional[builtins.bool] = None,
    default: typing.Optional[builtins.bool] = None,
    pmd: typing.Optional[builtins.bool] = None,
    recommended_security_checkers: typing.Optional[builtins.bool] = None,
    rule: typing.Optional[builtins.bool] = None,
    webapp_security: typing.Optional[typing.Union[CheckerConfigurationWebappSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846d906367a3a82580d316c7a445a95e059c18dc8ea53adca4a04d0c958decc2(
    *,
    aggressiveness_level: typing.Optional[CheckerConfigurationWebappSecurityAggressivenessLevel] = None,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d746461fb5b288993834907d57557d631e8a7e2b2aefb9659029516fce68eb(
    *,
    autosarcpp14: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    cert_c: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    cert_cpp: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    cert_c_recommendation: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    cert_java: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    hyundai_c: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    hyundai_cpp: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    hyundai_java: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ignore_deviated_findings: typing.Optional[builtins.bool] = None,
    iso_ts17961: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    misrac2004: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    misrac2012: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    misrac2023: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    misracpp2008: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    misracpp2023: typing.Optional[typing.Union[SpecificCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093a59ecfe140bbb066a4c2ce8ec4e051c97545feaddca5c4422d6edf24d2a89(
    *,
    deviation: builtins.str,
    reason: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29574609a2ede742a8d684fbf27d054f7005af44af80d1a5533394d600d082bc(
    *,
    connect: typing.Optional[typing.Union[CommitConfigurationConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    local: typing.Optional[typing.Union[CommitConfigurationLocal, typing.Dict[builtins.str, typing.Any]]] = None,
    srm: typing.Optional[typing.Union[CommitConfigurationSrm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed61ca990a2803b1dc8f189dde3a89fbb0438fa571a9d4245ff52892ab62713f(
    *,
    stream: builtins.str,
    url: builtins.str,
    auth_key_file: typing.Optional[builtins.str] = None,
    ca_certs_file: typing.Optional[builtins.str] = None,
    comparison_only: typing.Optional[builtins.bool] = None,
    comparison_report: typing.Optional[builtins.str] = None,
    cov_commit_defects_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    on_new_cert: typing.Optional[CommitConfigurationConnectOnNewCert] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_client_cert_file: typing.Optional[builtins.str] = None,
    proxy_client_key_file: typing.Optional[builtins.str] = None,
    proxy_url: typing.Optional[builtins.str] = None,
    scm: typing.Optional[CommitConfigurationConnectScm] = None,
    snapshot: typing.Optional[typing.Union[SnapshotConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    triage: typing.Optional[typing.Union[CommitConfigurationConnectTriage, typing.Dict[builtins.str, typing.Any]]] = None,
    upload_artifacts: typing.Optional[CommitConfigurationConnectUploadArtifacts] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca8942001713bf2b024f8c7d8f36592448f130bf302c4a48be012f6e42f1c6f(
    *,
    new_defect_owner: typing.Optional[builtins.str] = None,
    new_defect_owner_limit: typing.Optional[jsii.Number] = None,
    set_new_defect_owner: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441cf9fe31389f57447c8fff4013df705305b2ff8a2dec14ec84bfdea342d10f(
    *,
    path: builtins.str,
    format: typing.Optional[CommitConfigurationLocalFormat] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7719cef67abaafefdfae79698844a772a5114f09ff2e8da55d3c796e31a50958(
    *,
    url: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    parent_branch: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[jsii.Number] = None,
    project_name: typing.Optional[builtins.str] = None,
    token_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a94af515c2d1f0d4abeac655dd05070f012477b1be355b386870709ac204356(
    *,
    cov_configure: typing.Optional[typing.Sequence[typing.Sequence[builtins.str]]] = None,
    file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc20d36229af30b2db04b009de30659d54e39db473f44cd58d65ee8a14d1be9(
    *,
    command: builtins.str,
    cov_build_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    defer_decomp: typing.Optional[builtins.bool] = None,
    parallel_translate: typing.Optional[typing.Union[ParallelTranslateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    scan_transparency: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04394952de531f5747c84a1edc1f57889db3866770b7c415cb58d6f04f072ad1(
    *,
    config: typing.Optional[typing.Union[DirectivesConfigurationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7a4ee187ba693efb70331c8d4e7e9030f409b205c3261ce10d4ae77a5a689f(
    *,
    directives: typing.Sequence[typing.Any],
    language: builtins.str,
    format_version: typing.Optional[jsii.Number] = None,
    type: typing.Optional[DirectivesConfigurationConfigType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e21a938b0cd3f7f78413617cac3b659e5e592f27b0b1b359dbec52aa1065c4a(
    *,
    emit_minified_js: typing.Optional[builtins.bool] = None,
    exclude_glob: typing.Optional[builtins.str] = None,
    exclude_regex: typing.Optional[builtins.str] = None,
    include_dirs: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_glob: typing.Optional[builtins.str] = None,
    include_list_file: typing.Optional[builtins.str] = None,
    include_regex: typing.Optional[builtins.str] = None,
    java_version: typing.Optional[builtins.str] = None,
    library_dirs: typing.Optional[typing.Sequence[builtins.str]] = None,
    library_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    webapp_archives: typing.Optional[typing.Sequence[typing.Union[WebappArchiveConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5555fb5552ef0b1d1251be5a69c8c4999e25d70fc0ae2dfe513d0ffc56a08a0c(
    *,
    cov_import_scm_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    filename_regex: typing.Optional[builtins.str] = None,
    ms_delay: typing.Optional[jsii.Number] = None,
    scm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8db274644be63f71290f71e698f60a1d541bd5ff8d1be025629919de82a8dd5(
    *,
    auto: typing.Optional[builtins.bool] = None,
    count: typing.Optional[jsii.Number] = None,
    max: typing.Optional[jsii.Number] = None,
    override_worker_limit: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee84483a641935f1dfe18312eca06dcb545ad1d67e6ae2806221553c2db2fbc7(
    *,
    exclude: typing.Optional[typing.Sequence[LanguagesConfigurationExclude]] = None,
    include: typing.Optional[typing.Sequence[LanguagesConfigurationInclude]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53feeef20f3b05f5c93a14a5eef5c7c4946e0110a45c85fc4a4631da319c2f58(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    processes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcbf188f45310736039810da3f534c75ed3411f5ff12d48dc33afa270b3e373(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4c24407e00a34ed4c70234d7e25620c34f55d5e47791d87b198acbededa434(
    project: _projen_04054675.Project,
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5882a46d0d2414e8d78d86c82171084bcc091f8af0592a2fbf2e9482f42bafdb(
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acc879fddf1b7a5f1d4f7ee74c841099f637cf40a5656f85fa56adcf1ed57f3(
    project: _projen_04054675.Project,
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8839e24f68d014f3a20ab2e7a51a34763a500502d8f6cdcfec178447bc94e1eb(
    project: _projen_04054675.Project,
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf36697ef10b94b77c64a209132aed9ad4344145e79ca8f137be0d16e6cb30a5(
    project: _projen_04054675.Project,
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f776076c15568425956f38645c9dab8701fe2f9f2ec7df2bd73c6125bbe76274(
    *,
    title: builtins.str,
    deviations: typing.Optional[typing.Sequence[typing.Union[CodingStandardDeviation, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452ba86b55e09c8a885946c42ff660af53ba63df0071499ecfed2b0d1918e013(
    *,
    enable_check_set: typing.Optional[typing.Sequence[SigmaConfigurationEnableCheckSet]] = None,
    malicious_url_patterns_file: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3befdb2cff755168850b75cef14a0badf619654302171b70d71fb38dc515f28b(
    *,
    date: typing.Optional[builtins.str] = None,
    id: typing.Optional[jsii.Number] = None,
    reference: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5d78e52b734bea55549d850df5440d10efbc39969b85c4e4ade87e09f0aa31(
    *,
    config: typing.Optional[typing.Union[ResolvedCodingStandardConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[builtins.str] = None,
    pre_canned: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeda477dfccef585e14b6b5daaae99162b9ea695d60eb89108c537d67caea425(
    *,
    path: typing.Optional[builtins.str] = None,
    validate_webapp: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35e2e35bb0be5548bfe99d568501cecf320cc743a85523b183b1aa2910b9d8a(
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99765d77ecc4e7a0974dd639ba8a0d03979799d650010da78d894df08890f404(
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac76d5fd48c764ffb1bf6d271a1b3f5bd1ecf9b140c1a85f3b112bdcca52d59(
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a716860f9840a2f8643522f9c278650861c7f627216f7aff1d6da1451455b16(
    *,
    commit: typing.Union[CommitConfiguration, typing.Dict[builtins.str, typing.Any]],
    analyze: typing.Optional[typing.Union[AnalysisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    caching: typing.Optional[typing.Union[CachingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    capture: typing.Optional[typing.Union[CaptureConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
