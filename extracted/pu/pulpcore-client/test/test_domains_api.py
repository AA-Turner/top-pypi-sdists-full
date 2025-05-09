# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pulpcore.client.pulpcore.api.domains_api import DomainsApi


class TestDomainsApi(unittest.TestCase):
    """DomainsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = DomainsApi()

    def tearDown(self) -> None:
        pass

    def test_create(self) -> None:
        """Test case for create

        Create a domain
        """
        pass

    def test_delete(self) -> None:
        """Test case for delete

        Delete a domain
        """
        pass

    def test_list(self) -> None:
        """Test case for list

        List domains
        """
        pass

    def test_migrate(self) -> None:
        """Test case for migrate

        Migrate storage backend
        """
        pass

    def test_partial_update(self) -> None:
        """Test case for partial_update

        Update a domain
        """
        pass

    def test_read(self) -> None:
        """Test case for read

        Inspect a domain
        """
        pass

    def test_set_label(self) -> None:
        """Test case for set_label

        Set a label
        """
        pass

    def test_unset_label(self) -> None:
        """Test case for unset_label

        Unset a label
        """
        pass

    def test_update(self) -> None:
        """Test case for update

        Update a domain
        """
        pass


if __name__ == '__main__':
    unittest.main()
