import datetime as dt
from statistics import mean
from unittest.mock import MagicMock, patch

from pytz import utc

from django.test import TestCase
from django.utils.timezone import now

from taskmonitor.core import cached_reports
from taskmonitor.models import TaskLog

from ..factories import TaskLogFactory, fake_apps

MODULE_PATH = "taskmonitor.core.cached_reports"


@patch(MODULE_PATH + ".cache")
class TestCachedReports(TestCase):
    class DummyReport(cached_reports._CachedReport):
        def _calc_data(self):
            return "not cached"

    def test_should_create_obj(self, mock):
        # when
        obj = self.DummyReport()
        # then
        self.assertEqual(obj.name, "dummy_report")
        self.assertIn("tasklog", obj.changelist_url())

    def test_should_return_data_from_cache(self, mock_cache):
        # given
        mock_cache.get_or_set.return_value = "cached"
        report = self.DummyReport()
        # when
        data = report.data()
        # then
        self.assertEqual(data, "cached")

    def test_should_return_data_and_update_cache(self, mock_cache):
        # given
        report = self.DummyReport()
        # when
        data = report.data(use_cache=False)
        # then
        self.assertEqual(data, "not cached")
        self.assertTrue(mock_cache.set.called)


class TestCaseCachedReport(TestCase):
    def setUp(self) -> None:
        cached_reports.clear_cache()


class TestQueueLengthOverTime(TestCaseCachedReport):
    def test_should_create_queue_report(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        TaskLogFactory(
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=30,
        )
        TaskLogFactory(
            received=start_dt + dt.timedelta(seconds=5),
            started=start_dt + dt.timedelta(seconds=5),
            timestamp=start_dt + dt.timedelta(seconds=10),
            current_queue_length=10,
        )
        start_dt += dt.timedelta(minutes=5)
        TaskLogFactory(
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=50,
        )
        TaskLogFactory(
            received=start_dt + dt.timedelta(seconds=5),
            started=start_dt + dt.timedelta(seconds=5),
            timestamp=start_dt + dt.timedelta(seconds=10),
            current_queue_length=30,
        )
        report = cached_reports.QueueLengthOverTime()
        # when
        result = report._calc_data()
        # then
        series = result[0]
        self.assertEqual(series["name"], "length")
        data = series["data"]
        expected = [(1672574400000, 20), (1672574700000, 40)]
        self.assertEqual(data, expected)

    def test_should_work_with_null_values(self):
        # given
        TaskLogFactory(state=TaskLog.State.FAILURE)
        log = TaskLogFactory(state=TaskLog.State.SUCCESS, current_queue_length=None)
        self.assertIsNone(log.current_queue_length)
        report = cached_reports.QueueLengthOverTime()
        # when
        report._calc_data()

    def test_should_work_without_data(self):
        # given
        report = cached_reports.QueueLengthOverTime()
        # when
        report._calc_data()


class TestTruncateMinute(TestCaseCachedReport):
    @staticmethod
    def _make_qs(lst) -> MagicMock:
        m = MagicMock()
        m.values_list.return_value.iterator.return_value = lst
        return m

    def test_should_calc_mean(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        qs = self._make_qs(
            [
                (start_dt, 1),
                (start_dt, 3),
                (start_dt + dt.timedelta(minutes=2), 3),
                (start_dt + dt.timedelta(minutes=1), 3),
                (start_dt + dt.timedelta(minutes=1), 6),
            ]
        )
        # when
        result = cached_reports._CachedReport._truncate_minutes(mean, qs)
        # then
        expected = [(1672574400000, 2), (1672574460000, 4), (1672574520000, 3)]
        self.assertListEqual(result, expected)

    def test_should_calc_sum(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        qs = self._make_qs(
            [
                (start_dt, 1),
                (start_dt, 3),
                (start_dt + dt.timedelta(minutes=1), 3),
                (start_dt + dt.timedelta(minutes=1, seconds=5), 6),
                (start_dt + dt.timedelta(minutes=2), 3),
            ]
        )
        # when
        result = cached_reports._CachedReport._truncate_minutes(sum, qs)
        # then
        expected = [(1672574400000, 4), (1672574460000, 9), (1672574520000, 3)]
        self.assertListEqual(result, expected)

    def test_should_calc_sum_over_5_minutes(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        qs = self._make_qs(
            [
                (start_dt, 1),
                (start_dt, 3),
                (start_dt + dt.timedelta(minutes=1), 3),
                (start_dt + dt.timedelta(minutes=1, seconds=5), 6),
                (start_dt + dt.timedelta(minutes=6), 3),
            ]
        )
        # when
        result = cached_reports._CachedReport._truncate_minutes(sum, qs, 5)
        # then
        expected = [(1672574400000, 13), (1672574700000, 3)]
        self.assertListEqual(result, expected)


@patch(MODULE_PATH + ".report")
class TestTasksThroughputByApp(TestCaseCachedReport):
    def test_should_calc_with_no_data(self, mock_report):
        # given
        mock_report.return_value.data.return_value = None
        obj = cached_reports.TasksThroughputByApp()
        # when
        result = obj._calc_data()
        # then
        self.assertListEqual(result, [])


class TestExceptionsOverTime(TestCaseCachedReport):
    def test_should_create_report(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        TaskLogFactory(
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=30,
            exception="Bravo",
        )
        TaskLogFactory(
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=30,
            exception="Alpha",
        )
        start_dt += dt.timedelta(minutes=5)
        report = cached_reports.ExceptionsThroughput()
        # when
        result = report._calc_data()
        # then
        self.assertEqual(result[0]["name"], "Alpha")
        self.assertEqual(result[1]["name"], "Bravo")


class TestAppFailuresOverTime(TestCaseCachedReport):
    def test_should_create_report(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        app_1 = fake_apps[0]
        app_2 = fake_apps[1]
        TaskLogFactory(
            app_name=app_1,
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=30,
            exception="Bravo",
            state=TaskLog.State.FAILURE,
        )
        TaskLogFactory(
            app_name=app_1,
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=10),
            current_queue_length=30,
            exception="Alpha",
            state=TaskLog.State.FAILURE,
        )
        TaskLogFactory(
            app_name=app_2,
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=10),
            current_queue_length=30,
            state=TaskLog.State.SUCCESS,
        )
        report = cached_reports.AppFailuresOverTime()
        # when
        result = report._calc_data()
        # then
        apps = {obj["name"] for obj in result}
        self.assertSetEqual(apps, {app_1})


class TestCachedReport2(TestCaseCachedReport):
    """Testing a cached report without mocking the cache."""

    def test_should_create_report(self):
        # given
        start_dt = dt.datetime(2023, 1, 1, 12, 0, tzinfo=utc)
        TaskLogFactory(
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=30,
            exception="Bravo",
            state=TaskLog.State.FAILURE,
        )
        TaskLogFactory(
            received=start_dt,
            started=start_dt,
            timestamp=start_dt + dt.timedelta(seconds=5),
            current_queue_length=30,
            exception="Alpha",
            state=TaskLog.State.FAILURE,
        )
        start_dt += dt.timedelta(minutes=5)
        report = cached_reports.AppFailuresOverTime()
        # when
        result = report.data()
        # then
        self.assertTrue(result)
        self.assertAlmostEqual(
            report.last_update_at(), now(), delta=dt.timedelta(seconds=30)
        )
        self.assertLessEqual(report.last_update_at(), report.next_update_at())
