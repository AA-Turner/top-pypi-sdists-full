"""Contains utility functions / classes."""

import contextlib
import os
import re
from typing import Dict, Any, Pattern, Iterable, Callable, List, Tuple, Iterator, Optional, cast

from .types import YamlDocument
from .validator import Validator

PatternGenerator = Iterator[Tuple[Dict[Any, Any], str, Any]]
PathEvalCallable = Callable[[str, Optional[str]], Optional[str]]


def dict_find_pattern(_dict: Dict[Any, Any], pattern: str, search_in_keys: bool = True,
                      search_in_values: bool = True) -> PatternGenerator:
    """
    Find keys and values in a (nested) dictionary with regular expression pattern.
    Examples:
        >>> from collections import OrderedDict
        >>> d = OrderedDict((
        ...     ('foo', 'bar'),
        ...     ('bar', 'baz'),
        ...     ('nested', dict(p1=1, p2=2)),
        ...     ('lst', ['bar', 'foo', dict(p3=3, p4=4)])
        ... ))
        >>> f = dict_find_pattern(d, '.*a.*', search_in_keys=True, search_in_values=False)
        >>> def print_findings(f):
        ...     for _, key, value in f:
        ...         print(key, value)
        >>> print_findings(f)
        bar baz
        >>> f = dict_find_pattern(d, '.*a.*', search_in_keys=False, search_in_values=True)
        >>> print_findings(f)
        foo bar
        bar baz

    Args:
        _dict: Dictionary to scan for the specified pattern.
        pattern: The pattern to scan for.
        search_in_keys: If True keys will be probed for the pattern; otherwise not.
        search_in_values: If True values will be probed for the pattern; otherwise not.

    Returns:
        Generator to iterate over the findings.
    """

    def find(dic: Dict[Any, Any], regex: Pattern[str]) -> PatternGenerator:
        Validator.instance_of(target_type=dict, raise_ex=True, dic=dic)

        for k, val in dic.items():
            if search_in_keys and isinstance(k, str) and regex.match(k):
                yield dic, k, val
            if search_in_values and isinstance(val, str) and regex.match(val):
                yield dic, k, val
            if isinstance(val, list):
                for litem in val:
                    if isinstance(litem, dict):
                        for j in find(litem, regex):
                            yield j
            if isinstance(val, dict):
                for j in find(val, regex):
                    yield j

    regex = re.compile(pattern)
    return find(_dict, regex)


@contextlib.contextmanager
def modified_environ(*remove: str, **update: str) -> Iterator[None]:
    """
    Temporarily updates the ``os.environ`` dictionary in-place and resets it to the original state
    when finished.
    (https://stackoverflow.com/questions/2059482/
        python-temporarily-modify-the-current-processs-environment/34333710#34333710)

    The ``os.environ`` dictionary is updated in-place so that the modification is sure to work in
    all situations.

    Args:
        remove: Environment variables to remove.
        update: Dictionary of environment variables and values to add/update.

    Examples:
        >>> with modified_environ(Test='abc'):
        ...     import os
        ...     print(os.environ.get('Test'))
        abc
        >>> print(os.environ.get('Test'))
        None
    """
    env = os.environ
    update = update or {}
    remove = remove or ()

    # List of environment variables being updated or removed.
    stomped = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in stomped}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    try:
        env.update(update)
        [env.pop(k, None) for k in remove]  # pylint: disable=expression-not-assigned
        yield
    finally:
        env.update(update_after)
        [env.pop(k) for k in remove_after]  # pylint: disable=expression-not-assigned


def eval_first_non_none(eval_list: Iterable[Callable[..., Any]], **kwargs: Any) -> Any:
    """
    Executes a list of functions and returns the first non none result. All kwargs will be passed as
    kwargs to each individual function. If all functions return None, None is the overall result.

    Examples:

        >>> eval_first_non_none((lambda: None, lambda: None, lambda: 3))
        3
        >>> print(eval_first_non_none([lambda: None, lambda: None, lambda: None]))
        None
        >>> eval_first_non_none([
        ...     lambda cnt: cnt if cnt == 1 else None,
        ...     lambda cnt: cnt if cnt == 2 else None,
        ...     lambda cnt: cnt if cnt == 3 else None]
        ... , cnt=2)
        2
    """
    Validator.is_real_iterable(raise_ex=True, eval_list=eval_list)

    for eval_fun in eval_list:
        res = eval_fun(**kwargs)
        if res is not None:
            return res
    return None


def multi_process(
        process_fun: Callable[[Pattern[str], str], Any],
        _pattern: Pattern[str],
        initial_value: str
) -> Any:
    """Calls the process_fun over and over again with output of the last one being the
    input of the next one until the output does not change anymore."""
    res = initial_value
    while True:
        new_output = process_fun(_pattern, res)
        if new_output == res:
            # Nothing changed
            break
        res = new_output
    return res


class FileLocator:  # pylint: disable=too-few-public-methods
    """
    Based on a base_path, the given file path and a possible parent file path the locator
    will construct a absolute file_path if the given file name is relative.

    If the file path is absolute the absolute file path will be used. If it's relative and a
    base_path is given the both will be concatenated. If no base path is given, the path from the
    parent file path will be used. If there is no parent file path the current working directory is
    the default.
    """

    def __init__(self, base_path: Optional[str] = None, parent_overrides_base: bool = False):
        """
        Args:
            base_path:
            parent_overrides_base: If set to True the file path of the parent (if any) will
                overrule the base_path; otherwise the base_path will overrule the parent's file
                path even (if any).
        """
        self.base_path = base_path and str(base_path)
        self.parent_overrides_base = bool(parent_overrides_base)

    @staticmethod
    def _eval_absolute_path(abs_or_rel_file_path: str,
                            parent_file_path: Optional[str] = None) -> Optional[str]:  # pylint: disable=unused-argument
        if os.path.isabs(abs_or_rel_file_path):
            return abs_or_rel_file_path
        return None

    def _eval_base_path(self, abs_or_rel_file_path: str,
                        parent_file_path: Optional[str] = None) -> Optional[str]:  # pylint: disable=unused-argument
        if self.base_path is not None:
            return os.path.join(self.base_path, abs_or_rel_file_path)
        return None

    @staticmethod
    def _eval_parent_file_path(abs_or_rel_file_path: str,
                               parent_file_path: Optional[str]) -> Optional[str]:
        if parent_file_path is not None and Validator.is_file(parent_file_path=parent_file_path):
            # If the yaml data is from a file, we assume the base_path should be the path where
            # the file is located
            return os.path.join(os.path.dirname(parent_file_path), abs_or_rel_file_path)
        return None

    @staticmethod
    def _eval_cwd(abs_or_rel_file_path: str,
                  parent_file_path: Optional[str] = None) -> Optional[str]:  # pylint: disable=unused-argument
        return os.path.join(os.getcwd(), abs_or_rel_file_path)

    def _eval_list(self) -> Iterable[PathEvalCallable]:
        eval_list = [self._eval_absolute_path]  # type: List[PathEvalCallable]
        if self.parent_overrides_base:
            return eval_list + [self._eval_parent_file_path, self._eval_base_path, self._eval_cwd]
        return eval_list + [self._eval_base_path, self._eval_parent_file_path, self._eval_cwd]

    def __call__(self, abs_or_rel_file_path: str,
                 parent_file_path: Optional[YamlDocument] = None) -> str:
        """
        Given a file_path and the actual file path of the parent file the absolute path of the
        potential relative path will be determined. If `parent_file_path` is not None that basically
        means that the file to locate is part of an externally loaded file.

        Args:
            abs_or_rel_file_path: Absolute or relative file path.
            parent_file_path: When it's a file it is used to determine a base path if necessary.

        Returns:
            Returns the absolute path of the file. If it's already absolute, nothing changes.
        """
        return cast(str, eval_first_non_none(
            self._eval_list(),
            abs_or_rel_file_path=abs_or_rel_file_path,
            parent_file_path=parent_file_path
        ))
