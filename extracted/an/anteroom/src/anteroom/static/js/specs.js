const Specs = (() => {
    let _specs = [];
    let _refreshTimer = null;
    let _currentFqn = null;

    function init() {
        const btn = document.getElementById('btn-specs-toggle');
        if (btn) btn.addEventListener('click', togglePanel);
        const backBtn = document.getElementById('specs-detail-back');
        if (backBtn) backBtn.addEventListener('click', _showList);
        const ids = ['specs-filter-status', 'specs-filter-phase', 'specs-filter-phase-status', 'specs-filter-namespace', 'specs-filter-has-runs'];
        for (const id of ids) {
            const el = document.getElementById(id);
            if (el) el.addEventListener(el.tagName === 'INPUT' ? 'input' : 'change', _refreshList);
        }
    }

    function openPanel() {
        const panel = document.getElementById('specs-panel');
        if (!panel) return;
        if (typeof Sources !== 'undefined' && Sources.closePanel) Sources.closePanel();
        if (typeof Canvas !== 'undefined' && Canvas.closePanel) Canvas.closePanel();
        if (typeof Artifacts !== 'undefined' && Artifacts.closePanel) Artifacts.closePanel();
        if (typeof Workflows !== 'undefined' && Workflows.closePanel) Workflows.closePanel();
        panel.style.display = '';
        const main = document.getElementById('chat-main');
        if (main) main.classList.add('with-specs-panel');
        _refreshList();
        _refreshTimer = setInterval(() => _refreshList(true), 30000);
    }

    function closePanel() {
        const panel = document.getElementById('specs-panel');
        if (panel) panel.style.display = 'none';
        const main = document.getElementById('chat-main');
        if (main) main.classList.remove('with-specs-panel');
        if (_refreshTimer) { clearInterval(_refreshTimer); _refreshTimer = null; }
        _currentFqn = null;
    }

    function togglePanel() {
        const panel = document.getElementById('specs-panel');
        if (panel && panel.style.display !== 'none') closePanel();
        else openPanel();
    }

    async function _refreshList(isAutoRefresh) {
        let url = '/api/specs/dashboard';
        const params = [];
        const _val = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : ''; };
        const statusVal = _val('specs-filter-status');
        const phaseVal = _val('specs-filter-phase');
        const phaseStatusVal = _val('specs-filter-phase-status');
        const nsVal = _val('specs-filter-namespace');
        if (statusVal) params.push('status=' + encodeURIComponent(statusVal));
        if (phaseVal) params.push('phase=' + encodeURIComponent(phaseVal));
        if (phaseStatusVal) params.push('phase_status=' + encodeURIComponent(phaseStatusVal));
        if (nsVal) params.push('namespace=' + encodeURIComponent(nsVal));
        const hasRunsEl = document.getElementById('specs-filter-has-runs');
        if (hasRunsEl && hasRunsEl.checked) params.push('has_runs=true');
        // Thread active space for scoped results
        const spaceId = (typeof App !== 'undefined' && App.state && App.state.currentSpaceId)
            ? App.state.currentSpaceId : null;
        if (spaceId) params.push('space_id=' + encodeURIComponent(spaceId));
        if (params.length) url += '?' + params.join('&');

        try {
            const data = await App.api(url);
            _specs = data.specs || [];
            // If viewing detail and this is a background refresh, re-fetch detail instead of clobbering
            if (_currentFqn && isAutoRefresh) {
                _showDetail(_currentFqn);
                return;
            }
            _renderList(data);
        } catch (e) {
            console.error('Failed to load specs dashboard:', e);
        }
    }

    function _renderList(data) {
        _currentFqn = null;
        const container = document.getElementById('specs-list');
        if (!container) return;

        const listDiv = document.getElementById('specs-list-items');
        const detailDiv = document.getElementById('specs-detail');
        if (listDiv) listDiv.style.display = '';
        if (detailDiv) detailDiv.style.display = 'none';

        if (!data.specs || data.specs.length === 0) {
            container.innerHTML = '<div class="specs-empty">No specs found.</div>';
            return;
        }

        const statusColors = {
            all_approved: '#22c55e',
            in_progress: '#06b6d4',
            stale: '#eab308',
            blocked: '#ef4444',
            draft: '#6b7280',
        };
        const phaseColors = {
            approved: '#22c55e',
            draft: '#6b7280',
            stale: '#eab308',
        };

        let html = '<div class="specs-totals">';
        const t = data.totals;
        html += '<span class="specs-total-count">' + t.total_specs + ' specs</span> ';
        if (t.all_approved) html += '<span style="color:#22c55e">' + t.all_approved + ' approved</span> ';
        if (t.in_progress) html += '<span style="color:#06b6d4">' + t.in_progress + ' in progress</span> ';
        if (t.stale) html += '<span style="color:#eab308">' + t.stale + ' stale</span> ';
        if (t.blocked) html += '<span style="color:#ef4444">' + t.blocked + ' blocked</span> ';
        if (t.draft) html += '<span style="color:#6b7280">' + t.draft + ' draft</span> ';
        html += '</div>';

        for (const spec of data.specs) {
            const sc = statusColors[spec.overall_status] || '#6b7280';
            const rs = spec.run_summary;
            let runText = '';
            if (rs.total > 0) {
                runText = rs.completed + '/' + rs.total;
                if (rs.failed > 0) runText += ' <span style="color:#ef4444">(' + rs.failed + ' failed)</span>';
            }

            html += '<div class="spec-card" data-fqn="' + _escapeAttr(spec.fqn) + '">';
            html += '<div class="spec-card-header">';
            html += '<span class="spec-fqn">' + _escapeHtml(spec.fqn) + '</span>';
            html += '<span class="spec-status-badge" style="color:' + sc + '">' + _escapeHtml(spec.overall_status) + '</span>';
            html += '</div>';
            html += '<div class="spec-card-phases">';
            for (const phase of ['requirements', 'design', 'tasks']) {
                const ps = spec.phases[phase] || 'draft';
                const pc = phaseColors[ps] || '#6b7280';
                const label = phase === 'requirements' ? 'Req' : phase === 'design' ? 'Des' : 'Tasks';
                html += '<span class="spec-phase-badge" style="color:' + pc + '">' + label + ': ' + ps + '</span>';
            }
            html += '</div>';
            if (runText) {
                html += '<div class="spec-card-runs">Runs: ' + runText + '</div>';
            }
            html += '</div>';
        }

        container.innerHTML = html;

        container.querySelectorAll('.spec-card').forEach(card => {
            card.addEventListener('click', () => {
                const fqn = card.dataset.fqn;
                if (fqn) _showDetail(fqn);
            });
        });
    }

    async function _showDetail(fqn) {
        _currentFqn = fqn;
        const listDiv = document.getElementById('specs-list-items');
        const detailDiv = document.getElementById('specs-detail');
        if (listDiv) listDiv.style.display = 'none';
        if (detailDiv) detailDiv.style.display = '';

        try {
            const data = await App.api('/api/specs/' + encodeURIComponent(fqn));
            _renderDetail(data);
        } catch (e) {
            if (detailDiv) detailDiv.innerHTML = '<div class="specs-empty">Failed to load spec.</div>';
        }
    }

    function _renderDetail(data) {
        const container = document.getElementById('specs-detail-content');
        if (!container) return;

        const phaseColors = { approved: '#22c55e', draft: '#6b7280', stale: '#eab308' };
        let html = '<h3>' + _escapeHtml(data.fqn) + '</h3>';
        html += '<div class="spec-detail-meta">';
        html += '<span>Mode: ' + _escapeHtml(data.mode || 'feature') + '</span>';
        html += '<span>Version: ' + (data.version || 1) + '</span>';
        html += '</div>';

        if (data.phase_info) {
            html += '<div class="spec-detail-phases">';
            for (const [phase, info] of Object.entries(data.phase_info)) {
                const pc = phaseColors[info.status] || '#6b7280';
                html += '<div class="spec-detail-phase">';
                html += '<strong style="color:' + pc + '">' + _escapeHtml(phase) + ': ' + _escapeHtml(info.status) + '</strong>';
                if (info.reason) html += '<div class="spec-detail-reason">' + _escapeHtml(info.reason) + '</div>';
                html += '</div>';
            }
            html += '</div>';
        }

        container.innerHTML = html;
    }

    function _showList() {
        _currentFqn = null;
        const listDiv = document.getElementById('specs-list-items');
        const detailDiv = document.getElementById('specs-detail');
        if (listDiv) listDiv.style.display = '';
        if (detailDiv) detailDiv.style.display = 'none';
    }

    function _escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function _escapeAttr(str) {
        return str.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    return { init, openPanel, closePanel, togglePanel };
})();
