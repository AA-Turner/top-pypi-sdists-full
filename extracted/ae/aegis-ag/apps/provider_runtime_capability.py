from __future__ import annotations

import sys

from . import provider_runtime_support as _provider_runtime_support
from .provider_runtime_support import *  # noqa: F401,F403
from packages.tools import build_tool_fallback_prompt


def _request_json(*, url: str, headers: Mapping[str, str], timeout_seconds: float = 10.0) -> dict[str, Any]:
    runtime_module = sys.modules.get("apps.provider_runtime")
    patched = getattr(runtime_module, "_request_json", None) if runtime_module is not None else None
    if callable(patched) and patched is not _request_json:
        return patched(url=url, headers=headers, timeout_seconds=timeout_seconds)
    return _provider_runtime_support._request_json(
        url=url,
        headers=headers,
        timeout_seconds=timeout_seconds,
    )


class SurfaceModelProviderCapability(ModelProviderCapability):
    def __init__(
        self,
        *,
        repository: RuntimeStorageRepository,
        fallback: ModelProviderCapability,
        secret_key_path: Path,
        credential_resolver: ProfileCredentialResolver | None = None,
        tool_runtime: ToolRuntime | None = None,
        strong_provider_profile_id: str | None = None,
        weak_provider_profile_id: str | None = None,
        active_provider_id: str | None = None,
        capability_id: str = "surface.model.runtime",
        surface_label: str = "surface",
        intent_mode: str = "skip",
        bootstrap_state_dir: Path | None = None,
    ) -> None:
        self.repository = repository
        self.fallback = fallback
        self.secret_cipher = LocalEncryptedSecretCipher.from_path(secret_key_path)
        self.credential_resolver = credential_resolver or ProfileCredentialResolver(
            EncryptedRepositorySecretStore(
                repository,
                cipher=self.secret_cipher,
            )
        )
        self.tool_runtime = tool_runtime
        self.strong_provider_profile_id = strong_provider_profile_id
        self.weak_provider_profile_id = weak_provider_profile_id
        self.active_provider_id = active_provider_id
        self.intent_mode = intent_mode
        self.bootstrap_state_dir = bootstrap_state_dir or repository.database_path.parent
        self.runtime_resolver = ProviderRuntimeResolver.default()
        self._stream_observer = None
        self.descriptor = CapabilityDescriptor(
            capability_id=capability_id,
            kind="model_provider",
            version="1.0.0",
            metadata={
                "description": f"{surface_label} model provider runtime wired to persisted provider profiles.",
                "intent_mode": self.intent_mode,
            },
        )
        if self.strong_provider_profile_id is not None or self.active_provider_id is not None or self.intent_mode == "embedded":
            self.ensure_embedding_bootstrap_state()

    def set_active_profiles(
        self,
        *,
        strong_provider_profile_id: str | None,
        provider_id: str | None,
        weak_provider_profile_id: str | None = None,
        intent_mode: str | None = None,
    ) -> None:
        self.strong_provider_profile_id = strong_provider_profile_id
        self.weak_provider_profile_id = weak_provider_profile_id or strong_provider_profile_id
        self.active_provider_id = provider_id
        if intent_mode is not None:
            self.intent_mode = intent_mode
        self.ensure_embedding_bootstrap_state()

    def _load_profile(self, profile_id: str | None) -> AuthProfile | None:
        if profile_id is None:
            return None
        return self.repository.load_auth_profile(profile_id)

    def active_profile(self) -> AuthProfile | None:
        if self.strong_provider_profile_id is not None:
            profile = self._load_profile(self.strong_provider_profile_id)
            if profile is not None:
                return profile
        if self.active_provider_id is not None:
            try:
                return self.repository.select_auth_profile(self.active_provider_id)
            except LookupError:
                return None
        return None

    def weak_profile(self) -> AuthProfile | None:
        if self.weak_provider_profile_id is not None:
            profile = self._load_profile(self.weak_provider_profile_id)
            if profile is not None:
                return profile
        return self.active_profile()

    def _profile_for_role(self, model_role: str) -> AuthProfile:
        normalized_role = model_role.strip().lower()
        if normalized_role == "strong":
            profile = self.active_profile()
            if profile is None:
                raise LookupError("no active strong provider profile is configured")
            return profile
        if normalized_role == "weak":
            profile = self.weak_profile()
            if profile is None:
                raise LookupError("no active weak provider profile is configured")
            return profile
        raise ValueError(f"unsupported model_role: {model_role}")

    def selection_state(self) -> MixtureModelSelection:
        try:
            strong_profile = self._profile_for_role("strong")
            weak_profile = self._profile_for_role("weak")
        except LookupError:
            return self.fallback.selection_state()
        return mixture_model_selection_from_auth_profiles(
            strong_profile=strong_profile,
            weak_profile=weak_profile,
            intent_mode=self.intent_mode,
        )

    def resolve_credentials(self, provider_profile: AuthProfile) -> Mapping[str, str]:
        return self.credential_resolver.resolve(provider_profile).as_mapping()

    def resolve_discovered_credentials(self, provider_id: str) -> Mapping[str, str]:
        resolution = self._discovered_secret_resolution(provider_id)
        if resolution is None:
            return {}
        return {"api_key": resolution.value}

    def has_stored_secret(self, reference_id: str) -> bool:
        return self.repository.has_auth_secret_value(reference_id)

    def store_secret_value(self, reference: SecretReference, value: str) -> None:
        encrypted = self.secret_cipher.encrypt(
            reference_id=reference.reference_id,
            value=value,
        )
        self.repository.upsert_auth_secret_value(encrypted)

    def set_stream_observer(self, observer) -> None:
        self._stream_observer = observer

    def _resolved_extra_headers_for(
        self,
        *,
        provider_id: str,
        active_profile: AuthProfile | None = None,
    ) -> Mapping[str, str]:
        if active_profile is not None and active_profile.provider_id == provider_id:
            if active_profile.extra_headers:
                return dict(active_profile.extra_headers)
        definition = provider_definition(provider_id)
        if definition is None:
            return {}
        return dict(definition.extra_headers)

    def _resolved_metadata_base_url(
        self,
        *,
        provider_id: str,
        base_url: str | None,
        active_profile: AuthProfile | None = None,
    ) -> str | None:
        normalized = _normalize_base_url(base_url)
        if normalized:
            return normalized
        if active_profile is not None and active_profile.provider_id == provider_id:
            normalized = _normalize_base_url(active_profile.base_url)
            if normalized:
                return normalized
        try:
            configured_profile = self.repository.select_auth_profile(provider_id)
        except LookupError:
            configured_profile = None
        if configured_profile is not None and configured_profile != active_profile:
            normalized = _normalize_base_url(configured_profile.base_url)
            if normalized:
                return normalized
        definition = provider_definition(provider_id)
        if definition is None:
            return None
        return _provider_base_url_from_env(provider_id, definition.base_url_env_var) or definition.default_base_url

    def _resolved_metadata_api_key(
        self,
        *,
        provider_id: str,
        explicit_api_key: str | None,
        active_profile: AuthProfile | None = None,
    ) -> str | None:
        if explicit_api_key:
            return explicit_api_key
        if active_profile is not None and active_profile.provider_id == provider_id:
            try:
                bundle = self.credential_resolver.resolve(active_profile)
            except LookupError:
                bundle = None
            if bundle is not None:
                resolved = str(bundle.values.get("api_key", "")).strip()
                if resolved:
                    return resolved
        try:
            configured_profile = self.repository.select_auth_profile(provider_id)
        except LookupError:
            configured_profile = None
        if configured_profile is not None and configured_profile != active_profile:
            try:
                bundle = self.credential_resolver.resolve(configured_profile)
            except LookupError:
                bundle = None
            if bundle is not None:
                resolved = str(bundle.values.get("api_key", "")).strip()
                if resolved:
                    return resolved
        discovered = self._discovered_secret_resolution(provider_id)
        if discovered is not None:
            resolved = str(discovered.value).strip()
            if resolved:
                return resolved
        return None

    def _hinted_models(self, provider_id: str) -> tuple[DiscoveredProviderModel, ...]:
        definition = provider_definition(provider_id)
        if definition is None:
            return ()
        models: list[DiscoveredProviderModel] = []
        seen: set[str] = set()
        for model_id in definition.model_hints:
            normalized = str(model_id).strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            try:
                reasoning_efforts = self.runtime_resolver.resolve(
                    provider_id,
                    model_id=normalized,
                    base_url=definition.default_base_url,
                ).reasoning_efforts
            except Exception:
                reasoning_efforts = ()
            models.append(
                DiscoveredProviderModel(
                    model_id=normalized,
                    label=normalized,
                    context_window_tokens=_heuristic_context_window(normalized),
                    source="catalog-hint",
                    metadata={"reasoning_efforts": ",".join(reasoning_efforts)},
                )
            )
        return tuple(models)

    def _merge_discovered_models(
        self,
        primary: tuple[DiscoveredProviderModel, ...],
        fallback: tuple[DiscoveredProviderModel, ...],
    ) -> tuple[DiscoveredProviderModel, ...]:
        merged = list(primary)
        positions = {item.model_id: index for index, item in enumerate(merged)}
        for hinted in fallback:
            index = positions.get(hinted.model_id)
            if index is None:
                positions[hinted.model_id] = len(merged)
                merged.append(hinted)
                continue
            current = merged[index]
            current_reasoning = str(current.metadata.get("reasoning_efforts", "")).strip()
            hinted_reasoning = str(hinted.metadata.get("reasoning_efforts", "")).strip()
            if current.context_window_tokens is not None and current_reasoning:
                continue
            merged[index] = DiscoveredProviderModel(
                model_id=current.model_id,
                label=current.label or hinted.label,
                context_window_tokens=current.context_window_tokens or hinted.context_window_tokens,
                max_output_tokens=current.max_output_tokens or hinted.max_output_tokens,
                source=current.source,
                metadata={
                    **dict(hinted.metadata),
                    **dict(current.metadata),
                    "reasoning_efforts": current_reasoning or hinted_reasoning,
                },
            )
        return tuple(merged)

    def _profile_secret_status(self, profile: AuthProfile) -> tuple[str, str]:
        if not profile.secret_references:
            return ("not-required", "not-required")
        try:
            bundle = self.credential_resolver.resolve(profile)
        except LookupError:
            return ("missing", "missing")
        sources = tuple(dict.fromkeys(bundle.value_sources.values()))
        source_summary = ", ".join(source for source in sources if source) or "encrypted-local-store"
        return ("stored", source_summary)

    def ensure_embedding_bootstrap_state(self) -> EmbeddingBootstrapState:
        return trigger_embedding_bootstrap(
            self.bootstrap_state_dir,
            intent_mode=self.intent_mode,
        )

    def _embedding_bootstrap_state(self) -> EmbeddingBootstrapState:
        return resolve_embedding_bootstrap_state(
            self.bootstrap_state_dir,
            intent_mode=self.intent_mode,
        )

    def describe(self) -> Mapping[str, object]:
        embedding_bootstrap = self._embedding_bootstrap_state()
        profile = self.active_profile()
        if profile is None:
            summary = provider_fallback_summary()
            summary["intent_mode"] = self.intent_mode
            summary["strong_profile_id"] = None
            summary["strong_model"] = None
            summary["weak_profile_id"] = None
            summary["weak_model"] = None
            summary["embedding_bootstrap_status"] = embedding_bootstrap.status
            summary["embedding_bootstrap_summary"] = embedding_bootstrap.summary
            summary["embedding_bootstrap_updated_at"] = embedding_bootstrap.updated_at
            summary["embedding_bootstrap_failure_message"] = embedding_bootstrap.failure_message
            summary["embedding_model_id"] = embedding_bootstrap.model_id
            summary["embedding_model_root"] = embedding_bootstrap.model_root
            summary["embedding_model_source_url"] = embedding_bootstrap.model_source_url
            return summary
        weak_profile = self.weak_profile() or profile
        summary = provider_profile_summary(profile)
        resolution = self.runtime_resolver.resolve(
            profile.provider_id,
            model_id=profile.default_model,
            base_url=profile.base_url,
        )
        summary.update(
            {
                "display_name": resolution.display_name,
                "transport_display_name": resolution.transport_display_name,
                "supports_streaming": resolution.supports_streaming,
                "supports_reasoning": resolution.supports_reasoning,
                "reasoning_efforts": resolution.reasoning_efforts,
                "auth_type": str(resolution.provider_metadata.get("auth_type", profile.auth_method)),
                "secret_status": self._profile_secret_status(profile)[0],
                "secret_source": self._profile_secret_status(profile)[1],
                "intent_mode": self.intent_mode,
                "strong_profile_id": profile.profile_id,
                "strong_model": profile.default_model,
                "weak_profile_id": weak_profile.profile_id,
                "weak_model": weak_profile.default_model,
                "embedding_bootstrap_status": embedding_bootstrap.status,
                "embedding_bootstrap_summary": embedding_bootstrap.summary,
                "embedding_bootstrap_updated_at": embedding_bootstrap.updated_at,
                "embedding_bootstrap_failure_message": embedding_bootstrap.failure_message,
                "embedding_model_id": embedding_bootstrap.model_id,
                "embedding_model_root": embedding_bootstrap.model_root,
                "embedding_model_source_url": embedding_bootstrap.model_source_url,
            }
        )
        return summary

    def discover_models(
        self,
        *,
        provider_id: str,
        base_url: str | None,
        api_key: str | None = None,
    ) -> tuple[DiscoveredProviderModel, ...]:
        active_profile = self.active_profile()
        resolved_base_url = self._resolved_metadata_base_url(
            provider_id=provider_id,
            base_url=base_url,
            active_profile=active_profile,
        )
        hinted_models = self._hinted_models(provider_id)
        if not resolved_base_url:
            return hinted_models
        if not resolved_base_url.startswith(("http://", "https://")):
            return hinted_models
        resolution = self.runtime_resolver.resolve(
            provider_id,
            model_id=self._default_model_for(provider_id) or "model-id",
            base_url=resolved_base_url,
        )
        resolved_api_key = self._resolved_metadata_api_key(
            provider_id=provider_id,
            explicit_api_key=api_key,
            active_profile=active_profile,
        )
        try:
            payload = _request_json(
                url=_compose_provider_url(resolved_base_url, _provider_model_catalog_path(provider_id)),
                headers=_provider_request_headers(
                    provider_id=provider_id,
                    request_family=resolution.request_family,
                    api_key=resolved_api_key,
                    extra_headers=self._resolved_extra_headers_for(
                        provider_id=provider_id,
                        active_profile=active_profile,
                    ),
                ),
            )
        except RuntimeError:
            return hinted_models
        data = _provider_model_items(provider_id, payload)
        if not data:
            return hinted_models
        models: list[DiscoveredProviderModel] = []
        for item in data:
            model_id = ""
            for key in _provider_model_id_keys(provider_id):
                candidate = str(item.get(key) or "").strip()
                if candidate:
                    model_id = candidate
                    break
            if not model_id:
                continue
            context_window_tokens = _context_window_from_payload(item)
            max_output_tokens = _max_output_tokens_from_payload(item)
            label = str(item.get("name") or item.get("label") or model_id)
            reasoning_efforts = ()
            capabilities = item.get("capabilities")
            if isinstance(capabilities, Mapping):
                supports_payload = capabilities.get("supports")
                if isinstance(supports_payload, Mapping):
                    raw_efforts = supports_payload.get("reasoning_effort")
                    if isinstance(raw_efforts, list):
                        reasoning_efforts = tuple(
                            str(value).strip().lower()
                            for value in raw_efforts
                            if str(value).strip()
                        )
            models.append(
                DiscoveredProviderModel(
                    model_id=model_id,
                    label=label,
                    context_window_tokens=context_window_tokens,
                    max_output_tokens=max_output_tokens,
                    metadata={
                        "owned_by": str(item.get("owned_by", "")),
                        "reasoning_efforts": ",".join(reasoning_efforts),
                    },
                )
            )
        if not models:
            return hinted_models
        return self._merge_discovered_models(tuple(models), hinted_models)

    def detect_context_window(
        self,
        *,
        provider_id: str,
        base_url: str | None,
        model_id: str,
        api_key: str | None = None,
    ) -> int | None:
        normalized_provider_id = provider_id.strip().lower()
        models = self.discover_models(
            provider_id=provider_id,
            base_url=base_url,
            api_key=api_key,
        )
        for item in models:
            if (
                item.model_id == model_id
                and item.context_window_tokens is not None
                and not (normalized_provider_id == "ollama" and item.source == "catalog-hint")
            ):
                return item.context_window_tokens
        active_profile = self.active_profile()
        resolved_base_url = self._resolved_metadata_base_url(
            provider_id=provider_id,
            base_url=base_url,
            active_profile=active_profile,
        )
        if not resolved_base_url:
            return None
        if not resolved_base_url.startswith(("http://", "https://")):
            return _heuristic_context_window(model_id)
        if normalized_provider_id == "ollama":
            detected = _query_ollama_context_window(
                model_id=model_id,
                base_url=resolved_base_url,
            )
            if detected is not None:
                return detected
        resolution = self.runtime_resolver.resolve(
            provider_id,
            model_id=model_id,
            base_url=resolved_base_url,
        )
        resolved_api_key = self._resolved_metadata_api_key(
            provider_id=provider_id,
            explicit_api_key=api_key,
            active_profile=active_profile,
        )
        try:
            payload = _request_json(
                url=_compose_provider_url(resolved_base_url, _provider_model_detail_path(provider_id, model_id)),
                headers=_provider_request_headers(
                    provider_id=provider_id,
                    request_family=resolution.request_family,
                    api_key=resolved_api_key,
                    extra_headers=self._resolved_extra_headers_for(
                        provider_id=provider_id,
                        active_profile=active_profile,
                    ),
                ),
            )
        except RuntimeError:
            metadata = resolve_provider_model_metadata(
                provider_id=provider_id,
                model_id=model_id,
                base_url=resolved_base_url,
                api_key=resolved_api_key,
            )
            return (
                metadata.context_window_tokens
                if metadata is not None and metadata.context_window_tokens is not None
                else _heuristic_context_window(model_id)
            )
        detected = _context_window_from_payload(payload)
        if detected is not None:
            return detected
        metadata = resolve_provider_model_metadata(
            provider_id=provider_id,
            model_id=model_id,
            base_url=resolved_base_url,
            api_key=resolved_api_key,
        )
        return (
            metadata.context_window_tokens
            if metadata is not None and metadata.context_window_tokens is not None
            else _heuristic_context_window(model_id)
        )

    def reasoning_efforts(
        self,
        *,
        provider_id: str,
        model_id: str,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> tuple[str, ...]:
        resolved_base_url = _normalize_base_url(base_url)
        if resolved_base_url:
            try:
                models = self.discover_models(
                    provider_id=provider_id,
                    base_url=resolved_base_url,
                    api_key=api_key,
                )
            except Exception:
                models = ()
            for item in models:
                if item.model_id != model_id:
                    continue
                raw_efforts = str(item.metadata.get("reasoning_efforts", "")).strip()
                if raw_efforts:
                    return tuple(part for part in raw_efforts.split(",") if part)
        resolution = self.runtime_resolver.resolve(
            provider_id,
            model_id=model_id,
            base_url=base_url,
        )
        return resolution.reasoning_efforts

    def discover_provider_states(self) -> tuple[DiscoveredProviderState, ...]:
        states: list[DiscoveredProviderState] = []
        for definition in default_provider_definitions(include_discovery_only=True):
            state = self._discover_provider_state(definition.provider_id)
            self.repository.upsert_provider_auth_state(
                ProviderAuthState(
                    provider_id=state.provider_id,
                    auth_type=state.auth_type,
                    status=state.status,
                    source=state.source,
                    profile_id=state.profile_id,
                    transport_id=state.metadata.get("transport_id") or None,
                    provider_kind=state.provider_kind,
                    base_url=state.base_url,
                    default_model=state.default_model,
                    runtime_enabled=state.runtime_enabled,
                    summary=state.metadata.get("summary", ""),
                    metadata=dict(state.metadata),
                    discovered_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
            )
            states.append(state)
        return tuple(states)

    def discovered_provider_state(self, provider_id: str) -> DiscoveredProviderState:
        return self._discover_provider_state(provider_id)

    def _discover_provider_state(self, provider_id: str) -> DiscoveredProviderState:
        definition = provider_definition(provider_id)
        if definition is None:
            raise LookupError(f"unknown provider definition: {provider_id}")
        try:
            profile = self.repository.select_auth_profile(provider_id)
        except LookupError:
            profile = None
        active_profile = self.active_profile()
        selected_profile = profile if profile is not None else (active_profile if active_profile and active_profile.provider_id == provider_id else None)
        base_url = (
            (selected_profile.base_url if selected_profile is not None else None)
            or _provider_base_url_from_env(definition.provider_id, definition.base_url_env_var)
            or definition.default_base_url
        )
        default_model = (selected_profile.default_model if selected_profile is not None else None) or definition.default_model_id
        if selected_profile is not None:
            secret_status, secret_source = self._profile_secret_status(selected_profile)
            if secret_status == "missing":
                status = "configured-missing-secret"
            else:
                status = "configured"
            source = secret_source if secret_status != "not-required" else "profile"
        else:
            secret_resolution = self._discovered_secret_resolution(provider_id)
            if secret_resolution is not None:
                status = "authenticated"
                source = secret_resolution.source
            elif definition.auth_type == "external_process":
                process_status = _copilot_acp_status() if provider_id == "copilot-acp" else None
                if process_status is not None:
                    base_url = process_status[0]
                    status = "authenticated"
                    source = process_status[1]
                else:
                    status = "discovery-only"
                    source = definition.metadata.get("runtime_status", "discovery-only")
            elif definition.provider_kind == "local" and self._local_provider_reachable(provider_id, base_url):
                status = "available"
                source = "local-probe"
            elif not definition.runtime_enabled:
                status = "discovery-only"
                source = definition.metadata.get("runtime_status", "discovery-only")
            else:
                status = "requires-setup"
                source = "none"
        try:
            resolution = self.runtime_resolver.resolve(
                provider_id,
                model_id=default_model or definition.default_model_id,
                base_url=base_url,
            )
            transport_display_name = resolution.transport_display_name
            reasoning_efforts = resolution.reasoning_efforts
            transport_id = resolution.transport_id
        except Exception:
            transport_display_name = definition.transport_id
            reasoning_efforts = ()
            transport_id = definition.transport_id
        summary = f"{status} via {source}"
        return DiscoveredProviderState(
            provider_id=definition.provider_id,
            display_name=definition.display_name,
            transport_display_name=transport_display_name,
            auth_type=definition.auth_type,
            provider_kind=definition.provider_kind,
            runtime_enabled=definition.runtime_enabled,
            status=status,
            source=source,
            profile_id=selected_profile.profile_id if selected_profile is not None else None,
            base_url=base_url,
            default_model=default_model,
            reasoning_efforts=reasoning_efforts,
            metadata={
                "transport_id": transport_id,
                "summary": summary,
                "supports_custom_base_url": str(definition.supports_custom_base_url).lower(),
            },
        )

    def _discovered_secret_resolution(self, provider_id: str) -> SecretValueResolution | None:
        definition = provider_definition(provider_id)
        if definition is None or not definition.required_secret_keys:
            return None
        reference_metadata: dict[str, str] = {}
        if definition.env_var_names:
            reference_metadata["env_var"] = definition.env_var_names[0]
        synthetic_reference = SecretReference(
            reference_id=f"discovery:{provider_id}:api_key",
            provider_id=provider_id,
            secret_name="api_token",
            secret_key="api_key",
            source="discovery",
            metadata=reference_metadata,
        )
        try:
            return self.credential_resolver.secret_store.resolve(synthetic_reference)
        except LookupError:
            return None

    def _local_provider_reachable(self, provider_id: str, base_url: str | None) -> bool:
        if not _normalize_base_url(base_url):
            return False
        try:
            return bool(self.discover_models(provider_id=provider_id, base_url=base_url))
        except Exception:
            return False

    def _default_model_for(self, provider_id: str) -> str | None:
        try:
            guide = self.runtime_resolver.build_setup_guide(provider_id)
        except LookupError:
            return None
        return guide.suggested_model_id

    def _model_visible_tools(self) -> tuple[ToolDefinition, ...]:
        if self.tool_runtime is None:
            return ()
        return self.tool_runtime.list_tools(
            audience="model",
            enabled_only=True,
            available_only=True,
        )

    def _fallback_tool_prompt(self, tools: tuple[ToolDefinition, ...]) -> str:
        prompt = build_tool_fallback_prompt(tools)
        if not prompt:
            return ""
        return (
            "## available runtime tools\n"
            "Native provider tool calling is unavailable on this transport. "
            "Use the governed built-in tool surface through fallback markup when tool work is necessary.\n"
            f"{prompt}"
        )

    def generate(
        self,
        *,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        prompt: str,
        model_role: str = "strong",
    ) -> ExecutionResult:
        try:
            active_profile = self._profile_for_role(model_role)
        except LookupError:
            return self.fallback.generate(
                profile=profile,
                session=session,
                context=context,
                prompt=prompt,
                model_role=model_role,
            )
        resolution = self.runtime_resolver.resolve(
            active_profile.provider_id,
            model_id=active_profile.default_model or None,
            base_url=active_profile.base_url,
        )
        visible_tools = self._model_visible_tools()
        request_tools = (
            tuple(tool.model_function_schema() for tool in visible_tools)
            if resolution.supports_tools
            else ()
        )
        request = ModelRequest(
            request_id=f"{session.session_id}:model:{model_role}",
            profile_id=profile.profile_id,
            session_id=session.session_id,
            provider_id=active_profile.provider_id,
            model_id=active_profile.default_model or "",
            prompt=prompt,
            context={
                "bundle_id": context.bundle_id,
                "token_budget": str(context.token_budget),
                "instruction_refs": ",".join(context.instruction_refs),
                "goal_ids": ",".join(context.goal_ids),
                "memory_ids": ",".join(context.memory_ids),
                "artifact_ids": ",".join(context.artifact_ids),
                "frozen_prefix_prompt": context.prompt_envelope.frozen_prefix,
                "session_snapshot_prompt": context.prompt_envelope.session_snapshot,
                "turn_injections_prompt": context.prompt_envelope.turn_injections,
                "tool_schema_prompt": "",
                "rendered_prompt": context.rendered_prompt or "",
            },
            reasoning_effort=str(active_profile.metadata.get("reasoning_effort", "")).strip() or None,
            metadata={
                "profile_mode": profile.mode,
                "session_status": session.status,
                "provider_profile_id": active_profile.profile_id,
            },
            tools=request_tools,
        )

        credentials = self.credential_resolver.resolve(active_profile).as_mapping()
        adapter = build_model_adapter(
            active_profile,
            runtime_resolver=self.runtime_resolver,
            credentials=credentials,
            adapter_id=f"adapter.models.{active_profile.provider_id}.surface",
            stream_observer=self._stream_observer,
        )
        if adapter is None:
            return self.fallback.generate(
                profile=profile,
                session=session,
                context=context,
                prompt=prompt,
            )
        result = adapter.generate(request, credentials)
        return ExecutionResult(
            execution_id=result.result_id,
            session_id=session.session_id,
            outcome="ok" if result.failure_kind is None else "failed",
            summary=result.content,
            prompt_tokens=result.usage.prompt_tokens,
            completion_tokens=result.usage.completion_tokens,
            total_tokens=result.usage.total_tokens,
            cached_prompt_tokens=result.usage.cached_prompt_tokens,
            cache_creation_prompt_tokens=result.usage.cache_creation_prompt_tokens,
            cache_usage_reported=result.usage.cache_usage_reported,
            telemetry_event_ids=(request.request_id,),
            side_effects=(
                f"provider={result.provider_id}",
                f"model={result.model_id}",
                f"model_role={model_role}",
                f"transport={result.metadata.get('transport_id', 'unknown')}",
                f"credential_keys={result.metadata.get('credential_keys', 'unknown')}",
            ),
            tool_calls=result.tool_calls,
        )
