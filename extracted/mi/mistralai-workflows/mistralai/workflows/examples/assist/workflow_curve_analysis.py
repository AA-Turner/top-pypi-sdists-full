import asyncio

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

from mistralai.workflows.plugins.mistralai.conversational_ui_components import (
    Alert,
    Badge,
    Card,
    Chart,
    Column,
    Markdown,
    Row,
    Tooltip,
)

logger = structlog.get_logger(__name__)


@workflows.activity()
async def discover_curves() -> dict:
    """Simulate querying simulation and physical test databases for curve data."""
    async with workflows.task("discover_curves", {"status": "querying databases"}):
        await asyncio.sleep(1)
    return {
        "simulation_curves": 24,
        "physical_curves": 18,
        "sensor_channels": ["chest deflection", "head acceleration", "femur load", "neck moment"],
    }


@workflows.activity()
async def analyze_correlation() -> dict:
    """Simulate computing CORA scores between matched simulation/physical curve pairs."""
    async with workflows.task("analyze_correlation", {"status": "computing CORA scores"}):
        await asyncio.sleep(1)
    return {
        "matched_pairs": 12,
        "deviations_above_threshold": 4,
        "global_cora_score": 0.82,
    }


@workflows.workflow.define(
    name="curve-analysis-workflow",
    workflow_display_name="Curve Analysis",
    workflow_description="Compare simulation curves against physical test data with rich UI reports",
)
class CurveAnalysisWorkflow:
    @workflows.workflow.entrypoint
    async def run(
        self,
        simulation_test: str = "EuroNCAP-2024-F56-ODB",
        physical_test: str = "PHYS-2024-F56-ODB-03",
    ) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        # Step 1: Thinking — discovering curves
        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(
                type="thinking",
                title="Discovering curves",
                content=(
                    f"Querying the simulation database for test {simulation_test} "
                    f"and the physical test lab for {physical_test}. "
                    "Identifying available sensor channels: chest deflection, "
                    "head acceleration, femur load, neck moment."
                ),
            )
        ):
            curves = await discover_curves()
            logger.info("Discovered curves", **curves)

        # Step 2: Thinking — analyzing curves
        async with workflows.task_from(
            state=workflows_mistralai.ChatAssistantWorkingTask(
                type="thinking",
                title="Analyzing curves",
                content=(
                    "Computing CORA scores (corridor, phase, magnitude) between matched "
                    "simulation/physical curve pairs. Running peak detection, time-shift "
                    "analysis, and energy-based deviation metrics."
                ),
            )
        ):
            correlation = await analyze_correlation()
            logger.info("Analyzed correlation", **correlation)

        # Step 3: Assistant message — rich UI report
        report = Column(
            gap="md",
            children=[
                # Summary card with badges
                Card(
                    title="Overall Correlation Summary",
                    padding="md",
                    children=[
                        Row(
                            gap="md",
                            alignment="center",
                            children=[
                                Markdown(
                                    content=(
                                        f"**Global CORA Score:** {correlation['global_cora_score']} · "
                                        f"**Matched pairs:** {correlation['matched_pairs']}/12 · "
                                        f"**Deviations:** {correlation['deviations_above_threshold']} "
                                        "channels above threshold"
                                    ),
                                ),
                                Tooltip(
                                    trigger="Channels exceeding the 15% CORA deviation threshold",
                                    children=[
                                        Badge(
                                            variant="warning",
                                            children=[Markdown(content="4 warnings")],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                # Side-by-side line charts
                Row(
                    gap="md",
                    children=[
                        Card(
                            title="Chest Deflection (mm)",
                            padding="sm",
                            children=[
                                Chart(
                                    variant="line",
                                    title="Simulation vs Physical",
                                    xAxis="time_ms",
                                    yAxis=["deflection_mm", "physical_mm"],
                                    data=[
                                        {"time_ms": 0, "deflection_mm": 0, "physical_mm": 0},
                                        {"time_ms": 10, "deflection_mm": 5.2, "physical_mm": 4.8},
                                        {"time_ms": 20, "deflection_mm": 18.4, "physical_mm": 17.1},
                                        {"time_ms": 30, "deflection_mm": 34.7, "physical_mm": 31.9},
                                        {"time_ms": 40, "deflection_mm": 42.1, "physical_mm": 44.8},
                                        {"time_ms": 50, "deflection_mm": 38.6, "physical_mm": 41.2},
                                        {"time_ms": 60, "deflection_mm": 28.3, "physical_mm": 30.5},
                                        {"time_ms": 70, "deflection_mm": 15.1, "physical_mm": 16.8},
                                        {"time_ms": 80, "deflection_mm": 6.4, "physical_mm": 7.2},
                                        {"time_ms": 90, "deflection_mm": 2.1, "physical_mm": 2.8},
                                    ],
                                ),
                            ],
                        ),
                        Card(
                            title="Head Acceleration (g)",
                            padding="sm",
                            children=[
                                Chart(
                                    variant="line",
                                    title="Simulation vs Physical",
                                    xAxis="time_ms",
                                    yAxis=["accel_g", "physical_g"],
                                    data=[
                                        {"time_ms": 0, "accel_g": 0, "physical_g": 0},
                                        {"time_ms": 10, "accel_g": 12, "physical_g": 11},
                                        {"time_ms": 20, "accel_g": 38, "physical_g": 35},
                                        {"time_ms": 30, "accel_g": 62, "physical_g": 71},
                                        {"time_ms": 40, "accel_g": 78, "physical_g": 85},
                                        {"time_ms": 50, "accel_g": 65, "physical_g": 72},
                                        {"time_ms": 60, "accel_g": 41, "physical_g": 48},
                                        {"time_ms": 70, "accel_g": 22, "physical_g": 26},
                                        {"time_ms": 80, "accel_g": 8, "physical_g": 10},
                                        {"time_ms": 90, "accel_g": 2, "physical_g": 3},
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                # CORA scores bar chart
                Card(
                    title="CORA Scores by Channel",
                    padding="md",
                    children=[
                        Chart(
                            variant="bar",
                            xAxis="channel",
                            yAxis="score",
                            yMin=0,
                            yMax=1,
                            data=[
                                {"channel": "Chest Defl.", "score": 0.91},
                                {"channel": "Head Accel.", "score": 0.74},
                                {"channel": "Femur L", "score": 0.88},
                                {"channel": "Femur R", "score": 0.85},
                                {"channel": "Neck Fx", "score": 0.72},
                                {"channel": "Neck Mz", "score": 0.79},
                            ],
                        ),
                    ],
                ),
                # Deviations alert
                Alert(
                    title="Deviations Detected",
                    variant="warning",
                    children=[
                        Markdown(
                            content=(
                                "**Head Acceleration** — Peak shifted +3ms, magnitude +9.0% "
                                "above corridor at t=40ms\n\n"
                                "**Neck Fx** — Phase offset detected (CORA phase = 0.68), "
                                "possible sensor mounting difference\n\n"
                                "**Neck Mz** — Magnitude deviation at rebound phase (t=55-70ms), "
                                "simulation under-predicts by 12%\n\n"
                                "**Head Accel.** — HIC15 value: simulation 412 vs physical 478 "
                                "(delta: 13.8%)"
                            ),
                        ),
                    ],
                ),
                # Detailed results table
                Card(
                    title="Detailed Results",
                    padding="md",
                    children=[
                        Markdown(
                            content=(
                                "| Channel | CORA | Phase | Magnitude | Corridor | Status |\n"
                                "|---------|------|-------|-----------|----------|--------|\n"
                                "| Chest Deflection | 0.91 | 0.94 | 0.89 | 0.90 | Pass |\n"
                                "| Head Acceleration | 0.74 | 0.68 | 0.71 | 0.82 | **Fail** |\n"
                                "| Femur Load (L) | 0.88 | 0.91 | 0.85 | 0.87 | Pass |\n"
                                "| Femur Load (R) | 0.85 | 0.88 | 0.82 | 0.86 | Pass |\n"
                                "| Neck Force Fx | 0.72 | 0.68 | 0.75 | 0.74 | **Fail** |\n"
                                "| Neck Moment Mz | 0.79 | 0.82 | 0.74 | 0.80 | **Fail** |"
                            ),
                        ),
                    ],
                ),
            ],
        )

        await workflows_mistralai.send_assistant_message(
            [
                workflows_mistralai.TextOutput(
                    text=f"Here is the correlation report for **{simulation_test}** "
                    f"(simulation) vs **{physical_test}** (physical test).",
                ),
                workflows_mistralai.ResourceOutput(
                    resource=workflows_mistralai.UIComponentResource(component=report),
                ),
            ]
        )

        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[
                workflows_mistralai.ResourceOutput(
                    resource=workflows_mistralai.UIComponentResource(component=report),
                ),
            ],
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([CurveAnalysisWorkflow]))
