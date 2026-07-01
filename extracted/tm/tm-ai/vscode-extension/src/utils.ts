import { exec, execFile } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';

let _cvcPath: string | null = null;

export function getCvcPath(): string {
  const config = vscode.workspace.getConfiguration('cvc');
  const configPath = config.get<string>('cvcPath');
  if (configPath && configPath.trim() !== '') {
    return configPath.trim();
  }
  if (_cvcPath) {
    return _cvcPath;
  }
  // Common install locations
  const candidates = [
    path.join(process.env['HOME'] ?? '', '.local', 'bin', 'cvc'),
    '/usr/local/bin/cvc',
    '/opt/homebrew/bin/cvc',
    '/usr/bin/cvc',
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) {
      _cvcPath = c;
      return c;
    }
  }
  return 'cvc'; // fallback: rely on PATH
}

export function getWorkspacePath(): string {
  const config = vscode.workspace.getConfiguration('cvc');
  const configPath = config.get<string>('workspacePath');
  if (configPath && configPath.trim() !== '') {
    return configPath.trim();
  }
  const folders = vscode.workspace.workspaceFolders;
  if (folders && folders.length > 0) {
    return folders[0].uri.fsPath;
  }
  return process.cwd();
}

export function runCVC(args: string, cwd?: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const cvcBin = getCvcPath();
    const workdir = cwd ?? getWorkspacePath();
    const env = { ...process.env, PATH: `${path.join(process.env['HOME'] ?? '', '.local', 'bin')}:${process.env['PATH'] ?? ''}` };
    exec(`"${cvcBin}" ${args}`, { cwd: workdir, env }, (err, stdout, stderr) => {
      if (err) {
        reject(stderr || err.message);
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

export function runCVCArgs(args: string[], cwd?: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const cvcBin = getCvcPath();
    const workdir = cwd ?? getWorkspacePath();
    const env = { ...process.env, PATH: `${path.join(process.env['HOME'] ?? '', '.local', 'bin')}:${process.env['PATH'] ?? ''}` };
    execFile(cvcBin, args, { cwd: workdir, env }, (err, stdout, stderr) => {
      if (err) {
        reject(stderr || err.message);
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

export function formatTimestamp(date: Date): string {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export function debounce<T extends (...args: Parameters<T>) => void>(fn: T, delayMs: number): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout> | undefined;
  return (...args: Parameters<T>) => {
    if (timer !== undefined) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      fn(...args);
    }, delayMs);
  };
}
