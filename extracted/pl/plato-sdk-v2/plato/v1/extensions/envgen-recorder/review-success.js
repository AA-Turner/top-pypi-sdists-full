// Review Success
console.log('🎉 Review Success page loaded');

let activeSession = null;

chrome.storage.local.get(['activeSession'], (result) => {
  activeSession = result.activeSession;

  if (!activeSession || !activeSession.reviewResult) {
    console.error('❌ No review result found');
    window.location.href = 'popup.html';
    return;
  }

  console.log('✅ Loaded review result:', activeSession.reviewResult);

  // Update UI
  document.getElementById('simulator-name').textContent = activeSession.simulatorName;
  document.getElementById('artifact-id').textContent = activeSession.artifactId || 'default';
  
  const outcome = activeSession.reviewResult.outcome;
  document.getElementById('outcome').textContent = outcome === 'pass' ? '✅ Pass' : outcome === 'reject' ? '❌ Reject' : '⏭️ Skip';
  document.getElementById('status-change').textContent = activeSession.reviewResult.newStatus || 'N/A';
  document.getElementById('recording-count').textContent = activeSession.recording ? '1' : '0';
  document.getElementById('submitted-at').textContent = new Date(activeSession.reviewResult.submittedAt).toLocaleString();

  if (activeSession.reviewResult.tagged) {
    document.getElementById('tagged').textContent = activeSession.reviewResult.tagged;
    document.getElementById('tagged-row').style.display = 'list-item';
  }

  if (activeSession.reviewResult.comments) {
    document.getElementById('comments').textContent = activeSession.reviewResult.comments;
    document.getElementById('comments-box').style.display = 'block';
  }

  // Add event listeners
  const buttons = document.querySelectorAll('button');
  buttons.forEach(btn => {
    if (btn.textContent.includes('Start New Session')) {
      btn.addEventListener('click', startNewSession);
    } else if (btn.textContent.includes('Done')) {
      btn.addEventListener('click', done);
    }
  });
});

function startNewSession() {
  window.location.href = 'session-setup.html';
}

function done() {
  console.log('🏠 Cleared active session, returning home');
  chrome.storage.local.remove('activeSession', () => {
    chrome.storage.local.set({ mode: 'idle' });
    window.location.href = 'popup.html';
  });
}
