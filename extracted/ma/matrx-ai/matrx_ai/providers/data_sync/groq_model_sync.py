import asyncio
from matrx_utils import clear_terminal, vcprint
from matrx_utils.data_in_code.make_updates import update_data_in_code
from matrx_ai.providers.groq.client import get_groq_client
from matrx_ai.local_data.paths import GROQ_MODELS_FILE, MODELS_TS_FILE


def _dump(obj) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return obj


async def list_groq_models() -> list[dict]:
    client = get_groq_client()
    response = await client.models.list()
    return [_dump(model) for model in response.data]


if __name__ == "__main__":
    clear_terminal()

    results = asyncio.run(list_groq_models())

    vcprint(results, "[MODEL SYNC] Groq Results", color="blue")

    update_data_in_code(
        variable_name="groq_models",
        new_value=results,
        filename=GROQ_MODELS_FILE,
        ts_filename=MODELS_TS_FILE,
    )
