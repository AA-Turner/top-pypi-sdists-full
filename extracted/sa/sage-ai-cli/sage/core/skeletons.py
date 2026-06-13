"""T7 + T9 — Project skeletons + templates.

Match the user's task to a known skeleton (React+Vite, Node+Express, FastAPI,
fullstack), seed the boilerplate, and only have the LLM fill in the gaps.
This was the missing piece in the Novellia run — a fullstack-react-node
skeleton would have given the model a working server, working frontend, and
a real package.json from minute one.

Templates are kept inline as Python strings so they ship with the package
and are subject to the same content_validator we apply to LLM output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Skeleton", "SKELETONS", "match_skeleton", "apply_skeleton"]


@dataclass
class Skeleton:
    name: str
    description: str
    keywords: tuple[str, ...]
    files: dict[str, str] = field(default_factory=dict)


# ── Inline templates ───────────────────────────────────────────────────

_NODE_EXPRESS_PACKAGE_JSON = """\
{
  "name": "node-express-app",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "start": "node src/server.js",
    "dev": "node --watch src/server.js",
    "test": "vitest run"
  },
  "dependencies": {
    "express": "^4.19.2",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "vitest": "^1.6.0",
    "supertest": "^7.0.0"
  }
}
"""

_NODE_EXPRESS_SERVER = """\
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => res.json({ ok: true }));

const port = process.env.PORT || 3000;
if (process.env.NODE_ENV !== 'test') {
  app.listen(port, () => console.log(`API on :${port}`));
}

export default app;
"""

_NODE_EXPRESS_TEST = """\
import { describe, it, expect } from 'vitest';
import request from 'supertest';
import app from '../src/server.js';

describe('health', () => {
  it('returns ok', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.ok).toBe(true);
  });
});
"""

_REACT_VITE_PACKAGE_JSON = """\
{
  "name": "react-vite-app",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest run"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.3.1",
    "vitest": "^1.6.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.4.6",
    "jsdom": "^24.1.0"
  }
}
"""

_REACT_VITE_INDEX_HTML = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

_REACT_VITE_MAIN = """\
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

_REACT_VITE_APP = """\
import { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);
  return (
    <main>
      <h1>App</h1>
      <button onClick={() => setCount((c) => c + 1)}>count is {count}</button>
    </main>
  );
}
"""

_REACT_VITE_CONFIG = """\
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
});
"""

_FASTAPI_PYPROJECT = """\
[project]
name = "fastapi-app"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.9.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "httpx>=0.27.0"]
"""

_FASTAPI_MAIN = """\
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API")


class Health(BaseModel):
    ok: bool


@app.get("/health", response_model=Health)
def health() -> Health:
    return Health(ok=True)
"""

_FASTAPI_TEST = """\
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}
"""

_FULLSTACK_README = """\
# Fullstack React + Node MVP

## Run
```
docker compose up         # full stack
# or
cd backend && npm install && npm run dev
cd frontend && npm install && npm run dev
```
"""

_FULLSTACK_DOCKER_COMPOSE = """\
services:
  api:
    build: ./backend
    ports: ['3000:3000']
    environment:
      NODE_ENV: development
  web:
    build: ./frontend
    ports: ['5173:5173']
    depends_on: [api]
"""

_NODE_EXPRESS_README = """\
# Node + Express API

## Run
```
npm install
npm run dev
npm test
```
"""

_REACT_VITE_README = """\
# React + Vite App

## Run
```
npm install
npm run dev
npm test
```
"""

_NEXTJS_PACKAGE_JSON = """\
{
  "name": "nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "vitest run --passWithNoTests"
  },
  "dependencies": {
    "next": "latest",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vitest": "^1.6.0",
    "typescript": "^5.0.0"
  }
}
"""

_NEXTJS_LAYOUT = """\
import React from 'react';
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
"""

_NEXTJS_PAGE = """\
import React from 'react';
export default function Page() {
  return (
    <main>
      <h1>App</h1>
    </main>
  );
}
"""

_NEXTJS_TEST = """\
import { test } from 'vitest';
test('page renders', () => {});
"""

_NEXTJS_README = """\
# Next.js App

## Run
```
npm install
npm run dev
npm run build
npm test
```
"""


# ── Skeleton registry ──────────────────────────────────────────────────

SKELETONS: tuple[Skeleton, ...] = (
    Skeleton(
        name="node-express",
        description="Node.js + Express API with vitest",
        keywords=("node", "express", "api", "backend"),
        files={
            "backend/package.json": _NODE_EXPRESS_PACKAGE_JSON,
            "backend/src/server.js": _NODE_EXPRESS_SERVER,
            "backend/tests/server.test.js": _NODE_EXPRESS_TEST,
            "README.md": _NODE_EXPRESS_README,
        },
    ),
    Skeleton(
        name="react-vite",
        description="React + Vite SPA with vitest + RTL",
        keywords=("react", "vite", "spa", "frontend"),
        files={
            "frontend/package.json": _REACT_VITE_PACKAGE_JSON,
            "frontend/index.html": _REACT_VITE_INDEX_HTML,
            "frontend/vite.config.js": _REACT_VITE_CONFIG,
            "frontend/src/main.jsx": _REACT_VITE_MAIN,
            "frontend/src/App.jsx": _REACT_VITE_APP,
            "README.md": _REACT_VITE_README,
        },
    ),
    Skeleton(
        name="fastapi",
        description="FastAPI service with pytest",
        keywords=("fastapi", "python", "uvicorn"),
        files={
            "backend/pyproject.toml": _FASTAPI_PYPROJECT,
            "backend/app/__init__.py": "",
            "backend/app/main.py": _FASTAPI_MAIN,
            "backend/tests/test_health.py": _FASTAPI_TEST,
        },
    ),
    Skeleton(
        name="fullstack-react-node",
        description="React frontend + Node/Express backend, docker-compose",
        keywords=("fullstack", "react", "node", "express"),
        files={
            "README.md": _FULLSTACK_README,
            "docker-compose.yml": _FULLSTACK_DOCKER_COMPOSE,
            "backend/package.json": _NODE_EXPRESS_PACKAGE_JSON,
            "backend/src/server.js": _NODE_EXPRESS_SERVER,
            "backend/tests/server.test.js": _NODE_EXPRESS_TEST,
            "frontend/package.json": _REACT_VITE_PACKAGE_JSON,
            "frontend/index.html": _REACT_VITE_INDEX_HTML,
            "frontend/vite.config.js": _REACT_VITE_CONFIG,
            "frontend/src/main.jsx": _REACT_VITE_MAIN,
            "frontend/src/App.jsx": _REACT_VITE_APP,
        },
    ),
    Skeleton(
        name="nextjs",
        description="Next.js App Router project",
        keywords=("nextjs", "next.js", "next js", "next"),
        files={
            "frontend/package.json": _NEXTJS_PACKAGE_JSON,
            "frontend/src/app/layout.tsx": _NEXTJS_LAYOUT,
            "frontend/src/app/page.tsx": _NEXTJS_PAGE,
            "frontend/src/app/page.test.tsx": _NEXTJS_TEST,
            "README.md": _NEXTJS_README,
        },
    ),
)


# ── Matching ───────────────────────────────────────────────────────────

def _score(prompt: str, sk: Skeleton) -> int:
    p = prompt.lower()
    return sum(1 for kw in sk.keywords if re.search(rf"\b{re.escape(kw)}\b", p))


def match_skeleton(prompt: str) -> Skeleton | None:
    """Pick the best skeleton for a prompt, or None if no clear match.

    Tie-breaker: skeletons with more keywords win (more specific match).
    Cutoff: at least 2 keyword hits OR 1 hit with the prompt explicitly
    naming the framework.
    """
    if not prompt or not prompt.strip():
        return None
    p_lower = prompt.lower()
    if any(kw in p_lower for kw in ["react-native", "react native", "expo", "flutter", "swift", "kotlin"]):
        return None
    scored = [(sk, _score(prompt, sk)) for sk in SKELETONS]
    scored.sort(key=lambda t: (t[1], len(t[0].keywords)), reverse=True)
    best, score = scored[0]
    if score >= 2:
        return best
    if score == 1 and re.search(r"\b(?:react|node|express|fastapi|vite|next|nextjs)\b",
                                prompt, re.IGNORECASE):
        return best
    return None


# ── Application ────────────────────────────────────────────────────────

def apply_skeleton(skeleton: Skeleton, target: Path, *,
                   overwrite: bool = False) -> list[str]:
    """Write all skeleton files into `target`. Returns list of files written."""
    written: list[str] = []
    for relpath, content in skeleton.files.items():
        dest = target / relpath
        if dest.exists() and not overwrite:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written.append(relpath)
    return written
