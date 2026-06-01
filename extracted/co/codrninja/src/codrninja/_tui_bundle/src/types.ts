/** @deprecated use Phase/Modal instead */
export type Screen = 'sessions' | 'chat' | 'model-select' | 'provider-select' | 'provider-config' | 'onboarding';

// ── App state machine ─────────────────────────────────────────────────────────

export type Phase =
  | { tag: 'loading'; retries: number }
  | { tag: 'error'; msg: string }
  | { tag: 'onboarding' }
  | { tag: 'sessions' }
  | { tag: 'chat'; session: string; history: ChatMessage[]; model: string; provider: string; permMode: string; running: boolean }

/** Overlays rendered on top of the current Phase. null = no overlay. */
export type Modal =
  | null
  | { type: 'model-select' }
  | { type: 'provider-select' }
  | { type: 'provider-config'; providerName: string }
  | { type: 'config' }

export type ModelRef = { provider: string; model: string }

export interface ToolCall {
  call_id: string;
  tool: string;
  args: Record<string, unknown>;
  step: number;
  output?: string;
  success?: boolean;
  done: boolean;
  permMode?: string;
  durationMs?: number;
  lineStart?: number;
  contextBefore?: string[];
  contextAfter?: string[];
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'tool' | 'pre_tool';
  content: string;
  streaming?: boolean;
  toolData?: ToolCall;
  tokens?: number;
  tokensIn?: number;
  isThinkingComplete?: boolean;
  thinkingMs?: number;
  thinkingLabel?: string;
  thinkingIter?: number;
  thinkingTools?: number;
  isModelSwitch?: boolean;
  switchModel?: string;
  switchProvider?: string;
  contextData?: {
    tokIn: number;
    tokOut: number;
    maxCtx?: number;
    sessionName: string;
    provider: string;
    model: string;
    exchangeCount: number;
  };
}
