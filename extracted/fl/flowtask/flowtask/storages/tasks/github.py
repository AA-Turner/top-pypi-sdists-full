import os
from pathlib import PurePath
import tempfile
from navconfig.logging import logging
from ...exceptions import FlowTaskError, ConfigError
from .filesystem import FileTaskStorage


def _get_git():
    """Lazy-load GitPython to avoid importing it at module level."""
    try:
        import git  # noqa: E401
    except ImportError as exc:
        raise ImportError(
            "GitTaskStorage requires the optional 'git' extra. "
            "Install it with: pip install 'flowtask[git]'"
        ) from exc
    logging.getLogger("git").setLevel(logging.WARNING)
    return git.Repo, git.GitCommandError


class GitTaskStorage(FileTaskStorage):
    """Getting Tasks on Filesystem with Github Support."""
    _name_: str = "Git"
    use_ssh: bool = True

    def __init__(
        self,
        path: PurePath,
        git_url: str,
        *args,
        git_user: str = None,
        password: str = None,
        git_private_key: str = None,
        **kwargs,
    ):
        super(GitTaskStorage, self).__init__(path, *args, **kwargs)

        if git_url:
            self.git_url = git_url
            if git_url.startswith("http"):
                # using HTTP instead SSH for cloning
                self.use_ssh: bool = False
            self.git_private_key = git_private_key
            self.git_user = git_user
            self.git_password = password
            if not password:
                self.git_password = git_private_key
            self.refresh_repository()

    def clone_repository(self):
        Repo, _ = _get_git()
        url = self.git_url
        try:
            if self.use_ssh is False:
                self.git_url = self.git_url.replace(
                    "https://", f"https://{self.git_user}:{self.git_password}@"
                )
                Repo.clone_from(self.git_url, self.path)
            else:
                if self.git_private_key:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_key:
                        tmp_key.write(self.git_private_key.encode())
                        tmp_key.flush()  # Ensure the key is written to disk
                        env = {"GIT_SSH_COMMAND": f"ssh -i {tmp_key.name}"}
                        try:
                            Repo.clone_from(self.git_url, self.path, env=env)
                        finally:
                            os.unlink(tmp_key.name)
                else:
                    Repo.clone_from(self.git_url, self.path)
        except Exception as exc:
            raise ConfigError(
                f"Github Storage: Unable to Clone Repository: {exc}"
            ) from exc
        self.logger.info(f":: Cloned repository: {url}")

    def refresh_repository(self):
        Repo, GitCommandError = _get_git()
        try:
            if not self.path.exists() or not any(self.path.iterdir()):
                # If the directory is empty or doesn't exist, clone the repository
                self.clone_repository()
            else:
                # If the directory exists and is not empty, pull the latest changes
                try:
                    repo = Repo(self.path)
                except Exception as exc:
                    raise ConfigError(
                        f"Github Storage: Unable to sync with Repository: {exc}"
                    ) from exc
                env = {}
                if self.use_ssh is True:
                    env["GIT_SSH_COMMAND"] = f"ssh -i {self.git_private_key}"
                    with repo.git.custom_environment(**env):
                        repo.git.pull()
                else:
                    repo.git.fetch()
                    if len(repo.remote().refs) > 0:
                        upstream_branch = None
                        # Determine the correct upstream branch
                        for remote_ref in repo.remote().refs:
                            if (
                                remote_ref.remote_head == "master"
                                or remote_ref.remote_head == "main"
                            ):
                                upstream_branch = remote_ref.remote_head
                                break
                        else:
                            if upstream_branch:
                                # Set the correct upstream branch
                                repo.git.branch(
                                    "--set-upstream-to", f"origin/{upstream_branch}"
                                )
                            else:
                                self.logger.warning(
                                    "Unable to determine the correct upstream branch"
                                )
                        # Pull the latest changes
                        repo.git.pull()
                    else:
                        self.logger.warning(
                            f"Empty Upstream repository: {repo.remote()}"
                        )
                self.logger.info(
                    f"Pulled the latest changes from repository: {self.git_url}"
                )
        except GitCommandError as err:
            raise FlowTaskError(
                f"Error interacting with Git repository: {err}"
            ) from err
