/**
 * Workflows panel — read-only monitoring of workflow runs (#961).
 * Owns a dedicated EventSource for detail-view live updates.
 */
const Workflows = (() => {
    let _runs = [];
    let _currentRunId = null;
    let _currentView = 'list';
    let _statusFilter = '';
    let _workflowEventSource = null;
    let _refreshTimer = null;

    function _escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

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

    function _statusBadge(status) {
        const colors = {
            pending: '#9e9e9e', claimed: '#2196f3', running: '#2196f3',
            paused: '#ff9800', waiting_for_approval: '#ff9800', waiting_for_input: '#ff9800',
            completed: '#4caf50', failed: '#f44336', cancelled: '#9e9e9e', blocked: '#9e9e9e',
        };
        const color = colors[status] || '#9e9e9e';
        return `<span class="wf-status-badge" style="background:${color}">${_escapeHtml(status)}</span>`;
    }

    function init() {
        const toggleBtn = document.getElementById('btn-workflows-toggle');
        if (toggleBtn) toggleBtn.addEventListener('click', togglePanel);

        const closeBtn = document.getElementById('workflows-close');
        if (closeBtn) closeBtn.addEventListener('click', closePanel);

        const statusFilter = document.getElementById('workflows-status-filter');
        if (statusFilter) {
            statusFilter.addEventListener('change', (e) => {
                _statusFilter = e.target.value;
                _refreshRunsList();
            });
        }
    }

    function openPanel() {
        // Close other panels
        if (typeof Sources !== 'undefined' && Sources.closePanel) Sources.closePanel();
        if (typeof Artifacts !== 'undefined' && Artifacts.closePanel) Artifacts.closePanel();
        if (typeof Canvas !== 'undefined' && Canvas.closePanel) Canvas.closePanel();

        const panel = document.getElementById('workflows-panel');
        if (panel) panel.style.display = '';

        const main = document.querySelector('.chat-main');
        if (main) main.classList.add('with-workflows-panel');

        _showListView();
        _refreshRunsList();
        _startAutoRefresh();
    }

    function closePanel() {
        const panel = document.getElementById('workflows-panel');
        if (panel) panel.style.display = 'none';

        const main = document.querySelector('.chat-main');
        if (main) main.classList.remove('with-workflows-panel');

        _stopAutoRefresh();
        _closeDetailEventSource();
    }

    function togglePanel() {
        const panel = document.getElementById('workflows-panel');
        if (panel && panel.style.display !== 'none') {
            closePanel();
        } else {
            openPanel();
        }
    }

    function _showListView() {
        _currentView = 'list';
        _currentRunId = null;
        const list = document.getElementById('workflows-list');
        const detail = document.getElementById('workflows-detail');
        if (list) list.style.display = '';
        if (detail) detail.style.display = 'none';
        _closeDetailEventSource();
    }

    function _showDetailView() {
        _currentView = 'detail';
        const list = document.getElementById('workflows-list');
        const detail = document.getElementById('workflows-detail');
        if (list) list.style.display = 'none';
        if (detail) detail.style.display = '';
    }

    async function _refreshRunsList() {
        try {
            let url = '/api/workflow-runs?limit=20';
            if (_statusFilter) url += `&status=${encodeURIComponent(_statusFilter)}`;
            _runs = await App.api(url);
            _renderRunsList();
        } catch (e) {
            const container = document.getElementById('workflows-list');
            if (container) container.innerHTML = '<div class="wf-empty">Could not load workflow runs.</div>';
        }
    }

    function _renderRunsList() {
        const container = document.getElementById('workflows-list');
        if (!container) return;

        if (!_runs || _runs.length === 0) {
            container.innerHTML = '<div class="wf-empty">No workflow runs found.</div>';
            return;
        }

        const html = _runs.map(run => `
            <div class="wf-run-card" data-run-id="${_escapeHtml(run.id)}">
                <div class="wf-run-card-header">
                    ${_statusBadge(run.status)}
                    <span class="wf-run-workflow">${_escapeHtml(run.workflow_id || '')}</span>
                </div>
                <div class="wf-run-card-meta">
                    <span class="wf-run-time">${_relativeTime(run.created_at)}</span>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;

        container.querySelectorAll('.wf-run-card').forEach(card => {
            card.addEventListener('click', () => {
                const runId = card.dataset.runId;
                _loadRunDetail(runId);
            });
        });
    }

    async function _loadRunDetail(runId) {
        _currentRunId = runId;
        _showDetailView();

        try {
            const run = await App.api(`/api/workflow-runs/${encodeURIComponent(runId)}`);
            _renderRunDetail(run);

            const terminal = ['completed', 'failed', 'cancelled', 'blocked'];
            if (!terminal.includes(run.status)) {
                _openDetailEventSource(runId);
            }
        } catch (e) {
            const container = document.getElementById('workflows-detail');
            if (container) container.innerHTML = '<div class="wf-empty">Could not load run details.</div>';
        }
    }

    function _renderRunDetail(run) {
        const container = document.getElementById('workflows-detail');
        if (!container) return;

        const steps = run.steps || [];
        const stepsHtml = steps.map(step => {
            const statusColor = step.result_status === 'success' ? '#4caf50'
                : step.result_status === 'failed' ? '#f44336' : '#9e9e9e';
            return `
                <div class="wf-step">
                    <span class="wf-step-dot" style="background:${statusColor}"></span>
                    <div class="wf-step-info">
                        <span class="wf-step-id">${_escapeHtml(step.step_id || '')}</span>
                        <span class="wf-step-status">${_escapeHtml(step.result_status || step.status || 'pending')}</span>
                        ${step.duration_ms ? `<span class="wf-step-duration">${(step.duration_ms / 1000).toFixed(1)}s</span>` : ''}
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="wf-detail-header">
                <button class="wf-back-btn" id="wf-back-btn">&larr; Back</button>
                ${_statusBadge(run.status)}
                <span class="wf-detail-workflow">${_escapeHtml(run.workflow_id || '')}</span>
            </div>
            <div class="wf-detail-meta">
                <div>Started: ${_relativeTime(run.started_at || run.created_at)}</div>
                ${run.completed_at ? `<div>Completed: ${_relativeTime(run.completed_at)}</div>` : ''}
            </div>
            <div class="wf-step-timeline">${stepsHtml || '<div class="wf-empty">No steps yet.</div>'}</div>
        `;

        const backBtn = document.getElementById('wf-back-btn');
        if (backBtn) {
            backBtn.addEventListener('click', () => {
                _showListView();
                _refreshRunsList();
            });
        }
    }

    function _openDetailEventSource(runId) {
        _closeDetailEventSource();
        const db = (typeof App !== 'undefined' && App.state) ? (App.state.currentDatabase || 'personal') : 'personal';
        const url = `/api/events?db=${encodeURIComponent(db)}&workflow_run_id=${encodeURIComponent(runId)}`;
        _workflowEventSource = new EventSource(url);
        _workflowEventSource.onmessage = () => {
            if (_currentRunId === runId) _loadRunDetail(runId);
        };
        _workflowEventSource.onerror = () => {
            _closeDetailEventSource();
        };
    }

    function _closeDetailEventSource() {
        if (_workflowEventSource) {
            _workflowEventSource.close();
            _workflowEventSource = null;
        }
    }

    function _startAutoRefresh() {
        _stopAutoRefresh();
        _refreshTimer = setInterval(() => {
            if (_currentView === 'list') _refreshRunsList();
        }, 30000);
    }

    function _stopAutoRefresh() {
        if (_refreshTimer) {
            clearInterval(_refreshTimer);
            _refreshTimer = null;
        }
    }

    return { init, openPanel, closePanel, togglePanel };
})();
