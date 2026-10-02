"""Namespace facade, generated from `x-sdk-path`. Do not edit.

Mirrors the TypeScript SDK surface: `@SdkRoute('synthesizers', 'create')` on the
backend handler yields `rl.synthesizers.create(...)` in both clients.
"""

from __future__ import annotations

from typing import Any

from .types import Response


class RecursionApiError(Exception):
    """A non-2xx response. Mirrors the TypeScript client's `throwOnError: true`."""

    def __init__(self, status_code: int, parsed: Any, content: bytes) -> None:
        self.status_code = status_code
        self.parsed = parsed
        self.content = content
        super().__init__(f"Recursion API returned {status_code}")


def _unwrap(response: Response[Any]) -> Any:
    if response.status_code >= 400:
        raise RecursionApiError(int(response.status_code), response.parsed, response.content)
    return response.parsed


class _AgentSkills:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_content(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import get_content as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def upload_bundle(self, *args: Any, **kwargs: Any) -> Any:
        from .api.agent_skills import upload_bundle as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _CheckFixCycles:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.check_fix_cycles import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.check_fix_cycles import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Computes:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import execute as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def mint_access_session(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import mint_access_session as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def revoke_access_sessions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import revoke_access_sessions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def start(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import start as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def stop(self, *args: Any, **kwargs: Any) -> Any:
        from .api.computes import stop as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _CostLimits:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.cost_limits import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_problem_status(self, *args: Any, **kwargs: Any) -> Any:
        from .api.cost_limits import get_problem_status as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.cost_limits import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def upsert(self, *args: Any, **kwargs: Any) -> Any:
        from .api.cost_limits import upsert as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _CustomerSecrets:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def attach(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import attach as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import detach as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_attachments(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import list_attachments as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.customer_secrets import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _EnvironmentFiles:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create_signed_upload_urls(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environment_files import create_signed_upload_urls as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environment_files import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def finalize_uploads(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environment_files import finalize_uploads as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environment_files import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Environments:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def attach_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import attach_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import detach_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def ensure_template(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import ensure_template as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_by_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import get_by_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_template(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import get_template as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_settings(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import update_settings as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def upsert(self, *args: Any, **kwargs: Any) -> Any:
        from .api.environments import upsert as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Evaluations:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def bulk_create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import bulk_create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import cancel as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel_export(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import cancel_export as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_export(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import create_export as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_grade_only(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import create_grade_only as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_export(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import get_export as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_results(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import get_results as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_exports(self, *args: Any, **kwargs: Any) -> Any:
        from .api.evaluations import list_exports as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Exports:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def cancel(self, *args: Any, **kwargs: Any) -> Any:
        from .api.exports import cancel as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.exports import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.exports import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.exports import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Files:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def attach(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import attach as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def batch_organization_file_metadata(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import batch_organization_file_metadata as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def bulk_attach(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import bulk_attach as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_signed_upload_urls(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import create_signed_upload_urls as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import detach as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def download(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import download as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def finalize_uploads(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import finalize_uploads as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import list_for_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_gold_standard(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import update_gold_standard as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_tags(self, *args: Any, **kwargs: Any) -> Any:
        from .api.files import update_tags as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _FormAnswers:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def list_for_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.form_answers import list_for_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def upsert_for_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.form_answers import upsert_for_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Forms:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def attach_to_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import attach_to_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def attach_to_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import attach_to_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import create_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import create_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import create_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import create_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import delete_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach_from_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import detach_from_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach_from_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import detach_from_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach_from_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import detach_from_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import get_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_problem_override(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import get_problem_override as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import list_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def publish_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import publish_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def resolve_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import resolve_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.forms import update_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _GitRepoClaims:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.git_repo_claims import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _GradingRuns:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.grading_runs import get_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_problem_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.grading_runs import list_for_problem_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Images:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.images import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.images import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Imports:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def cancel(self, *args: Any, **kwargs: Any) -> Any:
        from .api.imports import cancel as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def confirm_upload(self, *args: Any, **kwargs: Any) -> Any:
        from .api.imports import confirm_upload as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.imports import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_platform_limits(self, *args: Any, **kwargs: Any) -> Any:
        from .api.imports import get_platform_limits as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def initiate(self, *args: Any, **kwargs: Any) -> Any:
        from .api.imports import initiate as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.imports import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _IssueComments:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issue_comments import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issue_comments import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issue_comments import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issue_comments import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Issues:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_by_problem_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import create_by_problem_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_by_problem_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import list_by_problem_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import list_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.issues import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _JobsV2:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def cancel_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import cancel_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import cancel_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import delete_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_event_log_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_event_log_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_events_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_events_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_output_files_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_output_files_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_rollout_events_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_rollout_events_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_rollout_output_files_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import get_rollout_output_files_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_children_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import list_children_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_children_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import list_children_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import list_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def rerun_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.jobs_v2 import rerun_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _ManagedAgents:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def add_session_resources(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import add_session_resources as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def apply_agent_tag(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import apply_agent_tag as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def archive_memory_store(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import archive_memory_store as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel_environment_setup_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import cancel_environment_setup_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel_session(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import cancel_session as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_agent(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_agent as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_agent_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_agent_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_environment_setup_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_environment_setup_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_event_source(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_event_source as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_memory(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_memory as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_memory_store(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_memory_store as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_skill(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_skill as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_skill_group(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_skill_group as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_skill_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_skill_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_tag(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_tag as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_vault(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_vault as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_vault_credential(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_vault_credential as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_webhook_endpoint(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import create_webhook_endpoint as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def define_session_outcome(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import define_session_outcome as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_agent(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_agent as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_event_source(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_event_source as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_file(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_file as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_memory(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_memory as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_memory_store(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_memory_store as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_session(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_session as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_session_resource(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_session_resource as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_skill(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_skill as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_skill_group(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_skill_group as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_tag(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_tag as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_trigger_binding(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_trigger_binding as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_vault(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_vault as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_vault_credential(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_vault_credential as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_webhook_endpoint(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import delete_webhook_endpoint as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def estimate_session_hour_cost(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import estimate_session_hour_cost as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_agent(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_agent as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_agent_learning(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_agent_learning as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_agent_memory(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_agent_memory as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_agent_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_agent_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_analytics(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_analytics as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_automation_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_automation_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_automation_status(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_automation_status as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_environment_setup_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_environment_setup_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_environment_setup_run_log(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_environment_setup_run_log as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_evaluation_overview(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_evaluation_overview as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_event_source(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_event_source as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_event_source_status(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_event_source_status as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_file(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_file as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_integration_slack_channel_catalog(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_integration_slack_channel_catalog as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_memory(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_memory as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_memory_by_path(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_memory_by_path as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_memory_store(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_memory_store as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_memory_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_memory_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_pull_request_review_result(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_pull_request_review_result as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_reflection(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_reflection as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_sandbox_provider_status(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_sandbox_provider_status as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session_board(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session_board as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session_event_content(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session_event_content as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session_model_costs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session_model_costs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session_resource(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session_resource as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session_thread(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session_thread as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_session_tree(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_session_tree as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_skill(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_skill as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_skill_group(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_skill_group as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_skill_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_skill_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_tag(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_tag as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_vault(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_vault as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_vault_credential(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_vault_credential as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_webhook_endpoint(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import get_webhook_endpoint as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def interrupt_and_send_session_message(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import interrupt_and_send_session_message as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def interrupt_session(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import interrupt_session as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_agent_memories(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_agent_memories as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_agent_memory_activity(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_agent_memory_activity as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_agent_memory_summaries(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_agent_memory_summaries as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_agent_templates(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_agent_templates as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_agent_versions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_agent_versions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_agents(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_agents as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_automation_runs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_automation_runs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_automations(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_automations as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_compute_offerings(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_compute_offerings as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_environment_setup_runs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_environment_setup_runs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_environment_setup_templates(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_environment_setup_templates as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_environments(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_environments as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_evaluation_runs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_evaluation_runs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_event_sources(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_event_sources as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_files(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_files as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_managed_agent_evaluations(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_managed_agent_evaluations as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_memories(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_memories as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_memory_stores(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_memory_stores as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_memory_versions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_memory_versions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_models(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_models as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_reflections(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_reflections as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_sandbox_providers(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_sandbox_providers as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_events(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_events as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_gestalt(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_gestalt as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_metadata_keys(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_metadata_keys as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_metadata_values(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_metadata_values as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_model_cost_nodes(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_model_cost_nodes as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_model_costs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_model_costs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_outcomes(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_outcomes as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_pending_inputs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_pending_inputs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_resource_samples(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_resource_samples as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_resources(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_resources as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_threads(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_threads as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_session_usage(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_session_usage as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_sessions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_sessions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_skill_groups(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_skill_groups as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_skill_versions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_skill_versions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_skills(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_skills as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_skills_in_group(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_skills_in_group as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_tags(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_tags as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_trigger_bindings(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_trigger_bindings as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_vault_credentials(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_vault_credentials as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_vaults(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_vaults as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_webhook_endpoints(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import list_webhook_endpoints as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def open_session_analyst(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import open_session_analyst as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def pause_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import pause_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def pause_event_source(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import pause_event_source as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def preview_skill_disclosure(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import preview_skill_disclosure as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def probe_mcp_server(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import probe_mcp_server as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def redact_memory_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import redact_memory_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def remove_agent_tag(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import remove_agent_tag as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def replace_agent_tags(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import replace_agent_tags as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def replace_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import replace_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def replace_event_source(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import replace_event_source as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def restore_memory_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import restore_memory_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def resume_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import resume_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def resume_event_source(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import resume_event_source as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def run_automation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import run_automation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def send_session_events(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import send_session_events as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def start_session(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import start_session as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_agent_learning(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_agent_learning as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_memory(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_memory as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_memory_store(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_memory_store as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_skill(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_skill as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_skill_group(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_skill_group as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_tag(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_tag as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_trigger_binding(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_trigger_binding as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_vault(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_vault as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_vault_credential(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_vault_credential as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_webhook_endpoint(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import update_webhook_endpoint as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def upsert_trigger_binding(self, *args: Any, **kwargs: Any) -> Any:
        from .api.managed_agents import upsert_trigger_binding as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Marketplace:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_image(self, *args: Any, **kwargs: Any) -> Any:
        from .api.marketplace import get_image as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_images(self, *args: Any, **kwargs: Any) -> Any:
        from .api.marketplace import list_images as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Me:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_identity(self, *args: Any, **kwargs: Any) -> Any:
        from .api.me import get_identity as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_permissions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.me import get_permissions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Models:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.models import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _ProbeRuns:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def cancel(self, *args: Any, **kwargs: Any) -> Any:
        from .api.probe_runs import cancel as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.probe_runs import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_live_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.probe_runs import get_live_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _ProblemRuns:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def bulk_create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import bulk_create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_live_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import get_live_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import get_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_usage(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import get_usage as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_workspace_file_download_url(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import get_workspace_file_download_url as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_job(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import list_for_job as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import list_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_grade_history(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import list_grade_history as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_output_files(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import list_output_files as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_workspace_entries(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import list_workspace_entries as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def regrade(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import regrade as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def regrade_failed_graders(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_runs import regrade_failed_graders as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _ProblemVersions:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_ai_operation(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import get_ai_operation as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import list_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def lock(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import lock as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problem_versions import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Problems:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def bulk_delete_by_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import bulk_delete_by_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def bulk_reset_by_external_id(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import bulk_reset_by_external_id as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def bulk_upsert(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import bulk_upsert as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_stats_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import get_stats_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def has_completed_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import has_completed_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_by_external_ids(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import list_by_external_ids as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_summaries_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import list_summaries_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def reset(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import reset as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def upsert_with_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.problems import upsert_with_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Qa:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def attach_config_file(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import attach_config_file as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel_job(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import cancel_job as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_config(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import create_config as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete_config(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import delete_config as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach_config_file(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import detach_config_file as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_config(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import get_config as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_job(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import get_job as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_job_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import get_job_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_live_job_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import get_live_job_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_oracle_result(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import get_oracle_result as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_configs_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import list_configs_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_grades_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import list_grades_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_jobs_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import list_jobs_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def trigger_job(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import trigger_job as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def trigger_job_batch(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import trigger_job_batch as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update_config(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa import update_config as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _QaGates:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_gates import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_gates import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_status(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_gates import get_status as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_gates import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def request_stage_clearance(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_gates import request_stage_clearance as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _QaTriggers:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_triggers import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_triggers import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.qa_triggers import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _RolloutBatches:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rollout_batches import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rollout_batches import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_results(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rollout_batches import get_results as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _RubricScores:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def get_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubric_scores import get_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_job(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubric_scores import list_for_job as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_problem_run(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubric_scores import list_for_problem_run as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Rubrics:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubrics import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubrics import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubrics import list_for_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.rubrics import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _RunConfigMenus:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def add_entry(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_menus import add_entry as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_readiness(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_menus import get_readiness as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _RunConfigRuns:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def cancel(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_runs import cancel as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_runs import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_runs import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _RunConfigVersions:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def clear_default(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import clear_default as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def discard(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import discard as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def discover_mcp_tools(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import discover_mcp_tools as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_probe_runs(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import list_probe_runs as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def lock(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import lock as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def probe(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import probe as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def resolve(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import resolve as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def set_default(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import set_default as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_config_versions import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _RunConfigs:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import create_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_inherited_default_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import get_inherited_default_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_bindable_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_bindable_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_system(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_for_system as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_reaped_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_reaped_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_reaped_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_reaped_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_reaped_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_reaped_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_reaped_for_system(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_reaped_for_system as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_snapshots_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_snapshots_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_versions(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_versions as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_visible_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_visible_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_visible_for_organization(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_visible_for_organization as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_visible_for_problem(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_visible_for_problem as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_visible_for_system(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import list_visible_for_system as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def restore(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import restore as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.run_configs import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Sessions:
    def __init__(self, client: Any) -> None:
        self._client = client

    @property
    def handoff(self) -> _SessionsHandoff:
        return _SessionsHandoff(self._client)


class _SessionsHandoff:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def open(self, *args: Any, **kwargs: Any) -> Any:
        from .api.sessions_handoff import open_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _SynthesizerRuns:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def apply(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import apply as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def cancel(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import cancel as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_live_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import get_live_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_transcript(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import get_transcript as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_environment(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import list_for_environment as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list_for_version(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import list_for_version as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def trigger(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizer_runs import trigger as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _Synthesizers:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def attach_file(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import attach_file as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import delete as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def detach_file(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import detach_file as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_built_in(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import get_built_in as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def list(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import list_ as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        from .api.synthesizers import update as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class _TuningRuns:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        from .api.tuning_runs import create as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        from .api.tuning_runs import get as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))

    async def get_training_contract(self, *args: Any, **kwargs: Any) -> Any:
        from .api.tuning_runs import get_training_contract as _endpoint
        return _unwrap(await _endpoint.asyncio_detailed(*args, client=self._client, **kwargs))


class Recursion:
    """Namespaced entry point. See `recursion.create_recursion_client`."""

    def __init__(self, client: Any) -> None:
        self._client = client

    @property
    def agent_skills(self) -> _AgentSkills:
        return _AgentSkills(self._client)

    @property
    def check_fix_cycles(self) -> _CheckFixCycles:
        return _CheckFixCycles(self._client)

    @property
    def computes(self) -> _Computes:
        return _Computes(self._client)

    @property
    def cost_limits(self) -> _CostLimits:
        return _CostLimits(self._client)

    @property
    def customer_secrets(self) -> _CustomerSecrets:
        return _CustomerSecrets(self._client)

    @property
    def environment_files(self) -> _EnvironmentFiles:
        return _EnvironmentFiles(self._client)

    @property
    def environments(self) -> _Environments:
        return _Environments(self._client)

    @property
    def evaluations(self) -> _Evaluations:
        return _Evaluations(self._client)

    @property
    def exports(self) -> _Exports:
        return _Exports(self._client)

    @property
    def files(self) -> _Files:
        return _Files(self._client)

    @property
    def form_answers(self) -> _FormAnswers:
        return _FormAnswers(self._client)

    @property
    def forms(self) -> _Forms:
        return _Forms(self._client)

    @property
    def git_repo_claims(self) -> _GitRepoClaims:
        return _GitRepoClaims(self._client)

    @property
    def grading_runs(self) -> _GradingRuns:
        return _GradingRuns(self._client)

    @property
    def images(self) -> _Images:
        return _Images(self._client)

    @property
    def imports(self) -> _Imports:
        return _Imports(self._client)

    @property
    def issue_comments(self) -> _IssueComments:
        return _IssueComments(self._client)

    @property
    def issues(self) -> _Issues:
        return _Issues(self._client)

    @property
    def jobs_v2(self) -> _JobsV2:
        return _JobsV2(self._client)

    @property
    def managed_agents(self) -> _ManagedAgents:
        return _ManagedAgents(self._client)

    @property
    def marketplace(self) -> _Marketplace:
        return _Marketplace(self._client)

    @property
    def me(self) -> _Me:
        return _Me(self._client)

    @property
    def models(self) -> _Models:
        return _Models(self._client)

    @property
    def probe_runs(self) -> _ProbeRuns:
        return _ProbeRuns(self._client)

    @property
    def problem_runs(self) -> _ProblemRuns:
        return _ProblemRuns(self._client)

    @property
    def problem_versions(self) -> _ProblemVersions:
        return _ProblemVersions(self._client)

    @property
    def problems(self) -> _Problems:
        return _Problems(self._client)

    @property
    def qa(self) -> _Qa:
        return _Qa(self._client)

    @property
    def qa_gates(self) -> _QaGates:
        return _QaGates(self._client)

    @property
    def qa_triggers(self) -> _QaTriggers:
        return _QaTriggers(self._client)

    @property
    def rollout_batches(self) -> _RolloutBatches:
        return _RolloutBatches(self._client)

    @property
    def rubric_scores(self) -> _RubricScores:
        return _RubricScores(self._client)

    @property
    def rubrics(self) -> _Rubrics:
        return _Rubrics(self._client)

    @property
    def run_config_menus(self) -> _RunConfigMenus:
        return _RunConfigMenus(self._client)

    @property
    def run_config_runs(self) -> _RunConfigRuns:
        return _RunConfigRuns(self._client)

    @property
    def run_config_versions(self) -> _RunConfigVersions:
        return _RunConfigVersions(self._client)

    @property
    def run_configs(self) -> _RunConfigs:
        return _RunConfigs(self._client)

    @property
    def sessions(self) -> _Sessions:
        return _Sessions(self._client)

    @property
    def synthesizer_runs(self) -> _SynthesizerRuns:
        return _SynthesizerRuns(self._client)

    @property
    def synthesizers(self) -> _Synthesizers:
        return _Synthesizers(self._client)

    @property
    def tuning_runs(self) -> _TuningRuns:
        return _TuningRuns(self._client)

