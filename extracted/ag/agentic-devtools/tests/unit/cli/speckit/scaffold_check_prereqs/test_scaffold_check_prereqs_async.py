"""Tests for ``scaffold_check_prereqs_async``."""

from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_check_prereqs import scaffold_check_prereqs_async


class TestScaffoldCheckPrereqsAsync:
    """scaffold_check_prereqs_async runs scaffold_check_prereqs_command in the background."""

    def test_spawns_background_task(self) -> None:
        mock_task = object()
        with (
            patch(
                "agentic_devtools.cli.speckit.scaffold_check_prereqs.run_function_in_background",
                return_value=mock_task,
            ) as mock_bg,
            patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.print_task_tracking_info") as mock_print,
            patch("sys.argv", ["agdt-speckit-scaffold-check-prereqs", "--json"]),
        ):
            scaffold_check_prereqs_async()

        mock_bg.assert_called_once_with(
            module_path="agentic_devtools.cli.speckit.scaffold_check_prereqs",
            function_name="scaffold_check_prereqs_command",
            command_display_name="agdt-speckit-scaffold-check-prereqs",
            func_kwargs={"argv": ["--json"]},
        )
        mock_print.assert_called_once_with(mock_task)
