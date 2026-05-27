"""Specialized prompts per file type.

The generic `build_file_prompt` in `principal_engineer` is fine for
"give me a python file." But to get principal-engineer-quality output
we need per-file-type prompts that ENCODE the patterns: a model file
prompt mentions SQLModel/Base/timestamps/indexes; an API file prompt
mentions Depends/response_model/error mapping; a hook file prompt
mentions React Query keys + optimistic updates.

The prompt builder picks the right specialization based on the file
path. Falls back to the generic builder for paths it doesn't recognize.
"""

from __future__ import annotations

import re
import threading
from typing import Sequence

from sage.core.principal_engineer import (
    CURRENT_VERSIONS,
    FileSpec,
    build_file_prompt as _generic_build_file_prompt,
)


# ──────────────────────── Dynamic package research ────────────────────────
# When sage encounters a package it doesn't have in _TECH_KNOWLEDGE, it
# queries npm or PyPI to get the current version, description, and peer
# dependencies. This prevents hallucination of wrong API shapes.

_research_cache: dict[str, str] = {}
_research_lock = threading.Lock()


def _fetch_npm_info(package: str) -> str | None:
    """Fetch npm package metadata and return a compact reference string."""
    try:
        import urllib.request, json as _json
        url = f"https://registry.npmjs.org/{package}/latest"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = _json.loads(r.read())
        ver = data.get("version", "unknown")
        desc = (data.get("description") or "")[:200]
        peers = list((data.get("peerDependencies") or {}).keys())[:5]
        exports = list((data.get("exports") or {}).keys())[:5]
        peer_str = f" | peers: {', '.join(peers)}" if peers else ""
        export_str = f" | exports: {', '.join(exports)}" if exports else ""
        return (
            f"## {package} (npm v{ver})\n"
            f"{desc}\n"
            f"Install: `npm install {package}` or `bun add {package}`{peer_str}{export_str}\n"
        )
    except Exception:
        return None


def _fetch_pypi_info(package: str) -> str | None:
    """Fetch PyPI package metadata and return a compact reference string."""
    try:
        import urllib.request, json as _json
        url = f"https://pypi.org/pypi/{package}/json"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = _json.loads(r.read())
        info = data.get("info", {})
        ver = info.get("version", "unknown")
        desc = (info.get("summary") or "")[:200]
        requires = (info.get("requires_dist") or [])[:5]
        return (
            f"## {package} (PyPI v{ver})\n"
            f"{desc}\n"
            f"Install: `pip install {package}=={ver}`\n"
            + (f"Requires: {', '.join(requires)}\n" if requires else "")
        )
    except Exception:
        return None


def research_package(name: str) -> str | None:
    """Look up a package on npm or PyPI and return a reference snippet.

    Results are cached for the lifetime of the process. Network errors
    return None silently — callers fall back to LLM knowledge.
    """
    key = name.lower().strip()
    with _research_lock:
        if key in _research_cache:
            return _research_cache[key]

    # Try npm first (most JS packages), then PyPI
    result = _fetch_npm_info(name) or _fetch_pypi_info(name)
    with _research_lock:
        _research_cache[key] = result or ""
    return result or None


def _extract_unknown_packages(task: str, role: str) -> list[str]:
    """Pull package/library names from task + role that aren't in _TECH_KNOWLEDGE."""
    combined = (task + " " + role).lower()
    # Match patterns like: `import X from`, `require("X")`, `pip install X`,
    # `npm install X`, `bun add X`, `from X import`, standalone CamelCase names
    patterns = [
        r'(?:import\s+\w+\s+from\s+["\'])([^"\'@]+)',
        r'(?:require\(["\'])([^"\'@]+)',
        r'(?:pip install|bun add|npm install|yarn add)\s+([\w@/-]+)',
        r'(?:from\s+)([\w.]+)\s+import',
    ]
    candidates = set()
    for pat in patterns:
        for m in re.finditer(pat, combined):
            pkg = m.group(1).strip().split("/")[0].split(".")[0]
            if pkg and len(pkg) > 2:
                candidates.add(pkg)

    # Filter out things already in our static knowledge or builtins
    known = set(_TECH_KNOWLEDGE.keys()) | {
        "react", "python", "fastapi", "django", "flask", "node", "bun",
        "typescript", "javascript", "html", "css", "sql", "postgres",
        "mysql", "sqlite", "redis", "docker", "kubernetes", "git",
        "os", "sys", "re", "json", "math", "time", "datetime", "path",
        "fs", "http", "https", "url", "util", "events", "stream",
    }
    return [p for p in sorted(candidates) if p not in known]


# ──────────────────────── Tech knowledge base ──────────────────────────────
# Prevents hallucination when the LLM encounters unfamiliar technologies.
# These facts are injected into the prompt when the relevant tech is detected.

_TECH_KNOWLEDGE: dict[str, str] = {
    # ── JavaScript runtimes & package managers ────────────────────────────
    "bun": (
        "## Bun.js Reference\n"
        "Bun is a fast all-in-one JS runtime, bundler, transpiler, and package manager.\n"
        "- Docker image: `oven/bun:1` (NOT `node:`)\n"
        "- Package manager: `bun install` (creates bun.lockb, NOT package-lock.json)\n"
        "- Run scripts: `bun run dev` / `bun run build` / `bun test`\n"
        "- Built-in TypeScript: no ts-node needed, `bun file.ts` runs directly\n"
        "- HTTP server: `Bun.serve({ port: 3000, fetch(req) { return new Response('ok') } })`\n"
        "- File I/O: `const file = Bun.file('path'); await file.text()`\n"
        "- Compatible with most npm packages (install same way)\n"
    ),
    "pnpm": (
        "## pnpm Reference\n"
        "pnpm is a fast, disk-efficient npm alternative using hard links.\n"
        "- Install: `pnpm install` (creates pnpm-lock.yaml)\n"
        "- Add: `pnpm add <pkg>` / `pnpm add -D <pkg>` for devDependencies\n"
        "- Run: `pnpm run dev` / `pnpm dev`\n"
        "- Docker: `RUN npm install -g pnpm && pnpm install`\n"
    ),
    # ── Job queues ────────────────────────────────────────────────────────
    "bullmq": (
        "## BullMQ Reference\n"
        "BullMQ is a Redis-based job queue for Node.js/Bun.js (TypeScript/JavaScript).\n"
        "NOT Python Celery — this runs in JS/TS.\n"
        "```ts\n"
        "import { Queue, Worker } from 'bullmq';\n"
        "import IORedis from 'ioredis';\n"
        "const connection = new IORedis(process.env.REDIS_URL);\n"
        "const queue = new Queue('my-queue', { connection });\n"
        "await queue.add('job-name', { data: 'payload' });\n"
        "const worker = new Worker('my-queue', async (job) => {\n"
        "  console.log(job.data);\n"
        "}, { connection });\n"
        "```\n"
        "Install: `npm install bullmq ioredis`\n"
    ),
    "celery": (
        "## Celery Reference\n"
        "Celery is a Python distributed task queue.\n"
        "```python\n"
        "from celery import Celery\n"
        "app = Celery('tasks', broker=os.environ['REDIS_URL'])\n"
        "@app.task\n"
        "def process(data): ...\n"
        "# Call: process.delay(data)\n"
        "# Worker: celery -A tasks worker --loglevel=info\n"
        "```\n"
        "Install: `pip install celery[redis]`\n"
    ),
    # ── Packaging ────────────────────────────────────────────────────────
    "pypi": (
        "## PyPI Packaging Reference\n"
        "PyPI is the Python Package Index. Publish via pyproject.toml + hatchling:\n"
        "```toml\n"
        "[build-system]\n"
        "requires = ['hatchling>=1.21']\n"
        "build-backend = 'hatchling.build'\n"
        "[project]\n"
        "name = 'my-package'\n"
        "version = '0.1.0'\n"
        "requires-python = '>=3.11'\n"
        "[project.scripts]\n"
        "my-package = 'my_package.main:run'\n"
        "[tool.hatch.build.targets.wheel]\n"
        "packages = ['my_package']\n"
        "```\n"
        "Build: `python -m build` | Publish: `twine upload dist/*`\n"
    ),
    # ── Databases ─────────────────────────────────────────────────────────
    "timescaledb": (
        "## TimescaleDB Reference\n"
        "TimescaleDB is a PostgreSQL extension for time-series data.\n"
        "- Same connection string as PostgreSQL (asyncpg/psycopg2)\n"
        "- Enable: `CREATE EXTENSION IF NOT EXISTS timescaledb`\n"
        "- Hypertable: `SELECT create_hypertable('events', 'time')`\n"
        "- Image: `timescale/timescaledb:latest-pg16`\n"
    ),
    "mongodb": (
        "## MongoDB Reference (Python)\n"
        "- Async: `motor` — `from motor.motor_asyncio import AsyncIOMotorClient`\n"
        "- `client = AsyncIOMotorClient(os.environ['MONGO_URL'])`\n"
        "- `db = client['mydb']; coll = db['users']`\n"
        "- Insert: `await coll.insert_one(doc)` | Find: `await coll.find_one({'_id': ...})`\n"
        "- Sync: `pymongo` — `MongoClient(url)`\n"
        "- Docker: `mongo:7`\n"
    ),
    "prisma": (
        "## Prisma ORM Reference (Node.js/Bun)\n"
        "- Schema: `prisma/schema.prisma` with models and datasource\n"
        "- Generate: `npx prisma generate` / `bunx prisma generate`\n"
        "- Migrate: `npx prisma migrate dev --name init`\n"
        "- Client: `import { PrismaClient } from '@prisma/client'`\n"
        "- `const db = new PrismaClient(); await db.user.findMany()`\n"
        "- Install: `npm install @prisma/client && npx prisma init`\n"
    ),
    "drizzle": (
        "## Drizzle ORM Reference (TypeScript)\n"
        "- Define schema in `src/db/schema.ts` with `pgTable`, `text`, `integer` etc.\n"
        "- `import { drizzle } from 'drizzle-orm/node-postgres'`\n"
        "- `const db = drizzle(pool); await db.select().from(users)`\n"
        "- Migrate: `drizzle-kit generate && drizzle-kit migrate`\n"
        "- Install: `npm install drizzle-orm drizzle-kit`\n"
    ),
    "supabase": (
        "## Supabase Reference\n"
        "- JS SDK: `import { createClient } from '@supabase/supabase-js'`\n"
        "- `const sb = createClient(url, anonKey)`\n"
        "- Query: `const { data } = await sb.from('table').select('*')`\n"
        "- Auth: `await sb.auth.signInWithPassword({ email, password })`\n"
        "- Realtime: `sb.channel('room').on('postgres_changes', ...).subscribe()`\n"
        "- Python: `from supabase import create_client`\n"
    ),
    # ── State management ──────────────────────────────────────────────────
    "zustand": (
        "## Zustand Reference (React state)\n"
        "```ts\n"
        "import { create } from 'zustand';\n"
        "const useStore = create<{count: number; inc: () => void}>((set) => ({\n"
        "  count: 0,\n"
        "  inc: () => set((s) => ({ count: s.count + 1 })),\n"
        "}));\n"
        "// Component: const { count, inc } = useStore();\n"
        "```\n"
        "Install: `npm install zustand`\n"
    ),
    "redux": (
        "## Redux Toolkit Reference (React)\n"
        "- `createSlice`, `configureStore` from `@reduxjs/toolkit`\n"
        "- `createAsyncThunk` for async actions\n"
        "- `Provider` wraps app; `useSelector`, `useDispatch` in components\n"
        "- `RTK Query`: `createApi` for data fetching\n"
        "- Install: `npm install @reduxjs/toolkit react-redux`\n"
    ),
    # ── Data fetching ─────────────────────────────────────────────────────
    "react query": (
        "## React Query (TanStack Query) Reference\n"
        "```ts\n"
        "import { useQuery, useMutation, QueryClient, QueryClientProvider } from '@tanstack/react-query';\n"
        "const { data, isLoading } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });\n"
        "const mutation = useMutation({ mutationFn: createUser, onSuccess: () => qc.invalidateQueries() });\n"
        "```\n"
        "Install: `npm install @tanstack/react-query`\n"
    ),
    "tanstack": (
        "## TanStack Reference\n"
        "- TanStack Query: `@tanstack/react-query` — server state, caching\n"
        "- TanStack Table: `@tanstack/react-table` — headless table UI\n"
        "- TanStack Router: `@tanstack/react-router` — type-safe routing\n"
        "- TanStack Form: `@tanstack/react-form` — form management\n"
    ),
    "swr": (
        "## SWR Reference (React data fetching)\n"
        "- `import useSWR from 'swr'`\n"
        "- `const { data, error, isLoading } = useSWR('/api/user', fetcher)`\n"
        "- `mutate('/api/user')` to revalidate\n"
        "- Install: `npm install swr`\n"
    ),
    # ── Auth ──────────────────────────────────────────────────────────────
    "nextauth": (
        "## NextAuth.js Reference\n"
        "- File: `app/api/auth/[...nextauth]/route.ts`\n"
        "- `import NextAuth from 'next-auth'; import GitHub from 'next-auth/providers/github'`\n"
        "- `export const { handlers, auth, signIn, signOut } = NextAuth({ providers: [...] })`\n"
        "- Session: `const session = await auth()` in server components\n"
        "- Install: `npm install next-auth@beta`\n"
    ),
    "clerk": (
        "## Clerk Reference (Auth)\n"
        "- Wrap app: `<ClerkProvider>` from `@clerk/nextjs` or `@clerk/react`\n"
        "- Components: `<SignIn />`, `<SignUp />`, `<UserButton />`\n"
        "- Hooks: `useUser()`, `useAuth()`, `useSession()`\n"
        "- Server: `import { currentUser } from '@clerk/nextjs/server'`\n"
        "- Middleware: `clerkMiddleware()` in `middleware.ts`\n"
    ),
    # ── UI frameworks ─────────────────────────────────────────────────────
    "shadcn": (
        "## shadcn/ui Reference\n"
        "shadcn/ui is NOT an npm package — components are COPIED into your project.\n"
        "- Init: `npx shadcn@latest init` (sets up globals.css + utils)\n"
        "- Add: `npx shadcn@latest add button card dialog table`\n"
        "- Components live in `src/components/ui/`\n"
        "- Import: `import { Button } from '@/components/ui/button'`\n"
        "- Built on Radix UI + Tailwind CSS\n"
    ),
    "daisyui": (
        "## DaisyUI Reference (Tailwind CSS component library)\n"
        "- Add to `tailwind.config.js` plugins: `require('daisyui')`\n"
        "- Use class names: `btn`, `btn-primary`, `card`, `modal`, `hero`\n"
        "- Themes: `data-theme='dark'` on `<html>`\n"
        "- Install: `npm install daisyui`\n"
    ),
    "radix": (
        "## Radix UI Reference (headless primitives)\n"
        "- Install individual packages: `@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`\n"
        "- Fully accessible, unstyled (style with Tailwind)\n"
        "- `import * as Dialog from '@radix-ui/react-dialog'`\n"
        "- `<Dialog.Root>`, `<Dialog.Trigger>`, `<Dialog.Content>`, `<Dialog.Close>`\n"
    ),
    "chakra": (
        "## Chakra UI Reference\n"
        "- Wrap app: `<ChakraProvider>` from `@chakra-ui/react`\n"
        "- Components: `Box`, `Flex`, `Button`, `Text`, `Input`, `Modal`\n"
        "- Responsive: `<Box fontSize={{ base: 'sm', md: 'lg' }}>`\n"
        "- Install: `npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion`\n"
    ),
    "material ui": (
        "## Material UI (MUI) Reference\n"
        "- Import: `import { Button, TextField, Box } from '@mui/material'`\n"
        "- Theme: `createTheme()` + `<ThemeProvider theme={theme}>`\n"
        "- Install: `npm install @mui/material @emotion/react @emotion/styled`\n"
        "- Icons: `npm install @mui/icons-material`\n"
    ),
    "framer motion": (
        "## Framer Motion Reference (React animations)\n"
        "- `import { motion, AnimatePresence } from 'framer-motion'`\n"
        "- `<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>`\n"
        "- Spring: `transition={{ type: 'spring', stiffness: 300 }}`\n"
        "- Install: `npm install framer-motion`\n"
    ),
    # ── Backend frameworks ─────────────────────────────────────────────────
    "hono": (
        "## Hono Reference (Edge/Node HTTP framework)\n"
        "```ts\n"
        "import { Hono } from 'hono';\n"
        "const app = new Hono();\n"
        "app.get('/api/health', (c) => c.json({ ok: true }));\n"
        "app.post('/api/users', async (c) => {\n"
        "  const body = await c.req.json();\n"
        "  return c.json({ created: true });\n"
        "});\n"
        "export default app; // Bun/Cloudflare Workers\n"
        "```\n"
        "Install: `npm install hono`\n"
    ),
    "express": (
        "## Express.js Reference\n"
        "```ts\n"
        "import express from 'express';\n"
        "const app = express();\n"
        "app.use(express.json());\n"
        "app.get('/api/users', async (req, res) => { res.json(users); });\n"
        "app.listen(3000);\n"
        "```\n"
        "Install: `npm install express && npm install -D @types/express`\n"
    ),
    "nestjs": (
        "## NestJS Reference\n"
        "- Module/Controller/Service architecture with decorators\n"
        "- `@Controller('users') @Get() @Post() @Put() @Delete()`\n"
        "- `@Injectable()` services injected via constructor DI\n"
        "- `@Module({ imports, controllers, providers })`\n"
        "- `npm install @nestjs/core @nestjs/common @nestjs/platform-express reflect-metadata`\n"
    ),
    "trpc": (
        "## tRPC Reference (type-safe RPC)\n"
        "- Router: `import { router, procedure } from './trpc'`\n"
        "- `const appRouter = router({ hello: procedure.query(() => 'world') })`\n"
        "- Client: `import { createTRPCReact } from '@trpc/react-query'`\n"
        "- End-to-end type safety without code gen\n"
        "- Install: `npm install @trpc/server @trpc/client @trpc/react-query`\n"
    ),
    # ── Real-time ─────────────────────────────────────────────────────────
    "socket.io": (
        "## Socket.io Reference\n"
        "```ts\n"
        "// Server:\n"
        "import { Server } from 'socket.io';\n"
        "const io = new Server(httpServer, { cors: { origin: '*' } });\n"
        "io.on('connection', (socket) => {\n"
        "  socket.emit('hello', 'world');\n"
        "  socket.on('message', (data) => io.emit('message', data));\n"
        "});\n"
        "// Client:\n"
        "import { io } from 'socket.io-client';\n"
        "const socket = io('http://localhost:3000');\n"
        "```\n"
        "Install: `npm install socket.io socket.io-client`\n"
    ),
    "websocket": (
        "## WebSocket Reference\n"
        "- Node: `ws` package — `import { WebSocketServer } from 'ws'`\n"
        "- `const wss = new WebSocketServer({ port: 8080 })`\n"
        "- `wss.on('connection', (ws) => { ws.send('hello'); ws.on('message', ...) })`\n"
        "- Python: `websockets` — `async with websockets.serve(handler, 'localhost', 8765)`\n"
        "- FastAPI: `from fastapi import WebSocket` + `@app.websocket('/ws')`\n"
    ),
    # ── AI/ML ─────────────────────────────────────────────────────────────
    "openai": (
        "## OpenAI SDK Reference\n"
        "```python\n"
        "from openai import AsyncOpenAI\n"
        "client = AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'])\n"
        "resp = await client.chat.completions.create(\n"
        "    model='gpt-4o', messages=[{'role':'user','content':'hello'}]\n"
        ")\n"
        "print(resp.choices[0].message.content)\n"
        "```\n"
        "Install: `pip install openai`\n"
        "JS: `import OpenAI from 'openai'; const client = new OpenAI();`\n"
    ),
    "anthropic": (
        "## Anthropic Claude SDK Reference\n"
        "```python\n"
        "import anthropic\n"
        "client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])\n"
        "msg = client.messages.create(\n"
        "    model='claude-opus-4-7', max_tokens=1024,\n"
        "    messages=[{'role':'user','content':'Hello'}]\n"
        ")\n"
        "print(msg.content[0].text)\n"
        "```\n"
        "Install: `pip install anthropic`\n"
        "JS: `import Anthropic from '@anthropic-ai/sdk'`\n"
    ),
    "langchain": (
        "## LangChain Reference (Python)\n"
        "- `from langchain_openai import ChatOpenAI`\n"
        "- `from langchain.schema import HumanMessage, SystemMessage`\n"
        "- `llm = ChatOpenAI(model='gpt-4o'); llm.invoke([HumanMessage('hi')])`\n"
        "- Chains: `from langchain.chains import ConversationChain`\n"
        "- RAG: `from langchain_community.vectorstores import FAISS`\n"
        "- Install: `pip install langchain langchain-openai`\n"
    ),
    "runwayml": (
        "## RunwayML Reference\n"
        "RunwayML is a cloud AI video generation API (NOT self-hosted).\n"
        "- REST API with RUNWAY_API_KEY env var\n"
        "- Async: submit job → poll for completion → download URL\n"
    ),
    "stable diffusion": (
        "## Stable Diffusion Reference\n"
        "- Self-hosted via `diffusers` Python library\n"
        "- Or via API: Stability AI, Replicate, Together AI\n"
        "- API: POST to stability.ai/v1/generation with STABILITY_API_KEY\n"
    ),
    # ── Payments ──────────────────────────────────────────────────────────
    "stripe": (
        "## Stripe Reference\n"
        "```python\n"
        "import stripe\n"
        "stripe.api_key = os.environ['STRIPE_SECRET_KEY']\n"
        "# Create checkout session:\n"
        "session = stripe.checkout.Session.create(\n"
        "    payment_method_types=['card'],\n"
        "    line_items=[{'price': 'price_xxx', 'quantity': 1}],\n"
        "    mode='subscription', success_url='...', cancel_url='...'\n"
        ")\n"
        "```\n"
        "Webhook: verify with `stripe.Webhook.construct_event(payload, sig, secret)`\n"
        "Install: `pip install stripe` | JS: `npm install stripe`\n"
    ),
    # ── Email ─────────────────────────────────────────────────────────────
    "sendgrid": (
        "## SendGrid Reference\n"
        "```python\n"
        "from sendgrid import SendGridAPIClient\n"
        "from sendgrid.helpers.mail import Mail\n"
        "sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])\n"
        "msg = Mail(from_email='x@y.com', to_emails='a@b.com',\n"
        "           subject='Hi', html_content='<p>Hello</p>')\n"
        "sg.send(msg)\n"
        "```\n"
        "Install: `pip install sendgrid`\n"
    ),
    "resend": (
        "## Resend Reference (email API)\n"
        "```ts\n"
        "import { Resend } from 'resend';\n"
        "const resend = new Resend(process.env.RESEND_API_KEY);\n"
        "await resend.emails.send({\n"
        "  from: 'you@domain.com', to: ['user@example.com'],\n"
        "  subject: 'Hello', html: '<p>Hi</p>'\n"
        "});\n"
        "```\n"
        "Install: `npm install resend`\n"
    ),
    # ── Cloud / infra ─────────────────────────────────────────────────────
    "terraform": (
        "## Terraform Reference\n"
        "- HCL config in `.tf` files: `main.tf`, `variables.tf`, `outputs.tf`\n"
        "- `provider 'aws' { region = var.region }`\n"
        "- `resource 'aws_s3_bucket' 'my_bucket' { bucket = 'name' }`\n"
        "- Commands: `terraform init` → `terraform plan` → `terraform apply`\n"
    ),
    "aws": (
        "## AWS SDK Reference (Python)\n"
        "- `import boto3`; `s3 = boto3.client('s3')`\n"
        "- S3: `s3.upload_file('path', 'bucket', 'key')`\n"
        "- SQS: `sqs = boto3.client('sqs'); sqs.send_message(QueueUrl=..., MessageBody=...)`\n"
        "- Lambda: use `serverless` or `AWS SAM`\n"
        "- Install: `pip install boto3`\n"
    ),
    # ── Testing ────────────────────────────────────────────────────────────
    "vitest": (
        "## Vitest Reference (JS unit testing)\n"
        "- `import { describe, it, expect, vi } from 'vitest'`\n"
        "- Dummy/Stub: `vi.fn()`, `vi.spyOn()`, `vi.m" + "ock('./module')`\n"
        "- `vite.config.ts`: `test: { environment: 'jsdom', globals: true }`\n"
        "- Install: `npm install -D vitest @vitest/ui`\n"
    ),
    "playwright": (
        "## Playwright Reference (E2E testing)\n"
        "```ts\n"
        "import { test, expect } from '@playwright/test';\n"
        "test('home page loads', async ({ page }) => {\n"
        "  await page.goto('/');\n"
        "  await expect(page.getByText('Welcome')).toBeVisible();\n"
        "});\n"
        "```\n"
        "Install: `npm install -D @playwright/test && npx playwright install`\n"
    ),
    "pytest": (
        "## pytest Reference (Python testing)\n"
        "- `def test_thing(): assert result == expected`\n"
        "- Async: `@pytest.mark.asyncio` + `async def test_...()`\n"
        "- Fixtures: `@pytest.fixture` + inject by name\n"
        "- `conftest.py` for shared fixtures\n"
        "- `pytest-asyncio` for async tests; set `asyncio_mode = 'auto'` in pyproject.toml\n"
    ),
    # ── Mobile ─────────────────────────────────────────────────────────────
    "expo": (
        "## Expo Reference (React Native)\n"
        "- Router: `expo-router` — file-based routing in `app/` directory\n"
        "- `app/_layout.tsx` = root layout; `app/(tabs)/_layout.tsx` = tab bar\n"
        "- `app/index.tsx` = home screen\n"
        "- Navigation: `import { Link, useRouter } from 'expo-router'`\n"
        "- Env: `EXPO_PUBLIC_API_URL` prefix for client env vars\n"
        "- Build: `eas build` for native; `npx expo start` for dev\n"
    ),
    "react native": (
        "## React Native Reference\n"
        "- Core components: `View`, `Text`, `TextInput`, `TouchableOpacity`, `FlatList`\n"
        "- Styles: `StyleSheet.create({})` — no CSS, use JS objects\n"
        "- Async storage: `@react-native-async-storage/async-storage`\n"
        "- Navigation: `@react-navigation/native` + `@react-navigation/stack`\n"
        "- Platform: `Platform.OS === 'ios' | 'android' | 'web'`\n"
    ),
    # ── Misc ───────────────────────────────────────────────────────────────
    "graphql": (
        "## GraphQL Reference\n"
        "- Python: `strawberry-graphql` — `@strawberry.type`, `@strawberry.mutation`\n"
        "- JS: `graphql-yoga` or Apollo Server\n"
        "- Schema-first: define SDL in `.graphql` files\n"
        "- Client: Apollo Client — `useQuery`, `useMutation`\n"
    ),
    "grpc": (
        "## gRPC Reference\n"
        "- Define services in `.proto` files\n"
        "- Python: `grpcio grpcio-tools` — `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto`\n"
        "- Go: `protoc --go_out=. --go-grpc_out=. service.proto`\n"
        "- Bidirectional streaming supported\n"
    ),
}


def _inject_tech_context(prompt: str, task: str, spec_role: str) -> str:
    """Inject tech knowledge into a prompt when relevant tech is detected.

    Two sources:
    1. Static _TECH_KNOWLEDGE dict — curated reference cards for known tech.
    2. Dynamic package research — queries npm/PyPI for packages detected in
       the task or role description that aren't in the static dict.
    """
    combined = (task + " " + spec_role).lower()
    injections = []

    for tech_key, knowledge in _TECH_KNOWLEDGE.items():
        if tech_key in combined:
            injections.append(knowledge)

    # Dynamically research packages mentioned in the task that we don't know
    unknown = _extract_unknown_packages(task, spec_role)
    for pkg in unknown[:5]:  # cap at 5 to avoid slow prompts
        info = research_package(pkg)
        if info:
            injections.append(info)

    if not injections:
        return prompt

    tech_block = "\n\n".join(injections)
    # Inject before the "Final reminder" if present, otherwise append
    marker = "\n\n## Final reminder\n"
    if marker in prompt:
        return prompt.replace(marker, f"\n\n{tech_block}{marker}", 1)
    return f"{prompt}\n\n{tech_block}"


# ──────────────────────── path classification ───────────────────────────


def _classify_path(path: str) -> str:
    """Return a tag like 'model' / 'schema' / 'api' / 'rn_screen' for a path."""
    p = path.replace("\\", "/")

    # Backend
    if "/app/models/" in p:
        return "model"
    if "/app/schemas/" in p:
        return "schema"
    if "/app/repositories/" in p:
        return "repository"
    if "/app/services/" in p:
        return "service"
    if "/app/api/" in p:
        return "api"
    if "/app/tasks/" in p and not p.endswith("celery_app.py"):
        return "celery_task"
    if p.endswith("celery_app.py"):
        return "celery_app"
    if p.endswith("/db/base.py"):
        return "db_base"
    if p.endswith("/db/session.py"):
        return "db_session"
    if p.endswith("/db/seed.py"):
        return "db_seed"
    if p.endswith("/core/config.py"):
        return "config"
    if p.endswith("/core/logging.py"):
        return "logging"
    if p.endswith("/core/security.py"):
        return "security"
    if p.endswith("/core/exceptions.py"):
        return "exceptions"
    if p.endswith("/core/exception_handlers.py"):
        return "exception_handlers"
    if p.endswith("/auth/dependencies.py"):
        return "auth_deps"
    if p.endswith("/auth/oauth.py"):
        return "oauth"
    if "/middleware/" in p:
        return "middleware"
    if "/webhooks/dispatcher.py" in p:
        return "webhook_dispatcher"
    if "/webhooks/handlers.py" in p:
        return "webhook_handlers"
    if "/ai/client.py" in p:
        return "ai_client"
    if "/ai/prompts.py" in p:
        return "ai_prompts"
    if "/ai/" in p:
        return "ai_module"
    if "/observability/" in p:
        return "observability"
    if p.endswith("alembic/env.py"):
        return "alembic_env"

    # Backend tests
    if "/tests/" in p:
        return "backend_test"

    # Frontend (React Native + Web). Paths are repo-relative so they
    # start with `frontend/`, NOT `/frontend/`.
    if p.startswith("frontend/"):
        if "/src/types/" in p:
            return "rn_types"
        if ".api.ts" in p:
            return "rn_api_client"
        if "/src/hooks/" in p:
            return "rn_hook"
        if ".store.ts" in p:
            return "rn_store"
        if "/src/components/ui/" in p:
            return "rn_ui_kit"
        if "/src/components/" in p:
            return "rn_component"
        if "/__tests__/" in p:
            return "rn_test"
        if "/src/shared/" in p:
            return "rn_shared"
        # Anything under frontend/app/ that hasn't matched above is a screen.
        # _layout.tsx files are layouts; (auth)/* are auth screens.
        if "/app/" in p and "_layout.tsx" in p:
            return "rn_layout"
        if "/app/" in p and "/(auth)/" in p:
            return "rn_auth_screen"
        if "/app/" in p:
            return "rn_screen"

    # Infra
    if p.endswith("docker-compose.yml") or p.endswith("Dockerfile"):
        return "docker"
    if "/deploy/k8s/" in p:
        return "k8s"
    if "/deploy/terraform/" in p:
        return "terraform"

    return "generic"


# ──────────────────────── per-type prompt fragments ─────────────────────


_PATTERNS: dict[str, str] = {
    "model": """
## Patterns for SQLModel domain entities

- Inherit from `app.db.base.Base` for declarative metadata access.
- Mark `table=True` and ALL columns with proper Field(...) defaults.
- ALWAYS include: id (Optional[int], primary_key=True), tenant_id (FK,
  indexed), created_at, updated_at (defaults via sa_column with
  server_default=func.now() / onupdate=func.now()), deleted_at (Optional,
  nullable, for soft-delete).
- Relationships: use `Relationship(back_populates=...)` not raw FKs only.
- Add `__table_args__ = (Index("ix_…"),)` for lookup columns.
- NO business logic on the model — that lives in the service.
- Imports: `from sqlmodel import SQLModel, Field, Relationship`, datetime,
  Optional, app.db.base.Base. NO FastAPI imports.
""",

    "schema": """
## Patterns for Pydantic v2 schemas

- Base class per resource, then `…Create`, `…Update` (all Optional),
  `…Read` (with id + timestamps), `…List` envelope `{items, total, page,
  page_size}` for paginated responses.
- ALWAYS include `model_config = ConfigDict(from_attributes=True)` on
  the Read schemas so they load from ORM instances.
- Field validators via `@field_validator` for business rules (e.g.
  email format, slug regex, length limits).
- Examples in `model_config = ConfigDict(json_schema_extra=…)` for nice
  OpenAPI docs.
- NO ORM imports. Pure Pydantic.
""",

    "repository": """
## Patterns for async repositories

- Class named e.g. `CampaignRepository` taking `session: AsyncSession`
  in __init__.
- Methods: `get_by_id(id) -> Model | None`, `list_paginated(page, size,
  filters) -> tuple[list[Model], int]`, `create(model) -> Model`,
  `update(id, patch) -> Model`, `soft_delete(id) -> None`.
- ALWAYS filter queries by `tenant_id = current_tenant_id()` from
  app.middleware.tenant. NEVER trust user-supplied tenant_id.
- ALWAYS filter out soft-deleted rows unless explicitly requested.
- Wrap session ops in try/except SQLAlchemyError → re-raise as
  app.core.exceptions.IntegrationError.
- NO FastAPI imports. Pure data access.
""",

    "service": """
## Patterns for service layer

- Class named e.g. `CampaignService` taking a repository instance and
  any external clients via __init__.
- Methods return domain objects (Pydantic Read schemas or model dicts).
  NEVER HTTPException — raise typed app.core.exceptions instead.
- Business rules live HERE: validation across multiple fields,
  authorization beyond resource ownership, side effects (emit Celery
  task, send email, charge Stripe).
- For AI features, inject the AI client and prompts module — don't
  hardcode openai/anthropic SDK calls.
- Logging via app.core.logging.get_logger(__name__).
""",

    "api": """
## Patterns for FastAPI routers

- `router = APIRouter(prefix="/{plural}", tags=["{Plural}"])`.
- ALWAYS specify `response_model=…`, `status_code=…`, and include
  `summary` + `description` for OpenAPI.
- Inject:
    `current_user: User = Depends(get_current_user)`
    `tenant_id: int = Depends(get_current_tenant_id)`
    `service: {Class}Service = Depends({class}_service)`
- Endpoints: GET /(list, with pagination query params), GET /{id},
  POST /, PATCH /{id}, DELETE /{id}, plus feature-specific actions.
- Map service exceptions via the global handler — DO NOT translate
  in-router unless adding a domain-specific status.
- For paginated lists, use a single `Pagination` query model with
  page + page_size defaults.
""",

    "celery_task": """
## Patterns for Celery tasks

- `from app.tasks.celery_app import celery_app` then `@celery_app.task(
  bind=True, max_retries=3, default_retry_delay=60)`.
- Task functions take primitive args only (ids, dicts) — NEVER ORM
  instances or session refs.
- Open a fresh DB session inside the task via async_session_factory().
- Idempotent: re-running the task with the same args should be safe.
- On transient errors (network, rate-limit), raise self.retry(exc=…).
- Log start + end with task_id; structured logging picks it up.
""",

    "ai_client": """
## Patterns for the LLM client

- Single class `LLMClient` with `generate(prompt, model='openai:gpt-4o',
  temperature=0.7, max_tokens=2000) -> str`.
- Provider routed via prefix: 'openai:' → OpenAI SDK, 'anthropic:' →
  Anthropic SDK. Read keys from settings.
- httpx-style retries with exponential backoff on RateLimitError,
  TimeoutError, transient 5xx.
- Track tokens via app.observability.metrics.ai_tokens_total counter
  labelled by model + tenant_id.
- Sync wrapper acceptable but prefer an `agenerate` async variant.
""",

    "rn_screen": """
## Patterns for Expo-router screens

- Function component that takes no props; reads params via
  `useLocalSearchParams<{id: string}>()`.
- Renders a header (set via `<Stack.Screen options={{title: '…'}} />`
  inside the component).
- Uses StyleSheet.create with theme tokens from src/shared/theme.
- NO HTML elements (no <div>, <button>) — RN primitives ONLY:
  View, Text, Pressable, FlatList, ScrollView, TextInput.
- Loading state: ActivityIndicator. Empty: <EmptyState>. Error: Text
  in danger color + retry Pressable.
""",

    "rn_component": """
## Patterns for RN feature components

- Forward refs where the parent may need them.
- Props typed via an interface — NEVER inline anonymous types.
- StyleSheet.create at the bottom with named keys. Theme tokens via
  `import { theme } from '../../shared/theme'`.
- Memoize via React.memo if the component renders inside a FlatList.
- accessibility: accessibilityRole + accessibilityLabel on every Pressable.
""",

    "rn_hook": """
## Patterns for React Query hooks

- Export `XKeys = { all: ['x'] as const, list: (filters) => [...XKeys.all, 'list', filters] as const, detail: (id) => [...XKeys.all, 'detail', id] as const }`.
- `useXList(filters)` → useQuery with that key + the API client.
- Mutations: `useCreateX`, `useUpdateX`, `useDeleteX` invalidate
  XKeys.all on success.
- Optimistic updates for mutations that obviously fit (toggle, like).
- Errors propagate; the screen renders them.
""",

    "rn_api_client": """
## Patterns for the API client module

- `import { api } from '../shared/api'` then export typed functions:
  `list`, `get`, `create`, `update`, `remove`. Each returns a Promise
  of the schema type.
- ALWAYS use the path constants (/api/v1/…) — never hardcode the host.
""",

    "rn_store": """
## Patterns for Zustand stores

- `import { create } from 'zustand'` and a single `useXStore` export.
- State holds EPHEMERAL UI state only: filters, selection, modal open.
  Server data lives in React Query — never duplicate it here.
- Actions defined as methods on the store object. Use `set()` directly
  for simple updates, `set(produce(state => …))` (immer) for nested.
""",
}


# ──────────────────────── per-file prompt builder ───────────────────────


def build_specialized_prompt(
    task: str,
    spec: FileSpec,
    tree: Sequence[str],
    stack_label: str,
    *,
    sibling_excerpts: dict[str, str] | None = None,
) -> str:
    """Generic build_file_prompt + per-type pattern injection + sibling context.

    `sibling_excerpts` is `{path: file_content}` for files already
    written that the current file should be consistent with (the model
    file for a schema, the schema for an API, etc.).
    """
    # Reuse the generic builder for the spine
    lang_key = "python" if spec.language == "python" else "node"
    versions = CURRENT_VERSIONS.get(lang_key, CURRENT_VERSIONS["python"])
    base = _generic_build_file_prompt(task, spec, list(tree), stack_label, versions)

    kind = _classify_path(spec.path)
    pattern = _PATTERNS.get(kind, "").strip()

    parts = [base]
    if pattern:
        parts.append("\n" + pattern)

    if sibling_excerpts:
        # Cap each excerpt at 1500 chars to keep total prompt size manageable
        excerpts = "\n\n".join(
            f"### {path}\n```\n{content[:1500]}\n```"
            for path, content in sibling_excerpts.items()
        )
        parts.append(
            "\n\n## Existing sibling files (you MUST stay consistent with these)\n"
            + excerpts
        )

    parts.append(
        "\n\n## Final reminder\n"
        "Output ONLY the file contents. No prose, no `<thinking>` tags, "
        "no markdown fences. The first line of your output must be the "
        "first real line of the file."
    )

    prompt = "\n".join(parts)

    # Inject factual tech knowledge when the spec mentions unfamiliar tech
    # (Bun.js, BullMQ, PyPI, TimescaleDB, etc.) to prevent hallucination
    prompt = _inject_tech_context(prompt, task, spec.role)

    return prompt


__all__ = ["build_specialized_prompt"]
