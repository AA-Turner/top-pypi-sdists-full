const BASE = process.env['CODRNINJA_SERVER'] ?? 'http://127.0.0.1:7384';
export async function fetchSessions() {
    const r = await fetch(`${BASE}/sessions`);
    const data = await r.json();
    return data.sessions;
}
export async function fetchSession(name) {
    const r = await fetch(`${BASE}/sessions/${encodeURIComponent(name)}`);
    if (!r.ok)
        throw new Error(`Session not found: ${name}`);
    return r.json();
}
export async function deleteSession(name) {
    await fetch(`${BASE}/sessions/${encodeURIComponent(name)}`, { method: 'DELETE' });
}
export async function fetchVersion() {
    try {
        const r = await fetch(`${BASE}/version`);
        const d = await r.json();
        return d.version;
    }
    catch {
        return '';
    }
}
export async function createSession(name) {
    const r = await fetch(`${BASE}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
    });
    return r.json();
}
export async function fetchConfig() {
    const r = await fetch(`${BASE}/config`);
    return r.json();
}
export async function fetchProviders() {
    const r = await fetch(`${BASE}/providers`);
    return r.json();
}
export async function setActiveProvider(provider) {
    const r = await fetch(`${BASE}/config/provider`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider }),
    });
    return r.json();
}
export async function setApiKey(provider, api_key) {
    const r = await fetch(`${BASE}/providers/${encodeURIComponent(provider)}/apikey`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key }),
    });
    return r.json();
}
export async function configureOllama(url) {
    const r = await fetch(`${BASE}/providers/ollama/configure`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });
    if (!r.ok) {
        const err = await r.json();
        throw new Error(err.detail ?? 'Failed');
    }
    return r.json();
}
function streamOAuth(endpoint, onEvent, onDone) {
    const ctrl = new AbortController();
    fetch(`${BASE}${endpoint}`, {
        method: 'POST', signal: ctrl.signal,
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
    }).then(async (res) => {
        if (!res.body) {
            onDone();
            return;
        }
        const reader = res.body.getReader();
        const dec = new TextDecoder();
        let buf = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done)
                break;
            buf += dec.decode(value, { stream: true });
            const lines = buf.split('\n');
            buf = lines.pop() ?? '';
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        onEvent(JSON.parse(line.slice(6)));
                    }
                    catch { /* ignore */ }
                }
                else if (line.startsWith('event: done')) {
                    onDone();
                    return;
                }
            }
        }
        onDone();
    }).catch((e) => {
        if (e instanceof Error && e.name !== 'AbortError')
            onDone();
    });
    return () => ctrl.abort();
}
export function streamOpenAIOAuth(onEvent, onDone) {
    return streamOAuth('/providers/openai/oauth', onEvent, onDone);
}
export async function loadOpenAICredentials() {
    const r = await fetch(`${BASE}/providers/openai/credentials`, { method: 'POST' });
    return r.json();
}
export async function fetchModels() {
    const r = await fetch(`${BASE}/models`);
    return r.json();
}
export async function setModel(model, provider) {
    const r = await fetch(`${BASE}/config/model`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, provider }),
    });
    return r.json();
}
export async function setSessionModel(sessionName, model, provider, setAsDefault = false) {
    const r = await fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/model`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, provider, set_as_default: setAsDefault }),
    });
    return r.json();
}
export async function fetchOllamaServers() {
    const r = await fetch(`${BASE}/providers/ollama/servers`);
    return r.json();
}
export async function addOllamaServer(url) {
    const r = await fetch(`${BASE}/providers/ollama/add-server`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });
    if (!r.ok) {
        const e = await r.json();
        throw new Error(e.detail ?? 'Failed');
    }
    return r.json();
}
export async function removeOllamaServer(url) {
    const r = await fetch(`${BASE}/providers/ollama/remove-server`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });
    return r.json();
}
export async function toggleOllamaServer(url) {
    const r = await fetch(`${BASE}/providers/ollama/toggle-server`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });
    return r.json();
}
export async function runExec(command) {
    const r = await fetch(`${BASE}/run/exec`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
    });
    return r.json();
}
export async function runSearch(query) {
    const r = await fetch(`${BASE}/run/search`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
    });
    return r.json();
}
export async function runFetch(url) {
    const r = await fetch(`${BASE}/run/fetch`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });
    return r.json();
}
export async function runCommit(message) {
    const r = await fetch(`${BASE}/run/commit`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
    });
    return r.json();
}
export async function runTest(command = 'pytest -q') {
    const r = await fetch(`${BASE}/run/test`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
    });
    return r.json();
}
export function streamAgent(sessionName, message, onEvent, onDone, onError, mode = 'build') {
    const controller = new AbortController();
    fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, auto_approve: true, mode }),
        signal: controller.signal,
    })
        .then(async (res) => {
        if (!res.ok || !res.body) {
            onError(new Error(`HTTP ${res.status}`));
            return;
        }
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buf = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done)
                break;
            buf += decoder.decode(value, { stream: true });
            const lines = buf.split('\n');
            buf = lines.pop() ?? '';
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const raw = line.slice(6).trim();
                    if (raw) {
                        try {
                            onEvent(JSON.parse(raw));
                        }
                        catch { /* ignore malformed */ }
                    }
                }
                else if (line.startsWith('event: done')) {
                    onDone();
                    return;
                }
            }
        }
        onDone();
    })
        .catch((err) => {
        if (err instanceof Error && err.name !== 'AbortError')
            onError(err);
    });
    return () => controller.abort();
}
