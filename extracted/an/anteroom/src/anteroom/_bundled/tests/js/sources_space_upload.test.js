import { describe, it, expect, beforeEach, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const sourcesSrc = readFileSync(
    resolve(__dirname, '../../src/anteroom/static/js/sources.js'),
    'utf-8',
);

function buildDom() {
    document.body.innerHTML = `
        <button id="sources-close"></button>
        <button id="btn-sources-toggle"></button>
        <button id="sources-add-btn"></button>
        <input id="sources-search" value="">
        <select id="sources-type-filter"><option value=""></option></select>
        <button id="source-create-cancel"></button>
        <button id="source-create-save">Save</button>
        <div id="source-file-drop"></div>
        <input id="source-file-input" type="file">
        <div class="sources-create-tabs">
            <button class="sources-tab" data-type="text"></button>
            <button class="sources-tab" data-type="url"></button>
            <button class="sources-tab" data-type="file"></button>
        </div>
        <div id="sources-list"></div>
        <div id="sources-groups-list"></div>
        <div id="sources-group-detail"></div>
        <div id="sources-detail"></div>
        <div id="sources-create"></div>
        <div id="sources-toolbar"></div>
        <input id="source-title-input" value="">
        <textarea id="source-content-input"></textarea>
        <input id="source-url-input" value="">
        <div id="source-file-name"></div>
        <div id="source-content-group"></div>
        <div id="source-url-group"></div>
        <div id="source-file-group"></div>
        <div id="source-ref-bar"></div>
    `;
}

function loadSources() {
    const factory = new Function(`${sourcesSrc}\nreturn Sources;`);
    return factory();
}

function selectSingleFile(file) {
    const input = document.getElementById('source-file-input');
    Object.defineProperty(input, 'files', {
        value: [file],
        configurable: true,
    });
    input.dispatchEvent(new Event('change'));
}

describe('sources upload space scoping', () => {
    beforeEach(() => {
        buildDom();
        globalThis.DOMPurify = { sanitize: (value) => value };
        globalThis.Chat = { showToast: vi.fn() };
        globalThis.Canvas = { closeCanvas: vi.fn() };
        globalThis.alert = vi.fn();
        globalThis.confirm = vi.fn(() => true);
    });

    it('includes active space_id in file upload requests and refreshes space membership', async () => {
        const api = vi.fn(async (url) => {
            if (url === '/api/sources/upload') return { id: 'src-1', warnings: [] };
            if (url === '/api/spaces/space-1/sources') return [{ id: 'src-1', title: 'Space File', type: 'file' }];
            if (url.startsWith('/api/sources?')) {
                return {
                    sources: [{ id: 'src-1', title: 'Space File', type: 'file', created_at: '2026-01-01T00:00:00Z' }],
                };
            }
            return {};
        });
        globalThis.App = {
            state: { currentSpaceId: 'space-1' },
            getState: () => ({ currentSpaceId: 'space-1' }),
            api,
            formatTimestamp: () => 'now',
        };

        const Sources = loadSources();
        Sources.init();
        Sources.showCreateView();
        document.querySelector(".sources-tab[data-type='file']").click();
        document.getElementById('source-title-input').value = 'Space File';
        selectSingleFile(new File(['hello'], 'space.txt', { type: 'text/plain' }));

        document.getElementById('source-create-save').click();

        await vi.waitFor(() => expect(api).toHaveBeenCalledWith('/api/sources/upload', expect.any(Object)));

        const uploadCall = api.mock.calls.find(([url]) => url === '/api/sources/upload');
        expect(uploadCall).toBeTruthy();
        expect(uploadCall[1].body.get('space_id')).toBe('space-1');
        expect(api).toHaveBeenCalledWith('/api/spaces/space-1/sources');
    });

    it('omits space_id when no active space is set', async () => {
        const api = vi.fn(async (url) => {
            if (url === '/api/sources/upload') return { id: 'src-1', warnings: [] };
            if (url.startsWith('/api/sources?')) {
                return {
                    sources: [{ id: 'src-1', title: 'Global File', type: 'file', created_at: '2026-01-01T00:00:00Z' }],
                };
            }
            return [];
        });
        globalThis.App = {
            state: { currentSpaceId: null },
            getState: () => ({ currentSpaceId: null }),
            api,
            formatTimestamp: () => 'now',
        };

        const Sources = loadSources();
        Sources.init();
        Sources.showCreateView();
        document.querySelector(".sources-tab[data-type='file']").click();
        document.getElementById('source-title-input').value = 'Global File';
        selectSingleFile(new File(['hello'], 'global.txt', { type: 'text/plain' }));

        document.getElementById('source-create-save').click();

        await vi.waitFor(() => expect(api).toHaveBeenCalledWith('/api/sources/upload', expect.any(Object)));

        const uploadCall = api.mock.calls.find(([url]) => url === '/api/sources/upload');
        expect(uploadCall).toBeTruthy();
        expect(uploadCall[1].body.get('space_id')).toBeNull();
    });
});
