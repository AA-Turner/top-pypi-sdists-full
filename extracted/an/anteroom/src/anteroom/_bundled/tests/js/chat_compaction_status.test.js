/**
 * JS unit tests for the chat.js compaction phase status lifecycle (#1553).
 *
 * chat.js keeps its phase helpers private inside the Chat IIFE, so this follows
 * the existing project convention of inlining the narrow behavior under test.
 * Keep these helpers in sync with the compaction/status functions in
 * src/anteroom/static/js/chat.js.
 */

import { beforeEach, describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

let _thinkingPhase = '';
let _phaseData = {};
let _phaseStartTime = 0;
let _phaseElapsedInterval = null;
let _stallCheckInterval = null;
const _PHASE_ELAPSED_DELAY_MS = 1500;

function scrollToBottom() {
    const container = document.getElementById('messages-container');
    container.scrollTop = container.scrollHeight;
}

function _ensureThinkingElement() {
    if (document.getElementById('thinking')) return;
    const el = document.createElement('div');
    el.className = 'thinking-indicator';
    el.id = 'thinking';
    el.innerHTML = '<span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span>'
        + '<span class="thinking-phase-label" id="thinking-phase"></span>';
    const container = document.getElementById('messages-container');
    container.appendChild(el);
    scrollToBottom();
}

function showThinking() {
    if (document.getElementById('thinking')) return;
    _phaseStartTime = Date.now();
    _thinkingPhase = '';
    _phaseData = {};
    _ensureThinkingElement();
}

function hideThinking() {
    document.querySelectorAll('.thinking-indicator').forEach(el => el.remove());
    _thinkingPhase = '';
    _phaseData = {};
    _phaseStartTime = 0;
    if (_phaseElapsedInterval) {
        clearInterval(_phaseElapsedInterval);
        _phaseElapsedInterval = null;
    }
    if (_stallCheckInterval) {
        clearInterval(_stallCheckInterval);
        _stallCheckInterval = null;
    }
}

function _formatElapsed(ms) {
    const s = Math.floor(ms / 1000);
    return s + 's';
}

function _setPhaseLabel(text, isStall) {
    const label = document.getElementById('thinking-phase');
    if (!label) return;
    label.textContent = text;
    if (isStall) {
        label.classList.add('stall');
    } else {
        label.classList.remove('stall');
    }
}

function _countLabel(value) {
    return Number.isInteger(value) ? value.toLocaleString() : '?';
}

function _compactionPhaseDetail(data) {
    const reason = data && data.reason;
    if (reason === 'context_error_recovery') {
        return 'context-error recovery';
    }
    if (reason === 'historical_tool_results') {
        return 'historical tool collapse';
    }
    const tokenDetail = 'token threshold ' + _countLabel(data && data.estimated_tokens) +
        '/' + _countLabel(data && data.token_threshold);
    const messageDetail = 'message threshold ' + _countLabel(data && data.message_count) +
        '/' + _countLabel(data && data.message_threshold);
    if (reason === 'token_threshold') {
        return tokenDetail;
    }
    if (reason === 'message_count') {
        return messageDetail;
    }
    if (reason === 'token_and_message_threshold') {
        return tokenDetail + ' \u00b7 ' + messageDetail;
    }
    return '';
}

function _renderPhaseLabel() {
    const phaseAge = Date.now() - _phaseStartTime;
    const elapsed = phaseAge >= _PHASE_ELAPSED_DELAY_MS ? ' (' + _formatElapsed(phaseAge) + ')' : '';

    switch (_thinkingPhase) {
        case 'compacting': {
            const detail = _compactionPhaseDetail(_phaseData);
            const suffix = detail ? ' \u00b7 ' + detail : '';
            _setPhaseLabel('compacting conversation history' + suffix + '\u2026' + elapsed, false);
            break;
        }
        default:
            if (!_thinkingPhase) _setPhaseLabel('', false);
            break;
    }
}

function updateThinkingPhase(phase, data) {
    _ensureThinkingElement();
    _thinkingPhase = phase;
    _phaseData = data || {};
    _phaseStartTime = Date.now();
    _renderPhaseLabel();
}

function handleSSEEvent(type, data) {
    switch (type) {
        case 'thinking':
            showThinking();
            break;
        case 'phase':
            updateThinkingPhase(data.phase, data);
            break;
        case 'done':
            hideThinking();
            break;
    }
}

beforeEach(() => {
    document.body.innerHTML = '<div id="messages-container"></div>';
    _thinkingPhase = '';
    _phaseData = {};
    _phaseStartTime = 0;
});

describe('chat compaction status lifecycle', () => {
    it('keeps the source compaction branch singular so reason detail is reachable', () => {
        const source = readFileSync('src/anteroom/static/js/chat.js', 'utf8');
        const branches = source.match(/case 'compacting':/g) || [];

        expect(branches).toHaveLength(1);
    });

    it('renders message-count compaction reason and clears on done and next turn', () => {
        handleSSEEvent('thinking', {});
        handleSSEEvent('phase', {
            phase: 'compacting',
            reason: 'message_count',
            estimated_tokens: 37000,
            token_threshold: 128000,
            message_count: 84,
            message_threshold: 80,
        });

        const label = document.getElementById('thinking-phase');
        expect(label).toBeTruthy();
        expect(label.textContent).toContain('compacting conversation history');
        expect(label.textContent).toContain('message threshold 84/80');

        handleSSEEvent('done', {});

        expect(document.getElementById('thinking')).toBeNull();

        handleSSEEvent('thinking', {});
        expect(document.getElementById('thinking-phase').textContent).toBe('');
    });

    it('renders historical tool collapse phase detail', () => {
        updateThinkingPhase('compacting', { reason: 'historical_tool_results' });

        const label = document.getElementById('thinking-phase');
        expect(label).toBeTruthy();
        expect(label.textContent).toContain('historical tool collapse');
    });
});
