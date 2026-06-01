import React, { useEffect, useRef, useState } from 'react';
import { Box, Text, useInput } from 'ink';
import { setActiveProvider, setApiKey, streamOpenAIOAuth, loadOpenAICredentials, fetchOllamaServers, addOllamaServer, removeOllamaServer, toggleOllamaServer, } from './api.js';
// ── shared OAuth browser-waiting screen ──────────────────────────────────────
function OAuthRunning({ providerName, onCancel }) {
    const [dots, setDots] = useState('');
    useEffect(() => {
        const t = setInterval(() => setDots((d) => d.length >= 3 ? '' : d + '.'), 500);
        return () => clearInterval(t);
    }, []);
    useInput((_ch, key) => { if (key.escape)
        onCancel(); });
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" },
            " ",
            providerName,
            " OAuth"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        React.createElement(Text, { color: "yellow" },
            " Browser opened",
            dots),
        React.createElement(Text, { dimColor: true }, " Log in and authorize codrninja in your browser."),
        React.createElement(Text, { dimColor: true }, " Waiting for callback on localhost:8765\u2026"),
        React.createElement(Box, { marginTop: 1 },
            React.createElement(Text, { dimColor: true }, " esc to cancel"))));
}
// ── OpenAI — 3 methods: OAuth (browser) | Credentials | API Key ──────────────
function OpenAIConfig({ onDone, onCancel }) {
    const [screen, setScreen] = useState('method');
    const [methodIdx, setMethodIdx] = useState(0);
    const [apiKey, setApiKey_] = useState('');
    const [error, setError] = useState('');
    const cancelOAuth = useRef(null);
    const METHODS = [
        'OAuth  (browser login)',
        'Credentials  (~/.codrninja/auth.json)',
        'API Key  (paste sk-…)',
    ];
    useEffect(() => () => { cancelOAuth.current?.(); }, []);
    function startOAuth() {
        setScreen('oauth-running');
        setError('');
        const cancel = streamOpenAIOAuth((e) => {
            if (e.type === 'success') {
                setActiveProvider('openai').finally(() => onDone('openai'));
            }
            else if (e.type === 'error') {
                setError(e.error);
                setScreen('method');
            }
        }, () => { });
        cancelOAuth.current = cancel;
    }
    function loadCredentials() {
        setScreen('credentials-loading');
        setError('');
        loadOpenAICredentials()
            .then((res) => {
            if (res.success) {
                setActiveProvider('openai').finally(() => onDone('openai'));
            }
            else {
                setError(res.error ?? 'Failed to load credentials');
                setScreen('method');
            }
        })
            .catch((e) => { setError(String(e)); setScreen('method'); });
    }
    useInput((ch, key) => {
        if (screen === 'oauth-running' || screen === 'credentials-loading')
            return;
        if (key.escape) {
            if (screen === 'method') {
                onCancel();
                return;
            }
            setScreen('method');
            setError('');
            return;
        }
        if (screen === 'method') {
            if (key.upArrow)
                setMethodIdx((i) => Math.max(0, i - 1));
            if (key.downArrow)
                setMethodIdx((i) => Math.min(METHODS.length - 1, i + 1));
            if (key.return) {
                if (methodIdx === 0)
                    startOAuth();
                else if (methodIdx === 1)
                    loadCredentials();
                else
                    setScreen('apikey');
            }
            return;
        }
        if (screen === 'apikey') {
            if (key.return) {
                const k = apiKey.trim();
                if (!k) {
                    setError('API key cannot be empty');
                    return;
                }
                setApiKey('openai', k)
                    .then(() => setActiveProvider('openai'))
                    .then(() => onDone('openai'))
                    .catch((e) => setError(String(e)));
                return;
            }
            if (key.backspace || key.delete)
                setApiKey_((s) => s.slice(0, -1));
            else if (ch && !key.ctrl && !key.meta)
                setApiKey_((s) => s + ch);
        }
    });
    if (screen === 'oauth-running') {
        return React.createElement(OAuthRunning, { providerName: "OpenAI", onCancel: () => { cancelOAuth.current?.(); setScreen('method'); } });
    }
    if (screen === 'credentials-loading') {
        return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
            React.createElement(Text, { bold: true, color: "cyan" }, " OpenAI Credentials"),
            React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
            React.createElement(Text, { color: "yellow" }, " Reading ~/.codrninja/auth.json\u2026")));
    }
    if (screen === 'method') {
        return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
            React.createElement(Text, { bold: true, color: "cyan" }, " Configure OpenAI"),
            React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
            React.createElement(Text, { dimColor: true }, " Choose authentication method:"),
            React.createElement(Box, { flexDirection: "column", marginTop: 1 }, METHODS.map((m, i) => (React.createElement(Box, { key: m },
                React.createElement(Text, { color: i === methodIdx ? 'cyan' : undefined, bold: i === methodIdx },
                    i === methodIdx ? ' ❯ ' : '   ',
                    m))))),
            error && React.createElement(Text, { color: "red" },
                " ",
                error),
            React.createElement(Box, { marginTop: 1 },
                React.createElement(Text, { dimColor: true }, " \u2191\u2193 navigate  enter select  esc cancel"))));
    }
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " OpenAI API Key"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        React.createElement(Text, { dimColor: true }, " Paste your API key (sk-\u2026 or sk-proj-\u2026):"),
        React.createElement(Box, { borderStyle: "round", borderColor: "cyan", marginTop: 1 },
            React.createElement(Text, null,
                " ",
                apiKey.replace(/./g, '•'),
                React.createElement(Text, { color: "cyan" }, "_"))),
        error && React.createElement(Text, { color: "red" },
            " ",
            error),
        React.createElement(Text, { dimColor: true }, " enter save  esc back")));
}
// ── Anthropic — 2 methods: Credentials | API Key ─────────────────────────────
function AnthropicConfig({ onDone, onCancel }) {
    const [apiKey, setApiKey_] = useState('');
    const [error, setError] = useState('');
    useInput((ch, key) => {
        if (key.escape) { onCancel(); return; }
        if (key.return) {
            const k = apiKey.trim();
            if (!k) { setError('API key cannot be empty'); return; }
            setApiKey('anthropic', k)
                .then(() => setActiveProvider('anthropic'))
                .then(() => onDone('anthropic'))
                .catch((e) => setError(String(e)));
            return;
        }
        if (key.backspace || key.delete)
            setApiKey_((s) => s.slice(0, -1));
        else if (ch && !key.ctrl && !key.meta)
            setApiKey_((s) => s + ch);
    });
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " Anthropic API Key"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        React.createElement(Text, { dimColor: true }, " Paste your Anthropic API key (sk-ant-\u2026):"),
        React.createElement(Box, { borderStyle: "round", borderColor: "cyan", marginTop: 1 },
            React.createElement(Text, null,
                " ",
                apiKey.replace(/./g, '\u2022'),
                React.createElement(Text, { color: "cyan" }, "_"))),
        error && React.createElement(Text, { color: "red" },
            " ",
            error),
        React.createElement(Text, { dimColor: true }, " enter save  esc cancel")));
}
// ── Ollama ────────────────────────────────────────────────────────────────────
function OllamaConfig({ onDone, onCancel }) {
    const [step, setStep] = useState('list');
    const [servers, setServers] = useState([]);
    const [serverIdx, setServerIdx] = useState(0);
    const [newUrl, setNewUrl] = useState('http://localhost:11434');
    const [error, setError] = useState('');
    const [loadingServers, setLoadingServers] = useState(true);
    function reload() {
        setLoadingServers(true);
        fetchOllamaServers()
            .then((data) => {
            const list = data?.servers ?? [];
            setServers(list);
            setServerIdx((i) => Math.min(i, Math.max(0, list.length - 1)));
        })
            .catch(() => { })
            .finally(() => setLoadingServers(false));
    }
    useEffect(() => { reload(); }, []);
    useInput((ch, key) => {
        if (key.escape) {
            if (step === 'add-url') {
                setStep('list');
                setError('');
                return;
            }
            onCancel();
            return;
        }
        if (step === 'connecting' || step === 'removing')
            return;
        if (step === 'add-url') {
            if (key.return) {
                const url = newUrl.trim();
                if (!url)
                    return;
                setStep('connecting');
                setError('');
                addOllamaServer(url)
                    .then(() => { reload(); setNewUrl('http://localhost:11434'); setStep('list'); })
                    .catch((e) => { setError(String(e)); setStep('add-url'); });
                return;
            }
            if (key.backspace || key.delete)
                setNewUrl((s) => s.slice(0, -1));
            else if (ch && !key.ctrl && !key.meta)
                setNewUrl((s) => s + ch);
            return;
        }
        // list step
        if (key.upArrow)
            setServerIdx((i) => Math.max(0, i - 1));
        if (key.downArrow)
            setServerIdx((i) => Math.min(servers.length - 1, i + 1));
        if (ch === 'a') {
            setStep('add-url');
            setError('');
            return;
        }
        if (ch === 't' || ch === ' ') {
            const s = servers[serverIdx];
            if (s) {
                toggleOllamaServer(s.url).then(() => reload()).catch(() => { });
            }
            return;
        }
        if (ch === 'd') {
            const s = servers[serverIdx];
            if (s) {
                setStep('removing');
                removeOllamaServer(s.url)
                    .then(() => { reload(); setStep('list'); })
                    .catch(() => setStep('list'));
            }
            return;
        }
        if (key.return) {
            setActiveProvider('ollama').then(() => onDone('ollama')).catch(() => onDone('ollama'));
        }
    });
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " Configure Ollama"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        step === 'connecting' && React.createElement(Text, { color: "yellow" }, " Adding server\u2026"),
        step === 'removing' && React.createElement(Text, { color: "yellow" }, " Removing server\u2026"),
        (step === 'list' || step === 'add-url') && (React.createElement(Box, { flexDirection: "column" },
            loadingServers ? (React.createElement(Text, { dimColor: true }, " Loading servers\u2026")) : servers.length === 0 ? (React.createElement(Text, { dimColor: true }, " No servers configured. Press a to add one.")) : (React.createElement(Box, { flexDirection: "column", marginBottom: 1 }, servers.map((s, i) => {
                const sel = step === 'list' && i === serverIdx;
                const activeLabel = s.active ? React.createElement(Text, { color: "green" }, " [active]") : React.createElement(Text, { dimColor: true }, " [off]");
                const onlineLabel = s.online ? React.createElement(Text, { color: "green" }, " online") : React.createElement(Text, { color: "red" }, " offline");
                return (React.createElement(Box, { key: s.url },
                    React.createElement(Text, { color: sel ? 'cyan' : undefined, bold: sel },
                        sel ? ' ❯ ' : '   ',
                        s.url),
                    activeLabel,
                    onlineLabel,
                    s.online && React.createElement(Text, { dimColor: true },
                        "  ",
                        s.models.length,
                        " model",
                        s.models.length !== 1 ? 's' : '')));
            }))),
            step === 'add-url' && (React.createElement(Box, { flexDirection: "column", marginTop: 1 },
                React.createElement(Text, { dimColor: true }, " New server URL:"),
                React.createElement(Box, { borderStyle: "round", borderColor: "cyan" },
                    React.createElement(Text, null,
                        " ",
                        newUrl,
                        React.createElement(Text, { color: "cyan" }, "_"))),
                error && React.createElement(Text, { color: "red" },
                    " ",
                    error),
                React.createElement(Text, { dimColor: true }, " enter add  esc cancel"))),
            step === 'list' && (React.createElement(Box, { flexDirection: "column", marginTop: 1 },
                error && React.createElement(Text, { color: "red" },
                    " ",
                    error),
                React.createElement(Text, { dimColor: true }, " \u2191\u2193 navigate  t toggle active  d remove  a add  enter confirm")))))));
}
// ── OpenRouter ────────────────────────────────────────────────────────────────
function OpenRouterConfig({ onDone, onCancel }) {
    const [apiKey, setApiKey_] = useState('');
    const [error, setError] = useState('');
    useInput((ch, key) => {
        if (key.escape) {
            onCancel();
            return;
        }
        if (key.return) {
            const k = apiKey.trim();
            if (!k) {
                setError('API key cannot be empty');
                return;
            }
            setApiKey('openrouter', k)
                .then(() => setActiveProvider('openrouter'))
                .then(() => onDone('openrouter'))
                .catch((e) => setError(String(e)));
            return;
        }
        if (key.backspace || key.delete)
            setApiKey_((s) => s.slice(0, -1));
        else if (ch && !key.ctrl && !key.meta)
            setApiKey_((s) => s + ch);
    });
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " Configure OpenRouter"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        React.createElement(Text, { dimColor: true }, " Paste your OpenRouter API key (sk-or-\u2026):"),
        React.createElement(Box, { borderStyle: "round", borderColor: "cyan", marginTop: 1 },
            React.createElement(Text, null,
                " ",
                apiKey.replace(/./g, '•'),
                React.createElement(Text, { color: "cyan" }, "_"))),
        error && React.createElement(Text, { color: "red" },
            " ",
            error),
        React.createElement(Text, { dimColor: true }, " enter to save  esc cancel")));
}
// ── Dispatcher ────────────────────────────────────────────────────────────────
// ── Claude CLI ────────────────────────────────────────────────────────────────
function ClaudeCliConfig({ onDone, onCancel }) {
    const [status, setStatus] = useState('idle');
    const [error, setError] = useState('');
    useEffect(() => {
        setStatus('loading');
        setActiveProvider('claude-cli')
            .then(() => onDone('claude-cli'))
            .catch((e) => {
            setError(String(e));
            setStatus('error');
        });
    }, []);
    useInput((_ch, key) => { if (key.escape)
        onCancel(); });
    if (status === 'error') {
        return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
            React.createElement(Text, { bold: true, color: "red" }, " claude-cli error"),
            React.createElement(Text, { color: "red" },
                " ",
                error),
            React.createElement(Box, { marginTop: 1 },
                React.createElement(Text, { dimColor: true }, " esc to cancel"))));
    }
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " claude-cli"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        React.createElement(Text, { color: "green" }, " Routes requests through your local Claude Code CLI."),
        React.createElement(Text, { dimColor: true }, " Uses your Claude Code subscription \u2014 no API key needed."),
        React.createElement(Box, { marginTop: 1 },
            React.createElement(Text, { dimColor: true }, " Activating\u2026"))));
}
export function ProviderConfig(props) {
    // VERIFIED WORKING — keep claude-cli case here.
    // claude-cli needs no API key or OAuth; ClaudeCliConfig auto-activates via setActiveProvider.
    // Missing this case shows "Unknown provider: claude-cli" error (the default branch).
    switch (props.provider.name) {
        case 'openai': return React.createElement(OpenAIConfig, { ...props });
        case 'anthropic': return React.createElement(AnthropicConfig, { ...props });
        case 'ollama': return React.createElement(OllamaConfig, { ...props });
        case 'openrouter': return React.createElement(OpenRouterConfig, { ...props });
        case 'claude-cli': return React.createElement(ClaudeCliConfig, { ...props });
        default: return React.createElement(Box, { paddingX: 2 },
            React.createElement(Text, { color: "red" },
                "Unknown provider: ",
                props.provider.name));
    }
}
