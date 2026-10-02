import unittest
import uuid

from rentdynamics.client import Client


class ClientTests(unittest.TestCase):
    def test_when_development_is_false_you_get_production_url(self):
        client = Client()
        base_url = client.get_base_url()
        self.assertEqual(base_url, 'https://api.rentdynamics.com')

    def test_when_development_is_false_with_alternate_base_url(self):
        base_url = str(uuid.uuid4())[:20]
        client = Client(base_url=base_url)
        url = client.get_base_url()
        self.assertEqual(url, base_url)

    def test_when_development_is_true_you_get_development_url(self):
        client = Client(development=True)
        base_url = client.get_base_url()
        self.assertEqual(base_url, 'https://api.rentdynamics.dev')

    def test_when_development_is_true_with_alternate_base_url(self):
        base_url = str(uuid.uuid4())[:20]
        client = Client(base_development_url=base_url, development=True)
        url = client.get_base_url()
        self.assertEqual(url, base_url)
