// Offscreen document for handling MediaRecorder

let mediaRecorder = null;
let recordedChunks = [];

console.log('[EnvGen Offscreen] Document loaded');

// IndexedDB for storing videos
const DB_NAME = 'envgen_sessions';
const DB_VERSION = 1;
const STORE_NAME = 'videos';

let db = null;

// Initialize IndexedDB
function initDB() {
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

// Save video to IndexedDB
async function saveVideoToDB(sessionId, videoBlob) {
    if (!db) await initDB();

    // Convert data URL back to blob
    const byteString = atob(videoBlob.data.split(',')[1]);
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([ab], { type: videoBlob.type });

    return new Promise((resolve, reject) => {
        const transaction = db.transaction([STORE_NAME], 'readwrite');
        const store = transaction.objectStore(STORE_NAME);
        const request = store.put({ sessionId, videoBlob: blob });

        request.onsuccess = () => {
            console.log('[EnvGen Offscreen] Video saved to IndexedDB:', sessionId);
            resolve();
        };
        request.onerror = () => reject(request.error);
    });
}

// Initialize DB on load
initDB().catch(err => console.error('[EnvGen Offscreen] Failed to init DB:', err));

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('[EnvGen Offscreen] Received message:', message.type);

    // Only respond to messages targeted at offscreen
    if (message.target !== 'offscreen') {
        return;
    }

    if (message.type === 'START_RECORDING') {
        console.log('[EnvGen Offscreen] Starting recording with streamId:', message.streamId);
        startRecording(message.streamId)
            .then(() => {
                console.log('[EnvGen Offscreen] Recording started successfully');
                sendResponse({ success: true });
            })
            .catch(err => {
                console.error('[EnvGen Offscreen] Recording start failed:', err);
                sendResponse({ success: false, error: err.message });
            });
        return true;
    } else if (message.type === 'STOP_RECORDING') {
        console.log('[EnvGen Offscreen] Stopping recording');
        stopRecording()
            .then(videoBlob => {
                console.log('[EnvGen Offscreen] Recording stopped, blob size:', videoBlob.size);
                sendResponse({ success: true, videoBlob });
            })
            .catch(err => {
                console.error('[EnvGen Offscreen] Recording stop failed:', err);
                sendResponse({ success: false, error: err.message });
            });
        return true;
    } else if (message.type === 'SAVE_VIDEO') {
        console.log('[EnvGen Offscreen] Saving video to IndexedDB:', message.sessionId);
        saveVideoToDB(message.sessionId, message.videoBlob)
            .then(() => {
                sendResponse({ success: true });
            })
            .catch(err => {
                console.error('[EnvGen Offscreen] Failed to save video:', err);
                sendResponse({ success: false, error: err.message });
            });
        return true;
    } else if (message.type === 'DELETE_VIDEO') {
        console.log('[EnvGen Offscreen] Deleting video from IndexedDB:', message.sessionId);
        deleteVideoFromDB(message.sessionId)
            .then(() => {
                sendResponse({ success: true });
            })
            .catch(err => {
                console.error('[EnvGen Offscreen] Failed to delete video:', err);
                sendResponse({ success: false, error: err.message });
            });
        return true;
    }
});

async function startRecording(streamId) {
    try {
        console.log('[EnvGen Offscreen] Getting media stream with streamId:', streamId);

        // Get the media stream from the streamId
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: {
                mandatory: {
                    chromeMediaSource: 'tab',
                    chromeMediaSourceId: streamId
                }
            }
        });

        console.log('[EnvGen Offscreen] Got media stream:', stream.id);

        // Reset chunks for new recording
        recordedChunks = [];
        console.log('[EnvGen Offscreen] Starting new recording');

        // Create MediaRecorder
        let options = { mimeType: 'video/webm;codecs=vp9' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            console.log('[EnvGen Offscreen] VP9 not supported, using VP8');
            options.mimeType = 'video/webm;codecs=vp8';
        }
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            console.log('[EnvGen Offscreen] VP8 not supported, using default');
            options = {};
        }

        console.log('[EnvGen Offscreen] Creating MediaRecorder with options:', options);
        mediaRecorder = new MediaRecorder(stream, options);

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                console.log('[EnvGen Offscreen] Data available:', event.data.size, 'bytes');
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onerror = (event) => {
            console.error('[EnvGen Offscreen] MediaRecorder error:', event.error);
        };

        mediaRecorder.start(1000); // Collect data every second
        console.log('[EnvGen Offscreen] MediaRecorder started, state:', mediaRecorder.state);
    } catch (error) {
        console.error('[EnvGen Offscreen] Error starting recording:', error);
        throw error;
    }
}

async function stopRecording() {
    return new Promise((resolve, reject) => {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            reject(new Error('No active recording'));
            return;
        }

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });

            // Stop all tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());

            // Convert blob to base64 for message passing
            const reader = new FileReader();
            reader.onloadend = () => {
                resolve({
                    data: reader.result,
                    type: blob.type,
                    size: blob.size
                });
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);

            console.log('[EnvGen Offscreen] Recording stopped');
        };

        mediaRecorder.stop();
    });
}
