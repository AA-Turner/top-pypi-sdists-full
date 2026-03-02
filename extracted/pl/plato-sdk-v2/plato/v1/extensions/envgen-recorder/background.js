// Background service worker for EnvGen Recorder

// Open side panel when extension icon is clicked
chrome.action.onClicked.addListener((tab) => {
    chrome.sidePanel.open({ tabId: tab.id });
});

// Handle keyboard shortcut for pause marker
chrome.commands.onCommand.addListener(async (command) => {
    if (command === 'toggle-pause') {
        console.log('[EnvGen] Keyboard shortcut triggered for pause marker');
        try {
            const result = await togglePauseMarker();
            console.log('[EnvGen] Pause marker toggle result:', result);
        } catch (error) {
            console.error('[EnvGen] Error handling pause marker shortcut:', error);
        }
    }
});

let isRecording = false;
let isPaused = false; // UI state only - recording continues
let pauseMarkerCount = 0;
let allEvents = [];
let networkEvents = [];
let recordingStartTime = null;
let currentTabId = null;
let networkRequestMap = new Map(); // Track pending requests
let currentRecording = {
    id: null,
    sessionId: null,
    startedAt: null
};

// Intercept new tab creation during recording
chrome.tabs.onCreated.addListener(async (tab) => {
    if (!isRecording || !currentTabId) return;

    // If a new tab is created during recording, wait for URL then redirect
    if (tab.id !== currentTabId) {
        console.log('[EnvGen] ⚠️  New tab created during recording, intercepting:', tab.id);

        // Wait for the tab to get a URL
        let attempts = 0;
        const maxAttempts = 20; // 2 seconds max

        const checkUrl = async () => {
            try {
                const newTab = await chrome.tabs.get(tab.id);
                const url = newTab.url || newTab.pendingUrl;

                if (url && url !== 'chrome://newtab/' && url !== 'about:blank' && !url.startsWith('chrome://')) {
                    console.log('[EnvGen] Got URL from new tab:', url);
                    console.log('[EnvGen] Redirecting recording tab to:', url);

                    // Navigate the recording tab to this URL
                    await chrome.tabs.update(currentTabId, { url: url, active: true });

                    // Close the new tab
                    console.log('[EnvGen] Closing intercepted tab:', tab.id);
                    await chrome.tabs.remove(tab.id);
                    return true;
                }

                attempts++;
                if (attempts < maxAttempts) {
                    setTimeout(checkUrl, 100);
                } else {
                    // Couldn't get URL, just close the tab
                    console.log('[EnvGen] No valid URL after', maxAttempts, 'attempts, closing tab');
                    await chrome.tabs.remove(tab.id);
                }
            } catch (e) {
                // Tab might be closed already
                console.log('[EnvGen] Tab check failed:', e.message);
            }
        };

        // Start checking for URL
        setTimeout(checkUrl, 50);
    }
});

// Also intercept when tabs get activated (user switches to new tab)
chrome.tabs.onActivated.addListener(async (activeInfo) => {
    if (!isRecording || !currentTabId) return;

    // If user switches to a different tab during recording, switch back
    if (activeInfo.tabId !== currentTabId) {
        console.log('[EnvGen] ⚠️  Tab switch detected during recording, forcing back to recording tab');
        console.log('[EnvGen] Switched from tab', currentTabId, 'to tab', activeInfo.tabId);

        try {
            // Switch back to the recording tab
            await chrome.tabs.update(currentTabId, { active: true });
            console.log('[EnvGen] ✓ Switched back to recording tab:', currentTabId);
        } catch (e) {
            console.error('[EnvGen] Could not switch back to recording tab:', e);
        }
    }
});

// Listen for messages from popup and content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'START_RECORDING') {
        startRecording(message.tabId, message.sessionId).then(sendResponse);
        return true; // Async response
    } else if (message.type === 'STOP_RECORDING') {
        stopRecording().then(sendResponse);
        return true; // Async response
    } else if (message.type === 'TOGGLE_PAUSE') {
        togglePauseMarker().then(sendResponse);
        return true; // Async response
    } else if (message.type === 'GET_STATUS') {
        sendResponse({
            isRecording,
            isPaused,
            eventCount: allEvents.length,
            pauseMarkerCount,
            networkEventCount: networkEvents.length,
            recordingStartTime: recordingStartTime || null,
            currentTabId: currentTabId || null,
            sessionId: currentRecording.sessionId || null
        });
    } else if (message.type === 'UPLOAD_SESSION_RECORDING') {
        // Upload recording when ending session
        uploadSessionRecording(message.sessionId).then(sendResponse);
        return true; // Async response
    } else if (message.type === 'UI_EVENTS') {
        // Collect events from content script
        // Log which tab the events are coming from
        const fromTabId = sender.tab?.id;
        console.log('[EnvGen Background] Received', message.events.length, 'UI events from tab', fromTabId, '(recording tab:', currentTabId, '), total now:', allEvents.length + message.events.length);

        // ALWAYS append events, even if from different tab
        // Tag events with source tab for debugging
        const taggedEvents = message.events.map(e => ({
            ...e,
            source_tab: fromTabId
        }));
        allEvents.push(...taggedEvents);

        // Warn if events coming from wrong tab
        if (isRecording && fromTabId !== currentTabId) {
            console.warn('[EnvGen Background] WARNING: Received events from tab', fromTabId, 'but recording tab is', currentTabId);
        }

        sendResponse({ success: true });
    }
    // Removed UPLOAD_TO_S3 handler - all uploads are automatic now
});

async function ensureOffscreenDocument() {
    // Check if offscreen document already exists
    const existingContexts = await chrome.runtime.getContexts({
        contextTypes: ['OFFSCREEN_DOCUMENT'],
        documentUrls: [chrome.runtime.getURL('offscreen.html')]
    });

    if (existingContexts.length > 0) {
        return;
    }

    // Create offscreen document
    await chrome.offscreen.createDocument({
        url: 'offscreen.html',
        reasons: ['USER_MEDIA'],
        justification: 'Recording tab video'
    });
}

// Network event listeners
chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
        // Capture network events from current tab during recording
        if (!isRecording) return;
        // Only capture from the tab we're actively recording
        if (details.tabId !== currentTabId) return;

        const timestamp = Date.now();
        networkRequestMap.set(details.requestId, {
            requestId: details.requestId,
            timestamp,
            url: details.url,
            method: details.method,
            type: details.type,
            initiator: details.initiator,
            requestBody: details.requestBody
        });
    },
    { urls: ["<all_urls>"] },
    ["requestBody"]
);

chrome.webRequest.onSendHeaders.addListener(
    (details) => {
        if (!isRecording || details.tabId !== currentTabId) return;

        const request = networkRequestMap.get(details.requestId);
        if (request) {
            request.requestHeaders = details.requestHeaders;
        }
    },
    { urls: ["<all_urls>"] },
    ["requestHeaders"]
);

chrome.webRequest.onCompleted.addListener(
    (details) => {
        if (!isRecording || details.tabId !== currentTabId) return;

        const request = networkRequestMap.get(details.requestId);
        if (request) {
            const completedEvent = {
                ...request,
                status: 'completed',
                statusCode: details.statusCode,
                responseHeaders: details.responseHeaders,
                completedTimestamp: Date.now(),
                duration: Date.now() - request.timestamp,
                ip: details.ip,
                fromCache: details.fromCache
            };

            networkEvents.push(completedEvent);
            networkRequestMap.delete(details.requestId);
        }
    },
    { urls: ["<all_urls>"] },
    ["responseHeaders"]
);

chrome.webRequest.onErrorOccurred.addListener(
    (details) => {
        if (!isRecording || details.tabId !== currentTabId) return;

        const request = networkRequestMap.get(details.requestId);
        if (request) {
            const errorEvent = {
                ...request,
                status: 'error',
                error: details.error,
                completedTimestamp: Date.now(),
                duration: Date.now() - request.timestamp
            };

            networkEvents.push(errorEvent);
            networkRequestMap.delete(details.requestId);
        }
    },
    { urls: ["<all_urls>"] }
);

async function togglePauseMarker() {
    if (!isRecording) {
        console.warn('[EnvGen] Cannot toggle pause marker - not recording');
        return { success: false, error: 'Not recording' };
    }

    try {
        // Get the active tab if currentTabId is not set or invalid
        let activeTabId = currentTabId;
        if (!activeTabId) {
            console.log('[EnvGen] currentTabId not set, getting active tab');
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (tab && tab.id) {
                activeTabId = tab.id;
                console.log('[EnvGen] Using active tab ID:', activeTabId);
            } else {
                console.error('[EnvGen] Could not find active tab');
                return { success: false, error: 'No active tab found' };
            }
        }

        isPaused = !isPaused;
        const timestamp = Date.now();

        // Get current tab URL
        let currentUrl = '';
        try {
            const tab = await chrome.tabs.get(activeTabId);
            currentUrl = tab.url || '';
        } catch (e) {
            console.warn('[EnvGen] Could not get current tab URL:', e);
        }

        if (isPaused) {
            // Add pause marker - recording continues!
            pauseMarkerCount++;
            console.log('[EnvGen] Pause marker added at', timestamp);

            allEvents.push({
                type: 'pause_marker',
                seq_id: allEvents.length,
                timestamp: timestamp,
                url: currentUrl,
                target: {},
                metadata: {
                    marker_number: pauseMarkerCount,
                    description: 'User toggled pause marker - recording continues'
                }
            });

            // Show visual indicator in content script
            try {
                await chrome.tabs.sendMessage(activeTabId, {
                    type: 'SHOW_PAUSE_INDICATOR'
                });
                console.log('[EnvGen] Pause indicator shown on tab:', activeTabId);
            } catch (e) {
                console.warn('[EnvGen] Could not show pause indicator:', e);
                // Try to inject content script if it's not loaded
                try {
                    await chrome.scripting.executeScript({
                        target: { tabId: activeTabId },
                        files: ['content.js']
                    });
                    // Retry sending message
                    await chrome.tabs.sendMessage(activeTabId, {
                        type: 'SHOW_PAUSE_INDICATOR'
                    });
                } catch (retryError) {
                    console.error('[EnvGen] Failed to inject content script and show indicator:', retryError);
                }
            }
        } else {
            // Add resume marker
            console.log('[EnvGen] Resume marker added at', timestamp);

            allEvents.push({
                type: 'resume_marker',
                seq_id: allEvents.length,
                timestamp: timestamp,
                url: currentUrl,
                target: {},
                metadata: {
                    marker_number: pauseMarkerCount,
                    description: 'User toggled resume marker - recording was never stopped'
                }
            });

            // Hide visual indicator
            try {
                await chrome.tabs.sendMessage(activeTabId, {
                    type: 'HIDE_PAUSE_INDICATOR'
                });
                console.log('[EnvGen] Pause indicator hidden on tab:', activeTabId);
            } catch (e) {
                console.warn('[EnvGen] Could not hide pause indicator:', e);
            }
        }

        return { success: true, isPaused, pauseMarkerCount };
    } catch (error) {
        console.error('[EnvGen] Error toggling pause marker:', error);
        return { success: false, error: error.message };
    }
}

async function startRecording(tabId, sessionId = null) {
    if (isRecording) {
        return { success: false, error: 'Already recording' };
    }

    try {
        currentTabId = tabId;
        allEvents = [];
        networkEvents = [];
        networkRequestMap.clear();
        recordingStartTime = Date.now();
        isPaused = false;
        pauseMarkerCount = 0;

        // Set up current recording
        currentRecording = {
            id: crypto.randomUUID(),
            sessionId: sessionId,
            startedAt: Date.now()
        };

        console.log('[EnvGen] Recording initialized:');
        console.log('  Tab ID:', currentTabId);
        console.log('  Start time:', new Date(recordingStartTime).toISOString());
        console.log('  Events reset to empty array');

        // Ensure offscreen document exists
        await ensureOffscreenDocument();

        // Ensure content script is injected and ready
        console.log('[EnvGen] Ensuring content script is loaded...');
        let contentScriptReady = false;

        for (let i = 0; i < 10; i++) {
            try {
                await chrome.tabs.sendMessage(tabId, { type: 'CLEAR_EVENTS' });
                contentScriptReady = true;
                console.log('[EnvGen] Content script is ready');
                break;
            } catch (e) {
                console.log(`[EnvGen] Content script not ready, attempting injection (retry ${i + 1}/10)`);

                // Try to inject content script programmatically
                try {
                    await chrome.scripting.executeScript({
                        target: { tabId: tabId },
                        files: ['content.js']
                    });
                    console.log('[EnvGen] Content script injected programmatically');
                    await new Promise(resolve => setTimeout(resolve, 500));
                } catch (injectError) {
                    console.warn('[EnvGen] Could not inject content script:', injectError.message);
                    await new Promise(resolve => setTimeout(resolve, 200));
                }
            }
        }

        if (!contentScriptReady) {
            throw new Error('Content script not ready after 10 retries. Please refresh the page and try again.');
        }

        // Get stream ID for tab capture
        const streamId = await chrome.tabCapture.getMediaStreamId({
            targetTabId: tabId
        });

        console.log('[EnvGen] Got streamId:', streamId);

        // Wait a bit for offscreen document to be ready
        await new Promise(resolve => setTimeout(resolve, 100));

        // Start recording in offscreen document FIRST
        const response = await chrome.runtime.sendMessage({
            type: 'START_RECORDING',
            streamId: streamId,
            target: 'offscreen'
        });

        if (!response || !response.success) {
            throw new Error(response?.error || 'Failed to start recording');
        }

        // Now show calibration marker AFTER recording has started
        // This ensures the marker is captured in the video
        console.log('[EnvGen] Showing calibration marker...');
        let markerShown = false;
        for (let i = 0; i < 5; i++) {
            try {
                const markerResponse = await chrome.tabs.sendMessage(tabId, { type: 'SHOW_RECORDING_MARKER' });
                if (markerResponse && markerResponse.success) {
                    markerShown = true;
                    console.log('[EnvGen] Calibration marker shown successfully');
                    break;
                }
            } catch (e) {
                console.warn(`[EnvGen] Calibration marker attempt ${i + 1}/5 failed:`, e);
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }

        if (!markerShown) {
            console.error('[EnvGen] WARNING: Calibration marker could not be shown!');
        }

        isRecording = true;
        isPaused = false; // Start in inactive state (green button)
        console.log('[EnvGen] Recording started');
        return { success: true };
    } catch (error) {
        console.error('[EnvGen] Error starting recording:', error);
        return { success: false, error: error.message };
    }
}

async function stopRecording() {
    if (!isRecording) {
        return { success: false, error: 'Not recording' };
    }

    try {
        // Get final events from content script (in case some weren't sent yet)
        try {
            const response = await chrome.tabs.sendMessage(currentTabId, {
                type: 'GET_EVENTS'
            });

            if (response && response.events && response.events.length > 0) {
                // Append any remaining events, don't overwrite!
                console.log('[EnvGen] Appending', response.events.length, 'final events from content script');
                allEvents.push(...response.events);
            }
        } catch (e) {
            console.warn('[EnvGen] Could not get events from content script:', e);
        }

        // Stop recording in offscreen document
        const videoResponse = await chrome.runtime.sendMessage({
            type: 'STOP_RECORDING',
            target: 'offscreen'
        });

        if (!videoResponse || !videoResponse.success) {
            throw new Error(videoResponse?.error || 'Failed to stop recording');
        }

        isRecording = false;

        // Generate unique UUID for recording (different from sessionId)
        const recordingId = currentRecording.id;
        const sessionId = currentRecording.sessionId; // May be null for freehand
        const recordingEnd = Date.now();

        const videoBlob = videoResponse.videoBlob;

        console.log('[EnvGen] Saving recording');
        console.log(`  Recording ID: ${recordingId}`);
        console.log(`  Session ID: ${sessionId || 'none (freehand)'}`);
        console.log(`  Video size: ${videoBlob.size} bytes`);
        console.log(`  UI events: ${allEvents.length}`);
        console.log(`  Network events: ${networkEvents.length}`);

        // Log event type breakdown for debugging
        const eventTypes = {};
        allEvents.forEach(e => {
            eventTypes[e.type] = (eventTypes[e.type] || 0) + 1;
        });
        console.log('  Event type breakdown:', eventTypes);

        // If part of a session, store recording locally (upload happens when ending session)
        if (sessionId) {
            const { activeSession } = await chrome.storage.local.get(['activeSession']);
            if (activeSession && activeSession.sessionId === sessionId) {
                // Prevent replacing existing recording
                if (activeSession.recording) {
                    throw new Error('A recording already exists for this session. Only one recording is allowed per session.');
                }

                // Clean events before storing (network events may contain non-serializable data)
                const cleanedEvents = cleanForJSON(allEvents);
                const cleanedNetworkEvents = cleanForJSON(networkEvents);

                // Store recording locally (no upload yet - upload happens when ending session)
                activeSession.recording = {
                    recordingId: recordingId,
                    startedAt: recordingStartTime,
                    stoppedAt: recordingEnd,
                    duration: recordingEnd - recordingStartTime,
                    sessionId: null, // Will be set when uploaded
                    videoPath: null, // Will be set when uploaded
                    eventsPath: null, // Will be set when uploaded
                    eventCount: allEvents.length,
                    networkEventCount: networkEvents.length,
                    // Store cleaned data for upload later
                    _uploadData: {
                        events: cleanedEvents,
                        networkEvents: cleanedNetworkEvents,
                        videoBlob: videoBlob
                    }
                };
                await chrome.storage.local.set({ activeSession });

                console.log('[EnvGen] Recording stored locally (will upload when session ends):', sessionId);

                // Save video blob to IndexedDB
                await chrome.runtime.sendMessage({
                    type: 'SAVE_VIDEO',
                    target: 'offscreen',
                    sessionId: recordingId,
                    videoBlob: videoBlob
                });

                // Reset current recording
                currentRecording = { id: null, sessionId: null, startedAt: null };

                return {
                    success: true,
                    eventCount: allEvents.length,
                    recordingId,
                    sessionId
                };
            }
        }

        // Freehand recording - upload first (mandatory - throws on failure)
        const uploadResult = await autoUploadToS3({
            sessionId: recordingId, // Use recordingId for tracking
            recordingStart: recordingStartTime,
            recordingEnd,
            events: allEvents,
            networkEvents: networkEvents,
            eventCount: allEvents.length,
            networkEventCount: networkEvents.length,
            videoSize: videoBlob.size,
            videoBlob: videoBlob
        });

        // Save session data (uploadResult is guaranteed - throws on failure)
        // Don't upload again - just save metadata with upload result
        await saveSession({
            sessionId: recordingId, // Use recordingId as sessionId for freehand
            recordingStart: recordingStartTime,
            recordingEnd,
            events: allEvents,
            networkEvents: networkEvents,
            eventCount: allEvents.length,
            networkEventCount: networkEvents.length,
            videoSize: videoBlob.size,
            videoBlob: videoBlob, // Still need blob for IndexedDB storage
            uploadResult: uploadResult // Pass upload result to avoid re-uploading
        });

        // Reset current recording
        currentRecording = { id: null, sessionId: null, startedAt: null };

        console.log('[EnvGen] Freehand recording saved:', recordingId);
        return {
            success: true,
            eventCount: allEvents.length,
            recordingId,
            uploadResult: {
                sessionId: uploadResult.sessionId,
                videoPath: uploadResult.videoPath,
                eventsPath: uploadResult.eventsPath
            }
        };
    } catch (error) {
        console.error('[EnvGen] Error stopping recording:', error);
        isRecording = false;
        // Upload errors are critical - propagate them
        const errorMessage = error.message || 'Unknown error';
        console.error('[EnvGen] Upload failed - exception thrown:', errorMessage);
        return { success: false, error: `Upload failed: ${errorMessage}` };
    }
}

// Clean data for JSON serialization (remove circular references, etc.)
function cleanForJSON(obj) {
    try {
        return JSON.parse(JSON.stringify(obj));
    } catch (e) {
        console.warn('[EnvGen] Failed to serialize object, attempting deep clean:', e);
        // If JSON.stringify fails, manually clean the object
        return deepClean(obj);
    }
}

function deepClean(obj) {
    if (obj === null || obj === undefined) {
        return obj;
    }

    if (typeof obj !== 'object') {
        return obj;
    }

    if (Array.isArray(obj)) {
        return obj.map(item => deepClean(item));
    }

    const cleaned = {};
    for (const key in obj) {
        try {
            const value = obj[key];

            // Skip functions and symbols
            if (typeof value === 'function' || typeof value === 'symbol') {
                continue;
            }

            // Handle special objects
            if (value instanceof Blob || value instanceof File) {
                cleaned[key] = '[Blob/File]';
            } else if (value instanceof FormData) {
                cleaned[key] = '[FormData]';
            } else if (value instanceof ArrayBuffer) {
                cleaned[key] = '[ArrayBuffer]';
            } else if (value instanceof Uint8Array || value instanceof ArrayBufferView) {
                cleaned[key] = '[TypedArray]';
            } else {
                cleaned[key] = deepClean(value);
            }
        } catch (e) {
            // Skip properties that can't be accessed
            console.warn(`[EnvGen] Could not clean property ${key}:`, e);
        }
    }
    return cleaned;
}

// Save session to storage
async function saveSession(session) {
    try {
        // Check storage usage
        const storageEstimate = await navigator.storage.estimate();
        const usedMB = (storageEstimate.usage / 1024 / 1024).toFixed(2);
        const quotaMB = (storageEstimate.quota / 1024 / 1024).toFixed(2);
        console.log(`[EnvGen] Storage usage: ${usedMB}MB / ${quotaMB}MB`);

        // Save metadata to Chrome storage
        const result = await chrome.storage.local.get('sessions');
        const sessions = result.sessions || [];

        // Auto-cleanup: keep only last 20 sessions to prevent quota issues
        if (sessions.length >= 20) {
            console.log('[EnvGen] Auto-cleanup: removing oldest sessions');
            const oldSessions = sessions.splice(0, sessions.length - 19); // Keep newest 19

            // Remove old videos from IndexedDB
            for (const oldSession of oldSessions) {
                try {
                    await chrome.runtime.sendMessage({
                        type: 'DELETE_VIDEO',
                        target: 'offscreen',
                        sessionId: oldSession.sessionId
                    });
                } catch (e) {
                    console.warn('[EnvGen] Could not delete old video:', e);
                }
            }
        }

        // Upload to /api/session/from-env-recording if not already uploaded
        // (for freehand recordings, upload happens before saveSession is called)
        let uploadResult;
        if (session.uploadResult) {
            // Already uploaded (freehand recording)
            uploadResult = session.uploadResult;
            console.log('[EnvGen] Using existing upload result:', uploadResult.sessionId);
        } else {
            // Not uploaded yet (session recording) - upload now
            uploadResult = await autoUploadToS3(session);
        }

        // Clean the data to ensure it's JSON-serializable
        const sessionData = {
            sessionId: session.sessionId,
            recordingStart: session.recordingStart,
            recordingEnd: session.recordingEnd,
            events: cleanForJSON(session.events),
            networkEvents: cleanForJSON(session.networkEvents),
            eventCount: session.eventCount,
            networkEventCount: session.networkEventCount,
            videoSize: session.videoSize
        };

        // Add upload result (guaranteed to exist - throws on failure)
        sessionData.s3Paths = {
            videoPath: uploadResult.videoPath,
            eventsPath: uploadResult.eventsPath
        };
        sessionData.uploadedSessionId = uploadResult.sessionId;

        sessions.push(sessionData);
        await chrome.storage.local.set({ sessions });

        // Store last upload info separately (for CLI to access)
        await chrome.storage.local.set({
            lastUpload: {
                sessionId: uploadResult.sessionId,
                timestamp: Date.now(),
                s3_path: uploadResult.videoPath,
                events_path: uploadResult.eventsPath
            }
        });

        // Save video blob to IndexedDB via offscreen document
        await chrome.runtime.sendMessage({
            type: 'SAVE_VIDEO',
            target: 'offscreen',
            sessionId: session.sessionId,
            videoBlob: session.videoBlob
        });

        console.log('[EnvGen] Session saved successfully');
        return uploadResult; // Return upload result (guaranteed - throws on failure)
    } catch (error) {
        console.error('[EnvGen] Error saving session:', error);
        // Upload errors are critical - always throw
        if (error.message && error.message.includes('quota')) {
            throw new Error('Storage quota exceeded! Please delete old sessions from the Sessions page.');
        }
        // Re-throw upload errors with clear message
        if (error.message && (error.message.includes('upload') || error.message.includes('API key'))) {
            throw new Error(`Upload failed: ${error.message}`);
        }
        throw error;
    }
}

// Upload session recording when ending session
// Throws exceptions on failure - upload is mandatory
async function uploadSessionRecording(sessionId) {
    try {
        const { activeSession } = await chrome.storage.local.get(['activeSession']);

        if (!activeSession || activeSession.sessionId !== sessionId) {
            throw new Error('Session not found');
        }

        if (!activeSession.recording) {
            throw new Error('No recording found for this session');
        }

        const recording = activeSession.recording;

        // Check if already uploaded
        if (recording.sessionId && recording.videoPath) {
            console.log('[EnvGen] Recording already uploaded, skipping');
            return {
                success: true,
                uploadResult: {
                    sessionId: recording.sessionId,
                    videoPath: recording.videoPath,
                    eventsPath: recording.eventsPath
                }
            };
        }

        // Get upload data
        if (!recording._uploadData) {
            throw new Error('Recording data not found - cannot upload');
        }

        const { events, networkEvents, videoBlob } = recording._uploadData;

        // Upload to /api/session/from-env-recording (mandatory - throws on failure)
        const uploadResult = await autoUploadToS3({
            sessionId: recording.recordingId,
            recordingStart: recording.startedAt,
            recordingEnd: recording.stoppedAt,
            events: events,
            networkEvents: networkEvents,
            eventCount: recording.eventCount,
            networkEventCount: recording.networkEventCount,
            videoSize: videoBlob.size,
            videoBlob: videoBlob
        });

        // Update recording with upload result
        activeSession.recording.sessionId = uploadResult.sessionId;
        activeSession.recording.videoPath = uploadResult.videoPath;
        activeSession.recording.eventsPath = uploadResult.eventsPath;
        // Remove upload data (no longer needed)
        delete activeSession.recording._uploadData;

        await chrome.storage.local.set({ activeSession });

        console.log('[EnvGen] Recording uploaded successfully:', uploadResult.sessionId);

        return {
            success: true,
            uploadResult: {
                sessionId: uploadResult.sessionId,
                videoPath: uploadResult.videoPath,
                eventsPath: uploadResult.eventsPath
            }
        };
    } catch (error) {
        console.error('[EnvGen] Failed to upload session recording:', error);
        throw error;
    }
}

// Upload to /api/session/from-env-recording endpoint
// Throws exceptions on failure - upload is mandatory
async function autoUploadToS3(session) {
    // Get API key - required for upload
    const settings = await chrome.storage.local.get(['platoApiKey']);

    if (!settings.platoApiKey) {
        const error = new Error('Plato API key not configured. Please configure it in extension settings (click ⚙️ Settings).');
        console.error('[EnvGen] Upload failed - API key missing:', error);
        throw error;
    }

    const platoApiUrl = 'https://plato.so';

    console.log('[EnvGen] Uploading session via /api/session/from-env-recording (mandatory)');

    // Clean events and network events before serialization (remove non-serializable data)
    const cleanedEvents = cleanForJSON(session.events || []);
    const cleanedNetworkEvents = cleanForJSON(session.networkEvents || []);

    // Prepare events JSON
    const eventsJson = {
        recording_start: session.recordingStart,
        recording_end: session.recordingEnd,
        ui_events: cleanedEvents,
        network_events: cleanedNetworkEvents,
        stats: {
            ui_event_count: session.eventCount,
            network_event_count: session.networkEventCount || 0,
            duration_ms: session.recordingEnd - session.recordingStart
        }
    };

    // Get simulator_id from activeSession if available
    let simulatorId = null;
    const { activeSession } = await chrome.storage.local.get(['activeSession']);
    if (activeSession && activeSession.simulatorId) {
        simulatorId = activeSession.simulatorId;
        console.log('[EnvGen] Using simulator_id:', simulatorId);
    } else {
        console.log('[EnvGen] No simulator_id found, uploading without it');
    }

    // Upload via /api/session/from-env-recording endpoint
    // This will throw if upload fails
    const uploadResult = await uploadSessionToPlato(
        platoApiUrl,
        settings.platoApiKey,
        session.videoBlob,
        eventsJson,
        simulatorId
    );

    console.log('[EnvGen] Upload successful');
    console.log('[EnvGen] Session ID:', uploadResult.sessionId);
    console.log('[EnvGen] Video uploaded to:', uploadResult.videoPath);
    console.log('[EnvGen] Events uploaded to:', uploadResult.eventsPath);

    return {
        sessionId: uploadResult.sessionId,
        videoPath: uploadResult.videoPath,
        eventsPath: uploadResult.eventsPath
    };
}

// Helper to convert base64 to blob (for legacy manual uploads)
async function base64ToBlob(base64) {
    const response = await fetch(`data:video/webm;base64,${base64}`);
    return await response.blob();
}

// Upload session via /api/session/from-env-recording endpoint
async function uploadSessionToPlato(apiUrl, apiKey, videoBlob, eventsJson, simulatorId = null) {
    console.log('[EnvGen] ========== UPLOAD START ==========');
    console.log('[EnvGen] API URL:', apiUrl);
    console.log('[EnvGen] Has API Key:', !!apiKey);
    console.log('[EnvGen] Simulator ID:', simulatorId);

    try {
        // Create FormData for multipart upload
        const formData = new FormData();

        // Convert videoBlob to actual Blob if it's a data URL object from offscreen
        let actualBlob;
        console.log('[EnvGen] Video blob type:', typeof videoBlob);
        console.log('[EnvGen] Video blob instanceof Blob:', videoBlob instanceof Blob);
        console.log('[EnvGen] Video blob keys:', videoBlob ? Object.keys(videoBlob) : 'null');

        if (videoBlob instanceof Blob) {
            actualBlob = videoBlob;
            console.log('[EnvGen] Using videoBlob directly as Blob');
        } else if (videoBlob && videoBlob.data && typeof videoBlob.data === 'string') {
            // It's a {data, type, size} object from offscreen - convert data URL to Blob
            console.log('[EnvGen] Converting data URL to Blob...');
            console.log('[EnvGen] Data URL length:', videoBlob.data.length);
            console.log('[EnvGen] Data URL prefix:', videoBlob.data.substring(0, 50));
            console.log('[EnvGen] Reported size from offscreen:', videoBlob.size);

            const response = await fetch(videoBlob.data);
            actualBlob = await response.blob();
            console.log('[EnvGen] ✅ Converted to Blob successfully');
            console.log('[EnvGen] Actual Blob size:', actualBlob.size, 'bytes');
            console.log('[EnvGen] Actual Blob type:', actualBlob.type);
        } else {
            console.error('[EnvGen] ❌ Invalid video data format!');
            console.error('[EnvGen] videoBlob:', videoBlob);
            throw new Error('Invalid video data format - check console for details');
        }

        // Validate blob size
        if (actualBlob.size < 1000) {
            console.error('[EnvGen] ❌ Video blob is suspiciously small:', actualBlob.size, 'bytes');
            throw new Error(`Video file is too small (${actualBlob.size} bytes) - recording may have failed`);
        }

        // Add video file
        const videoFile = new File([actualBlob], 'recording.webm', { type: 'video/webm' });
        console.log('[EnvGen] Created File object, size:', videoFile.size, 'bytes');
        formData.append('video_file', videoFile);

        // Add events file (as JSON)
        const eventsBlob = new Blob([JSON.stringify(eventsJson, null, 2)], { type: 'application/json' });
        const eventsFile = new File([eventsBlob], 'events.json', { type: 'application/json' });
        formData.append('events_file', eventsFile);

        // Add simulator_id if provided
        if (simulatorId !== null) {
            formData.append('simulator_id', simulatorId.toString());
        }

        // Log events file size
        console.log('[EnvGen] Events JSON size:', eventsBlob.size, 'bytes');
        console.log('[EnvGen] Events file name:', eventsFile.name);

        // Upload to endpoint
        console.log('[EnvGen] ========== SENDING REQUEST ==========');
        console.log('[EnvGen] Endpoint:', `${apiUrl}/api/session/from-env-recording`);
        console.log('[EnvGen] Video file size:', videoFile.size);
        console.log('[EnvGen] Events file size:', eventsFile.size);

        const response = await fetch(`${apiUrl}/api/session/from-env-recording`, {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey
                // Don't set Content-Type - browser will set it with boundary for FormData
            },
            body: formData
        });

        if (!response.ok) {
            let errorText;
            try {
                errorText = await response.text();
            } catch (e) {
                errorText = `HTTP ${response.status} ${response.statusText}`;
            }
            const error = new Error(`Session upload failed (${response.status}): ${errorText}`);
            console.error('[EnvGen] Upload failed - API error:', error);
            throw error;
        }

        const result = await response.json();
        console.log('[EnvGen] ========== UPLOAD SUCCESS ==========');
        console.log('[EnvGen] ✅ Session created:', result.session_id);
        console.log('[EnvGen] ✅ Video path:', result.video_path);
        console.log('[EnvGen] ✅ Events path:', result.events_path);

        return {
            sessionId: result.session_id,
            videoPath: result.video_path,
            eventsPath: result.events_path
        };
    } catch (error) {
        console.error('[EnvGen] ========== UPLOAD FAILED ==========');
        console.error('[EnvGen] ❌ Error:', error.message);
        console.error('[EnvGen] ❌ Stack:', error.stack);
        throw error;
    }
}

// Note: All old AWS S3 direct upload code (Signature V4, etc.) has been removed
// Now using Plato API proxy endpoint for uploads
