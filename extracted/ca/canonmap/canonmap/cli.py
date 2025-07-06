import shutil
import sys
import re
import subprocess
from pathlib import Path
from codename.codename import codename
from canonmap._example_usage.setup_api_environment import setup_environment

def find_available_port(start=8000, end=8010):
    import socket
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) != 0:
                return port
    return None

def create_api(app_name=None, run=False):
    app_name = app_name.strip().lower().replace(" ", "_") if app_name else f"{codename(separator='_')}_api"
    target = Path.cwd() / app_name
    source = Path(__file__).parent / "_example_usage" / "cm_api"

    print(f"📁 Creating new API project at: {target}")

    if not source.exists():
        print(f"❌ Template not found at {source}")
        return

    for src_path in source.rglob("*"):
        rel_path = src_path.relative_to(source)
        dst_path = target / rel_path

        if "__pycache__" in src_path.parts or src_path.name == "__init__.py":
            continue

        if src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
        else:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if not dst_path.exists():
                shutil.copy2(src_path, dst_path)
                print(f"✅ Copied {dst_path}")
            else: 
                print(f"⚠️ Skipped existing file: {dst_path}")

    print("🧩 Running setup environment tasks...")
    setup_environment()

    print("🎉 API project created successfully!")
    print("🚀 Run one of the following commands to start the API:")
    print(f"    \033[1;36muvicorn {target.name}.main:app\033[0m")
    print("    \033[1;33mor\033[0m")
    print(f"    \033[1;36muvicorn {target.name}.main:app --reload\033[0m\n")

    print("🛠️  Updating local imports to use generated name...")
    for file in target.rglob("*.py"):
        content = file.read_text()
        updated = re.sub(
            r"(from|import) canonmap\._example_usage\.cm_api(\.|(?=\s))",
            rf"\1 {target.name}\2",
            content
        )
        updated = updated.replace("from cm_api.", f"from {target.name}.").replace("import cm_api.", f"import {target.name}.")
        file.write_text(updated)

    if run:
        port = find_available_port()
        if not port:
            print("❌ No open port found between 8000 and 8010")
            return
        print(f"🚀 Launching API at http://localhost:{port}")
        subprocess.run(["uvicorn", f"{target.name}.main:app", "--reload", "--port", str(port)])

def main():
    import argparse
    parser = argparse.ArgumentParser(description="CanonMap CLI")
    parser.add_argument("command", choices=["create-api"])
    parser.add_argument("--name", type=str, help="Optional name for the API folder")
    parser.add_argument("--run", action="store_true", help="Run the API after creation")
    args = parser.parse_args()

    if args.command == "create-api":
        create_api(app_name=args.name, run=args.run)