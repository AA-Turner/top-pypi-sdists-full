import React, { useRef, useState } from 'react';
import { Box, Text, useInput } from 'ink';
import { runCommit, runExec, runFetch, runSearch, runTest, streamAgent, } from './api.js';
import { ThinkingIndicator } from './ThinkingIndicator.js';
import { ToolCallLine } from './ToolCallLine.js';
import { Markdown } from './Markdown.js';
import { C, LOGO } from './styles.js';
const SLASH_COMMANDS = {
    '/help': { description: 'Show available commands' },
    '/new': { description: 'Go back to session list / create new session' },
    '/clear': { description: 'Clear the current conversation' },
    '/compact': { description: 'Summarize and compact the conversation' },
    '/fork': { description: 'Duplicate this session under a new name' },
    '/undo': { description: 'Remove the last message pair' },
    '/session': { description: 'Show session info' },
    '/sessions': { description: 'Go back to session list', aliases: ['/resume', '/continue'] },
    '/status': { description: 'Show provider / model / session status' },
    '/model': { description: 'Show or change the current model' },
    '/provider': { description: 'Show current provider' },
    '/connect': { description: 'Show how to connect / configure a provider' },
    '/build': { description: 'Run build agent on a task' },
    '/plan': { description: 'Run plan agent on a task' },
    '/agent': { description: 'Show current agent mode (build / plan)' },
    '/exec': { description: 'Execute a shell command' },
    '/terminal': { description: 'Execute a shell command', aliases: ['/exec'] },
    '/diff': { description: 'Show current git diff' },
    '/commit': { description: 'Git add -A and commit with a message' },
    '/search': { description: 'Search the web' },
    '/fetch': { description: 'Fetch and read a web page' },
    '/open': { description: 'Read a file and show its contents' },
    '/test': { description: 'Run tests (default: pytest -q)' },
    '/todo': { description: 'Manage todos (powered by agent)' },
    '/skills': { description: 'List available agent skills' },
    '/mcp': { description: 'Show connected MCP servers' },
    '/warp': { description: 'Change working directory for this session' },
    '/share': { description: 'Print a shareable session summary' },
    '/themes': { description: 'Toggle light/dark color hint' },
    '/exit': { description: 'Exit codrninja', aliases: ['/quit', '/q'] },
};
// sorted A-Z
const CMD_NAMES = Object.keys(SLASH_COMMANDS).sort();
const COMPLETION_WINDOW = 12;
export function ChatView({ sessionName, history, onBack, onOpenModelSelect, onOpenProviderSelect, provider, model }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [thinking, setThinking] = useState(false);
    const [statusLine, setStatusLine] = useState('');
    const [inputHistory, setInputHistory] = useState(() => history
        .filter((m) => m.role === 'user' && !m.content.startsWith('Working directory:'))
        .map((m) => m.content)
        .reverse());
    const [historyIdx, setHistoryIdx] = useState(-1);
    const [completionIdx, setCompletionIdx] = useState(0);
    const [completionScrollTop, setCompletionScrollTop] = useState(0);
    const cancelRef = useRef(null);
    const thinkingStart = useRef(0);
    const lastThinkingPast = useRef('Thought');
    // show completions only when actively typing a '/' command (not navigating history)
    const firstWord = input.split(' ')[0] ?? '';
    const showCompletions = historyIdx === -1 &&
        input.startsWith('/') &&
        !input.includes(' ') &&
        firstWord.length > 0;
    const completions = showCompletions
        ? CMD_NAMES.filter((c) => c.startsWith(firstWord))
        : [];
    // hide thinking indicator once AI has started streaming text
    const lastMsg = messages[messages.length - 1];
    const aiIsStreaming = lastMsg?.role === 'assistant' && lastMsg.streaming === true && (lastMsg.content?.length ?? 0) > 0;
    useInput((ch, key) => {
        if (thinking) {
            if (key.escape && cancelRef.current) {
                cancelRef.current();
                cancelRef.current = null;
                setThinking(false);
                setStatusLine('Cancelled.');
            }
            return;
        }
        if (key.escape) {
            onBack();
            return;
        }
        // ── up/down: navigate slash popup when open, else input history ──
        if (key.upArrow) {
            if (showCompletions && completions.length > 0) {
                const newIdx = Math.max(0, completionIdx - 1);
                setCompletionIdx(newIdx);
                setCompletionScrollTop(top => newIdx < top ? top - 1 : top);
            }
            else {
                const newIdx = Math.min(historyIdx + 1, inputHistory.length - 1);
                if (newIdx >= 0 && newIdx !== historyIdx) {
                    setHistoryIdx(newIdx);
                    setInput(inputHistory[newIdx] ?? '');
                }
            }
            return;
        }
        if (key.downArrow) {
            if (showCompletions && completions.length > 0) {
                const newIdx = Math.min(completions.length - 1, completionIdx + 1);
                setCompletionIdx(newIdx);
                setCompletionScrollTop(top => newIdx >= top + COMPLETION_WINDOW ? top + 1 : top);
            }
            else if (historyIdx > 0) {
                const newIdx = historyIdx - 1;
                setHistoryIdx(newIdx);
                setInput(inputHistory[newIdx] ?? '');
            }
            else if (historyIdx === 0) {
                setHistoryIdx(-1);
                setInput('');
            }
            return;
        }
        // ── tab or enter on completion selects it ──
        if (key.tab && completions.length > 0) {
            const chosen = completions[completionIdx] ?? completions[0];
            if (chosen) {
                setInput(chosen + ' ');
                setHistoryIdx(-1);
                setCompletionIdx(0);
                setCompletionScrollTop(0);
            }
            return;
        }
        if (key.return) {
            // if popup open and user pressed enter, select the highlighted completion
            if (showCompletions && completions.length > 0 && input === (completions[completionIdx] ?? '')) {
                setInput(input + ' ');
                setCompletionIdx(0);
                setCompletionScrollTop(0);
                return;
            }
            const text = input.trim();
            if (!text)
                return;
            setInputHistory((h) => (h[0] === text ? h : [text, ...h].slice(0, 100)));
            setHistoryIdx(-1);
            setCompletionIdx(0);
            setCompletionScrollTop(0);
            setInput('');
            setStatusLine('');
            if (text.startsWith('/'))
                handleSlash(text);
            else
                submit(text, 'build');
            return;
        }
        if (key.backspace || key.delete) {
            setInput((s) => s.slice(0, -1));
            setHistoryIdx(-1);
            setCompletionIdx(0);
            setCompletionScrollTop(0);
        }
        else if (ch && !key.ctrl && !key.meta) {
            setInput((s) => s + ch);
            setHistoryIdx(-1);
            setCompletionIdx(0);
            setCompletionScrollTop(0);
        }
    });
    // ── helpers ────────────────────────────────────────────────────────────────
    function addSystem(text) {
        setMessages((m) => [...m, { role: 'assistant', content: text }]);
    }
    // ── slash dispatcher ───────────────────────────────────────────────────────
    function handleSlash(raw) {
        const parts = raw.trim().split(/\s+/);
        const cmd = parts[0].toLowerCase();
        const args = parts.slice(1);
        // resolve aliases
        const canonical = CMD_NAMES.find((c) => c === cmd || (SLASH_COMMANDS[c]?.aliases ?? []).includes(cmd)) ?? cmd;
        switch (canonical) {
            case '/exit':
                process.exit(0);
                return;
            case '/clear':
                setMessages([]);
                return;
            case '/new':
            case '/sessions':
                onBack();
                return;
            case '/undo':
                setMessages((m) => {
                    // remove last user+assistant pair
                    const copy = [...m];
                    if (copy.length >= 2)
                        copy.splice(-2, 2);
                    else
                        copy.pop();
                    return copy;
                });
                return;
            case '/compact':
                submit('Please summarize our conversation so far in a compact form, then continue from here.', 'build');
                return;
            case '/fork':
                addSystem(`Fork: open a new terminal and run: codrninja ${sessionName}-fork`);
                return;
            case '/help': {
                const lines = CMD_NAMES.map((c) => `${c.padEnd(14)} ${SLASH_COMMANDS[c]?.description ?? ''}`).join('\n');
                addSystem(lines);
                return;
            }
            case '/status':
            case '/session':
                addSystem(`Session:  ${sessionName}\nProvider: ${provider}\nModel:    ${model}`);
                return;
            case '/model':
            case '/models':
                onOpenModelSelect();
                return;
            case '/provider':
            case '/connect':
                onOpenProviderSelect();
                return;
            case '/agent':
                addSystem(`Current agent modes: /build (implement), /plan (design only)`);
                return;
            case '/build':
                if (!args.length) {
                    setStatusLine('Usage: /build <task>');
                    return;
                }
                submit(args.join(' '), 'build');
                return;
            case '/plan':
                if (!args.length) {
                    setStatusLine('Usage: /plan <task>');
                    return;
                }
                submit(args.join(' '), 'plan');
                return;
            case '/exec':
            case '/terminal':
                if (!args.length) {
                    setStatusLine('Usage: /exec <command>');
                    return;
                }
                runSlashExec(args.join(' '));
                return;
            case '/diff':
                runSlashExec('git diff HEAD');
                return;
            case '/commit':
                if (!args.length) {
                    setStatusLine('Usage: /commit <message>');
                    return;
                }
                runSlashCommit(args.join(' '));
                return;
            case '/search':
                if (!args.length) {
                    setStatusLine('Usage: /search <query>');
                    return;
                }
                runSlashSearch(args.join(' '));
                return;
            case '/fetch':
                if (!args.length) {
                    setStatusLine('Usage: /fetch <url>');
                    return;
                }
                runSlashFetch(args[0]);
                return;
            case '/open':
                if (!args.length) {
                    setStatusLine('Usage: /open <file>');
                    return;
                }
                runSlashExec(`cat ${args[0]}`);
                return;
            case '/test':
                runSlashTest(args.length ? args.join(' ') : undefined);
                return;
            case '/todo':
                submit('Show and manage my todos for this session.', 'build');
                return;
            case '/skills':
                runSlashExec('codrninja skills');
                return;
            case '/mcp':
                runSlashExec('codrninja mcp list');
                return;
            case '/warp':
                if (!args.length) {
                    setStatusLine('Usage: /warp <directory>');
                    return;
                }
                runSlashExec(`cd ${args[0]} && pwd`);
                return;
            case '/share':
                addSystem(`Session: ${sessionName}\nMessages: ${messages.length}\nProvider: ${provider} / ${model}`);
                return;
            case '/themes':
                addSystem("Theme switching: set TERM_PROGRAM or use your terminal's theme.");
                return;
            default:
                setStatusLine(`Unknown command: ${cmd}  — type /help`);
        }
    }
    // ── REST slash runners ─────────────────────────────────────────────────────
    async function runSlashExec(command) {
        setThinking(true);
        addSystem(`$ ${command}`);
        const res = await runExec(command).catch((e) => ({ success: false, output: '', error: String(e) }));
        setThinking(false);
        addSystem(res.success ? (res.output ?? '(no output)') : `Error: ${res.error}`);
    }
    async function runSlashSearch(query) {
        setThinking(true);
        const res = await runSearch(query).catch((e) => ({ success: false, output: '', error: String(e) }));
        setThinking(false);
        addSystem(res.success ? (res.output ?? '') : `Error: ${res.error}`);
    }
    async function runSlashFetch(url) {
        setThinking(true);
        const res = await runFetch(url).catch((e) => ({ success: false, output: '', error: String(e) }));
        setThinking(false);
        addSystem(res.success ? (res.output ?? '') : `Error: ${res.error}`);
    }
    async function runSlashTest(command) {
        setThinking(true);
        const res = await runTest(command).catch((e) => ({ success: false, output: '', error: String(e) }));
        setThinking(false);
        addSystem(res.success ? (res.output ?? 'Tests passed.') : `Error: ${res.error}`);
    }
    async function runSlashCommit(message) {
        setThinking(true);
        const res = await runCommit(message).catch((e) => ({ success: false, output: '', error: String(e) }));
        setThinking(false);
        addSystem(res.success ? (res.output ?? 'Committed.') : `Error: ${res.error}`);
    }
    // ── agent submit ───────────────────────────────────────────────────────────
    function submit(text, mode) {
        setMessages((m) => [...m, { role: 'user', content: text }]);
        thinkingStart.current = Date.now();
        setThinking(true);
        setMessages((m) => [...m, { role: 'assistant', content: '', streaming: true }]);
        const cancel = streamAgent(sessionName, text, (event) => {
            if (event.type === 'assistant_chunk' && event.text !== undefined) {
                setMessages((m) => {
                    const copy = [...m];
                    const last = copy[copy.length - 1];
                    if (last?.role === 'assistant') {
                        copy[copy.length - 1] = { ...last, content: event.text, streaming: true };
                    }
                    return copy;
                });
            }
            else if (event.type === 'tool_start') {
                const toolMsg = {
                    role: 'tool',
                    content: '',
                    toolData: { call_id: event.call_id, tool: event.tool, args: event.args ?? {}, step: event.step ?? 0, done: false },
                };
                setMessages((m) => {
                    // insert tool message before the last (streaming) assistant message
                    const copy = [...m];
                    copy.splice(copy.length - 1, 0, toolMsg);
                    return copy;
                });
            }
            else if (event.type === 'tool_result') {
                setMessages((m) => m.map((msg) => msg.role === 'tool' && msg.toolData?.call_id === event.call_id
                    ? { ...msg, toolData: { ...msg.toolData, output: event.output, success: event.success, done: true } }
                    : msg));
            }
            else if (event.type === 'result') {
                const elapsedMs = Date.now() - thinkingStart.current;
                setThinking(false);
                cancelRef.current = null;
                const outputTokens = event.result?.tokens?.output ?? undefined;
                setMessages((m) => {
                    const copy = [...m];
                    const lastIdx = copy.length - 1;
                    const last = copy[lastIdx];
                    if (last?.role === 'assistant') {
                        copy[lastIdx] = {
                            ...last,
                            content: event.result?.response ?? last.content,
                            streaming: false,
                            tokens: outputTokens,
                        };
                    }
                    // append thinking-complete marker after the assistant response
                    copy.push({
                        role: 'assistant',
                        content: '',
                        isThinkingComplete: true,
                        thinkingMs: elapsedMs,
                        thinkingLabel: lastThinkingPast.current,
                    });
                    return copy;
                });
                if (!event.result?.success)
                    setStatusLine(`Error: ${event.result?.error ?? 'unknown'}`);
            }
        }, () => {
            setThinking(false);
            cancelRef.current = null;
            setMessages((m) => {
                const copy = [...m];
                const last = copy[copy.length - 1];
                if (last?.streaming)
                    copy[copy.length - 1] = { ...last, streaming: false };
                return copy;
            });
        }, (err) => {
            setThinking(false);
            cancelRef.current = null;
            setStatusLine(`Error: ${err.message}`);
        }, mode);
        cancelRef.current = cancel;
    }
    // ── render ─────────────────────────────────────────────────────────────────
    return (React.createElement(Box, { flexDirection: "column", paddingX: 2 },
        React.createElement(Box, { marginBottom: 1 },
            React.createElement(Text, { bold: true, color: C.acc },
                " ",
                sessionName),
            React.createElement(Text, { color: C.dim },
                "  ",
                provider,
                "/",
                model,
                "  esc=back")),
        messages.length === 0 && (React.createElement(Box, { flexDirection: "column", marginBottom: 1 },
            React.createElement(Text, { color: C.acc }, LOGO),
            React.createElement(Text, { color: C.dim }, "  Type a message or / for commands"))),
        messages.map((msg, i) => {
            if (msg.role === 'user') {
                return (React.createElement(Box, { key: i, marginBottom: 1 },
                    React.createElement(Text, { color: C.acc, bold: true }, "you  "),
                    React.createElement(Text, { color: C.wh, wrap: "wrap" }, msg.content)));
            }
            if (msg.role === 'tool' && msg.toolData) {
                return React.createElement(ToolCallLine, { key: i, call: msg.toolData });
            }
            if (msg.isThinkingComplete && msg.thinkingMs !== undefined) {
                const secs = (msg.thinkingMs / 1000).toFixed(1);
                const label = msg.thinkingLabel ?? 'Thought';
                return (React.createElement(Box, { key: i, marginBottom: 1 },
                    React.createElement(Text, { color: C.dim },
                        "  \u2713 ",
                        label,
                        " for ",
                        secs,
                        "s")));
            }
            return (React.createElement(Box, { key: i, flexDirection: "column", marginBottom: 1 },
                React.createElement(Box, { marginBottom: 0 },
                    React.createElement(Text, { color: C.cyn, bold: true }, "ninja"),
                    msg.tokens ? (React.createElement(Text, { color: C.dim },
                        "  [",
                        msg.tokens >= 1000 ? `${(msg.tokens / 1000).toFixed(1)}k` : msg.tokens,
                        " tok]")) : null),
                React.createElement(Box, { marginLeft: 6 },
                    React.createElement(Markdown, { content: msg.content, streaming: msg.streaming }))));
        }),
        statusLine && React.createElement(Text, { color: C.red },
            " ",
            statusLine),
        completions.length > 0 && (React.createElement(Box, { flexDirection: "column", marginBottom: 1, paddingLeft: 2, borderStyle: "single", borderColor: C.acc },
            completionScrollTop > 0 && (React.createElement(Text, { color: C.dim },
                "  \u2191 ",
                completionScrollTop,
                " more")),
            completions.slice(completionScrollTop, completionScrollTop + COMPLETION_WINDOW).map((c, ci) => {
                const absIdx = completionScrollTop + ci;
                const sel = absIdx === completionIdx;
                return (React.createElement(Box, { key: c },
                    React.createElement(Text, { color: sel ? C.acc : C.dim }, sel ? '▶ ' : '  '),
                    React.createElement(Box, { minWidth: 16 },
                        React.createElement(Text, { color: sel ? C.acc : C.txt, bold: sel }, c)),
                    React.createElement(Text, { color: C.dim }, SLASH_COMMANDS[c]?.description ?? '')));
            }),
            completionScrollTop + COMPLETION_WINDOW < completions.length && (React.createElement(Text, { color: C.dim },
                "  \u2193 ",
                completions.length - completionScrollTop - COMPLETION_WINDOW,
                " more")),
            React.createElement(Text, { color: C.dim }, "  \u2191\u2193 navigate  tab/enter select"))),
        thinking && !aiIsStreaming && (React.createElement(Box, { flexDirection: "row", justifyContent: "space-between" },
            React.createElement(ThinkingIndicator, { onCurrentPast: (past) => { lastThinkingPast.current = past; } }),
            React.createElement(Text, { color: C.dim }, "esc to cancel  "))),
        React.createElement(Box, { borderStyle: "round", borderColor: thinking ? C.dim : C.acc, marginTop: 0 },
            React.createElement(Text, { color: C.acc }, " \u276F "),
            React.createElement(Text, { color: C.txt }, input),
            !thinking && React.createElement(Text, { color: C.acc }, "\u258C"))));
}
