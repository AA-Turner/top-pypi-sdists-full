import logging
import re
from dataclasses import dataclass
from functools import partial
from types import MethodType
from typing import Any, Dict, List, Optional, Sequence

from sqlfmt import actions, api
from sqlfmt.analyzer import Analyzer
from sqlfmt.comment import Comment
from sqlfmt.dialect import ClickHouse
from sqlfmt.exception import SqlfmtBracketError
from sqlfmt.jinjafmt import JinjaFormatter, JinjaTag
from sqlfmt.line import Line
from sqlfmt.mode import Mode
from sqlfmt.node import Node, get_previous_token
from sqlfmt.node_manager import NodeManager
from sqlfmt.rule import Rule
from sqlfmt.rules.common import SQL_QUOTED_EXP, group
from sqlfmt.tokens import Token, TokenType

# This class extends and monkey patches https://github.com/tconbeer/sqlfm
INDENT = " " * 4
# This is the default value in tb fmt --diff, let's use the same
DEFAULT_FMT_LINE_LENGTH = 100


@dataclass
class TBLine(Line):
    def render_with_comments(self, max_length: int) -> str:
        # 0.11 counted the trailing newline when deciding whether a comment
        # fits and moved overflowing inline comments above the SQL line.
        if len(self.comments) == 1 and not self.comments[0].is_standalone:
            comment = self.comments[0]
            if len(str(self).rstrip()) + len(comment.render_inline()) >= max_length:
                return comment.render_standalone(max_length - 1, self.prefix) + str(self)
        return super().render_with_comments(max_length - 1)

    @property
    def prefix(self) -> str:
        """
        Returns the whitespace to be printed at the start of this Line for
        proper indentation.

        Tinybird => This is overriden from the base Line because we want SQL inside a template to be indented
        https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/line.py#L92
        """
        return INDENT * (self.depth[0] + self.depth[1])


def from_nodes(
    _cls: type[Line],
    previous_node: Optional[Node],
    nodes: List[Node],
    comments: List[Comment],
) -> Line:
    """
    Creates and returns a new line from a list of Nodes. Useful for line
    splitting and merging.

    Tinybird => Monkey patched to use `TBLine` and our own indentation logic.
    """
    if nodes:
        formatting_disabled = nodes[0].formatting_disabled + nodes[-1].formatting_disabled
    else:
        formatting_disabled = previous_node.formatting_disabled if previous_node is not None else []

    return TBLine(
        previous_node=previous_node,
        nodes=nodes,
        comments=comments,
        formatting_disabled=formatting_disabled,
    )


def _format_jinja_node(self: JinjaFormatter, node: Node, max_length: int) -> bool:
    """
    Format a single jinja tag. No-ops for nodes that
    are not jinja. Returns True if the node was blackened.
    """
    if not node.is_jinja:
        return False

    tag = JinjaTag.from_string(node.value, node.depth)
    if self.use_black and self.code_formatter.black is not None:
        # Monkey patch black to preserve quote style inside Tinybird templates.
        black = self.code_formatter.black
        if not getattr(black, "_tinybird_preserve_string_normalization", False):
            old_format_str = black.format_str

            def format_str(string: str, mode: Any = None) -> str:
                black_mode = black.Mode(
                    line_length=mode.line_length if mode is not None else max_length,
                    string_normalization=False,
                )
                return old_format_str(string, mode=black_mode)

            black.format_str = format_str  # type: ignore[attr-defined]
            black._tinybird_preserve_string_normalization = True  # type: ignore[attr-defined]

    if tag.code and self.use_black:
        tag.code, tag.is_blackened = self.code_formatter.format_string(
            tag.code,
            max_length=tag.max_code_length(max_length),
        )

        if "{%" in node.value:
            parts = tag.code.split("\n")
            prefix = INDENT * (node.depth[0] + node.depth[1])
            if len(parts) > 1:
                tag.code = "\n".join([f"{prefix if i != 0 else ''}{part}" for i, part in enumerate(parts)])

    node.value = str(tag)

    return tag.is_blackened


# Some monkey patching
Line.from_nodes = MethodType(from_nodes, Line)  # type: ignore[method-assign]
JinjaFormatter._format_jinja_node = _format_jinja_node  # type: ignore[method-assign]


class TinybirdNodeManager(NodeManager):
    def __init__(self, case_sensitive_names: bool, lower_keywords: bool) -> None:
        super().__init__(case_sensitive_names)
        self.lower_keywords = lower_keywords

    def create_node(self, token: Token, previous_node: Optional[Node]) -> Node:
        try:
            return super().create_node(token, previous_node)
        except SqlfmtBracketError:
            if token.token == ">":
                raise
            # we already have tb check and the toolset to check the SQL, no need for this extra validation
            prev_token, extra_whitespace = get_previous_token(previous_node)
            prefix = self.whitespace(token, prev_token, extra_whitespace)
            value = self.standardize_value(token)
            return Node(
                token=token,
                previous_node=previous_node,
                prefix=prefix,
                value=value,
                formatting_disabled=[],
            )

    def raise_on_mismatched_bracket(self, token: Token, last_bracket: Node) -> None:
        # sqlfmt first tries `>` as an angle bracket. Retry comparisons inside
        # parentheses as operators instead of letting them consume the `(`.
        if token.token == ">":
            super().raise_on_mismatched_bracket(token, last_bracket)

    def standardize_value(self, token: Token) -> str:
        """
        Tinybird => Patched to not lower keywords
        https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/node_manager.py#L215
        """
        if self.lower_keywords:
            return super().standardize_value(token)

        if token.type in (
            TokenType.UNTERM_KEYWORD,
            TokenType.STATEMENT_START,
            TokenType.STATEMENT_END,
            TokenType.WORD_OPERATOR,
            TokenType.ON,
            TokenType.BOOLEAN_OPERATOR,
            TokenType.SET_OPERATOR,
        ):
            return " ".join(token.token.split())
        return token.token


def _replace_rules(rules: Sequence[Rule], override_rules_by_name: Dict[str, Rule]) -> List[Rule]:
    """Replace rules by name, including nested sqlfmt rulesets."""
    replaced_rules: List[Rule] = []
    for rule in rules:
        new_rule = override_rules_by_name.get(rule.name, rule)
        action = new_rule.action
        if isinstance(action, partial) and action.keywords:
            keywords = dict(action.keywords)
            changed = False
            for key, value in keywords.items():
                if isinstance(value, list) and all(isinstance(item, Rule) for item in value):
                    keywords[key] = _replace_rules(value, override_rules_by_name)
                    changed = True
            if changed:
                new_rule = Rule(
                    name=new_rule.name,
                    priority=new_rule.priority,
                    pattern=new_rule.pattern,
                    action=partial(action.func, *action.args, **keywords),
                )
        replaced_rules.append(new_rule)
    return replaced_rules


def _has_inline_jinja_block(sql: str) -> bool:
    """Return whether every Jinja control block has an inline body.

    Opening tags can span several lines when their Python expression is long.
    That formatting alone must not make an otherwise inline block look like a
    multiline one. Match each opening tag with its end tag, then inspect only
    the body between them. We conservatively skip the compatibility pass for
    malformed or genuinely mixed templates, because the pass works on the
    formatted output and cannot safely select individual blocks there.
    """
    tag_pattern = re.compile(
        r"\{%-?\s*(?P<start>if|for)\b.*?-?%\}|"
        r"\{%-?\s*end(?:\s+(?P<end>if|for))?\s*-?%\}",
        flags=re.IGNORECASE | re.DOTALL,
    )
    blocks: List[tuple[int, str]] = []
    has_control_block = False

    for tag in tag_pattern.finditer(sql):
        start_kind = tag.group("start")
        if start_kind is not None:
            has_control_block = True
            blocks.append((tag.end(), start_kind.lower()))
            continue

        if not blocks:
            return False

        body_start, start_kind = blocks.pop()
        end_kind = tag.group("end")
        if end_kind is not None and end_kind.lower() != start_kind:
            return False
        if "\n" in sql[body_start : tag.start()]:
            return False

    return has_control_block and not blocks


def _preserve_inline_jinja_blocks(source_sql: str, formatted_sql: str, line_length: int) -> str:
    """Keep Tinybird's old inline Jinja-block style when the input used it.

    sqlfmt 0.28 formats recognized Jinja blocks structurally, which turns
    ``{% if ... %} select 1 {% end %}`` into multiple lines. That is a valid
    formatting choice, but it creates formatting-only diffs for existing CLI
    users. Preserve the previous Tinybird style only for inputs that already had
    inline block contents; multiline blocks still benefit from proper nested
    block indentation.
    """
    if not _has_inline_jinja_block(source_sql):
        return formatted_sql

    lines = formatted_sql.splitlines()
    compacted_lines: List[str] = []
    branch_tag = re.compile(r"\{%-?\s*(if|for|elif|else)\b.*?-?%\}$", flags=re.IGNORECASE)
    chain_tag = re.compile(r"\{%-?\s*(elif|else|end)\b", flags=re.IGNORECASE)

    def single_line_body(at: int) -> Optional[str]:
        """Return lines[at] when it is a one-line body followed by a tag line."""
        if at + 1 >= len(lines):
            return None
        body = lines[at].strip()
        # A multiline {{ expression }} must retain its newline: joining
        # its opening {{ makes the next tb fmt pass undo this one.
        if not body or body.startswith("{%") or (body.startswith("{{") and not body.endswith("}}")):
            return None
        return body if lines[at + 1].strip().startswith("{%") else None

    inline_branch = re.compile(r"\{%-?\s*(elif|else)\b.*?-?%\}\s+[^{\s][^{]*$", flags=re.IGNORECASE)
    open_tag: Optional[str] = None
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        # Only opening/branch tags can absorb an inline body in 0.11; joining
        # text after {% end %} would move the following SQL clause or comment.
        if open_tag is not None and "{%" not in stripped and stripped.endswith("%}"):
            # Closing line of a tag whose long condition spans several lines.
            last_tag = f"{open_tag} {stripped}"
            open_tag = None
        else:
            last_tag = stripped[stripped.rfind("{%") :]
            if "{%" in stripped and "%}" not in last_tag:
                open_tag = last_tag
        body = single_line_body(index + 1) if branch_tag.match(last_tag) else None
        if body is None:
            compacted_lines.append(line)
            index += 1
            continue

        first = f"{line.rstrip()} {body}"
        # Try to fold the whole if/elif/else/end chain onto one line.
        chain = [first]
        closed = False
        cursor = index + 2
        while cursor < len(lines) and chain_tag.match(lines[cursor].strip()):
            tag_line = lines[cursor].strip()
            cursor += 1
            if re.match(r"\{%-?\s*end\b", tag_line, flags=re.IGNORECASE):
                chain.append(tag_line)
                closed = True
                break
            if inline_branch.match(tag_line):
                chain.append(tag_line)
                continue
            branch_body = single_line_body(cursor) if branch_tag.match(tag_line) else None
            if branch_body is None:
                break
            chain.append(f"{tag_line} {branch_body}")
            cursor += 1
        joined = " ".join(chain)
        if closed and len(joined) <= line_length:
            compacted_lines.append(joined)
            index = cursor
        elif len(first) <= line_length:
            compacted_lines.append(first)
            index += 2
        else:
            compacted_lines.append(line)
            index += 1

    return "\n".join(compacted_lines)


def _preserve_legacy_formatting(source_sql: str, formatted_sql: str, line_length: int) -> str:
    """Apply compatibility shims for customer-visible Tinybird formatting.

    These transformations intentionally preserve quirks from the sqlfmt 0.11
    based CLI output. The dependency upgrade is for Python 3.14 compatibility;
    it should not make customer projects fail `tb fmt --diff` because of style
    churn unrelated to their code.
    """
    formatted_sql = _preserve_inline_jinja_blocks(source_sql, formatted_sql, line_length)
    if re.search(r"\bas\s+end\b", source_sql, flags=re.IGNORECASE):
        # When `end` is a column alias, 0.11 kept adjacent Jinja control tags
        # on the same line instead of treating the alias as a CASE terminator.
        formatted_sql = re.sub(r"(?m)^end\n(?=\{%\s*(?:else|end)\b)", "end ", formatted_sql)
    lines = formatted_sql.splitlines()
    # 0.11 attached a trailing comment on two AND terms to the first term;
    # 0.28 attaches it to the last, mislabeling the condition in tb fmt output.
    source_comments = {
        line.split("--", 1)[1].strip(): line.strip()
        for line in source_sql.splitlines()
        if "--" in line and line.lstrip().lower().startswith("and ")
    }
    index = 1
    while index < len(lines):
        previous, current = lines[index - 1], lines[index]
        if (
            "  --" in current
            and current.lstrip().lower().startswith("and ")
            and previous.lstrip().lower().startswith("and ")
        ):
            statement, comment = current.split("  --", 1)
            source_line = source_comments.get(comment.strip(), "")
            if source_line.lower().count(" and ") >= 1:
                lines[index - 1] = f"{previous}  --{comment}"
                lines[index] = statement.rstrip()
                previous, current = lines[index - 1], lines[index]
        # 0.11 kept a following any(...) select item on the same line when
        # space allowed; 0.28 always splits these qualified/long expressions.
        if (
            previous.endswith(",")
            and ("." in previous or "(" in previous or len(previous.strip()) >= 26)
            and not previous.lstrip().lower().startswith("any (")
            and current.lstrip().lower().startswith("any (")
            and len(previous) - len(previous.lstrip()) == len(current) - len(current.lstrip())
            and len(previous) + 1 + len(current.strip()) <= line_length
        ):
            lines[index - 1] = f"{previous} {current.strip()}"
            lines.pop(index)
        else:
            index += 1
    return "\n".join(lines)


class TinybirdDialect(ClickHouse):
    """
    This is an extension of the base rules.

    We might need to override the base `word_operator` and `unterm_keyword` rules with some custom ClickHouse terms.

    For now we are just overriding the end blocks for `if` and `for` to work with Tornado templates.

    https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/dialect.py#L55
    """

    def __init__(self, lower_keywords: bool = False) -> None:
        super().__init__()
        self.lower_keywords = lower_keywords

        override_rules = [
            Rule(
                name="number",
                priority=401,
                pattern=group(
                    r"-?0x[0-9a-f][0-9a-f_]*(\.[0-9a-f_]*)?(p[+-]?\d[\d_]*)?",
                    r"-?0b[01][01_]*",
                    r"-?(\d[\d_]*\.?[\d_]*|\.\d[\d_]*)(e[+-]?\d[\d_]*)?",
                ),
                action=partial(actions.add_node_to_buffer, token_type=TokenType.NUMBER),
            ),
            Rule(
                name="quoted_name",
                priority=200,
                pattern=group(
                    SQL_QUOTED_EXP,
                    r"((?<!\\)\$[\w$]+)",  # Words starting with $ for .incl files
                ),
                action=partial(actions.add_node_to_buffer, token_type=TokenType.QUOTED_NAME),
            ),
            Rule(
                name="legacy_array_join",
                priority=1040,
                # 0.11 parsed ARRAY and JOIN separately, so wrapped joins keep
                # ARRAY at the end of the preceding line.
                pattern=group(r"array(?=\s+join\b)"),
                action=partial(actions.add_node_to_buffer, token_type=TokenType.NAME),
            ),
            Rule(
                name="join_using",
                priority=1049,
                # sqlfmt 0.11 treats USING without parentheses as a word operator.
                pattern=group(r"using") + group(r"\W", r"$"),
                action=partial(actions.add_node_to_buffer, token_type=TokenType.WORD_OPERATOR),
            ),
            Rule(
                name="legacy_any_operator",
                priority=1098,
                # 0.11 classified any(...) as an operator and printed any (...).
                pattern=group(r"any") + group(r"\W", r"$"),
                action=partial(actions.add_node_to_buffer, token_type=TokenType.WORD_OPERATOR),
            ),
            Rule(
                name="jinja_if_block_end",
                priority=203,
                # Accept both Tornado-style {% end %} and {% end if %}.
                pattern=group(r"\{%-?\s*end(\s+if)?\s*-?%\}"),
                action=actions.handle_jinja_block_end,
            ),
            Rule(
                name="jinja_for_block_end",
                priority=211,
                # Accept both Tornado-style {% end %} and {% end for %}.
                pattern=group(r"\{%-?\s*end(\s+for)?\s*-?%\}"),
                action=actions.handle_jinja_block_end,
            ),
        ]

        override_rules_by_name = {rule.name: rule for rule in override_rules}
        self.RULES = _replace_rules(self.RULES, override_rules_by_name)
        # Unlike USING, these are extra legacy tokens absent from 0.28's
        # ruleset; register them so old projects keep their formatted output.
        self.RULES.insert(0, override_rules_by_name["legacy_any_operator"])
        self.RULES.insert(0, override_rules_by_name["legacy_array_join"])

    def initialize_analyzer(self, line_length: int) -> Analyzer:
        """
        Creates and returns an analyzer that uses the Dialect's rules for lexing
        Custom NodeManager for Tinybird
        """
        return Analyzer(
            line_length=line_length,
            rules=self.get_rules(),
            node_manager=TinybirdNodeManager(self.case_sensitive_names, self.lower_keywords),
        )


@dataclass
class TBMode(Mode):
    lower_keywords: bool = False

    def __post_init__(self) -> None:
        """
        Tinybird => Overriden to use `TinybirdDialect`
        https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/mode.py#L31
        """
        self.dialect = TinybirdDialect(self.lower_keywords)


def _calc_str(self) -> str:
    if self.is_multiline:
        return self.token.token + "\n"
    marker, comment_text = self._comment_parts()
    if comment_text == "":
        return marker + "\n"
    return marker + " " + comment_text + "\n"


Comment._calc_str = property(_calc_str)  # type: ignore[attr-defined]


def format_sql_template(
    sql: str,
    line_length: Optional[int] = None,
    lower_keywords: bool = False,
    resource_name: Optional[str] = None,
    resource_source: Optional[str] = None,
) -> str:
    try:
        # https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/mode.py#L16-L29
        config: Dict[str, Any] = {
            "line_length": line_length or DEFAULT_FMT_LINE_LENGTH,
            "lower_keywords": lower_keywords,
        }

        mode = TBMode(**config)
        sql = sql.strip()
        formatted_sql = (
            "%\n" + api.format_string(sql[1:], mode=mode).strip()
            if sql[0] == "%"
            else api.format_string(sql, mode=mode).strip()
        )
        return _preserve_legacy_formatting(sql, formatted_sql, mode.line_length)
    except Exception as e:
        resource_info = f" in '{resource_name}'" if resource_name else ""
        source_info = f" ({resource_source})" if resource_source else ""
        logging.warning(f"sqlfmt error{resource_info}{source_info}: {str(e)}")
        return sql
