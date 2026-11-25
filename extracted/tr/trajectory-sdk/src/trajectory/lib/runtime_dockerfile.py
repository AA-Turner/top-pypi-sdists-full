"""Check runtime Dockerfiles for instructions the platform's image builder cannot run."""

from __future__ import annotations

import json
import re
import shlex
from collections.abc import Iterator
from urllib.parse import urlsplit

# Larger Dockerfiles are left for the platform to reject.
MAX_RUNTIME_DOCKERFILE_BYTES = 1024 * 1024
LOCAL_ADD_ERROR = (
  "ADD supports only a single http:// or https:// URL source; "
  "use COPY for files and directories, or COPY <archive> <tmp> then "
  "RUN mkdir -p <dest> && tar -xf <tmp> -C <dest>"
)
UNCLOSED_HEREDOC_ERROR = "heredoc is never closed by its delimiter line"
UNIMPLEMENTED_INSTRUCTIONS = ("EXPOSE", "HEALTHCHECK", "LABEL", "ONBUILD", "STOPSIGNAL", "VOLUME")


class RuntimeDockerfile:
  """`validate` mirrors the platform's ingestion check, so a submission fails before it uploads."""

  # Delimiters are any word without shell metacharacters, such as EOF or EOF.txt.
  _HEREDOC = re.compile(r"^\d*<<(-?)([\"']?)([^\s<>|;&()\"']+)\2$")
  _HEREDOC_INSTRUCTIONS = ("RUN", "COPY", "ADD")
  _ENV_DEFAULT = re.compile(r"\$\{\w+:?[-+]")

  @classmethod
  def validate(cls, dockerfile: str) -> None:
    for line, instruction in cls._iter_instructions(dockerfile):
      keyword, *arguments = instruction.split(None, 1)
      if keyword.upper() == "ADD" and not cls._is_single_url_source(" ".join(arguments)):
        raise ValueError(f"{LOCAL_ADD_ERROR} (line {line}: {instruction})")

  @classmethod
  def find_warnings(cls, dockerfile: str) -> list[str]:
    """Instructions the image builder documents as unimplemented, ignored or partly supported.

    These warn instead of failing because the platform accepts them.
    """
    warnings = []
    for line, instruction in cls._iter_instructions(dockerfile):
      keyword = instruction.split(None, 1)[0].upper()
      if keyword in UNIMPLEMENTED_INSTRUCTIONS:
        warnings.append(f"line {line}: {keyword} is not implemented by the image builder")
      elif keyword == "USER":
        warnings.append(f"line {line}: USER is ignored by the image builder")
      elif keyword == "ENV" and cls._ENV_DEFAULT.search(instruction):
        warnings.append(
          f"line {line}: ENV default values such as ${{VAR:-default}} are not supported "
          "by the image builder"
        )
    return warnings

  @classmethod
  def _iter_instructions(cls, dockerfile: str) -> Iterator[tuple[int, str]]:
    """Yield each instruction's first line number and its text with continuations joined."""
    lines = dockerfile.removeprefix("\ufeff").splitlines()
    index = 0
    while index < len(lines):
      start = index
      text = lines[index].strip()
      index += 1
      if not text or text.startswith("#"):
        continue
      parts = []
      while text.endswith("\\") and index < len(lines):
        parts.append(text[:-1].strip())
        text = lines[index].strip()
        index += 1
        # Docker drops comment and blank lines inside a continued instruction.
        if not text or text.startswith("#"):
          text = "\\"
      parts.append(text.removesuffix("\\").strip())
      instruction = " ".join(part for part in parts if part)
      # Docker ignores a continuation that runs into the end of the file.
      if not instruction:
        continue
      # Heredoc bodies are file content, not instructions.
      keyword = instruction.split(None, 1)[0].upper()
      words = cls._split_words(instruction) if keyword in cls._HEREDOC_INSTRUCTIONS else []
      heredocs = [match.groups() for match in map(cls._HEREDOC.match, words) if match]
      for strip_tabs, _, delimiter in heredocs:
        while index < len(lines):
          body = lines[index].lstrip("\t") if strip_tabs else lines[index]
          index += 1
          if body.rstrip() == delimiter:
            break
        else:
          # Docker rejects it too, and skipping it could hide an ADD.
          raise ValueError(f"{UNCLOSED_HEREDOC_ERROR} (line {start + 1}: {delimiter})")
      yield start + 1, instruction

  @staticmethod
  def _split_words(text: str) -> list[str]:
    """Split on unquoted whitespace, keeping quotes, as Docker does when it looks for heredocs."""
    words, word, quote, escaped = [], "", "", False
    for char in text:
      if escaped:
        escaped = False
      elif char == "\\" and quote != "'":
        escaped = True
      elif quote:
        quote = "" if char == quote else quote
      elif char in "\"'":
        quote = char
      elif char.isspace():
        if word:
          words.append(word)
        word = ""
        continue
      word += char
    return [*words, word] if word else words

  @staticmethod
  def _unquote(word: str) -> str:
    try:
      return "".join(shlex.split(word))
    except ValueError:
      # Docker rejects unbalanced quotes too, and a quoted token is never a URL.
      return word

  @classmethod
  def _is_single_url_source(cls, arguments: str) -> bool:
    tokens = arguments.split()
    while tokens and tokens[0].startswith("--"):
      tokens.pop(0)
    rest = " ".join(tokens)
    parsed = None
    if rest.startswith("["):
      # Docker reads an unparseable JSON array as the shell form.
      try:
        parsed = json.loads(rest)
      except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, list) and all(isinstance(token, str) for token in parsed):
      tokens = parsed
    else:
      # Shell-form ADD splits on whitespace, then strips each word's quotes.
      tokens = [cls._unquote(token) for token in tokens]
    if len(tokens) != 2:
      return False
    # A variable's value is unknown here, so leave it for the build instead of guessing.
    if "$" in tokens[0]:
      return True
    source = urlsplit(tokens[0])
    # Docker clones http(s) URLs ending in .git instead of downloading them.
    return source.scheme in ("http", "https") and not source.path.endswith(".git")
