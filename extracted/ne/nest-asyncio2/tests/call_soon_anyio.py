# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anyio~=4.0",
#     "nest-asyncio2",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///

'''Without handling call_soon(), hangs after printing — AnyIO worker threads are never stopped.'''
import asyncio
import threading
import anyio

async def use_worker_thread():
    await anyio.to_thread.run_sync(lambda: None)

def main():
    # Step 1: trigger nest_asyncio.apply() from a nested context
    async def inner():
        import nest_asyncio2
        nest_asyncio2.apply()
        asyncio.run(use_worker_thread())  # nested, uses patched run

    asyncio.run(inner())

    # Step 2: call asyncio.run() again (now globally patched)
    # Done callbacks (worker.stop) are scheduled but never processed
    asyncio.run(use_worker_thread())

    print('Threads (should be just MainThread):')
    for t in threading.enumerate():
        print(f"  {t.name} daemon={t.daemon}")

    print('main() done — without handling call_soon(), interpreter will now hang')

if __name__ == "__main__":
    main()
