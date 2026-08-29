#  testscenarios: extensions to python unittest to allow declarative
#  dependency injection ('scenarios') by tests.
#
# Copyright (c) 2009, Robert Collins <robertc@robertcollins.net>
#
# Licensed under either the Apache License, Version 2.0 or the BSD 3-clause
# license at the users choice. A copy of both licenses are available in the
# project source as Apache-2.0 and BSD. You may not use this file except in
# compliance with one of these two licences.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under these licenses is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# license you chose for the specific language governing permissions and
# limitations under that license.

__all__ = [
    "TestWithScenarios",
    "WithScenarios",
]

import unittest
from typing import TYPE_CHECKING

from testscenarios.scenarios import Scenario, generate_scenarios

# WithScenarios is a mixin that is always combined with unittest.TestCase (and
# calls up to it via super()). At runtime it must subclass ``object`` so it can
# be mixed in freely, but for type checking we treat the base as TestCase so
# that ``super()`` calls and inherited attributes resolve correctly.
if TYPE_CHECKING:
    _Base = unittest.TestCase
else:
    _Base = object

_doc = """
    When a test object which inherits from WithScenarios is run, and there is a
    non-empty scenarios attribute on the object, the test is multiplied by the
    run method into one test per scenario. For this to work reliably the
    WithScenarios.run method must not be overriden in a subclass (or overridden
    compatibly with WithScenarios).
    """


class WithScenarios(_Base):
    __doc__ = (
        """A mixin for TestCase with support for declarative scenarios.
    """
        + _doc
    )

    def _get_scenarios(self) -> list[Scenario] | None:
        return getattr(self, "scenarios", None)

    def countTestCases(self) -> int:
        scenarios = self._get_scenarios()
        if not scenarios:
            return 1
        else:
            return len(scenarios)

    def debug(self) -> None:
        scenarios = self._get_scenarios()
        if scenarios:
            for test in generate_scenarios(self):
                test.debug()
        else:
            return super().debug()

    def run(
        self, result: unittest.TestResult | None = None
    ) -> unittest.TestResult | None:
        scenarios = self._get_scenarios()
        if scenarios:
            for test in generate_scenarios(self):
                test.run(result)
            return None
        else:
            return super().run(result)


class TestWithScenarios(WithScenarios, unittest.TestCase):
    __doc__ = (
        """Unittest TestCase with support for declarative scenarios.
    """
        + _doc
    )
