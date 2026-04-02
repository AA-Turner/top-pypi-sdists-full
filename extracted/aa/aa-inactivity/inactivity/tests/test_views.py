import datetime as dt
from http import HTTPStatus
from unittest.mock import patch

from django.test import RequestFactory
from django.urls import reverse
from django.utils.timezone import now

from app_utils.testing import NoSocketsTestCase, json_response_to_python

from inactivity.views import (
    create_loa_request,
    inactive_users,
    inactive_users_data,
    index,
    list_pending_loa_requests,
    manage_requests,
    my_requests,
)

from .factories import (
    InactivityPingFactory,
    LeaveOfAbsenceFactory,
    UserMainManagerFactory,
    UserMainRequestorFactory,
)

MODULE_PATH = "inactivity.views"


class TestViewsAreWorking(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()

    def test_index(self):
        # given
        user = UserMainRequestorFactory()
        request = self.factory.get(reverse("inactivity:index"))
        request.user = user
        # when
        response = index(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("inactivity:my_requests"))

    def test_my_request(self):
        # given
        user = UserMainRequestorFactory()
        request = self.factory.get(reverse("inactivity:my_requests"))
        request.user = user
        # when
        response = my_requests(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_managers_can_manage_requests(self):
        # given
        user = UserMainManagerFactory()
        request = self.factory.get(reverse("inactivity:manage_requests"))
        request.user = user
        # when
        response = manage_requests(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_normal_users_can_not_manage_requests(self):
        # given
        user = UserMainRequestorFactory()
        request = self.factory.get(reverse("inactivity:manage_requests"))
        request.user = user
        # when
        response = manage_requests(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_list_pending_loa_requests(self):
        # given
        user = UserMainManagerFactory()
        request = self.factory.get(reverse("inactivity:list_pending_loa_requests"))
        request.user = user
        LeaveOfAbsenceFactory(is_approved=True)
        LeaveOfAbsenceFactory(
            start=now() - dt.timedelta(days=2), end=now() - dt.timedelta(days=1)
        )
        unapproved_loa = LeaveOfAbsenceFactory(approver=None, end=None)
        # when
        response = list_pending_loa_requests(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json_response_to_python(response)
        pks = {row["pk"] for row in data["data"]}
        self.assertSetEqual(pks, {unapproved_loa.pk})

    def test_inactive_users(self):
        # given
        InactivityPingFactory()
        user = UserMainManagerFactory()
        request = self.factory.get(reverse("inactivity:inactive_users"))
        request.user = user
        # when
        response = inactive_users(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_inactive_users_data(self):
        # given
        user = UserMainManagerFactory()
        request = self.factory.get(reverse("inactivity:inactive_users_data"))
        request.user = user
        ping = InactivityPingFactory()
        # when
        response = inactive_users_data(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json_response_to_python(response)
        pks = {row["pk"] for row in data["data"]}
        self.assertSetEqual(pks, {ping.pk})


@patch(MODULE_PATH + ".messages")
class TestCreateLoa(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()

    def test_should_show_empty_form(self, mock_messages):
        # given
        user = UserMainRequestorFactory()
        request = self.factory.get(reverse("inactivity:create_loa_request"))
        request.user = user
        # when
        response = create_loa_request(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_create_new_request(self, mock_messages):
        # given
        user = UserMainRequestorFactory()
        request = self.factory.post(
            reverse("inactivity:create_loa_request"),
            data={"start": now().date() + dt.timedelta(days=1), "notes": "dummy"},
        )
        request.user = user
        # when
        response = create_loa_request(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(mock_messages.info.called)

    def test_should_report_form_errors(self, mock_messages):
        # given
        user = UserMainRequestorFactory()
        request = self.factory.post(
            reverse("inactivity:create_loa_request"),
            data={"start": now().date() - dt.timedelta(days=1)},
        )
        request.user = user
        # when
        response = create_loa_request(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(mock_messages.info.called)
