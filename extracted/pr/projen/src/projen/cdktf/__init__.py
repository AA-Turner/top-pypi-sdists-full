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
    import projen.cdk as _cdk_bb21cefa
    import projen.github as _github_c49f935d
    import projen.github.workflows as _workflows_2b7f1587
    import projen.javascript as _javascript_eb5dbe11
    import projen.release as _release_1fa091fd
    import projen.typescript as _typescript_7a66cf84
else:

    _cdk_bb21cefa = _LazyImport("projen.cdk")
    _github_c49f935d = _LazyImport("projen.github")
    _javascript_eb5dbe11 = _LazyImport("projen.javascript")
    _projen_04054675 = _LazyImport("projen")
    _release_1fa091fd = _LazyImport("projen.release")
    _typescript_7a66cf84 = _LazyImport("projen.typescript")
    _workflows_2b7f1587 = _LazyImport("projen.github.workflows")


class ConstructLibraryCdktf(
    _cdk_bb21cefa.ConstructLibrary,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.cdktf.ConstructLibraryCdktf",
):
    '''(experimental) CDKTF construct library project.

    A multi-language (jsii) construct library which vends constructs designed to
    use within the CDK for Terraform (CDKTF), with a friendly workflow and
    automatic publishing to the construct catalog.

    :stability: experimental
    :pjid: cdktf-construct
    '''

    def __init__(
        self,
        *,
        cdktf_version: builtins.str,
        constructs_version: typing.Optional[builtins.str] = None,
        catalog: typing.Optional[typing.Union["_cdk_bb21cefa.Catalog", typing.Dict[builtins.str, typing.Any]]] = None,
        author: builtins.str,
        author_address: builtins.str,
        repository_url: builtins.str,
        compat: typing.Optional[builtins.bool] = None,
        compat_ignore: typing.Optional[builtins.str] = None,
        compress_assembly: typing.Optional[builtins.bool] = None,
        docgen_file_path: typing.Optional[builtins.str] = None,
        exclude_typescript: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsii_version: typing.Optional[builtins.str] = None,
        publish_to_go: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiGoTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_maven: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiJavaTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_nuget: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiDotNetTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_pypi: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiPythonTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        rootdir: typing.Optional[builtins.str] = None,
        validate_tsconfig: typing.Optional["_cdk_bb21cefa.ValidateTsconfig"] = None,
        disable_tsconfig: typing.Optional[builtins.bool] = None,
        disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
        docgen: typing.Optional[builtins.bool] = None,
        docs_directory: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union["_javascript_eb5dbe11.EslintOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        libdir: typing.Optional[builtins.str] = None,
        projenrc_ts: typing.Optional[builtins.bool] = None,
        projenrc_ts_options: typing.Optional[typing.Union["_typescript_7a66cf84.ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        runner: typing.Optional["_typescript_7a66cf84.TypeScriptRunner"] = None,
        sample_code: typing.Optional[builtins.bool] = None,
        srcdir: typing.Optional[builtins.str] = None,
        testdir: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[typing.Union["_javascript_eb5dbe11.TypescriptConfigOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev: typing.Optional[typing.Union["_javascript_eb5dbe11.TypescriptConfigOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev_file: typing.Optional[builtins.str] = None,
        ts_jest_options: typing.Optional[typing.Union["_typescript_7a66cf84.TsJestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        typescript_version: typing.Optional[builtins.str] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        audit_deps: typing.Optional[builtins.bool] = None,
        audit_deps_options: typing.Optional[typing.Union["_javascript_eb5dbe11.AuditOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        biome: typing.Optional[builtins.bool] = None,
        biome_options: typing.Optional[typing.Union["_javascript_eb5dbe11.BiomeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union["_javascript_eb5dbe11.BuildWorkflowOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        bundler_options: typing.Optional[typing.Union["_javascript_eb5dbe11.BundlerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        check_licenses: typing.Optional[typing.Union["_javascript_eb5dbe11.LicenseCheckerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union["_github_c49f935d.DependabotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union["_javascript_eb5dbe11.UpgradeDependenciesOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union["_javascript_eb5dbe11.JestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union["_projen_04054675.IgnoreFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        package: typing.Optional[builtins.bool] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union["_javascript_eb5dbe11.PrettierOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_js_options: typing.Optional[typing.Union["_javascript_eb5dbe11.ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_version: typing.Optional[builtins.str] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        release: typing.Optional[builtins.bool] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union["_workflows_2b7f1587.JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_git_identity: typing.Optional[typing.Union["_github_c49f935d.GitIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        auto_approve_options: typing.Optional[typing.Union["_github_c49f935d.AutoApproveOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union["_github_c49f935d.AutoMergeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union["_github_c49f935d.GitHubOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        projen_credentials: typing.Optional["_github_c49f935d.GithubCredentials"] = None,
        readme: typing.Optional[typing.Union["_projen_04054675.SampleReadmeProps", typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union["_github_c49f935d.StaleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        add_package_manager_to_dev_engines: typing.Optional[builtins.bool] = None,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        allow_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bun_version: typing.Optional[builtins.str] = None,
        code_artifact_options: typing.Optional[typing.Union["_javascript_eb5dbe11.CodeArtifactOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_orphaned_lock_files: typing.Optional[builtins.bool] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        dev_engines: typing.Optional[typing.Union["_javascript_eb5dbe11.DevEngines", typing.Dict[builtins.str, typing.Any]]] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        npm_access: typing.Optional["_javascript_eb5dbe11.NpmAccess"] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        npm_trusted_publishing: typing.Optional[builtins.bool] = None,
        package_manager: typing.Optional["_javascript_eb5dbe11.NodePackageManager"] = None,
        package_name: typing.Optional[builtins.str] = None,
        peer_dependency_options: typing.Optional[typing.Union["_javascript_eb5dbe11.PeerDependencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_options: typing.Optional[typing.Union["_javascript_eb5dbe11.PnpmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union["_javascript_eb5dbe11.ScopedPackagesOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        stability: typing.Optional[builtins.str] = None,
        yarn_berry_options: typing.Optional[typing.Union["_javascript_eb5dbe11.YarnBerryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        bump_package: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union["_workflows_2b7f1587.JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional["_projen_04054675.ReleasableCommits"] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union["_release_1fa091fd.BranchOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        release_environment: typing.Optional[builtins.str] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional["_release_1fa091fd.ReleaseTrigger"] = None,
        release_workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union["_workflows_2b7f1587.JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union["_projen_04054675.GroupRunnerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union["_projen_04054675.IgnoreFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union["_projen_04054675.GitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union["_projen_04054675.LoggerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional["_projen_04054675.Project"] = None,
        project_tree: typing.Optional[builtins.bool] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union["_projen_04054675.ProjenrcJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union["_projen_04054675.RenovatebotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cdktf_version: (experimental) Minimum target version this library is tested against. Default: "^0.13.0"
        :param constructs_version: (experimental) Construct version to use. Default: "^10.3.0"
        :param catalog: (experimental) Libraries will be picked up by the construct catalog when they are published to npm as jsii modules and will be published under:. https://awscdk.io/packages/[@SCOPE/]PACKAGE@VERSION The catalog will also post a tweet to https://twitter.com/awscdkio with the package name, description and the above link. You can disable these tweets through ``{ announce: false }``. You can also add a Twitter handle through ``{ twitter: 'xx' }`` which will be mentioned in the tweet. Default: - new version will be announced
        :param author: (experimental) The name of the library author. Default: $GIT_USER_NAME
        :param author_address: (experimental) Email or URL of the library author. Default: $GIT_USER_EMAIL
        :param repository_url: (experimental) Git repository URL. Default: $GIT_REMOTE
        :param compat: (experimental) Automatically run API compatibility test against the latest version published to npm after compilation. - You can manually run compatibility tests using ``yarn compat`` if this feature is disabled. - You can ignore compatibility failures by adding lines to a ".compatignore" file. Default: false
        :param compat_ignore: (experimental) Name of the ignore file for API compatibility tests. Default: ".compatignore"
        :param compress_assembly: (experimental) Emit a compressed version of the assembly. Default: false
        :param docgen_file_path: (experimental) File path for generated docs. Default: "API.md"
        :param exclude_typescript: (experimental) Accepts a list of glob patterns. Files matching any of those patterns will be excluded from the TypeScript compiler input. By default, jsii will include all *.ts files (except .d.ts files) in the TypeScript compiler input. This can be problematic for example when the package's build or test procedure generates .ts files that cannot be compiled with jsii's compiler settings.
        :param jsii_version: (experimental) Version of the jsii compiler to use. Set to "*" if you want to manually manage the version of jsii in your project by managing updates to ``package.json`` on your own. NOTE: The jsii compiler releases since 5.0.0 are not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~5.0.0``). Default: "~5.9.0"
        :param publish_to_go: (experimental) Publish Go bindings to a git repository. Default: - no publishing
        :param publish_to_maven: (experimental) Publish to maven. Default: - no publishing
        :param publish_to_nuget: (experimental) Publish to NuGet. Default: - no publishing
        :param publish_to_pypi: (experimental) Publish to pypi. Default: - no publishing
        :param rootdir: Default: "."
        :param validate_tsconfig: (experimental) Level of tsconfig validation jsii should perform on the user-provided tsconfig. Only relevant when the project synthesizes its own tsconfig (i.e. ``disableTsconfig`` is not set on the TypeScriptProject). Default: ValidateTsconfig.STRICT
        :param disable_tsconfig: (experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler). Default: false
        :param disable_tsconfig_dev: (experimental) Do not generate a development tsconfig file. Default: false
        :param docgen: (experimental) Docgen by Typedoc. Default: false
        :param docs_directory: (experimental) Docs directory. Default: "docs"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: - true, unless biome is enabled
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param libdir: (experimental) Typescript artifacts output directory. Default: "lib"
        :param projenrc_ts: (experimental) Use TypeScript for your projenrc file (``.projenrc.ts``). Default: false
        :param projenrc_ts_options: (experimental) Options for .projenrc.ts.
        :param runner: (experimental) The TypeScript runner to use for executing TypeScript files. This is a project-level setting that components (e.g. projenrc) will use as their default runner. Default: TypeScriptRunner.tsNode()
        :param sample_code: (experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there. Default: true
        :param srcdir: (experimental) Typescript sources directory. Default: "src"
        :param testdir: (experimental) Jest tests directory. Tests files should be named ``xxx.test.ts``. If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``), then tests are going to be compiled into ``lib/`` and executed as javascript. If the test directory is outside of ``src``, then we configure jest to compile the code in-memory. Default: "test"
        :param tsconfig: (experimental) Custom TSConfig. Default: - default options
        :param tsconfig_dev: (experimental) Custom tsconfig options for the development tsconfig.json file (used for testing). Default: - use the production tsconfig options
        :param tsconfig_dev_file: (experimental) The name (and path) of the development tsconfig file. By default this lives inside the test directory (e.g. ``test/tsconfig.json``) so that the TypeScript language service resolves it as the nearest config for test files. Default: - "{testdir}/tsconfig.json"
        :param ts_jest_options: (experimental) Options for ts-jest.
        :param typescript_version: (experimental) TypeScript version to use. NOTE: Typescript is not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``). Default: "latest"
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param audit_deps: (experimental) Run security audit on dependencies. When enabled, creates an "audit" task that checks for known security vulnerabilities in dependencies. By default, runs during every build and checks for "high" severity vulnerabilities or above in all dependencies (including dev dependencies). Default: false
        :param audit_deps_options: (experimental) Security audit options. Default: - default options
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configured). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param biome: (experimental) Setup Biome. Default: false
        :param biome_options: (experimental) Biome options. Default: - default options
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v5 By default, OIDC auth is used. Alternatively a token can be provided via ``codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token. Default: - OIDC auth is used
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: - ``true`` for root projects, ``false`` for subprojects
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: - true if not a subproject
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - default GitHub Actions user
        :param workflow_node_version: (experimental) The node version used in GitHub Actions workflows. Always use this option if your GitHub Actions workflows require a specific to run. Default: - ``minNodeVersion`` if set, otherwise ``lts/*``.
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param add_package_manager_to_dev_engines: (experimental) Automatically add the resolved ``packageManager`` to ``devEngines.packageManager`` in ``package.json``, setting ``onFail`` to ``ignore``. Default: true
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param allow_scripts: (experimental) List of dependency (package) names that are allowed to run lifecycle install scripts (``preinstall``, ``install``, ``postinstall``, ``prepare``) during dependency installation. These scripts can execute arbitrary code, making them a common supply-chain attack vector. Package managers are moving toward blocking them by default and requiring an explicit allowlist. Configuring ``allowScripts`` sets up that allowlist so scripts only run for the packages you have explicitly reviewed and trust. Support for this setting depends on the configured ``packageManager``: - ``NPM``: written to the native ``allowScripts`` field in ``package.json`` (requires npm >= 11.16; see https://docs.npmjs.com/cli/v11/commands/npm-approve-scripts). - ``BUN``: written to the native ``trustedDependencies`` field in ``package.json`` (see https://bun.com/docs/pm/lifecycle). - ``PNPM``: written to the ``onlyBuiltDependencies`` setting in ``pnpm-workspace.yaml`` (see https://pnpm.io/settings#onlybuiltdependencies). - ``YARN2``, ``YARN_BERRY``: written to the native ``dependenciesMeta.<pkg>.built`` allowlist in ``package.json``, combined with ``enableScripts: false`` in ``.yarnrc.yml`` (see https://yarnpkg.com/features/security#postinstalls). If you set ``yarnBerryOptions.yarnRcOptions.enableScripts`` explicitly, that value is respected instead of being overridden. - ``YARN``, ``YARN_CLASSIC``: not supported. Yarn Classic has no native mechanism to allowlist install scripts for specific dependencies. Setting this option with one of these package managers throws an error at synthesis time. Default: - all install scripts are allowed to run (package manager default)
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and this will be what your ``package.json`` will eventually include.
        :param bun_version: (experimental) The version of Bun to use if using Bun as a package manager. Default: "latest"
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param delete_orphaned_lock_files: (experimental) Automatically delete lockfiles from package managers that are not the active one. Only triggered when the lockfile for the configured package manager already exists. This is useful when migrating between package managers to avoid conflicts. Default: true
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and this will be what your ``package.json`` will eventually include. Default: []
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and this will be what your ``package.json`` will eventually include. Default: []
        :param dev_engines: (experimental) Configure the ``devEngines`` field in ``package.json``. The ``devEngines.packageManager`` field is automatically populated based on the resolved ``packageManager`` value. Any fields provided here are merged with the auto-populated ``packageManager`` entry.
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json Default: "lib/index.js"
        :param homepage: (experimental) Package's Homepage / Website.
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param max_node_version: (experimental) The maximum node version supported by this package. Most projects should not use this option. The value indicates that the package is incompatible with any newer versions of node. This requirement is enforced via the engines field. You will normally not need to set this option. Consider this option only if your package is known to not function with newer versions of node. Default: - no maximum version is enforced
        :param min_node_version: (experimental) The minimum node version required by this package to function. Most projects should not use this option. The value indicates that the package is incompatible with any older versions of node. This requirement is enforced via the engines field. You will normally not need to set this option, even if your package is incompatible with EOL versions of node. Consider this option only if your package depends on a specific feature, that is not available in other LTS versions. Setting this option has very high impact on the consumers of your package, as package managers will actively prevent usage with node versions you have marked as incompatible. To change the node version of your CI/CD workflows, use ``workflowNodeVersion``. Default: - no minimum version is enforced
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_provenance: (experimental) Should provenance statements be generated when the package is published. A supported package manager is required to publish a package with npm provenance statements and you will need to use a supported CI/CD provider. Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - true for public packages, false otherwise
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param npm_trusted_publishing: (experimental) Use trusted publishing for publishing to npmjs.com Needs to be pre-configured on npm.js to work. Default: - false
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: - Detected from the calling process or ``YARN_CLASSIC`` if detection fails.
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_options: (experimental) Options for pnpm. Default: - all default options
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "10.33.0"
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param stability: (experimental) Package's Stability.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: - A recent version of "commit-and-tag-version"
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. This setting cannot be specified together with ``minMajorVersion``; the invoked script can be used to achieve the effects of ``minMajorVersion``. Default: - The next version will be determined based on the commit history and project settings.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_environment: (experimental) The GitHub Actions environment used for the release. This can be used to add an explicit approval step to the release or limit who can initiate a release through environment protection rules. When multiple artifacts are released, the environment can be overwritten on a per artifact basis. Default: - no environment used, unless set at the artifact level
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_env: (experimental) Build environment variables for release workflows. Default: {}
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with commit-and-tag-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param project_tree: (experimental) Generate a project tree file (``.projen/tree.json``) that shows all components and their relationships. Useful for understanding your project structure and debugging. Default: false
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options

        :stability: experimental
        '''
        options = ConstructLibraryCdktfOptions(
            cdktf_version=cdktf_version,
            constructs_version=constructs_version,
            catalog=catalog,
            author=author,
            author_address=author_address,
            repository_url=repository_url,
            compat=compat,
            compat_ignore=compat_ignore,
            compress_assembly=compress_assembly,
            docgen_file_path=docgen_file_path,
            exclude_typescript=exclude_typescript,
            jsii_version=jsii_version,
            publish_to_go=publish_to_go,
            publish_to_maven=publish_to_maven,
            publish_to_nuget=publish_to_nuget,
            publish_to_pypi=publish_to_pypi,
            rootdir=rootdir,
            validate_tsconfig=validate_tsconfig,
            disable_tsconfig=disable_tsconfig,
            disable_tsconfig_dev=disable_tsconfig_dev,
            docgen=docgen,
            docs_directory=docs_directory,
            entrypoint_types=entrypoint_types,
            eslint=eslint,
            eslint_options=eslint_options,
            libdir=libdir,
            projenrc_ts=projenrc_ts,
            projenrc_ts_options=projenrc_ts_options,
            runner=runner,
            sample_code=sample_code,
            srcdir=srcdir,
            testdir=testdir,
            tsconfig=tsconfig,
            tsconfig_dev=tsconfig_dev,
            tsconfig_dev_file=tsconfig_dev_file,
            ts_jest_options=ts_jest_options,
            typescript_version=typescript_version,
            artifacts_directory=artifacts_directory,
            audit_deps=audit_deps,
            audit_deps_options=audit_deps_options,
            auto_approve_upgrades=auto_approve_upgrades,
            biome=biome,
            biome_options=biome_options,
            build_workflow=build_workflow,
            build_workflow_options=build_workflow_options,
            bundler_options=bundler_options,
            check_licenses=check_licenses,
            code_cov=code_cov,
            code_cov_token_secret=code_cov_token_secret,
            copyright_owner=copyright_owner,
            copyright_period=copyright_period,
            default_release_branch=default_release_branch,
            dependabot=dependabot,
            dependabot_options=dependabot_options,
            deps_upgrade=deps_upgrade,
            deps_upgrade_options=deps_upgrade_options,
            gitignore=gitignore,
            jest=jest,
            jest_options=jest_options,
            npmignore_enabled=npmignore_enabled,
            npm_ignore_options=npm_ignore_options,
            package=package,
            prettier=prettier,
            prettier_options=prettier_options,
            projen_dev_dependency=projen_dev_dependency,
            projenrc_js=projenrc_js,
            projenrc_js_options=projenrc_js_options,
            projen_version=projen_version,
            pull_request_template=pull_request_template,
            pull_request_template_contents=pull_request_template_contents,
            release=release,
            release_to_npm=release_to_npm,
            workflow_bootstrap_steps=workflow_bootstrap_steps,
            workflow_git_identity=workflow_git_identity,
            workflow_node_version=workflow_node_version,
            workflow_package_cache=workflow_package_cache,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            clobber=clobber,
            dev_container=dev_container,
            github=github,
            github_options=github_options,
            gitpod=gitpod,
            projen_credentials=projen_credentials,
            readme=readme,
            stale=stale,
            stale_options=stale_options,
            vscode=vscode,
            add_package_manager_to_dev_engines=add_package_manager_to_dev_engines,
            allow_library_dependencies=allow_library_dependencies,
            allow_scripts=allow_scripts,
            author_email=author_email,
            author_name=author_name,
            author_organization=author_organization,
            author_url=author_url,
            auto_detect_bin=auto_detect_bin,
            bin=bin,
            bugs_email=bugs_email,
            bugs_url=bugs_url,
            bundled_deps=bundled_deps,
            bun_version=bun_version,
            code_artifact_options=code_artifact_options,
            delete_orphaned_lock_files=delete_orphaned_lock_files,
            deps=deps,
            description=description,
            dev_deps=dev_deps,
            dev_engines=dev_engines,
            entrypoint=entrypoint,
            homepage=homepage,
            keywords=keywords,
            license=license,
            licensed=licensed,
            max_node_version=max_node_version,
            min_node_version=min_node_version,
            npm_access=npm_access,
            npm_provenance=npm_provenance,
            npm_registry_url=npm_registry_url,
            npm_token_secret=npm_token_secret,
            npm_trusted_publishing=npm_trusted_publishing,
            package_manager=package_manager,
            package_name=package_name,
            peer_dependency_options=peer_dependency_options,
            peer_deps=peer_deps,
            pnpm_options=pnpm_options,
            pnpm_version=pnpm_version,
            repository=repository,
            repository_directory=repository_directory,
            scoped_packages_options=scoped_packages_options,
            stability=stability,
            yarn_berry_options=yarn_berry_options,
            bump_package=bump_package,
            jsii_release_version=jsii_release_version,
            major_version=major_version,
            min_major_version=min_major_version,
            next_version_command=next_version_command,
            npm_dist_tag=npm_dist_tag,
            post_build_steps=post_build_steps,
            prerelease=prerelease,
            publish_dry_run=publish_dry_run,
            publish_tasks=publish_tasks,
            releasable_commits=releasable_commits,
            release_branches=release_branches,
            release_environment=release_environment,
            release_failure_issue=release_failure_issue,
            release_failure_issue_label=release_failure_issue_label,
            release_tag_prefix=release_tag_prefix,
            release_trigger=release_trigger,
            release_workflow_env=release_workflow_env,
            release_workflow_name=release_workflow_name,
            release_workflow_setup_steps=release_workflow_setup_steps,
            versionrc_options=versionrc_options,
            workflow_container_image=workflow_container_image,
            workflow_runs_on=workflow_runs_on,
            workflow_runs_on_group=workflow_runs_on_group,
            name=name,
            commit_generated=commit_generated,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            logging=logging,
            outdir=outdir,
            parent=parent,
            project_tree=project_tree,
            projen_command=projen_command,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
        )

        jsii.create(self.__class__, self, [options])


@jsii.data_type(
    jsii_type="projen.cdktf.ConstructLibraryCdktfOptions",
    jsii_struct_bases=[_cdk_bb21cefa.ConstructLibraryOptions],
    name_mapping={
        "name": "name",
        "commit_generated": "commitGenerated",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "logging": "logging",
        "outdir": "outdir",
        "parent": "parent",
        "project_tree": "projectTree",
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
        "projen_credentials": "projenCredentials",
        "readme": "readme",
        "stale": "stale",
        "stale_options": "staleOptions",
        "vscode": "vscode",
        "add_package_manager_to_dev_engines": "addPackageManagerToDevEngines",
        "allow_library_dependencies": "allowLibraryDependencies",
        "allow_scripts": "allowScripts",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "author_organization": "authorOrganization",
        "author_url": "authorUrl",
        "auto_detect_bin": "autoDetectBin",
        "bin": "bin",
        "bugs_email": "bugsEmail",
        "bugs_url": "bugsUrl",
        "bundled_deps": "bundledDeps",
        "bun_version": "bunVersion",
        "code_artifact_options": "codeArtifactOptions",
        "delete_orphaned_lock_files": "deleteOrphanedLockFiles",
        "deps": "deps",
        "description": "description",
        "dev_deps": "devDeps",
        "dev_engines": "devEngines",
        "entrypoint": "entrypoint",
        "homepage": "homepage",
        "keywords": "keywords",
        "license": "license",
        "licensed": "licensed",
        "max_node_version": "maxNodeVersion",
        "min_node_version": "minNodeVersion",
        "npm_access": "npmAccess",
        "npm_provenance": "npmProvenance",
        "npm_registry_url": "npmRegistryUrl",
        "npm_token_secret": "npmTokenSecret",
        "npm_trusted_publishing": "npmTrustedPublishing",
        "package_manager": "packageManager",
        "package_name": "packageName",
        "peer_dependency_options": "peerDependencyOptions",
        "peer_deps": "peerDeps",
        "pnpm_options": "pnpmOptions",
        "pnpm_version": "pnpmVersion",
        "repository": "repository",
        "repository_directory": "repositoryDirectory",
        "scoped_packages_options": "scopedPackagesOptions",
        "stability": "stability",
        "yarn_berry_options": "yarnBerryOptions",
        "bump_package": "bumpPackage",
        "jsii_release_version": "jsiiReleaseVersion",
        "major_version": "majorVersion",
        "min_major_version": "minMajorVersion",
        "next_version_command": "nextVersionCommand",
        "npm_dist_tag": "npmDistTag",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "publish_dry_run": "publishDryRun",
        "publish_tasks": "publishTasks",
        "releasable_commits": "releasableCommits",
        "release_branches": "releaseBranches",
        "release_environment": "releaseEnvironment",
        "release_failure_issue": "releaseFailureIssue",
        "release_failure_issue_label": "releaseFailureIssueLabel",
        "release_tag_prefix": "releaseTagPrefix",
        "release_trigger": "releaseTrigger",
        "release_workflow_env": "releaseWorkflowEnv",
        "release_workflow_name": "releaseWorkflowName",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "versionrc_options": "versionrcOptions",
        "workflow_container_image": "workflowContainerImage",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
        "artifacts_directory": "artifactsDirectory",
        "audit_deps": "auditDeps",
        "audit_deps_options": "auditDepsOptions",
        "auto_approve_upgrades": "autoApproveUpgrades",
        "biome": "biome",
        "biome_options": "biomeOptions",
        "build_workflow": "buildWorkflow",
        "build_workflow_options": "buildWorkflowOptions",
        "bundler_options": "bundlerOptions",
        "check_licenses": "checkLicenses",
        "code_cov": "codeCov",
        "code_cov_token_secret": "codeCovTokenSecret",
        "copyright_owner": "copyrightOwner",
        "copyright_period": "copyrightPeriod",
        "default_release_branch": "defaultReleaseBranch",
        "dependabot": "dependabot",
        "dependabot_options": "dependabotOptions",
        "deps_upgrade": "depsUpgrade",
        "deps_upgrade_options": "depsUpgradeOptions",
        "gitignore": "gitignore",
        "jest": "jest",
        "jest_options": "jestOptions",
        "npmignore_enabled": "npmignoreEnabled",
        "npm_ignore_options": "npmIgnoreOptions",
        "package": "package",
        "prettier": "prettier",
        "prettier_options": "prettierOptions",
        "projen_dev_dependency": "projenDevDependency",
        "projenrc_js": "projenrcJs",
        "projenrc_js_options": "projenrcJsOptions",
        "projen_version": "projenVersion",
        "pull_request_template": "pullRequestTemplate",
        "pull_request_template_contents": "pullRequestTemplateContents",
        "release": "release",
        "release_to_npm": "releaseToNpm",
        "workflow_bootstrap_steps": "workflowBootstrapSteps",
        "workflow_git_identity": "workflowGitIdentity",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_package_cache": "workflowPackageCache",
        "disable_tsconfig": "disableTsconfig",
        "disable_tsconfig_dev": "disableTsconfigDev",
        "docgen": "docgen",
        "docs_directory": "docsDirectory",
        "entrypoint_types": "entrypointTypes",
        "eslint": "eslint",
        "eslint_options": "eslintOptions",
        "libdir": "libdir",
        "projenrc_ts": "projenrcTs",
        "projenrc_ts_options": "projenrcTsOptions",
        "runner": "runner",
        "sample_code": "sampleCode",
        "srcdir": "srcdir",
        "testdir": "testdir",
        "tsconfig": "tsconfig",
        "tsconfig_dev": "tsconfigDev",
        "tsconfig_dev_file": "tsconfigDevFile",
        "ts_jest_options": "tsJestOptions",
        "typescript_version": "typescriptVersion",
        "author": "author",
        "author_address": "authorAddress",
        "repository_url": "repositoryUrl",
        "compat": "compat",
        "compat_ignore": "compatIgnore",
        "compress_assembly": "compressAssembly",
        "docgen_file_path": "docgenFilePath",
        "exclude_typescript": "excludeTypescript",
        "jsii_version": "jsiiVersion",
        "publish_to_go": "publishToGo",
        "publish_to_maven": "publishToMaven",
        "publish_to_nuget": "publishToNuget",
        "publish_to_pypi": "publishToPypi",
        "rootdir": "rootdir",
        "validate_tsconfig": "validateTsconfig",
        "catalog": "catalog",
        "cdktf_version": "cdktfVersion",
        "constructs_version": "constructsVersion",
    },
)
class ConstructLibraryCdktfOptions(_cdk_bb21cefa.ConstructLibraryOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union["_projen_04054675.IgnoreFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union["_projen_04054675.GitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union["_projen_04054675.LoggerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional["_projen_04054675.Project"] = None,
        project_tree: typing.Optional[builtins.bool] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union["_projen_04054675.ProjenrcJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union["_projen_04054675.RenovatebotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_options: typing.Optional[typing.Union["_github_c49f935d.AutoApproveOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union["_github_c49f935d.AutoMergeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union["_github_c49f935d.GitHubOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        projen_credentials: typing.Optional["_github_c49f935d.GithubCredentials"] = None,
        readme: typing.Optional[typing.Union["_projen_04054675.SampleReadmeProps", typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union["_github_c49f935d.StaleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        add_package_manager_to_dev_engines: typing.Optional[builtins.bool] = None,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        allow_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bun_version: typing.Optional[builtins.str] = None,
        code_artifact_options: typing.Optional[typing.Union["_javascript_eb5dbe11.CodeArtifactOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_orphaned_lock_files: typing.Optional[builtins.bool] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        dev_engines: typing.Optional[typing.Union["_javascript_eb5dbe11.DevEngines", typing.Dict[builtins.str, typing.Any]]] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        npm_access: typing.Optional["_javascript_eb5dbe11.NpmAccess"] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        npm_trusted_publishing: typing.Optional[builtins.bool] = None,
        package_manager: typing.Optional["_javascript_eb5dbe11.NodePackageManager"] = None,
        package_name: typing.Optional[builtins.str] = None,
        peer_dependency_options: typing.Optional[typing.Union["_javascript_eb5dbe11.PeerDependencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_options: typing.Optional[typing.Union["_javascript_eb5dbe11.PnpmOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union["_javascript_eb5dbe11.ScopedPackagesOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        stability: typing.Optional[builtins.str] = None,
        yarn_berry_options: typing.Optional[typing.Union["_javascript_eb5dbe11.YarnBerryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        bump_package: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union["_workflows_2b7f1587.JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional["_projen_04054675.ReleasableCommits"] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union["_release_1fa091fd.BranchOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        release_environment: typing.Optional[builtins.str] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional["_release_1fa091fd.ReleaseTrigger"] = None,
        release_workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union["_workflows_2b7f1587.JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union["_projen_04054675.GroupRunnerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        audit_deps: typing.Optional[builtins.bool] = None,
        audit_deps_options: typing.Optional[typing.Union["_javascript_eb5dbe11.AuditOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        biome: typing.Optional[builtins.bool] = None,
        biome_options: typing.Optional[typing.Union["_javascript_eb5dbe11.BiomeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union["_javascript_eb5dbe11.BuildWorkflowOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        bundler_options: typing.Optional[typing.Union["_javascript_eb5dbe11.BundlerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        check_licenses: typing.Optional[typing.Union["_javascript_eb5dbe11.LicenseCheckerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union["_github_c49f935d.DependabotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union["_javascript_eb5dbe11.UpgradeDependenciesOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union["_javascript_eb5dbe11.JestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union["_projen_04054675.IgnoreFileOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        package: typing.Optional[builtins.bool] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union["_javascript_eb5dbe11.PrettierOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_js_options: typing.Optional[typing.Union["_javascript_eb5dbe11.ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_version: typing.Optional[builtins.str] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        release: typing.Optional[builtins.bool] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union["_workflows_2b7f1587.JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_git_identity: typing.Optional[typing.Union["_github_c49f935d.GitIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        disable_tsconfig: typing.Optional[builtins.bool] = None,
        disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
        docgen: typing.Optional[builtins.bool] = None,
        docs_directory: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union["_javascript_eb5dbe11.EslintOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        libdir: typing.Optional[builtins.str] = None,
        projenrc_ts: typing.Optional[builtins.bool] = None,
        projenrc_ts_options: typing.Optional[typing.Union["_typescript_7a66cf84.ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        runner: typing.Optional["_typescript_7a66cf84.TypeScriptRunner"] = None,
        sample_code: typing.Optional[builtins.bool] = None,
        srcdir: typing.Optional[builtins.str] = None,
        testdir: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[typing.Union["_javascript_eb5dbe11.TypescriptConfigOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev: typing.Optional[typing.Union["_javascript_eb5dbe11.TypescriptConfigOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev_file: typing.Optional[builtins.str] = None,
        ts_jest_options: typing.Optional[typing.Union["_typescript_7a66cf84.TsJestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        typescript_version: typing.Optional[builtins.str] = None,
        author: builtins.str,
        author_address: builtins.str,
        repository_url: builtins.str,
        compat: typing.Optional[builtins.bool] = None,
        compat_ignore: typing.Optional[builtins.str] = None,
        compress_assembly: typing.Optional[builtins.bool] = None,
        docgen_file_path: typing.Optional[builtins.str] = None,
        exclude_typescript: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsii_version: typing.Optional[builtins.str] = None,
        publish_to_go: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiGoTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_maven: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiJavaTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_nuget: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiDotNetTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_to_pypi: typing.Optional[typing.Union["_cdk_bb21cefa.JsiiPythonTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        rootdir: typing.Optional[builtins.str] = None,
        validate_tsconfig: typing.Optional["_cdk_bb21cefa.ValidateTsconfig"] = None,
        catalog: typing.Optional[typing.Union["_cdk_bb21cefa.Catalog", typing.Dict[builtins.str, typing.Any]]] = None,
        cdktf_version: builtins.str,
        constructs_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param project_tree: (experimental) Generate a project tree file (``.projen/tree.json``) that shows all components and their relationships. Useful for understanding your project structure and debugging. Default: false
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
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param add_package_manager_to_dev_engines: (experimental) Automatically add the resolved ``packageManager`` to ``devEngines.packageManager`` in ``package.json``, setting ``onFail`` to ``ignore``. Default: true
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param allow_scripts: (experimental) List of dependency (package) names that are allowed to run lifecycle install scripts (``preinstall``, ``install``, ``postinstall``, ``prepare``) during dependency installation. These scripts can execute arbitrary code, making them a common supply-chain attack vector. Package managers are moving toward blocking them by default and requiring an explicit allowlist. Configuring ``allowScripts`` sets up that allowlist so scripts only run for the packages you have explicitly reviewed and trust. Support for this setting depends on the configured ``packageManager``: - ``NPM``: written to the native ``allowScripts`` field in ``package.json`` (requires npm >= 11.16; see https://docs.npmjs.com/cli/v11/commands/npm-approve-scripts). - ``BUN``: written to the native ``trustedDependencies`` field in ``package.json`` (see https://bun.com/docs/pm/lifecycle). - ``PNPM``: written to the ``onlyBuiltDependencies`` setting in ``pnpm-workspace.yaml`` (see https://pnpm.io/settings#onlybuiltdependencies). - ``YARN2``, ``YARN_BERRY``: written to the native ``dependenciesMeta.<pkg>.built`` allowlist in ``package.json``, combined with ``enableScripts: false`` in ``.yarnrc.yml`` (see https://yarnpkg.com/features/security#postinstalls). If you set ``yarnBerryOptions.yarnRcOptions.enableScripts`` explicitly, that value is respected instead of being overridden. - ``YARN``, ``YARN_CLASSIC``: not supported. Yarn Classic has no native mechanism to allowlist install scripts for specific dependencies. Setting this option with one of these package managers throws an error at synthesis time. Default: - all install scripts are allowed to run (package manager default)
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and this will be what your ``package.json`` will eventually include.
        :param bun_version: (experimental) The version of Bun to use if using Bun as a package manager. Default: "latest"
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param delete_orphaned_lock_files: (experimental) Automatically delete lockfiles from package managers that are not the active one. Only triggered when the lockfile for the configured package manager already exists. This is useful when migrating between package managers to avoid conflicts. Default: true
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and this will be what your ``package.json`` will eventually include. Default: []
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and this will be what your ``package.json`` will eventually include. Default: []
        :param dev_engines: (experimental) Configure the ``devEngines`` field in ``package.json``. The ``devEngines.packageManager`` field is automatically populated based on the resolved ``packageManager`` value. Any fields provided here are merged with the auto-populated ``packageManager`` entry.
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json Default: "lib/index.js"
        :param homepage: (experimental) Package's Homepage / Website.
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param max_node_version: (experimental) The maximum node version supported by this package. Most projects should not use this option. The value indicates that the package is incompatible with any newer versions of node. This requirement is enforced via the engines field. You will normally not need to set this option. Consider this option only if your package is known to not function with newer versions of node. Default: - no maximum version is enforced
        :param min_node_version: (experimental) The minimum node version required by this package to function. Most projects should not use this option. The value indicates that the package is incompatible with any older versions of node. This requirement is enforced via the engines field. You will normally not need to set this option, even if your package is incompatible with EOL versions of node. Consider this option only if your package depends on a specific feature, that is not available in other LTS versions. Setting this option has very high impact on the consumers of your package, as package managers will actively prevent usage with node versions you have marked as incompatible. To change the node version of your CI/CD workflows, use ``workflowNodeVersion``. Default: - no minimum version is enforced
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_provenance: (experimental) Should provenance statements be generated when the package is published. A supported package manager is required to publish a package with npm provenance statements and you will need to use a supported CI/CD provider. Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - true for public packages, false otherwise
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param npm_trusted_publishing: (experimental) Use trusted publishing for publishing to npmjs.com Needs to be pre-configured on npm.js to work. Default: - false
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: - Detected from the calling process or ``YARN_CLASSIC`` if detection fails.
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_options: (experimental) Options for pnpm. Default: - all default options
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "10.33.0"
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param stability: (experimental) Package's Stability.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: - A recent version of "commit-and-tag-version"
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. This setting cannot be specified together with ``minMajorVersion``; the invoked script can be used to achieve the effects of ``minMajorVersion``. Default: - The next version will be determined based on the commit history and project settings.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_environment: (experimental) The GitHub Actions environment used for the release. This can be used to add an explicit approval step to the release or limit who can initiate a release through environment protection rules. When multiple artifacts are released, the environment can be overwritten on a per artifact basis. Default: - no environment used, unless set at the artifact level
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_env: (experimental) Build environment variables for release workflows. Default: {}
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with commit-and-tag-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param audit_deps: (experimental) Run security audit on dependencies. When enabled, creates an "audit" task that checks for known security vulnerabilities in dependencies. By default, runs during every build and checks for "high" severity vulnerabilities or above in all dependencies (including dev dependencies). Default: false
        :param audit_deps_options: (experimental) Security audit options. Default: - default options
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configured). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param biome: (experimental) Setup Biome. Default: false
        :param biome_options: (experimental) Biome options. Default: - default options
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v5 By default, OIDC auth is used. Alternatively a token can be provided via ``codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token. Default: - OIDC auth is used
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: - ``true`` for root projects, ``false`` for subprojects
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: - true if not a subproject
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - default GitHub Actions user
        :param workflow_node_version: (experimental) The node version used in GitHub Actions workflows. Always use this option if your GitHub Actions workflows require a specific to run. Default: - ``minNodeVersion`` if set, otherwise ``lts/*``.
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param disable_tsconfig: (experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler). Default: false
        :param disable_tsconfig_dev: (experimental) Do not generate a development tsconfig file. Default: false
        :param docgen: (experimental) Docgen by Typedoc. Default: false
        :param docs_directory: (experimental) Docs directory. Default: "docs"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: - true, unless biome is enabled
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param libdir: (experimental) Typescript artifacts output directory. Default: "lib"
        :param projenrc_ts: (experimental) Use TypeScript for your projenrc file (``.projenrc.ts``). Default: false
        :param projenrc_ts_options: (experimental) Options for .projenrc.ts.
        :param runner: (experimental) The TypeScript runner to use for executing TypeScript files. This is a project-level setting that components (e.g. projenrc) will use as their default runner. Default: TypeScriptRunner.tsNode()
        :param sample_code: (experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there. Default: true
        :param srcdir: (experimental) Typescript sources directory. Default: "src"
        :param testdir: (experimental) Jest tests directory. Tests files should be named ``xxx.test.ts``. If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``), then tests are going to be compiled into ``lib/`` and executed as javascript. If the test directory is outside of ``src``, then we configure jest to compile the code in-memory. Default: "test"
        :param tsconfig: (experimental) Custom TSConfig. Default: - default options
        :param tsconfig_dev: (experimental) Custom tsconfig options for the development tsconfig.json file (used for testing). Default: - use the production tsconfig options
        :param tsconfig_dev_file: (experimental) The name (and path) of the development tsconfig file. By default this lives inside the test directory (e.g. ``test/tsconfig.json``) so that the TypeScript language service resolves it as the nearest config for test files. Default: - "{testdir}/tsconfig.json"
        :param ts_jest_options: (experimental) Options for ts-jest.
        :param typescript_version: (experimental) TypeScript version to use. NOTE: Typescript is not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``). Default: "latest"
        :param author: (experimental) The name of the library author. Default: $GIT_USER_NAME
        :param author_address: (experimental) Email or URL of the library author. Default: $GIT_USER_EMAIL
        :param repository_url: (experimental) Git repository URL. Default: $GIT_REMOTE
        :param compat: (experimental) Automatically run API compatibility test against the latest version published to npm after compilation. - You can manually run compatibility tests using ``yarn compat`` if this feature is disabled. - You can ignore compatibility failures by adding lines to a ".compatignore" file. Default: false
        :param compat_ignore: (experimental) Name of the ignore file for API compatibility tests. Default: ".compatignore"
        :param compress_assembly: (experimental) Emit a compressed version of the assembly. Default: false
        :param docgen_file_path: (experimental) File path for generated docs. Default: "API.md"
        :param exclude_typescript: (experimental) Accepts a list of glob patterns. Files matching any of those patterns will be excluded from the TypeScript compiler input. By default, jsii will include all *.ts files (except .d.ts files) in the TypeScript compiler input. This can be problematic for example when the package's build or test procedure generates .ts files that cannot be compiled with jsii's compiler settings.
        :param jsii_version: (experimental) Version of the jsii compiler to use. Set to "*" if you want to manually manage the version of jsii in your project by managing updates to ``package.json`` on your own. NOTE: The jsii compiler releases since 5.0.0 are not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~5.0.0``). Default: "~5.9.0"
        :param publish_to_go: (experimental) Publish Go bindings to a git repository. Default: - no publishing
        :param publish_to_maven: (experimental) Publish to maven. Default: - no publishing
        :param publish_to_nuget: (experimental) Publish to NuGet. Default: - no publishing
        :param publish_to_pypi: (experimental) Publish to pypi. Default: - no publishing
        :param rootdir: Default: "."
        :param validate_tsconfig: (experimental) Level of tsconfig validation jsii should perform on the user-provided tsconfig. Only relevant when the project synthesizes its own tsconfig (i.e. ``disableTsconfig`` is not set on the TypeScriptProject). Default: ValidateTsconfig.STRICT
        :param catalog: (experimental) Libraries will be picked up by the construct catalog when they are published to npm as jsii modules and will be published under:. https://awscdk.io/packages/[@SCOPE/]PACKAGE@VERSION The catalog will also post a tweet to https://twitter.com/awscdkio with the package name, description and the above link. You can disable these tweets through ``{ announce: false }``. You can also add a Twitter handle through ``{ twitter: 'xx' }`` which will be mentioned in the tweet. Default: - new version will be announced
        :param cdktf_version: (experimental) Minimum target version this library is tested against. Default: "^0.13.0"
        :param constructs_version: (experimental) Construct version to use. Default: "^10.3.0"

        :stability: experimental
        '''
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _github_c49f935d.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _github_c49f935d.AutoMergeOptions(**auto_merge_options)
        if isinstance(github_options, dict):
            github_options = _github_c49f935d.GitHubOptions(**github_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(stale_options, dict):
            stale_options = _github_c49f935d.StaleOptions(**stale_options)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = _javascript_eb5dbe11.CodeArtifactOptions(**code_artifact_options)
        if isinstance(dev_engines, dict):
            dev_engines = _javascript_eb5dbe11.DevEngines(**dev_engines)
        if isinstance(peer_dependency_options, dict):
            peer_dependency_options = _javascript_eb5dbe11.PeerDependencyOptions(**peer_dependency_options)
        if isinstance(pnpm_options, dict):
            pnpm_options = _javascript_eb5dbe11.PnpmOptions(**pnpm_options)
        if isinstance(yarn_berry_options, dict):
            yarn_berry_options = _javascript_eb5dbe11.YarnBerryOptions(**yarn_berry_options)
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _projen_04054675.GroupRunnerOptions(**workflow_runs_on_group)
        if isinstance(audit_deps_options, dict):
            audit_deps_options = _javascript_eb5dbe11.AuditOptions(**audit_deps_options)
        if isinstance(biome_options, dict):
            biome_options = _javascript_eb5dbe11.BiomeOptions(**biome_options)
        if isinstance(build_workflow_options, dict):
            build_workflow_options = _javascript_eb5dbe11.BuildWorkflowOptions(**build_workflow_options)
        if isinstance(bundler_options, dict):
            bundler_options = _javascript_eb5dbe11.BundlerOptions(**bundler_options)
        if isinstance(check_licenses, dict):
            check_licenses = _javascript_eb5dbe11.LicenseCheckerOptions(**check_licenses)
        if isinstance(dependabot_options, dict):
            dependabot_options = _github_c49f935d.DependabotOptions(**dependabot_options)
        if isinstance(deps_upgrade_options, dict):
            deps_upgrade_options = _javascript_eb5dbe11.UpgradeDependenciesOptions(**deps_upgrade_options)
        if isinstance(jest_options, dict):
            jest_options = _javascript_eb5dbe11.JestOptions(**jest_options)
        if isinstance(npm_ignore_options, dict):
            npm_ignore_options = _projen_04054675.IgnoreFileOptions(**npm_ignore_options)
        if isinstance(prettier_options, dict):
            prettier_options = _javascript_eb5dbe11.PrettierOptions(**prettier_options)
        if isinstance(projenrc_js_options, dict):
            projenrc_js_options = _javascript_eb5dbe11.ProjenrcOptions(**projenrc_js_options)
        if isinstance(workflow_git_identity, dict):
            workflow_git_identity = _github_c49f935d.GitIdentity(**workflow_git_identity)
        if isinstance(eslint_options, dict):
            eslint_options = _javascript_eb5dbe11.EslintOptions(**eslint_options)
        if isinstance(projenrc_ts_options, dict):
            projenrc_ts_options = _typescript_7a66cf84.ProjenrcOptions(**projenrc_ts_options)
        if isinstance(tsconfig, dict):
            tsconfig = _javascript_eb5dbe11.TypescriptConfigOptions(**tsconfig)
        if isinstance(tsconfig_dev, dict):
            tsconfig_dev = _javascript_eb5dbe11.TypescriptConfigOptions(**tsconfig_dev)
        if isinstance(ts_jest_options, dict):
            ts_jest_options = _typescript_7a66cf84.TsJestOptions(**ts_jest_options)
        if isinstance(publish_to_go, dict):
            publish_to_go = _cdk_bb21cefa.JsiiGoTarget(**publish_to_go)
        if isinstance(publish_to_maven, dict):
            publish_to_maven = _cdk_bb21cefa.JsiiJavaTarget(**publish_to_maven)
        if isinstance(publish_to_nuget, dict):
            publish_to_nuget = _cdk_bb21cefa.JsiiDotNetTarget(**publish_to_nuget)
        if isinstance(publish_to_pypi, dict):
            publish_to_pypi = _cdk_bb21cefa.JsiiPythonTarget(**publish_to_pypi)
        if isinstance(catalog, dict):
            catalog = _cdk_bb21cefa.Catalog(**catalog)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bbf02af18148d47e66a6d0672a809602f782953da7a849545a808c276a58ff4d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument project_tree", value=project_tree, expected_type=type_hints["project_tree"])
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
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument add_package_manager_to_dev_engines", value=add_package_manager_to_dev_engines, expected_type=type_hints["add_package_manager_to_dev_engines"])
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument allow_scripts", value=allow_scripts, expected_type=type_hints["allow_scripts"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument author_organization", value=author_organization, expected_type=type_hints["author_organization"])
            check_type(argname="argument author_url", value=author_url, expected_type=type_hints["author_url"])
            check_type(argname="argument auto_detect_bin", value=auto_detect_bin, expected_type=type_hints["auto_detect_bin"])
            check_type(argname="argument bin", value=bin, expected_type=type_hints["bin"])
            check_type(argname="argument bugs_email", value=bugs_email, expected_type=type_hints["bugs_email"])
            check_type(argname="argument bugs_url", value=bugs_url, expected_type=type_hints["bugs_url"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument bun_version", value=bun_version, expected_type=type_hints["bun_version"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument delete_orphaned_lock_files", value=delete_orphaned_lock_files, expected_type=type_hints["delete_orphaned_lock_files"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument dev_engines", value=dev_engines, expected_type=type_hints["dev_engines"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument licensed", value=licensed, expected_type=type_hints["licensed"])
            check_type(argname="argument max_node_version", value=max_node_version, expected_type=type_hints["max_node_version"])
            check_type(argname="argument min_node_version", value=min_node_version, expected_type=type_hints["min_node_version"])
            check_type(argname="argument npm_access", value=npm_access, expected_type=type_hints["npm_access"])
            check_type(argname="argument npm_provenance", value=npm_provenance, expected_type=type_hints["npm_provenance"])
            check_type(argname="argument npm_registry_url", value=npm_registry_url, expected_type=type_hints["npm_registry_url"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument npm_trusted_publishing", value=npm_trusted_publishing, expected_type=type_hints["npm_trusted_publishing"])
            check_type(argname="argument package_manager", value=package_manager, expected_type=type_hints["package_manager"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument peer_dependency_options", value=peer_dependency_options, expected_type=type_hints["peer_dependency_options"])
            check_type(argname="argument peer_deps", value=peer_deps, expected_type=type_hints["peer_deps"])
            check_type(argname="argument pnpm_options", value=pnpm_options, expected_type=type_hints["pnpm_options"])
            check_type(argname="argument pnpm_version", value=pnpm_version, expected_type=type_hints["pnpm_version"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_directory", value=repository_directory, expected_type=type_hints["repository_directory"])
            check_type(argname="argument scoped_packages_options", value=scoped_packages_options, expected_type=type_hints["scoped_packages_options"])
            check_type(argname="argument stability", value=stability, expected_type=type_hints["stability"])
            check_type(argname="argument yarn_berry_options", value=yarn_berry_options, expected_type=type_hints["yarn_berry_options"])
            check_type(argname="argument bump_package", value=bump_package, expected_type=type_hints["bump_package"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument next_version_command", value=next_version_command, expected_type=type_hints["next_version_command"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument publish_dry_run", value=publish_dry_run, expected_type=type_hints["publish_dry_run"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument release_branches", value=release_branches, expected_type=type_hints["release_branches"])
            check_type(argname="argument release_environment", value=release_environment, expected_type=type_hints["release_environment"])
            check_type(argname="argument release_failure_issue", value=release_failure_issue, expected_type=type_hints["release_failure_issue"])
            check_type(argname="argument release_failure_issue_label", value=release_failure_issue_label, expected_type=type_hints["release_failure_issue_label"])
            check_type(argname="argument release_tag_prefix", value=release_tag_prefix, expected_type=type_hints["release_tag_prefix"])
            check_type(argname="argument release_trigger", value=release_trigger, expected_type=type_hints["release_trigger"])
            check_type(argname="argument release_workflow_env", value=release_workflow_env, expected_type=type_hints["release_workflow_env"])
            check_type(argname="argument release_workflow_name", value=release_workflow_name, expected_type=type_hints["release_workflow_name"])
            check_type(argname="argument release_workflow_setup_steps", value=release_workflow_setup_steps, expected_type=type_hints["release_workflow_setup_steps"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument audit_deps", value=audit_deps, expected_type=type_hints["audit_deps"])
            check_type(argname="argument audit_deps_options", value=audit_deps_options, expected_type=type_hints["audit_deps_options"])
            check_type(argname="argument auto_approve_upgrades", value=auto_approve_upgrades, expected_type=type_hints["auto_approve_upgrades"])
            check_type(argname="argument biome", value=biome, expected_type=type_hints["biome"])
            check_type(argname="argument biome_options", value=biome_options, expected_type=type_hints["biome_options"])
            check_type(argname="argument build_workflow", value=build_workflow, expected_type=type_hints["build_workflow"])
            check_type(argname="argument build_workflow_options", value=build_workflow_options, expected_type=type_hints["build_workflow_options"])
            check_type(argname="argument bundler_options", value=bundler_options, expected_type=type_hints["bundler_options"])
            check_type(argname="argument check_licenses", value=check_licenses, expected_type=type_hints["check_licenses"])
            check_type(argname="argument code_cov", value=code_cov, expected_type=type_hints["code_cov"])
            check_type(argname="argument code_cov_token_secret", value=code_cov_token_secret, expected_type=type_hints["code_cov_token_secret"])
            check_type(argname="argument copyright_owner", value=copyright_owner, expected_type=type_hints["copyright_owner"])
            check_type(argname="argument copyright_period", value=copyright_period, expected_type=type_hints["copyright_period"])
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument dependabot", value=dependabot, expected_type=type_hints["dependabot"])
            check_type(argname="argument dependabot_options", value=dependabot_options, expected_type=type_hints["dependabot_options"])
            check_type(argname="argument deps_upgrade", value=deps_upgrade, expected_type=type_hints["deps_upgrade"])
            check_type(argname="argument deps_upgrade_options", value=deps_upgrade_options, expected_type=type_hints["deps_upgrade_options"])
            check_type(argname="argument gitignore", value=gitignore, expected_type=type_hints["gitignore"])
            check_type(argname="argument jest", value=jest, expected_type=type_hints["jest"])
            check_type(argname="argument jest_options", value=jest_options, expected_type=type_hints["jest_options"])
            check_type(argname="argument npmignore_enabled", value=npmignore_enabled, expected_type=type_hints["npmignore_enabled"])
            check_type(argname="argument npm_ignore_options", value=npm_ignore_options, expected_type=type_hints["npm_ignore_options"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument prettier", value=prettier, expected_type=type_hints["prettier"])
            check_type(argname="argument prettier_options", value=prettier_options, expected_type=type_hints["prettier_options"])
            check_type(argname="argument projen_dev_dependency", value=projen_dev_dependency, expected_type=type_hints["projen_dev_dependency"])
            check_type(argname="argument projenrc_js", value=projenrc_js, expected_type=type_hints["projenrc_js"])
            check_type(argname="argument projenrc_js_options", value=projenrc_js_options, expected_type=type_hints["projenrc_js_options"])
            check_type(argname="argument projen_version", value=projen_version, expected_type=type_hints["projen_version"])
            check_type(argname="argument pull_request_template", value=pull_request_template, expected_type=type_hints["pull_request_template"])
            check_type(argname="argument pull_request_template_contents", value=pull_request_template_contents, expected_type=type_hints["pull_request_template_contents"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument release_to_npm", value=release_to_npm, expected_type=type_hints["release_to_npm"])
            check_type(argname="argument workflow_bootstrap_steps", value=workflow_bootstrap_steps, expected_type=type_hints["workflow_bootstrap_steps"])
            check_type(argname="argument workflow_git_identity", value=workflow_git_identity, expected_type=type_hints["workflow_git_identity"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_package_cache", value=workflow_package_cache, expected_type=type_hints["workflow_package_cache"])
            check_type(argname="argument disable_tsconfig", value=disable_tsconfig, expected_type=type_hints["disable_tsconfig"])
            check_type(argname="argument disable_tsconfig_dev", value=disable_tsconfig_dev, expected_type=type_hints["disable_tsconfig_dev"])
            check_type(argname="argument docgen", value=docgen, expected_type=type_hints["docgen"])
            check_type(argname="argument docs_directory", value=docs_directory, expected_type=type_hints["docs_directory"])
            check_type(argname="argument entrypoint_types", value=entrypoint_types, expected_type=type_hints["entrypoint_types"])
            check_type(argname="argument eslint", value=eslint, expected_type=type_hints["eslint"])
            check_type(argname="argument eslint_options", value=eslint_options, expected_type=type_hints["eslint_options"])
            check_type(argname="argument libdir", value=libdir, expected_type=type_hints["libdir"])
            check_type(argname="argument projenrc_ts", value=projenrc_ts, expected_type=type_hints["projenrc_ts"])
            check_type(argname="argument projenrc_ts_options", value=projenrc_ts_options, expected_type=type_hints["projenrc_ts_options"])
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
            check_type(argname="argument sample_code", value=sample_code, expected_type=type_hints["sample_code"])
            check_type(argname="argument srcdir", value=srcdir, expected_type=type_hints["srcdir"])
            check_type(argname="argument testdir", value=testdir, expected_type=type_hints["testdir"])
            check_type(argname="argument tsconfig", value=tsconfig, expected_type=type_hints["tsconfig"])
            check_type(argname="argument tsconfig_dev", value=tsconfig_dev, expected_type=type_hints["tsconfig_dev"])
            check_type(argname="argument tsconfig_dev_file", value=tsconfig_dev_file, expected_type=type_hints["tsconfig_dev_file"])
            check_type(argname="argument ts_jest_options", value=ts_jest_options, expected_type=type_hints["ts_jest_options"])
            check_type(argname="argument typescript_version", value=typescript_version, expected_type=type_hints["typescript_version"])
            check_type(argname="argument author", value=author, expected_type=type_hints["author"])
            check_type(argname="argument author_address", value=author_address, expected_type=type_hints["author_address"])
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument compat", value=compat, expected_type=type_hints["compat"])
            check_type(argname="argument compat_ignore", value=compat_ignore, expected_type=type_hints["compat_ignore"])
            check_type(argname="argument compress_assembly", value=compress_assembly, expected_type=type_hints["compress_assembly"])
            check_type(argname="argument docgen_file_path", value=docgen_file_path, expected_type=type_hints["docgen_file_path"])
            check_type(argname="argument exclude_typescript", value=exclude_typescript, expected_type=type_hints["exclude_typescript"])
            check_type(argname="argument jsii_version", value=jsii_version, expected_type=type_hints["jsii_version"])
            check_type(argname="argument publish_to_go", value=publish_to_go, expected_type=type_hints["publish_to_go"])
            check_type(argname="argument publish_to_maven", value=publish_to_maven, expected_type=type_hints["publish_to_maven"])
            check_type(argname="argument publish_to_nuget", value=publish_to_nuget, expected_type=type_hints["publish_to_nuget"])
            check_type(argname="argument publish_to_pypi", value=publish_to_pypi, expected_type=type_hints["publish_to_pypi"])
            check_type(argname="argument rootdir", value=rootdir, expected_type=type_hints["rootdir"])
            check_type(argname="argument validate_tsconfig", value=validate_tsconfig, expected_type=type_hints["validate_tsconfig"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument cdktf_version", value=cdktf_version, expected_type=type_hints["cdktf_version"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "author": author,
            "author_address": author_address,
            "repository_url": repository_url,
            "cdktf_version": cdktf_version,
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
        if project_tree is not None:
            self._values["project_tree"] = project_tree
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
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if readme is not None:
            self._values["readme"] = readme
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if vscode is not None:
            self._values["vscode"] = vscode
        if add_package_manager_to_dev_engines is not None:
            self._values["add_package_manager_to_dev_engines"] = add_package_manager_to_dev_engines
        if allow_library_dependencies is not None:
            self._values["allow_library_dependencies"] = allow_library_dependencies
        if allow_scripts is not None:
            self._values["allow_scripts"] = allow_scripts
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if author_organization is not None:
            self._values["author_organization"] = author_organization
        if author_url is not None:
            self._values["author_url"] = author_url
        if auto_detect_bin is not None:
            self._values["auto_detect_bin"] = auto_detect_bin
        if bin is not None:
            self._values["bin"] = bin
        if bugs_email is not None:
            self._values["bugs_email"] = bugs_email
        if bugs_url is not None:
            self._values["bugs_url"] = bugs_url
        if bundled_deps is not None:
            self._values["bundled_deps"] = bundled_deps
        if bun_version is not None:
            self._values["bun_version"] = bun_version
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if delete_orphaned_lock_files is not None:
            self._values["delete_orphaned_lock_files"] = delete_orphaned_lock_files
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if dev_engines is not None:
            self._values["dev_engines"] = dev_engines
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if homepage is not None:
            self._values["homepage"] = homepage
        if keywords is not None:
            self._values["keywords"] = keywords
        if license is not None:
            self._values["license"] = license
        if licensed is not None:
            self._values["licensed"] = licensed
        if max_node_version is not None:
            self._values["max_node_version"] = max_node_version
        if min_node_version is not None:
            self._values["min_node_version"] = min_node_version
        if npm_access is not None:
            self._values["npm_access"] = npm_access
        if npm_provenance is not None:
            self._values["npm_provenance"] = npm_provenance
        if npm_registry_url is not None:
            self._values["npm_registry_url"] = npm_registry_url
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if npm_trusted_publishing is not None:
            self._values["npm_trusted_publishing"] = npm_trusted_publishing
        if package_manager is not None:
            self._values["package_manager"] = package_manager
        if package_name is not None:
            self._values["package_name"] = package_name
        if peer_dependency_options is not None:
            self._values["peer_dependency_options"] = peer_dependency_options
        if peer_deps is not None:
            self._values["peer_deps"] = peer_deps
        if pnpm_options is not None:
            self._values["pnpm_options"] = pnpm_options
        if pnpm_version is not None:
            self._values["pnpm_version"] = pnpm_version
        if repository is not None:
            self._values["repository"] = repository
        if repository_directory is not None:
            self._values["repository_directory"] = repository_directory
        if scoped_packages_options is not None:
            self._values["scoped_packages_options"] = scoped_packages_options
        if stability is not None:
            self._values["stability"] = stability
        if yarn_berry_options is not None:
            self._values["yarn_berry_options"] = yarn_berry_options
        if bump_package is not None:
            self._values["bump_package"] = bump_package
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if major_version is not None:
            self._values["major_version"] = major_version
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if next_version_command is not None:
            self._values["next_version_command"] = next_version_command
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if publish_dry_run is not None:
            self._values["publish_dry_run"] = publish_dry_run
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_environment is not None:
            self._values["release_environment"] = release_environment
        if release_failure_issue is not None:
            self._values["release_failure_issue"] = release_failure_issue
        if release_failure_issue_label is not None:
            self._values["release_failure_issue_label"] = release_failure_issue_label
        if release_tag_prefix is not None:
            self._values["release_tag_prefix"] = release_tag_prefix
        if release_trigger is not None:
            self._values["release_trigger"] = release_trigger
        if release_workflow_env is not None:
            self._values["release_workflow_env"] = release_workflow_env
        if release_workflow_name is not None:
            self._values["release_workflow_name"] = release_workflow_name
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if audit_deps is not None:
            self._values["audit_deps"] = audit_deps
        if audit_deps_options is not None:
            self._values["audit_deps_options"] = audit_deps_options
        if auto_approve_upgrades is not None:
            self._values["auto_approve_upgrades"] = auto_approve_upgrades
        if biome is not None:
            self._values["biome"] = biome
        if biome_options is not None:
            self._values["biome_options"] = biome_options
        if build_workflow is not None:
            self._values["build_workflow"] = build_workflow
        if build_workflow_options is not None:
            self._values["build_workflow_options"] = build_workflow_options
        if bundler_options is not None:
            self._values["bundler_options"] = bundler_options
        if check_licenses is not None:
            self._values["check_licenses"] = check_licenses
        if code_cov is not None:
            self._values["code_cov"] = code_cov
        if code_cov_token_secret is not None:
            self._values["code_cov_token_secret"] = code_cov_token_secret
        if copyright_owner is not None:
            self._values["copyright_owner"] = copyright_owner
        if copyright_period is not None:
            self._values["copyright_period"] = copyright_period
        if default_release_branch is not None:
            self._values["default_release_branch"] = default_release_branch
        if dependabot is not None:
            self._values["dependabot"] = dependabot
        if dependabot_options is not None:
            self._values["dependabot_options"] = dependabot_options
        if deps_upgrade is not None:
            self._values["deps_upgrade"] = deps_upgrade
        if deps_upgrade_options is not None:
            self._values["deps_upgrade_options"] = deps_upgrade_options
        if gitignore is not None:
            self._values["gitignore"] = gitignore
        if jest is not None:
            self._values["jest"] = jest
        if jest_options is not None:
            self._values["jest_options"] = jest_options
        if npmignore_enabled is not None:
            self._values["npmignore_enabled"] = npmignore_enabled
        if npm_ignore_options is not None:
            self._values["npm_ignore_options"] = npm_ignore_options
        if package is not None:
            self._values["package"] = package
        if prettier is not None:
            self._values["prettier"] = prettier
        if prettier_options is not None:
            self._values["prettier_options"] = prettier_options
        if projen_dev_dependency is not None:
            self._values["projen_dev_dependency"] = projen_dev_dependency
        if projenrc_js is not None:
            self._values["projenrc_js"] = projenrc_js
        if projenrc_js_options is not None:
            self._values["projenrc_js_options"] = projenrc_js_options
        if projen_version is not None:
            self._values["projen_version"] = projen_version
        if pull_request_template is not None:
            self._values["pull_request_template"] = pull_request_template
        if pull_request_template_contents is not None:
            self._values["pull_request_template_contents"] = pull_request_template_contents
        if release is not None:
            self._values["release"] = release
        if release_to_npm is not None:
            self._values["release_to_npm"] = release_to_npm
        if workflow_bootstrap_steps is not None:
            self._values["workflow_bootstrap_steps"] = workflow_bootstrap_steps
        if workflow_git_identity is not None:
            self._values["workflow_git_identity"] = workflow_git_identity
        if workflow_node_version is not None:
            self._values["workflow_node_version"] = workflow_node_version
        if workflow_package_cache is not None:
            self._values["workflow_package_cache"] = workflow_package_cache
        if disable_tsconfig is not None:
            self._values["disable_tsconfig"] = disable_tsconfig
        if disable_tsconfig_dev is not None:
            self._values["disable_tsconfig_dev"] = disable_tsconfig_dev
        if docgen is not None:
            self._values["docgen"] = docgen
        if docs_directory is not None:
            self._values["docs_directory"] = docs_directory
        if entrypoint_types is not None:
            self._values["entrypoint_types"] = entrypoint_types
        if eslint is not None:
            self._values["eslint"] = eslint
        if eslint_options is not None:
            self._values["eslint_options"] = eslint_options
        if libdir is not None:
            self._values["libdir"] = libdir
        if projenrc_ts is not None:
            self._values["projenrc_ts"] = projenrc_ts
        if projenrc_ts_options is not None:
            self._values["projenrc_ts_options"] = projenrc_ts_options
        if runner is not None:
            self._values["runner"] = runner
        if sample_code is not None:
            self._values["sample_code"] = sample_code
        if srcdir is not None:
            self._values["srcdir"] = srcdir
        if testdir is not None:
            self._values["testdir"] = testdir
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig
        if tsconfig_dev is not None:
            self._values["tsconfig_dev"] = tsconfig_dev
        if tsconfig_dev_file is not None:
            self._values["tsconfig_dev_file"] = tsconfig_dev_file
        if ts_jest_options is not None:
            self._values["ts_jest_options"] = ts_jest_options
        if typescript_version is not None:
            self._values["typescript_version"] = typescript_version
        if compat is not None:
            self._values["compat"] = compat
        if compat_ignore is not None:
            self._values["compat_ignore"] = compat_ignore
        if compress_assembly is not None:
            self._values["compress_assembly"] = compress_assembly
        if docgen_file_path is not None:
            self._values["docgen_file_path"] = docgen_file_path
        if exclude_typescript is not None:
            self._values["exclude_typescript"] = exclude_typescript
        if jsii_version is not None:
            self._values["jsii_version"] = jsii_version
        if publish_to_go is not None:
            self._values["publish_to_go"] = publish_to_go
        if publish_to_maven is not None:
            self._values["publish_to_maven"] = publish_to_maven
        if publish_to_nuget is not None:
            self._values["publish_to_nuget"] = publish_to_nuget
        if publish_to_pypi is not None:
            self._values["publish_to_pypi"] = publish_to_pypi
        if rootdir is not None:
            self._values["rootdir"] = rootdir
        if validate_tsconfig is not None:
            self._values["validate_tsconfig"] = validate_tsconfig
        if catalog is not None:
            self._values["catalog"] = catalog
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version

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
    def git_ignore_options(
        self,
    ) -> typing.Optional["_projen_04054675.IgnoreFileOptions"]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional["_projen_04054675.IgnoreFileOptions"], result)

    @builtins.property
    def git_options(self) -> typing.Optional["_projen_04054675.GitOptions"]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional["_projen_04054675.GitOptions"], result)

    @builtins.property
    def logging(self) -> typing.Optional["_projen_04054675.LoggerOptions"]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["_projen_04054675.LoggerOptions"], result)

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
    def parent(self) -> typing.Optional["_projen_04054675.Project"]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional["_projen_04054675.Project"], result)

    @builtins.property
    def project_tree(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate a project tree file (``.projen/tree.json``) that shows all components and their relationships. Useful for understanding your project structure and debugging.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("project_tree")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def projenrc_json_options(
        self,
    ) -> typing.Optional["_projen_04054675.ProjenrcJsonOptions"]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional["_projen_04054675.ProjenrcJsonOptions"], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional["_projen_04054675.RenovatebotOptions"]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional["_projen_04054675.RenovatebotOptions"], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional["_github_c49f935d.AutoApproveOptions"]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional["_github_c49f935d.AutoApproveOptions"], result)

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
    def auto_merge_options(
        self,
    ) -> typing.Optional["_github_c49f935d.AutoMergeOptions"]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional["_github_c49f935d.AutoMergeOptions"], result)

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
    def github_options(self) -> typing.Optional["_github_c49f935d.GitHubOptions"]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional["_github_c49f935d.GitHubOptions"], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional["_github_c49f935d.GithubCredentials"]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional["_github_c49f935d.GithubCredentials"], result)

    @builtins.property
    def readme(self) -> typing.Optional["_projen_04054675.SampleReadmeProps"]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental

        Example::

            "{ filename: 'readme.md', contents: '# title' }"
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional["_projen_04054675.SampleReadmeProps"], result)

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
    def stale_options(self) -> typing.Optional["_github_c49f935d.StaleOptions"]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional["_github_c49f935d.StaleOptions"], result)

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
    def add_package_manager_to_dev_engines(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add the resolved ``packageManager`` to ``devEngines.packageManager`` in ``package.json``, setting ``onFail`` to ``ignore``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("add_package_manager_to_dev_engines")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_library_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``.

        This is normally only allowed for libraries. For apps, there's no meaning
        for specifying these.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_library_dependencies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_scripts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dependency (package) names that are allowed to run lifecycle install scripts (``preinstall``, ``install``, ``postinstall``, ``prepare``) during dependency installation.

        These scripts can execute arbitrary code, making them a common
        supply-chain attack vector. Package managers are moving toward
        blocking them by default and requiring an explicit allowlist.
        Configuring ``allowScripts`` sets up that allowlist so scripts only run
        for the packages you have explicitly reviewed and trust.

        Support for this setting depends on the configured ``packageManager``:

        - ``NPM``: written to the native ``allowScripts`` field in ``package.json``
          (requires npm >= 11.16; see https://docs.npmjs.com/cli/v11/commands/npm-approve-scripts).
        - ``BUN``: written to the native ``trustedDependencies`` field in
          ``package.json`` (see https://bun.com/docs/pm/lifecycle).
        - ``PNPM``: written to the ``onlyBuiltDependencies`` setting in
          ``pnpm-workspace.yaml`` (see https://pnpm.io/settings#onlybuiltdependencies).
        - ``YARN2``, ``YARN_BERRY``: written to the native
          ``dependenciesMeta.<pkg>.built`` allowlist in ``package.json``, combined
          with ``enableScripts: false`` in ``.yarnrc.yml`` (see
          https://yarnpkg.com/features/security#postinstalls). If you set
          ``yarnBerryOptions.yarnRcOptions.enableScripts`` explicitly, that value
          is respected instead of being overridden.
        - ``YARN``, ``YARN_CLASSIC``: not supported. Yarn Classic has no native
          mechanism to allowlist install scripts for specific dependencies.
          Setting this option with one of these package managers throws an
          error at synthesis time.

        :default: - all install scripts are allowed to run (package manager default)

        :stability: experimental
        '''
        result = self._values.get("allow_scripts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_organization(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Is the author an organization.

        :stability: experimental
        '''
        result = self._values.get("author_organization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's URL / Website.

        :stability: experimental
        '''
        result = self._values.get("author_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_detect_bin(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_detect_bin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bin(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Binary programs vended with your module.

        You can use this option to add/customize how binaries are represented in
        your ``package.json``, but unless ``autoDetectBin`` is ``false``, every
        executable file under ``bin`` will automatically be added to this section.

        :stability: experimental
        '''
        result = self._values.get("bin")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bugs_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email address to which issues should be reported.

        :stability: experimental
        '''
        result = self._values.get("bugs_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bugs_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url to your project's issue tracker.

        :stability: experimental
        '''
        result = self._values.get("bugs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundled_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dependencies to bundle into this module.

        These modules will be
        added both to the ``dependencies`` section and ``bundledDependencies`` section of
        your ``package.json``.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and
        this will be what your ``package.json`` will eventually include.

        :stability: experimental
        '''
        result = self._values.get("bundled_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bun_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of Bun to use if using Bun as a package manager.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("bun_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_artifact_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.CodeArtifactOptions"]:
        '''(experimental) Options for npm packages using AWS CodeArtifact.

        This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.CodeArtifactOptions"], result)

    @builtins.property
    def delete_orphaned_lock_files(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically delete lockfiles from package managers that are not the active one.

        Only triggered when the lockfile for the configured package
        manager already exists.

        This is useful when migrating between package managers to avoid conflicts.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("delete_orphaned_lock_files")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Runtime dependencies of this module.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and
        this will be what your ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true

        Example::

            [ 'express', 'lodash', 'foo@^2' ]
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description is just a string that helps people understand the purpose of the package.

        It can be used when searching for packages in a package manager as well.
        See https://classic.yarnpkg.com/en/docs/package-json/#toc-description

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Build dependencies for this module.

        These dependencies will only be
        available in your build environment but will not be fetched when this
        module is consumed.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``pnpm add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``pnpm add`` or ``npm i`` (e.g. ``express@^2``) and
        this will be what your ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true

        Example::

            [ 'typescript', '@types/express' ]
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dev_engines(self) -> typing.Optional["_javascript_eb5dbe11.DevEngines"]:
        '''(experimental) Configure the ``devEngines`` field in ``package.json``.

        The ``devEngines.packageManager`` field is automatically populated based on
        the resolved ``packageManager`` value. Any fields provided here are merged
        with the auto-populated ``packageManager`` entry.

        :see: https://docs.npmjs.com/cli/v10/configuring-npm/package-json#devengines
        :stability: experimental
        '''
        result = self._values.get("dev_engines")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.DevEngines"], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Module entrypoint (``main`` in ``package.json``).

        Set to an empty string to not include ``main`` in your package.json

        :default: "lib/index.js"

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Homepage / Website.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Keywords to include in ``package.json``.

        :stability: experimental
        '''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License's SPDX identifier.

        See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses.
        Use the ``licensed`` option if you want to no license to be specified.

        :default: "Apache-2.0"

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if a license should be added.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("licensed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The maximum node version supported by this package. Most projects should not use this option.

        The value indicates that the package is incompatible with any newer versions of node.
        This requirement is enforced via the engines field.

        You will normally not need to set this option.
        Consider this option only if your package is known to not function with newer versions of node.

        :default: - no maximum version is enforced

        :stability: experimental
        '''
        result = self._values.get("max_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The minimum node version required by this package to function. Most projects should not use this option.

        The value indicates that the package is incompatible with any older versions of node.
        This requirement is enforced via the engines field.

        You will normally not need to set this option, even if your package is incompatible with EOL versions of node.
        Consider this option only if your package depends on a specific feature, that is not available in other LTS versions.
        Setting this option has very high impact on the consumers of your package,
        as package managers will actively prevent usage with node versions you have marked as incompatible.

        To change the node version of your CI/CD workflows, use ``workflowNodeVersion``.

        :default: - no minimum version is enforced

        :stability: experimental
        '''
        result = self._values.get("min_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_access(self) -> typing.Optional["_javascript_eb5dbe11.NpmAccess"]:
        '''(experimental) Access level of the npm package.

        :default:

        - for scoped packages (e.g. ``foo@bar``), the default is
        ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is
        ``NpmAccess.PUBLIC``.

        :stability: experimental
        '''
        result = self._values.get("npm_access")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.NpmAccess"], result)

    @builtins.property
    def npm_provenance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should provenance statements be generated when the package is published.

        A supported package manager is required to publish a package with npm provenance statements and
        you will need to use a supported CI/CD provider.

        Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages,
        which is using npm internally and supports provenance statements independently of the package manager used.

        :default: - true for public packages, false otherwise

        :see: https://docs.npmjs.com/generating-provenance-statements
        :stability: experimental
        '''
        result = self._values.get("npm_provenance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base URL of the npm package registry.

        Must be a URL (e.g. start with "https://" or "http://")

        :default: "https://registry.npmjs.org"

        :stability: experimental
        '''
        result = self._values.get("npm_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: "NPM_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_trusted_publishing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use trusted publishing for publishing to npmjs.com Needs to be pre-configured on npm.js to work.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("npm_trusted_publishing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def package_manager(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.NodePackageManager"]:
        '''(experimental) The Node Package Manager used to execute scripts.

        :default: - Detected from the calling process or ``YARN_CLASSIC`` if detection fails.

        :stability: experimental
        :pjnew: $PACKAGE_MANAGER
        '''
        result = self._values.get("package_manager")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.NodePackageManager"], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The "name" in package.json.

        :default: - defaults to project name

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_dependency_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.PeerDependencyOptions"]:
        '''(experimental) Options for ``peerDeps``.

        :stability: experimental
        '''
        result = self._values.get("peer_dependency_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.PeerDependencyOptions"], result)

    @builtins.property
    def peer_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Peer dependencies for this module.

        Dependencies listed here are required to
        be installed (and satisfied) by the *consumer* of this library. Using peer
        dependencies allows you to ensure that only a single module of a certain
        library exists in the ``node_modules`` tree of your consumers.

        Note that prior to npm@7, peer dependencies are *not* automatically
        installed, which means that adding peer dependencies to a library will be a
        breaking change for your customers.

        Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is
        enabled by default), projen will automatically add a dev dependency with a
        pinned version for each peer dependency. This will ensure that you build &
        test your module against the lowest peer version required.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("peer_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pnpm_options(self) -> typing.Optional["_javascript_eb5dbe11.PnpmOptions"]:
        '''(experimental) Options for pnpm.

        :default: - all default options

        :stability: experimental
        '''
        result = self._values.get("pnpm_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.PnpmOptions"], result)

    @builtins.property
    def pnpm_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of PNPM to use if using PNPM as a package manager.

        :default: "10.33.0"

        :stability: experimental
        '''
        result = self._values.get("pnpm_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) The repository is the location where the actual code for your package lives.

        See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.

        :stability: experimental
        '''
        result = self._values.get("repository_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scoped_packages_options(
        self,
    ) -> typing.Optional[typing.List["_javascript_eb5dbe11.ScopedPackagesOptions"]]:
        '''(experimental) Options for privately hosted scoped packages.

        :default: - fetch all scoped packages from the public npm registry

        :stability: experimental
        '''
        result = self._values.get("scoped_packages_options")
        return typing.cast(typing.Optional[typing.List["_javascript_eb5dbe11.ScopedPackagesOptions"]], result)

    @builtins.property
    def stability(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Stability.

        :stability: experimental
        '''
        result = self._values.get("stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def yarn_berry_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.YarnBerryOptions"]:
        '''(experimental) Options for Yarn Berry.

        :default: - Yarn Berry v4 with all default options

        :stability: experimental
        '''
        result = self._values.get("yarn_berry_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.YarnBerryOptions"], result)

    @builtins.property
    def bump_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string.

        This can be any compatible package version, including the deprecated ``standard-version@9``.

        :default: - A recent version of "commit-and-tag-version"

        :stability: experimental
        '''
        result = self._values.get("bump_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``publib`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Major version to release from the default branch.

        If this is specified, we bump the latest version of this major version line.
        If not specified, we bump the global latest version.

        :default: - Major version is not enforced.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimal Major version to release.

        This can be useful to set to 1, as breaking changes before the 1.x major
        release are not incrementing the major version number.

        Can not be set together with ``majorVersion``.

        :default: - No minimum version is being enforced

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def next_version_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command to control the next version to release.

        If present, this shell command will be run before the bump is executed, and
        it determines what version to release. It will be executed in the following
        environment:

        - Working directory: the project directory.
        - ``$VERSION``: the current version. Looks like ``1.2.3``.
        - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset.
        - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``.

        The command should print one of the following to ``stdout``:

        - Nothing: the next version number will be determined based on commit history.
        - ``x.y.z``: the next version number will be ``x.y.z``.
        - ``major|minor|patch``: the next version number will be the current version number
          with the indicated component bumped.

        This setting cannot be specified together with ``minMajorVersion``; the invoked
        script can be used to achieve the effects of ``minMajorVersion``.

        :default: - The next version will be determined based on the commit history and project settings.

        :stability: experimental
        '''
        result = self._values.get("next_version_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npmDistTag to use when publishing from the default branch.

        To set the npm dist-tag for release branches, set the ``npmDistTag`` property
        for each branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(
        self,
    ) -> typing.Optional[typing.List["_workflows_2b7f1587.JobStep"]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List["_workflows_2b7f1587.JobStep"]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Instead of actually publishing to package managers, just print the publishing command.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def releasable_commits(
        self,
    ) -> typing.Optional["_projen_04054675.ReleasableCommits"]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional["_projen_04054675.ReleasableCommits"], result)

    @builtins.property
    def release_branches(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "_release_1fa091fd.BranchOptions"]]:
        '''(experimental) Defines additional release branches.

        A workflow will be created for each
        release branch which will publish releases from commits in this branch.
        Each release branch *must* be assigned a major version number which is used
        to enforce that versions published from that branch always use that major
        version. If multiple branches are used, the ``majorVersion`` field must also
        be provided for the default branch.

        :default:

        - no additional branches are used for release. you can use
        ``addBranch()`` to add additional branches.

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "_release_1fa091fd.BranchOptions"]], result)

    @builtins.property
    def release_environment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub Actions environment used for the release.

        This can be used to add an explicit approval step to the release
        or limit who can initiate a release through environment protection rules.

        When multiple artifacts are released, the environment can be overwritten
        on a per artifact basis.

        :default: - no environment used, unless set at the artifact level

        :stability: experimental
        '''
        result = self._values.get("release_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a github issue on every failed publishing task.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to issues indicating publish failures.

        Only applies if ``releaseFailureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers.

        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: "v"

        :stability: experimental
        '''
        result = self._values.get("release_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_trigger(self) -> typing.Optional["_release_1fa091fd.ReleaseTrigger"]:
        '''(experimental) The release trigger to use.

        :default: - Continuous releases (``ReleaseTrigger.continuous()``)

        :stability: experimental
        '''
        result = self._values.get("release_trigger")
        return typing.cast(typing.Optional["_release_1fa091fd.ReleaseTrigger"], result)

    @builtins.property
    def release_workflow_env(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build environment variables for release workflows.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("release_workflow_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def release_workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the default release workflow.

        :default: "release"

        :stability: experimental
        '''
        result = self._values.get("release_workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List["_workflows_2b7f1587.JobStep"]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List["_workflows_2b7f1587.JobStep"]], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration used when creating changelog with commit-and-tag-version package.

        Given values either append to default configuration or overwrite values in it.

        :default: - standard configuration applicable for GitHub repositories

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(
        self,
    ) -> typing.Optional["_projen_04054675.GroupRunnerOptions"]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional["_projen_04054675.GroupRunnerOptions"], result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A directory which will contain build artifacts.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audit_deps(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run security audit on dependencies.

        When enabled, creates an "audit" task that checks for known security vulnerabilities
        in dependencies. By default, runs during every build and checks for "high" severity
        vulnerabilities or above in all dependencies (including dev dependencies).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("audit_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def audit_deps_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.AuditOptions"]:
        '''(experimental) Security audit options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("audit_deps_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.AuditOptions"], result)

    @builtins.property
    def auto_approve_upgrades(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configured).

        Throw if set to true but ``autoApproveOptions`` are not defined.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("auto_approve_upgrades")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def biome(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup Biome.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("biome")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def biome_options(self) -> typing.Optional["_javascript_eb5dbe11.BiomeOptions"]:
        '''(experimental) Biome options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("biome_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.BiomeOptions"], result)

    @builtins.property
    def build_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow for building PRs.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("build_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def build_workflow_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.BuildWorkflowOptions"]:
        '''(experimental) Options for PR build workflow.

        :stability: experimental
        '''
        result = self._values.get("build_workflow_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.BuildWorkflowOptions"], result)

    @builtins.property
    def bundler_options(self) -> typing.Optional["_javascript_eb5dbe11.BundlerOptions"]:
        '''(experimental) Options for ``Bundler``.

        :stability: experimental
        '''
        result = self._values.get("bundler_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.BundlerOptions"], result)

    @builtins.property
    def check_licenses(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.LicenseCheckerOptions"]:
        '''(experimental) Configure which licenses should be deemed acceptable for use by dependencies.

        This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered.

        :default: - no license checks are run during the build and all licenses will be accepted

        :stability: experimental
        '''
        result = self._values.get("check_licenses")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.LicenseCheckerOptions"], result)

    @builtins.property
    def code_cov(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v5 By default, OIDC auth is used. Alternatively a token can be provided via ``codeCovTokenSecret``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("code_cov")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_cov_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) Define the secret name for a specified https://codecov.io/ token.

        :default: - OIDC auth is used

        :stability: experimental
        '''
        result = self._values.get("code_cov_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) License copyright owner.

        :default: - defaults to the value of authorName or "" if ``authorName`` is undefined.

        :stability: experimental
        '''
        result = self._values.get("copyright_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_period(self) -> typing.Optional[builtins.str]:
        '''(experimental) The copyright years to put in the LICENSE file.

        :default: - current year

        :stability: experimental
        '''
        result = self._values.get("copyright_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_release_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the main release branch.

        :default: "main"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("default_release_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependabot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use dependabot to handle dependency upgrades.

        Cannot be used in conjunction with ``depsUpgrade``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dependabot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dependabot_options(
        self,
    ) -> typing.Optional["_github_c49f935d.DependabotOptions"]:
        '''(experimental) Options for dependabot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("dependabot_options")
        return typing.cast(typing.Optional["_github_c49f935d.DependabotOptions"], result)

    @builtins.property
    def deps_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use tasks and github workflows to handle dependency upgrades.

        Cannot be used in conjunction with ``dependabot``.

        :default: - ``true`` for root projects, ``false`` for subprojects

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps_upgrade_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.UpgradeDependenciesOptions"]:
        '''(experimental) Options for ``UpgradeDependencies``.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.UpgradeDependenciesOptions"], result)

    @builtins.property
    def gitignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional entries to .gitignore.

        :stability: experimental
        '''
        result = self._values.get("gitignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup jest unit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("jest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jest_options(self) -> typing.Optional["_javascript_eb5dbe11.JestOptions"]:
        '''(experimental) Jest options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("jest_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.JestOptions"], result)

    @builtins.property
    def npmignore_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("npmignore_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_ignore_options(
        self,
    ) -> typing.Optional["_projen_04054675.IgnoreFileOptions"]:
        '''(experimental) Configuration options for .npmignore file.

        :stability: experimental
        '''
        result = self._values.get("npm_ignore_options")
        return typing.cast(typing.Optional["_projen_04054675.IgnoreFileOptions"], result)

    @builtins.property
    def package(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("package")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prettier(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup prettier.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("prettier")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prettier_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.PrettierOptions"]:
        '''(experimental) Prettier options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("prettier_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.PrettierOptions"], result)

    @builtins.property
    def projen_dev_dependency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates of "projen" should be installed as a devDependency.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("projen_dev_dependency")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_js(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation.

        :default: - true if projenrcJson is false

        :stability: experimental
        '''
        result = self._values.get("projenrc_js")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_js_options(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.ProjenrcOptions"]:
        '''(experimental) Options for .projenrc.js.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_js_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.ProjenrcOptions"], result)

    @builtins.property
    def projen_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of projen to install.

        :default: - Defaults to the latest version.

        :stability: experimental
        '''
        result = self._values.get("projen_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_template(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a GitHub pull request template.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_template_contents(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The contents of the pull request template.

        :default: - default content

        :stability: experimental
        '''
        result = self._values.get("pull_request_template_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def release(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add release management to this project.

        :default: - true (false for subprojects)

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_to_npm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically release to npm when new versions are introduced.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_to_npm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_bootstrap_steps(
        self,
    ) -> typing.Optional[typing.List["_workflows_2b7f1587.JobStep"]]:
        '''(experimental) Workflow steps to use in order to bootstrap this repo.

        :default: "yarn install --frozen-lockfile && yarn projen"

        :stability: experimental
        '''
        result = self._values.get("workflow_bootstrap_steps")
        return typing.cast(typing.Optional[typing.List["_workflows_2b7f1587.JobStep"]], result)

    @builtins.property
    def workflow_git_identity(self) -> typing.Optional["_github_c49f935d.GitIdentity"]:
        '''(experimental) The git identity to use in workflows.

        :default: - default GitHub Actions user

        :stability: experimental
        '''
        result = self._values.get("workflow_git_identity")
        return typing.cast(typing.Optional["_github_c49f935d.GitIdentity"], result)

    @builtins.property
    def workflow_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The node version used in GitHub Actions workflows.

        Always use this option if your GitHub Actions workflows require a specific to run.

        :default: - ``minNodeVersion`` if set, otherwise ``lts/*``.

        :stability: experimental
        '''
        result = self._values.get("workflow_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_package_cache(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Node.js package cache in GitHub workflows.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("workflow_package_cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_tsconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_tsconfig")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_tsconfig_dev(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not generate a development tsconfig file.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_tsconfig_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docgen(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Docgen by Typedoc.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("docgen")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docs_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs directory.

        :default: "docs"

        :stability: experimental
        '''
        result = self._values.get("docs_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint_types(self) -> typing.Optional[builtins.str]:
        '''(experimental) The .d.ts file that includes the type declarations for this module.

        :default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)

        :stability: experimental
        '''
        result = self._values.get("entrypoint_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eslint(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup eslint.

        :default: - true, unless biome is enabled

        :stability: experimental
        '''
        result = self._values.get("eslint")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def eslint_options(self) -> typing.Optional["_javascript_eb5dbe11.EslintOptions"]:
        '''(experimental) Eslint options.

        :default: - opinionated default options

        :stability: experimental
        '''
        result = self._values.get("eslint_options")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.EslintOptions"], result)

    @builtins.property
    def libdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Typescript  artifacts output directory.

        :default: "lib"

        :stability: experimental
        '''
        result = self._values.get("libdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projenrc_ts(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use TypeScript for your projenrc file (``.projenrc.ts``).

        :default: false

        :stability: experimental
        :pjnew: true
        '''
        result = self._values.get("projenrc_ts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_ts_options(
        self,
    ) -> typing.Optional["_typescript_7a66cf84.ProjenrcOptions"]:
        '''(experimental) Options for .projenrc.ts.

        :stability: experimental
        '''
        result = self._values.get("projenrc_ts_options")
        return typing.cast(typing.Optional["_typescript_7a66cf84.ProjenrcOptions"], result)

    @builtins.property
    def runner(self) -> typing.Optional["_typescript_7a66cf84.TypeScriptRunner"]:
        '''(experimental) The TypeScript runner to use for executing TypeScript files.

        This is a project-level setting that components (e.g. projenrc) will
        use as their default runner.

        :default: TypeScriptRunner.tsNode()

        :stability: experimental
        '''
        result = self._values.get("runner")
        return typing.cast(typing.Optional["_typescript_7a66cf84.TypeScriptRunner"], result)

    @builtins.property
    def sample_code(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample_code")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def srcdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Typescript sources directory.

        :default: "src"

        :stability: experimental
        '''
        result = self._values.get("srcdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def testdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Jest tests directory. Tests files should be named ``xxx.test.ts``.

        If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``),
        then tests are going to be compiled into ``lib/`` and executed as javascript.
        If the test directory is outside of ``src``, then we configure jest to
        compile the code in-memory.

        :default: "test"

        :stability: experimental
        '''
        result = self._values.get("testdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tsconfig(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.TypescriptConfigOptions"]:
        '''(experimental) Custom TSConfig.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.TypescriptConfigOptions"], result)

    @builtins.property
    def tsconfig_dev(
        self,
    ) -> typing.Optional["_javascript_eb5dbe11.TypescriptConfigOptions"]:
        '''(experimental) Custom tsconfig options for the development tsconfig.json file (used for testing).

        :default: - use the production tsconfig options

        :stability: experimental
        '''
        result = self._values.get("tsconfig_dev")
        return typing.cast(typing.Optional["_javascript_eb5dbe11.TypescriptConfigOptions"], result)

    @builtins.property
    def tsconfig_dev_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name (and path) of the development tsconfig file.

        By default this lives inside the test directory (e.g. ``test/tsconfig.json``)
        so that the TypeScript language service resolves it as the nearest config
        for test files.

        :default: - "{testdir}/tsconfig.json"

        :stability: experimental
        '''
        result = self._values.get("tsconfig_dev_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ts_jest_options(self) -> typing.Optional["_typescript_7a66cf84.TsJestOptions"]:
        '''(experimental) Options for ts-jest.

        :stability: experimental
        '''
        result = self._values.get("ts_jest_options")
        return typing.cast(typing.Optional["_typescript_7a66cf84.TsJestOptions"], result)

    @builtins.property
    def typescript_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) TypeScript version to use.

        NOTE: Typescript is not semantically versioned and should remain on the
        same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``).

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("typescript_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author(self) -> builtins.str:
        '''(experimental) The name of the library author.

        :default: $GIT_USER_NAME

        :stability: experimental
        '''
        result = self._values.get("author")
        assert result is not None, "Required property 'author' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def author_address(self) -> builtins.str:
        '''(experimental) Email or URL of the library author.

        :default: $GIT_USER_EMAIL

        :stability: experimental
        '''
        result = self._values.get("author_address")
        assert result is not None, "Required property 'author_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''(experimental) Git repository URL.

        :default: $GIT_REMOTE

        :stability: experimental
        '''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compat(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically run API compatibility test against the latest version published to npm after compilation.

        - You can manually run compatibility tests using ``yarn compat`` if this feature is disabled.
        - You can ignore compatibility failures by adding lines to a ".compatignore" file.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("compat")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compat_ignore(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the ignore file for API compatibility tests.

        :default: ".compatignore"

        :stability: experimental
        '''
        result = self._values.get("compat_ignore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress_assembly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Emit a compressed version of the assembly.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("compress_assembly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docgen_file_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) File path for generated docs.

        :default: "API.md"

        :stability: experimental
        '''
        result = self._values.get("docgen_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_typescript(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Accepts a list of glob patterns.

        Files matching any of those patterns will be excluded from the TypeScript compiler input.

        By default, jsii will include all *.ts files (except .d.ts files) in the TypeScript compiler input.
        This can be problematic for example when the package's build or test procedure generates .ts files
        that cannot be compiled with jsii's compiler settings.

        :stability: experimental
        '''
        result = self._values.get("exclude_typescript")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jsii_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of the jsii compiler to use.

        Set to "*" if you want to manually manage the version of jsii in your
        project by managing updates to ``package.json`` on your own.

        NOTE: The jsii compiler releases since 5.0.0 are not semantically versioned
        and should remain on the same minor, so we recommend using a ``~`` dependency
        (e.g. ``~5.0.0``).

        :default: "~5.9.0"

        :stability: experimental
        :pjnew: "~6.0.0"
        '''
        result = self._values.get("jsii_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_to_go(self) -> typing.Optional["_cdk_bb21cefa.JsiiGoTarget"]:
        '''(experimental) Publish Go bindings to a git repository.

        :default: - no publishing

        :stability: experimental
        '''
        result = self._values.get("publish_to_go")
        return typing.cast(typing.Optional["_cdk_bb21cefa.JsiiGoTarget"], result)

    @builtins.property
    def publish_to_maven(self) -> typing.Optional["_cdk_bb21cefa.JsiiJavaTarget"]:
        '''(experimental) Publish to maven.

        :default: - no publishing

        :stability: experimental
        '''
        result = self._values.get("publish_to_maven")
        return typing.cast(typing.Optional["_cdk_bb21cefa.JsiiJavaTarget"], result)

    @builtins.property
    def publish_to_nuget(self) -> typing.Optional["_cdk_bb21cefa.JsiiDotNetTarget"]:
        '''(experimental) Publish to NuGet.

        :default: - no publishing

        :stability: experimental
        '''
        result = self._values.get("publish_to_nuget")
        return typing.cast(typing.Optional["_cdk_bb21cefa.JsiiDotNetTarget"], result)

    @builtins.property
    def publish_to_pypi(self) -> typing.Optional["_cdk_bb21cefa.JsiiPythonTarget"]:
        '''(experimental) Publish to pypi.

        :default: - no publishing

        :stability: experimental
        '''
        result = self._values.get("publish_to_pypi")
        return typing.cast(typing.Optional["_cdk_bb21cefa.JsiiPythonTarget"], result)

    @builtins.property
    def rootdir(self) -> typing.Optional[builtins.str]:
        '''
        :default: "."

        :stability: experimental
        '''
        result = self._values.get("rootdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_tsconfig(self) -> typing.Optional["_cdk_bb21cefa.ValidateTsconfig"]:
        '''(experimental) Level of tsconfig validation jsii should perform on the user-provided tsconfig.

        Only relevant when the project synthesizes its own tsconfig
        (i.e. ``disableTsconfig`` is not set on the TypeScriptProject).

        :default: ValidateTsconfig.STRICT

        :see: https://aws.github.io/jsii/user-guides/lib-author/configuration/#validatetsconfig
        :stability: experimental
        '''
        result = self._values.get("validate_tsconfig")
        return typing.cast(typing.Optional["_cdk_bb21cefa.ValidateTsconfig"], result)

    @builtins.property
    def catalog(self) -> typing.Optional["_cdk_bb21cefa.Catalog"]:
        '''(experimental) Libraries will be picked up by the construct catalog when they are published to npm as jsii modules and will be published under:.

        https://awscdk.io/packages/[@SCOPE/]PACKAGE@VERSION

        The catalog will also post a tweet to https://twitter.com/awscdkio with the
        package name, description and the above link. You can disable these tweets
        through ``{ announce: false }``.

        You can also add a Twitter handle through ``{ twitter: 'xx' }`` which will be
        mentioned in the tweet.

        :default: - new version will be announced

        :see: https://github.com/construct-catalog/catalog
        :stability: experimental
        '''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional["_cdk_bb21cefa.Catalog"], result)

    @builtins.property
    def cdktf_version(self) -> builtins.str:
        '''(experimental) Minimum target version this library is tested against.

        :default: "^0.13.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("cdktf_version")
        assert result is not None, "Required property 'cdktf_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Construct version to use.

        :default: "^10.3.0"

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstructLibraryCdktfOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ConstructLibraryCdktf",
    "ConstructLibraryCdktfOptions",
]

publication.publish()

def _typecheckingstub__bbf02af18148d47e66a6d0672a809602f782953da7a849545a808c276a58ff4d(
    *,
    name: builtins.str,
    commit_generated: typing.Optional[builtins.bool] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    project_tree: typing.Optional[builtins.bool] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_options: typing.Optional[typing.Union[_github_c49f935d.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_github_c49f935d.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_github_c49f935d.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    projen_credentials: typing.Optional[_github_c49f935d.GithubCredentials] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_github_c49f935d.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vscode: typing.Optional[builtins.bool] = None,
    add_package_manager_to_dev_engines: typing.Optional[builtins.bool] = None,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    allow_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    author_organization: typing.Optional[builtins.bool] = None,
    author_url: typing.Optional[builtins.str] = None,
    auto_detect_bin: typing.Optional[builtins.bool] = None,
    bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bugs_email: typing.Optional[builtins.str] = None,
    bugs_url: typing.Optional[builtins.str] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    bun_version: typing.Optional[builtins.str] = None,
    code_artifact_options: typing.Optional[typing.Union[_javascript_eb5dbe11.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_orphaned_lock_files: typing.Optional[builtins.bool] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    dev_engines: typing.Optional[typing.Union[_javascript_eb5dbe11.DevEngines, typing.Dict[builtins.str, typing.Any]]] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license: typing.Optional[builtins.str] = None,
    licensed: typing.Optional[builtins.bool] = None,
    max_node_version: typing.Optional[builtins.str] = None,
    min_node_version: typing.Optional[builtins.str] = None,
    npm_access: typing.Optional[_javascript_eb5dbe11.NpmAccess] = None,
    npm_provenance: typing.Optional[builtins.bool] = None,
    npm_registry_url: typing.Optional[builtins.str] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    npm_trusted_publishing: typing.Optional[builtins.bool] = None,
    package_manager: typing.Optional[_javascript_eb5dbe11.NodePackageManager] = None,
    package_name: typing.Optional[builtins.str] = None,
    peer_dependency_options: typing.Optional[typing.Union[_javascript_eb5dbe11.PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    pnpm_options: typing.Optional[typing.Union[_javascript_eb5dbe11.PnpmOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pnpm_version: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_directory: typing.Optional[builtins.str] = None,
    scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[_javascript_eb5dbe11.ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    stability: typing.Optional[builtins.str] = None,
    yarn_berry_options: typing.Optional[typing.Union[_javascript_eb5dbe11.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    bump_package: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    major_version: typing.Optional[jsii.Number] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    next_version_command: typing.Optional[builtins.str] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_workflows_2b7f1587.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    releasable_commits: typing.Optional[_projen_04054675.ReleasableCommits] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_release_1fa091fd.BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_environment: typing.Optional[builtins.str] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_trigger: typing.Optional[_release_1fa091fd.ReleaseTrigger] = None,
    release_workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_workflows_2b7f1587.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    artifacts_directory: typing.Optional[builtins.str] = None,
    audit_deps: typing.Optional[builtins.bool] = None,
    audit_deps_options: typing.Optional[typing.Union[_javascript_eb5dbe11.AuditOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_upgrades: typing.Optional[builtins.bool] = None,
    biome: typing.Optional[builtins.bool] = None,
    biome_options: typing.Optional[typing.Union[_javascript_eb5dbe11.BiomeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_workflow: typing.Optional[builtins.bool] = None,
    build_workflow_options: typing.Optional[typing.Union[_javascript_eb5dbe11.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    bundler_options: typing.Optional[typing.Union[_javascript_eb5dbe11.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_licenses: typing.Optional[typing.Union[_javascript_eb5dbe11.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_cov: typing.Optional[builtins.bool] = None,
    code_cov_token_secret: typing.Optional[builtins.str] = None,
    copyright_owner: typing.Optional[builtins.str] = None,
    copyright_period: typing.Optional[builtins.str] = None,
    default_release_branch: typing.Optional[builtins.str] = None,
    dependabot: typing.Optional[builtins.bool] = None,
    dependabot_options: typing.Optional[typing.Union[_github_c49f935d.DependabotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps_upgrade: typing.Optional[builtins.bool] = None,
    deps_upgrade_options: typing.Optional[typing.Union[_javascript_eb5dbe11.UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    jest: typing.Optional[builtins.bool] = None,
    jest_options: typing.Optional[typing.Union[_javascript_eb5dbe11.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    npmignore_enabled: typing.Optional[builtins.bool] = None,
    npm_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    package: typing.Optional[builtins.bool] = None,
    prettier: typing.Optional[builtins.bool] = None,
    prettier_options: typing.Optional[typing.Union[_javascript_eb5dbe11.PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_dev_dependency: typing.Optional[builtins.bool] = None,
    projenrc_js: typing.Optional[builtins.bool] = None,
    projenrc_js_options: typing.Optional[typing.Union[_javascript_eb5dbe11.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_version: typing.Optional[builtins.str] = None,
    pull_request_template: typing.Optional[builtins.bool] = None,
    pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    release: typing.Optional[builtins.bool] = None,
    release_to_npm: typing.Optional[builtins.bool] = None,
    workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_workflows_2b7f1587.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_git_identity: typing.Optional[typing.Union[_github_c49f935d.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_package_cache: typing.Optional[builtins.bool] = None,
    disable_tsconfig: typing.Optional[builtins.bool] = None,
    disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
    docgen: typing.Optional[builtins.bool] = None,
    docs_directory: typing.Optional[builtins.str] = None,
    entrypoint_types: typing.Optional[builtins.str] = None,
    eslint: typing.Optional[builtins.bool] = None,
    eslint_options: typing.Optional[typing.Union[_javascript_eb5dbe11.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    libdir: typing.Optional[builtins.str] = None,
    projenrc_ts: typing.Optional[builtins.bool] = None,
    projenrc_ts_options: typing.Optional[typing.Union[_typescript_7a66cf84.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    runner: typing.Optional[_typescript_7a66cf84.TypeScriptRunner] = None,
    sample_code: typing.Optional[builtins.bool] = None,
    srcdir: typing.Optional[builtins.str] = None,
    testdir: typing.Optional[builtins.str] = None,
    tsconfig: typing.Optional[typing.Union[_javascript_eb5dbe11.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tsconfig_dev: typing.Optional[typing.Union[_javascript_eb5dbe11.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tsconfig_dev_file: typing.Optional[builtins.str] = None,
    ts_jest_options: typing.Optional[typing.Union[_typescript_7a66cf84.TsJestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    typescript_version: typing.Optional[builtins.str] = None,
    author: builtins.str,
    author_address: builtins.str,
    repository_url: builtins.str,
    compat: typing.Optional[builtins.bool] = None,
    compat_ignore: typing.Optional[builtins.str] = None,
    compress_assembly: typing.Optional[builtins.bool] = None,
    docgen_file_path: typing.Optional[builtins.str] = None,
    exclude_typescript: typing.Optional[typing.Sequence[builtins.str]] = None,
    jsii_version: typing.Optional[builtins.str] = None,
    publish_to_go: typing.Optional[typing.Union[_cdk_bb21cefa.JsiiGoTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_to_maven: typing.Optional[typing.Union[_cdk_bb21cefa.JsiiJavaTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_to_nuget: typing.Optional[typing.Union[_cdk_bb21cefa.JsiiDotNetTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_to_pypi: typing.Optional[typing.Union[_cdk_bb21cefa.JsiiPythonTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    rootdir: typing.Optional[builtins.str] = None,
    validate_tsconfig: typing.Optional[_cdk_bb21cefa.ValidateTsconfig] = None,
    catalog: typing.Optional[typing.Union[_cdk_bb21cefa.Catalog, typing.Dict[builtins.str, typing.Any]]] = None,
    cdktf_version: builtins.str,
    constructs_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
