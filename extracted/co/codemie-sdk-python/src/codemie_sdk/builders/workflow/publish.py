# Copyright 2026 EPAM Systems, Inc. ("EPAM")
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Internal helper backing :meth:`WorkflowBuilder.publish`.

Resolves every name-only assistant reference against the live platform,
renders the definition's ``yaml_config``, and dispatches to
``WorkflowService.create_workflow``/``.update`` — both used completely
unmodified. Any exception either call raises propagates unchanged.

The public entry point is :meth:`WorkflowBuilder.publish` (``builder.py``),
which supplies the rendered definition from its own accumulated state; this
module's ``_publish`` stays private so the only public surface callers see
is the method, matching the original design's class diagram (``publish``
as a bound method on ``WorkflowBuilder``, not a free function taking a
``definition`` parameter).
"""

from typing import TYPE_CHECKING

from ...models.assistant import Assistant, AssistantBase
from ...models.workflow import WorkflowCreateRequest, WorkflowUpdateRequest
from .definition import WorkflowDefinition

if TYPE_CHECKING:
    from ...client.client import CodeMieClient

# AssistantService.list's own default; pass it explicitly so the paging loop
# below always knows the page size it asked for, regardless of that default.
_ASSISTANTS_PAGE_SIZE = 12


def _find_assistant_id(
    assistants: list[Assistant | AssistantBase], name: str, project: str
) -> str:
    """Return the single assistant id matching `name`, or raise."""
    matches = [a for a in assistants if a.name == name]
    if len(matches) == 0:
        raise ValueError(f"no assistant named {name!r} in project {project!r}")
    if len(matches) > 1:
        raise ValueError(
            f"ambiguous assistant name {name!r} in project {project!r}: "
            f"{len(matches)} matches"
        )
    return matches[0].id


def _list_all_assistants(
    client: "CodeMieClient", project: str
) -> list[Assistant | AssistantBase]:
    """Page through every assistant in `project`, not just the first page.

    `AssistantService.list` defaults `per_page` to 12; a single unpaginated
    call would silently miss a name-only reference to any assistant beyond
    that first page. Pages are requested sorted by `name` — the service's
    default order (`update_date desc`, no tie-breaker) can shift a row
    between pages while paging by offset, which would skip it or return it
    twice; a stable sort key doesn't. Results are also deduped by `id` as a
    second safety net against that same reordering. `minimal_response=True`
    is enough since only `id`/`name` are used.
    """
    assistants: dict[str, Assistant | AssistantBase] = {}
    page = 0
    while True:
        batch = client.assistants.list(
            minimal_response=True,
            filters={"project": project},
            sort_by="name",
            page=page,
            per_page=_ASSISTANTS_PAGE_SIZE,
        )
        for assistant in batch:
            assistants[assistant.id] = assistant
        if len(batch) < _ASSISTANTS_PAGE_SIZE:
            break
        page += 1
    return list(assistants.values())


def _make_assistant_resolver(client: "CodeMieClient", project: str):
    """Build a memoized `resolve_assistant_name` closure for `to_yaml_config`.

    The platform lookup (`client.assistants.list`, paged through in full)
    runs at most once per `publish()` call, regardless of how many
    name-only references the definition contains.
    """
    cache: dict[str, list[Assistant | AssistantBase]] = {}

    def resolve_assistant_name(name: str) -> str:
        if "assistants" not in cache:
            cache["assistants"] = _list_all_assistants(client, project)
        return _find_assistant_id(cache["assistants"], name, project)

    return resolve_assistant_name


def _non_empty_description(description: str | None) -> str:
    """Substitute a single space for a missing description.

    The backend's create/update request models both require a non-empty
    `description: str`; the builder's own `description` is optional. An
    empty string would still fail that `min_length=1`/required-string check
    before the request ever reaches the backend, so a single space stands
    in for "no meaningful description supplied" while satisfying it.
    """
    return description or " "


def _build_create_request(
    definition: WorkflowDefinition, project: str, yaml_config: str
) -> WorkflowCreateRequest:
    return WorkflowCreateRequest(
        project=project,
        name=definition.name,
        description=_non_empty_description(definition.description),
        yaml_config=yaml_config,
        mode=definition.mode,
        shared=definition.shared,
        icon_url=definition.icon_url,
    )


def _build_update_request(
    definition: WorkflowDefinition, project: str, yaml_config: str
) -> WorkflowUpdateRequest:
    return WorkflowUpdateRequest(
        project=project,
        name=definition.name,
        description=_non_empty_description(definition.description),
        yaml_config=yaml_config,
        mode=definition.mode,
        shared=definition.shared,
        icon_url=definition.icon_url,
    )


def _publish(
    client: "CodeMieClient",
    definition: WorkflowDefinition,
    project: str,
    *,
    workflow_id: str | None = None,
) -> dict:
    """Render `definition` and create or update it on the live platform.

    Private helper behind `WorkflowBuilder.publish`; not part of the
    package's public surface — see the module docstring.

    Args:
        client: An authenticated `CodeMieClient`.
        definition: The workflow definition to publish.
        project: Project the workflow belongs to; also scopes assistant-name
            resolution for any unresolved `WorkflowAssistant` reference.
        workflow_id: When given, updates that existing workflow instead of
            creating a new one.

    Returns:
        Whatever `WorkflowService.create_workflow`/`.update` returns today
        (currently the raw response `dict`, not a `Workflow` model).

    Raises:
        ValueError: An assistant name in `definition` matches zero or more
            than one assistant in `project`.
        Exception: Whatever `create_workflow`/`.update` raises (currently an
            unwrapped `requests.HTTPError` on backend rejection) propagates
            unchanged — never wrapped, reshaped, or swallowed here.
    """
    resolve_assistant_name = _make_assistant_resolver(client, project)
    yaml_config = definition.to_yaml_config(
        resolve_assistant_name=resolve_assistant_name
    )

    if workflow_id is None:
        request = _build_create_request(definition, project, yaml_config)
        return client.workflows.create_workflow(request)

    update_request = _build_update_request(definition, project, yaml_config)
    return client.workflows.update(workflow_id, update_request)
