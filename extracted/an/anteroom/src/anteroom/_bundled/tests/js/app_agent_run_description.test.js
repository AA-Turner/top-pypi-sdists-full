/**
 * JS unit tests for the agent_run_completed description-label fix (#1461).
 *
 * app.js is too heavy to import in jsdom (top-level EventSource/DOM globals),
 * so this follows the established project convention of inlining only the
 * logic under test. Keep this copy behaviourally in sync with the
 * ``agent_run_completed`` SSE handler in
 * ``src/anteroom/static/js/app.js``.
 *
 * The contract asserted here:
 *   - On agent_run_completed, prefer data.description over data.summary for
 *     the chip label (same label-preference as agent_run_started).
 *   - When description is absent, fall back to summary, then empty string.
 *   - The chip title text rendered by renderDetachedChip reflects the chosen
 *     label throughout the full status flow.
 */

import { describe, it, expect, beforeEach } from 'vitest';

// ---- Inline copy of renderDetachedChip from chat.js ----
// Must stay behaviourally in sync with the source.

function _escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function renderDetachedChip(runId, text, status) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    const chipId = `detached-${runId.slice(0, 8)}`;
    let chip = document.getElementById(chipId);
    if (!chip) {
        chip = document.createElement('div');
        chip.id = chipId;
        chip.className = 'tool-call detached-agent-chip';
        const summary = document.createElement('div');
        summary.className = 'tool-summary';
        chip.appendChild(summary);
        chatMessages.appendChild(chip);
    }
    const summary = chip.querySelector('.tool-summary');
    if (status === 'running') {
        summary.innerHTML = `<span class="tool-spinner"></span> Agent: <code>${_escapeHtml(text || '')}</code>`;
    } else {
        const icon = (status === 'completed') ? '\u2713' : '\u2717';
        const cls = (status === 'completed') ? 'tool-status-success' : 'tool-status-error';
        chip.classList.add(cls);
        summary.innerHTML = `<span>${icon}</span> Agent ${runId.slice(0, 8)}: ${status} \u2014 ${_escapeHtml(text || '')}`;
    }
}

// ---- Inline copy of the agent_run_completed handler label logic from app.js ----
// The ONLY change from the pre-fix version is: prefer data.description over data.summary.

function handleAgentRunCompleted(data) {
    // Fix (#1461): prefer description (stable label set at launch) over summary.
    const label = data.description || data.summary || '';
    renderDetachedChip(data.run_id, label, data.status);
}

function handleAgentRunStarted(data) {
    const label = data.description || data.prompt || '';
    renderDetachedChip(data.run_id, label, 'running');
}

// ---- Tests ----

beforeEach(() => {
    document.body.innerHTML = '<div id="chat-messages"></div>';
});

describe('agent_run_completed label preference (#1461)', () => {
    it('uses description over summary when both are present', () => {
        handleAgentRunCompleted({
            run_id: 'aabbccdd11223344',
            status: 'completed',
            description: 'Deploy health check',
            summary: 'All services healthy.',
        });
        const chip = document.getElementById('detached-aabbccdd');
        expect(chip).toBeTruthy();
        expect(chip.querySelector('.tool-summary').textContent).toContain('Deploy health check');
        expect(chip.querySelector('.tool-summary').textContent).not.toContain('All services healthy.');
    });

    it('falls back to summary when description is absent', () => {
        handleAgentRunCompleted({
            run_id: 'bbccddee22334455',
            status: 'completed',
            summary: 'Quarterly report summarised.',
        });
        const chip = document.getElementById('detached-bbccddee');
        expect(chip).toBeTruthy();
        expect(chip.querySelector('.tool-summary').textContent).toContain('Quarterly report summarised.');
    });

    it('renders empty label gracefully when neither description nor summary is present', () => {
        handleAgentRunCompleted({
            run_id: 'ccddeeff33445566',
            status: 'completed',
        });
        const chip = document.getElementById('detached-ccddeeff');
        expect(chip).toBeTruthy();
        // Should not throw; chip renders with status but empty label.
        expect(chip.querySelector('.tool-summary').textContent).toContain('completed');
    });

    it('preserves description label through the full started → completed flow', () => {
        const runId = 'ddeeff0044556677';

        // started: chip created with description label
        handleAgentRunStarted({
            run_id: runId,
            description: 'Nightly lint sweep',
            prompt: 'Run lint across the repo and report failures.',
        });
        const chip = document.getElementById(`detached-${runId.slice(0, 8)}`);
        expect(chip).toBeTruthy();
        expect(chip.querySelector('.tool-summary').textContent).toContain('Nightly lint sweep');
        expect(chip.querySelector('.tool-summary').textContent).not.toContain('Run lint across');

        // completed: same chip updated — description must still be the label
        handleAgentRunCompleted({
            run_id: runId,
            status: 'completed',
            description: 'Nightly lint sweep',
            summary: 'No lint errors found.',
        });
        expect(chip.querySelector('.tool-summary').textContent).toContain('Nightly lint sweep');
        expect(chip.querySelector('.tool-summary').textContent).not.toContain('No lint errors found.');
    });

    it('applies tool-status-success class on completed status', () => {
        handleAgentRunCompleted({
            run_id: 'eeff001155667788',
            status: 'completed',
            description: 'CI check',
        });
        const chip = document.getElementById('detached-eeff0011');
        expect(chip.classList.contains('tool-status-success')).toBe(true);
    });

    it('applies tool-status-error class on failed status', () => {
        handleAgentRunCompleted({
            run_id: 'ff00112266778899',
            status: 'failed',
            description: 'Deploy pipeline',
            summary: 'Timeout during deploy.',
        });
        const chip = document.getElementById('detached-ff001122');
        expect(chip.classList.contains('tool-status-error')).toBe(true);
        // description takes precedence over summary even for failure
        expect(chip.querySelector('.tool-summary').textContent).toContain('Deploy pipeline');
    });
});
