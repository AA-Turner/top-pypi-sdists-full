import * as vscode from 'vscode';
import { runCVC } from './utils';

export class CvcDashboard {
  private panel: vscode.WebviewPanel | undefined;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
  }

  async open(): Promise<void> {
    if (this.panel) {
      this.panel.reveal(vscode.ViewColumn.One);
      await this.refresh();
      return;
    }

    this.panel = vscode.window.createWebviewPanel(
      'cvcDashboard',
      '⚡ CVC Dashboard',
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
      },
    );

    this.panel.onDidDispose(() => {
      this.panel = undefined;
    });

    this.panel.webview.onDidReceiveMessage(async (msg: { command: string; hash?: string; branch?: string }) => {
      switch (msg.command) {
        case 'commit': {
          const m = await vscode.window.showInputBox({ prompt: 'Commit message', placeHolder: 'Describe this context checkpoint…' });
          if (m) {
            await runCVC(`commit -m "${m}"`).catch(e => vscode.window.showErrorMessage(String(e)));
            await this.refresh();
          }
          break;
        }
        case 'restore':
          if (msg.hash) {
            const ok = await vscode.window.showWarningMessage(`Restore to commit ${msg.hash}?`, 'Restore', 'Cancel');
            if (ok === 'Restore') {
              await runCVC(`restore ${msg.hash}`).catch(e => vscode.window.showErrorMessage(String(e)));
              await this.refresh();
            }
          }
          break;
        case 'switchBranch':
          if (msg.branch) {
            await runCVC(`branch ${msg.branch}`).catch(e => vscode.window.showErrorMessage(String(e)));
            await this.refresh();
          }
          break;
        case 'refresh':
          await this.refresh();
          break;
      }
    });

    await this.refresh();
  }

  private async refresh(): Promise<void> {
    if (!this.panel) return;

    let status = '';
    let log = '';
    let branches = '';

    try { status = await runCVC('status'); } catch { status = 'CVC not initialised'; }
    try { log = await runCVC('log --limit 10'); } catch { log = ''; }
    try { branches = await runCVC('branch --list'); } catch { branches = ''; }

    this.panel.webview.html = this.buildHtml(status, log, branches);
  }

  private parseLog(logText: string): Array<{ hash: string; message: string; time: string }> {
    return logText.split('\n')
      .filter(l => l.trim())
      .map(line => {
        const m = line.match(/^([a-f0-9]{7,12})\s+(.+?)(?:\s{2,}(.*))?$/);
        if (m) return { hash: m[1], message: m[2].trim(), time: (m[3] ?? '').trim() };
        return { hash: '', message: line.trim().substring(0, 70), time: '' };
      });
  }

  private parseBranches(branchText: string): Array<{ name: string; active: boolean }> {
    return branchText.split('\n')
      .filter(l => l.trim())
      .map(line => {
        const active = line.trim().startsWith('*');
        const name = line.replace(/^\*?\s*/, '').trim();
        return { name, active };
      });
  }

  private buildHtml(status: string, log: string, branches: string): string {
    const commits = this.parseLog(log);
    const branchList = this.parseBranches(branches);

    const commitRows = commits.length > 0
      ? commits.map(c => `
        <div class="commit-row" onclick="restore('${c.hash}')">
          <span class="commit-hash">${c.hash || '—'}</span>
          <span class="commit-msg">${escHtml(c.message)}</span>
          <span class="commit-time">${escHtml(c.time)}</span>
        </div>`).join('')
      : '<div class="empty">No commits yet. Start a session and commit!</div>';

    const branchRows = branchList.length > 0
      ? branchList.map(b => `
        <div class="branch-row ${b.active ? 'active' : ''}" onclick="switchBranch('${escHtml(b.name)}')">
          <span class="branch-icon">⎇</span>
          <span class="branch-name">${escHtml(b.name)}</span>
          ${b.active ? '<span class="badge">current</span>' : ''}
        </div>`).join('')
      : '<div class="empty">No branches found.</div>';

    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>CVC Dashboard</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: system-ui, -apple-system, sans-serif;
    background: #0f0f1a;
    color: #e2e8f0;
    padding: 0;
    min-height: 100vh;
  }
  .header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    padding: 24px 28px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .header-icon { font-size: 32px; }
  .header-title { font-size: 22px; font-weight: 700; color: #fff; }
  .header-sub { font-size: 13px; color: rgba(255,255,255,0.75); margin-top: 2px; }
  .actions {
    display: flex;
    gap: 10px;
    padding: 16px 28px;
    background: #13131f;
    border-bottom: 1px solid #1e1e2e;
  }
  .btn {
    padding: 8px 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.15s;
  }
  .btn-primary { background: linear-gradient(135deg,#6366f1,#8b5cf6); color: #fff; }
  .btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
  .btn-secondary { background: #1e1e2e; color: #a0aec0; border: 1px solid #2d2d3e; }
  .btn-secondary:hover { background: #2d2d3e; color: #e2e8f0; }
  .content { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
  .panel { padding: 20px 28px; }
  .panel + .panel { border-left: 1px solid #1e1e2e; }
  .panel-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6366f1;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .commit-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.1s;
    margin-bottom: 4px;
    border: 1px solid transparent;
  }
  .commit-row:hover { background: #1a1a2e; border-color: #6366f1; }
  .commit-hash {
    font-family: 'SF Mono', monospace;
    font-size: 11px;
    color: #8b5cf6;
    min-width: 60px;
    background: #1e1e2e;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .commit-msg { flex: 1; font-size: 13px; color: #cbd5e0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .commit-time { font-size: 11px; color: #4a5568; min-width: 60px; text-align: right; }
  .branch-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.1s;
    margin-bottom: 4px;
    border: 1px solid transparent;
  }
  .branch-row:hover { background: #1a1a2e; border-color: #6366f1; }
  .branch-row.active { border-color: #8b5cf6; background: #1a1a2e; }
  .branch-icon { font-size: 14px; color: #8b5cf6; }
  .branch-name { flex: 1; font-size: 13px; }
  .badge {
    font-size: 10px;
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    color: #fff;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
  }
  .status-box {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: 'SF Mono', monospace;
    font-size: 12px;
    color: #a0aec0;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 120px;
    overflow: auto;
    margin-bottom: 16px;
  }
  .empty { color: #4a5568; font-size: 13px; padding: 12px 0; }
  .full-panel { grid-column: 1 / -1; }
  @media (max-width: 600px) { .content { grid-template-columns: 1fr; } .panel + .panel { border-left: none; border-top: 1px solid #1e1e2e; } }
</style>
</head>
<body>
<div class="header">
  <div class="header-icon">🧠</div>
  <div>
    <div class="header-title">CVC Dashboard</div>
    <div class="header-sub">Cognitive Version Control — Git for your AI brain</div>
  </div>
</div>
<div class="actions">
  <button class="btn btn-primary" onclick="commit()">⚡ Commit Context</button>
  <button class="btn btn-secondary" onclick="refresh()">↻ Refresh</button>
</div>
<div class="content">
  <div class="panel full-panel" style="padding-bottom:0">
    <div class="panel-title">📊 Status</div>
    <div class="status-box">${escHtml(status)}</div>
  </div>
  <div class="panel">
    <div class="panel-title">🕒 Commit History</div>
    ${commitRows}
  </div>
  <div class="panel">
    <div class="panel-title">⎇ Branches</div>
    ${branchRows}
  </div>
</div>
<script>
  const vscode = acquireVsCodeApi();
  function commit() { vscode.postMessage({ command: 'commit' }); }
  function restore(hash) { if (hash) vscode.postMessage({ command: 'restore', hash }); }
  function switchBranch(branch) { vscode.postMessage({ command: 'switchBranch', branch }); }
  function refresh() { vscode.postMessage({ command: 'refresh' }); }
</script>
</body>
</html>`;

    function escHtml(s: string): string {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  }

  dispose(): void {
    this.panel?.dispose();
  }
}
