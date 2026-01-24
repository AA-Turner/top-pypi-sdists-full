from __future__ import annotations

import importlib
import inspect
import logging
import os
import re
import sys
from typing import Any, Callable

from setuptools_git_versioning.log import DEBUG, INFO

log = logging.getLogger(__name__)


def add_to_sys_path(root: str | os.PathLike | None) -> None:
    project_root = os.fspath(root) if root else os.getcwd()  # noqa: PTH109
    if project_root not in sys.path:
        log.log(DEBUG, "Adding '%s' folder to sys.path", project_root)
        sys.path.insert(0, project_root)


def import_reference(
    ref: str,
    package_name: str | None = None,
    root: str | os.PathLike | None = None,
) -> Any:
    if ":" not in ref:
        msg = f"Wrong reference name: {ref}"
        raise NameError(msg)

    add_to_sys_path(root)

    module_name, attr = ref.split(":")
    log.log(DEBUG, "Executing 'from %s.%s import %s'", package_name or "", module_name, attr)
    module = importlib.import_module(module_name, package_name)

    return getattr(module, attr)


def load_callable(
    inp: str,
    package_name: str | None = None,
    root: str | os.PathLike | None = None,
) -> Callable:
    ref = import_reference(inp, package_name, root=root)
    if not callable(ref):
        msg = f"{ref} of type {type(ref)} is not callable"
        raise TypeError(msg)

    return ref


def _callable_factory(
    callable_name: str,
    regexp_or_ref: str | Callable,
    callable_factory: Callable[[str], Callable],
    package_name: str | None = None,
    root: str | os.PathLike | None = None,
) -> Callable:
    log.log(INFO, "Parsing %s %r of type %r", callable_name, regexp_or_ref, type(regexp_or_ref).__name__)

    if callable(regexp_or_ref):
        log.log(DEBUG, "Value is callable with signature %s", inspect.Signature.from_callable(regexp_or_ref))
        return regexp_or_ref

    try:
        return load_callable(regexp_or_ref, package_name, root=root)
    except (ImportError, NameError) as e:
        log.log(DEBUG, "%s is not a valid function reference: %s", callable_name, e)

    try:
        return callable_factory(regexp_or_ref)
    except re.error as e:
        log.exception("%s is not valid regexp neither a valid function reference", callable_name)
        msg = f"Cannot parse {callable_name}"
        raise ValueError(msg) from e


def branch_formatter_factory(regexp: str) -> Callable[[str], str]:
    pattern = re.compile(regexp)

    def branch_formatter(branch: str) -> str:
        match = pattern.match(branch)
        if match:
            return match.group("branch")

        msg = f"Branch name {branch} does not match regexp '{regexp}'"
        raise ValueError(msg)

    return branch_formatter


def create_branch_formatter(
    branch_formatter: Callable[[str], str] | str,
    package_name: str | None = None,
    root: str | os.PathLike | None = None,
):
    return _callable_factory(
        callable_name="branch_formatter",
        regexp_or_ref=branch_formatter,
        callable_factory=branch_formatter_factory,
        package_name=package_name,
        root=root,
    )


def tag_formatter_factory(regexp: str) -> Callable[[str], str]:
    pattern = re.compile(regexp)

    def tag_formatter(tag: str) -> str:
        match = pattern.match(tag)
        if match:
            return match.group("tag")

        msg = f"Tag name {tag} does not match regexp '{regexp}'"
        raise ValueError(msg)

    return tag_formatter


def create_tag_formatter(
    tag_formatter: Callable[[str], str] | str,
    package_name: str | None = None,
    root: str | os.PathLike | None = None,
):
    return _callable_factory(
        callable_name="tag_formatter",
        regexp_or_ref=tag_formatter,
        callable_factory=tag_formatter_factory,
        package_name=package_name,
        root=root,
    )


def tag_filter_factory(regexp: str) -> Callable[[str], str | None]:
    pattern = re.compile(regexp)

    def tag_filter(tag: str) -> str | None:
        match = pattern.match(tag)
        if match:
            log.info("Matched %s", tag)
            return tag
        return None

    return tag_filter


def create_tag_filter(
    tag_filter: Callable[[str], str | None] | str,
    package_name: str | None = None,
    root: str | os.PathLike | None = None,
):
    return _callable_factory(
        callable_name="tag_filter",
        regexp_or_ref=tag_filter,
        callable_factory=tag_filter_factory,
        package_name=package_name,
        root=root,
    )
