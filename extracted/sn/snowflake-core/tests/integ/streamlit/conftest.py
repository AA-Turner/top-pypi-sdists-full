import os
import tempfile

from io import BytesIO
from pathlib import Path
from textwrap import dedent
from typing import Iterator

import pytest

from tests.integ.utils import random_string

from snowflake.core.stage import Stage, StageResource


@pytest.fixture(scope="module")
def streamlit_main_file():
    return "app.py"


@pytest.fixture(scope="module")
def streamlit_stage_with_file(session, stages, streamlit_main_file) -> Iterator[StageResource]:
    stage_name = random_string(8, "test_streamlit_stage_")
    stage = Stage(name=stage_name, kind="PERMANENT")

    st = stages.create(stage)
    try:
        file_path = f"@{st.name}/{streamlit_main_file}"

        session.file.put_stream(
            BytesIO(
                dedent(
                    """
                    import streamlit as st
                    st.write("Hello from streamlit test")
                    """
                ).encode()
            ),
            file_path,
            auto_compress=False,
        )

        yield st
    finally:
        st.drop()


@pytest.fixture(scope="module")
def git_repository():
    """Create a temporary Git repository with sample streamlit files.

    If TEST_GIT_REPO_URL environment variable is set, uses that repository.
    Otherwise, attempts to create a GitHub repository using GitHub CLI or API.
    If neither is available, returns a local repository (tests will be skipped).
    """
    import shutil
    import subprocess

    temp_dir = tempfile.mkdtemp(prefix="streamlit_test_git_")
    repo_path = Path(temp_dir)
    remote_repo_url = None
    repo_name = None
    github_org = None

    try:
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            yield {
                "path": str(repo_path),
                "commit_hash": None,
                "main_file": "app.py",
                "files": [],
                "remote_url": None,
                "repo_name": None,
                "github_org": None,
            }
            return

        subprocess.run(["git", "init"], cwd=repo_path, check=True)

        app_py = repo_path / "app.py"
        app_py.write_text(
            dedent("""
            import streamlit as st

            st.title("Test Streamlit App")
            st.write("Hello from Git repository!")

            # Add some interactivity
            name = st.text_input("Enter your name:")
            if name:
                st.write(f"Hello, {name}!")
        """)
        )

        utils_py = repo_path / "utils.py"
        utils_py.write_text(
            dedent("""
            def get_greeting(name):
                return f"Hello from utils, {name}!"
        """)
        )

        config_yaml = repo_path / "config.yaml"
        config_yaml.write_text(
            dedent("""
            app:
              title: "Test Streamlit App"
              description: "A test app from Git repository"
        """)
        )

        gitignore = repo_path / ".gitignore"
        gitignore.write_text("__pycache__/\n*.pyc\n.pytest_cache/\n")

        git_env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Test User",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test User",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        }

        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit with streamlit files"],
            cwd=repo_path,
            check=True,
            env=git_env,
        )

        readme = repo_path / "README.md"
        readme.write_text("# Test Streamlit Repository\n\nThis is a test repository for streamlit integration tests.")

        subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add README"],
            cwd=repo_path,
            check=True,
            env=git_env,
        )

        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_path, capture_output=True, text=True, check=True)
        commit_hash = result.stdout.strip()

        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)

        test_repo_url = os.getenv("TEST_GIT_REPO_URL")
        if test_repo_url:
            remote_repo_url = test_repo_url
            try:
                subprocess.run(["git", "remote", "add", "origin", remote_repo_url], cwd=repo_path, check=True)
                subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path, check=True, capture_output=True)
            except subprocess.CalledProcessError:
                pass
        else:
            try:
                github_org = os.getenv("GITHUB_ORG", "snowflakedb")
                repo_name = f"streamlit-test-{random_string(8, '')}"
                result = subprocess.run(
                    ["gh", "repo", "create", f"{github_org}/{repo_name}", "--public", "--source", ".", "--push"],
                    cwd=repo_path,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                remote_repo_url = f"https://github.com/{github_org}/{repo_name}.git"
            except (subprocess.CalledProcessError, FileNotFoundError):
                github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
                if github_token:
                    try:
                        import requests

                        github_org = os.getenv("GITHUB_ORG", "snowflakedb")
                        repo_name = f"streamlit-test-{random_string(8, '')}"
                        headers = {
                            "Authorization": f"token {github_token}",
                            "Accept": "application/vnd.github.v3+json",
                        }
                        data = {
                            "name": repo_name,
                            "description": "Temporary test repository for Streamlit integration tests",
                            "private": False,
                            "auto_init": False,
                        }
                        response = requests.post(
                            f"https://api.github.com/orgs/{github_org}/repos",
                            headers=headers,
                            json=data,
                            timeout=10,
                        )
                        response.raise_for_status()
                        remote_repo_url = response.json()["clone_url"]

                        subprocess.run(
                            ["git", "remote", "add", "origin", remote_repo_url],
                            cwd=repo_path,
                            check=True,
                        )
                        auth_url = remote_repo_url.replace("https://", f"https://{github_token}@")
                        subprocess.run(
                            ["git", "remote", "set-url", "origin", auth_url],
                            cwd=repo_path,
                            check=True,
                        )
                        subprocess.run(
                            ["git", "push", "-u", "origin", "main"],
                            cwd=repo_path,
                            check=True,
                            capture_output=True,
                        )
                    except Exception:
                        pass

        yield {
            "path": str(repo_path),
            "commit_hash": commit_hash,
            "main_file": "app.py",
            "files": ["app.py", "utils.py", "config.yaml", "README.md", ".gitignore"],
            "remote_url": remote_repo_url,
            "repo_name": repo_name,
            "github_org": github_org,
        }

    finally:
        if repo_name and github_org:
            github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
            if github_token:
                try:
                    import requests

                    headers = {
                        "Authorization": f"token {github_token}",
                        "Accept": "application/vnd.github.v3+json",
                    }
                    requests.delete(
                        f"https://api.github.com/repos/{github_org}/{repo_name}",
                        headers=headers,
                        timeout=10,
                    )
                except Exception:
                    pass
            else:
                try:
                    subprocess.run(
                        ["gh", "repo", "delete", f"{github_org}/{repo_name}", "--yes"],
                        check=True,
                        capture_output=True,
                    )
                except Exception:
                    pass

        shutil.rmtree(temp_dir, ignore_errors=True)
