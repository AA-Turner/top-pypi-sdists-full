import os
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from sage.main import app as sage_app
from sage.core.content_validator import validate_content

runner = CliRunner()

CORE_MOCKS = {
    "python": """
Output for Python:
FILE: main.py
```python
import asyncio

class ConnectionPool:
    def __init__(self, size: int):
        self.size = size
        self.pool = asyncio.Queue()
        for i in range(size):
            self.pool.put_nowait(f"Connection-{i}")

    async def acquire(self):
        return await self.pool.get()

    async def release(self, conn: str):
        await self.pool.put(conn)

async def main():
    pool = ConnectionPool(5)
    conn = await pool.acquire()
    print(f"Acquired: {conn}")
    await pool.release(conn)
```
""",
    "javascript_typescript": """
Output for TypeScript:
FILE: pool.ts
```typescript
export class PromisePool<T> {
    private activeCount = 0;
    private queue: (() => void)[] = [];

    constructor(private limit: number) {}

    async run(task: () => Promise<T>): Promise<T> {
        if (this.activeCount >= this.limit) {
            await new Promise<void>((resolve) => this.queue.push(resolve));
        }
        this.activeCount++;
        try {
            return await task();
        } finally {
            this.activeCount--;
            const next = this.queue.shift();
            if (next) next();
        }
    }
}
```
""",
    "rust": """
Output for Rust:
FILE: lib.rs
```rust
use std::sync::{Arc, Mutex};

pub struct ThreadSafeCounter {
    value: Arc<Mutex<i32>>,
}

impl ThreadSafeCounter {
    pub fn new() -> Self {
        Self {
            value: Arc::new(Mutex::new(0)),
        }
    }

    pub fn increment(&self) {
        let mut val = self.value.lock().unwrap();
        *val += 1;
    }

    pub fn get_value(&self) -> i32 {
        *self.value.lock().unwrap()
    }
}
```
""",
    "go": """
Output for Go:
FILE: main.go
```go
package main

import (
	"fmt"
	"sync"
)

type WorkerPool struct {
	numWorkers int
	jobs       chan int
	results    chan int
	wg         sync.WaitGroup
}

func NewWorkerPool(numWorkers int, numJobs int) *WorkerPool {
	return &WorkerPool{
		numWorkers: numWorkers,
		jobs:       make(chan int, numJobs),
		results:    make(chan int, numJobs),
	}
}

func (wp *WorkerPool) worker() {
	defer wp.wg.Done()
	for job := range wp.jobs {
		wp.results <- job * 2
	}
}

func (wp *WorkerPool) Run() {
	for i := 0; i < wp.numWorkers; i++ {
		wp.wg.Add(1)
		go wp.worker()
	}
	close(wp.jobs)
	wp.wg.Wait()
	close(wp.results)
}
```
""",
    "cpp": """
Output for C++:
FILE: allocator.h
```cpp
#ifndef ALLOCATOR_H
#define ALLOCATOR_H

#include <vector>
#include <memory>

template <typename T>
class ResourceAllocator {
private:
    std::vector<std::unique_ptr<T>> resources;
public:
    void addResource(std::unique_ptr<T> res) {
        resources.push_back(std::move(res));
    }
    T* getResource(size_t index) {
        if (index < resources.size()) {
            return resources[index].get();
        }
        return nullptr;
    }
};

#endif
```
""",
    "csharp": """
Output for C#:
FILE: Queue.cs
```csharp
using System;
using System.Collections.Generic;

public class ThreadSafeQueue<T>
{
    private readonly Queue<T> _queue = new Queue<T>();
    private readonly object _lock = new object();

    public void Enqueue(T item)
    {
        lock (_lock)
        {
            _queue.Enqueue(item);
        }
    }

    public bool TryDequeue(out T value)
    {
        lock (_lock)
        {
            if (_queue.Count > 0)
            {
                value = _queue.Dequeue();
                return true;
            }
            value = default(T);
            return false;
        }
    }
}
```
""",
    "java": """
Output for Java:
FILE: SimpleCache.java
```java
package com.sage.core;

import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class SimpleCache<K, V> {
    private final Map<K, V> storage = new ConcurrentHashMap<>();

    public void put(K key, V value) {
        storage.put(key, value);
    }

    public V get(K key) {
        return storage.get(key);
    }

    public void remove(K key) {
        storage.remove(key);
    }
}
```
""",
    "kotlin": """
Output for Kotlin:
FILE: EventNotifier.kt
```kotlin
package com.sage.core

class EventNotifier {
    private val listeners = mutableListOf<(String) -> Unit>()

    fun registerListener(listener: (String) -> Unit) {
        listeners.add(listener)
    }

    fun notifyAll(message: String) {
        listeners.forEach { it(message) }
    }
}
```
""",
    "swift": """
Output for Swift:
FILE: BankAccount.swift
```swift
import Foundation

actor BankAccount {
    private var balance: Double = 0.0

    func deposit(amount: Double) {
        balance += amount
    }

    func withdraw(amount: Double) -> Bool {
        if balance >= amount {
            balance -= amount
            return true
        }
        return false
    }

    func getBalance() -> Double {
        return balance
    }
}
```
""",
    "ruby": """
Output for Ruby:
FILE: pipeline.rb
```ruby
class CustomPipeline
  def initialize
    @steps = []
  end

  def add_step(&block)
    @steps << block
    self
  end

  def execute(input)
    @steps.reduce(input) { |acc, step| step.call(acc) }
  end
end
```
""",
    "php": """
Output for PHP:
FILE: router.php
```php
<?php
namespace Sage\\Core;

class SimpleRouter {
    private array $routes = [];

    public function addRoute(string $path, callable $callback): void {
        $this->routes[$path] = $callback;
    }

    public function dispatch(string $path): mixed {
        if (isset($this->routes[$path])) {
            return call_user_func($this->routes[$path]);
        }
        return null;
    }
}
```
""",
    "dart": """
Output for Dart:
FILE: event_bus.dart
```dart
import 'dart:async';

class EventBus {
  final StreamController _controller = StreamController.broadcast();

  Stream get stream => _controller.stream;

  void emit(dynamic event) {
    _controller.add(event);
  }

  void dispose() {
    _controller.close();
  }
}
```
""",
    "scala": """
Output for Scala:
FILE: User.scala
```scala
package com.sage.core

case class User(id: Int, name: String, isActive: Boolean)

class UserRepository {
  private var users = Map[Int, User]()

  def save(user: User): Unit = {
    users = users + (user.id -> user)
  }

  def findById(id: Int): Option[User] = {
    users.get(id)
  }
}
```
""",
    "gdscript": """
Output for GDScript:
FILE: player.gd
```gdscript
extends Node

signal health_changed(new_health)

@export var max_health: int = 100
var current_health: int = 100

func take_damage(amount: int) -> void:
	current_health = max(0, current_health - amount)
	health_changed.emit(current_health)
```
"""
}

@pytest.mark.parametrize("language", [
    "python", "javascript_typescript", "rust", "go", "cpp", "csharp",
    "java", "kotlin", "swift", "ruby", "php", "dart", "scala", "gdscript"
])
def test_core_language_generation(language):
    """Verify that core language tasks write complete code without placeholders."""
    prompt = f"Implement a complete, production-ready {language} module for concurrency or data management."
    mock_output = CORE_MOCKS[language]

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
                assert val_res.ok, f"File {f} contains placeholders/errors: {val_res.reason}"
