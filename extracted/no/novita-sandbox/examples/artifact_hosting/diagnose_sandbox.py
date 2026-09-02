#!/usr/bin/env python3
"""Diagnose Sandbox status"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from novita_sandbox.core.sandbox_sync.main import Sandbox


def main():
    parser = argparse.ArgumentParser(description="Diagnose Sandbox status")
    parser.add_argument("-s", "--sandbox-id", required=True, help="Sandbox ID")
    args = parser.parse_args()
    
    sandbox_id = args.sandbox_id
    print(f"🔍 Connecting to Sandbox: {sandbox_id}")
    
    sandbox = Sandbox.connect(sandbox_id)
    
    print("\n📂 Checking /app directory:")
    result = sandbox.commands.run("ls -la /app")
    print(result.stdout or "(empty)")
    if result.stderr:
        print(f"stderr: {result.stderr}")
    
    print("\n📄 Checking for index.html:")
    result = sandbox.commands.run("cat /app/index.html 2>&1 | head -20")
    print(result.stdout or "(file not found)")
    
    print("\n🔧 Checking running processes:")
    result = sandbox.commands.run("ps aux")
    print(result.stdout)
    
    print("\n🌐 Checking listening ports:")
    result = sandbox.commands.run("netstat -tlnp 2>/dev/null || ss -tlnp 2>/dev/null || echo 'netstat/ss not available'")
    print(result.stdout)
    
    print("\n🚀 Attempting to start server manually:")
    cmd_handle = sandbox.commands.run("cd /app && python -m http.server 3000", background=True)
    print(f"Server started (background handle: {cmd_handle})")
    
    import time
    time.sleep(2)
    
    print("\n🔍 Checking listening ports again:")
    result = sandbox.commands.run("netstat -tlnp 2>/dev/null || ss -tlnp 2>/dev/null || echo 'netstat/ss not available'")
    print(result.stdout)
    
    print("\n✅ Diagnosis complete")
    print(f"   Access: https://3000-{sandbox_id}.sandbox.novita.ai")


if __name__ == "__main__":
    main()

