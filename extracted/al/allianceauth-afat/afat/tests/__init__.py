"""
Initialize the tests
"""

# Standard Library
import socket

# Django
from django.test import TestCase

# Alliance Auth AFAT
from afat.tests.fixtures.load_allianceauth import load_allianceauth


class SocketAccessError(Exception):
    """
    Error raised when a test script accesses the network
    """


class BaseTestCase(TestCase):
    """
    Variation of Django's TestCase class that prevents any network use.

    Example:

        .. code-block:: python

            class TestMyStuff(BaseTestCase):
                def test_should_do_what_i_need(self): ...

    """

    @classmethod
    def setUpClass(cls):
        """
        Prevent any network access during tests.

        :return:
        :rtype:
        """

        cls.socket_original = socket.socket

        socket.socket = cls.guard

        load_allianceauth()

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Restore network access after tests.

        :return:
        :rtype:
        """

        socket.socket = cls.socket_original

        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        """
        Prevent any network access during tests.

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        raise SocketAccessError("Attempted to access network")
