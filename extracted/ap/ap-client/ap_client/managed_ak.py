"""Client-side validation and acknowledgement of managed AK references."""

import re
import unicodedata
from typing import Any


def validate_ak_id(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not 1 <= len(value) <= 128 or value != value.strip():
        raise ValueError(
            "ak_id must be a nonempty string of at most 128 characters without surrounding whitespace"
        )
    return value


def validate_ak_selection(ak_id: Any, params: Any, params_list: Any, overrides: Any) -> None:
    validate_ak_id(ak_id)
    candidates = [params, overrides]
    if isinstance(params_list, list):
        candidates.extend(params_list)
    for value in candidates:
        if (
            isinstance(value, dict)
            and {"ak_id", "ak_selection_source", "user_ak_id", "key_id"} & value.keys()
        ):
            raise ValueError(
                "AK selection belongs at the request top level; ak_selection_source is server-generated"
            )


def parameter_ak_usage(value: Any) -> tuple[set[str], set[tuple[str, str]]]:
    """Collect references for receipt checks; the server validates their syntax."""
    if isinstance(value, dict):
        usages = [parameter_ak_usage(v) for v in value.values()]
        return set().union(*(ids for ids, _ in usages)), set().union(
            *(selected for _, selected in usages)
        )
    if isinstance(value, list):
        usages = [parameter_ak_usage(v) for v in value]
        return set().union(*(ids for ids, _ in usages)), set().union(
            *(selected for _, selected in usages)
        )
    if isinstance(value, str) and "$akpool" in value:
        # Normalize only for receipt recognition; the request keeps the original value.
        value = re.sub(r"^\$akpool:[ \t]+", "$akpool:", value)
        match = re.fullmatch(r"\$akpool:([A-Za-z0-9][A-Za-z0-9_.-]{0,127})", value)
        if match:
            return {match[1]}, set()
        if value in ("$akpool", "$akpool:@queue", "$akpool:@me"):
            return set(), {("personal_default" if value == "$akpool:@me" else "queue_default", "")}
        match = re.fullmatch(r"\$akpool:#([^@]+)(?:@(queue|me))?", value)
        if match:
            tag = match[1]
            if (
                len(tag.encode()) <= 64
                and tag.strip() == tag
                and not any(
                    c in ",@#.$" or c.isspace() or unicodedata.category(c) == "Cc" for c in tag
                )
            ):
                return set(), {
                    (
                        "personal_default" if match[2] == "me" else "queue_default",
                        "" if match[2] == "me" and tag == "default" else tag,
                    )
                }
        # Keep the capability check for future syntax without echoing arbitrary values.
        return {"$akpool"}, set()
    return set(), set()


def _confirmed_selectors(value: Any) -> set[tuple[str, str]]:
    """Match source and exact, case-sensitive tag on actual parameter bindings."""
    if not isinstance(value, list):
        return set()
    return {
        (binding["selection_source"], binding.get("selection_tag") or "")
        for binding in value
        if isinstance(binding, dict)
        and binding.get("parameterized") is True
        and isinstance(binding.get("ak_id"), str)
        and 1 <= len(binding["ak_id"]) <= 128
        and binding["ak_id"].strip() == binding["ak_id"]
        and binding.get("selection_source") in ("queue_default", "personal_default")
        and (binding.get("selection_tag") is None or isinstance(binding["selection_tag"], str))
    }


def _version_one(value: Any) -> bool:
    return type(value) in (int, float) and value == 1


def _personal_default_alias(selectors: set[tuple[str, str]]) -> set[tuple[str, str]]:
    """Accept the pre-alias spelling of the personal default on reused Jobs.

    ``$akpool:#default@me`` is now the untagged personal default, but Jobs frozen by an
    older version stored ``selection_tag="default"``. An idempotent resubmission returns
    that frozen binding verbatim, so the alias must acknowledge the legacy tag as well.
    """
    expanded = set(selectors)
    for source, tag in selectors:
        if source == "personal_default" and tag in {"", "default"}:
            expanded.add((source, "default" if tag == "" else ""))
    return expanded


def require_parameter_ak_ack(
    response: Any, ak_ids: set[str], selectors: set[tuple[str, str]] | None = None
) -> None:
    if (ak_ids or selectors) and (
        not isinstance(response, dict) or not _version_one(response.get("ak_placeholder_version"))
    ):
        raise ManagedAKProtocolError(
            ",".join(sorted(ak_ids)) if ak_ids else "$akpool selector", response
        )
    if selectors:
        if not _version_one(response.get("ak_selection_version")):
            raise ManagedAKProtocolError("$akpool selector", response)
        reused_bindings: set[tuple[str, str]] = set()
        if response.get("dry_run") is True:
            preview = response.get("preview_job")
            if not response_ak_ids(preview):
                raise ManagedAKProtocolError("$akpool selector", response)
            confirmed = _confirmed_selectors(
                preview.get("ak_bindings") if isinstance(preview, dict) else None
            )
        else:
            jobs = response.get("jobs")
            if not isinstance(jobs, list):
                raise ManagedAKProtocolError("$akpool selector", response)
            job_list = [job for job in jobs if isinstance(job, dict)] if jobs else []
            aggregate = _confirmed_selectors(response.get("ak_bindings"))
            confirmed = (
                set().union(*(_confirmed_selectors(job.get("ak_bindings")) for job in job_list))
                if job_list
                else aggregate
            )
            # Only a reused Job may answer with the legacy tag: a fresh submission must
            # bind the alias as the untagged personal default. Large Profile receipts omit
            # per-Job details and sample the persisted bindings at the top level, so those
            # aggregated bindings are frozen evidence too: a fresh alias binding is always
            # untagged, which leaves "default" only on Jobs frozen before the alias existed.
            reused_bindings = (
                set().union(
                    *(
                        _confirmed_selectors(job.get("ak_bindings"))
                        for job in job_list
                        if job.get("reused") is True
                    )
                )
                if job_list
                else aggregate
            )
        accepted = confirmed | _personal_default_alias(reused_bindings)
        if not selectors <= accepted:
            raise ManagedAKProtocolError("$akpool selector", response)


def _safe_identifier(value: Any) -> str | None:
    """Echo an identifier only when it is safe, matching the TypeScript client's boundary."""
    if not isinstance(value, str) or not value:
        return None
    if re.search(r"[\s\ufeff]", value) or any(unicodedata.category(c) == "Cc" for c in value):
        return None
    return value


class ManagedAKProtocolError(RuntimeError):
    """An unconfirmed AK reference, with only safe receipt identities retained."""

    def __init__(self, ak_id: str, response: Any):
        self.ak_id = ak_id
        self.response: dict[str, Any] = {}
        self.job_ids: list[str] = []
        self.group_id = None
        if isinstance(response, dict):
            self.group_id = _safe_identifier(response.get("group_id"))
            if self.group_id:
                self.response["group_id"] = self.group_id
            job_id = _safe_identifier(response.get("job_id"))
            if job_id:
                self.response["job_id"] = job_id
                self.job_ids.append(job_id)
            jobs = response.get("jobs")
            if isinstance(jobs, list):
                job_ids = [
                    value
                    for job in jobs
                    if isinstance(job, dict)
                    if (value := _safe_identifier(job.get("job_id")))
                ]
                self.job_ids.extend(job_ids)
                self.response["jobs"] = [{"job_id": value} for value in job_ids]
        super().__init__(
            f"Managed AK protocol mismatch: server did not acknowledge ak_id={ak_id}. "
            f"Returned Job IDs: {self.job_ids}. Verify these jobs before resubmitting; "
            "the target AP server may need an upgrade."
            + (f" Returned Group ID: {self.group_id}." if self.group_id else "")
        )


def response_ak_ids(response: Any) -> list[str]:
    if not isinstance(response, dict):
        return []
    value = response.get("ak_ids", [])
    return value if isinstance(value, list) and all(isinstance(v, str) for v in value) else []


def require_managed_ak_ack(response: Any, ak_id: str | None) -> None:
    if ak_id is None:
        return
    if ak_id not in response_ak_ids(response):
        raise ManagedAKProtocolError(ak_id, response)
    jobs = response.get("jobs", [])
    if not isinstance(jobs, list) or any(ak_id not in response_ak_ids(job) for job in jobs):
        raise ManagedAKProtocolError(ak_id, response)
