// UI event tracking script for EnvGen
(function () {
    // Prevent duplicate initialization
    if (window.envgenUITracking) {
        console.log('[EnvGen] Already initialized, skipping');
        return;
    }
    window.envgenUITracking = true;

    // Initialize events array
    window.envgenEvents = [];
    window.envgenSeqId = 0;
    window.envgenRecordingStart = Date.now();
    window.envgenLastActionTime = 0;
    window.envgenDOMSettleTimer = null;
    window.envgenLastDOMChange = 0;

    console.log('[EnvGen] Content script loaded at', new Date().toISOString());
    console.log('[EnvGen] Document ready state:', document.readyState);
    console.log('[EnvGen] UI tracking initialized at', window.envgenRecordingStart);

    // XPath helper
    window.getXPath = (el) => {
        if (!el || !el.nodeType) return "";
        const parts = [];
        let node = el;

        while (node && node.nodeType && node !== document) {
            if (node.nodeType === Node.ELEMENT_NODE) {
                let siblingIndex = 1;
                let sibling = node.previousSibling;
                while (sibling) {
                    if (sibling.nodeType === Node.ELEMENT_NODE &&
                        sibling.nodeName === node.nodeName) {
                        siblingIndex++;
                    }
                    sibling = sibling.previousSibling;
                }
                const tagName = node.localName || node.nodeName.toLowerCase();
                parts.push(`${tagName}[${siblingIndex}]`);
            }
            node = node.parentNode;
        }
        return parts.length ? `/${parts.reverse().join("/")}` : "";
    };

    // CSS selector helper
    const cssPath = (el) => {
        if (!el) return 'unknown';
        if (el.id) return '#' + el.id;
        if (el.className && el.classList) {
            const classes = Array.from(el.classList).filter(c => c && !c.includes(' '));
            if (classes.length) return el.tagName.toLowerCase() + '.' + classes.join('.');
        }
        return el.tagName.toLowerCase();
    };

    // Event handler
    const handleEvent = (e) => {
        const timestamp = Date.now();
        const target = e.target;

        // Check for pause marker keyboard shortcut (Ctrl+Shift+Space or Cmd+Shift+Space)
        if (e.type === 'keydown') {
            console.log('[EnvGen] Keydown:', e.code, 'Shift:', e.shiftKey, 'Ctrl:', e.ctrlKey, 'Meta:', e.metaKey);

            if (e.shiftKey && e.code === 'Space' && (e.ctrlKey || e.metaKey)) {
                console.log('[EnvGen] Pause marker shortcut detected!');
                e.preventDefault();
                e.stopPropagation();

                // Send toggle pause message to background
                chrome.runtime.sendMessage({ type: 'TOGGLE_PAUSE' }).then(response => {
                    console.log('[EnvGen] Toggle pause response:', response);
                }).catch(err => {
                    console.warn('[EnvGen] Toggle pause failed:', err);
                });

                return; // Don't record this as a regular keydown event
            }
        }

        // Log every event for debugging
        console.log('[EnvGen Event]', e.type, target?.tagName, target?.id || target?.className || 'no-id');

        // Get element bounding box with proper scaling
        let boundingBox = null;
        if (target && target.getBoundingClientRect) {
            const rect = target.getBoundingClientRect();
            const scale = window.devicePixelRatio || 1;
            boundingBox = {
                x: (rect.left + window.scrollX) * scale,  // Scale to video coordinates
                y: (rect.top + window.scrollY) * scale,
                width: rect.width * scale,
                height: rect.height * scale,
                viewportWidth: window.innerWidth * scale,
                viewportHeight: window.innerHeight * scale,
                devicePixelRatio: scale
            };
        }

        // Capture inner text content (prefer innerText over textContent for better readability)
        let elementText = '';
        if (target) {
            // innerText gives rendered text (respects CSS, line breaks, etc.)
            elementText = target.innerText || target.textContent || '';
            // Trim and limit to 500 characters
            elementText = elementText.trim().substring(0, 500);
        }

        const event = {
            seq_id: window.envgenSeqId++,
            timestamp: timestamp,
            type: e.type,
            isTrusted: e.isTrusted,  // Capture whether this is a user-triggered event
            target: {
                tagName: target?.tagName,
                id: target?.id || '',
                className: target?.className || '',
                xpath: window.getXPath(target),
                cssPath: cssPath(target),
                innerText: elementText,  // Captured inner text of interacted element
                value: target?.value || '',
                boundingBox: boundingBox
            }
        };

        // Add event-specific data
        if (e.type === 'click' || e.type === 'mousedown' || e.type === 'mouseup' || e.type === 'dblclick') {
            const scale = window.devicePixelRatio || 1;
            event.mouse = {
                x: e.clientX,
                y: e.clientY,
                pageX: e.pageX * scale,  // Scale to video coordinates
                pageY: e.pageY * scale,
                button: e.button
            };

            // Track click time for DOM mutation detection
            if (e.type === 'click') {
                window.envgenLastActionTime = timestamp;
            }
        }

        if (e.type === 'mousemove') {
            event.mouse = {
                x: e.clientX,
                y: e.clientY,
                pageX: e.pageX,
                pageY: e.pageY
            };
        }

        if (e.type === 'wheel' || e.type === 'scroll') {
            event.scroll = {
                deltaX: e.deltaX || 0,
                deltaY: e.deltaY || 0,
                scrollX: window.scrollX,
                scrollY: window.scrollY
            };
        }

        if (e.type === 'keydown' || e.type === 'keyup') {
            event.key = {
                key: e.key,
                code: e.code,
                keyCode: e.keyCode,
                altKey: e.altKey,
                ctrlKey: e.ctrlKey,
                metaKey: e.metaKey,
                shiftKey: e.shiftKey
            };
        }

        if (e.type === 'input' || e.type === 'change') {
            event.input = {
                value: target?.value || '',
                inputType: e.inputType || ''
            };
        }

        // Add current URL
        event.url = window.location.href;

        window.envgenEvents.push(event);
        console.log('[EnvGen] Event stored, total events:', window.envgenEvents.length);

        // Send immediately to background script so we don't lose events on page navigation
        chrome.runtime.sendMessage({
            type: 'UI_EVENTS',
            events: [event]
        }).catch(err => {
            console.warn('[EnvGen] Failed to send event to background:', err);
        });
    };

    // Register event listeners
    const eventTypes = [
        'click', 'dblclick', 'mousedown', 'mouseup', 'mousemove', 'wheel',
        'keydown', 'keyup', 'input', 'change',
        'submit', 'scroll', 'focus', 'blur'
    ];

    // Register event listeners with capture to intercept before page scripts
    eventTypes.forEach(type => {
        document.addEventListener(type, handleEvent, { capture: true });
    });

    console.log('[EnvGen] Registered', eventTypes.length, 'event listeners:', eventTypes.join(', '));

    // Setup DOM mutation observer to detect when page changes settle
    const observer = new MutationObserver((mutations) => {
        // Only track mutations if we've had a recent user action
        if (Date.now() - window.envgenLastActionTime < 5000) {
            window.envgenLastDOMChange = Date.now();

            // Clear previous timer
            if (window.envgenDOMSettleTimer) {
                clearTimeout(window.envgenDOMSettleTimer);
            }

            // Set new timer - if DOM stops changing for 300ms, consider it "settled"
            window.envgenDOMSettleTimer = setTimeout(() => {
                const settleTime = Date.now();
                console.log('[EnvGen] DOM settled at', settleTime, '(action was at', window.envgenLastActionTime, ')');

                // Send DOM settle event
                chrome.runtime.sendMessage({
                    type: 'UI_EVENTS',
                    events: [{
                        type: 'dom_settle',
                        seq_id: window.envgenSeqId++,
                        timestamp: settleTime,
                        url: window.location.href,
                        target: {},
                        metadata: {
                            action_timestamp: window.envgenLastActionTime,
                            settle_delay_ms: settleTime - window.envgenLastActionTime,
                            mutation_count: mutations.length
                        }
                    }]
                }).catch(err => {
                    console.warn('[EnvGen] Failed to send DOM settle event:', err);
                });
            }, 300);
        }
    });

    // Observe DOM changes
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeOldValue: false,
        characterData: true
    });

    console.log('[EnvGen] DOM mutation observer enabled');

    // Intercept window.open() to prevent new tabs
    const originalWindowOpen = window.open;
    window.open = function (url, target, features) {
        console.log('[EnvGen] Intercepting window.open():', url);
        // Navigate in same window instead of opening new tab/window
        if (url) {
            window.location.href = url;
        }
        // Return a fake window object to avoid breaking code that expects a return value
        return window;
    };

    // Intercept links that would open in new tabs
    document.addEventListener('click', (e) => {
        const target = e.target;
        const link = target.closest('a');

        if (!link || !link.href) return;

        // Check if this would open in a new tab
        const wouldOpenNewTab = (
            link.target === '_blank' ||
            link.target === '_new' ||
            e.ctrlKey ||
            e.metaKey ||
            e.button === 1  // Middle click
        );

        if (wouldOpenNewTab) {
            console.log('[EnvGen] Intercepting new tab link:', link.href);
            e.preventDefault();
            e.stopPropagation();

            // Navigate in same tab instead
            window.location.href = link.href;
        }
    }, { capture: true });

    console.log('[EnvGen] Link and window.open() interception enabled - all navigation will stay in same tab');

    // Listen for messages from background script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'GET_EVENTS') {
            console.log('[EnvGen] Returning', window.envgenEvents.length, 'events to background');
            sendResponse({
                events: window.envgenEvents,
                recordingStart: window.envgenRecordingStart
            });
            return false; // Synchronous response
        } else if (message.type === 'CLEAR_EVENTS') {
            console.log('[EnvGen] Clearing events');
            window.envgenEvents = [];
            window.envgenSeqId = 0;
            sendResponse({ success: true });
            return false; // Synchronous response
        } else if (message.type === 'SHOW_PAUSE_INDICATOR') {
            // Show pause marker indicator (recording continues!)
            console.log('[EnvGen] Received SHOW_PAUSE_INDICATOR message');
            
            // Helper function to show pause indicator
            const showPauseIndicator = () => {
                // Remove existing indicator if present
                const existing = document.getElementById('envgen-pause-indicator');
                if (existing) {
                    existing.remove();
                }
                
                const indicator = document.createElement('div');
                indicator.id = 'envgen-pause-indicator';
                indicator.style.cssText = `
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    background: rgba(245, 158, 11, 0.15);
                    backdrop-filter: blur(2px);
                    color: #f59e0b;
                    padding: 12px 20px;
                    border-radius: 8px;
                    border: 1px solid rgba(245, 158, 11, 0.3);
                    z-index: 2147483647;
                    pointer-events: none;
                    font-family: system-ui, -apple-system, sans-serif;
                    font-size: 14px;
                    font-weight: 600;
                    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
                    text-align: center;
                    opacity: 0.8;
                `;
                indicator.innerHTML = '⏸ PAUSE MARKER ACTIVE';

                document.body.appendChild(indicator);
                console.log('[EnvGen] Pause marker indicator shown');
            };
            
            if (!document.body) {
                console.warn('[EnvGen] document.body not ready, waiting...');
                // Wait for body to be ready
                const checkBody = setInterval(() => {
                    if (document.body) {
                        clearInterval(checkBody);
                        showPauseIndicator();
                        sendResponse({ success: true });
                    }
                }, 100);
                // Timeout after 5 seconds
                setTimeout(() => {
                    clearInterval(checkBody);
                    sendResponse({ success: false, error: 'document.body timeout' });
                }, 5000);
                return true; // Async response
            }
            
            showPauseIndicator();
            sendResponse({ success: true });
            return false; // Synchronous response
        } else if (message.type === 'HIDE_PAUSE_INDICATOR') {
            // Hide pause marker indicator
            console.log('[EnvGen] Received HIDE_PAUSE_INDICATOR message');
            const indicator = document.getElementById('envgen-pause-indicator');
            if (indicator) {
                indicator.remove();
                console.log('[EnvGen] Pause marker indicator hidden');
            } else {
                console.warn('[EnvGen] Pause indicator not found to hide');
            }
            sendResponse({ success: true });
            return false; // Synchronous response
        } else if (message.type === 'SHOW_RECORDING_MARKER') {
            // Show clear calibration pattern: white-black-white flash sequence
            // Make sure body exists
            if (!document.body) {
                console.error('[EnvGen] Cannot show calibration marker - document.body not ready');
                sendResponse({ success: false, error: 'document.body not ready' });
                return;
            }

            const marker = document.createElement('div');
            marker.style.cssText = 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 2147483647; pointer-events: none;';
            document.body.appendChild(marker);

            const markerTimestamp = Date.now();
            console.log('[EnvGen] Calibration marker START at', markerTimestamp);

            // Send marker event to background
            chrome.runtime.sendMessage({
                type: 'UI_EVENTS',
                events: [{
                    type: 'calibration_marker',
                    seq_id: window.envgenSeqId++,
                    timestamp: markerTimestamp,
                    url: window.location.href,
                    target: {},
                    metadata: {
                        marker_type: 'calibration_start',
                        description: 'White-black-white flash pattern for timing calibration'
                    }
                }]
            });

            // Flash pattern: White (200ms) -> Black (200ms) -> White (200ms)
            const flashPattern = async () => {
                // Flash 1: White
                marker.style.background = 'rgb(255, 255, 255)';
                await new Promise(r => setTimeout(r, 200));

                // Flash 2: Black
                marker.style.background = 'rgb(0, 0, 0)';
                await new Promise(r => setTimeout(r, 200));

                // Flash 3: White
                marker.style.background = 'rgb(255, 255, 255)';
                await new Promise(r => setTimeout(r, 200));

                // Remove marker
                marker.remove();

                const endTimestamp = Date.now();
                console.log('[EnvGen] Calibration marker END at', endTimestamp, '(duration:', endTimestamp - markerTimestamp, 'ms)');
            };

            flashPattern();
            sendResponse({ success: true });
        }
    });

    console.log('[EnvGen] Content script fully initialized and ready');
})();
