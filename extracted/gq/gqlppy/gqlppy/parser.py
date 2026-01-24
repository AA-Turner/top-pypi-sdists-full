from lark import Lark, Tree, UnexpectedInput
from typing import Callable, IO, Optional, Union

class Parser():
   """A full ISO GQL parser based on a lark grammar derived from the ISO published EBNF.
   """

   def __init__(self, kind: str ='earley', strict: bool=False, starting_productions: list[str] = None, grammar_file: str = None, cache: bool | str = False):
      """Constructs a ISO GQL parser

      Args:
          kind (str, optional): The algorithm for the lark parser. Defaults to 'earley'.
          strict (bool, optional): Enables strict parsing the lark parser. Defaults to False.
          starting_productions (list[str], optional): The list of productions to allow as starting productions. Defaults to ['gql_program','query_specification','create_graph_type_statement']
          grammar_file (str, optional): An alternate grammar file location,
          cache (bool|str, optional): Enable caching - when a string, the value is a file location for the cached grammar
      """
      self._starting_productions = ['gql_program','query_specification','create_graph_type_statement'] if starting_productions is None else starting_productions
      self._parser = Lark.open(
         f'gql-{kind}.lark' if grammar_file is None else grammar_file,
         rel_to=__file__ if grammar_file is None else None,
         start=self._starting_productions,
         parser=kind,
         debug=True,
         strict=strict,
         propagate_positions=True,
         cache=cache
      )

   def parse(self, text : Union[str,IO], production: str='gql_program', on_error: Optional[Callable[[UnexpectedInput], bool]] = None) -> Tree:
      """Parses a text or stream according to the production specified.

      Args:
          text: The input ISO GQL program or syntax - string or IO
          production (str, optional): A starting production grammar. Defaults to 'gql_program'.

      Returns:
          Tree: A lark post-parse tree
      """
      if not isinstance(text,str):
         text = text.read()
      return self._parser.parse(text, start=production, on_error=on_error)

   def parse_query(self, text : Union[str,IO]) -> Tree:
      """A shorthand for parsing with the 'query_specification' grammar production

      Args:
          text: The ISO GQL query to parse - string or IO

      Returns:
          Tree: A lark post-parse tree
      """
      return self.parse(text,production='query_specification')

   def parse_schema(self, text: Union[str,IO]) -> Tree:
      """A shorthand for parsing with the 'create_graph_type_statement' grammar production

      Args:
          text: The ISO GQL query to parse - string or IO

      Returns:
          Tree: A lark post-parse tree
      """

      return self.parse(text,production='create_graph_type_statement')

   @property
   def starting_productions(self) -> list[str]:
      """Returns the configured starting productions."""
      return self._starting_productions.copy()

   @property
   def all_productions(self) -> list[str]:
      """Returns all the grammar productions."""
      return [ rule[0].value for rule in self._parser.grammar.rule_defs]
