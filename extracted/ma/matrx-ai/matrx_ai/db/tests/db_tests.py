from typing import Any
from matrx_ai.db import cxm
from matrx_ai.config.unified_config import UnifiedConfig

def get_full_conversation(conversation_id: str) -> dict[str, Any]:
    import asyncio

    return asyncio.run(cxm.get_full_conversation(conversation_id))


def get_conversation_unified_config(conversation_id: str) -> UnifiedConfig:
    import asyncio
    return asyncio.run(cxm.get_conversation_unified_config(conversation_id))


if __name__ == "__main__":
    from matrx_utils import vcprint, clear_terminal

    clear_terminal()
    conversation_id_basic = "237d16be-1d12-411f-9f79-ba79820ab062"
    conversation_id_tools = "4b796ad3-ef2e-465f-9cb0-5fa2f23273a3"
    conversation_3 = "03e46c9b-9fc7-4aa6-80dd-9a53cdf23708"

    # result = get_full_conversation(conversation_id_tools)
    # vcprint(result, "[CX MANAGERS] Result", color="cyan")


    result = get_conversation_unified_config(conversation_3)
    vcprint(result, "[CX MANAGERS] Result", color="cyan")