"""Raw Agent Task scope and clock validation."""

import re
from collections.abc import Mapping
from urllib.parse import urlsplit

_PULL_URL_PATTERN = re.compile(r"/pull/([0-9]+)(?:/|[?#]|$)")


def _artifact_pr_number_matches(value: object, pr_number: int) -> bool:
    if isinstance(value, int) and not isinstance(value, bool):
        return value == pr_number
    return not isinstance(value, str) or not value.isascii() or not value.isdigit() or int(value) == pr_number


def _artifact_url_matches(
    value: object,
    pr_number: int,
    *,
    pull_artifact: bool,
    repository: str | None = None,
) -> bool:
    if not isinstance(value, str):
        return True
    match = _PULL_URL_PATTERN.search(value)
    if match:
        if pull_artifact and repository:
            try:
                parsed = urlsplit(value)
            except ValueError:
                parsed = None
            if parsed is not None:
                path = parsed.path.strip("/").split("/")
                if (
                    parsed.hostname in {"github.com", "www.github.com"}
                    and len(path) >= 4
                    and path[2] == "pull"
                    and f"{path[0]}/{path[1]}".casefold() != repository.casefold()
                ):
                    return False
        return int(match.group(1)) == pr_number
    return not pull_artifact or not value.isascii() or not value.isdigit() or int(value) == pr_number


def _artifact_scope_matches(artifact: object, pr_number: int, repository: str | None = None) -> bool:
    if not isinstance(artifact, Mapping):
        return True
    artifact_type = artifact.get("type")
    data = artifact.get("data")
    if artifact_type == "pull" and isinstance(data, Mapping):
        for key in ("number", "pull_request_number", "target_id"):
            if not _artifact_pr_number_matches(data.get(key), pr_number):
                return False
    return all(
        _artifact_url_matches(
            container.get(key),
            pr_number,
            pull_artifact=artifact_type == "pull",
            repository=repository,
        )
        for container in (data, artifact)
        if isinstance(container, Mapping)
        for key in ("url", "html_url", "target_id", "targetId")
    )


def raw_lifecycle_artifact_scope_matches(
    task: Mapping[str, object],
    pr_number: int,
    *,
    repository: str | None = None,
) -> bool:
    """Reject any valid pull-artifact PR number that contradicts the requested scope."""
    artifacts = task.get("artifacts")
    if not isinstance(artifacts, list):
        return True
    return all(_artifact_scope_matches(artifact, pr_number, repository) for artifact in artifacts)
