from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Any

from aiohttp import web

from ..clients.capsule import (
    GetCollectionSchemaRequest,
)
from ..constants import (
    ACCESS_AUTHENTICATED,
    ACCESS_PUBLIC,
    CollectionDecl,
    DEFAULT_PAGE_SIZE,
    HEADER_AUTHENTICATED,
    HEADER_ORG_ID,
    HEADER_SESSION_ID,
    HEADER_USER_ID,
    MAX_PAGE_SIZE,
    PAGE_TYPE_REACT,
    SCOPE_APP,
    SETTINGS_COLLECTION,
    SETTINGS_KEY_FIELD,
    _TYPE_TO_STR,
)
from ..app import _ACCESS_ATTR
from ..db import Collection
from ..decorators import (
    _ASGI_ATTR,
    _ENDPOINT_ATTR,
    _MESSAGE_ATTR,
    _SCHEDULE_ATTR,
)
from ..home import serialize_suggestions
from ..page_bundle import page_bundle_handler
from ..page_source import (
    page_module_source_handler,
    page_source_handler,
    page_source_manifest_handler,
)
from ..task_types import TaskDescriptor
from .shared import (
    _BRANDING_LOGO_ROUTE,
    _RESERVED_QUERY_KEYS,
    _asset_to_data_uri,
    _log,
    _maybe_await,
    _serialize_collection_columns,
    _wants_request_context,
    _wants_session,
)


class RunnerRouteMixin:
    def _collect_meta(self) -> dict:
        from ..task_types import _TASK_ATTR

        endpoints: list[dict] = []
        tasks: list[dict] = []
        schedules: list[dict] = []
        channels: list[dict] = []

        if self._instance is not None:
            for name in dir(self._instance):
                attr = getattr(self._instance, name, None)
                if attr is None:
                    continue
                ep = getattr(attr, _ENDPOINT_ATTR, None)
                if ep:
                    endpoints.append(
                        {
                            "method": ep["method"].upper(),
                            "path": ep["path"],
                            "name": name,
                            "authorized": ep.get("authorized", True),
                        }
                    )
                if getattr(attr, _TASK_ATTR, False):
                    info: dict = {"name": name}
                    if isinstance(attr, TaskDescriptor):
                        info["retries"] = attr._retries
                        info["timeout"] = attr._timeout
                    tasks.append(info)
                cron = getattr(attr, _SCHEDULE_ATTR, None)
                if cron and isinstance(cron, str):
                    schedules.append({"name": name, "cron": cron})

        from ..app import _REGISTERED_CLASSES, _DATA_REGISTRY

        pages: list[dict] = []
        data_sources: list[dict] = []
        theme: dict | None = None
        home: dict | None = None
        chat: dict | None = None
        onboarding: dict | None = None
        shell: dict | None = None
        actions: list[str] = sorted(self._action_handlers.keys())
        has_message_handler = bool(self._hooks.get(_MESSAGE_ATTR))
        message_handlers = [
            {"name": name, "label": label}
            for name, label in sorted(self._message_handler_labels.items())
        ]
        for reg in _REGISTERED_CLASSES:
            has_message_handler = has_message_handler or bool(reg.get("has_message_handler"))
            for mh in reg.get("message_handlers", []):
                if mh not in message_handlers:
                    message_handlers.append(mh)
            for action in reg.get("actions", []):
                if action not in actions:
                    actions.append(action)
            for ch in reg.get("channels", []):
                channels.append(ch if isinstance(ch, dict) else {"type": str(ch)})
            for p in reg.get("pages", []):
                pages.append(p)
            for ds in reg.get("data_sources", []):
                ds_fn = _DATA_REGISTRY.get(ds)
                ds_access = getattr(ds_fn, _ACCESS_ATTR, ACCESS_PUBLIC) if ds_fn else ACCESS_PUBLIC
                entry = {"name": ds, "access": ds_access}
                if entry not in data_sources:
                    data_sources.append(entry)
            if reg.get("theme"):
                theme = dict(reg["theme"])
                for key in ("logo", "preview_image", "favicon"):
                    asset = theme.get(key)
                    if asset and not asset.startswith(("http://", "https://", "data:")):
                        theme[key] = _asset_to_data_uri(asset)
            if reg.get("home"):
                home = dict(reg["home"])
            if reg.get("chat"):
                chat = dict(reg["chat"])
            if reg.get("onboarding"):
                onboarding = dict(reg["onboarding"])
            if reg.get("shell"):
                shell = dict(reg["shell"])

        collections = self._get_all_collections()
        settings = self._get_all_settings()

        _SETTING_WIDGET_TYPES = frozenset({"toggle", "text_input", "number_input", "select"})

        def _serialize_decl_columns(decl):
            return _serialize_collection_columns(decl.columns)

        def _resolve_table_widget(node: dict) -> dict:
            if "collection_ref" in node:
                ref = node["collection_ref"]
                decl = collections.get(ref)
                resolved = dict(node)
                resolved.pop("collection_ref", None)
                resolved["collection"] = ref
                if decl:
                    cols = _serialize_decl_columns(decl)
                    if cols:
                        resolved["columns"] = cols
                    if decl.sortable:
                        resolved["sortable"] = True
                    if decl.filterable:
                        resolved["filterable"] = True
                    if decl.paginate:
                        resolved["paginate"] = decl.paginate
                    resolved["scope"] = decl.scope
                return resolved
            if "collection" in node:
                coll_name = node.get("collection")
                decl = collections.get(coll_name) if coll_name else None
                if decl:
                    node = dict(node)
                    node["scope"] = decl.scope
                return node
            return node

        def _resolve_widget(node: dict) -> dict:
            if node.get("type") == "table":
                return _resolve_table_widget(node)
            if node.get("type") in _SETTING_WIDGET_TYPES and "setting" in node:
                sname = node["setting"]
                sdecl = settings.get(sname)
                if sdecl:
                    node = dict(node)
                    node["setting_scope"] = sdecl.scope
                    node["setting_type"] = _TYPE_TO_STR.get(sdecl.type, "str")
                    if sdecl.default is not None:
                        node["setting_default"] = sdecl.default
                    if sdecl.options:
                        node["options"] = list(sdecl.options)
                return node
            if node.get("type") in {"table_browser", "table_group"} and isinstance(
                node.get("items"), list
            ):
                node = dict(node)
                node["items"] = [_resolve_widget(c) for c in node["items"]]
                return node
            if "children" in node and isinstance(node["children"], list):
                node = dict(node)
                node["children"] = [_resolve_widget(c) for c in node["children"]]
            return node

        for p in pages:
            if p.get("widget_tree"):
                p["widget_tree"] = _resolve_widget(p["widget_tree"])

        workflows: list[dict] = []
        for reg in _REGISTERED_CLASSES:
            for w in reg.get("workflows", []):
                wf_dict = dict(w) if isinstance(w, dict) else w
                if wf_dict.get("widget_tree"):
                    wf_dict["widget_tree"] = _resolve_widget(wf_dict["widget_tree"])
                workflows.append(wf_dict)

        if home and home.get("widget_tree"):
            home["widget_tree"] = _resolve_widget(home["widget_tree"])
        if chat and chat.get("widget_tree"):
            chat["widget_tree"] = _resolve_widget(chat["widget_tree"])
        if onboarding and onboarding.get("widget_tree"):
            onboarding["widget_tree"] = _resolve_widget(onboarding["widget_tree"])

        meta: dict = {
            "endpoints": endpoints,
            "tasks": tasks,
            "schedules": schedules,
            "channels": channels,
            "pages": pages,
            "workflows": workflows,
            "data_sources": data_sources,
            "collections": [d.to_dict() for d in collections.values()],
            "settings": [s.to_dict() for s in settings.values()],
            "has_message_handler": has_message_handler,
            "message_handlers": message_handlers,
            "actions": sorted(actions),
        }
        if theme:
            meta["theme"] = theme
        if home:
            meta["home"] = home
        if chat:
            meta["chat"] = chat
        if onboarding:
            meta["onboarding"] = onboarding
        if shell:
            meta["shell"] = shell
        return meta

    def _mount_endpoints(self, app: web.Application) -> None:
        meta = self._collect_meta()

        def _handle_meta(_req: web.Request) -> web.Response:
            self._last_activity = time.time()
            return web.json_response(meta)

        app.router.add_get("/_meta", _handle_meta)

        from ..app import _DATA_REGISTRY

        for ds_name, ds_fn in _DATA_REGISTRY.items():
            app.router.add_get(f"/data/{ds_name}", self._wrap_data_source(ds_fn))
            _log(f"data source mounted: GET /data/{ds_name}")

        app.router.add_get("/collection/{name}", self._wrap_collection_query())
        app.router.add_delete("/collection/{name}", self._wrap_collection_delete())
        _log("collection routes mounted: GET/DELETE /collection/{name}")

        if self._get_all_settings():
            app.router.add_get("/settings", self._handle_settings_list())
            app.router.add_get("/settings/{name}", self._handle_settings_get())
            app.router.add_put("/settings/{name}", self._handle_settings_put())
            _log("settings routes mounted: GET/PUT /settings/{name}")

        for page in meta.get("pages", []):
            if page.get("type") == PAGE_TYPE_REACT and page.get("component"):
                pname = page["name"]
                component = page["component"]
                app.router.add_get(
                    f"/pages/{pname}/source",
                    page_source_handler(component),
                )
                app.router.add_get(
                    f"/pages/{pname}/bundle.js",
                    page_bundle_handler(component, page.get("packages", [])),
                )
                app.router.add_get(
                    f"/pages/{pname}/source-manifest",
                    page_source_manifest_handler(component),
                )
                app.router.add_get(
                    f"/pages/{pname}/source/{{relative_path:.*}}",
                    page_module_source_handler(component),
                )
                _log(f"page source mounted: GET /pages/{pname}/source")
        onboarding = meta.get("onboarding")
        if onboarding and onboarding.get("type") == PAGE_TYPE_REACT and onboarding.get("component"):
            app.router.add_get(
                "/pages/__onboarding__/source",
                page_source_handler(onboarding["component"]),
            )
            app.router.add_get(
                "/pages/__onboarding__/bundle.js",
                page_bundle_handler(onboarding["component"], onboarding.get("packages", [])),
            )
            app.router.add_get(
                "/pages/__onboarding__/source-manifest",
                page_source_manifest_handler(onboarding["component"]),
            )
            app.router.add_get(
                "/pages/__onboarding__/source/{relative_path:.*}",
                page_module_source_handler(onboarding["component"]),
            )
            _log("page source mounted: GET /pages/__onboarding__/source")

        from ..app import _REGISTERED_CLASSES

        for reg in _REGISTERED_CLASSES:
            theme = reg.get("theme")
            if theme and theme.get("logo"):
                logo_path = theme["logo"]
                if not logo_path.startswith(("http://", "https://")):
                    app.router.add_get(_BRANDING_LOGO_ROUTE, self._wrap_logo(logo_path))
                    _log(f"branding logo mounted: GET {_BRANDING_LOGO_ROUTE} → {logo_path}")
                    break

        from ..app import _HOME_SUGGESTIONS_REGISTRY

        if self._app_name in _HOME_SUGGESTIONS_REGISTRY:
            app.router.add_get("/_home/suggestions", self._handle_home_suggestions())
            _log("home suggestions mounted: GET /_home/suggestions")

        if self._instance is None:
            return

        for name in dir(self._instance):
            attr = getattr(self._instance, name, None)
            if attr is None:
                continue

            ep = getattr(attr, _ENDPOINT_ATTR, None)
            if ep:
                method = ep["method"].upper()
                path = ep["path"]
                auth = ep.get("authorized", True)
                app.router.add_route(method, path, self._wrap_endpoint(attr, authorized=auth))
                _log(f"endpoint mounted: {method} {path} → {name} (authorized={auth})")

            asgi = getattr(attr, _ASGI_ATTR, None)
            if asgi:
                prefix = asgi["path"].rstrip("/")
                self._mount_asgi(app, prefix, attr(), name)

    def _handle_home_suggestions(self):
        from ..app import _HOME_SUGGESTIONS_REGISTRY

        fn = _HOME_SUGGESTIONS_REGISTRY.get(self._app_name)
        home = self._registered_home() or {}
        access = home.get("dynamic_suggestions_access", ACCESS_PUBLIC)
        ttl = int(home.get("dynamic_suggestions_ttl") or 0)
        wants_ctx = _wants_request_context(fn) if fn is not None else False

        async def handler(request: web.Request) -> web.Response:
            if fn is None:
                return web.json_response({"suggestions": []}, status=404)
            if (
                access == ACCESS_AUTHENTICATED
                and request.headers.get(HEADER_AUTHENTICATED) != "true"
            ):
                return web.json_response({"error": "authentication_required"}, status=401)

            now = time.time()
            cache_key = self._home_cache_key(request)
            if ttl > 0:
                cached = self._home_suggestions_cache.get(cache_key)
                if cached and cached[0] > now:
                    return web.json_response({"suggestions": cached[1], "cached": True})

            identity_token = self._set_session_on_refs(self._build_request_identity(request))
            try:

                async def call_handler():
                    if wants_ctx:
                        ctx = await self._build_home_context(request)
                        return await _maybe_await(fn(ctx))
                    return await _maybe_await(fn())

                result = await asyncio.wait_for(call_handler(), timeout=10)
                suggestions = serialize_suggestions(result)
                if ttl > 0:
                    self._home_suggestions_cache[cache_key] = (now + ttl, suggestions)
                return web.json_response({"suggestions": suggestions})
            except asyncio.TimeoutError:
                return web.json_response({"error": "home suggestions timed out"}, status=504)
            except Exception as exc:
                _log(f"home suggestions error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)
            finally:
                self._clear_session_on_refs(identity_token)

        return handler

    def _wrap_endpoint(self, fn, *, authorized: bool = True):
        needs_ctx = _wants_request_context(fn)

        async def handler(request: web.Request) -> web.Response:
            if authorized and request.headers.get(HEADER_AUTHENTICATED) != "true":
                return web.json_response({"error": "unauthorized"}, status=401)
            identity_token = self._set_session_on_refs(self._build_request_identity(request))
            try:
                if needs_ctx:
                    ctx = await self._build_request_context(request)
                    result = await _maybe_await(fn(ctx))
                else:
                    result = await _maybe_await(fn(request))
                if isinstance(result, web.Response):
                    return result
                if isinstance(result, dict):
                    return web.json_response(result)
                return web.Response(text=str(result))
            except Exception as exc:
                _log(f"endpoint error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)
            finally:
                self._clear_session_on_refs(identity_token)

        return handler

    def _wrap_data_source(self, fn):
        access = getattr(fn, _ACCESS_ATTR, ACCESS_PUBLIC)
        needs_ctx = _wants_request_context(fn)
        needs_session = _wants_session(fn)

        async def handler(request: web.Request) -> web.Response:
            if (
                access == ACCESS_AUTHENTICATED
                and request.headers.get(HEADER_AUTHENTICATED) != "true"
            ):
                return web.json_response({"error": "authentication_required"}, status=401)
            session = await self._build_request_session(request) if needs_session else None
            identity_token = self._set_session_on_refs(
                session if session is not None else self._build_request_identity(request)
            )
            try:
                kwargs = {k: v for k, v in request.query.items() if k not in _RESERVED_QUERY_KEYS}
                if needs_session:
                    kwargs.setdefault("session", session)
                if needs_ctx:
                    ctx = await self._build_request_context(request)
                    result = await _maybe_await(fn(ctx, **kwargs))
                else:
                    result = (
                        await _maybe_await(fn(**kwargs)) if kwargs else await _maybe_await(fn())
                    )
                return web.json_response(result)
            except Exception as exc:
                _log(f"data source error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)
            finally:
                self._clear_session_on_refs(identity_token)

        return handler

    def _wrap_collection_query(self):
        async def handler(request: web.Request) -> web.Response:
            name = request.match_info["name"]
            try:
                db = getattr(self._instance, "db", None)
                if db is None:
                    return web.json_response({"error": "database not available"}, status=503)

                col = getattr(db, name)
                page = int(request.query.get("page", "1"))
                per_page = min(
                    int(request.query.get("per_page", str(DEFAULT_PAGE_SIZE))), MAX_PAGE_SIZE
                )
                sort_field = request.query.get("sort")
                sort_dir = request.query.get("sort_dir", "asc")
                filter_raw = request.query.get("filter")

                query_filter: dict = {}
                if filter_raw:
                    try:
                        parsed = json.loads(filter_raw)
                        if isinstance(parsed, dict):
                            query_filter = parsed
                    except (json.JSONDecodeError, ValueError):
                        pass

                collections = self._get_all_collections()
                decl = collections.get(name)
                scope = request.query.get("scope") or (decl.scope if decl else SCOPE_APP)
                user_id = request.headers.get(HEADER_USER_ID, "")
                owner_id = request.headers.get(HEADER_ORG_ID, "")
                session_id = request.headers.get(HEADER_SESSION_ID, "")
                if scope != SCOPE_APP:
                    scope_decl = decl or CollectionDecl(name=name, scope=scope)
                    sf = scope_decl.scope_filter(
                        user_id=user_id,
                        owner_id=owner_id,
                        session_id=session_id,
                    )
                    query_filter.update(sf)

                dynamic_columns = None
                if self._data_stub:
                    try:
                        schema_resp = await self._run_rpc(
                            self._data_stub.get_collection_schema,
                            GetCollectionSchemaRequest(
                                app_id=self._data_app_id,
                                name=name,
                                scope=scope,
                                user_id=user_id,
                                owner_id=owner_id,
                                session_id=session_id,
                            ),
                        )
                        if schema_resp.found and schema_resp.schema:
                            dynamic_columns = _serialize_collection_columns(
                                schema_resp.schema.columns
                            )
                    except Exception as exc:
                        _log(f"collection schema lookup failed for {name}: {exc}")

                sort_spec = None
                if sort_field:
                    sort_spec = {sort_field: 1 if sort_dir == "asc" else -1}

                skip = (page - 1) * per_page
                data = await col.find(
                    filter=query_filter,
                    sort=sort_spec,
                    skip=skip,
                    limit=per_page,
                )
                total = await col.count(filter=query_filter)

                response = {
                    "data": data,
                    "total": total,
                    "page": page,
                    "per_page": per_page,
                }
                columns = dynamic_columns
                if columns is None and decl:
                    columns = _serialize_collection_columns(decl.columns)
                if columns:
                    response["columns"] = columns
                return web.json_response(response)
            except Exception as exc:
                _log(f"collection query error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)

        return handler

    def _wrap_collection_delete(self):
        async def handler(request: web.Request) -> web.Response:
            name = request.match_info["name"]
            try:
                db = getattr(self._instance, "db", None)
                if db is None:
                    return web.json_response({"error": "database not available"}, status=503)

                body = await request.json()
                if not isinstance(body, dict):
                    return web.json_response({"error": "invalid request body"}, status=400)

                ids = body.get("ids")
                raw_filter = body.get("filter")
                if ids:
                    if not isinstance(ids, list):
                        return web.json_response({"error": "ids must be a list"}, status=400)
                    query_filter: dict = {"_id": {"$in": ids}}
                elif isinstance(raw_filter, dict) and raw_filter:
                    query_filter = dict(raw_filter)
                else:
                    return web.json_response(
                        {"error": "ids or non-empty filter required"}, status=400
                    )

                collections = self._get_all_collections()
                decl = collections.get(name)
                scope = request.query.get("scope") or (decl.scope if decl else SCOPE_APP)
                if scope != SCOPE_APP:
                    scope_decl = decl or CollectionDecl(name=name, scope=scope)
                    query_filter.update(
                        scope_decl.scope_filter(
                            user_id=request.headers.get(HEADER_USER_ID, ""),
                            owner_id=request.headers.get(HEADER_ORG_ID, ""),
                            session_id=request.headers.get(HEADER_SESSION_ID, ""),
                        )
                    )

                col = getattr(db, name)
                result = await col.delete_many(query_filter)
                return web.json_response(result)
            except Exception as exc:
                _log(f"collection delete error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)

        return handler

    def _handle_settings_list(self):
        settings = self._get_all_settings()

        async def handler(request: web.Request) -> web.Response:
            self._last_activity = time.time()
            db = getattr(self._instance, "db", None)
            if db is None:
                return web.json_response({"error": "database not available"}, status=503)

            user_id = request.headers.get(HEADER_USER_ID, "")
            owner_id = request.headers.get(HEADER_ORG_ID, "")
            col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)

            result: dict[str, Any] = {}
            for name, decl in settings.items():
                sf = decl.scope_filter(user_id=user_id, owner_id=owner_id)
                filt = {SETTINGS_KEY_FIELD: name, **sf}
                doc = await col.find_one(filt)
                result[name] = doc.get("value", decl.default) if doc else decl.default

            return web.json_response(result)

        return handler

    def _handle_settings_get(self):
        settings = self._get_all_settings()

        async def handler(request: web.Request) -> web.Response:
            self._last_activity = time.time()
            name = request.match_info["name"]
            decl = settings.get(name)
            if decl is None:
                return web.json_response({"error": f"unknown setting: {name}"}, status=404)

            user_id = request.headers.get(HEADER_USER_ID, "")
            owner_id = request.headers.get(HEADER_ORG_ID, "")
            col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)

            sf = decl.scope_filter(user_id=user_id, owner_id=owner_id)
            filt = {SETTINGS_KEY_FIELD: name, **sf}
            doc = await col.find_one(filt)
            value = doc.get("value", decl.default) if doc else decl.default

            return web.json_response({"name": name, "value": value})

        return handler

    def _handle_settings_put(self):
        settings = self._get_all_settings()

        async def handler(request: web.Request) -> web.Response:
            self._last_activity = time.time()
            name = request.match_info["name"]
            decl = settings.get(name)
            if decl is None:
                return web.json_response({"error": f"unknown setting: {name}"}, status=404)

            try:
                body = await request.json()
            except Exception:
                return web.json_response({"error": "invalid JSON body"}, status=400)

            if "value" not in body:
                return web.json_response({"error": "missing 'value' field"}, status=400)

            value = body["value"]
            user_id = request.headers.get(HEADER_USER_ID, "")
            owner_id = request.headers.get(HEADER_ORG_ID, "")
            col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)

            sf = decl.scope_filter(user_id=user_id, owner_id=owner_id)
            filt = {SETTINGS_KEY_FIELD: name, **sf}
            existing = await col.find_one(filt)
            if existing:
                await col.update_one(filt, {"$set": {"value": value}})
            else:
                await col.insert_one({**filt, "value": value})

            return web.json_response({"ok": True, "name": name, "value": value})

        return handler

    def _wrap_logo(self, logo_path: str):
        import mimetypes

        async def handler(request: web.Request) -> web.Response:

            full_path = os.path.join(os.getcwd(), logo_path)
            if not os.path.isfile(full_path):
                return web.json_response({"error": "not found"}, status=404)
            ct = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
            return web.FileResponse(
                full_path,
                headers={
                    "Content-Type": ct,
                    "Cache-Control": "public, max-age=3600",
                },
            )

        return handler

    def _mount_asgi(self, app: web.Application, prefix: str, asgi_app, name: str) -> None:
        try:
            from aiohttp_asgi import ASGIApplicationServer

            subapp = ASGIApplicationServer(asgi_app).make_aiohttp_app()
            app.add_subapp(prefix, subapp)
            _log(f"asgi mounted: {prefix}/* → {name}")
        except ImportError:

            async def handler(request: web.Request) -> web.Response:
                try:
                    scope = {
                        "type": "http",
                        "asgi": {"version": "3.0"},
                        "http_version": "1.1",
                        "method": request.method,
                        "path": request.path[len(prefix) :] or "/",
                        "query_string": request.query_string.encode(),
                        "headers": [
                            (k.lower().encode(), v.encode()) for k, v in request.headers.items()
                        ],
                    }
                    body = await request.read()
                    status_code = 200
                    resp_headers: list[tuple[str, str]] = []
                    resp_body = bytearray()

                    async def receive():
                        return {"type": "http.request", "body": body}

                    async def send(message):
                        nonlocal status_code, resp_headers
                        if message["type"] == "http.response.start":
                            status_code = message["status"]
                            resp_headers = [
                                (k.decode(), v.decode()) for k, v in message.get("headers", [])
                            ]
                        elif message["type"] == "http.response.body":
                            resp_body.extend(message.get("body", b""))

                    await asgi_app(scope, receive, send)
                    resp = web.Response(body=bytes(resp_body), status=status_code)
                    for k, v in resp_headers:
                        resp.headers[k] = v
                    return resp
                except Exception as exc:
                    _log(f"asgi error: {exc}")
                    return web.json_response({"error": str(exc)}, status=500)

            app.router.add_route("*", prefix + "/{path:.*}", handler)
            app.router.add_route("*", prefix, handler)
            _log(f"asgi mounted (fallback): {prefix}/* → {name}")
