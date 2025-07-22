import importlib
import subprocess
import sys
import os
import glob

# def cleanup_init_files():
#     """Remove all __init__.py files from the copied ./app/ directory in the current working directory."""
#     print("🧹 Cleaning up __init__.py files...")
    
#     # Get the app directory in the current working directory
#     app_dir = os.path.join(os.getcwd(), "app")
    
#     # Find all __init__.py files in app/ and subdirectories
#     init_files = glob.glob(os.path.join(app_dir, "**", "__init__.py"), recursive=True)
    
#     if not init_files:
#         print("✓ No __init__.py files found to clean up")
#         return
    
#     deleted_count = 0
#     for init_file in init_files:
#         try:
#             os.remove(init_file)
#             print(f"🗑️  Deleted: {os.path.relpath(init_file, app_dir)}")
#             deleted_count += 1
#         except OSError as e:
#             print(f"⚠️  Could not delete {init_file}: {e}")
    
#     print(f"✅ Cleaned up {deleted_count} __init__.py files")

def get_install_command(installer, package_name):
    """Get the appropriate install command based on the installer."""
    if installer == "uv":
        return ["uv", "pip", "install", package_name]
    elif installer == "conda":
        return ["conda", "install", "-y", package_name]
    else:  # pip (default)
        return [sys.executable, "-m", "pip", "install", package_name]

def ensure_package(pkg_name, pip_name=None, installer="pip"):
    """Ensure a package is installed, install it if missing."""
    try:
        importlib.import_module(pkg_name)
        print(f"✓ Package '{pkg_name}' is already installed")
    except ImportError:
        print(f"📦 Package '{pkg_name}' not found. Installing with {installer}...")
        try:
            package_to_install = pip_name or pkg_name
            install_cmd = get_install_command(installer, package_to_install)
            subprocess.check_call(install_cmd)
            print(f"✓ Successfully installed '{pkg_name}' using {installer}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install '{pkg_name}' with {installer}: {e}")
            raise

def ensure_embedding_dependencies(installer="pip"):
    """Ensure all required embedding packages are installed."""
    print("🔍 Checking embedding dependencies...")
    
    # Core embedding packages
    ensure_package("transformers", installer=installer)
    ensure_package("sentence_transformers", "sentence-transformers", installer=installer)
    ensure_package("tokenizers", installer=installer)
    ensure_package("torch", installer=installer)
    
    print("✅ All embedding dependencies are ready!")

def ensure_api_dependencies(installer="pip"):
    """Ensure all required API packages are installed."""
    print("🔍 Checking API dependencies...")
    
    # API packages
    ensure_package("fastapi", installer=installer)
    ensure_package("uvicorn", installer=installer)
    ensure_package("python_dotenv", "python-dotenv", installer=installer)
    ensure_package("pydantic", installer=installer)
    
    print("✅ All API dependencies are ready!")

def setup_environment(installer="pip"):
    """Set up the environment by cleaning up and ensuring dependencies."""
    # cleanup_init_files()
    ensure_embedding_dependencies(installer=installer)
    ensure_api_dependencies(installer=installer)

if __name__ == "__main__":
    setup_environment()