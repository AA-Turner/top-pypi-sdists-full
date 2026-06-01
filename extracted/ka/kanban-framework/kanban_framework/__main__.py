"""Allow running kanban as: python -m kanban_framework <cmd>

Supports two invocation modes:
  1. From framework root:  cd .claude/skills/kanban && python -m kanban_framework status
  2. From project root:    PYTHONPATH=.claude/skills/kanban python -m kanban_framework status

Prefer the installed CLI: kanban status
"""
import sys
import os

# Add framework root to sys.path so kanban_framework module can be imported from any cwd
_framework_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _framework_root not in sys.path:
    sys.path.insert(0, _framework_root)

from kanban_framework.cli.main import main

main()
