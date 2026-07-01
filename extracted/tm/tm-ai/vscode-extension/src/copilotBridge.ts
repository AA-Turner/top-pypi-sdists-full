import * as vscode from 'vscode';
import { runCVC } from './utils';
import { AutoCommit } from './autoCommit';

export class CopilotBridge {
  private autoCommit: AutoCommit;
  private connected = false;
  private disposables: vscode.Disposable[] = [];

  constructor(autoCommit: AutoCommit) {
    this.autoCommit = autoCommit;
  }

  isCopilotActive(): boolean {
    const copilot = vscode.extensions.getExtension('github.copilot');
    const copilotChat = vscode.extensions.getExtension('github.copilot-chat');
    return (copilot?.isActive ?? false) || (copilotChat?.isActive ?? false);
  }

  async connect(): Promise<void> {
    if (!this.isCopilotActive()) {
      const install = await vscode.window.showWarningMessage(
        'GitHub Copilot extension is not active. Install it first.',
        'Open Extensions',
      );
      if (install === 'Open Extensions') {
        await vscode.commands.executeCommand('workbench.extensions.search', 'github.copilot');
      }
      return;
    }

    this.connected = true;

    // Watch for git commits → trigger CVC auto-commit
    const gitExt = vscode.extensions.getExtension('vscode.git');
    if (gitExt) {
      const git = gitExt.exports as { getAPI: (v: number) => { repositories: Array<{ state: { onDidChange: (cb: () => void) => vscode.Disposable } }> } };
      const api = git.getAPI(1);
      if (api && api.repositories.length > 0) {
        for (const repo of api.repositories) {
          const d = repo.state.onDidChange(() => {
            this.autoCommit.triggerCommit('git-commit');
          });
          this.disposables.push(d);
        }
      }
    }

    void vscode.window.showInformationMessage('✅ CVC connected to GitHub Copilot! Auto-commit is now active.');
  }

  async resumeLastSession(): Promise<void> {
    try {
      const log = await runCVC('log --limit 1');
      if (!log.trim()) {
        void vscode.window.showWarningMessage('CVC: No previous sessions found.');
        return;
      }

      let context = '';
      try {
        context = await runCVC('resume');
      } catch {
        context = log;
      }

      // Try to open a new Copilot chat with context injected
      const copilotChat = vscode.extensions.getExtension('github.copilot-chat');
      if (copilotChat?.isActive) {
        // Open the chat panel
        await vscode.commands.executeCommand('workbench.panel.chat.view.copilot.focus').then(
          undefined,
          () => vscode.commands.executeCommand('workbench.action.chat.open'),
        );

        // Copy context to clipboard for easy paste
        await vscode.env.clipboard.writeText(
          `[Resuming CVC session]\n\n${context}\n\nPlease continue from where we left off.`,
        );

        void vscode.window.showInformationMessage(
          '📋 CVC context copied to clipboard! Paste it in the Copilot chat to resume.',
          'OK',
        );
      } else {
        // Show in output channel
        const channel = vscode.window.createOutputChannel('CVC — Session Context');
        channel.appendLine('=== Last CVC Session Context ===');
        channel.appendLine(context);
        channel.show();
      }
    } catch (err) {
      void vscode.window.showErrorMessage(`CVC resume failed: ${String(err)}`);
    }
  }

  isConnected(): boolean {
    return this.connected;
  }

  dispose(): void {
    for (const d of this.disposables) {
      d.dispose();
    }
  }
}
