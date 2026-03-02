// Session Setup - Real implementation using Plato SDK
console.log('📋 Session Setup page loaded');

// Back button handler
document.querySelector('.back-btn').addEventListener('click', () => {
  window.location.href = 'popup.html';
});

// Collapse side panel - use window.close() to actually close it
// But first save the current page so we can restore it when reopening
const collapseBtn = document.getElementById('collapseBtn');
if (collapseBtn) {
  collapseBtn.addEventListener('click', async () => {
    // Save current page path before closing
    const currentPath = window.location.pathname.split('/').pop() || 'session-setup.html';
    await chrome.storage.local.set({ lastSidePanelPage: currentPath });
    window.close();
  });
}

document.getElementById('setup-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const simulatorName = document.getElementById('simulator-name').value.trim();
  const artifactId = document.getElementById('artifact-id').value.trim();

  if (!simulatorName) {
    document.getElementById('error').textContent = 'Simulator name is required';
    document.getElementById('error').classList.add('visible');
    return;
  }

  console.log('🚀 Starting session:', { simulatorName, artifactId });

  // Show loading
  document.getElementById('loading').classList.add('visible');
  document.getElementById('submit-btn').disabled = true;
  document.getElementById('error').classList.remove('visible');

  try {
    // Get API key from storage (always get fresh value)
    const result = await new Promise((resolve) => {
      chrome.storage.local.get(['platoApiKey'], resolve);
    });
    
    if (!result.platoApiKey) {
      throw new Error('API key not configured. Please go to Settings.');
    }

    const apiClient = new window.PlatoApiClient(result.platoApiKey);

    // Get simulator info (for authentication, artifact_id, etc.)
    const simulatorInfo = await apiClient.getSimulator(simulatorName);

    const setartifactId = artifactId || simulatorInfo.config?.data_artifact_id || null;
    const envResult = await apiClient.createEnvironment(simulatorName, setartifactId);

    // Create session object
    const sessionId = crypto.randomUUID();
    const session = {
      sessionId,
      simulatorName,
      simulatorId: simulatorInfo.id, // Store simulator ID for upload
      artifactId: setartifactId,
      environmentId: envResult.environmentId,
      environmentUrl: envResult.environmentUrl,
      authentication: simulatorInfo.config?.authentication || null,
      status: 'active',
      startedAt: Date.now(),
      endedAt: null,
      recording: null, // Single recording, not array
      reviewResult: null
    };

    console.log('✅ Session created:', session);
    console.log('🌐 Environment URL:', session.environmentUrl);

    // Store session
    chrome.storage.local.set({
      activeSession: session,
      mode: 'session-active'
    }, async () => {
      // Navigate current tab to environment
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      await chrome.tabs.update(tab.id, { url: session.environmentUrl });

      // Wait for tab to load, then navigate sidebar
      setTimeout(() => {
        window.location.href = 'session-active.html';
      }, 1000);
    });

  } catch (error) {
    console.error('❌ Error creating session:', error);
    document.getElementById('error').textContent = `Failed: ${error.message}`;
    document.getElementById('error').classList.add('visible');
    document.getElementById('loading').classList.remove('visible');
    document.getElementById('submit-btn').disabled = false;
  }
});
