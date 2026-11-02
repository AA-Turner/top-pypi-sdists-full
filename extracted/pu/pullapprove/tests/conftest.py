from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def isolated_git_env(monkeypatch):
    """Strip the host's git environment from every test.

    `git commit` exports GIT_INDEX_FILE (an absolute path to the in-progress
    commit's index) while running the pre-commit hook, which runs this suite.
    A test that runs git — even inside its own tmp_path repo — inherits that
    variable, so its `git add` writes the tmp repo's entries into the HOST
    repo's commit index. The referenced blobs only exist in the tmp repo's
    object store, so the commit later fails with "invalid object ... Error
    building trees". Dropping all GIT_* variables keeps test git activity
    (subprocesses and the CLI's own git calls) fully inside the test repo.

    Global/system git config is pointed at /dev/null for the same reason:
    the developer's ~/.gitconfig otherwise applies to test repos too (e.g.
    commit signing through 1Password, which fails whenever the agent is
    locked).
    """
    for var in list(os.environ):
        if var.startswith("GIT_"):
            monkeypatch.delenv(var)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)
