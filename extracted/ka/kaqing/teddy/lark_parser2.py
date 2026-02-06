from copy import copy
from typing import Union
import unittest
from lark import Lark, Token, Tree
from lark.grammar import NonTerminal, Terminal

class GNode:
    def __init__(self, name: str, token: Token = None, choices: dict[int, int] = {}):
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
            # print(self.choices, self.choices_to_list())
            choices = self.choices_to_list()
            n = f'{n}-{"-".join([f"{c}" for c in choices])}'

        return n

    def pname(self):
        return self.name if self.name else f'{self.token}'

    def choice(self, depth: int):
        if depth in self.choices:
            return self.choices[depth]

        return -1

    def set_choice(self, depth: int, choice: int):
        self.choices[depth] = choice

    def choices_to_list(self):
        choices = []

        if self.choices:
            for i in range(0, max(self.choices.keys()) + 1):
                if i in self.choices:
                    choices.append(self.choices[i])
                else:
                    choices.append(0)

        return choices

    def choice_list_to_str(self):
        return '-'.join([f'{c}' for c in self.choices_to_list()[:-1]])

    def choice_list_to_dict(self, choices: list[int]):
        return {i: c for i, c in enumerate(choices)}

    def drop_last(self):
        new_node = copy(self)
        choices = self.choices_to_list()[:-1]
        new_node.choices = self.choice_list_to_dict(choices)

        return new_node

class GPath:
    def __init__(self, nodes: list[GNode], complete: bool, trail: list[str] = []):
        self.nodes = nodes
        self.complete = complete
        self.trail = trail

    def __eq__(self, other: 'GPath'):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return '.'.join([f'{p}' for p in self.nodes])

    def token(self):
        return self.nodes[-1]

    def append(self, node):
        new_path = copy(self)
        nodes = []
        for n in self.nodes:
            n1 = copy(n)
            ss = {}
            for k, v in n.choices.items():
                ss[k] = v
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
            ss = {}
            for k, v in n.choices.items():
                ss[k] = v
            n1.choices = ss
            nodes.append(n1)
        new_path.nodes = nodes

        return new_path

    def terminal(self):
        last_node = self.nodes[-1]
        # print('SEAN', last_node.token.data)
        return last_node.pname()

    def terminals(paths: set['GPath']):
        return ','.join(p.terminal() for p in list(paths))

class CompletePath:
    def __init__(self, path: GPath, complete: False):
        self.path = path
        self.complete = complete

class SeqOrUnion:
    def __init__(self, collection: list, is_seq: bool):
        self.collection = collection
        self.is_seq = is_seq

class LarkParser:
    def __init__(self):
        grammar = """
            start: expression
            expression: term (("+" | "-") term)*
            term: factor (("*" | "/") factor)*
            factor: NUMBER | "(" expression ")"
            NUMBER: /[0-9]+/
            %ignore " "
        """

        parser = Lark(grammar, start='start')

        # print('TEST parsing', parser.parse('(56)'))

        # print(parser.grammar.term_defs)

        for rule in parser.grammar.rule_defs + parser.grammar.term_defs:
            lhv = rule[0]
            # print(f'{lhv} :=')
            # print(rule[1])
            if len(rule) > 2:
                tree = rule[2]
                # print(f'{tree.pretty()}')
                # print(rule[3])

        self.rules = {rule_def[0]: rule_def[2] for rule_def in parser.grammar.rule_defs}
        self.terminals = {rule_def[0]: rule_def[1] for rule_def in parser.grammar.term_defs}
        self.rules_by_name1 = {rule_def[0]: rule_def[1] for rule_def in parser.grammar.rule_defs}
        self.rules_by_name2 = {rule_def[0]: rule_def[3] for rule_def in parser.grammar.rule_defs}

    def children_by_choices(self, tree: Tree, choices: list[int] = [], depth: int = 0):
        children: dict[str, SeqOrUnion] = {}

        if isinstance(tree, Token):
            pass
        elif isinstance(tree, Terminal):
            pass
        elif isinstance(tree, NonTerminal):
            pass
        elif isinstance(tree, tuple):
            children |= self.children_by_choices(tree[0], choices, depth=depth)
        elif tree.data == 'expr':
            for child in tree.children[:1]:
                children |= self.children_by_choices(child, choices, depth=depth)
            # complete = False
        elif tree.data == 'value':
            # print('value')
            for child in tree.children:
                children |= self.children_by_choices(child, choices, depth=depth)
        elif tree.data == 'literal':
            # print('literal')
            for child in tree.children:
                children |= self.children_by_choices(child, choices, depth=depth)
        elif tree.data == 'expansions':
            # print('expansions')
            # print(tree.pretty())
            choices_str = '-'.join([f"{c}" for c in choices])
            children[choices_str] = SeqOrUnion(tree.children, False)
            # print(f'children_by_choices[{choices_str}] = {len(tree.children)}')
            for i, child in enumerate(tree.children):
                children |= self.children_by_choices(child, choices + [i], depth=depth+1)
        elif tree.data == 'expansion':
            # print('expansion')
            # print(tree.pretty())
            choices_str = '-'.join([f"{c}" for c in choices])
            children[choices_str] = SeqOrUnion(tree.children, True)
            # print(f'children_by_choices[{choices_str}] = {len(tree.children)}')
            for i, child in enumerate(tree.children):
                children |= self.children_by_choices(child, choices + [i], depth=depth+1)

        return children

    def find_next_terminals(self, path: GPath, debug=False):
        if path == 'start':
            return self.find_terminals(path, debug=debug)

        if isinstance(path, set):
            paths = set()

            for p in list(path):
                paths |= self.find_next_terminals(p, debug=debug)

            return paths
        elif isinstance(path, str):
            path = LarkParser.build_path(path)

        terminals = self.find_terminals(path, debug=debug)

        next_terminals = set()

        for t in terminals:
            paths = self.find_next(t)
            for path in paths:
                terms = self.find_terminals(path, debug=debug)
                for term in terms:
                    term.trail.append(term.terminal())
                next_terminals |= terms

        return next_terminals

    def _find_next_terminals(self, path: GPath, debug=False):
        # terminals = self.find_terminals(path)

        if isinstance(path, str):
            path = LarkParser.build_path(path)

        next_terminals = set()

        # for t in terminals:
        paths = self.find_next(path)
        for path in paths:
            next_terminals |= self.find_terminals(path, debug=debug)

        return next_terminals

    def find_next(self, path: GPath, depth: int = -1, debug=False):
        paths: set[GPath] = set()

        if not path.nodes:
            return paths

        if depth == -1:
            if debug: print('find_next', path)

        node = path.nodes[-1]
        if node.name in self.rules:
            tree = self.rules[node.name]
        elif node.name in self.terminals:
            tree = self.terminals[node.name]
        else:
            tree = node.token

        choices = node.choices_to_list()
        children = self.children_by_choices(tree)
        # print('children', children)

        if depth == -1:
            depth = len(choices) - 1

        # print(depth, len(choices), len(children[node.choice_list_to_str()]))
        # print(len(choices), len(children))
        check_parent = True
        if children and children[node.choice_list_to_str()].is_seq and choices[depth] + 1 < len(children[node.choice_list_to_str()].collection):
            node.choices[depth] += 1
            if debug: print('  move to next sibling  ', path)
            # print('paths', path.nodes[-1] )
            paths.add(path.clone())
            check_parent = False

            next_sibing = children[node.choice_list_to_str()].collection[node.choices[depth]]
            if next_sibing.data == 'expr':
                paths |=  self.find_next(path, depth, debug=debug)
                check_parent = True

            # print('next_sibling', next_sibing)

        if check_parent:
            if depth > 0:
                new_node = node.drop_last()
                path.nodes[-1] = new_node
                if debug: print('  move up to parent tree', new_node)
                depth -= 1
                paths |=  self.find_next(path, depth, debug=debug)
            else:
                path = path.drop_last()
                if debug: print('  move up to parent node', path)
                paths |= self.find_next(path, -1, debug=debug)

        return paths

    def find_terminals(self, path: GPath, paths: set[GPath] = set(), path_history: set[GNode] = set(), debug=False):
        if isinstance(path, str):
            path = LarkParser.build_path(path)

        if debug: print('find_terminals', path)

        path_history.add(path.nodes[-1])

        paths = self._find_terminals(None, path, debug=debug)

        new_paths = set()
        for p in paths:
            node = p.nodes[-1]
            if node.token:
                # print('found terminal node', node)
                new_paths.add(p)
            else:
                new_paths |= self.find_terminals(p, paths, path_history, debug=debug)

        return new_paths

    def _find_terminals(self, tree: Tree, path: GPath, depth = 0, debug=False):
        paths: set[GPath] = set()
        # complete = False

        node = path.nodes[-1]
        if not tree:
            if node.name in self.rules:
                tree = self.rules[node.name]
            elif node.name in self.terminals:
                tree = self.terminals[node.name]
            else:
                tree = node.token

        # print(tree)

        if isinstance(tree, Token):
            p = path.append(GNode(name=None, token=tree))
            print('<- ', tree.value, '\t\t', p)
            paths.add(p)
        elif isinstance(tree, Terminal):
            paths.add(path.append(GNode(tree.name)))
        elif isinstance(tree, NonTerminal):
            # print('non-termial', tree.name)
            paths.add(path.append(GNode(tree.name)))
        elif isinstance(tree, tuple):
            paths |= self._find_terminals(tree[0], path, depth=depth)
        elif tree.data == 'expr':
            # print('expr')
            for child in tree.children[:1]:
                paths |= self._find_terminals(child, path, depth=depth)
        elif tree.data == 'value':
            # print('value')
            for child in tree.children:
                paths |= self._find_terminals(child, path, depth=depth)
        elif tree.data == 'literal':
            # print('literal')
            for child in tree.children:
                paths |= self._find_terminals(child, path, depth=depth)
        elif tree.data == 'expansions':
            if node.choice(depth) == -1:
                for i, child in enumerate(tree.children):
                    p = path.clone()
                    node = p.nodes[-1]
                    node.set_choice(depth, i)
                    paths |= self._find_terminals(child, p, depth=depth+1)
            else:
                # node.set_choice(depth, node.choice(depth))
                paths |= self._find_terminals(tree.children[node.choice(depth)], path, depth=depth+1)
        elif tree.data == 'expansion':
            # print('expansion', path)
            if (choice := node.choice(depth)) == -1:
                choice = 0

            node.set_choice(depth, choice)
            paths |= self._find_terminals(tree.children[choice], path, depth=depth+1)

        return paths

    def visit(self, path: GPath, paths: set[GPath] = set(), path_history: set[GNode] = set(), next = False):
        if isinstance(path, str):
            print('visit', path)
            path = LarkParser.build_path(path)

        # print('visit', path)
        if path.nodes[-1] in path_history:
            return paths

        path_history.add(path.nodes[-1])

        paths = self.visit_tree(None, path, next=next)

        new_paths = set()
        for p in paths:
            node = p.nodes[-1]
            if node.token:
                # print('found terminal node', node)
                new_paths.add(p)
            else:
                new_paths |= self.visit(p, paths, path_history, next=False)

        return new_paths

    def visit_tree(self, tree: Tree, path: GPath, depth = 0, next = False):
        paths: set[GPath] = set()
        # complete = False

        node = path.nodes[-1]
        if not tree:
            if node.name in self.rules:
                tree = self.rules[node.name]
            elif node.name in self.terminals:
                tree = self.terminals[node.name]
            else:
                tree = node.token

        # print(tree)

        if isinstance(tree, Token):
            p = path.append(GNode(name=None, token=tree))
            print('<- ', tree.value, '\t\t', p)
            paths.add(p)
        elif isinstance(tree, Terminal):
            paths.add(path.append(GNode(tree.name)))
        elif isinstance(tree, NonTerminal):
            # print('non-termial', tree.name)
            paths.add(path.append(GNode(tree.name)))
        elif isinstance(tree, tuple):
            paths |= self.visit_tree(tree[0], path, depth=depth)
        elif tree.data == 'expr':
            # print('SEAN expr', tree.data, tree.children[1])
            # print('expr add extra', path)
            # paths.add(path)
            for child in tree.children[:1]:
                paths |= self.visit_tree(child, path, depth=depth)
            # complete = False
        elif tree.data == 'value':
            # print('value')
            for child in tree.children:
                paths |= self.visit_tree(child, path, depth=depth)
        elif tree.data == 'literal':
            # print('literal')
            for child in tree.children:
                paths |= self.visit_tree(child, path, depth=depth)
        elif tree.data == 'expansions':
            # print('expansions', path)
            if next:
                paths |= self.visit_tree(tree.children[node.choice(depth)], path, depth=depth+1)
            else:
                for i, child in enumerate(tree.children):
                    node.set_choice(depth, i)
                    paths |= self.visit_tree(child, path, depth=depth+1)
        elif tree.data == 'expansion':
            # print('expansion', path)
            if (choice := node.choice(depth)) == -1:
                choice = 0

            node.set_choice(depth, choice)
            paths |= self.visit_tree(tree.children[choice], path, depth=depth+1)

        return paths

    def _find_next(self, path: GPath, paths: set[GPath] = set(), path_history: set[GNode] = set()):
        if isinstance(path, str):
            print('visit_next', path)
            path = LarkParser.build_path(path)

        # print('visit', path)
        paths: set[GPath] = set()

        for i in reversed(range(1, len(path.nodes) + 1)):
            path = GPath(path.nodes[:i], False)
            print('testing path', path)

            complete = False
            next = self.find_tree_next(None, path)
            if next:
                for n in next:
                    print('visiting with next', n)
                    paths |= self.visit(n, paths, set(), next=True)
                    if n.complete:
                        complete = True
                    else:
                        pass
                        # print('SEAN not complete', n)
            # if not complete:
            #     break
            # if next.complete:
            #     print('SEAN complete', next.complete)
            #     continue
            if next and not complete:
                break

            # else:
            #     break

        return paths

    def find_tree_next(self, tree: Tree, path: GPath, depth = 0):
        print('find_tree_next', path, depth)
        paths: set[GPath] = set()
        # complete = False

        node = path.nodes[-1]
        if not tree:
            if node.name in self.rules:
                tree = self.rules[node.name]
            elif node.name in self.terminals:
                tree = self.terminals[node.name]
            else:
                tree = node.token

        if isinstance(tree, Token):
            path.complete = True
            pass
            # print('token found', tree.value)
        elif isinstance(tree, Terminal):
            path.complete = True
            pass
            # paths.add(path.append(GNode(tree.name)))
        elif isinstance(tree, NonTerminal):
            pass
            # print('non-termial', tree.name)
            # paths.add(path.append(GNode(tree.name)))
        elif isinstance(tree, tuple):
            paths |= self.find_tree_next(tree[0], path, depth=depth)
        elif tree.data == 'expr':
            print(" " * depth, 'expr')
            paths.add(path)
            for child in tree.children[:1]:
                paths |= self.find_tree_next(child, path, depth=depth)
            # complete = False
        elif tree.data == 'value':
            print(" " * depth, 'value')
            for child in tree.children:
                paths |= self.find_tree_next(child, path, depth=depth)
        elif tree.data == 'literal':
            print(" " * depth, 'literal')
            for child in tree.children:
                paths |= self.find_tree_next(child, path, depth=depth)
        elif tree.data == 'expansions':
            print(" " * depth, 'expansions')
            child = tree.children[node.choice(depth)]
            path = self.find_tree_next(child, path, depth=depth+1)
            if node.choices[depth] + 1 < len(tree.children):
                node.choices[depth] += 1

            paths |= path

            # for i, child in enumerate(tree.children):
            #     # self.set_next_choice(path.nodes[-1], depth)
            #     paths |= self.visit_tree_next(child, rules, terminals, path, depth=depth+1)
        elif tree.data == 'expansion':
            print(" " * depth, 'expansion')
            child = tree.children[node.choice(depth)]
            if depth < len(node.choices) -1:
                path = self.find_tree_next(child, path, depth=depth+1)
                if node.choices[depth] + 1 < len(tree.children):
                    node.choices[depth] += 1

                paths |= path
            # else:
            #     if len(tree.children) > node.choices[depth] + 1:
            #         node.choices[depth] += 1
            #         if tree.children[node.choices[depth]].data == 'expr':
            #             print('SEAN expr')
            #             # np = path.drop_last()
            #             # print('SEAN next choice', np)
            #             # paths.add(np)
            #             path.complete = True
            #             paths.add(path)

            #         # self.set_next_choice(node, depth)
            #         paths.add(path)


            # print(" " * depth, 'expansion', path)
            # print('SEAN expansion', tree.pretty())
            # if len(tree.children) > node.choices[depth] + 1:
            #     # print('next child found', tree.children, depth)

            #     node.choices[depth] += 1
            #     if tree.children[node.choices[depth]].data == 'expr':
            #         print('SEAN expr')
            #         # np = path.drop_last()
            #         # print('SEAN next choice', np)
            #         # paths.add(np)
            #         path.complete = True
            #         paths.add(path)

            #     # self.set_next_choice(node, depth)
            #     paths.add(path)

            #     # print('SEAN returning', path)

            #     return paths
            # else:
            #     path.complete = True

        # print('returning', paths)
        return paths

    def build_path(p: str):
        nodes = []
        for n in p.split('.'):
            name_n_choices = n.split('-')
            nodes.append(GNode(name_n_choices[0], choices={int(k): int(v) for k, v in enumerate(name_n_choices[1:])}))

        return GPath(nodes, False)