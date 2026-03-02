// Sessions page controller

// IndexedDB for storing video blobs
const DB_NAME = 'envgen_sessions';
const DB_VERSION = 1;
const STORE_NAME = 'videos';

let db = null;

// Initialize IndexedDB
async function initDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onerror = () => reject(request.error);
        request.onsuccess = () => {
            db = request.result;
            resolve(db);
        };

        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                db.createObjectStore(STORE_NAME, { keyPath: 'sessionId' });
            }
        };
    });
}

// Get all sessions from Chrome storage
async function getSessions() {
    const result = await chrome.storage.local.get('sessions');
    return result.sessions || [];
}

// Get video blob from IndexedDB
async function getVideoBlob(sessionId) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([STORE_NAME], 'readonly');
        const store = transaction.objectStore(STORE_NAME);
        const request = store.get(sessionId);

        request.onsuccess = () => resolve(request.result?.videoBlob);
        request.onerror = () => reject(request.error);
    });
}

// Delete session
async function deleteSession(sessionId) {
    // Delete from Chrome storage
    const sessions = await getSessions();
    const filtered = sessions.filter(s => s.sessionId !== sessionId);
    await chrome.storage.local.set({ sessions: filtered });

    // Delete video from IndexedDB
    if (db) {
        const transaction = db.transaction([STORE_NAME], 'readwrite');
        const store = transaction.objectStore(STORE_NAME);
        store.delete(sessionId);
    }
}

// Manual upload removed - all uploads are now automatic
// If a session doesn't have upload info, it means upload failed (exception thrown)

// Helper function to convert blob to base64
async function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

// Download session files
async function downloadSession(sessionId) {
    try {
        const sessions = await getSessions();
        const session = sessions.find(s => s.sessionId === sessionId);

        if (!session) {
            alert('Session not found');
            return;
        }

        console.log('[EnvGen Sessions] Downloading session:', sessionId);

        // Download video
        const videoBlob = await getVideoBlob(sessionId);
        if (videoBlob) {
            console.log('[EnvGen Sessions] Video blob retrieved, size:', videoBlob.size);
            const videoUrl = URL.createObjectURL(videoBlob);
            const a = document.createElement('a');
            a.href = videoUrl;
            a.download = `envgen_recording_${sessionId}.webm`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            // Delay cleanup to ensure download starts
            setTimeout(() => URL.revokeObjectURL(videoUrl), 100);
        } else {
            console.error('[EnvGen Sessions] Video blob not found');
            alert('Video not found in storage');
            return;
        }

        // Download events JSON
        const eventsJson = JSON.stringify({
            recording_start: session.recordingStart,
            recording_end: session.recordingEnd,
            ui_events: session.events,
            network_events: session.networkEvents || [],
            stats: {
                ui_event_count: session.eventCount,
                network_event_count: session.networkEventCount || 0,
                duration_ms: session.recordingEnd - session.recordingStart
            }
        }, null, 2);

        const eventsBlob = new Blob([eventsJson], { type: 'application/json' });
        const eventsUrl = URL.createObjectURL(eventsBlob);
        const a2 = document.createElement('a');
        a2.href = eventsUrl;
        a2.download = `envgen_recording_${sessionId}_events.json`;
        document.body.appendChild(a2);
        a2.click();
        document.body.removeChild(a2);

        setTimeout(() => URL.revokeObjectURL(eventsUrl), 100);

        console.log('[EnvGen Sessions] Downloads triggered successfully');
    } catch (error) {
        console.error('[EnvGen Sessions] Error downloading session:', error);
        alert('Error downloading session: ' + error.message);
    }
}

// Format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Format duration
function formatDuration(start, end) {
    const durationMs = end - start;
    const seconds = Math.floor(durationMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
        return `${minutes}m ${remainingSeconds}s`;
    }
    return `${seconds}s`;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Global flag to track if listeners are attached
let listenersAttached = false;

// Render sessions
async function renderSessions() {
    const container = document.getElementById('sessions-container');
    const emptyState = document.getElementById('empty-state');

    const sessions = await getSessions();

    if (sessions.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    // Sort by timestamp descending
    sessions.sort((a, b) => b.recordingEnd - a.recordingEnd);

    container.innerHTML = sessions.map(session => {
        const duration = formatDuration(session.recordingStart, session.recordingEnd);
        const timestamp = formatTimestamp(session.recordingEnd);
        const fileSize = session.videoSize ? formatFileSize(session.videoSize) : 'Unknown';
        const shortId = session.sessionId.split('-')[0];

        // Check if session has S3 paths from upload
        const hasS3Paths = session.s3Paths && (session.s3Paths.videoPath || session.s3Paths.eventsPath);

        console.log('[Sessions] Rendering session:', session.sessionId);
        console.log('[Sessions] s3Paths:', session.s3Paths);
        console.log('[Sessions] hasS3Paths:', hasS3Paths);

        return `
            <div class="session-card" data-session-id="${session.sessionId}">
                <div class="session-header">
                    <div>
                        <div class="session-id">${shortId}</div>
                        <div class="session-timestamp">${timestamp}</div>
                        ${hasS3Paths ? `
                            <div style="margin-top: 8px;">
                                ${session.s3Paths.videoPath ? `
                                    <div style="margin-bottom: 4px;">
                                        <div style="font-size: 9px; color: #666; margin-bottom: 2px;">📹 Video:</div>
                                        <div style="display: flex; gap: 4px;">
                                            <input type="text" readonly value="${session.s3Paths.videoPath}"
                                                   class="s3-path-input"
                                                   style="flex: 1; font-size: 9px; font-family: monospace; padding: 4px; background: #f9fafb; border: 1px solid #d1d5db; border-radius: 4px;">
                                            <button class="btn-copy-path btn-secondary" data-path="${session.s3Paths.videoPath}" style="padding: 4px 8px; font-size: 9px;">Copy</button>
                                        </div>
                                    </div>
                                ` : ''}
                                ${session.s3Paths.eventsPath ? `
                                    <div>
                                        <div style="font-size: 9px; color: #666; margin-bottom: 2px;">📄 Events:</div>
                                        <div style="display: flex; gap: 4px;">
                                            <input type="text" readonly value="${session.s3Paths.eventsPath}"
                                                   class="s3-path-input"
                                                   style="flex: 1; font-size: 9px; font-family: monospace; padding: 4px; background: #f9fafb; border: 1px solid #d1d5db; border-radius: 4px;">
                                            <button class="btn-copy-path btn-secondary" data-path="${session.s3Paths.eventsPath}" style="padding: 4px 8px; font-size: 9px;">Copy</button>
                                        </div>
                                    </div>
                                ` : ''}
                            </div>
                        ` : ''}
                    </div>
                </div>

                <div class="session-stats">
                    <div class="stat">
                        <span class="stat-label">Duration</span>
                        <span class="stat-value">${duration}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">UI Events</span>
                        <span class="stat-value">${session.eventCount}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Network</span>
                        <span class="stat-value">${session.networkEventCount || 0}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Video Size</span>
                        <span class="stat-value">${fileSize}</span>
                    </div>
                </div>

                <div class="session-actions">
                    ${session.s3Paths ? `
                        <span style="color: #10b981; font-size: 12px; margin-right: 12px;">✓ Uploaded</span>
                    ` : `
                        <span style="color: #ef4444; font-size: 12px; margin-right: 12px;">✗ Upload Failed</span>
                    `}
                    <button class="btn-primary btn-download" data-session-id="${session.sessionId}">
                        Download
                    </button>
                    <button class="btn-secondary btn-play" data-session-id="${session.sessionId}">
                        Play Video
                    </button>
                    <button class="btn-danger btn-delete" data-session-id="${session.sessionId}">
                        Delete
                    </button>
                </div>

                <video id="video-${session.sessionId}" class="video-preview" controls style="display: none;"></video>

                <div id="s3-paths-${session.sessionId}" class="s3-paths">
                    <div class="s3-path-item"><span class="s3-path-label">Video:</span><span id="s3-video-path-${session.sessionId}"></span></div>
                    <div class="s3-path-item"><span class="s3-path-label">Events:</span><span id="s3-events-path-${session.sessionId}"></span></div>
                </div>
            </div>
        `;
    }).join('');

    // Attach event listeners on first render only
    if (!listenersAttached) {
        attachEventListeners();
        listenersAttached = true;
    }
}

// Attach event listeners to buttons (only once)
function attachEventListeners() {
    // Use event delegation on the container
    const container = document.getElementById('sessions-container');

    console.log('[EnvGen Sessions] Attaching event listeners');

    // Add click listener with delegation
    container.addEventListener('click', async (e) => {
        const button = e.target.closest('button');
        if (!button) return;

        // Handle copy path buttons
        if (button.classList.contains('btn-copy-path')) {
            const path = button.dataset.path;
            if (!path) return;

            try {
                // Use modern Clipboard API
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(path);
                    const originalText = button.textContent;
                    button.textContent = '✓';
                    button.style.backgroundColor = '#10b981';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.style.backgroundColor = '';
                    }, 1500);
                } else {
                    // Fallback for older browsers
                    const input = button.previousElementSibling;
                    if (input && input.tagName === 'INPUT') {
                        input.select();
                        document.execCommand('copy');
                        button.textContent = '✓';
                        setTimeout(() => {
                            button.textContent = 'Copy';
                        }, 1500);
                    }
                }
            } catch (error) {
                console.error('[EnvGen Sessions] Error copying path:', error);
                button.textContent = '✗';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 1500);
            }
            return;
        }

        const sessionId = button.dataset.sessionId;
        if (!sessionId) return;

        console.log('[EnvGen Sessions] Button clicked:', button.className, sessionId);

        try {
            if (button.classList.contains('btn-download')) {
                console.log('[EnvGen Sessions] Downloading session...');
                await downloadSession(sessionId);
            } else if (button.classList.contains('btn-play')) {
                console.log('[EnvGen Sessions] Playing session...');
                await playSession(sessionId);
            } else if (button.classList.contains('btn-delete')) {
                console.log('[EnvGen Sessions] Deleting session...');
                await confirmDeleteSession(sessionId);
            }
        } catch (error) {
            console.error('[EnvGen Sessions] Error handling button click:', error);
            alert('Error: ' + error.message);
        }
    });
}

// Play video
async function playSession(sessionId) {
    const videoElement = document.getElementById(`video-${sessionId}`);

    if (videoElement.style.display === 'block') {
        videoElement.style.display = 'none';
        videoElement.pause();
        return;
    }

    const videoBlob = await getVideoBlob(sessionId);
    if (videoBlob) {
        const videoUrl = URL.createObjectURL(videoBlob);
        videoElement.src = videoUrl;
        videoElement.style.display = 'block';
        videoElement.play();
    } else {
        alert('Video not found');
    }
}

// Confirm delete
async function confirmDeleteSession(sessionId) {
    if (confirm('Are you sure you want to delete this session? This cannot be undone.')) {
        await deleteSession(sessionId);
        await renderSessions();
    }
}

// Delete all sessions
async function deleteAllSessions() {
    const sessions = await getSessions();

    if (sessions.length === 0) {
        alert('No sessions to delete');
        return;
    }

    const message = `Are you sure you want to delete all ${sessions.length} session(s)? This cannot be undone.`;
    if (!confirm(message)) {
        return;
    }

    try {
        console.log('[EnvGen Sessions] Deleting all sessions...');

        // Clear all from Chrome storage
        await chrome.storage.local.set({ sessions: [] });

        // Clear all from IndexedDB
        if (db) {
            const transaction = db.transaction([STORE_NAME], 'readwrite');
            const store = transaction.objectStore(STORE_NAME);

            // Get all keys and delete them
            const getAllKeysRequest = store.getAllKeys();
            getAllKeysRequest.onsuccess = () => {
                const keys = getAllKeysRequest.result;
                keys.forEach(key => {
                    store.delete(key);
                });
            };
        }

        console.log('[EnvGen Sessions] All sessions deleted');
        await renderSessions();
    } catch (error) {
        console.error('[EnvGen Sessions] Error deleting all sessions:', error);
        alert('Error deleting sessions: ' + error.message);
    }
}

// Initialize
(async () => {
    await initDB();
    await renderSessions();

    // Attach delete all button listener
    const deleteAllBtn = document.getElementById('delete-all-btn');
    if (deleteAllBtn) {
        deleteAllBtn.addEventListener('click', deleteAllSessions);
        console.log('[EnvGen Sessions] Delete all button listener attached');
    }
})();
