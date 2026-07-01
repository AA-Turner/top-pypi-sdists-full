"""execute_js helper — runs JavaScript in the browser via page.evaluate().

Variable injection: reads from testmu._vars._variable_store and injects
valid JS identifiers as const declarations before the user's code runs.

Raises RuntimeError on JS error or evaluation failure.
Returns the value directly (no wrapper dict).
"""
import json
import logging
import re

_log = logging.getLogger("testmu")

_JS_IDENT = re.compile(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$')


async def execute_js(page, script: str):
    """Execute JavaScript in browser context with IIFE error wrapping.

    Injects variables from testmu._vars._variable_store as JS const
    declarations (valid identifiers only). Wraps user code in a try/catch
    IIFE that captures errors with adjusted stack traces.

    Args:
        page: Playwright page instance.
        script: Raw JavaScript code to execute.

    Returns:
        The JS return value directly (JSON-serializable or str-coerced).

    Raises:
        RuntimeError: On JS error or page.evaluate() failure.
    """
    from testmu._vars import _variable_store

    preview = script[:100] + ("..." if len(script) > 100 else "")
    _log.info("    [execute_js] %s", preview)

    try:
        user_js_code = script + "\n"

        # Inject variables as const declarations inside the IIFE
        preamble = ""
        for name, value in _variable_store.items():
            if not _JS_IDENT.match(name):
                continue
            preamble += f"const {name} = {json.dumps(value, default=str)};\n"

        lines_before_user_code = 2 + preamble.count("\n")

        wrapped_js_code = f"""
        (function() {{
            try {{
                {preamble}return (function() {{ {user_js_code} }})();
            }} catch(e) {{
                e.stack = e.stack.replace(/<anonymous>:(\\d+):/g, function(match, lineNumber) {{
                    lineNumber = parseInt(lineNumber) - {lines_before_user_code};
                    return '<anonymous>:' + lineNumber + ':';
                }});
                return {{error: e.stack}};
            }}
        }})();
        """

        result = await page.evaluate(f"() => {wrapped_js_code}")

        if isinstance(result, dict) and "error" in result:
            error_stack = result["error"]
            lines = error_stack.split("\n")
            error_message = lines[0].strip()
            error_line = None

            if len(lines) > 1:
                match = re.search(r"<anonymous>:(\d+):", lines[1])
                if match:
                    error_line = int(match.group(1))

            _log.debug(f"execute_js error at line {error_line}: {error_message}")
            raise RuntimeError(f"JavaScript error at line {error_line}: {error_message}")

        # Normalize non-serializable values to string
        try:
            json.dumps(result)
        except (TypeError, OverflowError):
            result = str(result)

        if result is None or result == "":
            result = "null"

        _log.info("    [execute_js] result=%s", str(result)[:100])
        return result

    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"execute_js failed: {e}") from e
