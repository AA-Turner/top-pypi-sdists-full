#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup verification script for Novita Agent Sandbox SDK.

This script checks if all dependencies are properly installed and the package can be imported correctly.
"""

import sys
import importlib
import subprocess
from typing import List, Tuple


def check_python_version() -> bool:
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print(f"❌ Python 3.9+ required, found {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def check_package_import(package_name: str) -> bool:
    """Check if a package can be imported."""
    try:
        importlib.import_module(package_name)
        print(f"✅ {package_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: {e}")
        return False


def check_optional_packages(packages: List[str]) -> Tuple[int, int]:
    """Check optional packages and return (success_count, total_count)."""
    success = 0
    for package in packages:
        if check_package_import(package):
            success += 1
    return success, len(packages)


def main():
    """Main setup check function."""
    print("🔍 Novita Agent Sandbox SDK Setup Check")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Core Dependencies:")
    core_deps = [
        "novita_sandbox",
        "httpx", 
        "attrs",
        "protobuf",
        "typing_extensions",
        "packaging"
    ]
    
    core_success = sum(check_package_import(dep) for dep in core_deps)
    
    # Try to import main SDK components
    print("\n🧩 SDK Components:")
    try:
        from novita_sandbox import __version__, __author__, __email__
        print(f"✅ Novita Agent Sandbox SDK v{__version__}")
        print(f"   Author: {__author__}")
        print(f"   Email: {__email__}")
    except ImportError as e:
        print(f"❌ Failed to import SDK: {e}")
        core_success -= 1
    
    # Check optional dependencies
    print("\n🎨 Code Interpreter Dependencies:")
    code_deps = ["matplotlib", "plotly", "pandas", "numpy", "PIL"]
    code_success, code_total = check_optional_packages(code_deps)
    
    print("\n🖥️  Desktop Automation Dependencies:")
    desktop_deps = ["pyautogui", "pynput", "cv2"]
    desktop_success, desktop_total = check_optional_packages(desktop_deps)
    
    # Summary
    print("\n📊 Summary:")
    print(f"   Core dependencies: {core_success}/{len(core_deps)}")
    print(f"   Code interpreter: {code_success}/{code_total}")
    print(f"   Desktop automation: {desktop_success}/{desktop_total}")
    
    if core_success == len(core_deps):
        print("\n🎉 Core setup complete! You can use basic sandbox functionality.")
        
        if code_success == code_total:
            print("🎨 Code interpreter ready!")
        elif code_success > 0:
            print("⚠️  Some code interpreter features may not work.")
        else:
            print("💡 Install with: pip install -e '.[code-interpreter]'")
            
        if desktop_success == desktop_total:
            print("🖥️  Desktop automation ready!")
        elif desktop_success > 0:
            print("⚠️  Some desktop features may not work.")
        else:
            print("💡 Install with: pip install -e '.[desktop]'")
    else:
        print("\n❌ Setup incomplete. Please install missing dependencies.")
        print("💡 Try: pip install -e '.[all,dev]'")
        sys.exit(1)


if __name__ == "__main__":
    main()
