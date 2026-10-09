"""Validate resources and run tests against an installed distribution."""

import json
import subprocess
import sys
from importlib import resources
from pathlib import Path

import stjames

# Running outside the checkout must load the installed package, including its doctests.
assert Path(stjames.__file__).parent.parent.name == "site-packages", stjames.__file__
package = resources.files("stjames")
assert package.joinpath("py.typed").is_file()
for name in ("bragg_radii.json", "isotopes.json", "nist_isotopes.json", "symbol_element.json"):
    assert json.loads(package.joinpath("data", name).read_text())

subprocess.run([sys.executable, "-m", "pytest", "--pyargs", "stjames", "tests"], check=True)
