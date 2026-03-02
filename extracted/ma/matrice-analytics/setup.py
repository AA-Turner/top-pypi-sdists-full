import os
import shutil
import subprocess
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist

# Configuration of package name and source directory
PACKAGE_NAME = "matrice_analytics"
SOURCE_DIR = f"src/{PACKAGE_NAME}"
OBFUSCATED_DIR = f"{PACKAGE_NAME}_obfuscated"
BUILD_DIR = "build"

# Read version from appropriate version file based on environment
def get_version():
    """Get version based on environment or git branch.
    If environment is dev, append 'dev' suffix automatically."""
    # Check environment variable first (set by CI/CD)
    env_type = os.environ.get('BUILD_ENV', '').lower()
    append_dev_suffix = False
    
    if env_type == 'dev':
        version_file = "version-dev.txt"
        append_dev_suffix = True
    elif env_type == 'staging':
        version_file = "version-staging.txt"
    elif env_type == 'prod':
        version_file = "version-prod.txt"
    else:
        # Try to detect from git branch
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            branch = result.stdout.strip()
            
            if branch == 'dev':
                version_file = "version-dev.txt"
                append_dev_suffix = True
            elif branch == 'staging':
                version_file = "version-staging.txt"
            elif branch in ['main', 'master', 'prod']:
                version_file = "version-prod.txt"
            else:
                # Default to dev for unknown branches
                version_file = "version-dev.txt"
                append_dev_suffix = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Default to dev if git detection fails
            version_file = "version-dev.txt"
            append_dev_suffix = True
    
    # Read the determined version file
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            version = f.read().strip()
            if append_dev_suffix and not version.endswith("dev"):
                version = f"{version}dev"
            print(f"Using version {version} from {version_file}")
            return version
    except FileNotFoundError:
        raise FileNotFoundError(f"Version file not found: {version_file}")

VERSION = get_version()

class PyArmorBuild(_build_py):
    """Custom build_py to obfuscate Python files using PyArmor."""
    
    def run(self):
        try:
            # Clean up previous obfuscated files
            if os.path.exists(OBFUSCATED_DIR):
                shutil.rmtree(OBFUSCATED_DIR)
            
            # Run PyArmor obfuscation
            self._obfuscate_package()
            
            # Copy obfuscated files to build directory
            self._copy_obfuscated_files()
            
        except Exception as e:
            print(f"Error in PyArmorBuild: {e}")
            raise
    
    def _obfuscate_package(self):
        """Obfuscate the package using PyArmor."""
        print(f"Obfuscating package {PACKAGE_NAME}...")
        
        # Check if we should skip obfuscation
        skip_obfuscation = os.environ.get('SKIP_PYARMOR_OBFUSCATION', '').lower() == 'true'
        if skip_obfuscation:
            print("⚠ Skipping PyArmor obfuscation (SKIP_PYARMOR_OBFUSCATION=true)")
            self._copy_source_files()
            return
        
        # Create output directory
        os.makedirs(OBFUSCATED_DIR, exist_ok=True)
        
        # Try obfuscating core files first (most important)
        core_files = self._get_core_files()
        if core_files:
            print(f"Attempting to obfuscate {len(core_files)} core files first...")
            success = self._obfuscate_selective(core_files)
            if not success:
                print("⚠ Core file obfuscation failed, falling back to copying source files")
                self._copy_source_files()
                return
        
        # Try full obfuscation
        cmd = [
            "pyarmor",
            "gen",
            "--output", OBFUSCATED_DIR,
            SOURCE_DIR
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✓ PyArmor obfuscation completed successfully")
            if result.stdout:
                print(f"PyArmor output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or str(e)
            print(f"⚠ PyArmor obfuscation failed: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            
            # Handle specific license limitation error
            if "out of license" in error_msg or "license" in error_msg.lower():
                print("\n" + "="*60)
                print("PyArmor Trial License Limitation Detected")
                print("="*60)
                print("The free trial version of PyArmor has a file limit.")
                print("Your package has too many files to obfuscate with the trial version.")
                print("\nOptions to resolve this:")
                print("1. Purchase a PyArmor license: https://pyarmor.readthedocs.io/en/stable/licenses.html")
                print("2. Reduce the number of files (exclude test files, examples, etc.)")
                print("3. Set environment variable: SKIP_PYARMOR_OBFUSCATION=true")
                print("4. Use selective obfuscation of core files only")
                print("="*60)
                
                # Fall back to copying source files without obfuscation
                print("Falling back to building package without obfuscation...")
                self._copy_source_files()
                return
            else:
                raise
        except FileNotFoundError:
            print("PyArmor not found. Please install PyArmor: pip install pyarmor")
            raise
    
    def _get_core_files(self):
        """Get list of core files to obfuscate (excluding tests, examples)."""
        core_files = []
        if not os.path.exists(SOURCE_DIR):
            return core_files
            
        for root, dirs, files in os.walk(SOURCE_DIR):
            # Skip test directories and other non-essential directories
            dirs[:] = [d for d in dirs if not d.startswith(('test', '__pycache__', 'example', 'demo'))]
            
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    core_files.append(os.path.join(root, file))
        
        return core_files
    
    def _obfuscate_selective(self, file_list):
        """Obfuscate only selected files."""
        print(f"Attempting selective obfuscation of {len(file_list)} files...")
        
        # Create a temporary directory with only core files
        temp_source = f"{SOURCE_DIR}_temp"
        try:
            if os.path.exists(temp_source):
                shutil.rmtree(temp_source)
            
            # Copy only core files maintaining structure
            for file_path in file_list:
                rel_path = os.path.relpath(file_path, SOURCE_DIR)
                dest_path = os.path.join(temp_source, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)
            
            # Try to obfuscate the reduced set
            cmd = ["pyarmor", "gen", "--output", OBFUSCATED_DIR, temp_source]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✓ Selective obfuscation completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Selective obfuscation also failed: {e}")
            return False
        finally:
            if os.path.exists(temp_source):
                shutil.rmtree(temp_source)
    
    def _copy_source_files(self):
        """Copy source files without obfuscation as fallback."""
        print("Copying source files without obfuscation...")
        
        if os.path.exists(SOURCE_DIR):
            dest_package_dir = os.path.join(OBFUSCATED_DIR, PACKAGE_NAME)
            if os.path.exists(dest_package_dir):
                shutil.rmtree(dest_package_dir)
            shutil.copytree(SOURCE_DIR, dest_package_dir)
            print(f"✓ Source files copied to {dest_package_dir}")
        else:
            print(f"✗ Source directory not found: {SOURCE_DIR}")
    
    def _copy_obfuscated_files(self):
        """Copy obfuscated files to build directory."""
        build_package_dir = os.path.join(self.build_lib, PACKAGE_NAME)
        os.makedirs(build_package_dir, exist_ok=True)
        
        # Find the obfuscated package directory
        obfuscated_package_dir = None
        for root, dirs, files in os.walk(OBFUSCATED_DIR):
            if PACKAGE_NAME in dirs:
                obfuscated_package_dir = os.path.join(root, PACKAGE_NAME)
                break
        
        if not obfuscated_package_dir:
            # Try direct path if PyArmor created it differently
            obfuscated_package_dir = os.path.join(OBFUSCATED_DIR, PACKAGE_NAME)
        
        if os.path.exists(obfuscated_package_dir):
            # Copy all obfuscated files
            for root, dirs, files in os.walk(obfuscated_package_dir):
                for file in files:
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, obfuscated_package_dir)
                    dest_path = os.path.join(build_package_dir, rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(src_path, dest_path)
            
            print(f"Copied obfuscated files to {build_package_dir}")
        else:
            print(f"Warning: Obfuscated package directory not found at {obfuscated_package_dir}")
            print(f"Available directories in {OBFUSCATED_DIR}:")
            if os.path.exists(OBFUSCATED_DIR):
                for item in os.listdir(OBFUSCATED_DIR):
                    print(f"  - {item}")

class PyArmorSdist(_sdist):
    """Custom sdist to include obfuscated files."""
    
    def run(self):
        try:
            # Run the build command first to generate obfuscated files
            self.run_command("build_py")
            super().run()
        except Exception as e:
            print(f"Error in PyArmorSdist: {e}")
            raise

def find_original_packages():
    """Find packages in the original source directory."""
    packages = []
    source_path = Path(SOURCE_DIR)
    if source_path.exists():
        for py_file in source_path.rglob("__init__.py"):
            package_dir = py_file.parent
            rel_path = package_dir.relative_to(SOURCE_DIR)
            if rel_path == Path("."):
                packages.append(PACKAGE_NAME)
            else:
                packages.append(f"{PACKAGE_NAME}.{str(rel_path).replace(os.sep, '.')}")
    return packages

def get_package_data():
    """Get package data for obfuscated files."""
    return {
        PACKAGE_NAME: [
            "*.py",
            "*.pyi", 
            "*.pyx",
            "*.so",
            "*.pyd",
            "py.typed",
            "**/*.py",
            "**/*.pyi",
            "**/*.pyx", 
            "**/*.so",
            "**/*.pyd",
            "**/py.typed",
            "pytransform/*",
            "**/*",
        ],
    }

# Ensure py.typed exists for type hints
def ensure_py_typed():
    """Create py.typed file if it doesn't exist."""
    src_py_typed = os.path.join(SOURCE_DIR, "py.typed")
    if not os.path.exists(src_py_typed):
        with open(src_py_typed, "w") as f:
            f.write("")
        print("Created py.typed file")

# Create py.typed file
ensure_py_typed()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_original_packages(),
    package_dir={PACKAGE_NAME: SOURCE_DIR},
    include_package_data=True,
    package_data=get_package_data(),
    cmdclass={
        'build_py': PyArmorBuild,
        'sdist': PyArmorSdist,
    },
    zip_safe=False,
    python_requires=">=3.8",
    setup_requires=[
        "pyarmor>=8.0.0",
    ],
)