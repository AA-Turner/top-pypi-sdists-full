import inspect

from bir_mcp.atlassian import Jira
from bir_mcp.git_lab.sonarqube import SonarQube
from bir_mcp.git_lab.tools import GitLabTools
from bir_mcp.utils import wrap_with_xml_tag


def get_prompts() -> list[callable]:
    prompts = [
        get_merge_request_review_prompt,
        get_feature_development_prompt,
    ]
    return prompts


def get_merge_request_review_prompt(merge_request_url: str | None = None) -> str:
    """A prompt for reviewing a GitLab merge request."""
    merge_request = f'The merge request url is "{merge_request_url}".' if merge_request_url else ""
    prompt = inspect.cleandoc(f"""
        Your job is to conduct a thorough review of a GitLab merge request.

        Follow these steps:
        - Fetch the merge request overview using the {GitLabTools.get_merge_request_overview_from_url.__name__} tool.
        - Review the pipeline jobs, their statuses and traces, explain the meaning and value of the jobs, consider whether 
        they sufficiently verified the code quality and security.
        - Inspect the SonarQube data for the GitLab project's source and target branches using the 
        {SonarQube.get_project_quality_gates_status.__name__} and {SonarQube.get_main_project_metrics.__name__} tools.
        Pay attention to the analysis age, if it is older than 1 month, consider it stale. 
        - Inspect the first lines of the diffs in the merge request overview. Explain the purpose of the changes. 
        Evaluate the quality of the code, check for any potential bugs and security issues. If the first lines are
        not enough, use the {GitLabTools.get_merge_request_file_diffs.__name__} tool for full diffs and the 
        {GitLabTools.get_file_content.__name__} tool for the full file content in the source and target branches.
        Do not call the {GitLabTools.get_merge_request_file_diffs.__name__} tool with individual files, but rather
        collect all file paths that you need in a single call.
        - If the merge request overview returned any related Jira issues, use the {Jira.get_issue_overview.__name__}
        tool to fetch the issues. Ensure that the merge changes are related to the issues, that the issues have
        appropriate status and priority, that the issues include mentions of testing and have the necessary approvals.
        - Prepare the review summary, with purpose and explanation of the changes, findings from previous steps, 
        and the verdict, whether the changes are ready to be merged, if not, provide reasons and suggest next actions.
        - Ask the user if he wants to post the review summary as a comment on the merge request, if yes, use the 
        {GitLabTools.comment_on_merge_request.__name__} tool.
        
        {merge_request}
    """)
    # - If available, use the build HTML page tool to present the merge request review results, if not, use Markdown formatting.
    return prompt


def get_feature_development_prompt(
    jira_project_key: str,
    feature_description: str,
) -> str:
    """A prompt for feature development workflow setup."""
    feature_description = wrap_with_xml_tag("feature_description", feature_description)
    prompt = inspect.cleandoc(f"""
        Help a user setup a new feature branch by following these steps:

        ### Create a Jira issue for the feature in the project {jira_project_key}
        - Use the provided feature description: {feature_description} to prepare a summary and description for a new Jira issue, 
        ask for additional details if needed. 
        - Use tool to fetch allowed issue types in the project. Based on description and allowed types, suggest the most 
        appropriate types for the issue.
        - Try using local context to determine the user's name in Jira by inspecting local Git repo metadata via tools,
        if available, look at user emails in the Git config. If unsuccessful, ask for the user's Jira username directly. 
        Use the emails or provided username to search for the user in Jira to find or validate the username.
        - Provide the user with arguments to the Jira issue creation tool, after approval create a new Jira issue and
        provide the user with the created issue key and URL.
        
        ### Create a new feature branch in GitLab
        - Try inferring the GitLab project from local Git context by inspecting the remote urls from the get repo metadata tool,
        if unsuccessful, ask for the GitLab project path or url directly.
        - Build the feature branch name using the created Jira issue key: "feature/{{jira_issue_key}}-{{issue_summary}}".
        - The source branch in most cases should be "testing", but check that it exists in the project using the get project info tool.
        - Provide the user with arguments to the branch creation tool, after approval create the branch.

        ### Create a merge request in GitLab
        - Use the GitLab project path, source and target branch from the previous steps.
        - Use the created Jira issue description to create merge request title and description, the title should start with the 
        issue key.
        - Use the Jira username to find the user id in GitLab via the search users tool.
        - The merge request description should start with line "Closes {{jira_issue_key}}".
        - Provide the user with arguments to the merge request creation tool, after approval create the merge request and 
        provide the user with the created merge request url.
        - Use the {GitLabTools.search_merge_requests.__name__} tool to check whether an open merge request from testing to master
        branch exists, if not, suggest to create one.

        ### Add backward compatibility tests in GitLab
        - Ask user if he wants to add backward compatibility or other tests to the feature branch, either in GitLab or in local 
        development environment (only if local tools for editing files are available). If user doesn't agree or prefers local 
        development environment, skip this step.
        - Use tools to inspect code in the newly created GitLab feature branch.
        - Use create GitLab file tool to add tests to the feature branch.

        ### Pull the feature branch
        - If there are not local Git tools available, skip pulling the branch.
        - Inspect the local Git repo metadata and see if there is a remote that points to the GitLab project in which the 
        feature branch was created. If not, skip pulling the branch.
        - Suggest to user to pull the newly created feature branch, if approved, use the pull branch tool with the 
        feature branch name from the previous step.

        ### Add tests and initial changes locally
        - If local file editing tools are not available or user doesn't want to add tests and initial changes, skip this step.
        - Inspect local codebase. Based on feature description, determine which parts of the code are likely to change.
        - Based on the codebase and likely changes, add backward compatibilty tests to ensure that the feature doesn't break 
        existing functionality.
        - Based on the codebase and likely changes, add initial development changes.
    """)
    return prompt
