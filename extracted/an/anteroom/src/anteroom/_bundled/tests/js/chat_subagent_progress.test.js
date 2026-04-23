/**
 * JS unit tests for the chat.js live sub-agent progress contract (#1460).
 *
 * chat.js is too heavy to import in jsdom (2600+ lines of top-level state),
 * so this follows the existing project convention of inlining the logic
 * under test. Keep this copy behaviourally in sync with
 * ``renderSubagentEvent`` in ``src/anteroom/static/js/chat.js``.
 *
 * The contract asserted here:
 *   - one card per ``agent_id``, reused across frames (no duplicates)
 *   - ``tool_call_start`` updates the same card in place
 *   - ``subagent_end`` attaches a terminal-state class (completed/failed/cancelled)
 *     and a footer with duration + summary/error preview
 */

import { describe, it, expect, beforeEach } from 'vitest';

function _sanitizeId(id) {
    return String(id || '').replace(/[^a-zA-Z0-9_-]/g, '_');
}

function _resolveSubagentParent(defaultContainer, data, card) {
    const explicitParentId = data.parent_tool_call_id
        ? `tool-${_sanitizeId(data.parent_tool_call_id)}`
        : '';
    if (explicitParentId) {
        const explicitParent = document.getElementById(explicitParentId);
        if (explicitParent) {
            return explicitParent.querySelector('.subagent-cards-container') || defaultContainer;
        }
    }

    const cardParentId = card && card.dataset ? card.dataset.parentToolCallId : '';
    if (cardParentId) {
        const cardParent = document.getElementById(cardParentId);
        if (cardParent) {
            return cardParent.querySelector('.subagent-cards-container') || defaultContainer;
        }
    }

    return defaultContainer;
}

function renderSubagentEvent(container, data) {
    const kind = data.kind;
    const agentId = data.agent_id;
    const cardId = `subagent-${_sanitizeId(agentId)}`;
    const existingCard = document.getElementById(cardId);

    if (kind === 'subagent_start') {
        let card = document.getElementById(cardId);
        if (card) return;
        const insertTarget = _resolveSubagentParent(container, data, existingCard);
        card = document.createElement('div');
        card.className = 'subagent-card subagent-running';
        card.id = cardId;
        if (data.parent_tool_call_id) {
            card.dataset.parentToolCallId = `tool-${_sanitizeId(data.parent_tool_call_id)}`;
        }

        const header = document.createElement('div');
        header.className = 'subagent-header';
        const label = document.createElement('span');
        label.className = 'subagent-label';
        label.textContent = agentId;
        const model = document.createElement('span');
        model.className = 'subagent-model';
        model.textContent = data.model || '';
        header.appendChild(label);
        header.appendChild(model);

        const prompt = document.createElement('div');
        prompt.className = 'subagent-prompt';
        prompt.textContent = data.prompt || '';

        const tools = document.createElement('div');
        tools.className = 'subagent-tools';

        const count = document.createElement('span');
        count.className = 'subagent-tool-count';
        count.textContent = '0 tools';

        card.appendChild(header);
        card.appendChild(prompt);
        card.appendChild(count);
        card.appendChild(tools);
        insertTarget.appendChild(card);
    } else if (kind === 'tool_call_start' && agentId) {
        const card = document.getElementById(cardId);
        if (!card) return;
        const tools = card.querySelector('.subagent-tools');
        if (tools) {
            const chip = document.createElement('span');
            chip.className = 'subagent-tool-chip';
            chip.textContent = data.tool_name || 'tool';
            tools.appendChild(chip);
        }
        const count = card.querySelector('.subagent-tool-count');
        if (count) {
            const n = tools ? tools.childElementCount : 0;
            count.textContent = `${n} tool${n === 1 ? '' : 's'}`;
        }
    } else if (kind === 'subagent_end') {
        const card = document.getElementById(cardId);
        if (!card) return;
        card.classList.remove('subagent-running');
        const status = data.status || (data.error ? 'failed' : 'succeeded');
        const terminalClass =
            status === 'cancelled'
                ? 'subagent-cancelled'
                : status === 'failed'
                ? 'subagent-failed'
                : 'subagent-completed';
        card.classList.add(terminalClass);

        // Keep backward-compatible classes expected by existing e2e tests.
        card.classList.add(data.error ? 'subagent-error' : 'subagent-done');

        // Footer: always refresh so multiple subagent_end frames don't duplicate.
        let footer = card.querySelector('.subagent-footer');
        if (!footer) {
            footer = document.createElement('div');
            footer.className = 'subagent-footer';
            card.appendChild(footer);
        }
        const elapsed = data.elapsed_seconds != null ? `${data.elapsed_seconds.toFixed(1)}s` : '';
        const toolCount = (data.tool_calls || []).length;
        const errorMsg = data.error ? String(data.error).slice(0, 200) : '';
        if (errorMsg) {
            footer.textContent = `${status === 'cancelled' ? 'Cancelled' : 'Failed'}: ${errorMsg}`;
        } else {
            footer.textContent = `Done in ${elapsed} · ${toolCount} tool call${toolCount !== 1 ? 's' : ''}`;
        }
    }
}

let container;

beforeEach(() => {
    document.body.innerHTML = '<div id="host"></div>';
    container = document.getElementById('host');
});

describe('renderSubagentEvent (#1460 live contract)', () => {
    it('creates exactly one card per agent on subagent_start', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        expect(container.querySelectorAll('.subagent-card').length).toBe(1);
        expect(container.querySelector('#subagent-agent-1')).toBeTruthy();
    });

    it('does not duplicate the card if subagent_start is delivered twice', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        expect(container.querySelectorAll('.subagent-card').length).toBe(1);
    });

    it('updates tool count in place, not by creating new cards', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'tool_call_start',
            agent_id: 'agent-1',
            tool_name: 'read_file',
        });
        renderSubagentEvent(container, {
            kind: 'tool_call_start',
            agent_id: 'agent-1',
            tool_name: 'bash',
        });
        expect(container.querySelectorAll('.subagent-card').length).toBe(1);
        const card = container.querySelector('#subagent-agent-1');
        expect(card.querySelector('.subagent-tool-count').textContent).toBe('2 tools');
        expect(card.querySelectorAll('.subagent-tool-chip').length).toBe(2);
    });

    it('applies subagent-completed on successful terminal frame', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_end',
            agent_id: 'agent-1',
            elapsed_seconds: 2.3,
            tool_calls: ['read_file', 'bash'],
            status: 'succeeded',
        });
        const card = container.querySelector('#subagent-agent-1');
        expect(card.classList.contains('subagent-completed')).toBe(true);
        expect(card.classList.contains('subagent-running')).toBe(false);
        expect(card.classList.contains('subagent-failed')).toBe(false);
        expect(card.classList.contains('subagent-cancelled')).toBe(false);
        // Backward-compat class kept so the older e2e fixture still passes.
        expect(card.classList.contains('subagent-done')).toBe(true);
        expect(card.querySelector('.subagent-footer').textContent).toContain('Done in 2.3s');
        expect(card.querySelector('.subagent-footer').textContent).toContain('2 tool');
    });

    it('applies subagent-failed and shows error preview on failure', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_end',
            agent_id: 'agent-1',
            elapsed_seconds: 0.5,
            tool_calls: [],
            error: 'something broke',
            status: 'failed',
        });
        const card = container.querySelector('#subagent-agent-1');
        expect(card.classList.contains('subagent-failed')).toBe(true);
        expect(card.classList.contains('subagent-error')).toBe(true);
        expect(card.classList.contains('subagent-completed')).toBe(false);
        expect(card.querySelector('.subagent-footer').textContent).toContain('Failed: something broke');
    });

    it('applies subagent-cancelled when the server derives cancelled status', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'task',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_end',
            agent_id: 'agent-1',
            elapsed_seconds: 1.0,
            tool_calls: [],
            error: 'Sub-agent cancelled by user',
            status: 'cancelled',
        });
        const card = container.querySelector('#subagent-agent-1');
        expect(card.classList.contains('subagent-cancelled')).toBe(true);
        expect(card.classList.contains('subagent-failed')).toBe(false);
        expect(card.querySelector('.subagent-footer').textContent).toContain('Cancelled');
    });

    it('keeps parallel agents on distinct cards', () => {
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-1',
            prompt: 'a',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-2',
            prompt: 'b',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'tool_call_start',
            agent_id: 'agent-1',
            tool_name: 'read_file',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_end',
            agent_id: 'agent-2',
            elapsed_seconds: 0.2,
            tool_calls: [],
            status: 'succeeded',
        });

        expect(container.querySelectorAll('.subagent-card').length).toBe(2);
        const c1 = container.querySelector('#subagent-agent-1');
        const c2 = container.querySelector('#subagent-agent-2');
        expect(c1.classList.contains('subagent-running')).toBe(true);
        expect(c2.classList.contains('subagent-completed')).toBe(true);
    });

    it('ignores tool_call_start with no matching agent card', () => {
        renderSubagentEvent(container, {
            kind: 'tool_call_start',
            agent_id: 'ghost',
            tool_name: 'read_file',
        });
        expect(container.querySelectorAll('.subagent-card').length).toBe(0);
    });

    it('attaches each card to the matching parent run_agent wrapper', () => {
        container.innerHTML = `
            <details id="tool-run-agent-a" class="tool-call tool-call-subagent">
                <div class="subagent-cards-container"></div>
            </details>
            <details id="tool-run-agent-b" class="tool-call tool-call-subagent">
                <div class="subagent-cards-container"></div>
            </details>
        `;

        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-a',
            parent_tool_call_id: 'run-agent-a',
            prompt: 'task a',
            model: 'haiku',
        });
        renderSubagentEvent(container, {
            kind: 'subagent_start',
            agent_id: 'agent-b',
            parent_tool_call_id: 'run-agent-b',
            prompt: 'task b',
            model: 'haiku',
        });

        const wrapperA = document.querySelector('#tool-run-agent-a .subagent-cards-container');
        const wrapperB = document.querySelector('#tool-run-agent-b .subagent-cards-container');
        expect(wrapperA.querySelector('#subagent-agent-a')).toBeTruthy();
        expect(wrapperA.querySelector('#subagent-agent-b')).toBeFalsy();
        expect(wrapperB.querySelector('#subagent-agent-b')).toBeTruthy();
        expect(wrapperB.querySelector('#subagent-agent-a')).toBeFalsy();
    });
});
