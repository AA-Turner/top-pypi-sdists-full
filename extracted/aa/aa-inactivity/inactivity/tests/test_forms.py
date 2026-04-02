import datetime as dt

from django.test import TestCase
from django.utils.timezone import now

from inactivity.forms import CreateRequestForm

from .factories import LeaveOfAbsenceFactory, UserMainRequestorFactory


class TestForms(TestCase):
    def test_should_create_minimal_form(self):
        # given
        form_data = {"start": now() + dt.timedelta(days=1), "notes": "dummy"}
        user = UserMainRequestorFactory()
        # when
        form = CreateRequestForm(data=form_data, user=user)
        # then
        self.assertTrue(form.is_valid())

    def test_should_not_allow_empty_form(self):
        # given
        form_data = {}
        user = UserMainRequestorFactory()
        # when
        form = CreateRequestForm(data=form_data, user=user)
        # then
        self.assertFalse(form.is_valid())

    def test_should_not_allow_end_before_start(self):
        # given
        form_data = {
            "start": now() + dt.timedelta(days=3),
            "end": now() + dt.timedelta(days=1),
            "notes": "dummy",
        }
        user = UserMainRequestorFactory()
        # when
        form = CreateRequestForm(data=form_data, user=user)
        # then
        self.assertFalse(form.is_valid())

    def test_should_not_allow_start_date_in_the_past(self):
        # given
        user = UserMainRequestorFactory()
        form_data = {
            "start": now() - dt.timedelta(days=3),
            "end": now() + dt.timedelta(days=1),
            "notes": "dummy",
        }
        # when
        form = CreateRequestForm(data=form_data, user=user)
        # then
        self.assertFalse(form.is_valid())


class TestFormsOverlapping(TestCase):
    def setUp(self) -> None:
        self.today = now().date()

    def _some_date(self, delta_days: int):
        return self.today + dt.timedelta(days=delta_days)

    def _create_form(self, start: int, end: int):
        return {
            "start": self._some_date(start),
            "end": self._some_date(end),
            "notes": "dummy",
        }

    def test_should_not_allow_inside_existing(self):
        # given
        loa_request = LeaveOfAbsenceFactory(
            start=self._some_date(1), end=self._some_date(7)
        )
        form_data = self._create_form(2, 3)
        # when
        form = CreateRequestForm(data=form_data, user=loa_request.user)
        # then
        self.assertFalse(form.is_valid())

    def test_should_not_allow_overlap_at_beginning(self):
        # given
        loa_request = LeaveOfAbsenceFactory(
            start=self._some_date(1), end=self._some_date(4)
        )
        form_data = self._create_form(3, 7)
        # when
        form = CreateRequestForm(data=form_data, user=loa_request.user)
        # then
        self.assertFalse(form.is_valid())

    def test_should_not_allow_overlap_at_end(self):
        # given
        loa_request = LeaveOfAbsenceFactory(
            start=self._some_date(3), end=self._some_date(7)
        )
        form_data = self._create_form(1, 4)
        # when
        form = CreateRequestForm(data=form_data, user=loa_request.user)
        # then
        self.assertFalse(form.is_valid())

    def test_should_not_allow_encompassing_existing(self):
        # given
        loa_request = LeaveOfAbsenceFactory(
            start=self._some_date(3), end=self._some_date(4)
        )
        form_data = self._create_form(1, 7)
        # when
        form = CreateRequestForm(data=form_data, user=loa_request.user)
        # then
        self.assertFalse(form.is_valid())

    def test_should_allow_existing_before(self):
        # given
        loa_request = LeaveOfAbsenceFactory(
            start=self._some_date(3), end=self._some_date(4)
        )
        form_data = self._create_form(4, 7)
        # when
        form = CreateRequestForm(data=form_data, user=loa_request.user)
        # then
        self.assertTrue(form.is_valid())

    def test_should_allow_existing_after(self):
        # given
        loa_request = LeaveOfAbsenceFactory(
            start=self._some_date(4), end=self._some_date(7)
        )
        form_data = self._create_form(1, 4)
        # when
        form = CreateRequestForm(data=form_data, user=loa_request.user)
        # then
        self.assertTrue(form.is_valid())

    def test_should_ignore_overlaps_from_other_users(self):
        # given
        current_user = UserMainRequestorFactory()
        LeaveOfAbsenceFactory(start=self._some_date(3), end=self._some_date(5))
        form_data = self._create_form(3, 7)
        # when
        form = CreateRequestForm(data=form_data, user=current_user)
        # then
        self.assertTrue(form.is_valid())
