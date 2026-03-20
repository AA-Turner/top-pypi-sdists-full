import inspect
import json
import re
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from abstra_internals.environment import IS_DEVELOPMENT
from abstra_internals.interface.sdk import user_exceptions
from abstra_internals.repositories.users import UsersRepository
from abstra_internals.services.jwt import UserClaims
from abstra_internals.utils import serialize
from abstra_internals.utils.insensitive_dict import CaseInsensitiveDict

if TYPE_CHECKING:
    from abstra_internals.controllers.execution.execution_client_page import PageClient

RENDER_FUNCTION_NAME = "__render__"
_VALID_JS_IDENTIFIER = re.compile(r"^[a-zA-Z_$][a-zA-Z0-9_$]*$")


class PageSDKController:
    def __init__(
        self,
        client: "PageClient",
        users_repository: UsersRepository,
        user_jwt: Optional[str] = None,
    ) -> None:
        self.client = client
        self.users_repository = users_repository
        self.user_jwt = user_jwt
        self._registered_functions: Dict[str, Callable] = {}

    def register_function(self, func: Callable) -> Callable:
        self._registered_functions[func.__name__] = func
        return func

    def handle_request(self) -> None:
        request = self.client.get_request()

        if request.method == "POST":
            self._handle_function_call(request.body)
        else:
            self._handle_render()

    def _handle_render(self) -> None:
        render_fn = self._registered_functions.get(RENDER_FUNCTION_NAME)
        if not render_fn:
            self.client.set_response(
                500,
                "Page must define a __render__ function.",
                {"Content-Type": "text/plain"},
            )
            return

        try:
            html = render_fn()
        except user_exceptions.AuthorizationRequired:
            raise
        except Exception as e:
            detail = str(e) if IS_DEVELOPMENT else ""
            self.client.set_response(
                500,
                f"Error in __render__: {detail}"
                if IS_DEVELOPMENT
                else "An exception occurred during execution.",
                {"Content-Type": "text/plain"},
            )
            return

        if not isinstance(html, str):
            self.client.set_response(
                500,
                "__render__ must return a string (HTML).",
                {"Content-Type": "text/plain"},
            )
            return

        js_functions = self._build_js_functions()

        full_html = f"""<!-- abstra pages -->
<script>
{js_functions}
</script>

{html}"""

        self.client.set_response(200, full_html, {"Content-Type": "text/html"})

    def _handle_function_call(self, body: str) -> None:
        try:
            data = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            self.client.set_response(
                400,
                json.dumps({"error": "Invalid JSON body"}),
                {"Content-Type": "application/json"},
            )
            return

        function_name = data.get("function")
        params = data.get("params", {})

        if function_name == RENDER_FUNCTION_NAME:
            self.client.set_response(
                403,
                json.dumps({"error": "__render__ cannot be called from the frontend"}),
                {"Content-Type": "application/json"},
            )
            return

        func = self._registered_functions.get(function_name)
        if not func:
            self.client.set_response(
                404,
                json.dumps({"error": f"Function '{function_name}' not found"}),
                {"Content-Type": "application/json"},
            )
            return

        # Only pass declared parameters to prevent unexpected kwargs
        sig = inspect.signature(func)
        allowed_params = set(sig.parameters.keys())
        filtered_params = {k: v for k, v in params.items() if k in allowed_params}

        if inspect.isgeneratorfunction(func):
            self._handle_generator_call(func, filtered_params)
        else:
            self._handle_regular_call(func, filtered_params)

    def _handle_regular_call(self, func: Callable, params: dict) -> None:
        try:
            result = func(**params)
            self.client.set_response(
                200,
                serialize({"result": result}),
                {"Content-Type": "application/json"},
            )
        except user_exceptions.AuthorizationRequired as e:
            self.client.set_response(
                e.status_code,
                json.dumps({"error": e.message}),
                {"Content-Type": "application/json"},
            )
        except Exception as e:
            self.client.set_response(
                500,
                json.dumps({"error": str(e)}),
                {"Content-Type": "application/json"},
            )

    def _handle_generator_call(self, func: Callable, params: dict) -> None:
        try:
            gen = func(**params)
            self.client.send_stream_start(200, {"Content-Type": "application/x-ndjson"})
            for chunk in gen:
                self.client.send_stream_chunk(chunk)
            self.client.send_stream_end()
        except user_exceptions.AuthorizationRequired as e:
            self.client.send_stream_error(e.message)
        except Exception as e:
            self.client.send_stream_error(str(e))

    def _get_function_params(self, func: Callable) -> List[Dict[str, str]]:
        sig = inspect.signature(func)
        params = []
        for name, param in sig.parameters.items():
            annotation = param.annotation
            type_name = "any"
            if annotation != inspect.Parameter.empty:
                type_name = (
                    annotation.__name__
                    if hasattr(annotation, "__name__")
                    else str(annotation)
                )
            params.append({"name": name, "type": type_name})
        return params

    def _build_js_fetch(self, name: str, params: List[Dict[str, str]]) -> List[str]:
        js_params_obj = ", ".join(f"{p['name']}: {p['name']}" for p in params)
        return [
            "  const __endpoint = document.querySelector('base')?.getAttribute('href') || window.location.pathname;",
            "  const response = await fetch(__endpoint, {",
            '    method: "POST",',
            '    headers: { "Content-Type": "application/json" },',
            f'    body: JSON.stringify({{ function: "{name}", params: {{ {js_params_obj} }} }})',
            "  });",
            "  if (!response.ok) {",
            "    const text = await response.text();",
            "    try { const d = JSON.parse(text); throw new Error(d.error || text); }",
            "    catch (e) { if (e instanceof SyntaxError) throw new Error(text); throw e; }",
            "  }",
        ]

    def _build_js_regular(self, name: str, params: List[Dict[str, str]]) -> List[str]:
        param_names = ", ".join(p["name"] for p in params)
        lines = [f"async function {name}({param_names}) {{"]
        lines.extend(self._build_js_fetch(name, params))
        lines.append("  const data = await response.json();")
        lines.append("  return data.result;")
        lines.append("}")
        return lines

    def _build_js_generator(self, name: str, params: List[Dict[str, str]]) -> List[str]:
        param_names = ", ".join(p["name"] for p in params)
        # Wrapper: foo() returns an async iterable that also supports await.
        #   for await (const chunk of foo()) { ... }  — streaming
        #   const all = await foo()                    — collects into array
        #   for (const chunk of foo()) { ... }         — helpful error
        lines = [f"function {name}({param_names}) {{"]
        lines.append(f"  async function* __stream({param_names}) {{")
        lines.extend("  " + line for line in self._build_js_fetch(name, params))
        lines.append("    const reader = response.body.getReader();")
        lines.append("    const decoder = new TextDecoder();")
        lines.append('    let buffer = "";')
        lines.append("    while (true) {")
        lines.append("      const { done, value } = await reader.read();")
        lines.append("      if (done) break;")
        lines.append("      buffer += decoder.decode(value, { stream: true });")
        lines.append('      const lines = buffer.split("\\n");')
        lines.append("      buffer = lines.pop();")
        lines.append("      for (const line of lines) {")
        lines.append("        if (!line.trim()) continue;")
        lines.append("        const parsed = JSON.parse(line);")
        lines.append("        if (parsed.error) throw new Error(parsed.error);")
        lines.append("        yield parsed.data;")
        lines.append("      }")
        lines.append("    }")
        lines.append("    if (buffer.trim()) {")
        lines.append("      const parsed = JSON.parse(buffer);")
        lines.append("      if (parsed.error) throw new Error(parsed.error);")
        lines.append("      yield parsed.data;")
        lines.append("    }")
        lines.append("  }")
        lines.append(f"  const iter = __stream({param_names});")
        # await foo() — collects all chunks into array
        lines.append(
            "  iter.then = (resolve, reject) => {"
            " const a = [];"
            " (async () => { for await (const c of iter) a.push(c); })()"
            ".then(() => resolve(a), reject); };"
        )
        # foo().forEach(callback) — streams chunks via callback (works in non-async context)
        lines.append(
            "  iter.forEach = (fn) => {"
            " return (async () => { for await (const c of iter) fn(c); })(); };"
        )
        # for...of gives a helpful error
        lines.append(
            "  iter[Symbol.iterator] = () => {"
            " throw new TypeError("
            "'Use for await...of instead of for...of to iterate over " + name + "()');"
            " };"
        )
        lines.append("  return iter;")
        lines.append("}")
        return lines

    def _build_js_functions(self) -> str:
        lines = []
        for name, func in self._registered_functions.items():
            if name == RENDER_FUNCTION_NAME:
                continue

            if not _VALID_JS_IDENTIFIER.match(name):
                continue

            params = self._get_function_params(func)

            if inspect.isgeneratorfunction(func):
                lines.extend(self._build_js_generator(name, params))
            else:
                lines.extend(self._build_js_regular(name, params))
            lines.append("")
        return "\n".join(lines)

    def get_user(self) -> UserClaims:
        request = self.client.get_request()
        headers = CaseInsensitiveDict(request.headers)
        auth_header = headers.get("Authorization") or headers.get("Api-Authorization")

        if auth_header:
            jwt_token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        elif self.user_jwt:
            jwt_token = self.user_jwt
        else:
            raise user_exceptions.GetUserFailed()
        claims = UserClaims.from_jwt(jwt_token, skip_verify=IS_DEVELOPMENT)

        if not claims:
            raise user_exceptions.GetUserFailed()

        if user := self.users_repository.get_user(claims.email):
            claims.add_roles(user.roles)

        return claims

    def get_query_params(self) -> Dict[str, str]:
        return self.client.get_request().query_params
