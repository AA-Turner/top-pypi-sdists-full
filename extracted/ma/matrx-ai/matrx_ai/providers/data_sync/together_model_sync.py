import asyncio
from typing import Any

from matrx_utils import clear_terminal, vcprint
from matrx_utils.data_in_code.make_updates import update_data_in_code

from matrx_ai.local_data.paths import MODELS_TS_FILE, TOGETHER_MODELS_FILE
from matrx_ai.providers.together.client import get_together_client


def _dump(obj) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return obj


async def list_together_models() -> list[dict]:
    client = get_together_client()
    # Together answers with a bare JSON array, not OpenAI's {"data": [...]} page.
    models = await client.get("/models", cast_to=list[dict[str, Any]])
    return [_dump(model) for model in models]


if __name__ == "__main__":
    clear_terminal()

    results = asyncio.run(list_together_models())

    vcprint(results, "[MODEL SYNC] Together Results", color="blue")

    update_data_in_code(
        variable_name="together_models",
        new_value=results,
        filename=TOGETHER_MODELS_FILE,
        ts_filename=MODELS_TS_FILE,
    )
