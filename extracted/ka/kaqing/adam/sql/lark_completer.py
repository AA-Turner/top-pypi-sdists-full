import functools
import os
from typing import Iterable
from prompt_toolkit.completion import CompleteEvent, Completer, Completion, NestedCompleter, WordCompleter
from prompt_toolkit.document import Document

from adam.config import Config
from adam.sql.async_executor import AsyncExecutor
from adam.sql.lark_parser import LarkParser
from adam.utils import debug, log_timing, offload
from adam.utils_repl.appendable_completer import AppendableCompleter
from adam.utils_repl.repl_completer import merge_completions

__all__ = [
    "LarkCompleter",
]

def default_columns(x: list[str]):
    return 'id,x.,y.,z.'.split(',')

class LarkCompleter(Completer, AppendableCompleter):
    SYSTEM = 'system'

    def __init__(self,
                 dml: str = None,
                 expandables: dict = {},
                 variant: str = 'c',

                 name: str = None,
                 options_lambda: callable = None,
                 auto: str = 'lazy',
                 debug = False
    ) -> None:
        self.nested: NestedCompleter = None
        self.options_lambda = options_lambda
        if options_lambda and auto == 'lazy':
            AsyncExecutor.preload(options_lambda, log_key=name)

        self.variant = variant
        self.parser = None
        self.dml = dml
        self.expandables = expandables

        self.display_dict = {}
        self.meta_dict = {}
        self.WORD = None
        self.sentence = False
        self.match_middle = False
        self.pattern = None

        self.debug = debug

        if variant:
            self.parser = LarkCompleter.lark_parser(variant)
            self.preload_lazy_auto_completes()

    def __repr__(self):
        return f"LarkCompleter.{self.variant}"

    def preload_lazy_auto_completes(self):
        for key, value in self.expandables.items():
            if callable(value):
                if self.auto_complete(key) == 'lazy':
                    AsyncExecutor.preload(value, log_key=key)

    def from_lambda(name: str, options_lambda: callable, auto: str = 'lazy'):
        return LarkCompleter(name=name, options_lambda=options_lambda, auto=auto, variant=None)

    @functools.lru_cache()
    def lark_parser(variant: str):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + f"/qingl.lark") as f:
            grammar: str = None
            with log_timing(f'lark.{variant}.file-read'):
                grammar = f.read()

            common_contexts = {
                'cd_command.file_name': 'direct-dirs',
            }

            if variant in ['a', 'c0', 'p0', 'x0']:
                grammar = grammar.replace('start: statement_sequence', f'start: qing_{variant}_statement')
                contexts_by_path = {
                } | common_contexts

                debug(f'* GRAMMAR replaced to start: qing_{variant}_statement')

                return LarkParser(grammar, contexts_by_path)
            elif variant == 'system':
                grammar = grammar.replace('start: statement_sequence', f'start: qing_{variant}_statement')
                contexts_by_path = {
                } | common_contexts

                return LarkParser(grammar, contexts_by_path)

            grammar = grammar.replace('qing_statement: qing_p_statement', f'qing_statement: qing_{variant}_statement')
            debug(f'* GRAMMAR replaced to qing_statement: qing_{variant}_statement')

            bash_contexts = {
                'bash_statement.host_name': 'hosts',
                'bash_statement.bash_command': 'bash-commands',
            }

            contexts_by_path = {
                'describe_keyspace.keyspace_name': 'keyspaces',
                'keyspace_ref.keyspace_path.namespace_ref.identifier_ref': 'tables',
                'preview_table_statement.path.identifier_ref': 'tables',

                'insert_statement.insert_select': 'column-names',
                'update_statement.set_clause.path.identifier_ref': 'column-names',
                'update_statement.where_clause.cond.expr.path.identifier_ref': 'column-names',
                'delete_statement.where_clause.cond.expr.path.identifier_ref': 'column-names',

                'select_clause.projection.result_expr.expr.path.identifier_ref': 'columns',
                'select_from.where_clause.cond.expr.path.identifier_ref': 'columns',
                'select_from.where_clause.cond.expr.logical_term.and_expr.cond.expr.path.identifier_ref': 'columns',
                'select_from.group_by_clause.group_term.expr.path.identifier_ref': 'columns',
                'select_statement.order_by_clause.ordering_term.expr.path.identifier_ref': 'columns',
                'select_from.from_clause.from_terms.join_clause.ansi_join_clause.ansi_join_predicate.expr.path.identifier_ref': 'columns',
                'select_from.from_clause.from_terms.join_clause.ansi_join_clause.ansi_join_predicate.expr.comparison_term.relational_expr.expr.path.identifier_ref': 'columns',

                'select_from.from_clause.from_terms.from_generic.alias.identifier_ref': 'column-aliases',

                'select_statement.limit_clause.expr.literal.nbr.digit': 'limits',
            } | common_contexts

            if variant == 'p':
                contexts_by_path = bash_contexts | contexts_by_path
            elif variant == 'c':
                contexts_by_path = {
                    'export_table.path.identifier_ref': 'tables',
                    'show_column_counts_command.path.identifier_ref': 'tables',
                    'export_statement.export_tables.keyspace_name': 'keyspaces',

                    'alter_tables_statement.properties.property.property_name': 'table-props',
                    'alter_cql_table_statement.properties.property.property_name': 'table-props',
                    'alter_tables_statement.properties.property.property_value.literal': 'table-props-value',
                    'alter_cql_table_statement.properties.property.property_value.literal': 'table-props-value',

                    'select_clause.projection.result_expr.expr.path.identifier_ref': 'columns',
                    'export_statement.export_tables.export_table.column_name_list.column_name': 'columns',

                    'consistency_statement.consistency': 'consistencies',
                    'export_statement.export_to.export_database_type': 'export-database-types',
                    'drop_export_database.export_database_name': 'export-databases',
                    'use_export_db_statement.export_database_name': 'export-databases',
                    'clean_up_export_session_statement.clean_up_export_sessions.export_session_name': 'export-sessions',
                    'show_export_command.export_session_name': 'export-sessions',
                    'import_statement.import_session.export_session_name': 'export-sessions-incomplete',
                    'download_session_statement.export_session_name': 'export-sessions-incomplete',
                } | bash_contexts | contexts_by_path
            elif variant == 'l':
                contexts_by_path = {
                    'add_partition_action.partition_ref.partition_name': 'partition-columns',
                    'show_topn_statement.topn_count': 'topn-counts',
                    'show_topn_statement.topn_type': 'topn-types',
                    'show_topn_statement.topn_window': 'topn-windows'
                } | contexts_by_path
            elif variant == 'x':
                contexts_by_path = {
                    'show_column_counts_command.path.identifier_ref': 'tables',
                    'drop_export_database.export_database_name': 'export-databases',
                    'use_export_db_statement.export_database_name': 'export-databases',
                } | contexts_by_path

                grammar = grammar.replace('select_clause: "SELECT"i hint_comment? projection', 'select_clause: ("SELECT"i | "XELECT"i) hint_comment? projection')

            with offload():
                with open('/tmp/grammar.lark', 'wt') as f:
                    f.write(grammar)

            return LarkParser(grammar, contexts_by_path)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        if not self.nested and self.options_lambda:
            # for lazy completions
            self.nested = NestedCompleter.from_nested_dict(self.options_lambda())

        nested_words = set()

        if self.nested:
            # from NestedCompleter

            # Split document.
            text = document.text_before_cursor.lstrip()
            stripped_len = len(document.text_before_cursor) - len(text)

            # If there is a space, check for the first term, and use a
            # subcompleter.
            if " " in text:
                first_term = text.split()[0]
                completer = self.nested.options.get(first_term)

                # If we have a sub completer, use this for the completions.
                if completer is not None:
                    remaining_text = text[len(first_term) :].lstrip()
                    move_cursor = len(text) - len(remaining_text) + stripped_len

                    new_document = Document(
                        remaining_text,
                        cursor_position=document.cursor_position - move_cursor,
                    )

                    for c in completer.get_completions(new_document, complete_event):
                        nested_words.add(c.text)
                        yield c

            # No space in the input: behave exactly like `WordCompleter`.
            else:
                completer = WordCompleter(
                    list(self.nested.options.keys()), ignore_case=self.nested.ignore_case
                )
                for c in completer.get_completions(document, complete_event):
                    nested_words.add(c.text)
                    yield c

        if self.parser:
            full = document.text_before_cursor
            if self.dml:
                full = self.dml + ' ' + full

            words0 = []
            words1 = []
            context = {}
            for word in self.parser.next_terminals(full, context=context):
                if ex := self.expandable(word):
                    if ex in self.expandables:
                        e = self.expandables[ex]
                        if callable(e):
                            if self.auto_complete(ex) != 'off':
                                ctx = None
                                if 'last-id' in context:
                                    ctx = context['last-id']
                                e = e(ctx)
                                words0.extend(e)
                        else:
                            words0.extend(e)
                else:
                    words1.append(word)
            words = words0 + words1

            word_before_cursor = document.get_word_before_cursor(
                WORD=self.WORD, pattern=self.pattern
            )

            word_before_cursor = word_before_cursor.lower()

            def word_matches(word: str) -> bool:
                return word.lower().startswith(word_before_cursor)

            for word in words:
                if word_matches(word) and word not in nested_words:
                    display = self.display_dict.get(word, word)
                    display_meta = self.meta_dict.get(word, "")
                    yield Completion(
                        word,
                        -len(word_before_cursor),
                        display=display,
                        display_meta=display_meta,
                    )

    def completions_for_nesting(self, dml: str = None):
        if dml:
            return {dml: LarkCompleter(dml, expandables=self.expandables, variant=self.variant)}

        return {
            word.text.lower(): LarkCompleter(word.text, expandables=self.expandables, variant=self.variant)
            for word in self.get_completions(Document(''), None)
        }

    def expandable(self, word: str):
        return word.strip('`') if word.startswith('`') else None

    def append_completions(self, key: str, value: dict[str, any]):
        if isinstance(value, LarkCompleter) and self.variant == value.variant:
            return

        if self.nested:
            self.nested = NestedCompleter.from_nested_dict(merge_completions(self.nested.options, value))
        else:
            self.nested = NestedCompleter.from_nested_dict(value)

    def auto_complete(self, key: str, default = 'lazy'):
        return Config().get(f'auto-complete.{self.variant}.{key}', default=default)