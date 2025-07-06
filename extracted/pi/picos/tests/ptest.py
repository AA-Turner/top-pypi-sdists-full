# ------------------------------------------------------------------------------
# Copyright (C) 2018-2019 Maximilian Stahlberg
#
# This file is part of PICOS Testbench.
#
# PICOS Testbench is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PICOS Testbench is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""A production (optimization) test framework for PICOS.

Production tests are realized via this unittest-derived framework to allow the
same set of optimization problems to be tested using different solvers and
solver options.

:Naming Conventions:

    A *test* is a single test method (e.g. a test of optimality of a primal
    solution), a *test case* is a class containing tests (e.g. an optimization
    problem formulation), and a *test set* is a module containing related test
    cases (e.g. linear optimization problems). Further, a *test suite* is any
    collection of tests.
"""

import importlib
import inspect
import re
import unittest
from copy import copy as builtin_copy
from pathlib import Path

import cvxopt

import picos

PRODUCTION_TEST_PREFIX = "ptest_"


class ProductionTestError(Exception):
    """Base class for production testing specific exceptions."""

    pass


class ProductionTestCase(unittest.TestCase):
    """A test case base class for production (optimization) tests."""

    SLOW = False
    """Whether the test case is considered slow.

    Slow tests can be excluded from a test suite created by
    :func:`makeTestSuite`.
    """

    class Options:
        """Production test customization options.

        A class that contains options shared by all tests in a production test
        suite, such as their verbosity level or numerical precision.
        """

        def __init__(self, verbosity=0, knownFailures=False, objPlaces=6,
                varPlaces=3, solveBoth=False):
            """Create an :class:`Options` object.

            :param int verbosity: Verbosity level, can be used inside the tests
                and gets passed to PICOS.
            :param bool knownFailures: Whether to still run tests known to fail.
            :param int objPlaces: Number of places after the Point to consider
                when comparing objective values.
            :param int varPlaces: Number of places after the Point to consider
                when comparing variable values.
            """
            self.verbosity = verbosity
            self.knownFailures = knownFailures
            self.solveBoth = solveBoth
            self.objPlaces = objPlaces
            self.varPlaces = varPlaces

        def copy(self):
            """Copy the test customization options."""
            return builtin_copy(self)

    def __init__(self, test, solver, solverOptions={}, testOptions=None):
        """Construct a single test parameterized by a solver and solver options.

        The parameterization can be automated with :func:`loadTests`.
        """
        super(ProductionTestCase, self).__init__(test)
        self.solver = solver
        self.options = solverOptions

        # HACK: Give the test a copy of its options to allow a couple of tests
        #       to manipulate the tolerance settings.
        self.to = testOptions.copy() if testOptions else self.Options()

        # Sanity check solver options.
        for forbiddenOption in (
                "solver", "primals", "duals", "verbosity", "license_warnings"):
            if forbiddenOption in solverOptions:
                raise ProductionTestError("Forbidden testing option '{}'."
                    .format(forbiddenOption))

    @classmethod
    def loadTests(cls, tests=None, solvers=picos.solvers.available_solvers(),
            solverOptionSets=[{}], testOptions=None, listSelection=False):
        """Generate a parameterized test suite from this test case.

        This can be seen as a factory method of :class:`ProductionTestCase`,
        except that it creates potentially multiple instances and merges them
        in a :class:`unittest.TestSuite`.

        :param list(str) tests:
            Filter that allows loading only tests with a specific name, such as
            ``"testSolution"``. It is case insensitive and the ``"test"`` prefix
            can be omitted.

        :param list(str) solvers:
            Names of solvers to be tested.

        :param list(set) solverOptionSets:
            Sets of solver options to be tested.

        :pram Options testOptions:
            Production testing options to use.

        :param bool listSelection:
            If :obj:`True`, then only the names of the test methods matching the
            ``tests`` filter are returned.

        :returns:
            A :class:`unittest.TestSuite` containing one copy of every test
            matching ``tests`` for every solver in ``solvers`` and for every set
            of solver options in ``solverOptionSets``.
        """
        # Preprocess the tests filter.
        if tests:
            # Ignore case.
            tests = [test.lower() for test in tests]

            # Temporarily strip prefix, if given.
            tests = [test[4:] if test.startswith("test") else test for test in
                tests]

            # Add back the prefix.
            tests = ["test" + test for test in tests]

        # Select tests (in the form of method names).
        selectedTests = [test for test in
            unittest.TestLoader().getTestCaseNames(cls) if not tests or
            test.lower() in tests]

        if listSelection:
            return selectedTests

        # Assemble the test suite.
        testSuite = unittest.TestSuite()
        for solver in solvers:
            solverSuite = unittest.TestSuite()
            for solverOptions in solverOptionSets:
                for test in selectedTests:
                    solverSuite.addTest(
                        cls(test, solver, solverOptions.copy(), testOptions))
            testSuite.addTest(solverSuite)
        return testSuite

    def optionsToString(self, options):
        """Create a short string for a set of solver options."""
        pairs = []
        for key, val in options.items():
            pairs.append(key + "=" + str(val))
        pairs.sort()
        return ", ".join(pairs)

    def getTestName(self):
        """Produce a test name from the name of the test method."""
        name = self._testMethodName.split("test", 1)[1]
        return " ".join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', name).split())

    def __str__(self):
        """Description of the test as displayed by :package:`unittest`.

        Note that you can use a docstring with your test case to assign a more
        descriptive name to it.
        """
        if self.__doc__:
            # Select first non-empty line of docstring.
            problemName = self.__doc__.split("\n")
            while not problemName[0]:
                problemName.remove("")
            problemName = problemName[0].strip().rstrip(".")
        else:
            problemName = self.__class__.__name__
        solverName = self.solver.upper()
        testName = self.getTestName()
        if self.options:
            optionString = " with {}".format(self.optionsToString(self.options))
        else:
            optionString = ""
        description = "{} ({}): {} [{}{}]".format(problemName,
            self.__class__.__name__, testName, solverName, optionString)
        return description

    def knownFailure(self, solvers):
        """Skip a test if it's known to fail and not our fault."""
        if self.to.knownFailures:
            return

        if isinstance(solvers, str):
            solvers = (solvers,)

        if self.solver in solvers:
            self.skipTest("KNOWN FAILURE")

    def solve(self, problem, primals=True, duals=True):
        """Solve a PICOS optimization problem.

        Produces a primal/dual solution pair for the given problem, using the
        selected solver, verbosity, and set of options.

        If ``primals=None`` or ``duals=None``, then the solver is not told to
        not produce the respective solution, but its presence is not checked.
        """
        options = self.options.copy()

        options["solver"]           = self.solver
        options["verbosity"]        = self.to.verbosity
        options["primals"]          = primals
        options["duals"]            = duals
        options["license_warnings"] = False

        problem.options.update(**options)

        try:
            solution = problem.solve()
        except picos.SolutionFailure as error:
            if error.code == 1:  # No strategy found.
                self.skipTest("No strategy found")
            else:
                # Mimic "raise from None" with self.fail.
                solutionError = error.message if error.message \
                    else "Code {}.".format(error.code)
        except Exception as error:
            descr = str(error)

            if "Model too large for size-limited license" in descr:  # Gurobi
                self.skipTest("LICENSE INSUFFICIENT")
            elif "rescode.err_server_problem_size(8008)" in descr:  # MOSEK
                self.skipTest("TOO LARGE FOR PUBLIC SERVER")
            else:
                raise
        else:
            solutionError = None

        if solutionError:
            self.fail("Solution failed: {}".format(solutionError))

        if isinstance(solution, list):
            if not solution:
                self.fail("No solution returned.")
            else:
                solution = solution[0]

        if primals and not solution.primals:
            self.fail("No primal solution returned.")

        if duals and not solution.duals:
            self.fail("No dual solution returned.")

        return solution

    def primalSolve(self, problem):
        """Solve only the primal of a PICOS optimization problem.

        Produces a primal solution for the given problem, using the selected
        solver, verbosity, and set of options.
        """
        sol = self.solve(problem, duals=(None if self.to.solveBoth else False))
        assert sol.primalStatus == picos.modeling.solution.SS_OPTIMAL

        # The solver claims primal optimality, so check feasibility.
        try:
            infeasibility = problem.check_current_value_feasibility()[1]
        except picos.uncertain.IntractableWorstCase:
            pass
        else:
            infeasibility = infeasibility if infeasibility else 0
            self.assertAlmostEqual(infeasibility, 0, self.to.objPlaces,
                msg="Primal solution claimed optimal but found infeasible.")

    def dualSolve(self, problem):
        """Solve only the primal of a PICOS optimization problem.

        Produces a dual solution for the given problem, using the selected
        solver, verbosity, and set of options.
        """
        self.solve(problem, primals=(None if self.to.solveBoth else False))

    def infeasibleSolve(self, problem):
        """Attempt to solve a problem supposed to be infeasible."""
        solution = self.solve(problem, primals=None, duals=None)

        if solution.problemStatus not in (
                picos.modeling.solution.PS_INFEASIBLE,
                picos.modeling.solution.PS_INF_OR_UNB):
            self.fail("The problem was not detected to be infeasible; problem "
                "state is '{}'.".format(solution.problemStatus))

        return solution

    def unboundedSolve(self, problem):
        """Attempt to solve a problem supposed to be unbounded."""
        solution = self.solve(problem, primals=None, duals=None)

        if solution.problemStatus not in (
                picos.modeling.solution.PS_UNBOUNDED,
                picos.modeling.solution.PS_INF_OR_UNB):
            self.fail("The problem was not detected to be unbounded; problem "
                "state is '{}'.".format(solution.problemStatus))

        return solution

    def assertAlmostEqual(self, first, second, places, msg=None, delta=None):
        """Assert tha two numeric entities are almost equal.

        A wrapper around :func:`unittest.TestCase.assertAlmostEqual` that allows
        comparison of :class:`cvxopt.matrix` matrices.
        """
        if isinstance(first, (int, float)) and isinstance(second, (int, float)):
            super(ProductionTestCase, self).assertAlmostEqual(
                first, second, places, msg, delta)
        else:
            firstMatrix = isinstance(first, cvxopt.matrix)
            secondMatrix = isinstance(second, cvxopt.matrix)

            if firstMatrix and secondMatrix:
                pass
            elif firstMatrix and not secondMatrix:
                second = cvxopt.matrix(second)
            elif not firstMatrix and secondMatrix:
                first = cvxopt.matrix(first)
            else:
                raise TypeError(
                    "Expecting one argument to be a CVXOPT matrix.")

            self.assertEqual(first.size, second.size)

            for i in range(len(first)):
                super(ProductionTestCase, self).assertAlmostEqual(
                    first[i], second[i], places, msg, delta)

    def readDual(self, constraint, variable):
        """Read a dual value from a constraint into a variable."""
        dual = constraint.dual
        self.assertIsNotNone(dual,
            msg="No dual value for {}.".format(constraint))
        try:
            dualLen = len(dual)
        except TypeError:
            dualLen = 1
        self.assertEqual(dualLen, len(variable),
            msg="Dual of incompatible size.")
        variable.set_value(dual)

    def readDuals(self, constraint, *variables):
        """Read dual values from a constraint into a number of variables."""
        dual = constraint.dual
        self.assertIsNotNone(dual,
            msg="No dual value for {}.".format(constraint))
        try:
            dualLen = len(dual)
        except TypeError:
            dualLen = 1
        self.assertEqual(dualLen, sum(len(var) for var in variables),
            msg="Dual of incompatible size.")
        varIndex = 0
        for variable in variables:
            nextVarIndex = varIndex + len(variable)
            variable.set_value(dual[varIndex:nextVarIndex])
            varIndex = nextVarIndex

    def expectObjective(self, problem, should, by_picos=True, by_solver=None):
        """Assert that the objective value of a problem is as expected.

        :param ~picos.Problem problem:
            The optimization problem to check.

        :param float should:
            The exact optimal value.

        :param bool by_picos:
            Whether to check the optimal value as computed by PICOS.

         :param bool by_solver:
            Whether to check the optimal value as reported by the solver. If
            this is :obj:`None`, then the test is skipped if no solution object
            is associated with the problem or if the associated solution object
            reports the objective value as :obj:`None` (but the test is still
            performed whenever the solver does report a value).
        """
        if by_picos:
            obj_value = problem.value

            self.assertIsNotNone(obj_value, msg="Objective value.")

            self.assertAlmostEqual(obj_value, should, self.to.objPlaces,
                msg="Objective value.")

        if by_solver:
            self.assertIsNotNone(problem.last_solution,
                msg="No solution object was attached to the problem.")

            self.assertIsNotNone(problem.last_solution.reported_value,
                msg="The solver did not report an objective value.")

        if by_solver or (
                by_solver is None
                and problem.last_solution is not None
                and problem.last_solution.reported_value is not None):
            self.assertAlmostEqual(
                problem.last_solution.reported_value, should, self.to.objPlaces,
                msg="Objective value reported by solver.")

    def expectVariable(self, variable, should):
        """Assert that a variable has a certain value.

        Note that solvers might terminate as soon as the objective value gap is
        small while the distances of (dual) variables from their exact and
        unique solution can be much larger (but cancel out with respect to the
        objective function value). This is circumvented with some probability by
        using a lower numeric precision for variable checks by default.
        """
        if hasattr(should, "__len__"):
            self.assertEqual(len(variable), len(should),
                msg="Variable of incompatible size.")
        self.assertAlmostEqual(variable.value, should, self.to.varPlaces,
            msg="Variable {}.".format(variable.name))

    def expectExpression(self, expression, should):
        """Assert that an expression has a certain value."""
        if hasattr(should, "__len__"):
            self.assertEqual(len(expression), len(should),
                msg="Expression of incompatible size.")
        self.assertAlmostEqual(expression.value, should, self.to.varPlaces,
            msg="Expression {}.".format(expression.string))

    def expectSlack(self, constraint, should):
        """Assert that a constraint has a certain slack value."""
        if hasattr(should, "__len__"):
            self.assertEqual(len(constraint), len(should),
                msg="Slack of incompatible size.")
        self.assertAlmostEqual(constraint.slack, should, self.to.varPlaces,
            msg="Slack of {}.".format(constraint))


def availableTestSets():
    """Return the names of all available production test sets."""
    testSets = []

    for testFile in Path(__file__).parent.iterdir():
        if not testFile.suffix == ".py":
            continue

        if not testFile.stem.startswith(PRODUCTION_TEST_PREFIX):
            continue

        testSetName = testFile.stem.split(PRODUCTION_TEST_PREFIX, 1)[1]
        testSets.append(testSetName)
    return testSets


def makeTestSuite(testSetFilter=None, testCaseFilter=None, testNameFilter=None,
        slowTests=True, solvers=picos.solvers.available_solvers(),
        solverOptionSets=[{}], testOptions=None, listSelection=False):
    """Create a parameterized production test suite.

    This collects :class:`ProductionTestCase` implementations (test cases) over
    multiple files (test sets) and creates a test suite of parameterized tests
    from them.

    Defaults to collect all tests for all solvers and with default options.
    With the ``listSelection`` switch, all selected test sets, test cases, and
    tests are returned, which can be used to generate a list of all available
    filter options (by leaving all filters blank).

    :param list(str) testSetFilter:
        Collection of test set names to select.

    :param list(str) testCaseFilter:
        Collection of test case names to select.

    :param list(str) testNameFilter:
        Collection of test names to select.

    :param bool slowTests:
        Whether to also include test cases marked as slow. This parameter is
        ignored in case a ``testCaseFilter`` is specified.

    :param list(str) solvers:
        Solvers to test with.

    :param dict(set) solverOptionSets:
        Sets of solver options to test with.

    :param ProductionTestCase.Options testOptions:
        Production test options to use.

    :param bool listSelection:
        Whether to return a triple ``(sets, cases, names)`` with sorted names of
        selected test sets, cases, and tests.

    :returns:
        A :class:`unittest.TestSuite` containing one copy of every production
        test matching ``tests`` in test cases matching ``testCases`` in test
        sets matching ``testSets`` for every solver in ``solvers`` and for every
        set of solver options in ``solverOptionSets``.
    """
    testSuite = unittest.TestSuite()

    # Ignore case for all filters handled in this method.
    if testSetFilter:
        testSetFilter = [testSet.lower() for testSet in testSetFilter]
    if testCaseFilter:
        testCaseFilter = [testCase.lower() for testCase in testCaseFilter]

    # Select test sets (in the form of string names).
    selectedSets = [testSet for testSet in availableTestSets()
        if not testSetFilter or testSet.lower() in testSetFilter]

    if listSelection:
        setList  = set(selectedSets)
        caseList = set()
        testList = set()

    for testSet in selectedSets:
        # Load the test set (as a module).
        testSetModuleName = PRODUCTION_TEST_PREFIX + testSet
        testSetModule = importlib.import_module(
            "." + testSetModuleName, package=__package__)

        # Select test cases (in the form of classes).
        selectedCases = [
            testCase for testCaseName, testCase
            in inspect.getmembers(testSetModule, inspect.isclass)
            if issubclass(testCase, ProductionTestCase)
            and testCase is not ProductionTestCase
            and (not testCaseFilter or testCaseName.lower() in testCaseFilter)
            and (testCaseFilter or slowTests or not testCase.SLOW)]

        if listSelection:
            caseList.update([testCase.__name__ for testCase in selectedCases])

        for testCase in selectedCases:
            if listSelection:
                testList.update(testCase.loadTests(listSelection=True))
            else:
                # Add all tests with matching names from the test case.
                testSuite.addTest(testCase.loadTests(
                    testNameFilter, solvers, solverOptionSets, testOptions))

    if listSelection:
        return sorted(setList), sorted(caseList), sorted(testList)

    return testSuite
