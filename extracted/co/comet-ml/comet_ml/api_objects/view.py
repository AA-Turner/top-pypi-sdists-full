# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import json
from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional


@dataclass
class View:
    """Represents a saved dashboard view configuration.

    A View stores dashboard layout and query state for a project or experiment.
    Views can be created and retrieved via the API or APIExperiment classes.

    Args:
        name: The display name of the view (required).
        template_id: Unique identifier for the view template.
        project_id: The project this view belongs to.
        experiment_key: The experiment this view is scoped to.
        query_state: Serialized experiment query/filter state.
        chart_state: Serialized dashboard chart configuration.
        table_state: Serialized react grid table configuration.
        v2: v2-format view state dict returned by the backend.
    """

    name: str

    # Settable optional fields
    template_id: Optional[str] = None
    project_id: Optional[str] = None
    experiment_key: Optional[str] = None
    query_state: Optional[str] = None
    chart_state: Optional[str] = None
    table_state: Optional[str] = None
    v2: Optional[Any] = None

    # Read-only fields from backend response
    v3: Optional[Any] = None
    source: Optional[str] = None
    view_source: Optional[str] = None  # "dashboard_template" or "chart_template"
    current: Optional[bool] = None
    unsaved_view: Optional[bool] = None
    created_by: Optional[str] = None
    created_from_template_id: Optional[str] = None
    project_default: Optional[bool] = None
    project_personal_default: Optional[bool] = None
    auto_refresh_enabled: Optional[bool] = None
    last_update: Optional[int] = None
    pinned_experiments: Optional[List[str]] = field(default=None)
    code_panel_template_ids: Optional[List[str]] = field(default=None)

    def __post_init__(self):
        if not self.name:
            raise ValueError("View name must not be empty")
        for field_name in ("query_state", "chart_state", "table_state"):
            value = getattr(self, field_name)
            if value is not None:
                try:
                    json.loads(value)
                except (ValueError, TypeError):
                    raise ValueError("%s must be a valid JSON string" % field_name)

    def to_upsert_payload(self, project_id: str) -> Dict[str, Any]:
        """Build a camelCase payload dict for the upsert endpoint.

        Args:
            project_id: The project ID to include in the payload.

        Returns:
            A dict suitable for POST to ``write/views/upsert``.
        """
        payload: Dict[str, Any] = {
            "projectId": project_id,
            "templateName": self.name,
        }

        _optional_mappings = {
            "templateId": self.template_id,
            "experimentKey": self.experiment_key,
            "experimentQueryState": self.query_state,
            "dashboardChartState": self.chart_state,
            "reactGridTableState": self.table_state,
            "v2": self.v2,
            "v3": self.v3,
        }

        for key, value in _optional_mappings.items():
            if value is not None:
                payload[key] = value

        return payload

    def as_portable(self) -> "View":
        """Return a copy of this view with all project- and experiment-specific
        identifiers removed, suitable for creating in a different project or
        experiment context.

        The following fields are cleared:
        - template_id: backend-assigned ID in the source project; a new one
          will be assigned by the backend on creation
        - experiment_key: the experiment does not exist in the target project
        - project_id: cleared for clarity (not used during upsert anyway)
        - pinned_experiments: experiment keys are invalid in a different project
        - experimentKey inside v2/v3: the backend only embeds a new experimentKey
          into v2 if v2 does not already contain one, so the embedded key must be
          cleared here to allow the destination experiment key to be set correctly

        The layout/configuration fields (query_state, chart_state, table_state)
        are preserved as-is. If those fields embed experiment keys in their JSON,
        the caller is responsible for adjusting them before creating the view.

        Returns:
            A new View instance safe to pass to API.create_view or
            APIExperiment.create_view in a different context.
        """

        def _strip_experiment_key(node):
            if isinstance(node, dict) and "experimentKey" in node:
                node = {k: v for k, v in node.items() if k != "experimentKey"}
                if not node:
                    return None
            return node

        return replace(
            self,
            template_id=None,
            project_id=None,
            experiment_key=None,
            pinned_experiments=None,
            v2=_strip_experiment_key(self.v2),
            v3=_strip_experiment_key(self.v3),
        )

    @classmethod
    def from_payload_dict(cls, payload: Dict[str, Any]) -> "View":
        """Deserialize a backend response dict into a View instance.

        Args:
            payload: A dict from the backend ``views/get-all`` response.

        Returns:
            A View instance populated from the payload.
        """

        def _get(*keys):
            for k in keys:
                if k in payload:
                    return payload[k]
            return None

        return cls(
            name=_get("templateName", "template_name") or "",
            template_id=_get("templateId", "template_id"),
            project_id=_get("projectId", "project_id"),
            experiment_key=_get("experimentKey", "experiment_key"),
            query_state=payload.get("experimentQueryState") or None,
            chart_state=payload.get("dashboardChartState") or None,
            table_state=payload.get("reactGridTableState") or None,
            v2=payload.get("v2"),
            v3=payload.get("v3"),
            source=payload.get("source"),
            view_source=_get("viewSource", "view_source"),
            current=payload.get("current"),
            unsaved_view=_get("unsavedView", "unsaved_view"),
            created_by=_get("createdBy", "created_by"),
            created_from_template_id=_get(
                "createdFromTemplateId", "created_from_template_id"
            ),
            project_default=_get("projectDefault", "project_default"),
            project_personal_default=_get(
                "projectPersonalDefault", "project_personal_default"
            ),
            auto_refresh_enabled=_get("autoRefreshEnabled", "isAutoRefreshEnabled"),
            last_update=payload.get("lastUpdate"),
            pinned_experiments=payload.get("pinnedExperiments"),
            code_panel_template_ids=payload.get("codePanelTemplateIds"),
        )
