// CSSL Language Extension for VS Code
// Provides run functionality for .cssl files

const vscode = require('vscode');
const path = require('path');
const { spawn } = require('child_process');

let outputChannel;

function activate(context) {
    // Create output channel for CSSL
    outputChannel = vscode.window.createOutputChannel('CSSL');

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
        outputChannel.appendLine('─'.repeat(50));

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
            outputChannel.appendLine('─'.repeat(50));
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

    context.subscriptions.push(runCommand);
    context.subscriptions.push(outputChannel);

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

    console.log('CSSL extension activated');
}

function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};
