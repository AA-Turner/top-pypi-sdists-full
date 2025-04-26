from github import Github


def get_repo_and_contents(host, token, repo_name, branch, repo_location):
    """
        This method will get the GitHub contents object provided arguments.

        Arguments:
            host (str): GitHub URL
            token (str): GitHub API token
            repo_name (str): name of GitHub repository
            branch (str): name of GitHub branch
            source_code (str): source code
            repo_location (str): local path to source code location in repo

        Returns:
            github ContentFile object
    """
    # Initialize GitHub instance using GHE Token
    github_instance = Github(base_url=host, login_or_token=token)
    # Return repo and contents objects
    repo = github_instance.get_repo(repo_name)
    return repo, repo.get_contents(repo_location, ref=branch)


def update_source_code(repo, contents, branch, source_code):
    """
        This method will update source code in GitHub using local source code.

        Arguments:
            repo (github.Repository.Repository): GitHub repository instance
            contents (github.ContentFile.ContentFile): file contents
            branch (str): name of GitHub branch
            source_code (str): source code

        Returns:
            commit dict
    """
    # Update source code
    return repo.update_file(
        contents.path, "Automated code update.", source_code, contents.sha,
        branch=branch)
