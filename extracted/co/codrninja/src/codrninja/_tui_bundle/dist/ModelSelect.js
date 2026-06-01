import React, { useEffect, useState } from 'react';
import { Box, Text, useInput } from 'ink';
import { fetchModels, setModel, setSessionModel } from './api.js';
const SCOPE_OPTIONS = ['This session only', 'Set as global default'];
// Ollama multi-server format: "display (host)|actual_model_value"
function modelDisplay(m) { const i = m.indexOf('|'); return i >= 0 ? m.slice(0, i).trim() : m; }
function modelValue(m) { const i = m.indexOf('|'); return i >= 0 ? m.slice(i + 1) : m; }
export function ModelSelect({ currentModel, currentProvider, sessionName, onSelect, onCancel }) {
    const [models, setModels] = useState([]);
    const [idx, setIdx] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [filter, setFilter] = useState('');
    const [screen, setScreen] = useState('list');
    const [pending, setPending] = useState('');
    const [scopeIdx, setScopeIdx] = useState(0);
    const [saving, setSaving] = useState(false);
    useEffect(() => {
        fetchModels()
            .then((data) => {
            setModels(data.models);
            // models may be "display (host)|value" for multi-server Ollama
            const cur = data.models.findIndex((m) => modelValue(m) === currentModel || m === currentModel);
            if (cur >= 0)
                setIdx(cur);
        })
            .catch((e) => setError(String(e)))
            .finally(() => setLoading(false));
    }, [currentModel]);
    const filtered = models.filter((m) => filter ? modelDisplay(m).toLowerCase().includes(filter.toLowerCase()) : true);
    function confirmModel(raw, asDefault) {
        const value = modelValue(raw);
        setSaving(true);
        if (sessionName) {
            setSessionModel(sessionName, value, undefined, asDefault)
                .then((res) => onSelect(res.model, res.provider))
                .catch(() => onSelect(value, currentProvider));
        }
        else {
            setModel(value)
                .then((res) => onSelect(res.model, res.provider))
                .catch(() => onSelect(value, currentProvider));
        }
    }
    useInput((ch, key) => {
        if (saving)
            return;
        if (screen === 'scope') {
            if (key.escape) {
                setScreen('list');
                return;
            }
            if (key.upArrow)
                setScopeIdx((i) => Math.max(0, i - 1));
            if (key.downArrow)
                setScopeIdx((i) => Math.min(SCOPE_OPTIONS.length - 1, i + 1));
            if (key.return) {
                confirmModel(pending, scopeIdx === 1);
            }
            return;
        }
        // list screen
        if (key.escape) {
            onCancel();
            return;
        }
        if (key.upArrow) {
            setIdx((i) => Math.max(0, i - 1));
            return;
        }
        if (key.downArrow) {
            setIdx((i) => Math.min(filtered.length - 1, i + 1));
            return;
        }
        if (key.return) {
            const chosen = filtered[idx];
            if (chosen) {
                if (sessionName) {
                    setPending(chosen);
                    setScopeIdx(0);
                    setScreen('scope');
                }
                else {
                    confirmModel(chosen, false);
                }
            }
            return;
        }
        if (key.backspace || key.delete) {
            setFilter((f) => f.slice(0, -1));
            setIdx(0);
        }
        else if (ch && !key.ctrl && !key.meta) {
            setFilter((f) => f + ch);
            setIdx(0);
        }
    });
    if (loading) {
        return (React.createElement(Box, { paddingX: 2 },
            React.createElement(Text, { dimColor: true }, "Loading models\u2026")));
    }
    if (error) {
        return (React.createElement(Box, { flexDirection: "column", paddingX: 2 },
            React.createElement(Text, { color: "red" },
                "Could not load models: ",
                error),
            React.createElement(Text, { dimColor: true }, "esc to go back")));
    }
    if (screen === 'scope') {
        return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
            React.createElement(Text, { bold: true, color: "cyan" }, " Apply model change"),
            React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
            React.createElement(Text, { dimColor: true },
                " Selected: ",
                React.createElement(Text, { color: "white" }, modelDisplay(pending))),
            React.createElement(Box, { flexDirection: "column", marginTop: 1 }, SCOPE_OPTIONS.map((opt, i) => (React.createElement(Box, { key: opt },
                React.createElement(Text, { color: i === scopeIdx ? 'cyan' : undefined, bold: i === scopeIdx },
                    i === scopeIdx ? ' ❯ ' : '   ',
                    opt))))),
            React.createElement(Box, { marginTop: 1 },
                React.createElement(Text, { dimColor: true }, " \u2191\u2193 navigate  enter confirm  esc back"))));
    }
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2, paddingY: 1 },
        React.createElement(Text, { bold: true, color: "cyan" }, " Select model"),
        React.createElement(Text, { dimColor: true },
            " Current: ",
            currentModel,
            "  (",
            currentProvider,
            ")"),
        sessionName && React.createElement(Text, { dimColor: true },
            " Session: ",
            sessionName),
        React.createElement(Text, { dimColor: true }, " \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"),
        React.createElement(Box, { marginBottom: 1 },
            React.createElement(Text, { color: "cyan" }, " Filter: "),
            React.createElement(Text, null,
                filter,
                React.createElement(Text, { color: "cyan" }, "_"))),
        filtered.length === 0 && (React.createElement(Text, { dimColor: true }, " No models match.")),
        filtered.slice(0, 16).map((m, i) => {
            const selected = i === idx;
            const isCurrent = modelValue(m) === currentModel || m === currentModel;
            return (React.createElement(Box, { key: m },
                React.createElement(Text, { color: selected ? 'cyan' : undefined, bold: selected },
                    selected ? ' ❯ ' : '   ',
                    modelDisplay(m)),
                isCurrent && React.createElement(Text, { dimColor: true }, "  \u2190 current")));
        }),
        filtered.length > 16 && (React.createElement(Text, { dimColor: true },
            "  \u2026 ",
            filtered.length - 16,
            " more (type to filter)")),
        React.createElement(Box, { marginTop: 1 },
            React.createElement(Text, { dimColor: true }, " \u2191\u2193 navigate  enter select  type to filter  esc cancel"))));
}
