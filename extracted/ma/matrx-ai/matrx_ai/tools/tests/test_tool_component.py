import asyncio
from matrx_utils import vcprint, clear_terminal
from matrx_ai.tools.tool_def_db import tool_def_manager_instance


tm = tool_def_manager_instance

""""
    async def get_conversation_data(self, conversation_id: str) -> dict[str, Any]:
        item, all_related = await self.conversation.get_conversation_with_all_related(
            conversation_id
        )
        # vcprint(item, "[CX MANAGERS] Item", color="green")
        # vcprint(all_related, "[CX MANAGERS] All Related", color="cyan")
        conversation = item
        foreign_keys = all_related.foreign_keys
        inverse_fks = all_related.inverse_foreign_keys
        
        user_requests = inverse_fks.get("user_request", [])
        requests = inverse_fks.get("request", [])
        messages = inverse_fks.get("message", [])
        tool_calls = inverse_fks.get("tool_call", [])
        media = inverse_fks.get("media", [])

        return {
            "conversation": conversation,
            "foreign_keys": foreign_keys,
            "user_requests": user_requests,
            "requests": requests,
            "messages": messages,
            "tool_calls": tool_calls,
            "media": media,
        }



"""



async def fetch_components_for_tool(tool_id: str):
    tool, all_related = await tm.get_tool_with_all_related(tool_id)
    vcprint(tool, "[TEST] Data", color="green")
    vcprint(all_related, "[TEST] All Related", color="cyan")
    
    fks = all_related.foreign_keys
    ifks = all_related.inverse_foreign_keys
    vcprint(fks, "[TEST] Foreign Keys", color="cyan")
    vcprint(ifks, "[TEST] Inverse Foreign Keys", color="cyan")
    
    tool_ui_components = ifks.get("tool_ui_components", [])
    vcprint(tool_ui_components, "[TEST] Tool UI Components", color="blue")
    
    return tool_ui_components


async def fetch_samples_for_tool(tool_id: str):
    tool = await tm.get_tool_with_all_related(tool_id)
    return tool.tool_test_samples

async def fetch_incidents_for_tool(tool_id: str):
    tool = await tm.get_tool_with_all_related(tool_id)
    return tool.tool_ui_incidents



if __name__ == "__main__":
    clear_terminal()
    tool_id = "075194f7-3766-4ae7-a887-2234331b49c1"
    
    components = asyncio.run(fetch_components_for_tool(tool_id))
    vcprint(components, "[TEST] Components", color="yellow")
    
    # samples = asyncio.run(fetch_samples_for_tool(tool_id))
    # vcprint(samples, "[TEST] Samples", color="green")
    
    # incidents = asyncio.run(fetch_incidents_for_tool(tool_id))
    # vcprint(incidents, "[TEST] Incidents", color="green")
    
    
    