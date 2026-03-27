/**
 * JS unit tests for workflows panel logic (#961).
 *
 * Since workflows.js is an IIFE, we reproduce key logic functions
 * inline for testing (same pattern as approval.test.js).
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';

// ---------------------------------------------------------------------------
// Reproduce _escapeHtml from workflows.js
// ---------------------------------------------------------------------------
function _escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ---------------------------------------------------------------------------
// Reproduce _relativeTime from workflows.js
// ---------------------------------------------------------------------------
function _relativeTime(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const now = Date.now();
    const diff = now - d.getTime();
    if (diff < 60000) return 'just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return `${Math.floor(diff / 86400000)}d ago`;
}

// ---------------------------------------------------------------------------
// Reproduce _statusBadge from workflows.js
// ---------------------------------------------------------------------------
function _statusBadge(status) {
    const colors = {
        pending: '#9e9e9e', claimed: '#2196f3', running: '#2196f3',
        paused: '#ff9800', waiting_for_approval: '#ff9800', waiting_for_input: '#ff9800',
        completed: '#4caf50', failed: '#f44336', cancelled: '#9e9e9e', blocked: '#9e9e9e',
    };
    const color = colors[status] || '#9e9e9e';
    return `<span class="wf-status-badge" style="background:${color}">${_escapeHtml(status)}</span>`;
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('_escapeHtml', () => {
    it('escapes angle brackets', () => {
        expect(_escapeHtml('<script>alert("xss")</script>')).toBe(
            '&lt;script&gt;alert("xss")&lt;/script&gt;'
        );
    });

    it('escapes ampersands', () => {
        expect(_escapeHtml('a & b')).toBe('a &amp; b');
    });

    it('returns empty string for empty input', () => {
        expect(_escapeHtml('')).toBe('');
    });

    it('passes through plain text', () => {
        expect(_escapeHtml('hello world')).toBe('hello world');
    });
});

describe('_relativeTime', () => {
    it('returns empty string for null/undefined', () => {
        expect(_relativeTime(null)).toBe('');
        expect(_relativeTime(undefined)).toBe('');
    });

    it('returns "just now" for recent timestamps', () => {
        const now = new Date().toISOString();
        expect(_relativeTime(now)).toBe('just now');
    });

    it('returns minutes for times within an hour', () => {
        const fiveMinAgo = new Date(Date.now() - 5 * 60 * 1000).toISOString();
        expect(_relativeTime(fiveMinAgo)).toBe('5m ago');
    });

    it('returns hours for times within a day', () => {
        const twoHoursAgo = new Date(Date.now() - 2 * 3600 * 1000).toISOString();
        expect(_relativeTime(twoHoursAgo)).toBe('2h ago');
    });

    it('returns days for older timestamps', () => {
        const threeDaysAgo = new Date(Date.now() - 3 * 86400 * 1000).toISOString();
        expect(_relativeTime(threeDaysAgo)).toBe('3d ago');
    });
});

describe('_statusBadge', () => {
    it('renders a badge with correct status text', () => {
        const badge = _statusBadge('running');
        expect(badge).toContain('running');
        expect(badge).toContain('wf-status-badge');
    });

    it('uses green for completed', () => {
        const badge = _statusBadge('completed');
        expect(badge).toContain('#4caf50');
    });

    it('uses red for failed', () => {
        const badge = _statusBadge('failed');
        expect(badge).toContain('#f44336');
    });

    it('uses blue for running', () => {
        const badge = _statusBadge('running');
        expect(badge).toContain('#2196f3');
    });

    it('uses yellow for waiting_for_approval', () => {
        const badge = _statusBadge('waiting_for_approval');
        expect(badge).toContain('#ff9800');
    });

    it('uses gray for unknown status', () => {
        const badge = _statusBadge('something_unknown');
        expect(badge).toContain('#9e9e9e');
    });

    it('escapes HTML in status text', () => {
        const badge = _statusBadge('<img onerror=alert(1)>');
        expect(badge).not.toContain('<img');
        expect(badge).toContain('&lt;img');
    });
});

describe('panel DOM behavior', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div class="chat-main">
                <aside id="workflows-panel" style="display:none">
                    <div class="workflows-list" id="workflows-list"></div>
                    <div class="workflows-detail" id="workflows-detail" style="display:none"></div>
                    <select id="workflows-status-filter">
                        <option value="">All</option>
                        <option value="running">Running</option>
                    </select>
                </aside>
                <button id="btn-workflows-toggle"></button>
                <button id="workflows-close"></button>
            </div>
        `;
    });

    it('panel is hidden by default', () => {
        const panel = document.getElementById('workflows-panel');
        expect(panel.style.display).toBe('none');
    });

    it('list container exists', () => {
        const list = document.getElementById('workflows-list');
        expect(list).not.toBeNull();
    });

    it('detail container is hidden by default', () => {
        const detail = document.getElementById('workflows-detail');
        expect(detail.style.display).toBe('none');
    });

    it('status filter has options', () => {
        const select = document.getElementById('workflows-status-filter');
        expect(select.options.length).toBeGreaterThanOrEqual(2);
    });
});

describe('list/detail view transitions', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div class="chat-main">
                <aside id="workflows-panel" style="display:none">
                    <div class="workflows-list" id="workflows-list"></div>
                    <div class="workflows-detail" id="workflows-detail" style="display:none"></div>
                </aside>
            </div>
        `;
    });

    it('switching to detail hides list and shows detail', () => {
        const list = document.getElementById('workflows-list');
        const detail = document.getElementById('workflows-detail');

        // Simulate detail view transition
        list.style.display = 'none';
        detail.style.display = '';

        expect(list.style.display).toBe('none');
        expect(detail.style.display).toBe('');
    });

    it('switching back to list shows list and hides detail', () => {
        const list = document.getElementById('workflows-list');
        const detail = document.getElementById('workflows-detail');

        // Start in detail view
        list.style.display = 'none';
        detail.style.display = '';

        // Switch back
        list.style.display = '';
        detail.style.display = 'none';

        expect(list.style.display).toBe('');
        expect(detail.style.display).toBe('none');
    });
});

describe('run card rendering', () => {
    it('renders run card HTML with status and workflow', () => {
        const run = {
            id: 'run-1',
            workflow_id: 'deploy',
            status: 'completed',
            created_at: new Date().toISOString(),
        };

        const html = `
            <div class="wf-run-card" data-run-id="${_escapeHtml(run.id)}">
                <div class="wf-run-card-header">
                    ${_statusBadge(run.status)}
                    <span class="wf-run-workflow">${_escapeHtml(run.workflow_id)}</span>
                </div>
            </div>
        `;

        document.body.innerHTML = html;
        const card = document.querySelector('.wf-run-card');
        expect(card).not.toBeNull();
        expect(card.dataset.runId).toBe('run-1');
        expect(card.querySelector('.wf-run-workflow').textContent).toBe('deploy');
        expect(card.querySelector('.wf-status-badge').textContent).toBe('completed');
    });

    it('escapes XSS in run data', () => {
        const run = {
            id: '<script>',
            workflow_id: '<img onerror=alert(1)>',
            status: 'running',
            created_at: new Date().toISOString(),
        };

        const html = `
            <div class="wf-run-card" data-run-id="${_escapeHtml(run.id)}">
                <span class="wf-run-workflow">${_escapeHtml(run.workflow_id)}</span>
            </div>
        `;

        document.body.innerHTML = html;
        const card = document.querySelector('.wf-run-card');
        expect(card.innerHTML).not.toContain('<script>');
        expect(card.innerHTML).not.toContain('<img');
    });
});

describe('detail view rendering', () => {
    it('renders step timeline with correct structure', () => {
        const steps = [
            { step_id: 'lint', result_status: 'success', duration_ms: 5000 },
            { step_id: 'test', result_status: 'failed', duration_ms: 12000 },
        ];

        const stepsHtml = steps.map(step => {
            const statusColor = step.result_status === 'success' ? '#4caf50' : '#f44336';
            return `
                <div class="wf-step">
                    <span class="wf-step-dot" style="background:${statusColor}"></span>
                    <div class="wf-step-info">
                        <span class="wf-step-id">${_escapeHtml(step.step_id)}</span>
                        <span class="wf-step-status">${_escapeHtml(step.result_status)}</span>
                        <span class="wf-step-duration">${(step.duration_ms / 1000).toFixed(1)}s</span>
                    </div>
                </div>
            `;
        }).join('');

        document.body.innerHTML = `<div class="wf-step-timeline">${stepsHtml}</div>`;

        const timeline = document.querySelector('.wf-step-timeline');
        expect(timeline).not.toBeNull();

        const stepEls = document.querySelectorAll('.wf-step');
        expect(stepEls.length).toBe(2);

        const ids = Array.from(document.querySelectorAll('.wf-step-id')).map(el => el.textContent);
        expect(ids).toEqual(['lint', 'test']);

        // Check color coding
        const dots = document.querySelectorAll('.wf-step-dot');
        expect(dots[0].style.background).toBe('rgb(76, 175, 80)');  // green
        expect(dots[1].style.background).toBe('rgb(244, 67, 54)');  // red

        // Check duration formatting
        const durations = Array.from(document.querySelectorAll('.wf-step-duration')).map(el => el.textContent);
        expect(durations).toEqual(['5.0s', '12.0s']);
    });

    it('renders back button', () => {
        document.body.innerHTML = `
            <div class="wf-detail-header">
                <button class="wf-back-btn" id="wf-back-btn">&larr; Back</button>
                ${_statusBadge('completed')}
                <span class="wf-detail-workflow">deploy</span>
            </div>
        `;

        const backBtn = document.getElementById('wf-back-btn');
        expect(backBtn).not.toBeNull();
        expect(document.querySelector('.wf-detail-workflow').textContent).toBe('deploy');
    });
});
