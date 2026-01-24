import json
import os
import sys
import stat
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any


def _supports_unicode():
    """Check if terminal supports Unicode output."""
    if sys.platform == 'win32':
        try:
            '✓✗❌'.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, LookupError, AttributeError):
            return False
    return True


_UNICODE_OK = _supports_unicode()

# Unicode symbols with ASCII fallbacks
SYM_CHECK = '✓' if _UNICODE_OK else '[OK]'
SYM_CROSS = '✗' if _UNICODE_OK else '[X]'
SYM_ERROR = '❌' if _UNICODE_OK else '[ERR]'
SYM_ARROW = '→' if _UNICODE_OK else '->'
SYM_BULLET = '•' if _UNICODE_OK else '*'

MODELS = {
    'gpt-3.5-turbo': {'context': 16385, 'endpoint': 'gpt-3.5-turbo'},
    'gpt-4-turbo': {'context': 128000, 'endpoint': 'gpt-4-turbo'},
    'gpt-4o': {'context': 128000, 'endpoint': 'gpt-4o'},
    'gpt-4o-mini': {'context': 128000, 'endpoint': 'gpt-4o-mini'},
    'gpt-5': {'context': 256000, 'endpoint': 'gpt-5'},
    'gpt-5-nano': {'context': 32000, 'endpoint': 'gpt-5-nano'},
    'o1': {'context': 200000, 'endpoint': 'o1'},
    'o1-mini': {'context': 128000, 'endpoint': 'o1-mini'},
    'o1-preview': {'context': 128000, 'endpoint': 'o1-preview'},
}

DEFAULT_MODEL = 'gpt-5'
DEFAULT_DAILY_LIMIT = 220000

OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
BRAVE_SEARCH_URL = 'https://api.search.brave.com/res/v1/web/search'

CONTEXT_LIMITS = {
    'standard': 3000,
    'think': 5000,
    'think2': 10000,
    'think3': 25000,
}

QUESTION_PROMPT_ADDITION = '''
INTERACTIVE MODE:
If you need clarification before proceeding, you may ask ONE question.
Format: ASK_USER: <your question>
OPTIONS: <option1> | <option2> | <option3>  (optional, max 4 options)

Only ask if genuinely needed. If task is clear, proceed without asking.'''

# AI Generate Tools
GENERATE_TOOLS = {
    'READ_FILE': {
        'desc': 'Read file contents',
        'format': 'TOOL: READ_FILE\nPATH: <absolute_or_relative_path>',
    },
    'WRITE_FILE': {
        'desc': 'Create or overwrite a file',
        'format': 'TOOL: WRITE_FILE\nPATH: <path>\n```<lang>\n<content>\n```',
    },
    'EDIT_FILE': {
        'desc': 'Edit existing file with changes',
        'format': 'TOOL: EDIT_FILE\nPATH: <path>\nCHANGES:\n- <desc>\n```<lang>\n<full_content>\n```',
    },
    'DELETE_FILE': {
        'desc': 'Delete a file',
        'format': 'TOOL: DELETE_FILE\nPATH: <path>',
    },
    'CREATE_FOLDER': {
        'desc': 'Create directory (with parents)',
        'format': 'TOOL: CREATE_FOLDER\nPATH: <path>',
    },
    'LIST_FOLDER': {
        'desc': 'List directory contents',
        'format': 'TOOL: LIST_FOLDER\nPATH: <path>',
    },
    'SEARCH_FILES': {
        'desc': 'Find files by glob pattern',
        'format': 'TOOL: SEARCH_FILES\nPATTERN: <glob_pattern>\nPATH: <base_path>',
    },
    'GREP': {
        'desc': 'Search file contents with regex',
        'format': 'TOOL: GREP\nPATTERN: <regex>\nPATH: <path_or_glob>',
    },
    'RUN_CMD': {
        'desc': 'Execute system command',
        'format': 'TOOL: RUN_CMD\nCMD: <command>',
    },
    'INCLUDECPP_CMD': {
        'desc': 'Run includecpp CLI command',
        'format': 'TOOL: INCLUDECPP_CMD\nCMD: <subcommand> (e.g., plugin mymod, rebuild --fast)',
    },
}

SYSTEM_PROMPT_GENERATE = '''You are an expert AI assistant for IncludeCPP projects.

You have access to tools for file operations and command execution.

AVAILABLE TOOLS:
{tools_list}

TOOL USAGE:
- Call tools by outputting the exact format shown above
- Wait for tool results before continuing
- You can call multiple tools in sequence
- Always use absolute paths or paths relative to project root

RESPONSE FORMAT:
1. If you need to use tools, output tool calls first
2. After all tools complete, provide final summary
3. For file changes, use EDIT_FILE with full content and change descriptions

CONTEXT:
- Project root: {project_root}
- System: {system_info}
- IncludeCPP is always available via `includecpp` command

{includecpp_context}

RULES:
1. All C++ code MUST be in namespace includecpp {{ }}
2. Use EDIT_FILE for modifications (shows diff)
3. Use WRITE_FILE only for new files
4. Always confirm destructive operations
5. Keep responses professional and concise
'''

SYSTEM_PROMPT_GENERATE_PLAN = '''You are planning and executing a task for an IncludeCPP project.

WORKFLOW (execute ALL phases immediately):

PHASE 1: RESEARCH - Use tools NOW
Call these tools immediately to gather information:
- SEARCH_FILES to find relevant files
- GREP to search file contents
- READ_FILE to examine code
- LIST_FOLDER to understand structure

PHASE 2: PLAN - Brief summary
After research, output:
PLAN:
1. Step one
2. Step two

PHASE 3: EXECUTE - Complete the task NOW
Execute all required tool calls to complete the task.
DO NOT wait for user confirmation - execute immediately.
DO NOT ask "Please confirm" or "Should I proceed" - just do it.

{base_prompt}
'''

SYSTEM_PROMPT_NEW_MODULE = '''You are creating a new C++ module for IncludeCPP.

Module name: {module_name}
Description: {description}

CREATE THESE FILES:
1. include/{module_name}.cpp - Main source with namespace includecpp {{ }}
2. include/{module_name}.h - Header file with declarations
3. plugins/{module_name}.cp - Plugin definition

CRITICAL .CP FILE FORMAT:
- ALWAYS use SOURCE() && HEADER() together on the SAME LINE when you create both .cpp and .h files
- Example: SOURCE(include/{module_name}.cpp) && HEADER(include/{module_name}.h) {module_name}

REQUIREMENTS:
- All code in namespace includecpp {{ }}
- Include practical, working implementations
- Add appropriate FUNC(), CLASS(), METHOD() in .cp file
- Follow existing project patterns

OUTPUT FORMAT - USE THIS EXACT FORMAT FOR EACH FILE:

TOOL: WRITE_FILE
PATH: include/{module_name}.h
```cpp
#pragma once
namespace includecpp {{
// declarations
}}
```

TOOL: WRITE_FILE
PATH: include/{module_name}.cpp
```cpp
#include "{module_name}.h"
namespace includecpp {{
// implementations
}}
```

TOOL: WRITE_FILE
PATH: plugins/{module_name}.cp
```
SOURCE(include/{module_name}.cpp) && HEADER(include/{module_name}.h) {module_name}
PUBLIC(
    {module_name} FUNC(...)
    {module_name} CLASS(...) {{ ... }}
)
```

Create all required files now using the format above. ALWAYS include && HEADER() in the .cp file!
'''

INCLUDECPP_CONTEXT = '''
CRITICAL KNOWLEDGE FOR INCLUDECPP:

1. NAMESPACE REQUIREMENT:
   ALL C++ code MUST be inside `namespace includecpp { }` - this is REQUIRED, not optional.

2. PLUGIN FILE (.cp) FORMAT:
   IMPORTANT: Use && to combine SOURCE and HEADER on the SAME LINE!

   With header file (REQUIRED when you create both .cpp and .h):
   SOURCE(include/math.cpp) && HEADER(include/math.h) math

   Without header (source only):
   SOURCE(include/math.cpp) math

   FULL EXAMPLE:
   SOURCE(include/mymodule.cpp) && HEADER(include/mymodule.h) mymodule
   PUBLIC(
       mymodule CLASS(MyClass) {
           CONSTRUCTOR()
           CONSTRUCTOR(int, double)
           METHOD(foo)
           METHOD_CONST(bar, const std::string&)
           FIELD(x)
       }
       mymodule FUNC(standalone_function)
       mymodule TEMPLATE_FUNC(generic_func) TYPES(int, float, double)
       mymodule STRUCT(Point) { FIELD(x) FIELD(y) }
   )

3. HEADER RULES:
   - If you create a .h header file, you MUST include HEADER() in the .cp file
   - SOURCE() and HEADER() MUST be on the SAME LINE with && between them
   - Without && HEADER(), the build system won't find the header

4. BUILD OUTPUT:
   ~/.includecpp/builds/ (Windows: %APPDATA%/IncludeCPP/)

5. COMMON ERRORS AND FIXES:
   * "undefined reference" -> Code not in namespace includecpp { }, or missing FUNC() in .cp
   * "no matching function" -> Wrong parameter types in .cp METHOD() definition
   * "template instantiation" -> Missing TEMPLATE_FUNC() with TYPES() in .cp file
   * "namespace includecpp not found" -> Source file missing namespace wrapper
   * "no member named X" -> Method not in class public section, or missing METHOD() in .cp
   * "header not found" -> Missing HEADER() directive in .cp file, or wrong path

6. FIELD DECLARATIONS:
   FIELD(name) - only the field name is needed, not the type.
   Comma-separated fields like `double x, y, z;` are parsed as separate fields.
'''

SYSTEM_PROMPT_OPTIMIZE = '''You are a C++ expert specializing in pybind11 bindings and the IncludeCPP framework.

IMPORTANT: Be conservative. Only suggest safe optimizations that will NOT break compilation.

Rules:
1. NEVER remove existing functions or code blocks
2. Preserve all public API signatures EXACTLY
3. NEVER change function parameters or return types
4. Only make changes that are 100% safe and backwards compatible
5. Maintain namespace includecpp structure
6. Do not add comments, docstrings, or explanatory text
7. Do not add AI-typical output markers or annotations
8. If unsure about a change, DO NOT make it

Safe optimizations:
- Adding const where appropriate
- Using reserve() before loops
- Replacing raw loops with STL algorithms (if equivalent)
- Adding noexcept to functions that don't throw
- Using move semantics for local variables

AVOID:
- Changing function signatures
- Removing code that might be used elsewhere
- Complex refactoring
- Template changes

If a change would alter existing functionality, you MUST prefix with:
CONFIRM_REQUIRED: <brief description>

Output format for each file:
FILE: <relative_path>
CHANGES:
- Line X: <what changed> - <why>
- Line Y-Z: <what changed> - <why>
```cpp
<complete file content with no comments about changes>
```

Only output files that need changes. If no safe optimizations found, respond with: NO_CHANGES_NEEDED'''

SYSTEM_PROMPT_FIX = '''You are a C++ expert analyzing code for the IncludeCPP framework.

Context:
- IncludeCPP generates pybind11 bindings from .cp plugin files
- SOURCE() and HEADER() directives link to C++ source files
- All exposed code MUST be inside namespace includecpp { ... }
- Modules compile to .pyd (Windows) or .so (Linux/Mac) Python extensions

CRITICAL CHECKS (in order):
1. SYNTAX ERRORS: Missing semicolons, unmatched braces, invalid tokens
2. NAMESPACE: All classes/functions MUST be inside namespace includecpp { }
3. TYPE ERRORS: Undefined types, wrong return types, parameter mismatches
4. MEMORY: Dangling pointers, leaks, uninitialized variables
5. PYBIND11: Return policies, holder types, opaque types

Rules:
1. Never remove functions or change public API signatures
2. Fix ALL syntax errors first - code must compile
3. Ensure code is inside namespace includecpp { }
4. Do not add comments or docstrings
5. Preserve exact logic and behavior

If removal is necessary, prefix with:
CONFIRM_REQUIRED: <description>

Output format for each file:
FILE: <path>
CHANGES:
- Line X: <what changed> - <why>
- Line Y-Z: <what changed> - <why>
```cpp
<complete fixed file content>
```

Only output files that need changes. If no issues found, respond with: NO_ISSUES_FOUND'''

SYSTEM_PROMPT_BUILD_ERROR = '''You are analyzing a C++ build error in an IncludeCPP project.

IncludeCPP Architecture:
- Plugin files (.cp) define bindings: SOURCE(file.cpp), HEADER(file.h), CLASS(), METHOD(), FUNC()
- SOURCE() links C++ implementation files
- HEADER() links header files for declarations
- All exposed code MUST be in namespace includecpp { }
- Build generates pybind11 bindings in a temp bindings.cpp file
- Compiles to .pyd (Windows) or .so (Linux/Mac) Python extensions

Common Error Categories:
1. USER CODE ERROR: Syntax errors, missing includes, type mismatches in user C++ files
2. PLUGIN FILE ERROR: Wrong signatures in .cp file, missing METHOD(), wrong parameter types
3. NAMESPACE ERROR: Code not inside namespace includecpp { }
4. BINDING ERROR: pybind11 type conversion issues, missing opaque declarations
5. INCLUDECPP BUG: Framework generated incorrect bindings (rare, report at github.com/liliassg/IncludeCPP/issues)

Analyze the error and provide:

ERROR TYPE: [USER CODE | PLUGIN FILE | NAMESPACE | BINDING | INCLUDECPP BUG]

ROOT CAUSE:
<one line explanation>

FIX:
File: <exact file path>
Line: <line number if known>
```cpp
<exact code fix>
```

WHY:
<brief explanation of what was wrong>

PREVENTION:
<one line tip to avoid this in future>'''

SYSTEM_PROMPT_AGENT = '''You are a C++ expert working on an IncludeCPP project.

Context:
- IncludeCPP generates pybind11 bindings
- Code must be in namespace includecpp
- Focus on the specific task requested

Rules:
1. Never remove existing functions unless explicitly asked
2. Preserve public API signatures
3. No comments, docstrings, or explanatory markers
4. Output complete file contents

If removal needed, prefix with:
CONFIRM_REQUIRED: <description>

Output format:
FILE: <path>
```cpp
<complete file content>
```'''

SYSTEM_PROMPT_ASK = '''You are an expert assistant for IncludeCPP projects.

You have access to:
- IncludeCPP documentation (README)
- Project source files (.cpp, .h, .py)
- Plugin definitions (.cp files)
- Build system knowledge

Answer questions precisely and concisely. Reference specific files and line numbers when relevant.

Response format:
- Direct answer first
- File references: path:line if applicable
- Code examples if helpful (brief)

Do not explain IncludeCPP basics unless asked. Assume user knows the system.
Max 200 words unless complexity requires more.'''

SYSTEM_PROMPT_EDIT = '''You are a C++ expert editing code in an IncludeCPP project.

CRITICAL BEHAVIOR - READ CAREFULLY:
1. ALWAYS output FILE: blocks with code changes
2. NEVER say "no changes needed" - the user wants changes, make them
3. When task says "add X" - you MUST add X
4. When task says "improve/optimize/refactor" - you MUST make improvements
5. BE ASSERTIVE - implement what is requested, do not refuse

Context:
- IncludeCPP generates pybind11 bindings from .cp plugin files
- All exposed code must be in namespace includecpp { }
- Focus on the specific edit task requested

Rules:
1. ALWAYS make changes when user requests them
2. Preserve existing functionality unless told otherwise
3. No comments, docstrings, or explanatory text
4. Maintain exact coding style
5. Output COMPLETE file content, not just changed parts

If the edit would break existing functionality:
CONFIRM_REQUIRED: <description>

OUTPUT FORMAT (MANDATORY - YOU MUST USE THIS FORMAT):
FILE: <exact_path>
CHANGES:
- <what changed>
```cpp
<complete file content here>
```

REQUIREMENTS:
- Start with FILE: on its own line
- List changes with - bullet points
- Use ```cpp code block for the full content
- You MUST output at least one FILE: block
- If multiple files need changes, output multiple FILE: blocks

DO NOT explain why you cannot make changes. MAKE the changes.'''

SYSTEM_PROMPT_AUTO_FIX = '''You are an AI that automatically fixes C++ build errors in IncludeCPP projects.

IncludeCPP Architecture:
- Plugin files (.cp) define bindings: SOURCE(file.cpp), HEADER(file.h), CLASS(), METHOD(), FUNC(), TEMPLATE_FUNC()
- All exposed code MUST be in namespace includecpp { }
- Build generates pybind11 bindings and compiles to .pyd/.so

You have access to CLI commands:
- includecpp plugin <modulename>: Regenerate .cp file from source analysis
- includecpp rebuild --fast <modulename>: Rebuild specific module
- includecpp rebuild --clean: Full clean rebuild

IMPORTANT: You must FIX the error. Analyze the error, determine the fix, and output actionable changes.

Output format:

ACTION: FILE_CHANGE
FILE: <exact path>
```cpp
<complete fixed file content>
```

ACTION: CLI_COMMAND
COMMAND: <command to run>
REASON: <why this command is needed>

Multiple actions can be output. Process in order:
1. FILE_CHANGE actions first (fix source files)
2. CLI_COMMAND actions after (regenerate .cp or other commands)

Common fixes:
- Syntax error -> Fix the syntax in source file
- Missing namespace -> Wrap code in namespace includecpp { }
- .cp out of sync -> Run: includecpp plugin <modulename>
- Template not detected -> Run: includecpp plugin <modulename> (regenerates with TEMPLATE_FUNC)
- Missing include -> Add #include directive

If the error cannot be fixed automatically, output:
CANNOT_FIX: <explanation>

Do NOT add comments or docstrings. Output complete file contents for FILE_CHANGE.'''

SYSTEM_PROMPT_THINK3_PLAN = '''You are an expert C++ and Python developer analyzing a build error in an IncludeCPP project.

PHASE 1: ANALYSIS (take your time)
- Analyze the exact error message and location
- Identify the root cause (syntax, linker, template, namespace, etc.)
- Consider all possible fixes
- Review relevant documentation and patterns

PHASE 2: RESEARCH FINDINGS
You have access to web research results. Use them to:
- Find similar issues and solutions
- Identify best practices for the specific error
- Check if this is a known issue with pybind11 or compilers

PHASE 3: PLANNING
Create a structured plan:

PLAN:
1. Primary Fix: <main solution>
2. Alternative: <backup approach if primary fails>
3. Files to Modify: <list of files>
4. Commands Needed: <CLI commands if any>
5. Verification: <how to verify the fix worked>

PHASE 4: IMPLEMENTATION
After planning, output the actual fixes using:

ACTION: FILE_CHANGE
FILE: <path>
```cpp
<complete fixed content>
```

ACTION: CLI_COMMAND
COMMAND: <command>
REASON: <why>

Be thorough. This is professional-grade analysis.'''


CLI_KEYWORDS = {
    'plugin': ['def plugin', '@cli.command', 'plugin_name', 'extract_fields', 'extract_methods'],
    'rebuild': ['def rebuild', 'build_manager', '--fast', '--clean', '--auto-ai'],
    'build': ['def build', 'build_manager'],
    'auto': ['def auto', 'auto_plugins', '--all'],
    'fix': ['def fix', 'fix_code', '--ai', 'ai_mgr'],
    'init': ['def init', 'cpp.proj', 'plugins/', 'include/'],
    'ai': ['@ai.command', 'ai_mgr', 'get_ai_manager', 'ai ask', 'ai edit', 'ai optimize'],
    'settings': ['def settings', 'settings_ui', 'PyQt6'],
    'flag': ['@click.option', 'is_flag', '--think', '--websearch', '--confirm'],
    'command': ['@cli.command', '@click.argument', '@click.option'],
}


class AIManager:
    def __init__(self):
        self.secret_dir = Path.home() / '.includecpp'
        self.secret_path = self.secret_dir / '.secret'
        self.config = self._load_config()
        self._doc_cache = None
        self._cli_cache = None

    def _get_documentation(self) -> str:
        if self._doc_cache:
            return self._doc_cache
        try:
            readme_path = Path(__file__).parent.parent.parent / 'README.md'
            if readme_path.exists():
                self._doc_cache = readme_path.read_text(encoding='utf-8')
                return self._doc_cache
        except:
            pass
        return ''

    def _get_build_info(self) -> str:
        """Read build info from AppData for AI context."""
        import platform
        if platform.system() == "Windows":
            appdata = Path(os.environ.get('APPDATA', str(Path.home() / 'AppData' / 'Roaming')))
            build_base = appdata / 'IncludeCPP'
        else:
            build_base = Path.home() / '.includecpp' / 'builds'

        info_parts = []
        if build_base.exists():
            for item in build_base.iterdir():
                if item.is_dir():
                    registry = item / '.module_registry.json'
                    if registry.exists():
                        try:
                            data = json.loads(registry.read_text(encoding='utf-8'))
                            modules = list(data.get('modules', {}).keys())
                            if modules:
                                info_parts.append(f"Project: {item.name}, Modules: {', '.join(modules[:5])}")
                        except:
                            pass

        if info_parts:
            return '\n\nBUILD CONTEXT (user\'s projects):\n' + '\n'.join(info_parts[:5])
        return ''

    def _get_cli_context(self, question: str) -> str:
        """Extract relevant CLI implementation context based on the question.

        Only extracts code sections matching keywords from the question to save tokens.
        """
        question_lower = question.lower()

        # Check if question is about CLI/commands
        cli_terms = ['command', 'flag', 'option', 'cli', 'includecpp', '--', 'how to', 'usage']
        if not any(term in question_lower for term in cli_terms):
            return ''

        # Find which CLI topics are relevant
        relevant_keywords = set()
        for topic, keywords in CLI_KEYWORDS.items():
            if topic in question_lower:
                relevant_keywords.update(keywords)

        # Add generic command keywords if asking about flags/options
        if '--' in question or 'flag' in question_lower or 'option' in question_lower:
            relevant_keywords.update(CLI_KEYWORDS['flag'])

        if not relevant_keywords:
            return ''

        # Load CLI source if not cached
        if self._cli_cache is None:
            try:
                cli_path = Path(__file__).parent.parent / 'cli' / 'commands.py'
                if cli_path.exists():
                    self._cli_cache = cli_path.read_text(encoding='utf-8')
            except:
                return ''

        if not self._cli_cache:
            return ''

        # Extract relevant sections (functions/decorators containing keywords)
        lines = self._cli_cache.split('\n')
        extracted = []
        in_relevant_block = False
        block_lines = []
        indent_level = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Check for function/decorator start
            if stripped.startswith('@') or stripped.startswith('def '):
                # Save previous block if relevant
                if in_relevant_block and block_lines:
                    extracted.extend(block_lines[:50])  # Max 50 lines per block
                    extracted.append('    # ... (truncated)\n')

                # Check if new block is relevant
                in_relevant_block = any(kw in line for kw in relevant_keywords)
                block_lines = [f'{i+1}: {line}'] if in_relevant_block else []
                indent_level = len(line) - len(line.lstrip())

            elif in_relevant_block:
                # Continue block until dedent
                current_indent = len(line) - len(line.lstrip()) if stripped else indent_level + 1
                if stripped and current_indent <= indent_level and not stripped.startswith('@'):
                    # Block ended
                    if block_lines:
                        extracted.extend(block_lines[:50])
                        if len(block_lines) > 50:
                            extracted.append('    # ... (truncated)\n')
                    in_relevant_block = False
                    block_lines = []
                else:
                    block_lines.append(f'{i+1}: {line}')

        # Limit total context
        if extracted:
            context = '\n'.join(extracted[:200])  # Max 200 lines total
            return f'\n\nCLI IMPLEMENTATION (relevant sections):\n```python\n{context}\n```'
        return ''

    def _get_context_limit(self, think: bool = False, think_twice: bool = False,
                           think_three: bool = False) -> int:
        """Get the appropriate context limit based on thinking mode."""
        if think_three:
            return CONTEXT_LIMITS['think3']
        elif think_twice:
            return CONTEXT_LIMITS['think2']
        elif think:
            return CONTEXT_LIMITS['think']
        return CONTEXT_LIMITS['standard']

    def _add_line_numbers(self, content: str) -> str:
        """Add line numbers to source code for AI context."""
        lines = content.split('\n')
        return '\n'.join(f"{i:4d} | {line}" for i, line in enumerate(lines, 1))

    def _categorize_error(self, error: str) -> str:
        """Categorize build error for better AI context."""
        e = error.lower()
        if 'undefined reference' in e or 'unresolved external' in e:
            return 'LINKER_ERROR - Missing definition, check namespace includecpp and FUNC() in .cp'
        elif 'syntax error' in e or 'expected' in e:
            return 'SYNTAX_ERROR - Check for missing semicolons, braces, or typos'
        elif 'namespace' in e:
            return 'NAMESPACE_ERROR - Code likely not wrapped in namespace includecpp { }'
        elif 'template' in e:
            return 'TEMPLATE_ERROR - Check TEMPLATE_FUNC() with TYPES() in .cp file'
        elif 'no matching function' in e or 'no member named' in e:
            return 'SIGNATURE_ERROR - Method signature in .cp doesn\'t match source'
        elif 'include' in e or 'no such file' in e:
            return 'INCLUDE_ERROR - Missing header file or wrong include path'
        return 'UNKNOWN - Analyze error message carefully'

    def _reset_daily_if_needed(self):
        """Reset daily usage if it's a new day."""
        from datetime import date
        today = date.today().isoformat()
        if self.config.get('daily_usage', {}).get('date') != today:
            self.config['daily_usage'] = {'date': today, 'tokens': 0}
            self._save_config()

    def _check_daily_limit(self) -> Tuple[bool, str]:
        """Check if daily limit is exceeded.
        Returns: (can_proceed, warning_message)
        """
        self._reset_daily_if_needed()
        limit = self.config.get('daily_limit', DEFAULT_DAILY_LIMIT)
        used = self.config.get('daily_usage', {}).get('tokens', 0)

        if used >= limit:
            return False, f"Daily token limit reached ({used:,}/{limit:,}). Resets at midnight."
        if used >= limit * 0.8:
            remaining = limit - used
            return True, f"Warning: {remaining:,} tokens remaining today ({int(used/limit*100)}% used)"
        return True, ""

    def get_daily_usage_info(self) -> Dict[str, Any]:
        """Get current daily usage information."""
        self._reset_daily_if_needed()
        limit = self.config.get('daily_limit', DEFAULT_DAILY_LIMIT)
        used = self.config.get('daily_usage', {}).get('tokens', 0)
        return {
            'date': self.config.get('daily_usage', {}).get('date'),
            'tokens_used': used,
            'daily_limit': limit,
            'remaining': max(0, limit - used),
            'percentage': min(100, int(used / limit * 100)) if limit > 0 else 0
        }

    def set_daily_limit(self, limit: int) -> Tuple[bool, str]:
        """Set the daily token limit."""
        if limit < 1000:
            return False, "Daily limit must be at least 1,000 tokens"
        if limit > 10000000:
            return False, "Daily limit cannot exceed 10,000,000 tokens"
        self.config['daily_limit'] = limit
        self._save_config()
        return True, f"Daily limit set to {limit:,} tokens"

    def _load_config(self) -> dict:
        if self.secret_path.exists():
            try:
                data = json.loads(self.secret_path.read_text(encoding='utf-8'))
                if 'usage' not in data:
                    data['usage'] = {'total_tokens': 0, 'total_requests': 0, 'last_request': None}
                if 'daily_limit' not in data:
                    data['daily_limit'] = DEFAULT_DAILY_LIMIT
                if 'daily_usage' not in data:
                    data['daily_usage'] = {'date': None, 'tokens': 0}
                return data
            except (json.JSONDecodeError, IOError):
                pass
        return {
            'api_key': None,
            'brave_api_key': None,
            'enabled': False,
            'model': DEFAULT_MODEL,
            'usage': {
                'total_tokens': 0,
                'total_requests': 0,
                'last_request': None
            },
            'daily_limit': DEFAULT_DAILY_LIMIT,
            'daily_usage': {'date': None, 'tokens': 0}
        }

    def _save_config(self):
        self.secret_dir.mkdir(parents=True, exist_ok=True)
        self.secret_path.write_text(json.dumps(self.config, indent=2), encoding='utf-8')
        if os.name != 'nt':
            os.chmod(self.secret_path, stat.S_IRUSR | stat.S_IWUSR)

    def _mask_key(self) -> str:
        key = self.config.get('api_key')
        if not key:
            return 'Not set'
        if len(key) <= 8:
            return '****'
        return f"{key[:7]}...{key[-4:]}"

    def set_key(self, key: str) -> Tuple[bool, str]:
        if not key:
            return False, 'API key cannot be empty'
        if not key.startswith('sk-'):
            return False, 'Invalid API key format. Key should start with sk-'
        test_result, test_msg = self._test_key(key)
        if not test_result:
            return False, test_msg
        self.config['api_key'] = key
        self._save_config()
        return True, 'API key saved and verified'

    def _test_key(self, key: str) -> Tuple[bool, str]:
        try:
            headers = {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': 'test'}],
                'max_tokens': 1
            }
            response = requests.post(OPENAI_API_URL, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                return True, 'OK'
            elif response.status_code == 401:
                return False, 'Invalid API key'
            elif response.status_code == 429:
                return True, 'OK (rate limited but valid)'
            else:
                return False, f'API error: {response.status_code}'
        except requests.exceptions.Timeout:
            return False, 'Connection timeout'
        except requests.exceptions.ConnectionError:
            return False, 'Connection failed'
        except Exception as e:
            return False, str(e)

    def is_enabled(self) -> bool:
        return bool(self.config.get('enabled', False) and self.config.get('api_key'))

    def has_key(self) -> bool:
        return bool(self.config.get('api_key'))

    def set_brave_key(self, key: str) -> Tuple[bool, str]:
        if not key:
            return False, 'Brave API key cannot be empty'
        test_result, test_msg = self._test_brave_key(key)
        if not test_result:
            return False, test_msg
        self.config['brave_api_key'] = key
        self._save_config()
        return True, 'Brave Search API key saved and verified'

    def _test_brave_key(self, key: str) -> Tuple[bool, str]:
        try:
            headers = {
                'Accept': 'application/json',
                'X-Subscription-Token': key
            }
            response = requests.get(
                f'{BRAVE_SEARCH_URL}?q=test&count=1',
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, 'OK'
            elif response.status_code == 401:
                return False, 'Invalid Brave API key'
            elif response.status_code == 429:
                return True, 'OK (rate limited but valid)'
            else:
                return False, f'Brave API error: {response.status_code}'
        except requests.exceptions.Timeout:
            return False, 'Connection timeout'
        except requests.exceptions.ConnectionError:
            return False, 'Connection failed'
        except Exception as e:
            return False, str(e)

    def has_brave_key(self) -> bool:
        return bool(self.config.get('brave_api_key'))

    def brave_search(self, query: str, count: int = 5) -> Tuple[bool, List[Dict]]:
        if not self.has_brave_key():
            return False, []
        try:
            headers = {
                'Accept': 'application/json',
                'X-Subscription-Token': self.config['brave_api_key']
            }
            response = requests.get(
                f'{BRAVE_SEARCH_URL}?q={query}&count={count}',
                headers=headers,
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get('web', {}).get('results', []):
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'description': item.get('description', '')
                    })
                return True, results
            return False, []
        except Exception:
            return False, []

    def enable(self) -> Tuple[bool, str]:
        if not self.config.get('api_key'):
            return False, 'No API key configured. Use: includecpp ai key <YOUR_KEY>'
        self.config['enabled'] = True
        self._save_config()
        return True, 'AI features enabled'

    def disable(self) -> Tuple[bool, str]:
        self.config['enabled'] = False
        self._save_config()
        return True, 'AI features disabled'

    def get_model(self) -> str:
        return self.config.get('model', DEFAULT_MODEL)

    def set_model(self, model: str) -> Tuple[bool, str]:
        if model not in MODELS:
            available = ', '.join(MODELS.keys())
            return False, f'Unknown model. Available: {available}'
        self.config['model'] = model
        self._save_config()
        return True, f'Model set to {model}'

    def list_models(self) -> List[Dict[str, Any]]:
        current = self.get_model()
        result = []
        for name, info in MODELS.items():
            result.append({
                'name': name,
                'context': info['context'],
                'active': name == current
            })
        return result

    def get_info(self) -> Dict[str, Any]:
        usage = self.config.get('usage', {})
        return {
            'key_set': bool(self.config.get('api_key')),
            'key_preview': self._mask_key(),
            'enabled': self.config.get('enabled', False),
            'model': self.config.get('model', DEFAULT_MODEL),
            'total_tokens': usage.get('total_tokens', 0),
            'total_requests': usage.get('total_requests', 0),
            'last_request': usage.get('last_request')
        }

    def _update_usage(self, tokens: int):
        if 'usage' not in self.config:
            self.config['usage'] = {'total_tokens': 0, 'total_requests': 0, 'last_request': None}
        self.config['usage']['total_tokens'] = self.config['usage'].get('total_tokens', 0) + tokens
        self.config['usage']['total_requests'] = self.config['usage'].get('total_requests', 0) + 1
        self.config['usage']['last_request'] = datetime.now().isoformat()
        self._reset_daily_if_needed()
        self.config['daily_usage']['tokens'] = self.config['daily_usage'].get('tokens', 0) + tokens
        self._save_config()

    def query(self, system_prompt: str, user_prompt: str, temperature: float = 0.3,
              timeout: int = 180) -> Tuple[bool, str]:
        if not self.config.get('api_key'):
            return False, 'No API key configured'
        can_proceed, limit_warning = self._check_daily_limit()
        if not can_proceed:
            return False, limit_warning
        model = self.config.get('model', DEFAULT_MODEL)
        model_info = MODELS.get(model, MODELS[DEFAULT_MODEL])
        headers = {
            'Authorization': f'Bearer {self.config["api_key"]}',
            'Content-Type': 'application/json'
        }
        token_limit = min(16000, model_info['context'] // 2)

        # o1 models use different message format (no system message, combined into user)
        # gpt-5 models use max_completion_tokens instead of max_tokens
        is_o1_model = model.startswith('o1')
        is_gpt5_model = model.startswith('gpt-5')

        if is_o1_model:
            # o1 models: combine system + user into single user message
            combined_content = f"{system_prompt}\n\n---\n\n{user_prompt}"
            data = {
                'model': model_info['endpoint'],
                'messages': [
                    {'role': 'user', 'content': combined_content}
                ],
                'max_completion_tokens': token_limit
            }
            # o1 models don't support temperature
        elif is_gpt5_model:
            # gpt-5 models: use max_completion_tokens, no custom temperature
            data = {
                'model': model_info['endpoint'],
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'max_completion_tokens': token_limit
            }
        else:
            data = {
                'model': model_info['endpoint'],
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'max_tokens': token_limit,
                'temperature': temperature
            }
        try:
            response = requests.post(OPENAI_API_URL, headers=headers, json=data, timeout=timeout)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                tokens = result.get('usage', {}).get('total_tokens', 0)
                self._update_usage(tokens)
                return True, content
            elif response.status_code == 401:
                return False, 'Invalid API key'
            elif response.status_code == 429:
                return False, 'Rate limit exceeded. Please wait and try again'
            elif response.status_code == 503:
                return False, 'OpenAI service unavailable'
            else:
                try:
                    err = response.json().get('error', {}).get('message', '')
                except:
                    err = response.text
                return False, f'API error ({response.status_code}): {err}'
        except requests.exceptions.Timeout:
            return False, 'Request timeout'
        except requests.exceptions.ConnectionError:
            return False, 'Connection failed. Check your internet connection'
        except Exception as e:
            return False, str(e)

    def _build_prompt_with_docs(self, base_prompt: str, include_build_info: bool = True) -> str:
        parts = [INCLUDECPP_CONTEXT]
        docs = self._get_documentation()
        if docs:
            doc_section = docs[:8000] if len(docs) > 8000 else docs
            parts.append(f'\nIncludeCPP Documentation:\n{doc_section}')
        if include_build_info:
            build_info = self._get_build_info()
            if build_info:
                parts.append(build_info)
        parts.append(f'\n\n---\n\n{base_prompt}')
        return '\n'.join(parts)

    def optimize_code(self, files: Dict[str, str], custom_task: Optional[str] = None) -> Tuple[bool, str, List[Dict]]:
        if not files:
            return False, 'No files provided', []
        file_content = ''
        for path, content in files.items():
            file_content += f'\nFILE: {path}\n```cpp\n{content}\n```\n'
        if custom_task:
            prompt = f'Task: {custom_task}\n\nFiles:\n{file_content}'
            system = SYSTEM_PROMPT_AGENT
        else:
            prompt = f'Optimize the following C++ files for performance, safety, and pybind11 compatibility:\n{file_content}'
            system = SYSTEM_PROMPT_OPTIMIZE
        prompt = self._build_prompt_with_docs(prompt)
        # v3.2.2: Use longer timeout (5 min) for optimize operations with multiple files
        timeout = 300 if len(files) > 1 else 180
        success, response = self.query(system, prompt, timeout=timeout)
        if not success:
            return False, response, []
        changes = self._parse_file_changes(response)
        return True, response, changes

    def fix_code(self, files: Dict[str, str]) -> Tuple[bool, str, List[Dict]]:
        if not files:
            return False, 'No files provided', []
        file_content = ''
        for path, content in files.items():
            file_content += f'\nFILE: {path}\n```cpp\n{content}\n```\n'
        prompt = f'Analyze and fix issues in these C++ files:\n{file_content}'
        prompt = self._build_prompt_with_docs(prompt)
        success, response = self.query(SYSTEM_PROMPT_FIX, prompt)
        if not success:
            return False, response, []
        changes = self._parse_file_changes(response)
        return True, response, changes

    def analyze_build_error(self, error: str, source_files: Dict[str, str]) -> Tuple[bool, str]:
        context = f'Build error:\n{error}\n\n'
        if source_files:
            context += 'Relevant source files:\n'
            for path, content in list(source_files.items())[:3]:
                lines = content.split('\n')
                preview = '\n'.join(lines[:100])
                context += f'\nFILE: {path}\n```cpp\n{preview}\n```\n'
        context = self._build_prompt_with_docs(context)
        success, response = self.query(SYSTEM_PROMPT_BUILD_ERROR, context)
        return success, response

    def auto_fix_build_error(self, error: str, source_files: Dict[str, str],
                              plugin_content: Optional[str] = None,
                              module_name: Optional[str] = None,
                              think: bool = False,
                              think_twice: bool = False,
                              think_three: bool = False,
                              use_websearch: bool = False) -> Tuple[bool, str, List[Dict], List[Dict]]:
        error_category = self._categorize_error(error)
        context = f'Build error:\n{error}\n\nError category: {error_category}\n\n'
        if module_name:
            context += f'Module name: {module_name}\n\n'
        if use_websearch and self.has_brave_key():
            search_query = f'C++ pybind11 {error[:100]}'
            success, results = self.brave_search(search_query, count=5)
            if success and results:
                context += 'Web Research Results:\n'
                for r in results:
                    context += f'- {r["title"]}: {r["description"][:200]}\n'
                context += '\n'
        if source_files:
            context += 'Source files (with line numbers):\n'
            max_lines = self._get_context_limit(think, think_twice, think_three)
            for path, content in source_files.items():
                lines = content.split('\n')
                if len(lines) > max_lines:
                    preview = '\n'.join(lines[:max_lines])
                    numbered = self._add_line_numbers(preview)
                    context += f'\nFILE: {path}\n```cpp\n{numbered}\n... ({len(lines) - max_lines} more lines)\n```\n'
                else:
                    numbered = self._add_line_numbers(content)
                    context += f'\nFILE: {path}\n```cpp\n{numbered}\n```\n'
        if plugin_content:
            context += f'\nPlugin definition (.cp file):\n```\n{plugin_content}\n```\n'
        if think_three:
            context += '\nIMPORTANT: This is professional-grade analysis. Take your time to plan thoroughly before implementing.'
        elif think_twice:
            context += '\nIMPORTANT: Analyze thoroughly. This is a complex codebase requiring careful consideration.'
        elif think:
            context += '\nIMPORTANT: Think step by step before fixing.'
        context = self._build_prompt_with_docs(context)
        system_prompt = SYSTEM_PROMPT_THINK3_PLAN if think_three else SYSTEM_PROMPT_AUTO_FIX
        temperature = 0.1 if think_three else (0.2 if think_twice else 0.3)
        success, response = self.query(system_prompt, context, temperature=temperature)
        if not success:
            return False, response, [], []
        file_changes, cli_commands = self._parse_auto_fix_response(response)
        return True, response, file_changes, cli_commands

    def _parse_auto_fix_response(self, response: str) -> Tuple[List[Dict], List[Dict]]:
        file_changes = []
        cli_commands = []
        lines = response.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == 'ACTION: FILE_CHANGE':
                i += 1
                if i < len(lines) and lines[i].strip().startswith('FILE:'):
                    file_path = lines[i].strip()[5:].strip()
                    i += 1
                    content_lines = []
                    in_code = False
                    while i < len(lines):
                        l = lines[i]
                        if l.strip().startswith('```cpp'):
                            in_code = True
                            i += 1
                            continue
                        if in_code and l.strip().startswith('```'):
                            break
                        if in_code:
                            content_lines.append(l)
                        i += 1
                    if content_lines:
                        file_changes.append({
                            'file': file_path,
                            'content': '\n'.join(content_lines)
                        })
            elif line == 'ACTION: CLI_COMMAND':
                i += 1
                command = None
                reason = None
                while i < len(lines):
                    l = lines[i].strip()
                    if l.startswith('COMMAND:'):
                        command = l[8:].strip()
                    elif l.startswith('REASON:'):
                        reason = l[7:].strip()
                    elif l.startswith('ACTION:') or l.startswith('CANNOT_FIX:'):
                        break
                    i += 1
                    if command and reason:
                        break
                if command:
                    cli_commands.append({
                        'command': command,
                        'reason': reason or ''
                    })
                continue
            elif line.startswith('CANNOT_FIX:'):
                break
            i += 1
        return file_changes, cli_commands

    def ask_question(self, question: str, files: Dict[str, str], plugins: Dict[str, str] = None,
                      think: bool = False, think_twice: bool = False, think_three: bool = False,
                      use_websearch: bool = False) -> Tuple[bool, str]:
        context_parts = []
        if use_websearch and self.has_brave_key():
            search_query = f'C++ pybind11 {question[:100]}'
            success, results = self.brave_search(search_query, count=5)
            if success and results:
                context_parts.append('Web Research Results:')
                for r in results:
                    context_parts.append(f'- {r["title"]}: {r["description"][:200]}')
                context_parts.append('')
        max_lines = self._get_context_limit(think, think_twice, think_three)
        if files:
            context_parts.append('Project files:')
            for path, content in files.items():
                lines = content.split('\n')
                if len(lines) > max_lines:
                    preview = '\n'.join(lines[:max_lines])
                    preview += f'\n... ({len(lines) - max_lines} more lines)'
                else:
                    preview = content
                ext = Path(path).suffix
                lang = 'cpp' if ext in ['.cpp', '.h', '.hpp', '.c'] else 'python' if ext == '.py' else ''
                context_parts.append(f'\nFILE: {path}\n```{lang}\n{preview}\n```')
        if plugins:
            context_parts.append('\nPlugin definitions:')
            for path, content in plugins.items():
                context_parts.append(f'\nPLUGIN: {path}\n```\n{content}\n```')
        # v3.2.2: Add CLI context for questions about commands/flags
        cli_context = self._get_cli_context(question)
        if cli_context:
            context_parts.append(cli_context)
        context = '\n'.join(context_parts)
        prompt = f'Question: {question}\n\n{context}'
        if think_three:
            prompt += '\n\nIMPORTANT: Provide thorough, professional-grade analysis with detailed reasoning.'
        elif think_twice:
            prompt += '\n\nIMPORTANT: Analyze carefully and consider multiple angles before answering.'
        elif think:
            prompt += '\n\nIMPORTANT: Think step by step before answering.'
        prompt = self._build_prompt_with_docs(prompt)
        temperature = 0.1 if think_three else (0.2 if think_twice else 0.3)
        timeout = None if think_three else (420 if think_twice else (300 if think else 180))
        return self.query(SYSTEM_PROMPT_ASK, prompt, temperature=temperature, timeout=timeout)

    def edit_code(self, task: str, files: Dict[str, str], think: bool = False,
                   think_twice: bool = False, think_three: bool = False,
                   use_websearch: bool = False) -> Tuple[bool, str, List[Dict]]:
        if not files:
            return False, 'No files provided', []
        context_parts = []
        if use_websearch and self.has_brave_key():
            search_query = f'C++ pybind11 {task[:100]}'
            success, results = self.brave_search(search_query, count=5)
            if success and results:
                context_parts.append('Web Research Results:')
                for r in results:
                    context_parts.append(f'- {r["title"]}: {r["description"][:200]}')
                context_parts.append('')
        max_lines = self._get_context_limit(think, think_twice, think_three)
        file_content = ''
        for path, content in files.items():
            lines = content.split('\n')
            if len(lines) > max_lines:
                preview = '\n'.join(lines[:max_lines])
                preview += f'\n... ({len(lines) - max_lines} more lines)'
            else:
                preview = content
            ext = Path(path).suffix
            lang = 'cpp' if ext in ['.cpp', '.h', '.hpp', '.c'] else 'python' if ext == '.py' else ''
            file_content += f'\nFILE: {path}\n```{lang}\n{preview}\n```\n'
        prompt = '\n'.join(context_parts) + f'Edit task: {task}\n\nFiles:\n{file_content}'
        if think_three:
            prompt += '\n\nIMPORTANT: This is professional-grade editing. Plan thoroughly, consider all implications, and implement carefully.'
            prompt += QUESTION_PROMPT_ADDITION
        elif think_twice:
            prompt += '\n\nIMPORTANT: Think carefully before making changes. Consider edge cases and potential issues.'
            prompt += QUESTION_PROMPT_ADDITION
        elif think:
            prompt += '\n\nIMPORTANT: Think step by step before editing.'
        prompt = self._build_prompt_with_docs(prompt)
        temperature = 0.1 if think_three else (0.2 if think_twice else 0.3)
        timeout = None if think_three else (420 if think_twice else (300 if think else 180))
        success, response = self.query(SYSTEM_PROMPT_EDIT, prompt, temperature=temperature, timeout=timeout)
        if not success:
            return False, response, [], None
        question = self._extract_question(response)
        if question:
            return True, response, [], question
        changes = self._parse_file_changes(response)
        return True, response, changes, None

    def _extract_question(self, response: str) -> Optional[Dict]:
        """Extract ASK_USER question from AI response."""
        import re
        match = re.search(r'ASK_USER:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
        if not match:
            return None
        question = match.group(1).strip()
        options = []
        opts_match = re.search(r'OPTIONS:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
        if opts_match:
            opts_str = opts_match.group(1).strip()
            options = [o.strip() for o in opts_str.split('|') if o.strip()]
        return {'question': question, 'options': options}

    def continue_with_answer(self, original_prompt: str, ai_question: str, user_answer: str,
                              think_twice: bool = False, think_three: bool = False) -> Tuple[bool, str, List[Dict]]:
        """Continue edit_code after user answers a question."""
        continuation = f'{original_prompt}\n\nYou asked: {ai_question}\nUser answered: {user_answer}\n\nNow proceed with the edit based on this answer.'
        temperature = 0.1 if think_three else (0.2 if think_twice else 0.3)
        timeout = None if think_three else (420 if think_twice else 180)
        success, response = self.query(SYSTEM_PROMPT_EDIT, continuation, temperature=temperature, timeout=timeout)
        if not success:
            return False, response, []
        changes = self._parse_file_changes(response)
        return True, response, changes

    def generate(self, task: str, files: Dict[str, str], project_root: Path,
                 think: bool = False, think_twice: bool = False, think_three: bool = False,
                 use_websearch: bool = False, max_context: bool = False,
                 plan_mode: bool = False, new_module: str = None,
                 skip_tool_execution: bool = False) -> Tuple[bool, str, List[Dict]]:
        """Super assistant with tool execution."""
        import platform
        import subprocess

        # Early fail-fast checks
        if not self.config.get('api_key'):
            return False, 'No API key configured. Run: includecpp ai setup', []

        # Build tools list for prompt
        tools_list = '\n'.join([
            f"- {name}: {info['desc']}\n  Format:\n  {info['format']}"
            for name, info in GENERATE_TOOLS.items()
        ])

        # System info
        system_info = f"{platform.system()} ({platform.release()})"

        # Choose prompt based on mode
        if new_module:
            system_prompt = SYSTEM_PROMPT_NEW_MODULE.format(
                module_name=new_module,
                description=task
            )
        elif plan_mode:
            system_prompt = SYSTEM_PROMPT_GENERATE_PLAN.format(
                base_prompt=SYSTEM_PROMPT_GENERATE.format(
                    tools_list=tools_list,
                    project_root=str(project_root),
                    system_info=system_info,
                    includecpp_context=INCLUDECPP_CONTEXT
                )
            )
        else:
            system_prompt = SYSTEM_PROMPT_GENERATE.format(
                tools_list=tools_list,
                project_root=str(project_root),
                system_info=system_info,
                includecpp_context=INCLUDECPP_CONTEXT
            )

        # Context limits
        if max_context:
            max_lines = 50000
        else:
            max_lines = self._get_context_limit(think, think_twice, think_three)

        # Build file context
        file_context = self._build_file_context(files, max_lines)

        # Web search if enabled
        web_context = ''
        if use_websearch and self.has_brave_key():
            success, results = self.brave_search(f'C++ pybind11 {task[:100]}')
            if success and results:
                web_context = '\n\nWEB RESEARCH:\n' + '\n'.join(
                    f"- {r['title']}: {r['description'][:200]}" for r in results[:5]
                )

        # Build prompt
        prompt = f'Task: {task}\n\n'
        if file_context:
            prompt += f'Project Files:\n{file_context}\n'
        if web_context:
            prompt += web_context

        prompt = self._build_prompt_with_docs(prompt)

        # Temperature and timeout (reduced for faster failure detection)
        temperature = 0.1 if think_three else (0.2 if think_twice else 0.3)
        timeout = 180 if think_three else (120 if think_twice else (90 if think else 60))

        # Execute with tool loop
        all_changes = []
        max_iterations = 10

        for iteration in range(max_iterations):
            success, response = self.query(system_prompt, prompt, temperature, timeout)
            if not success:
                return False, response, []

            # Parse tool calls
            tool_calls = self._parse_tool_calls(response)

            if not tool_calls:
                # No more tools, parse final changes
                changes = self._parse_file_changes(response)
                all_changes.extend(changes)
                break

            # Execute tools (unless skip_tool_execution is set)
            tool_results = []
            for tool in tool_calls:
                # Collect file changes from WRITE_FILE/EDIT_FILE
                if tool['name'] in ['WRITE_FILE', 'EDIT_FILE'] and tool.get('content'):
                    all_changes.append({
                        'file': tool.get('path', 'unknown'),
                        'content': tool['content'],
                        'changes_desc': tool.get('changes', ['Tool-generated']),
                        'confirm_required': []
                    })

                # Skip actual execution if flag is set
                if skip_tool_execution:
                    tool_results.append(f"{tool['name']} SKIPPED (parse-only mode)")
                    continue

                result = self._execute_tool(tool, project_root)
                tool_results.append(result)

            # Add tool results to prompt for next iteration
            if not skip_tool_execution:
                prompt += '\n\nTOOL RESULTS:\n' + '\n---\n'.join(tool_results)

        # Deduplicate changes by file path (keep last version of each file)
        seen_files = {}
        for change in all_changes:
            file_path = change.get('file', '')
            if file_path:
                seen_files[file_path] = change
        deduplicated_changes = list(seen_files.values())

        return True, response, deduplicated_changes

    def _parse_tool_calls(self, response: str) -> List[Dict]:
        """Parse TOOL: blocks from AI response."""
        import re
        import json
        tools = []

        # Primary pattern: TOOL: <NAME>\n<params>
        pattern = r'TOOL:\s*(\w+)\n((?:(?!TOOL:).)*?)(?=TOOL:|$)'
        matches = re.findall(pattern, response, re.DOTALL)

        for name, params in matches:
            tool = {'name': name.strip()}

            # Parse PATH
            path_match = re.search(r'PATH:\s*(.+?)(?:\n|$)', params)
            if path_match:
                tool['path'] = path_match.group(1).strip()

            # Parse PATTERN
            pattern_match = re.search(r'PATTERN:\s*(.+?)(?:\n|$)', params)
            if pattern_match:
                tool['pattern'] = pattern_match.group(1).strip()

            # Parse CMD
            cmd_match = re.search(r'CMD:\s*(.+?)(?:\n|$)', params)
            if cmd_match:
                tool['cmd'] = cmd_match.group(1).strip()

            # Parse CHANGES
            changes_match = re.search(r'CHANGES:\n((?:- .+\n?)+)', params)
            if changes_match:
                tool['changes'] = [c.strip('- \n') for c in changes_match.group(1).split('\n') if c.strip().startswith('-')]

            # Parse code block
            code_match = re.search(r'```(?:\w+)?\n(.*?)```', params, re.DOTALL)
            if code_match:
                tool['content'] = code_match.group(1)

            tools.append(tool)

        # Fallback: Parse JSON-style tool calls (e.g., WRITE_FILE{"path":...,"content":...})
        if not tools:
            json_pattern = r'(WRITE_FILE|EDIT_FILE|READ_FILE|DELETE_FILE|CREATE_FOLDER|LIST_FOLDER|SEARCH_FILES|GREP|RUN_CMD|INCLUDECPP_CMD)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
            json_matches = re.findall(json_pattern, response, re.DOTALL)
            for name, json_body in json_matches:
                try:
                    # Try to parse as JSON
                    data = json.loads('{' + json_body + '}')
                    tool = {'name': name}
                    if 'path' in data:
                        tool['path'] = data['path']
                    if 'content' in data:
                        tool['content'] = data['content']
                    if 'pattern' in data:
                        tool['pattern'] = data['pattern']
                    if 'cmd' in data:
                        tool['cmd'] = data['cmd']
                    tools.append(tool)
                except json.JSONDecodeError:
                    pass

        return tools

    def _execute_tool(self, tool: Dict, project_root: Path) -> str:
        """Execute a single tool and return result string."""
        import subprocess
        import re as re_module

        name = tool['name']

        try:
            if name == 'READ_FILE':
                path = self._resolve_path(tool.get('path', ''), project_root)
                if path.exists():
                    content = path.read_text(encoding='utf-8', errors='replace')
                    lines = content.split('\n')
                    if len(lines) > 500:
                        content = '\n'.join(lines[:500]) + f'\n... ({len(lines)-500} more lines)'
                    return f"READ_FILE {path}:\n```\n{content}\n```"
                return f"READ_FILE ERROR: File not found: {path}"

            elif name == 'WRITE_FILE':
                path = self._resolve_path(tool.get('path', ''), project_root)
                content = tool.get('content', '')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
                return f"WRITE_FILE SUCCESS: Created {path}"

            elif name == 'EDIT_FILE':
                path = self._resolve_path(tool.get('path', ''), project_root)
                content = tool.get('content', '')
                if path.exists():
                    path.write_text(content, encoding='utf-8')
                    return f"EDIT_FILE SUCCESS: Modified {path}"
                return f"EDIT_FILE ERROR: File not found: {path}"

            elif name == 'DELETE_FILE':
                path = self._resolve_path(tool.get('path', ''), project_root)
                if path.exists():
                    path.unlink()
                    return f"DELETE_FILE SUCCESS: Deleted {path}"
                return f"DELETE_FILE ERROR: File not found: {path}"

            elif name == 'CREATE_FOLDER':
                path = self._resolve_path(tool.get('path', ''), project_root)
                path.mkdir(parents=True, exist_ok=True)
                return f"CREATE_FOLDER SUCCESS: Created {path}"

            elif name == 'LIST_FOLDER':
                path = self._resolve_path(tool.get('path', '.'), project_root)
                if path.is_dir():
                    items = list(path.iterdir())[:50]
                    listing = '\n'.join(f"  {'[D]' if p.is_dir() else '[F]'} {p.name}" for p in items)
                    return f"LIST_FOLDER {path}:\n{listing}"
                return f"LIST_FOLDER ERROR: Not a directory: {path}"

            elif name == 'SEARCH_FILES':
                pattern = tool.get('pattern', '*')
                base = self._resolve_path(tool.get('path', '.'), project_root)
                matches = list(base.glob(pattern))[:100]
                return f"SEARCH_FILES {pattern}:\n" + '\n'.join(f"  {m}" for m in matches)

            elif name == 'GREP':
                pattern = tool.get('pattern', '')
                path = self._resolve_path(tool.get('path', '.'), project_root)
                results = []
                if path.is_file():
                    files_to_search = [path]
                else:
                    files_to_search = list(path.rglob('*'))[:50]
                for f in files_to_search:
                    if f.is_file() and f.suffix in ['.cpp', '.h', '.py', '.cp', '.md', '.txt', '.hpp', '.c']:
                        try:
                            content = f.read_text(encoding='utf-8', errors='replace')
                            for i, line in enumerate(content.split('\n'), 1):
                                if re_module.search(pattern, line, re_module.IGNORECASE):
                                    results.append(f"  {f}:{i}: {line[:100]}")
                        except:
                            pass
                return f"GREP {pattern}:\n" + '\n'.join(results[:50])

            elif name == 'RUN_CMD':
                cmd = tool.get('cmd', '')
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, cwd=project_root)
                output = result.stdout[:2000] if result.returncode == 0 else result.stderr[:2000]
                return f"RUN_CMD `{cmd}`:\nExit: {result.returncode}\n{output}"

            elif name == 'INCLUDECPP_CMD':
                cmd = tool.get('cmd', '')
                full_cmd = f'includecpp {cmd}'
                result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=120, cwd=project_root)
                output = result.stdout[:2000] if result.returncode == 0 else result.stderr[:2000]
                return f"INCLUDECPP_CMD `{cmd}`:\nExit: {result.returncode}\n{output}"

            else:
                return f"UNKNOWN TOOL: {name}"

        except Exception as e:
            return f"TOOL ERROR ({name}): {str(e)}"

    def _resolve_path(self, path_str: str, project_root: Path) -> Path:
        """Resolve path relative to project root or absolute."""
        if not path_str:
            return project_root
        p = Path(path_str)
        if p.is_absolute():
            return p
        return project_root / p

    def _build_file_context(self, files: Dict[str, str], max_lines: int) -> str:
        """Build file context string with line limits."""
        context_parts = []
        for path, content in files.items():
            lines = content.split('\n')
            if len(lines) > max_lines:
                preview = '\n'.join(lines[:max_lines])
                preview += f'\n... ({len(lines) - max_lines} more lines)'
            else:
                preview = content
            ext = Path(path).suffix
            lang = 'cpp' if ext in ['.cpp', '.h', '.hpp', '.c'] else 'python' if ext == '.py' else ''
            context_parts.append(f'\nFILE: {path}\n```{lang}\n{preview}\n```')
        return '\n'.join(context_parts)

    def get_tools_info(self) -> str:
        """Return formatted tools list for ai tools command."""
        lines = ["Available AI Tools:", ""]
        for name, info in GENERATE_TOOLS.items():
            lines.append(f"  {name}")
            lines.append(f"    {info['desc']}")
            fmt_line = info['format'].split('\n')[0]
            lines.append(f"    Format: {fmt_line}")
            lines.append("")
        return '\n'.join(lines)

    def _parse_file_changes(self, response: str) -> List[Dict]:
        import re

        # Only return empty if response ONLY contains "no changes" with no code blocks
        lower_response = response.lower()
        has_code_blocks = '```' in response
        no_change_phrases = [
            'no_changes_needed', 'no_issues_found', 'no changes are needed',
            'no changes necessary', 'no modifications required'
        ]
        # Only skip if we have no code AND a definite "no changes" statement
        if not has_code_blocks and any(p in lower_response for p in no_change_phrases):
            return []

        changes = []
        lines = response.split('\n')
        current_file = None
        current_content = []
        current_changes_desc = []
        in_code_block = False
        in_changes_section = False
        confirm_required = []
        code_block_lang = None

        for line in lines:
            stripped = line.strip()

            if stripped.startswith('CONFIRM_REQUIRED:'):
                confirm_required.append(stripped[17:].strip())
                continue

            # Detect FILE: in various formats
            file_match = re.match(r'^(?:\*\*)?(?:###?\s*)?FILE[:\s*]+(.+?)(?:\*\*)?$', stripped, re.IGNORECASE)
            if file_match:
                if current_file and current_content:
                    changes.append({
                        'file': current_file,
                        'content': '\n'.join(current_content),
                        'changes_desc': current_changes_desc.copy(),
                        'confirm_required': confirm_required.copy()
                    })
                    confirm_required = []
                current_file = file_match.group(1).strip().strip('`').strip('*').strip()
                current_content = []
                current_changes_desc = []
                in_code_block = False
                in_changes_section = False
                continue

            # Detect CHANGES: section
            if re.match(r'^(?:\*\*)?(?:###?\s*)?CHANGES[:\s*]+(?:\*\*)?$', stripped, re.IGNORECASE):
                in_changes_section = True
                continue

            if in_changes_section and not in_code_block:
                if stripped.startswith('- ') or stripped.startswith('* '):
                    current_changes_desc.append(stripped[2:])
                elif stripped.startswith('```'):
                    in_changes_section = False
                    in_code_block = True
                    code_block_lang = stripped[3:].strip()
                continue

            # Detect code block start
            if stripped.startswith('```') and not in_code_block:
                in_code_block = True
                code_block_lang = stripped[3:].strip()
                in_changes_section = False
                continue

            # Detect code block end
            if stripped == '```' and in_code_block:
                in_code_block = False
                code_block_lang = None
                continue

            # Collect code content
            if in_code_block and current_file:
                current_content.append(line)

        # Save last file if exists
        if current_file and current_content:
            changes.append({
                'file': current_file,
                'content': '\n'.join(current_content),
                'changes_desc': current_changes_desc,
                'confirm_required': confirm_required
            })

        # Fallback: try to parse code blocks if no FILE: markers found
        if not changes and has_code_blocks:
            changes = self._fallback_parse_code_blocks(response)

        return changes

    def _fallback_parse_code_blocks(self, response: str) -> List[Dict]:
        """Fallback parser for responses that don't follow the exact format."""
        import re
        changes = []

        # Find all code blocks (cpp, c++, c, h, or unmarked)
        blocks = re.findall(r'```(?:cpp|c\+\+|c|h)?\n(.*?)```', response, re.DOTALL | re.IGNORECASE)

        # Find file references in text
        file_patterns = [
            r'(?:file|path|in|modify|update|editing)[:\s]*[`"]?([^\s`"\n]+\.(?:cpp|h|hpp|c))[`"]?',
            r'[`"]([^\s`"\n]+\.(?:cpp|h|hpp|c))[`"]',
            r'\b([a-zA-Z_][a-zA-Z0-9_]*\.(?:cpp|h|hpp|c))\b'
        ]
        file_matches = []
        for pattern in file_patterns:
            file_matches.extend(re.findall(pattern, response, re.IGNORECASE))
        # Deduplicate while preserving order
        seen = set()
        unique_files = []
        for f in file_matches:
            if f.lower() not in seen:
                seen.add(f.lower())
                unique_files.append(f)

        for idx, content in enumerate(blocks):
            if not content.strip():
                continue
            # Try to match file from references, otherwise use index
            file_name = unique_files[idx] if idx < len(unique_files) else f'file_{idx}.cpp'
            changes.append({
                'file': file_name,
                'content': content.strip(),
                'changes_desc': ['Parsed from code block'],
                'confirm_required': []
            })

        return changes


_ai_manager_instance = None


# ============================================================================
# Verbose Output System for AI Operations
# ============================================================================

class AIVerboseOutput:
    """Verbose output manager for AI operations with real-time status updates."""

    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'cyan': '\033[36m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'magenta': '\033[35m',
        'blue': '\033[34m',
        'red': '\033[31m',
        'white': '\033[37m',
    }

    # Status icons and messages - with ASCII fallbacks for Windows
    PHASES = {
        'init': ('*' if not _UNICODE_OK else '⚙', 'cyan', 'Initializing'),
        'context': ('*' if not _UNICODE_OK else '📋', 'blue', 'Building context'),
        'thinking': ('*' if not _UNICODE_OK else '🧠', 'magenta', 'Thinking'),
        'planning': ('*' if not _UNICODE_OK else '📝', 'yellow', 'Planning'),
        'analyzing': ('>' if not _UNICODE_OK else '🔍', 'cyan', 'Analyzing'),
        'generating': ('+' if not _UNICODE_OK else '✨', 'green', 'Generating'),
        'writing': ('>' if not _UNICODE_OK else '📄', 'blue', 'Writing'),
        'editing': ('>' if not _UNICODE_OK else '✏️', 'yellow', 'Editing'),
        'reading': ('>' if not _UNICODE_OK else '👁', 'cyan', 'Reading'),
        'searching': ('>' if not _UNICODE_OK else '🔎', 'blue', 'Searching'),
        'executing': ('!' if not _UNICODE_OK else '⚡', 'magenta', 'Executing'),
        'converting': ('~' if not _UNICODE_OK else '🔄', 'cyan', 'Converting'),
        'optimizing': ('!' if not _UNICODE_OK else '⚡', 'green', 'Optimizing'),
        'websearch': ('@' if not _UNICODE_OK else '🌐', 'blue', 'Web searching'),
        'parsing': ('>' if not _UNICODE_OK else '📊', 'cyan', 'Parsing response'),
        'applying': ('+' if not _UNICODE_OK else '💾', 'green', 'Applying changes'),
        'complete': ('[OK]' if not _UNICODE_OK else '✅', 'green', 'Complete'),
        'error': ('[ERR]' if not _UNICODE_OK else '❌', 'red', 'Error'),
        'warning': ('[!]' if not _UNICODE_OK else '⚠️', 'yellow', 'Warning'),
        'waiting': ('...' if not _UNICODE_OK else '⏳', 'dim', 'Waiting for API'),
        'tool': ('#' if not _UNICODE_OK else '🔧', 'cyan', 'Running tool'),
    }

    def __init__(self, enabled: bool = True, use_colors: bool = True):
        self.enabled = enabled
        self.use_colors = use_colors and self._supports_color()
        self.current_phase = None
        self.indent_level = 0
        self.start_time = None
        self._last_line_length = 0

    def _supports_color(self) -> bool:
        """Check if terminal supports colors."""
        import sys
        if not hasattr(sys.stdout, 'isatty'):
            return False
        if not sys.stdout.isatty():
            return False
        import os
        if os.name == 'nt':
            # Windows: enable ANSI support
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except Exception:
                return False
        return True

    def _color(self, text: str, color: str) -> str:
        """Apply color to text if enabled."""
        if not self.use_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"

    def _get_indent(self) -> str:
        """Get current indentation."""
        return "  " * self.indent_level

    def start(self, operation: str):
        """Start verbose output for an operation."""
        if not self.enabled:
            return
        import time
        self.start_time = time.time()
        print()
        print(self._color("=" * 60, 'dim'))
        print(self._color(f"  AI Operation: {operation}", 'bold'))
        print(self._color("=" * 60, 'dim'))
        print()

    def end(self, success: bool = True, message: str = None):
        """End verbose output."""
        if not self.enabled:
            return
        import time
        elapsed = time.time() - self.start_time if self.start_time else 0
        print()
        print(self._color("-" * 60, 'dim'))
        if success:
            icon, color, _ = self.PHASES['complete']
            status = message or "Operation completed successfully"
            print(f"  {icon} {self._color(status, color)}")
        else:
            icon, color, _ = self.PHASES['error']
            status = message or "Operation failed"
            print(f"  {icon} {self._color(status, color)}")
        print(f"  {self._color(f'Time: {elapsed:.2f}s', 'dim')}")
        print(self._color("=" * 60, 'dim'))
        print()

    def phase(self, phase_name: str, detail: str = None):
        """Show a new phase in the operation."""
        if not self.enabled:
            return
        if phase_name not in self.PHASES:
            phase_name = 'thinking'
        icon, color, label = self.PHASES[phase_name]
        indent = self._get_indent()
        if detail:
            print(f"{indent}{icon} {self._color(label, color)}: {detail}")
        else:
            print(f"{indent}{icon} {self._color(label, color)}...")
        self.current_phase = phase_name

    def status(self, message: str, phase: str = None):
        """Show a status message."""
        if not self.enabled:
            return
        indent = self._get_indent()
        if phase and phase in self.PHASES:
            icon, color, _ = self.PHASES[phase]
            print(f"{indent}{icon} {self._color(message, color)}")
        else:
            print(f"{indent}  {self._color(message, 'dim')}")

    def detail(self, label: str, value: str):
        """Show a detail line."""
        if not self.enabled:
            return
        indent = self._get_indent()
        print(f"{indent}  {self._color(label + ':', 'dim')} {value}")

    def progress(self, current: int, total: int, label: str = None):
        """Show progress indicator."""
        if not self.enabled:
            return
        indent = self._get_indent()
        pct = int((current / total) * 100) if total > 0 else 0
        bar_width = 30
        filled = int(bar_width * current / total) if total > 0 else 0
        fill_char = '#' if not _UNICODE_OK else '█'
        empty_char = '-' if not _UNICODE_OK else '░'
        bar = fill_char * filled + empty_char * (bar_width - filled)
        label_str = f" {label}" if label else ""
        print(f"\r{indent}  [{self._color(bar, 'cyan')}] {pct}%{label_str}", end='', flush=True)
        if current >= total:
            print()

    def tool_call(self, tool_name: str, params: dict = None):
        """Show a tool being called."""
        if not self.enabled:
            return
        indent = self._get_indent()
        icon, color, _ = self.PHASES['tool']
        print(f"{indent}{icon} {self._color('Tool:', color)} {self._color(tool_name, 'bold')}")
        if params:
            for key, value in params.items():
                val_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                print(f"{indent}    {self._color(key + ':', 'dim')} {val_str}")

    def tool_result(self, success: bool, message: str = None):
        """Show tool result."""
        if not self.enabled:
            return
        indent = self._get_indent()
        if success:
            icon = SYM_CHECK
            color = 'green'
        else:
            icon = SYM_CROSS
            color = 'red'
        msg = message[:60] + "..." if message and len(message) > 60 else (message or "")
        print(f"{indent}    {self._color(icon, color)} {msg}")

    def context_info(self, files: int = 0, lines: int = 0, tokens: int = 0, model: str = None):
        """Show context information."""
        if not self.enabled:
            return
        indent = self._get_indent()
        print(f"{indent}  {self._color('Context:', 'cyan')}")
        if files > 0:
            print(f"{indent}    Files: {files}")
        if lines > 0:
            print(f"{indent}    Lines: {lines:,}")
        if tokens > 0:
            print(f"{indent}    Tokens: ~{tokens:,}")
        if model:
            print(f"{indent}    Model: {model}")

    def api_call(self, endpoint: str = None, tokens_in: int = 0, tokens_out: int = 0):
        """Show API call information."""
        if not self.enabled:
            return
        indent = self._get_indent()
        print(f"{indent}  {self._color('API Call:', 'blue')}")
        if endpoint:
            print(f"{indent}    Endpoint: {endpoint}")
        if tokens_in > 0:
            print(f"{indent}    Input tokens: ~{tokens_in:,}")

    def api_response(self, tokens: int = 0, time_ms: int = 0):
        """Show API response information."""
        if not self.enabled:
            return
        indent = self._get_indent()
        if tokens > 0:
            print(f"{indent}    Output tokens: ~{tokens:,}")
        if time_ms > 0:
            print(f"{indent}    Response time: {time_ms}ms")

    def code_block(self, filename: str, lines: int = 0, lang: str = None):
        """Show code block being processed."""
        if not self.enabled:
            return
        indent = self._get_indent()
        lang_str = f" ({lang})" if lang else ""
        lines_str = f" [{lines} lines]" if lines > 0 else ""
        print(f"{indent}  📄 {self._color(filename, 'cyan')}{lang_str}{lines_str}")

    def changes_summary(self, changes=None, files_changed: int = 0, lines_added: int = 0, lines_removed: int = 0):
        """Show summary of changes.

        Args:
            changes: List of dicts with 'file' and 'changes' keys, OR None
            files_changed: Number of files changed (if not using changes list)
            lines_added: Lines added (if not using changes list)
            lines_removed: Lines removed (if not using changes list)
        """
        if not self.enabled:
            return
        indent = self._get_indent()
        print(f"{indent}  {self._color('Changes:', 'yellow')}")

        # Handle list of change dicts
        if isinstance(changes, list):
            for change in changes:
                if isinstance(change, dict):
                    fname = change.get('file', 'unknown')
                    change_list = change.get('changes', [])
                    is_new = change.get('new', False)
                    prefix = "[NEW] " if is_new else ""
                    print(f"{indent}    {prefix}{self._color(fname, 'cyan')}")
                    for c in change_list:
                        print(f"{indent}      - {c}")
            return

        # Handle integer format (legacy)
        if files_changed > 0:
            print(f"{indent}    Files: {files_changed}")
        if lines_added > 0:
            print(f"{indent}    Added: {self._color(f'+{lines_added}', 'green')}")
        if lines_removed > 0:
            print(f"{indent}    Removed: {self._color(f'-{lines_removed}', 'red')}")

    def section(self, title: str):
        """Show a section header."""
        if not self.enabled:
            return
        print()
        print(f"  {self._color('─' * 40, 'dim')}")
        print(f"  {self._color(title, 'bold')}")
        print(f"  {self._color('─' * 40, 'dim')}")

    def indent(self):
        """Increase indentation."""
        self.indent_level += 1

    def dedent(self):
        """Decrease indentation."""
        self.indent_level = max(0, self.indent_level - 1)

    def warning(self, message: str):
        """Show a warning."""
        if not self.enabled:
            return
        icon, color, _ = self.PHASES['warning']
        print(f"  {icon} {self._color(message, color)}")

    def error(self, message: str):
        """Show an error."""
        if not self.enabled:
            return
        icon, color, _ = self.PHASES['error']
        print(f"  {icon} {self._color(message, color)}")

    def thinking_indicator(self, message: str = "Processing"):
        """Show a thinking indicator (for long operations)."""
        if not self.enabled:
            return
        icon, color, _ = self.PHASES['thinking']
        print(f"  {icon} {self._color(message, color)}...", end='', flush=True)

    def thinking_done(self):
        """Complete thinking indicator."""
        if not self.enabled:
            return
        print(f" {self._color('done', 'green')}")

    def websearch_result(self, query: str, results: int = 0):
        """Show websearch results."""
        if not self.enabled:
            return
        indent = self._get_indent()
        icon, color, _ = self.PHASES['websearch']
        print(f"{indent}{icon} {self._color('Web search:', color)} \"{query}\"")
        if results > 0:
            print(f"{indent}    Found: {results} results")

    def file_operation(self, operation: str, path: str, success: bool = True):
        """Show a file operation."""
        if not self.enabled:
            return
        indent = self._get_indent()
        if _UNICODE_OK:
            ops = {
                'read': ('👁', 'Reading'),
                'write': ('📝', 'Writing'),
                'edit': ('✏️', 'Editing'),
                'delete': ('🗑', 'Deleting'),
                'create': ('📁', 'Creating'),
            }
            default_icon = '📄'
        else:
            ops = {
                'read': ('>', 'Reading'),
                'write': ('>', 'Writing'),
                'edit': ('>', 'Editing'),
                'delete': ('x', 'Deleting'),
                'create': ('+', 'Creating'),
            }
            default_icon = '>'
        icon, label = ops.get(operation, (default_icon, operation))
        status = self._color(SYM_CHECK, 'green') if success else self._color(SYM_CROSS, 'red')
        # Truncate path if too long
        display_path = path if len(path) <= 40 else "..." + path[-37:]
        print(f"{indent}  {icon} {label}: {display_path} {status}")


# Global verbose output instance
_verbose_output = None


def get_verbose_output(enabled: bool = True) -> AIVerboseOutput:
    """Get or create verbose output instance."""
    global _verbose_output
    if _verbose_output is None or _verbose_output.enabled != enabled:
        _verbose_output = AIVerboseOutput(enabled=enabled)
    return _verbose_output


def get_ai_manager() -> AIManager:
    global _ai_manager_instance
    if _ai_manager_instance is None:
        _ai_manager_instance = AIManager()
    return _ai_manager_instance
