#!/usr/bin/env python3
"""
Novita Sandbox Cleanup Script

Used for manually cleaning up test sandboxes
"""

import sys
import argparse
from novita_sandbox.core import Sandbox, SandboxQuery, SandboxState


def cleanup_sandbox(sandbox_id: str) -> bool:
    """
    Clean up the specified sandbox
    
    Args:
        sandbox_id: Sandbox ID
    
    Returns:
        Whether cleanup was successful
    """
    try:
        print(f"Connecting to sandbox: {sandbox_id}")
        sandbox = Sandbox.connect(sandbox_id)
        
        print(f"Cleaning up sandbox...")
        sandbox.kill()
        
        print(f"✅ Sandbox {sandbox_id} cleaned up")
        return True
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}", file=sys.stderr)
        return False


def cleanup_all_running() -> int:
    """
    Clean up all running sandboxes
    
    Returns:
        Number of sandboxes cleaned up
    """
    try:
        print("Fetching list of running sandboxes...")
        paginator = Sandbox.list(query=SandboxQuery(state=[SandboxState.RUNNING]))
        sandboxes = paginator.next_items()
        
        if not sandboxes:
            print("No running sandboxes")
            return 0
        
        print(f"Found {len(sandboxes)} running sandbox(es)")
        
        cleaned = 0
        for sb in sandboxes:
            if cleanup_sandbox(sb.sandbox_id):
                cleaned += 1
        
        print(f"\nCleaned {cleaned}/{len(sandboxes)} sandbox(es)")
        return cleaned
        
    except Exception as e:
        print(f"❌ Failed to fetch sandbox list: {e}", file=sys.stderr)
        return 0


def list_running_sandboxes():
    """List all running sandboxes"""
    try:
        print("Fetching list of running sandboxes...")
        paginator = Sandbox.list(query=SandboxQuery(state=[SandboxState.RUNNING]))
        sandboxes = paginator.next_items()
        
        if not sandboxes:
            print("No running sandboxes")
            return
        
        print(f"\nFound {len(sandboxes)} running sandbox(es):")
        print("-" * 50)
        for sb in sandboxes:
            print(f"  ID: {sb.sandbox_id}")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Failed to fetch sandbox list: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Novita Sandbox Cleanup Tool")
    parser.add_argument(
        "sandbox_id",
        nargs="?",
        help="Sandbox ID to clean up"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Clean up all running sandboxes"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all running sandboxes"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_running_sandboxes()
        sys.exit(0)
    
    if args.all:
        cleaned = cleanup_all_running()
        sys.exit(0 if cleaned >= 0 else 1)
    
    if args.sandbox_id:
        success = cleanup_sandbox(args.sandbox_id)
        sys.exit(0 if success else 1)
    
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
