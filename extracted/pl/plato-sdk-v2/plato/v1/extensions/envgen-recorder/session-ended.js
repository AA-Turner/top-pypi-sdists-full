// Session Ended
console.log('✅ Session Ended page loaded');

let activeSession = null;

chrome.storage.local.get(['activeSession'], (result) => {
  activeSession = result.activeSession;

  if (!activeSession || activeSession.status !== 'ended') {
    console.error('❌ No ended session found');
    window.location.href = 'popup.html';
    return;
  }

  console.log('✅ Loaded ended session:', activeSession);

  // Get single recording
  const recording = activeSession.recording;
  const sessionDuration = activeSession.endedAt ? activeSession.endedAt - activeSession.startedAt : (recording?.duration || 0);

  // Update UI
  document.getElementById('simulator-name').textContent = activeSession.simulatorName;
  document.getElementById('artifact-id').textContent = activeSession.artifactId || 'default';
  document.getElementById('session-duration').textContent = formatSessionDuration(sessionDuration);
  document.getElementById('recording-count').textContent = recording ? '1' : '0';
  document.getElementById('total-duration').textContent = recording ? formatDuration(recording.duration || 0) : '0m 0s';
  document.getElementById('total-events').textContent = recording ? (recording.eventCount || 0).toLocaleString() : '0';
  document.getElementById('total-network').textContent = recording ? (recording.networkEventCount || 0).toLocaleString() : '0';

  // Add event listeners
  document.getElementById('start-again-card').addEventListener('click', startAgain);
  document.getElementById('review-card').addEventListener('click', submitReview);
  document.getElementById('back-home-btn').addEventListener('click', () => {
    window.location.href = 'popup.html';
  });
});

function startAgain() {
  window.location.href = 'session-setup.html';
}

function submitReview() {
  window.location.href = 'review-panel.html';
}

function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  return `${minutes}m ${seconds % 60}s`;
}

function formatSessionDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  
  if (hours > 0) {
    return `${hours}h ${minutes % 60}m`;
  }
  return `${minutes}m`;
}
