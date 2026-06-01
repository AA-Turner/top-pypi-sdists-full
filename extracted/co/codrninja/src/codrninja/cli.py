"""Command-line interface for codrninja with dual modes."""

import json
import os
import shlex
import sys

from .agent import Agent, AgentMode
from .config import Config
from .core import AICode
from .skills import SkillRegistry
from .tui_textual import CodrninjaTUI, main_tui
from .mcp import MCPManager
from .permissions import PermissionManager, PermissionRule
from .todo import TodoManager, format_todo_item
from .tools import ToolRegistry
from .safety import SafetyConfig


BUILTIN_SUBAGENT_MODES = {
    'general': AgentMode.BUILD,
    'explore': AgentMode.PLAN,
}


def main():
    automation_mode = os.environ.get('AI_CODE_MODE') == 'automation' or '--json' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != '--json']

    if len(args) < 1:
        start_tui(None)
        return

    first_arg = args[0]
    known_commands = [
        'create-session', 'send', 'list-sessions', 'show-session',
        'config', 'agent', 'run', 'chat', 'interactive', 'i',
        'new', 'help', '--help', '-h', '--version', '-v',
        'tui', 'onboard', 'skills', 'mcp', 'lsp',
        'build', 'plan', 'review', 'explain', 'test', 'commit', 'exec',
        'search', 'fetch', 'subagent', 'subagents', 'todo', 'permissions',
        'session', 'ask', 'reasoning', 'auth', 'serve', 'stop',
        # session management parity commands
        'model', 'provider', 'clear', 'undo', 'fork', 'compact', 'warp', 'open', 'status', 'share',
    ]

    if first_arg not in known_commands and not first_arg.startswith('-'):
        start_tui(first_arg)
        return

    command = first_arg
    ai = AICode()

    if command == 'tui':
        session_name = args[1] if len(args) > 1 else 'default'
        start_tui(session_name)
        return

    if command == 'serve':
        host = '127.0.0.1'
        port = 7384
        for i, arg in enumerate(args[1:], 1):
            if arg == '--host' and i + 1 < len(args):
                host = args[i + 1]
            elif arg == '--port' and i + 1 < len(args):
                port = int(args[i + 1])
        # Kill any existing server on this port first
        if _port_in_use(port):
            print(f'Port {port} in use — stopping old server...')
            _kill_server(port)
            import time
            deadline = time.monotonic() + 5.0
            while time.monotonic() < deadline:
                if not _port_in_use(port):
                    break
                time.sleep(0.1)
        from .server import run_server
        print(f'Starting codrninja server on {host}:{port}')
        run_server(host=host, port=port)
        return

    if command == 'stop':
        port = 7384
        for i, arg in enumerate(args[1:], 1):
            if arg == '--port' and i + 1 < len(args):
                port = int(args[i + 1])
        if _port_in_use(port):
            print(f'Stopping codrninja server on port {port}...')
            ok = kill_server_cmd(port)
            if ok:
                print('Stopped.')
            else:
                print(f'Warning: could not stop server on port {port} — process still running.')
        else:
            print(f'No server running on port {port}.')
        return

    if command == 'debug':
        _debug_diagnostics()
        return

    if command == 'session':
        handle_session_command(ai, args[1:], automation_mode)
        return

    if command == 'create-session':
        if len(args) < 2:
            error_out('Usage: codrninja create-session <name>', automation_mode)
        session = ai.create_session(args[1])
        output({'$schema': 'codrninja.create-session.v1', 'id': session.id, 'name': session.name, 'created': True}, automation_mode)

    elif command == 'send':
        if len(args) < 3:
            error_out('Usage: codrninja send <session> <message>', automation_mode)
        result = ai.send_message(args[1], args[2])
        result['$schema'] = 'codrninja.send.v1'
        output(result, automation_mode)

    elif command == 'list-sessions':
        output({'$schema': 'codrninja.list-sessions.v1', 'sessions': ai.list_sessions()}, automation_mode)

    elif command == 'show-session':
        if len(args) < 2:
            error_out('Usage: codrninja show-session <name>', automation_mode)
        result = ai.get_history(args[1])
        if result:
            result['$schema'] = 'codrninja.show-session.v1'
            output(result, automation_mode)
        else:
            error_out(f"Session '{args[1]}' not found", automation_mode)

    elif command == 'config':
        config = Config.from_env()
        output({
            '$schema': 'codrninja.config.v1',
            'ollama_url': config.ollama_url,
            'default_model': config.default_model,
            'db_path': config.db_path,
        }, automation_mode)

    elif command == 'onboard':
        start_onboarding()

    elif command == 'skills':
        handle_skills(args[1:])

    elif command == 'mcp':
        handle_mcp(args[1:], automation_mode)

    elif command == 'lsp':
        handle_lsp(args[1:], automation_mode)

    elif command in ('agent', 'run', 'ask', 'plan', 'build'):
        handle_agent_command(ai, command, args[1:], automation_mode)

    elif command == 'review':
        if len(args) < 3:
            error_out('Usage: codrninja review <session> <file>', automation_mode)
        session_name, target = args[1], args[2]
        result = ai.tools.read_file(target)
        if result.success:
            run_agent_mode(ai, session_name, f'Review this code:\n\n{result.output}', AgentMode.PLAN, automation_mode)
        else:
            error_out(f'Error reading file: {result.error}', automation_mode)

    elif command == 'explain':
        if len(args) < 3:
            error_out('Usage: codrninja explain <session> <topic>', automation_mode)
        run_agent_mode(ai, args[1], f'Explain: {args[2]}', AgentMode.PLAN, automation_mode)

    elif command == 'test':
        session_name = args[1] if len(args) > 2 else 'default'
        test_cmd = args[2] if len(args) > 2 else (args[1] if len(args) > 1 else 'pytest -q')
        result = ai.tools.execute_command(test_cmd)
        output({'$schema': 'codrninja.test.v1', 'success': result.success, 'output': result.output, 'error': result.error, 'session': session_name}, automation_mode)

    elif command == 'commit':
        if len(args) < 2:
            error_out('Usage: codrninja commit <message>', automation_mode)
        msg = args[1]
        ai.tools.execute_command('git add -A')
        result = ai.tools.execute_command(f'git commit -m {shlex.quote(msg)}')
        output({'$schema': 'codrninja.commit.v1', 'success': result.success, 'output': result.output, 'error': result.error}, automation_mode)

    elif command == 'exec':
        if len(args) < 2:
            error_out('Usage: codrninja exec <command>', automation_mode)
        cmd = ' '.join(args[1:])
        result = ai.tools.execute_command(cmd)
        output({'$schema': 'codrninja.exec.v1', 'success': result.success, 'output': result.output, 'error': result.error}, automation_mode)

    elif command == 'search':
        if len(args) < 2:
            error_out('Usage: codrninja search <query>', automation_mode)
        query = ' '.join(args[1:])
        result = ai.tools.web_search(query)
        payload = {'$schema': 'codrninja.search.v1', 'success': result.success, 'results': None, 'output': result.output, 'error': result.error}
        if result.success:
            try:
                payload['results'] = json.loads(result.output)
            except json.JSONDecodeError:
                payload['results'] = result.output
        output(payload, automation_mode)

    elif command == 'fetch':
        if len(args) < 2:
            error_out('Usage: codrninja fetch <url>', automation_mode)
        url = args[1]
        result = ai.tools.web_fetch(url)
        output({'$schema': 'codrninja.fetch.v1', 'success': result.success, 'content': result.output if result.success else None, 'error': result.error}, automation_mode)

    elif command == 'todo':
        handle_todo(args[1:], automation_mode)

    elif command == 'permissions':
        handle_permissions(args[1:], automation_mode)

    elif command == 'auth':
        handle_auth_command(args[1:], automation_mode)

    elif command == 'subagent':
        if len(args) < 4:
            error_out('Usage: codrninja subagent <session> <name> <task>', automation_mode)
        session_name, name = args[1], args[2]
        task = ' '.join(args[3:])
        ai.create_session(session_name)
        agent = Agent(ai, session_name, max_iterations=10, mode=AgentMode.BUILD)
        mode = BUILTIN_SUBAGENT_MODES.get(name.lower(), AgentMode.BUILD)
        subagent = agent.spawn_subagent(name, task, mode)
        result = subagent.run(task, auto_approve=automation_mode)
        output({
            '$schema': 'codrninja.subagent.v1',
            'success': result.get('success', False),
            'session': session_name,
            'subagent': {
                'name': name,
                'session_id': subagent.session_name,
                'task': task,
                'mode': subagent.mode,
            },
            'result': result,
        }, automation_mode)

    elif command == 'subagents':
        if len(args) < 2:
            error_out('Usage: codrninja subagents <session>', automation_mode)
        session_name = args[1]
        ai.create_session(session_name)
        agent = Agent(ai, session_name, max_iterations=10, mode=AgentMode.BUILD)
        output({'$schema': 'codrninja.subagents.v1', 'session': session_name, 'subagents': agent.subagent_manager.list()}, automation_mode)

    elif command == 'reasoning':
        levels = ['none', 'low', 'medium', 'high']
        if len(args) < 2:
            current = ai.config.reasoning_level
            if automation_mode:
                output({'$schema': 'codrninja.reasoning.v1', 'current': current, 'levels': levels}, True)
            else:
                print(f'Current reasoning level: {current}')
                print(f'Levels: {", ".join(levels)}')
                print(f'Usage: codrninja reasoning <{"|".join(levels)}>')
        else:
            level = args[1].lower()
            if level not in levels:
                error_out(f'Invalid level: {level}. Must be one of: {", ".join(levels)}', automation_mode)
            ai.config.reasoning_level = level
            try:
                config_path = os.path.expanduser('~/.codrninja/config.json')
                config = {}
                if os.path.exists(config_path):
                    with open(config_path) as f:
                        config = json.load(f)
                config['reasoning_level'] = level
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
            except Exception:
                pass
            if automation_mode:
                output({'$schema': 'codrninja.reasoning.v1', 'success': True, 'level': level}, True)
            else:
                print(f'Reasoning level set to: {level}')

    elif command == 'model':
        if len(args) < 3:
            error_out('Usage: codrninja model <session> <model> [<provider>]', automation_mode)
        from .sessions import SessionManager
        sm = SessionManager()
        session_name, model_name = args[1], args[2]
        provider_name = args[3] if len(args) > 3 else None
        kwargs: dict = {'model': model_name}
        if provider_name:
            kwargs['provider'] = provider_name
        state = sm.update_state(session_name, **kwargs)
        if not state:
            error_out(f"Session '{session_name}' not found", automation_mode)
        output({'$schema': 'codrninja.model.v1', 'session': session_name,
                'model': state['model'], 'provider': state.get('provider', '')}, automation_mode)

    elif command == 'provider':
        if len(args) < 3:
            error_out('Usage: codrninja provider <session> <provider>', automation_mode)
        from .sessions import SessionManager
        sm = SessionManager()
        session_name, provider_name = args[1], args[2]
        state = sm.update_state(session_name, provider=provider_name)
        if not state:
            error_out(f"Session '{session_name}' not found", automation_mode)
        output({'$schema': 'codrninja.provider.v1', 'session': session_name,
                'provider': state.get('provider', '')}, automation_mode)

    elif command == 'clear':
        if len(args) < 2:
            error_out('Usage: codrninja clear <session>', automation_mode)
        from .sessions import SessionManager
        sm = SessionManager()
        session_name = args[1]
        state = sm.get(session_name)
        if not state:
            error_out(f"Session '{session_name}' not found", automation_mode)
        slug = state.get('slug') or sm.sanitize_name(session_name)
        (sm.sessions_dir / slug / 'messages.jsonl').write_text('')
        sm.update_state(session_name, message_count=0)
        output({'$schema': 'codrninja.clear.v1', 'session': session_name, 'cleared': True}, automation_mode)

    elif command == 'undo':
        if len(args) < 2:
            error_out('Usage: codrninja undo <session>', automation_mode)
        from .sessions import SessionManager
        sm = SessionManager()
        session_name = args[1]
        state = sm.get(session_name)
        if not state:
            error_out(f"Session '{session_name}' not found", automation_mode)
        messages = sm.get_messages(session_name)
        if not messages:
            error_out(f"Session '{session_name}' has no messages to undo", automation_mode)
        # remove last assistant then last user message
        while messages and messages[-1].get('role') == 'assistant':
            messages.pop()
        while messages and messages[-1].get('role') == 'user':
            messages.pop()
        slug = state.get('slug') or sm.sanitize_name(session_name)
        content = '\n'.join(json.dumps(m) for m in messages)
        (sm.sessions_dir / slug / 'messages.jsonl').write_text(content + '\n' if content else '')
        sm.update_state(session_name, message_count=len(messages))
        output({'$schema': 'codrninja.undo.v1', 'session': session_name,
                'messages_remaining': len(messages)}, automation_mode)

    elif command == 'fork':
        if len(args) < 3:
            error_out('Usage: codrninja fork <session> <new-name>', automation_mode)
        import shutil as _shutil, uuid as _uuid
        from datetime import datetime, timezone
        from .sessions import SessionManager
        sm = SessionManager()
        source_name, new_name = args[1], args[2]
        source_state = sm.get(source_name)
        if not source_state:
            error_out(f"Session '{source_name}' not found", automation_mode)
        new_slug = sm.sanitize_name(new_name)
        dst_dir = sm.sessions_dir / new_slug
        if dst_dir.exists():
            error_out(f"Session '{new_name}' already exists", automation_mode)
        src_slug = source_state.get('slug') or sm.sanitize_name(source_name)
        _shutil.copytree(str(sm.sessions_dir / src_slug), str(dst_dir))
        now = datetime.now(timezone.utc).isoformat()
        new_state = dict(source_state)
        new_state.update({'id': str(_uuid.uuid4()), 'name': new_name, 'slug': new_slug,
                          'created_at': now, 'updated_at': now})
        (dst_dir / 'state.json').write_text(json.dumps(new_state, indent=2))
        output({'$schema': 'codrninja.fork.v1', 'source': source_name,
                'new_session': new_name, 'slug': new_slug}, automation_mode)

    elif command == 'compact':
        if len(args) < 2:
            error_out('Usage: codrninja compact <session>', automation_mode)
        run_agent_mode(
            ai, args[1],
            'Summarize this entire conversation into a single compact message that '
            'preserves all key decisions, code changes, file paths, and context. '
            'Then clear the history and replace it with just this summary.',
            AgentMode.BUILD, automation_mode,
        )

    elif command == 'warp':
        if len(args) < 3:
            error_out('Usage: codrninja warp <session> <directory>', automation_mode)
        from .sessions import SessionManager
        sm = SessionManager()
        session_name = args[1]
        directory = os.path.abspath(os.path.expanduser(args[2]))
        if not os.path.isdir(directory):
            error_out(f"Directory not found: {directory}", automation_mode)
        state = sm.update_state(session_name, working_directory=directory)
        if not state:
            error_out(f"Session '{session_name}' not found", automation_mode)
        output({'$schema': 'codrninja.warp.v1', 'session': session_name,
                'working_directory': directory}, automation_mode)

    elif command == 'open':
        if len(args) < 2:
            error_out('Usage: codrninja open <file>', automation_mode)
        file_path = os.path.expanduser(args[1])
        try:
            with open(file_path) as fh:
                content = fh.read()
            output({'$schema': 'codrninja.open.v1', 'file': file_path,
                    'content': content, 'size': len(content)}, automation_mode)
        except FileNotFoundError:
            error_out(f"File not found: {file_path}", automation_mode)
        except Exception as e:
            error_out(str(e), automation_mode)

    elif command == 'status':
        from .sessions import SessionManager
        sm = SessionManager()
        session_name = args[1] if len(args) > 1 else None
        config = Config.from_env()
        payload: dict = {
            '$schema': 'codrninja.status.v1',
            'provider': config.default_provider,
            'model': config.default_model,
            'reasoning_level': config.reasoning_level,
        }
        if session_name:
            state = sm.get(session_name)
            if not state:
                error_out(f"Session '{session_name}' not found", automation_mode)
            payload['session'] = {
                'name': state['name'],
                'model': state.get('model') or config.default_model,
                'provider': state.get('provider') or config.default_provider,
                'status': state.get('status'),
                'message_count': state.get('message_count', 0),
                'working_directory': state.get('working_directory', os.getcwd()),
            }
        output(payload, automation_mode)

    elif command == 'share':
        if len(args) < 2:
            error_out('Usage: codrninja share <session>', automation_mode)
        from .sessions import SessionManager
        sm = SessionManager()
        session_name = args[1]
        state = sm.get(session_name)
        if not state:
            error_out(f"Session '{session_name}' not found", automation_mode)
        messages = sm.get_messages(session_name)
        lines = [
            f"# {state['name']}",
            f"Model: {state.get('model', 'unknown')}  Provider: {state.get('provider', 'unknown')}",
            f"Created: {state.get('created_at', '')}",
            '',
        ]
        for msg in messages:
            role = msg.get('role', 'unknown').upper()
            lines.append(f"**{role}**: {msg.get('content', '')}")
            lines.append('')
        summary = '\n'.join(lines)
        if automation_mode:
            output({'$schema': 'codrninja.share.v1', 'session': session_name,
                    'summary': summary, 'message_count': len(messages)}, automation_mode)
        else:
            print(summary)

    elif command in ('chat', 'interactive', 'i'):
        session_name = args[1] if len(args) > 1 else 'default'
        ai.create_session(session_name)
        app = CodrninjaTUI(ai, session_name)
        app.run()

    elif command == 'new':
        session_name = args[1] if len(args) > 1 else f"session-{os.urandom(4).hex()}"
        ai.create_session(session_name)
        if automation_mode:
            output({'$schema': 'codrninja.new.v1', 'session': session_name, 'status': 'created'}, True)
        else:
            print(f"Created session: {session_name}")
            app = CodrninjaTUI(ai, session_name)
            app.run()

    elif command in ('help', '--help', '-h'):
        if automation_mode:
            output({'$schema': 'codrninja.help.v1', 'help': get_help_text()}, True)
        else:
            print_help()

    elif command in ('--version', '-v'):
        try:
            import importlib.metadata
            from codrninja import __version__
            print(f'codrninja {__version__}')
        except Exception:
            print('codrninja')

    else:
        error_out(f'Unknown command: {command}', automation_mode)


def parse_safety_flags(args):
    config = {
        'dry_run': False,
        'no_shell': False,
        'allow_shell': False,
        'allow_write': False,
        'require_approval': False,
        'max_steps': None,
    }
    cleaned = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--dry-run':
            config['dry_run'] = True
        elif arg == '--no-shell':
            config['no_shell'] = True
        elif arg == '--allow-shell':
            config['allow_shell'] = True
        elif arg == '--allow-write':
            config['allow_write'] = True
        elif arg == '--require-approval':
            config['require_approval'] = True
        elif arg == '--max-steps' and i + 1 < len(args):
            config['max_steps'] = int(args[i + 1])
            i += 1
        else:
            cleaned.append(arg)
        i += 1
    return cleaned, SafetyConfig.from_cli_flags(**config)




def _spinner_thread(msg: str = ""):
    """Return (start_fn, stop_fn) for a Claude-style flower spinner."""
    import sys, threading, time
    running = [False]
    thread = [None]
    # Claude Code thinking animation characters (left-aligned, no text)
    FLOWERS = ["·", "✻", "✽", "✶", "✳", "✢"]
    PEACH = "\033[38;5;216m"   # 256-color peachy pink (like Claude)
    RESET = "\033[0m"

    def _loop():
        idx = 0
        start = time.monotonic()
        while running[0]:
            elapsed = time.monotonic() - start
            char = FLOWERS[idx % len(FLOWERS)]
            sys.stdout.write(f"\r{PEACH}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.12)
            idx += 1
        sys.stdout.write("\r \r")
        sys.stdout.flush()

    def start():
        running[0] = True
        thread[0] = threading.Thread(target=_loop, daemon=True)
        thread[0].start()

    def stop():
        running[0] = False
        if thread[0]:
            thread[0].join(timeout=1.0)

    return start, stop


def handle_agent_command(ai, command, args, automation_mode):
    cleaned_args, safety = parse_safety_flags(args)
    mode = AgentMode.BUILD
    if command == 'plan':
        mode = AgentMode.PLAN
    elif command == 'build':
        mode = AgentMode.BUILD
    elif command in ('agent', 'run'):
        for i, arg in enumerate(list(cleaned_args)):
            if arg == '--mode' and i + 1 < len(cleaned_args):
                mode = cleaned_args[i + 1]
                cleaned_args = cleaned_args[:i] + cleaned_args[i + 2:]
                break

    if len(cleaned_args) < 2:
        error_out(f'Usage: codrninja {command} <session> <message>', automation_mode)

    session_name = cleaned_args[0]
    message = cleaned_args[1]
    ai.create_session(session_name)
    agent = Agent(ai, session_name, max_iterations=10, mode=mode, safety_config=safety)

    if not automation_mode:
        def on_progress(msg):
            print(f"  {msg}")
        agent.on_progress = on_progress
        spinner_start, spinner_stop = _spinner_thread()
        spinner_start()

    result = agent.run(message, auto_approve=automation_mode)
    if not automation_mode:
        spinner_stop()

    schema_name = f'codrninja.{command}.v1'
    if automation_mode:
        result['$schema'] = schema_name
        output(result, True)
    elif result['success']:
        print(f"\n[OK] Task completed in {result['iterations']} iterations")
        print(f"Tools used: {result['tool_calls']}")
        print(f"\nResponse:\n{result['response'][:500]}...")
    else:
        print(f"\n[FAIL] Error: {result.get('error', 'Unknown error')}")


def handle_session_command(ai: AICode, args, automation_mode: bool):
    if not args:
        error_out('Usage: codrninja session <create|list|status|log|events|diff|rollback>', automation_mode)
    action = args[0]
    sm = ai.session_manager
    if action == 'create':
        if len(args) < 2:
            error_out('Usage: codrninja session create <name> [--model <model>]', automation_mode)
        name = args[1]
        model = ai.config.default_model
        if '--model' in args:
            idx = args.index('--model')
            if idx + 1 < len(args):
                model = args[idx + 1]
        state = sm.create(name, model=model, provider=ai.config.default_provider, git_branch=ai.git.get_branch() or '')
        output({'$schema': 'codrninja.session.create.v1', 'session': state}, automation_mode)
        return
    if action == 'list':
        output({'$schema': 'codrninja.session.list.v1', 'sessions': ai.list_sessions()}, automation_mode)
        return
    if len(args) < 2:
        error_out(f'Usage: codrninja session {action} <name>', automation_mode)
    name = args[1]
    state = sm.get(name)
    if not state:
        error_out(f"Session '{name}' not found", automation_mode)
    if action == 'status':
        output({'$schema': 'codrninja.session.status.v1', 'session': state}, automation_mode)
        return
    if action == 'log':
        output({'$schema': 'codrninja.session.log.v1', 'session': state.get('name'), 'messages': sm.get_messages(name)}, automation_mode)
        return
    if action == 'events':
        output({'$schema': 'codrninja.session.events.v1', 'session': state.get('name'), 'events': sm.get_events(name)}, automation_mode)
        return
    if action == 'diff':
        diff = ai.git.get_diff()
        payload = {'$schema': 'codrninja.session.diff.v1', 'session': state.get('name'), 'diff': diff}
        output(payload, automation_mode)
        return
    if action == 'rollback':
        result = ai.git.rollback('stash')
        output({'$schema': 'codrninja.session.rollback.v1', 'session': state.get('name'), 'result': result}, automation_mode)
        return
    error_out('Usage: codrninja session <create|list|status|log|events|diff|rollback>', automation_mode)


def output(data: dict, automation_mode: bool):
    if automation_mode:
        print(json.dumps(data))
    else:
        print(json.dumps(data, indent=2))


def error_out(message: str, automation_mode: bool):
    if automation_mode:
        print(json.dumps({'error': message}))
    else:
        print(f'Error: {message}')
    sys.exit(1)


def print_help():
    print(get_help_text())


def get_help_text() -> str:
    return """Available commands:

  Sessions
  ──────────────────────────────────────────────────
  list-sessions                  List all sessions (JSON)
  create-session <name>          Create a new session
  show-session <name>            Show session history
  status [<session>]             Show provider/model/session status
  model <session> <model> [prov] Set model (and optionally provider) for a session
  provider <session> <provider>  Set provider for a session
  clear <session>                Clear conversation history
  undo <session>                 Remove last message pair
  fork <session> <new-name>      Duplicate a session under a new name
  compact <session>              AI-summarize and compact conversation
  warp <session> <directory>     Set working directory for a session
  share <session>                Print shareable session summary
  session <cmd>                  Low-level session commands (log/events/diff/rollback)

  Messaging & Agent
  ──────────────────────────────────────────────────
  send <session> <msg>           Send a chat message
  build <session> <task>         Run build agent (writes files, runs commands)
  plan <session> <task>          Run plan agent (reasons, no execution)
  ask <session> <question>       Ask a question in build mode
  review <session> <file>        Code review a file
  explain <session> <topic>      Explain code or a concept
  subagent <s> <name> <task>     Spawn a child subagent
  subagents <session>            List active subagents

  Tools
  ──────────────────────────────────────────────────
  exec <command>                 Execute a shell command
  search <query>                 Web search
  fetch <url>                    Fetch and read a web page
  open <file>                    Read a file and output its contents
  commit <message>               Git add -A and commit
  test [command]                 Run tests (default: pytest -q)
  todo ...                       Manage todos

  Configuration
  ──────────────────────────────────────────────────
  config                         Show current configuration
  reasoning [level]              Get/set reasoning level (none/low/medium/high)
  permissions ...                Manage permission rules
  auth <provider|status|revoke>  OAuth authentication
  mcp ...                        Manage MCP servers
  lsp ...                        Language server operations
  skills                         List available skills

  Interface
  ──────────────────────────────────────────────────
  tui [session]                  Start interactive TUI
  serve [--port <n>]             Start the backend server (kills old one first)
  stop [--port <n>]              Stop the backend server
  help                           Show this help
"""


def run_agent_mode(ai, session_name, message, mode, automation_mode):
    agent = Agent(ai, session_name, max_iterations=10, mode=mode)
    if not automation_mode:
        def on_progress(msg):
            print(f"  {msg}")
        agent.on_progress = on_progress
        spinner_start, spinner_stop = _spinner_thread()
        spinner_start()

    result = agent.run(message, auto_approve=automation_mode)
    if not automation_mode:
        spinner_stop()

    if automation_mode:
        output(result, True)
    elif result['success']:
        print(f"\n[OK] Task completed in {result['iterations']} iterations")
        print(f"Tools used: {result['tool_calls']}")
        print(f"\nResponse:\n{result['response'][:500]}...")
    else:
        print(f"\n[FAIL] Error: {result.get('error', 'Unknown error')}")


def _installed_tui_version(tui_path: str) -> str:
    try:
        import json as _j
        pkg = os.path.join(tui_path, 'package.json')
        if os.path.isfile(pkg):
            return _j.loads(open(pkg).read()).get('codrninja_version', '')
    except Exception:
        pass
    return ''


def _find_ts_tui() -> str | None:
    """Return path to the TypeScript TUI if it matches the running codrninja version.
    Returns None to force reinstall whenever versions differ."""
    # User-specified override: never auto-update
    env_path = os.environ.get('CODRNINJA_TUI_PATH', '')
    if env_path and os.path.isfile(os.path.join(env_path, 'package.json')):
        return env_path

    from codrninja import __version__

    installed_tui = os.path.expanduser('~/.codrninja/tui')
    if os.path.isfile(os.path.join(installed_tui, 'package.json')):
        installed_ver = _installed_tui_version(installed_tui)
        if installed_ver == __version__:
            return installed_tui
        # Version mismatch — force reinstall
        return None

    # Dev path (local checkout) — use as-is without version check
    dev_path = os.path.expanduser('~/codrninja/tui')
    if os.path.isfile(os.path.join(dev_path, 'package.json')):
        return dev_path

    return None


def _setup_bundled_tui() -> str | None:
    """Extract the bundled TUI to ~/.codrninja/tui.

    If dist/bundle.js exists (self-contained esbuild bundle) we skip npm install
    entirely — bundle.js has all dependencies inlined.  This makes setup instant
    and removes the dependency on network access / npm availability.
    """
    import shutil
    import subprocess

    node = shutil.which('node')
    if not node:
        print('[codrninja] node not found — cannot set up TUI automatically.')
        print('            Install Node.js from https://nodejs.org and run codrninja again.')
        return None

    bundle_dir = os.path.join(os.path.dirname(__file__), '_tui_bundle')
    if not os.path.isdir(bundle_dir):
        return None

    tui_dest = os.path.expanduser('~/.codrninja/tui')
    if os.path.exists(tui_dest):
        shutil.rmtree(tui_dest)
    shutil.copytree(bundle_dir, tui_dest)

    # Stamp the installed version so _find_ts_tui can detect stale installs
    try:
        import json as _j
        from codrninja import __version__
        pkg_path = os.path.join(tui_dest, 'package.json')
        with open(pkg_path) as f:
            pkg = _j.load(f)
        pkg['codrninja_version'] = __version__
        with open(pkg_path, 'w') as f:
            _j.dump(pkg, f, indent=2)
    except Exception:
        pass

    # If a self-contained bundle exists we're done — no npm install needed.
    if os.path.isfile(os.path.join(tui_dest, 'dist', 'bundle.js')):
        return tui_dest

    # Fallback: traditional tsc output needs node_modules
    npm = shutil.which('npm')
    if not npm:
        print('[codrninja] npm not found — cannot install TUI dependencies.')
        print('            Install Node.js (includes npm) from https://nodejs.org')
        shutil.rmtree(tui_dest, ignore_errors=True)
        return None

    print('codrninja: first run — installing TUI (one-time setup)...')
    result = subprocess.run([npm, 'install', '--silent'], cwd=tui_dest, timeout=180)
    if result.returncode != 0:
        shutil.rmtree(tui_dest, ignore_errors=True)
        print('[codrninja] TUI dependency install failed. Try: npm install in ~/.codrninja/tui')
        return None

    return tui_dest


def _port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def _pid_file(port: int = 7384) -> str:
    return os.path.expanduser(f"~/.codrninja/server-{port}.pid")


def _write_pid_file(pid: int, port: int = 7384):
    try:
        path = _pid_file(port)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(str(pid))
    except Exception:
        pass


def _read_pid_file(port: int = 7384) -> int | None:
    try:
        with open(_pid_file(port)) as f:
            v = f.read().strip()
            return int(v) if v.isdigit() else None
    except Exception:
        return None


def _clear_pid_file(port: int = 7384):
    try:
        os.remove(_pid_file(port))
    except Exception:
        pass


def _clear_version_stamp(port: int = 7384):
    try:
        os.remove(os.path.expanduser(f"~/.codrninja/server-{port}.ver"))
    except Exception:
        pass


def _debug_diagnostics(port: int = 7384):
    """Print everything needed to diagnose why the wrong codrninja version is running."""
    import shutil as _sh
    import json as _j
    import urllib.request
    import subprocess as _sp

    def line(label, value):
        print(f"  {label:<28} {value}")

    print("=" * 68)
    print("codrninja diagnostic report")
    print("=" * 68)

    print("\n[1] THIS PROCESS")
    line("sys.argv[0]:", sys.argv[0] if sys.argv else '(empty)')
    line("abspath(argv[0]):", os.path.abspath(sys.argv[0]) if sys.argv else '(empty)')
    line("sys.executable:", sys.executable)
    line("cli.py __file__:", os.path.abspath(__file__))
    line("os.getcwd():", os.getcwd())
    try:
        from codrninja import __version__
        line("imported __version__:", __version__)
    except Exception as e:
        line("imported __version__:", f"ERROR {e}")
    try:
        import importlib.metadata
        line("importlib.metadata:", importlib.metadata.version("codrninja"))
    except Exception as e:
        line("importlib.metadata:", f"ERROR {e}")

    print("\n[2] EVERY codrninja BINARY IN PATH")
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    found_any = False
    seen = set()
    for d in path_dirs:
        cd = os.path.join(d, 'codrninja')
        if os.path.exists(cd) and cd not in seen:
            seen.add(cd)
            found_any = True
            try:
                real = os.path.realpath(cd)
                print(f"  {cd}  →  {real}")
            except Exception:
                print(f"  {cd}")
    if not found_any:
        print("  (none found on PATH)")
    line("\nshutil.which:", _sh.which('codrninja') or '(not found)')

    print("\n[3] PIPX INSTALLATION")
    try:
        r = _sp.run(['pipx', 'list', '--short'], capture_output=True, text=True, timeout=10)
        print(f"  pipx list --short:\n{r.stdout.rstrip() or '(empty)'}")
    except Exception as e:
        line("pipx list:", f"ERROR {e}")

    print("\n[4] SYSTEM PIP INSTALLATIONS (potential conflicts)")
    candidates = [
        '/usr/local/bin/codrninja',
        '/usr/bin/codrninja',
        '/opt/data/home/.local/bin/codrninja',
        os.path.expanduser('~/.local/bin/codrninja'),
    ]
    for c in candidates:
        if os.path.exists(c) and c not in seen:
            seen.add(c)
            try:
                real = os.path.realpath(c)
                print(f"  {c}  →  {real}")
            except Exception:
                print(f"  {c}")

    print("\n[5] INSTALLED TUI BUNDLE  (~/.codrninja/tui)")
    tui_pkg = os.path.expanduser('~/.codrninja/tui/package.json')
    if os.path.isfile(tui_pkg):
        try:
            with open(tui_pkg) as f:
                pkg = _j.load(f)
            line("codrninja_version stamp:", pkg.get('codrninja_version', '(not set)'))
        except Exception as e:
            line("read package.json:", f"ERROR {e}")
    else:
        line("status:", "(not installed)")

    print("\n[6] BUNDLED TUI (inside currently running package)")
    bundle_pkg = os.path.join(os.path.dirname(__file__), '_tui_bundle', 'package.json')
    if os.path.isfile(bundle_pkg):
        try:
            with open(bundle_pkg) as f:
                pkg = _j.load(f)
            line("path:", bundle_pkg)
            line("codrninja_version stamp:", pkg.get('codrninja_version', '(not set)'))
        except Exception as e:
            line("read package.json:", f"ERROR {e}")
    else:
        line("status:", f"NOT FOUND at {bundle_pkg}")

    print(f"\n[7] SERVER ON PORT {port}")
    line("port in use:", _port_in_use(port))
    try:
        r = urllib.request.urlopen(f'http://127.0.0.1:{port}/version', timeout=2)
        data = _j.loads(r.read())
        line("/version returns:", data.get('version', '(missing field)'))
    except Exception as e:
        line("/version returns:", f"unreachable ({type(e).__name__})")

    print("\n[8] PROCESSES BINDING PORT 7384")
    try:
        r = _sp.run(['lsof', '-i', f':{port}'], capture_output=True, text=True, timeout=5)
        if r.stdout.strip():
            print("  lsof output:")
            for ln in r.stdout.rstrip().split('\n'):
                print(f"    {ln}")
        else:
            print("  lsof: (no output or not available)")
    except Exception as e:
        print(f"  lsof: ERROR {e}")
    try:
        r = _sp.run(['fuser', f'{port}/tcp'], capture_output=True, text=True, timeout=5)
        line("fuser output:", (r.stdout + r.stderr).strip() or '(empty)')
    except Exception as e:
        line("fuser:", f"ERROR {e}")

    print("\n[9] /proc SCAN FOR PORT 7384 (Docker)")
    try:
        hex_port = f'{port:04X}'
        found_inodes = []
        for net_file in ('/proc/net/tcp', '/proc/net/tcp6'):
            try:
                with open(net_file) as f:
                    for ln in f:
                        parts = ln.split()
                        if len(parts) < 10:
                            continue
                        local = parts[1]
                        if ':' in local and local.split(':')[1].upper() == hex_port:
                            found_inodes.append((net_file, parts[9], local))
            except FileNotFoundError:
                pass
        if found_inodes:
            for nf, inode, local in found_inodes:
                print(f"  {nf}: local={local} inode={inode}")
                try:
                    for pid_dir in os.listdir('/proc'):
                        if not pid_dir.isdigit():
                            continue
                        try:
                            for fd in os.listdir(f'/proc/{pid_dir}/fd'):
                                link = os.readlink(f'/proc/{pid_dir}/fd/{fd}')
                                if f'socket:[{inode}]' in link:
                                    cmdline = ''
                                    try:
                                        with open(f'/proc/{pid_dir}/cmdline') as cf:
                                            cmdline = cf.read().replace('\x00', ' ').strip()
                                    except Exception:
                                        pass
                                    print(f"    PID {pid_dir}: {cmdline}")
                        except Exception:
                            pass
                except Exception:
                    pass
        else:
            print("  (no entry for this port in /proc/net/tcp)")
    except Exception as e:
        print(f"  ERROR {e}")

    print("\n[10] FULL PATH ENV")
    for d in path_dirs:
        print(f"  {d}")

    print("\n" + "=" * 68)


def kill_server_cmd(port: int = 7384) -> bool:
    """Public entry point: stop the codrninja server. Returns True if port is free."""
    _clear_version_stamp(port)
    _clear_pid_file(port)
    return _kill_server(port)


def _kill_server(port: int = 7384) -> bool:
    """Kill any running process on the given port. Returns True if port is free afterwards."""
    import signal
    import subprocess as _sp
    import time
    import urllib.request

    def _pids_on_port() -> list:
        pids: list = []
        try:
            r = _sp.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True, timeout=3)
            for p in r.stdout.strip().split('\n'):
                p = p.strip()
                if p.isdigit():
                    pids.append(int(p))
        except Exception:
            pass
        if not pids:
            try:
                r = _sp.run(['fuser', f'{port}/tcp'], capture_output=True, text=True, timeout=3)
                for p in r.stdout.strip().split():
                    if p.strip().isdigit():
                        pids.append(int(p.strip()))
            except Exception:
                pass
        if not pids:
            try:
                hex_port = f'{port:04X}'
                for net_file in ('/proc/net/tcp', '/proc/net/tcp6'):
                    try:
                        with open(net_file) as f:
                            for line in f:
                                parts = line.split()
                                if len(parts) < 10:
                                    continue
                                local = parts[1]
                                inode = parts[9]
                                if ':' in local and local.split(':')[1].upper() == hex_port:
                                    inode_int = int(inode)
                                    for pid_dir in os.listdir('/proc'):
                                        if not pid_dir.isdigit():
                                            continue
                                        try:
                                            for fd in os.listdir(f'/proc/{pid_dir}/fd'):
                                                link = os.readlink(f'/proc/{pid_dir}/fd/{fd}')
                                                if f'socket:[{inode_int}]' in link:
                                                    pids.append(int(pid_dir))
                                        except Exception:
                                            pass
                    except FileNotFoundError:
                        pass
            except Exception:
                pass
        return list(set(pids))

    def _wait_free(seconds: float) -> bool:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if not _port_in_use(port):
                return True
            time.sleep(0.1)
        return False

    # 1. Ask the server to shut itself down via HTTP (works even if PID detection fails,
    #    and works against servers from ANY codrninja installation on this port).
    try:
        urllib.request.urlopen(f'http://127.0.0.1:{port}/shutdown', timeout=2)
        if _wait_free(3.0):
            _clear_pid_file(port)
            return True
    except Exception:
        pass

    # 2. Signal-based kill: PID file + port scan
    pid_from_file = _read_pid_file(port)
    pids = list(set(([pid_from_file] if pid_from_file else []) + _pids_on_port()))
    _clear_pid_file(port)

    if pids:
        for pid in pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
        if _wait_free(3.0):
            return True
        for pid in _pids_on_port():
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        if _wait_free(2.0):
            return True

    # 3. Last resort: fuser -k kills by port directly (no PID detection needed)
    try:
        _sp.run(['fuser', '-k', f'{port}/tcp'], timeout=5, capture_output=True)
        if _wait_free(2.0):
            return True
    except Exception:
        pass

    return not _port_in_use(port)


def _get_installed_version() -> str:
    try:
        from codrninja import __version__
        return __version__
    except Exception:
        return "unknown"


def _get_server_version(port: int = 7384) -> str:
    """Query the running server's /version endpoint directly via HTTP.
    This is the only reliable method — stamp files can be stale or from wrong installations."""
    import urllib.request, json as _json
    try:
        r = urllib.request.urlopen(f'http://127.0.0.1:{port}/version', timeout=2)
        data = _json.loads(r.read())
        ver = data.get('version', '')
        if ver:
            return ver
    except Exception:
        pass
    return 'unknown'


def _start_server_background(port: int = 7384):
    """Start server if not running. If running with a different version, restart it."""
    import subprocess as _sp
    import sys as _sys
    import time

    if _port_in_use(port):
        installed = _get_installed_version()
        running = _get_server_version(port)
        if installed == running:
            return  # Correct version already running — nothing to do

        # Wrong version (possibly from a different/older installation): kill aggressively
        _clear_version_stamp(port)
        killed = _kill_server(port)
        if not killed:
            # Port still occupied — can't start new server safely
            return

    # Use the exact same codrninja binary that's running now — avoids launching
    # a system-wide older version via sys.executable + -m codrninja.
    import shutil as _shutil
    self_exe = os.path.abspath(_sys.argv[0]) if _sys.argv else ''
    if self_exe and os.path.isfile(self_exe) and os.access(self_exe, os.X_OK):
        cmd = [self_exe, 'serve', '--port', str(port)]
    else:
        # Fallback: find codrninja on PATH, else use sys.executable -m codrninja
        on_path = _shutil.which('codrninja')
        if on_path:
            cmd = [on_path, 'serve', '--port', str(port)]
        else:
            cmd = [_sys.executable, '-m', 'codrninja', 'serve', '--port', str(port)]

    proc = _sp.Popen(
        cmd,
        start_new_session=True,
        stdout=_sp.DEVNULL,
        stderr=_sp.DEVNULL,
    )
    _write_pid_file(proc.pid, port)


def _wait_for_server(port: int = 7384, timeout: float = 8.0):
    """Poll /health until server is up or timeout."""
    import time
    import urllib.request
    url = f'http://127.0.0.1:{port}/health'
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=0.5)
            return
        except Exception:
            time.sleep(0.1)
    raise RuntimeError(f'Server did not start within {timeout}s')


def _launch_ts_tui(tui_path: str, session_name: str | None, port: int = 7384):
    """Exec the TypeScript TUI, replacing the current process image."""
    import os
    import shutil
    import subprocess

    env = {**os.environ, 'CODRNINJA_SERVER': f'http://127.0.0.1:{port}'}

    # Let the TUI know which binary to use when restarting the server
    import sys as _sys
    self_exe = os.path.abspath(_sys.argv[0]) if _sys.argv else ''
    if self_exe and os.path.isfile(self_exe) and os.access(self_exe, os.X_OK):
        env['CODRNINJA_BIN'] = self_exe
    elif shutil.which('codrninja'):
        env['CODRNINJA_BIN'] = shutil.which('codrninja')  # type: ignore
    if session_name:
        env['CODRNINJA_SESSION'] = session_name

    node = shutil.which('node') or 'node'

    # Prefer self-contained esbuild bundle (no node_modules needed)
    bundle_entry = os.path.join(tui_path, 'dist', 'bundle.js')
    if os.path.isfile(bundle_entry):
        cmd = [node, bundle_entry]
    else:
        # Fallback: pre-built tsc output (needs node_modules)
        dist_entry = os.path.join(tui_path, 'dist', 'index.js')
        if os.path.isfile(dist_entry):
            cmd = [node, dist_entry]
        else:
            # Last resort: tsx dev mode
            tsx_local = os.path.join(tui_path, 'node_modules', '.bin', 'tsx')
            tsx = shutil.which('tsx') or (tsx_local if os.path.isfile(tsx_local) else None)
            if not tsx:
                if not os.path.isdir(os.path.join(tui_path, 'node_modules')):
                    print('Installing TUI dependencies…')
                    subprocess.run(['npm', 'install', '--silent'], cwd=tui_path,
                                   check=False, timeout=120)
                tsx = tsx_local
            cmd = [tsx, os.path.join(tui_path, 'src', 'index.tsx')]

    # Replace Python process with Node so Ctrl+C goes straight to Node.
    # Force truecolor so the shimmer/hex colors work over SSH too.
    os.execvpe(cmd[0], cmd, {**env, 'FORCE_COLOR': '1', 'COLORTERM': 'truecolor'})


def start_tui(session_name: str = None):
    tui_path = _find_ts_tui() or _setup_bundled_tui()
    if tui_path:
        _start_server_background()
        try:
            _wait_for_server(timeout=15.0)
        except RuntimeError:
            pass  # Server still starting; TUI has its own retry loop
        _launch_ts_tui(tui_path, session_name)
        return

    # Fallback: Textual TUI (no TypeScript TUI found)
    try:
        ai = AICode()
        app = CodrninjaTUI(ai, session_name)
        app.run()
    except ImportError:
        print('[FAIL] Rich not installed. Install with: pip3 install rich')
        print('   Or use: codrninja chat my-session')
        sys.exit(1)
    except Exception as e:
        print(f'[FAIL] Error starting TUI: {e}')
        sys.exit(1)


def start_onboarding():
    ai = AICode()
    app = CodrninjaTUI(ai, 'onboarding')
    app.run()


def handle_skills(args):
    registry = SkillRegistry()
    registry.discover()
    if not args:
        skills = registry.list_skills()
        if not skills:
            print('No skills installed.')
            return
        for skill in skills:
            print(f"{skill['name']}: {skill['description']}")
        return
    error_out('Usage: codrninja skills', False)


def handle_todo(args, automation_mode: bool):
    manager = TodoManager()
    if not args or args[0] == 'list':
        session = args[1] if len(args) > 1 else None
        todos = manager.list(session) if session else manager.list_all()
        payload = [{
            'id': todo.id,
            'session_id': todo.session_id,
            'task': todo.task,
            'status': todo.status,
            'created_at': todo.created_at,
            'completed_at': todo.completed_at,
            'display': format_todo_item(todo),
        } for todo in todos]
        output({'$schema': 'codrninja.todo.list.v1', 'todos': payload}, automation_mode)
        return
    action = args[0]
    if action == 'add':
        if len(args) < 3:
            error_out('Usage: codrninja todo add <session> <task>', automation_mode)
        session = args[1]
        task = ' '.join(args[2:]).strip()
        todo_id = manager.add(task, session)
        todo = manager.get(todo_id)
        output({'$schema': 'codrninja.todo.add.v1', 'success': True, 'todo': {
            'id': todo.id,
            'session_id': todo.session_id,
            'task': todo.task,
            'status': todo.status,
            'created_at': todo.created_at,
            'completed_at': todo.completed_at,
            'display': format_todo_item(todo),
        }}, automation_mode)
        return
    if action == 'done':
        if len(args) < 2:
            error_out('Usage: codrninja todo done <id>', automation_mode)
        ok = manager.complete(args[1])
        if not ok:
            error_out(f"Todo not found: {args[1]}", automation_mode)
        todo = manager.get(args[1])
        output({'$schema': 'codrninja.todo.done.v1', 'success': True, 'todo': {
            'id': todo.id,
            'session_id': todo.session_id,
            'task': todo.task,
            'status': todo.status,
            'created_at': todo.created_at,
            'completed_at': todo.completed_at,
            'display': format_todo_item(todo),
        }}, automation_mode)
        return
    if action == 'remove':
        if len(args) < 2:
            error_out('Usage: codrninja todo remove <id>', automation_mode)
        ok = manager.remove(args[1])
        if not ok:
            error_out(f"Todo not found: {args[1]}", automation_mode)
        output({'$schema': 'codrninja.todo.remove.v1', 'success': True, 'removed': args[1]}, automation_mode)
        return
    error_out('Usage: codrninja todo [list [session]|add <session> <task>|done <id>|remove <id>]', automation_mode)


def handle_permissions(args, automation_mode: bool):
    manager = PermissionManager(mode=Config.from_env().permissions_mode)
    if not args or args[0] == 'list':
        rules = [{
            'pattern': rule.pattern,
            'action': rule.action,
            'scope': rule.scope,
            'agent_type': rule.agent_type,
            'priority': rule.priority,
        } for rule in manager.list_rules()]
        output({'$schema': 'codrninja.permissions.list.v1', 'default': manager.default_action, 'rules': rules}, automation_mode)
        return
    command = args[0]
    if command == 'mode':
        if len(args) < 2:
            error_out('Usage: codrninja permissions mode <none|ask|auto|strict|relaxed|custom>', automation_mode)
        manager.set_mode(args[1])
        output({'$schema': 'codrninja.permissions.mode.v1', 'success': True, 'mode': manager.mode, 'default': manager.default_action}, automation_mode)
        return
    if command == 'add':
        if len(args) < 3:
            error_out('Usage: codrninja permissions add <pattern> <action> [scope]', automation_mode)
        pattern = args[1]
        action = args[2]
        scope = args[3] if len(args) > 3 else 'all'
        manager.add_rule(PermissionRule(pattern, action, scope, 'all', 100))
        output({'$schema': 'codrninja.permissions.add.v1', 'success': True, 'added': pattern}, automation_mode)
        return
    if command == 'remove':
        if len(args) < 2:
            error_out('Usage: codrninja permissions remove <pattern>', automation_mode)
        removed = manager.remove_rule(args[1])
        output({'$schema': 'codrninja.permissions.remove.v1', 'success': removed, 'removed': args[1]}, automation_mode)
        return
    if command == 'default':
        if len(args) < 2:
            error_out('Usage: codrninja permissions default <action>', automation_mode)
        manager.set_default(args[1])
        output({'$schema': 'codrninja.permissions.default.v1', 'success': True, 'default': manager.default_action}, automation_mode)
        return
    if command == 'explain':
        if len(args) < 3:
            error_out('Usage: codrninja permissions explain <action> <path>', automation_mode)
        output({'$schema': 'codrninja.permissions.explain.v1', 'explanation': manager.explain(args[1], args[2], 'build')}, automation_mode)
        return
    error_out('Usage: codrninja permissions [list|mode|add|remove|default|explain]', automation_mode)


def handle_auth_command(args, automation_mode: bool):
    from .auth import OAuthFlow, TokenManager

    token_manager = TokenManager()
    if not args or args[0] == 'status':
        status = token_manager.list_status()
        payload = {'$schema': 'codrninja.auth.status.v1', 'providers': status}
        if not status:
            payload['providers'] = {}
        output(payload, automation_mode)
        return

    action = args[0].lower()
    if action == 'revoke':
        if len(args) < 2:
            error_out('Usage: codrninja auth revoke <provider>', automation_mode)
        provider = args[1].lower()
        removed = token_manager.revoke(provider)
        if not removed:
            error_out(f'No stored OAuth tokens for {provider}', automation_mode)
        output({'$schema': 'codrninja.auth.revoke.v1', 'success': True, 'provider': provider}, automation_mode)
        return

    provider = action
    if provider not in ('anthropic', 'openai'):
        error_out('Usage: codrninja auth <anthropic|openai|status|revoke>', automation_mode)
    flow = OAuthFlow(provider)
    success, detail = flow.run()
    payload = {'$schema': 'codrninja.auth.run.v1', 'success': success, 'provider': provider, 'detail': detail}
    if not success and automation_mode:
        print(json.dumps(payload))
        sys.exit(1)
    if not success:
        error_out(detail, automation_mode)
    output(payload, automation_mode)


def handle_mcp(args, automation_mode: bool):
    manager = MCPManager()
    if not args or args[0] == 'list':
        servers = [{
            'name': server.name,
            'type': server.type,
            'enabled': server.enabled,
            'tool_count': len(server.tools),
        } for server in manager.list_servers()]
        output({'$schema': 'codrninja.mcp.list.v1', 'servers': servers}, automation_mode)
        return
    command = args[0]
    if command == 'add':
        if len(args) < 3:
            error_out('Usage: codrninja mcp add <name> <config_json>', automation_mode)
        name = args[1]
        try:
            config = json.loads(' '.join(args[2:]))
        except json.JSONDecodeError as e:
            error_out(f'Invalid JSON: {e}', automation_mode)
        config['name'] = name
        server = manager.add_server(config)
        output({'$schema': 'codrninja.mcp.add.v1', 'added': server.name}, automation_mode)
        return
    if command == 'remove':
        if len(args) < 2:
            error_out('Usage: codrninja mcp remove <name>', automation_mode)
        output({'$schema': 'codrninja.mcp.remove.v1', 'removed': manager.remove_server(args[1])}, automation_mode)
        return
    if command == 'tools':
        tools = manager.discover_tools(force=True)
        output({'$schema': 'codrninja.mcp.tools.v1', 'tools': tools}, automation_mode)
        return
    error_out('Usage: codrninja mcp [list|add|remove|tools]', automation_mode)


def handle_lsp(args, automation_mode: bool):
    tools = ToolRegistry()
    if not args or args[0] == 'status':
        output({'$schema': 'codrninja.lsp.status.v1', 'servers': tools.lsp.status()}, automation_mode)
        return
    command = args[0]
    if command == 'start':
        if len(args) < 2:
            error_out('Usage: codrninja lsp start <lang>', automation_mode)
        language = args[1]
        client = tools.lsp.get_client(language)
        if not client:
            error_out(tools.lsp.install_hint(language), automation_mode)
        output({'$schema': 'codrninja.lsp.start.v1', 'started': language, 'command': client.command}, automation_mode)
        return
    if command == 'stop':
        if len(args) < 2:
            error_out('Usage: codrninja lsp stop <lang>', automation_mode)
        language = args[1]
        stopped = tools.lsp.stop(language)
        output({'$schema': 'codrninja.lsp.stop.v1', 'stopped': stopped, 'language': language}, automation_mode)
        return
    if command == 'diagnostics':
        if len(args) < 2:
            error_out('Usage: codrninja lsp diagnostics <file>', automation_mode)
        result = tools.lsp_diagnostics(args[1])
        payload = {'$schema': 'codrninja.lsp.diagnostics.v1', 'success': result.success, 'file': args[1], 'diagnostics': result.output if result.success else None, 'error': result.error}
        output(payload, automation_mode)
        return
    error_out('Usage: codrninja lsp [status|start <lang>|stop <lang>|diagnostics <file>]', automation_mode)


def stop_server_entry():
    """Entry point for 'codrninja-stop' — kills the running server.
    Use as a pipx post-install hook: pipx inject codrninja codrninja-stop"""
    kill_server_cmd()
    print("codrninja server stopped.")


if __name__ == '__main__':
    main()
