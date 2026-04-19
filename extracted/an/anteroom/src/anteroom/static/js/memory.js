/* Memory management panel — IIFE, follows the Artifacts panel pattern.
 *
 * Scope (per issue #1416): list / show / create / edit / delete. The
 * approve / reject review workflow (reviewer identity, rejection reason,
 * candidate lineage) is owned by #920 — this module must not grow those
 * actions.
 *
 * All user-supplied strings go through textContent rather than innerHTML to
 * avoid XSS. DOM structure is assembled with createElement. */
const MemoryPanel = (() => {
    'use strict';

    let _memories = [];
    let _currentView = 'list';
    const _scopes = ['user', 'project', 'local'];
    const _categories = ['preference', 'project_fact', 'decision', 'workflow_hint'];
    const _statuses = ['active', 'candidate', 'pending_review', 'rejected', 'archived'];

    function _badge(text, className) {
        const el = document.createElement('span');
        el.className = 'memory-badge ' + (className || '');
        el.textContent = text;
        return el;
    }

    function _statusBadge(status) {
        return _badge(status || '-', 'memory-status-' + (status || 'unknown'));
    }

    /* ── filter predicate (unit-tested in tests/js/memory.test.js) ── */

    function _matchesFilters(mem, filters) {
        if (!mem || !mem.metadata) return false;
        const meta = mem.metadata;
        if (filters.scope && meta.memory_scope !== filters.scope) return false;
        if (filters.status && meta.memory_status !== filters.status) return false;
        if (filters.category && meta.memory_category !== filters.category) return false;
        if (filters.namespace && mem.namespace !== filters.namespace) return false;
        return true;
    }

    /* ── query string construction ── */

    function _buildQueryString(filters) {
        const params = new URLSearchParams();
        if (filters.scope) params.set('scope', filters.scope);
        if (filters.status) params.set('status', filters.status);
        if (filters.category) params.set('category', filters.category);
        if (filters.namespace) params.set('namespace', filters.namespace);
        const qs = params.toString();
        return qs ? '?' + qs : '';
    }

    /* ── panel open / close ── */

    function togglePanel() {
        const panel = document.getElementById('memory-panel');
        if (panel && panel.style.display !== 'none') {
            closePanel();
        } else {
            openPanel();
        }
    }

    async function openPanel() {
        const panel = document.getElementById('memory-panel');
        if (!panel) return;
        panel.style.display = '';
        _showListView();
        await _refreshList();
    }

    function closePanel() {
        const panel = document.getElementById('memory-panel');
        if (panel) panel.style.display = 'none';
    }

    /* ── view switching ── */

    function _showListView() {
        _currentView = 'list';
        const list = document.getElementById('memory-list');
        const detail = document.getElementById('memory-detail');
        const edit = document.getElementById('memory-edit-form');
        const create = document.getElementById('memory-create-form');
        if (list) list.style.display = '';
        if (detail) detail.style.display = 'none';
        if (edit) edit.style.display = 'none';
        if (create) create.style.display = 'none';
    }

    function _showDetailView() {
        _currentView = 'detail';
        const list = document.getElementById('memory-list');
        const detail = document.getElementById('memory-detail');
        const edit = document.getElementById('memory-edit-form');
        const create = document.getElementById('memory-create-form');
        if (list) list.style.display = 'none';
        if (detail) detail.style.display = '';
        if (edit) edit.style.display = 'none';
        if (create) create.style.display = 'none';
    }

    function _showEditView() {
        _currentView = 'edit';
        const list = document.getElementById('memory-list');
        const detail = document.getElementById('memory-detail');
        const edit = document.getElementById('memory-edit-form');
        const create = document.getElementById('memory-create-form');
        if (list) list.style.display = 'none';
        if (detail) detail.style.display = 'none';
        if (edit) edit.style.display = '';
        if (create) create.style.display = 'none';
    }

    function _showCreateView() {
        _currentView = 'create';
        const list = document.getElementById('memory-list');
        const detail = document.getElementById('memory-detail');
        const edit = document.getElementById('memory-edit-form');
        const create = document.getElementById('memory-create-form');
        if (list) list.style.display = 'none';
        if (detail) detail.style.display = 'none';
        if (edit) edit.style.display = 'none';
        if (create) create.style.display = '';
    }

    /* ── API calls ── */

    async function _apiRequest(path, options) {
        // Thin wrapper around App.api so tests can stub fetch directly.
        if (typeof App !== 'undefined' && App && typeof App.api === 'function') {
            return App.api(path, options);
        }
        const resp = await fetch('/api' + path, options || {});
        if (!resp.ok) {
            const msg = await resp.text();
            throw new Error(msg || ('HTTP ' + resp.status));
        }
        if (resp.status === 204) return null;
        return resp.json();
    }

    async function _refreshList() {
        const list = document.getElementById('memory-list');
        if (!list) return;
        list.textContent = '';
        const loading = document.createElement('div');
        loading.className = 'memory-loading';
        loading.textContent = 'Loading...';
        list.appendChild(loading);
        try {
            const filters = _readFilters();
            const qs = _buildQueryString(filters);
            _memories = await _apiRequest('/memory' + qs);
            list.textContent = '';
            if (!_memories || _memories.length === 0) {
                const empty = document.createElement('div');
                empty.className = 'memory-empty';
                empty.textContent = 'No memories found.';
                list.appendChild(empty);
                return;
            }
            _memories.forEach(mem => list.appendChild(_buildListItem(mem)));
        } catch (err) {
            list.textContent = '';
            const errEl = document.createElement('div');
            errEl.className = 'memory-error';
            errEl.textContent = (err && err.message) || String(err);
            list.appendChild(errEl);
        }
    }

    function _readFilters() {
        const get = id => {
            const el = document.getElementById(id);
            return el ? el.value : '';
        };
        return {
            scope: get('memory-filter-scope'),
            status: get('memory-filter-status'),
            category: get('memory-filter-category'),
            namespace: get('memory-filter-namespace'),
        };
    }

    function _buildListItem(mem) {
        const meta = mem.metadata || {};
        const item = document.createElement('div');
        item.className = 'memory-item';

        const title = document.createElement('div');
        title.className = 'memory-item-title';
        title.textContent = mem.fqn || mem.name || '';
        item.appendChild(title);

        const metaRow = document.createElement('div');
        metaRow.className = 'memory-item-meta';
        metaRow.appendChild(_badge(meta.memory_scope || '-', 'memory-scope'));
        metaRow.appendChild(_badge(meta.memory_category || '-', 'memory-category'));
        metaRow.appendChild(_statusBadge(meta.memory_status));
        item.appendChild(metaRow);

        item.addEventListener('click', () => _showMemoryDetail(mem.fqn));
        return item;
    }

    async function _showMemoryDetail(fqn) {
        _showDetailView();
        const detail = document.getElementById('memory-detail');
        if (!detail) return;
        detail.textContent = 'Loading...';
        try {
            const mem = await _apiRequest('/memory/' + fqn);
            detail.textContent = '';

            const header = document.createElement('div');
            header.className = 'memory-detail-header';
            const backBtn = document.createElement('button');
            backBtn.className = 'memory-back-btn';
            backBtn.textContent = '←';
            backBtn.addEventListener('click', () => { _showListView(); _refreshList(); });
            header.appendChild(backBtn);

            const titleEl = document.createElement('span');
            titleEl.className = 'memory-detail-title';
            titleEl.textContent = mem.fqn;
            header.appendChild(titleEl);
            detail.appendChild(header);

            const body = document.createElement('div');
            body.className = 'memory-detail-body';

            const meta = mem.metadata || {};
            const fields = [
                ['Scope', meta.memory_scope],
                ['Category', meta.memory_category],
                ['Status', meta.memory_status],
                ['Created by', meta.created_by],
                ['Recall count', meta.recall_count],
                ['Last recalled', meta.last_recalled_at || '-'],
                ['Created', mem.created_at],
                ['Source', mem.source || '-'],
            ];
            const metaList = document.createElement('dl');
            metaList.className = 'memory-detail-meta';
            fields.forEach(([k, v]) => {
                const dt = document.createElement('dt');
                dt.textContent = k;
                const dd = document.createElement('dd');
                dd.textContent = v != null ? String(v) : '-';
                metaList.appendChild(dt);
                metaList.appendChild(dd);
            });
            body.appendChild(metaList);

            // Provenance block — where the memory came from (conversation,
            // message, workflow run, source artifact). Shown even when empty
            // so users learn the schema.
            const prov = meta.provenance || {};
            const provHeader = document.createElement('div');
            provHeader.className = 'memory-detail-provenance-label';
            provHeader.textContent = 'Provenance';
            body.appendChild(provHeader);

            const provList = document.createElement('dl');
            provList.className = 'memory-detail-provenance';
            const provKeys = ['conversation_id', 'message_id', 'workflow_run_id', 'source_artifact_id'];
            const hasAnyProv = provKeys.some(k => prov[k]);
            if (hasAnyProv) {
                provKeys.forEach(k => {
                    if (!prov[k]) return;
                    const dt = document.createElement('dt');
                    dt.textContent = k;
                    const dd = document.createElement('dd');
                    dd.textContent = prov[k];
                    provList.appendChild(dt);
                    provList.appendChild(dd);
                });
            } else {
                const empty = document.createElement('div');
                empty.className = 'memory-provenance-empty';
                empty.textContent = 'No provenance recorded.';
                provList.appendChild(empty);
            }
            body.appendChild(provList);

            const contentLabel = document.createElement('div');
            contentLabel.className = 'memory-detail-content-label';
            contentLabel.textContent = 'Content';
            body.appendChild(contentLabel);

            const pre = document.createElement('pre');
            pre.className = 'memory-detail-content';
            pre.textContent = mem.content || '';
            body.appendChild(pre);

            const actions = document.createElement('div');
            actions.className = 'memory-detail-actions';
            const editBtn = document.createElement('button');
            editBtn.textContent = 'Edit';
            editBtn.addEventListener('click', () => _showEditForm(mem));
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', () => _deleteMemory(mem.fqn));
            actions.appendChild(editBtn);
            actions.appendChild(deleteBtn);
            body.appendChild(actions);

            detail.appendChild(body);
        } catch (err) {
            detail.textContent = '';
            const errEl = document.createElement('div');
            errEl.className = 'memory-error';
            errEl.textContent = (err && err.message) || String(err);
            detail.appendChild(errEl);
        }
    }

    function _showEditForm(mem) {
        _showEditView();
        const form = document.getElementById('memory-edit-form');
        if (!form) return;
        form.textContent = '';
        const title = document.createElement('h3');
        title.textContent = 'Edit ' + mem.fqn;
        form.appendChild(title);

        const textarea = document.createElement('textarea');
        textarea.id = 'memory-edit-content';
        textarea.value = mem.content || '';
        form.appendChild(textarea);

        const saveBtn = document.createElement('button');
        saveBtn.id = 'memory-edit-save';
        saveBtn.textContent = 'Save';
        saveBtn.addEventListener('click', () => _saveEdit(mem.fqn));

        const cancelBtn = document.createElement('button');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', () => _showMemoryDetail(mem.fqn));

        form.appendChild(saveBtn);
        form.appendChild(cancelBtn);
    }

    async function _saveEdit(fqn) {
        const textarea = document.getElementById('memory-edit-content');
        const content = textarea ? textarea.value : '';
        if (!content.trim()) {
            const form = document.getElementById('memory-edit-form');
            if (form) {
                const existing = form.querySelector('.memory-error');
                if (existing) existing.remove();
                const err = document.createElement('div');
                err.className = 'memory-error';
                err.textContent = 'Content cannot be empty.';
                form.appendChild(err);
            }
            return;
        }
        await _apiRequest('/memory/' + fqn, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content }),
        });
        await _showMemoryDetail(fqn);
    }

    async function _deleteMemory(fqn) {
        await _apiRequest('/memory/' + fqn, { method: 'DELETE' });
        _showListView();
        await _refreshList();
    }

    async function createMemory(payload) {
        return _apiRequest('/memory', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
    }

    /* ── Review queue (#920) ─────────────────────────────────────────────
     * Review actions live on top of the same panel. Approve / reject /
     * edit-and-approve talk to /api/memory/{fqn}/approve|reject. "Active"
     * tab and "Review" tab share the filter row but fetch different data.
     */

    let _currentTab = 'active';  // 'active' or 'review'

    function _switchTab(tab) {
        _currentTab = tab;
        document.querySelectorAll('.memory-tab').forEach(el => {
            el.classList.toggle('active', el.dataset.tab === tab);
        });
        _showListView();
        _refreshCurrentTab();
    }

    async function _refreshCurrentTab() {
        if (_currentTab === 'review') {
            await _refreshReviewQueue();
        } else if (_currentTab === 'retention') {
            await _refreshRetentionPreview();
        } else {
            await _refreshList();
        }
    }

    async function _refreshReviewQueue() {
        const list = document.getElementById('memory-list');
        if (!list) return;
        list.textContent = '';
        const loading = document.createElement('div');
        loading.className = 'memory-loading';
        loading.textContent = 'Loading...';
        list.appendChild(loading);
        try {
            const candidates = await _apiRequest('/memory/candidates');
            list.textContent = '';
            if (!candidates || candidates.length === 0) {
                const empty = document.createElement('div');
                empty.className = 'memory-empty';
                empty.textContent = 'No pending candidates.';
                list.appendChild(empty);
                return;
            }
            candidates.forEach(mem => list.appendChild(_buildReviewItem(mem)));
        } catch (err) {
            list.textContent = '';
            const errEl = document.createElement('div');
            errEl.className = 'memory-error';
            errEl.textContent = (err && err.message) || String(err);
            list.appendChild(errEl);
        }
    }

    function _buildReviewItem(mem) {
        const meta = mem.metadata || {};
        const item = document.createElement('div');
        item.className = 'memory-item memory-review-item';
        item.dataset.fqn = mem.fqn;

        const title = document.createElement('div');
        title.className = 'memory-item-title';
        title.textContent = mem.fqn || mem.name || '';
        item.appendChild(title);

        const preview = document.createElement('div');
        preview.className = 'memory-item-preview';
        // Trim long content for the row; full content is shown in detail view.
        const content = mem.content || '';
        preview.textContent = content.length > 200 ? content.slice(0, 200) + '…' : content;
        item.appendChild(preview);

        const metaRow = document.createElement('div');
        metaRow.className = 'memory-item-meta';
        metaRow.appendChild(_badge(meta.memory_scope || '-', 'memory-scope'));
        metaRow.appendChild(_badge(meta.memory_category || '-', 'memory-category'));
        metaRow.appendChild(_statusBadge(meta.memory_status));
        item.appendChild(metaRow);

        const actions = document.createElement('div');
        actions.className = 'memory-review-actions';

        const approveBtn = document.createElement('button');
        approveBtn.type = 'button';
        approveBtn.className = 'memory-review-approve';
        approveBtn.textContent = 'Approve';
        approveBtn.addEventListener('click', evt => {
            evt.stopPropagation();
            _approveCandidate(mem.fqn);
        });

        const editApproveBtn = document.createElement('button');
        editApproveBtn.type = 'button';
        editApproveBtn.className = 'memory-review-edit-approve';
        editApproveBtn.textContent = 'Edit & approve';
        editApproveBtn.addEventListener('click', evt => {
            evt.stopPropagation();
            _showEditAndApproveForm(mem);
        });

        const rejectBtn = document.createElement('button');
        rejectBtn.type = 'button';
        rejectBtn.className = 'memory-review-reject';
        rejectBtn.textContent = 'Reject';
        rejectBtn.addEventListener('click', evt => {
            evt.stopPropagation();
            _showRejectForm(mem);
        });

        actions.appendChild(approveBtn);
        actions.appendChild(editApproveBtn);
        actions.appendChild(rejectBtn);
        item.appendChild(actions);

        return item;
    }

    async function _approveCandidate(fqn, edits) {
        const body = {};
        if (edits) body.edits = edits;
        try {
            const path = edits ? `/memory/${fqn}/edit-and-approve` : `/memory/${fqn}/approve`;
            await _apiRequest(path, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            await _refreshCurrentTab();
        } catch (err) {
            _showInlineError(fqn, (err && err.message) || String(err));
        }
    }

    function _showInlineError(fqn, message) {
        // Attach an error message below the item row so users see context
        // without a blocking modal.
        const item = document.querySelector(`.memory-review-item[data-fqn="${CSS.escape(fqn)}"]`);
        if (!item) return;
        const existing = item.querySelector('.memory-error');
        if (existing) existing.remove();
        const err = document.createElement('div');
        err.className = 'memory-error';
        err.textContent = message;
        item.appendChild(err);
    }

    function _showEditAndApproveForm(mem) {
        const item = document.querySelector(`.memory-review-item[data-fqn="${CSS.escape(mem.fqn)}"]`);
        if (!item) return;
        const existing = item.querySelector('.memory-review-form');
        if (existing) { existing.remove(); return; }

        const form = document.createElement('div');
        form.className = 'memory-review-form memory-edit-approve-form';

        const label = document.createElement('label');
        label.textContent = 'Edited content (required)';
        form.appendChild(label);

        const ta = document.createElement('textarea');
        ta.className = 'memory-edit-approve-content';
        ta.value = mem.content || '';
        form.appendChild(ta);

        const saveBtn = document.createElement('button');
        saveBtn.type = 'button';
        saveBtn.textContent = 'Save & approve';
        saveBtn.addEventListener('click', async () => {
            const edited = ta.value.trim();
            if (!edited) {
                _showInlineError(mem.fqn, 'Edited content cannot be empty.');
                return;
            }
            await _approveCandidate(mem.fqn, { content: edited });
        });

        const cancelBtn = document.createElement('button');
        cancelBtn.type = 'button';
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', () => form.remove());

        form.appendChild(saveBtn);
        form.appendChild(cancelBtn);
        item.appendChild(form);
    }

    function _showRejectForm(mem) {
        const item = document.querySelector(`.memory-review-item[data-fqn="${CSS.escape(mem.fqn)}"]`);
        if (!item) return;
        const existing = item.querySelector('.memory-review-form');
        if (existing) { existing.remove(); return; }

        const form = document.createElement('div');
        form.className = 'memory-review-form memory-reject-form';

        const label = document.createElement('label');
        label.textContent = 'Rejection reason (required)';
        form.appendChild(label);

        const reason = document.createElement('textarea');
        reason.className = 'memory-reject-reason';
        reason.maxLength = 2000;
        form.appendChild(reason);

        const submitBtn = document.createElement('button');
        submitBtn.type = 'button';
        submitBtn.textContent = 'Reject';
        submitBtn.addEventListener('click', async () => {
            const text = reason.value.trim();
            if (!text) {
                _showInlineError(mem.fqn, 'Rejection reason is required.');
                return;
            }
            try {
                await _apiRequest(`/memory/${mem.fqn}/reject`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason: text }),
                });
                await _refreshCurrentTab();
            } catch (err) {
                _showInlineError(mem.fqn, (err && err.message) || String(err));
            }
        });

        const cancelBtn = document.createElement('button');
        cancelBtn.type = 'button';
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', () => form.remove());

        form.appendChild(submitBtn);
        form.appendChild(cancelBtn);
        item.appendChild(form);
    }

    async function proposeCandidate(payload) {
        return _apiRequest('/memory/candidates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
    }

    function _showCreateForm() {
        _showCreateView();
        const form = document.getElementById('memory-create-form');
        if (!form) return;
        form.textContent = '';

        const title = document.createElement('h3');
        title.textContent = 'New memory';
        form.appendChild(title);

        const buildRow = (labelText, input) => {
            const row = document.createElement('div');
            row.className = 'memory-create-row';
            const lbl = document.createElement('label');
            lbl.textContent = labelText;
            row.appendChild(lbl);
            row.appendChild(input);
            return row;
        };

        const content = document.createElement('textarea');
        content.id = 'memory-create-content';
        content.placeholder = 'Memory content';
        form.appendChild(buildRow('Content', content));

        const scope = document.createElement('select');
        scope.id = 'memory-create-scope';
        _scopes.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = s;
            scope.appendChild(opt);
        });
        form.appendChild(buildRow('Scope', scope));

        const category = document.createElement('select');
        category.id = 'memory-create-category';
        _categories.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            category.appendChild(opt);
        });
        form.appendChild(buildRow('Category', category));

        const name = document.createElement('input');
        name.id = 'memory-create-name';
        name.type = 'text';
        name.placeholder = 'Optional slug (auto-generated if blank)';
        form.appendChild(buildRow('Name', name));

        const projectSlug = document.createElement('input');
        projectSlug.id = 'memory-create-project-slug';
        projectSlug.type = 'text';
        projectSlug.placeholder = 'Required when scope = project';
        form.appendChild(buildRow('Project slug', projectSlug));

        const errorBox = document.createElement('div');
        errorBox.id = 'memory-create-error';
        errorBox.className = 'memory-error';
        errorBox.style.display = 'none';
        form.appendChild(errorBox);

        const saveBtn = document.createElement('button');
        saveBtn.id = 'memory-create-save';
        saveBtn.textContent = 'Create';
        saveBtn.addEventListener('click', _submitCreate);

        const cancelBtn = document.createElement('button');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', () => { _showListView(); _refreshList(); });

        form.appendChild(saveBtn);
        form.appendChild(cancelBtn);
    }

    async function _submitCreate() {
        const err = document.getElementById('memory-create-error');
        if (err) { err.style.display = 'none'; err.textContent = ''; }

        const get = id => {
            const el = document.getElementById(id);
            return el ? el.value : '';
        };
        const content = get('memory-create-content').trim();
        if (!content) {
            if (err) { err.textContent = 'Content cannot be empty.'; err.style.display = ''; }
            return;
        }
        const payload = {
            content: content,
            scope: get('memory-create-scope'),
            category: get('memory-create-category'),
        };
        const name = get('memory-create-name').trim();
        if (name) payload.name = name;
        const projectSlug = get('memory-create-project-slug').trim();
        if (projectSlug) payload.project_slug = projectSlug;

        try {
            await createMemory(payload);
            _showListView();
            await _refreshList();
        } catch (e) {
            if (err) { err.textContent = (e && e.message) || String(e); err.style.display = ''; }
        }
    }

    /* ── Retention tab (#625) ────────────────────────────────────────────
     * Shows the dry-run would-be-purged set and the governed "Run purge"
     * button. Never renders user-supplied content unsafely — all fields
     * go through ``textContent``. Pin toggles live on the "Active" tab
     * via ``togglePinOnItem`` so they're reachable even when retention
     * is disabled.
     */

    async function _refreshRetentionPreview() {
        const list = document.getElementById('memory-list');
        if (!list) return;
        list.textContent = '';
        const loading = document.createElement('div');
        loading.className = 'memory-loading';
        loading.textContent = 'Loading retention preview...';
        list.appendChild(loading);
        try {
            const result = await _apiRequest('/memory/retention-preview');
            list.textContent = '';
            list.appendChild(_buildRetentionHeader(result));
            if (!result || !result.items || result.items.length === 0) {
                const empty = document.createElement('div');
                empty.className = 'memory-empty';
                empty.textContent = 'No memories match the current retention policy.';
                list.appendChild(empty);
                return;
            }
            result.items.forEach(item => list.appendChild(_buildRetentionItem(item)));
        } catch (err) {
            list.textContent = '';
            const errEl = document.createElement('div');
            errEl.className = 'memory-error';
            errEl.textContent = (err && err.message) || String(err);
            list.appendChild(errEl);
        }
    }

    function _buildRetentionHeader(result) {
        const header = document.createElement('div');
        header.className = 'memory-retention-header';

        const summary = document.createElement('div');
        summary.className = 'memory-retention-summary';
        const count = (result && result.purged_count) || 0;
        const skipped = (result && result.skipped_pinned_count) || 0;
        summary.textContent = count === 0
            ? 'No memories would be purged on the next cycle.'
            : count + ' memory(ies) would be purged on the next cycle.' +
              (skipped > 0 ? ' (' + skipped + ' pinned memory(ies) will be skipped.)' : '');
        header.appendChild(summary);

        const purgeBtn = document.createElement('button');
        purgeBtn.type = 'button';
        purgeBtn.className = 'memory-retention-purge';
        purgeBtn.textContent = 'Run purge now';
        purgeBtn.disabled = count === 0;
        purgeBtn.addEventListener('click', evt => {
            evt.stopPropagation();
            _confirmAndRunPurge(count);
        });
        header.appendChild(purgeBtn);

        return header;
    }

    function _buildRetentionItem(item) {
        const row = document.createElement('div');
        row.className = 'memory-item memory-retention-item';
        row.dataset.fqn = item.fqn;

        const title = document.createElement('div');
        title.className = 'memory-item-title';
        title.textContent = item.fqn || '';
        row.appendChild(title);

        const metaRow = document.createElement('div');
        metaRow.className = 'memory-item-meta';
        metaRow.appendChild(_badge('reason: ' + (item.reason || '-'), 'memory-retention-reason'));
        metaRow.appendChild(_badge('age: ' + (item.age_days || 0) + 'd', 'memory-retention-age'));
        if (item.last_recalled_at) {
            metaRow.appendChild(_badge('recalled: ' + String(item.last_recalled_at).slice(0, 10), 'memory-retention-recalled'));
        }
        metaRow.appendChild(_statusBadge(item.status));
        if (item.pinned) {
            metaRow.appendChild(_badge('pinned', 'memory-pinned'));
        }
        row.appendChild(metaRow);

        return row;
    }

    async function _confirmAndRunPurge(count) {
        const message = 'Permanently delete ' + count + ' memory(ies)? This cannot be undone.';
        if (typeof window !== 'undefined' && typeof window.confirm === 'function') {
            if (!window.confirm(message)) return;
        }
        try {
            const result = await _apiRequest('/memory/retention-purge', {
                method: 'POST',
                body: JSON.stringify({confirm: true}),
            });
            await _refreshRetentionPreview();
            if (typeof window !== 'undefined' && typeof window.alert === 'function') {
                // The response carries ``purged_by`` — the reviewer identity
                // the backend stamped on the audit entry. Surface it so the
                // user sees which session was recorded.
                const who = result && result.purged_by ? ' by ' + result.purged_by : '';
                window.alert('Purged ' + (result.purged_count || 0) + ' memory(ies)' + who + '.');
            }
        } catch (err) {
            if (typeof window !== 'undefined' && typeof window.alert === 'function') {
                window.alert('Purge failed: ' + ((err && err.message) || err));
            }
        }
    }

    /* ── Pin toggle (#625) ─────────────────────────────────────────────── */

    async function togglePin(fqn, pinned) {
        const endpoint = pinned ? '/memory/' + fqn + '/unpin' : '/memory/' + fqn + '/pin';
        await _apiRequest(endpoint, {method: 'POST', body: JSON.stringify({})});
        await _refreshCurrentTab();
    }

    function init() {
        const btn = document.getElementById('btn-memory-toggle');
        if (btn) btn.addEventListener('click', togglePanel);
        const closeBtn = document.getElementById('memory-close-btn');
        if (closeBtn) closeBtn.addEventListener('click', closePanel);
        const refreshBtn = document.getElementById('memory-refresh-btn');
        if (refreshBtn) refreshBtn.addEventListener('click', _refreshCurrentTab);
        const newBtn = document.getElementById('memory-new-btn');
        if (newBtn) newBtn.addEventListener('click', _showCreateForm);
        document.querySelectorAll('.memory-tab').forEach(el => {
            el.addEventListener('click', () => _switchTab(el.dataset.tab));
        });
        ['memory-filter-scope', 'memory-filter-status', 'memory-filter-category', 'memory-filter-namespace'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.addEventListener('change', _refreshCurrentTab);
        });
    }

    return {
        init,
        openPanel,
        closePanel,
        togglePanel,
        createMemory,
        proposeCandidate,
        togglePin,
        // Exposed for tests — allows direct assertion on pure helpers.
        _matchesFilters,
        _buildQueryString,
        _scopes,
        _categories,
        _statuses,
        _refreshList,
        _refreshReviewQueue,
        _refreshRetentionPreview,
        _refreshCurrentTab,
        _switchTab,
        _showMemoryDetail,
        _showCreateForm,
        _submitCreate,
        _buildListItem,
        _buildReviewItem,
        _buildRetentionHeader,
        _buildRetentionItem,
        _confirmAndRunPurge,
        _approveCandidate,
        _showEditAndApproveForm,
        _showRejectForm,
    };
})();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = MemoryPanel;
}
