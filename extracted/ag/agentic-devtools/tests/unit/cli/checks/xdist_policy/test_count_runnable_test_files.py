"""Tests for count_runnable_test_files."""

from __future__ import annotations

from agentic_devtools.cli.checks.xdist_policy import count_runnable_test_files


class TestCountRunnableTestFiles:
    """Tests for counting existing test files represented by targets."""

    def test_empty_targets_count_no_files(self, tmp_path):
        assert count_runnable_test_files([], tmp_path) == 0

    def test_counts_unique_test_files_from_files_directories_and_nodeids(self, tmp_path):
        test_dir = tmp_path / "tests"
        nested = test_dir / "nested"
        nested.mkdir(parents=True)
        (test_dir / "test_directory.py").mkdir()
        first = test_dir / "test_first.py"
        second = nested / "test_second.py"
        non_test = test_dir / "helper.py"
        non_matching_suffix = test_dir / "test_notes.txt"
        first.touch()
        second.touch()
        non_test.touch()
        non_matching_suffix.touch()

        assert (
            count_runnable_test_files(
                [
                    str(test_dir),
                    str(first),
                    "tests/nested/test_second.py::test_case",
                    str(non_test),
                    str(non_matching_suffix),
                    "tests/missing.py",
                ],
                tmp_path,
            )
            == 2
        )

    def test_counts_only_matching_files_and_deduplicates_resolved_paths(self, tmp_path, monkeypatch):
        test_file = tmp_path / "test_one.py"
        test_file.touch()

        assert count_runnable_test_files([str(test_file), str(tmp_path / "." / "test_one.py")], tmp_path) == 1
        monkeypatch.chdir(tmp_path)
        assert count_runnable_test_files(["test_one.py"], None) == 1

    def test_threshold_boundary_is_distinct_file_count(self, tmp_path):
        for count in (30, 31):
            test_dir = tmp_path / str(count)
            test_dir.mkdir()
            for index in range(count):
                (test_dir / f"test_{index}.py").touch()

            assert count_runnable_test_files([str(test_dir)], tmp_path) == count
