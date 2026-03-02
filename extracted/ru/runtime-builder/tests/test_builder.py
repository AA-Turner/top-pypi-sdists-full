from pathlib import Path

import shutil
import subprocess
import tempfile


def copy_template(dst: Path, src_name: Path):
    my_path = Path(__file__).parent.resolve()
    project_template_path = my_path / src_name
    shutil.copytree(project_template_path, dst, dirs_exist_ok=True)


def run_shell_test(script_name: str, src_name: Path):
    with tempfile.TemporaryDirectory() as dest:
        dest = Path(dest)
        copy_template(dest, src_name)
        with open(dest / "RUNTIME_BUILDER_ROOT.env", "w") as f:
            f.write(str(Path(__file__).parent.parent))
        command = str(dest / script_name)
        result = subprocess.run(command, shell=True, cwd=dest)
    assert result.returncode == 0


def test_enscons_build():
    run_shell_test("test_pip_install.sh", "project_template_enscons")


def test_enscons_build_editable():
    run_shell_test("test_pip_install_editable.sh", "project_template_enscons")


def test_setuptools_build():
    run_shell_test("test_pip_install.sh", "project_template_setuptools")


def test_setuptools_build_editable():
    run_shell_test("test_pip_install_editable.sh", "project_template_setuptools")


"""
v0.1.3 and prior have a bug where if wheel A uses wheel B and both use
runtime_builder then when A is installed, the use of B fails. These "two_wheel"
tests cover this case.
"""


def test_two_wheels_build():
    run_shell_test("test_pip_install.sh", "two_wheels")


def test_two_wheels_build_editable():
    run_shell_test("test_pip_install_editable.sh", "two_wheels")
