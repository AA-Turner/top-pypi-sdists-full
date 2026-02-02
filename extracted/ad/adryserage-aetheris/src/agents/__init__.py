"""
Agents d'analyse spécialisés

Core agents (v2.0+):
- CodeAnalysisExpert: File-level code analysis
- SecurityAnalysisAgent: Security vulnerability detection
- ArchitectAnalysisAgent: Architecture and design patterns
- CodeMetricsAgent: Code quality metrics
- DependencyVulnerabilityAgent: Dependency vulnerability scanning
- QualityAssuranceAgent: Quality assurance checks
- UserStoryAnalysisAgent: User story flow analysis
- PRReviewAgent: Pull request review

Extended agents (v2.10+):
- TypeSafetyAgent: Type safety issue detection
- PerformanceAnalysisAgent: Performance anti-pattern detection
- APIContractAgent: API contract violation detection
- DataPrivacyAgent: Data privacy and compliance analysis
"""

from src.agents.api_contract_agent import APIContractAgent
from src.agents.base_agent import BaseAgent
from src.agents.data_privacy_agent import DataPrivacyAgent
from src.agents.performance_analysis_agent import PerformanceAnalysisAgent
from src.agents.type_safety_agent import TypeSafetyAgent

__all__ = [
    # Base
    "BaseAgent",
    # v2.10 Extended Agents
    "TypeSafetyAgent",
    "PerformanceAnalysisAgent",
    "APIContractAgent",
    "DataPrivacyAgent",
]
