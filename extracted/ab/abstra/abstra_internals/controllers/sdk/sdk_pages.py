from __future__ import annotations

import datetime
import inspect
import json
import math
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Dict, List, Optional
from urllib.parse import urlencode

import jwt as pyjwt

from abstra_internals.controllers.sdk._multipart import parse_multipart
from abstra_internals.environment import CLOUD_API_PROD_SHARED_TOKEN, IS_DEVELOPMENT
from abstra_internals.interface.sdk import user_exceptions
from abstra_internals.repositories.users import UsersRepository
from abstra_internals.services.jwt import UserClaims
from abstra_internals.settings import Settings
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

    def register_static(self, file_path: str | os.PathLike) -> str:
        root = Settings.root_path.resolve()
        source = Path(file_path)
        if not source.is_absolute():
            source = root / source
        source = source.resolve()

        try:
            rel_path = source.relative_to(root)
        except ValueError:
            raise ValueError(
                f"Static file must be inside the project root ({root}): {file_path}"
            )

        if not source.is_file():
            raise FileNotFoundError(f"Static file not found: {file_path}")

        relative = rel_path.as_posix()
        token = pyjwt.encode(
            {
                "asset": relative,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(hours=24),
            },
            key=CLOUD_API_PROD_SHARED_TOKEN,
            algorithm="HS256",
        )

        page_path = self.client.context.page_path
        query = urlencode({"token": token})
        if page_path:
            return f"/_page/{page_path}/{relative}?{query}"
        return f"/_page-home/{relative}?{query}"

    def handle_request(self) -> None:
        request = self.client.get_request()

        if request.method == "POST":
            self._handle_function_call(request.body, request.headers)
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

    def _handle_function_call(self, body: str, headers: Dict[str, str]) -> None:
        content_type = CaseInsensitiveDict(headers).get("Content-Type") or ""

        if "multipart/form-data" in content_type.lower():
            try:
                function_name, params = self._parse_multipart_call(body, headers)
            except (ValueError, KeyError):
                # ValueError covers binascii.Error (bad base64) and multipart
                # parse failures; KeyError covers a missing boundary option.
                self.client.set_response(
                    400,
                    json.dumps({"error": "Invalid multipart body"}),
                    {"Content-Type": "application/json"},
                )
                return
        else:
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

        func = (
            self._registered_functions.get(function_name)
            if isinstance(function_name, str)
            else None
        )
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

    def _parse_multipart_call(
        self, body: str, headers: Dict[str, str]
    ) -> tuple[Optional[str], Dict]:
        """Decode a multipart/form-data call into (function_name, params).

        File fields arrive as ``{"filename", "content_type", "content": bytes}``;
        non-file fields are JSON-decoded so structure (lists, dicts, numbers,
        booleans) survives the round-trip. Multiple parts sharing a name are
        collapsed into a list.
        """
        parts = parse_multipart(body, CaseInsensitiveDict(headers))

        function_name: Optional[str] = None
        params: Dict = {}
        for part in parts:
            name = part.get("name")
            if not isinstance(name, str):
                continue
            if "filename" in part:
                raw_filename = str(part["filename"])
                value = {
                    "filename": os.path.basename(raw_filename.replace("\\", "/")),
                    "content_type": part["content_type"],
                    "content": part["content"],
                }
            else:
                raw_value = part.get("value")
                try:
                    value = json.loads(raw_value) if raw_value is not None else None
                except (json.JSONDecodeError, TypeError):
                    value = raw_value

            if name == "__function__":
                if isinstance(value, str):
                    function_name = value
                continue

            if name in params:
                existing = params[name]
                if isinstance(existing, list):
                    existing.append(value)
                else:
                    params[name] = [existing, value]
            else:
                params[name] = value

        return function_name, params

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
            "  const __headers = {};",
            "  const __token = document.querySelector('meta[name=\"abstra-auth-token\"]')?.getAttribute('content');",
            "  if (__token) __headers['Authorization'] = 'Bearer ' + __token;",
            "  const __pageExecId = document.querySelector('meta[name=\"abstra-execution-id\"]')?.getAttribute('content');",
            "  if (__pageExecId) __headers['X-Page-Execution-Id'] = __pageExecId;",
            f"  const __params = {{ {js_params_obj} }};",
            "  const __isBlob = (v) => v instanceof Blob;",
            "  const __isBlobList = (v) => (Array.isArray(v) || (typeof FileList !== 'undefined' && v instanceof FileList)) && Array.from(v).every(__isBlob);",
            "  const __hasFile = Object.values(__params).some(v => __isBlob(v) || __isBlobList(v));",
            "  let __body;",
            "  if (__hasFile) {",
            "    const __fd = new FormData();",
            f'    __fd.append("__function__", "{name}");',
            "    for (const [__k, __v] of Object.entries(__params)) {",
            "      if (__isBlob(__v)) {",
            "        __fd.append(__k, __v, __v.name || __k);",
            "      } else if (__isBlobList(__v)) {",
            "        for (const __f of __v) __fd.append(__k, __f, __f.name || __k);",
            "      } else if (__v !== undefined) {",
            "        __fd.append(__k, JSON.stringify(__v));",
            "      }",
            "    }",
            "    __body = __fd;",
            "    // Intentionally omit Content-Type — browser sets it with boundary",
            "  } else {",
            "    __headers['Content-Type'] = 'application/json';",
            f'    __body = JSON.stringify({{ function: "{name}", params: __params }});',
            "  }",
            "  const response = await fetch(__endpoint, {",
            '    method: "POST",',
            "    headers: __headers,",
            "    body: __body",
            "  });",
            "  if (!response.ok) {",
            "    const text = await response.text();",
            "    try { const d = JSON.parse(text); throw new Error(d.error || text); }",
            "    catch (e) { if (e instanceof SyntaxError) throw new Error(text); throw e; }",
            "  }",
        ]

    def _build_js_regular(
        self,
        name: str,
        params: List[Dict[str, str]],
        cache_ttl_seconds: Optional[float] = None,
    ) -> List[str]:
        param_names = ", ".join(p["name"] for p in params)

        if cache_ttl_seconds is None:
            lines = [f"async function {name}({param_names}) {{"]
            lines.extend(self._build_js_fetch(name, params))
            lines.append("  const data = await response.json();")
            lines.append("  return data.result;")
            lines.append("}")
            return lines

        # Cached path. The strategy:
        #   1. Wrap the fetch in __doFetch so we can call it from multiple branches.
        #   2. Bypass cache when any arg is a Blob/FileList — keying file content
        #      is impractical and stale uploads are surprising.
        #   3. Bypass cache (gracefully) if the args aren't JSON-serializable,
        #      e.g. circular refs or BigInt.
        #   4. Store the *promise* (not the resolved value) so concurrent in-flight
        #      callers share a single round trip. Evict on rejection so we never
        #      cache errors.
        ttl_ms = int(cache_ttl_seconds * 1000)
        lines = [f"async function {name}({param_names}) {{"]
        lines.append("  const __doFetch = async () => {")
        lines.extend("  " + line for line in self._build_js_fetch(name, params))
        lines.append("    const data = await response.json();")
        lines.append("    return data.result;")
        lines.append("  };")
        lines.append(f"  const __args = [{param_names}];")
        lines.append("  const __cIsBlob = (v) => v instanceof Blob;")
        lines.append(
            "  const __cIsBlobList = (v) => (Array.isArray(v) || "
            "(typeof FileList !== 'undefined' && v instanceof FileList)) "
            "&& Array.from(v).every(__cIsBlob);"
        )
        lines.append(
            "  if (__args.some(v => __cIsBlob(v) || __cIsBlobList(v))) return __doFetch();"
        )
        lines.append("  let __key;")
        lines.append(
            "  try { __key = JSON.stringify(__args); } "
            "catch (e) { return __doFetch(); }"
        )
        lines.append(f"  const __cache = ({name}._cache ||= new Map());")
        lines.append("  const __hit = __cache.get(__key);")
        lines.append(
            "  if (__hit && __hit.expiresAt > Date.now()) return __hit.promise;"
        )
        lines.append("  const __promise = __doFetch();")
        lines.append(
            f"  __cache.set(__key, {{ promise: __promise, "
            f"expiresAt: Date.now() + {ttl_ms} }});"
        )
        lines.append("  __promise.catch(() => __cache.delete(__key));")
        lines.append("  return __promise;")
        lines.append("}")
        lines.append(f"{name}.clearCache = () => {{ {name}._cache?.clear(); }};")
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
                # The public decorator rejects cache= on generators. Defensive:
                # ignore any stray attribute rather than emit unreachable JS.
                lines.extend(self._build_js_generator(name, params))
            else:
                cache_ttl = getattr(func, "_abstra_cache_ttl", None)
                if cache_ttl is not None and not (
                    isinstance(cache_ttl, (int, float))
                    and not isinstance(cache_ttl, bool)
                    and math.isfinite(cache_ttl)
                    and cache_ttl > 0
                ):
                    cache_ttl = None
                lines.extend(self._build_js_regular(name, params, cache_ttl))
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
