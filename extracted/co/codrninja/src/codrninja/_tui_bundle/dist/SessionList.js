import React, { useState } from 'react';
import { Box, Text, useInput, useApp } from 'ink';
import { C, LOGO } from './styles.js';
const PROVIDER_ENV = {
    openai: 'OAuth / API Key',
    anthropic: 'OAuth / API Key',
    ollama: 'local server',
    openrouter: 'API Key',
    'claude-cli': 'Claude Code CLI',
};
function relativeTime(iso) {
    if (!iso)
        return '';
    const diff = Date.now() - new Date(iso).getTime();
    const m = Math.floor(diff / 60000);
    if (m < 1)
        return 'just now';
    if (m < 60)
        return `${m}m ago`;
    const h = Math.floor(m / 60);
    if (h < 24)
        return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
}
export function SessionList({ sessions, onSelect, onNew, onDelete, error, version, providers }) {
    const { exit } = useApp();
    const [idx, setIdx] = useState(0);
    const [mode, setMode] = useState('list');
    const [newName, setNewName] = useState('');
    const total = sessions.length;
    useInput((input, key) => {
        if (mode === 'new') {
            if (key.return && newName.trim()) {
                onNew(newName.trim());
                setNewName('');
                setMode('list');
            }
            else if (key.escape) {
                setNewName('');
                setMode('list');
            }
            else if (key.backspace || key.delete) {
                setNewName(p => p.slice(0, -1));
            }
            else if (input && !key.ctrl && !key.meta) {
                setNewName(p => p + input);
            }
            return;
        }
        if (mode === 'delete') {
            if (input === 'y' && sessions[idx]) {
                onDelete?.(sessions[idx].name);
                setIdx(i => Math.max(0, i - 1));
                setMode('list');
            }
            else if (key.escape) {
                setMode('list');
            }
            return;
        }
        if (key.upArrow)
            setIdx(i => Math.max(0, i - 1));
        if (key.downArrow)
            setIdx(i => Math.min(total - 1, i + 1));
        if (key.return && sessions[idx])
            onSelect(sessions[idx].name);
        if (input === 'n')
            setMode('new');
        if (input === 'd' && sessions[idx])
            setMode('delete');
        if (input === 'q')
            exit();
    });
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { color: C.acc }, LOGO),
        version && (React.createElement(Box, { marginTop: 1 },
            React.createElement(Text, { color: C.acc },
                "v",
                version),
            React.createElement(Text, { color: C.dim }, "  codrninja"))),
        React.createElement(Text, { color: C.dim }, '─'.repeat(70)),
        error && React.createElement(Text, { color: C.red },
            " ",
            error),
        React.createElement(Box, { justifyContent: "space-between", marginTop: 1, marginBottom: 1 },
            React.createElement(Text, { color: C.acc, bold: true }, "SESSIONS"),
            React.createElement(Box, { gap: 2 },
                React.createElement(Text, { color: C.dim }, "n "),
                React.createElement(Text, { color: C.acc }, "new"),
                onDelete && React.createElement(React.Fragment, null,
                    React.createElement(Text, { color: C.dim }, "  d "),
                    React.createElement(Text, { color: C.acc }, "delete")))),
        React.createElement(Box, { flexDirection: "column", borderStyle: "single", borderColor: "#2a2a3e" }, sessions.length === 0 ? (React.createElement(Box, { paddingX: 2, paddingY: 1 },
            React.createElement(Text, { color: C.dim }, "No sessions \u2014 press "),
            React.createElement(Text, { color: C.acc }, "n"),
            React.createElement(Text, { color: C.dim }, " to create one"))) : (sessions.map((s, i) => {
            const sel = i === idx && mode !== 'new';
            return (React.createElement(Box, { key: s.name, paddingX: 1 },
                React.createElement(Text, { color: C.acc }, sel ? '▶ ' : '  '),
                React.createElement(Box, { minWidth: 20 },
                    React.createElement(Text, { color: sel ? C.wh : C.txt, bold: sel }, s.name)),
                React.createElement(Box, { minWidth: 12 },
                    React.createElement(Text, { color: C.dim }, relativeTime(s.updated_at))),
                React.createElement(Box, { minWidth: 20 },
                    React.createElement(Text, { color: sel ? C.acc : '#4a4a68' }, s.model ?? '')),
                React.createElement(Text, { color: C.dim }, s.provider ?? '')));
        }))),
        mode === 'delete' && sessions[idx] && (React.createElement(Box, { borderStyle: "single", borderColor: C.red, paddingX: 1, marginTop: 1 },
            React.createElement(Text, { color: C.red }, "Delete "),
            React.createElement(Text, { color: C.acc },
                "'",
                sessions[idx].name,
                "'"),
            React.createElement(Text, { color: C.red }, "?  "),
            React.createElement(Text, { color: C.wh }, "y "),
            React.createElement(Text, { color: C.dim }, "confirm  "),
            React.createElement(Text, { color: C.wh }, "Esc "),
            React.createElement(Text, { color: C.dim }, "cancel"))),
        mode === 'new' && (React.createElement(Box, { borderStyle: "single", borderColor: C.acc, paddingX: 1, marginTop: 1 },
            React.createElement(Text, { color: C.dim }, "session name  \u203A "),
            React.createElement(Text, { color: C.acc }, newName),
            React.createElement(Text, { color: C.acc, bold: true }, "\u258C"))),
        providers && providers.length > 0 && (React.createElement(Box, { flexDirection: "column", marginTop: 1 },
            React.createElement(Text, { color: C.acc, bold: true }, "PROVIDERS"),
            providers.map(p => {
                const connected = p.authenticated || p.oauth;
                return (React.createElement(Box, { key: p.name },
                    React.createElement(Text, { color: connected ? C.grn : '#252535' }, connected ? '● ' : '○ '),
                    React.createElement(Box, { minWidth: 12 },
                        React.createElement(Text, { color: connected ? C.txt : C.dim }, p.name)),
                    React.createElement(Box, { minWidth: 22 },
                        React.createElement(Text, { color: "#252535" }, PROVIDER_ENV[p.name] ?? '')),
                    connected ? (React.createElement(Text, { color: p.active ? C.acc : C.grn }, p.active ? 'active' : 'connected')) : (React.createElement(Text, { color: "#2a2a3e" }, "not configured"))));
            }))),
        React.createElement(Text, { color: C.dim }, '─'.repeat(70)),
        React.createElement(Box, { gap: 3, marginTop: 1 }, [['↑↓', 'navigate'], ['Enter', 'open'], ['n', 'new'], ['d', 'delete'], ['q', 'quit']].map(([k, l]) => (React.createElement(Box, { key: k },
            React.createElement(Text, { color: C.dim },
                k,
                " "),
            React.createElement(Text, { color: C.acc }, l)))))));
}
