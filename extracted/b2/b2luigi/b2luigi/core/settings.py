import json
import os
import contextlib
from typing import Any, Generator, List, Optional
import warnings

# The global object hosting the current settings
_current_global_settings = {}
_no_value = object()


def get_setting(
    key: str, default: Any = None, task: Optional[object] = None, deprecated_keys: Optional[List[str]] = None
) -> Any:
    """
    ``b2luigi`` adds a settings management to ``luigi``
    and also uses it at various places.
    Many batch systems, the output and log path, the environment
    etc. is controlled via these settings.

    There are four ways settings could be defined.
    They are used in the following order (an earlier setting
    overrides a later one):

    1. If the currently processed (or scheduled) task has a property
       of the given name, it is used.
       Please note that you can either set the property directly, e.g.

       .. code-block:: python

         class MyTask(b2luigi.Task):
             batch_system = "htcondor"

       or by using a function (which might even depend on the parameters)

       .. code-block:: python

         class MyTask(b2luigi.Task):
             @property
             def batch_system(self):
                 return "htcondor"

       The latter is especially useful for batch system specific settings
       such as requested wall time etc.

    2. Settings set directly by the user in your script with a call to
       :meth:`b2luigi.set_setting`.
    3. Settings specified in the ``settings.json`` in the folder of your
       script *or any folder above that*.
       This makes it possible to have general project settings (e.g. the output path
       or the batch system) and a specific ``settings.json`` for your sub-project.

    With this function, you can get the current value of a specific setting with the given key.
    If there is no setting defined with this name,
    either the default is returned or, if you did not supply any default, a value error is raised.

    Settings can be of any type, but are mostly strings.

    Args:
        key (:obj:`str`): The name of the parameter to query.
        task: (:obj:`b2luigi.Task`): If given, check if the task has a parameter
            with this name.
        default (optional): If there is no setting which the name,
            either return this default or if it is not set,
            raise a ValueError.
        deprecated_keys (:obj:`List`): Former names of this setting,
            will throw a warning when still used
    """
    # First check if the correct name is set. If yes, just use it
    try:
        return _get_setting_implementation(key=key, task=task)
    except KeyError:
        pass

    # Ok, now test the deprecated setting names, but issue a warning
    if deprecated_keys:
        for deprecated_key in deprecated_keys:
            try:
                value = _get_setting_implementation(key=deprecated_key, task=task)
                _warn_deprecated_setting(deprecated_key, key)
                return value
            except KeyError:
                pass

    # Still not found? At this point we can only return the default or raise an error
    if default is None:
        raise ValueError(f"No settings found for {key}!")
    return default


def set_setting(key: str, value: Any) -> None:
    """
    Updates the global settings dictionary with a specified key-value pair.

    This function allows overriding any existing settings defined in
    `setting.json`. It is particularly useful for dynamically updating
    settings during runtime. For task-specific settings, consider creating
    a parameter with the given name in your task instead.

    Args:
        key (str): The name of the setting to update or add.
        value (Any): The value to associate with the specified key.
    """
    _current_global_settings[key] = value


def clear_setting(key: str) -> None:
    """
    Removes a setting from the global settings dictionary.

    If the key does not exist, the function silently handles the ``KeyError``.

    Args:
        key (str): The key of the setting to be removed.
    """
    try:
        del _current_global_settings[key]
    except KeyError:
        pass


def _setting_file_iterator() -> Generator[str, None, None]:
    """
    A generator function that yields the path to a settings JSON file.

    This function first checks if the environment variable ``B2LUIGI_SETTINGS_JSON``
    is set. If it is, the value of this environment variable (assumed to be a
    file path) is yielded. If the environment variable is not set, the function
    searches for a file named `settings.json` in the current working directory
    and its parent directories, moving upwards in the directory hierarchy until
    the root directory is reached.

    Yields:
        str: The path to the `settings.json` file if found, or the value of the
        ``B2LUIGI_SETTINGS_JSON`` environment variable if it is set.
    """
    # first, check if B2LUIGI_SETTINGS_JSON is set in the environment
    if "B2LUIGI_SETTINGS_JSON" in os.environ:
        yield os.environ["B2LUIGI_SETTINGS_JSON"]
    # if it is not set, search in the durrent working dir (old behaviour)
    else:
        path = os.getcwd()
        while True:
            json_file = os.path.join(path, "settings.json")
            if os.path.exists(json_file):
                yield json_file

            path = os.path.split(path)[0]
            if path == "/":
                break


@contextlib.contextmanager
def with_new_settings():
    global _current_global_settings
    old_settings = _current_global_settings.copy()
    _current_global_settings = {}

    yield

    _current_global_settings = old_settings.copy()


def _get_setting_implementation(key: str, task: Optional[object] = None) -> Any:
    """
    Retrieve a setting value based on a specified key and task.

    This function attempts to retrieve the value of a setting in the following order:
    1. Check if the provided task object has an attribute matching the key.
    2. Check if the setting is explicitly defined in the global settings.
    3. Check the setting files for the key.

    If the key is not found in any of these locations, a ``KeyError`` is raised.

    Args:
        key (str): The name of the setting to retrieve.
        task (object): An optional task that may contain the setting as an attribute.

    Returns:
        Any: The value of the setting corresponding to the given key.

    Raises:
        KeyError: If the setting cannot be found in the task, global settings, or setting files.
    """
    # First check if the task has an attribute with this name
    if task:
        try:
            return getattr(task, key)
        except AttributeError:
            pass

    # Then check if the setting was set explicitly
    try:
        return _current_global_settings[key]
    except KeyError:
        pass

    # And finally check the settings files
    for settings_file in _setting_file_iterator():
        try:
            with open(settings_file, "r") as f:
                j = json.load(f)
                return j[key]
        except KeyError:
            pass

    # The setting was not found, so raise a KeyError
    raise KeyError(f"No settings found for {key}!")


class DeprecatedSettingsWarning(DeprecationWarning):
    """
    A custom warning class used to indicate deprecated settings.

    This warning is a subclass of ``DeprecationWarning`` and can be used
    to alert users about the usage of settings that are no longer supported
    or will be removed in future versions.

    Usage:
        Raise this warning when a deprecated setting is accessed or used.

    Example:

        .. code-block:: python

            warnings.warn("This setting is deprecated.", DeprecatedSettingsWarning)
    """

    pass


def _warn_deprecated_setting(setting_name: str, new_name: str) -> None:
    """
    Emit a warning indicating that a specific setting is deprecated and should be replaced.

    Args:
        setting_name (str): The name of the deprecated setting.
        new_name (str): The name of the new setting that should be used instead.

    Raises:
        DeprecatedSettingsWarning: A warning to inform users about the deprecation
        and encourage migration to the new setting.
    """
    warnings.warn(
        f"The setting with the name {setting_name} is deprecated. "
        f"Please use {new_name} instead. Future versions might remove this setting.",
        DeprecatedSettingsWarning,
    )
