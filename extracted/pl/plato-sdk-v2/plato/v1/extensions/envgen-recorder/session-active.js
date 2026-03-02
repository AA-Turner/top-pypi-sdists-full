// Session Active - Real implementation
console.log('📹 Session Active page loaded');

let activeSession = null;
let isRecording = false;
let recordingStartTime = null;
let recordingInterval = null;

// Load session on page load
chrome.storage.local.get(['activeSession'], (result) => {
  activeSession = result.activeSession;

  if (!activeSession || activeSession.status !== 'active') {
    console.error('❌ No active session found');
    alert('No active session found');
    window.location.href = 'popup.html';
    return;
  }

  console.log('✅ Loaded session:', activeSession);

  // Update UI
  document.getElementById('session-title').textContent = `📋 Session: ${activeSession.simulatorName}`;
  document.getElementById('artifact-id').textContent = activeSession.artifactId || 'default';
  document.getElementById('environment-id').textContent = activeSession.environmentId;

  // Show login info if available
  const loginBox = document.getElementById('login-box');
  if (activeSession.authentication && loginBox) {
    loginBox.style.display = 'block';
    document.getElementById('auth-user').textContent = activeSession.authentication.user;
    document.getElementById('auth-pass').textContent = activeSession.authentication.password;
  }

  renderRecording();

  // Check background recording state and sync local state
  chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
    if (response && response.isRecording) {
      console.log('[EnvGen Session Active] Recording is active in background, syncing state');
      isRecording = true;

      // Sync recording start time if available
      if (response.recordingStartTime) {
        recordingStartTime = response.recordingStartTime;
        console.log('[EnvGen Session Active] Synced recording start time:', recordingStartTime);

        // Start timer if not already running
        if (!recordingInterval) {
          recordingInterval = setInterval(() => {
            const elapsed = Date.now() - recordingStartTime;
            const durationEl = document.getElementById('duration');
            if (durationEl) {
              durationEl.textContent = formatDuration(elapsed);
            }
          }, 1000);
        }

        // Show recording UI
        document.getElementById('not-recording-ui').style.display = 'none';
        document.getElementById('recording-ui').style.display = 'block';

        // Update pause button state
        updatePauseButtonState(response.isPaused);
      }

      // Update the UI to show recording state
      renderRecording();
      updateStartButtonState();

      // Start polling for recording stats if recording is active
      if (isRecording) {
        updateEventStats();
      }
    }
  });

  // Set up event listeners
  document.getElementById('start-rec').addEventListener('click', startRecording);
  document.getElementById('pause-btn').addEventListener('click', togglePause);
  document.getElementById('stop-rec').addEventListener('click', stopRecording);
  document.getElementById('end-session').addEventListener('click', endSession);

  // Collapse side panel - use window.close() to actually close it
  // But first save the current page so we can restore it when reopening
  const collapseBtn = document.getElementById('collapseBtn');
  if (collapseBtn) {
    collapseBtn.addEventListener('click', async () => {
      // Save current page path before closing
      const currentPath = window.location.pathname.split('/').pop() || 'session-active.html';
      await chrome.storage.local.set({ lastSidePanelPage: currentPath });
      window.close();
    });
  }

  // Poll for recording updates and sync with background state
  setInterval(() => {
    // Check background recording state
    chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
      if (response) {
        // Sync local recording state with background
        const wasRecording = isRecording;
        isRecording = response.isRecording;

        // Update pause button state
        if (isRecording) {
          updatePauseButtonState(response.isPaused);
        }

        // If recording state changed, update UI
        if (isRecording !== wasRecording) {
          console.log('[EnvGen Session Active] Recording state changed:', isRecording);
          renderRecording();
          updateStartButtonState();

          if (isRecording && !wasRecording) {
            // Recording just started, start polling stats
            updateEventStats();
          }
        }
      }
    });

    // Also check for session updates
    chrome.storage.local.get(['activeSession'], (result) => {
      if (result.activeSession && result.activeSession.sessionId === activeSession.sessionId) {
        activeSession = result.activeSession;
        renderRecording();
        updateStartButtonState();
      }
    });
  }, 2000);

  // Check if recording already exists and disable start button
  updateStartButtonState();
});

async function startRecording() {
  // Prevent starting if recording already exists - only one recording per session
  if (activeSession.recording) {
    alert('A recording already exists for this session. Only one recording is allowed per session.');
    return;
  }

  console.log('🔴 Starting recording');
  isRecording = true;
  recordingStartTime = Date.now();

  // Disable start button
  document.getElementById('start-rec').disabled = true;

  // Update UI
  document.getElementById('not-recording-ui').style.display = 'none';
  document.getElementById('recording-ui').style.display = 'block';

  // Initialize pause button state (inactive - green)
  updatePauseButtonState(false);

  // Start timer
  recordingInterval = setInterval(() => {
    const elapsed = Date.now() - recordingStartTime;
    document.getElementById('duration').textContent = formatDuration(elapsed);
  }, 1000);

  // Start event stats updater
  updateEventStats();

  // Get stream ID first (must be called from user-interaction context, not background)
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  try {
    // Get stream ID for tab capture (this grants permission)
    const streamId = await chrome.tabCapture.getMediaStreamId({
      targetTabId: tab.id
    });

    console.log('✅ Got streamId:', streamId);
    console.log('📋 Starting recording for session:', activeSession.sessionId);

    // Send to background with sessionId
    chrome.runtime.sendMessage({
      type: 'START_RECORDING',
      tabId: tab.id,
      sessionId: activeSession.sessionId
    }, (response) => {
      if (!response || !response.success) {
        alert('Failed to start recording: ' + (response?.error || 'Unknown error'));
        stopRecordingUI();
      } else {
        console.log('✅ Recording started for session');
      }
    });
  } catch (error) {
    console.error('❌ Failed to get stream:', error);
    alert('Failed to start recording: ' + error.message);
    stopRecordingUI();
  }
}

function updateEventStats() {
  if (!isRecording) return;

  chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
    if (response && response.isRecording) {
      const eventsEl = document.getElementById('events');
      const networkEl = document.getElementById('network');
      if (eventsEl) {
        eventsEl.textContent = response.eventCount || 0;
      }
      if (networkEl) {
        networkEl.textContent = response.networkEventCount || 0;
      }
      // Continue polling while recording
      setTimeout(updateEventStats, 500);
    } else if (isRecording) {
      // Still recording but response might be delayed, keep polling
      setTimeout(updateEventStats, 500);
    }
  });
}

function togglePause() {
  console.log('⏸️ Toggle pause marker');
  chrome.runtime.sendMessage({ type: 'TOGGLE_PAUSE' }, (response) => {
    if (response && response.success) {
      updatePauseButtonState(response.isPaused);
    }
  });
}

function updatePauseButtonState(isPaused) {
  const pauseBtn = document.getElementById('pause-btn');
  if (!pauseBtn) return;

  if (isPaused) {
    // Active state: Yellow with "Pause Marker Active"
    pauseBtn.textContent = '⏸️ Pause Marker Active (Ctrl+Shift+Space)';
    pauseBtn.style.backgroundColor = '#f59e0b'; // Yellow when active
    pauseBtn.style.borderColor = '#f59e0b';
    pauseBtn.classList.remove('btn-success');
    pauseBtn.classList.add('btn-warning');
  } else {
    // Inactive state: Green with "Pause Marker Inactive"
    pauseBtn.textContent = '⏸️ Pause Marker Inactive (Ctrl+Shift+Space)';
    pauseBtn.style.backgroundColor = '#10b981'; // Green when inactive
    pauseBtn.style.borderColor = '#10b981';
    pauseBtn.classList.remove('btn-warning');
    pauseBtn.classList.add('btn-success');
  }
}

function stopRecording() {
  console.log('⏹️ Stopping recording');

  if (!isRecording) return;

  chrome.runtime.sendMessage({ type: 'STOP_RECORDING' }, (response) => {
    if (response.success) {
      stopRecordingUI();

      // Reload recording from storage (background.js will have saved it locally, no upload yet)
      setTimeout(() => {
        chrome.storage.local.get(['activeSession'], (result) => {
          activeSession = result.activeSession;
          renderRecording();
          updateStartButtonState();
        });
      }, 500);
    } else {
      const errorMsg = response.error || 'Unknown error';
      alert(`❌ Failed to stop recording: ${errorMsg}`);
      console.error('[EnvGen Session Active] Stop recording failed:', errorMsg);
    }
  });
}

function stopRecordingUI() {
  clearInterval(recordingInterval);
  isRecording = false;
  document.getElementById('not-recording-ui').style.display = 'block';
  document.getElementById('recording-ui').style.display = 'none';
}

function renderRecording() {
  const recording = activeSession.recording;
  const container = document.getElementById('recording-info');
  const noRecordingMsg = document.getElementById('no-recording');

  if (!recording) {
    container.innerHTML = '';
    if (noRecordingMsg) noRecordingMsg.style.display = 'block';
    return;
  }

  if (noRecordingMsg) noRecordingMsg.style.display = 'none';

  const isUploaded = recording.videoPath && recording.eventsPath;
  container.innerHTML = `
    <div class="recording-item">
      <div class="recording-header">
        <strong>Recording</strong>
        <span>${formatDuration(recording.duration || 0)}</span>
      </div>
      <div style="font-size: 11px; color: #6b7280; margin: 8px 0;">
        ${isUploaded ? '✓ Uploaded' : '⏳ Not Uploaded (will upload when session ends)'} | ${recording.eventCount || 0} events | ${recording.networkEventCount || 0} network
      </div>
      ${isUploaded ? `
        <div class="recording-actions">
          <button class="btn-small" onclick="copyPath('${recording.videoPath}')">📋 Copy Video Path</button>
          <button class="btn-small" onclick="copyPath('${recording.eventsPath}')">📋 Copy Events Path</button>
        </div>
        <div style="font-size: 10px; color: #6b7280; margin-top: 8px;">
          Session ID: ${recording.sessionId || 'N/A'}
        </div>
      ` : `
        <div style="font-size: 10px; color: #6b7280; margin-top: 8px; font-style: italic;">
          Recording will be uploaded when you end the session
        </div>
      `}
    </div>
  `;
}

function updateStartButtonState() {
  const startBtn = document.getElementById('start-rec');
  if (activeSession.recording && !isRecording) {
    // Recording already exists - disable start button
    startBtn.disabled = true;
    startBtn.textContent = '✓ Recording Complete';
    startBtn.style.backgroundColor = '#10b981';
  } else if (!isRecording) {
    startBtn.disabled = false;
    startBtn.textContent = '🔴 Start Recording';
    startBtn.style.backgroundColor = '';
  }
}

// Make copyPath available globally
window.copyPath = copyPath;

function copyPath(path) {
  navigator.clipboard.writeText(path).then(() => {
    console.log('📋 Copied:', path);
  });
}

async function endSession() {
  // If currently recording, stop it first
  if (isRecording) {
    if (!confirm('Stop current recording and end session?')) {
      return;
    }

    // Stop recording first
    await new Promise((resolve) => {
      chrome.runtime.sendMessage({ type: 'STOP_RECORDING' }, (response) => {
        if (response.success) {
          stopRecordingUI();
          // Wait a bit for storage to update
          setTimeout(() => {
            chrome.storage.local.get(['activeSession'], (result) => {
              activeSession = result.activeSession;
              resolve();
            });
          }, 500);
        } else {
          alert('Failed to stop recording: ' + (response.error || 'Unknown error'));
          resolve();
        }
      });
    });
  }

  // Check if recording exists
  if (!activeSession.recording) {
    if (!confirm('No recording exists. End session without recording?')) {
      return;
    }
    proceedToEndSession();
    return;
  }

  // Upload happens here when ending session
  await proceedToEndSession();
}

async function proceedToEndSession() {
  console.log('🛑 Ending session - uploading recording...');

  // Show loading overlay
  const overlay = document.createElement('div');
  overlay.id = 'upload-overlay';
  overlay.innerHTML = `
    <div style="
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.85);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      color: white;
      font-family: system-ui, -apple-system, sans-serif;
    ">
      <div style="font-size: 48px; margin-bottom: 20px;">⏳</div>
      <div style="font-size: 18px; font-weight: 600; margin-bottom: 10px;">Uploading Recording...</div>
      <div id="upload-status" style="font-size: 13px; color: #9ca3af; text-align: center; max-width: 280px;">
        Preparing video and events data for upload...
      </div>
      <div style="margin-top: 20px; width: 200px; height: 4px; background: #374151; border-radius: 2px; overflow: hidden;">
        <div id="upload-progress" style="height: 100%; width: 20%; background: #3b82f6; transition: width 0.3s;"></div>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const updateStatus = (text, progress) => {
    const statusEl = document.getElementById('upload-status');
    const progressEl = document.getElementById('upload-progress');
    if (statusEl) statusEl.textContent = text;
    if (progressEl) progressEl.style.width = progress + '%';
  };

  // Also disable the button
  const endBtn = document.getElementById('end-session');
  const originalText = endBtn.textContent;
  endBtn.disabled = true;

  try {
    updateStatus('Sending recording to server...', 40);

    // Upload the recording (mandatory - throws on failure)
    const response = await chrome.runtime.sendMessage({
      type: 'UPLOAD_SESSION_RECORDING',
      sessionId: activeSession.sessionId
    });

    if (!response.success) {
      throw new Error(response.error || 'Upload failed');
    }

    updateStatus('Upload complete! Saving session...', 80);
    console.log('✅ Upload successful, ending session');

    // Update session with upload result
    activeSession.recording.sessionId = response.uploadResult.sessionId;
    activeSession.recording.videoPath = response.uploadResult.videoPath;
    activeSession.recording.eventsPath = response.uploadResult.eventsPath;
    activeSession.status = 'ended';
    activeSession.endedAt = Date.now();

    await chrome.storage.local.set({ activeSession, mode: 'session-ended' });

    updateStatus('✅ Success! Redirecting...', 100);
    console.log('✅ Session ended');

    // Brief pause to show success
    await new Promise(r => setTimeout(r, 500));
    window.location.href = 'session-ended.html';

  } catch (error) {
    console.error('[EnvGen Session Active] Upload failed:', error);

    // Remove overlay
    overlay.remove();

    endBtn.disabled = false;
    endBtn.textContent = originalText;
    alert(`❌ Failed to upload recording!\n\n${error.message}\n\nPlease check your API key in Settings and check the browser console (F12) for detailed logs.`);
  }
}

function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  const h = String(hours).padStart(2, '0');
  const m = String(minutes % 60).padStart(2, '0');
  const s = String(seconds % 60).padStart(2, '0');

  return `${h}:${m}:${s}`;
}
