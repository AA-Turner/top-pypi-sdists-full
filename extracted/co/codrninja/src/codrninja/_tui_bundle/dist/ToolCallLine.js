import React from 'react';
import { Box, Text } from 'ink';
function trunc(s, n) {
    return s.length > n ? s.slice(0, n) + '…' : s;
}
function formatLabel(tool, args) {
    const a = args;
    switch (tool) {
        case 'read_file':
            return `read  ${trunc(a.path ?? '', 50)}`;
        case 'write_file':
            return `write ${trunc(a.path ?? '', 50)}`;
        case 'edit_file':
            return `edit  ${trunc(a.path ?? '', 50)}`;
        case 'execute_command':
            return `$  ${trunc(a.command ?? '', 55)}`;
        case 'list_files':
            return `ls    ${trunc(a.path ?? '.', 50)}`;
        case 'search_files':
            return `grep  "${trunc(a.pattern ?? '', 30)}"  ${trunc(a.path ?? '.', 24)}`;
        case 'web_fetch':
            return `fetch ${trunc(a.url ?? '', 50)}`;
        case 'web_search':
            return `search  "${trunc(a.query ?? '', 50)}"`;
        case 'todo_add':
            return `todo+ ${trunc(a.task ?? '', 50)}`;
        case 'todo_complete':
            return `todo✓ ${a.todo_id ?? ''}`;
        case 'todo_list':
            return `todo list`;
        case 'todo_remove':
            return `todo- ${a.todo_id ?? ''}`;
        default:
            if (tool.startsWith('lsp_')) {
                const file = trunc(String(a.file_path ?? a.path ?? ''), 35);
                const line = a.line ? `:${a.line}` : '';
                return `${tool.slice(4)}  ${file}${line}`;
            }
            if (tool.startsWith('mcp_')) {
                const short = tool.slice(4).replace(/_/g, ' ');
                return `mcp  ${short}`;
            }
            return `${tool}  ${trunc(JSON.stringify(args), 45)}`;
    }
}
function formatOutput(tool, output) {
    const s = output.trim();
    switch (tool) {
        case 'read_file': {
            const lines = s.split('\n').length;
            return `${lines} line${lines === 1 ? '' : 's'}`;
        }
        case 'write_file':
        case 'edit_file':
            return 'saved';
        case 'execute_command': {
            const first = s.split('\n')[0] ?? '';
            return trunc(first || 'done', 60);
        }
        case 'list_files': {
            const items = s.split('\n').filter(Boolean).length;
            return `${items} item${items === 1 ? '' : 's'}`;
        }
        default:
            return trunc(s, 60);
    }
}
export function ToolCallLine({ call }) {
    const label = formatLabel(call.tool, call.args);
    if (!call.done) {
        return (React.createElement(Box, null,
            React.createElement(Text, { color: "yellow", dimColor: true },
                '  ',
                "\u27F3  ",
                label)));
    }
    const icon = call.success ? '✓' : '✗';
    const color = call.success ? 'green' : 'red';
    const out = call.output ? '  ' + formatOutput(call.tool, call.output) : '';
    return (React.createElement(Box, null,
        React.createElement(Text, { color: color, dimColor: true },
            '  ',
            icon,
            "  ",
            label),
        out ? React.createElement(Text, { dimColor: true }, out) : null));
}
