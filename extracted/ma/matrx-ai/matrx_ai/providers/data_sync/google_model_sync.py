from matrx_utils import clear_terminal, vcprint
from matrx_utils.data_in_code.make_updates import update_data_in_code
from matrx_ai.providers.google.google_client import get_google_client
from matrx_ai.local_data.paths import GOOGLE_MODELS_FILE, MODELS_TS_FILE


def _dump(obj) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return obj


def list_google_models() -> list[dict]:
    client = get_google_client()
    return [_dump(model) for model in client.models.list()]


if __name__ == "__main__":
    clear_terminal()

    results = list_google_models()

    vcprint(results, "[MODEL SYNC] Google Results", color="blue")

    update_data_in_code(
        variable_name="google_models",
        new_value=results,
        filename=GOOGLE_MODELS_FILE,
        ts_filename=MODELS_TS_FILE,
    )
