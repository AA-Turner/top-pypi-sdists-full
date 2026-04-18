/**
 * JS unit tests for the memory review-queue tab (#920).
 *
 * Exercises the new review surface on top of the #1416 memory panel:
 * - Review tab renders candidate items with approve / edit-and-approve / reject buttons
 * - Approve click POSTs to /api/memory/{fqn}/approve and refreshes
 * - Reject form validates non-empty reason, then POSTs to .../reject
 * - Edit-and-approve form requires non-empty edited content, then POSTs to .../edit-and-approve
 * - Tab switch routes _refreshCurrentTab to the right loader
 * - All user-supplied strings render via textContent (no innerHTML)
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MODULE_PATH = path.resolve(__dirname, '../../src/anteroom/static/js/memory.js');

// jsdom may not expose `CSS.escape`; polyfill a minimal version for tests.
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

let Mem;

function _buildPanelShell() {
    document.body.innerHTML = `
        <button class="memory-tab active" data-tab="active">Active</button>
        <button class="memory-tab" data-tab="review">Review queue</button>
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

function _makeCandidate(overrides = {}) {
    return {
        id: 'id-1',
        fqn: '@user/memory/sample',
        name: 'sample',
        namespace: 'user',
        content: 'pending candidate content',
        created_at: '2026-04-17T00:00:00Z',
        metadata: {
            memory_scope: 'user',
            memory_category: 'preference',
            memory_status: 'candidate',
        },
        ...overrides,
    };
}

beforeEach(() => {
    _buildPanelShell();
    Mem = loadMemoryModule();
    globalThis.App = { api: vi.fn() };
});

afterEach(() => {
    delete globalThis.App;
});

// ---------------------------------------------------------------------------
// Review queue render
// ---------------------------------------------------------------------------

describe('_refreshReviewQueue', () => {
    it('fetches /memory/candidates and renders empty state', async () => {
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem._refreshReviewQueue();
        expect(globalThis.App.api.mock.calls[0][0]).toBe('/memory/candidates');
        expect(document.querySelector('.memory-empty').textContent).toContain('No pending candidates');
    });

    it('renders one row per candidate with three action buttons each', async () => {
        globalThis.App.api.mockResolvedValueOnce([_makeCandidate(), _makeCandidate({ fqn: '@user/memory/two', name: 'two' })]);
        await Mem._refreshReviewQueue();
        const rows = document.querySelectorAll('.memory-review-item');
        expect(rows.length).toBe(2);
        rows.forEach(row => {
            expect(row.querySelector('.memory-review-approve')).toBeTruthy();
            expect(row.querySelector('.memory-review-edit-approve')).toBeTruthy();
            expect(row.querySelector('.memory-review-reject')).toBeTruthy();
        });
    });

    it('renders error state when API rejects', async () => {
        globalThis.App.api.mockRejectedValueOnce(new Error('queue boom'));
        await Mem._refreshReviewQueue();
        const err = document.querySelector('.memory-error');
        expect(err).toBeTruthy();
        expect(err.textContent).toContain('queue boom');
    });

    it('renders candidate content via textContent (no XSS)', async () => {
        const hostile = _makeCandidate({ content: '<script>evil()</script>' });
        globalThis.App.api.mockResolvedValueOnce([hostile]);
        await Mem._refreshReviewQueue();
        const preview = document.querySelector('.memory-item-preview');
        expect(preview.textContent).toBe('<script>evil()</script>');
        expect(document.querySelector('script')).toBeNull();
    });
});

// ---------------------------------------------------------------------------
// Approve flow
// ---------------------------------------------------------------------------

describe('_approveCandidate', () => {
    it('POSTs to /approve and refreshes the queue', async () => {
        const cand = _makeCandidate();
        // One call for list, one for approve, one for refresh.
        globalThis.App.api.mockResolvedValueOnce([cand])
                          .mockResolvedValueOnce({})
                          .mockResolvedValueOnce([]);
        await Mem._refreshReviewQueue();
        await Mem._approveCandidate(cand.fqn);
        const approveCall = globalThis.App.api.mock.calls[1];
        expect(approveCall[0]).toBe('/memory/@user/memory/sample/approve');
        expect(approveCall[1].method).toBe('POST');
    });

    it('POSTs to /edit-and-approve when edits are supplied', async () => {
        globalThis.App.api.mockResolvedValueOnce({}).mockResolvedValueOnce([]);
        // Skip list render to shorten the setup — render one item manually.
        const cand = _makeCandidate();
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        await Mem._approveCandidate(cand.fqn, { content: 'refined body' });
        const call = globalThis.App.api.mock.calls[0];
        expect(call[0]).toBe('/memory/@user/memory/sample/edit-and-approve');
        expect(JSON.parse(call[1].body)).toEqual({ edits: { content: 'refined body' } });
    });

    it('renders inline error on failed approve', async () => {
        const cand = _makeCandidate();
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        globalThis.App.api.mockRejectedValueOnce(new Error('409 conflict'));
        await Mem._approveCandidate(cand.fqn);
        const err = document.querySelector('.memory-review-item .memory-error');
        expect(err).toBeTruthy();
        expect(err.textContent).toContain('409 conflict');
    });
});

// ---------------------------------------------------------------------------
// Reject flow
// ---------------------------------------------------------------------------

describe('_showRejectForm', () => {
    it('opens a form with a reason textarea and submit button', () => {
        const cand = _makeCandidate();
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        Mem._showRejectForm(cand);
        const form = document.querySelector('.memory-reject-form');
        expect(form).toBeTruthy();
        expect(form.querySelector('.memory-reject-reason')).toBeTruthy();
    });

    it('blocks submit when reason is blank', async () => {
        const cand = _makeCandidate();
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        Mem._showRejectForm(cand);
        // Leave the textarea empty and click submit.
        const form = document.querySelector('.memory-reject-form');
        const submitBtn = form.querySelector('button');
        submitBtn.click();
        // Micro-delay so the handler runs.
        await Promise.resolve();
        expect(globalThis.App.api).not.toHaveBeenCalled();
        expect(document.querySelector('.memory-error').textContent).toContain('required');
    });

    it('POSTs to /reject with the reason when provided', async () => {
        const cand = _makeCandidate();
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        Mem._showRejectForm(cand);
        const reason = document.querySelector('.memory-reject-reason');
        reason.value = 'Not useful';
        globalThis.App.api.mockResolvedValueOnce({}).mockResolvedValueOnce([]);
        const submitBtn = document.querySelector('.memory-reject-form button');
        submitBtn.click();
        await new Promise(resolve => setTimeout(resolve, 0));
        const call = globalThis.App.api.mock.calls[0];
        expect(call[0]).toBe('/memory/@user/memory/sample/reject');
        expect(JSON.parse(call[1].body)).toEqual({ reason: 'Not useful' });
    });
});

// ---------------------------------------------------------------------------
// Edit-and-approve flow
// ---------------------------------------------------------------------------

describe('_showEditAndApproveForm', () => {
    it('pre-populates the textarea with the candidate content', () => {
        const cand = _makeCandidate({ content: 'original content' });
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        Mem._showEditAndApproveForm(cand);
        const ta = document.querySelector('.memory-edit-approve-content');
        expect(ta.value).toBe('original content');
    });

    it('blocks submit when the textarea is emptied', async () => {
        const cand = _makeCandidate();
        document.getElementById('memory-list').appendChild(Mem._buildReviewItem(cand));
        Mem._showEditAndApproveForm(cand);
        document.querySelector('.memory-edit-approve-content').value = '   ';
        document.querySelector('.memory-edit-approve-form button').click();
        await new Promise(resolve => setTimeout(resolve, 0));
        expect(globalThis.App.api).not.toHaveBeenCalled();
    });
});

// ---------------------------------------------------------------------------
// Tab switching
// ---------------------------------------------------------------------------

describe('_switchTab', () => {
    it('routes the active tab to _refreshList', async () => {
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem._switchTab('active');
        const firstArg = globalThis.App.api.mock.calls[0][0];
        expect(firstArg).toMatch(/^\/memory(\?.*)?$/);
    });

    it('routes the review tab to _refreshReviewQueue', async () => {
        globalThis.App.api.mockResolvedValueOnce([]);
        await Mem._switchTab('review');
        expect(globalThis.App.api.mock.calls[0][0]).toBe('/memory/candidates');
    });
});
