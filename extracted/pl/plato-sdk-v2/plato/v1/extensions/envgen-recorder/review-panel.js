// Review Panel
console.log('✅ Review Panel page loaded');

let activeSession = null;
let selectedOutcome = null;

chrome.storage.local.get(['activeSession'], (result) => {
  activeSession = result.activeSession;

  if (!activeSession) {
    console.error('❌ No session found');
    window.location.href = 'popup.html';
    return;
  }

  console.log('✅ Loaded session for review:', activeSession);

  // Update UI
  document.getElementById('simulator-name').textContent = activeSession.simulatorName;
  document.getElementById('artifact-id').textContent = activeSession.artifactId || 'default';

  renderRecordings();

  // Add event listeners
  document.getElementById('btn-pass').addEventListener('click', () => selectOutcome('pass'));
  document.getElementById('btn-reject').addEventListener('click', () => selectOutcome('reject'));
  document.getElementById('btn-skip').addEventListener('click', () => selectOutcome('skip'));
  document.getElementById('submit-btn').addEventListener('click', submitReview);
  document.querySelector('.back-btn').addEventListener('click', goBack);
  
  // Collapse side panel - use window.close() to actually close it
  // But first save the current page so we can restore it when reopening
  const collapseBtn = document.getElementById('collapseBtn');
  if (collapseBtn) {
    collapseBtn.addEventListener('click', async () => {
      // Save current page path before closing
      const currentPath = window.location.pathname.split('/').pop() || 'review-panel.html';
      await chrome.storage.local.set({ lastSidePanelPage: currentPath });
      window.close();
    });
  }
  
  // Disable submit initially
  document.getElementById('submit-btn').disabled = true;
});

function renderRecordings() {
  const recording = activeSession.recording;
  const container = document.getElementById('recordings-list');

  document.getElementById('recording-count').textContent = recording ? '1' : '0';

  if (!recording) {
    container.innerHTML = '<div class="error-box">No recording found. Please go back and create a recording.</div>';
    return;
  }

  const isUploaded = recording.videoPath && recording.eventsPath;
  container.innerHTML = `
    <div class="recording-item">
      <div class="recording-header">
        <strong>Recording</strong>
        <span>${formatDuration(recording.duration || 0)}</span>
      </div>
      ${isUploaded ? `
        <div style="font-size: 10px; color: #6b7280; margin: 4px 0;">
          Video: ${recording.videoPath}<br>
          Events: ${recording.eventsPath}
        </div>
        <div class="recording-actions">
          <button class="btn-small" onclick="copyPath('${recording.videoPath}')">📋 Copy Video</button>
          <button class="btn-small" onclick="copyPath('${recording.eventsPath}')">📋 Copy Events</button>
        </div>
        <div style="font-size: 10px; color: #6b7280; margin-top: 8px;">
          Session ID: ${recording.sessionId || 'N/A'}<br>
          Events: ${recording.eventCount || 0} | Network: ${recording.networkEventCount || 0}
        </div>
      ` : '<div style="color: #f59e0b;">⏳ Uploading...</div>'}
    </div>
  `;
}

function selectOutcome(outcome) {
  console.log('🎯 Selected outcome:', outcome);
  selectedOutcome = outcome;

  // Update button states
  document.querySelectorAll('.outcome-btn').forEach(btn => {
    btn.classList.remove('selected');
  });
  document.getElementById(`btn-${outcome}`).classList.add('selected');

  // Show/hide comments section
  const commentsSection = document.getElementById('comments-section');
  if (outcome === 'reject') {
    commentsSection.style.display = 'block';
  } else {
    commentsSection.style.display = 'none';
  }

  // Enable submit
  document.getElementById('submit-btn').disabled = false;
}

async function submitReview() {
  if (!selectedOutcome) {
    alert('Please select an outcome');
    return;
  }

  // Validate reject requires comments
  if (selectedOutcome === 'reject') {
    const comments = document.getElementById('comments').value.trim();
    if (!comments) {
      alert('Comments are required when rejecting');
      return;
    }
  }

  console.log('📤 Submitting review');

  const comments = document.getElementById('comments').value.trim();
  const loadingDiv = document.getElementById('loading');
  const submitBtn = document.getElementById('submit-btn');

  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';
  loadingDiv.classList.add('visible');

  try {
    // Get API key (always get fresh value, not cached)
    const result = await new Promise((resolve) => {
      chrome.storage.local.get(['platoApiKey'], resolve);
    });
    const platoApiKey = result.platoApiKey;
    
    if (!platoApiKey) {
      throw new Error('API key not configured. Please configure it in Settings.');
    }

    const apiClient = new window.PlatoApiClient(platoApiKey);

    // Build review with single recording
    if (!activeSession.recording || !activeSession.recording.videoPath) {
      throw new Error('Recording not uploaded yet. Please wait for upload to complete.');
    }

    const review = {
      outcome: selectedOutcome,
      artifactId: activeSession.artifactId,
      recordings: [{
        video_s3_path: activeSession.recording.videoPath,
        events_s3_path: activeSession.recording.eventsPath,
        duration: activeSession.recording.duration
      }],
      comments: comments || null
    };

    // Submit
    const submitResult = await apiClient.submitReview(activeSession.simulatorName, review);

    // Tag if pass
    if (selectedOutcome === 'pass') {
      await apiClient.tagArtifact(activeSession.simulatorName, activeSession.artifactId);
    }

    // Save result
    activeSession.reviewResult = {
      outcome: selectedOutcome,
      submittedAt: Date.now(),
      comments: comments || null,
      newStatus: submitResult.newStatus,
      tagged: selectedOutcome === 'pass' ? 'prod-latest' : null
    };
    activeSession.status = 'reviewed';

    await chrome.storage.local.set({ activeSession });
    console.log('✅ Review submitted:', activeSession.reviewResult);
    window.location.href = 'review-success.html';

  } catch (error) {
    console.error('❌ Error submitting review:', error);
    document.getElementById('error').textContent = `Failed: ${error.message}`;
    document.getElementById('error').classList.add('visible');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit Review';
    loadingDiv.classList.remove('visible');
  }
}

function goBack() {
  window.location.href = 'session-ended.html';
}

function copyPath(path) {
  navigator.clipboard.writeText(path).then(() => {
    console.log('📋 Copied:', path);
    // Show toast notification
    const toast = document.createElement('div');
    toast.textContent = 'S3 path copied!';
    toast.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #10b981; color: white; padding: 8px 16px; border-radius: 4px; z-index: 10000;';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
  }).catch(err => {
    console.error('Failed to copy:', err);
  });
}

// Make copyPath available globally
window.copyPath = copyPath;

function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  return `${minutes}m ${seconds % 60}s`;
}
