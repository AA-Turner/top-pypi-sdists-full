/**
 * codrninja · TUI Design Tokens
 * ──────────────────────────────
 * Exact same hex values as the HTML design mockup.
 * Import into every component for guaranteed visual consistency.
 *
 * Usage:  import { C, LOGO, TYPING_MSGS, SLASH_COMMANDS } from './styles';
 */

export const C = {
  acc: '#ff6b35',   // orange accent  — prompts, active items, live tokens
  dim: '#55556a',   // dimmed         — labels, hints, timestamps
  txt: '#c4c4d4',   // body text      — general content
  wh:  '#f0f0f5',   // bright/bold    — user messages
  grn: '#4ade80',   // success        — tool ✓, connected providers
  red: '#f87171',   // error          — tool ✗, failures
  cyn: '#67e8f9',   // cyan/ninja     — AI responses
  mnt: '#c084fc',   // purple         — code keywords
} as const;

export const LOGO =
`  ██████╗ ██████╗ ██████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗     ██╗ █████╗
 ██╔════╝██╔═══██╗██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║     ██║██╔══██╗
 ██║     ██║   ██║██║  ██║██████╔╝██╔██╗ ██║██║██╔██╗ ██║     ██║███████║
 ██║     ██║   ██║██║  ██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██   ██║██╔══██║
 ╚██████╗╚██████╔╝██████╔╝██║  ██║██║ ╚████║██║██║ ╚████║╚█████╔╝██║  ██║
  ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚════╝ ╚═╝  ╚═╝`;

/** Cycles while waiting for AI response — ~2.6 s per message */
export const TYPING_MSGS: readonly string[] = [
  '🥷  infiltrating the codebase...',
  '⚔️   sharpening the katana...',
  '📜  consulting the ancient scrolls...',
  '🌑  moving through the shadows...',
  '🎯  plotting the perfect strike...',
  '🔮  channeling inner ninja focus...',
  '👁️   scanning with precision...',
  '🌊  flowing like water...',
  '🐉  awakening ancient wisdom...',
  '⚡  lightning speed analysis...',
];

export const SLASH_COMMANDS: Record<string, string> = {
  '/help':    'Show all commands',
  '/files':   'List project files',
  '/read':    'Read a file  /read <path>',
  '/write':   'Write a file  /write <path>',
  '/exec':    'Run a shell command  /exec <cmd>',
  '/model':   'Show AI model config',
  '/session': 'Show session info',
  '/clear':   'Clear the screen',
  '/exit':    'Quit codrninja',
};
