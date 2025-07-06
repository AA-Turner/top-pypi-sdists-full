from cnvrgv2 import Project
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.workflows.experiment.experiment import Experiment


class TestExperiment:
    def test_stopped_experiment_restart_attribute(self, empty_context):
        try:
            e = Experiment(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
            e.restart()
        except AttributeError as err:
            assert "'Experiment' object has no attribute 'restart'" in str(err)

    def test_logs_experiment_offset_attribute(self, empty_context):
        try:
            e = Experiment(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
            e.logs(offset="test")
        except CnvrgArgumentsError as err:
            assert "offset: Wrong attribute type, expected int, got <class 'str'>" in str(err)

    def test_logs_experiment_page_attribute(self, empty_context):
        try:
            e = Experiment(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
            e.logs(page="test")
        except CnvrgArgumentsError as err:
            assert "page: Wrong attribute type, expected dict, got <class 'str'>" in str(err)

    def test_create_experiment_parameters_duplicate_key_error(self, empty_context):
        try:
            params = [
                {
                    "key": "",
                    "type": "discrete",
                    "min": 0,
                    "max": 0,
                    "scale": "linear",
                    "steps": 0,
                    "values": [
                        1,
                        2,
                        3,
                    ]
                },
                {
                    "key": "key2",
                    "type": "float",
                    "min": 1,
                    "max": 40,
                    "scale": "linear",
                    "steps": 3,
                    "values": []
                },
            ]
            project = Project(context=empty_context, slug="test-slug")
            project.experiments.create_grid(title="test", command="echo 'test'", parameters=params, sync_before=False)
        except CnvrgArgumentsError as err:
            assert "Key cannot be empty" in str(err)

    def test_create_experiment_parameters_discrete_values_error(self, empty_context):
        try:
            params = [
                {
                    "key": "key1",
                    "type": "discrete",
                    "min": 0,
                    "max": 0,
                    "scale": "linear",
                    "steps": 0,
                    "values": [
                        "1",
                        2,
                        3,
                    ]
                },
                {
                    "key": "key2",
                    "type": "float",
                    "min": 1,
                    "max": 40,
                    "scale": "linear",
                    "steps": 3,
                    "values": []
                },
            ]
            project = Project(context=empty_context, slug="test-slug")
            project.experiments.create_grid(title="test", command="echo 'test'", parameters=params, sync_before=False)
        except CnvrgArgumentsError as err:
            assert "Discrete values may only contain numbers" in str(err)

    def test_create_experiment_parameters_command_missing_error(self, empty_context):
        try:
            params = [
                {
                    "key": "key1",
                    "type": "discrete",
                    "min": 0,
                    "max": 0,
                    "scale": "linear",
                    "steps": 0,
                    "values": [
                        1,
                        2,
                        3,
                    ]
                },
                {
                    "key": "key2",
                    "type": "float",
                    "min": 1,
                    "max": 40,
                    "scale": "linear",
                    "steps": 3,
                    "values": []
                },
            ]
            project = Project(context=empty_context, slug="test-slug")
            project.experiments.create_grid(title="test", parameters=params, sync_before=False)
        except CnvrgArgumentsError as err:
            assert "Command Cannot be blank" in str(err)
