/**
 * JS unit tests for the memory retention tab (#625).
 *
 * Covers:
 * - Retention tab renders the preview header + candidate list from /memory/retention-preview
 * - Empty state when policy is disabled or matches nothing
 * - Error rendering when the API rejects
 * - "Run purge now" button confirms via window.confirm before POSTing
 * - Purge button is disabled when purged_count is 0
 * - Pin toggle calls /pin or /unpin then refreshes
 * - All fields render via textContent (no innerHTML / XSS)
 * - _switchTab('retention') routes _refreshCurrentTab to the retention loader
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MODULE_PATH = path.resolve(__dirname, '../../src/anteroom/static/js/memory.js');

const _CSS_POLYFILL = globalThis.CSS && typeof globalThis.CSS.escape === 'function'
    ? globalThis.CSS
    : { escape: s => String(s).replace(/([^\w-])/g, '\\$1') };

function loadMemoryModule() {
    const source = fs.readFileSync(MODULE_PATH, 'utf8');
    const module = { exports: {} };
    const fn = new Function(
        'window', 'document', 'console', 'fetch', 'URLSearchParams', 'CSS', 'module',
        source + '\nreturn module.exports;',
    );
    return fn(window, document, console, globalThis.fetch, URLSearchParams, _CSS_POLYFILL, module);
}

function _buildPanelShell() {
    document.body.innerHTML = `
        <button class="memory-tab active" data-tab="active">Active</button>
        <button class="memory-tab" data-tab="review">Review queue</button>
        <button class="memory-tab" data-tab="retention">Retention</button>
        <select id="memory-filter-scope"><option value=""></option></select>
        <select id="memory-filter-status"><option value=""></option></select>
        <select id="memory-filter-category"><option value=""></option></select>
        <input id="memory-filter-namespace" value="" />
        <div id="memory-list"></div>
        <div id="memory-detail" style="display:none"></div>
        <div id="memory-edit-form" style="display:none"></div>
        <div id="memory-create-form" style="display:none"></div>
    `;
}

function _makePreviewResult(overrides = {}) {
    return {
        dry_run: true,
        purged_count: 2,
        skipped_pinned_count: 1,
        items: [
            {
                fqn: '@user/memory/stale',
                reason: 'status',
                age_days: 45,
                last_recalled_at: '2026-01-01T00:00:00Z',
                recall_count: 3,
                status: 'rejected',
                pinned: false,
            },
            {
                fqn: '@user/memory/old',
                reason: 'max_age',
                age_days: 180,
                last_recalled_at: null,
                recall_count: 0,
                status: 'active',
                pinned: false,
            },
        ],
        ...overrides,
    };
}

let Mem;

beforeEach(() => {
    _buildPanelShell();
    Mem = loadMemoryModule();
    globalThis.App = { api: vi.fn() };
});

afterEach(() => {
    delete globalThis.App;
    vi.restoreAllMocks();
});

// ---------------------------------------------------------------------------
// _refreshRetentionPreview render
// ---------------------------------------------------------------------------

describe('_refreshRetentionPreview', () => {
    it('fetches /memory/retention-preview and renders rows', async () => {
        globalThis.App.api.mockResolvedValueOnce(_makePreviewResult());
        await Mem._refreshRetentionPreview();
        expect(globalThis.App.api.mock.calls[0][0]).toBe('/memory/retention-preview');
        const rows = document.querySelectorAll('.memory-retention-item');
        expect(rows.length).toBe(2);
    });

    it('renders the summary header with the would-be-purged count', async () => {
        globalThis.App.api.mockResolvedValueOnce(_makePreviewResult({ purged_count: 5, skipped_pinned_count: 0 }));
        await Mem._refreshRetentionPreview();
        const summary = document.querySelector('.memory-retention-summary');
        expect(summary.textContent).toContain('5 memory(ies) would be purged');
    });

    it('renders empty state when nothing matches', async () => {
        globalThis.App.api.mockResolvedValueOnce({
            dry_run: true,
            purged_count: 0,
            skipped_pinned_count: 0,
            items: [],
        });
        await Mem._refreshRetentionPreview();
        const empty = document.querySelector('.memory-empty');
        expect(empty).toBeTruthy();
        expect(empty.textContent).toContain('No memories match');
        const purgeBtn = document.querySelector('.memory-retention-purge');
        expect(purgeBtn.disabled).toBe(true);
    });

    it('renders error state when API rejects', async () => {
        globalThis.App.api.mockRejectedValueOnce(new Error('retention boom'));
        await Mem._refreshRetentionPreview();
        const err = document.querySelector('.memory-error');
        expect(err).toBeTruthy();
        expect(err.textContent).toContain('retention boom');
    });

    it('renders FQN and reason via textContent (no XSS)', async () => {
        const hostile = _makePreviewResult({
            items: [
                {
                    fqn: '<script>alert(1)</script>',
                    reason: 'status',
                    age_days: 10,
                    last_recalled_at: null,
                    recall_count: 0,
                    status: 'rejected',
                    pinned: false,
                },
            ],
            purged_count: 1,
            skipped_pinned_count: 0,
        });
        globalThis.App.api.mockResolvedValueOnce(hostile);
        await Mem._refreshRetentionPreview();
        const title = document.querySelector('.memory-retention-item .memory-item-title');
        expect(title.textContent).toBe('<script>alert(1)</script>');
        expect(document.querySelector('script')).toBeNull();
    });

    it('marks pinned items with a pinned badge', async () => {
        const withPinned = _makePreviewResult({
            items: [
                {
                    fqn: '@user/memory/pinned',
                    reason: 'status',
                    age_days: 10,
                    last_recalled_at: null,
                    recall_count: 0,
                    status: 'rejected',
                    pinned: true,
                },
            ],
            purged_count: 0,
            skipped_pinned_count: 1,
        });
        globalThis.App.api.mockResolvedValueOnce(withPinned);
        await Mem._refreshRetentionPreview();
        const row = document.querySelector('.memory-retention-item');
        expect(row.textContent).toContain('pinned');
    });
});

// ---------------------------------------------------------------------------
// Purge-confirmation guard
// ---------------------------------------------------------------------------

describe('_confirmAndRunPurge', () => {
    it('does not POST when user cancels the confirm dialog', async () => {
        const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(false);
        await Mem._confirmAndRunPurge(3);
        expect(confirmSpy).toHaveBeenCalled();
        expect(globalThis.App.api).not.toHaveBeenCalled();
    });

    it('POSTs to /retention-purge with confirm=true when user confirms', async () => {
        vi.spyOn(window, 'confirm').mockReturnValue(true);
        vi.spyOn(window, 'alert').mockImplementation(() => { });
        globalThis.App.api.mockResolvedValueOnce({ purged_count: 3, dry_run: false, skipped_pinned_count: 0, items: [] });
        globalThis.App.api.mockResolvedValueOnce({ dry_run: true, purged_count: 0, skipped_pinned_count: 0, items: [] });
        await Mem._confirmAndRunPurge(3);
        const call = globalThis.App.api.mock.calls[0];
        expect(call[0]).toBe('/memory/retention-purge');
        expect(call[1].method).toBe('POST');
        expect(JSON.parse(call[1].body)).toEqual({ confirm: true });
    });

    it('surfaces API errors through alert', async () => {
        vi.spyOn(window, 'confirm').mockReturnValue(true);
        const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });
        globalThis.App.api.mockRejectedValueOnce(new Error('purge failed'));
        await Mem._confirmAndRunPurge(2);
        expect(alertSpy).toHaveBeenCalled();
        const msg = alertSpy.mock.calls.find(c => String(c[0]).includes('Purge failed'));
        expect(msg).toBeTruthy();
    });

    it('surfaces the reviewer identity in the success alert when present', async () => {
        vi.spyOn(window, 'confirm').mockReturnValue(true);
        const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });
        globalThis.App.api.mockResolvedValueOnce({
            purged_count: 2,
            dry_run: false,
            skipped_pinned_count: 0,
            items: [],
            purged_by: 'alice-session-uid',
        });
        globalThis.App.api.mockResolvedValueOnce({
            dry_run: true,
            purged_count: 0,
            skipped_pinned_count: 0,
            items: [],
            purged_by: null,
        });
        await Mem._confirmAndRunPurge(2);
        const successMsg = alertSpy.mock.calls.find(c => String(c[0]).includes('Purged'));
        expect(successMsg).toBeTruthy();
        expect(String(successMsg[0])).toContain('alice-session-uid');
    });

    it('omits the "by <reviewer>" phrase when purged_by is null', async () => {
        vi.spyOn(window, 'confirm').mockReturnValue(true);
        const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => { });
        globalThis.App.api.mockResolvedValueOnce({
            purged_count: 1,
            dry_run: false,
            skipped_pinned_count: 0,
            items: [],
            purged_by: null,
        });
        globalThis.App.api.mockResolvedValueOnce({
            dry_run: true,
            purged_count: 0,
            skipped_pinned_count: 0,
            items: [],
            purged_by: null,
        });
        await Mem._confirmAndRunPurge(1);
        const successMsg = alertSpy.mock.calls.find(c => String(c[0]).includes('Purged'));
        expect(successMsg).toBeTruthy();
        expect(String(successMsg[0])).not.toContain(' by ');
    });
});

// ---------------------------------------------------------------------------
// togglePin
// ---------------------------------------------------------------------------

describe('togglePin', () => {
    it('POSTs to /pin when the memory is not pinned', async () => {
        globalThis.App.api.mockResolvedValueOnce({});
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem.togglePin('@user/memory/target', false);
        const call = globalThis.App.api.mock.calls[0];
        expect(call[0]).toBe('/memory/@user/memory/target/pin');
        expect(call[1].method).toBe('POST');
    });

    it('POSTs to /unpin when the memory is already pinned', async () => {
        globalThis.App.api.mockResolvedValueOnce({});
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem.togglePin('@user/memory/target', true);
        const call = globalThis.App.api.mock.calls[0];
        expect(call[0]).toBe('/memory/@user/memory/target/unpin');
    });
});

// ---------------------------------------------------------------------------
// Tab routing
// ---------------------------------------------------------------------------

describe('_switchTab routes to retention loader', () => {
    it('_switchTab("retention") triggers a /retention-preview fetch', async () => {
        globalThis.App.api.mockResolvedValue({
            dry_run: true,
            purged_count: 0,
            skipped_pinned_count: 0,
            items: [],
        });
        await Mem._switchTab('retention');
        // _switchTab is sync, but the refresh it kicks off is async; give
        // microtasks a tick to run.
        await Promise.resolve();
        await Promise.resolve();
        const retentionCalls = globalThis.App.api.mock.calls.filter(c => c[0] === '/memory/retention-preview');
        expect(retentionCalls.length).toBeGreaterThanOrEqual(1);
    });
});
