import sys

new_cmds = """
@main.group("config")
def config_group() -> None:
    \"\"\"Manage CVC global configuration.\"\"\"
    pass

@config_group.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    \"\"\"Set a configuration value in ~/.cvc/config.json.\"\"\"
    import json
    from pathlib import Path
    config_file = Path.home() / ".cvc" / "config.json"
    config = {}
    if config_file.exists():
        with open(config_file, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                pass
    config[key] = value
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    console.print(f"[bold #55AA55]✓[/bold #55AA55] Set [bold]{key}[/bold] = {value}")

@main.command("ignore")
@click.argument("path")
def ignore_cmd(path: str) -> None:
    \"\"\"Automatically append a file or directory to .cvcignore.\"\"\"
    from pathlib import Path
    ignore_file = Path(".cvcignore")
    if not ignore_file.exists():
        ignore_file.touch()
    with open(ignore_file, "a") as f:
        f.write(f"\\n{path}")
    console.print(f"[bold #55AA55]✓[/bold #55AA55] Added [bold]{path}[/bold] to .cvcignore")

@main.command("ui")
def ui_cmd() -> None:
    \"\"\"Open the CVC dashboard in the default web browser.\"\"\"
    import webbrowser
    console.print("[bold #55AA55]Opening CVC UI at http://localhost:8000[/bold #55AA55]")
    webbrowser.open("http://localhost:8000")

@main.command("open")
def open_cmd() -> None:
    \"\"\"Alias for 'cvc ui' to open the CVC dashboard.\"\"\"
    ui_cmd()

@main.command("clean")
@click.option("--force", is_flag=True, help="Force clean without prompt")
def clean_cmd(force: bool) -> None:
    \"\"\"Safely purge old cognitive checkpoints or temporary chat sessions.\"\"\"
    import shutil
    from pathlib import Path
    cache_dir = Path.home() / ".cvc" / "cache"
    if cache_dir.exists():
        if force or click.confirm(f"Are you sure you want to clear {cache_dir}?"):
            shutil.rmtree(cache_dir)
            console.print("[bold #55AA55]✓[/bold #55AA55] Cache cleared successfully.")
    else:
        console.print("[dim]No cache found to clean.[/dim]")

@main.command("clear-cache")
@click.option("--force", is_flag=True, help="Force clean without prompt")
def clear_cache_cmd(force: bool) -> None:
    \"\"\"Alias for 'cvc clean'.\"\"\"
    clean_cmd(force=force)

@main.command("uninstall")
def uninstall_cmd() -> None:
    \"\"\"Completely remove CVC installation and its global binaries.\"\"\"
    import shutil
    from pathlib import Path
    if click.confirm("Are you sure you want to completely uninstall CVC and remove ~/.cvc?", abort=True):
        cvc_dir = Path.home() / ".cvc"
        if cvc_dir.exists():
            shutil.rmtree(cvc_dir)
            console.print("[bold #55AA55]✓[/bold #55AA55] Removed ~/.cvc directory.")
        console.print("[bold #CC3333]Note:[/bold #CC3333] To remove the executable completely, please run:")
        console.print("  [dim]uv tool uninstall tm-ai[/dim]  or  [dim]pip uninstall tm-ai[/dim]")

"""

file_path = "/Users/jkm/projects/cvc/cvc/cli.py"
with open(file_path, "r") as f:
    content = f.read()

marker = 'if __name__ == "__main__":'
if marker in content and '@main.command("uninstall")' not in content:
    content = content.replace(marker, new_cmds + "\n" + marker)
    with open(file_path, "w") as f:
        f.write(content)
    print("Patched cvc/cli.py successfully")
else:
    print("Could not find marker or already patched")
