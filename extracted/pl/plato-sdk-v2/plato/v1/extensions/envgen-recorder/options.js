// Options page controller

// Load saved settings
async function loadSettings() {
    const settings = await chrome.storage.local.get(['platoApiKey']);

    // Populate form
    document.getElementById('platoApiKey').value = settings.platoApiKey || '';

    // Update credential status
    updateCredentialStatus(settings.platoApiKey);
}

// Update credential status display
function updateCredentialStatus(apiKey) {
    const statusDiv = document.getElementById('credentialStatus');

    if (apiKey) {
        statusDiv.className = 'credential-status configured';
        statusDiv.textContent = '✓ Plato API Configured - Recordings will automatically upload to plato.so';
    } else {
        statusDiv.className = 'credential-status not-configured';
        statusDiv.textContent = '⚠ Plato API Key Required - Recordings will fail to upload without an API key';
    }
}

// Save settings
async function saveSettings() {
    const platoApiKey = document.getElementById('platoApiKey').value.trim();

    // Save to storage
    await chrome.storage.local.set({
        platoApiKey: platoApiKey
    });

    // Update status display
    updateCredentialStatus(platoApiKey);

    // Show success message
    if (platoApiKey) {
        showStatus('success', 'Settings saved! Recordings will automatically upload to plato.so');
    } else {
        showStatus('error', 'API key is required. Recordings will fail to upload without it.');
    }

    console.log('[EnvGen Options] Settings saved:', {
        hasApiKey: !!platoApiKey
    });
}

// Clear credentials
async function clearCredentials() {
    if (!confirm('Are you sure you want to clear your Plato API key?')) {
        return;
    }

    await chrome.storage.local.set({
        platoApiKey: ''
    });

    // Clear form
    document.getElementById('platoApiKey').value = '';

    // Update status
    updateCredentialStatus('');

    showStatus('info', 'Plato API key cleared');

    console.log('[EnvGen Options] API key cleared');
}

// Show status message
function showStatus(type, message) {
    const statusDiv = document.getElementById('statusMessage');
    statusDiv.className = `status-message ${type}`;
    statusDiv.textContent = message;
    statusDiv.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();

    // Attach event listeners
    document.getElementById('saveButton').addEventListener('click', saveSettings);
    document.getElementById('clearButton').addEventListener('click', clearCredentials);

    // Save on Enter key
    document.querySelectorAll('input[type="text"], input[type="password"]').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                saveSettings();
            }
        });
    });
});
