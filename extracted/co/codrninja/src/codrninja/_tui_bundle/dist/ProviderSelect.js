import React, { useEffect, useState } from 'react';
import { Box, Text, useInput } from 'ink';
import { fetchProviders } from './api.js';
const PROVIDER_LABELS = {
    'openai': 'OpenAI  (GPT-4, o1, Codex)',
    'anthropic': 'Anthropic  (Claude)',
    'ollama': 'Ollama  (local models)',
    'openrouter': 'OpenRouter  (100+ models)',
    'claude-cli': 'Claude Code CLI  (no API key needed)',
};
export function ProviderSelect({ onSelect, onCancel }) {
    const [providers, setProviders] = useState([]);
    const [idx, setIdx] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    useEffect(() => {
        fetchProviders()
            .then((d) => setProviders(d.providers))
            .catch((e) => setError(String(e)))
            .finally(() => setLoading(false));
    }, []);
    useInput((_ch, key) => {
        if (key.escape) {
            onCancel();
            return;
        }
        if (key.upArrow)
            setIdx((i) => Math.max(0, i - 1));
        if (key.downArrow)
            setIdx((i) => Math.min(providers.length - 1, i + 1));
        if (key.return && providers[idx])
            onSelect(providers[idx]);
    });
    if (loading)
        return React.createElement(Box, { paddingX: 2 },
            React.createElement(Text, { dimColor: true }, "Loading providers\u2026"));
    if (error)
        return React.createElement(Box, { paddingX: 2 },
            React.createElement(Text, { color: "red" }, error));
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " Select provider"),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        providers.map((p, i) => {
            const selected = i === idx;
            const authBadge = p.active
                ? React.createElement(Text, { color: "cyan" }, " \u2190 active")
                : p.oauth
                    ? React.createElement(Text, { color: "green" }, "  oauth")
                    : p.authenticated
                        ? React.createElement(Text, { color: "green" }, "  \u2713")
                        : React.createElement(Text, { color: "yellow" }, "  not configured");
            return (React.createElement(Box, { key: p.name },
                React.createElement(Text, { color: selected ? 'cyan' : undefined, bold: selected },
                    selected ? ' ❯ ' : '   ',
                    (PROVIDER_LABELS[p.name] ?? p.name).padEnd(38)),
                authBadge));
        }),
        React.createElement(Box, { marginTop: 1 },
            React.createElement(Text, { dimColor: true }, " \u2191\u2193 navigate  enter configure  esc cancel"))));
}
