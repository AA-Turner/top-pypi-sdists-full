import * as vscode from 'vscode';
import { runCVC } from './utils';

export interface CommitEntry {
  hash: string;
  message: string;
  timestamp: string;
}

type CvcNodeKind = 'section' | 'branch' | 'commit' | 'action';

export class CvcTreeItem extends vscode.TreeItem {
  constructor(
    label: string,
    public readonly kind: CvcNodeKind,
    collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly meta?: string,
  ) {
    super(label, collapsibleState);
    this.contextValue = kind;

    switch (kind) {
      case 'section':
        this.iconPath = new vscode.ThemeIcon('folder');
        break;
      case 'branch':
        this.iconPath = new vscode.ThemeIcon('git-branch');
        break;
      case 'commit':
        this.iconPath = new vscode.ThemeIcon('git-commit');
        this.description = meta ?? '';
        this.command = {
          command: 'cvc.showCommitDetail',
          title: 'Show Commit',
          arguments: [this.meta],
        };
        break;
      case 'action':
        this.iconPath = new vscode.ThemeIcon('zap');
        break;
    }
  }
}

export class CvcProvider implements vscode.TreeDataProvider<CvcTreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<CvcTreeItem | undefined | null | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  private currentBranch = 'main';
  private commits: CommitEntry[] = [];
  private loading = false;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  async load(): Promise<void> {
    if (this.loading) {
      return;
    }
    this.loading = true;
    try {
      const statusOut = await runCVC('status --short').catch(() => '');
      const branchMatch = statusOut.match(/branch[:\s]+(\S+)/i);
      this.currentBranch = branchMatch ? branchMatch[1] : 'main';

      const logOut = await runCVC('log --limit 5').catch(() => '');
      this.commits = this.parseLog(logOut);
    } finally {
      this.loading = false;
    }
    this.refresh();
  }

  private parseLog(logOutput: string): CommitEntry[] {
    const entries: CommitEntry[] = [];
    const lines = logOutput.split('\n').filter(l => l.trim());
    for (const line of lines) {
      const m = line.match(/^([a-f0-9]{7,12})\s+(.+?)(?:\s{2,}(.+))?$/);
      if (m) {
        entries.push({ hash: m[1], message: m[2].trim(), timestamp: m[3]?.trim() ?? '' });
      } else if (line.trim()) {
        entries.push({ hash: '', message: line.trim().substring(0, 60), timestamp: '' });
      }
    }
    return entries.slice(0, 5);
  }

  getTreeItem(element: CvcTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: CvcTreeItem): CvcTreeItem[] {
    if (!element) {
      return [
        new CvcTreeItem('📍 Current Branch', 'section', vscode.TreeItemCollapsibleState.Expanded),
        new CvcTreeItem('🕒 Recent Commits', 'section', vscode.TreeItemCollapsibleState.Expanded),
        new CvcTreeItem('⚡ Quick Actions', 'section', vscode.TreeItemCollapsibleState.Expanded),
      ];
    }

    if (element.label === '📍 Current Branch') {
      return [new CvcTreeItem(this.currentBranch, 'branch', vscode.TreeItemCollapsibleState.None)];
    }

    if (element.label === '🕒 Recent Commits') {
      if (this.commits.length === 0) {
        return [new CvcTreeItem('No commits yet', 'commit', vscode.TreeItemCollapsibleState.None)];
      }
      return this.commits.map(c =>
        new CvcTreeItem(
          c.message || c.hash || 'commit',
          'commit',
          vscode.TreeItemCollapsibleState.None,
          c.hash,
        ),
      );
    }

    if (element.label === '⚡ Quick Actions') {
      const actions: CvcTreeItem[] = [
        new CvcTreeItem('Commit Context', 'action', vscode.TreeItemCollapsibleState.None, 'cvc.commit'),
        new CvcTreeItem('Resume Last Session', 'action', vscode.TreeItemCollapsibleState.None, 'cvc.resume'),
        new CvcTreeItem('Switch Branch', 'action', vscode.TreeItemCollapsibleState.None, 'cvc.branch'),
        new CvcTreeItem('Open Dashboard', 'action', vscode.TreeItemCollapsibleState.None, 'cvc.openDashboard'),
      ];
      for (const a of actions) {
        a.command = { command: a.meta ?? '', title: typeof a.label === 'string' ? a.label : '' };
      }
      return actions;
    }

    return [];
  }
}

export class CvcLogProvider implements vscode.TreeDataProvider<CvcTreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<CvcTreeItem | undefined | null | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  private commits: CommitEntry[] = [];

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  async load(): Promise<void> {
    try {
      const logOut = await runCVC('log --limit 20').catch(() => '');
      this.commits = this.parseLog(logOut);
    } catch {
      this.commits = [];
    }
    this.refresh();
  }

  private parseLog(logOutput: string): CommitEntry[] {
    const entries: CommitEntry[] = [];
    const lines = logOutput.split('\n').filter(l => l.trim());
    for (const line of lines) {
      const m = line.match(/^([a-f0-9]{7,12})\s+(.+?)(?:\s{2,}(.+))?$/);
      if (m) {
        entries.push({ hash: m[1], message: m[2].trim(), timestamp: m[3]?.trim() ?? '' });
      } else if (line.trim()) {
        entries.push({ hash: '', message: line.trim().substring(0, 60), timestamp: '' });
      }
    }
    return entries;
  }

  getTreeItem(element: CvcTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(): CvcTreeItem[] {
    if (this.commits.length === 0) {
      return [new CvcTreeItem('No commits found', 'commit', vscode.TreeItemCollapsibleState.None)];
    }
    return this.commits.map(c =>
      new CvcTreeItem(
        c.message || c.hash || 'commit',
        'commit',
        vscode.TreeItemCollapsibleState.None,
        c.hash,
      ),
    );
  }
}
