/**
 * JS unit tests for the chat.js attribution footer (#923, #1473).
 *
 * Follows the same inline-copy pattern as chat_save_memory.test.js:
 * loading the full chat.js IIFE into jsdom is heavy because of all
 * the globals it expects, so the renderer under test is re-declared
 * here and must stay behaviourally in sync with
 * ``_addAttributionFooter`` in src/anteroom/static/js/chat.js.
 *
 * The core guarantee these tests pin down is that every user-derived
 * snapshot value flows through ``textContent``, never ``innerHTML`` —
 * so a hostile payload (``<script>…`` in a tool name, for example)
 * can never execute. See the XSS negative test.
 */

import { describe, it, expect, beforeEach } from 'vitest';

// #1473 — prefer canonical <section>_count field; fall back to
// truncation-aware computation for older persisted snapshots.
// This is a sync copy of _attrCount from chat.js and must stay in sync.
function _attrCount(snapshot, section) {
    const countField = section + '_count';
    if (snapshot[countField] !== undefined) {
        const n = parseInt(snapshot[countField], 10);
        if (!isNaN(n)) return n;
    }
    const items = snapshot[section] || [];
    const last = items[items.length - 1];
    const truncated = (last && last.truncated !== undefined) ? last.truncated : 0;
    return items.length - (truncated ? 1 : 0) + truncated;
}

function _addAttributionFooter(msgEl, snapshot) {
    if (!msgEl || !snapshot || typeof snapshot !== 'object') return;

    const details = document.createElement('details');
    details.className = 'attribution-footer';

    const summary = document.createElement('summary');
    summary.className = 'attribution-summary';
    const parts = [
        `${_attrCount(snapshot, 'turns')} turns`,
        `${_attrCount(snapshot, 'memory')} memories`,
        `${_attrCount(snapshot, 'sources')} sources`,
        `${_attrCount(snapshot, 'tools')} tools`,
        `${_attrCount(snapshot, 'packs')} packs`,
    ];
    // #1462 — instruction-file segment. Hidden when no file loaded so
    // the default footer stays compact, matching the CLI footer rule.
    const _instrCount = _attrCount(snapshot, 'instructions');
    if (_instrCount) {
        parts.push(`${_instrCount} ${_instrCount === 1 ? 'instruction file' : 'instruction files'}`);
    }
    if (snapshot.dlp_match_count) parts.push(`DLP:${snapshot.dlp_match_count}`);
    if (snapshot.output_filter_match_count) parts.push(`OF:${snapshot.output_filter_match_count}`);
    summary.textContent = `Why this context? — ${parts.join(' · ')}`;
    details.appendChild(summary);

    const body = document.createElement('div');
    body.className = 'attribution-body';
    body.appendChild(_attrSection('Recent turns', snapshot.turns, ['message_id', 'role']));
    body.appendChild(_attrSection('Recalled memories', snapshot.memory, ['fqn', 'scope', 'category']));
    body.appendChild(_attrSection('RAG sources', snapshot.sources, ['label', 'type']));
    body.appendChild(_attrSection('Tool calls', snapshot.tools, ['id', 'name']));
    body.appendChild(_attrSection('Attached packs', snapshot.packs, ['namespace', 'name', 'scope']));
    // #1462 — project instructions section. Every user-derived value
    // (path) flows through textContent only; see _attrSection.
    body.appendChild(_attrSection('Project instructions', snapshot.instructions, ['path', 'scope', 'estimated_tokens']));
    details.appendChild(body);

    msgEl.appendChild(details);
}

function _attrSection(title, items, fields) {
    const section = document.createElement('div');
    section.className = 'attribution-section';

    const heading = document.createElement('div');
    heading.className = 'attribution-section-title';
    heading.textContent = title;
    section.appendChild(heading);

    const list = Array.isArray(items) ? items : [];
    if (list.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'attribution-empty';
        empty.textContent = '(none)';
        section.appendChild(empty);
        return section;
    }

    const ul = document.createElement('ul');
    ul.className = 'attribution-list';
    for (const item of list) {
        const li = document.createElement('li');
        if (item && typeof item === 'object' && 'truncated' in item) {
            li.className = 'attribution-more';
            li.textContent = `+${Number(item.truncated) || 0} more`;
        } else if (item && typeof item === 'object') {
            const parts = [];
            for (const f of fields) {
                const v = item[f];
                if (v !== undefined && v !== null && v !== '') {
                    parts.push(String(v));
                }
            }
            li.textContent = parts.length > 0 ? parts.join(' · ') : '(empty)';
        } else {
            li.textContent = '(empty)';
        }
        ul.appendChild(li);
    }
    section.appendChild(ul);
    return section;
}

beforeEach(() => {
    document.body.innerHTML = '<div class="message assistant" id="msg"></div>';
});

function typical() {
    return {
        turns: [{ message_id: 'm-1', role: 'user' }, { message_id: 'm-2', role: 'assistant' }],
        memory: [{ fqn: '@user/memory/pref', scope: 'user', category: 'preference' }],
        sources: [{ label: 'README.md', type: 'source_chunk' }],
        tools: [{ id: 'tc-1', name: 'read_file' }],
        packs: [{ namespace: 'core', name: 'alpha', scope: 'global' }],
        instructions: [{ path: '/repo/ANTEROOM.md', scope: 'project', estimated_tokens: 9894 }],
        dlp_match_count: 0,
        output_filter_match_count: 0,
    };
}

describe('_addAttributionFooter', () => {
    it('renders six sections with items from a typical snapshot', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(msg, typical());
        const footer = msg.querySelector('.attribution-footer');
        expect(footer).toBeTruthy();
        const titles = [...footer.querySelectorAll('.attribution-section-title')].map(e => e.textContent);
        expect(titles).toEqual([
            'Recent turns',
            'Recalled memories',
            'RAG sources',
            'Tool calls',
            'Attached packs',
            'Project instructions',
        ]);
        const body = footer.textContent;
        expect(body).toContain('m-1');
        expect(body).toContain('@user/memory/pref');
        expect(body).toContain('README.md');
        expect(body).toContain('read_file');
        expect(body).toContain('core');
        expect(body).toContain('/repo/ANTEROOM.md');
    });

    it('summary reflects counts and omits DLP/OF when zero', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(msg, typical());
        const summary = msg.querySelector('.attribution-summary').textContent;
        expect(summary).toContain('2 turns');
        expect(summary).toContain('1 memories');
        expect(summary).toContain('1 sources');
        expect(summary).toContain('1 tools');
        expect(summary).toContain('1 packs');
        // #1462 — singular noun for exactly one file.
        expect(summary).toContain('1 instruction file');
        expect(summary).not.toContain('DLP:');
        expect(summary).not.toContain('OF:');
    });

    // #1462 — instructions-section tests
    it('summary hides instructions count when no file loaded', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(msg, {
            turns: [], memory: [], sources: [], tools: [], packs: [],
            instructions: [],
            dlp_match_count: 0, output_filter_match_count: 0,
        });
        const summary = msg.querySelector('.attribution-summary').textContent;
        expect(summary).not.toContain('instruction');
    });

    it('summary uses plural noun when multiple instruction files load', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(msg, {
            turns: [], memory: [], sources: [], tools: [], packs: [],
            instructions: [
                { path: '/home/u/.anteroom/ANTEROOM.md', scope: 'global', estimated_tokens: 400 },
                { path: '/repo/ANTEROOM.md', scope: 'project', estimated_tokens: 9000 },
            ],
            dlp_match_count: 0, output_filter_match_count: 0,
        });
        const summary = msg.querySelector('.attribution-summary').textContent;
        expect(summary).toContain('2 instruction files');
    });

    it('renders instructions[].path via textContent even when hostile', () => {
        // The path field is user-controlled (any filesystem location). If a
        // hostile payload reaches the renderer, it must NOT execute. This
        // mirrors the XSS discipline applied to every other per-field test.
        const msg = document.getElementById('msg');
        const hostile = '<img src=x onerror="window.__INSTR_PWNED__=true">';
        _addAttributionFooter(msg, {
            turns: [], memory: [], sources: [], tools: [], packs: [],
            instructions: [{ path: hostile, scope: 'project', estimated_tokens: 1 }],
            dlp_match_count: 0, output_filter_match_count: 0,
        });
        const footer = msg.querySelector('.attribution-footer');
        // Rendered as literal text (textContent), not as parsed HTML.
        expect(footer.textContent).toContain(hostile);
        // No <img> element attached (innerHTML would have created one).
        expect(msg.querySelectorAll('img').length).toBe(0);
        // And no onerror side effect ran.
        expect(globalThis.__INSTR_PWNED__).toBeUndefined();
    });

    it('surfaces DLP:N and OF:N in summary when non-zero', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(msg, {
            turns: [], memory: [], sources: [], tools: [], packs: [],
            dlp_match_count: 2,
            output_filter_match_count: 1,
        });
        const summary = msg.querySelector('.attribution-summary').textContent;
        expect(summary).toContain('DLP:2');
        expect(summary).toContain('OF:1');
    });

    it('renders (none) for every empty section', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(msg, {
            turns: [], memory: [], sources: [], tools: [], packs: [],
            instructions: [],
            dlp_match_count: 0,
            output_filter_match_count: 0,
        });
        const empties = msg.querySelectorAll('.attribution-empty');
        expect(empties.length).toBe(6);
        empties.forEach(e => expect(e.textContent).toBe('(none)'));
    });

    it('renders the truncation marker as "+N more"', () => {
        const msg = document.getElementById('msg');
        const snap = typical();
        snap.tools = [
            { id: 'tc-1', name: 'read_file' },
            { truncated: 12 },
        ];
        _addAttributionFooter(msg, snap);
        const more = msg.querySelector('.attribution-more');
        expect(more).toBeTruthy();
        expect(more.textContent).toBe('+12 more');
    });

    it('never executes hostile payloads — <script> renders as text, not markup', () => {
        const msg = document.getElementById('msg');
        const hostile = '<script>window.__PWNED__=true;</script>';
        _addAttributionFooter(msg, {
            turns: [],
            memory: [],
            sources: [{ label: hostile, type: 'source_chunk' }],
            tools: [{ id: 'tc-1', name: hostile }],
            packs: [],
            dlp_match_count: 0,
            output_filter_match_count: 0,
        });
        // The hostile literal shows up as text, meaning textContent was used
        // (innerHTML would have parsed and stripped the <script> tag).
        const footer = msg.querySelector('.attribution-footer');
        expect(footer.textContent).toContain(hostile);
        // No actual <script> element ever attached to the DOM.
        expect(msg.querySelectorAll('script').length).toBe(0);
        // And no side effect: the script body never ran.
        expect(globalThis.__PWNED__).toBeUndefined();
    });

    it('is called from the loadMessages replay path for persisted metadata (#923 resume parity)', () => {
        // Mimic the branch added to the loadMessages loop in chat.js.
        // On reload, msg.metadata may be a JSON string or a parsed object.
        const msg = document.getElementById('msg');
        const raw = {
            metadata: JSON.stringify({
                rag_sources: [],
                attribution: {
                    turns: [{message_id: 'm-1', role: 'user'}],
                    memory: [],
                    sources: [],
                    tools: [{id: 'tc-1', name: 'read_file'}],
                    packs: [],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                },
            }),
        };
        // Reproduce the parse + dispatch logic in chat.js:
        const meta = typeof raw.metadata === 'string' ? JSON.parse(raw.metadata) : raw.metadata;
        if (meta && meta.attribution && typeof meta.attribution === 'object') {
            _addAttributionFooter(msg, meta.attribution);
        }
        const footer = msg.querySelector('.attribution-footer');
        expect(footer).toBeTruthy();
        expect(footer.textContent).toContain('m-1');
        expect(footer.textContent).toContain('read_file');
    });

    it('is safe on null/missing/malformed inputs', () => {
        const msg = document.getElementById('msg');
        _addAttributionFooter(null, typical());
        _addAttributionFooter(msg, null);
        _addAttributionFooter(msg, undefined);
        _addAttributionFooter(msg, 'not-an-object');
        expect(msg.querySelector('.attribution-footer')).toBeNull();

        // Partial/fieldless items render as (empty), never throw.
        _addAttributionFooter(msg, {
            turns: [{}],
            memory: [null],
            sources: [],
            tools: [],
            packs: [],
            dlp_match_count: 0,
            output_filter_match_count: 0,
        });
        const footer = msg.querySelector('.attribution-footer');
        expect(footer).toBeTruthy();
        const emptyItems = footer.querySelectorAll('.attribution-list li');
        expect(emptyItems.length).toBe(2);
        emptyItems.forEach(li => expect(li.textContent).toBe('(empty)'));
    });

    // #1473 — canonical count field tests
    it('_attrCount prefers the canonical <section>_count field', () => {
        // With tools_count=30 the function should return 30 even if the list has
        // only 21 entries (cap + sentinel).
        const snap = {
            tools: Array.from({ length: 20 }, (_, i) => ({ id: `tc-${i}`, name: `tool_${i}` })).concat([{ truncated: 10 }]),
            tools_count: 30,
        };
        expect(_attrCount(snap, 'tools')).toBe(30);
    });

    it('_attrCount falls back to truncation-aware computation for legacy snapshots', () => {
        // Legacy snapshot: no tools_count, tools list ends in sentinel.
        const snap = {
            tools: Array.from({ length: 20 }, (_, i) => ({ id: `tc-${i}`, name: `tool_${i}` })).concat([{ truncated: 10 }]),
        };
        expect(_attrCount(snap, 'tools')).toBe(30);
    });

    it('summary shows 30 tools for a truncated-then-counted snapshot', () => {
        const msg = document.getElementById('msg');
        const tools = Array.from({ length: 20 }, (_, i) => ({ id: `tc-${i}`, name: `tool_${i}` }));
        tools.push({ truncated: 10 });
        _addAttributionFooter(msg, {
            turns: [],
            memory: [],
            sources: [],
            tools,
            tools_count: 30,
            packs: [],
            instructions: [],
            dlp_match_count: 0,
            output_filter_match_count: 0,
        });
        const summary = msg.querySelector('.attribution-summary').textContent;
        expect(summary).toContain('30 tools');
        expect(summary).not.toContain('21 tools');
    });

    it('summary shows 30 tools for legacy truncated dict without count field', () => {
        const msg = document.getElementById('msg');
        const tools = Array.from({ length: 20 }, (_, i) => ({ id: `tc-${i}`, name: `tool_${i}` }));
        tools.push({ truncated: 10 });
        _addAttributionFooter(msg, {
            turns: [],
            memory: [],
            sources: [],
            tools,
            // No tools_count field — legacy shape, fallback must compute 30.
            packs: [],
            instructions: [],
            dlp_match_count: 0,
            output_filter_match_count: 0,
        });
        const summary = msg.querySelector('.attribution-summary').textContent;
        expect(summary).toContain('30 tools');
        expect(summary).not.toContain('21 tools');
    });
});
