import * as vscode from 'vscode';
import { runCVC, debounce, formatTimestamp } from './utils';

export class AutoCommit {
  private disposables: vscode.Disposable[] = [];
  private debouncedCommit: (filename: string) => void;
  private enabled: boolean;

  constructor() {
    const config = vscode.workspace.getConfiguration('cvc');
    this.enabled = config.get<boolean>('autoCommit') ?? true;
    const debounceSeconds = config.get<number>('autoCommitDebounceSeconds') ?? 30;

    this.debouncedCommit = debounce((filename: string) => {
      void this.tryAutoCommit(filename);
    }, debounceSeconds * 1000);
  }

  start(): void {
    if (!this.enabled) {
      return;
    }

    const saveWatcher = vscode.workspace.onDidSaveTextDocument((doc) => {
      if (doc.uri.scheme === 'file') {
        const name = doc.fileName.split('/').pop() ?? doc.fileName;
        this.debouncedCommit(name);
      }
    });
    this.disposables.push(saveWatcher);

    const configWatcher = vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('cvc.autoCommit') || e.affectsConfiguration('cvc.autoCommitDebounceSeconds')) {
        this.restart();
      }
    });
    this.disposables.push(configWatcher);
  }

  restart(): void {
    this.dispose();
    const config = vscode.workspace.getConfiguration('cvc');
    this.enabled = config.get<boolean>('autoCommit') ?? true;
    const debounceSeconds = config.get<number>('autoCommitDebounceSeconds') ?? 30;
    this.debouncedCommit = debounce((filename: string) => {
      void this.tryAutoCommit(filename);
    }, debounceSeconds * 1000);
    this.start();
  }

  private async tryAutoCommit(filename: string): Promise<void> {
    try {
      const status = await runCVC('status --short');
      // Only commit if there is something pending (status not empty / not "clean")
      if (!status || status.toLowerCase().includes('nothing') || status.toLowerCase().includes('clean')) {
        return;
      }
      const time = formatTimestamp(new Date());
      const msg = `auto: saved ${filename} at ${time}`;
      await runCVC(`commit -m "${msg}"`);
      void vscode.window.setStatusBarMessage(`⚡ CVC: auto-committed — ${filename}`, 4000);
    } catch {
      // Silently ignore auto-commit failures to not disrupt workflow
    }
  }

  triggerCommit(reason: string): void {
    this.debouncedCommit(reason);
  }

  dispose(): void {
    for (const d of this.disposables) {
      d.dispose();
    }
    this.disposables = [];
  }
}
