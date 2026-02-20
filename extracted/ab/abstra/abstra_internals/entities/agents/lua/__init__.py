"""Lua REPL executor for AgentStage.

Replaces the one-tool-per-step ReAct pattern with a Lua scripting
interface where the LLM writes Lua code that can call multiple tools,
use loops, variables, and functions within a single step.
"""
