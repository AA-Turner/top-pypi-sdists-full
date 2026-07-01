import * as vscode from 'vscode';
import { runCVC, formatTimestamp } from './utils';

export class CvcStatusBar {
  private item: vscode.StatusBarItem;
  private refreshInterval: ReturnType<typeof setInterval> | undefined;

  constructor() {
    this.item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    this.item.command = 'cvc.openDashboard';
    this.item.tooltip = 'CVC — Click to open dashboard';
    this.item.text = '$(brain) CVC: loading…';
    this.item.show();
  }

  async refresh(): Promise<void> {
    try {
      const status = await runCVC('status --short');
      const branch = this.parseBranch(status);
      const time = formatTimestamp(new Date());
      this.item.text = `$(brain) CVC: ${branch} ✓`;
      this.item.tooltip = `CVC active on branch: ${branch}\nLast refresh: ${time}\nClick to open dashboard`;
      this.item.backgroundColor = undefined;
    } catch {
      this.item.text = '$(brain) CVC: ⚠';
      this.item.tooltip = 'CVC: not initialised or binary not found.\nClick to setup.';
      this.item.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
    }
  }

  private parseBranch(statusOutput: string): string {
    const match = statusOutput.match(/branch[:\s]+(\S+)/i);
    if (match) {
      return match[1];
    }
    const lines = statusOutput.split('\n');
    for (const line of lines) {
      if (line.trim()) {
        return line.trim().substring(0, 20);
      }
    }
    return 'main';
  }

  startAutoRefresh(intervalMs = 60_000): void {
    this.refreshInterval = setInterval(() => void this.refresh(), intervalMs);
  }

  dispose(): void {
    if (this.refreshInterval !== undefined) {
      clearInterval(this.refreshInterval);
    }
    this.item.dispose();
  }
}
