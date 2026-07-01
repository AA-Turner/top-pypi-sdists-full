import asyncio
import base64
import json
import logging
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from cvc.adapters.telegram_streamer import TelegramStreamer

logger = logging.getLogger("cvc.telegram_handler")

# We will maintain a global dict of pending tool approvals for Telegram
# message_id -> { "tool": tc, "event": asyncio.Event(), "decision": "" }
pending_approvals = {}

# Locks to prevent concurrent execution for the same user
session_locks = {}

def register_handlers(dp: Dispatcher, bot: Bot, settings: Any, workspace_mgr: Any):
    
    @dp.message()
    async def handle_message(message: types.Message):
        print(f"DEBUG: Received message from {message.from_user.id}: {message.text}")
        if message.from_user.id not in settings.telegram.allowlist:
            logger.warning(f"Unauthorized access from Telegram ID: {message.from_user.id}")
            return
            
        import cvc.gateway as gw
        
        if not gw._agent_llm or not gw._agent_tools:
            await message.answer("CVC Agent LLM is not initialized yet.")
            return
            
        session_key = f"{message.chat.id}_{message.message_thread_id or 0}"
        
        # Ensure only one task runs per session at a time
        if session_key not in session_locks:
            session_locks[session_key] = asyncio.Lock()
            
        if session_locks[session_key].locked():
            await message.answer("⚠️ <i>A task is currently running. Please wait until it completes.</i>", parse_mode=ParseMode.HTML)
            return
            
        async with session_locks[session_key]:
            # Push message to LLM context
            if not hasattr(gw, "_tg_sessions"):
                gw._tg_sessions = {}
                
            if session_key not in gw._tg_sessions:
                gw._tg_sessions[session_key] = [{"role": "system", "content": gw._system_prompt}]
                
            user_text = message.text or message.caption or ""
            
            # Handle Slash Commands
            if user_text.startswith("/"):
                cmd_parts = user_text.split(maxsplit=1)
                cmd = cmd_parts[0].lower()
                
                if cmd == "/clear":
                    gw._tg_sessions[session_key] = [{"role": "system", "content": gw._system_prompt}]
                    await message.answer("🔄 <i>Conversation cleared. CVC state preserved.</i>", parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/help":
                    help_text = (
                        "<b>🤖 CVC Telegram Bot Commands</b>\n\n"
                        "<code>/status</code> - Show agent status\n"
                        "<code>/log</code> - Show recent commits\n"
                        "<code>/commit [msg]</code> - Commit changes\n"
                        "<code>/branch [name]</code> - Switch/create branch\n"
                        "<code>/checkout [name]</code> - Checkout branch\n"
                        "<code>/branches</code> - List all branches\n"
                        "<code>/search [query]</code> - Search codebase\n"
                        "<code>/model</code> - Change LLM model\n"
                        "<code>/provider</code> - Change LLM provider\n"
                        "<code>/clear</code> - Clear context\n"
                        "<code>/history</code> - Session history\n"
                        "<i>Other tools:</i> /undo, /retry, /cost, /analytics, /web, /git, /image, /memory, /compact, /health"
                    )
                    await message.answer(help_text, parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/history":
                    llms = gw._tg_sessions[session_key]
                    user_turns = len([m for m in llms if m.get("role") == "user"])
                    tool_calls = len([m for m in llms if m.get("role") == "tool"])
                    await message.answer(f"📜 <b>Session History:</b>\n\nUser Turns: {user_turns}\nTool Calls: {tool_calls}\nTotal Context Messages: {len(llms)}", parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/status":
                    model_info = getattr(gw._agent_llm, "model", "Unknown")
                    provider_info = getattr(gw._agent_llm, "provider", "Unknown")
                    ws_path = getattr(workspace_mgr, "workspace_dir", "Unknown")
                    status_text = (
                        f"📊 <b>CVC Agent Status</b>\n\n"
                        f"<b>Provider:</b> <code>{provider_info}</code>\n"
                        f"<b>Model:</b> <code>{model_info}</code>\n"
                        f"<b>Workspace:</b> <code>{ws_path}</code>\n"
                    )
                    await message.answer(status_text, parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/cvc":
                    await message.answer("🔧 <b>CVC Agent is Active.</b>\nSend me a message to execute a task, or use /help to see commands.", parse_mode=ParseMode.HTML)
                    return
                elif cmd in ("/exit", "/quit", "/q"):
                    gw._tg_sessions[session_key] = [{"role": "system", "content": gw._system_prompt}]
                    await message.answer("🛑 <i>Session ended and context cleared.</i>", parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/model":
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                        [
                            types.InlineKeyboardButton(text="GPT-4o", callback_data="set_model:gpt-4o"),
                            types.InlineKeyboardButton(text="Claude 3.7 Sonnet", callback_data="set_model:claude-3-7-sonnet-20250219"),
                        ],
                        [
                            types.InlineKeyboardButton(text="Gemini 3.1 Pro", callback_data="set_model:gemini-3.1-pro-preview"),
                            types.InlineKeyboardButton(text="Qwen 2.5", callback_data="set_model:qwen2.5"),
                        ]
                    ])
                    await message.answer("Select a model:", reply_markup=keyboard)
                    return
                elif cmd == "/provider":
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                        [
                            types.InlineKeyboardButton(text="Anthropic", callback_data="set_provider:anthropic"),
                            types.InlineKeyboardButton(text="Google", callback_data="set_provider:google"),
                        ],
                        [
                            types.InlineKeyboardButton(text="GitHub Copilot", callback_data="set_provider:github"),
                            types.InlineKeyboardButton(text="OpenAI", callback_data="set_provider:openai"),
                        ],
                        [
                            types.InlineKeyboardButton(text="Ollama", callback_data="set_provider:ollama"),
                            types.InlineKeyboardButton(text="LM Studio", callback_data="set_provider:lmstudio"),
                        ]
                    ])
                    await message.answer("Select a provider:", reply_markup=keyboard)
                    return
                elif cmd == "/branch" or cmd == "/checkout":
                    arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
                    if arg:
                        engine = gw._get_engine()
                        if engine:
                            if cmd == "/branch":
                                from cvc.core.models import CVCBranchRequest
                                res = engine.branch(CVCBranchRequest(name=arg))
                            else:
                                res = engine.switch_branch(arg)
                            if res.success:
                                await message.answer(f"✅ Switched to branch '{arg}'")
                            else:
                                await message.answer(f"❌ Failed: {res.message}")
                        else:
                            await message.answer("❌ CVC engine not initialized.")
                    else:
                        branches_list = []
                        if hasattr(gw, "_workspace_mgr") and hasattr(gw._workspace_mgr, "list_branches"):
                            branches_list = gw._workspace_mgr.list_branches()
                        else:
                            branches_data = await gw.ops_branches()
                            branches_list = [b.get("name", "") for b in branches_data.get("branches", [])]
                            
                        if not branches_list:
                            await message.answer("No branches found.")
                            return
                        buttons = []
                        for b in branches_list:
                            name = b if isinstance(b, str) else b.get("name", "")
                            buttons.append([types.InlineKeyboardButton(text=name, callback_data=f"set_branch:{name[:40]}")])
                        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                        await message.answer("Select a branch to checkout:", reply_markup=keyboard)
                    return
                elif cmd == "/branches":
                    branches_list = []
                    if hasattr(gw, "_workspace_mgr") and hasattr(gw._workspace_mgr, "list_branches"):
                        branches_list = gw._workspace_mgr.list_branches()
                    else:
                        branches_data = await gw.ops_branches()
                        branches_list = branches_data.get("branches", [])
                    
                    if not branches_list:
                        await message.answer("No branches found.")
                    else:
                        lines = []
                        for b in branches_list:
                            if isinstance(b, str):
                                lines.append(f"🌿 <code>{b}</code>")
                            else:
                                lines.append(f"🌿 <code>{b.get('name')}</code> ({b.get('head', '')[:8]})")
                        await message.answer("<b>Branches:</b>\n" + "\n".join(lines), parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/commit":
                    engine = gw._get_engine()
                    if engine:
                        arg = cmd_parts[1] if len(cmd_parts) > 1 else "Commit from Telegram"
                        from cvc.core.models import CVCCommitRequest
                        res = engine.commit(CVCCommitRequest(message=arg, context_extras={}))
                        if res.success:
                            await message.answer(f"✅ Committed: <code>{res.commit_hash[:8]}</code> - {arg}", parse_mode=ParseMode.HTML)
                        else:
                            await message.answer(f"❌ Commit failed: {res.message}")
                    else:
                        await message.answer("❌ CVC engine not initialized.")
                    return
                elif cmd == "/log":
                    engine = gw._get_engine()
                    if engine:
                        entries = engine.log(limit=10)
                        if not entries:
                            await message.answer("No commits found.")
                        else:
                            lines = [f"<code>{e['short']}</code> {e['message'][:50]}" for e in entries]
                            await message.answer("📜 <b>Recent Commits</b>\n" + "\n".join(lines), parse_mode=ParseMode.HTML)
                    return
                elif cmd == "/search":
                    arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
                    if not arg:
                        await message.answer("Usage: /search <query>")
                    else:
                        loop = asyncio.get_event_loop()
                        result = await loop.run_in_executor(None, gw._tool_executor.execute, "cvc_search", {"query": arg})
                        await message.answer(f"🔍 <b>Search Results:</b>\n<pre>{str(result)[:3900]}</pre>", parse_mode=ParseMode.HTML)
                    return
                elif cmd in ("/undo", "/compact", "/health", "/retry", "/cost", "/analytics", "/web", "/git", "/image", "/memory"):
                    # Process via LLM
                    pass
                else:
                    await message.answer(f"❌ <i>Unknown command: {cmd}</i>\nType /help for a list of commands.", parse_mode=ParseMode.HTML)
                    return
                
            llm_messages = gw._tg_sessions[session_key]
            
            if message.photo:
                photo_file = await bot.download(message.photo[-1])
                photo_bytes = photo_file.read()
                b64_img = base64.b64encode(photo_bytes).decode("utf-8")
                
                prompt_text = user_text if user_text.strip() else "Examine this image and resolve any issues."
                content = [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]
                llm_messages.append({"role": "user", "content": content})
            else:
                llm_messages.append({"role": "user", "content": user_text})
            
            # Start streaming response
            
            reply_msg = await message.answer("⚙️ <i>Thinking...</i>", parse_mode=ParseMode.HTML)
            streamer = TelegramStreamer(bot, message.chat.id, reply_msg.message_id)
            
            # Run agentic loop
            await run_agentic_loop(bot, message, streamer, llm_messages, gw, session_key)

    @dp.callback_query()
    async def handle_callback(callback: types.CallbackQuery):
        if callback.from_user.id not in settings.telegram.allowlist:
            return
            
        data = callback.data
        msg_id = callback.message.message_id
        
        import cvc.gateway as gw
        
        if data.startswith("set_model:"):
            model = data.split(":", 1)[1]
            if gw._agent_llm:
                gw._agent_llm.model = model
            await callback.message.edit_text(f"✅ Model changed to <b>{model}</b>", parse_mode=ParseMode.HTML)
            await callback.answer(f"Model set to {model}")
            return
            
        if data.startswith("set_provider:"):
            provider = data.split(":", 1)[1]
            if gw._agent_llm:
                gw._agent_llm.provider = provider
            await callback.message.edit_text(f"✅ Provider changed to <b>{provider}</b>", parse_mode=ParseMode.HTML)
            await callback.answer(f"Provider set to {provider}")
            return
            
        if data.startswith("set_branch:"):
            branch = data.split(":", 1)[1]
            engine = gw._get_engine()
            if engine:
                res = engine.switch_branch(branch)
                if res.success:
                    await callback.message.edit_text(f"✅ Switched to branch <b>{branch}</b>", parse_mode=ParseMode.HTML)
                    await callback.answer(f"Checked out {branch}")
                else:
                    await callback.message.edit_text(f"❌ Failed to switch branch: {res.message}", parse_mode=ParseMode.HTML)
                    await callback.answer(f"Failed to checkout {branch}")
            return
            
        if msg_id in pending_approvals:
            approval = pending_approvals[msg_id]
            approval["decision"] = data
            approval["event"].set()
            
            # Edit the message to show decision
            await callback.message.edit_text(
                f"{callback.message.text}\n\n<b>Decision:</b> {data}",
                parse_mode=ParseMode.HTML
            )
            await callback.answer(f"Decision registered: {data}")
        else:
            await callback.answer("This approval request has expired or is invalid.", show_alert=True)

async def run_agentic_loop(bot: Bot, message: types.Message, streamer, llm_messages: list, gw, session_key: str):
    iteration = 0
    max_iterations = getattr(gw, "_MAX_AGENT_ITERATIONS", 50)
    
    try:
        while iteration < max_iterations:
            iteration += 1
            response_text = ""
            tool_calls = []
            tool_call_args_buffer = {}
            gemini_parts = None
            
            temp = 0.7 if iteration == 1 else 0.5
            max_tok = 8192 if iteration == 1 else 16384
            
            async for event in gw._agent_llm.chat_stream(
                messages=llm_messages,
                tools=gw._agent_tools,
                temperature=temp,
                max_tokens=max_tok,
            ):
                if event.type == "text_delta" and event.text:
                    response_text += event.text
                    streamer.push(event.text)
                    
                elif event.type == "tool_call_start" and event.tool_call:
                    tc = event.tool_call
                    tool_calls.append(tc)
                    tool_call_args_buffer[event.tool_call_index] = ""
                    
                elif event.type == "tool_call_delta":
                    idx = event.tool_call_index
                    if idx in tool_call_args_buffer:
                        tool_call_args_buffer[idx] += event.args_delta
                        if tool_calls and idx < len(tool_calls):
                            try:
                                tool_calls[idx].arguments = json.loads(tool_call_args_buffer[idx])
                            except Exception:
                                pass
                                
                elif event.type == "done":
                    if event._provider_meta.get("gemini_parts"):
                        gemini_parts = event._provider_meta["gemini_parts"]

            # Output streaming stops when done with text
            await streamer.finalize()
            
            if not tool_calls:
                if response_text:
                    llm_messages.append({"role": "assistant", "content": response_text})
                break
                
            assistant_msg = {"role": "assistant", "content": response_text or ""}
            if gw._agent_llm.provider in ("openai", "ollama", "lmstudio", "google"):
                assistant_msg["tool_calls"] = [
                    {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)}}
                    for tc in tool_calls
                ]
                if gemini_parts:
                    assistant_msg["_gemini_parts"] = gemini_parts
            elif gw._agent_llm.provider == "anthropic":
                content_blocks = []
                if response_text:
                    content_blocks.append({"type": "text", "text": response_text})
                for tc in tool_calls:
                    content_blocks.append({"type": "tool_use", "id": tc.id, "name": tc.name, "input": tc.arguments})
                assistant_msg = {"role": "assistant", "content": content_blocks}
                
            llm_messages.append(assistant_msg)
            
            for tc in tool_calls:
                # Permission logic
                needs_confirm = (
                    not gw._autopilot
                    and not getattr(gw, "_session_trust_all", False)
                    and tc.name not in getattr(gw, "_SAFE_TOOLS", set())
                    and tc.name not in getattr(gw, "_session_trusted_tools", set())
                )
                
                decision = "allow_once"
                if needs_confirm:
                    # Ask via Inline Keyboard
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                        [
                            types.InlineKeyboardButton(text="✅ Approve", callback_data="allow_once"),
                            types.InlineKeyboardButton(text="✅ Always", callback_data="allow_always"),
                        ],
                        [
                            types.InlineKeyboardButton(text="❌ Deny", callback_data="deny"),
                        ]
                    ])
                    args_disp = json.dumps(tc.arguments, indent=2)[:500]
                    prompt_text = f"⚠️ <b>Tool Execution Requested</b>\n\n<b>Tool:</b> <code>{tc.name}</code>\n<b>Args:</b>\n<code>{args_disp}</code>"
                    
                    req_msg = await message.answer(
                        text=prompt_text,
                        reply_markup=keyboard,
                        parse_mode=ParseMode.HTML
                    )
                    
                    evt = asyncio.Event()
                    pending_approvals[req_msg.message_id] = {"event": evt, "decision": "deny"}
                    
                    try:
                        await asyncio.wait_for(evt.wait(), timeout=120.0)
                    except asyncio.TimeoutError:
                        pass
                        
                    decision = pending_approvals[req_msg.message_id]["decision"]
                    del pending_approvals[req_msg.message_id]
                    
                if decision == "allow_always":
                    gw._session_trusted_tools.add(tc.name)
                elif decision == "deny":
                    result = f"Tool '{tc.name}' was denied by the user via Telegram."
                    llm_messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tc.name,
                        "content": result,
                    })
                    continue

                # Execute tool
                try:
                    if tc.name == "cvc_switch_workspace":
                        result = await gw._execute_workspace_switch(tc.arguments)
                    else:
                        loop = asyncio.get_event_loop()
                        result = await loop.run_in_executor(
                            None, gw._tool_executor.execute, tc.name, tc.arguments
                        )
                except Exception as exc:
                    result = f"Error executing {tc.name}: {exc}"
                    
                max_out = getattr(gw, "_MAX_TOOL_OUTPUT_LLM", 15000)
                llm_result = result[:max_out] if len(result) > max_out else result
                
                llm_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.name,
                    "content": llm_result,
                })

            # Re-initialize streamer for the next turn
            reply_msg = await message.answer("⚙️ <i>Processing...</i>", parse_mode=ParseMode.HTML)
            streamer = TelegramStreamer(bot, message.chat.id, reply_msg.message_id)

    except Exception as exc:
        logger.error(f"Agentic loop error: {exc}", exc_info=True)
        await message.answer(f"<b>Error:</b> {exc}", parse_mode=ParseMode.HTML)
        
    finally:
        await streamer.finalize()
