"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const child_process_1 = require("child_process");
const path = require("path");
const riskGutter_1 = require("./riskGutter");
const CODE_EXTS = new Set([
    ".py", ".pyi",
    ".js", ".jsx", ".mjs", ".cjs",
    ".ts", ".tsx", ".mts", ".cts",
    ".go", ".rs", ".java", ".php", ".rb",
    ".cs", ".cshtml", ".razor",
    ".cpp", ".c", ".h", ".hpp", ".cc", ".cxx",
    ".swift", ".kt", ".kts", ".scala", ".dart",
    ".lua", ".luau", ".ex", ".exs", ".erl", ".hrl",
    ".vue", ".svelte", ".sql",
    ".gd", ".al", ".gleam", ".nix",
    ".hcl", ".tf", ".proto", ".graphql", ".gql",
    ".jl", ".r", ".R", ".hs",
    ".f90", ".f95", ".f03", ".f08",
    ".groovy", ".pl", ".pm",
    ".bash", ".sh", ".zsh",
]);
const pendingTimers = new Map();
let outputChannel;
function getChannel() {
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel("jCodeMunch");
    }
    return outputChannel;
}
function matchesAny(filePath, patterns) {
    const rel = vscode.workspace.asRelativePath(filePath, false);
    for (const pat of patterns) {
        const re = globToRegex(pat);
        if (re.test(rel) || re.test(filePath))
            return true;
    }
    return false;
}
function globToRegex(glob) {
    const escaped = glob
        .replace(/[.+^${}()|[\]\\]/g, "\\$&")
        .replace(/\*\*/g, "::DOUBLESTAR::")
        .replace(/\*/g, "[^/\\\\]*")
        .replace(/::DOUBLESTAR::/g, ".*")
        .replace(/\?/g, ".");
    return new RegExp("^" + escaped + "$");
}
function reindex(filePath) {
    const cfg = vscode.workspace.getConfiguration("jcodemunch.indexOnSave");
    const cmd = cfg.get("command", "jcodemunch-mcp");
    const ch = getChannel();
    const child = (0, child_process_1.spawn)(cmd, ["index-file", filePath], {
        stdio: ["ignore", "pipe", "pipe"],
        windowsHide: true,
    });
    let stderr = "";
    child.stderr?.on("data", (d) => { stderr += d.toString(); });
    child.on("error", (err) => {
        ch.appendLine(`[error] ${cmd} failed: ${err.message}`);
    });
    child.on("exit", (code) => {
        if (code === 0) {
            ch.appendLine(`[ok] reindexed ${filePath}`);
        }
        else {
            ch.appendLine(`[exit ${code}] ${filePath}${stderr ? ": " + stderr.trim() : ""}`);
        }
    });
}
function scheduleReindex(filePath) {
    const cfg = vscode.workspace.getConfiguration("jcodemunch.indexOnSave");
    if (!cfg.get("enabled", true))
        return;
    const ext = path.extname(filePath).toLowerCase();
    if (!CODE_EXTS.has(ext))
        return;
    const exclude = cfg.get("exclude", []);
    if (matchesAny(filePath, exclude))
        return;
    const debounceMs = cfg.get("debounceMs", 500);
    const existing = pendingTimers.get(filePath);
    if (existing)
        clearTimeout(existing);
    const timer = setTimeout(() => {
        pendingTimers.delete(filePath);
        reindex(filePath);
    }, debounceMs);
    pendingTimers.set(filePath, timer);
}
function activate(context) {
    const ch = getChannel();
    ch.appendLine("jCodeMunch auto-reindex active.");
    context.subscriptions.push(vscode.workspace.onDidSaveTextDocument((doc) => {
        if (doc.uri.scheme !== "file")
            return;
        scheduleReindex(doc.uri.fsPath);
    }));
    // Risk-density gutter (v1.89.0) — gated by jcodemunch.riskGutter.enabled.
    (0, riskGutter_1.activateRiskGutter)(context);
}
function deactivate() {
    for (const t of pendingTimers.values())
        clearTimeout(t);
    pendingTimers.clear();
    (0, riskGutter_1.deactivateRiskGutter)();
}
//# sourceMappingURL=extension.js.map