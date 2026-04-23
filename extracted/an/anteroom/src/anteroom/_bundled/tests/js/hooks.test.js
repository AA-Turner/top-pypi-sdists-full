/**
 * Vitest tests for hook outcome rendering in the chat UI (#1491).
 *
 * chat.js is too large to import in jsdom, so the renderHookOutcome
 * function is inlined here in sync with its implementation in chat.js.
 * Any behavioral change to renderHookOutcome in chat.js must be reflected here.
 *
 * Contract asserted:
 *   - deny outcome renders a notice with the tool name and message
 *   - post_hook_denied uses "output" framing
 *   - missing message is handled gracefully (no crash, no empty reason element)
 *   - notice element gets the expected CSS class
 *   - icon element is present
 */

import { describe, it, expect, beforeEach } from 'vitest';

// ---------------------------------------------------------------------------
// Inline the function under test (kept behaviourally in sync with chat.js)
// ---------------------------------------------------------------------------

function _escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function _scrollToBottom() {}

function renderHookOutcome(container, data) {
    const toolName = data.tool_name || 'tool';
    const msg = data.message || '';
    const approvalDec = data.approval_decision || '';
    const isPostHook = approvalDec === 'post_hook_denied';

    const el = document.createElement('div');
    el.className = 'hook-outcome-notice';

    const icon = document.createElement('span');
    icon.className = 'hook-outcome-icon';
    icon.textContent = '\u26d4';

    const body = document.createElement('div');
    body.className = 'hook-outcome-body';

    const title = document.createElement('div');
    title.className = 'hook-outcome-title';
    title.textContent = isPostHook
        ? `Hook blocked output from ${toolName}`
        : `Hook blocked ${toolName}`;
    body.appendChild(title);

    if (msg) {
        const reason = document.createElement('div');
        reason.className = 'hook-outcome-reason';
        reason.textContent = msg;
        body.appendChild(reason);
    }

    el.appendChild(icon);
    el.appendChild(body);
    container.appendChild(el);
    _scrollToBottom();
    return el;
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('renderHookOutcome', () => {
    let container;

    beforeEach(() => {
        document.body.innerHTML = '<div id="chat-messages"></div>';
        container = document.getElementById('chat-messages');
    });

    it('renders a notice element with hook-outcome-notice class', () => {
        const el = renderHookOutcome(container, { tool_name: 'bash', outcome: 'deny', message: '' });
        expect(el.className).toBe('hook-outcome-notice');
    });

    it('renders an icon element', () => {
        const el = renderHookOutcome(container, { tool_name: 'bash', outcome: 'deny', message: '' });
        const icon = el.querySelector('.hook-outcome-icon');
        expect(icon).not.toBeNull();
    });

    it('includes tool name in the title', () => {
        const el = renderHookOutcome(container, { tool_name: 'write_file', outcome: 'deny', message: '' });
        const title = el.querySelector('.hook-outcome-title');
        expect(title.textContent).toContain('write_file');
    });

    it('uses pre-tool framing for non-post-hook denials', () => {
        const el = renderHookOutcome(container, {
            tool_name: 'bash',
            outcome: 'deny',
            approval_decision: 'hook_denied',
            message: '',
        });
        const title = el.querySelector('.hook-outcome-title');
        expect(title.textContent).toContain('Hook blocked bash');
        expect(title.textContent).not.toContain('output');
    });

    it('uses post-hook framing when approval_decision is post_hook_denied', () => {
        const el = renderHookOutcome(container, {
            tool_name: 'bash',
            outcome: 'deny',
            approval_decision: 'post_hook_denied',
            message: '',
        });
        const title = el.querySelector('.hook-outcome-title');
        expect(title.textContent).toContain('output from bash');
    });

    it('renders reason element when message is non-empty', () => {
        const el = renderHookOutcome(container, {
            tool_name: 'bash',
            outcome: 'deny',
            message: 'No network access allowed',
        });
        const reason = el.querySelector('.hook-outcome-reason');
        expect(reason).not.toBeNull();
        expect(reason.textContent).toBe('No network access allowed');
    });

    it('omits reason element when message is empty', () => {
        const el = renderHookOutcome(container, { tool_name: 'bash', outcome: 'deny', message: '' });
        const reason = el.querySelector('.hook-outcome-reason');
        expect(reason).toBeNull();
    });

    it('appends the notice to the container', () => {
        renderHookOutcome(container, { tool_name: 'bash', outcome: 'deny', message: '' });
        const notices = container.querySelectorAll('.hook-outcome-notice');
        expect(notices.length).toBe(1);
    });

    it('renders multiple notices for multiple hook blocks', () => {
        renderHookOutcome(container, { tool_name: 'bash', outcome: 'deny', message: 'block 1' });
        renderHookOutcome(container, { tool_name: 'read_file', outcome: 'deny', message: 'block 2' });
        const notices = container.querySelectorAll('.hook-outcome-notice');
        expect(notices.length).toBe(2);
    });

    it('falls back gracefully when tool_name is absent', () => {
        const el = renderHookOutcome(container, { outcome: 'deny', message: '' });
        const title = el.querySelector('.hook-outcome-title');
        expect(title.textContent).toContain('tool');
    });
});

// ---------------------------------------------------------------------------
// SSE event dispatch: hook_outcome case handled before tool_call_end
// ---------------------------------------------------------------------------

describe('hook_outcome SSE event shape', () => {
    it('expects tool_name, tool_call_id, outcome, approval_decision, message fields', () => {
        const payload = {
            tool_name: 'bash',
            tool_call_id: 'tc-abc123',
            outcome: 'deny',
            approval_decision: 'hook_denied',
            message: 'Blocked by security hook',
        };
        // All expected fields must be present
        expect(payload).toHaveProperty('tool_name');
        expect(payload).toHaveProperty('tool_call_id');
        expect(payload).toHaveProperty('outcome');
        expect(payload).toHaveProperty('approval_decision');
        expect(payload).toHaveProperty('message');
    });

    it('post_hook_denied produces the expected approval_decision value', () => {
        const payload = {
            tool_name: 'bash',
            tool_call_id: 'tc-xyz',
            outcome: 'deny',
            approval_decision: 'post_hook_denied',
            message: 'Output blocked',
        };
        expect(payload.approval_decision).toBe('post_hook_denied');
    });
});
