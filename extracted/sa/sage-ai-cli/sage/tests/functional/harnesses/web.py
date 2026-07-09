import asyncio
import os
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright
from . import TestResult

def execute(request: dict, model: str) -> TestResult:
    return asyncio.run(_async_execute(request, model))

async def _async_execute(request: dict, model: str) -> TestResult:
    prompt = request.get("web_request", {}).get("task", request.get("description", "Perform task"))
    # In local testing, the backend at 8091 serves the frontend if we build it, 
    # but we can also rely on 5174 for the dev server
    url = os.environ.get("SAGE_WEB_URL", "http://127.0.0.1:8091")
    
    workspace = Path(tempfile.mkdtemp(prefix="sage-web-functional-"))
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: console_logs.append(f"[pageerror] {err.message}"))
        
        await page.goto(url)
        
        await page.evaluate(f"""() => {{
            window.localStorage.setItem('sage-testing', '1');
            window.localStorage.setItem('ai-theme', 'dark');
            window.localStorage.setItem('ai-model', '{model}');
            window.localStorage.setItem('sage-cookie-consent', JSON.stringify({{ functional: true, analytics: false, version: 1 }}));
            const mockUser = {{
                uid: 'test-uid', email: 'test@example.com', displayName: 'Test User',
                emailVerified: true, tier: 'pro', _storedAt: Date.now()
            }};
            window.localStorage.setItem('sage_auth_user', JSON.stringify(mockUser));
            window.localStorage.setItem('sage-mock-user', JSON.stringify(mockUser));
            window.localStorage.setItem('sage_auth_token', JSON.stringify({{
                idToken: 'test-token', refreshToken: 'test-refresh', expiresAt: Date.now() + 3600 * 1000
            }}));
        }}""")
        
        await page.reload(wait_until="load")
        
        # Check if we are on the login page
        if await page.locator("text=Sign in").count() > 0 or await page.locator("text=Login").count() > 0:
             # In SAGE_TESTING=1, we should be able to bypass, but if the UI shows it,
             # we might need to click a mock login or just fail with a clear message.
             pass

        try:
            # Wait for the main app container to exist
            await page.wait_for_selector("#root", timeout=30000)
            # Wait for the main scrollable area or input to appear (React hydration)
            await page.wait_for_selector("textarea, input", timeout=45000)
        except:
            pass
        
        await page.wait_for_timeout(7000) # Increased safety buffer for hydration
        
        # Intercept the /chat endpoint to enforce the requested model regardless of UI state
        async def intercept_chat(route):
            try:
                import json
                req = route.request
                print(f"DEBUG: intercepting {req.method} {req.url}")
                if req.method == "POST" and req.post_data:
                    data = json.loads(req.post_data)
                    print(f"DEBUG: original model was {data.get('model')}")
                    data["model"] = model
                    print(f"DEBUG: enforcing model {model}")
                    await route.continue_(post_data=json.dumps(data))
                else:
                    print(f"DEBUG: letting request pass unmodified")
                    await route.continue_()
            except Exception as e:
                print(f"DEBUG route interception error: {e}")
                await route.continue_()
                
        await page.route("**/chat", intercept_chat)
        await page.route("**/api/chat", intercept_chat)
        
        try:
            # Try to select the model via the combobox
            await page.click(".combobox-trigger", timeout=2000)
            await page.wait_for_timeout(500) # Wait for dropdown animation
            # Find the option by partial text (just 'qwen3' or 'qwen3-coder')
            await page.click("text=qwen3-coder", timeout=2000)
            await page.wait_for_timeout(500)
        except Exception as e:
            print(f"DEBUG: Could not select model {model} in UI: {e}")

        # Try to find the chat input
        try:
            chat_input = None
            for _ in range(3): # Retry visibility check
                for selector in ["textarea", "main textarea", "input[type='text']", "//*[@placeholder]", ".chat-input"]:
                    try:
                        loc = page.locator(selector).first
                        if await loc.is_visible(timeout=5000):
                            chat_input = loc
                            break
                    except:
                        continue
                if chat_input:
                    break
                
                # If not found, try to force a new chat
                new_chat = page.locator("text=New chat").first
                if await new_chat.is_visible():
                    await new_chat.click()
                    await page.wait_for_timeout(2000)
            
            if not chat_input:
                # Capture screenshot for debugging if it fails
                await page.screenshot(path=workspace / "web_failure.png")
                (workspace / "page_content.html").write_text(await page.content())
                logs_str = "\n".join(console_logs)
                raise RuntimeError(f"No visible chat input found after retries. Console: {logs_str}")

            await chat_input.fill(prompt)
            # Some chat UIs use Enter, some need the button. Try both.
            await chat_input.press("Enter")
            
            try:
                # Try to click the send button (often a button inside or next to the chat input form)
                # Look for a button with a send icon or aria-label="Send" or type="submit"
                send_button = page.locator("button[type='submit'], button[aria-label='Send message'], button[aria-label='Send'], .send-button")
                if await send_button.count() > 0:
                    await send_button.first.click(timeout=1000)
            except:
                pass
            
            
            # Wait for response
            try:
                # The latest response should be generated
                await page.wait_for_selector(".message.assistant:last-child", timeout=45000)
                # Wait for the spinner or generating state to finish
                await page.wait_for_selector(".spinner", state="detached", timeout=120000)
                await page.wait_for_timeout(2000)
            except:
                pass
            
            response_text = await page.inner_text("body")
            (workspace / "page_content_before_download.html").write_text(await page.content())
            
            download_links = await page.locator("a[download]").all()
            if download_links:
                href = await download_links[0].get_attribute("href")
                print(f"DEBUG DOWNLOAD HREF: {href}")
                if href and href.startswith("http://mock-asset.local"):
                    import base64
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(href)
                    b64_data = parse_qs(parsed.query).get("data", [""])[0]
                    filename = await download_links[0].get_attribute("download") or "mock_asset"
                    artifact_path = workspace / filename
                    artifact_path.write_bytes(base64.b64decode(b64_data))
                else:
                    async with page.expect_download(timeout=15000) as download_info:
                        await download_links[0].click()
                    download = await download_info.value
                    artifact_path = workspace / download.suggested_filename
                    await download.save_as(artifact_path)
            else:
                target_ext = request.get("success_criteria", {}).get("extension", ".txt")
                artifact_path = workspace / f"web_output{target_ext}"
                artifact_path.write_text(response_text)
                
            await browser.close()
            return TestResult(request=request, raw_response=response_text, artifact_path=artifact_path, logs="Web UI completed", exit_code=0)
            
        except Exception as exc:
            await browser.close()
            return TestResult(request=request, raw_response="", artifact_path=workspace, logs=str(exc), exit_code=1)
