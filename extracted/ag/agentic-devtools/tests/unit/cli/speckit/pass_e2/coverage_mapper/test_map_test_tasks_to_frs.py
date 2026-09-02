"""Tests for pass_e2.coverage_mapper — map_test_tasks_to_frs."""

from agentic_devtools.cli.speckit.pass_e2.coverage_mapper import map_test_tasks_to_frs
from agentic_devtools.cli.speckit.pass_e2.models import FRInfo
from agentic_devtools.cli.speckit.pass_e2.models import TestTask as _TestTask


class TestMapTestTasksToFrs:
    """Verify FR-003 mapping strategies."""

    def test_explicit_fr_refs(self) -> None:
        tasks = [
            _TestTask(
                task_id="T001",
                description="Test FR-001",
                fr_refs=["FR-001"],
                us_labels=[],
                test_types=["unit"],
            )
        ]
        fr_infos = [FRInfo(fr_id="FR-001", priority=1)]
        us_to_fr: dict[int, list[str]] = {}

        fr_to_tasks, unmapped = map_test_tasks_to_frs(tasks, fr_infos, us_to_fr)
        assert len(fr_to_tasks["FR-001"]) == 1
        assert unmapped == []

    def test_us_label_mapping(self) -> None:
        tasks = [
            _TestTask(
                task_id="T001",
                description="Test via US1",
                fr_refs=[],
                us_labels=[1],
                test_types=["unit"],
            )
        ]
        fr_infos = [FRInfo(fr_id="FR-001", priority=1, user_story=1)]
        us_to_fr = {1: ["FR-001"]}

        fr_to_tasks, unmapped = map_test_tasks_to_frs(tasks, fr_infos, us_to_fr)
        assert len(fr_to_tasks["FR-001"]) == 1
        assert unmapped == []

    def test_unmapped_task(self) -> None:
        tasks = [
            _TestTask(
                task_id="T001",
                description="Some test",
                fr_refs=[],
                us_labels=[],
                test_types=["unit"],
            )
        ]
        fr_infos = [FRInfo(fr_id="FR-001", priority=1)]
        us_to_fr: dict[int, list[str]] = {}

        fr_to_tasks, unmapped = map_test_tasks_to_frs(tasks, fr_infos, us_to_fr)
        assert len(fr_to_tasks["FR-001"]) == 0
        assert len(unmapped) == 1

    def test_fr_ref_not_in_fr_infos(self) -> None:
        """Task references an FR not in fr_infos → ref skipped, task still unmapped."""
        tasks = [
            _TestTask(
                task_id="T001",
                description="Test FR-999",
                fr_refs=["FR-999"],
                us_labels=[],
                test_types=["unit"],
            )
        ]
        fr_infos = [FRInfo(fr_id="FR-001", priority=1)]
        us_to_fr: dict[int, list[str]] = {}

        fr_to_tasks, unmapped = map_test_tasks_to_frs(tasks, fr_infos, us_to_fr)
        assert len(fr_to_tasks["FR-001"]) == 0
        assert len(unmapped) == 1

    def test_us_label_exceeds_max_us(self) -> None:
        """Task with US label exceeding max US number → condition false branch."""
        tasks = [
            _TestTask(
                task_id="T001",
                description="Test via US10",
                fr_refs=[],
                us_labels=[10],
                test_types=["unit"],
            )
        ]
        fr_infos = [FRInfo(fr_id="FR-001", priority=1)]
        us_to_fr = {1: ["FR-001"]}

        fr_to_tasks, unmapped = map_test_tasks_to_frs(tasks, fr_infos, us_to_fr)
        assert len(fr_to_tasks["FR-001"]) == 0
        assert len(unmapped) == 1

    def test_us_label_maps_to_unknown_fr(self) -> None:
        """US label maps to an FR not in fr_infos → fr_key not in fr_to_tasks."""
        tasks = [
            _TestTask(
                task_id="T001",
                description="Test via US1",
                fr_refs=[],
                us_labels=[1],
                test_types=["unit"],
            )
        ]
        fr_infos = [FRInfo(fr_id="FR-001", priority=1)]
        # US1 maps to FR-999 which is not in fr_infos
        us_to_fr = {1: ["FR-999"]}

        fr_to_tasks, unmapped = map_test_tasks_to_frs(tasks, fr_infos, us_to_fr)
        assert len(fr_to_tasks["FR-001"]) == 0
        assert len(unmapped) == 1
