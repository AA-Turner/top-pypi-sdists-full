import unittest

from abstra_internals.repositories.linter.rules.job_schedule_validity import (
    JobScheduleValidity,
)
from abstra_internals.repositories.project.project import (
    JobStage,
    LocalProjectRepository,
)
from tests.fixtures import clear_dir, init_dir


class JobScheduleValidityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()
        self.project_repository = LocalProjectRepository()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def _add_job(self, *, id: str, title: str, file: str, schedule: str) -> None:
        project = self.project_repository.load()
        job = JobStage.create(id=id, title=title, file=file)
        job.schedule = schedule
        project.add_stage(job)
        self.project_repository.save(project)

    def test_empty_project_has_no_issues(self):
        rule = JobScheduleValidity()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_schedule_passes(self):
        self._add_job(id="daily", title="Daily", file="daily.py", schedule="0 0 * * *")
        rule = JobScheduleValidity()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_impossible_schedule_is_flagged(self):
        self._add_job(
            id="feb31", title="Feb 31 job", file="feb31.py", schedule="0 0 31 2 *"
        )
        rule = JobScheduleValidity()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        # The job title surfaces in the message so the user knows which job to fix.
        self.assertIn("Feb 31 job", issues[0].label)

    def test_reports_one_issue_per_invalid_job_and_skips_valid_ones(self):
        self._add_job(
            id="feb31", title="Feb 31 job", file="feb31.py", schedule="0 0 31 2 *"
        )
        self._add_job(
            id="apr31", title="Apr 31 job", file="apr31.py", schedule="0 0 31 4 *"
        )
        self._add_job(id="ok", title="OK job", file="ok.py", schedule="0 0 * * *")
        rule = JobScheduleValidity()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 2)


if __name__ == "__main__":
    unittest.main()
