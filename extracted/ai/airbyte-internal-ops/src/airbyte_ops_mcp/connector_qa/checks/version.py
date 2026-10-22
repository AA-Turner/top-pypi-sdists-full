# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

import os
import subprocess
from pathlib import Path
from typing import Any

import requests  # type: ignore
import semver
import yaml  # type: ignore

from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    get_changed_files,
    get_file_at_merge_base,
    get_merge_base,
)
from airbyte_ops_mcp.connector_ops.utils import (
    Connector,  # type: ignore
)
from airbyte_ops_mcp.connector_qa import consts
from airbyte_ops_mcp.connector_qa.models import (
    Check,
    CheckCategory,
    CheckResult,
)

# Paths, relative to the connector directory, that hold no production code: tests,
# test configuration and documentation are not part of the released connector, so
# a change limited to them needs no version increment. Entries ending with "/"
# match a directory, the others match a single file. The connector matrix already
# ignores README.md, CONTRIBUTING.md, AGENTS.md, CLAUDE.md, .coveragerc and
# poe_tasks.toml; they are listed here for a PR that also touches tests.
# metadata.yaml, .dockerignore and build files are deliberately absent: changing
# them changes what is built or registered.
NON_PRODUCTION_PATHS = (
    "acceptance-test-config.yml",
    "README.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "CLAUDE.md",
    "bootstrap.md",
    ".coveragerc",
    "poe_tasks.toml",
    "unit_tests/",
    "integration_tests/",
    "erd/",
    "src/test/",
    "src/test-integration/",
    "src/test-performance/",
)


# Fields of `data` in metadata.yaml that change neither the image nor how the
# platform runs the connector, so a metadata.yaml change limited to them needs no
# version increment. They still reach the registry entry, but only on the next
# publish, and the platform's registry model reads none of them:
# - externalDocumentationUrls: reference links for people and agents.
# - connectorTestSuitesOptions: test suites and their secrets, read by CI from the
#   repository.
# - tags: only the `language:` and `cdk:` tags matter (see
#   RELEASED_TAG_PREFIXES); the others, such as `keyword:`, are labels.
# Everything else is compared, including ab_internal (read by the platform and
# by these checks), documentationUrl (the platform's docs link) and every field
# that selects the image, its resources or its rollout.
UNRELEASED_METADATA_FIELDS = (
    "externalDocumentationUrls",
    "connectorTestSuitesOptions",
    "tags",
)

# Tags that select the build and the registry's `language`, so changing them is
# a released change even though other tags are not.
RELEASED_TAG_PREFIXES = ("language:", "cdk:")


def _is_production_path(relative_path: str) -> bool:
    """Whether a path, relative to the connector directory, is production code."""
    return not any(
        relative_path.startswith(entry)
        if entry.endswith("/")
        else relative_path == entry
        for entry in NON_PRODUCTION_PATHS
    )


def _released_metadata(metadata: dict[str, Any]) -> tuple[dict[str, Any], Any]:
    """Split the released parts out of a parsed metadata.yaml.

    Returns:
        A copy of `metadata` without `UNRELEASED_METADATA_FIELDS` in `data`, and
        the released tags in their original order: the registry takes its
        `language` from the first `language:` tag, so reordering them counts.
    """
    data = metadata["data"]
    tags = data.get("tags") or []
    released_tags = (
        [
            tag
            for tag in tags
            if not isinstance(tag, str) or tag.startswith(RELEASED_TAG_PREFIXES)
        ]
        if isinstance(tags, list)
        else tags
    )
    released = {
        **metadata,
        "data": {
            key: value
            for key, value in data.items()
            if key not in UNRELEASED_METADATA_FIELDS
        },
    }
    return released, released_tags


class CheckVersionIncrement(Check):
    """Check that the connector version was incremented if files were modified."""

    category = CheckCategory.VERSION
    name = "Connector Version Increment Check"
    description = (
        "Validates that the connector version was incremented if files were modified. "
        "Changes that touch no production code, such as tests and documentation "
        "inside the connector directory, or metadata.yaml fields that are not part "
        "of the released connector (external documentation URLs, test suite "
        "options, tags other than language and CDK), do not require a version "
        "increment."
    )

    @staticmethod
    def _get_merge_base(connector: Connector) -> str | None:
        """Find where the current branch forked from the base branch.

        Uses the base branch (`GITHUB_BASE_REF`, else master) on the `upstream`
        remote when it exists and on `origin` otherwise.

        Returns:
            The merge base commit, or None when it cannot be determined (not a
            git checkout, base branch not fetched).
        """
        base_branch = os.getenv("GITHUB_BASE_REF") or "master"
        for remote in ("upstream", "origin"):
            try:
                return get_merge_base(
                    connector.code_directory, f"{remote}/{base_branch}"
                )
            except (subprocess.SubprocessError, OSError):
                continue
        return None

    @staticmethod
    def _get_changed_files(
        connector: Connector, merge_base: str | None
    ) -> list[str] | None:
        """List the connector's files changed since `merge_base`.

        Returns:
            Paths relative to the connector directory, or None when the changes
            cannot be determined (no merge base, git fails).
        """
        if merge_base is None:
            return None
        try:
            return get_changed_files(connector.code_directory, merge_base)
        except (subprocess.SubprocessError, OSError):
            return None

    @staticmethod
    def _get_unreleased_metadata_changes(
        connector: Connector, merge_base: str | None
    ) -> list[str] | None:
        """List the changed metadata.yaml fields if none of them is released.

        Compares metadata.yaml in the working tree with its version at
        `merge_base`.

        Returns:
            The changed fields of `data`, all from `UNRELEASED_METADATA_FIELDS`
            (empty if only formatting or comments changed). None if a released
            field changed, if there is no merge base, or if the file is new,
            deleted or cannot be read or parsed on either side.
        """
        if merge_base is None:
            return None
        try:
            base_text = get_file_at_merge_base(
                connector.code_directory, consts.METADATA_FILE_NAME, merge_base
            )
            if base_text is None:
                return None
            base = yaml.safe_load(base_text)
            head = yaml.safe_load(
                (Path(connector.code_directory) / consts.METADATA_FILE_NAME).read_text()
            )
        except (
            subprocess.SubprocessError,
            OSError,
            UnicodeDecodeError,
            yaml.YAMLError,
        ):
            return None
        if not all(
            isinstance(doc, dict) and isinstance(doc.get("data"), dict)
            for doc in (base, head)
        ):
            return None
        if _released_metadata(base) != _released_metadata(head):
            return None
        return [
            field
            for field in UNRELEASED_METADATA_FIELDS
            if base["data"].get(field) != head["data"].get(field)
        ]

    def _get_master_metadata(self, connector: Connector) -> dict[str, Any] | None:
        """Get the metadata from the master branch or None if unable to retrieve."""
        # TODO: test out if this works on the private airbyte-enterprise repo - consider using git-based approach
        github_url_prefix = "https://raw.githubusercontent.com/airbytehq/airbyte/master/airbyte-integrations/connectors"
        master_metadata_url = f"{github_url_prefix}/{connector.technical_name}/{consts.METADATA_FILE_NAME}"
        response = requests.get(master_metadata_url)

        # New connectors will not have a metadata file in master
        if not response.ok:
            return None
        return yaml.safe_load(response.text)["data"]

    def _parse_version_from_metadata(self, metadata: dict[str, Any]) -> semver.Version:
        return semver.Version.parse(str(metadata["dockerImageTag"]))

    def _get_master_connector_version(self, connector: Connector) -> semver.Version:
        """Get the version from the master branch."""
        master_metadata = self._get_master_metadata(connector)
        if not master_metadata:
            return semver.Version.parse("0.0.0")

        return self._parse_version_from_metadata(master_metadata)

    def _get_current_connector_version(self, connector: Connector) -> semver.Version:
        """Get the current version."""
        return self._parse_version_from_metadata(connector.metadata)

    def _are_both_versions_release_candidates(
        self, master_version: semver.Version, current_version: semver.Version
    ) -> bool:
        """Check if both versions are release candidates."""
        return bool(
            master_version.prerelease
            and current_version.prerelease
            and master_version.prerelease.startswith("rc.")
            and current_version.prerelease.startswith("rc.")
        )

    def _have_same_major_minor_patch(
        self, master_version: semver.Version, current_version: semver.Version
    ) -> bool:
        """Check if both versions have the same major, minor, and patch versions."""
        return (
            master_version.major == current_version.major
            and master_version.minor == current_version.minor
            and master_version.patch == current_version.patch
        )

    @staticmethod
    def _get_registry_override_tag(
        metadata: dict[str, Any] | None, channel: str
    ) -> str | None:
        """Extract the dockerImageTag from registryOverrides for a given channel.

        Args:
            metadata: The metadata dictionary (master or current).
            channel: The channel to extract from ("cloud" or "oss").

        Returns:
            The dockerImageTag value if present, None otherwise.
        """
        if metadata is None:
            return None
        try:
            return (
                metadata.get("registryOverrides", {})
                .get(channel, {})
                .get("dockerImageTag")
            )
        except (TypeError, AttributeError):
            return None

    def _has_registry_override_docker_tag_change(
        self,
        master_metadata: dict[str, Any] | None,
        current_metadata: dict[str, Any] | None,
    ) -> bool:
        """Check if registryOverrides.cloud.dockerImageTag or registryOverrides.oss.dockerImageTag has changed.

        Args:
            master_metadata: The metadata from the master branch.
            current_metadata: The current metadata.

        Returns:
            bool: True if either cloud or oss dockerImageTag has been added, removed, or changed.
        """
        master_cloud = self._get_registry_override_tag(master_metadata, "cloud")
        current_cloud = self._get_registry_override_tag(current_metadata, "cloud")

        master_oss = self._get_registry_override_tag(master_metadata, "oss")
        current_oss = self._get_registry_override_tag(current_metadata, "oss")

        return (master_cloud != current_cloud) or (master_oss != current_oss)

    def _run(self, connector: Connector) -> CheckResult:
        """Run the version increment check."""
        if (
            connector.metadata
            and connector.metadata.get("ab_internal", {}).get(
                "requireVersionIncrementsInPullRequests"
            )
            is False
        ):
            return self.skip(
                connector, "Connector opts out of version increment checks."
            )

        # Both the file list and the metadata.yaml comparison use this merge base.
        merge_base = self._get_merge_base(connector)
        changed_files = self._get_changed_files(connector, merge_base) or []
        production_paths = [path for path in changed_files if _is_production_path(path)]
        # An unknown or empty diff counts as a production change, so the check runs.
        if changed_files and not production_paths:
            return self.skip(
                connector,
                f"No production code changed (only {', '.join(changed_files)}), "
                "so no version increment is required.",
            )
        if production_paths == [consts.METADATA_FILE_NAME]:
            metadata_changes = self._get_unreleased_metadata_changes(
                connector, merge_base
            )
            if metadata_changes is not None:
                detail = (
                    f"{consts.METADATA_FILE_NAME} changes only "
                    f"{', '.join(metadata_changes)}, which are not released"
                    if metadata_changes
                    else f"{consts.METADATA_FILE_NAME} changes no field"
                )
                return self.skip(
                    connector,
                    f"No production code changed (only {', '.join(changed_files)}; "
                    f"{detail}), so no version increment is required.",
                )

        try:
            master_metadata = self._get_master_metadata(connector)
            # Note: master_metadata being None is expected for new connectors that don't exist
            # in master yet. In this case, we use 0.0.0 as the baseline, allowing any version.
            master_version = (
                self._parse_version_from_metadata(master_metadata)
                if master_metadata
                else semver.Version.parse("0.0.0")
            )
            current_version = self._get_current_connector_version(connector)

            # Require a version increment
            if current_version < master_version:
                return self.fail(
                    connector,
                    f"The dockerImageTag in {consts.METADATA_FILE_NAME} appears to be lower than the "
                    f"version on the default branch. Master version is {master_version}, current "
                    f"version is {current_version}. "
                    f"Update your PR branch from the default branch to get the latest connector version. "
                    f"Maintainers can use the `/bump-version` PR slash command. "
                    f"AI agents can use the `bump_version_in_repo` tool from the `airbyte-ops-mcp` MCP server.",
                )

            if current_version == master_version:
                # Allow version to stay the same if registryOverrides.cloud.dockerImageTag or
                # registryOverrides.oss.dockerImageTag has been added, removed, or changed
                if self._has_registry_override_docker_tag_change(
                    master_metadata, connector.metadata
                ):
                    return self.skip(
                        connector,
                        f"The current change is modifying the registryOverrides pinned version on Cloud or OSS. "
                        f"Skipping this check because the defined version {current_version} is allowed to be unchanged.",
                    )
                return self.fail(
                    connector,
                    f"The dockerImageTag in {consts.METADATA_FILE_NAME} was not incremented. "
                    f"Master version is {master_version}, current version is {current_version}. "
                    f"Ignore this message if you do not intend to re-release the connector. "
                    f"Maintainers can use the `/bump-version` PR slash command. "
                    f"AI agents can use the `bump_version_in_repo` tool from the `airbyte-ops-mcp` MCP server.",
                )

            if self._are_both_versions_release_candidates(
                master_version, current_version
            ) and not self._have_same_major_minor_patch(
                master_version, current_version
            ):
                return self.fail(
                    connector,
                    f"Master and current version are release candidates but they have different major, minor or patch versions. "
                    f"Release candidates should only differ in the prerelease part. Master version is {master_version}, "
                    f"current version is {current_version}",
                )

            # If master is an RC and the current version is not an RC, the only
            # valid stable version is the promotion of that RC (same major.minor.patch).
            if (
                master_version.prerelease
                and master_version.prerelease.startswith("rc.")
                and not current_version.prerelease
            ):
                expected_stable = semver.Version(
                    major=master_version.major,
                    minor=master_version.minor,
                    patch=master_version.patch,
                )
                if current_version != expected_stable:
                    return self.fail(
                        connector,
                        f"Master version {master_version} is a release candidate. "
                        f"The next stable version must be {expected_stable}, not {current_version}. "
                        f"Promote the RC to stable before bumping to a new major, minor, or patch version.",
                    )

            return self.pass_(
                connector,
                f"Version was properly incremented from {master_version} to {current_version}.",
            )
        except (requests.HTTPError, ValueError, TypeError) as e:
            return self.fail(connector, str(e))


ENABLED_CHECKS = [CheckVersionIncrement()]
