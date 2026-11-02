"""Tests for ``scaffold_plan_async``."""

from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_plan import scaffold_plan_async


class TestScaffoldPlanAsync:
    """scaffold_plan_async runs scaffold_plan_command in the background."""

    def test_spawns_background_task(self) -> None:
        mock_task = object()
        with (
            patch(
                "agentic_devtools.cli.speckit.scaffold_plan.run_function_in_background",
                return_value=mock_task,
            ) as mock_bg,
            patch("agentic_devtools.cli.speckit.scaffold_plan.print_task_tracking_info") as mock_print,
            patch("sys.argv", ["agdt-speckit-scaffold-plan", "--json"]),
        ):
            scaffold_plan_async()

        mock_bg.assert_called_once_with(
            module_path="agentic_devtools.cli.speckit.scaffold_plan",
            function_name="scaffold_plan_command",
            command_display_name="agdt-speckit-scaffold-plan",
            func_kwargs={"argv": ["--json"]},
        )
        mock_print.assert_called_once_with(mock_task)
