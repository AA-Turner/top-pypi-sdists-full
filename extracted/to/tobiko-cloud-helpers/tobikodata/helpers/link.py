import enum
import typing as t
import urllib.parse
from dataclasses import dataclass

from tobikodata.helpers import urljoin


class ActionTab(str, enum.Enum):
    SUMMARY = "summary"
    EXPLORE = "explore"


class RunSummaryTab(str, enum.Enum):
    EXECUTIONS = "executions"
    AUDITS = "audits"


class PlanSummaryTab(str, enum.Enum):
    DIFF_CHANGES = "diff-changes"
    PHYSICAL_UPDATES = "physical-updates"
    EXECUTIONS = "executions"
    AUDITS = "audits"
    VIRTUAL_UPDATES = "virtual-updates"


class DebuggerModelEvaluationTab(str, enum.Enum):
    DEFINITION = "definition"
    IMPACT = "impact"
    SCHEMA = "schema"
    INTERVALS = "intervals"


class DebuggerEvaluationTab(str, enum.Enum):
    OVERVIEW = "overview"
    ERROR = "error"
    LOG = "log"


class TabName(str, enum.Enum):
    TAB = "tab"
    TAB_SUMMARY = "tab_summary"
    TAB_MODEL_EVALUATION = "tab_model_evaluation"
    TAB_EVALUATION = "tab_evaluation"
    MODEL_NAME = "model_name"
    EVALUATION_ID = "evaluation_id"


TabSummary = t.Union[RunSummaryTab, PlanSummaryTab]

EvaluationScope = t.Literal["plans", "runs"]
EnvironmentScope = t.Union[EvaluationScope, t.Literal["models"]]

# This is primarily for generating deep links for Plan or Run UI pages
# Used for Airflow / Dagster integrations, CICD bot, Plan links in the CLI


@dataclass
class TobikoCloudLinkGenerator:
    environment: str
    url_template: str = "/environments/{environment}/{scope}/{id}"
    base: str = "/"

    def get_environment_url(self) -> str:
        return self._get_url(url_template="/environments/{environment}")

    def get_model_details_url(self, model_name: str, model_version: str) -> str:
        return self._get_url_with_query_params(
            scope="models",
            id=model_name,
            query_params=urllib.parse.urlencode({"version": model_version}),
        )

    def get_plan_summary_url(self, plan_id: str) -> str:
        return self._get_summary_url("plans", plan_id, PlanSummaryTab.DIFF_CHANGES)

    def get_plan_audits_url(self, plan_id: str) -> str:
        return self._get_summary_url("plans", plan_id, PlanSummaryTab.AUDITS)

    def get_run_summary_url(self, run_id: str) -> str:
        return self._get_summary_url(
            scope="runs", plan_or_run_id=run_id, tab=RunSummaryTab.EXECUTIONS
        )

    def get_run_audits_url(self, run_id: str) -> str:
        return self._get_summary_url(scope="runs", plan_or_run_id=run_id, tab=RunSummaryTab.AUDITS)

    def get_plan_evaluation_overview_url(
        self, plan_id: str, model_name: str, evaluation_id: str
    ) -> str:
        return self._get_evaluation_url(
            "plans", plan_id, model_name, evaluation_id, DebuggerEvaluationTab.OVERVIEW
        )

    def get_plan_evaluation_log_url(self, plan_id: str, model_name: str, evaluation_id: str) -> str:
        return self._get_evaluation_url(
            "plans", plan_id, model_name, evaluation_id, DebuggerEvaluationTab.LOG
        )

    def get_run_evaluation_overview_url(
        self, run_id: str, model_name: str, evaluation_id: str
    ) -> str:
        return self._get_evaluation_url(
            "runs", run_id, model_name, evaluation_id, DebuggerEvaluationTab.OVERVIEW
        )

    def get_run_evaluation_log_url(self, run_id: str, model_name: str, evaluation_id: str) -> str:
        return self._get_evaluation_url(
            "runs", run_id, model_name, evaluation_id, DebuggerEvaluationTab.LOG
        )

    def _get_summary_url(
        self,
        scope: EvaluationScope,
        plan_or_run_id: str,
        tab: t.Union[PlanSummaryTab, RunSummaryTab],
    ) -> str:
        """Generate the URL for the summary with the search params (if any)"""
        return self._get_url_with_query_params(
            scope,
            plan_or_run_id,
            self._parse_query_params(
                tab=ActionTab.SUMMARY,
                tab_summary=tab,
            ),
        )

    def _get_evaluation_url(
        self,
        scope: EvaluationScope,
        plan_or_run_id: str,
        model_name: str,
        evaluation_id: str,
        tab: DebuggerEvaluationTab,
    ) -> str:
        """Generate the URL for the evaluation log with the search params (if any)"""
        return self._get_url_with_query_params(
            scope,
            plan_or_run_id,
            self._parse_query_params(
                tab=ActionTab.EXPLORE,
                model_name=model_name,
                evaluation_id=evaluation_id,
                tab_model_evaluation=DebuggerModelEvaluationTab.DEFINITION,
                tab_evaluation=tab,
            ),
        )

    def _get_url(
        self,
        scope: t.Optional[EnvironmentScope] = None,
        id: t.Optional[str] = None,
        url_template: t.Optional[str] = None,
    ) -> str:
        """Generate the URL"""
        url_template = url_template or self.url_template
        return urljoin(
            self.base,
            url_template.format(
                environment=self.environment,
                scope=scope,
                id=id,
            ),
        )

    def _get_url_with_query_params(
        self, scope: EnvironmentScope, id: str, query_params: str
    ) -> str:
        """Generate the URL with the search params (if any)"""
        url = self._get_url(scope, id)
        if query_params:
            url += "?" + query_params
        return url

    def _parse_query_params(self, **kwargs: t.Any) -> str:
        """Parse the search params from the kwargs"""
        return urllib.parse.urlencode(
            {
                TabName(k).value: v.value if isinstance(v, enum.Enum) else v
                for k, v in kwargs.items()
                if v is not None
            }
        )
