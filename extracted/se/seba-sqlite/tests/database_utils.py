import contextlib
import logging
import os
import random
import shutil
import tempfile
from datetime import datetime

from seba_sqlite import Database


def relpath(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def tmpdir(path, teardown=True):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            with tmp(path, teardown=teardown):
                return function(*args, **kwargs)

        return wrapper

    return real_decorator


@contextlib.contextmanager
def tmp(path=None, teardown=True):
    """Create and go into tmp directory, returns the path.
    This function creates a temporary directory and enters that directory.  The
    returned object is the path to the created directory.
    If @path is not specified, we create an empty directory, otherwise, it must
    be a path to an existing directory. In that case, the directory will be
    copied into the temporary directory.
    If @teardown is True (defaults to True), the directory is (attempted)
    deleted after context, otherwise it is kept as is.
    """
    cwd = os.getcwd()
    fname = tempfile.NamedTemporaryFile().name

    if path:
        if not os.path.isdir(path):
            logging.debug("tmp:raise no such path")
            raise IOError("No such directory: %s" % path)
        shutil.copytree(path, fname)
    else:
        # no path to copy, create empty dir
        os.mkdir(fname)

    os.chdir(fname)

    yield fname  # give control to caller scope

    os.chdir(cwd)

    if teardown:
        try:
            shutil.rmtree(fname)
        except OSError as oserr:
            logging.debug("tmp:rmtree failed %s (%s)", fname, oserr)
            shutil.rmtree(fname, ignore_errors=True)


_CONTROLS = [
    "control1",
    "control2",
    "control3",
    "control4",
    "control5",
    "control6",
    "control7",
    "control8",
    "control9",
    "control10",
    "control11",
    "control12",
]
_FUNCTIONS = [
    "ObjectiveFunction1",
    "ObjectiveFunction2",
    "ConstraintFunction1",
]
_REALIZATIONS = [
    "realization1",
    "realization2",
    "realization3",
    "realization4",
    "realization5",
    "realization6",
    "realization7",
    "realization8",
    "realization9",
    "realization10",
    "realization11",
    "realization12",
]

_REALIZATION_WEIGHTS = [1.0 / len(_REALIZATIONS)] * len(_REALIZATIONS)
_EXPERIMENT_NAME = "Test Experiment"
_NUMBER_OF_SIMULATIONS = 5
_NUMBER_OF_BATCHES = 10
_EXISTING_FUNCTION_NAME = "Existing function"
_EXISTING_SIMULATION_NAME = "Existing simulation"


# This could use some refactoring, but since its just a test, leave it.
def load_info_to_db(database, **kwargs):
    plain_names = ["Batch"]
    special = ["Function", "Simulation", "control_definition"]
    function_type_sequence = ["OBJECTIVE", "CONSTRAINT"]

    # first is the experiment:
    if "Experiment" in kwargs:
        fun = getattr(Database, "add_experiment")
        for value in kwargs.pop("Experiment"):
            fun(database, value, datetime.now())
    if "Realization" in kwargs:
        fun = getattr(Database, "add_realization")
        for name, weight in kwargs.pop("Realization"):
            fun(database, name, weight)
    func_names = kwargs.get("dict_order", kwargs.keys())
    for name in func_names:
        fun = getattr(Database, "add_{}".format(name.lower()))
        if name in plain_names:
            for value in kwargs[name]:
                fun(database)
        elif name == special[0]:
            for value in kwargs[name]:
                input_values = {
                    "name": value,
                    "function_type": random.choice(function_type_sequence),
                    "weight": random.uniform(1.0, 2.0),
                    "normalization": random.uniform(1.0, 2.0),
                    "rhs_value": random.uniform(0.0, 0.5),
                    "constraint_type": None,
                }
                fun(database, **input_values)
        elif name == special[1]:
            for value in kwargs[name]:
                input_values = {
                    "realization_name": value[0],
                    "set_id": value[1],
                    "sim_name": value[2],
                    "is_gradient": False,
                }
                fun(database, **input_values)
        elif name == special[2]:
            for value in kwargs[name]:
                input_values = {
                    "name": value,
                    "init_value": random.uniform(1.0, 2.0),
                    "min_value": random.uniform(0.5, 1.5),
                    "max_value": random.uniform(1.5, 2.5),
                }
                fun(database, **input_values)
