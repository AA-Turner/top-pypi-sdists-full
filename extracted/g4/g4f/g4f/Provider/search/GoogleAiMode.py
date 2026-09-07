from __future__ import annotations

import asyncio
import urllib.parse

from ...typing import AsyncResult, Messages
from ...requests.cdp import CDPSession
from ... import debug
from ..helper import get_last_user_message
from .GoogleSearch import GoogleSearch


class GoogleAiMode(GoogleSearch):
    label = "Google AI Mode"
    url = "https://google.com"
    working = True
    active_by_default = True
    supports_native_tools = True
    default_model = "ai-mode"
    models = [default_model]

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        **kwargs,
    ) -> AsyncResult:
        query = get_last_user_message(messages)
        search_url = f"{cls.url}/search?q={urllib.parse.quote_plus(query)}"

        debug.log(f"Google Search: Starting CDPSession for query: {query}")
        session = CDPSession(headless=False)
        await session.start()

        try:
            await session.navigate(search_url)
            await session.click_accept_button()
        except Exception as e:
            await session.close()
            raise e

        try:
            await session.wait_for_network_idle(idle_time=1, timeout=10.0)
            search_results = await cls._read_search_results(session)
            if search_results:
                yield search_results
                yield "\n\n---\n\n"
        except Exception as e:
            debug.log(f"Google Search: Error reading search results: {e}")
            await session.close()
            raise e

        try:
            for _ in range(5):
                result = await session.evaluate_js("""const b =Array.from(document.querySelectorAll("a, button")).filter(a=>a.textContent.endsWith("KI‑Modus") || a.textContent.endsWith("AI-Mode")).pop(); b ? b.click() : null; !!b""")
                await asyncio.sleep(1)
                if not result:
                    continue
                await session.wait_for_network_idle(idle_time=1, timeout=10.0)
                results = await session.call("Runtime.evaluate", expression=r"""const cyrb53 = (str, seed = 0) => {
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for(let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1  = Math.imul(h1 ^ (h1 >>> 16), 2246822507);
    h1 ^= Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2  = Math.imul(h2 ^ (h2 >>> 16), 2246822507);
    h2 ^= Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  
    return 4294967296 * (2097151 & h2) + (h1 >>> 0);
};

const result = [];
const rootElement = document.querySelector('[decode-data-ved="1"]');

if (rootElement) {
    for (const nodes of Array.from(rootElement.querySelectorAll('*')).map(e => Array.from(e.childNodes))) {
        for (const node of nodes) { 
            result.push(node); 
        } 
    }
}

const lines = result.map(n => n.textContent ? n.textContent.trim() : "");
const keepLines = { };

for (let l of lines) {
    if (!l) continue;
    if (l.startsWith('TgQPHd')) continue;
    const find = l.indexOf("KI-Antworten können Fehler enthalten.");
    if (find !== -1) {
        l = l.substring(0, find).trim();
        if (l) keepLines[cyrb53(l)] = l;
        break;
    }

    // Regex für das Finden und Extrahieren von _setImageSrc('ID', 'BASE64')
    // Verwendet einfache Anführungszeichen als Begrenzer (wie von Google ausgegeben)
    const imgMatch = l.match(/_setImageSrc\s*\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)/);

    if (imgMatch) {
        // imgMatch[2] ist der Base64-String (data:image/png;base64,...)
        // Dekodiere Hex-Escapes wie \x3d (=) am Ende des Base64-Strings
        const base64Data = imgMatch[2].replace(/\\x([0-9a-fA-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
        // Ersetze nur den _setImageSrc-Aufruf, behalte umgebenden Text
        l = l.replace(imgMatch[0], ''); // `\n![Bild](${base64Data})`);
    }

    // Behebt den fehlerhaften Regex für die Datei-Metadaten am Zeilenende
    const fileMatch = l.match(/\\\{.+\\}/);
    if (fileMatch) {
        l = l.replace(fileMatch[0], '');
    }

    const hash = cyrb53(l);
    keepLines[hash] = l;
}
Object.values(keepLines);
""", returnByValue=True);
                debug.log(f"Google Search: AI mode results: {results}")
                if results:
                    for text in results.get("result", {}).get("value", []):
                        yield f"{text}\n"
                    return
            raise RuntimeError("No AI mode results found.")
        finally:
            await session.close()
