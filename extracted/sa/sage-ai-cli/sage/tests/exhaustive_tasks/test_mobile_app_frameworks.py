import os
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from sage.main import app as sage_app
from sage.core.content_validator import validate_content

runner = CliRunner()

MOBILE_MOCKS = {
    "react_native": """
Output for React Native:
FILE: FeedScreen.tsx
```tsx
import React, { useState } from 'react';
import { StyleSheet, Text, View, FlatList, SafeAreaView, TouchableOpacity } from 'react-native';

interface Post {
    id: string;
    title: string;
}

export default function FeedScreen() {
    const [posts, setPosts] = useState<Post[]>([
        { id: '1', title: 'Welcome to SAGE Native' },
        { id: '2', title: 'Ad Campaign dashboard launch' }
    ]);

    return (
        <SafeAreaView style={styles.container}>
            <Text style={styles.header}>Ad Feed</Text>
            <FlatList
                data={posts}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <TouchableOpacity style={styles.card}>
                        <Text style={styles.title}>{item.title}</Text>
                    </TouchableOpacity>
                )}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    header: { fontSize: 24, fontWeight: 'bold', padding: 16 },
    card: { padding: 16, marginHorizontal: 16, marginBottom: 12, backgroundColor: '#fff', borderRadius: 8 },
    title: { fontSize: 16, fontWeight: '600' }
});
```
""",
    "flutter_dart": """
Output for Flutter Dart:
FILE: main.dart
```dart
import 'package:flutter/material.dart';

void main() => runApp(const AdPlatformApp());

class AdPlatformApp extends StatelessWidget {
  const AdPlatformApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ad Platform',
      theme: ThemeData.dark(),
      home: const FeedScreen(),
    );
  }
}

class FeedScreen extends StatefulWidget {
  const FeedScreen({Key? key}) : super(key: key);

  @override
  State<FeedScreen> createState() => _FeedScreenState();
}

class _FeedScreenState extends State<FeedScreen> {
  final List<String> _campaigns = ['Summer Promo', 'Winter Clearance'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Campaigns')),
      body: ListView.builder(
        itemCount: _campaigns.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(_campaigns[index]),
          );
        },
      ),
    );
  }
}
```
""",
    "swift_ios": """
Output for Swift iOS:
FILE: ContentView.swift
```swift
import SwiftUI

struct ContentView: View {
    @State private var items = ["iOS Ad Campaign 1", "iOS Ad Campaign 2"]
    
    var body: some View {
        NavigationView {
            List(items, id: \\.self) { item in
                Text(item)
            }
            .navigationTitle("Campaigns")
        }
    }
}
```
""",
    "kotlin_android": """
Output for Kotlin Android:
FILE: MainActivity.kt
```kotlin
package com.sage.adplatform

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Greeting("Kotlin Android App")
            }
        }
    }
}

@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}
```
"""
}

@pytest.mark.parametrize("framework", ["react_native", "flutter_dart", "swift_ios", "kotlin_android"])
def test_mobile_framework_generation(framework):
    """Verify mobile framework tasks are written and validate perfectly."""
    prompt = f"Implement a complete {framework} mobile component with lists and navigation."
    mock_output = MOBILE_MOCKS[framework]

    with patch("sage.main._prepare_model_for_use") as mock_prep, \
         patch("sage.main._build_router") as mock_router:
         
        mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
        mock_router_inst = MagicMock()
        mock_router_inst.stream.return_value = [mock_output]
        mock_router.return_value = mock_router_inst
        
        with runner.isolated_filesystem():
            result = runner.invoke(sage_app, ["ask", prompt, "--raw", "--agent"])
            assert result.exit_code == 0, f"Task failed: {result.output}"
            
            generated_files = [
                f for f in Path(".").glob("**/*")
                if f.is_file() and not any(part.startswith(".") or part in ("venv", "__pycache__") for part in f.parts) and f.suffix != ".pyc"
            ]
            assert len(generated_files) > 0, "No files written"
            
            for f in generated_files:
                content = f.read_text(encoding="utf-8")
                val_res = validate_content(str(f), content)
                assert val_res.ok, f"File {f} contains placeholders: {val_res.reason}"
