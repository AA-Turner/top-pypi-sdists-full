"""
Novita Agent Sandbox SDK - Python library for sandbox environments and AI agent tools.

This package provides a comprehensive SDK for working with Novita Agent Sandbox environments,
enabling developers to create, manage, and interact with sandboxed execution contexts
for AI agents and applications.

The SDK is organized into three main modules:
- core: Core sandbox functionality and API clients
- code_interpreter: Code execution and interpretation capabilities  
- desktop: Desktop environment interaction tools
"""

__version__ = "1.0.0"
__author__ = "Novita"
__email__ = "support@novita.ai"

# Import core functionality
from . import core
from . import connect
from . import code_interpreter
from . import desktop
from .core import *
from .code_interpreter import AsyncSandbox as AsyncCodeInterpreterSandbox
from .code_interpreter import Context
from .code_interpreter import Execution
from .code_interpreter import ExecutionError
from .code_interpreter import Logs
from .code_interpreter import MIMEType
from .code_interpreter import OutputMessage
from .code_interpreter import Result
from .code_interpreter import Sandbox as CodeInterpreterSandbox
from .desktop import Sandbox as DesktopSandbox

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Modules (for backwards compatibility)
    "core",
    "connect",
    "code_interpreter",
    "desktop",
    # Explicit runtime sandbox aliases
    "CodeInterpreterSandbox",
    "AsyncCodeInterpreterSandbox",
    "DesktopSandbox",
    # Code interpreter public types
    "Context",
    "Execution",
    "ExecutionError",
    "Logs",
    "MIMEType",
    "OutputMessage",
    "Result",
] + core.__all__
