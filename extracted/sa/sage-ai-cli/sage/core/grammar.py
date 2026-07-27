"""GBNF grammar for Sage's tool-call protocol."""

from __future__ import annotations

__all__ = ["SAGE_PROTOCOL_GBNF", "load_grammar"]


SAGE_PROTOCOL_GBNF = r"""
root      ::= turn
turn      ::= action (ws+ action)* ws*
action    ::= file-block | read-cmd | search-cmd | run-cmd | webfetch-cmd | websearch-cmd | answer
answer    ::= "ANSWER:" ws+ text-line ("\n" text-line)*
read-cmd     ::= "READ:" ws+ path
search-cmd   ::= "SEARCH:" ws+ text-line
run-cmd      ::= "RUN:" ws+ text-line
webfetch-cmd ::= "WEB_FETCH:" ws+ url
websearch-cmd ::= "SEARCH_WEB:" ws+ text-line
file-block ::= "FILE:" ws+ path "\n" code-fence
code-fence ::= "```" lang "\n" code-content "\n```"
lang       ::= [a-zA-Z0-9_+\-]*
code-content ::= ([^`] | "`" [^`] | "``" [^`])*
path  ::= [^\n ]+
url   ::= "http" "s"? "://" [^\n ]+
text-line ::= [^\n]*
ws ::= [ \t\n]
"""


def load_grammar():
    try:
        from llama_cpp import LlamaGrammar  # type: ignore
    except ImportError:
        return None
    try:
        return LlamaGrammar.from_string(SAGE_PROTOCOL_GBNF)
    except Exception:
        return None
