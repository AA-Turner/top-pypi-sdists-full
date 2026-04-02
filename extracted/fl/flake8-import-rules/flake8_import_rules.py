import argparse
import ast
from os.path import basename, dirname, relpath
from textwrap import dedent

import yaml


__version__ = "1.0.0"


class ConfigError(Exception):
    pass


class LineError(Exception):
    def __init__(self, line):
        self.line = line


def is_any(word):
    return word == "all" or word == "any" or word == "ALL" or word == "ANY"


def add_or_update(the_set, val):
    if isinstance(val, set):
        the_set.update(val)
    else:
        the_set.add(val)


def mod_maches(current: str, rule: str, context: dict):
    variants = rule.split("|")

    def is_var_letter(word):
        return len(word) == 1 and word.isupper()

    variants = [x.strip() for x in variants]

    def_var = None
    def_others = None

    word = variants[0]
    if is_var_letter(word) and word not in context:
        def_var = word
        variants = variants[1:]
        if len(variants) > 0:
            word = variants[0]
            if is_var_letter(word) and word not in context:
                def_others = word
                variants = variants[1:]

    values = set()
    has_any = False
    for v in variants:
        if is_var_letter(v):
            if v in context:
                add_or_update(values, context[v])
            else:
                raise ConfigError("Undefined vairable {v}. Undefined variable can be first or second in expression")
        else:
            if is_any(v):
                has_any = True
            else:
                add_or_update(values, v)
    if len(variants) == 0:
        has_any = True

    if has_any or current in values:
        if def_var is not None:
            context[def_var] = current
        if def_others is not None:
            context[def_others] = values - set([current])

        return True
    return False


def is_fit(current: str, rule: str, context: dict):
    """Check if current module name match to rule module name"""
    clen = len(current)
    rlen = len(rule)
    if is_any(rule):
        return True

    # If match literally
    if current.startswith(rule) and (clen == rlen or clen > rlen and current[rlen] == "."):
        return True

    # Compare parts with variables
    current_parts = current.split(".")
    rule_parts = rule.split(".")

    for i, rule_module in enumerate(rule_parts):
        if i >= len(current_parts):
            return False
        current_module = current_parts[i]
        if not mod_maches(current_module, rule_module, context):
            return False

    return True


def check(src_modname: str, import_modname: str, config: list) -> tuple[bool, str]:
    """
    Args:
        src_modname: module name, where we are checking the imports
        import_modname: import to check
        config: list like
                ("foo", [
                    {"allow": True
                     "name": "bar"},
                     ... ]
                )
    """

    for rule_modname, rules in config:
        context: dict = dict()
        if is_fit(src_modname, rule_modname, context):
            for rule in rules:
                if is_fit(import_modname, rule["name"], context):
                    return rule["allow"], f"{rule_modname} : {rule['name']}"
    return True, ""


def preprocess_rules(rules_string: str):
    """
    Parse loaded rules string and make consequence of rules
    """
    config = list()
    rules_in = yaml.load(rules_string, yaml.Loader)
    if isinstance(rules_in, list):
        for rules_dict in rules_in:
            dest_module = next(iter(rules_dict.keys()))
            module_rules = rules_dict[dest_module]
            rules = list()
            if isinstance(module_rules, str):
                module_rules = [module_rules]
            for line in module_rules:
                try:
                    modname, op = line.split()
                except Exception:
                    raise LineError(line)
                op = op.strip()
                modname = modname.strip()
                if not (op == "allow" or op == "deny"):
                    raise LineError(line)
                rules.append(dict(allow=op == "allow", name=modname))
            config.append((dest_module, rules))
    else:
        raise ConfigError("Config should be a list (all items starts with `-` )")
    return config


class ImportsFinder(ast.NodeVisitor):
    def __init__(self, current_module, config, source):
        self.current_module = current_module
        self.config = config
        self.errors = []
        self.source = source

    def remember_error(self, node, rule_string):
        line = ast.get_source_segment(self.source, node).replace("\n", " ")[:80]
        self.errors.append(
            (
                node.lineno,
                node.col_offset,
                f"I013 denied import: {line}. Rule: {rule_string}",
            )
        )

    def visit_Import(self, node):
        for alias in node.names:
            checked, rule_string = check(self.current_module, alias.name, self.config)
            if not checked:
                self.remember_error(node, rule_string)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        base = []
        if node.module is not None:
            base.append(node.module)
        if node.level > 0:
            # Handle .mod and ..mod imports
            base = self.current_module.split(".")[: -node.level] + base
        checked, rule_string = check(self.current_module, ".".join(base), self.config)
        if not checked:
            self.remember_error(node, rule_string)
        self.generic_visit(node)


class ImportRulesChecker(object):
    options = None
    name = "flake8-import-rules"
    version = __version__

    def __init__(self, tree, filename, lines):
        self.tree = tree
        self.filename = filename
        self.modname = dirname(relpath(filename)).replace("/", ".") + "." + basename(filename)[:-3]
        self.source = "".join(lines)
        self.config = ImportRulesChecker.config

    @classmethod
    def raise_error(cls, line):
        format_string = "Format of rule: [module_name | any] [allow | deny]"
        raise ConfigError(f"Wrong format at: {line}\n{format_string}")

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            "--import-rules",
            parse_from_config=True,
            help="Import rules for flake8-import-rules plugin",
        )

    @classmethod
    def parse_options(cls, options):
        cls.config = None
        if options.import_rules:
            try:
                cls.config = preprocess_rules(options.import_rules)
            except LineError as e:
                cls.raise_error(e.line)

    def run(self):
        if self.config:
            finder = ImportsFinder(self.modname, self.config, self.source)
            finder.visit(self.tree)
            for a, b, c in finder.errors:
                yield (a, b, c, ImportRulesChecker)
