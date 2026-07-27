import pytest
import subprocess
import os

@pytest.fixture
def run_cli():
    def _run(args, stdin=""):
        env = os.environ.copy()
        result = subprocess.run(
            ["python", "-m", "sage.main"] + args,
            input=stdin,
            capture_output=True,
            text=True,
            env=env
        )
        return result
    return _run

def test_quadrant_python(run_cli, tmp_path):
    """
    Test the 4-Point Verification Quadrant for Python generated code.
    1. Install (pip install -r requirements.txt)
    2. Build (python -m py_compile main.py)
    3. Run (python main.py)
    4. Tests (pytest test_main.py)

    The files under test MUST be the ones Sage actually generated. This test
    never fabricates them — if Sage produced nothing, the existence assertions
    below fail, which is the correct outcome.
    """
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        stdin = "Create a python calculator app with requirements.txt, main.py, and test_main.py using pytest. It should be fully functional.\n/exit\n"
        res = run_cli(["run"], stdin=stdin)

        assert os.path.exists("requirements.txt"), (
            f"Sage did not generate requirements.txt.\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )
        assert os.path.exists("main.py"), (
            f"Sage did not generate main.py.\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )
        assert os.path.exists("test_main.py"), (
            f"Sage did not generate test_main.py.\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )

        # 1. Install
        inst = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True)
        assert inst.returncode == 0

        # 2. Build / Syntax check
        bld = subprocess.run(["python", "-m", "py_compile", "main.py"], capture_output=True)
        assert bld.returncode == 0

        # 3. Run
        run_res = subprocess.run(["python", "main.py"], capture_output=True)
        assert run_res.returncode == 0

        # 4. Tests
        test_res = subprocess.run(["pytest", "test_main.py"], capture_output=True)
        assert test_res.returncode == 0
    finally:
        os.chdir(original_cwd)

def test_quadrant_node(run_cli, tmp_path):
    """
    Test the 4-Point Verification Quadrant for Node.js generated code.

    As with the Python quadrant, the artifacts under test must be Sage's real
    output — nothing here is fabricated on Sage's behalf.
    """
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        stdin = "Create a Node.js calculator app with package.json, index.js, and index.test.js using jest. It should be fully functional.\n/exit\n"
        res = run_cli(["run"], stdin=stdin)

        assert os.path.exists("package.json"), (
            f"Sage did not generate package.json.\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )
        assert os.path.exists("index.js"), (
            f"Sage did not generate index.js.\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )
        assert os.path.exists("index.test.js"), (
            f"Sage did not generate index.test.js.\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )

        # 1. Install
        inst = subprocess.run(["npm", "install"], capture_output=True)
        assert inst.returncode == 0

        # 2. Build / Syntax check
        bld = subprocess.run(["node", "--check", "index.js"], capture_output=True)
        assert bld.returncode == 0

        # 3. Run
        run_res = subprocess.run(["node", "index.js"], capture_output=True)
        assert run_res.returncode == 0

        # 4. Tests
        test_res = subprocess.run(["npm", "test"], capture_output=True)
        assert test_res.returncode == 0
    finally:
        os.chdir(original_cwd)
