import React from 'react';
import { Box, Text } from 'ink';
function parseInline(line) {
    const segs = [];
    let i = 0;
    let buf = '';
    while (i < line.length) {
        // bold-italic ***
        if (line.startsWith('***', i)) {
            const end = line.indexOf('***', i + 3);
            if (end !== -1) {
                if (buf) {
                    segs.push({ t: 'text', v: buf });
                    buf = '';
                }
                segs.push({ t: 'bold-italic', v: line.slice(i + 3, end) });
                i = end + 3;
                continue;
            }
        }
        // bold **
        if (line.startsWith('**', i)) {
            const end = line.indexOf('**', i + 2);
            if (end !== -1) {
                if (buf) {
                    segs.push({ t: 'text', v: buf });
                    buf = '';
                }
                segs.push({ t: 'bold', v: line.slice(i + 2, end) });
                i = end + 2;
                continue;
            }
        }
        // italic *
        if (line[i] === '*' && line[i + 1] !== '*') {
            const end = line.indexOf('*', i + 1);
            if (end !== -1 && end > i + 1) {
                if (buf) {
                    segs.push({ t: 'text', v: buf });
                    buf = '';
                }
                segs.push({ t: 'italic', v: line.slice(i + 1, end) });
                i = end + 1;
                continue;
            }
        }
        // inline code `
        if (line[i] === '`') {
            const end = line.indexOf('`', i + 1);
            if (end !== -1) {
                if (buf) {
                    segs.push({ t: 'text', v: buf });
                    buf = '';
                }
                segs.push({ t: 'code', v: line.slice(i + 1, end) });
                i = end + 1;
                continue;
            }
        }
        buf += line[i];
        i++;
    }
    if (buf)
        segs.push({ t: 'text', v: buf });
    return segs;
}
function InlineLine({ text }) {
    const segs = parseInline(text);
    if (segs.length === 1 && segs[0].t === 'text') {
        return React.createElement(Text, { wrap: "wrap" }, segs[0].v);
    }
    return (React.createElement(Box, { flexWrap: "wrap" }, segs.map((s, i) => {
        switch (s.t) {
            case 'bold': return React.createElement(Text, { key: i, bold: true }, s.v);
            case 'italic': return React.createElement(Text, { key: i, italic: true }, s.v);
            case 'bold-italic': return React.createElement(Text, { key: i, bold: true, italic: true }, s.v);
            case 'code': return React.createElement(Text, { key: i, color: "yellow" }, s.v);
            default: return React.createElement(Text, { key: i }, s.v);
        }
    })));
}
export function Markdown({ content, streaming }) {
    const lines = content.split('\n');
    const nodes = [];
    let i = 0;
    while (i < lines.length) {
        const line = lines[i];
        // fenced code block
        if (line.startsWith('```')) {
            const lang = line.slice(3).trim();
            const block = [];
            i++;
            while (i < lines.length && !lines[i].startsWith('```')) {
                block.push(lines[i]);
                i++;
            }
            nodes.push(React.createElement(Box, { key: `cb-${i}`, flexDirection: "column", borderStyle: "single", borderColor: "gray", paddingX: 1, marginY: 0 },
                lang ? React.createElement(Text, { dimColor: true }, lang) : null,
                block.map((l, j) => React.createElement(Text, { key: j, color: "yellow" }, l))));
            i++;
            continue;
        }
        // heading
        const hm = line.match(/^(#{1,3})\s+(.+)/);
        if (hm) {
            const level = hm[1].length;
            nodes.push(React.createElement(Text, { key: `h-${i}`, bold: true, color: level === 1 ? 'cyan' : level === 2 ? 'green' : 'white' }, hm[2]));
            i++;
            continue;
        }
        // horizontal rule
        if (/^[-*_]{3,}$/.test(line.trim())) {
            nodes.push(React.createElement(Text, { key: `hr-${i}`, dimColor: true }, '─'.repeat(50)));
            i++;
            continue;
        }
        // bullet
        const bm = line.match(/^(\s*)[-*•]\s+(.+)/);
        if (bm) {
            nodes.push(React.createElement(Box, { key: `b-${i}`, marginLeft: Math.floor(bm[1].length / 2) },
                React.createElement(Text, { color: "cyan" }, "\u2022 "),
                React.createElement(InlineLine, { text: bm[2] })));
            i++;
            continue;
        }
        // numbered list
        const nm = line.match(/^(\s*)(\d+)\.\s+(.+)/);
        if (nm) {
            nodes.push(React.createElement(Box, { key: `n-${i}`, marginLeft: Math.floor(nm[1].length / 2) },
                React.createElement(Text, { color: "cyan" },
                    nm[2],
                    ". "),
                React.createElement(InlineLine, { text: nm[3] })));
            i++;
            continue;
        }
        // empty line → small gap
        if (line.trim() === '') {
            nodes.push(React.createElement(Text, { key: `e-${i}` }, ''));
            i++;
            continue;
        }
        // regular line
        const isLast = i === lines.length - 1;
        nodes.push(React.createElement(Box, { key: `l-${i}` },
            React.createElement(InlineLine, { text: line }),
            isLast && streaming && React.createElement(Text, { color: "cyan" }, "\u258C")));
        i++;
    }
    // cursor on trailing newline
    if (streaming && content.endsWith('\n')) {
        nodes.push(React.createElement(Text, { key: "cur" }, "\u258C"));
    }
    return React.createElement(Box, { flexDirection: "column" }, nodes);
}
