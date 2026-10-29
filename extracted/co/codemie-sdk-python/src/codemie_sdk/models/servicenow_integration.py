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

"""ServiceNow integration models for the CodeMie SDK.

The integration endpoints are callable only by the ServiceNow integration service account.
The request model is deliberately permissive: the server owns the validation rules, so the
SDK sends what the caller gives it and surfaces the server's verdict as an HTTP error.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ServiceNowBudgetAction(str, Enum):
    """Budget action requested by ServiceNow."""

    SET = "set"
    ADJUST = "adjust"
    CANCEL = "cancel"


class ServiceNowProject(BaseModel):
    """A shared project returned by the project lookup."""

    model_config = ConfigDict(extra="ignore")

    project_name: str
    display_name: str | None = None


class ServiceNowBudgetRequest(BaseModel):
    """Request body for applying a ServiceNow budget request to a project.

    Attributes:
        action: ``set`` replaces the budget, ``adjust`` merges into it, ``cancel`` deletes it.
        request_id: ServiceNow request number, used for audit logs and new budget names.
        epam_project_code: EPAM project code; names the cost center when it differs from
            the CodeMie project name.
        codemie_project_name: CodeMie project to manage; the server defaults it to
            ``epam_project_code`` when omitted.
        admin_emails: People to make project admins (ignored by ``cancel``).
        amounts: Monthly budget in USD per category (``platform``, ``cli``,
            ``premium_models``); required for ``set`` and ``adjust``.
    """

    # Non-finite amounts are sent as the JSON constants NaN / Infinity instead of null,
    # so the server, not the client, rejects them.
    model_config = ConfigDict(ser_json_inf_nan="constants")

    action: ServiceNowBudgetAction
    request_id: str
    epam_project_code: str
    codemie_project_name: str | None = None
    admin_emails: list[str] = Field(default_factory=list)
    amounts: dict[str, float] | None = None


class ServiceNowBudgetCategory(BaseModel):
    """Budget of one spend category in a budget response."""

    model_config = ConfigDict(extra="ignore")

    category: str
    max_budget: float
    soft_budget: float
    budget_reset_at: str | None = None


class ServiceNowBudgetGroup(BaseModel):
    """Budget of a project after the request, with its categories in a fixed order."""

    model_config = ConfigDict(extra="ignore")

    total_amount: float
    budget_duration: str
    categories: list[ServiceNowBudgetCategory]


class ServiceNowBudgetResponse(BaseModel):
    """Outcome of a budget request."""

    model_config = ConfigDict(extra="ignore")

    project_name: str
    cost_center: str | None = None
    created_project: bool
    created_cost_center: bool
    budget: ServiceNowBudgetGroup | None = None
    admins_assigned: list[str] = Field(default_factory=list)
    admins_pending: list[str] = Field(default_factory=list)
