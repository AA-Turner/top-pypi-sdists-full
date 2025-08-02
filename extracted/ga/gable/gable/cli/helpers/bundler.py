import fnmatch
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from io import BytesIO

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from loguru import logger


def get_installed_packages(project_dir):
    os.chdir(project_dir)
    result = subprocess.run(
        ["pip", "list", "--format=json"], capture_output=True, text=True
    )
    packages = json.loads(result.stdout)
    dependencies = []
    total_packages = len(packages)
    logger.debug("Loading project dependencies...")
    for index, package in enumerate(packages, start=1):
        # Get the installation location using pip show
        install_location = get_install_location(package["name"])
        logger.debug(f"\t{index}/{total_packages}: {package['name']}")
        temp_dir = tempfile.mkdtemp()
        if install_location is not None and os.path.exists(install_location):
            # Copy the entire contents of the package folder to temp location
            curr_dir = os.path.join(temp_dir, package["name"])
            shutil.copytree(install_location, curr_dir)
            dependencies.append(curr_dir)

    return dependencies


def get_install_location(package_name):
    try:
        package_info = subprocess.run(
            ["pip", "show", package_name], capture_output=True, text=True, check=True
        )
        for line in package_info.stdout.split("\n"):
            if line.startswith("Location: "):
                return line.split(" ")[1].strip() + "/" + package_name.replace("-", "_")
        return None
    except subprocess.CalledProcessError:
        return None


def should_ignore(directory, names):
    ignore_patterns = {
        "__pycache__",
        "*.py[cod]",
        "*.pyd",  # Python file artifacts
        "venv",
        "env",
        ".venv",
        "ENV",  # Virtual environments
        ".idea",
        ".vscode",  # IDE/Editor settings
        "build",
        "dist",
        "*.egg-info",  # Distribution / Packaging
        ".coverage",
        ".pytest_cache",
        "htmlcov",  # Test reports
        ".ipynb_checkpoints",  # Jupyter Notebook checkpoints
        ".DS_Store",
        "Thumbs.db",  # OS generated files
        ".env",
        ".flaskenv",  # Configuration files
        "*.log",  # Log files
        "*.sqlite",  # Database files
        "*.tmp",
        "*.temp",
        "*.tar.gz",
        "*~",  # Temporary files
        "node_modules",
    }

    ignored_names = set()
    for name in names:
        if any(fnmatch.fnmatch(name, pattern) for pattern in ignore_patterns):
            ignored_names.add(name)
        elif os.path.isdir(os.path.join(directory, name)):
            # Additional logic for directories, if needed
            pass

    return ignored_names


def copy_project_files(src, dest):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isdir(src_path):
            if not should_ignore(src, [item]):
                shutil.copytree(src_path, dest_path, ignore=should_ignore)
                logger.trace(f"Copied directory: {item}")
        else:
            if not should_ignore(src, [item]):
                shutil.copy2(src_path, dest_path)
                logger.trace(f"Copied file: {item}")


def create_gzip_bundle_buffer(project_dir, dependencies, debug=False):
    logger.trace("Starting the bundling process...")
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.trace("Copying project files from the root directory...")
        copy_project_files(project_dir, temp_dir)
        dependencies_dir = os.path.join(temp_dir, "dependencies")
        os.mkdir(dependencies_dir)
        logger.trace("Copying dependencies...")
        for dep in dependencies:
            dep_name = os.path.basename(dep)
            shutil.move(dep, os.path.join(dependencies_dir, dep_name))
            logger.trace(f"Added dependency: {dep_name}")

        logger.trace("Bundling all the files into a .tar.gz archive in memory...")
        tar_buffer = BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar_file:
            tar_file.add(temp_dir, arcname=os.path.basename(project_dir))
        logger.trace("Bundle creation complete. Resetting buffer position...")
        tar_buffer.seek(0)
        if debug:
            logger.trace("Creating .tar.gz file on disk for debugging...")
            debug_file_path = os.path.join(
                os.getcwd(), f"{os.path.basename(project_dir)}.tar.gz"
            )
            logger.trace("debug_file_path", debug_file_path)
            with open(debug_file_path, "wb") as file:
                file.write(tar_buffer.read())
            tar_buffer.seek(0)
            logger.trace(f"Debug .tar.gz file created at {debug_file_path}")
        logger.trace("Bundling process completed successfully.")
        return tar_buffer


def get_bundled_project(project_root, debug=False):
    dependencies = get_installed_packages(project_root)
    return create_gzip_bundle_buffer(os.path.abspath(project_root), dependencies, debug)


def encrypt_gzip_payload(gzip_payload: BytesIO) -> tuple[bytes, str]:
    # Generate a one-time use encryption key and Initialization vector, and
    # encrypt the payload using AES-256-CBC encryption
    aes_key = get_random_bytes(32)
    iv = get_random_bytes(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    encrypted_payload = cipher.encrypt(pad(gzip_payload.read(), AES.block_size))
    # Set the encryption key value to send to the handler in the format key_hex:iv_hex
    temp_encryption_key = aes_key.hex() + ":" + iv.hex()
    return encrypted_payload, temp_encryption_key
