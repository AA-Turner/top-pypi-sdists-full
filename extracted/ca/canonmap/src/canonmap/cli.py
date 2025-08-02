#!/usr/bin/env python3
"""
Command-line interface for CanonMap.
"""

import logging
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from canonmap.logger import make_console_handler

logger = logging.getLogger(__name__)


def normalize_name(name: str) -> str:
    """
    Normalize a name to follow Python directory naming conventions.
    
    Args:
        name: The name to normalize
        
    Returns:
        Normalized name suitable for directory names
    """
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and special characters with underscores
    name = re.sub(r'[^a-z0-9_]', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Replace multiple underscores with single underscore
    name = re.sub(r'_+', '_', name)
    # Ensure it starts with a letter or underscore
    if name and not name[0].isalpha() and name[0] != '_':
        name = f"api_{name}"
    return name or "app"


def find_available_name(base_name: str) -> str:
    """
    Find an available directory name, appending numbers if needed.
    
    Args:
        base_name: The base name to try
        
    Returns:
        Available directory name
    """
    name = base_name
    counter = 1
    
    while os.path.exists(name):
        name = f"{base_name}-{counter}"
        counter += 1
    
    return name


def replace_in_file(file_path: Path, old_name: str, new_name: str) -> None:
    """
    Replace all occurrences of old_name with new_name in a file.
    
    Args:
        file_path: Path to the file
        old_name: The old name to replace
        new_name: The new name to use
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        # Replace imports and references
        content = content.replace(f"from {old_name}.", f"from {new_name}.")
        content = content.replace(f"import {old_name}.", f"import {new_name}.")
        content = content.replace(f"app.{old_name}", f"app.{new_name}")
        content = content.replace(f"{old_name}_", f"{new_name}_")
        content = content.replace(f"_{old_name}", f"_{new_name}")
        
        # Replace in comments and strings
        content = content.replace(f"# {old_name}", f"# {new_name}")
        content = content.replace(f'"{old_name}"', f'"{new_name}"')
        content = content.replace(f"'{old_name}'", f"'{new_name}'")
        
        file_path.write_text(content, encoding='utf-8')
        logger.debug(f"Updated {file_path}")
    except Exception as e:
        logger.warning(f"Could not update {file_path}: {e}")


def copy_and_customize_api(source_dir: Path, target_dir: Path, old_name: str, new_name: str) -> None:
    """
    Copy the API template and customize it with the new name.
    
    Args:
        source_dir: Source directory (template)
        target_dir: Target directory (new API)
        old_name: Original name in template
        new_name: New name for the API
    """
    # Copy the entire directory structure
    shutil.copytree(source_dir, target_dir, dirs_exist_ok=False)
    
    # Walk through all files and replace content
    for file_path in target_dir.rglob("*.py"):
        if file_path.is_file():
            replace_in_file(file_path, old_name, new_name)
    
    # Also check for other text files
    for file_path in target_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.yml', '.yaml', '.json']:
            replace_in_file(file_path, old_name, new_name)
    
    # Create .env file with required environment variables
    env_content = f"""# Environment Configuration for {new_name}
# Copy this file to .env and fill in your values

# Environment (dev/prod)
ENV=dev

# Database Configuration
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_UNIX_SOCKET=

# Cohere API Configuration
COHERE_API_KEY=

# Instructions:
# 1. Copy this file to .env: cp .env.example .env
# 2. Fill in your database credentials
# 3. Add your Cohere API key
# 4. For production, set ENV=prod and configure DB_UNIX_SOCKET if needed
"""
    
    env_file = target_dir / ".env.example"
    env_file.write_text(env_content, encoding='utf-8')
    logger.debug(f"Created {env_file}")


def create_api_command(name: Optional[str] = None) -> int:
    """
    Create a new API project from the template.
    
    Args:
        name: Optional name for the API directory
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Get the template directory
        template_dir = Path(__file__).parent / "_example_usage" / "api" / "app"
        
        if not template_dir.exists():
            logger.error(f"Template directory not found: {template_dir}")
            return 1
        
        # Normalize and find available name
        if name is None:
            base_name = "app"
        else:
            base_name = normalize_name(name)
        
        api_name = find_available_name(base_name)
        
        # Create the target directory
        target_dir = Path.cwd() / api_name
        
        logger.info(f"Creating API project: {api_name}")
        logger.info(f"Template: {template_dir}")
        logger.info(f"Target: {target_dir}")
        
        # Copy and customize the template
        copy_and_customize_api(template_dir, target_dir, "app", api_name)
        
        logger.info(f"✅ API project created successfully!")
        logger.info(f"📁 Directory: {target_dir}")
        
        # Check and install dependencies
        logger.info("📦 Checking dependencies...")
        
        # Check if dependencies are already installed
        missing_deps = []
        for dep in ["fastapi", "uvicorn"]:
            try:
                __import__(dep)
                logger.debug(f"✅ {dep} already installed")
            except ImportError:
                missing_deps.append(dep)
        
        if not missing_deps:
            logger.info("✅ All dependencies already installed!")
        else:
            logger.info(f"📦 Installing missing dependencies: {', '.join(missing_deps)}")
            
            # Detect available package manager
            package_manager = None
            install_cmd = None
            
            # Check for uv
            try:
                subprocess.run(["uv", "--version"], check=True, capture_output=True)
                package_manager = "uv"
                install_cmd = ["uv", "pip", "install"] + missing_deps
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            # Check for pip if uv not found
            if not package_manager:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
                    package_manager = "pip"
                    install_cmd = [sys.executable, "-m", "pip", "install", "--quiet"] + missing_deps
                except subprocess.CalledProcessError:
                    pass
            
            # Try to install with detected package manager
            if install_cmd:
                try:
                    result = subprocess.run(
                        install_cmd,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    logger.info(f"✅ Dependencies installed successfully using {package_manager}!")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"⚠️  Could not install dependencies automatically using {package_manager}")
                    if e.stderr:
                        logger.debug(f"Error details: {e.stderr}")
                    logger.info("📋 Please install manually:")
                    if package_manager == "uv":
                        logger.info(f"   uv pip install {' '.join(missing_deps)}")
                    else:
                        logger.info(f"   pip install {' '.join(missing_deps)}")
            else:
                logger.warning("⚠️  No package manager found (pip or uv)")
                logger.info("📋 Please install manually:")
                logger.info(f"   pip install {' '.join(missing_deps)}")
        
        logger.info(f"📋 Next Steps:")
        logger.info(f"   1. Configure your environment:\n")
        # logger.info(f"      cd {api_name}")
        logger.info(f"      #########################################################")
        logger.info(f"      cp {api_name}/.env.example .env")
        logger.info(f"      #########################################################")
        logger.info(f"\n    # Edit .env with your database credentials")
        logger.info(f"")
        logger.info(f"   2. Set up your database:")
        logger.info(f"      - Install MySQL if not already installed")
        logger.info(f"      - Create a database for your project")
        logger.info(f"      - Update DB_USER and DB_PASSWORD in .env")
        logger.info(f"")
        logger.info(f"   3. (Optional) Get your Cohere API key for enhanced matching:")
        logger.info(f"      - Visit https://cohere.ai to sign up")
        logger.info(f"      - Add your API key to COHERE_API_KEY in .env")
        logger.info(f"      - This enables an extra layer of AI-powered reranking")
        logger.info(f"")
        logger.info(f"🚀 To run your API:")
        logger.info(f"   uvicorn {api_name}.main:app --reload")
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to create API project: {e}")
        return 1


def main(args: Optional[list[str]] = None) -> int:
    """
    Main entry point for the CanonMap CLI.
    
    Args:
        args: Command line arguments. If None, uses sys.argv[1:].
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(
        description="CanonMap - Data matching and canonicalization library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cm --version                    Show version information
  cm --help                       Show this help message
  cm create-api                   Create a new API project (default name: app)
  cm create-api --name my-api     Create a new API project named 'my-api'
  cm create-api --name "My API"   Create a new API project named 'my_api'
        """,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="CanonMap 0.4.3",
        help="Show version information and exit",
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create API command
    create_api_parser = subparsers.add_parser(
        "create-api",
        help="Create a new API project from template"
    )
    create_api_parser.add_argument(
        "--name", "-n",
        type=str,
        help="Name for the API directory (default: app, will auto-increment if exists)"
    )
    
    # Parse arguments
    parsed_args = parser.parse_args(args)
    
    # Set up logging
    make_console_handler(set_root=True)
    
    if parsed_args.verbose:
        logger.setLevel("DEBUG")
        logger.debug("Verbose logging enabled")
    
    # Handle commands
    if parsed_args.command == "create-api":
        return create_api_command(parsed_args.name)
    elif not parsed_args.command:
        # No command specified, show help
        parser.print_help()
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 