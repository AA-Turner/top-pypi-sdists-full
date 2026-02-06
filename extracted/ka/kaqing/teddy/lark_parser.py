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

class LarkParser:
    show_returns = False

    def __init__(self, grammar: str = None):
        if not grammar:
            grammar = """
                start: expression
                expression: term (("+" | "-") term)*
                term: factor (("*" | "/") factor)*
                factor: NUMBER | "(" expression ")"
                NUMBER: /[0-9]+/
                %ignore " "
            """

        parser = Lark(grammar, start='start')
        self.parser = parser

        self.rules = {rule_def[0]: rule_def[2] for rule_def in parser.grammar.rule_defs}
        self.terminals = {rule_def[0]: rule_def[1] for rule_def in parser.grammar.term_defs}
        self.rules_by_name1 = {rule_def[0]: rule_def[1] for rule_def in parser.grammar.rule_defs}
        self.rules_by_name2 = {rule_def[0]: rule_def[3] for rule_def in parser.grammar.rule_defs}

        self.trees: dict[str, Tree] = {}

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

        if debug: print(f'visit_expansion({path}, {path.token().token}), {path.nodes[-1].choices}')
        if not tree:
            tree, _ = self.tree_by_choices(path, debug=debug)

        if isinstance(tree, Token):
            if debug: print('token', tree)
            if path.nodes[-1].token:
                path = path.drop_last()

            p = path.append(GNode(name=self.token_name_from_raw(f'{tree}'), token=tree, choices=[]))
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
            paths |= self.visit_current(path.with_new_choice(0), tree=tree.children[0], debug=debug)

            if cast(Token, tree.children[1]).value in ['*', '?']:
                paths |= self.visit_next(path, debug=debug)
        elif tree.data == 'value':
            # print('value')
            for child in tree.children:
                paths |= self.visit_current(path, tree=child, debug=debug)
        elif tree.data == 'range':
            # print('range')
            token0: Token = tree.children[0]
            token1: Token = tree.children[1]
            if token0.value == '"0"' and token1.value == '"9"':
                p = path.append(GNode(name=self.token_name_from_raw(f'{token0}'), token=token0, choices=[]))
                if LarkParser.show_returns: print('<- ', 0, '\t\t', p)
                paths.add(p)
            else:
                raise Exception('not implented')
                for i in range(ord(token0.value.strip('"')), ord(token1.value.strip('"')) + 1):
                    ch = chr(i)
                    p = path.append(GNode(name=self.token_name_from_raw(f'{token0}'), token=token0, choices=[]))
                    # p = path.append(GNode(name=self.token_name_from_raw(f'{tree}'), token=tree, choices=[]))
                    if LarkParser.show_returns: print('<- ', ch, '\t\t', p)
                    paths.add(p)
        elif tree.data == 'literal':
            # print('literal')
            for child in tree.children:
                paths |= self.visit_current(path, tree=child, debug=debug)
        elif tree.data == 'expansions':
            for i, child in enumerate(tree.children):
                paths |= self.visit_current(path.with_new_choice(i), tree=child, debug=debug)
        elif tree.data == 'expansion':
            paths |= self.visit_current(path.with_new_choice(0), tree=tree.children[0], debug=debug)

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
        if isinstance(me, Tree) and me.data == 'expr' and me.children[1] == '*':
            if debug: print('  add expr repeat       ', path)
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
        elif tree.data == 'expr':
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
        else:
            if debug: log('else', debug, depth)

        return trees

    def strip_terminal_nodes(self, path: GPath):
        while path.nodes[-1].name not in self.rules:
            path = path.drop_last()

        return path

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

    def token_name(self, token):
        td: TerminalDef = None
        for t in reversed(self.parser.terminals):
            td = t
            # print(td)
            if td.pattern.raw == '/./':
                if token == '.':
                    return td.name
            elif re.fullmatch(td.pattern.to_regexp(), token):
                return td.name

        raise Exception('cannot resolve string to a token')

    def token_name_from_raw(self, raw_token):
        td: TerminalDef = None
        for t in reversed(self.parser.terminals):
            if t.pattern.raw == raw_token:
                td = t
                return td.name

        return self.token_name(raw_token.strip('"'))

    def parse(self, s: str, debug=False):
        ps = 'start'
        ps = self.find_next_terminals(ps, debug=debug)

        for token in self.parser.lex(s):
            token_name = self.token_name(token)

            ps = self.choose(ps, token_name)
            ps = self.find_next_terminals(ps, debug=debug)

        terminals = {p.terminal().strip('"') for p in ps}

        # print(terminals)

        return terminals

    def choose(self, paths: list[GPath], token: str):
        if LarkParser.show_returns: print(f'\n{token}\t-----------------------------')

        ps = set()
        for p in paths:
            if f'{p.token()}' == token:
                ps.add(p)

        return ps