from copy import copy
import re
from typing import Union, cast
from lark import Lark, Token, Tree
from lark.lexer import TerminalDef
from lark.grammar import NonTerminal, Terminal

def log(msg: str = None, debug: bool = False, depth: int = 0):
    if not msg:
        print()
        return

    if debug:
        print(depth * '  ' + msg)

class GNode:
    def __init__(self, name: str, token: Token = None, choices: list[int] = []):
        self.name = name
        self.token = token
        self.choices = choices

    def __eq__(self, other: 'GNode'):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        n = self.name if self.name else f'{self.token}'
        if self.choices:
            n = f'{n}-{"-".join([f"{c}" for c in self.choices])}'

        return n

    def pname(self):
        return self.name if self.name else f'{self.token}'

    def choice(self, depth: int):
        if depth < len(self.choices):
            return self.choices[depth]

        return -1

    def drop_last_choice(self):
        new_node = copy(self)
        new_node.choices = self.choices[:-1]

        return new_node

    def parse(s: str):
        name_n_choices = s.split('-')
        choices = []
        if len(name_n_choices) > 1:
            choices = {int(k) for k in name_n_choices[1:]}

        return GNode(name_n_choices[0], choices=choices)

    def add_choice(self, choice: int):
        self.choices.append(choice)

class GPath:
    def __init__(self, nodes: list[GNode], complete: bool):
        self.nodes = nodes
        self.complete = complete

    def __eq__(self, other: 'GPath'):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        r = '.'.join([f'{p}' for p in self.nodes])

        return r

    def token(self):
        return self.nodes[-1] if self.nodes else GNode(None, choices={})

    def append(self, node):
        new_path = copy(self)
        nodes = []
        for n in self.nodes:
            n1 = copy(n)
            ss = []
            for k in n.choices:
                ss.append(k)
            n1.choices = ss
            nodes.append(n1)
        nodes.append(node)
        new_path.nodes = nodes

        return new_path

    def drop_last(self):
        new_path = copy(self)
        nodes = []
        for n in self.nodes[:-1]:
            nodes.append(n)

        new_path.nodes = nodes

        return new_path

    def clone(self):
        new_path = copy(self)
        nodes = []
        for n in self.nodes:
            n1 = copy(n)
            ss = []
            for k in n.choices:
                ss.append(k)
            n1.choices = ss
            nodes.append(n1)
        new_path.nodes = nodes

        return new_path

    def terminal(self):
        last_node = self.nodes[-1]
        return last_node.pname()

    def terminals(paths: set['GPath']):
        return ','.join(p.terminal() for p in list(paths))

    def with_new_choice(self, choice: int):
        new_path = self.clone()
        new_path.nodes[-1].add_choice(choice)

        return new_path

    def with_next_choice(self):
        new_path = self.clone()
        new_path.nodes[-1].choices[-1] += 1

        return new_path

    def drop_last_choice(self):
        new_path = self.clone()
        new_path.nodes[-1] = new_path.nodes[-1].drop_last_choice()

        return new_path

    def name_path(self):
        # select_clause-0-2.projection-0-1-0-0.result_expr-1-0.expr-0-0-0-0-1-0.path-0-0.identifier_ref-0-0
        return '.'.join([n.name for n in self.nodes])

class LarkParser:
    show_returns = False

    def __init__(self, grammar: str = None, contexts_by_path: dict[str, str] = {}):
        if not grammar:
            grammar = """
                start: expression
                expression: term (("+" | "-") term)*
                term: factor (("*" | "/") factor)*
                factor: NUMBER | "(" expression ")"
                NUMBER: /[0-9]+/
                %ignore " "
            """

        self.contexts_by_path = contexts_by_path

        parser = Lark(grammar, start='start')
        self.parser = parser

        self.rules = {rule_def[0]: rule_def[2] for rule_def in parser.grammar.rule_defs}
        self.terminals = {rule_def[0]: rule_def[1] for rule_def in parser.grammar.term_defs}
        self.rules_by_name1 = {rule_def[0]: rule_def[1] for rule_def in parser.grammar.rule_defs}
        self.rules_by_name2 = {rule_def[0]: rule_def[3] for rule_def in parser.grammar.rule_defs}

        self.trees: dict[str, Tree] = {}
        self._token_values_by_type: dict[str, str] = {}

    def find_next_terminals(self, path: GPath, debug=False):
        if path == 'start':
            return self.visit_current(LarkParser.build_path(path), debug=debug)

        if isinstance(path, set):
            paths = set()

            for p in list(path):
                paths |= self.visit_next(p, debug=debug)

            return paths
        elif isinstance(path, str):
            path = LarkParser.build_path(path)

        if debug: print(f'find_next_terminals({path}, {path.token().token})')

        return self.visit_next(path, debug=debug)

    def visit_current(self, path: GPath, tree: Tree = None, debug=False):
        paths: set[GPath] = set()

        if debug: print(f'visit_current({path}, {path.token().token}), {path.nodes[-1].choices}')
        if not tree:
            tree, _ = self.tree_by_choices(path, debug=debug)

        if isinstance(tree, Token):
            if debug: print('token', tree)
            if path.nodes[-1].token:
                path = path.drop_last()

            p = path.append(GNode(name=self.token_type_from_raw(f'{tree}'), token=tree, choices=[]))
            if LarkParser.show_returns: print('<- ', tree.value, '\t\t', p)
            paths.add(p)
        elif isinstance(tree, Terminal):
            if debug: print('terminal', tree.name)
            p = path.append(GNode(tree.name, choices=[]))
            if LarkParser.show_returns: print('<- ', tree.name, '\t\t', p)
            paths.add(p)
        elif isinstance(tree, NonTerminal):
            if debug: print('non-termial', tree.name, tree)
            paths |= self.visit_current(path.append(GNode(tree.name, choices=[])), debug=debug)
        elif isinstance(tree, tuple):
            paths |= self.visit_current(path, tree=tree[0], debug=debug)
        elif not tree:
            raise Exception(f'null tree at {path}')
        elif tree.data == 'expr':
            if debug: print('expr')
            paths |= self.visit_current(path.with_new_choice(0), tree=tree.children[0], debug=debug)

            if cast(Token, tree.children[1]).value in ['*', '?']:
                paths |= self.visit_next(path, debug=debug)
        elif tree.data == 'maybe':
            if debug: print('maybe')

            paths |= self.visit_current(path.with_new_choice(0), tree=tree.children[0], debug=debug)
            paths |= self.visit_next(path, debug=debug)
        elif tree.data == 'value':
            if debug: print('value')
            for child in tree.children:
                paths |= self.visit_current(path, tree=child, debug=debug)
        elif tree.data == 'range':
            if debug: print('range')
            token0: Token = tree.children[0]
            token1: Token = tree.children[1]
            if token0.value == '"0"' and token1.value == '"9"':
                p = path.append(GNode(name=self.token_type_from_raw(f'{token0}'), token=token0, choices=[]))
                if LarkParser.show_returns: print('<- ', token0, '\t\t', p)
                paths.add(p)
            else:
                raise Exception('not implented')
        elif tree.data == 'literal':
            if debug: print('literal')
            for child in tree.children:
                paths |= self.visit_current(path, tree=child, debug=debug)
        elif tree.data == 'expansions':
            for i, child in enumerate(tree.children):
                paths |= self.visit_current(path.with_new_choice(i), tree=child, debug=debug)
        elif tree.data == 'expansion':
            paths |= self.visit_current(path.with_new_choice(0), tree=tree.children[0], debug=debug)
        elif tree.data == 'alias':
            paths |= self.visit_current(path, tree=tree.children[0], debug=debug)

        return paths

    def visit_next(self, path: GPath, debug=False):
        paths: set[GPath] = set()

        if not path.nodes:
            return paths

        path = self.strip_terminal_nodes(path)
        node = path.nodes[-1]

        me: Tree
        parent: Tree
        me, parent = self.tree_by_choices(path)

        check_parent = True
        if isinstance(me, Tree) and me.data == 'expr' and me.children[1] in ['*', '+']:
            if debug: print('  add expr repeat       ', path)
            paths |= self.visit_current(path.with_new_choice(0), debug=debug)
        elif isinstance(me, Tree) and me.data == 'maybe':
            if debug: print('  add maybe repeat       ', path)
            paths |= self.visit_current(path.with_new_choice(0), debug=debug)

        if isinstance(parent, Tree) and parent.data == 'expansion' and (node.choices[-1] + 1) < len(parent.children):
            np = path.with_next_choice()
            if debug: print('  move to next sibling  ', np)
            paths |= self.visit_current(np, debug=debug)
            check_parent = False

        if check_parent:
            if len(node.choices) > 0:
                p = path.drop_last_choice()
                if debug: print('  move up to parent tree', p)
                paths |= self.visit_next(p, debug=debug)
            else:
                path = path.drop_last()
                if debug: print('  move up to parent node', path)
                paths |= self.visit_next(path, debug=debug)

        return paths

    def tree_by_choices(self, path: GPath, debug=False):
        debug = False

        c = f'{path.nodes[-1]}'
        p = f'{path.nodes[-1].drop_last_choice()}'
        if c not in self.trees:
            for key, value in self.trees_by_choices(path, debug=debug).items():
                if not key:
                    self.trees[f'{path.token().name}'] = value
                else:
                    self.trees[f'{path.token().name}-{key}'] = value

        return self.trees[c], self.trees[p]

    def trees_by_choices(self, path_or_tree: Union[GPath, Tree], choices: list[int] = [], depth: int = 0, debug=False):
        if debug: print(f'trees_by_choices({path_or_tree}, {choices})')

        if isinstance(path_or_tree, GPath):
            n = self.find_last_rule(path_or_tree)
            tree = self.rules[n.name]
        else:
            tree = path_or_tree

        trees: dict[str, Tree] = {}

        if isinstance(tree, Token):
            if debug: log('tree', debug, depth)
            pass
        elif isinstance(tree, Terminal):
            if debug: log('terminal', debug, depth)

            choices_str = '-'.join([f"{c}" for c in choices])
            trees[choices_str] = tree

            pass
        elif isinstance(tree, NonTerminal):
            if debug: log('non-terminal', debug, depth)
            pass
        elif isinstance(tree, tuple):
            if debug: log('tuple', debug, depth)
            trees |= self.trees_by_choices(tree[0], choices, depth=depth, debug=debug)
        elif tree.data in ['expr', 'maybe']:
            if debug: log('expr', debug, depth)
            choices_str = '-'.join([f"{c}" for c in choices])
            trees[choices_str] = tree

            for child in tree.children[:1]:
                trees |= self.trees_by_choices(child, choices + [0], depth=depth+1, debug=debug)
        elif tree.data == 'value':
            if debug: log('value', debug, depth)

            choices_str = '-'.join([f"{c}" for c in choices])
            trees[choices_str] = tree

            for child in tree.children:
                trees |= self.trees_by_choices(child, choices, depth=depth+1, debug=debug)
        elif tree.data == 'literal':
            if debug: log('literal', debug, depth)

            choices_str = '-'.join([f"{c}" for c in choices])
            trees[choices_str] = tree

            for child in tree.children:
                trees |= self.trees_by_choices(child, choices, depth=depth+1, debug=debug)
        elif tree.data == 'expansions':
            if debug: log('expansions', debug, depth)

            choices_str = '-'.join([f"{c}" for c in choices])
            trees[choices_str] = tree
            for i, child in enumerate(tree.children):
                trees |= self.trees_by_choices(child, choices + [i], depth=depth+1, debug=debug)
        elif tree.data == 'expansion':
            if debug: log('expansion', debug, depth)

            choices_str = '-'.join([f"{c}" for c in choices])
            trees[choices_str] = tree
            for i, child in enumerate(tree.children):
                trees |= self.trees_by_choices(child, choices + [i], depth=depth+1, debug=debug)
        elif tree.data == 'alias':
            if debug: log('alias', debug, depth)
            trees |= self.trees_by_choices(tree.children[0], choices, depth=depth, debug=debug)
        else:
            if debug: log('else', debug, depth)

        return trees

    def strip_terminal_nodes(self, path: GPath):
        while path.nodes[-1].name not in self.rules:
            path = path.drop_last()

        return path

    def non_terminal_node_name_path(self, path: GPath):
        return self.strip_terminal_nodes(path).name_path()

    def find_last_rule(self, path: GPath):
        for n in reversed(path.nodes):
            if n.name in self.rules:
                return n

        return None

    def build_path(p: str):
        nodes = []
        for n in p.split('.'):
            name_n_choices = n.split('-')
            nodes.append(GNode(name_n_choices[0], choices=[int(c) for c in name_n_choices[1:]]))

        return GPath(nodes, False)

    def token_type_for_value(self, token):
        for t in reversed(self.parser.terminals):
            td: TerminalDef = t
            td_value = td.pattern.raw
            if td.pattern.type == 'str':
                lower = False
                if td_value.endswith('i'):
                    td_value = td_value[:-1]
                    if len(td_value) > 1 and td_value.startswith('"') and td_value.endswith('"'):
                        td_value = td_value[1:-1].lower()
                        lower = True
                elif len(td_value) > 1 and td_value.startswith('"') and td_value.endswith('"'):
                    td_value = td_value[1:-1]
                td_value = td_value.encode('utf-8').decode('unicode-escape')

                t = token
                if lower:
                    t = t.lower()
                if t == td_value:
                    return td.name

        for t in reversed(self.parser.terminals):
            td: TerminalDef = t
            td_value = td.pattern.raw
            if td.pattern.type != 'str' and re.fullmatch(td.pattern.to_regexp(), token):
                return td.name

        raise Exception('cannot resolve string to a token')

    def token_type_from_raw(self, raw_token):
        td: TerminalDef = None
        for t in reversed(self.parser.terminals):
            if t.pattern.raw == raw_token:
                td = t
                return td.name

        return self.token_type_for_value(raw_token.strip('"'))

    def token_value_from_type(self, token_type: str):
        value = None

        # print('token_value', token_name)

        if not self._token_values_by_type:
            for t in self.parser.terminals:
                td: TerminalDef = t
                if td.pattern.type == 'str':
                    value = td.pattern.raw
                    if value.endswith('i'):
                        value = value[:-1]
                        if len(value) > 1 and value.startswith('"') and value.endswith('"'):
                            value = value[1:-1].lower()
                    elif len(value) > 1 and value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]

                    value = value.encode('utf-8').decode('unicode-escape')
                elif td.pattern.type == 're' and td.pattern.value == '[0-9]':
                    value = '`DIGIT'
                else:
                    value = f'`{td.name}'

                self._token_values_by_type[td.name] = value

        return self._token_values_by_type[token_type]

    def next_terminals(self, s: str, debug=False, print_terminals=False, context: dict[any, any] = {}):
        terminals = set()

        ps = 'start'
        ps = self.find_next_terminals(ps, debug=debug)
        ps0: set[GPath] = None
        last_id_value = None

        state: str = ''

        def emit(ps: set[GPath], token_type: str, token_value: str):
            ps0 = ps
            ps = self.choose(ps, token_type, token_value)
            ps = self.find_next_terminals(ps, debug=debug)

            return ps0, ps

        token_type_for_a = self.token_type_for_value('a')
        token_type: str = None
        for token in self.parser.lex(s):
            token_type = token.type
            if token_type not in ['IDENTIFIER']:
                token_type = self.token_type_for_value(token)

            if state == '':
                if token_type == 'QUOTE':
                    state = 'quote'
                elif token_type == 'DBLQUOTE':
                    state = 'dblquote'
            elif state == 'quote':
                if token_type == 'QUOTE':
                    state = 'quote_in_quote'
            elif state == 'dblquote':
                if token_type == 'DBLQUOTE':
                    state = 'dblquote_in_dblquote'
            elif state == 'quote_in_quote':
                if token_type == 'QUOTE':
                    token_type = token_type_for_a
                    state = 'quote'
                else:
                    ps0, ps = emit(ps, 'QUOTE', '\'')
                    state = ''
            elif state == 'dblquote_in_dblquote':
                if token_type == 'DBLQUOTE':
                    token_type = token_type_for_a
                    state = 'dblquote'
                else:
                    ps0, ps = emit(ps, 'DBLQUOTE', '"')
                    state = ''

            # inside quotes, a word comes back as an IDENTIFIER while escaped quote comes back as their specific anonymous terminals
            if token_type == 'IDENTIFIER' and state in ['quote', 'dblquote']:
                for t1 in token:
                    token_type1 = self.token_type_for_value(t1)

                    ps0, ps = emit(ps, token_type1, t1)
            elif state not in ['quote_in_quote', 'dblquote_in_dblquote']:
                ps0, ps = emit(ps, token_type, token)

            if token_type == 'IDENTIFIER':
                last_id_value = token.value
                context['last-id'] = last_id_value

        # emit left-overs
        if state == 'quote_in_quote':
            ps0, ps = emit(ps, 'QUOTE', '\'')
            state = ''
        elif state == 'dblquote_in_dblquote':
            ps0, ps = emit(ps, 'DBLQUOTE', '"')
            state = ''

        if token_type:
            last_value: str = self.token_value_from_type(token_type)
            if not s.endswith(' ') and self.isalpha(last_value):
                ps = ps0

        for p in ps:
            name_path = self.non_terminal_node_name_path(p)

            translated = False
            for k, v in self.contexts_by_path.items():
                if k in name_path:
                    translated = True
                    terminals.add(f'`{v}')

            if not translated:
                next_value: str = self.token_value_from_type(f'{p.token()}')

                # TODO hack to pass in all hosts to repl completer
                if not s and next_value == '@':
                    terminals.add('`hosts')
                else:
                    terminals.add(next_value)

        if print_terminals:
            print(terminals)

        return terminals

    def isalpha(self, value: str):
        return self.contains_letter(value) or value == '*' or self.is_non_terminal_value(value)

    def is_non_terminal_value(self, value: str):
        return len(value) > 1 and value.startswith('`')

    def contains_letter(self, s):
        return any(c.isalpha() for c in s)

    def parse(self, s: str, debug=False, show_terminals=False):
        ps = 'start'
        ps = self.find_next_terminals(ps, debug=debug)

        for token in self.parser.lex(s):
            token_name = self.token_type_for_value(token)

            ps = self.choose(ps, token_name)
            ps = self.find_next_terminals(ps, debug=debug)

        terminals = {p.terminal().strip('"') for p in ps}

        return terminals

    def choose(self, paths: list[GPath], token_name: str, token_value: str):
        if LarkParser.show_returns: print(f'\n{token_name}({token_value})\t-----------------------------')

        ps = set()
        for p in paths:
            # print('choose', token, 'from', p.token())
            if f'{p.token()}' == token_name:
                ps.add(p)

        return ps