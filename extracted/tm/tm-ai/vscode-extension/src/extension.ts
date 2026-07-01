import * as vscode from 'vscode';
import { CvcStatusBar } from './statusBar';
import { CvcProvider, CvcLogProvider } from './cvcProvider';
import { AutoCommit } from './autoCommit';
import { CopilotBridge } from './copilotBridge';
import { CvcDashboard } from './webviewPanel';
import { runCVC, getCvcPath } from './utils';

export function activate(context: vscode.ExtensionContext): void {
  // Core components
  const statusBar = new CvcStatusBar();
  const cvcProvider = new CvcProvider();
  const logProvider = new CvcLogProvider();
  const autoCommit = new AutoCommit();
  const copilotBridge = new CopilotBridge(autoCommit);
  const dashboard = new CvcDashboard(context);

  // Register tree views
  const branchView = vscode.window.createTreeView('cvcBranchView', {
    treeDataProvider: cvcProvider,
    showCollapseAll: false,
  });
  const logView = vscode.window.createTreeView('cvcLogView', {
    treeDataProvider: logProvider,
    showCollapseAll: false,
  });

  // Initial load
  void statusBar.refresh();
  void cvcProvider.load();
  void logProvider.load();
  statusBar.startAutoRefresh(60_000);

  // Start auto-commit watcher
  autoCommit.start();

  // === Commands ===

  context.subscriptions.push(
    vscode.commands.registerCommand('cvc.commit', async () => {
      const msg = await vscode.window.showInputBox({
        prompt: 'CVC Commit Message',
        placeHolder: 'Describe this context checkpoint…',
        value: `checkpoint: ${new Date().toLocaleTimeString()}`,
      });
      if (!msg) return;
      try {
        await runCVC(`commit -m "${msg}"`);
        void vscode.window.showInformationMessage(`✅ CVC committed: ${msg}`);
        void statusBar.refresh();
        void cvcProvider.load();
        void logProvider.load();
      } catch (err) {
        void vscode.window.showErrorMessage(`CVC commit failed: ${String(err)}`);
      }
    }),

    vscode.commands.registerCommand('cvc.restore', async () => {
      try {
        const log = await runCVC('log --limit 10');
        const items = log.split('\n').filter(l => l.trim()).map(l => ({ label: l.trim() }));
        const pick = await vscode.window.showQuickPick(items, { placeHolder: 'Select commit to restore' });
        if (!pick) return;
        const hash = pick.label.split(/\s/)[0];
        const confirm = await vscode.window.showWarningMessage(`Restore to commit ${hash}?`, 'Restore', 'Cancel');
        if (confirm !== 'Restore') return;
        await runCVC(`restore ${hash}`);
        void vscode.window.showInformationMessage(`✅ CVC restored to ${hash}`);
        void statusBar.refresh();
        void cvcProvider.load();
      } catch (err) {
        void vscode.window.showErrorMessage(`CVC restore failed: ${String(err)}`);
      }
    }),

    vscode.commands.registerCommand('cvc.log', async () => {
      try {
        const log = await runCVC('log');
        const channel = vscode.window.createOutputChannel('CVC Log');
        channel.appendLine(log);
        channel.show();
      } catch (err) {
        void vscode.window.showErrorMessage(`CVC log failed: ${String(err)}`);
      }
    }),

    vscode.commands.registerCommand('cvc.status', async () => {
      try {
        const status = await runCVC('status');
        void vscode.window.showInformationMessage(`CVC Status:\n${status}`, { modal: true });
      } catch (err) {
        void vscode.window.showErrorMessage(`CVC status failed: ${String(err)}`);
      }
    }),

    vscode.commands.registerCommand('cvc.branch', async () => {
      try {
        const branches = await runCVC('branch --list').catch(() => '');
        const newBranch = '+ Create new branch…';
        const items = [
          ...branches.split('\n').filter(l => l.trim()).map(l => l.replace(/^\*?\s*/, '')),
          newBranch,
        ];
        const pick = await vscode.window.showQuickPick(items, { placeHolder: 'Select or create a CVC branch' });
        if (!pick) return;
        if (pick === newBranch) {
          const name = await vscode.window.showInputBox({ prompt: 'New branch name' });
          if (!name) return;
          await runCVC(`branch ${name}`);
          void vscode.window.showInformationMessage(`✅ Created and switched to branch: ${name}`);
        } else {
          await runCVC(`branch ${pick}`);
          void vscode.window.showInformationMessage(`✅ Switched to branch: ${pick}`);
        }
        void statusBar.refresh();
        void cvcProvider.load();
      } catch (err) {
        void vscode.window.showErrorMessage(`CVC branch failed: ${String(err)}`);
      }
    }),

    vscode.commands.registerCommand('cvc.resume', async () => {
      await copilotBridge.resumeLastSession();
    }),

    vscode.commands.registerCommand('cvc.connect', async () => {
      // Auto-detect CVC path
      const binPath = getCvcPath();
      await vscode.workspace.getConfiguration('cvc').update('cvcPath', binPath, vscode.ConfigurationTarget.Global);
      await copilotBridge.connect();
    }),

    vscode.commands.registerCommand('cvc.openDashboard', async () => {
      await dashboard.open();
    }),

    vscode.commands.registerCommand('cvc.refresh', () => {
      void statusBar.refresh();
      void cvcProvider.load();
      void logProvider.load();
    }),

    vscode.commands.registerCommand('cvc.showCommitDetail', async (hash: string) => {
      if (!hash) return;
      try {
        const detail = await runCVC(`log --hash ${hash}`).catch(() => `Commit: ${hash}`);
        const channel = vscode.window.createOutputChannel(`CVC Commit ${hash}`);
        channel.appendLine(detail);
        channel.show();
      } catch {
        void vscode.window.showInformationMessage(`CVC commit: ${hash}`);
      }
    }),
  );

  // Show welcome message on first install
  const hasWelcomed = context.globalState.get<boolean>('cvc.welcomed');
  if (!hasWelcomed) {
    void vscode.window.showInformationMessage(
      '🧠 CVC is active! Click "Connect to GitHub Copilot" to enable auto-commit.',
      'Connect Now',
      'Open Dashboard',
    ).then(action => {
      if (action === 'Connect Now') {
        void vscode.commands.executeCommand('cvc.connect');
      } else if (action === 'Open Dashboard') {
        void vscode.commands.executeCommand('cvc.openDashboard');
      }
    });
    void context.globalState.update('cvc.welcomed', true);
  }

  // Register disposables
  context.subscriptions.push(statusBar, branchView, logView, autoCommit, copilotBridge, dashboard);
}

export function deactivate(): void {
  // Cleanup handled by disposables
}
