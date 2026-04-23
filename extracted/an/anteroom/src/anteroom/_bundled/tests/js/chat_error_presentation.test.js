import { beforeEach, describe, expect, it } from 'vitest';

function _formatUserError(error) {
    if (!error) return 'An internal error occurred';
    if (typeof error === 'string') return error.replace(/\s+/g, ' ').trim();
    if (typeof error === 'object') {
        if (typeof error.display_message === 'string' && error.display_message.trim()) {
            return error.display_message.replace(/\s+/g, ' ').trim();
        }
        const message = typeof error.message === 'string' ? error.message.replace(/\s+/g, ' ').trim() : '';
        const suggestion = typeof error.suggestion === 'string' ? error.suggestion.replace(/\s+/g, ' ').trim() : '';
        if (message && suggestion && !message.toLowerCase().includes(suggestion.toLowerCase())) {
            return `${message} — ${suggestion}`;
        }
        if (message) return message;
    }
    return 'An internal error occurred';
}

function showError(msgEl, error, retryFn) {
    const errDiv = document.createElement('div');
    errDiv.className = 'error-message';

    const errText = document.createElement('span');
    errText.className = 'error-message-text';
    errText.textContent = `Error: ${_formatUserError(error)}`;
    errDiv.appendChild(errText);

    if (retryFn) {
        const retryBtn = document.createElement('button');
        retryBtn.className = 'btn-retry';
        retryBtn.textContent = 'Retry';
        retryBtn.addEventListener('click', retryFn);
        errDiv.appendChild(retryBtn);
    }

    msgEl.appendChild(errDiv);
    return errDiv;
}

beforeEach(() => {
    document.body.innerHTML = '<div id="msg"></div>';
});

describe('chat error presentation', () => {
    it('renders compact actionable display_message text', () => {
        const msg = document.getElementById('msg');
        showError(msg, {
            message: 'Cannot connect to API (3 attempts).',
            suggestion: 'Check AI_CHAT_BASE_URL',
            display_message: 'Cannot connect to API (3 attempts). — Check AI_CHAT_BASE_URL',
        });
        expect(msg.textContent).toContain('Error: Cannot connect to API (3 attempts). — Check AI_CHAT_BASE_URL');
    });

    it('falls back to message plus suggestion when display_message missing', () => {
        const msg = document.getElementById('msg');
        showError(msg, {
            message: 'Authentication failed.',
            suggestion: 'Run: aroom init',
        });
        expect(msg.textContent).toContain('Error: Authentication failed. — Run: aroom init');
    });

    it('renders hostile text as textContent, not HTML', () => {
        const msg = document.getElementById('msg');
        const hostile = '<img src=x onerror="window.__ERR_XSS__=true">';
        showError(msg, { display_message: hostile });
        expect(msg.textContent).toContain(hostile);
        expect(msg.querySelectorAll('img').length).toBe(0);
        expect(globalThis.__ERR_XSS__).toBeUndefined();
    });
});
