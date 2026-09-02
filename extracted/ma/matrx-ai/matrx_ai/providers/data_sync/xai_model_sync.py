import asyncio
from matrx_utils import clear_terminal, vcprint
from matrx_utils.data_in_code.make_updates import update_data_in_code
from matrx_ai.providers.xai.client import get_xai_client
from matrx_ai.local_data.paths import XAI_MODELS_FILE, MODELS_TS_FILE


def _dump(obj) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return obj


async def list_xai_models() -> list[dict]:
    client = get_xai_client()
    models = []
    async for model in client.models.list():
        models.append(_dump(model))
    return models


if __name__ == "__main__":
    clear_terminal()

    results = asyncio.run(list_xai_models())

    vcprint(results, "[MODEL SYNC] xAI Results", color="blue")

    update_data_in_code(
        variable_name="xai_models",
        new_value=results,
        filename=XAI_MODELS_FILE,
        ts_filename=MODELS_TS_FILE,
    )
