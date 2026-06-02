#!/usr/bin/env python3
"""Provides access to a Gerrit instance with some convenience functionality

Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
"""

# ruff: noqa: D411 doc
# ruff: noqa: D417 doc

import asyncio
import base64
import getpass
import inspect
import json
import logging
import netrc
import os
import re
import sys
import tomllib
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections import defaultdict
from collections.abc import (
    AsyncIterable,
    Callable,
    Coroutine,
    Iterable,
    Mapping,
    MutableMapping,
    Sequence,
)
from contextlib import suppress
from datetime import date, datetime
from fnmatch import fnmatch
from functools import wraps
from pathlib import Path
from typing import Any, Literal, TypeVar, cast  # fixme(frans): remove cast
from urllib.parse import quote, urljoin, urlparse

# from aiohttp.http_exceptions import HttpBadRequest
import aiohttp
import secretstorage
from aiohttp import ClientResponse
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    Json,
    ValidationError,
    field_validator,
    model_validator,
)
from rich.status import Status

ReturnT = TypeVar("ReturnT")

DEFAULT_GERRIT_URL = "https://review.lan.tribe29.com"
DEFAULT_BRANCH = "master"
DEFAULT_PROJECT_NAME = "check_mk"
USE_GERRIT_FALLBACK = False


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.gerrit")


class GerritBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    # model_config = ConfigDict(extra="forbid")


class GerritAccountAvatar(GerritBase):
    url: str
    height: int


class GerritAccount(GerritBase):
    account_id: int = Field(..., alias="_account_id")
    name: str
    username: str
    status: None | str = None
    avatars: list[GerritAccountAvatar]
    email: None | str = None
    display_name: None | str = None


class GerritReviewer(GerritAccount):
    approvals: dict[str, str]  #': {'Code-Review': ' 0', 'Verified': ' 0'},
    tags: None | list[Literal["SERVICE_USER"]] = None
    status: None | str = None  # "Developer"


class GerritUser(GerritBase):
    account_id: int = Field(..., alias="_account_id")


class GerritAttentionSet(GerritBase):
    account: GerritUser
    last_update: datetime
    reason: str
    reason_account: None | GerritUser = None


class GerritSubmitRecordLabel(GerritBase):
    label: str
    status: str
    applied_by: None | GerritUser = None


class GerritSubmitRecord(GerritBase):
    rule_name: None | str = None
    status: Literal["NOT_READY", "OK", "CLOSED"]
    labels: None | list[GerritSubmitRecordLabel] = None
    requirements: None | list[Mapping[str, str]] = None


class GerritRevision(GerritBase):
    number: int = Field(..., alias="_number")
    ref: str
    description: None | str = None
    conflicts: None | Mapping[str, bool | str] = None
    kind: Literal["REWORK", "TRIVIAL_REBASE"]
    created: datetime
    uploader: GerritUser
    fetch: Mapping[str, Mapping[str, str]]
    branch: str


class GerritChange(GerritBase):
    number: int = Field(..., alias="_number")
    change_id: str
    owner: GerritUser
    subject: str
    project: str
    branch: str
    current_revision: str
    revisions: Mapping[str, GerritRevision]

    full_branch: str
    status: Literal["NEW", "MERGED", "ABANDONED"]
    created: datetime
    updated: datetime
    submitted: None | datetime = None
    id: str  # unique id := <project>~<number>
    virtual_id_number: int  # same as number
    triplet_id: str
    hashtags: list[str]
    submit_type: None | Literal["REBASE_IF_NECESSARY", "MERGE_IF_NECESSARY"] = None
    insertions: int
    deletions: int
    total_comment_count: int
    unresolved_comment_count: int
    has_review_started: bool
    meta_rev_id: str
    current_revision_number: int
    requirements: list[Mapping[str, str]]
    submit_records: list[GerritSubmitRecord]
    removed_from_attention_set: None | dict[str, GerritAttentionSet] = None
    attention_set: None | dict[str, GerritAttentionSet] = None
    work_in_progress: None | bool = None
    submission_id: None | str = None
    submitter: None | GerritUser = None
    topic: None | str = None
    more_changes: None | bool = Field(default=None, alias="_more_changes")
    revert_of: None | int = None
    cherry_pick_of_patch_set: None | int = None
    cherry_pick_of_change: None | int = None
    is_private: None | bool = None


class GerritCommitPerson(GerritBase):
    name: str
    email: str
    time: datetime

    @field_validator("time", mode="before")
    @classmethod
    def parse_time(cls, v: object) -> datetime:
        with suppress(ValueError):
            return datetime.strptime(str(v).rsplit(" ", 1)[0], "%a %b %d %H:%M:%S %Y")  # noqa: DTZ007
        return datetime.strptime(str(v), "%Y-%m-%dT%H:%M:%S")  # noqa: DTZ007


class GerritCommit(GerritBase):
    # model_config = ConfigDict(extra="forbid")
    commit: str
    message: str
    author: GerritCommitPerson
    committer: GerritCommitPerson
    affected_files: Sequence[str] = []
    tree: str
    tree_diff: Sequence[Mapping[str, int | str]]
    parents: list[str]


class Component(GerritBase):
    component_id: str
    display_name: None | str = None  # will be derived from component_id if not available
    previous_name: None | str = None
    type: Literal["Component", "System", "Process"]
    description: None | str = None
    has_support_component: bool = False
    members_required: int
    code_location: None | Sequence[str]
    external_code_location: None | Sequence[str]
    component_owner_email: str  # component owner as in Jira - is code owner, too
    code_owners_email: Sequence[str]

    @staticmethod
    def component_id_from(display_name: str) -> str:
        """Returns an FS safe, lowercase variant of a display name"""
        return (
            display_name.lower()
            .replace(" - ", "_")
            .replace("/", "_")
            .replace(",", "_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("&", "_and_")
            .replace("__", "_")
            .replace("__", "_")
        )

    @property
    def name(self) -> str:
        """Returns the display name if given, otherwise derives it from the component_id"""
        return self.display_name or self.display_name_from(self.component_id)

    @staticmethod
    def display_name_from(component_id: str) -> str:
        """To be used only if display name not explicitly given"""
        return component_id.replace("_", " ").title().replace(" And ", " and ")

    @staticmethod
    def sanatized_description(raw_description: str) -> str:
        return "\n".join(
            line
            for raw_line in raw_description.splitlines()
            if (line := raw_line.rstrip()).strip() != "-"
        ).strip()

    def dump_rich(self) -> str:
        description = self.description and self.description.splitlines()[0].strip(" -")
        rich_description = f" / [italic]{description}[/]" if description else ""
        return (
            rf"[bold cyan]{self.name}[/] [gray]\[{self.component_id}][/]"
            f"{rich_description}"
        )

    @model_validator(mode="before")
    @classmethod
    def fix_component_model(cls, obj: Json[dict[str, Any]]) -> Json[dict[str, Any]]:
        if "description" in obj:
            obj["description"] = cls.sanatized_description(obj["description"])
        if "checkmk_component" in obj:
            obj["display_name"] = obj["checkmk_component"]
            del obj["checkmk_component"]
        if "support_component" in obj:
            obj["has_support_component"] = bool(obj["support_component"])
            del obj["support_component"]
        if "number_required" in obj:
            obj["members_required"] = obj["number_required"]
            del obj["number_required"]
        return obj


class GerritClient:
    def __init__(self, url: str, username: str, password: str) -> None:
        """Initializes a GerritClient with given credentials"""
        self.url = url
        self._username = username
        self._auth = aiohttp.BasicAuth(self._username, password)
        self._session: None | aiohttp.ClientSession = None
        self._accounts: MutableMapping[int, GerritAccount] = {}
        self._cached_file_contents: MutableMapping[tuple[str, str, str], str] = {}

    async def __aenter__(self) -> "GerritClient":
        """Creates a Gerrit session context"""
        self._session = aiohttp.ClientSession(auth=self._auth)
        return self

    async def __aexit__(self, *args: object) -> None:
        """Closes a Gerrit session"""
        if self._session:
            await self._session.close()

    @property
    def username(self) -> str:
        return self._username

    async def commit_id(self, project: str, branch: str) -> str:
        """Returns branch tip commit id of provided @project and @branch"""
        return (
            await self.get(
                f"a/projects/{quote(project, safe='')}/branches/{quote(branch, safe='')}"
            )
        )["revision"]

    async def get_commit_details(self, project: str, commit_id: str) -> GerritCommit:
        return GerritCommit.model_validate(
            await self.get(
                f"a/plugins/gitiles/{quote(project, safe='')}/+/{commit_id}",
                params={"format": "JSON"},
            )
        )

    async def get_commit_text(self, project: str, commit_id: str) -> str:
        return await self.get(
            f"a/plugins/gitiles/{quote(project, safe='')}/+/{commit_id}",
            params={"format": "TEXT"},
        )

    async def get_log(
        self, file_path: str, since: datetime | date, project: str, branch: str
    ) -> Sequence[GerritCommit]:
        """Returns git log output for a path since a given date.

        Args:
            file_path: Path to the file in the repository
            since: Date from which to start the log
            project: Project name
            branch: Branch name

        Returns:
            Sequence of tuples containing (commit_id, date, author, message, list of files affected)

        """
        ref = branch if "refs/" in branch else f"refs/heads/{branch}"
        endpoint = f"a/plugins/gitiles/{quote(project, safe='')}/+log/{quote(ref, safe='')}"
        if file_path:
            endpoint += f"/{quote(file_path.lstrip('/'), safe='')}"

        results: list[GerritCommit] = []
        cursor: None | str = None
        since_dt = (
            datetime.combine(since, datetime.min.time()) if isinstance(since, date) else since
        )

        while True:
            log_response: dict[str, Any] = await self.get(
                endpoint, params={"format": "JSON", "s": cursor}
            )
            logs = [GerritCommit.model_validate(raw) for raw in log_response.get("log", [])]

            for commit in logs:
                commit_response: dict[str, Any] = await self.get(
                    f"a/projects/{quote(project, safe='')}/commits/{commit.commit}/files"
                )
                commit.affected_files = [p for p in commit_response if p != "/COMMIT_MSG"]

            done = False
            for commit in logs:
                if commit.committer.time < since_dt:
                    done = True
                    break
                results.append(commit)

            if done or not (cursor := log_response.get("next")):
                break

        return results

    async def repo_file_content(self, file_path: str, project: str, branch: str) -> str:
        """Get the content of a file from Gerrit.

        Args:
            file_path: Path to the file in the repository
            branch: Branch name

        Returns:
            File content as string
        """
        if (file_path, project, branch) not in self._cached_file_contents:
            endpoint = (
                f"a/projects/{quote(project, safe='')}"
                f"/branches/{quote(branch, safe='')}"
                f"/files/{quote(file_path.lstrip('/'), safe='')}/content"
            )
            try:
                raw_response = cast("str", await self.get(endpoint))
            except aiohttp.ClientResponseError as exc:
                if exc.status == 404:  # noqa: PLR2004 (magic value)
                    raise FileNotFoundError(
                        f"File not found in {project}@{branch}: {file_path}"
                    ) from exc
                raise
            response_bytes = base64.b64decode(raw_response)
            try:
                self._cached_file_contents[file_path, project, branch] = response_bytes.decode(
                    "utf-8"
                )
            except UnicodeDecodeError:
                self._cached_file_contents[file_path, project, branch] = response_bytes.decode(
                    "latin-1"
                )
        return self._cached_file_contents[file_path, project, branch]

    async def list_files(self, project: str, branch: str) -> Sequence[str]:
        """Returns list of files on given @project and @branch"""
        entries: list[dict[str, str]] = (
            await self.get(
                f"a/plugins/gitiles/{quote(project, safe='')}"
                f"/+/{quote(branch if 'refs/' in branch else f'refs/heads/{branch}', safe='')}/",
                params={"format": "JSON", "recursive": "1", "long": "1"},
            )
        ).get("entries", [])
        return [f"/{entry['name']}" for entry in entries if entry["type"] == "blob"]

    async def change_reviewers(self, change: GerritChange) -> Iterable[GerritReviewer]:
        raw_reviewers: Json[dict[str, Any]] = await self.get(f"a/changes/{change.number}/reviewers")
        return [GerritReviewer.model_validate(raw) for raw in raw_reviewers]

    async def get_change_sets(self, change_id: str) -> Sequence[GerritChange]:
        return [
            GerritChange.model_validate(raw)
            for raw in cast(
                "list[Mapping[str, str]]",
                await self.get(
                    "a/changes/",
                    params={"q": f"change:{change_id}", "o": "ALL_REVISIONS"},
                ),
            )
        ]

    async def fetch_changes(self, query: Mapping[str, str]) -> AsyncIterable[GerritChange]:
        start_index = 0
        while True:
            if not (
                changes := [
                    GerritChange.model_validate(raw)
                    for raw in cast(
                        "list[Mapping[str, str]]",
                        await self.get(
                            "a/changes/",
                            params={
                                "q": "+".join(f"{key}:{value}" for key, value in query.items()),
                                "start": f"{start_index}",
                            },
                        ),
                    )
                ]
            ):
                return
            for change in changes:
                yield change
                continue
            start_index += len(changes)

    async def current_account(self) -> GerritAccount:
        """Returns the account of the currently authenticated user"""
        return GerritAccount.model_validate(await self.get("a/accounts/self"))

    async def get_account(self, user_or_id: GerritUser | int) -> GerritAccount:
        account_id = user_or_id.account_id if isinstance(user_or_id, GerritUser) else user_or_id
        if account_id not in self._accounts:
            self._accounts[account_id] = GerritAccount.model_validate(
                await self.get(f"a/accounts/{account_id}")
            )
        return self._accounts[account_id]

    async def get[T](self, request: str, params: None | Mapping[str, None | str | int] = None) -> T:
        assert self._session
        # fixme(frans): check for Authentication required
        args_str = "&".join(
            f"{key}={value}" for key, value in (params or {}).items() if value is not None
        )
        url = f"{urljoin(self.url, request)}?{args_str}"
        log().debug("GET %s", f"{request}?{args_str}")  # shorter log message
        async with self._session.get(url, raise_for_status=True) as response:
            return await self._parse_response(response)

    async def post[T](self, request: str, params: None | Mapping[str, str] = None) -> T:
        assert self._session
        # fixme(frans): check for Authentication required
        url = f"{urljoin(self.url, request)}?{'&'.join(f'{key}={value}' for key, value in (params or {}).items())}"
        log().debug("POST %s", url)
        async with self._session.post(url, json={}, raise_for_status=True) as response:
            return await self._parse_response(response)

    async def _parse_response[T](self, response: ClientResponse) -> T:
        # fixme(frans): response.raise_for_status()
        if (raw_response := await response.text()).startswith(")]}'\n"):
            try:
                # first 5 bytes are a XSSI protection prefix we have to get rid of
                return cast("T", json.loads(raw_response[5:]))
            except json.decoder.JSONDecodeError:
                print(raw_response, file=sys.stderr)
                raise
        return cast("T", raw_response)


class CodeOwnersClient:
    """Provides information about code ownership and components based on Gerrit OWNERS files
    and component-info.toml files.
    While the implementation herein is based on custom inference rather than relying on the official
    Gerrit Code Owners REST API endpoints
    (see https://android-review.googlesource.com/plugins/code-owners/Documentation/rest-api.html)
    it still needs to return the same information as the plugin is being used in Gerrit for suggesting
    reviewers.
    """

    class Entry(GerritBase):
        """Reflects one entry in an OWNERS file, which can be either a directory or a per-file entry."""

        # note: currently we use `noparent` for validation only (we expect it to be set on all entries)
        #       but it's not taken into account when it comes to path -> component mapping
        noparent: bool = False
        components: set[str] = set()

    class OwnershipInfo(GerritBase):
        """Brings together what we need to persist for caching"""

        commit_id: str
        components: MutableMapping[str, Component] = {}
        all_components_loaded: bool = False  # set only if _all_ components loaded
        # this maps `OWNERS-directory` -> (`per-file pattern` -> [`Component``])
        entries: Mapping[str, Mapping[str, "CodeOwnersClient.Entry"]] = {}
        all_remote_files: None | Sequence[str] = None
        latest_commits: MutableMapping[str, Sequence[GerritCommit]] = {}

    def __init__(self, gerrit_client: GerritClient, project: str, branch: str) -> None:
        """Initialize the Gerrit Code Owners client.

        Args:
            gerrit_url: Base URL of the Gerrit instance (e.g., "http://localhost:8080")
            username: Username for authentication
            password: Password for authentication
        """
        self._gerrit_client = gerrit_client
        self._project = project
        self._branch = branch
        self._component_root_directory = "component_owners/"
        self._cached: CodeOwnersClient.OwnershipInfo = CodeOwnersClient.OwnershipInfo(commit_id="")
        self._cache_file_path = Path("~/.cache/cwz/cmk-components.json").expanduser()

    async def __aenter__(self) -> "CodeOwnersClient":
        """Does nothing - populating ownership data is explicitly triggered by initialize_data()
        to have better control over when we do it"""
        return self

    async def __aexit__(self, *args: object) -> None:
        """Persists the cached component/ownership data to file when exiting the context"""
        await self._persist_cached_state()

    async def initialize_data(self, *, cache_mode: str) -> None:
        if await self._load_cached_state(cache_mode):
            return
        # For now we assert we always need component details, so we load them all right away
        # Also, not all components might be referenced by OWNERS files, so pre-fetching independently from OWNERS files
        # is required anyway
        await self._ensure_all_components_loaded()

    async def commit_id(self) -> str:
        """Returns the remote commit ID ownership data is based on."""
        return self._cached.commit_id

    async def all_remote_files(self) -> Sequence[str]:
        if not self._cached.all_remote_files:
            self._cached.all_remote_files = await self._gerrit_client.list_files(
                self._project, self._branch
            )
        return self._cached.all_remote_files

    async def all_remote_paths(self) -> Sequence[str]:
        all_file_paths = await self.all_remote_files()
        return sorted(
            {
                "/".join(split_path[:pi])
                for file_path in all_file_paths
                for split_path in (file_path.split("/"),)
                for pi in range(len(split_path), 0, -1)
            }
        )

    async def get_log(self, file_path: str, since: datetime | date) -> Sequence[GerritCommit]:
        if file_path not in self._cached.latest_commits:
            log().debug("fetching log for %s since %s", file_path, since)
            self._cached.latest_commits[file_path] = await self._gerrit_client.get_log(
                file_path, since, self._project, self._branch
            )
        return self._cached.latest_commits[file_path]

    async def all_code_owners_config_files(self) -> Sequence[str]:
        """Get list of code owners configuration files using the official endpoint.
        Args:
            branch: Branch name
        Returns:
            List of file paths that are code owners configuration files
        """
        if USE_GERRIT_FALLBACK:
            log().warning("fetch OWNERS files via gitiles API..")
            return [path for path in (await self.all_remote_files()) if path.endswith("OWNERS")]
        log().debug("fetch OWNERS files..")
        code_owners_config_files: Sequence[str] = await self._gerrit_client.get(
            f"a/projects/{quote(self._project, safe='')}"
            f"/branches/{quote(self._branch, safe='')}"
            f"/code_owners.config_files/"
        )
        return [path for path in code_owners_config_files if path.endswith("OWNERS")]

    async def all_components_info(
        self, *, with_code_locations: bool = False
    ) -> Mapping[str, Component]:
        """Get comprehensive component data using the code_owners.config_files endpoint.

        This method:
        1. Uses the official endpoint to get all config files
        2. Parses component names from self._component_root_directory paths
        3. Retrieves owner and member information for each component
        4. Extracts meta information from comments in OWNERS_DEFINITION files
        5. Returns a cohesive data structure

        Args:
            branch: Branch name

        Returns:
            Dictionary with component names as keys and component data as values.
            Each component data includes 'owners', 'members', 'definition_file', 'all_emails',
            and 'meta_info' keys. The 'meta_info' contains 'description' and 'raw_comments'
            parsed from the beginning comments of the OWNERS_DEFINITION file.
        """
        await self._ensure_all_components_loaded()
        if with_code_locations:
            await self._ensure_all_entries_loaded()
        return self._cached.components

    async def code_locations(self, component_name: str) -> None | Sequence[str]:
        """List all paths that belong to a specific component.
        Args:
            component_name: Name of the component
        Returns:
            List of directory paths that belong to the component
        """
        await self._ensure_all_entries_loaded()
        return (await self._component_details(component_name)).code_location

    async def component_for_path(self, file_path: str) -> str | None:
        """Get the component that owns a specific file path.

        This method finds the most specific OWNERS file that applies to the given path
        and extracts the component name from its content.

        Args:
            file_path: Path to the file (e.g., "core_component/core_file.py")
            branch: Branch name
        Returns:
            Component name if found, None if no component owns the path
        """
        await self._ensure_all_entries_loaded()
        return ", ".join(self._query(file_path)[1]) or None

    async def owners_for(self, file_path: str) -> Sequence[Mapping[str, Any]]:
        """Get owners for a specific file path with resolved email addresses.

        Args:
            file_path: Path to the file
            branch: Branch name

        Returns:
            Dictionary with code owners information including resolved email addresses
        """

        async def augmented_owner(owner: Mapping[str, Any]) -> Mapping[str, Any]:
            account = owner["account"]
            if "email" in account:
                return {**owner, "email": account["email"]}
            if "_account_id" in account:
                # Resolve account ID to email
                return {
                    **owner,
                    "email": (await self._gerrit_client.get_account(account["_account_id"])).email,
                    "account_id": account["_account_id"],
                }
            return owner

        # fixme(frans): create BaseModel
        raw_data: Mapping[str, Any] = await self._gerrit_client.get(
            f"a/projects/{quote(self._project, safe='')}"
            f"/branches/{quote(self._branch, safe='')}"
            f"/code_owners/{quote(file_path, safe='')}",
            params={"limit": 999},
        )
        log().debug("raw owners data: %s", repr(raw_data))

        return [await augmented_owner(owner) for owner in raw_data["code_owners"]]

    async def check(
        self,
        *,
        email: str,
        path: str,
        change: None | str = None,
        user: None | str = None,
    ) -> Sequence[Mapping[str, Any]]:
        return await self._gerrit_client.get(
            f"a/projects/{quote(self._project, safe='')}"
            f"/branches/{quote(self._branch, safe='')}"
            f"/code_owners.check/",
            params={"email": email, "path": path, "change": change, "user": user},
        )

    async def check_config(self) -> None:
        """Runs the code_owners.check_config endpoint and complains about all findings"""
        check_config_result = cast(
            "Mapping[str, Mapping[str, Sequence[Mapping[str, str]]]]",
            await self._gerrit_client.post(
                f"a/projects/{quote(self._project, safe='')}/code_owners.check_config"
            ),
        )
        fatal_errors = [
            f"{branch}:{file_path} - {issue.get('message', 'Unknown error')}"
            for branch, files in check_config_result.items()
            for file_path, issues in files.items()
            for issue in issues
            if issue.get("status") == "FATAL"
        ]
        if fatal_errors:
            for error in fatal_errors:
                log().warning(error)
            raise ValueError(
                "Fatal errors detected in Gerrit Code Owners configuration. "
                "Please resolve these issues before using the client."
            )

    async def project_config(self) -> Mapping[str, Any]:
        return await self._gerrit_client.get(
            f"a/projects/{quote(self._project, safe='')}/code_owners.project_config"
        )

    async def branch_config(self) -> Sequence[Mapping[str, Any]]:
        return await self._gerrit_client.get(
            f"a/projects/{quote(self._project, safe='')}"
            f"/branches/{quote(self._branch, safe='')}"
            f"/code_owners.branch_config"
        )

    async def config_for(self, path: str) -> Sequence[Mapping[str, Any]]:
        # https://android-review.googlesource.com/plugins/code-owners/Documentation/config.html#pluginCodeOwnersEnableExperimentalRestEndpoints
        return await self._gerrit_client.get(
            f"a/projects/{quote(self._project, safe='')}"
            f"/branches/{quote(self._branch, safe='')}"
            f"/code_owners.config/{quote(path, safe='')}"
        )

    async def _load_cached_state(self, mode: str) -> bool:
        self._cached = CodeOwnersClient.OwnershipInfo(
            commit_id=await self._gerrit_client.commit_id(self._project, self._branch)
        )

        if mode == "never":
            return False

        with suppress(FileNotFoundError, json.JSONDecodeError):
            log().info("load local ownership data cache..")
            with self._cache_file_path.open() as f:
                try:
                    cached = self.OwnershipInfo.model_validate(json.load(f))
                except ValidationError:
                    raise RuntimeError(f"{self._cache_file_path} seems to be invalid") from None

                if mode == "always" or cached.commit_id == self._cached.commit_id:
                    self._cached = cached
                    log().info(
                        f"{len(self._cached.components)} components loaded from cache file (commit={cached.commit_id[:6]})"
                    )
                    return True
                log().info(
                    "commit ID %s from cache does not match current commit id %s => reload",
                    cached.commit_id[:6],
                    self._cached.commit_id[:6],
                )
        return False

    async def _persist_cached_state(self) -> None:
        self._cache_file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._cache_file_path.open("w") as f:
            # fixme(frans): backup write
            # fixme(frans): capture signal
            f.write(self._cached.model_dump_json(indent=2))

    async def _component_details(self, identifier: str) -> Component:
        """Reads OWNERS_DEFINITION and component_info.toml"""
        component_id, definition_file = (
            (identifier.rsplit("/", maxsplit=2)[-2], identifier)
            if "/" in identifier
            else (identifier, f"{self._component_root_directory}/{identifier}/OWNERS_DEFINITION")
        )

        if component_id not in self._cached.components:
            definition_file_content = await self._gerrit_client.repo_file_content(
                definition_file, self._project, branch=self._branch
            )

            owners_emails = [
                line
                for raw in definition_file_content.splitlines()
                if (line := raw.split("#", 1)[0].strip())
            ]
            meta_info = tomllib.loads(
                await self._gerrit_client.repo_file_content(
                    f"{definition_file.rsplit('/', maxsplit=1)[0]}/component_info.toml",
                    self._project,
                    self._branch,
                )
            )
            self._cached.components[component_id] = Component(
                component_id=component_id,
                display_name=meta_info.get("display_name") or None,
                previous_name=meta_info.get("previous_name") or None,
                type=meta_info["type"],
                description=meta_info["description"],
                has_support_component=meta_info.get("has_support_component") or False,
                members_required=meta_info["members_required"],
                code_location=[],
                external_code_location=meta_info.get("external_code_location") or None,
                component_owner_email=owners_emails[0],
                code_owners_email=owners_emails[1:],
            )

        return self._cached.components[component_id]

    async def _ensure_all_components_loaded(self) -> None:
        # components can be partially loaded, so we skip
        if self._cached.all_components_loaded:
            return

        for definition_file in (
            path for path in (await self.all_remote_files()) if path.endswith("OWNERS_DEFINITION")
        ):
            log().debug((await self._component_details(definition_file)).dump_rich())
        self._cached.all_components_loaded = True

    async def _ensure_all_entries_loaded(self) -> Iterable[str]:
        # in case we have one entry we have them all..
        if self._cached.entries:
            return []

        owners_pattern = r"^(?:per-file (.*)=)?(?:(?:file:/(.*/OWNERS_DEFINITION))|(set noparent))$"
        issues = []
        entries: MutableMapping[str, MutableMapping[str, CodeOwnersClient.Entry]] = defaultdict(
            lambda: defaultdict(CodeOwnersClient.Entry)
        )
        for owners_file in sorted(await self.all_code_owners_config_files()):
            file_directory = owners_file.rsplit("/", maxsplit=1)[0]
            content = await self._gerrit_client.repo_file_content(
                owners_file.lstrip("/"), self._project, branch=self._branch
            )
            for line in (
                clean for raw in content.splitlines() if (clean := raw.split("#", 1)[0].strip())
            ):
                if not (match := re.match(owners_pattern, line)):
                    issues.append(f"Invalid line in {owners_file}: {line!r}")
                    continue

                per_file_path, definition_file, noparent = match.groups()
                if bool(definition_file) == bool(noparent):
                    issues.append(
                        f"{owners_file}: only one of `set noparent` or `file:` may be set ({line!r})"
                    )
                    continue
                if per_file_path and "/" in per_file_path:
                    issues.append(
                        f"{owners_file}: `per-file` entry in contains directory: {per_file_path}"
                    )
                    continue

                entry = entries[file_directory][per_file_path or ""]

                if definition_file:
                    try:
                        component = await self._component_details(definition_file)
                    except FileNotFoundError:
                        issues.append(f"{owners_file}: file not found: {line}")
                    entry.components.add(component.component_id)
                    component.code_location = [
                        *(component.code_location or []),
                        f"{file_directory}/{per_file_path or ''}".rstrip("/"),
                    ]
                if noparent:
                    entry.noparent = True
        self._cached.entries = entries
        return issues

    def _query(self, file_path: str) -> tuple[None | str, Sequence[str], Sequence[str]]:
        # start with full path and then go up directory by directory, checking for matching entries
        for i in range(len(split_path := f"/{file_path.strip('/')}".split("/")), 0, -1):
            if entries := self._cached.entries.get(composite_path := "/".join(split_path[:i])):
                # check all pattern, with "" being the whole directory as the last one
                for per_file_path, entry in sorted(entries.items(), reverse=True):
                    # note(frans): optimization potential: we only need to check fnmatch if i == len(split_path) - 1
                    if not per_file_path or fnmatch(split_path[-1], per_file_path):
                        return (
                            f"{composite_path}:{per_file_path}",
                            sorted(entry.components),
                            [
                                mail
                                for component_id in entry.components
                                for component in (self._cached.components[component_id],)
                                for mail in (
                                    component.component_owner_email,
                                    *(component.code_owners_email or []),
                                )
                            ],
                        )
        return None, [], []


def credentials_from_env(cli_args: Args) -> None | tuple[str, str]:
    """Returns credentials from environment if available"""
    if (_username_var := cli_args.gerrit_username_var) and (
        _password_var := cli_args.gerrit_api_token_var
    ):
        try:
            return os.environ[_username_var], os.environ[_password_var]
        except KeyError as exc:
            print(
                f"You provided credentials via environment variables, but one or both are missing: {exc}",
                file=sys.stderr,
            )
            raise SystemExit(1) from None
    return None


def credentials_from_netrc(hostname: str) -> None | tuple[str, str]:
    """Read credentials from ~/.netrc"""
    with suppress(FileNotFoundError):
        if credentials := netrc.netrc((Path.home() / ".netrc").as_posix()).authenticators(hostname):
            return str(credentials[0]), str(credentials[2])
    return None


def credentials_from_keyring(hostname: str) -> tuple[str, str] | None:
    """Returns credentials for @hostname from a running secret service (e.g. GNOME keyring).
    Returns None if secretstorage is not installed, the keyring is unavailable,
    or no matching entry exists for the given URL.
    """
    log().debug("try to retrieve credentials from keyring for %s", hostname)
    with secretstorage.dbus_init() as bus:
        collection = secretstorage.get_default_collection(bus)
        for item in collection.search_items({"server": hostname}):
            attrs = item.get_attributes()
            if (username := attrs.get("username") or attrs.get("user") or "") and (
                password := item.get_secret().decode()
            ):
                return str(username), password
    return None


def credentials_from_interactive(gerrit_url: str) -> tuple[str, str]:
    """Prompt the user interactively for credentials."""
    username = input("Gerrit username: ").strip()
    password = getpass.getpass(f"HTTP token (get at {gerrit_url}/settings/#HTTPCredentials): ")
    return username, password


def store_gerrit_credentials(hostname: str, username: str, password: str) -> None:
    """Stores provided @hostname using a running secret service (e.g. GNOME keyring)."""
    with secretstorage.dbus_init() as bus:
        collection = secretstorage.get_default_collection(bus)
        collection.create_item(
            label=f"Gerrit ({hostname})",
            attributes={"server": hostname, "username": username},
            secret=password.encode(),
            replace=True,
        )


def select_credentials(cli_args: Args) -> tuple[str, str, str]:
    """Get credentials for the given URL.

    Tries in order: GNOME keyring, then ~/.netrc.
    """
    hostname = urlparse(cli_args.gerrit_url).netloc
    store_credentials = cli_args.store_credentials
    if (creds := credentials_from_env(cli_args)) is not None:
        log().debug("using credentials from keyring for %s", hostname)
    elif (creds := credentials_from_netrc(hostname)) is not None:
        log().debug("using credentials from .netrc for %s", hostname)
    elif (creds := credentials_from_keyring(hostname)) is not None:
        log().debug("using credentials from keyring for %s", hostname)
        store_credentials = False
    else:
        for line in (
            "No credentials found to access the Gerrit instance.",
            "You may provide them either via environment variables (specified"
            " with both `--gerrit-username-var` and `--gerrit-api-token-var`),"
            " via a ~/.netrc file (or an entry therein) with the following content:",
            "```",
            f"machine {cli_args.gerrit_url.split('//', maxsplit=1)[-1]}",
            "login <YOUR.GERRIT-NAME>",
            f"# get your's at {cli_args.gerrit_url}/settings/#HTTPCredentials",
            "password <GERRIT-WEB-TOKEN>",
            "```",
            "or via keyring",
        ):
            print(line, file=sys.stderr)

        if not sys.stdout.isatty():
            raise SystemExit(1)

        print("\nEnter credentials interactively and optionally store them in the keyring:")
        creds = credentials_from_interactive(cli_args.gerrit_url)
        if not store_credentials:
            store_credentials = input("Store in keyring? [y/N] ").strip().lower() == "y"

    if store_credentials:
        store_gerrit_credentials(hostname, *creds)

    return cli_args.gerrit_url, *creds


def apply_common_gerrit_cli_args(parser: ArgumentParser) -> ArgumentParser:
    """Populates given @parser with arguments needed for a Gerrit connection"""
    parser.add_argument("--gerrit-url", type=str, default=DEFAULT_GERRIT_URL)
    parser.add_argument("--project-name", type=str, default=DEFAULT_PROJECT_NAME)
    parser.add_argument("--branch", type=str, default=DEFAULT_BRANCH)
    parser.add_argument("--gerrit-username-var", type=str)
    parser.add_argument("--gerrit-api-token-var", type=str)
    parser.add_argument("--store-credentials", type=str, help="Store credentials in local keyring")
    return parser


def apply_code_owner_cli_args(parser: ArgumentParser) -> ArgumentParser:
    """Populates given @parser with arguments needed for a Gerrit connection"""
    apply_common_gerrit_cli_args(parser)
    parser.add_argument(
        "--cache-mode", type=str, default="auto", choices=["auto", "always", "never"]
    )
    return parser


def with_gerrit_client(
    *, populate: bool = True
) -> Callable[
    [Callable[..., Coroutine[Any, Any, ReturnT]]],
    Callable[..., Coroutine[Any, Any, ReturnT]],
]:
    """Provides an entrypoint function with a GerritClient and a CodeOwnersClient instance"""

    def decorator(
        func: Callable[..., Coroutine[Any, Any, ReturnT]],
    ) -> Callable[..., Coroutine[Any, Any, ReturnT]]:
        func_params = set(inspect.signature(func).parameters)

        @wraps(func)
        async def _with_gerrit_client(cli_args: Args, status: Status, **kwargs: object) -> ReturnT:
            gerrit_url, username, password = select_credentials(cli_args)

            log().debug("authenticate on %s using username=%s", gerrit_url, username)
            status.start()
            status.update(f"authenticate at {gerrit_url}..")
            async with GerritClient(gerrit_url, username, password) as gerrit_client:
                async with CodeOwnersClient(
                    gerrit_client, cli_args.project_name, branch=cli_args.branch
                ) as owners_client:
                    if populate:
                        cache_mode_hint = (
                            "- use --cache-mode=always for faster repeated calls"
                            if cli_args.cache_mode == "auto"
                            else ""
                        )
                        status.update(
                            f"populate code-owners data (cache-mode is {cli_args.cache_mode!r}{cache_mode_hint}).."
                        )
                        await owners_client.initialize_data(cache_mode=cli_args.cache_mode)

                    available: dict[str, Any] = {
                        "cli_args": cli_args,
                        "status": status,
                        "gerrit_client": gerrit_client,
                        "owners_client": owners_client,
                        **kwargs,
                    }
                    log().debug("call %s", func.__name__)
                    status.stop()
                    return await func(**{k: v for k, v in available.items() if k in func_params})

        return _with_gerrit_client

    return decorator


async def demo_fetch_open_reviews() -> None:
    """Example: list all own open reviews"""
    query = {
        # "reviewer": "self",
        # "-owner": "self",
        "owner": "self",
        "status": "open",
        # "status": "closed",
    }

    # query for open reviews
    query = {"reviewer": "self", "-owner": "self", "status": "open"}
    # accounts = {}

    if (creds := credentials_from_netrc(urlparse(GERRIT_URL).netloc)) is None:
        return

    username, password = creds

    async with GerritClient(url=GERRIT_URL, username=username, password=password) as gerrit_client:
        async for change in gerrit_client.fetch_changes(query):
            owner = await gerrit_client.get_account(change.owner)
            reviewers = await gerrit_client.change_reviewers(change)
            print(
                f"[link ={GERRIT_URL}/c/{change.project}/+/{change.number}]{change.project}/{change.branch} {change.change_id[:10]}/{change.number}[/link]"
                f" - O: {owner.name}"
                f" - [bold red]{change.subject}[/]"
                f" - R: {', '.join(f'{r.name}' for r in reviewers)}"
            )
            # print(yaml.dump(change))


async def demo_show_code_owners_info() -> None:
    """Example: use some of the Gerrit API wrappers"""
    if (creds := credentials_from_netrc(urlparse(GERRIT_URL).netloc)) is None:
        return

    username, password = creds

    async with GerritClient(GERRIT_URL, username, password) as gerrit_client:
        owners_client = CodeOwnersClient(gerrit_client, DEFAULT_PROJECT_NAME, branch=DEFAULT_BRANCH)
        print(await owners_client.project_config())
        # await owners_client.check_config()
        # for owners_file in await owners_client.all_code_owners_config_files(DEFAULT_BRANCH):
        #    owners_file_content = await gerrit_client.repo_file_content(
        #        owners_file, DEFAULT_PROJECT_NAME, DEFAULT_BRANCH
        #    )
        #    print(owners_file, len(owners_file_content))

        # print(await owners_client.all_components_data(DEFAULT_BRANCH))
        # print(await owners_client.component_for_path("mixed_component/core_part", DEFAULT_BRANCH))
        # print(await owners_client.code_locations("core_component", DEFAULT_BRANCH))
        # print(await owners_client.owners_for("mixed_component/core_part", DEFAULT_BRANCH))
        # print(await owners_client.component_owners_and_members("core_component", DEFAULT_BRANCH))
        # print(await owners_client.branch_config(DEFAULT_BRANCH))
        # print(await owners_client.check(branch=DEFAULT_BRANCH, email="andreas.boesl@checkmk.de", path="mixed_component/core_part"))
        # print(await owners_client.config_for(path="mixed_component/core_part", branch=DEFAULT_BRANCH))


if __name__ == "__main__":
    GERRIT_URL, DEFAULT_PROJECT_NAME = "https://review.lan.tribe29.com", "check_mk"
    GERRIT_URL, DEFAULT_PROJECT_NAME = "http://localhost:8080", "test-project"

    DEFAULT_BRANCH = "master"

    asyncio.run(demo_show_code_owners_info())
    asyncio.run(demo_fetch_open_reviews())
