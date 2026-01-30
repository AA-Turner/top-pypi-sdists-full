// CSSL Language Extension for VS Code
// Provides Language Server Protocol (LSP) support and run functionality for .cssl files

const vscode = require('vscode');
const path = require('path');
const { spawn } = require('child_process');
const {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} = require('vscode-languageclient/node');

let outputChannel;
let languageClient;
let serverOutputChannel;

/**
 * Activate the CSSL extension
 * @param {vscode.ExtensionContext} context
 */
async function activate(context) {
    // Create output channels
    outputChannel = vscode.window.createOutputChannel('CSSL');
    serverOutputChannel = vscode.window.createOutputChannel('CSSL Language Server');

    // Start Language Server
    await startLanguageServer(context);

    // Register the run command
    const runCommand = vscode.commands.registerCommand('cssl.runFile', async () => {
        const editor = vscode.window.activeTextEditor;

        if (!editor) {
            vscode.window.showErrorMessage('No active editor found');
            return;
        }

        const document = editor.document;
        const filePath = document.fileName;
        const ext = path.extname(filePath).toLowerCase();

        // Only allow .cssl files (not .cssl-mod or .cssl-pl)
        if (ext !== '.cssl') {
            vscode.window.showWarningMessage('Only .cssl files can be executed. Modules (.cssl-mod) and Payloads (.cssl-pl) cannot be run directly.');
            return;
        }

        // Save the file before running
        if (document.isDirty) {
            await document.save();
        }

        // Get configuration
        const config = vscode.workspace.getConfiguration('cssl');
        const pythonPath = config.get('pythonPath', 'python');
        const showOutput = config.get('showOutput', true);

        // Show output channel
        if (showOutput) {
            outputChannel.show(true);
        }

        outputChannel.clear();
        outputChannel.appendLine(`[CSSL] Running: ${path.basename(filePath)}`);
        outputChannel.appendLine(`[CSSL] Path: ${filePath}`);
        outputChannel.appendLine('\u2500'.repeat(50));

        // Run the CSSL file using includecpp cssl run
        const args = ['-m', 'includecpp', 'cssl', 'run', filePath];

        const childProcess = spawn(pythonPath, args, {
            cwd: path.dirname(filePath),
            env: { ...process.env }
        });

        let hasError = false;

        childProcess.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });

        childProcess.stderr.on('data', (data) => {
            hasError = true;
            outputChannel.append(data.toString());
        });

        childProcess.on('close', (code) => {
            outputChannel.appendLine('');
            outputChannel.appendLine('\u2500'.repeat(50));
            if (code === 0) {
                outputChannel.appendLine(`[CSSL] Finished successfully`);
            } else {
                outputChannel.appendLine(`[CSSL] Exited with code: ${code}`);
            }
        });

        childProcess.on('error', (err) => {
            outputChannel.appendLine(`[CSSL] Error: ${err.message}`);
            vscode.window.showErrorMessage(`Failed to run CSSL: ${err.message}. Make sure IncludeCPP is installed (pip install includecpp).`);
        });
    });

    // Register restart server command
    const restartCommand = vscode.commands.registerCommand('cssl.restartServer', async () => {
        vscode.window.showInformationMessage('Restarting CSSL Language Server...');
        await stopLanguageServer();
        await startLanguageServer(context);
        vscode.window.showInformationMessage('CSSL Language Server restarted');
    });

    context.subscriptions.push(runCommand);
    context.subscriptions.push(restartCommand);
    context.subscriptions.push(outputChannel);
    context.subscriptions.push(serverOutputChannel);

    // Register task provider for CSSL
    const taskProvider = vscode.tasks.registerTaskProvider('cssl', {
        provideTasks: () => {
            return [];
        },
        resolveTask: (task) => {
            if (task.definition.type === 'cssl') {
                const config = vscode.workspace.getConfiguration('cssl');
                const pythonPath = config.get('pythonPath', 'python');
                const file = task.definition.file;

                const execution = new vscode.ShellExecution(
                    `${pythonPath} -m includecpp cssl run "${file}"`
                );

                return new vscode.Task(
                    task.definition,
                    vscode.TaskScope.Workspace,
                    'Run CSSL',
                    'cssl',
                    execution,
                    []
                );
            }
            return undefined;
        }
    });

    context.subscriptions.push(taskProvider);

    // Listen for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(async (e) => {
            if (e.affectsConfiguration('cssl.languageServer')) {
                const config = vscode.workspace.getConfiguration('cssl');
                const enabled = config.get('languageServer.enabled', true);

                if (enabled && !languageClient) {
                    await startLanguageServer(context);
                } else if (!enabled && languageClient) {
                    await stopLanguageServer();
                }
            }
        })
    );

    console.log('CSSL extension activated with Language Server support');
}

/**
 * Start the CSSL Language Server
 * @param {vscode.ExtensionContext} context
 */
async function startLanguageServer(context) {
    const config = vscode.workspace.getConfiguration('cssl');
    const enabled = config.get('languageServer.enabled', true);

    if (!enabled) {
        serverOutputChannel.appendLine('[LSP] Language Server is disabled in settings');
        return;
    }

    const pythonPath = config.get('pythonPath', 'python');
    const trace = config.get('trace.server', 'off');

    serverOutputChannel.appendLine('[LSP] Starting CSSL Language Server...');
    serverOutputChannel.appendLine(`[LSP] Python path: ${pythonPath}`);

    // Server options - run Python language server
    const serverOptions = {
        command: pythonPath,
        args: ['-m', 'includecpp.vscode.cssl.server', '--stdio'],
        options: {
            env: {
                ...process.env,
                PYTHONUNBUFFERED: '1'
            }
        }
    };

    // Get diagnostics configuration
    const diagnosticsConfig = {
        enabled: config.get('diagnostics.enabled', true),
        showSyntaxErrors: config.get('diagnostics.showSyntaxErrors', true),
        showTypeErrors: config.get('diagnostics.showTypeErrors', true),
        showUndefinedVariables: config.get('diagnostics.showUndefinedVariables', true),
        showUnusedVariables: config.get('diagnostics.showUnusedVariables', true),
        maxProblems: config.get('diagnostics.maxProblems', 100)
    };

    // Client options
    const clientOptions = {
        // Register for CSSL files
        documentSelector: [
            { scheme: 'file', language: 'cssl' },
            { scheme: 'untitled', language: 'cssl' }
        ],
        synchronize: {
            // Watch for .cssl files
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.{cssl,cssl-mod,cssl-pl}')
        },
        outputChannel: serverOutputChannel,
        traceOutputChannel: serverOutputChannel,
        // Middleware to debug didChange notifications
        middleware: {
            didChange: (event, next) => {
                serverOutputChannel.appendLine(`[CLIENT] Sending didChange for ${event.document.uri.toString()} (version ${event.document.version})`);
                return next(event);
            },
            didOpen: (document, next) => {
                serverOutputChannel.appendLine(`[CLIENT] Sending didOpen for ${document.uri.toString()}`);
                return next(document);
            }
        },
        initializationOptions: {
            diagnostics: diagnosticsConfig
        }
    };

    // Create language client
    languageClient = new LanguageClient(
        'cssl',
        'CSSL Language Server',
        serverOptions,
        clientOptions
    );

    // Set trace level
    if (trace !== 'off') {
        languageClient.setTrace(trace === 'verbose' ? 2 : 1);
    }

    // Handle client state changes
    languageClient.onDidChangeState((e) => {
        const stateNames = ['Stopped', 'Running', 'Starting'];
        serverOutputChannel.appendLine(`[LSP] State changed: ${stateNames[e.oldState]} -> ${stateNames[e.newState]}`);
    });

    try {
        // Start the client
        await languageClient.start();
        serverOutputChannel.appendLine('[LSP] CSSL Language Server started successfully');

        // Register client with context for cleanup
        context.subscriptions.push(languageClient);
    } catch (error) {
        serverOutputChannel.appendLine(`[LSP] Failed to start Language Server: ${error.message}`);
        serverOutputChannel.appendLine('[LSP] Make sure IncludeCPP is installed: pip install includecpp');
        serverOutputChannel.appendLine('[LSP] And pygls is available: pip install pygls>=2.0.0 lsprotocol>=2025.0.0');

        // Show error notification
        const action = await vscode.window.showErrorMessage(
            'Failed to start CSSL Language Server. Check the output for details.',
            'Show Output',
            'Install Dependencies'
        );

        if (action === 'Show Output') {
            serverOutputChannel.show();
        } else if (action === 'Install Dependencies') {
            const terminal = vscode.window.createTerminal('CSSL Setup');
            terminal.show();
            terminal.sendText('pip install includecpp pygls>=2.0.0 lsprotocol>=2025.0.0');
        }

        languageClient = null;
    }
}

/**
 * Stop the CSSL Language Server
 */
async function stopLanguageServer() {
    if (languageClient) {
        serverOutputChannel.appendLine('[LSP] Stopping CSSL Language Server...');
        try {
            await languageClient.stop();
            serverOutputChannel.appendLine('[LSP] Language Server stopped');
        } catch (error) {
            serverOutputChannel.appendLine(`[LSP] Error stopping server: ${error.message}`);
        }
        languageClient = null;
    }
}

/**
 * Deactivate the extension
 */
async function deactivate() {
    await stopLanguageServer();

    if (outputChannel) {
        outputChannel.dispose();
    }
    if (serverOutputChannel) {
        serverOutputChannel.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};
