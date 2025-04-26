from unittest import TestCase

from pycarlo.core import Mutation, Query
from tests.test_client import MOCK_GET_USER_QUERY

MOCK_GEN_COLLECTOR_TEMPLATE_MUTATION = """
mutation {
  generateCollectorTemplate {
    dc {
      uuid
    }
  }
}
"""


class OperationTest(TestCase):
    def test_generate_operation(self):
        query = Query()
        query.get_user.__fields__("email")
        self.assertEqual(str(query).strip(), MOCK_GET_USER_QUERY.strip())

    def test_generate_mutation(self):
        mutation = Mutation()
        mutation.generate_collector_template().dc.uuid()  # type: ignore

        self.assertEqual(str(mutation).strip(), MOCK_GEN_COLLECTOR_TEMPLATE_MUTATION.strip())
