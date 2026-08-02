import os
from typing import Optional

from python_agent.common.constants import PREFIXES

ci_env_vars = [
    "BUILD_NUMBER",
    "BUILD_ID",
    "BUILD_URL",
    "NODE_NAME",
    "JOB_NAME",
    "BUILD_TAG",
    "JENKINS_URL",
    "WORKSPACE",
    "GIT_COMMIT",
    "GIT_URL",
    "GIT_BRANCH",
    "TEAMCITY_VERSION",
    "TEAMCITY_PROJECT_NAME",
    "TEAMCITY_BUILDCONF_NAME",
    "TEAMCITY_BUILD_IS_PERSONAL",
    "TEAMCITY_BUILD_PROPERTIES_FILE",
    "CIRCLE_BRANCH",
    "CIRCLE_BUILD_NUM",
    "CIRCLE_BUILD_URL",
    "CIRCLE_JOB",
    "CIRCLE_NODE_INDEX",
    "CIRCLE_NODE_TOTAL",
    "CIRCLE_PR_NUMBER",
    "CIRCLE_PR_REPONAME",
    "CIRCLE_PULL_REQUEST",
    "CIRCLE_PULL_REQUESTS",
    "CIRCLE_REPOSITORY_URL",
    "CIRCLE_SHA1",
    "CIRCLE_TAG",
    "CIRCLE_WORKFLOW_ID",
    "CIRCLE_WORKFLOW_JOB_ID",
    "CIRCLE_WORKFLOW_WORKSPACE_ID",
    "CIRCLE_WORKING_DIRECTORY",
    "CI_BUILDS_ID",
    "CI_COMMIT_AUTHOR",
    "CI_COMMIT_BEFORE_SHA",
    "CI_COMMIT_BRANCH",
    "CI_COMMIT_DESCRIPTION",
    "CI_COMMIT_MESSAGE",
    "CI_COMMIT_REF_NAME",
    "CI_COMMIT_SHORT_SHA",
    "CI_COMMIT_SHA",
    "CI_COMMIT_TAG",
    "CI_COMMIT_TITLE",
    "CI_COMMIT_TIMESTAMP",
    "CI_CONCURRENT_ID",
    "CI_CONCURRENT_PROJECT_ID",
    "CI_CONFIG_PATH",
    "CI_DEFAULT_BRANCH",
    "CI_DEPENDENCY_PROXY_SERVER",
    "CI_DISPOSABLE_ENVIRONMENT",
    "CI_ENVIRONMENT_NAME",
    "CI_ENVIRONMENT_SLUG",
    "CI_ENVIRONMENT_URL",
    "CI_ENVIRONMENT_ACTION",
    "CI_ENVIRONMENT_TIER",
    "CI_JOB_ID",
    "CI_JOB_NAME",
    "CI_JOB_STAGE",
    "CI_JOB_IMAGE",
    "CI_JOB_URL",
    "CI_JOB_STARTED_AT",
    "CI_KUBERNETES_ACTIVE",
    "CI_NODE_INDEX",
    "CI_NODE_TOTAL",
    "CI_PIPELINE_URL",
    "CI_PIPELINE_DIR",
    "CI_PROJECT_DIR",
    "CI_PROJECT_NAME",
    "CI_PROJECT_NAMESPACE",
    "CI_PROJECT_PATH",
    "CI_PROJECT_PATH_SLUG",
    "CI_PROJECT_REPOSITORY_LANGUAGES",
    "CI_PROJECT_ROOT_NAMESPACE",
    "CI_PROJECT_TITLE",
    "CI_PROJECT_URL",
    "CI_PROJECT_DESCRIPTION",
    "CI_REGISTRY_IMAGE",
    "CI_REPOSITORY_URL",
    "CI_SERVER_HOST",
    "CI_SERVER_NAME",
    "CI_SERVER_URL",
    "CI_SERVER_VERSION_MAJOR",
    "CI_SERVER_VERSION_MINOR",
    "CI_SERVER_VERSION_PATCH",
    "CI_SERVER_VERSION",
    "GITLAB_CI",
    "CI_MERGE_REQUEST_APPROVED",
    "CI_MERGE_REQUEST_ASSIGNEES",
    "CI_MERGE_REQUEST_ID",
    "CI_MERGE_REQUEST_IID",
    "CI_MERGE_REQUEST_PROJECT_ID",
    "CI_MERGE_REQUEST_PROJECT_PATH",
    "CI_MERGE_REQUEST_PROJECT_URL",
    "CI_MERGE_REQUEST_REFS_PATH",
    "CI_MERGE_REQUEST_LABELS",
    "CI_MERGE_REQUEST_MILESTONE",
    "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME",
    "CI_MERGE_REQUEST_SOURCE_BRANCH_SHA",
    "CI_MERGE_REQUEST_SOURCE_PROJECT_ID",
    "CI_MERGE_REQUEST_SOURCE_PROJECT_PATH",
    "CI_MERGE_REQUEST_SOURCE_PROJECT_URL",
    "CI_MERGE_REQUEST_TARGET_BRANCH_NAME",
    "CI_MERGE_REQUEST_TARGET_BRANCH_SHA",
    "CI_MERGE_REQUEST_TITLE",
    "CI_MERGE_REQUEST_EVENT_TYPE",
    "CI_MERGE_REQUEST_DIFF_ID",
    "CI_MERGE_REQUEST_DIFF_BASE_SHA",
    "CI_EXTERNAL_PULL_REQUEST_IID",
    "CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY",
    "CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY",
    "CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME",
    "CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME",
    "CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA",
    "CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA",
    "CI",
    "GITHUB_ACTION",
    "GITHUB_ACTION_PATH",
    "GITHUB_ACTION_REPOSITORY",
    "GITHUB_BASE_REF",
    "GITHUB_ENV",
    "GITHUB_HEAD_REF",
    "GITHUB_JOB",
    "GITHUB_PATH",
    "GITHUB_REF",
    "GITHUB_REF_NAME",
    "GITHUB_REF_TYPE",
    "GITHUB_REPOSITORY",
    "GITHUB_REPOSITORY_OWNER",
    "GITHUB_SHA",
    "GITHUB_STEP_SUMMARY",
    "GITHUB_WORKFLOW",
    "GITHUB_WORKSPACE",
    "RUNNER_OS",
    "RUNNER_TEMP",
    "RUNNER_ARCH",
    "RUNNER_NAME",
    "RUNNER_TOOL_CACHE",
]


def get_ci_env_vars():
    env_vars_dict = {}
    for env_var in ci_env_vars:
        if env_var in os.environ:
            env_vars_dict[env_var] = os.environ[env_var]
    return env_vars_dict


def redact_token(value: Optional[str]) -> Optional[str]:
    if not value:
        return value
    if len(value) > 6:
        return f"***{value[-6:]}"
    return "***"


def get_sl_env_vars() -> dict[str, str]:
    return {
        name: value
        for name, value in os.environ.items()
        if name.startswith(tuple(PREFIXES))
    }


def get_agent_env_vars() -> dict[str, str]:
    merged = {**get_ci_env_vars(), **get_sl_env_vars()}
    return {
        name: redact_token(value)
        if name.upper().replace(".", "_") == "SL_TOKEN"
        else value
        for name, value in merged.items()
    }


def redact_argv(argv: list[str]) -> list[str]:
    redacted = list(argv)
    for i, arg in enumerate(redacted):
        lowered = arg.lower()
        if lowered == "--token" and i + 1 < len(redacted):
            redacted[i + 1] = redact_token(redacted[i + 1])
        elif lowered.startswith("--token="):
            prefix, value = arg[: len("--token=")], arg[len("--token=") :]
            redacted[i] = f"{prefix}{redact_token(value)}"
    return redacted
