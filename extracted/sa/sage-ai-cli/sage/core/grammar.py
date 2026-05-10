"""GBNF grammar for Sage's tool-call protocol.

llama-cpp-python supports `grammar=LlamaGrammar.from_string(gbnf)`. When set,
the model can ONLY emit tokens consistent with the grammar — making
malformed FILE: blocks mathematically impossible.

The grammar mirrors the protocol described in the SAGE system prompt:
  ANSWER: <free text>
  READ: <path>
  SEARCH: <pattern>
  RUN: <shell>
  WEB_FETCH: <url>
  SEARCH_WEB: <query>
  FILE: <path>
  ```<lang>
  <content>
  ```

We intentionally support a *subset* of natural model output — the grammar
is opt-in via `enable_grammar=True` so freeform answers still work when the
caller doesn't enforce structure.
"""

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
    """Return a llama_cpp.LlamaGrammar instance, or None if llama-cpp unavailable."""
    try:
        from llama_cpp import LlamaGrammar  # type: ignore
    except ImportError:
        return None
    try:
        return LlamaGrammar.from_string(SAGE_PROTOCOL_GBNF)
    except Exception:
        return None
