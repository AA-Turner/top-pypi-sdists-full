// Popup UI controller - Mode selector and freehand recording
console.log('🎥 Popup loaded');

// Check if we should restore a previous page or active session
// This must block the rest of initialization to prevent race conditions
(async () => {
    // First check for saved page from collapse
    const { lastSidePanelPage, activeSession, mode } = await chrome.storage.local.get(['lastSidePanelPage', 'activeSession', 'mode']);

    if (lastSidePanelPage && lastSidePanelPage !== 'popup.html') {
        console.log('[EnvGen] Restoring previous side panel page:', lastSidePanelPage);
        await chrome.storage.local.remove('lastSidePanelPage');
        window.location.href = lastSidePanelPage;
        return; // Stop - we're navigating away
    }

    // Check if there's an active session we should restore to
    if (activeSession && activeSession.status === 'active') {
        console.log('[EnvGen] Active session found, redirecting to session-active');
        window.location.href = 'session-active.html';
        return; // Stop - we're navigating away
    }

    // Check if session just ended
    if (mode === 'session-ended' && activeSession) {
        console.log('[EnvGen] Session ended, redirecting to session-ended');
        window.location.href = 'session-ended.html';
        return; // Stop - we're navigating away
    }

    // No redirect needed, continue with normal popup initialization
    initializePopup();
})();

// Wrap initialization in a function so it can be called after redirect checks
function initializePopup() {
    console.log('[EnvGen] Initializing popup (no redirect needed)');

    const modeSelectorState = document.getElementById('mode-selector-state');
    const freehandRecordingState = document.getElementById('freehand-recording-state');
    const credentialsWarning = document.getElementById('credentialsWarning');
    const openSettings = document.getElementById('openSettings');
    const collapseBtn = document.getElementById('collapseBtn');
    const settingsBtn = document.getElementById('settingsBtn');
    const btnFreehand = document.getElementById('btn-freehand');
    const btnSession = document.getElementById('btn-session');
    const freehandPauseBtn = document.getElementById('freehand-pause-btn');
    const freehandStopBtn = document.getElementById('freehand-stop-btn');
    const freehandDuration = document.getElementById('freehand-duration');
    const freehandUiEvents = document.getElementById('freehand-ui-events');
    const freehandNetwork = document.getElementById('freehand-network');
    const recentList = document.getElementById('recent-list');
    const domainWarning = document.getElementById('domainWarning');

    let freehandRecordingInterval = null;
    let freehandStartTime = null;

    // Check if current tab is on a valid Plato domain
    async function checkDomain() {
        try {
            const tab = await getCurrentTab();
            const url = tab?.url || '';

            // Check if URL matches valid Plato domains:
            // - sims.plato.so (and dev/staging variants)
            // - *.web.plato.so (simulator-specific URLs like fathom.web.plato.so)
            const isValidPlatoDomain = url.includes('sims.plato.so') ||
                url.includes('dev.sims.plato.so') ||
                url.includes('staging.sims.plato.so') ||
                url.includes('.web.plato.so');

            if (!isValidPlatoDomain) {
                domainWarning.style.display = 'block';
                // Disable recording buttons if not on valid domain
                if (btnFreehand) btnFreehand.disabled = true;
                if (btnSession) btnSession.disabled = true;
                return false;
            } else {
                domainWarning.style.display = 'none';
                // Enable recording buttons
                if (btnFreehand) btnFreehand.disabled = false;
                if (btnSession) btnSession.disabled = false;
                return true;
            }
        } catch (error) {
            console.error('[EnvGen] Error checking domain:', error);
            // Show warning if we can't check
            domainWarning.style.display = 'block';
            if (btnFreehand) btnFreehand.disabled = true;
            if (btnSession) btnSession.disabled = true;
            return false;
        }
    }

    // Check Plato API configuration
    async function checkCredentials() {
        const settings = await chrome.storage.local.get(['platoApiKey']);
        if (!settings.platoApiKey) {
            credentialsWarning.style.display = 'block';
        } else {
            credentialsWarning.style.display = 'none';
        }
    }

    // Listen for storage changes to update credentials warning
    chrome.storage.onChanged.addListener((changes, areaName) => {
        if (areaName === 'local' && changes.platoApiKey) {
            checkCredentials();
        }
    });

    // Collapse side panel - use window.close() to actually close it
    // But first save the current page so we can restore it when reopening
    if (collapseBtn) {
        collapseBtn.addEventListener('click', async () => {
            // Save current page path before closing
            const currentPath = window.location.pathname.split('/').pop() || 'popup.html';
            await chrome.storage.local.set({ lastSidePanelPage: currentPath });
            window.close();
        });
    }

    // Get current tab
    async function getCurrentTab() {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        return tab;
    }

    // Show mode selector state
    function showModeSelector() {
        modeSelectorState.style.display = 'block';
        freehandRecordingState.classList.remove('active');
        loadRecentActivity();
    }

    // Show freehand recording state
    function showFreehandRecording() {
        modeSelectorState.style.display = 'none';
        freehandRecordingState.classList.add('active');
        updateFreehandRecordingUI();
    }

    // Update freehand recording UI
    async function updateFreehandRecordingUI() {
        const response = await chrome.runtime.sendMessage({ type: 'GET_STATUS' });

        if (response.isRecording) {
            // Update duration
            if (freehandStartTime) {
                const elapsed = Date.now() - freehandStartTime;
                freehandDuration.textContent = formatDuration(elapsed);
            }

            // Update stats
            freehandUiEvents.textContent = response.eventCount || 0;
            freehandNetwork.textContent = response.networkEventCount || 0;

            // Update pause button
            if (response.isPaused) {
                // Active state: Yellow with "Pause Marker Active"
                freehandPauseBtn.textContent = '⏸️ Pause Marker Active (Ctrl+Shift+Space)';
                freehandPauseBtn.style.backgroundColor = '#f59e0b'; // Yellow when active
                freehandPauseBtn.classList.remove('btn-success');
                freehandPauseBtn.classList.add('btn-warning');
            } else {
                // Inactive state: Green with "Pause Marker Inactive"
                freehandPauseBtn.textContent = '⏸️ Pause Marker Inactive (Ctrl+Shift+Space)';
                freehandPauseBtn.style.backgroundColor = '#10b981'; // Green when inactive
                freehandPauseBtn.classList.remove('btn-warning');
                freehandPauseBtn.classList.add('btn-success');
            }
        } else {
            // Not recording, show mode selector
            showModeSelector();
        }
    }

    // Start freehand recording
    async function startFreehandRecording() {
        try {
            const tab = await getCurrentTab();
            const response = await chrome.runtime.sendMessage({
                type: 'START_RECORDING',
                tabId: tab.id,
                sessionId: null // Freehand has no session
            });

            if (response.success) {
                freehandStartTime = Date.now();
                showFreehandRecording();

                // Start timer
                freehandRecordingInterval = setInterval(() => {
                    updateFreehandRecordingUI();
                }, 500);
            } else {
                alert('Failed to start recording: ' + (response.error || 'Unknown error'));
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }

    // Stop freehand recording
    async function stopFreehandRecording() {
        try {
            if (freehandRecordingInterval) {
                clearInterval(freehandRecordingInterval);
                freehandRecordingInterval = null;
            }

            const response = await chrome.runtime.sendMessage({
                type: 'STOP_RECORDING'
            });

            if (response.success) {
                freehandStartTime = null;
                showModeSelector();
            } else {
                // Upload failures are critical - show error prominently
                const errorMsg = response.error || 'Unknown error';
                alert(`❌ Recording stopped but upload failed!\n\n${errorMsg}\n\nPlease check your API key in Settings.`);
                console.error('[EnvGen Popup] Upload failed:', errorMsg);
                // Still show mode selector
                freehandStartTime = null;
                showModeSelector();
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }

    // Toggle pause marker
    async function togglePauseMarker() {
        try {
            await chrome.runtime.sendMessage({ type: 'TOGGLE_PAUSE' });
            updateFreehandRecordingUI();
        } catch (error) {
            console.error('Error toggling pause:', error);
        }
    }

    // Load recent activity
    async function loadRecentActivity() {
        try {
            const { sessions } = await chrome.storage.local.get(['sessions']);
            const recentSessions = (sessions || []).slice(-3).reverse();

            if (recentSessions.length === 0) {
                recentList.innerHTML = '<div class="recent-item">No recordings yet</div>';
                return;
            }

            recentList.innerHTML = recentSessions.map(session => {
                const timeAgo = formatTimeAgo(session.recordingEnd || session.recordingStart);
                return `<div class="recent-item">• Session: ${session.sessionId?.substring(0, 8) || 'unknown'} (${timeAgo})</div>`;
            }).join('');
        } catch (error) {
            console.error('Error loading recent activity:', error);
            recentList.innerHTML = '<div class="recent-item">Error loading activity</div>';
        }
    }

    // Format duration
    function formatDuration(ms) {
        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);

        const h = String(hours).padStart(2, '0');
        const m = String(minutes % 60).padStart(2, '0');
        const s = String(seconds % 60).padStart(2, '0');

        return `${h}:${m}:${s}`;
    }

    // Format time ago
    function formatTimeAgo(timestamp) {
        const seconds = Math.floor((Date.now() - timestamp) / 1000);
        if (seconds < 60) return `${seconds}s ago`;
        const minutes = Math.floor(seconds / 60);
        if (minutes < 60) return `${minutes}m ago`;
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        const days = Math.floor(hours / 24);
        return `${days}d ago`;
    }

    // Event listeners
    btnFreehand.addEventListener('click', startFreehandRecording);
    btnSession.addEventListener('click', () => {
        window.location.href = 'session-setup.html';
    });
    settingsBtn.addEventListener('click', () => {
        chrome.runtime.openOptionsPage();
    });
    openSettings.addEventListener('click', () => {
        chrome.runtime.openOptionsPage();
    });
    freehandPauseBtn.addEventListener('click', togglePauseMarker);
    freehandStopBtn.addEventListener('click', stopFreehandRecording);

    // Initialize popup state
    (async () => {
        // Check domain first - this is critical
        await checkDomain();
        await checkCredentials();

        // Check current recording state
        chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
            if (response && response.isRecording) {
                // Freehand recording is active (session recordings redirect at top of file)
                showFreehandRecording();
            } else {
                showModeSelector();
            }
        });
    })();

    // Auto-refresh when recording
    setInterval(() => {
        if (freehandRecordingState.classList.contains('active')) {
            updateFreehandRecordingUI();
        }
    }, 500);

} // End of initializePopup()
