from typing import Any, Dict, Callable

import pytest

from scale_gp_beta.lib.tracing import (
    PlatformError,
    ApplicationError,
    ExceptionMapping,
    ErrorClassifierConfig,
    TracebackOwnershipPolicy,
    classify_error,
)


def _function(module: str, filename: str, body: str, **values: Any) -> Callable[[], None]:
    namespace: Dict[str, Any] = {"__name__": module, **values}
    exec(compile(f"def run():\n    {body}\n", filename, "exec"), namespace)
    return namespace["run"]


def _classify_raised(
    function: Callable[[], None],
    config: ErrorClassifierConfig,
    **kwargs: Any,
):
    try:
        function()
    except Exception as exc:
        return classify_error(exc, config=config, **kwargs)
    raise AssertionError("synthetic function did not raise")


@pytest.fixture
def policy() -> TracebackOwnershipPolicy:
    return TracebackOwnershipPolicy(
        application_module_prefixes=("customer_app",),
        platform_module_prefixes=("managed_runtime",),
        ignored_module_prefixes=("third_party",),
        ignored_file_roots=("/venv/site-packages",),
    )


def test_application_origin(policy: TracebackOwnershipPolicy) -> None:
    application = _function("customer_app.tool", "/workspace/app/tool.py", "raise RuntimeError('boom')")

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == "application"
    assert result.source == "stack_trace"
    assert result.reason == "stack_rule:application_module"


def test_platform_origin(policy: TracebackOwnershipPolicy) -> None:
    platform = _function(
        "managed_runtime.worker",
        "/runtime/worker.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(platform, ErrorClassifierConfig(policy))

    assert result.category == "platform"
    assert result.reason == "stack_rule:platform_module"


def test_platform_calling_application_uses_innermost_owner(policy: TracebackOwnershipPolicy) -> None:
    application = _function("customer_app.tool", "/workspace/app/tool.py", "raise RuntimeError('boom')")
    platform = _function(
        "managed_runtime.runner",
        "/runtime/runner.py",
        "target()",
        target=application,
    )

    result = _classify_raised(platform, ErrorClassifierConfig(policy))

    assert result.category == "application"


def test_application_calling_platform_uses_innermost_owner(policy: TracebackOwnershipPolicy) -> None:
    platform = _function("managed_runtime.store", "/runtime/store.py", "raise RuntimeError('boom')")
    application = _function(
        "customer_app.main",
        "/workspace/app/main.py",
        "target()",
        target=platform,
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == "platform"


def test_dependency_under_application(policy: TracebackOwnershipPolicy) -> None:
    dependency = _function(
        "third_party.transport",
        "/venv/site-packages/third_party/transport.py",
        "raise RuntimeError('boom')",
    )
    application = _function(
        "customer_app.main",
        "/workspace/app/main.py",
        "target()",
        target=dependency,
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == "application"
    assert result.reason == "stack_rule:application_module"


def test_dependency_under_platform(policy: TracebackOwnershipPolicy) -> None:
    dependency = _function(
        "third_party.transport",
        "/venv/site-packages/third_party/transport.py",
        "raise RuntimeError('boom')",
    )
    platform = _function(
        "managed_runtime.transport",
        "/runtime/transport.py",
        "target()",
        target=dependency,
    )

    result = _classify_raised(platform, ErrorClassifierConfig(policy))

    assert result.category == "platform"


def test_explicit_category_overrides_traceback(policy: TracebackOwnershipPolicy) -> None:
    platform = _function("managed_runtime.worker", "/runtime/worker.py", "raise RuntimeError('boom')")

    result = _classify_raised(
        platform,
        ErrorClassifierConfig(policy),
        explicit_category="application",
    )

    assert result.category == "application"
    assert result.source == "explicit"


@pytest.mark.parametrize(
    ("error_type", "category"),
    [(ApplicationError, "application"), (PlatformError, "platform")],
)
def test_typed_error_overrides_traceback(
    policy: TracebackOwnershipPolicy,
    error_type: type,
    category: str,
) -> None:
    application = _function(
        "customer_app.main",
        "/workspace/app/main.py",
        "raise error_type('boom')",
        error_type=error_type,
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == category
    assert result.source == "categorized_error"


def test_no_traceback_is_unknown() -> None:
    result = classify_error(RuntimeError("boom"))

    assert result.category == "unknown"
    assert result.reason == "stack_no_traceback"


def test_conflicting_frame_ownership_is_unknown() -> None:
    policy = TracebackOwnershipPolicy(
        application_module_prefixes=("shared",),
        platform_module_prefixes=("shared",),
        ignored_file_roots=(),
    )
    shared = _function("shared.runtime", "/shared/runtime.py", "raise RuntimeError('boom')")

    result = _classify_raised(shared, ErrorClassifierConfig(policy))

    assert result.category == "unknown"
    assert result.reason == "stack_ambiguous_owned_frame"


def test_application_module_ownership_beats_platform_file_root() -> None:
    policy = TracebackOwnershipPolicy(
        application_module_prefixes=("customer_app",),
        platform_file_roots=("/shared/runtime",),
        ignored_file_roots=(),
    )
    application = _function(
        "customer_app.worker",
        "/shared/runtime/worker.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == "application"
    assert result.reason == "stack_rule:application_module"


def test_platform_module_ownership_beats_application_file_root() -> None:
    policy = TracebackOwnershipPolicy(
        platform_module_prefixes=("managed_runtime",),
        application_file_roots=("/shared/runtime",),
        ignored_file_roots=(),
    )
    platform = _function(
        "managed_runtime.worker",
        "/shared/runtime/worker.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(platform, ErrorClassifierConfig(policy))

    assert result.category == "platform"
    assert result.reason == "stack_rule:platform_module"


def test_specific_owned_prefix_beats_broad_ignored_prefix() -> None:
    policy = TracebackOwnershipPolicy(
        platform_module_prefixes=("framework.persistence",),
        ignored_module_prefixes=("framework",),
        ignored_file_roots=(),
    )
    persistence = _function(
        "framework.persistence.store",
        "/framework/persistence/store.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(persistence, ErrorClassifierConfig(policy))

    assert result.category == "platform"
    assert result.reason == "stack_rule:platform_module"


def test_unresolvable_synthetic_frame_is_unknown(policy: TracebackOwnershipPolicy) -> None:
    unknown = _function("obfuscated", "<obfuscated>", "raise RuntimeError('boom')")
    application = _function(
        "customer_app.main",
        "/workspace/app/main.py",
        "target()",
        target=unknown,
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == "unknown"
    assert result.reason == "stack_unresolvable_frame"


def test_installed_application_module_prefix_overrides_ignored_root() -> None:
    policy = TracebackOwnershipPolicy(
        application_module_prefixes=("installed_app",),
        ignored_file_roots=("/venv/site-packages",),
    )
    application = _function(
        "installed_app.main",
        "/venv/site-packages/installed_app/main.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))

    assert result.category == "application"


def test_owned_archive_module_uses_module_rule() -> None:
    policy = TracebackOwnershipPolicy(platform_module_prefixes=("managed_runtime",))
    platform = _function(
        "managed_runtime.worker",
        "/packages/runtime.pyz/managed_runtime/worker.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(platform, ErrorClassifierConfig(policy))

    assert result.category == "platform"


def test_unowned_archive_frame_is_unknown() -> None:
    unknown = _function(
        "unknown_package.worker",
        "/packages/runtime.pyz/unknown_package/worker.py",
        "raise RuntimeError('boom')",
    )

    result = _classify_raised(unknown, ErrorClassifierConfig())

    assert result.category == "unknown"
    assert result.reason == "stack_archive_frame"


def test_scoped_mapping_is_not_global() -> None:
    config = ErrorClassifierConfig(
        mappings=(ExceptionMapping("provider", TimeoutError, "platform"),),
    )
    unscoped = classify_error(TimeoutError("boom"), config=config)
    scoped = classify_error(TimeoutError("boom"), config=config, mapping_scope="provider")

    assert unscoped.category == "unknown"
    assert scoped.category == "platform"
    assert scoped.source == "mapping"
    assert scoped.reason == "registered_exception_mapping"


def test_mapping_subclasses_require_opt_in() -> None:
    class ProviderTimeout(TimeoutError):
        pass

    exact_config = ErrorClassifierConfig(
        mappings=(ExceptionMapping("provider", TimeoutError, "platform"),),
    )
    subclass_config = ErrorClassifierConfig(
        mappings=(ExceptionMapping("provider", TimeoutError, "platform", include_subclasses=True),),
    )

    assert classify_error(ProviderTimeout(), config=exact_config, mapping_scope="provider").category == "unknown"
    assert classify_error(ProviderTimeout(), config=subclass_config, mapping_scope="provider").category == "platform"


def test_boundary_is_fallback_after_unresolved_stack(policy: TracebackOwnershipPolicy) -> None:
    unknown = _function("obfuscated", "<obfuscated>", "raise RuntimeError('boom')")

    result = _classify_raised(
        unknown,
        ErrorClassifierConfig(policy),
        boundary_category="application",
    )

    assert result.category == "application"
    assert result.source == "boundary"


def test_provenance_never_contains_traceback_details(policy: TracebackOwnershipPolicy) -> None:
    application = _function(
        "customer_app.secret",
        "/workspace/customer-secret/path.py",
        "raise RuntimeError('sensitive message')",
    )

    result = _classify_raised(application, ErrorClassifierConfig(policy))
    serialized = f"{result.source}|{result.reason}|{result.classifier_version}"

    assert "/workspace" not in serialized
    assert "customer-secret" not in serialized
    assert "sensitive message" not in serialized
    assert "RuntimeError" not in serialized
