import os

import pytest

from gqlppy import Parser
from lark import LarkError


@pytest.fixture
def parser() -> Parser:
   return Parser()

def test_parse_gql(parser: Parser) -> None:
   dir = os.path.dirname(__file__)
   with os.scandir(dir) as files:
      for entry in files:
         if entry.name.startswith('gql_') and entry.name.endswith('.gql'):
            production, _, test_id = entry.name[4:-4].rpartition('_')
            positive_test = test_id[0] != 'N'
            assert production in parser.starting_productions, f'The production {production} is not in the parser.'
            with open(entry.path,'r') as gql_syntax:
               try:
                  parser.parse(gql_syntax,production=production)
                  assert positive_test, f'Negative test case {entry.name} passed'
               except LarkError as ex:
                  assert not positive_test, f"Positive test case {entry.name} failed: {ex}"
