"""Tests for project_schedule FlowMutator."""

import pytest
from obproject.project_schedule import (
    project_schedule,
    ProjectScheduleException,
)


# -- Mock for MutableFlow --


class MockMutableFlow:
    ERROR = "error"

    def __init__(self, project_config, project_spec=None):
        self._configs = {
            "project_config": project_config,
            "project_spec": project_spec or {},
        }
        self.added_decorators = []

    @property
    def configs(self):
        return self._configs.items()

    def add_decorator(self, name, deco_kwargs=None, duplicates=None):
        self.added_decorators.append((name, deco_kwargs, duplicates))


# -- Helpers --


def make_mutator(schedule_map):
    """Create a project_schedule instance with the given schedule_map."""
    ps = project_schedule.__new__(project_schedule)
    ps._args = (schedule_map,)
    ps._kwargs = {}
    ps._flow_cls = None
    ps.statically_defined = True
    ps.inserted_by = None
    ps.init(schedule_map)
    return ps


# -- Validation tests --


class TestInit:
    def test_rejects_non_dict(self):
        with pytest.raises(ProjectScheduleException, match="expects a dict"):
            make_mutator("daily")

    def test_rejects_empty_dict(self):
        with pytest.raises(ProjectScheduleException, match="cannot be empty"):
            make_mutator({})

    def test_rejects_non_dict_spec_value(self):
        with pytest.raises(ProjectScheduleException, match="must be a dict"):
            make_mutator({"main": "daily"})

    def test_rejects_invalid_schedule_keys(self):
        with pytest.raises(ProjectScheduleException, match="Invalid schedule keys"):
            make_mutator({"main": {"cron": "0 * * * *", "bogus": True}})

    def test_accepts_valid_schedule_map(self):
        ps = make_mutator({
            "main": {"cron": "0 8 * * 1-5", "timezone": "America/New_York"},
            "develop": {"daily": True},
            "release/*": {"hourly": True},
        })
        assert ps.schedule_map == {
            "main": {"cron": "0 8 * * 1-5", "timezone": "America/New_York"},
            "develop": {"daily": True},
            "release/*": {"hourly": True},
        }

    def test_accepts_empty_spec_dict(self):
        ps = make_mutator({"main": {}})
        assert ps.schedule_map == {"main": {}}


# -- Pattern matching tests --


class TestPreMutate:
    def test_exact_match(self):
        ps = make_mutator({"main": {"daily": True}})
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={"branch": "main"},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 1
        name, kwargs, dup = mf.added_decorators[0]
        assert name == "schedule"
        assert kwargs == {"daily": True}
        assert dup == MockMutableFlow.ERROR

    def test_glob_match(self):
        ps = make_mutator({"release/*": {"hourly": True}})
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={"branch": "release/v2"},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 1
        assert mf.added_decorators[0][1] == {"hourly": True}

    def test_no_match_is_noop(self):
        ps = make_mutator({"main": {"daily": True}})
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={"branch": "feature/x"},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 0

    def test_first_match_wins(self):
        ps = make_mutator({
            "*": {"weekly": True},
            "main": {"daily": True},
        })
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={"branch": "main"},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 1
        assert mf.added_decorators[0][1] == {"weekly": True}

    def test_missing_branch_is_noop(self):
        ps = make_mutator({"main": {"daily": True}})
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 0

    def test_branch_from_project_spec_nested(self):
        ps = make_mutator({"main": {"daily": True}})
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={"spec": {"project_branch": "main"}},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 1

    def test_branch_from_dev_assets_fallback(self):
        ps = make_mutator({"develop": {"daily": True}})
        mf = MockMutableFlow(
            project_config={"project": "test", "dev-assets": {"branch": "develop"}},
            project_spec={},
        )
        ps.pre_mutate(mf)
        assert len(mf.added_decorators) == 1
        assert mf.added_decorators[0][1] == {"daily": True}

    def test_no_project_config_raises(self):
        ps = make_mutator({"main": {"daily": True}})
        mf = MockMutableFlow(project_config=None)
        # project_config is None but we set it via _configs, need to bypass
        mf._configs["project_config"] = None
        with pytest.raises(ProjectScheduleException, match="only to ProjectFlows"):
            ps.pre_mutate(mf)

    def test_cron_with_timezone(self):
        ps = make_mutator({
            "main": {"cron": "0 8 * * 1-5", "timezone": "America/New_York"},
        })
        mf = MockMutableFlow(
            project_config={"project": "test"},
            project_spec={"branch": "main"},
        )
        ps.pre_mutate(mf)
        assert mf.added_decorators[0][1] == {
            "cron": "0 8 * * 1-5",
            "timezone": "America/New_York",
        }
