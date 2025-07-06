from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..tristar.governor import TriStarGovernor
from ..core.tsal_executor import TSALExecutor
from ..tools.issue_agent import create_issue, handle_http_error


@dataclass
class ThreatReport:
    anomalies: List[str]
    resonance: float
    entropy: int
    health: int


@dataclass
class PriorityResearchTeamAgent:
    repo: str
    token: str | None = None
    governor: TriStarGovernor = field(default_factory=TriStarGovernor)
    log: List[ThreatReport] = field(default_factory=list)

    def scan(self, executor: TSALExecutor) -> ThreatReport:
        anomalies = self.governor.patrol(executor)
        report = ThreatReport(
            anomalies=anomalies,
            resonance=executor._calculate_mesh_resonance(),
            entropy=executor.meta_agent.entropy,
            health=executor.meta_agent.health,
        )
        self.log.append(report)
        if anomalies and self.token:
            msg = f"{anomalies} | resonance={report.resonance:.3f}"
            try:
                create_issue(self.repo, "Threat detected", msg, self.token)
            except Exception as exc:  # pragma: no cover - network faults
                handle_http_error(self.repo, exc, msg, token=self.token)
        return report
