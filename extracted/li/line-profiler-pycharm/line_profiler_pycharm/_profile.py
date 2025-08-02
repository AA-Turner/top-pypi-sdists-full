import atexit
import json
import os
import pathlib
import sys

import line_profiler


class PyCharmLineProfiler(line_profiler.LineProfiler):
    """Singleton extension around the LineProfiler from line_profiler that writes profile data to a .pclprof file

    When the process exits, the profile results are written to a `.pclprof` file, which contains json data.
    This json file is recognized by the PyCharm Line Profiler plugin.
    The PyCharm Line Profiler plugin can visualize the json file with neat colormaps and other stuff
    directly into the code in the editors.

    PyCharmLineProfiler uses an environment variable called
        PC_LINE_PROFILER_STATS_FILENAME
    to determine where to save the profile file. This environment variable is set by the Line Profiler plugin
    so that plugin's Executor extension can automatically open the results of a profiling after running it.
    """
    _instance = None
    _units = None

    def __init__(self, *args, **kwargs):
        self._units = dict()
        super(PyCharmLineProfiler, self).__init__(*args, **kwargs)
        # Stats file defaults to file in same directory as script with `.pclprof` appended
        self._stats_filename = os.environ.get("PC_LINE_PROFILER_STATS_FILENAME",
                                              pathlib.Path(sys.argv[0]).name)
        atexit.register(self._dump_stats_for_pycharm)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __call__(self, func, unit=None):
        if unit:
            code = func.__code__
            self._units[code.co_filename, code.co_firstlineno, code.co_name] = unit

        return super().__call__(func)

    def _dump_stats_for_pycharm(self):
        """Dumps profile stats that can be read by the PyCharm Line Profiler plugin

        The stats are written to a json file, with extension .pclprof
        This extension is recognized by the PyCharm Line Profiler plugin
        """
        stats = self.get_stats()

        profiled_functions = []

        for key, value in stats.timings.items():
            multiplier = self._units[key] / stats.unit if key in self._units else 1
            profiled_functions.append({
                "file": key[0],
                "lineNo": key[1],
                "functionName": key[2],
                "profiledLines": [{
                    "lineNo": element[0],
                    "hits": element[1],
                    "time": element[2] // multiplier,
                } for element in value],
                "unit": stats.unit * multiplier
            })

        stats_dict = {
            "profiledFunctions": profiled_functions,
            # Note that this unit key is for the entire profiling session. It is the original unit of the profilings,
            # not multiplied for a specific profiled function.
            # This is required for backwards compatibility with older versions of the Pycharm Line Profiler plugin
            "unit": stats.unit
        }

        with open(f"{self._stats_filename}.pclprof", 'w') as fp:
            json.dump(stats_dict, fp)


def profile(_func=None, unit=None):
    """Decorator to be used on functions that have to be profiled

    The decorator wraps the `PyCharmLineProfiler`.

    The method detects whether the script is executed with the PyCharm debugger. If this is the case, the function
    will not be wrapped and the original function will be returned. This is done because it is not possible to use
    the PyCharm debugger in combination with the line profiler.

    :param unit: Desired output unit, use 1 for seconds, 1e-3 for milliseconds, 1e-6 for microseconds.
    :param _func: function to profile. This parameter only exists so that the decorator can be used
                    without calling it when no arguments are required.
                    This means that `@profile()` and `@profile` will both work.
                    It is never needed to explicitely set this parameter
    """

    def _profile(func):
        if sys.gettrace() is None:
            return PyCharmLineProfiler.get_instance()(func, unit)
        else:
            # Debugger is active
            # See also https://intellij-support.jetbrains.com/hc/en-us/community/posts/205819799-Way-for-my-Python-code-to-detect-if-it-s-being-run-in-the-debugger-
            return func

    # Make sure the decorator can be used with or without parenthesis
    if _func is None:
        return _profile
    else:
        return _profile(_func)
