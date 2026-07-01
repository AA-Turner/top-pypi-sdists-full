import json
import logging
import re

_log = logging.getLogger(__name__)

# A valid JS identifier — only such store keys can become `const` declarations.
_JS_IDENT = re.compile(r"^[a-zA-Z_$][a-zA-Z0-9_$]*$")


def executeJS(driver, user_js_code: str) -> dict:
    """Execute JavaScript via Selenium with IIFE error wrapping.

    Injects variables from testmu_selenium._vars._variable_store as JS const
    declarations (valid identifiers only) so a JS step can reference prior
    variables (e.g. an API-call result) — matching the Playwright runtime.
    Wraps user code in a try/catch IIFE that captures errors with adjusted
    stack traces. Returns a dict with value, error, and line keys.

    Args:
        driver: Selenium WebDriver instance.
        user_js_code: Raw JavaScript code to execute.

    Returns:
        {"value": Any, "error": str, "line": int | None}
    """
    preview = user_js_code.strip().splitlines()[0][:80] if user_js_code.strip() else ""
    _log.info("    [execute_js] %s", preview)
    try:
        from testmu_selenium._vars import _variable_store

        user_js_code += "\n"

        # Inject store variables as const declarations before the user code.
        preamble = ""
        for name, value in _variable_store.items():
            if not _JS_IDENT.match(name):
                continue
            preamble += f"const {name} = {json.dumps(value, default=str)};\n"

        lines_before_user_code = 2 + preamble.count("\n")

        wrapped_js_code = (
            f"(function() {{ try {{ {preamble}return (function() {{ {user_js_code} }})(); }}"
            f" catch(e) {{ e.stack = e.stack.replace(/<anonymous>:(\\d+):/g,"
            f" function(match, lineNumber) {{ lineNumber = parseInt(lineNumber)"
            f" - {lines_before_user_code}; return '<anonymous>:' + lineNumber"
            f" + ':'; }}); return {{error: e.stack}}; }} }})();"
        )

        client_response_js = driver.execute_script("return " + wrapped_js_code)

        if isinstance(client_response_js, dict) and 'error' in client_response_js:
            error_stack = client_response_js['error']
            lines = error_stack.split('\n')
            error_message = lines[0].strip()
            error_line = None

            if len(lines) > 1:
                match = re.search(r'<anonymous>:(\d+):', lines[1])
                if match:
                    error_line = int(match.group(1))

            return {
                'value': '',
                'error': error_message,
                'line': error_line
            }
        else:
            try:
                json.dumps(client_response_js)
                if client_response_js is None or client_response_js == '':
                    client_response_js = "null"
                value = client_response_js
            except (TypeError, OverflowError):
                value = str(client_response_js)
            _log.info("    [execute_js] result=%s", str(value)[:200])
            return {
                'value': value,
                'error': '',
                'line': None
            }
    except Exception as e:
        return {
            'value': '',
            'error': str(e),
            'line': None
        }
