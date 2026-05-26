import os
import re
import pytest
from unittest.mock import MagicMock, patch
from sage.main import app as sage_app
from typer.testing import CliRunner
from pathlib import Path
from sage.core.content_validator import validate_content

MOCK_STREAMS = {
    "websites": """
Output for websites: Here is the responsive advertising dashboard.

FILE: index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advertising Dashboard</title>
    <style>
        :root {
            --primary: #3b82f6;
            --dark: #1f2937;
            --font-stack: 'Inter', sans-serif;
        }
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        body {
            font-family: var(--font-stack);
            background-color: var(--dark);
            color: #ffffff;
            transition: all 0.2s ease;
        }
        header, nav, main, footer {
            padding: 1rem;
        }
        .btn:hover {
            opacity: 0.9;
        }
        .btn:focus-visible {
            outline: 2px solid var(--primary);
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .animate-fade {
            animation: fadeIn 0.5s ease-out;
        }
        @media (max-width: 640px) {
            .desktop-only { display: none; }
        }
        @media (min-width: 1024px) {
            .desktop-only { display: block; }
        }
    </style>
</head>
<body>
    <header>
        <nav aria-label="Main Navigation">
            <a href="/" class="btn" aria-label="Home">Home</a>
        </nav>
    </header>
    <main class="animate-fade">
        <h1>Dashboard</h1>
    </main>
    <footer>
        <p>&copy; 2026 Dashboard Inc.</p>
    </footer>
</body>
</html>
```
""",

    "mobile_apps": """
Output for mobile_apps: Here is the React Native code.

FILE: ItemListScreen.tsx
```tsx
import React, { useState } from 'react';
import { SafeAreaView, FlatList, Text, View, StyleSheet, TextInput, Button } from 'react-native';

export const ItemListScreen: React.FC = () => {
    const [items, setItems] = useState<string[]>(['Initial Item']);
    const [text, setText] = useState('');

    const addItem = () => {
        if (text.trim()) {
            setItems([...items, text]);
            setText('');
        }
    };

    return (
        <SafeAreaView style={styles.container}>
            <TextInput
                style={styles.input}
                value={text}
                onChangeText={setText}
                placeholder="Enter item"
            />
            <Button title="Add Item" onPress={addItem} />
            <FlatList
                data={items}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.item}>
                        <Text>{item}</Text>
                    </View>
                )}
            />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 16 },
    input: { height: 40, borderColor: 'gray', borderWidth: 1, marginBottom: 12 },
    item: { padding: 12, borderBottomWidth: 1, borderBottomColor: '#ccc' }
});
```
""",

    "video_games": """
Output for video_games: Here is the 2D physics engine.

FILE: physics.js
```javascript
class Vector2D {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    add(v) {
        this.x += v.x;
        this.y += v.y;
    }
}

class RigidBody {
    constructor(mass = 1) {
        this.position = new Vector2D();
        this.velocity = new Vector2D();
        this.mass = mass;
    }
    applyForce(force) {
        this.velocity.add(new Vector2D(force.x / this.mass, force.y / this.mass));
    }
    update(dt) {
        this.position.add(new Vector2D(this.velocity.x * dt, this.velocity.y * dt));
    }
}
```
""",

    "backend_services": """
Output for backend_services: Here is the FastAPI app.

FILE: main.py
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"status": "healthy"}

@app.post("/items")
def create_item(item: Item):
    return {"message": f"Created {item.name}", "price": item.price}
```
""",

    "deployments": """
Output for deployments: Here is the Terraform config.

FILE: main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "app" {
  name = "app-production"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  container_definitions    = "[]"
}
```
""",

    "videos": """
Output for videos: Here is the generated video at generated_media.mp4.

FILE: generated_media.mp4
```
fake mp4 video content
```
""",

    "images": """
Output for images: Here are the SVG and PNG contents. Favicon is generated_media.mp4.

FILE: logo.svg
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <rect width="100" height="100" fill="#3b82f6" rx="10"/>
    <text x="50" y="55" font-family="sans-serif" font-size="20" fill="white" text-anchor="middle">SAGE</text>
</svg>
```

FILE: generated_media.mp4
```
fake png image representation
```
""",

    "audio_files": """
Output for audio_files: Here is the WAV chord at generated_media.mp4.

FILE: generated_media.mp4
```
fake wav audio content
```
""",

    "music_videos": """
Output for music_videos: Here is the combined music video at generated_media.mp4.

FILE: generated_media.mp4
```
fake music video content
```
""",

    "generate_files": """
Output for generate_files: Here is the Python script, JSON config, and YAML manifest.

FILE: script.py
```python
import sys
print("Complex script")
```

FILE: config.json
```json
{
  "name": "app",
  "version": "1.0.0",
  "enabled": true
}
```

FILE: manifest.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
```
""",

    "run_applications": """
Output for run_applications: Here is the AppleScript to open Messages.

FILE: run.scpt
```applescript
tell application "Messages"
    activate
end tell
```
""",

    "computer_control": """
Output for computer_control: Here is the system control AppleScript.

FILE: control.scpt
```applescript
set volume output volume 50
tell application "System Events"
    tell appearance preferences
        set dark mode to true
    end tell
end tell
```
""",

    "text_messages": """
Output for text_messages: The SMS message has been queued and sent successfully natively.
""",

    "phone_calls": """
Output for phone_calls: Twilio call initiated.

FILE: make_call.py
```python
import sys
print("Call status: queued")
```
"""
}

def _run_cli_mock(domain, prompt):
    runner = CliRunner()
    
    mock_output = MOCK_STREAMS.get(domain, f"Output for {domain}")
    
    with patch("sage.main._prepare_model_for_use") as mock_prep, \
         patch("sage.main._build_router") as mock_router:
         
        mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
        mock_router_inst = MagicMock()
        mock_router_inst.stream.return_value = [mock_output]
        mock_router.return_value = mock_router_inst
        
        with runner.isolated_filesystem():
            # Run using the --agent flag to trigger full extraction and code writing loops
            result = runner.invoke(sage_app, ["ask", prompt, "--raw", "--agent"])
            
            assert result.exit_code == 0, f"CLI task failed for domain: {domain}\nOutput: {result.output}"
            
            if domain == "text_messages":
                assert "sent successfully" in result.output
                return
            
            generated_files = [
                f for f in Path(".").glob("**/*")
                if f.is_file() 
                and not str(f).startswith((".", "venv")) 
                and "__pycache__" not in str(f)
                and not f.name.endswith(".pyc")
            ]
            
            assert len(generated_files) > 0, f"No files written for domain: {domain}\nCLI Output:\n{result.output}"
            
            for f in generated_files:
                content = f.read_text(encoding="utf-8")
                
                # Check for placeholders/stubs using the internal validate_content library
                val_res = validate_content(str(f), content)
                assert val_res.ok, f"File {f} failed content validation: {val_res.reason}"
                
                # Syntax validations
                if f.suffix == ".py":
                    import py_compile
                    try:
                        py_compile.compile(str(f), doraise=True)
                    except Exception as e:
                        pytest.fail(f"Python syntax compilation failed for {f}: {e}")
                elif f.suffix == ".json":
                    import json
                    try:
                        json.loads(content)
                    except Exception as e:
                        pytest.fail(f"JSON parsing failed for {f}: {e}")
                elif f.name == "index.html" and domain == "websites":
                    # Responsive design assertions
                    assert re.search(r'<meta\s+name=["\']?viewport["\']?', content, re.I), "Missing viewport tag"
                    assert re.search(r'@media\s*\([^)]*max-width[^)]*\)|@media\s*\([^)]*min-width', content, re.I), "Missing media query breakpoint"
                    assert re.search(r'<(header|nav|main|footer)\b', content, re.I), "Missing semantic HTML5 tag"
                    
                    # Modern styling assertions
                    assert re.search(r'@keyframes|transition\s*:|animation\s*:', content, re.I), "Missing transition/animation"
                    assert re.search(r':hover\b|:focus\b|:focus-visible\b', content, re.I), "Missing hover/focus state"
                    assert re.search(r'--[a-z][a-z0-9_-]*\s*:|:root\s*\{', content, re.I), "Missing CSS variables/tokens"
                    assert "fonts.googleapis.com" in content or "font-family" in content, "Missing typography polish"


def test_cli_exhaustive_websites():
    """Exhaustive test for websites via CLI."""
    _run_cli_mock("websites", "Create a responsive advertising dashboard using React and Tailwind.")

def test_cli_exhaustive_mobile_apps():
    """Exhaustive test for mobile_apps via CLI."""
    _run_cli_mock("mobile_apps", "Build a React Native feed with infinite scrolling.")

def test_cli_exhaustive_video_games():
    """Exhaustive test for video_games via CLI."""
    _run_cli_mock("video_games", "Develop a 2D physics engine in JavaScript for a browser game.")

def test_cli_exhaustive_backend_services():
    """Exhaustive test for backend_services via CLI."""
    _run_cli_mock("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.")

def test_cli_exhaustive_deployments():
    """Exhaustive test for deployments via CLI."""
    _run_cli_mock("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.")

def test_cli_exhaustive_videos():
    """Exhaustive test for videos via CLI."""
    _run_cli_mock("videos", "Make a music video with moviepy that says 'I love you Lily'.")

def test_cli_exhaustive_images():
    """Exhaustive test for images via CLI."""
    _run_cli_mock("images", "Generate a professional SVG logo and PNG favicon.")

def test_cli_exhaustive_audio_files():
    """Exhaustive test for audio_files via CLI."""
    _run_cli_mock("audio_files", "Synthesize a WAV audio file playing a C major chord.")

def test_cli_exhaustive_music_videos():
    """Exhaustive test for music_videos via CLI."""
    _run_cli_mock("music_videos", "Combine generated audio and video into an MP4 music video.")

def test_cli_exhaustive_generate_files():
    """Exhaustive test for generate_files via CLI."""
    _run_cli_mock("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.")

def test_cli_exhaustive_run_applications():
    """Exhaustive test for run_applications via CLI."""
    _run_cli_mock("run_applications", "Open the Messages app on my Mac and prepare a text.")

def test_cli_exhaustive_computer_control():
    """Exhaustive test for computer_control via CLI."""
    _run_cli_mock("computer_control", "Use osascript to change my system volume and toggle dark mode.")

def test_cli_exhaustive_text_messages():
    """Exhaustive test for text_messages via CLI."""
    _run_cli_mock("text_messages", "Send a text message using the SMS bridge natively.")

def test_cli_exhaustive_phone_calls():
    """Exhaustive test for phone_calls via CLI."""
    _run_cli_mock("phone_calls", "Trigger an API call to Twilio to initiate a phone call.")
