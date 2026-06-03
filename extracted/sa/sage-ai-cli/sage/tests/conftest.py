"""Shared pytest fixtures for sage/tests.

Provides a real local background completions server fixture to allow completely
pure functional integration testing of SAGE's capabilities and routing.
"""

from __future__ import annotations

import json
import os
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import contextlib
import tempfile
import shutil
import typer.testing

# Monkeypatch isolated_filesystem for typer.testing.CliRunner in newer Typer versions
@contextlib.contextmanager
def _isolated_filesystem(self, temp_dir=None):
    cwd = os.getcwd()
    t_dir = tempfile.mkdtemp(dir=temp_dir)
    os.chdir(t_dir)
    try:
        yield t_dir
    finally:
        os.chdir(cwd)
        try:
            shutil.rmtree(t_dir)
        except OSError:
            pass

typer.testing.CliRunner.isolated_filesystem = _isolated_filesystem

import pytest

# This file lives at <project_root>/sage/tests/conftest.py
_HERE = Path(__file__).resolve().parent          # .../sage/tests
_SAGE_MODULE = _HERE.parent                       # .../sage
_PROJECT_ROOT = _SAGE_MODULE.parent               # .../ai-platform



@pytest.fixture
def sage_project_root() -> Path:
    """The ai-platform/ directory — contains pyproject.toml, sage/, backend/."""
    return _PROJECT_ROOT


@pytest.fixture
def sage_module_root() -> Path:
    """The sage/ module directory — contains main.py, __init__.py, tests/."""
    return _SAGE_MODULE


@pytest.fixture
def sage_tests_dir() -> Path:
    """The sage/tests/ directory."""
    return _HERE


@pytest.fixture(autouse=True)
def reset_sage_global_state():
    """Reset global state variables in sage.main between every test to prevent cross-test leakage."""
    import sage.main as sage_main
    sage_main._global_agent = None
    sage_main._current_cwd = None
    sage_main._current_classification = None
    sage_main._force_implementation_mode = False
    yield
    sage_main._global_agent = None
    sage_main._current_cwd = None
    sage_main._current_classification = None
    sage_main._force_implementation_mode = False


class CompletionsHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress logging to stderr

    def _get_domain_from_prompt(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "react native feed" in prompt_lower or "infinite scroll" in prompt_lower or "react_native" in prompt_lower or "react-native" in prompt_lower or "flutter_bloc" in prompt_lower or "swiftui" in prompt_lower or "expo" in prompt_lower:
            return "mobile_apps"
        if (
            "react and tailwind" in prompt_lower
            or "advertising dashboard" in prompt_lower
            or "advertising-dashboard" in prompt_lower
            or "react_tailwind" in prompt_lower
            or "vue_pinia" in prompt_lower
            or "svelte_kanban" in prompt_lower
            or "vite" in prompt_lower
            or "react-vite" in prompt_lower
            or "tailwindcss" in prompt_lower
            or "tailwind" in prompt_lower
            or "react" in prompt_lower
        ):
            return "websites"
        if "2d physics" in prompt_lower or "physics engine" in prompt_lower or "phaser_arcade" in prompt_lower or "unity_controller" in prompt_lower or "godot_movement" in prompt_lower:
            return "video_games"
        if "fastapi backend" in prompt_lower or "backend service" in prompt_lower or "fastapi_redis" in prompt_lower or "express_postgres" in prompt_lower or "django_rest" in prompt_lower:
            return "backend_services"
        if "terraform" in prompt_lower or "iac" in prompt_lower:
            return "deployments"
        if "combine" in prompt_lower and "music video" in prompt_lower:
            return "music_videos"
        if "moviepy" in prompt_lower or "music video" in prompt_lower:
            return "videos"
        if "svg logo" in prompt_lower or "favicon" in prompt_lower:
            return "images"
        if "wav audio" in prompt_lower:
            return "audio_files"
        if "complex python script" in prompt_lower:
            return "generate_files"
        if "messages app" in prompt_lower:
            return "run_applications"
        if "system volume" in prompt_lower:
            return "computer_control"
        if "sms bridge natively" in prompt_lower:
            return "text_messages"
        if "twilio" in prompt_lower:
            return "phone_calls"
        return "generate_files"


    def _get_expected_filename(self, domain: str) -> str:
        mapping = {
            "websites": "frontend/index.html",
            "mobile_apps": "frontend/ItemListScreen.tsx",
            "video_games": "frontend/physics.js",
            "backend_services": "backend/main.py",
            "deployments": "deploy/main.tf",
            "videos": "generated_media.mp4",
            "images": "logo.svg",
            "audio_files": "generated_media.mp4",
            "music_videos": "generated_media.mp4",
            "generate_files": "script.py",
            "run_applications": "run.scpt",
            "computer_control": "control.scpt",
            "text_messages": "sms_log.txt",
            "phone_calls": "make_call.py"
        }
        return mapping.get(domain, "file.py")

    def _get_file_content(self, domain: str) -> str:
        if domain == "websites":
            return """<!DOCTYPE html>
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
        body {
            font-family: var(--font-stack);
            background-color: var(--dark);
            color: #ffffff;
            transition: all 0.2s ease;
        }
        .btn:hover { opacity: 0.9; }
        .btn:focus-visible { outline: 2px solid var(--primary); }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .animate-fade { animation: fadeIn 0.5s ease-out; }
        @media (max-width: 640px) { .desktop-only { display: none; } }
    </style>
</head>
<body>
    <header><nav aria-label="Main Navigation"><a href="/" class="btn" aria-label="Home">Home</a></nav></header>
    <main class="animate-fade"><h1>Dashboard</h1></main>
    <footer><p>&copy; 2026 Dashboard Inc.</p></footer>
</body>
</html>"""
        elif domain == "mobile_apps":
            return """import React, { useState } from 'react';
import { SafeAreaView, FlatList, Text, View, StyleSheet } from 'react-native';
export const ItemListScreen: React.FC = () => {
    const [items] = useState<string[]>(['Initial Item']);
    return (
        <SafeAreaView style={styles.container}>
            <FlatList data={items} renderItem={({ item }) => <View><Text>{item}</Text></View>} />
        </SafeAreaView>
    );
};
const styles = StyleSheet.create({ container: { flex: 1 } });"""
        elif domain == "video_games":
            return """class Vector2D {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
}"""
        elif domain == "backend_services":
            return """from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root(): return {"status": "healthy"}"""
        elif domain == "deployments":
            return """provider "aws" { region = "us-east-1" }"""
        elif domain == "videos":
            return "fake mp4 video content"
        elif domain == "images":
            return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <rect width="100" height="100" fill="#3b82f6" rx="10"/>
</svg>"""
        elif domain == "audio_files":
            return "fake wav audio content"
        elif domain == "music_videos":
            return "fake music video content"
        elif domain == "run_applications":
            return """tell application "Messages" to activate"""
        elif domain == "computer_control":
            return """set volume output volume 50"""
        elif domain == "phone_calls":
            return """import sys\nprint("Call status: queued")"""
        return "pass"

    def _get_content_for_ext(self, ext: str) -> str:
        ext_lower = ext.lower()
        if ext_lower in ("py", "pyw"):
            return 'import sys\n\ndef test_dummy():\n    assert True\n\ndef main():\n    print("Hello")\n\nif __name__ == "__main__":\n    main()'
        elif ext_lower in ("js", "mjs"):
            return 'function greet() {\n    console.log("Hello");\n}\ngreet();'
        elif ext_lower in ("ts", "mts"):
            return 'function greet(name: string): void {\n    console.log("Hello, " + name);\n}\ngreet("World");'
        elif ext_lower in ("jsx", "tsx"):
            return 'import React from "react";\n\nexport default function App() {\n    return <div>Hello</div>;\n}'
        elif ext_lower in ("c", "h"):
            return '#include <stdio.h>\n\nint main() {\n    printf("Hello\\n");\n    return 0;\n}'
        elif ext_lower in ("cpp", "hpp"):
            return '#include <iostream>\n\nint main() {\n    std::cout << "Hello" << std::endl;\n    return 0;\n}'
        elif ext_lower in ("kt", "scala"):
            return 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello");\n    }\n}'
        elif ext_lower == "java":
            return 'class test_file {\n    public static void main(String[] args) {\n        System.out.println("Hello");\n    }\n}'
        elif ext_lower == "swift":
            return 'import Foundation\n\nfunc main() {\n    print("Hello")\n}\nmain()'
        elif ext_lower == "go":
            return 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello")\n}'
        elif ext_lower == "rs":
            return 'fn main() {\n    println!("Hello");\n}'
        elif ext_lower == "cs":
            return 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello");\n    }\n}'
        elif ext_lower == "php":
            return '<?php\n\nfunction main() {\n    echo "Hello";\n}\nmain();'
        elif ext_lower == "rb":
            return 'def main\n  puts "Hello"\nend\n\nmain'
        elif ext_lower == "pl":
            return 'use strict;\nuse warnings;\n\nprint "Hello\\n";'
        elif ext_lower == "sh":
            return '#!/bin/bash\n\necho "Hello"\nexit 0'
        elif ext_lower == "bat":
            return '@echo off\necho Hello\npause'
        elif ext_lower == "ps1":
            return 'Write-Host "Hello"\nexit 0'
        elif ext_lower == "gd":
            return 'extends Node\n\nfunc _ready():\n    print("Hello")'
        elif ext_lower == "dart":
            return 'void main() {\n  print("Hello");\n}'
        elif ext_lower == "lua":
            return 'function main()\n    print("Hello")\nend\nmain()'
        elif ext_lower == "r":
            return 'main <- function() {\n  print("Hello")\n}\nmain()'
        elif ext_lower == "hs":
            return 'main :: IO ()\nmain = putStrLn "Hello"'
        elif ext_lower in ("erl", "ex", "exs", "hrl"):
            return 'defmodule Main do\n  def main do\n    IO.puts "Hello"\n  end\nend'
        elif ext_lower in ("fs", "fsi"):
            return 'module Main\nlet main() = printfn "Hello"\nmain()'
        elif ext_lower == "cr":
            return 'def main\n  puts "Hello"\nend\nmain'
        elif ext_lower in ("groovy", "gvy"):
            return 'class Main {\n    static void main(String[] args) {\n        println "Hello"\n    }\n}'
        elif ext_lower == "sql":
            return 'SELECT * FROM users WHERE id = 1;'
        elif ext_lower == "sol":
            return '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\ncontract HelloWorld {\n    string public message = "Hello";\n}'
        elif ext_lower == "zig":
            return 'const std = @import("std");\npub fn main() !void {\n    std.debug.print("Hello\\n", .{});\n}'
        elif ext_lower == "nim":
            return 'echo "Hello"'
        elif ext_lower == "d":
            return 'import std.stdio;\nvoid main() {\n    writeln("Hello");\n}'
        elif ext_lower == "pas":
            return 'program Hello;\nbegin\n  writeln(\'Hello\');\nend.'
        elif ext_lower == "elm":
            return 'module Main exposing (main)\nimport Html exposing (text)\nmain = text "Hello"'
        elif ext_lower == "vue":
            return '<template>\n  <div>Hello</div>\n</template>\n<script>\nexport default {}\n</script>'
        elif ext_lower == "svelte":
            return '<script>\n</script>\n<h1>Hello</h1>'
        elif ext_lower == "xml":
            return '<?xml version="1.0" encoding="UTF-8"?>\n<note>\n  <to>Tove</to>\n</note>'
        elif ext_lower == "tex":
            return '\\documentclass{article}\n\\begin{document}\nHello\n\\end{document}'
        elif ext_lower == "toml":
            return '[package]\nname = "hello"\nversion = "0.1.0"'
        elif ext_lower == "ini":
            return '[owner]\nname=John Doe\n'
        elif ext_lower == "csv":
            return 'name,email\nJohn,john@example.com\n'
        elif ext_lower in ("dockerfile", "docker"):
            return 'FROM alpine\nCMD ["echo", "Hello"]'
        elif ext_lower == "json":
            return '{\n  "status": "ok"\n}'
        elif ext_lower in ("yaml", "yml"):
            return 'status: ok\nenabled: true'
        elif ext_lower == "html":
            return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Test</title><style>:root { --primary: #3b82f6; } body { font-family: sans-serif; transition: all 0.2s; }</style></head><body><header><nav aria-label="Main Navigation"><a href="/" class="btn" aria-label="Home">Home</a></nav></header><h1>Test</h1></body></html>'
        elif ext_lower == "css":
            return 'body {\n  color: #333333;\n  background-color: #ffffff;\n}'
        elif ext_lower == "md":
            return '# Test\n\nThis is a test document.'
        elif ext_lower == "svg":
            return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n  <rect width="100" height="100" fill="#3b82f6" rx="10"/>\n</svg>'
        return 'import sys\nprint("Hello")'

    def _get_task_response(self, task_id: str) -> tuple[str, str]:
        task_id = task_id.upper().strip()
        # 1. PROGRAMMING LANGUAGES (Core Language-Only Challenges)
        if task_id == "PY-001":
            return "pipeline.py", """import sys
import json
from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    name: str
    email: str

def run_pipeline():
    data = {"id": 1, "name": "Lily", "email": "lily@example.com"}
    user = UserSchema(**data)
    report = {"status": "success", "user": user.model_dump()}
    print(json.dumps(report))

if __name__ == "__main__":
    run_pipeline()
"""
        elif task_id == "JS-002":
            return "server.js", """const http = require('http');
const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: "ok", service: "CQRS" }));
});
server.listen(0);
"""
        elif task_id == "JAVA-003":
            return "LockFreeMap.java", """import java.util.concurrent.atomic.AtomicReferenceArray;

public class LockFreeMap<K, V> {
    private final AtomicReferenceArray<V> array = new AtomicReferenceArray<>(1024);
    public void put(int key, V value) {
        array.set(key % 1024, value);
    }
    public V get(int key) {
        return array.get(key % 1024);
    }
}
"""
        elif task_id == "GO-004":
            return "main.go", """package main
import (
	"fmt"
	"net/http"
)
func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello from HTTP/2 Server")
	})
	fmt.Println("gRPC/REST server ready")
}
"""
        elif task_id == "RS-005":
            return "lib.rs", """#![no_std]
pub struct Tmp102 {
    pub addr: u8,
}
impl Tmp102 {
    pub fn read_temp(&self) -> i32 {
        22
    }
}
"""
        elif task_id == "CPP-006":
            return "main.cpp", """#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> data = {5, 2, 8, 1, 9};
    std::sort(data.begin(), data.end());
    std::cout << "Sorted: " << data[0] << std::endl;
    return 0;
}
"""
        elif task_id == "TS-007":
            return "parser.ts", """export type Eval<S extends string> = S extends "2+3*4" ? 14 : number;
export function evaluate(expr: string): number {
    return 14;
}
"""
        elif task_id == "PHP-008":
            return "middleware.php", """<?php
class RateLimiter {
    public function limit($key) {
        return true;
    }
}
"""
        elif task_id == "RUB-009":
            return "tenant_migrator.rb", """class TenantMigrator
  def migrate(tenant_id)
    puts "Migrating tenant: #{tenant_id}"
    true
  end
end
"""
        elif task_id == "SWIFT-010":
            return "NetworkService.swift", """import Foundation
public class NetworkService {
    public func fetchItems() -> [String] {
        return ["Swift Item 1", "Swift Item 2"]
    }
}
"""
        elif task_id == "CRYSTAL-011":
            return "fiber_pool.cr", """class FiberPool
  def initialize(@size : Int32)
  end
  def run
    puts "Fiber pool running with size: #{@size}"
  end
end
"""
        # 2.1 Backend Frameworks
        elif task_id == "PY-FLK-01":
            return "app.py", """from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/projects")
def get_projects():
    return jsonify([{"id": 1, "name": "Flask project"}])
if __name__ == "__main__":
    app.run(port=0)
"""
        elif task_id == "PY-DJ-02":
            return "consumers.py", """import json
class ChatConsumer:
    def receive(self, text_data):
        return json.dumps({"message": "Hello from Django Channels"})
"""
        elif task_id == "JS-EXP-03":
            return "auth.js", """const express = require('express');
const app = express();
app.get('/.well-known/openid-configuration', (req, res) => {
    res.json({ issuer: "https://localhost", authorization_endpoint: "/oauth/auth" });
});
"""
        elif task_id == "JS-NXT-04":
            return "order.service.ts", """export class OrderService {
    validateOrder(orderId: string): boolean {
        return orderId.length > 0;
    }
}
"""
        elif task_id == "JAVA-SPR-05":
            return "MetricsController.java", """import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
@RestController
public class MetricsController {
    @GetMapping("/actuator/metrics")
    public String getMetrics() {
        return "{\\"metrics\\": []}";
    }
}
"""
        elif task_id == "GO-GIN-06":
            return "main.go", """package main
import "github.com/gin-gonic/gin"
func main() {
    r := gin.New()
    r.GET("/traces", func(c *gin.Context) {
        c.JSON(200, gin.H{"status": "traces exported"})
    })
}
"""
        elif task_id == "RS-ACT-07":
            return "main.rs", """use actix_web::{get, Responder, HttpResponse};
#[get("/shorten")]
async fn shorten() -> impl Responder {
    HttpResponse::Ok().body("URL Shortener")
}
"""
        elif task_id == "CPP-POCO-08":
            return "main.cpp", """#include <iostream>
int main() {
    std::cout << "Multipart POCO File Upload ready" << std::endl;
    return 0;
}
"""
        elif task_id == "PHP-LAR-09":
            return "WizardController.php", """<?php
class WizardController {
    public function saveStep() {
        return ["status" => "step saved"];
    }
}
"""
        elif task_id == "RUB-RAI-10":
            return "collab_channel.rb", """class CollabChannel
  def subscribed
    puts "Subscribed to collaborate channel"
  end
end
"""
        # 2.2 Frontend Frameworks
        elif task_id == "TS-REACT-01":
            return "Dashboard.tsx", """import React from 'react';
export default function Dashboard() {
    return <div>React Metrics Dashboard</div>;
}
"""
        elif task_id == "TS-NG-02":
            return "kanban.component.ts", """import { Component } from '@angular/core';
@Component({
  selector: 'app-kanban',
  template: '<div>Angular Kanban Board</div>'
})
export class KanbanComponent {
  title: string = 'Kanban Board';
}
"""
        elif task_id == "JS-VUE-03":
            return "taskStore.js", """export const useTaskStore = {
    state: () => ({ tasks: [] }),
    actions: {
        addTask(task) { return task; }
    }
};
"""
        elif task_id == "DART-FLUT-04":
            return "notes_screen.dart", """class NotesScreen {
  void render() {
    print("Notes screen rendered");
  }
}
"""
        elif task_id == "KOT-COM-05":
            return "BudgetTracker.kt", """class BudgetTracker {
    fun track() {
        println("Compose Multiplatform budget tracker")
    }
}
"""
        elif task_id == "SWIFT-UI-06":
            return "MenuBarApp.swift", """import SwiftUI
struct MenuBarApp: View {
    var body: some View {
        Text("SwiftUI MenuBar Monitoring App")
    }
}
"""
        # 3. Mobile, Game & Other Platforms
        elif task_id == "ANDROID-01":
            return "BeaconScanner.kt", """class BeaconScanner {
    fun startScan() {
        println("Discovering BLE beacons")
    }
}
"""
        elif task_id == "IOS-02":
            return "ARManager.swift", """public class ARManager {
    public func placeFurniture() {
        print("Placing furniture via ARKit")
    }
}
"""
        elif task_id == "REACT-N-03":
            return "VideoPlayer.tsx", """import React from 'react';
export default function VideoPlayer() {
    return <div>HLS Video Player</div>;
}
"""
        elif task_id == "FLUT-04":
            return "game_screen.dart", """class GameScreen {
  void start() {
    print("TicTacToe multiplayer screen");
  }
}
"""
        elif task_id == "UNITY-05":
            return "PuzzleInteraction.cs", """using UnityEngine;
public class PuzzleInteraction : MonoBehaviour {
    void Update() {}
}
"""
        elif task_id == "UNREAL-06":
            return "AbilitySystem.cpp", """#include <iostream>
void AbilitySystemInit() {
    std::cout << "Unreal ability system initialized" << std::endl;
}
"""
        elif task_id == "GODOT-07":
            return "level_generator.gd", """extends Node
func generate_level():
    print("Generating cellular automata Godot level")
"""
        elif task_id == "XNA-08":
            return "ECSSystem.cs", """public class ECSSystem {
    public void Update() {}
}
"""
        elif task_id == "HTML5-09":
            return "App.svelte", """<main>
  <h1>Double Pendulum Simulation</h1>
</main>
"""
        elif task_id == "VR-10":
            return "VRDrawing.cs", """using UnityEngine;
public class VRDrawing : MonoBehaviour {
    public void DrawStroke() {}
}
"""
        # 4. File Extensions & Asset-Creation Pipelines
        elif task_id == "IMG-01":
            return "generate_sprites.py", """from PIL import Image
def generate_sprites():
    img = Image.new("RGB", (64, 64), color="red")
    img.save("sprites.png")
    print("Sprite sheet generated")
    return True

if __name__ == "__main__":
    generate_sprites()
"""
        elif task_id == "IMG-02":
            return "generate_logo.js", """const fs = require('fs');
const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:1" />
            <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
        </linearGradient>
    </defs>
    <circle cx="50" cy="50" r="40" fill="url(#grad)" />
</svg>`;
fs.writeFileSync('logo.svg', svgContent);
console.log("Vector SVG logo with gradient generated successfully.");
"""
        elif task_id == "AUD-01":
            return "generate_audio.py", """import numpy as np
import wave

sample_rate = 44100
t = np.linspace(0, 1, sample_rate, endpoint=False)
data = np.sin(2 * np.pi * 60 * t) * np.exp(-10 * t)
audio_bytes = (data * 32767).astype(np.int16).tobytes()

with wave.open('drum_loop.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sample_rate)
    w.writeframes(audio_bytes)
print("Procedural wav drum loop generated successfully.")
"""
        elif task_id == "AUD-02":
            return "synthesize.py", """import wave
import struct

def synthesize_narration():
    print("Sending TTS API request for narration...")
    with wave.open("narration.mp3", "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        for i in range(8000):
            data = struct.pack('<h', int(16384 * 0.5))
            w.writeframesraw(data)
    print("Voiceover narration MP3 synthesized successfully.")

if __name__ == "__main__":
    synthesize_narration()
"""
        elif task_id == "VID-01":
            return "generate_intro.py", """from moviepy.editor import ColorClip

def build_animated_intro():
    print("Creating animated intro scenes...")
    clip = ColorClip(size=(64, 64), color=(255, 0, 0), duration=1)
    clip.write_videofile("intro.mp4", fps=10, logger=None)
    print("Animated intro MP4 created successfully.")

if __name__ == "__main__":
    build_animated_intro()
"""
        elif task_id == "MODEL-01":
            return "blend_rig.py", """import sys

def rig_humanoid():
    print("Initializing Blender Python API context...")
    with open("character.fbx", "w") as f:
        f.write("FBX Header\\nVersion: 7400\\n")
    print("Humanoid 3D character rig exported to FBX successfully.")

if __name__ == "__main__":
    rig_humanoid()
"""
        elif task_id == "MODEL-02":
            return "build_scene.js", """const fs = require('fs');

function exportThreeJSScene() {
    console.log("Building Three.js scene with a sun light source...");
    const glbHeader = Buffer.from([0x67, 0x6C, 0x54, 0x46, 0x02, 0x00, 0x00, 0x00]);
    fs.writeFileSync('scene.glb', glbHeader);
    console.log("Three.js sun scene GLB exporter execution finished successfully.");
}
exportThreeJSScene();
"""
        elif task_id == "DOC-01":
            return "README.md", """# Project Documentation
- Task ID: DOC-01
- Purpose: Generate README.md
"""
        elif task_id == "DOC-02":
            return "spec.tex", """\\\\documentclass{article}
\\\\begin{document}
Technical Specification for OAuth2 Server
\\\\end{document}
"""
        elif task_id == "DATA-01":
            return "schema.json", """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RateLimiterConfig",
  "type": "object",
  "properties": {
    "limit": { "type": "integer" }
  }
}
"""
        elif task_id == "DATA-02":
            return "generate_data.py", """def generate_data():
    print("10M rows user data CSV dataset created")
    return True

if __name__ == "__main__":
    generate_data()
"""
        return "file.py", 'def main():\n    print("Hello default")\n\nif __name__ == "__main__":\n    main()'

    def do_GET(self):
        if self.path.endswith("/models"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            models_response = {
                "data": [
                    {
                        "id": "meta-llama/llama-3.3-70b-instruct:free",
                        "name": "Meta: Llama 3.3 70B Instruct (Free)",
                        "description": "Meta Llama 3.3 70B Instruct model",
                        "pricing": {
                            "prompt": "0.0",
                            "completion": "0.0"
                        }
                    }
                ]
            }
            self.wfile.write(json.dumps(models_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))

        messages = payload.get("messages", [])
        last_msg = messages[-1]["content"] if messages else ""
        last_msg_lower = last_msg.lower()

        filtered_contents = []
        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "")
            if role == "system":
                continue
            content_lower = content.lower()
            if "you are working on the project rooted" in content_lower or "project scan complete" in content_lower:
                continue
            if "i've scanned the project" in content_lower or "i have scanned the project" in content_lower:
                continue
            filtered_contents.append(content)
        
        filtered_history = "\n".join(filtered_contents).lower()

        # Parse requested extension if any (only looking at actual user messages to avoid matching simulated assistant output)
        import re
        user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
        user_history = "\n".join(user_msgs).lower()
        requested_ext = None

        # Parse requested extension if any (only looking at actual user messages to avoid matching simulated assistant output)
        import re
        user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
        user_history = "\n".join(user_msgs).lower()
        requested_ext = None

        if "extension" in user_history:
            ext_match = re.search(r'\.([a-zA-Z0-9]+)\s+extension', user_history)
            if ext_match:
                requested_ext = ext_match.group(1).lower()
            else:
                ext_match = re.search(r'extension\s+([a-zA-Z0-9]+)', user_history)
                if ext_match:
                    requested_ext = ext_match.group(1).lower()
                else:
                    ext_match = re.search(r'for\s+([a-zA-Z0-9]+)\s+extension', user_history)
                    if ext_match:
                        requested_ext = ext_match.group(1).lower()

        # Extract requested path if any
        requested_path = None
        for msg in reversed(messages):
            content = msg.get("content", "")
            path_match = re.search(r"Path:\s*`([^`]+)`", content)
            if path_match:
                requested_path = path_match.group(1)
                break

        # Check if the prompt/history mentions a task ID (e.g. PY-001, PY-FLK-01)
        task_match = re.search(r'\b([A-Z]+-[A-Z0-9]+-[0-9]+|[A-Z]+-[0-9]+)\b', filtered_history, re.IGNORECASE)
        task_id = task_match.group(1).upper() if task_match else None
        if task_id:
            prefix = task_id.split("-")[0].upper()
            known_prefixes = {
                "PY", "JS", "JAVA", "GO", "RS", "CPP", "TS", "PHP", "RUB", "SWIFT", "CRYSTAL",
                "KOT", "DART", "ANDROID", "IOS", "REACT", "FLUT", "UNITY", "UNREAL", "GODOT",
                "XNA", "HTML5", "VR", "IMG", "AUD", "VID", "MODEL", "DOC", "DATA", "LARGE", "EXTREME",
                "FS", "SQL", "ZIG", "NIM", "D", "PAS", "ELM", "VUE", "SVELTE", "XML", "TEX", "TOML",
                "INI", "CSV", "DOCKER"
            }
            if prefix not in known_prefixes:
                task_id = None

        use_task_response = False
        if task_id:
            # Check if this is a game decomposition prompt (requesting JSON game plan)
            is_game_decomp = (
                "extract the spec" in filtered_history
                or "detected genre" in filtered_history
                or "detected perspective" in filtered_history
                or "output json with these keys" in filtered_history
            )
            if is_game_decomp:
                use_task_response = False
            else:
                task_filename, task_file_content = self._get_task_response(task_id)
                task_ext = task_filename.split(".")[-1].lower()
                if not requested_path:
                    use_task_response = True
                else:
                    req_basename = os.path.basename(requested_path).lower()
                    req_ext = req_basename.split(".")[-1].lower() if "." in req_basename else ""
                    is_test_file = "test" in req_basename or "spec" in req_basename
                    if is_test_file:
                        use_task_response = False
                    elif req_basename == task_filename.lower():
                        use_task_response = True
                    elif req_ext == task_ext:
                        is_build_request = (
                            "build a " in filtered_history
                            or "fastapi backend for:" in filtered_history
                            or "nextjs app for:" in filtered_history
                            or "spring-boot java" in filtered_history
                            or "go-microservices app" in filtered_history
                            or "rust-axum backend" in filtered_history
                            or "cpp microservice" in filtered_history
                            or "laravel php api" in filtered_history
                            or "rails ruby on rails" in filtered_history
                            or "ios-swift app" in filtered_history
                        )
                        if is_build_request:
                            use_task_response = (req_basename == task_filename.lower())
                        else:
                            use_task_response = True
                    elif task_id in ("LARGE-001", "EXTREME-002"):
                        use_task_response = True


        if use_task_response:
            filename = os.path.basename(requested_path) if requested_path else task_filename
            file_content = task_file_content
            domain = "task_generation"
        elif "extract the spec" in filtered_history or "detected genre" in filtered_history:
            filename = "game_plan.json"
            game_desc = "A game demonstrating 2D physics concepts in a browser."
            if task_id:
                game_desc = f"Game implementation for {task_id}"
            file_content = json.dumps({
                "title": "2D Physics Game",
                "description": game_desc,
                "features": ["Rigid body collision", "Gravity simulation", "User interaction"],
                "sprites": [
                    {"role": "ball", "prompt": "a red bouncing ball"},
                    {"role": "box", "prompt": "a wooden box crate"}
                ],
                "meshes": [],
                "audio": [
                    {"role": "bounce", "prompt": "a clean bounce sound effect", "kind": "sfx"},
                    {"role": "music", "prompt": "retro 8-bit chip tunes background music", "kind": "music"}
                ]
            }, indent=2)
            domain = "game_decomposition"
        elif "gdscript" in filtered_history or "godot 4 gdscript" in filtered_history or "main.gd" in filtered_history:
            filename = "scripts"
            file_content = """Here is the implementation.

```Main.gd
extends Node2D
func _ready():
    print("Main screen ready")
```

```Player.gd
extends CharacterBody2D
func _physics_process(delta):
    pass
```
"""
            domain = "game_scripts"
        elif requested_path:
            filename = requested_path
            basename = os.path.basename(requested_path)
            ext = basename.split(".")[-1].lower() if "." in basename else ""
            
            is_test_file = "test" in basename.lower() or "spec" in basename.lower()
            if is_test_file:
                if ext == "py":
                    file_content = 'import sys\n\ndef test_system_properties():\n    assert sys.platform in ("darwin", "linux", "win32")\n    assert sys.version_info.major == 3\n'
                elif ext in ("js", "ts", "jsx", "tsx"):
                    stack_match = re.search(r"## stack\s+([a-z0-9_+-]+)", filtered_history)
                    stack_name = stack_match.group(1) if stack_match else ""
                    is_react_native = "react-native" in stack_name or "expo" in stack_name
                    if requested_path:
                        req_path_lower = requested_path.replace("\\", "/").lower()
                        if "/src/" in req_path_lower:
                            is_react_native = False
                        elif "/app/" in req_path_lower or "app.json" in req_path_lower or "metro.config" in req_path_lower:
                            is_react_native = True
                    if is_react_native:
                        file_content = 'test("runtime platform verification", () => {\n    expect(1 + 1).toBe(2);\n});'
                    else:
                        file_content = 'import { test, expect } from "vitest";\ntest("runtime platform verification", () => {\n    expect(process.platform).toBeDefined();\n    expect(typeof process.nextTick).toBe("function");\n});'
                elif ext == "go":
                    file_content = 'package main\nimport "testing"\nimport "runtime"\nfunc TestRuntimeEnvironment(t *testing.T) {\n    if runtime.GOOS == "" {\n        t.Error("Unknown GOOS")\n    }\n}'
                elif ext == "rs":
                    file_content = '#[test]\nfn test_rust_runtime() {\n    assert!(core::any::type_name::<i32>() == "i32");\n}'
                elif ext in ("cpp", "cc"):
                    file_content = '#include <cassert>\n#include <string>\nint main() {\n    std::string s = "valid";\n    assert(!s.empty());\n    return 0;\n}'
                elif ext in ("java", "kt"):
                    file_content = 'public class TestClass {\n    @org.junit.Test\n    public void testJavaRuntime() {\n        assert System.getProperty("java.version") != null;\n    }\n}'
                elif ext == "swift":
                    file_content = 'import XCTest\nclass MyTests: XCTestCase {\n    func testSwiftRuntime() {\n        XCTAssertNotNil(ProcessInfo.processInfo.arguments)\n    }\n}'
                elif ext == "dart":
                    file_content = 'import "package:test/test.dart";\nimport "dart:io";\nvoid main() {\n  test("dart platform", () {\n    expect(Platform.version, isNotNull);\n  });\n}'
                elif ext == "cs":
                    file_content = 'using Xunit;\nusing System;\npublic class TestClass {\n    [Fact]\n    public void TestDotNetRuntime() {\n        Assert.NotNull(Environment.Version);\n    }\n}'
                elif ext == "gd":
                    file_content = 'extends Node2D\nfunc test_pass():\n    var node = Node2D.new()\n    assert(node != null)'
                else:
                    file_content = 'import sys\nprint("system platform:", sys.platform)'
            elif basename.lower() == "dockerfile":
                file_content = 'FROM alpine\nCMD ["echo", "Hello"]\n'
            elif basename == "app.json":
                file_content = '{\n  "expo": {\n    "name": "App",\n    "slug": "app",\n    "version": "1.0.0",\n    "sdkVersion": "51.0.0"\n  }\n}'
            elif basename == ".gitignore":
                file_content = ".sage/\nnode_modules/\nvenv/\n__pycache__/\n*.pyc\n.pytest_cache/\n"
            elif basename == "tsconfig.json":
                file_content = '{\n  "compilerOptions": {\n    "target": "esnext",\n    "module": "commonjs",\n    "strict": true,\n    "esModuleInterop": true,\n    "skipLibCheck": true,\n    "forceConsistentCasingInFileNames": true,\n    "jsx": "react-jsx"\n  }\n}'
            elif basename == "docker-compose.yml":
                file_content = "version: '3.8'\nservices:\n  db:\n    image: postgres:15\n    environment:\n      POSTGRES_DB: app\n      POSTGRES_USER: postgres\n      POSTGRES_PASSWORD: password\n    ports:\n      - '5432:5432'\n"
            elif basename == "ci.yml":
                file_content = 'name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v2\n      - name: Run tests\n        run: echo "Tests passed"\n'
            elif basename in ("README.md", "README"):
                file_content = "# Project\nThis is a production-ready application built with SAGE.\n"
            elif basename == "alembic.ini":
                file_content = "[alembic]\nscript_location = alembic\nsqlalchemy.url = ${DATABASE_URL}\n"
            elif basename == "script.py.mako":
                file_content = '"""${message}\nRevision ID: ${up_revision}\nRevises: ${down_revision}\n"""\ndef upgrade():\n    pass\ndef downgrade():\n    pass\n'
            elif basename == ".env.example":
                file_content = "DATABASE_URL=postgresql://postgres:password@localhost:5432/app\nREDIS_URL=redis://localhost:6379/0\n"
            elif basename == "__init__.py":
                file_content = "# Package marker\n"
            elif basename == ".gitkeep":
                file_content = "# Keep directory\n"
            elif basename == "auth.js":
                file_content = "import { initializeApp } from 'firebase/app';\nconst app = initializeApp({ apiKey: 'fake-api-key' });\nexport default app;\n"
            elif basename == "AuthContext.jsx":
                file_content = "import React, { createContext } from 'react';\nexport const AuthContext = createContext(null);\nexport const AuthProvider = ({ children }) => {\n    return <AuthContext.Provider value={{user: null}}>{children}</AuthContext.Provider>;\n};\n"
            elif basename in ("firebaseEnv.js", "firebaseEnv.ts"):
                file_content = "export const firebaseConfig = { apiKey: 'fake' };\n"
            elif basename in ("index.js", "index.ts") and requested_path and "firebase" in requested_path.lower():
                file_content = "export { default } from './auth';\n"
            elif basename == "babel.config.js":
                file_content = "module.exports = function(api) {\n  api.cache(true);\n  return {\n    presets: ['babel-preset-expo'],\n  };\n};\n"
            elif basename == "metro.config.js":
                file_content = "const { getDefaultConfig } = require('expo/metro-config');\nconst config = getDefaultConfig(__dirname);\nmodule.exports = config;\n"
            elif basename == "jest.config.js":
                file_content = "module.exports = {\n  preset: 'jest-expo',\n  transformIgnorePatterns: [\n    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)',\n  ],\n};\n"
            elif basename.lower() == "index.html":
                file_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Advertising Dashboard</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>"""
            elif ext == "json":
                file_content = '{\n  "status": "ok"\n}'
            elif ext in ("yaml", "yml"):
                file_content = 'status: ok\nenabled: true'
            elif ext in ("py", "pyw"):
                file_content = 'import sys\n\ndef main():\n    print("Hello")\n\nif __name__ == "__main__":\n    main()'
            elif ext in ("js", "mjs"):
                file_content = 'function greet() {\n    console.log("Hello");\n}\ngreet();'
            elif ext in ("ts", "mts"):
                file_content = 'export function greet(name: string): void {\n    console.log("Hello, " + name);\n}\ngreet("World");'
            elif ext in ("jsx", "tsx"):
                stack_match = re.search(r"## stack\s+([a-z0-9_+-]+)", filtered_history)
                stack_name = stack_match.group(1) if stack_match else ""
                is_rn = "react-native" in stack_name or "expo" in stack_name
                if requested_path:
                    req_path_lower = requested_path.replace("\\", "/").lower()
                    if "/app/" in req_path_lower or "app.json" in req_path_lower or "metro.config" in req_path_lower:
                        is_rn = True
                if is_rn:
                    file_content = """import React, { useState } from 'react';
import { SafeAreaView, FlatList, Text, View, StyleSheet } from 'react-native';
export const ItemListScreen: React.FC = () => {
    const [items] = useState<string[]>(['Initial Item']);
    return (
        <SafeAreaView style={styles.container}>
            <FlatList data={items} renderItem={({ item }) => <View><Text>{item}</Text></View>} />
        </SafeAreaView>
    );
};
const styles = StyleSheet.create({ container: { flex: 1 } });"""
                else:
                    file_content = 'import React from "react";\n\nexport default function App() {\n    return <div>Hello</div>;\n}'
            else:
                file_content = self._get_content_for_ext(ext)
            domain = "path_generation"
        elif requested_ext and len(requested_ext) <= 10:
            domain = "generate_files"
            filename = f"test_file.{requested_ext}"
            file_content = self._get_content_for_ext(requested_ext)
        else:
            domain = self._get_domain_from_prompt(filtered_history)
            filename = self._get_expected_filename(domain)
            file_content = self._get_file_content(domain)

            # Customize framework file details if relevant
            if "express_postgres" in filtered_history:
                filename = "index.js"
                file_content = 'const express = require("express");\nconst app = express();\napp.get("/", (req, res) => res.json({status: "healthy"}));\napp.listen(3000);'
            elif "swiftui" in filtered_history:
                filename = "ContentView.swift"
                file_content = "import SwiftUI\nstruct ContentView: View {\n    var body: some View {\n        Text(\"Hello SwiftUI\")\n    }\n}"
            elif "flutter_bloc" in filtered_history:
                filename = "main.dart"
                file_content = "import 'package:flutter/material.dart';\nvoid main() => runApp(MaterialApp(home: Scaffold(body: Center(child: Text('Hello Flutter')))));"
            elif "unity_controller" in filtered_history or "playercontroller.cs" in filtered_history or "writing unity c#" in filtered_history:
                domain = "task_generation"
                filename = "PlayerController.cs"
                file_content = "using UnityEngine;\npublic class PlayerController : MonoBehaviour {\n    void Update() {}\n}"
            elif "godot_movement" in filtered_history:
                filename = "player_movement.gd"
                file_content = "extends CharacterBody2D\nfunc _physics_process(delta):\n    pass"

        is_direct_chat = len(messages) <= 1 or not any(msg.get("role") == "system" for msg in messages)
        is_planning = False
        if not is_direct_chat:
            if (
                "file_manifest" in last_msg_lower
                or "output a file_manifest" in last_msg_lower
                or "concrete implementation steps" in last_msg_lower
                or "brief analysis plan" in last_msg_lower
                or "steps to resolve" in last_msg_lower
                or "break this into" in last_msg_lower
                or "planning" in last_msg_lower
            ):
                is_planning = True

        if is_planning:
            if task_id == "LARGE-001":
                files_list = [f"src/module_{i}/service.py" for i in range(1, 401)]
                manifest = "FILE_MANIFEST:\n" + "\n".join(files_list)
            elif task_id == "EXTREME-002":
                files_list = [f"app/component_{i}/impl.py" for i in range(1, 1001)]
                manifest = "FILE_MANIFEST:\n" + "\n".join(files_list)
            else:
                manifest = f"FILE_MANIFEST:\n{filename}"
            response_text = f"I will plan the structure.\n\n{manifest}"
        else:
            is_test_file = False
            if requested_path:
                req_basename = os.path.basename(requested_path).lower()
                is_test_file = "test" in req_basename or "spec" in req_basename
                
            if task_id == "LARGE-001" and not is_test_file:
                match = re.search(r'already written \((\d+) files\):', last_msg_lower)
                already_written = int(match.group(1)) if match else 0
                batch_size = 40
                end_idx = min(400, already_written + batch_size)
                
                blocks = []
                for i in range(already_written + 1, end_idx + 1):
                    blocks.append(f"FILE: src/module_{i}/service.py\n```python\ndef run_{i}():\n    print(\"Running service {i}\")\n```")
                
                response_text = "Here is the implementation.\n\n" + "\n\n".join(blocks)
                if end_idx >= 400:
                    response_text += "\n\nSCAFFOLD_COMPLETE"
            elif task_id == "EXTREME-002" and not is_test_file:
                match = re.search(r'already written \((\d+) files\):', last_msg_lower)
                already_written = int(match.group(1)) if match else 0
                batch_size = 50
                end_idx = min(1000, already_written + batch_size)
                
                blocks = []
                for i in range(already_written + 1, end_idx + 1):
                    blocks.append(f"FILE: app/component_{i}/impl.py\n```python\ndef impl_{i}():\n    print(\"implement\")\n    return True\n```")
                
                response_text = "Here is the implementation.\n\n" + "\n\n".join(blocks)
                if end_idx >= 1000:
                    response_text += "\n\nSCAFFOLD_COMPLETE"
            elif domain == "task_generation":
                ext = filename.split(".")[-1].lower()
                lang_map = {
                    "py": "python", "js": "javascript", "ts": "typescript", "tsx": "tsx",
                    "go": "go", "rs": "rust", "cpp": "cpp", "java": "java", "php": "php",
                    "rb": "ruby", "swift": "swift", "cr": "crystal", "kt": "kotlin",
                    "dart": "dart", "cs": "csharp", "html": "html", "css": "css",
                    "json": "json", "yaml": "yaml", "yml": "yaml", "md": "markdown",
                    "svg": "xml", "tex": "tex"
                }
                lang = lang_map.get(ext, "text")
                # Game engine adapters (Unity/Unreal/Godot) match code block fences by filename rather than lang tag.
                block_tag = filename if ext in ("cs", "cpp", "h", "hpp", "gd") else lang
                response_text = f"Here is the implementation.\n\nFILE: {filename}\n```{block_tag}\n{file_content}\n```\nSCAFFOLD_COMPLETE"
            elif requested_ext and len(requested_ext) <= 10:
                response_text = f"Here is the implementation.\n\nFILE: {filename}\n```\n{file_content}\n```\nSCAFFOLD_COMPLETE"
            elif domain == "generate_files":

                response_text = """Here is the implementation.

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
SCAFFOLD_COMPLETE"""
            elif domain == "text_messages":
                response_text = "Output for text_messages: The SMS message has been queued and sent successfully natively."
            elif domain == "videos":
                response_text = """Here is the video generation implementation.

FILE: generate_video.py
```python
from moviepy.editor import ColorClip
clip = ColorClip(size=(64, 64), color=(255, 0, 0), duration=1)
clip.write_videofile("generated_media.mp4", fps=10, logger=None)
```

FILE: test_video.py
```python
import os
import subprocess
import sys
def test_video_exists():
    res = subprocess.run([sys.executable, "generate_video.py"], capture_output=True)
    assert res.returncode == 0
    assert os.path.exists("generated_media.mp4")
```
SCAFFOLD_COMPLETE"""
            elif domain == "images":
                response_text = """Here is the image generation implementation.

FILE: generate_image.py
```python
from PIL import Image
img = Image.new("RGB", (64, 64), color="blue")
img.save("logo.png")
with open("logo.svg", "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#3b82f6"/></svg>')
```

FILE: test_image.py
```python
import os
import subprocess
import sys
def test_image_exists():
    res = subprocess.run([sys.executable, "generate_image.py"], capture_output=True)
    assert res.returncode == 0
    assert os.path.exists("logo.png")
    assert os.path.exists("logo.svg")
```
SCAFFOLD_COMPLETE"""
            elif domain == "audio_files":
                response_text = """Here is the audio generation implementation.

FILE: generate_audio.py
```python
import wave
import struct
with wave.open("drum_loop.wav", "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(8000)
    for i in range(8000):
        data = struct.pack('<h', int(16384 * 0.5))
        w.writeframesraw(data)
with open("generated_media.mp4", "wb") as f:
    f.write(b"fake mp4 audio content")
```

FILE: test_audio.py
```python
import os
import subprocess
import sys
def test_audio_exists():
    res = subprocess.run([sys.executable, "generate_audio.py"], capture_output=True)
    assert res.returncode == 0
    assert os.path.exists("drum_loop.wav")
```
SCAFFOLD_COMPLETE"""
            elif domain == "music_videos":
                response_text = """Here is the music video generation implementation.

FILE: generate_music_video.py
```python
from moviepy.editor import ColorClip
clip = ColorClip(size=(64, 64), color=(0, 255, 0), duration=1)
clip.write_videofile("generated_media.mp4", fps=10, logger=None)
```

FILE: test_music_video.py
```python
import os
import subprocess
import sys
def test_music_video_exists():
    res = subprocess.run([sys.executable, "generate_music_video.py"], capture_output=True)
    assert res.returncode == 0
    assert os.path.exists("generated_media.mp4")
```
SCAFFOLD_COMPLETE"""
            else:
                lang_map = {
                    "websites": "html",
                    "mobile_apps": "tsx",
                    "video_games": "javascript",
                    "backend_services": "python",
                    "deployments": "hcl",
                    "images": "xml",
                    "run_applications": "applescript",
                    "computer_control": "applescript",
                    "phone_calls": "python"
                }
                lang = lang_map.get(domain, "text")
                response_text = f"Here is the implementation.\n\nFILE: {filename}\n```{lang}\n{file_content}\n```\nSCAFFOLD_COMPLETE"

        # Override response for self-healing loop compilation error repair test
        is_repair = (
            "return only a json object" in filtered_history
            or "fix a '" in filtered_history
            or "failure in a" in filtered_history
        )
        if is_repair:
            if "app/main.py" in filtered_history:
                response_text = '{"app/main.py": "def run_app():\\n    print(\'broken\')\\n"}'

            else:
                import re
                config_basenames = {
                    "package.json", "tsconfig.json", "vite.config.ts", ".env", ".env.example",
                    ".gitignore", ".npmrc", "babel.config.js", "metro.config.js", "tailwind.config.js",
                    "postcss.config.js", "webpack.config.js"
                }
                files_to_fix = []
                matches = re.findall(r"##\s+([^\s\n`]+)", last_msg)
                for m in matches:
                    m_clean = m.strip("`:")
                    if m_clean and "." in m_clean:
                        files_to_fix.append(m_clean)
                if not files_to_fix:
                    matches = re.findall(r"##\s+([^\s\n`]+)", filtered_history)
                    for m in matches:
                        m_clean = m.strip("`:")
                        if m_clean and "." in m_clean:
                            files_to_fix.append(m_clean)

                # Filter out configuration files from files_to_fix so we can fallback to extracting code paths from compiler logs
                files_to_fix = [f for f in files_to_fix if os.path.basename(f) not in config_basenames]

                # Fallback: extract paths directly from compiler error logs in the prompt
                if not files_to_fix:
                    path_matches = re.findall(
                        r'\b(?:frontend/|backend/|src/|[\w\-]+/)*[\w\-]+\.(?:py|tsx?|jsx?|go|rs|cpp|h|html|css|json)\b',
                        last_msg
                    )
                    for pm in path_matches:
                        pm_clean = pm.strip("`'\"\\:,()[]{}<>")
                        if pm_clean and "." in pm_clean:
                            if "node_modules" in pm_clean:
                                continue
                            # Prepend frontend/ if it's a src/ component and we're inside a node project
                            if "src/" in pm_clean and not pm_clean.startswith("frontend/") and ("node" in filtered_history or "react" in filtered_history or "vite" in filtered_history):
                                pm_clean = "frontend/" + pm_clean
                            files_to_fix.append(pm_clean)
                    # Filter config files again after fallback matching
                    files_to_fix = [f for f in files_to_fix if os.path.basename(f) not in config_basenames]

                # Extra heuristics for compilation/Vite issues (always check regardless of files_to_fix empty state)
                last_msg_lower = last_msg.lower()
                if "onwarn" in last_msg_lower or "rollup" in last_msg_lower or "vite" in last_msg_lower or "invalid resolved id" in last_msg_lower:
                    files_to_fix.append("frontend/src/App.jsx")
                    files_to_fix.append("frontend/src/main.jsx")
                    files_to_fix.append("frontend/src/App.tsx")
                    files_to_fix.append("frontend/src/main.tsx")

                # Extra heuristics for other cases with empty files_to_fix
                if not files_to_fix:
                    if "couldn't find any `pages` or `app` directory" in last_msg_lower or "couldn't find any pages or app directory" in last_msg_lower:
                        files_to_fix.append("frontend/pages/index.tsx")
                    elif "no inputs were found in config file" in last_msg_lower:
                        files_to_fix.append("frontend/src/index.ts")

                # Filter config files again after heuristics matching
                files_to_fix = [f for f in files_to_fix if os.path.basename(f) not in config_basenames]

                fixes_dict = {}
                for fpath in set(files_to_fix):
                    # Normalize fpath to prevent malformed paths like frontend/tend/...
                    if "src/" in fpath:
                        parts = fpath.split("src/", 1)
                        fpath = "frontend/src/" + parts[1]
                    elif "index.html" in fpath:
                        fpath = "frontend/index.html"
                    elif "main.jsx" in fpath:
                        fpath = "frontend/src/main.jsx"
                    elif "main.tsx" in fpath:
                        fpath = "frontend/src/main.tsx"
                    elif "App.jsx" in fpath:
                        fpath = "frontend/src/App.jsx"
                    elif "App.tsx" in fpath:
                        fpath = "frontend/src/App.tsx"

                    basename = os.path.basename(fpath)
                    if basename in config_basenames:
                        continue  # Keep original generated configuration
                    
                    ext = basename.split(".")[-1].lower() if "." in basename else ""
                    is_test_file = "test" in basename.lower() or "spec" in basename.lower()
                    
                    if basename == "index.html":
                        fixes_dict[fpath] = '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><title>App</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>'
                    elif basename == "main.jsx":
                        fixes_dict[fpath] = 'import React from "react";\nimport ReactDOM from "react-dom/client";\nimport App from "./App";\nReactDOM.createRoot(document.getElementById("root")).render(React.createElement(React.StrictMode, null, React.createElement(App, null)));'
                    elif basename == "main.tsx":
                        fixes_dict[fpath] = 'import React from "react";\nimport ReactDOM from "react-dom/client";\nimport App from "./App";\nReactDOM.createRoot(document.getElementById("root")!).render(React.createElement(React.StrictMode, null, React.createElement(App, null)));'
                    elif is_test_file:
                        if ext in ("js", "ts", "jsx", "tsx"):
                            fixes_dict[fpath] = 'import { test, expect } from "vitest";\ntest("runs successfully", () => {\n    expect(1 + 1).toBe(2);\n});'
                        elif ext == "py":
                            fixes_dict[fpath] = 'def test_dummy():\n    assert True'
                        else:
                            fixes_dict[fpath] = 'assert True'
                    else:
                        if ext in ("jsx", "tsx"):
                            is_rn_project = "react-native" in filtered_history.lower() or "expo" in filtered_history.lower()
                            if is_rn_project:
                                fixes_dict[fpath] = 'import React from "react";\nimport { View, Text } from "react-native";\nexport default function App() {\n    return React.createElement(View, null, React.createElement(Text, null, "App"));\n}'
                            else:
                                fixes_dict[fpath] = 'import React from "react";\nexport default function App() {\n    return React.createElement("div", null, "App");\n}'
                        elif ext in ("js", "ts"):
                            fixes_dict[fpath] = 'export function helper() {\n    return "helper";\n}'
                        elif ext == "py":
                            fixes_dict[fpath] = 'def main():\n    print("main service running")\n    return True\nif __name__ == "__main__":\n    main()'
                        else:
                            fixes_dict[fpath] = '/* ok */'
                
                if fixes_dict:
                    # Extended fixes dictionary to include variants with/without frontend prefix
                    extended_fixes = {}
                    for k, v in fixes_dict.items():
                        extended_fixes[k] = v
                        if k.startswith("frontend/"):
                            stripped_k = k.replace("frontend/", "", 1)
                            extended_fixes[stripped_k] = v
                        else:
                            extended_fixes["frontend/" + k] = v
                    response_text = json.dumps(extended_fixes)
                else:
                    response_text = '{}'

        try:
            with open("/Users/laynefaler/.gemini/antigravity/brain/c83ce90c-9e34-44d5-af14-b1ee6d85c486/mock_server_debug.log", "a", encoding="utf-8") as f_dbg:
                f_dbg.write(f"\n=====================================\n")
                f_dbg.write(f"REQUEST FOR PATH: {requested_path}\n")
                f_dbg.write(f"LAST MESSAGE: {last_msg}\n")
                f_dbg.write(f"DOMAIN: {domain if 'domain' in locals() else 'N/A'}\n")
                f_dbg.write(f"FILENAME: {filename if 'filename' in locals() else 'N/A'}\n")
                f_dbg.write(f"IS_RN: {is_rn if 'is_rn' in locals() else 'N/A'}\n")
                f_dbg.write(f"RESPONSE LENGTH: {len(response_text)}\n")
        except Exception:
            pass

        # Return OpenAI-compatible stream or non-stream JSON
        stream = payload.get("stream", False)
        if stream:
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()

            # First send thinking block
            think_data = {"choices": [{"delta": {"content": "<thinking>\nPlanning functional steps...\n</thinking>\n"}}]}
            self.wfile.write(b"data: " + json.dumps(think_data).encode() + b"\n\n")

            # Stream main content in chunks
            chunk_size = 64
            for i in range(0, len(response_text), chunk_size):
                chunk = response_text[i:i+chunk_size]
                chunk_data = {"choices": [{"delta": {"content": chunk}}]}
                self.wfile.write(b"data: " + json.dumps(chunk_data).encode() + b"\n\n")
            self.wfile.write(b"data: [DONE]\n\n")
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_obj = {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": f"<thinking>\nPlanning...\n</thinking>\n{response_text}"
                    }
                }]
            }
            self.wfile.write(json.dumps(response_obj).encode())


@pytest.fixture(scope="session", autouse=True)
def completions_test_server():
    """Start local background HTTP completions server for functional integration testing."""
    server = HTTPServer(('127.0.0.1', 0), CompletionsHTTPHandler)
    port = server.server_address[1]
    
    # Configure provider routing env variables
    os.environ["SAGE_OPENROUTER_BASE_URL"] = f"http://127.0.0.1:{port}/v1"
    os.environ["SAGE_OPENROUTER_API_KEY"] = "test-key-value"
    os.environ["SAGE_TESTING"] = "1"

    # Force using our local openrouter provider by default during tests
    os.environ["SAGE_DEFAULT_MODEL"] = "openrouter:meta-llama/llama-3.3-70b-instruct:free"

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    yield server

    server.shutdown()
    server.server_close()
