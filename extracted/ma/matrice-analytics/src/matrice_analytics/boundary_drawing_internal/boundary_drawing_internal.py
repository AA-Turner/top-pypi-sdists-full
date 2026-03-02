import cv2
import numpy as np
import argparse
import os
import webbrowser
import sys
import json
import base64
from pathlib import Path
from typing import List, Tuple, Dict, Any


class BoundaryDrawingTool:
    """
    A comprehensive tool for drawing boundaries, polygons, and lines on video frames or images.
    Supports multiple zones with custom tags like queue, staff, entry, exit, restricted zone, etc.
    """
    
    def __init__(self):
        """Initialize the boundary drawing tool."""
        self.supported_formats = {
            'video': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'],
            'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        }
        
    def extract_first_frame(self, video_path: str, output_path: str = None) -> str:
        """
        Extract the first frame from a video file.
        
        Args:
            video_path (str): Path to the video file
            output_path (str): Path to save the extracted frame
            
        Returns:
            str: Path to the extracted frame
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
            
        # Read first frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError(f"Cannot read first frame from video: {video_path}")
            
        # Generate output path if not provided
        if output_path is None:
            video_name = Path(video_path).stem
            output_path = f"{video_name}_first_frame.jpg"
            
        # Save frame
        cv2.imwrite(output_path, frame)
        print(f"First frame extracted and saved to: {output_path}")
        
        return output_path
        
    def create_grid_reference_image(self, frame_path: str, output_path: str = None, grid_step: int = 50) -> str:
        """
        Create a grid reference image to help users define coordinates.
        
        Args:
            frame_path (str): Path to the input frame/image
            output_path (str): Path to save the grid reference image
            grid_step (int): Grid line spacing in pixels
            
        Returns:
            str: Path to the grid reference image
        """
        # Read the image
        frame = cv2.imread(frame_path)
        if frame is None:
            raise ValueError(f"Cannot read image file: {frame_path}")
            
        h, w = frame.shape[:2]
        
        # Create a grid overlay
        grid_frame = frame.copy()
        
        # Draw vertical lines
        for x in range(0, w, grid_step):
            cv2.line(grid_frame, (x, 0), (x, h), (255, 255, 255), 1)
            # Add x-coordinate labels
            if x % 100 == 0:  # Label every 100 pixels
                cv2.putText(grid_frame, str(x), (x + 2, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
        # Draw horizontal lines
        for y in range(0, h, grid_step):
            cv2.line(grid_frame, (0, y), (w, y), (255, 255, 255), 1)
            # Add y-coordinate labels
            if y % 100 == 0:  # Label every 100 pixels
                cv2.putText(grid_frame, str(y), (5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Generate output path if not provided
        if output_path is None:
            frame_name = Path(frame_path).stem
            output_path = f"{frame_name}_grid_reference.jpg"
            
        # Save the grid image
        cv2.imwrite(output_path, grid_frame)
        print(f"Grid reference image saved to: {output_path}")
        
        return output_path
        
    def image_to_base64(self, image_path: str) -> str:
        """
        Convert image to base64 for embedding in HTML.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Base64 encoded image data
        """
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        # Get file extension for MIME type
        ext = Path(image_path).suffix.lower()
        mime_type = "image/jpeg" if ext in ['.jpg', '.jpeg'] else f"image/{ext[1:]}"
        
        return f"data:{mime_type};base64,{encoded_string}"
        
    def create_interactive_html(self, image_path: str, output_html: str = None, embed_image: bool = True) -> str:
        """
        Create an interactive HTML page for drawing boundaries with custom tags.
        
        Args:
            image_path (str): Path to the reference image
            output_html (str): Path to save the HTML file
            embed_image (bool): Whether to embed image as base64 or use file path
            
        Returns:
            str: Path to the HTML file
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        # Generate output path if not provided
        if output_html is None:
            image_name = Path(image_path).stem
            output_html = f"{image_name}_boundary_tool.html"
            
        # Prepare image source
        if embed_image:
            image_src = self.image_to_base64(image_path)
        else:
            image_src = Path(image_path).name
            
        html_content = self._generate_html_template(image_src, Path(image_path).name)
        
        # Write HTML file
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Interactive HTML boundary tool created: {output_html}")
        return output_html
        
    def _generate_html_template(self, image_src: str, image_name: str) -> str:
        """Generate the HTML template for the boundary drawing tool."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boundary Drawing Tool - {image_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
        }}
        .main-content {{
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 20px;
            min-height: calc(100vh - 120px);
        }}
        .sidebar {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            height: fit-content;
            position: sticky;
            top: 20px;
        }}
        .image-container {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: relative;
            overflow: auto;
        }}
        .image-wrapper {{
            position: relative;
            display: inline-block;
            border: 2px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
        }}
        img {{
            display: block;
            max-width: 100%;
            height: auto;
        }}
        canvas {{
            position: absolute;
            top: 0;
            left: 0;
            cursor: crosshair;
            pointer-events: auto;
        }}
        .control-section {{
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }}
        .control-section:last-child {{
            border-bottom: none;
        }}
        .control-section h3 {{
            margin: 0 0 15px 0;
            color: #34495e;
            font-size: 16px;
            font-weight: 600;
        }}
        .zone-types {{
            display: grid;
            gap: 8px;
            margin-bottom: 15px;
        }}
        .zone-btn {{
            padding: 10px 15px;
            border: 2px solid transparent;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            text-align: center;
            transition: all 0.2s ease;
            background: #f8f9fa;
            color: #495057;
        }}
        .zone-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .zone-btn.active {{
            background: #007bff;
            color: white;
            border-color: #0056b3;
        }}
        .zone-btn.queue {{ background: #28a745; color: white; }}
        .zone-btn.staff {{ background: #17a2b8; color: white; }}
        .zone-btn.entry {{ background: #ffc107; color: #212529; }}
        .zone-btn.exit {{ background: #dc3545; color: white; }}
        .zone-btn.restricted {{ background: #6f42c1; color: white; }}
        .zone-btn.waiting {{ background: #fd7e14; color: white; }}
        .zone-btn.service {{ background: #20c997; color: white; }}
        .zone-btn.security {{ background: #495057; color: white; }}
        
        .drawing-controls {{
            display: grid;
            gap: 8px;
        }}
        .control-btn {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s ease;
        }}
        .control-btn:hover {{
            background: #f8f9fa;
            border-color: #adb5bd;
        }}
        .control-btn.primary {{
            background: #007bff;
            color: white;
            border-color: #0056b3;
        }}
        .control-btn.danger {{
            background: #dc3545;
            color: white;
            border-color: #c82333;
        }}
        .control-btn.success {{
            background: #28a745;
            color: white;
            border-color: #1e7e34;
        }}
        
        .coordinates-display {{
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #666;
            background: #f8f9fa;
            padding: 8px;
            border-radius: 4px;
            margin-bottom: 10px;
            min-height: 20px;
        }}
        
        .zones-list {{
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #f8f9fa;
        }}
        .zone-item {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: white;
            margin-bottom: 1px;
        }}
        .zone-item:last-child {{
            border-bottom: none;
        }}
        .zone-tag {{
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
            color: white;
        }}
        .zone-actions {{
            display: flex;
            gap: 5px;
        }}
        .zone-actions button {{
            padding: 2px 6px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 11px;
        }}
        
        .code-output {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
            margin-top: 10px;
            border: 1px solid #4a5568;
        }}
        
        .current-mouse {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
        }}
        
        .mode-indicator {{
            background: #e3f2fd;
            border: 1px solid #2196f3;
            border-radius: 4px;
            padding: 8px 12px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: 500;
            color: #1976d2;
        }}
        
        .instructions {{
            background: #f0f8f0;
            border: 1px solid #4caf50;
            border-radius: 4px;
            padding: 12px;
            margin-bottom: 20px;
            font-size: 13px;
            line-height: 1.4;
        }}
        
        .custom-tag-input {{
            display: flex;
            gap: 5px;
            margin-top: 10px;
        }}
        .custom-tag-input input {{
            flex: 1;
            padding: 6px 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }}
        .custom-tag-input button {{
            padding: 6px 10px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Boundary Drawing Tool</h1>
        
        <div class="main-content">
            <div class="sidebar">
                <div class="instructions">
                    <strong>Instructions:</strong><br>
                    1. Select a zone type<br>
                    2. Click on image to add points<br>
                    3. Complete polygon/line<br>
                    4. Copy generated code
                </div>
                
                <div class="mode-indicator" id="modeIndicator">
                    Select a zone type to start
                </div>
                
                <div class="control-section">
                    <h3>Zone Types</h3>
                    <div class="zone-types">
                        <div class="zone-btn queue" onclick="setZoneType('queue')">🏃 Queue Area</div>
                        <div class="zone-btn staff" onclick="setZoneType('staff')">👥 Staff Area</div>
                        <div class="zone-btn entry" onclick="setZoneType('entry')">🚪 Entry Zone</div>
                        <div class="zone-btn exit" onclick="setZoneType('exit')">🚶 Exit Zone</div>
                        <div class="zone-btn restricted" onclick="setZoneType('restricted')">🚫 Restricted</div>
                        <div class="zone-btn waiting" onclick="setZoneType('waiting')">⏰ Waiting Area</div>
                        <div class="zone-btn service" onclick="setZoneType('service')">🛎️ Service Area</div>
                        <div class="zone-btn security" onclick="setZoneType('security')">🔒 Security Zone</div>
                    </div>
                    
                    <div class="custom-tag-input">
                        <input type="text" id="customTagInput" placeholder="Custom tag...">
                        <button onclick="setCustomZoneType()">Add</button>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>Drawing Mode</h3>
                    <div class="drawing-controls">
                        <button class="control-btn" onclick="setDrawingMode('polygon')" id="polygonBtn">📐 Polygon</button>
                        <button class="control-btn" onclick="setDrawingMode('line')" id="lineBtn">📏 Line</button>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>Controls</h3>
                    <div class="drawing-controls">
                        <button class="control-btn primary" onclick="completeCurrentZone()">✅ Complete Zone</button>
                        <button class="control-btn" onclick="undoLastPoint()">↶ Undo Point</button>
                        <button class="control-btn danger" onclick="cancelCurrentZone()">❌ Cancel Zone</button>
                        <button class="control-btn" onclick="clearAll()">🗑️ Clear All</button>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>Current Position</h3>
                    <div class="coordinates-display" id="currentCoords">
                        Move mouse over image
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>Export</h3>
                    <div class="drawing-controls">
                        <button class="control-btn success" onclick="generateCode()">📋 Generate Code</button>
                        <button class="control-btn" onclick="saveConfiguration()">💾 Save Config</button>
                        <button class="control-btn" onclick="loadConfiguration()">📁 Load Config</button>
                    </div>
                </div>
            </div>
            
            <div class="image-container">
                <div class="image-wrapper">
                    <img src="{image_src}" id="referenceImage" alt="Reference Image">
                    <canvas id="drawingCanvas"></canvas>
                </div>
                
                <div class="control-section">
                    <h3>Defined Zones</h3>
                    <div class="zones-list" id="zonesList">
                        <div style="padding: 20px; text-align: center; color: #666;">
                            No zones defined yet
                        </div>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>Generated Code</h3>
                    <div class="code-output" id="codeOutput">
# No zones defined yet
zones = {{}}
                    </div>
                    <button class="control-btn success" onclick="copyCode()" style="margin-top: 10px;">📋 Copy Code</button>
                </div>
            </div>
        </div>
    </div>
    
    <div class="current-mouse" id="mouseTracker">x: 0, y: 0</div>
    
    <input type="file" id="fileInput" accept=".json" style="display: none;" onchange="handleFileLoad(event)">
    
    <script>
        // Global state
        let currentZoneType = null;
        let currentDrawingMode = 'polygon';
        let currentPoints = [];
        let completedZones = [];
        let isDrawing = false;
        let mousePos = {{ x: 0, y: 0 }};
        
        // Canvas and image elements
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('referenceImage');
        const modeIndicator = document.getElementById('modeIndicator');
        const currentCoords = document.getElementById('currentCoords');
        const mouseTracker = document.getElementById('mouseTracker');
        const zonesList = document.getElementById('zonesList');
        const codeOutput = document.getElementById('codeOutput');
        
        // Zone type colors
        const zoneColors = {{
            'queue': '#28a745',
            'staff': '#17a2b8', 
            'entry': '#ffc107',
            'exit': '#dc3545',
            'restricted': '#6f42c1',
            'waiting': '#fd7e14',
            'service': '#20c997',
            'security': '#495057'
        }};
        
        // Initialize canvas when image loads
        img.onload = function() {{
            setupCanvas();
        }};
        
        if (img.complete) {{
            setupCanvas();
        }}
        
        function setupCanvas() {{
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            canvas.style.width = img.clientWidth + 'px';
            canvas.style.height = img.clientHeight + 'px';
            redrawCanvas();
        }}
        
        // Mouse event handlers
        canvas.addEventListener('mousemove', function(e) {{
            updateMousePosition(e);
        }});
        
        canvas.addEventListener('click', function(e) {{
            if (!currentZoneType) {{
                alert('Please select a zone type first!');
                return;
            }}
            addPoint(e);
        }});
        
        canvas.addEventListener('contextmenu', function(e) {{
            e.preventDefault();
            if (currentPoints.length > 0) {{
                completeCurrentZone();
            }}
        }});
        
        function updateMousePosition(e) {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            mousePos.x = Math.round((e.clientX - rect.left) * scaleX);
            mousePos.y = Math.round((e.clientY - rect.top) * scaleY);
            
            currentCoords.textContent = `x: ${{mousePos.x}}, y: ${{mousePos.y}}`;
            mouseTracker.textContent = `x: ${{mousePos.x}}, y: ${{mousePos.y}}`;
            
            redrawCanvas();
        }}
        
        function addPoint(e) {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            const x = Math.round((e.clientX - rect.left) * scaleX);
            const y = Math.round((e.clientY - rect.top) * scaleY);
            
            currentPoints.push([x, y]);
            isDrawing = true;
            
            updateModeIndicator();
            redrawCanvas();
            
            // Auto-complete line when 2 points are added
            if (currentDrawingMode === 'line' && currentPoints.length === 2) {{
                completeCurrentZone();
            }}
        }}
        
        function setZoneType(type) {{
            currentZoneType = type;
            
            // Update UI
            document.querySelectorAll('.zone-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            updateModeIndicator();
        }}
        
        function setCustomZoneType() {{
            const input = document.getElementById('customTagInput');
            const customType = input.value.trim();
            
            if (customType) {{
                currentZoneType = customType;
                input.value = '';
                
                // Remove active class from preset buttons
                document.querySelectorAll('.zone-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                
                updateModeIndicator();
            }}
        }}
        
        function setDrawingMode(mode) {{
            currentDrawingMode = mode;
            
            // Update UI
            document.getElementById('polygonBtn').classList.remove('primary');
            document.getElementById('lineBtn').classList.remove('primary');
            document.getElementById(mode + 'Btn').classList.add('primary');
            
            updateModeIndicator();
        }}
        
        function updateModeIndicator() {{
            if (!currentZoneType) {{
                modeIndicator.textContent = 'Select a zone type to start';
                modeIndicator.style.background = '#f8f9fa';
                modeIndicator.style.borderColor = '#ddd';
                modeIndicator.style.color = '#666';
                return;
            }}
            
            let modeText = `Drawing ${{currentDrawingMode}} for "${{currentZoneType}}" zone`;
            
            if (isDrawing) {{
                const pointsNeeded = currentDrawingMode === 'line' ? 2 : 3;
                const remaining = Math.max(0, pointsNeeded - currentPoints.length);
                modeText += ` (${{currentPoints.length}} points, need ${{remaining}} more)`;
            }}
            
            modeIndicator.textContent = modeText;
            modeIndicator.style.background = '#e3f2fd';
            modeIndicator.style.borderColor = '#2196f3';
            modeIndicator.style.color = '#1976d2';
        }}
        
        function completeCurrentZone() {{
            if (!currentZoneType || currentPoints.length === 0) return;
            
            const minPoints = currentDrawingMode === 'line' ? 2 : 3;
            if (currentPoints.length < minPoints) {{
                alert(`Need at least ${{minPoints}} points for a ${{currentDrawingMode}}!`);
                return;
            }}
            
            // Create zone object
            const zone = {{
                type: currentZoneType,
                mode: currentDrawingMode,
                points: [...currentPoints],
                color: zoneColors[currentZoneType] || '#333333',
                id: 'zone_' + Date.now()
            }};
            
            completedZones.push(zone);
            
            // Reset current drawing
            currentPoints = [];
            isDrawing = false;
            
            updateModeIndicator();
            updateZonesList();
            generateCode();
            redrawCanvas();
        }}
        
        function undoLastPoint() {{
            if (currentPoints.length > 0) {{
                currentPoints.pop();
                updateModeIndicator();
                redrawCanvas();
            }}
        }}
        
        function cancelCurrentZone() {{
            currentPoints = [];
            isDrawing = false;
            updateModeIndicator();
            redrawCanvas();
        }}
        
        function clearAll() {{
            if (confirm('Clear all zones? This cannot be undone.')) {{
                currentPoints = [];
                completedZones = [];
                isDrawing = false;
                updateModeIndicator();
                updateZonesList();
                generateCode();
                redrawCanvas();
            }}
        }}
        
        function deleteZone(zoneId) {{
            completedZones = completedZones.filter(zone => zone.id !== zoneId);
            updateZonesList();
            generateCode();
            redrawCanvas();
        }}
        
        function redrawCanvas() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw completed zones
            completedZones.forEach(zone => {{
                drawZone(zone);
            }});
            
            // Draw current drawing
            if (currentPoints.length > 0) {{
                const color = zoneColors[currentZoneType] || '#333333';
                drawCurrentDrawing(color);
            }}
            
            // Draw mouse cursor
            if (mousePos.x > 0 && mousePos.y > 0 && isDrawing) {{
                ctx.beginPath();
                ctx.arc(mousePos.x, mousePos.y, 6, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.fill();
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.stroke();
            }}
        }}
        
        function drawZone(zone) {{
            if (zone.points.length === 0) return;
            
            ctx.strokeStyle = zone.color;
            ctx.fillStyle = zone.color + '40'; // Add transparency
            ctx.lineWidth = 3;
            
            if (zone.mode === 'line') {{
                // Draw line
                ctx.beginPath();
                ctx.moveTo(zone.points[0][0], zone.points[0][1]);
                ctx.lineTo(zone.points[1][0], zone.points[1][1]);
                ctx.stroke();
            }} else {{
                // Draw polygon
                ctx.beginPath();
                ctx.moveTo(zone.points[0][0], zone.points[0][1]);
                for (let i = 1; i < zone.points.length; i++) {{
                    ctx.lineTo(zone.points[i][0], zone.points[i][1]);
                }}
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
            }}
            
            // Draw points
            zone.points.forEach((point, index) => {{
                ctx.beginPath();
                ctx.arc(point[0], point[1], 5, 0, Math.PI * 2);
                ctx.fillStyle = '#fff';
                ctx.fill();
                ctx.strokeStyle = zone.color;
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Draw point number
                ctx.fillStyle = '#333';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(index + 1, point[0], point[1] - 10);
            }});
            
            // Draw zone label
            if (zone.points.length > 0) {{
                const centerX = zone.points.reduce((sum, p) => sum + p[0], 0) / zone.points.length;
                const centerY = zone.points.reduce((sum, p) => sum + p[1], 0) / zone.points.length;
                
                ctx.fillStyle = zone.color;
                ctx.font = 'bold 14px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(zone.type.toUpperCase(), centerX, centerY);
            }}
        }}
        
        function drawCurrentDrawing(color) {{
            if (currentPoints.length === 0) return;
            
            ctx.strokeStyle = color;
            ctx.fillStyle = color + '20';
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 5]);
            
            if (currentDrawingMode === 'line' && currentPoints.length >= 2) {{
                // Draw line
                ctx.beginPath();
                ctx.moveTo(currentPoints[0][0], currentPoints[0][1]);
                ctx.lineTo(currentPoints[1][0], currentPoints[1][1]);
                ctx.stroke();
            }} else if (currentDrawingMode === 'polygon' && currentPoints.length >= 2) {{
                // Draw polygon outline
                ctx.beginPath();
                ctx.moveTo(currentPoints[0][0], currentPoints[0][1]);
                for (let i = 1; i < currentPoints.length; i++) {{
                    ctx.lineTo(currentPoints[i][0], currentPoints[i][1]);
                }}
                ctx.stroke();
                
                // Draw line to mouse position
                if (mousePos.x > 0 && mousePos.y > 0) {{
                    ctx.lineTo(mousePos.x, mousePos.y);
                    ctx.stroke();
                }}
            }}
            
            ctx.setLineDash([]);
            
            // Draw current points
            currentPoints.forEach((point, index) => {{
                ctx.beginPath();
                ctx.arc(point[0], point[1], 4, 0, Math.PI * 2);
                ctx.fillStyle = '#fff';
                ctx.fill();
                ctx.strokeStyle = color;
                ctx.lineWidth = 2;
                ctx.stroke();
            }});
        }}
        
        function updateZonesList() {{
            if (completedZones.length === 0) {{
                zonesList.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">No zones defined yet</div>';
                return;
            }}
            
            zonesList.innerHTML = completedZones.map(zone => `
                <div class="zone-item">
                    <div>
                        <span class="zone-tag" style="background: ${{zone.color}};">${{zone.type}}</span>
                        <small style="margin-left: 8px; color: #666;">
                            ${{zone.mode}} (${{zone.points.length}} points)
                        </small>
                    </div>
                    <div class="zone-actions">
                        <button onclick="deleteZone('${{zone.id}}')" style="background: #dc3545; color: white;">Delete</button>
                    </div>
                </div>
            `).join('');
        }}
        
        function generateCode() {{
            if (completedZones.length === 0) {{
                codeOutput.textContent = '# No zones defined yet\\nzones = {{}}';
                return;
            }}
            
            let code = '# Generated boundary definitions\\n';
            code += '# Copy this code for use in your applications\\n\\n';
            
            // Group zones by type
            const zonesByType = {{}};
            completedZones.forEach(zone => {{
                if (!zonesByType[zone.type]) {{
                    zonesByType[zone.type] = [];
                }}
                zonesByType[zone.type].push(zone);
            }});
            
            // Generate Python dictionary
            code += 'zones = {{\\n';
            Object.keys(zonesByType).forEach(type => {{
                const zones = zonesByType[type];
                if (zones.length === 1) {{
                    code += `    "${{type}}": ${{JSON.stringify(zones[0].points)}},\\n`;
                }} else {{
                    code += `    "${{type}}": {{\\n`;
                    zones.forEach((zone, index) => {{
                        code += `        "${{type}}_${{index + 1}}": ${{JSON.stringify(zone.points)}},\\n`;
                    }});
                    code += `    }},\\n`;
                }}
            }});
            code += '}}\\n\\n';
            
            // Add usage examples
            code += '# Usage examples:\\n';
            code += '# For post-processing configuration:\\n';
            code += '# config.customer_service.customer_areas = zones["queue"]\\n';
            code += '# config.advanced_tracking.boundary_config = {{ "points": zones["entry"] }}\\n\\n';
            
            // Add individual zone coordinates for easy copying
            code += '# Individual zone coordinates:\\n';
            completedZones.forEach((zone, index) => {{
                code += `# ${{zone.type}} ${{zone.mode}} (${{zone.points.length}} points):\\n`;
                code += `${{zone.type}}_${{index + 1}} = ${{JSON.stringify(zone.points)}}\\n`;
            }});
            
            codeOutput.textContent = code;
        }}
        
        function copyCode() {{
            const text = codeOutput.textContent;
            navigator.clipboard.writeText(text).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied!';
                btn.style.background = '#28a745';
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.style.background = '';
                }}, 2000);
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
                alert('Failed to copy to clipboard. Please copy manually.');
            }});
        }}
        
        function saveConfiguration() {{
            const config = {{
                zones: completedZones,
                metadata: {{
                    created: new Date().toISOString(),
                    image: '{image_name}',
                    tool_version: '1.0'
                }}
            }};
            
            const blob = new Blob([JSON.stringify(config, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'boundary_config.json';
            a.click();
            URL.revokeObjectURL(url);
        }}
        
        function loadConfiguration() {{
            document.getElementById('fileInput').click();
        }}
        
        function handleFileLoad(event) {{
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const config = JSON.parse(e.target.result);
                    if (config.zones && Array.isArray(config.zones)) {{
                        completedZones = config.zones;
                        updateZonesList();
                        generateCode();
                        redrawCanvas();
                        alert('Configuration loaded successfully!');
                    }} else {{
                        alert('Invalid configuration file format.');
                    }}
                }} catch (err) {{
                    alert('Error reading configuration file: ' + err.message);
                }}
            }};
            reader.readAsText(file);
        }}
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                cancelCurrentZone();
            }} else if (e.key === 'Enter') {{
                completeCurrentZone();
            }} else if (e.ctrlKey && e.key === 'z') {{
                e.preventDefault();
                undoLastPoint();
            }}
        }});
        
        // Initialize
        updateModeIndicator();
        generateCode();
    </script>
</body>
</html>"""
        
    def open_in_browser(self, html_path: str):
        """
        Open the HTML file in the default web browser.
        
        Args:
            html_path (str): Path to the HTML file
        """
        try:
            webbrowser.open(f'file://{os.path.abspath(html_path)}')
            print(f"Opened boundary tool in browser: {html_path}")
        except Exception as e:
            print(f"Could not open browser: {e}")
            print(f"Please manually open: {html_path}")
            
    def get_file_type(self, file_path: str) -> str:
        """
        Determine if the file is a video or image.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: 'video', 'image', or 'unknown'
        """
        ext = Path(file_path).suffix.lower()
        
        if ext in self.supported_formats['video']:
            return 'video'
        elif ext in self.supported_formats['image']:
            return 'image'
        else:
            return 'unknown'
            
    def process_input_file(self, input_path: str, output_dir: str = None, grid_step: int = 50, 
                          open_browser: bool = True, embed_image: bool = True) -> Dict[str, str]:
        """
        Process an input video or image file and create the boundary drawing tool.
        
        Args:
            input_path (str): Path to input video or image file
            output_dir (str): Directory to save output files
            grid_step (int): Grid line spacing for reference image
            open_browser (bool): Whether to open the tool in browser
            embed_image (bool): Whether to embed image as base64 in HTML
            
        Returns:
            Dict[str, str]: Dictionary with paths to created files
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        # Determine file type
        file_type = self.get_file_type(input_path)
        if file_type == 'unknown':
            raise ValueError(f"Unsupported file format: {Path(input_path).suffix}")
            
        # Set up output directory
        if output_dir is None:
            output_dir = os.path.dirname(input_path) or '.'
        os.makedirs(output_dir, exist_ok=True)
        
        # Get base name for output files
        base_name = Path(input_path).stem
        
        results = {}
        
        # Extract first frame if video
        if file_type == 'video':
            frame_path = os.path.join(output_dir, f"{base_name}_first_frame.jpg")
            frame_path = self.extract_first_frame(input_path, frame_path)
            results['frame'] = frame_path
        else:
            frame_path = input_path
            results['frame'] = frame_path
            
        # Create grid reference image
        grid_path = os.path.join(output_dir, f"{base_name}_grid_reference.jpg")
        grid_path = self.create_grid_reference_image(frame_path, grid_path, grid_step)
        results['grid_reference'] = grid_path
        
        # Create interactive HTML
        html_path = os.path.join(output_dir, f"{base_name}_boundary_tool.html")
        html_path = self.create_interactive_html(grid_path, html_path, embed_image)
        results['html_tool'] = html_path
        
        # Open in browser
        if open_browser:
            self.open_in_browser(html_path)
            
        return results


def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(
        description="Boundary Drawing Tool - Create interactive tools for defining zones and boundaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a video file
  python boundary_drawing_internal.py --input video.mp4 --output ./boundaries/
  
  # Process an image file with custom grid spacing
  python boundary_drawing_internal.py --input frame.jpg --grid-step 25
  
  # Create tool without opening browser
  python boundary_drawing_internal.py --input video.mp4 --no-browser
  
  # Create tool with external image reference (not embedded)
  python boundary_drawing_internal.py --input video.mp4 --no-embed
        """
    )
    
    parser.add_argument('--input', '-i', required=True,
                       help='Input video or image file')
    parser.add_argument('--output', '-o', 
                       help='Output directory for generated files')
    parser.add_argument('--grid-step', type=int, default=50,
                       help='Grid line spacing in pixels (default: 50)')
    parser.add_argument('--no-browser', action='store_true',
                       help='Do not open the tool in browser automatically')
    parser.add_argument('--no-embed', action='store_true',
                       help='Do not embed image as base64 in HTML')
    
    args = parser.parse_args()
    
    try:
        tool = BoundaryDrawingTool()
        
        results = tool.process_input_file(
            input_path=args.input,
            output_dir=args.output,
            grid_step=args.grid_step,
            open_browser=not args.no_browser,
            embed_image=not args.no_embed
        )
        
        print("\n" + "="*60)
        print("🎯 Boundary Drawing Tool - Results")
        print("="*60)
        
        for file_type, path in results.items():
            print(f"{file_type.title().replace('_', ' ')}: {path}")
            
        print("\n📝 Instructions:")
        print("1. Use the interactive HTML tool to draw zones")
        print("2. Select zone types (queue, staff, entry, exit, etc.)")
        print("3. Click on the image to add points")
        print("4. Right-click or press Enter to complete a zone")
        print("5. Copy the generated code for use in your applications")
        
        if not args.no_browser:
            print(f"\n🌐 Tool opened in browser: {results['html_tool']}")
        else:
            print(f"\n🌐 Open this file in browser: {results['html_tool']}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()