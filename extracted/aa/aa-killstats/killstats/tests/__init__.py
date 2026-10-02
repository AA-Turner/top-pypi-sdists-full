# Standard Library
import socket
from unittest.mock import Mock

# Django
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory, TestCase

# Alliance Auth
from allianceauth.authentication.models import User

# AA Killstats
from killstats.tests.testdata.killstats import UserMainFactory


class SocketAccessError(Exception):
    """Error raised when a test script accesses the network"""


class NoSocketsTestCase(TestCase):
    """Variation of Django's TestCase class that prevents any network use.

    Example:

        .. code-block:: python

            class TestMyStuff(BaseTestCase):
                def test_should_do_what_i_need(self): ...

    """

    @classmethod
    def setUpClass(cls):
        cls.socket_original = socket.socket
        socket.socket = cls.guard
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        socket.socket = cls.socket_original
        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        raise SocketAccessError("Attempted to access network")


class AuthTestCase(NoSocketsTestCase):
    """Base test case for authentication-related tests that prevents network access."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Request Factory & Default Request
        cls.factory = RequestFactory()
        cls.request = cls.factory.get("/")

        # User with Standard Access
        cls.user: User = UserMainFactory()

        # User with Superuser Access
        cls.superuser: User = UserMainFactory()
        cls.superuser.is_superuser = True
        cls.superuser.save()

    def setUp(self):
        super().setUp()
        self.request = self.factory.get("/")

    def _middleware_process_request(self, request: WSGIRequest):
        """Helper method to process middleware for a request."""
        session_middleware = SessionMiddleware(Mock())
        session_middleware.process_request(request)
        message_middleware = MessageMiddleware(Mock())
        message_middleware.process_request(request)
