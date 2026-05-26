import os
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from sage.main import app as sage_app
from sage.core.content_validator import validate_content

runner = CliRunner()

FRONTEND_MOCKS = {
    "react_tailwind": """
Output for React/Tailwind Dashboard:
FILE: App.jsx
```jsx
import React, { useState } from 'react';

export default function App() {
    const [theme, setTheme] = useState('dark');
    return (
        <div className={theme === 'dark' ? 'bg-gray-900 text-white min-h-screen' : 'bg-white text-gray-900 min-h-screen'}>
            <header className="p-4 border-b border-gray-700 flex justify-between items-center">
                <h1 className="text-2xl font-bold tracking-tight">Analytics Dashboard</h1>
                <button 
                    onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    Toggle Theme
                </button>
            </header>
            <main className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in">
                <div className="p-4 bg-gray-800 rounded-lg shadow border border-gray-700">
                    <h2 className="text-lg font-semibold mb-2">Total Users</h2>
                    <p className="text-3xl font-bold">1,240</p>
                </div>
                <div className="p-4 bg-gray-800 rounded-lg shadow border border-gray-700">
                    <h2 className="text-lg font-semibold mb-2">Active Sessions</h2>
                    <p className="text-3xl font-bold">342</p>
                </div>
                <div className="p-4 bg-gray-800 rounded-lg shadow border border-gray-700">
                    <h2 className="text-lg font-semibold mb-2">Conversion Rate</h2>
                    <p className="text-3xl font-bold">4.2%</p>
                </div>
            </main>
        </div>
    );
}
```
""",
    "vue_pinia": """
Output for Vue/Pinia App:
FILE: index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue Store</title>
</head>
<body>
    <div id="app"></div>
</body>
</html>
```
FILE: store.js
```javascript
import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: []
    }),
    actions: {
        addItem(item) {
            this.items.push(item);
        },
        removeItem(id) {
            this.items = this.items.filter(item => item.id !== id);
        }
    }
});
```
FILE: App.vue
```vue
<template>
  <div class="app">
    <h1>Vue 3 Shopping Store</h1>
    <ul>
      <li v-for="item in cart.items" :key="item.id">
        {{ item.name }} - ${{ item.price }}
        <button @click="cart.removeItem(item.id)">Remove</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { useCartStore } from './store.js';

export default {
  setup() {
    const cart = useCartStore();
    return { cart };
  }
}
</script>
```
""",
    "svelte_kanban": """
Output for Svelte Kanban Board:
FILE: App.svelte
```html
<script>
    import { onMount } from 'svelte';
    let columns = [
        { id: 'todo', title: 'To Do', tasks: [{ id: 1, title: 'Write Tests' }] },
        { id: 'in_progress', title: 'In Progress', tasks: [] },
        { id: 'done', title: 'Done', tasks: [] }
    ];
    let nextId = 2;
    let newTaskTitle = '';

    function addTask() {
        if (!newTaskTitle.trim()) return;
        columns[0].tasks = [...columns[0].tasks, { id: nextId++, title: newTaskTitle }];
        newTaskTitle = '';
    }
</script>

<main class="p-6">
    <h1 class="text-2xl font-bold mb-4">Svelte Kanban Board</h1>
    <div class="flex gap-4">
        {#each columns as col}
            <div class="col bg-gray-100 p-4 rounded w-64">
                <h2 class="font-semibold mb-2">{col.title}</h2>
                <div class="task-list">
                    {#each col.tasks as task}
                        <div class="task bg-white p-2 rounded shadow mb-2">{task.title}</div>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
</main>
```
"""
}

@pytest.mark.parametrize("framework", ["react_tailwind", "vue_pinia", "svelte_kanban"])
def test_frontend_framework_generation(framework):
    """Verify frontend framework tasks are written and validate perfectly."""
    prompt = f"Implement a complete {framework} application with state management and layouts."
    mock_output = FRONTEND_MOCKS[framework]

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
                # Enforce no placeholders/stubs using the core validator
                val_res = validate_content(str(f), content)
                assert val_res.ok, f"File {f} contains placeholders: {val_res.reason}"
