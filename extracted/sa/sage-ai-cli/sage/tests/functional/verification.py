import os
import subprocess
import shutil
from pathlib import Path

class VerificationQuadrantHarness:
    """
    4-Point Verification Quadrant (AI Capabilities Validation)
    1. install_ok: Dependencies install successfully.
    2. build_ok: Code compiles cleanly.
    3. run_ok: Program boots without exceptions.
    4. tests_ok: Sage generated self-tests and they pass.
    """

    def verify_quadrant(self, project_path: Path, language: str) -> bool:
        """
        Executes all 4 steps of the verification quadrant based on the language.
        Returns True if all steps pass. Raises assertions if they fail.
        """
        assert project_path.exists() and project_path.is_dir(), "Project path does not exist."

        if language == "python":
            self._verify_python(project_path)
        elif language == "node" or language == "typescript":
            self._verify_node(project_path)
        elif language == "rust":
            self._verify_rust(project_path)
        else:
            # Generic fallback or throw unimplemented
            raise NotImplementedError(f"Verification for language {language} is not yet implemented in harness.")

        return True

    def _verify_python(self, path: Path):
        # 1. install_ok
        if (path / "requirements.txt").exists():
            res = subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=path, capture_output=True)
            assert res.returncode == 0, f"install_ok failed: {res.stderr.decode('utf-8')}"
        elif (path / "pyproject.toml").exists():
            res = subprocess.run(["pip", "install", "."], cwd=path, capture_output=True)
            assert res.returncode == 0, f"install_ok failed: {res.stderr.decode('utf-8')}"
        
        # 2. build_ok
        res = subprocess.run(["python", "-m", "py_compile", "main.py"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"build_ok failed (compilation): {res.stderr.decode('utf-8')}"

        # 3. run_ok
        res = subprocess.run(["python", "main.py", "--help"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"run_ok failed: {res.stderr.decode('utf-8')}"

        # 4. tests_ok
        # Assume pytest is used for python generated tests
        res = subprocess.run(["pytest"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"tests_ok failed: {res.stderr.decode('utf-8')}"

    def _verify_node(self, path: Path):
        # 1. install_ok
        res = subprocess.run(["npm", "install"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"install_ok failed: {res.stderr.decode('utf-8')}"

        # 2. build_ok
        if (path / "tsconfig.json").exists():
            res = subprocess.run(["npm", "run", "build"], cwd=path, capture_output=True)
            assert res.returncode == 0, f"build_ok failed: {res.stderr.decode('utf-8')}"

        # 3. run_ok
        # Try to run node index.js or npm start
        if (path / "index.js").exists():
            res = subprocess.run(["node", "index.js", "--help"], cwd=path, capture_output=True)
        else:
            res = subprocess.run(["npm", "start", "--", "--help"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"run_ok failed: {res.stderr.decode('utf-8')}"

        # 4. tests_ok
        res = subprocess.run(["npm", "test"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"tests_ok failed: {res.stderr.decode('utf-8')}"

    def _verify_rust(self, path: Path):
        # 1. install_ok (Cargo handles deps on build, but we can cargo fetch)
        res = subprocess.run(["cargo", "fetch"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"install_ok failed: {res.stderr.decode('utf-8')}"

        # 2. build_ok
        res = subprocess.run(["cargo", "build"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"build_ok failed: {res.stderr.decode('utf-8')}"

        # 3. run_ok
        res = subprocess.run(["cargo", "run", "--", "--help"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"run_ok failed: {res.stderr.decode('utf-8')}"

        # 4. tests_ok
        res = subprocess.run(["cargo", "test"], cwd=path, capture_output=True)
        assert res.returncode == 0, f"tests_ok failed: {res.stderr.decode('utf-8')}"
