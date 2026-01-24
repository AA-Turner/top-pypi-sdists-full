import shutil
from pathlib import Path

from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.build_py import build_py


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self):
        return True


class BuildPyWithExtension(build_py):
    """Custom build command that copies the Chrome extension into the package.     """

    def run(self):
        # Copy extension to package directory before building
        # This ensures it gets included in the wheel via package-data
        setup_dir = Path(__file__).resolve().parent
        repo_root = setup_dir.parent
        extension_source = repo_root / "extensions" / "envgen-recorder"
        extension_dest = setup_dir / "src" / "plato" / "extensions" / "envgen-recorder"

        if extension_source.exists():
            # Create destination directory
            extension_dest.parent.mkdir(parents=True, exist_ok=True)
            # Remove existing if present
            if extension_dest.exists():
                shutil.rmtree(extension_dest)
            # Copy extension (exclude node_modules and other build artifacts)
            shutil.copytree(
                extension_source,
                extension_dest,
                ignore=shutil.ignore_patterns("node_modules", "__pycache__", "*.pyc", ".git"),
            )
            print(f"✅ Copied extension from {extension_source} to {extension_dest}")
        else:
            print(f"⚠️  Warning: Extension not found at {extension_source}")

        # Run the standard build
        super().run()


setup(
    distclass=BinaryDistribution,
    cmdclass={"build_py": BuildPyWithExtension},
)
