"""
Spark JAR dependencies for Snowpark Connect (Part 1).

This package contains Apache Spark 3.5.6 framework JARs.
"""
from pathlib import Path
from typing import List

__version__ = "3.56.2"


def get_jars_dir() -> Path:
    """Get the path to the JARs directory."""
    jars_dir = Path(__file__).parent / "jars"
    if not jars_dir.exists():
        raise RuntimeError(
            f"JARs directory not found at {jars_dir}. "
            "The snowpark-connect-deps-1 package may be incorrectly installed."
        )
    return jars_dir


def list_jars() -> List[Path]:
    """List all available JAR files."""
    jars_dir = get_jars_dir()
    return sorted(jars_dir.glob("*.jar"))


def get_jar_path(jar_name: str) -> Path:
    """Get the path to a specific JAR file."""
    jar_path = get_jars_dir() / jar_name
    if not jar_path.exists():
        raise FileNotFoundError(f"JAR file '{jar_name}' not found in package 1. ")
    return jar_path
