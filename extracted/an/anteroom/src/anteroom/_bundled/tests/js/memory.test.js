/**
 * JS unit tests for the memory panel module (#1416).
 *
 * Covers the logic-heavy parts of static/js/memory.js per
 * .claude/rules/ux-testing.md: filter predicate, query string construction,
 * list render, detail render, edit form validation, API call shape, and
 * error rendering — all without a browser.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MODULE_PATH = path.resolve(__dirname, '../../src/anteroom/static/js/memory.js');

function loadMemoryModule() {
    // memory.js is an IIFE that publishes a global `MemoryPanel` plus a
    // CommonJS export under `module.exports`. Evaluate the source in a
    // sandbox that exposes both `document` (from jsdom) and a fresh
    // `module` so we can grab the exported API surface.
    const source = fs.readFileSync(MODULE_PATH, 'utf8');
    const module = { exports: {} };
    const context = {
        window,
        document,
        console,
        fetch: globalThis.fetch,
        URLSearchParams,
        module,
        MemoryPanel: undefined,
    };
    const fn = new Function(
        'window', 'document', 'console', 'fetch', 'URLSearchParams', 'module',
        source + '\nreturn module.exports;',
    );
    return fn(window, document, console, globalThis.fetch, URLSearchParams, module);
}

let Mem;
beforeEach(() => {
    document.body.innerHTML = '';
    // Reset the DOM between tests — avoid cross-test interference.
    Mem = loadMemoryModule();
    // Stub App.api so tests can assert request shape.
    globalThis.App = { api: vi.fn() };
});

afterEach(() => {
    delete globalThis.App;
});

function _makeMemory(overrides = {}) {
    return {
        id: 'id-1',
        fqn: '@user/memory/sample',
        name: 'sample',
        namespace: 'user',
        content: 'a sample memory',
        created_at: '2026-04-16T00:00:00Z',
        metadata: {
            memory_scope: 'user',
            memory_category: 'preference',
            memory_status: 'active',
            created_by: 'user',
            recall_count: 0,
            last_recalled_at: null,
            ...overrides.metadata,
        },
        ...overrides,
    };
}

// ---------------------------------------------------------------------------
// _matchesFilters — pure filter predicate
// ---------------------------------------------------------------------------

describe('_matchesFilters', () => {
    it('matches everything when no filters set', () => {
        const m = _makeMemory();
        expect(Mem._matchesFilters(m, {})).toBe(true);
    });

    it('respects scope filter', () => {
        const m = _makeMemory();
        expect(Mem._matchesFilters(m, { scope: 'user' })).toBe(true);
        expect(Mem._matchesFilters(m, { scope: 'local' })).toBe(false);
    });

    it('respects status filter', () => {
        const m = _makeMemory({ metadata: { memory_status: 'candidate' } });
        expect(Mem._matchesFilters(m, { status: 'candidate' })).toBe(true);
        expect(Mem._matchesFilters(m, { status: 'active' })).toBe(false);
    });

    it('respects category filter', () => {
        const m = _makeMemory();
        expect(Mem._matchesFilters(m, { category: 'preference' })).toBe(true);
        expect(Mem._matchesFilters(m, { category: 'decision' })).toBe(false);
    });

    it('combines filters with AND semantics', () => {
        const m = _makeMemory();
        expect(Mem._matchesFilters(m, { scope: 'user', status: 'active' })).toBe(true);
        expect(Mem._matchesFilters(m, { scope: 'user', status: 'archived' })).toBe(false);
    });

    it('rejects when metadata missing', () => {
        expect(Mem._matchesFilters({ fqn: 'x' }, { scope: 'user' })).toBe(false);
    });
});

// ---------------------------------------------------------------------------
// _buildQueryString — URL param construction
// ---------------------------------------------------------------------------

describe('_buildQueryString', () => {
    it('returns empty string for empty filters', () => {
        expect(Mem._buildQueryString({})).toBe('');
    });

    it('serialises only set filters', () => {
        const qs = Mem._buildQueryString({ scope: 'user', status: 'active' });
        expect(qs).toContain('?');
        expect(qs).toContain('scope=user');
        expect(qs).toContain('status=active');
    });

    it('URL-encodes namespace with special chars', () => {
        const qs = Mem._buildQueryString({ namespace: 'my project' });
        // URLSearchParams encodes spaces as '+'.
        expect(qs).toContain('namespace=my+project');
    });

    it('omits blank filter values', () => {
        expect(Mem._buildQueryString({ scope: '', status: '' })).toBe('');
    });
});

// ---------------------------------------------------------------------------
// _buildListItem — DOM render
// ---------------------------------------------------------------------------

describe('_buildListItem', () => {
    it('uses textContent for user fields (no XSS via fqn)', () => {
        const m = _makeMemory({ fqn: '<script>evil()</script>' });
        const node = Mem._buildListItem(m);
        const title = node.querySelector('.memory-item-title');
        expect(title).toBeTruthy();
        // textContent round-trips to the literal string, and no <script> element exists.
        expect(title.textContent).toBe('<script>evil()</script>');
        expect(node.querySelector('script')).toBeNull();
    });

    it('renders scope / category / status badges', () => {
        const m = _makeMemory();
        const node = Mem._buildListItem(m);
        const badges = node.querySelectorAll('.memory-badge');
        const texts = Array.from(badges).map(b => b.textContent);
        expect(texts).toContain('user');
        expect(texts).toContain('preference');
        expect(texts).toContain('active');
    });
});

// ---------------------------------------------------------------------------
// _refreshList — fetch, empty state, error state, filter propagation
// ---------------------------------------------------------------------------

describe('_refreshList', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="memory-list"></div>
            <select id="memory-filter-scope"><option value=""></option><option value="user">user</option></select>
            <select id="memory-filter-status"><option value=""></option></select>
            <select id="memory-filter-category"><option value=""></option></select>
            <input id="memory-filter-namespace" value="" />
        `;
    });

    it('renders empty state when API returns no memories', async () => {
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem._refreshList();
        const list = document.getElementById('memory-list');
        expect(list.textContent).toContain('No memories found');
    });

    it('calls API with filter query string', async () => {
        document.getElementById('memory-filter-scope').value = 'user';
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem._refreshList();
        const calledWith = globalThis.App.api.mock.calls[0][0];
        expect(calledWith).toContain('/memory');
        expect(calledWith).toContain('scope=user');
    });

    it('renders the error state when the API rejects', async () => {
        globalThis.App.api.mockRejectedValueOnce(new Error('boom'));
        await Mem._refreshList();
        const err = document.querySelector('.memory-error');
        expect(err).toBeTruthy();
        expect(err.textContent).toContain('boom');
    });

    it('renders list items for returned memories', async () => {
        globalThis.App.api.mockResolvedValueOnce([_makeMemory(), _makeMemory({ fqn: '@user/memory/second', name: 'second' })]);
        await Mem._refreshList();
        const items = document.querySelectorAll('.memory-item');
        expect(items.length).toBe(2);
    });
});

// ---------------------------------------------------------------------------
// createMemory — POST request shape
// ---------------------------------------------------------------------------

describe('createMemory', () => {
    it('POSTs JSON body to /memory', async () => {
        globalThis.App.api.mockResolvedValueOnce({ fqn: '@user/memory/x' });
        await Mem.createMemory({ content: 'hi', scope: 'user', category: 'preference' });
        expect(globalThis.App.api).toHaveBeenCalledWith(
            '/memory',
            expect.objectContaining({
                method: 'POST',
                headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
            }),
        );
        const call = globalThis.App.api.mock.calls[0][1];
        expect(JSON.parse(call.body)).toEqual({ content: 'hi', scope: 'user', category: 'preference' });
    });
});

// ---------------------------------------------------------------------------
// _showCreateForm — builds a functional create form in the panel
// ---------------------------------------------------------------------------

describe('_showCreateForm', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="memory-list"></div>
            <div id="memory-detail"></div>
            <div id="memory-edit-form"></div>
            <div id="memory-create-form"></div>
            <select id="memory-filter-scope"><option value=""></option></select>
            <select id="memory-filter-status"><option value=""></option></select>
            <select id="memory-filter-category"><option value=""></option></select>
            <input id="memory-filter-namespace" value="" />
        `;
    });

    it('builds all required fields and a Create button', () => {
        Mem._showCreateForm();
        const form = document.getElementById('memory-create-form');
        expect(form).toBeTruthy();
        expect(document.getElementById('memory-create-content')).toBeTruthy();
        expect(document.getElementById('memory-create-scope')).toBeTruthy();
        expect(document.getElementById('memory-create-category')).toBeTruthy();
        expect(document.getElementById('memory-create-name')).toBeTruthy();
        expect(document.getElementById('memory-create-project-slug')).toBeTruthy();
        expect(document.getElementById('memory-create-save')).toBeTruthy();
        // Only the create form is visible.
        expect(form.style.display).toBe('');
    });
});

describe('_submitCreate', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="memory-list"></div>
            <div id="memory-detail"></div>
            <div id="memory-edit-form"></div>
            <div id="memory-create-form"></div>
            <select id="memory-filter-scope"><option value=""></option></select>
            <select id="memory-filter-status"><option value=""></option></select>
            <select id="memory-filter-category"><option value=""></option></select>
            <input id="memory-filter-namespace" value="" />
        `;
        Mem._showCreateForm();
    });

    it('rejects empty content inline without calling the API', async () => {
        document.getElementById('memory-create-content').value = '   ';
        await Mem._submitCreate();
        expect(globalThis.App.api).not.toHaveBeenCalled();
        const err = document.getElementById('memory-create-error');
        expect(err.textContent).toContain('empty');
        expect(err.style.display).toBe('');
    });

    it('POSTs the filled-in values on submit', async () => {
        document.getElementById('memory-create-content').value = 'new memory body';
        document.getElementById('memory-create-scope').value = 'user';
        document.getElementById('memory-create-category').value = 'preference';
        document.getElementById('memory-create-name').value = 'ui-create';
        globalThis.App.api.mockResolvedValueOnce({ fqn: '@user/memory/ui-create' });
        // Second call is the refresh after create.
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem._submitCreate();
        expect(globalThis.App.api).toHaveBeenCalledWith(
            '/memory',
            expect.objectContaining({ method: 'POST' }),
        );
        const body = JSON.parse(globalThis.App.api.mock.calls[0][1].body);
        expect(body).toMatchObject({
            content: 'new memory body',
            scope: 'user',
            category: 'preference',
            name: 'ui-create',
        });
    });
});

// ---------------------------------------------------------------------------
// _showMemoryDetail — provenance block is rendered from metadata
// ---------------------------------------------------------------------------

describe('_showMemoryDetail provenance block', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="memory-list"></div>
            <div id="memory-detail"></div>
            <div id="memory-edit-form"></div>
            <div id="memory-create-form"></div>
            <select id="memory-filter-scope"><option value=""></option></select>
            <select id="memory-filter-status"><option value=""></option></select>
            <select id="memory-filter-category"><option value=""></option></select>
            <input id="memory-filter-namespace" value="" />
        `;
    });

    it('lists provenance fields when present', async () => {
        globalThis.App.api.mockResolvedValueOnce({
            fqn: '@user/memory/withprov',
            name: 'withprov',
            content: 'p1',
            source: 'local',
            metadata: {
                memory_scope: 'user',
                memory_category: 'preference',
                memory_status: 'active',
                provenance: {
                    conversation_id: '11111111-1111-1111-1111-111111111111',
                    message_id: '22222222-2222-2222-2222-222222222222',
                },
            },
        });
        await Mem._showMemoryDetail('@user/memory/withprov');
        const prov = document.querySelector('.memory-detail-provenance');
        expect(prov).toBeTruthy();
        expect(prov.textContent).toContain('conversation_id');
        expect(prov.textContent).toContain('11111111');
        expect(prov.textContent).toContain('message_id');
    });

    it('renders empty-state text when no provenance is recorded', async () => {
        globalThis.App.api.mockResolvedValueOnce({
            fqn: '@user/memory/noprov',
            name: 'noprov',
            content: 'p2',
            metadata: { memory_scope: 'user', memory_status: 'active' },
        });
        await Mem._showMemoryDetail('@user/memory/noprov');
        expect(document.querySelector('.memory-provenance-empty').textContent).toContain('No provenance');
    });
});
