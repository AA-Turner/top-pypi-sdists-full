import asyncio
from matrx_utils import vcprint, clear_terminal
from matrx_ai.db.content_types.notes import notes_manager_instance
from matrx_ai.db.content_types.tasks import tasks_manager_instance


# ---------------------------------------------------------------------------
# Note helpers
# ---------------------------------------------------------------------------

async def fetch_note(note_id: str):
    return await notes_manager_instance.get_note(note_id)

async def fetch_note_as_llm_xml(note_id: str):
    note = await notes_manager_instance.get_note(note_id)
    vcprint(note, "[TEST] Note")
    result = await notes_manager_instance.get_note_as_xml(note_id)
    vcprint(result.get("xml", result), "[TEST] Note XML")
    return result

async def test_update_note(note_id: str):
    result = await notes_manager_instance.update_note(
        note_id,
        label="Speaking Topics (updated)",
    )
    vcprint(result, "[TEST] Update Note")
    return result

async def test_patch_note(note_id: str):
    result = await notes_manager_instance.patch_note_content(
        note_id,
        search_text="I need to work on this when there is more time.",
        replacement_text="I need to work on this before the next sprint.",
    )
    vcprint(result, "[TEST] Patch Note")
    return result

async def test_patch_note_fuzzy(note_id: str):
    # Deliberately sloppy whitespace — should still match via pass 2 or 3
    result = await notes_manager_instance.patch_note_content(
        note_id,
        search_text="I  need  to  work  on  this  when  there  is  more  time.",
        replacement_text="I need to work on this before the next sprint.",
    )
    vcprint(result, "[TEST] Patch Note (fuzzy whitespace)")
    return result

async def test_append_note(note_id: str):
    result = await notes_manager_instance.append_to_note(
        note_id,
        text="## Action Items\n\n- Book venue\n- Prepare slides",
    )
    vcprint(result, "[TEST] Append to Note")
    return result

async def test_prepend_note(note_id: str):
    result = await notes_manager_instance.prepend_to_note(
        note_id,
        text="**Status:** In Progress",
    )
    vcprint(result, "[TEST] Prepend to Note")
    return result

# ---------------------------------------------------------------------------
# Task helpers
# ---------------------------------------------------------------------------

async def fetch_task(task_id: str):
    result = await tasks_manager_instance.get_task(task_id)
    vcprint(result, "[TEST] Task")
    return result

async def fetch_task_as_xml(task_id: str):
    result = await tasks_manager_instance.get_task_as_xml(task_id)
    vcprint(result.get("xml", result), "[TEST] Task XML")
    return result

async def test_list_tasks_for_project(project_id: str):
    result = await tasks_manager_instance.list_tasks_for_project(project_id)
    vcprint(result, "[TEST] Tasks for Project")
    return result

async def test_list_subtasks(parent_task_id: str):
    result = await tasks_manager_instance.list_subtasks(parent_task_id)
    vcprint(result, "[TEST] Subtasks")
    return result

async def test_update_task(task_id: str):
    result = await tasks_manager_instance.update_task(
        task_id,
        status="completed",
        priority="high",
    )
    vcprint(result, "[TEST] Update Task")
    return result


# ---------------------------------------------------------------------------
# Runner — set test_mode to any key below to run that test.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_terminal()

    # Constants
    quick_note_id = "e6dafe9f-3505-44d4-87df-789405b7fec9"
    full_note_id   = "cd199d26-12fe-4c88-a229-e751c71eb9e0"
    task_id        = "1814841d-2726-44fe-8954-8dd6a12985a5"
    project_id     = "4e34e88a-861f-4458-8d9c-fbe00f6a8fc5"

    # ---- pick one ----
    test_mode = "task_xml"
    note_id   = quick_note_id

    if test_mode == "note":
        result = asyncio.run(fetch_note(note_id))
        vcprint(result, "[TEST] Note")

    elif test_mode == "note_xml":
        asyncio.run(fetch_note_as_llm_xml(note_id))

    elif test_mode == "update":
        asyncio.run(test_update_note(note_id))

    elif test_mode == "patch":
        asyncio.run(test_patch_note(note_id))

    elif test_mode == "patch_fuzzy":
        asyncio.run(test_patch_note_fuzzy(note_id))

    elif test_mode == "append":
        asyncio.run(test_append_note(note_id))

    elif test_mode == "prepend":
        asyncio.run(test_prepend_note(note_id))

    elif test_mode == "task":
        asyncio.run(fetch_task(task_id))

    elif test_mode == "task_xml":
        asyncio.run(fetch_task_as_xml(task_id))

    elif test_mode == "task_list_project":
        asyncio.run(test_list_tasks_for_project(project_id))

    elif test_mode == "task_subtasks":
        asyncio.run(test_list_subtasks(task_id))

    elif test_mode == "task_update":
        asyncio.run(test_update_task(task_id))
