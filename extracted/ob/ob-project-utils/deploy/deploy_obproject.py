import re
import subprocess
import os
import datetime
import json
import sys
import glob
import requests

try:
    # python >= 3.11
    import tomllib as toml
except ImportError:
    import toml

PROJECT_SPEC = "project_spec.json"
DEFAULT_APP_CONFIG = "config.yml"

# CI Environment Registry
class CIEnvironment:
    """Base class for CI environment handlers"""

    @staticmethod
    def is_active():
        raise NotImplementedError

    @staticmethod
    def get_branch():
        return ""

    @staticmethod
    def get_urls():
        raise NotImplementedError

    @staticmethod
    def post_comment(url, token, comment):
        raise NotImplementedError

    @staticmethod
    def write_summary(markdown):
        pass


class GitHubEnvironment(CIEnvironment):
    @staticmethod
    def is_active():
        return os.getenv("GITHUB_ACTIONS") == "true"

    @staticmethod
    def get_branch():
        # Try PR head ref first, then push ref
        return os.getenv("GH_HEAD_REF") or os.getenv("GH_REF", "")

    @staticmethod
    def get_urls():
        repo = os.getenv("GITHUB_REPOSITORY", "")
        return {
            "commit_url": f"https://github.com/{repo}/commit/",
            "ci_url": f"https://github.com/{repo}/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}",
            "comments_api": os.getenv("COMMENTS_URL"),
            "token": os.getenv("GH_TOKEN"),
            "pr_number": os.getenv("GITHUB_EVENT_NAME") == "pull_request",
        }

    @staticmethod
    def post_comment(url, token, comment):
        requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"token {token}",
            },
            json={"body": comment},
        )

    @staticmethod
    def write_summary(markdown):
        if "GITHUB_STEP_SUMMARY" in os.environ:
            with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as f:
                f.write(markdown)


class AzureDevOpsEnvironment(CIEnvironment):

    @staticmethod
    def get_collection_uri():
        return os.getenv("SYSTEM_COLLECTIONURI", "").rstrip("/")

    @staticmethod
    def is_active():
        return bool(AzureDevOpsEnvironment.get_collection_uri())

    @staticmethod
    def get_branch():
        # For PRs: refs/pull/1/merge -> extract source branch name
        branch = os.getenv("BUILD_SOURCEBRANCH", "")
        if branch.startswith("refs/pull/"):
            # In PR context, get the actual source branch name
            return os.getenv("SYSTEM_PULLREQUEST_SOURCEBRANCH", "").replace(
                "refs/heads/", ""
            )
        else:
            # Direct push: refs/heads/main -> main
            return branch.replace("refs/heads/", "")

    @staticmethod
    def get_urls():
        collection_uri = AzureDevOpsEnvironment.get_collection_uri()
        team_project = os.getenv("SYSTEM_TEAMPROJECT", "")
        repo_name = os.getenv("BUILD_REPOSITORY_NAME", "")

        # Comments API only available in PR context
        pr_id = os.getenv("SYSTEM_PULLREQUEST_PULLREQUESTID")
        comments_api = None
        if pr_id:
            repo_id = os.getenv("BUILD_REPOSITORY_ID", "")
            comments_api = (
                f"{collection_uri}/{team_project}/_apis/git/repositories/"
                f"{repo_id}/pullRequests/{pr_id}/threads?api-version=6.0"
            )

        return {
            "commit_url": f"{collection_uri}/{team_project}/_git/{repo_name}/commit/",
            "ci_url": f"{collection_uri}/{team_project}/_build/results?buildId={os.getenv('BUILD_BUILDID', '')}&view=results",
            "comments_api": comments_api,
            "token": os.getenv("SYSTEM_ACCESSTOKEN"),
            "pr_number": pr_id is not None,
        }

    @staticmethod
    def post_comment(url, token, comment):
        requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={
                "comments": [
                    {"parentCommentId": 0, "content": comment, "commentType": 1}
                ],
                "status": 1,
            },
        )

    @staticmethod
    def write_summary(markdown):
        # Azure DevOps uses ##vso commands for markdown summaries
        summary_file = os.path.abspath("deployment_summary.md")
        with open(summary_file, "w") as f:
            f.write(markdown)
        print(f"##vso[task.uploadsummary]{summary_file}")


class CircleCIEnvironment(CIEnvironment):
    """CI environment handler for CircleCI."""

    @staticmethod
    def is_active():
        return os.getenv("CIRCLECI") == "true"

    @staticmethod
    def get_branch():
        # CIRCLE_BRANCH contains the branch name
        # For PRs from forks, CIRCLE_BRANCH is the PR branch
        return os.getenv("CIRCLE_BRANCH", "")

    @staticmethod
    def get_urls():
        # Determine VCS provider for commit URL
        # CircleCI supports GitHub, Bitbucket, and GitLab
        project_username = os.getenv("CIRCLE_PROJECT_USERNAME", "")
        project_reponame = os.getenv("CIRCLE_PROJECT_REPONAME", "")

        # Try to determine the VCS host from the repository URL
        repo_url = os.getenv("CIRCLE_REPOSITORY_URL", "")
        if "github.com" in repo_url:
            vcs_host = "github.com"
        elif "bitbucket.org" in repo_url:
            vcs_host = "bitbucket.org"
        elif "gitlab.com" in repo_url:
            vcs_host = "gitlab.com"
        else:
            # Default to GitHub
            vcs_host = "github.com"

        commit_url = f"https://{vcs_host}/{project_username}/{project_reponame}/commit/"

        # Check if this is a PR build
        pr_url = os.getenv("CIRCLE_PULL_REQUEST")
        is_pr = pr_url is not None and pr_url != ""

        return {
            "commit_url": commit_url,
            "ci_url": os.getenv("CIRCLE_BUILD_URL", ""),
            "comments_api": None,  # CircleCI doesn't have native PR comments API
            "token": None,  # Would need separate GitHub/Bitbucket token for PR comments
            "pr_number": is_pr,
        }

    @staticmethod
    def post_comment(url, token, comment):
        # CircleCI doesn't have a native PR comments API
        # PR commenting would require using the underlying VCS API (GitHub, Bitbucket, etc.)
        # with a separate token. For now, skip PR commenting in CircleCI.
        pass

    @staticmethod
    def write_summary(markdown):
        # CircleCI doesn't have a native job summary feature like GitHub Actions or Azure DevOps
        # Write to a file that can be stored as an artifact
        summary_file = os.path.abspath("deployment_summary.md")
        with open(summary_file, "w") as f:
            f.write(markdown)
        print(f"Deployment summary written to {summary_file}")
        print("To view this summary, store it as a CircleCI artifact.")


class GitLabEnvironment(CIEnvironment):
    """CI environment handler for GitLab CI/CD."""

    @staticmethod
    def is_active():
        return os.getenv("GITLAB_CI") == "true"

    @staticmethod
    def get_branch():
        # CI_COMMIT_REF_NAME contains the branch or tag name
        # For MRs, CI_MERGE_REQUEST_SOURCE_BRANCH_NAME has the source branch
        return os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME") or os.getenv(
            "CI_COMMIT_REF_NAME", ""
        )

    @staticmethod
    def get_urls():
        project_url = os.getenv("CI_PROJECT_URL", "")
        commit_sha = os.getenv("CI_COMMIT_SHA", "")

        # Check if this is a merge request pipeline
        mr_iid = os.getenv("CI_MERGE_REQUEST_IID")
        is_mr = mr_iid is not None and mr_iid != ""

        # GitLab MR comments API
        # Requires CI_JOB_TOKEN or a personal access token with api scope
        comments_api = None
        if is_mr:
            project_id = os.getenv("CI_PROJECT_ID", "")
            api_url = os.getenv("CI_API_V4_URL", "https://gitlab.com/api/v4")
            comments_api = f"{api_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"

        return {
            "commit_url": f"{project_url}/-/commit/",
            "ci_url": os.getenv("CI_PIPELINE_URL", ""),
            "comments_api": comments_api,
            "token": os.getenv("GITLAB_TOKEN") or os.getenv("CI_JOB_TOKEN"),
            "pr_number": is_mr,
        }

    @staticmethod
    def post_comment(url, token, comment):
        # GitLab uses "notes" for MR comments
        requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "PRIVATE-TOKEN": token,
            },
            json={"body": comment},
        )

    @staticmethod
    def write_summary(markdown):
        # GitLab doesn't have a native job summary feature like GitHub Actions
        # Write to a file that can be stored as an artifact
        summary_file = os.path.abspath("deployment_summary.md")
        with open(summary_file, "w") as f:
            f.write(markdown)
        print(f"Deployment summary written to {summary_file}")
        print("To view this summary, store it as a GitLab CI artifact.")


CI_ENVIRONMENTS = {
    "github": GitHubEnvironment,
    "azuredevops": AzureDevOpsEnvironment,
    "circleci": CircleCIEnvironment,
    "gitlab": GitLabEnvironment,
}

# Global CI environment detection (cached)
_CI_ENV = None
_CI_HANDLER = None


def detect_ci_environment():
    """
    Detect which CI/CD environment we're running in.
    Returns the CI environment name or None if running locally.
    Caches the result to avoid repeated detection.
    """
    global _CI_ENV, _CI_HANDLER

    if _CI_ENV is not None:
        return _CI_ENV

    detected_envs = []

    # Check each CI environment handler
    for name, handler in CI_ENVIRONMENTS.items():
        if handler.is_active():
            detected_envs.append(name)

    # Validate we don't have conflicting environments
    if len(detected_envs) > 1:
        raise RuntimeError(
            f"Multiple CI environments detected: {', '.join(detected_envs)}. "
            f"This usually happens when CI-specific environment variables are manually set. "
            f"Please ensure only one set of CI environment variables is present."
        )

    _CI_ENV = detected_envs[0] if detected_envs else "local"
    _CI_HANDLER = CI_ENVIRONMENTS.get(_CI_ENV, None)
    return _CI_ENV


def get_ci_handler():
    """Get the CI handler for the current environment."""
    if _CI_HANDLER is None:
        detect_ci_environment()
    return _CI_HANDLER


def get_ci_urls():
    """
    Get CI/CD-specific URLs and tokens based on the detected environment.
    Returns a dict with commit_url, ci_url, comments_api, and token.
    """
    handler = get_ci_handler()
    if handler:
        return handler.get_urls()
    else:
        # Local or unknown environment
        return {
            "commit_url": os.getenv("COMMIT_URL", "https://no-commit-url/"),
            "ci_url": os.getenv("CI_URL"),
            "comments_api": None,
            "token": None,
            "pr_number": False,
        }


def listdir(root):
    if os.path.exists(root):
        return os.listdir(root)
    else:
        return []


def read_toml_config(filename):
    with open(filename) as f:
        return toml.loads(f.read())


def detect_multi_project_config():
    """
    Detect and validate multi-project configuration.
    Returns (is_multi_project, multi_config, project_dirs) tuple.
    """
    multi_project_file = "obproject_multi.toml"
    single_project_file = "obproject.toml"

    # Check current directory for config files
    has_multi = os.path.exists(multi_project_file)
    has_single = os.path.exists(single_project_file)

    # Validation: Can't have both at the same level
    if has_multi and has_single:
        raise RuntimeError(
            f"Found both {multi_project_file} and {single_project_file} in the same directory. "
            f"Please use either single-project ({single_project_file}) or "
            f"multi-project ({multi_project_file}) configuration, not both."
        )

    if has_multi:
        # Check for multiple multi-project files (walking up the tree)
        multi_files_found = []
        current_dir = os.path.abspath(".")
        root_dir = os.path.abspath(os.sep)

        while current_dir != root_dir:
            check_file = os.path.join(current_dir, multi_project_file)
            if os.path.exists(check_file):
                multi_files_found.append(check_file)
            parent = os.path.dirname(current_dir)
            if parent == current_dir:  # Reached filesystem root
                break
            current_dir = parent

        if len(multi_files_found) > 1:
            raise RuntimeError(
                f"Found multiple {multi_project_file} files in the directory tree:\n"
                + "\n".join(f"  - {f}" for f in multi_files_found)
                + f"\nOnly one {multi_project_file} is allowed per repository."
            )

        # Read and validate multi-project config
        multi_config = read_toml_config(multi_project_file)

        if "projects" not in multi_config:
            raise RuntimeError(
                f"{multi_project_file} must contain a [projects] section with project mappings."
            )

        projects = multi_config["projects"]
        if not isinstance(projects, dict):
            raise RuntimeError(
                f"[projects] section in {multi_project_file} must be a table/dict of project names to paths."
            )

        if not projects:
            raise RuntimeError(
                f"[projects] section in {multi_project_file} cannot be empty."
            )

        # Validate all project directories exist and have obproject.toml
        project_dirs = {}
        for name, path in projects.items():
            full_path = os.path.abspath(path)
            if not os.path.isdir(full_path):
                raise RuntimeError(
                    f"Project '{name}' points to non-existent directory: {path}"
                )

            project_toml = os.path.join(full_path, single_project_file)
            if not os.path.exists(project_toml):
                raise RuntimeError(
                    f"Project '{name}' directory '{path}' does not contain {single_project_file}"
                )

            project_dirs[name] = full_path

        return True, multi_config, project_dirs

    # Single project mode
    if not has_single:
        raise RuntimeError(
            f"No {single_project_file} or {multi_project_file} found in the current directory."
        )

    return False, None, None


def get(key, default=None):
    config = read_toml_config("obproject.toml")
    return config.get(key, default)


def get_environment_name():
    """
    Map current branch to environment name using branch_to_environment mapping.
    Supports glob patterns (e.g., 'feature/*' matches 'feature/new-ui').
    Returns 'default' if no mapping matches.
    """
    import fnmatch

    branch = git_branch()
    # Use PROJECT_ROOT to find obproject.toml
    config_path = os.path.join(PROJECT_ROOT, "obproject.toml")
    config = read_toml_config(config_path)
    branch_map = config.get("branch_to_environment", {})

    # Check exact match first
    if branch in branch_map:
        return branch_map[branch]

    # Check glob patterns
    for pattern, env in branch_map.items():
        if fnmatch.fnmatch(branch, pattern):
            return env

    # Fallback
    return "default"


def get_branch_config(key, default=None):
    """
    Get branch-specific configuration value for the current environment.
    Looks up config in [environments.<env>] based on current branch.


    """
    env_name = get_environment_name()
    # Use PROJECT_ROOT to find obproject.toml
    config_path = os.path.join(PROJECT_ROOT, "obproject.toml")
    config = read_toml_config(config_path)
    environments = config.get("environments", {})
    env_config = environments.get(env_name, {})

    return env_config.get(key, default)


def get_flow_configs():
    """
    Get flow-specific configs for current environment.

    Looks up [environments.<env>.flow_configs] and returns a dict of
    config_name -> absolute_path mappings.

    Example obproject.toml:
        [environments.production.flow_configs]
        model_config = "configs/model.prod.json"
        training_config = "configs/training.prod.json"

    Returns:
        Dict mapping config names to absolute paths
    """
    env_name = get_environment_name()
    config_path = os.path.join(PROJECT_ROOT, "obproject.toml")
    config = read_toml_config(config_path)
    environments = config.get("environments", {})
    env_config = environments.get(env_name, {})

    flow_configs = env_config.get("flow_configs", {})

    # Resolve paths relative to PROJECT_ROOT
    resolved = {}
    for key, path in flow_configs.items():
        abs_path = os.path.join(PROJECT_ROOT, path)
        if os.path.exists(abs_path):
            resolved[key] = abs_path
        else:
            print(f"⚠️  Warning: flow_config '{key}' path not found: {abs_path}")

    return resolved


def get_flow_config_names(flow_file_path):
    """
    Parse a flow file to find Config() declarations.

    Returns a set of config names declared in the flow.
    Uses simple regex to avoid full AST parsing.
    """
    import re

    config_names = set()
    try:
        with open(flow_file_path, "r") as f:
            content = f.read()

        # Match patterns like: Config("name" or Config('name'
        # Also match: = Config("name" for class attributes
        pattern = r'Config\s*\(\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content)
        config_names.update(matches)
    except Exception:
        pass

    return config_names


def project():
    project_name = get("project")
    if project_name:
        return re.sub(r"[-/]", "_", project_name).lower()

    try:
        repo_path = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        project_name = os.path.basename(repo_path)
        return re.sub(r"[-/]", "_", project_name).lower()
    except subprocess.CalledProcessError:
        raise RuntimeError("No project name found in obproject.toml or git repo!")


def git_branch():
    try:
        # Try CI environment first
        handler = get_ci_handler()
        if handler:
            ci_branch = handler.get_branch()
            if ci_branch:
                return ci_branch

        # Fall back to local git
        current_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return current_branch
    except subprocess.CalledProcessError:
        return ""


def is_main_branch():
    branch_name = get("branch") or git_branch()
    return branch_name in ("main", "master")


def branch():
    branch_name = get("branch") or git_branch()
    if is_main_branch():
        print("Deploying to the main branch (aka --production)\n")
        return branch_name
    elif branch_name:
        trimmed_branch = re.sub(r"[-/]", "_", branch_name).lower()
        print(f"Deploying to branch {trimmed_branch}\n")
        return trimmed_branch
    else:
        raise Exception("Branch not found - is this a Git repo?")


def version():
    ver = get("version")
    if ver:
        return ver

    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
        return git_sha
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "No version found in obproject.toml and not in a git repository!"
        )


def current_perimeter():
    # Check branch-specific perimeter first
    branch_perimeter = get_branch_config("perimeter")
    if branch_perimeter:
        return branch_perimeter

    try:
        result = subprocess.check_output(
            ["outerbounds", "perimeter", "show-current", "-o", "json"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        data = json.loads(result)
        return data["data"]["current_perimeter"]
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        config = read_toml_config("obproject.toml")
        return config.get("perimeter", os.environ.get("PERIMETER_NAME", "default"))


def created_at():
    created_at_ts = get("created_at")
    if created_at_ts:
        return created_at_ts

    try:
        root_commit = (
            subprocess.check_output(
                ["git", "rev-list", "--max-parents=0", "HEAD"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            .strip()
            .split("\n")[0]
        )

        first_commit_timestamp = subprocess.check_output(
            ["git", "show", "-s", "--format=%at", root_commit],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()

        dt = datetime.datetime.fromtimestamp(
            int(first_commit_timestamp), tz=datetime.timezone.utc
        )
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    except subprocess.CalledProcessError:
        pass
    return "2025-01-01T00:00:00.000000Z"


# These globals will be set per project in multi-project mode
PROJECT_ROOT = None
REPO_ROOT = None  # Set in multi-project mode to the directory containing obproject_multi.toml
DEPLOYED_AT = None
PROJECT = None
GIT_BRANCH = None
BRANCH = None
VERSION = None
PERIMETER = None


def init_project_globals(project_root=None):
    """Initialize global variables for a specific project directory."""
    global PROJECT_ROOT, DEPLOYED_AT, PROJECT, GIT_BRANCH, BRANCH, VERSION, PERIMETER

    # Save current directory and change to project root if specified
    original_cwd = os.getcwd()
    if project_root:
        os.chdir(project_root)

    try:
        PROJECT_ROOT = os.path.abspath(os.getcwd())
        DEPLOYED_AT = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        PROJECT = project()
        GIT_BRANCH = git_branch()
        BRANCH = branch()
        VERSION = version()
        PERIMETER = current_perimeter()
    finally:
        # Always restore original directory
        os.chdir(original_cwd)


def pyproject_cmd(flag):
    conf = read_toml_config(os.path.join(PROJECT_ROOT, "obproject.toml"))
    include_pyproject = conf.get("dependencies", {}).get("include_pyproject_toml", True)
    project_deps = os.path.join(PROJECT_ROOT, "pyproject.toml")
    if os.path.exists(project_deps) and include_pyproject:
        return flag + [project_deps]
    else:
        return []


def deploy_flows(flows):
    project_config = os.path.abspath("obproject.toml")
    project_spec = os.path.abspath(PROJECT_SPEC)

    # Get flow-specific configs from [environments.<env>.flow_configs]
    all_flow_configs = get_flow_configs()

    if is_main_branch():
        project_branch = "--production"
    else:
        project_branch = f"--branch={BRANCH}"
    for flow_dir, flow_file, flow_spec in flows:
        # Detect which configs this flow actually uses
        # flow_file is already the full relative path (e.g., "flows/train/flow.py")
        declared_configs = get_flow_config_names(flow_file)

        cmd = [
            sys.executable,
            os.path.basename(flow_file),
            project_branch,
            "--config",
            "project_spec",
            project_spec,
            "--config",
            "project_config",
            project_config,
            "--package-suffixes=.html",
            "--environment=fast-bakery",
        ]

        # Only add configs that this flow declares
        for config_name, config_path in all_flow_configs.items():
            if config_name in declared_configs:
                cmd.extend(["--config", config_name, config_path])

        cmd += pyproject_cmd(["--config", "project_deps"])
        cmd += [
            "argo-workflows",
            "create",
        ]
        print(f"⚙️ Deploying flow at {flow_dir}:")

        # Set PYTHONPATH to project root so flows can import shared modules
        # (e.g., `from src import ...`). This enables METAFLOW_PACKAGE_POLICY
        # to work - modules with METAFLOW_PACKAGE_POLICY="include" in their
        # __init__.py will be automatically included in the code package.
        #
        # In multi-project mode, also include REPO_ROOT so flows can import
        # shared modules at the repository root level (e.g., `import utils`
        # when utils/ is at repo root, not inside the project directory).
        env = os.environ.copy()
        pythonpath_parts = [PROJECT_ROOT]
        if REPO_ROOT and REPO_ROOT != PROJECT_ROOT:
            pythonpath_parts.append(REPO_ROOT)
        existing_pythonpath = env.get("PYTHONPATH", "")
        if existing_pythonpath:
            pythonpath_parts.append(existing_pythonpath)
        env["PYTHONPATH"] = ":".join(pythonpath_parts)

        subprocess.run(cmd, check=True, cwd=flow_dir, env=env)


def app_config_has_dependencies(config_path):
    """Check if app config.yml has a dependencies section."""
    try:
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config and "dependencies" in config
    except Exception:
        return False


def deploy_apps():
    """Deploy apps from project root.

    Apps are deployed from the project root directory so that the entire
    project structure is packaged. This allows apps to import from src/.

    Apps should use full module paths in their gunicorn commands, e.g.:
        gunicorn deployments.api.app:app

    The config.yml should NOT use package.src_paths since the whole project
    is already packaged from root.
    """
    num_apps = 0
    for app_dir in listdir("deployments"):
        app_path = os.path.join("deployments", app_dir)
        # Skip non-directories (e.g., __init__.py files)
        if not os.path.isdir(app_path):
            continue

        # Skip directories that start with _ or . (e.g., __pycache__, .git)
        if app_dir.startswith(('_', '.')):
            continue

        # Use branch-specific deployment config
        app_config = os.path.join(app_path, get_branch_config("deployment_config", DEFAULT_APP_CONFIG))
        # Skip directories without a config file - they're not apps
        # Check for both .yml and .yaml extensions
        if not os.path.exists(app_config):
            # Try .yaml if .yml doesn't exist
            if app_config.endswith('.yml'):
                app_config_yaml = app_config[:-4] + '.yaml'
                if os.path.exists(app_config_yaml):
                    app_config = app_config_yaml
                else:
                    continue
            elif app_config.endswith('.yaml'):
                app_config_yml = app_config[:-5] + '.yml'
                if os.path.exists(app_config_yml):
                    app_config = app_config_yml
                else:
                    continue
            else:
                continue

        num_apps += 1
        cmd = [
            "outerbounds",
            "app",
            "deploy",
            "--no-loader",
            "--config-file",
            app_config,
            f"--project={PROJECT}",
            f"--branch={BRANCH}",
            "--readiness-condition=async",
            "--readiness-wait-time=0",
            "--env",
            f"OB_PROJECT={PROJECT}",
            "--env",
            f"OB_BRANCH={BRANCH}",
            # Add project root to PYTHONPATH so apps can import from src/
            "--env",
            "PYTHONPATH=.",
        ]
        # Only add --dep-from-pyproject if config.yml doesn't have dependencies
        if not app_config_has_dependencies(app_config):
            cmd += pyproject_cmd(["--dep-from-pyproject"])
        print(f"⚙️ Deploying app at {app_dir}:")
        print(f"   Running command: {' '.join(cmd)}")
        print(f"   Working directory: {os.getcwd()}")

        # Run with output capture for better error diagnostics
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   Error output: {result.stderr}")
            print(f"   Standard output: {result.stdout}")
            raise subprocess.CalledProcessError(
                result.returncode, cmd, result.stdout, result.stderr
            )
        else:
            print(f"   {result.stdout}")
    return num_apps


"""
def persist_asset(config, previous_version=None, asset_dir=None):
    def _config_hash(config):
        json_cfg = json.dumps(config, sort_keys=True)
        return hashlib.sha256(json_cfg.encode('utf-8')).hexdigest()

    config_hash = _config_hash(config)
    if asset_dir:
        files = config['files']
    else:
        new_ver = f'version:{config_hash}'
"""


def register_assets():
    from obproject.assets import Asset

    # Read custom folder names from obproject.toml [obproject_dirs] section
    conf = read_toml_config(os.path.join(PROJECT_ROOT, "obproject.toml"))
    obproject_dirs = conf.get("obproject_dirs", {})
    models_folder = obproject_dirs.get("models", "models")
    data_folder = obproject_dirs.get("data", "data")

    def ensure_types(d):
        for k, v in d.items():
            if not (isinstance(k, str) and isinstance(v, str)):
                raise AttributeError(
                    f"Invalid property '{k}': Both the key and value need to be strings"
                )
        return d

    # FIXME entity_ref should be more meaningful for CI/CD - fix kind and id
    entity_ref = {
        "entity_kind": "task",
        "entity_id": f"deployer",
    }
    asset = Asset(project=PROJECT, branch=BRANCH, entity_ref=entity_ref)

    def register(asset_type, register_func):
        for asset_dir in listdir(asset_type):
            root = os.path.join(asset_type, asset_dir)
            try:
                config = read_toml_config(os.path.join(root, "asset_config.toml"))
                markdown = ""
                readme = os.path.join(root, "README.md")
                if os.path.exists(readme):
                    with open(readme) as f:
                        markdown = f.read().strip()

                # note that we don't add an instance-level description here,
                # we just populate the top-level info in the project spec
                register_func(
                    config["id"],
                    kind=config.get("kind", asset_type.strip("s")),
                    blobs=config.get("blobs", []),
                    tags=ensure_types(config.get("tags", {})),
                    annotations=ensure_types(config.get("properties", {})),
                )
                # pass down information for the spec
                yield {
                    "display_name": config["name"],
                    "id": config["id"],
                    "card_markdown": markdown,
                    "description": config.get("description", ""),
                    "icon": config.get("icon"),
                }
                print(f"📝 Registered {asset_type.strip('s')}: {config['id']}")
            except:
                print(f"❌ parsing {root} failed:")
                raise

    return list(register(models_folder, asset.register_model_asset)), list(
        register(data_folder, asset.register_data_asset)
    )


def git_log():
    # Format: SHA | Timestamp | Author | Subject | Body
    format_str = "%H|%aI|%ae|%s|%b"
    result = subprocess.run(
        ["git", "log", "-20", f"--pretty=format:{format_str}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    # Get commit URL from CI environment
    ci_urls = get_ci_urls()
    repo = ci_urls.get("commit_url", "https://no-commit-url/")

    commits = []
    for line in result.stdout.split("\n"):
        parts = line.split("|", 4)
        if len(parts) < 5:
            continue
        sha, timestamp, email, title, body = parts

        commit = {
            "commit_sha": sha,
            "commit_link": f"{repo}{sha}",
            # "container_image": f"some.container:image:{sha}",  # Placeholder logic
            "owner": email,
            "pr_description": body.strip().replace("\n", " "),
            "pr_title": title.strip(),
            "timestamp": timestamp,
        }
        commits.append(commit)

    return commits


def summary(conf):
    platform = get("platform")
    spec = conf.get("spec", {})
    project_title = conf.get("title", conf.get("project"))
    project_name = conf.get("project")
    branch_name = conf.get("branch", "main")
    updated_at = spec.get("updated_at", "Unknown")
    try:
        dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        formatted_deployed = dt.strftime("%Y-%m-%d %H:%M UTC")
    except:
        formatted_deployed = updated_at

    markdown_lines = [
        f"### 🚧 {project_title} updated!",
        f"→ [Open in Outerbounds](https://ui.{platform}/dashboard/p/{PERIMETER}/j/{project_name}/b/{branch_name}/overview)",
        "",
        f"🗂️ **Project:** `{project_title}`",
        f"🌿 **Branch:** `{branch_name}`",
        f"🕒 **Last deployed:** {formatted_deployed}",
        "",
        "| Category         | Name/ID                                  | Description                                  |",
        "|------------------|-------------------------------------------|----------------------------------------------|",
    ]

    models = spec.get("models", [])
    if models:
        for i, model in enumerate(models):
            prefix = "🧠 **Models**" if i == 0 else ""
            name = model.get(
                "display_name",
                model.get(
                    "id",
                ),
            )
            description = model.get("description", "AI model for inference")
            model_id = model.get("id")
            model_url = f"https://ui.{platform}/dashboard/p/{PERIMETER}/j/{project_name}/b/{branch_name}/models/{model_id}"
            markdown_lines.append(
                f"| {prefix:<15} | [`{name}`]({model_url}) | {description[:42]}{'...' if len(description) > 42 else ''} |"
            )

    data_assets = spec.get("data", [])
    if data_assets:
        for i, data in enumerate(data_assets):
            prefix = "📦 **Data Assets**" if i == 0 else ""
            name = data.get("display_name", data.get("id"))
            description = data.get(
                "description", "Dataset for model training/evaluation"
            )
            data_id = data.get("id")
            data_url = f"https://ui.{platform}/dashboard/p/{PERIMETER}/j/{project_name}/b/{branch_name}/data/{data_id}"
            markdown_lines.append(
                f"| {prefix:<15} | [`{name}`]({data_url}) | {description[:42]}{'...' if len(description) > 42 else ''} |"
            )

    workflows = spec.get("workflows", [])
    if workflows:
        for i, workflow in enumerate(workflows):
            prefix = "⚙️ **Workflows**" if i == 0 else ""
            name = workflow.get("flow_name")
            description = workflow.get("markdown_description")
            template_id = workflow.get("flow_template_id", name.lower())
            workflow_url = (
                f"https://ui.{platform}/dashboard/flows/p/{PERIMETER}/{template_id}"
            )
            markdown_lines.append(
                f"| {prefix:<15} | [`{name}`]({workflow_url}) | {description[:42]}{'...' if len(description) > 42 else ''} |"
            )

    # markdown_lines.extend(
    #     [
    #         f"| {'🚀 **Deployments**':<15} | [`staging`](https://staging.example.com) | Model deployed to staging environment |",
    #         f"| {'':<15} | [`production`](https://prod.example.com) | Live production model endpoint |",
    #     ]
    # )

    markdown = "\n".join(markdown_lines)

    # Write summary based on CI environment
    handler = get_ci_handler()
    if handler:
        handler.write_summary(markdown)

    comment_pr(markdown)

    return markdown


def comment_pr(comment):
    handler = get_ci_handler()
    ci_urls = get_ci_urls()

    token = ci_urls.get("token")
    url = ci_urls.get("comments_api")

    if not token:
        print(
            f"No auth token for {detect_ci_environment()} environment. Skipping PR commenting."
        )
        return
    if not url:
        print("Not in PR context. Skipping PR commenting.")
        return

    try:
        if handler:
            handler.post_comment(url, token, comment)
    except Exception as ex:
        print(f"Posting comment to {detect_ci_environment()} failed:", str(ex))


def check_evaluation_flow(flow_src):
    EVAL_CARD_RE = re.compile(
        r"""
        @card                       # Match @card decorator
        \s*                         # Optional whitespace
        \(                          # Opening parenthesis
        \s*
        (                           # Capture args (for further parsing)
            [^)]*?                  #   Non-greedy: everything until...
            \bid\s*=\s*             #   ...id =
            (['"]{1,3})             #   ...with matching quotes
            project_eval            #   ...the target id value
            \2                      #   ...closing quote matches opening
            [^)]*                   #   ...and other optional args
        )
        \)                          # Closing parenthesis
        \s+@step\s+def\s+           # Followed by @step and def
        (\w+)                       # Capture method name
        \s*\(                       # Followed by (
    """,
        re.VERBOSE | re.MULTILINE | re.DOTALL,
    )
    CARD_TYPE_RE = re.compile(r'type\s*=\s*([\'"]{1,3})(.*?)\1')
    matches = EVAL_CARD_RE.findall(flow_src)
    if len(matches) > 1:
        raise Exception("Specify at most one @card(id='project_eval')")
    elif matches:
        [(args, _, step_name)] = matches
        [(_, card_type)] = CARD_TYPE_RE.findall(args)
        return {"card_type": card_type, "is_eval_flow": True, "step_name": step_name}


def get_metaflow_branch():
    if is_main_branch():
        return "prod"
    else:
        return f"test.{BRANCH}"


def discover_flows():
    # find a flow class that subclasses from ProjectFlow (amongst other superclasses)
    FLOW_RE = re.compile(
        r"^class\s+(\w+)\s*\([^)]*?\bProjectFlow\b[^)]*\)\s*:", re.MULTILINE
    )
    # find steps with a @highlight decorator
    HIGHLIGHT_RE = re.compile(
        r"@highlight\s+(?:@\w+(?:\([^)]*\))?\s+)*@step\s+def\s+(\w+)\s*\(", re.MULTILINE
    )
    metaflow_branch = get_metaflow_branch()
    evals = []
    flows = []

    for flow_dir in listdir("flows"):
        root = os.path.join("flows", flow_dir)
        flowfile = os.path.join(root, "flow.py")
        try:
            # read flow
            with open(flowfile) as f:
                src = f.read()

            # flow_name
            matches = FLOW_RE.search(src)
            if matches:
                flow_name = matches.group(1)
            else:
                raise Exception(
                    f"Could not find a flow subclassing from ProjectFlow in {flowfile}"
                )
            flow_template_id = (
                f"{PROJECT}.{metaflow_branch}.{flow_name.lower()}".replace("_", "")
            )

            # highlights
            hl_steps = HIGHLIGHT_RE.findall(src)
            if len(hl_steps) > 1:
                raise Exception(
                    "Currently you can have at most one @highlight per flow"
                )
            elif hl_steps:
                highlight_step_name = hl_steps[0]
            else:
                highlight_step_name = None

            # markdown description
            markdown = ""
            readme = os.path.join(root, "README.md")
            if os.path.exists(readme):
                with open(readme) as f:
                    markdown = f.read().strip()

            # check if this flow is an evaluation flow
            eval_info = check_evaluation_flow(src)
            if eval_info:
                eval_info.update(
                    {
                        "metaflow_branch": metaflow_branch,
                        "metaflow_project": PROJECT,
                        "workflow_name": flow_name,
                    }
                )
                evals.append(eval_info)

            flows.append(
                (
                    root,
                    flowfile,
                    {
                        "flow_name": flow_name,
                        "flow_template_id": flow_template_id,
                        "highlight_step_name": highlight_step_name,
                        "markdown_description": markdown,
                        "metaflow_branch": metaflow_branch,
                        "metaflow_project": PROJECT,
                        "tags": [],
                    },
                )
            )
            print(f"🌀 Found flow: {flow_name}")
            if highlight_step_name:
                print(f"    ✨ @highlight included from the {highlight_step_name} step")
            if eval_info:
                print(f"    📊 this flow is an evaluation flow")

        except:
            print(f"❌ parsing a flow at {flowfile} failed:")
            raise
    return flows, evals


def create_spec(flows, evals, data, models):
    commits = git_log()
    first = commits[0]
    code = {
        "display_name": f"{first['pr_title']} ({first['commit_sha'][:6]})",
        "url": first["commit_link"],
    }
    # Get CI URL from environment detection
    ci_urls = get_ci_urls()
    ci_url = ci_urls.get("ci_url")
    # should match schema https://github.com/outerbounds/obp-foundation/blob/master/utqiagvik/backend/internal/services/assets_api/internal/api_types/api_types.go#L47
    # and spec should be https://github.com/outerbounds/obp-foundation/blob/master/utqiagvik/backend/internal/services/assets_api/internal/api_types/api_types.go#L54

    if os.path.exists("README.md"):
        with open("README.md") as f:
            markdown = f.read()
    else:
        markdown = None

    conf = {
        "perimeter": current_perimeter(),
        "project": PROJECT,
        "branch": BRANCH,
        "version_id": VERSION,
        "spec": {
            "metaflow_project": PROJECT,
            "metaflow_branch": get_metaflow_branch(),
            "card_info": evals,
            "ci_url": ci_url,
            "code": [code],
            "created_at": datetime.datetime.fromisoformat(
                created_at().replace("Z", "+00:00")
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data": data,
            "deployment_events": commits[:10],
            "markdown": markdown,
            "models": models,
            "perimeter": current_perimeter(),
            "project_branch": BRANCH,
            "project_name": PROJECT,
            "title": get("title"),
            "updated_at": datetime.datetime.fromisoformat(
                DEPLOYED_AT.replace("Z", "+00:00")
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "workflows": [f for _, _, f in flows],
        },
    }

    def clean(obj):
        return (
            {k: clean(v) for k, v in obj.items() if v is not None}
            if isinstance(obj, dict)
            else (
                [clean(item) for item in obj if item is not None]
                if isinstance(obj, list)
                else obj if obj is not None else None
            )
        )

    spec = clean(conf)
    with open(PROJECT_SPEC, "w") as f:
        json.dump(spec, f)
    print(f"Config written to {PROJECT_SPEC}")
    return spec


def register_spec(spec):
    cmd = ["outerbounds", "flowproject", "set-metadata", json.dumps(spec)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def deploy_single_project(project_name=None):
    """Deploy a single project. If project_name is provided, it's from a multi-project setup."""
    cwd = os.getcwd()
    try:
        if project_name:
            print(f"\n{'='*60}")
            print(f"🚀 Deploying project: {project_name}")
            print(f"{'='*60}\n")

        # Switch to branch-specific perimeter if configured
        target_perimeter = get_branch_config("perimeter")
        if target_perimeter:
            print(f"🔄 Switching to perimeter: {target_perimeter}")
            try:
                result = subprocess.run(
                    ["outerbounds", "perimeter", "switch", "--id", target_perimeter, "--force"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"✅ Switched to perimeter: {target_perimeter}")
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.strip() if e.stderr else e.stdout.strip()
                print(f"\n❌ Failed to switch to perimeter '{target_perimeter}'")
                print(f"   Error: {error_msg}\n")
                sys.exit(1)

        print("🟩🟩🟩 Registering Assets")
        models, data = register_assets()
        print(
            f"✅ {len(data)} data assets and {len(models)} models registered successfully"
        )

        print("🟩🟩🟩 Discovering Flows")
        flows, evals = discover_flows()
        print(
            f"✅ {len(flows)} flows parsed successfully - found {len(evals)} evaluation flows"
        )

        print("🟩🟩🟩 Updating Project Specification")
        spec = create_spec(flows, evals, data, models)
        print(f"✅ project specification ok")

        if not os.environ.get("SPEC_ONLY"):
            print("🟩🟩🟩 Deploying flows")
            deploy_flows(flows)
            print(f"✅ {len(flows)} flows deployed successfully")

            print("🟩🟩🟩 Deploying apps and endpoints")
            num_apps = deploy_apps()
            print(f"✅ {num_apps} endpoints and apps deployed successfully")

            print("🟩🟩🟩 Pushing Project Specification")
            register_spec(spec)
            print(f"✅ project updated successfully")

            summary(spec)
            print("✅✅✅ Deployment successful!")

        return True
    except Exception as e:
        if project_name:
            print(f"\n❌ Failed to deploy project '{project_name}': {str(e)}\n")
        raise
    finally:
        os.chdir(cwd)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Deploy Outerbounds projects")
    parser.add_argument(
        "--project",
        help="Deploy only the specified project from obproject_multi.toml",
        default=None,
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Deploy all projects in obproject_multi.toml (default if no --project specified)",
    )
    args = parser.parse_args()

    global REPO_ROOT

    is_multi, _, project_dirs = detect_multi_project_config()
    if is_multi:
        # Store the repo root (where obproject_multi.toml lives) so shared
        # modules at repo root level can be imported by flows in sub-projects.
        REPO_ROOT = os.path.abspath(os.getcwd())

        if args.project:
            # Deploy specific project
            if args.project not in project_dirs:
                available = ", ".join(sorted(project_dirs.keys()))
                raise RuntimeError(
                    f"Project '{args.project}' not found in obproject_multi.toml.\n"
                    f"Available projects: {available}"
                )

            project_root = project_dirs[args.project]
            os.chdir(project_root)
            init_project_globals()
            deploy_single_project(args.project)
        else:
            # Deploy all projects
            print(f"🌟 Found {len(project_dirs)} projects to deploy")
            failed_projects = []

            for project_name, project_root in project_dirs.items():
                try:
                    os.chdir(project_root)
                    init_project_globals()
                    deploy_single_project(project_name)
                except Exception as e:
                    failed_projects.append((project_name, str(e)))
                    if not os.environ.get("CONTINUE_ON_ERROR"):
                        raise

            if failed_projects:
                print(f"\n❌ {len(failed_projects)} project(s) failed to deploy:")
                for name, error in failed_projects:
                    print(f"  - {name}: {error}")
                raise RuntimeError("Some projects failed to deploy")
            else:
                print(f"\n✅ All {len(project_dirs)} projects deployed successfully!")
    else:
        # Single project mode
        init_project_globals()
        deploy_single_project()


if __name__ == "__main__":
    main()
