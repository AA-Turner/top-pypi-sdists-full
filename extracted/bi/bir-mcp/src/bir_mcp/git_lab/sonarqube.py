import datetime
import inspect
from typing import override

import fastmcp.tools
import httpx

from bir_mcp.core import AhttpxMixin, BaseMcp, build_readonly_tools
from bir_mcp.git_lab.annotations import ProjectPathOrUrlType
from bir_mcp.git_lab.utils import GitLabUrl
from bir_mcp.utils import araise_for_status, build_url, filter_dict_by_keys, to_maybe_ssl_context


class SonarQube(BaseMcp, AhttpxMixin):
    def __init__(
        self,
        token: str,
        url: str = "https://sonarqube.kapitalbank.az",
        gitlab_url: str = "https://gitlab.kapitalbank.az",
        ssl_verify: bool | str = True,
        timezone: str = "UTC",
    ):
        super().__init__(timezone=timezone)
        self.ahttpx = httpx.AsyncClient(
            base_url=url,
            auth=(token, ""),
            verify=to_maybe_ssl_context(ssl_verify),
            event_hooks={"response": [araise_for_status]},
        )
        self.gitlab_url = GitLabUrl(base_url=gitlab_url)
        self.main_metrics = [
            "alert_status",
            "reliability_rating",
            "new_reliability_rating",
            "security_rating",
            "new_security_rating",
            "sqale_rating",
            "new_maintainability_rating",
            "security_review_rating",
            "new_security_review_rating",
            "coverage",
            "new_coverage",
            "duplicated_lines_density",
            "new_duplicated_lines_density",
            "sqale_index",
            "bugs",
            "new_bugs",
            "vulnerabilities",
            "new_vulnerabilities",
            "code_smells",
            "new_code_smells",
            "security_hotspots",
            "new_security_hotspots",
            "security_hotspots_reviewed",
            "new_security_hotspots_reviewed",
            "complexity",
            "cognitive_complexity",
        ]

    @override
    def get_tag(self):
        return "sonarqube"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="Bir SonarQube MCP server",
            instructions=inspect.cleandoc("""
                SonarQube related tools.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            self.get_main_project_metrics,
            self.get_project_quality_gates_status,
            self.http_request,
        ]
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        return tools

    async def list_all_metrics(self, page_size: int = 500) -> list[dict]:
        response = await self.ahttpx_get("metrics/search", ps=page_size)
        metrics = response.json()["metrics"]
        metrics = [filter_dict_by_keys(metric, ["key", "description"]) for metric in metrics]
        return metrics

    def gitlab_to_sonarqube_project(self, project_path_or_url: ProjectPathOrUrlType) -> str:
        project_path = self.gitlab_url.extract_project_path(project_path_or_url)
        # The convention is that SonarQube projects are named as "{gitlab_group}-{gitlab_project}".
        sonarqube_project = "-".join(project_path.split("/")[-2:]).lower()
        return sonarqube_project

    async def get_analysis_age(self, project: str, branch: str = "master") -> datetime.timedelta:
        response = await self.ahttpx_get("/api/components/show", component=project, branch=branch)
        analysis_date = response.json()["component"]["analysisDate"]
        age = datetime.datetime.now(datetime.UTC) - datetime.datetime.fromisoformat(analysis_date)
        return age

    async def get_main_project_metrics(
        self, project_path_or_url: ProjectPathOrUrlType, branch: str = "master"
    ) -> dict:
        """
        Get the main metrics for a project, such as alert status, reliability and security ratings,
        coverage, bugs, complexity, etc.
        """
        project = self.gitlab_to_sonarqube_project(project_path_or_url)
        response = await self.ahttpx_get(
            "measures/component",
            component=project,
            branch=branch,
            metricKeys=",".join(self.main_metrics),
        )
        measures = response.json()["component"]["measures"]
        metrics = []
        for measure in measures:
            if period := measure.pop("period", None):
                measure.pop("periods")
                period.pop("index")
                measure |= period

            metrics.append(measure)

        age = await self.get_analysis_age(project=project, branch=branch)
        url = build_url(self.ahttpx.base_url, "dashboard", id=project, branch=branch)
        metrics = {
            "metrics": metrics,
            "analysis_age": str(age),
            "sonarqube_dashboard_url": url,
        }
        return metrics

    async def get_project_quality_gates_status(
        self, project_path_or_url: ProjectPathOrUrlType, branch: str = "master"
    ) -> dict:
        """Get the quality gates status for a project."""
        project = self.gitlab_to_sonarqube_project(project_path_or_url)
        response = await self.ahttpx_get(
            "qualitygates/project_status", projectKey=project, branch=branch
        )
        project_status = response.json()["projectStatus"]
        conditions = [
            filter_dict_by_keys(i, ["metricKey", "status", "actualValue", "errorThreshold"])
            for i in project_status["conditions"]
        ]
        age = await self.get_analysis_age(project=project, branch=branch)
        project_status = {
            "status": project_status["status"],
            "conditions": conditions,
            "analysis_age": str(age),
        }
        return project_status
