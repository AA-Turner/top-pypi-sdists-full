import asyncio
from matrx_utils import clear_terminal, vcprint
from matrx_utils.data_in_code.make_updates import update_data_in_code
from matrx_ai.providers.anthropic.client import get_anthropic_client
from matrx_ai.local_data.paths import (
    ANTHROPIC_MODELS_FILE,
    MODELS_DATA_FILE,
    MODELS_TS_FILE,
)


def _dump(obj) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return obj


async def list_anthropic_models() -> list[dict]:
    client = get_anthropic_client()
    models = []
    async for model in client.beta.models.list(limit=1000):
        models.append(_dump(model))
    return models


async def get_anthropic_model(model_id: str) -> dict:
    client = get_anthropic_client()
    model = await client.beta.models.retrieve(model_id)
    return _dump(model)


async def sync_all_providers() -> dict[str, list[dict]]:
    from matrx_ai.providers.data_sync.openai_model_sync import list_openai_models
    from matrx_ai.providers.data_sync.google_model_sync import list_google_models
    from matrx_ai.providers.data_sync.groq_model_sync import list_groq_models
    from matrx_ai.providers.data_sync.together_model_sync import list_together_models
    from matrx_ai.providers.data_sync.xai_model_sync import list_xai_models
    from matrx_ai.providers.data_sync.cerebras_model_sync import list_cerebras_models
    from matrx_ai.local_data.paths import (
        OPENAI_MODELS_FILE, GOOGLE_MODELS_FILE, GROQ_MODELS_FILE,
        TOGETHER_MODELS_FILE, XAI_MODELS_FILE, CEREBRAS_MODELS_FILE,
    )

    async def _safe_fetch(name: str, coro) -> tuple[str, list[dict]]:
        try:
            result = await coro
            return name, result
        except Exception as e:
            vcprint(f"[MODEL SYNC] {name} failed: {e}", color="red")
            return name, []

    def _safe_sync_fetch(name: str, fn) -> tuple[str, list[dict]]:
        try:
            return name, fn()
        except Exception as e:
            vcprint(f"[MODEL SYNC] {name} failed: {e}", color="red")
            return name, []

    async_results = await asyncio.gather(
        _safe_fetch("anthropic", list_anthropic_models()),
        _safe_fetch("openai", list_openai_models()),
        _safe_fetch("groq", list_groq_models()),
        _safe_fetch("together", list_together_models()),
        _safe_fetch("xai", list_xai_models()),
        _safe_fetch("cerebras", list_cerebras_models()),
    )

    all_results: dict[str, list[dict]] = dict(async_results)

    # Google SDK is synchronous — run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    _, google_models = await loop.run_in_executor(
        None, lambda: _safe_sync_fetch("google", list_google_models)
    )
    all_results["google"] = google_models

    file_map = {
        "anthropic": ANTHROPIC_MODELS_FILE,
        "openai": OPENAI_MODELS_FILE,
        "google": GOOGLE_MODELS_FILE,
        "groq": GROQ_MODELS_FILE,
        "together": TOGETHER_MODELS_FILE,
        "xai": XAI_MODELS_FILE,
        "cerebras": CEREBRAS_MODELS_FILE,
    }

    for provider, models in all_results.items():
        if models:
            update_data_in_code(
                variable_name=f"{provider}_models",
                new_value=models,
                filename=file_map[provider],
                ts_filename=MODELS_TS_FILE,
            )

    update_data_in_code(
        variable_name="all_provider_models",
        new_value=all_results,
        filename=MODELS_DATA_FILE,
        ts_filename=MODELS_TS_FILE,
    )

    return all_results


if __name__ == "__main__":
    clear_terminal()

    task = "sync_all"  # "sync_all" | "list_anthropic" | "get_anthropic_model"

    if task == "sync_all":
        all_results = asyncio.run(sync_all_providers())
        for provider, models in all_results.items():
            vcprint(models, f"[MODEL SYNC] {provider} ({len(models)} models)", color="blue")

    elif task == "list_anthropic":
        results = asyncio.run(list_anthropic_models())
        vcprint(results, "[MODEL SYNC] Anthropic Results", color="blue")
        update_data_in_code(
            variable_name="anthropic_models",
            new_value=results,
            filename=ANTHROPIC_MODELS_FILE,
            ts_filename=MODELS_TS_FILE,
        )

    elif task == "get_anthropic_model":
        model_id = "claude-opus-4-5"
        result = asyncio.run(get_anthropic_model(model_id))
        vcprint(result, f"[MODEL SYNC] {model_id}", color="blue")
