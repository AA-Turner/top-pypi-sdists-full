/**
 * JS unit tests for the chat.js attribution footer (#923).
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

function _addAttributionFooter(msgEl, snapshot) {
    if (!msgEl || !snapshot || typeof snapshot !== 'object') return;

    const details = document.createElement('details');
    details.className = 'attribution-footer';

    const summary = document.createElement('summary');
    summary.className = 'attribution-summary';
    const parts = [
        `${(snapshot.turns || []).length} turns`,
        `${(snapshot.memory || []).length} memories`,
        `${(snapshot.sources || []).length} sources`,
        `${(snapshot.tools || []).length} tools`,
        `${(snapshot.packs || []).length} packs`,
    ];
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
        dlp_match_count: 0,
        output_filter_match_count: 0,
    };
}

describe('_addAttributionFooter', () => {
    it('renders five sections with items from a typical snapshot', () => {
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
        ]);
        const body = footer.textContent;
        expect(body).toContain('m-1');
        expect(body).toContain('@user/memory/pref');
        expect(body).toContain('README.md');
        expect(body).toContain('read_file');
        expect(body).toContain('core');
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
        expect(summary).not.toContain('DLP:');
        expect(summary).not.toContain('OF:');
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
            dlp_match_count: 0,
            output_filter_match_count: 0,
        });
        const empties = msg.querySelectorAll('.attribution-empty');
        expect(empties.length).toBe(5);
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
});
