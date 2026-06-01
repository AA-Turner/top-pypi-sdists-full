/** Curated known models per provider — always up-to-date model list. */

export interface KnownModel {
  id: string
  label: string
  ctx: string
}

export const PROVIDER_MODELS: Record<string, KnownModel[]> = {
  openai: [
    { id: 'gpt-4o',            label: 'GPT-4o',             ctx: '128k' },
    { id: 'gpt-4o-mini',       label: 'GPT-4o mini',        ctx: '128k' },
    { id: 'gpt-4.1',           label: 'GPT-4.1',            ctx: '1M'   },
    { id: 'gpt-4.1-mini',      label: 'GPT-4.1 mini',       ctx: '1M'   },
    { id: 'o3',                label: 'o3',                 ctx: '200k' },
    { id: 'o4-mini',           label: 'o4-mini',            ctx: '200k' },
    { id: 'gpt-5.5',           label: 'GPT-5.5 (Codex)',    ctx: '128k' },
    { id: 'codex-mini-latest', label: 'Codex Mini Latest',  ctx: '200k' },
  ],
  anthropic: [
    { id: 'claude-opus-4-7',            label: 'Claude Opus 4.7',   ctx: '200k' },
    { id: 'claude-sonnet-4-6',          label: 'Claude Sonnet 4.6', ctx: '200k' },
    { id: 'claude-haiku-4-5-20251001',  label: 'Claude Haiku 4.5',  ctx: '200k' },
    { id: 'claude-3-7-sonnet-20250219', label: 'Claude 3.7 Sonnet', ctx: '200k' },
    { id: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet', ctx: '200k' },
    { id: 'claude-3-5-haiku-20241022',  label: 'Claude 3.5 Haiku',  ctx: '200k' },
  ],
  'claude-cli': [
    { id: 'claude-opus-4-7',           label: 'Claude Opus 4.7',   ctx: '200k' },
    { id: 'claude-sonnet-4-6',         label: 'Claude Sonnet 4.6', ctx: '200k' },
    { id: 'claude-haiku-4-5-20251001', label: 'Claude Haiku 4.5',  ctx: '200k' },
  ],
  // ollama and openrouter: populated dynamically from server
  ollama: [],
  openrouter: [],
}

export const PROVIDER_ORDER = ['openai', 'anthropic', 'ollama', 'openrouter', 'claude-cli']

export const PROVIDER_COLORS: Record<string, string> = {
  openai:       '#10a37f',
  anthropic:    '#d97706',
  ollama:       '#60a5fa',
  openrouter:   '#a78bfa',
  'claude-cli': '#f472b6',
}
