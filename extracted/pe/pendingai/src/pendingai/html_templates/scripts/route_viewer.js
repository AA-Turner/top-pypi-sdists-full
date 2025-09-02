document.addEventListener('DOMContentLoaded', function() {
    var elements = JSON.parse(document.getElementById('cytoscape-data').textContent);

    elements.forEach(function(el) {
        if (el.group === 'nodes' && el.data.svg) {
            el.data.svg = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(el.data.svg);
        }
    });

    // Some depictions are slightly blurred in FF at 100% zoom level.
    // Adding an small offset to the zoom level of 100% removes the issue.
    // For a less confusing UX we don't show this offset to the user in the UI components.
    const zoomFuzzinessOffset = 0.05;
    var cy = cytoscape({
        container: document.getElementById('cy'),
        elements: elements,

        zoom: 1 + zoomFuzzinessOffset,
        zoomingEnabled: true,
        userZoomingEnabled: true,
        panningEnabled: true,
        userPanningEnabled: true,
        autolock: false,
        autoungrabify: false,
        autounselectify: false,

        style: [
            {
                selector: 'node',
                style: {
                    'shape': 'rectangle',
                    'background-image': 'data(svg)',
                    'background-fit': 'none',
                    'background-color': 'white',
                    'width': 'data(width)',
                    'height': 'data(height)',
                    'border-width': 2,
                    'border-color': '#e5e7eb',
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#d1d5db',
                    'source-arrow-color': '#d1d5db',
                    'source-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            }
        ],
        layout: {
            name: 'breadthfirst',
            directed: true,
            fit: false,
            spacingFactor: 1,
            grid: true
        }
    });

    // --- START: CUSTOM CONTROLS LOGIC ---
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const zoomSlider = document.getElementById('zoom-slider');
    const zoomLevelSpan = document.getElementById('zoom-level');
    const panLeftBtn = document.getElementById('pan-left');
    const panRightBtn = document.getElementById('pan-right');
    const panUpBtn = document.getElementById('pan-up');
    const panDownBtn = document.getElementById('pan-down');
    const fitBtn = document.getElementById('fit-view');
    const resetBtn = document.getElementById('reset-view');

    const panStep = 50;
    const zoomStep = 0.2;

    /**
     * Checks if the graph is taller than the viewport and, if so, pans
     * the graph down to ensure the root node is visible.
     */
    function panRootIntoView() {
        // Use requestAnimationFrame to ensure calculations happen after the DOM is updated.
        requestAnimationFrame(() => {
            const allElementsRbb = cy.elements().renderedBoundingBox();
            if (allElementsRbb.h > cy.height()) {
                const root = cy.nodes().roots()[0];
                if (root) {
                    const rootRbb = root.renderedBoundingBox();
                    // If root's top is above the viewport, pan down to make it visible
                    if (rootRbb.y1 < 0) {
                        cy.panBy({ y: -rootRbb.y1 + 30 }); // 30px padding
                    }
                }
            }
        });
    }


    // --- Event Listeners ---
    zoomInBtn.addEventListener('click', () => {
        const currentDisplayZoom = cy.zoom() - zoomFuzzinessOffset;
        cy.zoom({
            level: currentDisplayZoom + zoomStep + zoomFuzzinessOffset,
            renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 }
        });
    });

    zoomOutBtn.addEventListener('click', () => {
        const currentDisplayZoom = cy.zoom() - zoomFuzzinessOffset;
        cy.zoom({
            level: currentDisplayZoom - zoomStep + zoomFuzzinessOffset,
            renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 }
        });
    });

    zoomSlider.addEventListener('input', (e) => {
        cy.zoom({
            level: parseFloat(e.target.value) + zoomFuzzinessOffset,
            renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 }
        });
    });

    cy.on('zoom', () => {
        const displayZoom = cy.zoom() - zoomFuzzinessOffset;
        zoomSlider.value = displayZoom;
        zoomLevelSpan.textContent = `${(displayZoom * 100).toFixed(0)}%`;
    });

    panLeftBtn.addEventListener('click', () => cy.panBy({ x: panStep, y: 0 }));
    panRightBtn.addEventListener('click', () => cy.panBy({ x: -panStep, y: 0 }));
    panUpBtn.addEventListener('click', () => cy.panBy({ x: 0, y: panStep }));
    panDownBtn.addEventListener('click', () => cy.panBy({ x: 0, y: -panStep }));

    fitBtn.addEventListener('click', () => {
        cy.fit(cy.elements(), 30); // 30px padding
    });

    resetBtn.addEventListener('click', () => {
        cy.zoom(1 + zoomFuzzinessOffset);
        cy.center();
        panRootIntoView(); // Ensure the root is visible after resetting
    });
    // --- END: CUSTOM CONTROLS LOGIC ---

    cy.ready(function() {
        var layout = cy.layout({
            name: 'breadthfirst',
            directed: true,
            fit: false,
            padding: 15,
            spacingFactor: 0.85,
            grid: true
        });

        layout.promiseOn('layoutstop').then(function() {
            // vertical compression and centering ---
            const minGap = 50; // the gap between tree levels; adjust to control vertical tree compression
            const nodesByY = {};

            // 1. Group nodes by their original Y position to identify levels
            cy.nodes().forEach(node => {
                const y = node.position().y;
                if (!nodesByY[y]) {
                    nodesByY[y] = [];
                }
                nodesByY[y].push(node);
            });

            const sortedYLevels = Object.keys(nodesByY).map(parseFloat).sort((a, b) => a - b);

            // 2. Reposition levels sequentially from top to bottom
            if (sortedYLevels.length > 1) {
                let lastLevelNodes = nodesByY[sortedYLevels[0]];
                let lastLevelMaxY = Math.max(...lastLevelNodes.map(n => n.position().y + n.height() / 2));

                for (let i = 1; i < sortedYLevels.length; i++) {
                    const currentLevelY = sortedYLevels[i];
                    const currentLevelNodes = nodesByY[currentLevelY];
                    const maxNodeHeightInLevel = Math.max(...currentLevelNodes.map(n => n.height()));
                    const newY = lastLevelMaxY + minGap + (maxNodeHeightInLevel / 2);

                    currentLevelNodes.forEach(node => {
                        node.position('y', newY);
                    });
                    lastLevelMaxY = newY + maxNodeHeightInLevel / 2;
                }
            }

            // 3. Center the graph and then ensure the root node is visible
            cy.center();
            panRootIntoView();
        });

        layout.run();
    });
});
