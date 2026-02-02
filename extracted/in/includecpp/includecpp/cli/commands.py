import click
import subprocess
import shutil
import platform
import os
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from colorama import init as colorama_init, Fore, Style
from .config_parser import CppProjectConfig

# Initialize colorama for Windows ANSI color support
colorama_init()


def _preprocess_doc_option():
    """
    Preprocess sys.argv to handle --doc with optional value.
    Converts: --doc (alone) -> --doc ""
    Keeps: --doc "term" -> --doc "term"
    """
    args = sys.argv[:]
    new_args = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--doc':
            new_args.append(arg)
            # Check if next arg exists and is not another option
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                new_args.append(args[i + 1])
                i += 1
            else:
                # No value provided - add empty string
                new_args.append('')
        else:
            new_args.append(arg)
        i += 1
    sys.argv[:] = new_args


# Preprocess before Click parses arguments
_preprocess_doc_option()


def _is_experimental_enabled() -> bool:
    """Check if experimental features (cppy, ai) are enabled."""
    config_path = Path.home() / '.includecpp' / '.secret'
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            return config.get('experimental_features', False)
        except:
            pass
    return False


# Check once at module load time
_EXPERIMENTAL_ENABLED = _is_experimental_enabled()

# Unicode fallback for Windows terminals with limited encoding
def _supports_unicode():
    """Check if terminal supports Unicode output."""
    if sys.platform == 'win32':
        try:
            # Handle frozen PyInstaller where stdout may be None
            if sys.stdout is None:
                return False
            # Test if we can encode Unicode box characters
            '╔═╗'.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, LookupError, AttributeError):
            return False
    return True

# ASCII fallbacks for box-drawing characters
_UNICODE = _supports_unicode()
_BOX_TOP = "╔══════════════════════════════════════════════════════════════╗" if _UNICODE else "+--------------------------------------------------------------+"
_BOX_BOTTOM = "╚══════════════════════════════════════════════════════════════╝" if _UNICODE else "+--------------------------------------------------------------+"
_BOX_SIDE = "║" if _UNICODE else "|"
_SEC_TOP = "┌─────────────────────────────────────────────────────────────┐" if _UNICODE else "+-------------------------------------------------------------+"
_SEC_BOTTOM = "└─────────────────────────────────────────────────────────────┘" if _UNICODE else "+-------------------------------------------------------------+"
_SEC_SIDE = "│" if _UNICODE else "|"
_HLINE = "═" if _UNICODE else "-"
_CHECK = ""  # Removed check marks per user request
_CROSS = "✗" if _UNICODE else "[X]"
_BULLET = "•" if _UNICODE else "*"
_ARROW = "→" if _UNICODE else "->"
_TRIANGLE = "▶" if _UNICODE else ">"
_DIAMOND = "◆" if _UNICODE else "*"

def _safe_echo(text, **kwargs):
    """Echo text with Unicode fallback for unsupported terminals."""
    try:
        click.secho(text, **kwargs)
    except UnicodeEncodeError:
        # Fallback: replace Unicode with ASCII
        ascii_text = text
        replacements = [
            ('╔', '+'), ('╗', '+'), ('╚', '+'), ('╝', '+'),
            ('┌', '+'), ('┐', '+'), ('└', '+'), ('┘', '+'),
            ('═', '-'), ('─', '-'), ('║', '|'), ('│', '|'),
            ('✗', '[X]'), ('✓', '[OK]'), ('❌', '[X]'), ('•', '*'),
            ('→', '->'), ('▶', '>'), ('◆', '*'),
            ('\u2011', '-'), ('\u2010', '-'),
            ('\u2013', '-'), ('\u2014', '--'),
            ('\u2018', "'"), ('\u2019', "'"),
            ('\u201c', '"'), ('\u201d', '"'),
            ('\u2022', '*'), ('\u2026', '...'),
            ('\u00a0', ' '),
        ]
        for uni, ascii_char in replacements:
            ascii_text = ascii_text.replace(uni, ascii_char)
        try:
            click.secho(ascii_text, **kwargs)
        except UnicodeEncodeError:
            click.secho(ascii_text.encode('ascii', errors='replace').decode('ascii'), **kwargs)

def _render_readme_with_colors(readme_text):
    """Render README.md with color highlighting in terminal."""
    lines = readme_text.split('\n')

    for line in lines:
        stripped = line.strip()

        # Headers
        if stripped.startswith('# '):
            click.echo()
            click.secho("=" * 70, fg='cyan', bold=True)
            click.secho(stripped[2:], fg='cyan', bold=True)
            click.secho("=" * 70, fg='cyan', bold=True)
        elif stripped.startswith('## '):
            click.echo()
            click.secho("+" + "-" * 68 + "+", fg='blue', bold=True)
            click.secho("| " + stripped[3:], fg='blue', bold=True)
            click.secho("+" + "-" * 68 + "+", fg='blue')
        elif stripped.startswith('### '):
            click.echo()
            click.secho("  " + stripped[4:], fg='green', bold=True)
            click.secho("  " + "-" * len(stripped[4:]), fg='green')
        elif stripped.startswith('#### '):
            click.secho("    " + stripped[5:], fg='yellow', bold=True)
        # Code blocks
        elif stripped.startswith('```'):
            lang = stripped[3:] if len(stripped) > 3 else ''
            if lang:
                click.secho("    [" + lang + "]", fg='magenta')
            else:
                click.echo()
        # Bullet points
        elif stripped.startswith('- '):
            click.echo("  * ", nl=False)
            click.echo(stripped[2:])
        elif stripped.startswith('* '):
            click.echo("  * ", nl=False)
            click.echo(stripped[2:])
        # Numbered lists
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == '.':
            click.secho("  " + stripped[:2] + " ", fg='yellow', nl=False)
            click.echo(stripped[3:])
        # Code lines (indented with 4+ spaces in markdown code blocks)
        elif line.startswith('    ') or line.startswith('\t'):
            click.secho("    " + stripped, fg='bright_black')
        # Bold text **text**
        elif '**' in stripped:
            # Simple bold rendering
            parts = stripped.split('**')
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Bold parts
                    click.secho(part, fg='white', bold=True, nl=False)
                else:
                    click.echo(part, nl=False)
            click.echo()
        # Horizontal rules
        elif stripped.startswith('---'):
            click.secho("-" * 70, fg='bright_black')
        # Empty lines
        elif not stripped:
            click.echo()
        # Regular text
        else:
            click.echo("  " + stripped)


def _get_changelog_path():
    """Get path to CHANGELOG.md file."""
    # Try package location first
    package_dir = Path(__file__).parent.parent
    changelog_path = package_dir / 'CHANGELOG.md'
    if changelog_path.exists():
        return changelog_path
    # Fallback to current directory
    cwd_path = Path.cwd() / 'CHANGELOG.md'
    if cwd_path.exists():
        return cwd_path
    return None


def _parse_changelog_entries(content: str) -> list:
    """Parse changelog into list of version entries.

    Returns list of tuples: (version_header, content_lines)
    """
    entries = []
    lines = content.split('\n')
    current_version = None
    current_lines = []

    for line in lines:
        # Match version headers like "## v4.2.0 (2025-01-08)"
        if line.startswith('## '):
            # Save previous entry
            if current_version:
                entries.append((current_version, current_lines))
            current_version = line[3:].strip()
            current_lines = []
        elif current_version:
            current_lines.append(line)

    # Save last entry
    if current_version:
        entries.append((current_version, current_lines))

    return entries


def _show_changelog(count: int = 2, show_all: bool = False):
    """Display changelog from local CHANGELOG.md file.

    Args:
        count: Number of version entries to show (default 2)
        show_all: If True, show all entries
    """
    _safe_echo("=" * 70)
    _safe_echo("IncludeCPP Changelog", fg='cyan', bold=True)
    _safe_echo("=" * 70)
    _safe_echo("")

    changelog_path = _get_changelog_path()
    if not changelog_path:
        _safe_echo("CHANGELOG.md not found.", fg='yellow')
        _safe_echo("")
        _safe_echo("=" * 70)
        return

    try:
        content = changelog_path.read_text(encoding='utf-8')
        entries = _parse_changelog_entries(content)

        if not entries:
            _safe_echo("No changelog entries found.", fg='yellow')
            _safe_echo("")
            _safe_echo("=" * 70)
            return

        # Determine how many to show
        if show_all:
            entries_to_show = entries
        else:
            entries_to_show = entries[:count]

        _safe_echo(f"Showing {len(entries_to_show)} of {len(entries)} releases", fg='bright_black')
        _safe_echo("")

        for version, lines in entries_to_show:
            _safe_echo(version, fg='yellow', bold=True)

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                elif stripped.startswith('### '):
                    _safe_echo("  " + stripped[4:], fg='cyan', bold=True)
                elif stripped.startswith('- '):
                    _safe_echo("    " + stripped)
                elif stripped.startswith('---'):
                    _safe_echo("")
                else:
                    _safe_echo("    " + stripped)

            _safe_echo("")

        if not show_all and len(entries) > count:
            _safe_echo(f"Use --changelog --all to see all {len(entries)} releases", fg='bright_black')
            _safe_echo(f"Or --changelog --{len(entries)} to see specific count", fg='bright_black')

    except Exception as e:
        _safe_echo(f"Error reading changelog: {e}", fg='red', err=True)

    _safe_echo("")
    _safe_echo("=" * 70)


def _get_doc_path():
    """Get path to README.md or DOCUMENTATION.md file."""
    package_dir = Path(__file__).parent.parent

    # 1. Check if running from development (project root has README.md)
    project_root = package_dir.parent
    readme_path = project_root / 'README.md'
    if readme_path.exists() and (project_root / 'pyproject.toml').exists():
        # We're in development mode - use project README
        return readme_path

    # 2. DOCUMENTATION.md in package (installed package)
    doc_path = package_dir / 'DOCUMENTATION.md'
    if doc_path.exists():
        return doc_path

    # 3. README.md in package dir
    readme_pkg = package_dir / 'README.md'
    if readme_pkg.exists():
        return readme_pkg

    # 4. Try current working directory
    cwd_readme = Path.cwd() / 'README.md'
    if cwd_readme.exists():
        return cwd_readme
    cwd_doc = Path.cwd() / 'DOCUMENTATION.md'
    if cwd_doc.exists():
        return cwd_doc

    # 5. Try using importlib.resources for installed package
    try:
        import importlib.resources as pkg_resources
        try:
            # Python 3.9+
            files = pkg_resources.files('includecpp')
            doc_file = files / 'DOCUMENTATION.md'
            if doc_file.is_file():
                return Path(str(doc_file))
        except Exception:
            pass
    except ImportError:
        pass

    return None


def _show_doc(search_term: str = None):
    """Display documentation from local DOCUMENTATION.md file.

    Args:
        search_term: Optional search term to filter content
    """
    _safe_echo("=" * 70)
    _safe_echo("IncludeCPP Documentation", fg='cyan', bold=True)
    _safe_echo("=" * 70)
    _safe_echo("")

    doc_path = _get_doc_path()
    if not doc_path:
        _safe_echo("DOCUMENTATION.md not found.", fg='yellow')
        _safe_echo("")
        _safe_echo("=" * 70)
        return

    try:
        content = doc_path.read_text(encoding='utf-8')

        if search_term:
            # Search mode - find matching sections
            _safe_echo(f"Searching for: '{search_term}'", fg='green', bold=True)
            _safe_echo("")

            # Split into sections (## headers)
            sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

            # Find matching sections
            matches = []
            for section in sections:
                if search_term.lower() in section.lower():
                    # Get section title
                    title_match = re.match(r'^## (.+)$', section, re.MULTILINE)
                    if title_match:
                        matches.append((title_match.group(1), section))

            if matches:
                _safe_echo(f"Found {len(matches)} matching section(s):", fg='green')
                _safe_echo("")

                for title, section_content in matches[:5]:  # Limit to 5
                    _safe_echo(f"## {title}", fg='yellow', bold=True)

                    # Highlight search term
                    lines = section_content.split('\n')
                    for line in lines[:30]:  # Limit lines per section
                        stripped = line.strip()
                        if not stripped or stripped.startswith('## '):
                            continue

                        # Highlight matches
                        if search_term.lower() in stripped.lower():
                            # Simple highlight - wrap matches
                            highlighted = re.sub(
                                f'({re.escape(search_term)})',
                                lambda m: click.style(m.group(1), fg='green', bold=True),
                                stripped,
                                flags=re.IGNORECASE
                            )
                            _safe_echo("  " + highlighted)
                        else:
                            _safe_echo("  " + stripped)

                    _safe_echo("")
                    _safe_echo("-" * 40)
                    _safe_echo("")

                if len(matches) > 5:
                    _safe_echo(f"... and {len(matches) - 5} more sections", fg='bright_black')
            else:
                _safe_echo(f"No matches found for '{search_term}'", fg='yellow')
                _safe_echo("")
                _safe_echo("Try searching for:")
                _safe_echo("  - Commands: init, rebuild, plugin, auto")
                _safe_echo("  - Features: CSSL, AI, CPPY, classes, functions")
                _safe_echo("  - Syntax: $, @, <==, define, class")
        else:
            # Full documentation display
            _safe_echo("+" + "=" * 68 + "+", fg='red', bold=True)
            _safe_echo("|  IMPORTANT: All C++ code MUST be in 'namespace includecpp { }'     |", fg='red', bold=True)
            _safe_echo("+" + "=" * 68 + "+", fg='red', bold=True)
            _safe_echo("")
            _render_readme_with_colors(content)

    except Exception as e:
        _safe_echo(f"Error reading documentation: {e}", fg='red', err=True)

    _safe_echo("")
    _safe_echo("=" * 70)


def _show_pypi_stats():
    """Show detailed PyPI download statistics with charts."""
    from datetime import datetime, timedelta
    import json
    try:
        import pypistats
    except ImportError:
        click.secho("Installing pypistats...", fg='yellow')
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pypistats', '-q'])
        import pypistats

    package = 'includecpp'

    # Header
    click.echo()
    click.secho("=" * 70, fg='cyan', bold=True)
    click.secho("   INCLUDECPP - PyPI Download Statistics (CONFIDENTIAL)", fg='cyan', bold=True)
    click.secho("=" * 70, fg='cyan', bold=True)
    click.echo()

    def draw_bar(value, max_value, width=40, fill_char='#', empty_char='.'):
        """Draw a horizontal bar chart using ASCII."""
        if max_value == 0:
            return empty_char * width
        filled = int((value / max_value) * width)
        return fill_char * filled + empty_char * (width - filled)

    def format_number(n):
        """Format number with K/M suffix."""
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        elif n >= 1_000:
            return f"{n/1_000:.1f}K"
        return str(n)

    def section_header(title, color='green'):
        """Print section header using ASCII."""
        click.secho("+" + "-" * 68 + "+", fg=color)
        click.secho(f"|  {title:<65}|", fg=color, bold=True)
        click.secho("+" + "-" * 68 + "+", fg=color)

    try:
        # === ALL TIME DOWNLOADS ===
        section_header("ALL TIME DOWNLOADS (since first release)", 'green')

        try:
            overall = pypistats.overall(package, format='json')
            overall_data = json.loads(overall)
            total_with_mirrors = 0
            total_without_mirrors = 0
            for row in overall_data.get('data', []):
                if row.get('category') == 'with_mirrors':
                    total_with_mirrors = row.get('downloads', 0)
                elif row.get('category') == 'without_mirrors':
                    total_without_mirrors = row.get('downloads', 0)

            click.echo()
            click.echo(f"  {'All downloads (incl. mirrors):':<35} {click.style(format_number(total_with_mirrors), fg='bright_white', bold=True):>10}")
            click.echo(f"  {'Excl. known mirrors:':<35} {click.style(format_number(total_without_mirrors), fg='bright_white', bold=True):>10}")
            click.echo()
            click.secho("  Note: 'Excl. mirrors' still includes CI/CD, Docker, reinstalls.", fg='bright_black')
            click.secho("  Actual unique users is likely 5-20% of this number.", fg='bright_black')
            click.echo()
        except Exception as e:
            click.secho(f"  Could not fetch overall stats: {e}", fg='yellow')

        # === RECENT DOWNLOADS (Last 30 days breakdown) ===
        section_header("RECENT DOWNLOADS (Last 30 Days)", 'blue')

        try:
            recent = pypistats.recent(package, format='json')
            recent_data = json.loads(recent) if isinstance(recent, str) else recent
            # Handle both dict format {'data': [...]} and list format [...]
            if isinstance(recent_data, dict):
                rows = recent_data.get('data', [])
            elif isinstance(recent_data, list):
                rows = recent_data
            else:
                rows = []

            click.echo()
            # Find max for bar scaling
            max_downloads = max((r.get('downloads', 0) for r in rows if isinstance(r, dict)), default=1)
            for row in rows:
                if not isinstance(row, dict):
                    continue
                period = row.get('category', 'unknown')
                downloads = row.get('downloads', 0)
                period_display = {'last_day': 'Last Day', 'last_week': 'Last Week', 'last_month': 'Last Month'}.get(period, period)
                bar = draw_bar(downloads, max_downloads, width=30)
                click.echo(f"  {period_display:<15} {click.style(bar, fg='green')} {click.style(format_number(downloads), fg='bright_white', bold=True):>10}")
            click.echo()
        except Exception as e:
            click.secho(f"  Could not fetch recent stats: {e}", fg='yellow')

        # === PYTHON VERSION BREAKDOWN (Last 30 days with classification) ===
        section_header("PYTHON VERSION (Last 30 Days - classified only)", 'magenta')

        try:
            python_major = pypistats.python_major(package, format='json')
            major_data = json.loads(python_major)
            click.echo()
            versions = [(row.get('category'), row.get('downloads', 0)) for row in major_data.get('data', []) if row.get('category') != 'null']
            versions.sort(key=lambda x: x[1], reverse=True)
            max_dl = versions[0][1] if versions else 1
            for version, downloads in versions[:5]:
                bar = draw_bar(downloads, max_dl, width=35, fill_char='=', empty_char='.')
                pct = (downloads / sum(d for _, d in versions)) * 100 if versions else 0
                click.echo(f"  Python {version:<6} {click.style(bar, fg='magenta')} {format_number(downloads):>8} ({pct:>5.1f}%)")
            click.echo()
        except Exception as e:
            click.secho(f"  Could not fetch Python version stats: {e}", fg='yellow')

        # === PYTHON MINOR VERSION (3.10, 3.11, 3.12, etc.) ===
        section_header("PYTHON MINOR VERSION (Last 30 Days - classified only)", 'yellow')

        try:
            python_minor = pypistats.python_minor(package, format='json')
            minor_data = json.loads(python_minor)
            click.echo()
            versions = [(row.get('category'), row.get('downloads', 0)) for row in minor_data.get('data', []) if row.get('category') and row.get('category') != 'null']
            versions.sort(key=lambda x: x[1], reverse=True)
            max_dl = versions[0][1] if versions else 1
            for version, downloads in versions[:8]:
                bar = draw_bar(downloads, max_dl, width=30, fill_char='#', empty_char='.')
                pct = (downloads / sum(d for _, d in versions)) * 100 if versions else 0
                click.echo(f"  {version:<8} {click.style(bar, fg='yellow')} {format_number(downloads):>8} ({pct:>5.1f}%)")
            click.echo()
        except Exception as e:
            click.secho(f"  Could not fetch Python minor version stats: {e}", fg='yellow')

        # === SYSTEM/OS BREAKDOWN ===
        section_header("OPERATING SYSTEM (Last 30 Days - classified only)", 'red')

        try:
            system_stats = pypistats.system(package, format='json')
            system_data = json.loads(system_stats)
            click.echo()
            systems = [(row.get('category'), row.get('downloads', 0)) for row in system_data.get('data', []) if row.get('category') and row.get('category') != 'null']
            systems.sort(key=lambda x: x[1], reverse=True)
            max_dl = systems[0][1] if systems else 1
            os_labels = {'Windows': '[Win]', 'Linux': '[Lin]', 'Darwin': '[Mac]', 'null': '[?]'}
            for system, downloads in systems[:5]:
                bar = draw_bar(downloads, max_dl, width=35, fill_char='=', empty_char='.')
                pct = (downloads / sum(d for _, d in systems)) * 100 if systems else 0
                label = os_labels.get(system, '     ')
                click.echo(f"  {label} {system:<10} {click.style(bar, fg='red')} {format_number(downloads):>8} ({pct:>5.1f}%)")
            click.echo()
        except Exception as e:
            click.secho(f"  Could not fetch system stats: {e}", fg='yellow')

        # === DAILY DOWNLOADS TREND (Last 14 days) ===
        section_header("DAILY DOWNLOADS TREND (Last 14 Days)", 'cyan')

        try:
            # Fetch daily data directly from pypistats.org API
            import urllib.request
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
            api_url = f"https://pypistats.org/api/packages/{package}/overall?start_date={start_date}&end_date={end_date}"

            req = urllib.request.Request(api_url, headers={'User-Agent': 'IncludeCPP-CLI'})
            with urllib.request.urlopen(req, timeout=10) as response:
                daily_data = json.loads(response.read().decode())

            click.echo()
            days = []
            for row in daily_data.get('data', []):
                date_val = row.get('date')
                if date_val and row.get('category') == 'without_mirrors':
                    days.append((date_val, row.get('downloads', 0)))

            if days:
                days.sort(key=lambda x: x[0])
                max_dl = max(d for _, d in days) if days else 1

                # Draw sparkline-style chart
                click.echo("  Date        Downloads")
                click.echo("  " + "-" * 50)
                for date, downloads in days[-14:]:
                    bar = draw_bar(downloads, max_dl, width=30, fill_char='=', empty_char=' ')
                    date_short = date[5:]  # MM-DD format
                    click.echo(f"  {date_short}    {click.style(bar, fg='cyan')} {format_number(downloads):>6}")

                click.echo()
                # Summary stats
                total = sum(d for _, d in days)
                avg = total / len(days) if days else 0
                peak = max(d for _, d in days)
                peak_date = [date for date, d in days if d == peak][0] if days else 'N/A'

                click.echo(f"  {'14-Day Total:':<20} {click.style(format_number(total), fg='bright_white', bold=True)}")
                click.echo(f"  {'Daily Average:':<20} {click.style(format_number(int(avg)), fg='bright_white')}")
                click.echo(f"  {'Peak Day:':<20} {click.style(f'{format_number(peak)} ({peak_date})', fg='green', bold=True)}")
            else:
                click.secho("  No daily data available yet (data updates daily)", fg='yellow')
            click.echo()
        except Exception as e:
            click.secho(f"  Could not fetch daily trend: {e}", fg='yellow')

        # === REALISTIC ESTIMATE ===
        section_header("REALISTIC USER ESTIMATE", 'bright_black')
        click.echo()
        click.secho("  PyPI download counts are NOT unique users. They include:", fg='bright_black')
        click.secho("  * CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)", fg='bright_black')
        click.secho("  * Docker container builds", fg='bright_black')
        click.secho("  * Package reinstalls and cache misses", fg='bright_black')
        click.secho("  * Multiple machines per user (laptop, PC, VM, WSL)", fg='bright_black')
        click.secho("  * Corporate proxies (Artifactory, devpi)", fg='bright_black')
        click.echo()
        click.secho("  Industry estimate: Actual unique humans ~ 5-15% of downloads", fg='yellow')
        try:
            if total_without_mirrors:
                low_est = int(total_without_mirrors * 0.05)
                high_est = int(total_without_mirrors * 0.15)
                click.echo(f"  For {format_number(total_without_mirrors)} downloads: ~{format_number(low_est)} - {format_number(high_est)} unique users")
        except:
            pass
        click.echo()

        # === FOOTER ===
        click.echo()
        click.secho("=" * 70, fg='cyan', bold=True)
        click.secho(f"  Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fg='bright_black')
        click.secho(f"  Package: includecpp | Source: PyPI Stats API (BigQuery)", fg='bright_black')
        click.secho("=" * 70, fg='cyan', bold=True)
        click.echo()

    except Exception as e:
        click.secho(f"Error fetching PyPI stats: {e}", fg='red')
        import traceback
        traceback.print_exc()


def _make_executable(script_path: str, output_name: str = None, onefile: bool = True, console: bool = True, icon: str = None):
    """Build .exe from Python script using PyInstaller.

    Auto-detects dependencies, rebuilds includecpp if needed, and cleans up.

    Args:
        script_path: Path to the Python script
        output_name: Optional custom name for output executable (without .exe)
        onefile: Build as single file (True) or directory (False)
        console: Show console window (True) or windowed mode (False)
        icon: Path to icon file (.ico)
    """
    import re
    import shutil
    import ast

    script_path = Path(script_path).resolve()
    if not script_path.exists():
        click.secho(f"Error: File not found: {script_path}", fg='red')
        return

    if script_path.suffix.lower() != '.py':
        click.secho(f"Error: Not a Python file: {script_path}", fg='red')
        return

    script_dir = script_path.parent
    script_name = output_name if output_name else script_path.stem

    click.echo()
    click.secho(f"Building executable from: {script_path.name}", fg='cyan', bold=True)
    if output_name:
        click.echo(f"  Output name: {output_name}.exe")
    click.echo("=" * 50)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        click.echo(f"  PyInstaller: v{PyInstaller.__version__}")
    except ImportError:
        click.secho("Error: PyInstaller is not installed.", fg='red')
        click.echo("Install it with: pip install pyinstaller")
        return

    # Read and analyze the script
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except Exception as e:
        click.secho(f"Error reading script: {e}", fg='red')
        return

    # Detect imports
    detected_imports = set()
    uses_includecpp = False
    uses_pyqt6 = False
    uses_pyqt5 = False
    uses_tkinter = False
    uses_pyside6 = False
    uses_pyside2 = False

    # Simple regex-based import detection
    import_patterns = [
        r'^import\s+(\w+)',
        r'^from\s+(\w+)',
    ]

    for line in script_content.split('\n'):
        line = line.strip()
        for pattern in import_patterns:
            match = re.match(pattern, line)
            if match:
                module = match.group(1)
                detected_imports.add(module)
                if module == 'includecpp':
                    uses_includecpp = True
                elif module == 'PyQt6':
                    uses_pyqt6 = True
                elif module == 'PyQt5':
                    uses_pyqt5 = True
                elif module == 'PySide6':
                    uses_pyside6 = True
                elif module == 'PySide2':
                    uses_pyside2 = True
                elif module == 'tkinter':
                    uses_tkinter = True

    click.echo(f"  Detected imports: {len(detected_imports)}")

    # Build data files list for PyInstaller
    datas = []
    binaries = []  # For .pyd/.so files
    hidden_imports = []

    # If includecpp is used, rebuild and include the compiled modules
    includecpp_files_to_copy = []  # Initialize here for later use

    if uses_includecpp:
        click.echo()
        click.secho("  IncludeCPP detected - checking for modules...", fg='yellow')

        # Look for cpp.proj in script directory or parent directories
        cpp_proj_path = None
        search_dir = script_dir
        for _ in range(5):  # Search up to 5 levels up
            candidate = search_dir / 'cpp.proj'
            if candidate.exists():
                cpp_proj_path = candidate
                break
            if search_dir.parent == search_dir:
                break
            search_dir = search_dir.parent

        if cpp_proj_path:
            click.echo(f"    Found project: {cpp_proj_path}")

            # Load project config to find build directory
            try:
                import json
                with open(cpp_proj_path, 'r') as f:
                    proj_config = json.load(f)

                proj_dir = cpp_proj_path.parent

                # Rebuild the modules
                click.echo("    Rebuilding C++ modules...")
                try:
                    from ..core.build_manager import BuildManager
                    from .config_parser import CppProjectConfig
                    # detect_compiler is defined in this file

                    config = CppProjectConfig(config_path=cpp_proj_path)
                    project_root = cpp_proj_path.parent
                    compiler = detect_compiler()
                    build_dir_path = config.get_build_dir(compiler)
                    build_dir_path.mkdir(parents=True, exist_ok=True)

                    builder = BuildManager(project_root, build_dir_path, config)
                    success = builder.rebuild(incremental=True)

                    if success:
                        click.secho("    Rebuild complete!", fg='green')
                    else:
                        click.secho("    Warning: Rebuild had errors", fg='yellow')
                except Exception as e:
                    click.secho(f"    Warning: Rebuild failed: {e}", fg='yellow')

                # Use the build directory from the project config (already computed above)
                build_dir = build_dir_path

                # Store paths for copying AFTER PyInstaller completes
                # (Don't bundle into exe - create external includecpp.dll instead)
                if build_dir.exists():
                    ext = '.pyd' if sys.platform == 'win32' else '.so'
                    bindings_dir = build_dir / 'bindings'

                    # Find api.pyd (or api.so)
                    pyd_files = list(bindings_dir.glob(f'*{ext}')) if bindings_dir.exists() else []
                    if not pyd_files:
                        pyd_files = list(build_dir.glob(f'**/*{ext}'))

                    if pyd_files:
                        # Store the main api.pyd path for creating includecpp.dll
                        api_pyd = pyd_files[0]  # Usually api.pyd
                        includecpp_files_to_copy.append(('api', api_pyd))
                        click.echo(f"    Found: {api_pyd.name} (will create includecpp.dll)")

                    # Find runtime DLLs
                    if bindings_dir.exists():
                        dll_files = list(bindings_dir.glob('*.dll'))
                        for dll_file in dll_files:
                            includecpp_files_to_copy.append(('dll', dll_file))
                            click.echo(f"    Found: {dll_file.name}")

                    if pyd_files:
                        click.secho(f"    Will copy {len(includecpp_files_to_copy)} file(s) to output directory", fg='green')
                    else:
                        click.secho("    Warning: No compiled modules found in build directory", fg='yellow')
                else:
                    click.secho("    Warning: Build directory not found", fg='yellow')

            except Exception as e:
                click.secho(f"    Warning: Could not process cpp.proj: {e}", fg='yellow')
        else:
            click.secho("    Warning: cpp.proj not found. C++ modules may not be included.", fg='yellow')

        hidden_imports.append('includecpp')
        hidden_imports.append('api')  # The compiled module

    # Add GUI-specific settings
    if uses_pyqt6:
        click.echo("  PyQt6 detected")
        hidden_imports.extend(['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'])
    if uses_pyqt5:
        click.echo("  PyQt5 detected")
        hidden_imports.extend(['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'])
    if uses_pyside6:
        click.echo("  PySide6 detected")
        hidden_imports.extend(['PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'])
    if uses_pyside2:
        click.echo("  PySide2 detected")
        hidden_imports.extend(['PySide2', 'PySide2.QtCore', 'PySide2.QtGui', 'PySide2.QtWidgets'])

    # Build PyInstaller command
    click.echo()
    click.secho("Building executable...", fg='cyan')

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--noconfirm',
        '--clean',
    ]

    if onefile:
        cmd.append('--onefile')
    else:
        cmd.append('--onedir')

    if console:
        cmd.append('--console')
    else:
        cmd.append('--windowed')

    if icon:
        cmd.extend(['--icon', str(Path(icon).resolve())])

    # Set output name if specified
    if output_name:
        cmd.extend(['--name', output_name])

    # Add data files
    for src, dest in datas:
        cmd.extend(['--add-data', f'{src}{os.pathsep}{dest}'])

    # Add binary files (.pyd/.so)
    for src, dest in binaries:
        cmd.extend(['--add-binary', f'{src}{os.pathsep}{dest}'])

    # Add hidden imports
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])

    # Set output directory to script directory
    cmd.extend(['--distpath', str(script_dir)])
    cmd.extend(['--workpath', str(script_dir / 'build')])
    cmd.extend(['--specpath', str(script_dir)])

    # Add the script
    cmd.append(str(script_path))

    # Run PyInstaller
    try:
        result = subprocess.run(cmd, cwd=str(script_dir), capture_output=True, text=True)

        if result.returncode != 0:
            click.secho("PyInstaller failed!", fg='red')
            if result.stderr:
                click.echo(result.stderr[-2000:])  # Show last 2000 chars of error
            return

        click.secho("PyInstaller completed!", fg='green')

    except Exception as e:
        click.secho(f"Error running PyInstaller: {e}", fg='red')
        return

    # Copy includecpp.dll and runtime DLLs to output directory
    if uses_includecpp and includecpp_files_to_copy:
        click.echo()
        click.echo("Creating includecpp.dll...")
        try:
            for file_type, file_path in includecpp_files_to_copy:
                if file_type == 'api':
                    # Copy api.pyd as includecpp.dll
                    dll_output = script_dir / 'includecpp.dll'
                    shutil.copy2(file_path, dll_output)
                    click.secho("  Created: includecpp.dll", fg='green')
                else:
                    # Copy runtime DLLs
                    dest = script_dir / file_path.name
                    shutil.copy2(file_path, dest)
                    click.echo(f"  Copied: {file_path.name}")
        except Exception as e:
            click.secho(f"  Warning: Could not copy files: {e}", fg='yellow')

    # Clean up
    click.echo()
    click.echo("Cleaning up...")

    # Remove build directory
    build_path = script_dir / 'build'
    if build_path.exists():
        try:
            shutil.rmtree(build_path)
            click.echo("  Removed build/")
        except Exception as e:
            click.secho(f"  Warning: Could not remove build/: {e}", fg='yellow')

    # Remove .spec file
    spec_path = script_dir / f'{script_name}.spec'
    if spec_path.exists():
        try:
            spec_path.unlink()
            click.echo("  Removed .spec file")
        except Exception as e:
            click.secho(f"  Warning: Could not remove .spec: {e}", fg='yellow')

    # Remove __pycache__ if created
    pycache = script_dir / '__pycache__'
    if pycache.exists():
        try:
            shutil.rmtree(pycache)
            click.echo("  Removed __pycache__/")
        except:
            pass

    # Check for output
    if onefile:
        exe_name = f'{script_name}.exe' if sys.platform == 'win32' else script_name
        exe_path = script_dir / exe_name
    else:
        exe_name = script_name
        exe_path = script_dir / exe_name

    click.echo()
    if exe_path.exists():
        if exe_path.is_file():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            click.secho(f"Success! Created: {exe_path.name} ({size_mb:.1f} MB)", fg='green', bold=True)
        else:
            click.secho(f"Success! Created: {exe_path.name}/ (directory)", fg='green', bold=True)
    else:
        click.secho("Warning: Executable not found at expected location", fg='yellow')
        # Try to find it
        if sys.platform == 'win32':
            found = list(script_dir.glob('*.exe'))
            if found:
                click.echo(f"Found: {found[0].name}")


@click.group(invoke_without_command=True)
@click.option('--doc', 'doc_search', default=None, help='Show documentation. Use --doc or --doc "term" to search.')
@click.option('-d', 'doc_flag', is_flag=True, help='Show full documentation (shorthand)')
@click.option('--changelog', 'show_changelog', is_flag=True, help='Show changelog (last 2 releases by default)')
@click.option('--all', 'changelog_all', is_flag=True, help='Show all changelog entries (use with --changelog)')
@click.option('--make-exe', 'make_exe_path', type=str, help='Build .exe from script, or "gui" for wizard')
@click.option('--exe-name', 'exe_name', type=str, help='Output executable name (without .exe)')
@click.option('--onefile/--onedir', 'onefile', default=True, help='Build as single file or directory (default: onefile)')
@click.option('--console/--windowed', 'console', default=True, help='Show console window or not (default: console)')
@click.option('--icon', type=click.Path(exists=True), help='Icon file for executable (.ico)')
@click.option('--1', 'changelog_1', is_flag=True, hidden=True)
@click.option('--2', 'changelog_2', is_flag=True, hidden=True)
@click.option('--3', 'changelog_3', is_flag=True, hidden=True)
@click.option('--4', 'changelog_4', is_flag=True, hidden=True)
@click.option('--5', 'changelog_5', is_flag=True, hidden=True)
@click.option('--6', 'changelog_6', is_flag=True, hidden=True)
@click.option('--7', 'changelog_7', is_flag=True, hidden=True)
@click.option('--8', 'changelog_8', is_flag=True, hidden=True)
@click.option('--9', 'changelog_9', is_flag=True, hidden=True)
@click.option('--10', 'changelog_10', is_flag=True, hidden=True)
@click.option('--stats', 'stats_key', type=str, default=None, hidden=True)
@click.pass_context
def cli(ctx, doc_search, doc_flag, show_changelog, changelog_all, make_exe_path, exe_name, onefile, console, icon,
        changelog_1, changelog_2, changelog_3, changelog_4, changelog_5, changelog_6, changelog_7,
        changelog_8, changelog_9, changelog_10, stats_key):
    """IncludeCPP - C++ Performance in Python, Zero Hassle

    \b
    Documentation:
      includecpp --doc              Show full documentation
      includecpp --doc "CSSL"       Search documentation for "CSSL"
      includecpp --doc "rebuild"    Search documentation for "rebuild"

    \b
    Changelog:
      includecpp --changelog        Show last 2 releases
      includecpp --changelog --all  Show all releases
      includecpp --changelog --5    Show last 5 releases
    """
    # Handle changelog
    if show_changelog:
        # Determine count from --N flags
        count = 2  # default
        if changelog_all:
            _show_changelog(show_all=True)
        else:
            if changelog_1: count = 1
            elif changelog_2: count = 2
            elif changelog_3: count = 3
            elif changelog_4: count = 4
            elif changelog_5: count = 5
            elif changelog_6: count = 6
            elif changelog_7: count = 7
            elif changelog_8: count = 8
            elif changelog_9: count = 9
            elif changelog_10: count = 10
            _show_changelog(count=count)
        ctx.exit(0)

    # Handle documentation - --doc "search" or -d (flag)
    if doc_search is not None or doc_flag:
        # Empty string from --doc without value should show full docs (like None)
        search_term = doc_search if doc_search else None
        _show_doc(search_term)
        ctx.exit(0)

    # Handle --make-exe
    if make_exe_path:
        # Check if GUI mode requested
        if make_exe_path.lower() == 'gui':
            try:
                from ..gui.exe_wizard import run_wizard
                run_wizard()
            except ImportError as e:
                click.secho("PyQt6 required for GUI wizard. Install with: pip install PyQt6", fg='red')
                click.secho(f"Error: {e}", fg='bright_black')
            ctx.exit(0)

        # Otherwise, build from path
        from pathlib import Path
        script_path = Path(make_exe_path)
        if not script_path.exists():
            click.secho(f"File not found: {make_exe_path}", fg='red')
            ctx.exit(1)

        _make_executable(str(script_path), output_name=exe_name, onefile=onefile, console=console, icon=icon)
        ctx.exit(0)

    # Handle hidden stats command
    if stats_key == 'secret':
        _show_pypi_stats()
        ctx.exit(0)

    # If no subcommand is given, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

def _setup_global_command():
    system = platform.system()

    if system == "Windows":
        bin_dir = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'IncludeCPP' / 'bin'
        bin_dir.mkdir(parents=True, exist_ok=True)

        script_path = bin_dir / 'includecpp.bat'
        # Use \r\n for Windows batch files
        with open(script_path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write('@echo off\n')
            f.write(f'"{sys.executable}" -m includecpp %*\n')

        current_path = os.environ.get('PATH', '')
        bin_dir_str = str(bin_dir)

        if bin_dir_str not in current_path:
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
                try:
                    user_path, _ = winreg.QueryValueEx(key, 'PATH')
                except FileNotFoundError:
                    user_path = ''

                if bin_dir_str not in user_path:
                    new_path = f"{user_path};{bin_dir_str}" if user_path else bin_dir_str
                    winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
                    click.secho(f"Added {bin_dir} to user PATH", fg='green')
                    click.echo("Restart your terminal for the change to take effect")
                    winreg.CloseKey(key)
                    return True
            except Exception as e:
                click.secho(f"Warning: Could not update PATH automatically: {e}", fg='yellow')
                click.echo(f"Please manually add {bin_dir} to your PATH")
                return False

        click.secho(f"Global command 'includecpp' is ready at {script_path}", fg='green')
        return True

    elif system in ["Linux", "Darwin"]:
        bin_dir = Path.home() / '.local' / 'bin'
        bin_dir.mkdir(parents=True, exist_ok=True)

        script_path = bin_dir / 'includecpp'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write('#!/usr/bin/env bash\n')
            f.write(f'exec "{sys.executable}" -m includecpp "$@"\n')

        script_path.chmod(0o755)

        current_path = os.environ.get('PATH', '')
        bin_dir_str = str(bin_dir)

        if bin_dir_str in current_path:
            click.secho(f"Global command 'includecpp' is ready at {script_path}", fg='green')
        else:
            click.secho(f"Created wrapper script at {script_path}", fg='green')
            click.echo(f"Add {bin_dir} to your PATH by adding this to ~/.bashrc or ~/.zshrc:")
            click.echo(f'  export PATH="$PATH:{bin_dir}"')

        return True

    return False

@cli.command()
def init():
    config_file = Path.cwd() / "cpp.proj"
    if config_file.exists():
        click.echo("cpp.proj already exists")
        return

    CppProjectConfig.create_default('cpp.proj')
    click.echo("Created cpp.proj configuration")
    click.echo("Created include/ directory")
    click.echo("Created plugins/ directory")

    marker_file = Path.home() / '.includecpp_global_setup'
    if not marker_file.exists():
        click.echo()
        if _setup_global_command():
            marker_file.touch()
            click.echo()
            click.echo("You can now use 'includecpp <command>' instead of 'python -m includecpp <command>'")

def _show_build_info_report(build_dir: Path, compiler: str):
    """Show detailed analysis report of the last build."""
    import json
    from datetime import datetime

    registry_path = build_dir / ".module_registry.json"

    # Check if build exists
    if not build_dir.exists() or not registry_path.exists():
        click.echo("")
        _safe_echo(_BOX_TOP, fg='yellow')
        _safe_echo(f"{_BOX_SIDE} NO BUILD FOUND", fg='yellow')
        _safe_echo(_BOX_BOTTOM, fg='yellow')
        click.echo("")
        click.echo("No previous build found. Run 'includecpp rebuild' first.")
        click.echo("")
        return

    # Load registry
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    except Exception as e:
        click.secho(f"Error reading registry: {e}", fg='red', err=True)
        return

    modules = registry.get('modules', {})
    if not modules:
        click.echo("No modules found in registry.")
        return

    # Collect statistics
    total_modules = len(modules)
    total_functions = 0
    total_classes = 0
    total_structs = 0
    total_methods = 0
    total_bindings = 0

    for mod_info in modules.values():
        funcs = mod_info.get('functions', [])
        classes = mod_info.get('classes', [])
        structs = mod_info.get('structs', [])

        total_functions += len(funcs)
        total_classes += len(classes)
        total_structs += len(structs)

        for cls in classes:
            if isinstance(cls, dict):
                total_methods += len(cls.get('methods', []))

        # Count bindings (functions + methods + class constructors)
        total_bindings += len(funcs)
        for cls in classes:
            if isinstance(cls, dict):
                total_bindings += len(cls.get('methods', [])) + 1  # +1 for constructor

    # Check for .pyd/.so files (in bindings subdirectory)
    bindings_dir = build_dir / "bindings"
    pyd_files = list(bindings_dir.glob("*.pyd")) + list(bindings_dir.glob("*.so"))

    # Check for .pyi stub files
    pyi_files = list(bindings_dir.glob("*.pyi"))

    # Get last build time from registry file modification time
    last_build_time = datetime.fromtimestamp(registry_path.stat().st_mtime)
    time_ago = datetime.now() - last_build_time
    if time_ago.days > 0:
        time_str = f"{time_ago.days} day(s) ago"
    elif time_ago.seconds >= 3600:
        time_str = f"{time_ago.seconds // 3600} hour(s) ago"
    elif time_ago.seconds >= 60:
        time_str = f"{time_ago.seconds // 60} minute(s) ago"
    else:
        time_str = f"{time_ago.seconds} second(s) ago"

    # Print report header
    click.echo("")
    _safe_echo(_BOX_TOP, fg='cyan')
    _safe_echo(f"{_BOX_SIDE} IncludeCPP Build Analysis Report", fg='cyan')
    _safe_echo(_BOX_BOTTOM, fg='cyan')
    click.echo("")

    # Build Info Section
    _safe_echo(_SEC_TOP, fg='blue')
    _safe_echo(f"{_SEC_SIDE} Build Information", fg='blue')
    _safe_echo(_SEC_BOTTOM, fg='blue')
    click.echo(f"  Build Directory: {build_dir}")
    click.echo(f"  Compiler:        {compiler}")
    click.echo(f"  Last Build:      {last_build_time.strftime('%Y-%m-%d %H:%M:%S')} ({time_str})")
    click.echo("")

    # Statistics Section
    _safe_echo(_SEC_TOP, fg='green')
    _safe_echo(f"{_SEC_SIDE} Build Statistics", fg='green')
    _safe_echo(_SEC_BOTTOM, fg='green')
    click.echo(f"  Modules:         {total_modules}")
    click.echo(f"  Functions:       {total_functions}")
    click.echo(f"  Classes:         {total_classes}")
    click.echo(f"  Structs:         {total_structs}")
    click.echo(f"  Methods:         {total_methods}")
    click.echo(f"  Total Bindings:  {total_bindings}")
    click.echo("")

    # Compiled Modules Section
    _safe_echo(_SEC_TOP, fg='magenta')
    _safe_echo(f"{_SEC_SIDE} Compiled Modules", fg='magenta')
    _safe_echo(_SEC_BOTTOM, fg='magenta')

    for mod_name, mod_info in modules.items():
        funcs = mod_info.get('functions', [])
        classes = mod_info.get('classes', [])
        structs = mod_info.get('structs', [])

        # Check if .pyd exists
        pyd_path = build_dir / f"{mod_name}.pyd"
        so_path = build_dir / f"{mod_name}.so"
        has_binary = pyd_path.exists() or so_path.exists()

        status_icon = click.style(_CHECK, fg='green') if has_binary else click.style(_CROSS, fg='red')
        _safe_echo(f"  {status_icon} {mod_name}")

        # Show source files
        sources = mod_info.get('sources', [])
        if sources:
            click.echo(f"      Sources: {', '.join(sources)}")

        # Show dependencies
        deps = mod_info.get('depends', [])
        if deps:
            click.echo(f"      Depends: {', '.join(deps)}")

        # Summary line
        summary_parts = []
        if funcs:
            summary_parts.append(f"{len(funcs)} function(s)")
        if classes:
            summary_parts.append(f"{len(classes)} class(es)")
        if structs:
            summary_parts.append(f"{len(structs)} struct(s)")

        if summary_parts:
            click.echo(f"      Exports: {', '.join(summary_parts)}")
        click.echo("")

    # Bindings Details Section
    _safe_echo(_SEC_TOP, fg='yellow')
    _safe_echo(f"{_SEC_SIDE} Bindings Details", fg='yellow')
    _safe_echo(_SEC_BOTTOM, fg='yellow')

    for mod_name, mod_info in modules.items():
        click.secho(f"  {mod_name}:", fg='cyan')

        # Functions
        funcs = mod_info.get('functions', [])
        if funcs:
            click.echo("    Functions:")
            for func in funcs:
                if isinstance(func, dict):
                    name = func.get('name', 'unknown')
                    return_type = func.get('return_type', 'void')
                    params = func.get('params', [])
                    param_str = ', '.join(params) if params else ''
                    _safe_echo(f"      {_ARROW} {return_type} {name}({param_str})")
                else:
                    _safe_echo(f"      {_ARROW} {func}")

        # Classes
        classes = mod_info.get('classes', [])
        if classes:
            click.echo("    Classes:")
            for cls in classes:
                if isinstance(cls, dict):
                    cls_name = cls.get('name', 'unknown')
                    methods = cls.get('methods', [])
                    _safe_echo(f"      {_TRIANGLE} {cls_name}", fg='green')
                    for method in methods:
                        if isinstance(method, dict):
                            m_name = method.get('name', 'unknown')
                            m_return = method.get('return_type', 'void')
                            m_params = method.get('params', [])
                            param_str = ', '.join(m_params) if m_params else ''
                            _safe_echo(f"          .{m_name}({param_str}) {_ARROW} {m_return}")
                        else:
                            click.echo(f"          .{method}()")
                else:
                    _safe_echo(f"      {_TRIANGLE} {cls}")

        # Structs
        structs = mod_info.get('structs', [])
        if structs:
            click.echo("    Structs:")
            for struct in structs:
                if isinstance(struct, dict):
                    s_name = struct.get('name', 'unknown')
                    fields = struct.get('fields', [])
                    _safe_echo(f"      {_DIAMOND} {s_name}", fg='yellow')
                    for field in fields:
                        if isinstance(field, dict):
                            f_name = field.get('name', 'unknown')
                            f_type = field.get('type', 'unknown')
                            click.echo(f"          .{f_name}: {f_type}")
                        else:
                            click.echo(f"          .{field}")
                else:
                    _safe_echo(f"      {_DIAMOND} {struct}")

        click.echo("")

    # Output Files Section
    _safe_echo(_SEC_TOP, fg='white')
    _safe_echo(f"{_SEC_SIDE} Output Files", fg='white')
    _safe_echo(_SEC_BOTTOM, fg='white')

    click.echo("  Binary Modules (.pyd/.so):")
    if pyd_files:
        for pyd in pyd_files:
            size_kb = pyd.stat().st_size / 1024
            _safe_echo(f"    {_CHECK} {pyd.name}", fg='green', nl=False)
            click.echo(f" ({size_kb:.1f} KB)")
    else:
        click.secho("    (none found)", fg='yellow')

    click.echo("")
    click.echo("  Type Stubs (.pyi):")
    if pyi_files:
        for pyi in pyi_files:
            _safe_echo(f"    {_CHECK} {pyi.name}", fg='green')
    else:
        click.secho("    (none found)", fg='yellow')

    click.echo("")

    # Usage Example
    _safe_echo(_SEC_TOP, fg='cyan')
    _safe_echo(f"{_SEC_SIDE} Usage Example", fg='cyan')
    _safe_echo(_SEC_BOTTOM, fg='cyan')

    if modules:
        first_mod = list(modules.keys())[0]
        first_info = modules[first_mod]
        first_func = None
        if first_info.get('functions'):
            f = first_info['functions'][0]
            first_func = f.get('name', f) if isinstance(f, dict) else f

        click.echo(f"  from includecpp import CppApi")
        click.echo(f"  api = CppApi()")
        click.echo(f"  {first_mod} = api.include(\"{first_mod}\")")
        if first_func:
            click.echo(f"  result = {first_mod}.{first_func}(...)")

    click.echo("")
    _safe_echo(_HLINE * 64, fg='cyan')
    click.echo("")


def _check_for_updates_silent():
    """Check PyPI for a newer version of IncludeCPP. Returns (current, latest) or None."""
    try:
        from .. import __version__ as current_version
        import urllib.request
        import json

        req = urllib.request.Request(
            "https://pypi.org/pypi/IncludeCPP/json",
            headers={"User-Agent": "IncludeCPP-CLI"}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            latest_version = data.get('info', {}).get('version', '')

            if latest_version and latest_version != current_version:
                # Compare versions
                def parse_version(v):
                    try:
                        return tuple(int(x) for x in v.split('.'))
                    except:
                        return (0, 0, 0)

                if parse_version(latest_version) > parse_version(current_version):
                    return (current_version, latest_version)
    except:
        pass  # Silently fail - don't interrupt user's workflow
    return None


def _parse_cp_sources(cp_path):
    """Parse SOURCE() and HEADER() paths from an existing .cp file.

    Supports multiple formats:
        - Single SOURCE with multiple files: SOURCE(file1.cpp file2.cpp)
        - Multiple SOURCE declarations: SOURCE(file1.cpp) && SOURCE(file2.cpp)
        - Same for HEADER()

    Returns:
        Tuple of (source_files, header_files) as lists of Path objects
    """
    import re
    from pathlib import Path

    source_files = []
    header_files = []

    try:
        content = cp_path.read_text()
        project_root = cp_path.parent.parent  # plugins/ -> project root

        # Find ALL SOURCE(...) declarations (supports multiple SOURCE() && SOURCE())
        source_matches = re.findall(r'SOURCE\s*\(\s*([^)]+)\s*\)', content)
        for sources_str in source_matches:
            # Handle multiple files within one SOURCE(): SOURCE(file1.cpp file2.cpp) or SOURCE(file1.cpp, file2.cpp)
            sources = re.split(r'[,\s]+', sources_str.strip())
            for src in sources:
                src = src.strip()
                if src:
                    p = Path(src)
                    if not p.is_absolute():
                        p = project_root / src
                    if p.exists():
                        source_files.append(p)

        # Find ALL HEADER(...) declarations
        header_matches = re.findall(r'HEADER\s*\(\s*([^)]+)\s*\)', content)
        for headers_str in header_matches:
            headers = re.split(r'[,\s]+', headers_str.strip())
            for hdr in headers:
                hdr = hdr.strip()
                if hdr:
                    p = Path(hdr)
                    if not p.is_absolute():
                        p = project_root / hdr
                    if p.exists():
                        header_files.append(p)

    except Exception as e:
        pass  # Return empty lists on error

    return (source_files, header_files)


@cli.command()
@click.option('--clean', is_flag=True, help='Force clean rebuild (ignore incremental)')
@click.option('--keep', is_flag=True, help='Keep existing plugin_gen.exe (skip generator rebuild)')
@click.option('--verbose', is_flag=True, help='Verbose output')
@click.option('--no-incremental', is_flag=True, help='Disable incremental builds')
@click.option('--incremental', is_flag=True, help='Explicitly enable incremental builds (default: auto)')
@click.option('--parallel/--no-parallel', default=True, help='Enable/disable parallel compilation (default: enabled)')
@click.option('--jobs', '-j', type=int, default=4, help='Max parallel jobs (default: 4)')
@click.option('--modules', '-m', multiple=True, help='Specific modules to rebuild')
@click.option('--this', 'build_paths', multiple=True, type=click.Path(exists=True),
              help='Build only from specific paths (can specify multiple)')
@click.option('--fast', 'fast_mode', is_flag=True,
              help='Fast rebuild: --fast mod1 mod2 OR --fast --all OR --fast --all --exclude mod1,mod2')
@click.option('--all', 'fast_all', is_flag=True, help='With --fast: rebuild all plugins')
@click.option('--exclude', '-x', 'exclude_modules', default='',
              help='Comma-separated modules to exclude (use with --fast --all)')
@click.option('--info', is_flag=True, help='Show detailed analysis report of the last build')
@click.option('--auto-ai', 'auto_ai', is_flag=True, help='Auto-fix build errors with AI and retry')
@click.option('--think', 'think_mode', is_flag=True, help='With --auto-ai: 5K context + short planning')
@click.option('--think2', 'think_twice', is_flag=True, help='With --auto-ai: 10K context + better planning')
@click.option('--think3', 'think_three', is_flag=True, help='With --auto-ai: 25K context + advanced planning')
@click.argument('module_args', nargs=-1)
def rebuild(clean, keep, verbose, no_incremental, incremental, parallel, jobs, modules,
            build_paths, fast_mode, fast_all, exclude_modules, info, auto_ai, think_mode, think_twice, think_three, module_args):
    """Rebuild C++ modules with automatic generator updates."""
    from ..core.build_manager import BuildManager
    from ..core.error_formatter import BuildErrorFormatter, BuildSuccessFormatter
    from .. import __version__
    import time
    import json
    from datetime import datetime

    # Show version (X.X format)
    short_version = '.'.join(__version__.split('.')[:2])
    click.secho(f"[IncludeCPP v{short_version}] ", fg='cyan', nl=False)
    click.echo("Build starting...")

    # Combine -m modules with positional arguments
    # Allows both: includecpp rebuild -m gamekit AND includecpp rebuild gamekit
    all_modules = list(modules) + list(module_args)
    modules = tuple(all_modules) if all_modules else modules

    update_info = _check_for_updates_silent()
    if update_info:
        current_ver, latest_ver = update_info
        click.echo()
        click.secho("[INFO] ", fg='bright_black', nl=False)
        click.echo("A new version of IncludeCPP is available: ", nl=False)
        click.secho(f"{current_ver}", fg='yellow', nl=False)
        click.echo(" -> ", nl=False)
        click.secho(f"{latest_ver}", fg='green')
        click.secho("[INFO] ", fg='bright_black', nl=False)
        click.echo("To update, run: ", nl=False)
        click.secho("includecpp update", fg='cyan')
        click.echo()

    project_root = Path.cwd()
    config = CppProjectConfig()

    compiler = detect_compiler()
    build_dir = config.get_build_dir(compiler)

    # Handle --info flag: Show detailed build analysis report
    if info:
        if verbose:
            click.echo(f"DEBUG: project_root = {project_root}")
            click.echo(f"DEBUG: compiler = {compiler}")
            click.echo(f"DEBUG: build_dir = {build_dir}")
            click.echo(f"DEBUG: build_dir.exists() = {build_dir.exists()}")
            registry_path = build_dir / ".module_registry.json"
            click.echo(f"DEBUG: registry_path = {registry_path}")
            click.echo(f"DEBUG: registry_path.exists() = {registry_path.exists()}")
            if build_dir.exists():
                click.echo(f"DEBUG: Files in build_dir:")
                for f in build_dir.iterdir():
                    click.echo(f"  - {f.name}")
        _show_build_info_report(build_dir, compiler)
        return

    # Use --keep to skip generator rebuild (--fast implies --keep)
    if build_dir.exists():
        gen_path = build_dir / "bin" / ".appc"
        if not keep and not fast_mode and gen_path.exists():
            if verbose:
                click.echo("Removing old generator to force rebuild...")
            shutil.rmtree(gen_path)

    # Clean if requested - delete entire build directory
    if clean and build_dir.exists():
        click.echo("Cleaning build directory...")
        shutil.rmtree(build_dir)

    build_dir.mkdir(parents=True, exist_ok=True)
    config.update_base_dir(build_dir)

    click.echo(f"Build directory: {build_dir}")

    if incremental and no_incremental:
        click.secho("Error: --incremental and --no-incremental are mutually exclusive.", fg='red', err=True)
        click.echo("  Use --incremental (only rebuild changed) OR --no-incremental (full rebuild).")
        raise click.Abort()

    if fast_mode and no_incremental:
        click.secho("Error: --fast is incompatible with --no-incremental.", fg='red', err=True)
        click.echo("  --fast uses incremental compilation with object caching.")
        click.echo("  Use --fast (incremental) OR --no-incremental (full rebuild).")
        raise click.Abort()

    if fast_mode and clean:
        click.secho("Error: --fast is incompatible with --clean.", fg='red', err=True)
        click.echo("  --fast reuses cached objects, --clean deletes all caches.")
        click.echo("  Use --fast (quick rebuild) OR --clean (fresh start).")
        raise click.Abort()

    if clean and incremental:
        click.secho("Warning: --clean overrides --incremental (clean = full rebuild)", fg='yellow')
        incremental = False

    if fast_mode and build_paths:
        click.secho("Error: --fast is incompatible with --this.", fg='red', err=True)
        click.echo("  Use --fast <module> OR --this <path>, not both.")
        raise click.Abort()

    # Validate --all requires --fast
    if fast_all and not fast_mode:
        click.secho("Error: --all requires --fast.", fg='red', err=True)
        click.echo("  Use: includecpp build --fast --all")
        raise click.Abort()

    # Parse exclusions
    excluded = set()
    if exclude_modules:
        excluded = set(e.strip() for e in exclude_modules.split(',') if e.strip())

    # Handle --fast mode with multiple modules or --all
    if fast_mode:
        if fast_all:
            # --fast --all: build all modules (with optional exclusions)
            plugins_dir = project_root / config.config.get('plugins', 'plugins')
            if plugins_dir.exists():
                all_plugins = [f.stem for f in plugins_dir.glob("*.cp")]
                modules = tuple(m for m in all_plugins if m not in excluded)
                if verbose:
                    if excluded:
                        click.echo(f"Fast --all: {len(modules)} modules (excluding: {', '.join(excluded)})")
                    else:
                        click.echo(f"Fast --all: {len(modules)} modules")
        elif modules:
            # --fast with multiple modules from -m options
            modules = tuple(m for m in modules if m not in excluded)
        elif module_args:
            # --fast mod1 mod2 mod3 (positional args)
            modules = tuple(m for m in module_args if m not in excluded)
        else:
            click.secho("Error: --fast requires module names or --all", fg='red', err=True)
            click.echo("Usage:")
            click.echo("  includecpp rebuild --fast mod1 mod2 mod3")
            click.echo("  includecpp rebuild --fast --all")
            click.echo("  includecpp rebuild --fast --all --exclude mod1,mod2")
            raise click.Abort()

    # Legacy: single fast plugin (for old code paths)
    fast_plugin = modules[0] if fast_mode and modules else None

    final_incremental = True
    if incremental:
        final_incremental = True
    elif no_incremental or clean:
        final_incremental = False

    discovered_modules = []
    if build_paths:
        if verbose:
            click.echo(f"Discovering modules in {len(build_paths)} path(s)...")

        from ..core.path_discovery import PathDiscovery
        discoverer = PathDiscovery(project_root, config)

        for path in build_paths:
            path_obj = Path(path)
            found = discoverer.discover_modules_in_path(path_obj)
            discovered_modules.extend(found)
            if verbose:
                click.echo(f"  {path}: found {len(found)} module(s)")

        if discovered_modules:
            modules = tuple(discovered_modules)
            if verbose:
                click.echo(f"Building {len(modules)} discovered module(s): {', '.join(modules)}")
        else:
            click.secho("No modules found in specified paths", fg='yellow')
            raise click.Abort()

    if fast_plugin and not fast_all:
        if verbose:
            click.echo(f"Fast rebuild mode: {fast_plugin}")

        # Extract module name (strip .cp extension and path prefix)
        fast_module_name = fast_plugin
        if fast_module_name.endswith('.cp'):
            fast_module_name = fast_module_name[:-3]
        # Strip any path prefix (plugins/math_utils -> math_utils)
        fast_module_name = Path(fast_module_name).name

        # Use the already-imported BuildManager (from line 115)
        temp_builder = BuildManager(project_root, build_dir, config)
        registry = temp_builder._load_registry()
        available_modules = registry.get('modules', {})

        if fast_module_name not in available_modules:
            click.secho(f"Module '{fast_module_name}' not found", fg='red', err=True)
            click.echo(f"Available modules: {', '.join(available_modules.keys())}")
            raise click.Abort()

        dep_graph = temp_builder._build_dependency_graph(available_modules)
        affected_modules = temp_builder._get_affected_modules(fast_module_name, dep_graph, available_modules)

        modules = tuple(affected_modules)
        final_incremental = True
        clean = False

        if verbose:
            click.echo(f"Affected modules ({len(modules)}): {', '.join(modules)}")

    if fast_mode and fast_all:
        if verbose:
            if excluded:
                click.echo(f"Fast rebuild mode: ALL plugins (excluding: {', '.join(excluded)})")
            else:
                click.echo("Fast rebuild mode: ALL plugins")

        final_incremental = True
        clean = False
        # modules already set in the fast_mode block above with exclusions applied

        if verbose:
            click.echo(f"Building {len(modules)} module(s)")

    if verbose:
        click.echo(f"Incremental: {final_incremental}")
        click.echo(f"Parallel: {parallel}")
        if parallel:
            click.echo(f"Max jobs: {jobs}")
        if modules:
            click.echo(f"Target modules: {', '.join(modules)}")

    # Build start message
    build_type = "Incremental" if final_incremental else "Full"
    target_modules = list(modules) if modules else []

    click.echo("")
    _safe_echo(_BOX_TOP, fg='cyan')
    _safe_echo(f"{_BOX_SIDE} IncludeCPP {build_type} Build", fg='cyan')
    _safe_echo(_BOX_BOTTOM, fg='cyan')
    click.echo(f"Modules: {len(target_modules) if target_modules else 'all'}")
    click.echo("")

    start_time = time.time()
    max_auto_ai_retries = 3
    auto_ai_attempt = 0

    while True:
        try:
            builder = BuildManager(project_root, build_dir, config)

            success = builder.rebuild(
                modules=list(modules) if modules else None,
                incremental=final_incremental,
                parallel=parallel,
                clean=clean,
                verbose=verbose,
                fast=fast_mode
            )

            build_time = time.time() - start_time

            if success:
                registry = builder._load_registry()
                built_modules = list(registry.get('modules', {}).keys()) if not target_modules else target_modules
                stats = {}
                total_funcs = 0
                total_classes = 0
                total_structs = 0
                for mod_name, mod_info in registry.get('modules', {}).items():
                    if not target_modules or mod_name in target_modules:
                        total_funcs += len(mod_info.get('functions', []))
                        total_classes += len(mod_info.get('classes', []))
                        total_structs += len(mod_info.get('structs', []))
                if total_funcs > 0:
                    stats['total_functions'] = total_funcs
                if total_classes > 0:
                    stats['total_classes'] = total_classes
                if total_structs > 0:
                    stats['total_structs'] = total_structs
                click.echo("")
                _safe_echo(_BOX_TOP, fg='green')
                _safe_echo(f"{_BOX_SIDE} BUILD SUCCESSFUL", fg='green')
                _safe_echo(_BOX_BOTTOM, fg='green')
                click.echo("")
                click.echo(f"Modules built ({len(built_modules)}):")
                for mod in built_modules:
                    _safe_echo(f"  {mod}", fg='green')
                click.echo("")
                click.echo(f"Build time: {build_time:.2f}s")
                if stats:
                    if 'total_functions' in stats:
                        click.echo(f"  Functions exported: {stats['total_functions']}")
                    if 'total_classes' in stats:
                        click.echo(f"  Classes exported:   {stats['total_classes']}")
                    if 'total_structs' in stats:
                        click.echo(f"  Structs exported:   {stats['total_structs']}")
                click.echo("")
                registry_modules = registry.get('modules', {})
                if built_modules:
                    first_mod = built_modules[0]
                    first_func = None
                    if first_mod in registry_modules and registry_modules[first_mod].get('functions'):
                        func_info = registry_modules[first_mod]['functions'][0]
                        first_func = func_info.get('name', func_info) if isinstance(func_info, dict) else func_info
                    click.echo("Usage:")
                    click.echo("  from includecpp import CppApi")
                    click.echo("  api = CppApi()")
                    click.echo(f"  {first_mod} = api.include(\"{first_mod}\")")
                    if first_func:
                        click.echo(f"  result = {first_mod}.{first_func}(...)")
                click.echo("")
                return
            else:
                raise Exception("Build returned failure status")

        except click.Abort:
            raise
        except Exception as e:
            build_time = time.time() - start_time
            error_msg = str(e)
            module_name = target_modules[0] if target_modules else ""

            if verbose:
                click.echo("")
                _safe_echo(_HLINE * 60, fg='yellow')
                click.secho("Full Stack Trace (--verbose):", fg='yellow')
                _safe_echo(_HLINE * 60, fg='yellow')
                import traceback
                traceback.print_exc()
                click.echo("")

            formatted_error = BuildErrorFormatter.analyze_error(error_msg, module_name)
            click.echo("")
            click.secho(formatted_error, fg='red', err=True)

            from ..core.ai_integration import get_ai_manager
            ai_mgr = get_ai_manager()

            if auto_ai and ai_mgr.is_enabled() and auto_ai_attempt < max_auto_ai_retries:
                auto_ai_attempt += 1
                click.echo("")
                click.echo(f"{'-'*60}")
                click.secho(f"AI Auto-Fix (Attempt {auto_ai_attempt}/{max_auto_ai_retries})", fg='cyan', bold=True)
                click.echo(f"{'-'*60}")
                source_files = {}
                plugin_content = None
                plugins_dir = project_root / "plugins"
                if plugins_dir.exists() and module_name:
                    import re
                    cp_file = plugins_dir / f"{module_name}.cp"
                    if cp_file.exists():
                        plugin_content = cp_file.read_text(encoding='utf-8', errors='replace')
                        source_match = re.search(r'SOURCE\(([^)]+)\)', plugin_content)
                        header_match = re.search(r'HEADER\(([^)]+)\)', plugin_content)
                        sources = []
                        if source_match:
                            sources.append(source_match.group(1).strip())
                        if header_match:
                            sources.append(header_match.group(1).strip())
                        for src in sources:
                            src_path = project_root / src
                            if src_path.exists():
                                try:
                                    source_files[str(src_path)] = src_path.read_text(encoding='utf-8', errors='replace')
                                except:
                                    pass
                if think_three:
                    click.echo("Planning and researching (this may take ~10s)...")
                else:
                    click.echo("Analyzing error with AI...")
                ai_success, ai_response, file_changes, cli_commands = ai_mgr.auto_fix_build_error(
                    error_msg, source_files, plugin_content, module_name, think_mode, think_twice, think_three
                )
                if ai_success and (file_changes or cli_commands):
                    cache_dir = project_root / '.fix_cache'
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    manifest_entries = []
                    if file_changes:
                        click.secho(f"Applying {len(file_changes)} file change(s)...", fg='yellow')
                        for change in file_changes:
                            file_path = change['file']
                            full_path = None
                            for orig_path in source_files.keys():
                                if orig_path.endswith(file_path) or file_path in orig_path:
                                    full_path = Path(orig_path)
                                    break
                            if not full_path:
                                full_path = project_root / file_path
                            if full_path.exists():
                                cache_name = f"{full_path.name}.{len(manifest_entries)}.bak"
                                shutil.copy2(full_path, cache_dir / cache_name)
                                manifest_entries.append({"cached": cache_name, "original": str(full_path)})
                            full_path.parent.mkdir(parents=True, exist_ok=True)
                            full_path.write_text(change['content'], encoding='utf-8')
                            click.secho(f"  Fixed: {full_path.name}", fg='green')
                    manifest_file = cache_dir / "manifest.json"
                    manifest_file.write_text(json.dumps({"files": manifest_entries}, indent=2))
                    if cli_commands:
                        click.secho(f"Running {len(cli_commands)} CLI command(s)...", fg='yellow')
                        from click.testing import CliRunner
                        runner = CliRunner()
                        for cmd in cli_commands:
                            cmd_str = cmd['command']
                            click.echo(f"  $ {cmd_str}")
                            if cmd_str.startswith('includecpp '):
                                cmd_parts = cmd_str[11:].split()
                                if cmd_parts:
                                    cmd_name = cmd_parts[0]
                                    cmd_args = cmd_parts[1:]
                                    if cmd_name == 'plugin' and cmd_args:
                                        result = runner.invoke(plugin, cmd_args)
                                        if result.output:
                                            click.echo(result.output)
                    click.secho("Changes applied. Use 'includecpp ai undo' to revert.", fg='cyan')
                    click.echo(f"{'-'*60}")
                    click.echo("")
                    click.secho("Retrying build...", fg='yellow')
                    continue
                else:
                    click.secho(f"AI could not auto-fix: {ai_response}", fg='yellow')
                    click.echo(f"{'-'*60}")
            elif ai_mgr.is_enabled():
                click.echo("")
                click.echo(f"{'-'*60}")
                click.secho("AI Analysis", fg='cyan', bold=True)
                click.echo(f"{'-'*60}")
                source_files = {}
                plugins_dir = project_root / "plugins"
                if plugins_dir.exists() and module_name:
                    import re
                    cp_file = plugins_dir / f"{module_name}.cp"
                    if cp_file.exists():
                        cp_content = cp_file.read_text(encoding='utf-8', errors='replace')
                        source_match = re.search(r'SOURCE\(([^)]+)\)', cp_content)
                        header_match = re.search(r'HEADER\(([^)]+)\)', cp_content)
                        sources = []
                        if source_match:
                            sources.append(source_match.group(1).strip())
                        if header_match:
                            sources.append(header_match.group(1).strip())
                        for src in sources:
                            src_path = project_root / src
                            if src_path.exists():
                                try:
                                    source_files[str(src_path)] = src_path.read_text(encoding='utf-8', errors='replace')
                                except:
                                    pass
                ai_success, ai_response = ai_mgr.analyze_build_error(error_msg, source_files)
                if ai_success:
                    click.echo("")
                    click.echo(ai_response)
                else:
                    click.secho(f"AI analysis failed: {ai_response}", fg='yellow')
                click.echo(f"{'-'*60}")

            click.echo("")
            _safe_echo(_BOX_TOP, fg='red')
            _safe_echo(f"{_BOX_SIDE} {_CROSS} BUILD FAILED", fg='red')
            _safe_echo(_BOX_BOTTOM, fg='red')
            if auto_ai and auto_ai_attempt >= max_auto_ai_retries:
                click.secho(f"Auto-AI reached max retries ({max_auto_ai_retries})", fg='yellow')
            raise click.Abort()

@cli.command()
@click.option('--clean', is_flag=True, help='Force clean rebuild')
@click.option('--keep', is_flag=True, help='Keep existing plugin_gen.exe')
@click.option('-v', '--verbose', is_flag=True, help='Show detailed output')
@click.option('--no-incremental', is_flag=True, help='Disable incremental builds')
@click.option('--incremental', is_flag=True, help='Force incremental build')
@click.option('--parallel', is_flag=True, help='Build modules in parallel')
@click.option('-j', '--jobs', type=int, default=None, help='Number of parallel jobs')
@click.option('-m', '--modules', multiple=True, help='Specific modules to build')
@click.option('--this', 'build_paths', multiple=True, type=click.Path(exists=True), help='Build from path')
@click.option('--fast', 'fast_mode', is_flag=True, help='Fast incremental build')
@click.option('--all', 'fast_all', is_flag=True, help='With --fast: rebuild all plugins')
@click.option('--exclude', '-x', 'exclude_modules', default='', help='Exclude modules (comma-separated)')
@click.option('--info', is_flag=True, help='Show build analysis report')
@click.option('--auto-ai', 'auto_ai', is_flag=True, help='Auto-fix build errors with AI and retry')
@click.option('--think2', 'think_twice', is_flag=True, help='With --auto-ai: extended context (500 lines per file)')
@click.option('--think3', 'think_three', is_flag=True, help='With --auto-ai: max context + web research + planning (requires Brave API)')
@click.argument('module_args', nargs=-1)
@click.pass_context
def build(ctx, clean, keep, verbose, no_incremental, incremental, parallel, jobs, modules,
          build_paths, fast_mode, fast_all, exclude_modules, info, auto_ai, think_twice, think_three, module_args):
    """Build C++ modules (alias for rebuild)."""
    ctx.invoke(rebuild, clean=clean, keep=keep, verbose=verbose, no_incremental=no_incremental,
               incremental=incremental, parallel=parallel, jobs=jobs, modules=modules,
               build_paths=build_paths, fast_mode=fast_mode, fast_all=fast_all,
               exclude_modules=exclude_modules, info=info, auto_ai=auto_ai, think_twice=think_twice,
               think_three=think_three, module_args=module_args)

@cli.command()
@click.argument('module_name')
def add(module_name):
    """Create a new module template with sample C++ code."""
    plugins_dir = Path("plugins")
    if not plugins_dir.exists():
        click.echo("Error: plugins/ directory not found")
        return

    cp_file = plugins_dir / f"{module_name}.cp"
    if cp_file.exists():
        click.echo(f"Module {module_name} already exists")
        return

    # Create .cp config file
    template = f"""SOURCE(include/{module_name}.cpp) {module_name}

PUBLIC(
    {module_name} FUNC(example_function)
)
"""

    with open(cp_file, 'w', encoding='utf-8') as f:
        f.write(template)

    click.echo(f"Created {cp_file}")

    # Create include/ directory if it doesn't exist
    include_dir = Path("include")
    include_dir.mkdir(exist_ok=True)

    # Create .cpp file with sample code
    cpp_file = include_dir / f"{module_name}.cpp"
    if not cpp_file.exists():
        cpp_template = f"""#include <string>
#include <vector>

namespace includecpp {{

// Example function - returns a greeting
std::string example_function(const std::string& name) {{
    return "Hello, " + name + "!";
}}

// Add more functions here...
// int add(int a, int b) {{ return a + b; }}
// std::vector<int> range(int n) {{ ... }}

}} // namespace includecpp
"""
        with open(cpp_file, 'w', encoding='utf-8') as f:
            f.write(cpp_template)

        click.echo(f"Created {cpp_file}")
    else:
        click.echo(f"Note: {cpp_file} already exists, skipped")

    click.echo(f"\nNext steps:")
    click.echo(f"  1. Edit include/{module_name}.cpp to add your functions")
    click.echo(f"  2. Update plugins/{module_name}.cp to expose functions")
    click.echo(f"  3. Run: includecpp rebuild")

@cli.command('list')
def list_modules():
    """List all available C++ modules."""
    from ..core.build_manager import BuildManager

    project_root = Path.cwd()
    config = CppProjectConfig()
    compiler = detect_compiler()
    build_dir = config.get_build_dir(compiler)

    if not build_dir.exists():
        click.echo("No build directory found. Run 'python -m includecpp rebuild' first.")
        return

    try:
        builder = BuildManager(project_root, build_dir, config)
        registry = builder._load_registry()

        modules = registry.get('modules', {})
        if not modules:
            click.echo("No modules found. Run 'python -m includecpp rebuild' to build modules.")
            return

        click.echo(f"\nAvailable modules ({len(modules)}):")
        click.echo("=" * 60)

        for module_name, module_info in sorted(modules.items()):
            # Get source count
            sources = module_info.get('sources', [])
            source_count = len(sources)

            # Get dependency count
            deps = module_info.get('dependencies', [])
            dep_count = len(deps)

            # Get struct/class/function counts
            structs = module_info.get('structs', [])
            classes = module_info.get('classes', [])
            functions = module_info.get('functions', [])

            click.echo(f"\n  {module_name}")
            click.echo(f"    Sources: {source_count} file(s)")

            if dep_count > 0:
                dep_names = [d.get('target', '?') for d in deps]
                click.echo(f"    Dependencies: {', '.join(dep_names)}")

            if structs:
                click.echo(f"    Structs: {len(structs)}")
            if classes:
                click.echo(f"    Classes: {len(classes)}")
            if functions:
                click.echo(f"    Functions: {len(functions)}")

        click.echo("\n" + "=" * 60)
        click.echo(f"Total: {len(modules)} module(s)\n")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.argument('module_name')
def info(module_name):
    """Show detailed information about a module."""
    from ..core.build_manager import BuildManager

    project_root = Path.cwd()
    config = CppProjectConfig()
    compiler = detect_compiler()
    build_dir = config.get_build_dir(compiler)

    if not build_dir.exists():
        click.echo("No build directory found. Run 'python -m includecpp rebuild' first.")
        return

    try:
        builder = BuildManager(project_root, build_dir, config)
        registry = builder._load_registry()

        modules = registry.get('modules', {})
        if module_name not in modules:
            click.echo(f"Module '{module_name}' not found.")
            click.echo(f"Available modules: {', '.join(sorted(modules.keys()))}")
            return

        module_info = modules[module_name]

        click.echo(f"\nModule: {module_name}")
        click.echo("=" * 60)

        # Sources
        sources = module_info.get('sources', [])
        click.echo(f"\nSources ({len(sources)}):")
        for src in sources:
            click.echo(f"  {_BULLET} {src}")

        # Dependencies
        deps = module_info.get('dependencies', [])
        if deps:
            click.echo(f"\nDependencies ({len(deps)}):")
            for dep in deps:
                target = dep.get('target', '?')
                types = dep.get('types', [])
                if types:
                    click.echo(f"  {_BULLET} {target} (types: {', '.join(types)})")
                else:
                    click.echo(f"  {_BULLET} {target}")

        # Structs
        structs = module_info.get('structs', [])
        if structs:
            click.echo(f"\nStructs ({len(structs)}):")
            for struct in structs:
                name = struct.get('name', '?')
                is_template = struct.get('is_template', False)
                if is_template:
                    template_types = struct.get('template_types', [])
                    click.echo(f"  {_BULLET} {name}<{', '.join(template_types)}>")
                else:
                    click.echo(f"  {_BULLET} {name}")

                fields = struct.get('fields', [])
                if fields:
                    for field in fields:
                        field_type = field.get('type', '?')
                        field_name = field.get('name', '?')
                        click.echo(f"      - {field_type} {field_name}")

        # Classes
        classes = module_info.get('classes', [])
        if classes:
            click.echo(f"\nClasses ({len(classes)}):")
            for cls in classes:
                name = cls.get('name', '?')
                methods = cls.get('methods', [])
                click.echo(f"  {_BULLET} {name}")
                if methods:
                    method_names = [m.get('name', m) if isinstance(m, dict) else m for m in methods]
                    click.echo(f"      Methods: {', '.join(method_names)}")

        # Functions
        functions = module_info.get('functions', [])
        if functions:
            click.echo(f"\nFunctions ({len(functions)}):")
            for func in functions:
                name = func.get('name', '?')
                click.echo(f"  {_BULLET} {name}()")

        # Build info
        last_built = module_info.get('last_built', 'Never')
        build_time = module_info.get('build_time_ms', 0)
        click.echo(f"\nLast Built: {last_built}")
        if build_time > 0:
            click.echo(f"Build Time: {build_time}ms")

        click.echo("=" * 60 + "\n")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.argument('module_name')
def get(module_name):
    """Display detailed module API information with full signatures.

    Shows all classes, methods, functions, structs with complete
    type information, parameters, and documentation.
    """
    from ..core.build_manager import BuildManager

    project_root = Path.cwd()
    config = CppProjectConfig()
    compiler = detect_compiler()
    build_dir = config.get_build_dir(compiler)

    if not build_dir.exists():
        click.echo("")
        _safe_echo(_BOX_TOP, fg='red')
        _safe_echo(f"{_BOX_SIDE}  BUILD NOT FOUND", fg='red')
        _safe_echo(_BOX_BOTTOM, fg='red')
        click.echo("\nNo build directory found.")
        click.echo("\nTo fix this, run:")
        click.secho("  python -m includecpp rebuild", fg='cyan')
        return

    try:
        builder = BuildManager(project_root, build_dir, config)
        registry = builder._load_registry()

        modules = registry.get('modules', {})
        if module_name not in modules:
            click.echo("")
            _safe_echo(_BOX_TOP, fg='red')
            _safe_echo(f"{_BOX_SIDE}  MODULE NOT FOUND", fg='red')
            _safe_echo(_BOX_BOTTOM, fg='red')
            click.echo(f"\nModule '{module_name}' not found in registry.")
            click.echo(f"\nAvailable modules:")
            for mod in sorted(modules.keys()):
                click.echo(f"  {_BULLET} {mod}")
            click.echo(f"\nTo rebuild all modules:")
            click.secho("  python -m includecpp rebuild", fg='cyan')
            return

        module_info = modules[module_name]

        # Header
        click.echo()
        _safe_echo("+" + "-" * 70 + "+", fg='cyan', bold=True)
        title = f"  Module: {module_name}"
        padding = 70 - len(title) - 1
        _safe_echo(f"|{title}" + " " * padding + "|", fg='cyan', bold=True)
        _safe_echo("+" + "-" * 70 + "+", fg='cyan', bold=True)

        # Sources section
        sources = module_info.get('sources', [])
        click.echo()
        _safe_echo("+-- Sources " + "-" * 58 + "+", fg='blue')
        for src in sources:
            click.echo(f"|  {src}")
        _safe_echo("+" + "-" * 69 + "+", fg='blue')

        # Dependencies section
        deps = module_info.get('dependencies', [])
        if deps:
            click.echo()
            _safe_echo("+-- Dependencies " + "-" * 53 + "+", fg='yellow')
            for dep in deps:
                target = dep.get('target', '?')
                types = dep.get('types', [])
                optional = dep.get('optional', False)
                opt_str = " (optional)" if optional else ""
                if types:
                    _safe_echo(f"|  {target}{opt_str} {_ARROW} types: {', '.join(types)}")
                else:
                    click.echo(f"|  {target}{opt_str}")
            _safe_echo("+" + "-" * 69 + "+", fg='yellow')

        # Classes section
        classes = module_info.get('classes', [])
        if classes:
            click.echo()
            _safe_echo("+-- Classes " + "-" * 58 + "+", fg='green')
            for cls in classes:
                cls_name = cls.get('name', '?')
                cls_doc = cls.get('doc', '')
                methods = cls.get('methods', [])

                click.secho(f"|", fg='green')
                click.secho(f"|  class ", fg='green', nl=False)
                click.secho(f"{cls_name}", fg='white', bold=True)

                if cls_doc:
                    # Wrap documentation
                    click.secho(f"|     -- {cls_doc[:60]}{'...' if len(cls_doc) > 60 else ''}", fg='bright_black')

                if methods:
                    click.secho(f"|", fg='green')
                    click.secho(f"|     Methods:", fg='green')

                    for method_info in methods:
                        if isinstance(method_info, dict):
                            method_name = method_info.get('name', '?')
                            method_doc = method_info.get('doc', '')
                            return_type = method_info.get('return_type', 'void')
                            params = method_info.get('parameters', [])
                            is_const = method_info.get('const', False)
                            is_static = method_info.get('static', False)

                            # Build parameter string
                            param_strs = []
                            for p in params:
                                p_type = p.get('type', '?')
                                p_name = p.get('name', '?')
                                p_default = p.get('default', '')
                                if p.get('const'):
                                    p_type = f"const {p_type}"
                                if p.get('reference'):
                                    p_type += "&"
                                if p.get('pointer'):
                                    p_type += "*"
                                if p_default:
                                    param_strs.append(f"{p_type} {p_name} = {p_default}")
                                else:
                                    param_strs.append(f"{p_type} {p_name}")

                            params_str = ", ".join(param_strs) if param_strs else ""
                            const_str = " const" if is_const else ""
                            static_str = "static " if is_static else ""

                            click.echo(f"|       +- ", nl=False)
                            click.secho(f"{static_str}{return_type} ", fg='magenta', nl=False)
                            click.secho(f"{method_name}", fg='white', bold=True, nl=False)
                            click.echo(f"({params_str}){const_str}")

                            if method_doc:
                                click.secho(f"|       |     -- {method_doc[:55]}{'...' if len(method_doc) > 55 else ''}", fg='bright_black')
                        else:
                            # Simple string method name (legacy format)
                            click.echo(f"|       +- {method_info}()")

            click.secho("|", fg='green')
            _safe_echo("+" + "-" * 69 + "+", fg='green')

        # Structs section
        structs = module_info.get('structs', [])
        if structs:
            click.echo()
            _safe_echo("+-- Structs " + "-" * 58 + "+", fg='magenta')
            for struct in structs:
                struct_name = struct.get('name', '?')
                struct_doc = struct.get('doc', '')
                is_template = struct.get('is_template', False)
                template_types = struct.get('template_types', [])
                fields = struct.get('fields', [])

                click.secho(f"|", fg='magenta')
                if is_template:
                    click.secho(f"|  struct ", fg='magenta', nl=False)
                    click.secho(f"{struct_name}<{', '.join(template_types)}>", fg='white', bold=True)
                else:
                    click.secho(f"|  struct ", fg='magenta', nl=False)
                    click.secho(f"{struct_name}", fg='white', bold=True)

                if struct_doc:
                    click.secho(f"|     -- {struct_doc[:60]}{'...' if len(struct_doc) > 60 else ''}", fg='bright_black')

                if fields:
                    click.secho(f"|", fg='magenta')
                    click.secho(f"|     Fields:", fg='magenta')
                    for field in fields:
                        field_type = field.get('type', '?')
                        field_name = field.get('name', '?')
                        click.echo(f"|       +- ", nl=False)
                        click.secho(f"{field_type} ", fg='cyan', nl=False)
                        click.echo(f"{field_name}")

            click.secho("|", fg='magenta')
            _safe_echo("+" + "-" * 69 + "+", fg='magenta')

        # Functions section
        functions = module_info.get('functions', [])
        if functions:
            click.echo()
            _safe_echo("+-- Functions " + "-" * 56 + "+", fg='cyan')
            for func in functions:
                func_name = func.get('name', '?')
                func_doc = func.get('doc', '')
                return_type = func.get('return_type', 'void')
                params = func.get('parameters', [])
                is_static = func.get('static', False)
                is_const = func.get('const', False)
                is_inline = func.get('inline', False)

                # Build parameter string with types
                param_strs = []
                for p in params:
                    p_type = p.get('type', '?')
                    p_name = p.get('name', '?')
                    p_default = p.get('default', '')
                    if p.get('const'):
                        p_type = f"const {p_type}"
                    if p.get('reference'):
                        p_type += "&"
                    if p.get('pointer'):
                        p_type += "*"
                    if p_default:
                        param_strs.append(f"{p_type} {p_name} = {p_default}")
                    else:
                        param_strs.append(f"{p_type} {p_name}")

                params_str = ", ".join(param_strs) if param_strs else ""
                qualifiers = []
                if is_static:
                    qualifiers.append("static")
                if is_inline:
                    qualifiers.append("inline")
                if is_const:
                    qualifiers.append("const")
                qualifier_str = " ".join(qualifiers) + " " if qualifiers else ""

                click.secho(f"|", fg='cyan')
                click.echo(f"|  ", nl=False)
                click.secho(f"{qualifier_str}{return_type} ", fg='yellow', nl=False)
                click.secho(f"{func_name}", fg='white', bold=True, nl=False)
                click.echo(f"({params_str})")

                if func_doc:
                    click.secho(f"|     -- {func_doc[:60]}{'...' if len(func_doc) > 60 else ''}", fg='bright_black')

                # Show parameters in detail if any
                if params:
                    click.secho(f"|     Parameters:", fg='cyan')
                    for p in params:
                        p_type = p.get('type', '?')
                        p_name = p.get('name', '?')
                        p_default = p.get('default', '')
                        type_info = []
                        if p.get('const'):
                            type_info.append("const")
                        if p.get('reference'):
                            type_info.append("ref")
                        if p.get('pointer'):
                            type_info.append("ptr")
                        type_suffix = f" [{', '.join(type_info)}]" if type_info else ""
                        default_str = f" = {p_default}" if p_default else ""
                        click.echo(f"|       +- {p_name}: ", nl=False)
                        click.secho(f"{p_type}", fg='cyan', nl=False)
                        click.echo(f"{type_suffix}{default_str}")

            click.secho("|", fg='cyan')
            _safe_echo("+" + "-" * 69 + "+", fg='cyan')

        # Usage section
        click.echo()
        _safe_echo("+-- Usage Example " + "-" * 52 + "+", fg='white')
        click.echo(f"|")
        click.echo(f"|  from includecpp import CppApi")
        click.echo(f"|")
        click.echo(f"|  cpp = CppApi()")
        click.echo(f"|  {module_name} = cpp.include(\"{module_name}\")")
        click.echo(f"|")
        if functions:
            first_func = functions[0].get('name', 'function')
            click.echo(f"|  # Call a function")
            click.echo(f"|  result = {module_name}.{first_func}(...)")
        if classes:
            first_cls = classes[0].get('name', 'Class')
            click.echo(f"|")
            click.echo(f"|  # Use a class")
            click.echo(f"|  obj = {module_name}.{first_cls}()")
        click.echo(f"|")
        _safe_echo("+" + "-" * 69 + "+", fg='white')
        click.echo()

    except Exception as e:
        click.echo("")
        _safe_echo(_BOX_TOP, fg='red')
        _safe_echo(f"{_BOX_SIDE}  ERROR", fg='red')
        _safe_echo(_BOX_BOTTOM, fg='red')
        click.echo(f"\n{e}")

@cli.command()
@click.argument('module_name', required=False)
@click.option('--list-all', is_flag=True, help='List all available modules')
@click.option('--search', 'search_term', help='Search modules by name')
@click.pass_context
def install(ctx, module_name, list_all, search_term, _installed=None):
    """Install a module from GitHub: https://github.com/liliassg/IncludeCPP/minstall/{module}"""
    if _installed is None:
        _installed = set()

    if module_name and module_name in _installed:
        return

    if module_name:
        _installed.add(module_name)
    import tempfile
    import urllib.request
    import urllib.error
    import json

    # Handle --search option
    if search_term:
        click.echo("=" * 60)
        click.secho(f"Searching modules: '{search_term}'", fg='cyan', bold=True)
        click.echo("=" * 60)
        click.echo()

        try:
            api_url = "https://api.github.com/repos/liliassg/IncludeCPP/contents/minstall"
            click.echo("  Searching...", nl=False)

            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read())
                click.secho(" OK", fg='green')
                click.echo()

            # Filter modules by search term
            modules = [item['name'] for item in data if item['type'] == 'dir']
            matches = [m for m in modules if search_term.lower() in m.lower()]

            if not matches:
                click.secho(f"  No modules matching '{search_term}' found.", fg='yellow')
                click.echo()
                click.echo("  Available modules:")
                for m in sorted(modules)[:10]:
                    click.echo(f"    {_BULLET} {m}")
                if len(modules) > 10:
                    click.echo(f"    ... and {len(modules) - 10} more")
            else:
                click.secho(f"Found {len(matches)} matching module(s):", fg='green', bold=True)
                click.echo()
                for m in sorted(matches):
                    click.echo(f"  {_BULLET} {m}")
                click.echo()
                click.echo("Install with: includecpp install <module_name>")

        except Exception as e:
            click.secho(f"  FAILED ({e})", fg='red', err=True)

        click.echo("=" * 60)
        return

    # Handle --list-all option
    if list_all:
        click.echo("=" * 60)
        click.secho("Available IncludeCPP Modules", fg='cyan', bold=True)
        click.echo("=" * 60)
        click.echo(f"Source: https://github.com/liliassg/IncludeCPP/tree/main/minstall")
        click.echo()

        try:
            # Fetch directory listing from GitHub API
            api_url = "https://api.github.com/repos/liliassg/IncludeCPP/contents/minstall"
            click.echo("  Fetching module list...", nl=False)

            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read())
                click.secho(" OK", fg='green')
                click.echo()

            # Extract module names (directories)
            modules = [item['name'] for item in data if item['type'] == 'dir']

            if not modules:
                click.secho("  No modules found.", fg='yellow')
            else:
                click.secho(f"Found {len(modules)} module(s):", fg='green', bold=True)
                click.echo()
                for module in sorted(modules):
                    click.echo(f"  {_BULLET} {module}")

                click.echo()
                click.echo("Install a module with:")
                click.echo("  includecpp install <module_name>")

        except urllib.error.HTTPError as e:
            click.secho(f"  FAILED (HTTP {e.code})", fg='red', err=True)
            click.echo()
            click.echo("Could not fetch module list from GitHub.")
        except Exception as e:
            click.secho(f"  FAILED ({e})", fg='red', err=True)

        click.echo("=" * 60)
        return

    # Require module_name if not using --list-all
    if not module_name:
        click.secho("Error: Missing argument 'MODULE_NAME'.", fg='red', err=True)
        click.echo("Use 'includecpp install --list-all' to see available modules.")
        return

    # Check if include and plugins directories exist
    include_dir = Path.cwd() / "include"
    plugins_dir = Path.cwd() / "plugins"

    if not include_dir.exists() or not plugins_dir.exists():
        click.secho("Error: Not in a valid IncludeCPP project directory.", fg='red', err=True)
        click.echo("Run 'python -m includecpp init' first.")
        return

    click.echo("=" * 60)
    click.secho(f"Collecting {module_name}", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo(f"Source: https://github.com/liliassg/IncludeCPP/tree/main/minstall/{module_name}")
    click.echo()

    # GitHub raw content base URL
    base_url = f"https://raw.githubusercontent.com/liliassg/IncludeCPP/main/minstall/{module_name}/"

    # Try to download .cp, .cpp, .h, and .py files
    project_root = Path.cwd()
    files_to_download = [
        (f"{module_name}.cp", plugins_dir, "Plugin definition"),
        (f"{module_name}.cpp", include_dir, "C++ implementation"),
        (f"{module_name}.h", include_dir, "C++ header"),
        (f"{module_name}.py", project_root, "Python wrapper")
    ]

    downloaded = []

    for filename, target_dir, description in files_to_download:
        url = base_url + filename
        target_path = target_dir / filename

        try:
            click.echo(f"  Collecting {filename:20} ({description})...", nl=False)
            with urllib.request.urlopen(url) as response:
                content = response.read()

                # Write to target directory
                with open(target_path, 'wb') as f:
                    f.write(content)

                downloaded.append(filename)
                file_size_kb = len(content) / 1024
                click.secho(f" OK ({file_size_kb:.1f} KB)", fg='green')

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # File doesn't exist, skip (optional file like .h)
                click.secho(" SKIP (optional)", fg='yellow')
            else:
                click.secho(f" FAILED ({e})", fg='red', err=True)
        except Exception as e:
            click.secho(f" FAILED ({e})", fg='red', err=True)

    click.echo()

    if not downloaded:
        click.secho(f"Error: Module '{module_name}' not found or no files available.", fg='red', err=True)
        click.echo(f"Check https://github.com/liliassg/IncludeCPP/tree/main/minstall for available modules.")
        return

    click.secho(f"Successfully installed {len(downloaded)} file(s):", fg='green', bold=True)
    for f in downloaded:
        click.echo(f"  - {f}")

    # Check for dependencies in metadata.json
    try:
        meta_url = base_url + "metadata.json"
        with urllib.request.urlopen(meta_url) as response:
            metadata = json.loads(response.read())
            dependencies = metadata.get('dependencies', [])

            if dependencies:
                click.echo()
                click.secho("Dependencies detected:", fg='yellow')
                for dep in dependencies:
                    click.echo(f"  {_BULLET} {dep}")
                click.echo()
                click.echo("Installing dependencies...")

                # Recursively install dependencies
                for dep in dependencies:
                    if dep not in _installed:
                        click.echo(f"  Installing {dep}...")
                        ctx.invoke(install, module_name=dep, list_all=False, search_term=None, _installed=_installed)
    except Exception:
        pass  # No metadata or no dependencies

    click.echo()
    click.secho(f"Module '{module_name}' installed successfully!", fg='green', bold=True)
    click.echo("Run 'python -m includecpp rebuild' to build the module.")
    click.echo("=" * 60)

@cli.command()
@click.argument('module_name', required=False)
@click.option('--list-all', is_flag=True, help='List all available modules')
@click.option('--search', 'search_term', help='Search modules by name')
def minstall(module_name, list_all, search_term):
    """Alias for 'install' - Install modules from GitHub minstall repository."""
    # Call the install command with the same arguments
    ctx = click.get_current_context()
    ctx.invoke(install, module_name=module_name, list_all=list_all, search_term=search_term)

@cli.command()
@click.argument('target_version', required=False)
@click.option('--version', 'show_version', is_flag=True, help='Show current installed version')
@click.option('--all', 'list_all', is_flag=True, help='List all available versions from PyPI')
def update(target_version, show_version, list_all):
    """Update IncludeCPP package from PyPI.

    Usage:
      includecpp update              Upgrade to latest version
      includecpp update --version    Show current version
      includecpp update --all        List all available versions
      includecpp update X.X.X        Install specific version
    """
    import subprocess
    import urllib.request
    import json

    from .. import __version__ as current_version

    # --version: Show current version
    if show_version:
        click.echo("=" * 60)
        click.secho("IncludeCPP Version Info", fg='cyan', bold=True)
        click.echo("=" * 60)
        click.echo()
        click.echo(f"  Installed version: ", nl=False)
        click.secho(f"{current_version}", fg='green', bold=True)
        click.echo()
        click.echo("=" * 60)
        return

    # --all: List all PyPI versions
    if list_all:
        click.echo("=" * 60)
        click.secho("Available IncludeCPP Versions", fg='cyan', bold=True)
        click.echo("=" * 60)
        click.echo("Source: https://pypi.org/project/IncludeCPP/")
        click.echo()

        try:
            click.echo("  Fetching version list from PyPI...", nl=False)
            req = urllib.request.Request(
                "https://pypi.org/pypi/IncludeCPP/json",
                headers={"User-Agent": "IncludeCPP-CLI"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_data = response.read().decode('utf-8')

            data = json.loads(raw_data)
            click.secho(" OK", fg='green')
            click.echo()

            # Get all versions from releases
            releases = data.get('releases', {})
            version_list = [str(v) for v in releases.keys()]
            latest = str(data.get('info', {}).get('version', ''))

            if not version_list:
                click.secho("  No versions found.", fg='yellow')
            else:
                # Sort versions (newest first)
                def parse_version(ver):
                    try:
                        return tuple(int(x) for x in str(ver).split('.'))
                    except:
                        return (0, 0, 0)

                version_list.sort(key=parse_version, reverse=True)

                click.secho("Found " + str(len(version_list)) + " version(s):", fg='green', bold=True)
                click.echo()

                for ver in version_list:
                    ver_str = str(ver)
                    if ver_str == current_version and ver_str == latest:
                        click.echo("  * " + ver_str + " ", nl=False)
                        click.secho("[installed] [latest]", fg='green', bold=True)
                    elif ver_str == current_version:
                        click.echo("  * " + ver_str + " ", nl=False)
                        click.secho("[installed]", fg='cyan')
                    elif ver_str == latest:
                        click.echo("  * " + ver_str + " ", nl=False)
                        click.secho("[latest]", fg='yellow')
                    else:
                        click.echo("  * " + ver_str)

                click.echo()
                click.echo("Install a specific version with:")
                click.secho("  includecpp update <version>", fg='cyan')

        except Exception as e:
            click.secho(" FAILED", fg='red', err=True)
            click.echo()
            click.secho("Could not fetch version list: " + str(e), fg='red', err=True)

        click.echo("=" * 60)
        return

    # Install specific version
    if target_version:
        target = str(target_version)
        click.echo("=" * 60)
        click.secho("Installing IncludeCPP " + target, fg='cyan', bold=True)
        click.echo("=" * 60)
        click.echo()

        # Verify version exists on PyPI
        try:
            click.echo("  Verifying version on PyPI...", nl=False)
            req = urllib.request.Request(
                "https://pypi.org/pypi/IncludeCPP/json",
                headers={"User-Agent": "IncludeCPP-CLI"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_data = response.read().decode('utf-8')

            data = json.loads(raw_data)
            releases = data.get('releases', {})
            available = [str(v) for v in releases.keys()]

            if target not in available:
                click.secho(" NOT FOUND", fg='red')
                click.echo()
                click.secho("Version '" + target + "' does not exist on PyPI.", fg='red', err=True)
                click.echo("Use 'includecpp update --all' to see available versions.")
                click.echo("=" * 60)
                return

            click.secho(" OK", fg='green')

        except Exception as e:
            click.secho(" FAILED (" + str(e) + ")", fg='red', err=True)
            click.echo("=" * 60)
            return

        click.echo("  Current version:  " + current_version)
        click.echo("  Target version:   " + target)
        click.echo()

        if current_version == target:
            click.secho("Version " + target + " is already installed!", fg='green', bold=True)
            click.echo("=" * 60)
            return

        click.echo("  Installing IncludeCPP==" + target + "...", nl=False)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "IncludeCPP==" + target],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            click.secho(" OK", fg='green')
            click.echo()
            click.secho("Successfully installed IncludeCPP " + target + "!", fg='green', bold=True)
            click.echo("Restart your terminal to use the new version.")
        else:
            click.secho(" FAILED", fg='red', err=True)
            click.echo()
            click.secho("Installation failed!", fg='red', err=True, bold=True)
            if result.stderr:
                click.echo(result.stderr[:500])

        click.echo("=" * 60)
        return

    # Default: Upgrade to latest
    click.echo("=" * 60)
    click.secho("Checking for IncludeCPP Updates", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo()

    try:
        click.echo("  Fetching latest version from PyPI...", nl=False)
        with urllib.request.urlopen("https://pypi.org/pypi/IncludeCPP/json") as response:
            data = json.loads(response.read())
            latest_version = data['info']['version']
            click.secho(" OK", fg='green')

        click.echo()
        click.echo(f"  Current version: {current_version}")
        click.echo(f"  Latest version:  {latest_version}")
        click.echo()

        if current_version == latest_version:
            click.secho("IncludeCPP is already up to date!", fg='green', bold=True)
            click.echo("=" * 60)
            return

        click.echo(f"  Upgrading to version {latest_version}...", nl=False)

        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "IncludeCPP"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            click.secho(" OK", fg='green')
            click.echo()
            click.secho(f"Successfully upgraded to IncludeCPP {latest_version}!", fg='green', bold=True)
            click.echo("Restart your terminal to use the new version.")
        else:
            click.secho(" FAILED", fg='red', err=True)
            click.echo()
            click.secho("Upgrade failed!", fg='red', err=True, bold=True)
            if result.stderr:
                click.echo(result.stderr[:500])

    except Exception as e:
        click.secho(f" FAILED", fg='red', err=True)
        click.echo()
        click.secho(f"Failed to check for updates: {e}", fg='red', err=True)

    click.echo("=" * 60)


@cli.command()
def reboot():
    """Reinstall IncludeCPP (uninstall + install current version).

    This command reinstalls the currently installed version without upgrading.
    Useful for fixing corrupted installations or resetting to a clean state.
    """
    import subprocess

    from .. import __version__ as current_version

    click.echo("=" * 60)
    click.secho("IncludeCPP Reboot", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo()
    click.echo(f"  Current version: {current_version}")
    click.echo()
    click.secho("This will reinstall IncludeCPP without changing the version.", fg='yellow')
    click.echo()

    # Step 1: Uninstall
    click.echo(f"  [1/2] Uninstalling IncludeCPP...", nl=False)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "IncludeCPP", "-y"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        click.secho(" FAILED", fg='red', err=True)
        click.echo()
        click.secho("Uninstall failed!", fg='red', err=True, bold=True)
        if result.stderr:
            click.echo(result.stderr[:500])
        click.echo("=" * 60)
        return

    click.secho(" OK", fg='green')

    # Step 2: Reinstall same version
    click.echo(f"  [2/2] Installing IncludeCPP=={current_version}...", nl=False)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", f"IncludeCPP=={current_version}"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        click.secho(" OK", fg='green')
        click.echo()
        click.secho(f"Successfully reinstalled IncludeCPP {current_version}!", fg='green', bold=True)
        click.echo("Restart your terminal to use the reinstalled version.")
    else:
        click.secho(" FAILED", fg='red', err=True)
        click.echo()
        click.secho("Reinstall failed!", fg='red', err=True, bold=True)
        if result.stderr:
            click.echo(result.stderr[:500])
        click.echo()
        click.echo("Try manually installing with:")
        click.secho(f"  pip install IncludeCPP=={current_version}", fg='cyan')

    click.echo("=" * 60)

@cli.command()
@click.argument('plugin_name')
@click.argument('files', nargs=-1, required=False)
@click.option('--private', '-p', multiple=True, help='Private functions to exclude from public API')
def plugin(plugin_name, files, private):
    """Generate or regenerate a .cp plugin definition from C++ source files.

    If no files are provided and an existing .cp file exists, SOURCE() and HEADER()
    paths are read from it to auto-regenerate the plugin definition.
    """
    import re
    from pathlib import Path

    # Normalize plugin_name: strip .cp extension and path prefixes
    if plugin_name.endswith('.cp'):
        plugin_name = plugin_name[:-3]
    plugin_name = Path(plugin_name).stem

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"

    if not plugins_dir.exists():
        click.secho("Error: plugins/ directory not found", fg='red', err=True)
        click.echo("Run 'python -m includecpp init' first")
        return

    if not files:
        existing_cp = plugins_dir / f"{plugin_name}.cp"
        if existing_cp.exists():
            click.echo(f"Auto-regenerating from existing: {existing_cp}")
            source_files, header_files = _parse_cp_sources(existing_cp)
            if not source_files:
                click.secho("Error: No SOURCE() found in existing .cp file", fg='red', err=True)
                click.echo("Usage: includecpp plugin <name> <file1.cpp> [file2.h] ...")
                return
            # Combine and use as input files
            files = tuple(source_files + header_files)
            click.echo(f"Found sources: {', '.join(str(f) for f in files)}")
        else:
            click.secho("Error: No files provided and no existing .cp file found", fg='red', err=True)
            click.echo("Usage: includecpp plugin <name> <file1.cpp> [file2.h] ...")
            return

    cpp_files = []
    h_files = []

    for file_path in files:
        p = Path(file_path)
        if not p.is_absolute():
            p = project_root / p

        if not p.exists():
            click.secho(f"Error: File not found: {file_path}", fg='red', err=True)
            return

        if p.suffix == '.cpp':
            cpp_files.append(p)
        elif p.suffix == '.h':
            h_files.append(p)

    if not cpp_files:
        click.secho("Error: No .cpp files provided", fg='red', err=True)
        return

    classes = {}
    functions = set()
    template_functions = {}  # v3.1.6: {name: set of types}
    enums = {}  # v4.6.5: {name: {'is_class': bool, 'values': list}}
    namespaces = set()

    def find_matching_brace(text, start_pos):
        """Find the position of the matching closing brace using bracket counting."""
        brace_count = 0
        for i, char in enumerate(text[start_pos:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return start_pos + i
        return len(text) - 1

    def extract_public_section(class_body, is_struct=False):
        """Extract ALL public sections from a class body.

        v2.8.2: Fixed to collect multiple public sections, not just the first one.
        Classes can have: public: ... private: ... public: ... (multiple public blocks)
        """
        # For struct, everything before first access specifier is public
        if is_struct:
            first_access = re.search(r'\b(private|protected)\s*:', class_body)
            if first_access:
                struct_public = class_body[:first_access.start()]
            else:
                struct_public = class_body
            # Also collect any explicit public: sections in struct
            public_sections = [struct_public]
        else:
            public_sections = []

        # Find ALL public: sections (there can be multiple)
        access_pattern = re.compile(r'\b(public|private|protected)\s*:', re.MULTILINE)

        matches = list(access_pattern.finditer(class_body))
        if not matches and not is_struct:
            return ""  # No access specifiers in class = nothing public

        for i, match in enumerate(matches):
            if match.group(1) == 'public':
                start = match.end()
                # Find where this public section ends (next access specifier or end of class)
                if i + 1 < len(matches):
                    end = matches[i + 1].start()
                else:
                    end = len(class_body)
                public_sections.append(class_body[start:end])

        return '\n'.join(public_sections)

    def extract_param_types(params_str):
        """Extract parameter types from a parameter string like 'double x, double y'."""
        if not params_str or params_str.strip() == '':
            return []

        types = []
        # Split by comma, but be careful with template types like std::vector<int, alloc>
        depth = 0
        current = ''
        for char in params_str:
            if char in '<(':
                depth += 1
                current += char
            elif char in '>)':
                depth -= 1
                current += char
            elif char == ',' and depth == 0:
                types.append(current.strip())
                current = ''
            else:
                current += char
        if current.strip():
            types.append(current.strip())

        # Extract just the type from each parameter (remove variable name)
        result = []
        for param in types:
            param = param.strip()
            if not param:
                continue
            # Remove default value if present
            if '=' in param:
                param = param.split('=')[0].strip()
            # Find the type: everything before the last word (variable name)
            # Handle cases like "const std::string& name" -> "const std::string&"
            parts = param.rsplit(None, 1)
            if len(parts) == 1:
                # Just a type, no name (e.g., in declaration "void foo(int)")
                result.append(parts[0])
            else:
                # Check if last part is a pointer/reference suffix attached to type
                type_part = parts[0]
                # Handle cases where * or & is attached to variable name
                if parts[1].startswith('*') or parts[1].startswith('&'):
                    type_part = parts[0] + parts[1][0]
                result.append(type_part)
        return result

    def extract_method_param_types(params_str):
        """v2.4.13: Extract parameter types for method overload resolution.

        Input: 'const Circle& other, int count'
        Output: ['const Circle&', 'int']
        """
        if not params_str or params_str.strip() == '':
            return []

        params = []
        depth = 0
        current = ''

        # Split by comma, respecting template depth
        for char in params_str:
            if char in '<(':
                depth += 1
                current += char
            elif char in '>)':
                depth -= 1
                current += char
            elif char == ',' and depth == 0:
                params.append(current.strip())
                current = ''
            else:
                current += char
        if current.strip():
            params.append(current.strip())

        result = []
        for param in params:
            param = param.strip()
            if not param:
                continue

            # Remove default value
            if '=' in param:
                param = param.split('=')[0].strip()

            # Parse: [const] type[&*] [name]
            # We need to extract the full type including const, &, *

            # Check for trailing reference/pointer that might be attached to name
            # e.g., "const Circle& other" or "Circle &other"

            # Strategy: Extract type by properly handling nested templates
            # Handle cases like "const std::vector<std::pair<int, float>>& items"

            import re

            # First, extract the type portion by finding where the variable name starts
            # The variable name is the last identifier not inside < >

            def extract_type_from_param(param_str):
                """Extract type from parameter, handling nested templates."""
                param_str = param_str.strip()

                # Find where the type ends and variable name begins
                # We scan from the end to find the variable name (last word not in templates)
                depth = 0
                type_end = len(param_str)

                # Scan backwards to find the start of the variable name
                i = len(param_str) - 1
                while i >= 0:
                    c = param_str[i]
                    if c == '>':
                        depth += 1
                    elif c == '<':
                        depth -= 1
                    elif c in ' \t' and depth == 0:
                        # Found space outside templates - check if what follows is a variable name
                        rest = param_str[i+1:].strip()
                        if rest and re.match(r'^[a-zA-Z_]\w*$', rest):
                            type_end = i
                            break
                    i -= 1

                type_str = param_str[:type_end].strip()

                # Handle case where & or * is attached to the variable name
                # e.g., "Circle &other" -> type should be "Circle&"
                rest = param_str[type_end:].strip()
                if rest.startswith('&') or rest.startswith('*'):
                    type_str += rest[0]

                # Normalize spacing
                type_str = re.sub(r'\s+([&*])', r'\1', type_str)  # Remove space before &/*
                type_str = re.sub(r'\s+', ' ', type_str)  # Normalize spaces

                return type_str if type_str else param_str

            type_str = extract_type_from_param(param)
            result.append(type_str)

        return result

    def extract_methods(public_section, class_name):
        """Extract method names from public section, handling inline bodies.

        """
        methods = set()
        method_signatures = {}
        constructor_signatures = []

        method_regex = re.compile(
            r'(?:(?:virtual|static|inline|explicit|constexpr)\s+)*'  # Optional modifiers
            r'(?:const\s+)?'  # Optional const before return type
            r'((?:(?:unsigned|signed|long|short)\s+)*'  # v4.3.2: Handle multi-word types (unsigned long long, etc.)
            r'[a-zA-Z_][\w:]*(?:<[^<>]*(?:<[^<>]*>[^<>]*)*>)?(?:\s*[&*])?)\s+'  # Return type (handles nested templates)
            r'(\w+)\s*'  # Method name
            r'\(([^)]*)\)\s*'  # Parameters (captured in group 3)
            r'(const)?'  # Const qualifier after params (captured in group 4)
            r'(?:override|final|noexcept|\s)*'  # Other qualifiers
            r'(?::\s*[^{;]+)?'  # Optional initializer list
            r'(?:\{|;)',  # Body start or declaration end
            re.MULTILINE
        )

        invalid_return_types = {'return', 'new', 'delete', 'throw', 'co_return', 'co_yield'}

        cpp_keywords = {
            'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor',
            'bool', 'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t',
            'class', 'compl', 'concept', 'const', 'consteval', 'constexpr', 'constinit',
            'const_cast', 'continue', 'co_await', 'co_return', 'co_yield', 'decltype',
            'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum',
            'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto',
            'if', 'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept',
            'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected',
            'public', 'register', 'reinterpret_cast', 'requires', 'return', 'short',
            'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct',
            'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try',
            'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual',
            'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
        }

        for match in method_regex.finditer(public_section):
            return_type = match.group(1).strip()
            method_name = match.group(2).strip()
            params_str = match.group(3).strip() if match.group(3) else ''
            is_const = match.group(4) is not None

            if return_type.lower() in invalid_return_types:
                continue

            if method_name.lower() in cpp_keywords:
                continue

            text_before_match = public_section[:match.start()]
            open_braces = text_before_match.count('{')
            close_braces = text_before_match.count('}')
            if open_braces > close_braces:
                continue  # Inside a function body, this is a local var not a method

            # Skip if method name is the class name (it's a constructor)
            if method_name == class_name:
                continue  # Will be handled by dedicated constructor pattern

            # Skip destructors
            if method_name.startswith('~'):
                continue

            # Skip operators (operator+, operator==, etc.)
            if method_name == 'operator':
                continue

            methods.add(method_name)

            param_types = extract_method_param_types(params_str)

            # Store method signature
            sig = {'params': param_types, 'is_const': is_const}
            if method_name not in method_signatures:
                method_signatures[method_name] = []
            method_signatures[method_name].append(sig)

        potential_ctor_pattern = re.compile(
            rf'(?:explicit\s+)?\b{re.escape(class_name)}\s*\(([^)]*)\)',
            re.MULTILINE
        )

        for match in potential_ctor_pattern.finditer(public_section):
            params_str = match.group(1).strip()
            match_start = match.start()

            # Get the text before this match on the same line
            line_start = public_section.rfind('\n', 0, match_start)
            if line_start == -1:
                line_start = 0
            else:
                line_start += 1  # Skip the newline character
            text_before = public_section[line_start:match_start]

            # Skip if this is a constructor call (after return, new, =, etc.)
            if re.search(r'\b(return|new)\s*$', text_before):
                continue
            if text_before.strip().endswith('='):
                continue
            if text_before.strip().endswith('('):
                continue  # Inside another function call

            # Skip if we're inside a function body (unbalanced braces before us)
            text_from_start = public_section[:match_start]
            open_braces = text_from_start.count('{')
            close_braces = text_from_start.count('}')
            if open_braces > close_braces:
                continue  # We're inside a function body, this is a call not a declaration

            # Check what follows the constructor - must indicate a declaration
            after_match = public_section[match.end():match.end() + 100]

            # A declaration is followed by : (initializer), { (body), ; (forward decl), or = default/delete
            if not re.match(r'\s*(?::\s*|[{;]|=\s*(?:default|delete))', after_match):
                continue  # Not a declaration

            # This is a valid constructor declaration
            param_types = extract_param_types(params_str)
            constructor_signatures.append(tuple(param_types))

        return methods, constructor_signatures, method_signatures

    def extract_fields(public_section, class_name):
        """Extract member variable declarations from public section.

        v3.2.2: Handles comma-separated field declarations like:
        double x, y, z;  ->  [('double', 'x'), ('double', 'y'), ('double', 'z')]
        """
        fields = []

        # Pattern to match field declarations
        # Matches: type name; OR type name1, name2, name3;
        # Handles: int x; double x, y, z; std::vector<int> items; const float PI = 3.14;
        field_pattern = re.compile(
            r'^\s*'  # Start of line, optional whitespace
            r'(?:static\s+)?'  # Optional static
            r'(const\s+)?'  # Optional const (group 1)
            r'([a-zA-Z_][\w:]*(?:<[^<>]*(?:<[^<>]*>[^<>]*)*>)?)'  # Type (group 2) - handles nested templates
            r'(\s*[&*])?'  # Optional reference/pointer (group 3)
            r'\s+'  # Required whitespace
            r'([^;(=]+)'  # Names part - everything until ; ( or = (group 4)
            r'\s*(?:=\s*[^;]+)?'  # Optional initializer
            r'\s*;',  # Semicolon
            re.MULTILINE
        )

        cpp_keywords = {
            'return', 'new', 'delete', 'throw', 'if', 'else', 'for', 'while', 'switch',
            'case', 'break', 'continue', 'class', 'struct', 'enum', 'typedef', 'using',
            'namespace', 'template', 'typename', 'virtual', 'override', 'final', 'public',
            'private', 'protected', 'friend', 'operator', 'sizeof', 'alignof', 'decltype',
            'auto', 'register', 'extern', 'mutable', 'thread_local', 'constexpr', 'consteval',
            'constinit', 'inline', 'volatile'
        }

        # Process line by line to handle function body context
        lines = public_section.split('\n')
        brace_depth = 0

        for line in lines:
            # Track brace depth to skip function bodies
            brace_depth += line.count('{') - line.count('}')
            if brace_depth > 0:
                continue  # Inside a function body

            # Skip lines that look like function declarations/definitions
            stripped = line.strip()
            if '(' in stripped and ')' in stripped:
                continue

            match = field_pattern.match(line)
            if match:
                is_const = match.group(1) is not None
                base_type = match.group(2).strip()
                ref_ptr = (match.group(3) or '').strip()
                names_part = match.group(4).strip()

                # Skip if type looks like a keyword or constructor
                if base_type.lower() in cpp_keywords:
                    continue
                if base_type == class_name:
                    continue  # Constructor, not a field

                # Build full type
                full_type = ''
                if is_const:
                    full_type = 'const '
                full_type += base_type
                if ref_ptr:
                    full_type += ref_ptr

                # Split comma-separated names: "x, y, z" -> ["x", "y", "z"]
                # Handle cases like: "*ptr1, *ptr2" or "&ref1, &ref2"
                name_parts = names_part.split(',')

                for name in name_parts:
                    name = name.strip()
                    if not name:
                        continue

                    # Handle pointer/reference attached to variable name
                    actual_type = full_type
                    if name.startswith('*'):
                        name = name[1:].strip()
                        if '*' not in actual_type:
                            actual_type += '*'
                    elif name.startswith('&'):
                        name = name[1:].strip()
                        if '&' not in actual_type:
                            actual_type += '&'

                    # v4.6.6: Detect array fields and capture size
                    array_size = 0
                    if '[' in name:
                        # Extract array size: "magic[4]" -> size=4, name="magic"
                        bracket_idx = name.find('[')
                        end_bracket = name.find(']')
                        if end_bracket > bracket_idx:
                            size_str = name[bracket_idx+1:end_bracket].strip()
                            try:
                                array_size = int(size_str) if size_str else 0
                            except ValueError:
                                array_size = 0  # Unknown/variable size
                        name = name[:bracket_idx].strip()

                    # Validate field name
                    if name and re.match(r'^[a-zA-Z_]\w*$', name):
                        # Skip if name is a keyword
                        if name.lower() not in cpp_keywords:
                            # v4.6.6: Include array info (type, name, array_size)
                            # array_size=0 means not an array
                            fields.append((actual_type, name, array_size))

        return fields

    all_files = cpp_files + h_files

    def read_source_file(filepath):
        """Read source file with encoding detection (UTF-8, UTF-16, Latin-1)."""
        encodings = ['utf-8', 'utf-16', 'utf-8-sig', 'latin-1']
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        # Last resort: read as binary and decode with errors replaced
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='replace')

    for file in all_files:
        content = read_source_file(file)

        # Extract namespaces
        namespace_matches = re.findall(r'\bnamespace\s+(\w+)', content)
        namespaces.update(namespace_matches)

        # Find class/struct declarations with proper bracket matching
        class_pattern = re.compile(
            r'\b(class|struct)\s+(\w+)\s*'  # class/struct keyword and name
            r'(?::\s*(?:public|private|protected)?\s*\w+(?:\s*,\s*(?:public|private|protected)?\s*\w+)*)?\s*'  # Optional inheritance
            r'\{',  # Opening brace
            re.MULTILINE
        )

        for match in class_pattern.finditer(content):
            keyword = match.group(1)
            class_name = match.group(2)
            is_struct = keyword == 'struct'
            brace_start = match.end() - 1

            # v4.6.5: Skip "enum class" declarations - check if preceded by "enum"
            text_before_match = content[max(0, match.start()-10):match.start()]
            if re.search(r'\benum\s*$', text_before_match):
                continue

            text_before = content[:match.start()]
            open_braces = text_before.count('{')
            close_braces = text_before.count('}')

            if open_braces > close_braces:
                # We're inside another class/struct body - check access level
                last_public = text_before.rfind('public:')
                last_private = text_before.rfind('private:')
                last_protected = text_before.rfind('protected:')

                # Skip if in private/protected section of parent class
                if last_private > last_public or last_protected > last_public:
                    continue

            # Find matching closing brace
            brace_end = find_matching_brace(content, brace_start)
            class_body = content[brace_start + 1:brace_end]

            # Extract public section
            public_section = extract_public_section(class_body, is_struct)

            if class_name not in classes:
                classes[class_name] = {'methods': set(), 'constructors': [], 'method_signatures': {}, 'fields': []}

            methods, constructor_sigs, method_sigs = extract_methods(public_section, class_name)
            classes[class_name]['methods'].update(methods)

            for mname, sigs in method_sigs.items():
                if mname not in classes[class_name]['method_signatures']:
                    classes[class_name]['method_signatures'][mname] = []
                for sig in sigs:
                    if sig not in classes[class_name]['method_signatures'][mname]:
                        classes[class_name]['method_signatures'][mname].append(sig)

            existing_ctors = set(classes[class_name]['constructors'])
            for sig in constructor_sigs:
                if sig not in existing_ctors:
                    classes[class_name]['constructors'].append(sig)
                    existing_ctors.add(sig)

            # v3.2.2: Extract fields (including comma-separated declarations)
            # v4.6.6: Now returns (type, name, array_size) tuples
            field_list = extract_fields(public_section, class_name)
            for field_info in field_list:
                field_type, field_name = field_info[0], field_info[1]
                array_size = field_info[2] if len(field_info) > 2 else 0
                if (field_type, field_name) not in classes[class_name]['fields']:
                    classes[class_name]['fields'].append((field_type, field_name))

        # Find free functions (not inside class bodies)
        # First, remove all class bodies from content to avoid matching class methods
        content_no_classes = content
        for match in class_pattern.finditer(content):
            brace_start = match.end() - 1
            brace_end = find_matching_brace(content, brace_start)
            # Replace class body with spaces to preserve positions
            class_body = content[match.start():brace_end + 1]
            content_no_classes = content_no_classes.replace(class_body, ' ' * len(class_body), 1)

        # Now find functions in the cleaned content
        func_pattern = re.compile(
            r'((?:(?:inline|static|extern|constexpr)\s+)*)'  # Capture modifiers (group 1)
            r'(?:const\s+)?'  # Optional const
            r'[a-zA-Z_][\w:]*(?:<[^<>]*(?:<[^<>]*>[^<>]*)*>)?(?:\s*[&*])?\s+'  # Return type (must start with letter, handles nested templates)
            r'(\w+)\s*'  # Function name (group 2)
            r'\([^)]*\)\s*'  # Parameters
            r'(?:const|noexcept|\s)*'  # Optional qualifiers
            r'\{',  # Body start (not just declaration)
            re.MULTILINE
        )

        # v3.1.6: Find template function definitions
        template_func_pattern = re.compile(
            r'template\s*<[^>]+>\s*'  # template<typename T> or template<class T>
            r'(?:(?:inline|static|extern|constexpr)\s+)*'  # Optional modifiers
            r'(?:const\s+)?'  # Optional const
            r'[a-zA-Z_][\w:]*(?:<[^<>]*>)?(?:\s*[&*])?\s+'  # Return type (T or specific type)
            r'(\w+)\s*'  # Function name (group 1)
            r'\([^)]*\)\s*'  # Parameters
            r'(?:const|noexcept|\s)*'  # Optional qualifiers
            r'\{',  # Body start
            re.MULTILINE
        )

        # v3.1.6: Find explicit template instantiations
        # Pattern: template int clamp<int>(int, int, int);
        template_instantiation_pattern = re.compile(
            r'template\s+'  # template keyword
            r'[a-zA-Z_][\w:]*(?:<[^<>]*>)?(?:\s*[&*])?\s+'  # Return type
            r'(\w+)\s*'  # Function name (group 1)
            r'<\s*(\w+)\s*>'  # Template argument (group 2)
            r'\s*\([^)]*\)\s*;',  # Parameters and semicolon
            re.MULTILINE
        )

        # Collect template function names
        template_func_names = set()
        for match in template_func_pattern.finditer(content_no_classes):
            func_name = match.group(1)
            if func_name not in ['if', 'while', 'for', 'switch', 'catch']:
                template_func_names.add(func_name)
                if func_name not in template_functions:
                    template_functions[func_name] = set()

        # Parse explicit instantiations for types
        for match in template_instantiation_pattern.finditer(content):
            func_name = match.group(1)
            type_arg = match.group(2)
            if func_name in template_func_names:
                template_functions[func_name].add(type_arg)

        for match in func_pattern.finditer(content_no_classes):
            modifiers = match.group(1) or ''
            func_name = match.group(2)
            # Skip static functions - they have internal linkage, not public API
            if 'static' in modifiers:
                continue
            # Skip inline functions - they are typically internal helpers
            if 'inline' in modifiers:
                continue
            # Skip functions starting with underscore - internal/private by convention
            if func_name.startswith('_'):
                continue
            if func_name not in ['if', 'while', 'for', 'switch', 'catch']:
                # v3.1.6: Skip template functions (handled separately)
                if func_name not in template_func_names:
                    functions.add(func_name)

        # v4.6.5: Find enum declarations
        enum_pattern = re.compile(
            r'\benum\s+(class\s+)?(\w+)\s*\{([^}]*)\}',
            re.MULTILINE | re.DOTALL
        )

        for match in enum_pattern.finditer(content):
            is_class_enum = bool(match.group(1))
            enum_name = match.group(2)
            enum_body = match.group(3)

            # Parse enum values
            values = []
            # Split by comma and extract value names (ignoring assignments)
            for part in enum_body.split(','):
                part = part.strip()
                if not part:
                    continue
                # Get the value name (before any = assignment)
                value_name = part.split('=')[0].strip()
                if value_name and re.match(r'^[a-zA-Z_]\w*$', value_name):
                    values.append(value_name)

            if enum_name not in enums and values:
                enums[enum_name] = {
                    'is_class': is_class_enum,
                    'values': values
                }

    private_set = set(private) if private else set()
    public_functions = functions - private_set - set(classes.keys())

    cp_file = plugins_dir / f"{plugin_name}.cp"

    # Generate individual SOURCE() declarations for each file (cleaner format)
    cpp_paths = [str(f.relative_to(project_root) if f.is_relative_to(project_root) else f).replace('\\', '/') for f in cpp_files]
    h_paths = [str(f.relative_to(project_root) if f.is_relative_to(project_root) else f).replace('\\', '/') for f in h_files] if h_files else []

    with open(cp_file, 'w', encoding='utf-8') as f:
        # Build the declaration line: SOURCE(file1) && SOURCE(file2) && HEADER(h1) plugin_name
        parts = [f'SOURCE({p})' for p in cpp_paths]
        parts.extend([f'HEADER({p})' for p in h_paths])
        declaration = ' && '.join(parts) + f' {plugin_name}'
        f.write(declaration + '\n\n')

        if classes or public_functions or template_functions or enums:
            f.write('PUBLIC(\n')

            # v4.6.5: Write enum bindings
            for enum_name in sorted(enums.keys()):
                enum_info = enums[enum_name]
                is_class = enum_info.get('is_class', False)
                values = enum_info.get('values', [])

                class_kw = ' CLASS' if is_class else ''
                values_str = ' '.join(values)
                f.write(f'    {plugin_name} ENUM({enum_name}){class_kw} {{ {values_str} }}\n')

            if enums and classes:
                f.write('\n')

            for cls_name in sorted(classes.keys()):
                cls_info = classes[cls_name]
                f.write(f'    {plugin_name} CLASS({cls_name}) {{\n')

                if cls_info['constructors']:
                    for ctor_params in cls_info['constructors']:
                        if ctor_params:
                            # Parametrized constructor
                            params_str = ', '.join(ctor_params)
                            f.write(f'        CONSTRUCTOR({params_str})\n')
                        else:
                            # Default constructor
                            f.write(f'        CONSTRUCTOR()\n')
                else:
                    f.write(f'        CONSTRUCTOR()\n')

                method_sigs = cls_info.get('method_signatures', {})
                if method_sigs:
                    # Use new signature-based METHOD format
                    for method_name in sorted(method_sigs.keys()):
                        for sig in method_sigs[method_name]:
                            param_types = sig.get('params', [])
                            is_const = sig.get('is_const', False)

                            if param_types:
                                params_str = ', '.join(param_types)
                                if is_const:
                                    f.write(f'        METHOD_CONST({method_name}, {params_str})\n')
                                else:
                                    f.write(f'        METHOD({method_name}, {params_str})\n')
                            else:
                                if is_const:
                                    f.write(f'        METHOD_CONST({method_name})\n')
                                else:
                                    f.write(f'        METHOD({method_name})\n')
                else:
                    # Legacy: simple method names (backward compatibility)
                    for method in sorted(cls_info['methods']):
                        f.write(f'        METHOD({method})\n')

                # v3.2.2: Write fields
                # v4.6.6: Support array fields with FIELD_ARRAY(name, type, size)
                if cls_info.get('fields'):
                    for field_info in cls_info['fields']:
                        # Handle both old (type, name) and new (type, name, array_size) formats
                        if len(field_info) >= 3:
                            field_type, field_name, array_size = field_info
                        else:
                            field_type, field_name = field_info
                            array_size = 0

                        if array_size > 0:
                            # Array field: use FIELD_ARRAY with type info for proper binding
                            f.write(f'        FIELD_ARRAY({field_name}, {field_type}, {array_size})\n')
                        else:
                            f.write(f'        FIELD({field_name})\n')

                f.write(f'    }}\n')

            if classes and (public_functions or template_functions):
                f.write('\n')

            # v3.1.6: Write template functions with TYPES
            for func_name in sorted(template_functions.keys()):
                types = template_functions[func_name]
                if types:
                    types_str = ', '.join(sorted(types))
                    f.write(f'    {plugin_name} TEMPLATE_FUNC({func_name}) TYPES({types_str})\n')
                else:
                    # Template function without explicit instantiations - write as regular
                    f.write(f'    {plugin_name} FUNC({func_name})\n')

            for func in sorted(public_functions):
                if not any(c.lower() in func.lower() or func.lower() in c.lower() for c in classes.keys()):
                    f.write(f'    {plugin_name} FUNC({func})\n')

            f.write(')\n')

    click.secho(f"Generated plugin: {cp_file}", fg='green', bold=True)
    click.echo(f"Enums found: {len(enums)}")
    click.echo(f"Classes found: {len(classes)}")
    total_fields = sum(len(c.get('fields', [])) for c in classes.values())
    if total_fields:
        click.echo(f"Fields found: {total_fields}")
    click.echo(f"Template functions: {len(template_functions)}")
    click.echo(f"Public functions: {len(public_functions)}")
    if private_set:
        click.echo(f"Private functions excluded: {len(private_set)}")
    click.echo()
    click.echo("Build commands:")
    click.echo("  includecpp rebuild --fast   Incremental build (existing plugins)")
    click.echo("  includecpp rebuild --clean  Full rebuild (new plugins)")
    click.echo("  includecpp rebuild          Standard build")

# GitHub API configuration for bug reporting and module upload
_GITHUB_TOKEN = "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"
_GITHUB_REPO = "liliassg/IncludeCPP"

@cli.command()
@click.argument('message')
@click.argument('files', nargs=-1, type=click.Path())
def bug(message, files):
    """Report a bug on GitHub Issues.

    Opens your browser to create a new issue with pre-filled system info.

    Usage:
      includecpp bug "Description of the bug"
      includecpp bug "Crash when loading module" ./include/mylib.cpp ./app.py
    """
    import webbrowser
    import urllib.parse
    import platform
    from .. import __version__

    click.echo("=" * 60)
    click.secho("Bug Report", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo()

    # Build issue title
    title = f"[Bug] {message[:50]}{'...' if len(message) > 50 else ''}"

    # Build issue body with system info
    body_parts = [
        "## Bug Description",
        message,
        "",
        "## System Information",
        f"- **IncludeCPP Version:** {__version__}",
        f"- **Python:** {platform.python_version()}",
        f"- **OS:** {platform.system()} {platform.release()}",
        f"- **Architecture:** {platform.machine()}",
    ]

    # Add file info if provided
    if files:
        body_parts.append("")
        body_parts.append("## Related Files")
        for filepath in files:
            filepath = Path(filepath)
            if filepath.exists():
                size = filepath.stat().st_size
                ext = filepath.suffix
                body_parts.append(f"- `{filepath.name}` ({ext}, {size} bytes)")

                # Include small file contents (< 2KB)
                if size < 2048 and ext in ['.py', '.cpp', '.h', '.hpp', '.cssl', '.txt']:
                    try:
                        content = filepath.read_text(errors='replace')[:1500]
                        body_parts.append(f"```{ext[1:] if ext else 'text'}")
                        body_parts.append(content)
                        body_parts.append("```")
                    except:
                        pass
            else:
                body_parts.append(f"- `{filepath}` (file not found)")

    body_parts.append("")
    body_parts.append("---")
    body_parts.append("*Submitted via `includecpp bug` command*")

    body = "\n".join(body_parts)

    # Build GitHub issue URL with pre-filled content
    params = urllib.parse.urlencode({
        'title': title,
        'body': body,
        'labels': 'bug'
    })

    issue_url = f"https://github.com/{_GITHUB_REPO}/issues/new?{params}"

    click.echo(f"  Description: {message[:60]}{'...' if len(message) > 60 else ''}")
    if files:
        click.echo(f"  Files: {len(files)} attached")
    click.echo()

    click.echo("  Opening GitHub Issues...", nl=False)

    try:
        webbrowser.open(issue_url)
        click.secho(" OK", fg='green')
        click.echo()
        click.secho("Browser opened! Complete your bug report on GitHub.", fg='green')
    except Exception as e:
        click.secho(f" FAILED", fg='red')
        click.echo()
        click.echo("Could not open browser. Please visit manually:")
        click.echo(f"  https://github.com/{_GITHUB_REPO}/issues/new")
        click.echo()
        click.echo("Title:")
        click.secho(f"  {title}", fg='yellow')
        click.echo()
        click.echo("Copy this description:")
        click.echo("-" * 40)
        click.echo(body[:500])
        if len(body) > 500:
            click.echo("...")

    click.echo()
    click.echo("=" * 60)

# =============================================================================
# MODULE UPLOAD COMMAND
# =============================================================================

# Security patterns for upload validation
_API_KEY_PATTERNS = [
    r'["\']?(?:api[_-]?key|apikey|api_secret|secret_key|access_token|auth_token|bearer)["\']?\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}["\']',
    r'(?:ghp_|github_pat_|sk-|pk_live_|pk_test_|sk_live_|sk_test_)[a-zA-Z0-9_\-]{20,}',
    r'(?:AKIA|ASIA)[A-Z0-9]{16}',  # AWS keys
    r'-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?:password|passwd|pwd)\s*[:=]\s*["\'][^"\']{8,}["\']',
]

# Extreme bad words only (user requested: bitch, fuck etc are OK)
_EXTREME_BAD_WORDS = [
    'n1gger', 'n1gga', 'nigger', 'nigga', 'faggot', 'kike', 'spic', 'chink', 'wetback',
    'kill yourself', 'kys',
]


def _scan_file_security(filepath):
    """Scan a file for security issues.

    Returns:
        Tuple of (is_safe, issues) where issues is a list of problem descriptions
    """
    import re

    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            content_lower = content.lower()

        # Check for API keys/secrets
        for pattern in _API_KEY_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append(f"Potential API key/secret detected in {filepath.name}")
                break  # One is enough to block

        # Check for extreme bad words
        for word in _EXTREME_BAD_WORDS:
            if word.lower() in content_lower:
                issues.append(f"Inappropriate content detected in {filepath.name}")
                break

    except Exception as e:
        pass  # Ignore read errors

    return (len(issues) == 0, issues)


def _collect_local_includes(cpp_file, project_root):
    """Collect all local #include "..." files recursively.

    Returns:
        Set of Path objects for all included files
    """
    import re

    collected = set()
    to_process = [cpp_file]
    processed = set()

    while to_process:
        current = to_process.pop()
        if current in processed:
            continue
        processed.add(current)

        try:
            with open(current, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Find local includes (with quotes, not angle brackets)
            includes = re.findall(r'#include\s*"([^"]+)"', content)

            for inc in includes:
                # Try to resolve relative to current file's directory
                inc_path = current.parent / inc
                if not inc_path.exists():
                    # Try relative to project root
                    inc_path = project_root / inc
                if not inc_path.exists():
                    # Try include/ directory
                    inc_path = project_root / 'include' / inc

                if inc_path.exists() and inc_path not in collected:
                    collected.add(inc_path)
                    to_process.append(inc_path)

        except Exception:
            pass

    return collected


def _parse_cp_dependencies(cp_file):
    """Parse DEPENDS() from a .cp file.

    Returns:
        List of dependency module names
    """
    import re

    try:
        content = cp_file.read_text()
        match = re.search(r'DEPENDS\s*\(([^)]+)\)', content)
        if match:
            deps_str = match.group(1)
            return [d.strip() for d in deps_str.split(',') if d.strip()]
    except Exception:
        pass

    return []


@cli.command()
@click.option('--python', 'include_python', is_flag=True, help='Include a Python wrapper file')
@click.argument('module_name')
@click.argument('author')
@click.argument('version')
@click.argument('python_file', required=False)
def upload(include_python, module_name, author, version, python_file):
    """Upload a module to the community repository.

    Example:
        includecpp upload mymodule MyName 1.0.0
        includecpp upload --python solarsystem solar 1.0.0 system.py

    Security checks are performed automatically:
    - API key/secret detection (blocks upload)
    - Content filtering
    - All local includes are bundled

    With --python, the Python file is installed to the project root on 'includecpp install'.
    """
    import urllib.request
    import urllib.error
    import json
    import base64
    import re

    click.echo("=" * 60)
    click.secho(f"Uploading Module: {module_name}", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo(f"  Author:  {author}")
    click.echo(f"  Version: {version}")
    click.echo()

    # Validate version format
    if not re.match(r'^\d+\.\d+(\.\d+)?$', version):
        click.secho("ERROR: Invalid version format. Use: X.Y or X.Y.Z", fg='red', err=True)
        return

    # Check project structure
    project_root = Path.cwd()
    plugins_dir = project_root / 'plugins'
    include_dir = project_root / 'include'

    cp_file = plugins_dir / f'{module_name}.cp'
    if not cp_file.exists():
        click.secho(f"ERROR: Plugin file not found: {cp_file}", fg='red', err=True)
        click.echo("Run 'includecpp plugin' first to create the .cp file.")
        return

    click.echo("[1/5] Collecting files...")

    # Parse the .cp file for source files
    source_files, header_files = _parse_cp_sources(cp_file)

    if not source_files:
        click.secho("ERROR: No source files found in .cp file.", fg='red', err=True)
        return

    # Collect all files to upload
    files_to_upload = [cp_file]
    files_to_upload.extend(source_files)
    files_to_upload.extend(header_files)

    # Collect local includes from all source files
    for src in source_files:
        local_includes = _collect_local_includes(src, project_root)
        files_to_upload.extend(local_includes)

    # Remove duplicates
    files_to_upload = list(set(files_to_upload))

    # Add Python file if --python flag is set
    python_file_path = None
    if include_python:
        if not python_file:
            click.secho("ERROR: --python requires a Python file argument.", fg='red', err=True)
            click.echo("Usage: includecpp upload --python <module> <author> <version> <file.py>")
            return
        python_file_path = Path(python_file)
        if not python_file_path.exists():
            click.secho(f"ERROR: Python file not found: {python_file}", fg='red', err=True)
            return
        files_to_upload.append(python_file_path)
        click.secho(f"  Including Python wrapper: {python_file_path.name}", fg='cyan')
    elif python_file:
        click.secho("ERROR: Python file provided but --python flag not set.", fg='red', err=True)
        click.echo("Usage: includecpp upload --python <module> <author> <version> <file.py>")
        return

    click.echo(f"  Found {len(files_to_upload)} file(s) to upload")
    for f in files_to_upload:
        suffix = " (Python wrapper)" if python_file_path and f == python_file_path else ""
        click.echo(f"    {_BULLET} {f.name}{suffix}")
    click.echo()

    # Security scan
    click.echo("[2/5] Security scan...")
    all_issues = []

    for filepath in files_to_upload:
        is_safe, issues = _scan_file_security(filepath)
        if not is_safe:
            all_issues.extend(issues)

    if all_issues:
        click.secho("SECURITY CHECK FAILED", fg='red', bold=True, err=True)
        click.echo()
        for issue in all_issues:
            click.secho(f"  {_BULLET} {issue}", fg='red')
        click.echo()
        click.secho("Upload blocked. Remove sensitive content and try again.", fg='red', err=True)
        return

    click.secho("  Security check passed", fg='green')
    click.echo()

    # Check if module already exists and compare versions
    click.echo("[3/5] Checking for existing module...")

    api_base = "https://api.github.com/repos/liliassg/IncludeCPP/contents/minstall"
    headers = {
        "Authorization": f"Bearer {_GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "IncludeCPP-CLI"
    }

    existing_version = None
    existing_sha = {}

    try:
        # Check if module directory exists
        req = urllib.request.Request(f"{api_base}/{module_name}", headers=headers)
        with urllib.request.urlopen(req) as response:
            existing_files = json.loads(response.read())

            # Look for version file or parse from existing metadata
            for f in existing_files:
                existing_sha[f['name']] = f['sha']
                if f['name'] == 'VERSION':
                    # Fetch version content
                    ver_req = urllib.request.Request(f['download_url'])
                    with urllib.request.urlopen(ver_req) as ver_resp:
                        existing_version = ver_resp.read().decode().strip()

        if existing_version:
            click.echo(f"  Existing version: {existing_version}")

            # Compare versions
            def parse_ver(v):
                return tuple(int(x) for x in v.split('.'))

            try:
                if parse_ver(version) <= parse_ver(existing_version):
                    click.secho(f"ERROR: Version {version} must be higher than existing {existing_version}", fg='red', err=True)
                    return
            except ValueError:
                pass  # Continue if version parsing fails

            click.secho(f"  Upgrading: {existing_version} -> {version}", fg='yellow')
        else:
            click.echo("  Module exists but no version found, will overwrite")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            click.secho("  New module (first upload)", fg='green')
        else:
            click.secho(f"  Warning: Could not check existing module (HTTP {e.code})", fg='yellow')
    except Exception as e:
        click.secho(f"  Warning: Could not check existing module ({e})", fg='yellow')

    click.echo()

    # Parse dependencies
    dependencies = _parse_cp_dependencies(cp_file)
    if dependencies:
        click.echo(f"  Dependencies: {', '.join(dependencies)}")

    # Upload files
    click.echo("[4/5] Uploading to GitHub...")

    uploaded = 0
    failed = 0

    for filepath in files_to_upload:
        try:
            # Read file content
            with open(filepath, 'rb') as f:
                content = base64.b64encode(f.read()).decode()

            # Determine target path in repo
            # Python files are renamed to {module_name}.py for install compatibility
            if python_file_path and filepath == python_file_path:
                filename = f"{module_name}.py"
            else:
                filename = filepath.name
            target_path = f"minstall/{module_name}/{filename}"

            # Prepare request
            upload_data = {
                "message": f"Upload {module_name}/{filename} v{version} by {author}",
                "content": content,
                "branch": "main"
            }

            # If file exists, include SHA for update
            if filename in existing_sha:
                upload_data["sha"] = existing_sha[filename]

            req = urllib.request.Request(
                f"https://api.github.com/repos/liliassg/IncludeCPP/contents/{target_path}",
                data=json.dumps(upload_data).encode(),
                headers={**headers, "Content-Type": "application/json"},
                method="PUT"
            )

            click.echo(f"  Uploading {filename}...", nl=False)
            with urllib.request.urlopen(req) as response:
                click.secho(" OK", fg='green')
                uploaded += 1

        except urllib.error.HTTPError as e:
            click.secho(f" FAILED (HTTP {e.code})", fg='red')
            failed += 1
        except Exception as e:
            click.secho(f" FAILED ({e})", fg='red')
            failed += 1

    # Upload VERSION file
    upload_warnings = []
    try:
        version_content = base64.b64encode(version.encode()).decode()
        version_data = {
            "message": f"Update VERSION for {module_name} to {version}",
            "content": version_content,
            "branch": "main"
        }
        if 'VERSION' in existing_sha:
            version_data["sha"] = existing_sha['VERSION']

        req = urllib.request.Request(
            f"https://api.github.com/repos/liliassg/IncludeCPP/contents/minstall/{module_name}/VERSION",
            data=json.dumps(version_data).encode(),
            headers={**headers, "Content-Type": "application/json"},
            method="PUT"
        )
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        upload_warnings.append(f"VERSION: {e}")

    # Upload metadata
    try:
        metadata = {
            "name": module_name,
            "author": author,
            "version": version,
            "dependencies": dependencies,
            "files": [f.name for f in files_to_upload]
        }
        meta_content = base64.b64encode(json.dumps(metadata, indent=2).encode()).decode()
        meta_data = {
            "message": f"Update metadata for {module_name} v{version}",
            "content": meta_content,
            "branch": "main"
        }
        if 'metadata.json' in existing_sha:
            meta_data["sha"] = existing_sha['metadata.json']

        req = urllib.request.Request(
            f"https://api.github.com/repos/liliassg/IncludeCPP/contents/minstall/{module_name}/metadata.json",
            data=json.dumps(meta_data).encode(),
            headers={**headers, "Content-Type": "application/json"},
            method="PUT"
        )
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        upload_warnings.append(f"metadata.json: {e}")

    click.echo()
    click.echo("[5/5] Complete!")
    click.echo()

    if upload_warnings:
        click.secho("Warnings:", fg='yellow')
        for warn in upload_warnings:
            click.echo(f"  {_BULLET} {warn}")
        click.echo()

    if failed == 0:
        click.secho(f"Successfully uploaded {module_name} v{version}!", fg='green', bold=True)
        click.echo()
        click.echo("Users can install with:")
        click.echo(f"  includecpp install {module_name}")
    else:
        click.secho(f"Uploaded {uploaded} file(s), {failed} failed.", fg='yellow')

    click.echo("=" * 60)


# Compiler detection cache
_compiler_cache = None

def detect_compiler(force_refresh=False):
    """Detect available C++ compiler with caching.

    Checks g++ first per user requirement, then clang++, then cl (MSVC).
    Results are cached to avoid repeated PATH scans.
    """
    global _compiler_cache

    if not force_refresh and _compiler_cache is not None:
        return _compiler_cache

    # g++ first (user requirement)
    for compiler in ['g++', 'clang++', 'cl']:
        if shutil.which(compiler):
            _compiler_cache = compiler.replace('++', '').replace('cl', 'msvc')
            return _compiler_cache

    _compiler_cache = 'gcc'
    return _compiler_cache


@cli.command()
@click.argument('plugin_name', required=False)
@click.option('--all', 'all_plugins', is_flag=True, help='Process all plugins in plugins/')
@click.option('--exclude', '-x', multiple=True, help='Exclude specific plugins (can be used multiple times)')
@click.option('--fast', 'fast_mode', is_flag=True, help='Use fast incremental build after regeneration')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('--auto-ai', 'auto_ai', is_flag=True, help='Auto-fix build errors with AI and retry')
@click.option('--think2', 'think_twice', is_flag=True, help='With --auto-ai: extended context (500 lines per file)')
@click.option('--think3', 'think_three', is_flag=True, help='With --auto-ai: max context + web research + planning (requires Brave API)')
def auto(plugin_name, all_plugins, exclude, fast_mode, verbose, auto_ai, think_twice, think_three):
    """Regenerate .cp file and build in one step.

    Scans the C++ source files, regenerates the plugin definition,
    then builds the module.

    Examples:
      includecpp auto stress          # Regenerate + default build
      includecpp auto stress --fast   # Regenerate + fast build
      includecpp auto stress --auto-ai  # With AI auto-fix on build errors
      includecpp auto --all           # Process all plugins
      includecpp auto --all -x noise  # All except noise
      includecpp auto --all --exclude noise --exclude debug
    """
    from pathlib import Path

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"

    if not plugins_dir.exists():
        click.secho("Error: plugins/ directory not found. Run: includecpp init", fg='red', err=True)
        raise click.Abort()

    # Determine which plugins to process
    if all_plugins:
        cp_files = list(plugins_dir.glob("*.cp"))
        if not cp_files:
            click.secho("No .cp files found in plugins/", fg='yellow')
            return
        plugin_names = [f.stem for f in cp_files]
        # Apply exclusions
        exclude_set = {e.replace('.cp', '') for e in exclude}
        plugin_names = [p for p in plugin_names if p not in exclude_set]
        if not plugin_names:
            click.secho("All plugins excluded, nothing to process", fg='yellow')
            return
    elif plugin_name:
        # Single plugin mode
        if plugin_name.endswith('.cp'):
            plugin_name = plugin_name[:-3]
        plugin_name = Path(plugin_name).stem
        plugin_names = [plugin_name]
    else:
        click.secho("Error: Specify a plugin name or use --all", fg='red', err=True)
        raise click.Abort()

    # Validate all plugins exist
    for pname in plugin_names:
        existing_cp = plugins_dir / f"{pname}.cp"
        if not existing_cp.exists():
            click.secho(f"Error: {pname}.cp not found in plugins/", fg='red', err=True)
            click.echo(f"Create it first: includecpp plugin {pname} include/{pname}.cpp")
            raise click.Abort()

    click.secho("Using cached generator. Build error? -> includecpp build --clean", fg='yellow')

    from click.testing import CliRunner
    runner = CliRunner()

    total = len(plugin_names)
    failed = []

    for idx, pname in enumerate(plugin_names, 1):
        existing_cp = plugins_dir / f"{pname}.cp"

        # Step 1: Regenerate .cp file
        click.echo(f"\n[{idx}/{total}] Regenerating {pname}.cp...")
        try:
            result = runner.invoke(plugin, [pname])
            if result.exit_code != 0:
                click.secho(f"Error regenerating {pname}.cp", fg='red', err=True)
                if result.output:
                    click.echo(result.output)
                failed.append(pname)
                continue
            if verbose and result.output:
                click.echo(result.output)
            click.secho(f"  Regenerated: {existing_cp.name}", fg='green')
        except Exception as e:
            click.secho(f"Error: {e}", fg='red', err=True)
            failed.append(pname)
            continue

        # Step 2: Build
        click.echo(f"  Building {pname}...")
        if fast_mode:
            build_args = ['--fast', pname]
        else:
            build_args = ['--keep', '-m', pname]
        if verbose:
            build_args.append('--verbose')
        if auto_ai:
            build_args.append('--auto-ai')
        if think_twice:
            build_args.append('--think2')
        if think_three:
            build_args.append('--think3')

        try:
            result = runner.invoke(rebuild, build_args)
            if result.exit_code != 0:
                if 'generator' in result.output.lower() or 'plugin_gen' in result.output.lower():
                    click.secho("\nBuild failed - generator may be outdated.", fg='yellow')
                    click.echo("Try: includecpp build --clean")
                if result.output:
                    click.echo(result.output)
                failed.append(pname)
                continue
            if result.output:
                click.echo(result.output)
            click.secho(f"  Built: {pname}", fg='green')
        except Exception as e:
            click.secho(f"Build error: {e}", fg='red', err=True)
            failed.append(pname)
            continue

    # Summary
    if total > 1:
        click.echo(f"\n{'='*40}")
        succeeded = total - len(failed)
        click.secho(f"Completed: {succeeded}/{total} plugins", fg='green' if not failed else 'yellow')
        if failed:
            click.secho(f"Failed: {', '.join(failed)}", fg='red')


def _show_diff_view(original_content: str, new_content: str, file_path: str):
    """Show colored diff with 6 lines context around changes.

    Colors:
    - Green (+): New lines
    - Red (-): Removed lines
    - Yellow (~): Modified (shown as remove old + add new)
    - Default: Context lines
    """
    import difflib
    import re

    original_lines = original_content.split('\n')
    new_lines = new_content.split('\n')

    diff = list(difflib.unified_diff(original_lines, new_lines, lineterm='', n=6))

    if len(diff) < 3:
        click.echo(click.style("  No changes detected.", fg='yellow'))
        return

    click.echo(f"\n{'='*60}")
    click.echo(click.style(f"Changes: {file_path}", fg='cyan', bold=True))
    click.echo(f"{'='*60}")

    line_num_old = 0
    line_num_new = 0

    for line in diff[2:]:
        if line.startswith('@@'):
            match = re.search(r'@@ -(\d+)', line)
            if match:
                line_num_old = int(match.group(1)) - 1
            match = re.search(r'\+(\d+)', line)
            if match:
                line_num_new = int(match.group(1)) - 1
            click.echo(click.style(f"  {'-'*54}", fg='white', dim=True))
            continue

        content = line[1:] if len(line) > 0 else ''

        if line.startswith('-'):
            line_num_old += 1
            click.echo(click.style(f"-{line_num_old:4} | {content}", fg='red'))
        elif line.startswith('+'):
            line_num_new += 1
            click.echo(click.style(f"+{line_num_new:4} | {content}", fg='green'))
        else:
            line_num_old += 1
            line_num_new += 1
            click.echo(f" {line_num_new:4} | {content}")

    click.echo(f"{'='*60}\n")


def _show_all_diffs(changes: list, source_files: dict, project_root):
    """Show diffs for all changes before confirmation."""
    from pathlib import Path

    for change in changes:
        file_path = change['file']
        full_path = None

        if Path(file_path).is_absolute():
            full_path = Path(file_path)
        else:
            for orig_path in source_files.keys():
                if Path(orig_path).name == Path(file_path).name:
                    full_path = Path(orig_path)
                    break
            if not full_path:
                full_path = project_root / file_path.lstrip('/\\')

        original = ''
        if full_path and full_path.exists():
            try:
                original = full_path.read_text(encoding='utf-8')
            except:
                original = ''

        _show_diff_view(original, change['content'], str(full_path))


@cli.command()
@click.argument('module_name', required=False)
@click.option('--all', 'all_modules', is_flag=True, help='Check all modules')
@click.option('--exclude', '-x', multiple=True, help='Exclude specific modules')
@click.option('--undo', is_flag=True, help='Undo last fix changes')
@click.option('--confirm', 'auto_fix', is_flag=True, help='Skip confirmation, apply changes directly')
@click.option('-v', '--verbose', is_flag=True, help='Show detailed analysis')
@click.option('--ai', 'use_ai', is_flag=True, help='Use AI for enhanced analysis')
def fix(module_name, all_modules, exclude, undo, auto_fix, verbose, use_ai):
    """Analyze and fix common C++ issues in your modules.

    Examples:
      includecpp fix math              # Fix specific module
      includecpp fix --all             # Fix all modules
      includecpp fix --all -x noise    # All except noise
      includecpp fix --undo            # Revert last fix
      includecpp fix math --confirm    # Apply fixes without asking
    """
    from pathlib import Path
    import re
    import json
    import shutil
    from collections import defaultdict

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"
    include_dir = project_root / "include"
    cache_dir = Path.home() / ".includecpp" / "fix_cache" / project_root.name

    if not plugins_dir.exists():
        click.secho("Error: plugins/ directory not found. Run: includecpp init", fg='red', err=True)
        return

    # Handle --undo
    if undo:
        if not cache_dir.exists():
            click.secho("No fix cache found. Nothing to undo.", fg='yellow')
            return
        cache_manifest = cache_dir / "manifest.json"
        if not cache_manifest.exists():
            click.secho("No fix cache manifest found.", fg='yellow')
            return
        try:
            manifest = json.loads(cache_manifest.read_text())
            restored = 0
            for entry in manifest.get("files", []):
                cached_file = cache_dir / entry["cached"]
                original_path = Path(entry["original"])
                if cached_file.exists():
                    shutil.copy2(cached_file, original_path)
                    click.echo(f"  Restored: {original_path.name}")
                    restored += 1
            shutil.rmtree(cache_dir)
            click.secho(f"\nUndo complete: {restored} file(s) restored", fg='green')
        except Exception as e:
            click.secho(f"Error during undo: {e}", fg='red', err=True)
        return

    if use_ai:
        from ..core.ai_integration import get_ai_manager
        ai_mgr = get_ai_manager()
        if not ai_mgr.is_enabled():
            if not ai_mgr.has_key():
                click.secho("AI not configured. Use: includecpp ai key <YOUR_API_KEY>", fg='red', err=True)
            else:
                click.secho("AI is disabled. Use: includecpp ai enable", fg='red', err=True)
            return

    # Determine which modules to check
    if all_modules:
        cp_files = list(plugins_dir.glob("*.cp"))
        if not cp_files:
            click.secho("No .cp files found in plugins/", fg='yellow')
            return
        module_names = [f.stem for f in cp_files]
        exclude_set = {e.replace('.cp', '') for e in exclude}
        module_names = [m for m in module_names if m not in exclude_set]
    elif module_name:
        if module_name.endswith('.cp'):
            module_name = module_name[:-3]
        module_names = [Path(module_name).stem]
    else:
        click.secho("Error: Specify a module name or use --all", fg='red', err=True)
        return

    # Issue tracking
    class Issue:
        def __init__(self, severity, category, file_path, line, code, message, suggestion=None, auto_fixable=False, fix_func=None):
            self.severity = severity  # 'error', 'warning', 'info'
            self.category = category  # Category name
            self.file_path = file_path
            self.line = line
            self.code = code  # Issue code like N001, D002
            self.message = message
            self.suggestion = suggestion
            self.auto_fixable = auto_fixable
            self.fix_func = fix_func

    all_issues = []
    files_to_backup = set()

    def add_issue(severity, category, file_path, line, code, message, suggestion=None, auto_fixable=False, fix_func=None):
        all_issues.append(Issue(severity, category, file_path, line, code, message, suggestion, auto_fixable, fix_func))
        if auto_fixable and fix_func:
            files_to_backup.add(str(file_path))

    # Helper to strip comments and strings for analysis
    def strip_comments_strings(content):
        # Remove single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove strings
        content = re.sub(r'"(?:[^"\\]|\\.)*"', '""', content)
        content = re.sub(r"'(?:[^'\\]|\\.)*'", "''", content)
        return content

    # =========================================================================
    # CATEGORY 1: NAMESPACE CHECKS (N001-N010)
    # =========================================================================
    def check_namespace_issues(file_path, content):
        lines = content.split('\n')
        clean_content = strip_comments_strings(content)

        # N001: Missing namespace includecpp
        if 'namespace includecpp' not in content:
            add_issue('error', 'Namespace', file_path, 1, 'N001',
                      "Missing 'namespace includecpp'",
                      "Wrap your code in: namespace includecpp { ... }")

        # N002: Wrong namespace name (typos)
        typos = ['namespace includeCpp', 'namespace include_cpp', 'namespace IncludeCpp',
                 'namespace INCLUDECPP', 'namespace Includecpp']
        for typo in typos:
            if typo in content:
                line_num = next((i+1 for i, l in enumerate(lines) if typo in l), 1)
                add_issue('error', 'Namespace', file_path, line_num, 'N002',
                          f"Wrong namespace name: '{typo.split()[1]}'",
                          "Use 'namespace includecpp' (lowercase)")

        # N003: Nested namespace issues
        ns_count = clean_content.count('namespace includecpp')
        if ns_count > 1:
            add_issue('warning', 'Namespace', file_path, 1, 'N003',
                      f"Multiple namespace includecpp declarations ({ns_count})",
                      "Use single namespace block or nested namespace syntax")

        # N004: Anonymous namespace in public code
        if 'namespace {' in clean_content or 'namespace{' in clean_content:
            line_num = next((i+1 for i, l in enumerate(lines) if 'namespace {' in l or 'namespace{' in l), 1)
            add_issue('warning', 'Namespace', file_path, line_num, 'N004',
                      "Anonymous namespace found",
                      "Anonymous namespaces create internal linkage - may cause issues with bindings")

        # N005: using namespace in header files
        if file_path.suffix in ('.h', '.hpp'):
            if 'using namespace' in content:
                line_num = next((i+1 for i, l in enumerate(lines) if 'using namespace' in l), 1)
                add_issue('warning', 'Namespace', file_path, line_num, 'N005',
                          "'using namespace' in header file",
                          "Avoid 'using namespace' in headers - pollutes global namespace")

        # N006: Namespace not closed properly (brace mismatch in namespace block)
        ns_match = re.search(r'namespace\s+includecpp\s*\{', content)
        if ns_match:
            ns_start = ns_match.end()
            brace_count = 1
            for i, char in enumerate(content[ns_start:]):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                if brace_count == 0:
                    break
            if brace_count != 0:
                add_issue('error', 'Namespace', file_path, len(lines), 'N006',
                          f"Namespace not closed properly (brace imbalance: {brace_count})",
                          "Check for missing '}' to close namespace includecpp")

        # N007: Code before namespace includecpp (excluding includes/pragmas)
        ns_match = re.search(r'namespace\s+includecpp\s*\{', content)
        if ns_match:
            before_ns = content[:ns_match.start()]
            # Remove preprocessor directives, comments, empty lines
            code_before = re.sub(r'#.*$', '', before_ns, flags=re.MULTILINE)
            code_before = strip_comments_strings(code_before).strip()
            if code_before:
                add_issue('warning', 'Namespace', file_path, 1, 'N007',
                          "Code found before namespace includecpp",
                          "Move all code inside namespace includecpp")

    # =========================================================================
    # CATEGORY 2: DUPLICATE DECLARATIONS (D001-D015)
    # =========================================================================
    def check_duplicate_declarations(all_files_content):
        declarations = defaultdict(list)  # name -> [(file, line, type), ...]

        # Patterns for different declaration types
        patterns = {
            'function': re.compile(
                r'(?:(?:inline|static|extern|constexpr|virtual)\s+)*'
                r'(?:const\s+)?'
                r'([a-zA-Z_][\w:]*(?:<[^>]+>)?(?:\s*[&*])?)\s+'
                r'([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*(?:const|override|final|noexcept|\s)*\{',
                re.MULTILINE
            ),
            'class': re.compile(r'\bclass\s+([a-zA-Z_]\w*)\s*(?:final\s*)?[:{]', re.MULTILINE),
            'struct': re.compile(r'\bstruct\s+([a-zA-Z_]\w*)\s*(?:final\s*)?[:{]', re.MULTILINE),
            'enum': re.compile(r'\benum\s+(?:class\s+)?([a-zA-Z_]\w*)\s*(?::\s*\w+\s*)?\{', re.MULTILINE),
            'typedef': re.compile(r'\btypedef\s+.+?\s+([a-zA-Z_]\w*)\s*;', re.MULTILINE),
            'using_type': re.compile(r'\busing\s+([a-zA-Z_]\w*)\s*=', re.MULTILINE),
            'global_var': re.compile(r'^(?!.*(?:static|const|constexpr))([a-zA-Z_][\w:]*(?:<[^>]+>)?(?:\s*[&*])?)\s+([a-zA-Z_]\w*)\s*[=;]', re.MULTILINE),
            'const_var': re.compile(r'\bconst\s+([a-zA-Z_][\w:]*)\s+([a-zA-Z_]\w*)\s*=', re.MULTILINE),
            'constexpr_var': re.compile(r'\bconstexpr\s+([a-zA-Z_][\w:]*)\s+([a-zA-Z_]\w*)\s*=', re.MULTILINE),
            'macro': re.compile(r'^\s*#define\s+([a-zA-Z_]\w*)', re.MULTILINE),
        }

        for file_path, content in all_files_content.items():
            clean = strip_comments_strings(content)
            fp = Path(file_path)

            # Check functions
            for match in patterns['function'].finditer(clean):
                name = match.group(2)
                if name in ('if', 'for', 'while', 'switch', 'catch', 'return', 'sizeof', 'alignof'):
                    continue
                params = match.group(3).strip()
                line_num = content[:match.start()].count('\n') + 1
                sig = f"{name}({params})"
                declarations[('func', name)].append((file_path, line_num, sig))

            # Check classes, structs, enums
            for dtype, pattern in [('class', 'class'), ('struct', 'struct'), ('enum', 'enum')]:
                for match in patterns[dtype].finditer(clean):
                    name = match.group(1)
                    line_num = content[:match.start()].count('\n') + 1
                    declarations[(dtype, name)].append((file_path, line_num, dtype))

            # Check typedefs and using
            for match in patterns['typedef'].finditer(clean):
                name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                declarations[('typedef', name)].append((file_path, line_num, 'typedef'))

            for match in patterns['using_type'].finditer(clean):
                name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                declarations[('using', name)].append((file_path, line_num, 'using'))

            # Check macros
            for match in patterns['macro'].finditer(content):  # Don't strip for macros
                name = match.group(1)
                if name.startswith('_') or name in ('NULL', 'TRUE', 'FALSE'):
                    continue
                line_num = content[:match.start()].count('\n') + 1
                declarations[('macro', name)].append((file_path, line_num, 'macro'))

        # Report duplicates
        code_map = {'func': 'D001', 'class': 'D002', 'struct': 'D003', 'enum': 'D004',
                    'typedef': 'D005', 'using': 'D006', 'macro': 'D010'}

        for (dtype, name), locations in declarations.items():
            if len(locations) > 1:
                unique_files = set(loc[0] for loc in locations)
                if len(unique_files) > 1:
                    first_file, first_line, first_type = locations[0]
                    code = code_map.get(dtype, 'D001')
                    for other_file, other_line, other_type in locations[1:]:
                        add_issue('error', 'Duplicate', Path(other_file), other_line, code,
                                  f"Duplicate {dtype}: '{name}'",
                                  f"Already defined in {Path(first_file).name}:{first_line}. "
                                  f"Use 'inline' keyword or move to common header.")

    # =========================================================================
    # CATEGORY 3: SYNTAX ERRORS (S001-S020)
    # =========================================================================
    def check_syntax_errors(file_path, content):
        lines = content.split('\n')
        clean = strip_comments_strings(content)

        # S001-S004: Bracket balance
        brackets = [
            ('{', '}', 'braces', 'S001'),
            ('(', ')', 'parentheses', 'S002'),
            ('[', ']', 'brackets', 'S003'),
            ('<', '>', 'angle brackets', 'S004'),
        ]

        for open_b, close_b, name, code in brackets:
            if name == 'angle brackets':
                # Skip angle brackets in non-template context
                template_content = re.findall(r'template\s*<[^>]*>|<[^<>]*>', clean)
                count = sum(s.count('<') - s.count('>') for s in template_content)
            else:
                count = clean.count(open_b) - clean.count(close_b)

            if count != 0 and name != 'angle brackets':
                # Find approximate location
                running = 0
                error_line = len(lines)
                for i, line in enumerate(lines, 1):
                    line_clean = strip_comments_strings(line)
                    running += line_clean.count(open_b) - line_clean.count(close_b)
                    if (count > 0 and running > count) or (count < 0 and running < 0):
                        error_line = i
                        break
                add_issue('error', 'Syntax', file_path, error_line, code,
                          f"Unmatched {name}: {'+' if count > 0 else ''}{count}",
                          f"Check for missing '{open_b}' or '{close_b}'")

        # S005: Missing semicolon after class/struct
        class_struct_pattern = re.compile(r'\b(class|struct)\s+(\w+)[^;{]*\{')
        for match in class_struct_pattern.finditer(clean):
            start = match.end()
            brace_count = 1
            for i, char in enumerate(clean[start:]):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                if brace_count == 0:
                    end_pos = start + i + 1
                    if end_pos < len(clean) and clean[end_pos:end_pos+1] not in (';', '\n'):
                        # Check if next non-whitespace is semicolon
                        rest = clean[end_pos:].lstrip()
                        if not rest.startswith(';'):
                            line_num = content[:match.start()].count('\n') + 1
                            add_issue('error', 'Syntax', file_path, line_num, 'S005',
                                      f"Missing semicolon after {match.group(1)} '{match.group(2)}'",
                                      "Add ';' after closing brace")
                    break

        # S006: Missing semicolon after enum
        enum_pattern = re.compile(r'\benum\s+(?:class\s+)?(\w+)[^{]*\{')
        for match in enum_pattern.finditer(clean):
            start = match.end()
            brace_count = 1
            for i, char in enumerate(clean[start:]):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                if brace_count == 0:
                    end_pos = start + i + 1
                    rest = clean[end_pos:].lstrip()
                    if not rest.startswith(';'):
                        line_num = content[:match.start()].count('\n') + 1
                        add_issue('error', 'Syntax', file_path, line_num, 'S006',
                                  f"Missing semicolon after enum '{match.group(1)}'",
                                  "Add ';' after closing brace")
                    break

        # S007: Double semicolons (suspicious)
        for i, line in enumerate(lines, 1):
            if ';;' in strip_comments_strings(line):
                add_issue('info', 'Syntax', file_path, i, 'S007',
                          "Double semicolon found",
                          "This may be intentional but often indicates a typo")

        # S008: Missing return in non-void function
        func_pattern = re.compile(
            r'(?<!void\s)(?:int|float|double|bool|char|auto|[A-Z]\w*)\s+(\w+)\s*\([^)]*\)\s*(?:const\s*)?\{([^}]*)\}',
            re.DOTALL
        )
        for match in func_pattern.finditer(clean):
            body = match.group(2)
            if 'return' not in body and '{' not in body:  # Simple function without nested blocks
                line_num = content[:match.start()].count('\n') + 1
                add_issue('warning', 'Syntax', file_path, line_num, 'S008',
                          f"Function '{match.group(1)}' may be missing return statement",
                          "Non-void functions should have a return statement")

        # S009: Unclosed multi-line comment
        if '/*' in content:
            opens = [m.start() for m in re.finditer(r'/\*', content)]
            closes = [m.start() for m in re.finditer(r'\*/', content)]
            if len(opens) > len(closes):
                line_num = content[:opens[-1]].count('\n') + 1
                add_issue('error', 'Syntax', file_path, line_num, 'S009',
                          "Unclosed multi-line comment",
                          "Missing '*/' to close comment")

        # S010: Unclosed string literal (basic check)
        for i, line in enumerate(lines, 1):
            # Skip preprocessor and comments
            if line.strip().startswith('#') or line.strip().startswith('//'):
                continue
            # Count unescaped quotes
            in_char = False
            quote_count = 0
            j = 0
            while j < len(line):
                if line[j] == '\\' and j + 1 < len(line):
                    j += 2
                    continue
                if line[j] == "'" and not in_char:
                    in_char = True
                elif line[j] == "'" and in_char:
                    in_char = False
                elif line[j] == '"' and not in_char:
                    quote_count += 1
                j += 1
            if quote_count % 2 != 0:
                add_issue('error', 'Syntax', file_path, i, 'S010',
                          "Possible unclosed string literal",
                          "Check for missing closing quote")

    # =========================================================================
    # CATEGORY 4: TYPE ERRORS (T001-T015)
    # =========================================================================
    def check_type_errors(file_path, content):
        lines = content.split('\n')
        clean = strip_comments_strings(content)

        # T001: void pointer arithmetic
        if 'void*' in clean or 'void *' in clean:
            for i, line in enumerate(lines, 1):
                if re.search(r'\bvoid\s*\*\s*\w+\s*[+\-]', line):
                    add_issue('error', 'Type', file_path, i, 'T001',
                              "Arithmetic on void pointer",
                              "void* has no size - cast to appropriate pointer type first")

        # T002: Implicit narrowing conversion warnings
        narrowing_patterns = [
            (r'\bint\s+\w+\s*=\s*\d+\.\d+', "float/double to int"),
            (r'\bchar\s+\w+\s*=\s*\d{3,}', "large integer to char"),
            (r'\bshort\s+\w+\s*=\s*\d{6,}', "large integer to short"),
        ]
        for pattern, conv_type in narrowing_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, strip_comments_strings(line)):
                    add_issue('warning', 'Type', file_path, i, 'T002',
                              f"Implicit narrowing conversion: {conv_type}",
                              "Use explicit cast or appropriate type")

        # T003: Comparison of signed/unsigned
        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)
            if re.search(r'\bunsigned\b.*[<>=!]=?.*-\d+|\b-\d+.*[<>=!]=?.*\bunsigned\b', line_clean):
                add_issue('warning', 'Type', file_path, i, 'T003',
                          "Comparison of signed and unsigned integers",
                          "This may cause unexpected results - use consistent types")

        # T004: Float equality comparison
        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)
            if re.search(r'\b(float|double)\b.*==|\b==.*\b(float|double)\b', line_clean):
                if 'nullptr' not in line_clean and 'NULL' not in line_clean:
                    add_issue('warning', 'Type', file_path, i, 'T004',
                              "Direct floating-point equality comparison",
                              "Use epsilon comparison: std::abs(a - b) < epsilon")

        # T005: C-style cast
        c_cast_pattern = re.compile(r'\(\s*(int|float|double|char|void|long|short|unsigned)\s*\*?\s*\)')
        for i, line in enumerate(lines, 1):
            if c_cast_pattern.search(strip_comments_strings(line)):
                add_issue('info', 'Type', file_path, i, 'T005',
                          "C-style cast detected",
                          "Consider using static_cast, reinterpret_cast, or const_cast")

    # =========================================================================
    # CATEGORY 5: MEMORY & RESOURCE ISSUES (M001-M010)
    # =========================================================================
    def check_memory_issues(file_path, content):
        lines = content.split('\n')
        clean = strip_comments_strings(content)

        # M001: new without delete (basic check within function scope)
        func_pattern = re.compile(r'(\w+)\s*\([^)]*\)\s*(?:const\s*)?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', re.DOTALL)
        for match in func_pattern.finditer(clean):
            body = match.group(2)
            news = len(re.findall(r'\bnew\s+', body))
            deletes = len(re.findall(r'\bdelete\s+', body))
            if news > deletes:
                line_num = content[:match.start()].count('\n') + 1
                add_issue('warning', 'Memory', file_path, line_num, 'M001',
                          f"Potential memory leak in '{match.group(1)}'",
                          f"Found {news} 'new' but only {deletes} 'delete'. Consider smart pointers.")

        # M002: Missing virtual destructor
        class_pattern = re.compile(r'\bclass\s+(\w+)[^{]*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', re.DOTALL)
        for match in class_pattern.finditer(clean):
            class_name = match.group(1)
            class_body = match.group(2)
            has_virtual = 'virtual' in class_body
            has_virtual_dtor = re.search(r'virtual\s+~' + class_name, class_body)
            if has_virtual and not has_virtual_dtor:
                line_num = content[:match.start()].count('\n') + 1
                add_issue('warning', 'Memory', file_path, line_num, 'M002',
                          f"Class '{class_name}' has virtual methods but no virtual destructor",
                          f"Add: virtual ~{class_name}() = default;")

        # M003: delete[] vs delete mismatch
        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)
            # Check for new[] with potential wrong delete
            if 'new' in line_clean and '[' in line_clean and 'delete' in line_clean:
                if 'delete[' not in line_clean and 'delete [' not in line_clean:
                    add_issue('warning', 'Memory', file_path, i, 'M003',
                              "Possible delete/delete[] mismatch",
                              "Arrays allocated with new[] must be freed with delete[]")

        # M004: Raw pointer member without clear ownership
        for i, line in enumerate(lines, 1):
            if re.search(r'\b\w+\s*\*\s+m_\w+\s*;', strip_comments_strings(line)):
                add_issue('info', 'Memory', file_path, i, 'M004',
                          "Raw pointer member variable",
                          "Consider std::unique_ptr or std::shared_ptr for ownership clarity")

        # M005: Use after potential delete
        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)
            if 'delete' in line_clean:
                # Check if same variable is used after delete on same line
                delete_match = re.search(r'delete\s+(\w+)', line_clean)
                if delete_match:
                    var = delete_match.group(1)
                    after_delete = line_clean[delete_match.end():]
                    if var in after_delete:
                        add_issue('error', 'Memory', file_path, i, 'M005',
                                  f"Use of '{var}' after delete",
                                  f"Set {var} = nullptr after delete and check before use")

    # =========================================================================
    # CATEGORY 6: INCLUDE & HEADER ISSUES (I001-I010)
    # =========================================================================
    def check_include_issues(file_path, content):
        lines = content.split('\n')
        is_header = file_path.suffix in ('.h', '.hpp')

        # I001: Missing include guard or pragma once
        if is_header:
            has_pragma_once = '#pragma once' in content
            has_include_guard = bool(re.search(r'#ifndef\s+\w+.*\n\s*#define\s+\w+', content))
            if not has_pragma_once and not has_include_guard:
                add_issue('error', 'Include', file_path, 1, 'I001',
                          "Missing include guard or #pragma once",
                          "Add '#pragma once' at the top of the header")

        # I002: #include inside namespace
        in_namespace = False
        ns_line = 0
        for i, line in enumerate(lines, 1):
            if 'namespace' in line and '{' in line:
                in_namespace = True
                ns_line = i
            if in_namespace and line.strip().startswith('#include'):
                add_issue('error', 'Include', file_path, i, 'I002',
                          "#include inside namespace block",
                          f"Move this #include before namespace (line {ns_line})")

        # I003: Duplicate includes
        includes = []
        for i, line in enumerate(lines, 1):
            match = re.match(r'\s*#include\s*[<"]([^>"]+)[>"]', line)
            if match:
                inc = match.group(1)
                if inc in includes:
                    add_issue('warning', 'Include', file_path, i, 'I003',
                              f"Duplicate include: {inc}",
                              "Remove duplicate #include directive")
                includes.append(inc)

        # I004: System include after local include
        saw_local = False
        for i, line in enumerate(lines, 1):
            if re.match(r'\s*#include\s*"', line):
                saw_local = True
            elif re.match(r'\s*#include\s*<', line) and saw_local:
                add_issue('info', 'Include', file_path, i, 'I004',
                          "System include after local include",
                          "Consider ordering: system includes first, then local includes")
                break  # Report once

        # I005: Missing common includes (heuristic)
        common_types = {
            'std::vector': '<vector>',
            'std::string': '<string>',
            'std::map': '<map>',
            'std::unordered_map': '<unordered_map>',
            'std::set': '<set>',
            'std::pair': '<utility>',
            'std::cout': '<iostream>',
            'std::unique_ptr': '<memory>',
            'std::shared_ptr': '<memory>',
            'std::function': '<functional>',
            'std::thread': '<thread>',
            'std::mutex': '<mutex>',
            'uint32_t': '<cstdint>',
            'int32_t': '<cstdint>',
            'size_t': '<cstddef>',
        }
        included = set()
        for line in lines:
            match = re.match(r'\s*#include\s*<([^>]+)>', line)
            if match:
                included.add(match.group(1))

        clean = strip_comments_strings(content)
        for type_name, header in common_types.items():
            header_name = header.strip('<>')
            if type_name in clean and header_name not in included:
                # Find first usage line
                for i, line in enumerate(lines, 1):
                    if type_name in strip_comments_strings(line):
                        add_issue('warning', 'Include', file_path, i, 'I005',
                                  f"'{type_name}' used but {header} may be missing",
                                  f"Add: #include {header}")
                        break

    # =========================================================================
    # CATEGORY 7: PYBIND11 SPECIFIC (P001-P015)
    # =========================================================================
    def check_pybind11_issues(file_path, content):
        lines = content.split('\n')
        clean = strip_comments_strings(content)

        # P001: Class without default constructor
        class_pattern = re.compile(r'\bclass\s+(\w+)[^{]*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', re.DOTALL)
        for match in class_pattern.finditer(clean):
            class_name = match.group(1)
            class_body = match.group(2)
            # Check for explicit constructors
            has_explicit_ctor = re.search(rf'\b{class_name}\s*\([^)]+\)', class_body)
            has_default_ctor = re.search(rf'\b{class_name}\s*\(\s*\)', class_body)
            has_deleted_default = re.search(rf'{class_name}\s*\(\s*\)\s*=\s*delete', class_body)

            if has_explicit_ctor and not has_default_ctor and not has_deleted_default:
                line_num = content[:match.start()].count('\n') + 1
                add_issue('warning', 'pybind11', file_path, line_num, 'P001',
                          f"Class '{class_name}' has no default constructor",
                          "pybind11 needs default constructor or explicit py::init<>")

        # P002: std::vector return without holder
        if 'std::vector' in clean:
            func_returning_vec = re.search(r'std::vector<[^>]+>\s+(\w+)\s*\(', clean)
            if func_returning_vec:
                line_num = content[:func_returning_vec.start()].count('\n') + 1
                add_issue('info', 'pybind11', file_path, line_num, 'P002',
                          "Function returning std::vector",
                          "Ensure PYBIND11_MAKE_OPAQUE or use py::return_value_policy")

        # P003: Raw pointer return
        raw_ptr_return = re.search(r'(\w+)\s*\*\s+(\w+)\s*\([^)]*\)\s*(?:const\s*)?\{', clean)
        if raw_ptr_return:
            line_num = content[:raw_ptr_return.start()].count('\n') + 1
            add_issue('warning', 'pybind11', file_path, line_num, 'P003',
                      f"Function '{raw_ptr_return.group(2)}' returns raw pointer",
                      "Specify return_value_policy (e.g., reference, take_ownership)")

        # P004: Virtual method without override
        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)
            if 'virtual' in line_clean and '=' not in line_clean:
                if 'override' not in line_clean and 'final' not in line_clean:
                    if '~' not in line_clean:  # Not destructor
                        add_issue('info', 'pybind11', file_path, i, 'P004',
                                  "Virtual method without override specifier",
                                  "Add 'override' keyword for clarity")

    # =========================================================================
    # CATEGORY 8: COMMON C++ MISTAKES (C001-C015)
    # =========================================================================
    def check_common_mistakes(file_path, content):
        lines = content.split('\n')
        clean = strip_comments_strings(content)

        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)

            # C001: Assignment in condition
            if_match = re.search(r'\bif\s*\(([^)]+)\)', line_clean)
            if if_match:
                cond = if_match.group(1)
                # Check for single = that's not ==, !=, <=, >=
                if re.search(r'[^=!<>]=[^=]', cond) and '==' not in cond:
                    add_issue('warning', 'Mistake', file_path, i, 'C001',
                              "Possible assignment in condition",
                              "Did you mean '==' instead of '='?")

            # C002: Integer division
            if re.search(r'\b\d+\s*/\s*\d+\s*[^.0-9]', line_clean):
                if 'float' in line_clean or 'double' in line_clean:
                    add_issue('warning', 'Mistake', file_path, i, 'C002',
                              "Integer division result assigned to float/double",
                              "Use floating-point literals: 1.0/2.0 or cast")

            # C003: Unused variable (simple pattern)
            var_decl = re.match(r'\s*(?:const\s+)?(?:auto|int|float|double|bool|char|std::\w+)\s+(\w+)\s*[;=]', line_clean)
            if var_decl:
                var_name = var_decl.group(1)
                # Check if variable appears again in rest of content
                # v3.4.1: Use word boundaries to avoid false positives from substring matches
                rest_content = '\n'.join(lines[i:])
                uses = len(re.findall(rf'\b{re.escape(var_name)}\b', rest_content))
                if uses <= 1:
                    add_issue('info', 'Mistake', file_path, i, 'C003',
                              f"Variable '{var_name}' may be unused",
                              "Remove unused variable or mark as [[maybe_unused]]")

            # C004: Switch without default
            if re.search(r'\bswitch\s*\(', line_clean):
                # Find matching closing brace
                start = i
                brace_count = 0
                has_default = False
                for j in range(i-1, min(i+50, len(lines))):
                    check_line = strip_comments_strings(lines[j])
                    brace_count += check_line.count('{') - check_line.count('}')
                    if 'default:' in check_line:
                        has_default = True
                    if brace_count == 0 and j > i:
                        break
                if not has_default:
                    add_issue('warning', 'Mistake', file_path, i, 'C004',
                              "Switch statement without default case",
                              "Add 'default:' case for completeness")

            # C005: Fallthrough without comment
            if re.search(r'\bcase\s+.+:', line_clean):
                # Check if previous case has break or return
                if i > 1:
                    prev_lines = '\n'.join(lines[max(0, i-5):i-1])
                    if 'case' in prev_lines or 'default' in prev_lines:
                        if 'break' not in prev_lines and 'return' not in prev_lines:
                            if '[[fallthrough]]' not in prev_lines and '// fallthrough' not in prev_lines.lower():
                                add_issue('warning', 'Mistake', file_path, i, 'C005',
                                          "Possible switch fallthrough without annotation",
                                          "Add '[[fallthrough]];' or '// fallthrough' comment")

            # C006: std::move of const object
            if 'std::move' in line_clean:
                move_match = re.search(r'std::move\s*\(\s*(\w+)\s*\)', line_clean)
                if move_match:
                    var = move_match.group(1)
                    # Check if variable is const
                    for prev_line in lines[max(0, i-10):i]:
                        if re.search(rf'\bconst\b.*\b{var}\b', strip_comments_strings(prev_line)):
                            add_issue('warning', 'Mistake', file_path, i, 'C006',
                                      f"std::move on const object '{var}'",
                                      "std::move on const has no effect - will copy instead")
                            break

            # C007: Potential null dereference
            if re.search(r'(\w+)\s*->\s*\w+.*\|\|.*\1\s*==\s*(nullptr|NULL|0)', line_clean):
                add_issue('warning', 'Mistake', file_path, i, 'C007',
                          "Potential null dereference - checked after use",
                          "Check for null before dereferencing")

            # C008: Copy in range-based for
            for_match = re.search(r'for\s*\(\s*(?:const\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*:', line_clean)
            if for_match:
                type_name = for_match.group(1)
                if type_name in ('std::string', 'std::vector', 'std::map') or type_name.startswith('std::'):
                    add_issue('info', 'Mistake', file_path, i, 'C008',
                              f"Range-based for copies '{type_name}'",
                              "Use 'const auto&' to avoid copying")

    # =========================================================================
    # CATEGORY 9: PERFORMANCE ISSUES (F001-F010)
    # =========================================================================
    def check_performance_issues(file_path, content):
        lines = content.split('\n')
        clean = strip_comments_strings(content)

        for i, line in enumerate(lines, 1):
            line_clean = strip_comments_strings(line)

            # F001: Pass by value for large types
            param_match = re.search(r'\(\s*(?:const\s+)?(std::(?:string|vector|map|set|unordered_map)[^&*,)]+)\s+\w+', line_clean)
            if param_match:
                type_name = param_match.group(1).strip()
                if '&' not in param_match.group(0) and '*' not in param_match.group(0):
                    add_issue('info', 'Performance', file_path, i, 'F001',
                              f"'{type_name}' passed by value",
                              "Pass by const reference to avoid copy: const T&")

            # F002: String concatenation in loop
            if '+=' in line_clean and 'std::string' in clean:
                # Check if we're in a loop
                in_loop = False
                for prev_line in lines[max(0, i-10):i]:
                    if re.search(r'\b(for|while)\s*\(', prev_line):
                        in_loop = True
                        break
                if in_loop and ('+= "' in line_clean or "+= '" in line_clean):
                    add_issue('info', 'Performance', file_path, i, 'F002',
                              "String concatenation in loop",
                              "Consider using std::stringstream or reserve() for better performance")

            # F003: .size() in loop condition
            for_match = re.search(r'for\s*\([^;]*;\s*\w+\s*[<>=]+\s*\w+\.size\(\)', line_clean)
            if for_match:
                add_issue('info', 'Performance', file_path, i, 'F003',
                          "Calling .size() in loop condition",
                          "Cache size before loop: const auto size = container.size();")

            # F004: Using std::endl instead of '\n'
            if 'std::endl' in line_clean:
                add_issue('info', 'Performance', file_path, i, 'F004',
                          "Using std::endl instead of '\\n'",
                          "std::endl flushes buffer - use '\\n' unless flush is needed")

            # F005: push_back without reserve
            if '.push_back(' in line_clean:
                # Check for nearby reserve
                context = '\n'.join(lines[max(0, i-10):i+1])
                if '.reserve(' not in context:
                    add_issue('info', 'Performance', file_path, i, 'F005',
                              "push_back without prior reserve()",
                              "Consider vector.reserve(n) if size is known")

    # =========================================================================
    # CATEGORY 10: STYLE ISSUES (Y001-Y005)
    # =========================================================================
    def check_style_issues(file_path, content):
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Y001: Long lines
            if len(line) > 120:
                add_issue('info', 'Style', file_path, i, 'Y001',
                          f"Line too long ({len(line)} chars)",
                          "Consider breaking line at 120 characters")

            # Y002: TODO/FIXME comments
            if 'TODO' in line or 'FIXME' in line or 'HACK' in line or 'XXX' in line:
                add_issue('info', 'Style', file_path, i, 'Y002',
                          "TODO/FIXME comment found",
                          "Remember to address this before release")

            # Y003: Magic numbers
            line_clean = strip_comments_strings(line)
            # Skip array sizes, loop bounds
            if re.search(r'[^0-9a-zA-Z_]([2-9]\d{2,}|[1-9]\d{3,})[^0-9a-zA-Z_]', line_clean):
                if 'const' not in line and 'define' not in line and '#' not in line:
                    add_issue('info', 'Style', file_path, i, 'Y003',
                              "Magic number in code",
                              "Consider using named constant")

            # Y004: Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                add_issue('info', 'Style', file_path, i, 'Y004',
                          "Trailing whitespace",
                          "Remove trailing spaces/tabs")

    # =========================================================================
    # COLLECT AND ANALYZE FILES
    # =========================================================================
    all_files_content = {}
    source_files_to_check = []

    for mod_name in module_names:
        cp_file = plugins_dir / f"{mod_name}.cp"
        if not cp_file.exists():
            click.secho(f"Warning: {mod_name}.cp not found", fg='yellow')
            continue

        # Parse .cp file for source files
        cp_content = cp_file.read_text(encoding='utf-8', errors='replace')
        source_match = re.search(r'SOURCE\(([^)]+)\)', cp_content)
        header_match = re.search(r'HEADER\(([^)]+)\)', cp_content)

        sources = []
        if source_match:
            sources.append(source_match.group(1).strip())
        if header_match:
            sources.append(header_match.group(1).strip())

        for src in sources:
            src_path = project_root / src
            if src_path.exists():
                source_files_to_check.append(src_path)
                try:
                    all_files_content[str(src_path)] = src_path.read_text(encoding='utf-8', errors='replace')
                except Exception as e:
                    add_issue('error', 'File', src_path, 1, 'F000', f"Cannot read file: {e}")

    if not source_files_to_check:
        click.secho("No source files found to analyze.", fg='yellow')
        return

    click.echo(f"\n{'='*60}")
    if use_ai:
        click.secho("IncludeCPP Fix (AI)", fg='cyan', bold=True)
    else:
        click.secho("IncludeCPP Fix", fg='cyan', bold=True)
    click.echo(f"{'='*60}")
    click.echo(f"Analyzing {len(source_files_to_check)} file(s)...\n")

    if use_ai:
        from ..core.ai_integration import get_ai_manager
        ai_mgr = get_ai_manager()
        click.echo(f"Model: {ai_mgr.get_model()}\n")
        for fp in source_files_to_check:
            click.echo(f"  Analyzing {fp.name}...")
        click.echo("")
        success, response, changes = ai_mgr.fix_code(all_files_content)
        if not success:
            click.secho(f"AI Error: {response}", fg='red', err=True)
            return
        if not changes:
            click.secho("No issues found!", fg='green', bold=True)
            click.echo(f"\nAnalyzed: {len(source_files_to_check)} file(s)")
            return
        cache_dir.mkdir(parents=True, exist_ok=True)
        manifest_entries = []
        for change in changes:
            file_path = change['file']
            if file_path.startswith('/') or file_path.startswith('\\'):
                full_path = project_root / file_path.lstrip('/\\')
            else:
                full_path = project_root / file_path
            if not full_path.exists():
                for src_path in source_files_to_check:
                    if src_path.name == Path(file_path).name:
                        full_path = src_path
                        break
            if full_path.exists():
                cache_name = f"{full_path.name}.{len(manifest_entries)}.bak"
                shutil.copy2(full_path, cache_dir / cache_name)
                manifest_entries.append({"cached": cache_name, "original": str(full_path)})
        manifest_file = cache_dir / "manifest.json"
        manifest_file.write_text(json.dumps({"files": manifest_entries}, indent=2))
        click.echo(f"{'-'*50}")
        click.secho("Changes proposed:\n", bold=True)
        for change in changes:
            click.secho(f"  {Path(change['file']).name}", fg='cyan', bold=True)
            if change.get('changes_desc'):
                for desc in change['changes_desc']:
                    click.echo(f"    {desc}")
            if change.get('confirm_required'):
                for confirm in change['confirm_required']:
                    click.secho(f"    CONFIRM: {confirm}", fg='yellow')
            click.echo("")

        # Show diffs before asking for confirmation
        _show_all_diffs(changes, all_files_content, project_root)

        has_confirms = any(c.get('confirm_required') for c in changes)
        if has_confirms:
            for change in changes:
                if change.get('confirm_required'):
                    for confirm in change['confirm_required']:
                        click.echo(f"\n{'-'*50}")
                        click.secho("CONFIRM REQUIRED:", fg='yellow', bold=True)
                        click.echo(f"\n{confirm}\n")
                        if not click.confirm("Apply this change?"):
                            click.secho("Skipped.", fg='yellow')
                            changes = [c for c in changes if c != change]
        if not auto_fix:
            if not click.confirm("Apply all changes?"):
                click.secho("Aborted. Use --undo to restore if needed.", fg='yellow')
                return
        applied = 0
        for change in changes:
            file_path = change['file']
            if file_path.startswith('/') or file_path.startswith('\\'):
                full_path = project_root / file_path.lstrip('/\\')
            else:
                full_path = project_root / file_path
            if not full_path.exists():
                for src_path in source_files_to_check:
                    if src_path.name == Path(file_path).name:
                        full_path = src_path
                        break
            if full_path.exists():
                full_path.write_text(change['content'], encoding='utf-8')
                click.secho(f"  Applied: {full_path.name}", fg='green')
                applied += 1
        click.echo(f"\n{'='*60}")
        click.secho(f"Applied {applied} fix(es)", fg='green', bold=True)
        click.echo(f"{'='*60}")
        return

    # Run all checks
    for file_path, content in all_files_content.items():
        fp = Path(file_path)
        check_namespace_issues(fp, content)
        check_syntax_errors(fp, content)
        check_type_errors(fp, content)
        check_memory_issues(fp, content)
        check_include_issues(fp, content)
        check_pybind11_issues(fp, content)
        check_common_mistakes(fp, content)
        check_performance_issues(fp, content)
        if verbose:
            check_style_issues(fp, content)

    # Check duplicates across all files
    check_duplicate_declarations(all_files_content)

    # Display results
    if not all_issues:
        click.secho("No issues found!", fg='green', bold=True)
        click.echo(f"\nAnalyzed: {len(source_files_to_check)} file(s)")
        return

    # Group issues by file
    issues_by_file = defaultdict(list)
    for issue in all_issues:
        issues_by_file[str(issue.file_path)].append(issue)

    # Count by severity
    error_count = sum(1 for i in all_issues if i.severity == 'error')
    warning_count = sum(1 for i in all_issues if i.severity == 'warning')
    info_count = sum(1 for i in all_issues if i.severity == 'info')

    # Display issues grouped by file
    for file_path, issues in sorted(issues_by_file.items()):
        click.echo(f"\n{Path(file_path).name}")
        click.echo("-" * 50)

        for issue in sorted(issues, key=lambda x: (x.line, x.severity)):
            # Severity styling
            if issue.severity == 'error':
                sev_color, sev_icon = 'red', 'X'
            elif issue.severity == 'warning':
                sev_color, sev_icon = 'yellow', '!'
            else:
                sev_color, sev_icon = 'blue', 'i'

            # Line and code
            click.echo(f"  ", nl=False)
            click.secho(f"Line {issue.line:4d}", fg='cyan', nl=False)
            click.echo(" | ", nl=False)
            click.secho(f"[{issue.code}]", fg='white', dim=True, nl=False)
            click.echo(" ", nl=False)
            click.secho(f"{sev_icon} ", fg=sev_color, nl=False)
            click.secho(issue.message, fg=sev_color)

            if issue.suggestion:
                click.echo(f"             ", nl=False)
                click.secho(f"-> {issue.suggestion}", fg='white', dim=True)

    # Category summary
    categories = defaultdict(lambda: {'error': 0, 'warning': 0, 'info': 0})
    for issue in all_issues:
        categories[issue.category][issue.severity] += 1

    click.echo(f"\n{'='*60}")
    click.echo("Summary by Category:")
    for cat, counts in sorted(categories.items()):
        parts = []
        if counts['error']:
            parts.append(click.style(f"{counts['error']}E", fg='red'))
        if counts['warning']:
            parts.append(click.style(f"{counts['warning']}W", fg='yellow'))
        if counts['info']:
            parts.append(click.style(f"{counts['info']}I", fg='blue'))
        click.echo(f"  {cat:15} {' '.join(parts)}")

    click.echo(f"\n{'='*60}")
    click.echo("Total: ", nl=False)
    if error_count:
        click.secho(f"{error_count} error(s)", fg='red', nl=False)
    if warning_count:
        click.echo(", " if error_count else "", nl=False)
        click.secho(f"{warning_count} warning(s)", fg='yellow', nl=False)
    if info_count:
        click.echo(", " if (error_count or warning_count) else "", nl=False)
        click.secho(f"{info_count} info", fg='blue', nl=False)
    click.echo()

    # Auto-fix handling
    fixable = [i for i in all_issues if i.auto_fixable]
    if fixable and auto_fix:
        click.echo(f"\nApplying {len(fixable)} auto-fix(es)...")
        cache_dir.mkdir(parents=True, exist_ok=True)
        manifest = {"files": []}
        for idx, file_path in enumerate(files_to_backup):
            cached_name = f"backup_{idx}.cpp"
            shutil.copy2(file_path, cache_dir / cached_name)
            manifest["files"].append({"original": file_path, "cached": cached_name})
        (cache_dir / "manifest.json").write_text(json.dumps(manifest))
        click.secho("Backup created. Use 'includecpp fix --undo' to revert.", fg='cyan')

        for issue in fixable:
            if issue.fix_func:
                try:
                    issue.fix_func()
                    click.secho(f"  Fixed: [{issue.code}] {issue.message}", fg='green')
                except Exception as e:
                    click.secho(f"  Failed: [{issue.code}] {issue.message} - {e}", fg='red')
    elif fixable:
        click.echo(f"\n{len(fixable)} issue(s) can be auto-fixed. Run with --auto to apply.")

    click.echo(f"{'='*60}")


# AI group - conditionally registered based on experimental_features setting
@click.group(invoke_without_command=True)
@click.option('--info', is_flag=True, help='Show AI status and usage')
@click.pass_context
def ai(ctx, info):
    if info:
        from ..core.ai_integration import get_ai_manager
        ai_mgr = get_ai_manager()
        ai_info = ai_mgr.get_info()
        click.echo(f"\n{'='*60}")
        click.secho("IncludeCPP AI", fg='cyan', bold=True)
        click.echo(f"{'='*60}")
        status = "Enabled" if ai_info['enabled'] else "Disabled"
        status_color = 'green' if ai_info['enabled'] else 'yellow'
        click.echo(f"Status:       ", nl=False)
        click.secho(status, fg=status_color)
        click.echo(f"API Key:      {ai_info['key_preview']}")
        click.echo(f"Model:        {ai_info['model']}")
        click.echo(f"{'-'*50}")
        click.echo("Usage:")
        click.echo(f"  Requests:   {ai_info['total_requests']:,}")
        click.echo(f"  Tokens:     {ai_info['total_tokens']:,}")
        last = ai_info['last_request']
        if last:
            click.echo(f"  Last:       {last[:19].replace('T', ' ')}")
        else:
            click.echo(f"  Last:       -")
        click.echo(f"{'='*60}\n")
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@ai.command(name='key')
@click.argument('api_key')
def ai_key(api_key):
    """Set OpenAI API key (stored globally in ~/.includecpp/.secret)."""
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    click.echo("Verifying API key...")
    success, msg = ai_mgr.set_key(api_key)
    if success:
        click.secho(msg, fg='green')
    else:
        click.secho(msg, fg='red', err=True)


@ai.group(invoke_without_command=True)
@click.pass_context
def token(ctx):
    """Manage API tokens for AI features.

    Tokens are stored globally in ~/.includecpp/.secret

    Available tokens:
      --brave   Brave Search API (required for --think3)
    """
    if ctx.invoked_subcommand is None:
        from ..core.ai_integration import get_ai_manager
        ai_mgr = get_ai_manager()
        click.echo(f"\n{'='*60}")
        click.secho("API Tokens", fg='cyan', bold=True)
        click.echo(f"{'='*60}")
        click.echo(f"  Brave Search: {'Configured' if ai_mgr.has_brave_key() else 'Not set'}")
        click.echo(f"{'='*60}")
        click.echo("\nSet tokens:")
        click.echo("  includecpp ai token --brave <YOUR_TOKEN>")
        click.echo("")


@token.command(name='--brave')
@click.argument('brave_key')
def token_brave(brave_key):
    """Set Brave Search API key for --think3 web research."""
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    click.echo("Verifying Brave API key...")
    success, msg = ai_mgr.set_brave_key(brave_key)
    if success:
        click.secho(msg, fg='green')
        click.echo("You can now use --think3 for advanced web research.")
    else:
        click.secho(msg, fg='red', err=True)


@ai.command(name='enable')
def ai_enable():
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    success, msg = ai_mgr.enable()
    if success:
        click.secho(msg, fg='green')
    else:
        click.secho(msg, fg='red', err=True)


@ai.command(name='disable')
def ai_disable():
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    success, msg = ai_mgr.disable()
    if success:
        click.secho(msg, fg='green')
    else:
        click.secho(msg, fg='red', err=True)


@ai.group(invoke_without_command=True)
@click.pass_context
def limit(ctx):
    """Daily token limit management.

    Controls daily token usage limit to prevent excessive API costs.
    Default limit: 220,000 tokens per day, auto-resets at midnight.

    Examples:
      includecpp ai limit              # Show current usage
      includecpp ai limit set 500000   # Set limit to 500K tokens
      includecpp ai limit get          # Show current limit
    """
    from ..core.ai_integration import get_ai_manager
    if ctx.invoked_subcommand is None:
        ai_mgr = get_ai_manager()
        info = ai_mgr.get_daily_usage_info()
        click.echo(f"\n{'='*60}")
        click.secho("Daily Token Usage", fg='cyan', bold=True)
        click.echo(f"{'='*60}")
        click.echo(f"Date:     {info['date']}")
        click.echo(f"Used:     {info['tokens_used']:,} / {info['daily_limit']:,}")
        click.echo(f"Remaining: {info['remaining']:,}")
        pct = info['percentage']
        bar_filled = int(pct / 3)
        bar_empty = 33 - bar_filled
        bar_color = 'green' if pct < 70 else ('yellow' if pct < 90 else 'red')
        click.echo(f"Progress: [", nl=False)
        click.secho('=' * bar_filled, fg=bar_color, nl=False)
        click.echo('-' * bar_empty + f"] {pct}%")
        click.echo(f"{'='*60}\n")


@limit.command(name='set')
@click.argument('tokens', type=int)
def limit_set(tokens):
    """Set daily token limit.

    Example: includecpp ai limit set 500000
    """
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    success, msg = ai_mgr.set_daily_limit(tokens)
    if success:
        click.secho(msg, fg='green')
    else:
        click.secho(msg, fg='red', err=True)


@limit.command(name='get')
def limit_get():
    """Show current daily limit."""
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    info = ai_mgr.get_daily_usage_info()
    click.echo(f"Daily limit: {info['daily_limit']:,} tokens")


@ai.command(name='undo')
def ai_undo():
    """Undo last AI changes (restore from backup)."""
    from pathlib import Path
    project_root = Path.cwd()
    cache_dir = project_root / '.fix_cache'
    manifest_file = cache_dir / 'manifest.json'
    if not manifest_file.exists():
        click.secho("No AI changes to undo.", fg='yellow')
        return
    manifest = json.loads(manifest_file.read_text())
    restored = 0
    for entry in manifest.get('files', []):
        cached = cache_dir / entry['cached']
        original = Path(entry['original'])
        if cached.exists():
            shutil.copy2(cached, original)
            click.secho(f"  Restored: {original.name}", fg='green')
            restored += 1
    for entry in manifest.get('files', []):
        cached = cache_dir / entry['cached']
        if cached.exists():
            cached.unlink()
    manifest_file.unlink()
    click.secho(f"\nRestored {restored} file(s)", fg='green', bold=True)


@ai.group(invoke_without_command=True)
@click.option('--list', 'list_models', is_flag=True, help='List available models')
@click.pass_context
def model(ctx, list_models):
    if list_models:
        from ..core.ai_integration import get_ai_manager
        ai_mgr = get_ai_manager()
        models = ai_mgr.list_models()
        click.echo(f"\n{'='*60}")
        click.secho("Available Models", fg='cyan', bold=True)
        click.echo(f"{'='*60}")
        for m in models:
            if m['active']:
                click.secho(f"  {m['name']} (active)", fg='green')
            else:
                click.echo(f"  {m['name']}")
        click.echo(f"{'='*60}\n")
    elif ctx.invoked_subcommand is None:
        from ..core.ai_integration import get_ai_manager
        ai_mgr = get_ai_manager()
        click.echo(f"Current model: {ai_mgr.get_model()}")


@model.command(name='set')
@click.argument('model_name')
def model_set(model_name):
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    success, msg = ai_mgr.set_model(model_name)
    if success:
        click.secho(msg, fg='green')
    else:
        click.secho(msg, fg='red', err=True)


def _resolve_plugin_files(project_root, module_name, plugins_dir):
    """Resolve SOURCE and HEADER files from a plugin .cp file."""
    import re
    if module_name.endswith('.cp'):
        module_name = module_name[:-3]
    cp_file = plugins_dir / f"{module_name}.cp"
    if not cp_file.exists():
        return None, None, f"Plugin not found: {cp_file}"
    cp_content = cp_file.read_text(encoding='utf-8', errors='replace')
    source_match = re.search(r'SOURCE\(([^)]+)\)', cp_content)
    header_match = re.search(r'HEADER\(([^)]+)\)', cp_content)
    files = {}
    if source_match:
        src = source_match.group(1).strip()
        src_path = project_root / src
        if src_path.exists():
            files[str(src_path)] = src_path.read_text(encoding='utf-8', errors='replace')
    if header_match:
        hdr = header_match.group(1).strip()
        hdr_path = project_root / hdr
        if hdr_path.exists():
            files[str(hdr_path)] = hdr_path.read_text(encoding='utf-8', errors='replace')
    return files, {str(cp_file): cp_content}, None


def _collect_files(project_root, plugins_dir, module_name=None, file_paths=None, exclude=None, collect_all=False):
    """Collect files based on module, --file, --all, --exclude flags."""
    from pathlib import Path
    files = {}
    plugins = {}
    exclude = exclude or []
    if file_paths:
        for f in file_paths:
            fp = Path(f)
            if not fp.is_absolute():
                fp = project_root / f
            if fp.suffix == '.cp':
                resolved, plugin_content, err = _resolve_plugin_files(project_root, fp.stem, plugins_dir)
                if err:
                    return None, None, err
                files.update(resolved or {})
                plugins.update(plugin_content or {})
            elif fp.exists():
                files[str(fp)] = fp.read_text(encoding='utf-8', errors='replace')
            else:
                return None, None, f"File not found: {f}"
    elif module_name:
        resolved, plugin_content, err = _resolve_plugin_files(project_root, module_name, plugins_dir)
        if err:
            return None, None, err
        files.update(resolved or {})
        plugins.update(plugin_content or {})
    elif collect_all:
        for cp_file in plugins_dir.glob('*.cp'):
            if cp_file.stem in exclude:
                continue
            resolved, plugin_content, _ = _resolve_plugin_files(project_root, cp_file.stem, plugins_dir)
            files.update(resolved or {})
            plugins.update(plugin_content or {})
    return files, plugins, None


@ai.command(name='ask')
@click.argument('question')
@click.argument('module_name', required=False)
@click.option('--file', 'files', multiple=True, help='Specific files to include')
@click.option('--all', 'all_modules', is_flag=True, help='Include all modules')
@click.option('-x', '--exclude', 'exclude', multiple=True, help='Exclude modules')
@click.option('--think', 'think_mode', is_flag=True, help='5K context + short planning')
@click.option('--think2', 'think_twice', is_flag=True, help='10K context + better planning')
@click.option('--think3', 'think_three', is_flag=True, help='25K context + advanced professional planning')
@click.option('--websearch', 'use_websearch', is_flag=True, help='Enable web search (requires Brave API)')
@click.option('--no-verbose', 'no_verbose', is_flag=True, help='Disable verbose output')
def ai_ask(question, module_name, files, all_modules, exclude, think_mode, think_twice, think_three, use_websearch, no_verbose):
    """Ask a question about the project with full context."""
    from pathlib import Path
    from ..core.ai_integration import get_ai_manager, get_verbose_output
    ai_mgr = get_ai_manager()
    verbose = get_verbose_output(enabled=not no_verbose)

    if not ai_mgr.is_enabled():
        if not ai_mgr.has_key():
            click.secho("AI not configured. Use: includecpp ai key <YOUR_API_KEY>", fg='red', err=True)
        else:
            click.secho("AI is disabled. Use: includecpp ai enable", fg='red', err=True)
        return

    # Start verbose output
    mode = "Think Three" if think_three else ("Think Twice" if think_twice else ("Think" if think_mode else "Standard"))
    if use_websearch:
        mode += " + Web Search"
    verbose.start(f"AI Ask [{mode}]")

    if use_websearch and not ai_mgr.has_brave_key():
        verbose.warning("--websearch requires Brave API. Use: includecpp ai token --brave <KEY>")

    verbose.phase('init', 'Setting up context')
    verbose.detail('Question', question[:50] + '...' if len(question) > 50 else question)
    verbose.detail('Mode', mode)
    verbose.detail('Model', ai_mgr.config.get('model', 'gpt-4o'))

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"
    collect_all = all_modules or (not module_name and not files)

    verbose.phase('context', 'Collecting source files')
    source_files, plugin_files, err = _collect_files(
        project_root, plugins_dir, module_name, files, list(exclude), collect_all
    )
    if err:
        verbose.error(err)
        verbose.end(success=False, message=err)
        return

    total_lines = sum(content.count('\n') for content in source_files.values())
    total_lines += sum(content.count('\n') for content in plugin_files.values())
    verbose.context_info(
        files=len(source_files) + len(plugin_files),
        lines=total_lines,
        tokens=total_lines * 4,  # Approximate
        model=ai_mgr.config.get('model', 'gpt-4o')
    )

    if use_websearch:
        verbose.phase('websearch', f'Searching: "{question[:30]}..."')

    verbose.phase('thinking', 'Processing question')
    verbose.api_call(endpoint='chat/completions', tokens_in=total_lines * 4)

    success, response = ai_mgr.ask_question(question, source_files, plugin_files, think_mode, think_twice, think_three, use_websearch)

    if not success:
        verbose.error(response)
        verbose.end(success=False, message="AI request failed")
        return

    response_lines = response.count('\n')
    verbose.api_response(tokens=response_lines * 4)
    verbose.phase('parsing', f'Response: {response_lines} lines')

    verbose.end(success=True, message="Question answered")

    click.echo(f"\n{'='*60}")
    _safe_echo(response)
    click.echo(f"{'='*60}\n")


@ai.command(name='edit')
@click.argument('task')
@click.argument('module_name', required=False)
@click.option('--file', 'files', multiple=True, help='Specific files to edit')
@click.option('--all', 'all_modules', is_flag=True, help='Edit all modules')
@click.option('-x', '--exclude', 'exclude', multiple=True, help='Exclude modules')
@click.option('--think', 'think_mode', is_flag=True, help='5K context + short planning')
@click.option('--think2', 'think_twice', is_flag=True, help='10K context + better planning')
@click.option('--think3', 'think_three', is_flag=True, help='25K context + advanced professional planning')
@click.option('--websearch', 'use_websearch', is_flag=True, help='Enable web search (requires Brave API)')
@click.option('--confirm', 'auto_confirm', is_flag=True, help='Skip confirmation, apply changes directly')
@click.option('--no-verbose', 'no_verbose', is_flag=True, help='Disable verbose output')
def ai_edit(task, module_name, files, all_modules, exclude, think_mode, think_twice, think_three, use_websearch, auto_confirm, no_verbose):
    """Edit code with AI assistance."""
    from pathlib import Path
    import shutil
    import json
    from ..core.ai_integration import get_ai_manager, get_verbose_output
    ai_mgr = get_ai_manager()
    verbose = get_verbose_output(enabled=not no_verbose)

    if not ai_mgr.is_enabled():
        if not ai_mgr.has_key():
            click.secho("AI not configured. Use: includecpp ai key <YOUR_API_KEY>", fg='red', err=True)
        else:
            click.secho("AI is disabled. Use: includecpp ai enable", fg='red', err=True)
        return

    mode = "Think Three" if think_three else ("Think Twice" if think_twice else ("Think" if think_mode else "Standard"))
    if use_websearch:
        mode += " + Web Search"
    verbose.start(f"AI Edit [{mode}]")

    if use_websearch and not ai_mgr.has_brave_key():
        verbose.warning("--websearch requires Brave API. Use: includecpp ai token --brave <KEY>")

    verbose.phase('init', 'Setting up edit task')
    verbose.detail('Task', task[:60] + '...' if len(task) > 60 else task)
    verbose.detail('Mode', mode)
    verbose.detail('Model', ai_mgr.get_model())

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"
    cache_dir = Path.home() / ".includecpp" / "fix_cache" / project_root.name

    verbose.phase('context', 'Collecting source files')
    source_files, plugin_files, err = _collect_files(
        project_root, plugins_dir, module_name, files, list(exclude), all_modules
    )
    if err:
        verbose.error(err)
        verbose.end(success=False, message=err)
        return
    if not source_files:
        verbose.error("No files to edit. Specify module, --file, or --all")
        verbose.end(success=False, message="No files found")
        return

    total_lines = sum(content.count('\n') for content in source_files.values())
    verbose.context_info(
        files=len(source_files),
        lines=total_lines,
        tokens=total_lines * 4,
        model=ai_mgr.get_model()
    )

    verbose.phase('analyzing', 'Reading source files')
    for fp in source_files.keys():
        verbose.file_operation('read', Path(fp).name, success=True)

    if use_websearch:
        verbose.phase('websearch', f'Researching: "{task[:30]}..."')

    verbose.phase('thinking', 'AI is analyzing and planning edits')
    verbose.api_call(endpoint='chat/completions', tokens_in=total_lines * 4)

    success, response, changes, question = ai_mgr.edit_code(task, source_files, think_mode, think_twice, think_three, use_websearch)

    if not success:
        verbose.error(f"AI Error: {response}")
        verbose.end(success=False, message=response[:100])
        return

    verbose.api_call(endpoint='chat/completions', tokens_out=len(str(changes)) // 4 if changes else 0)

    # Handle AI asking a clarifying question (think2/think3 only)
    while question and (think_twice or think_three):
        verbose.phase('waiting', 'AI needs clarification')
        click.echo("")
        click.secho("AI needs clarification:", fg='cyan', bold=True)
        click.echo(f"  {question['question']}")
        if question.get('options'):
            click.echo("\nOptions:")
            for i, opt in enumerate(question['options'], 1):
                click.echo(f"  {i}. {opt}")
            click.echo(f"  {len(question['options'])+1}. Custom answer")
            choice = click.prompt("Select option", type=int, default=1)
            if choice <= len(question['options']):
                answer = question['options'][choice - 1]
            else:
                answer = click.prompt("Your answer")
        else:
            answer = click.prompt("Your answer")
        click.echo(f"\nContinuing with answer: {answer}\n")
        verbose.phase('thinking', 'Continuing with user answer')
        verbose.api_call(endpoint='chat/completions', tokens_in=len(answer) * 4)
        original_prompt = f'Edit task: {task}'
        success, response, changes = ai_mgr.continue_with_answer(
            original_prompt, question['question'], answer, think_twice, think_three
        )
        if not success:
            verbose.error(f"AI Error: {response}")
            verbose.end(success=False, message=response[:100])
            return
        verbose.api_call(endpoint='chat/completions', tokens_out=len(str(changes)) // 4 if changes else 0)
        question = None  # Continuation doesn't ask more questions

    if not changes:
        verbose.status("No changes needed", phase='complete')
        verbose.end(success=True, message="No changes required")
        return

    verbose.phase('backup', 'Creating file backups')
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest_entries = []
    for change in changes:
        file_path = change['file']
        full_path = None
        for orig_path in source_files.keys():
            if Path(orig_path).name == Path(file_path).name:
                full_path = Path(orig_path)
                break
        if full_path and full_path.exists():
            cache_name = f"{full_path.name}.{len(manifest_entries)}.bak"
            shutil.copy2(full_path, cache_dir / cache_name)
            manifest_entries.append({"cached": cache_name, "original": str(full_path)})
            verbose.file_operation('backup', Path(cache_name).name, success=True)
    manifest_file = cache_dir / "manifest.json"
    manifest_file.write_text(json.dumps({"files": manifest_entries}, indent=2))

    verbose.phase('review', f'Reviewing {len(changes)} proposed changes')
    click.echo(f"{'-'*50}")
    click.secho("Changes proposed:\n", bold=True)

    changes_summary = []
    for change in changes:
        click.secho(f"  {Path(change['file']).name}", fg='cyan', bold=True)
        desc_list = []
        if change.get('changes_desc'):
            for desc in change['changes_desc']:
                click.echo(f"    {desc}")
                desc_list.append(desc)
        if change.get('confirm_required'):
            for confirm in change['confirm_required']:
                click.secho(f"    CONFIRM: {confirm}", fg='yellow')
        click.echo("")
        changes_summary.append({'file': Path(change['file']).name, 'changes': desc_list})

    # Show diffs before asking for confirmation
    _show_all_diffs(changes, source_files, project_root)

    if not auto_confirm:
        if not click.confirm("Apply changes?"):
            verbose.warning("Changes aborted by user")
            verbose.end(success=False, message="Aborted by user")
            return

    verbose.phase('writing', 'Applying changes to files')
    applied = 0
    for change in changes:
        file_path = change['file']
        full_path = None
        for orig_path in source_files.keys():
            if Path(orig_path).name == Path(file_path).name:
                full_path = Path(orig_path)
                break
        if full_path and full_path.exists():
            full_path.write_text(change['content'], encoding='utf-8')
            verbose.file_operation('write', full_path.name, success=True)
            click.secho(f"  Applied: {full_path.name}", fg='green')
            applied += 1

    verbose.changes_summary(changes_summary)
    verbose.end(success=True, message=f"Applied {applied} edit(s)")


@ai.command(name='generate')
@click.argument('task')
@click.option('--file', 'files', multiple=True, help='Files to include (unlimited)')
@click.option('--think', 'think_mode', is_flag=True, help='5K context + planning')
@click.option('--think2', 'think_twice', is_flag=True, help='10K context + better planning')
@click.option('--think3', 'think_three', is_flag=True, help='25K context + professional planning')
@click.option('--websearch', 'use_websearch', is_flag=True, help='Enable web search')
@click.option('--t-max-context', 'max_context', is_flag=True, help='Full context (no reduction)')
@click.option('--t-plan', 'plan_mode', is_flag=True, help='Planning mode with search/grep')
@click.option('--t-new-module', 'new_module', type=str, help='Create new module from scratch')
@click.option('--confirm', 'auto_confirm', is_flag=True, help='Skip confirmations')
@click.option('--python', 'python_file', type=str, help='Include Python file (auto-detect modules)')
@click.option('--no-verbose', 'no_verbose', is_flag=True, help='Disable verbose output')
def ai_generate(task, files, think_mode, think_twice, think_three, use_websearch,
                max_context, plan_mode, new_module, auto_confirm, python_file, no_verbose):
    """AI super assistant with tool execution.

    Examples:
        includecpp ai generate "add logging" mymodule.cp
        includecpp ai generate "fast math lib" --t-new-module math_utils
        includecpp ai generate "optimize" --t-plan --think2
        includecpp ai generate "update api" mymod.cp --python main.py

    The generate command has access to tools for:
    - File operations (read, write, edit, delete)
    - Folder operations (create, list, search)
    - Command execution (system and includecpp commands)
    """
    from pathlib import Path
    import shutil
    import json
    import re
    from ..core.ai_integration import get_ai_manager, get_verbose_output

    ai_mgr = get_ai_manager()
    verbose = get_verbose_output(enabled=not no_verbose)

    if not ai_mgr.is_enabled():
        if not ai_mgr.has_key():
            click.secho("AI not configured. Use: includecpp ai key <YOUR_API_KEY>", fg='red')
        else:
            click.secho("AI is disabled. Use: includecpp ai enable", fg='red')
        return

    # Build mode string
    mode_parts = []
    if think_three: mode_parts.append("Think3")
    elif think_twice: mode_parts.append("Think2")
    elif think_mode: mode_parts.append("Think")
    if use_websearch: mode_parts.append("WebSearch")
    if max_context: mode_parts.append("MaxContext")
    if plan_mode: mode_parts.append("Plan")
    if new_module: mode_parts.append(f"NewModule")
    mode = ' + '.join(mode_parts) if mode_parts else 'Standard'

    verbose.start(f"AI Generate [{mode}]")

    if use_websearch and not ai_mgr.has_brave_key():
        verbose.warning("--websearch requires Brave API. Use: includecpp ai token --brave <KEY>")

    verbose.phase('init', 'Setting up generation task')
    verbose.detail('Task', task[:60] + '...' if len(task) > 60 else task)
    verbose.detail('Mode', mode)
    verbose.detail('Model', ai_mgr.get_model())
    if new_module:
        verbose.detail('New Module', new_module)

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"
    cache_dir = Path.home() / ".includecpp" / "fix_cache" / project_root.name

    verbose.phase('context', 'Collecting source files')

    # Collect files
    source_files = {}
    if files:
        for f in files:
            fp = Path(f)
            if not fp.is_absolute():
                fp = project_root / f
            if fp.suffix == '.cp':
                # Auto-resolve SOURCE/HEADER from .cp
                resolved, _, err = _resolve_plugin_files(project_root, fp.stem, plugins_dir)
                if resolved:
                    source_files.update(resolved)
                    verbose.file_operation('read', f'{fp.stem}.cp (resolved)', success=True)
            elif fp.exists():
                source_files[str(fp)] = fp.read_text(encoding='utf-8', errors='replace')
                verbose.file_operation('read', fp.name, success=True)
            else:
                verbose.file_operation('read', fp.name, success=False, message='not found')

    # Handle --python flag
    detected_modules = []
    if python_file:
        verbose.phase('analyzing', f'Analyzing Python file: {python_file}')
        py_path = Path(python_file)
        if not py_path.is_absolute():
            py_path = project_root / python_file
        if py_path.exists():
            py_content = py_path.read_text(encoding='utf-8', errors='replace')
            source_files[str(py_path)] = py_content
            verbose.file_operation('read', py_path.name, success=True)
            # Detect includecpp imports
            imports = re.findall(r'from\s+includecpp\s+import\s+(\w+)', py_content)
            imports += re.findall(r'from\s+includecpp\.(\w+)', py_content)
            detected_modules = list(set(imports))
            if detected_modules:
                verbose.detail('Detected modules', ', '.join(detected_modules))
            # Auto-add detected modules
            for mod in detected_modules:
                if (plugins_dir / f"{mod}.cp").exists():
                    resolved, _, _ = _resolve_plugin_files(project_root, mod, plugins_dir)
                    if resolved:
                        source_files.update(resolved)
                        verbose.file_operation('read', f'{mod}.cp (auto)', success=True)

    total_lines = sum(content.count('\n') for content in source_files.values())
    verbose.context_info(
        files=len(source_files),
        lines=total_lines,
        tokens=total_lines * 4,
        model=ai_mgr.get_model()
    )

    if use_websearch:
        verbose.phase('websearch', f'Researching: "{task[:30]}..."')

    verbose.phase('thinking', 'AI is analyzing and generating code')
    verbose.api_call(endpoint='chat/completions', tokens_in=total_lines * 4 + len(task) * 4)

    # Execute
    success, response, changes = ai_mgr.generate(
        task, source_files, project_root,
        think_mode, think_twice, think_three, use_websearch,
        max_context, plan_mode, new_module
    )

    if not success:
        verbose.error(f"AI Error: {response}")
        verbose.end(success=False, message=response[:100] if response else "Generation failed")
        return

    verbose.api_call(endpoint='chat/completions', tokens_out=len(str(changes)) // 4 if changes else len(response) // 4)

    if not changes:
        verbose.status("No file changes needed", phase='complete')
        # Show response if any
        if response:
            _safe_echo(f"\n{response[:2000]}")
        verbose.end(success=True, message="Completed (no changes)")
        return

    verbose.phase('backup', 'Creating file backups')
    # Backup files
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest_entries = []
    for change in changes:
        file_path = Path(change['file'])
        if not file_path.is_absolute():
            file_path = project_root / change['file']
        if file_path.exists():
            cache_name = f"{file_path.name}.{len(manifest_entries)}.bak"
            shutil.copy2(file_path, cache_dir / cache_name)
            manifest_entries.append({"cached": cache_name, "original": str(file_path)})
            verbose.file_operation('backup', file_path.name, success=True)
    manifest_file = cache_dir / "manifest.json"
    manifest_file.write_text(json.dumps({"files": manifest_entries}, indent=2))

    verbose.phase('review', f'Reviewing {len(changes)} proposed changes')

    # Show changes
    click.echo(f"{'-'*50}")
    click.secho("Changes proposed:\n", bold=True)
    changes_summary = []
    for change in changes:
        fp = Path(change['file'])
        if not fp.is_absolute():
            fp = project_root / change['file']
        is_new = not fp.exists()
        click.secho(f"  {'[NEW] ' if is_new else ''}{fp.name}", fg='green' if is_new else 'cyan', bold=True)
        desc_list = []
        if change.get('changes_desc'):
            for desc in change['changes_desc']:
                click.echo(f"    - {desc}")
                desc_list.append(desc)
        click.echo("")
        changes_summary.append({'file': fp.name, 'changes': desc_list, 'new': is_new})

    # Show diffs for existing files
    _show_all_diffs(changes, source_files, project_root)

    # Confirm
    if not auto_confirm:
        if not click.confirm("Apply changes?"):
            verbose.warning("Changes aborted by user")
            verbose.end(success=False, message="Aborted by user")
            return

    verbose.phase('writing', 'Applying changes to files')
    # Apply
    applied = 0
    for change in changes:
        file_path = Path(change['file'])
        if not file_path.is_absolute():
            file_path = project_root / change['file']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(change['content'], encoding='utf-8')
        verbose.file_operation('write', file_path.name, success=True)
        click.secho(f"  Applied: {file_path.name}", fg='green')
        applied += 1

    # Auto plugin + build for new module
    if new_module:
        verbose.phase('building', f'Building new module: {new_module}')

        # Generate plugin
        import subprocess
        verbose.tool_call('includecpp', f'plugin {new_module}')
        result = subprocess.run(
            f'includecpp plugin {new_module}',
            shell=True, capture_output=True, text=True, cwd=project_root
        )
        if result.returncode == 0:
            verbose.status("Plugin generated", phase='complete')
        else:
            verbose.error(f"Plugin error: {result.stderr[:100]}")
            verbose.end(success=False, message="Plugin generation failed")
            return

        # Build
        verbose.tool_call('includecpp', f'rebuild --fast -m {new_module}')
        result = subprocess.run(
            f'includecpp rebuild --fast -m {new_module}',
            shell=True, capture_output=True, text=True, cwd=project_root
        )
        if result.returncode == 0:
            verbose.status("Build successful", phase='complete')
        else:
            verbose.error(f"Build error: {result.stderr[:100]}")

    verbose.changes_summary(changes_summary)
    verbose.end(success=True, message=f"Applied {applied} change(s)")


@ai.command(name='tools')
def ai_tools():
    """List available AI tools for the generate command."""
    from ..core.ai_integration import get_ai_manager
    ai_mgr = get_ai_manager()
    click.echo(ai_mgr.get_tools_info())


@ai.command(name='optimize')
@click.argument('module_name', required=False)
@click.option('--file', 'files', multiple=True, help='Specific files to optimize')
@click.option('--agent', 'agent_task', type=str, help='Custom AI task description')
@click.option('--confirm', 'auto_confirm', is_flag=True, help='Skip confirmation, apply changes directly')
@click.option('--no-verbose', 'no_verbose', is_flag=True, help='Disable verbose output')
def ai_optimize(module_name, files, agent_task, auto_confirm, no_verbose):
    """Optimize code with AI assistance."""
    from pathlib import Path
    import shutil
    import json
    from ..core.ai_integration import get_ai_manager, get_verbose_output

    ai_mgr = get_ai_manager()
    verbose = get_verbose_output(enabled=not no_verbose)

    if not ai_mgr.is_enabled():
        if not ai_mgr.has_key():
            click.secho("AI not configured. Use: includecpp ai key <YOUR_API_KEY>", fg='red', err=True)
        else:
            click.secho("AI is disabled. Use: includecpp ai enable", fg='red', err=True)
        return

    verbose.start("AI Optimize")

    verbose.phase('init', 'Setting up optimization task')
    verbose.detail('Model', ai_mgr.get_model())
    if agent_task:
        verbose.detail('Custom Task', agent_task[:50] + '...' if len(agent_task) > 50 else agent_task)

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"
    cache_dir = Path.home() / ".includecpp" / "fix_cache" / project_root.name

    verbose.phase('context', 'Collecting source files')
    files_to_optimize = {}
    if files:
        for f in files:
            fp = Path(f)
            if not fp.is_absolute():
                fp = project_root / f
            if fp.exists():
                files_to_optimize[str(fp)] = fp.read_text(encoding='utf-8', errors='replace')
                verbose.file_operation('read', fp.name, success=True)
            else:
                verbose.file_operation('read', f, success=False, message='not found')
                verbose.end(success=False, message=f"File not found: {f}")
                return
    elif module_name:
        if module_name.endswith('.cp'):
            module_name = module_name[:-3]
        verbose.detail('Module', module_name)
        cp_file = plugins_dir / f"{module_name}.cp"
        if not cp_file.exists():
            verbose.error(f"Plugin not found: {cp_file}")
            verbose.end(success=False, message="Plugin not found")
            return
        import re
        cp_content = cp_file.read_text(encoding='utf-8', errors='replace')
        verbose.file_operation('read', f'{module_name}.cp', success=True)
        source_match = re.search(r'SOURCE\(([^)]+)\)', cp_content)
        header_match = re.search(r'HEADER\(([^)]+)\)', cp_content)
        sources = []
        if source_match:
            sources.append(source_match.group(1).strip())
        if header_match:
            sources.append(header_match.group(1).strip())
        for src in sources:
            src_path = project_root / src
            if src_path.exists():
                files_to_optimize[str(src_path)] = src_path.read_text(encoding='utf-8', errors='replace')
                verbose.file_operation('read', Path(src).name, success=True)
    else:
        verbose.error("Specify a module name or use --file")
        verbose.end(success=False, message="No input specified")
        return

    if not files_to_optimize:
        verbose.warning("No files to optimize")
        verbose.end(success=True, message="No files found")
        return

    total_lines = sum(content.count('\n') for content in files_to_optimize.values())
    verbose.context_info(
        files=len(files_to_optimize),
        lines=total_lines,
        tokens=total_lines * 4,
        model=ai_mgr.get_model()
    )

    verbose.phase('analyzing', 'Analyzing code for optimization opportunities')
    for fp in files_to_optimize.keys():
        verbose.status(f"Scanning {Path(fp).name}", phase='analyzing')

    verbose.phase('thinking', 'AI is analyzing and planning optimizations')
    verbose.api_call(endpoint='chat/completions', tokens_in=total_lines * 4)

    success, response, changes = ai_mgr.optimize_code(files_to_optimize, agent_task)

    if not success:
        verbose.error(f"AI Error: {response}")
        verbose.end(success=False, message=response[:100] if response else "Optimization failed")
        return

    verbose.api_call(endpoint='chat/completions', tokens_out=len(str(changes)) // 4 if changes else 0)

    if not changes:
        verbose.status("No optimizations needed", phase='complete')
        verbose.end(success=True, message="Code is already optimal")
        return

    verbose.phase('backup', 'Creating file backups')
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest_entries = []
    for change in changes:
        file_path = change['file']
        full_path = None
        for orig_path in files_to_optimize.keys():
            if Path(orig_path).name == Path(file_path).name:
                full_path = Path(orig_path)
                break
        if full_path and full_path.exists():
            cache_name = f"{full_path.name}.{len(manifest_entries)}.bak"
            shutil.copy2(full_path, cache_dir / cache_name)
            manifest_entries.append({"cached": cache_name, "original": str(full_path)})
            verbose.file_operation('backup', full_path.name, success=True)
    manifest_file = cache_dir / "manifest.json"
    manifest_file.write_text(json.dumps({"files": manifest_entries}, indent=2))

    verbose.phase('review', f'Reviewing {len(changes)} proposed optimizations')
    click.echo(f"{'-'*50}")
    click.secho("Changes proposed:\n", bold=True)

    changes_summary = []
    for change in changes:
        click.secho(f"  {Path(change['file']).name}", fg='cyan', bold=True)
        desc_list = []
        if change.get('changes_desc'):
            for desc in change['changes_desc']:
                click.echo(f"    {desc}")
                desc_list.append(desc)
        if change.get('confirm_required'):
            for confirm in change['confirm_required']:
                click.secho(f"    CONFIRM: {confirm}", fg='yellow')
        click.echo("")
        changes_summary.append({'file': Path(change['file']).name, 'changes': desc_list})

    # Show diffs before asking for confirmation
    _show_all_diffs(changes, files_to_optimize, project_root)

    if not auto_confirm:
        has_confirms = any(c.get('confirm_required') for c in changes)
        if has_confirms:
            for change in changes:
                if change.get('confirm_required'):
                    for confirm in change['confirm_required']:
                        click.echo(f"\n{'-'*50}")
                        click.secho("CONFIRM REQUIRED:", fg='yellow', bold=True)
                        click.echo(f"\n{confirm}\n")
                        if not click.confirm("Apply this change?"):
                            verbose.status(f"Skipped: {change['file']}", phase='warning')
                            changes = [c for c in changes if c != change]
        if not click.confirm("Apply all changes?"):
            verbose.warning("Changes aborted by user")
            verbose.end(success=False, message="Aborted by user")
            return

    verbose.phase('writing', 'Applying optimizations to files')
    applied = 0
    for change in changes:
        file_path = change['file']
        full_path = None
        for orig_path in files_to_optimize.keys():
            if Path(orig_path).name == Path(file_path).name:
                full_path = Path(orig_path)
                break
        if full_path and full_path.exists():
            full_path.write_text(change['content'], encoding='utf-8')
            verbose.file_operation('write', full_path.name, success=True)
            click.secho(f"  Applied: {full_path.name}", fg='green')
            applied += 1

    verbose.changes_summary(changes_summary)
    verbose.end(success=True, message=f"Applied {applied} optimization(s)")


@cli.command()
def settings():
    """Open graphical settings panel.

    Opens a dark-themed PyQt6 widget for configuring:
    - AI features (enable/disable, API key, model)
    - API tokens (Brave Search for --think3)

    Settings are stored globally in ~/.includecpp/.secret

    Requires: pip install PyQt6
    """
    try:
        from ..core.settings_ui import show_settings, PYQT_AVAILABLE
        if not PYQT_AVAILABLE:
            click.secho("PyQt6 not installed.", fg='red', err=True)
            click.echo("Install with: pip install PyQt6")
            click.echo("\nAlternatively, use CLI commands:")
            click.echo("  includecpp ai key <YOUR_KEY>")
            click.echo("  includecpp ai enable")
            click.echo("  includecpp ai model set <MODEL>")
            click.echo("  includecpp ai token --brave <TOKEN>")
            return
        success, msg = show_settings()
        if success:
            click.secho("Settings saved.", fg='green')
        else:
            click.secho(msg, fg='red', err=True)
    except Exception as e:
        click.secho(f"Error opening settings: {e}", fg='red', err=True)
        click.echo("\nUse CLI commands instead:")
        click.echo("  includecpp ai --info")
        click.echo("  includecpp ai key <YOUR_KEY>")


@click.command()
@click.option('--path', '-p', type=click.Path(), default=None,
              help='Path to project directory (default: current directory)')
def project(path):
    """Open the Project Interface with CodeMaker.

    Opens a professional visual mindmap tool for planning and designing
    your C++ project structure.

    Features:
    - Visual node-based system design
    - Class, Function, Object, and Definition nodes
    - Connectable nodes with bezier curves
    - Pan/zoom navigation (middle mouse button)
    - Auto-save functionality
    - .ma map file management

    Controls:
    - Right-click canvas: Create new nodes
    - Right-click node: Edit/Connect/Delete
    - Middle mouse + drag: Pan view
    - Middle mouse + scroll: Zoom in/out
    - ESC: Cancel connection mode
    - DELETE: Remove selected nodes

    Requires: pip install PyQt6
    """
    from pathlib import Path as PathLib
    project_path = PathLib(path) if path else PathLib.cwd()

    if not project_path.exists():
        click.secho(f"Path does not exist: {project_path}", fg='red', err=True)
        return

    try:
        from ..core.project_ui import show_project, PYQT_AVAILABLE
        if not PYQT_AVAILABLE:
            click.secho("PyQt6 not installed.", fg='red', err=True)
            click.echo("Install with: pip install PyQt6")
            return
        success, msg = show_project(str(project_path))
        if not success:
            click.secho(msg, fg='red', err=True)
    except Exception as e:
        click.secho(f"Error opening project interface: {e}", fg='red', err=True)


# ============================================================================
# CPPY - Code Conversion Tools (Experimental)
# ============================================================================

# CPPY group - conditionally registered based on experimental_features setting
@click.group(invoke_without_command=True)
@click.pass_context
def cppy(ctx):
    """Code conversion tools for Python <-> C++.

    Convert Python code to optimized C++ or C++ to Python.

    Examples:
        includecpp cppy convert math.py --cpp
        includecpp cppy convert utils.cpp --py
        includecpp cppy convert mymodule.cp --cpp --no-h
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cppy.command(name='convert')
@click.argument('files', nargs=-1, required=True)
@click.option('--cpp', 'to_cpp', is_flag=True, help='Convert Python to C++')
@click.option('--py', 'to_py', is_flag=True, help='Convert C++ to Python')
@click.option('--no-h', 'no_header', is_flag=True, help='Skip header generation (--cpp only)')
@click.option('--output', '-o', type=click.Path(), help='Output directory (default: same as source)')
@click.option('--namespace', 'ns', default='includecpp', help='C++ namespace (default: includecpp)')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed conversion info')
@click.option('--ai', 'use_ai', is_flag=True, help='AI-assisted conversion (default: --think2 mode)')
@click.option('--think', 'use_think', is_flag=True, help='Use --think mode with AI (less context)')
@click.option('--think3', 'use_think3', is_flag=True, help='Use --think3 mode with AI (max context)')
@click.option('--websearch', 'use_websearch', is_flag=True, help='Enable web search for AI conversion')
@click.option('--no-verbose', 'no_ai_verbose', is_flag=True, help='Disable AI verbose output (--ai only)')
@click.option('--force', is_flag=True, help='Force conversion even with unconvertible code')
def cppy_convert(files, to_cpp, to_py, no_header, output, ns, verbose, use_ai, use_think, use_think3, use_websearch, no_ai_verbose, force):
    """Convert code between Python and C++.

    Supports full bidirectional conversion with:
    - Classes, structs, dataclasses
    - Functions with type hints
    - Methods (static, const, virtual)
    - Constructors and destructors
    - Fields and properties
    - Templates and generics
    - List comprehensions
    - Lambda expressions
    - Exception handling
    - Control flow (if, for, while, with)

    \b
    Python to C++ (--cpp):
        Creates .cpp and .h files with namespace includecpp {}
        Type hints are converted to C++ types
        Python builtins mapped to STL equivalents

    \b
    C++ to Python (--py):
        Creates .py file with type hints
        STL types mapped to Python equivalents
        Methods become class methods with self

    \b
    Auto-resolve .cp files:
        If input is a .cp plugin file, SOURCE() directive is read
        to find the actual source file for conversion.

    \b
    AI-assisted mode (--ai):
        Uses AI with --think2 context for intelligent conversion
        - Section-by-section analysis and conversion
        - Automatic workarounds for unconvertible patterns
        - pybind11 wrappers for Python-specific features
        - Reports API changes to user

    Examples:
        includecpp cppy convert math_utils.py --cpp
        includecpp cppy convert data_types.py --cpp --no-h
        includecpp cppy convert vector_ops.cpp --py
        includecpp cppy convert mymodule.cp --cpp -o include/
        includecpp cppy convert complex_lib.py --cpp --ai
    """
    from pathlib import Path
    from ..core.cppy_converter import (
        convert_python_to_cpp,
        convert_cpp_to_python,
        PythonToCppConverter,
        CppToPythonConverter
    )

    if not to_cpp and not to_py:
        click.secho("Error: Specify --cpp or --py conversion mode", fg='red', err=True)
        click.echo("\nUsage:")
        click.echo("  includecpp cppy convert <files> --cpp  # Python to C++")
        click.echo("  includecpp cppy convert <files> --py   # C++ to Python")
        return

    if to_cpp and to_py:
        click.secho("Error: Cannot use both --cpp and --py", fg='red', err=True)
        return

    project_root = Path.cwd()
    plugins_dir = project_root / "plugins"
    include_dir = project_root / "include"
    output_dir = Path(output) if output else None

    click.echo("=" * 60)
    click.secho("IncludeCPP CPPY Convert", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo()

    mode = "Python -> C++" if to_cpp else "C++ -> Python"
    click.echo(f"  Mode:           {mode}")
    click.echo(f"  Files:          {len(files)}")
    click.echo(f"  Namespace:      {ns}")
    if output_dir:
        click.echo(f"  Output:         {output_dir}")
    if no_header and to_cpp:
        click.echo(f"  Header:         Disabled")
    if use_ai:
        ai_mode = "--think" if use_think else ("--think3" if use_think3 else "--think2")
        extra = " + websearch" if use_websearch else ""
        click.secho(f"  AI Mode:        Enabled ({ai_mode}{extra})", fg='magenta')
    click.echo()

    resolved_files = []
    for f in files:
        fp = Path(f)
        if not fp.is_absolute():
            fp = project_root / f

        if fp.suffix == '.cp':
            source_file = _resolve_cp_source(fp, project_root)
            if source_file:
                resolved_files.append(source_file)
                if verbose:
                    click.echo(f"  Resolved {fp.name} -> {source_file.name}")
            else:
                click.secho(f"  Warning: Could not resolve SOURCE in {fp.name}", fg='yellow')
        elif fp.exists():
            resolved_files.append(fp)
        else:
            click.secho(f"  Warning: File not found: {fp}", fg='yellow')

    if not resolved_files:
        click.secho("No valid files to convert.", fg='red', err=True)
        return

    total_converted = 0
    total_functions = 0
    total_classes = 0
    total_lines_generated = 0
    all_api_changes = []
    all_workarounds = []

    for source_file in resolved_files:
        click.echo("-" * 50)
        click.secho(f"Converting: {source_file.name}", fg='cyan', bold=True)
        click.echo()

        try:
            content = source_file.read_text(encoding='utf-8', errors='replace')
            module_name = source_file.stem

            if use_ai:
                # AI-assisted conversion
                result = _convert_with_ai(
                    content, module_name, source_file,
                    output_dir, no_header, ns, verbose, to_cpp, no_ai_verbose,
                    use_think=use_think, use_think3=use_think3, use_websearch=use_websearch
                )
                if result.get('api_changes'):
                    all_api_changes.extend(result['api_changes'])
                if result.get('workarounds'):
                    all_workarounds.extend(result['workarounds'])
            elif to_cpp:
                result = _convert_to_cpp(
                    content, module_name, source_file,
                    output_dir, no_header, ns, verbose, force
                )
            else:
                result = _convert_to_python(
                    content, module_name, source_file,
                    output_dir, verbose
                )

            if result['success']:
                total_converted += 1
                total_functions += result.get('functions', 0)
                total_classes += result.get('classes', 0)
                total_lines_generated += result.get('lines', 0)

                click.echo(f"  Parsed:         {result.get('functions', 0)} functions, {result.get('classes', 0)} classes")
                for out_file, lines in result.get('outputs', []):
                    click.secho(f"  Generated:      {out_file} ({lines} lines)", fg='green')

                # Show workarounds used in AI mode
                if use_ai and result.get('workarounds'):
                    click.secho(f"  Workarounds:    {len(result['workarounds'])} applied", fg='yellow')
                    if verbose:
                        for w in result['workarounds']:
                            click.echo(f"    - {w}")

                # Show unconvertible code warnings (even if forced)
                if result.get('unconvertible'):
                    click.echo()
                    click.secho("  UNCONVERTIBLE CODE:", fg='yellow', bold=True)
                    for item, reason, line in result['unconvertible']:
                        click.secho(f"    Line {line}: {item} - {reason}", fg='yellow')
            else:
                # Show unconvertible code in red if blocked
                if result.get('blocked'):
                    click.echo()
                    click.secho("  UNCONVERTIBLE CODE DETECTED:", fg='red', bold=True)
                    for item, reason, line in result.get('unconvertible', []):
                        click.secho(f"    Line {line}: {item} - {reason}", fg='red')
                    click.echo()
                    click.secho("  Use --force to convert anyway (with /* UNCONVERTIBLE */ comments)", fg='yellow')
                else:
                    click.secho(f"  Error: {result.get('error', 'Unknown error')}", fg='red')

        except Exception as e:
            click.secho(f"  Error: {str(e)}", fg='red', err=True)
            if verbose:
                import traceback
                click.echo(traceback.format_exc())

        click.echo()

    click.echo("=" * 60)
    if total_converted > 0:
        click.secho(f"Conversion complete: {total_converted} file(s) processed", fg='green', bold=True)
        click.echo(f"  Total functions: {total_functions}")
        click.echo(f"  Total classes:   {total_classes}")
        click.echo(f"  Lines generated: {total_lines_generated}")

        # Report API changes to user (important!)
        if all_api_changes:
            click.echo()
            click.secho("API CHANGES:", fg='yellow', bold=True)
            for change in all_api_changes:
                click.secho(f"  ! {change}", fg='yellow')

        # Report workarounds summary
        if all_workarounds and use_ai:
            click.echo()
            click.secho(f"WORKAROUNDS APPLIED: {len(all_workarounds)}", fg='cyan')
            if verbose:
                for w in all_workarounds:
                    click.echo(f"  - {w}")
    else:
        click.secho("No files were converted.", fg='yellow')
    click.echo("=" * 60)


def _resolve_cp_source(cp_file: Path, project_root: Path) -> Path:
    """Resolve SOURCE() directive from .cp file to actual source file.

    Returns the first valid source file found. Supports:
        - Single file: SOURCE(file.cpp)
        - Multiple files in one SOURCE: SOURCE(file1.cpp file2.cpp)
        - Multiple SOURCE declarations: SOURCE(file1.cpp) && SOURCE(file2.cpp)
    """
    try:
        content = cp_file.read_text(encoding='utf-8', errors='replace')
        import re

        # Find all SOURCE() declarations
        source_matches = re.findall(r'SOURCE\s*\(\s*([^)]+)\s*\)', content)
        for sources_str in source_matches:
            # Handle multiple files within one SOURCE()
            sources = re.split(r'[,\s]+', sources_str.strip())
            for source_name in sources:
                source_name = source_name.strip().strip('"\'')
                if not source_name:
                    continue

                include_dir = project_root / "include"

                # Try direct path first (relative to project root)
                direct_from_root = project_root / source_name
                if direct_from_root.exists():
                    return direct_from_root

                # Try in include directory
                direct = include_dir / source_name
                if direct.exists():
                    return direct

                # Try with different extensions
                for ext in ['.cpp', '.h', '.hpp', '.cc', '.cxx']:
                    base_name = source_name.replace('.cpp', '').replace('.h', '').replace('.hpp', '')
                    candidate = include_dir / (base_name + ext)
                    if candidate.exists():
                        return candidate
    except Exception:
        pass
    return None


def _convert_to_cpp(content: str, module_name: str, source_file: Path,
                    output_dir: Path, no_header: bool, namespace: str,
                    verbose: bool, force: bool = False) -> dict:
    """Convert Python to C++."""
    from ..core.cppy_converter import PythonToCppConverter
    import ast

    result = {
        'success': False,
        'functions': 0,
        'classes': 0,
        'lines': 0,
        'outputs': [],
        'error': None,
        'unconvertible': [],
        'blocked': False
    }

    try:
        tree = ast.parse(content)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                result['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                result['classes'] += 1

        converter = PythonToCppConverter()
        cpp_content, header_content = converter.convert(content, module_name)

        # Check for unconvertible code
        if converter.has_unconvertible_code():
            result['unconvertible'] = converter.unconvertible
            if not force:
                result['blocked'] = True
                result['error'] = "Contains unconvertible code. Use --force to convert anyway."
                return result

        if namespace != 'includecpp':
            cpp_content = cpp_content.replace('namespace includecpp', f'namespace {namespace}')
            cpp_content = cpp_content.replace('} // namespace includecpp', f'}} // namespace {namespace}')
            header_content = header_content.replace('namespace includecpp', f'namespace {namespace}')
            header_content = header_content.replace('} // namespace includecpp', f'}} // namespace {namespace}')

        out_dir = output_dir if output_dir else source_file.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        cpp_file = out_dir / f"{module_name}.cpp"
        cpp_file.write_text(cpp_content, encoding='utf-8')
        cpp_lines = len(cpp_content.split('\n'))
        result['outputs'].append((cpp_file.name, cpp_lines))
        result['lines'] += cpp_lines

        if not no_header:
            h_file = out_dir / f"{module_name}.h"
            h_file.write_text(header_content, encoding='utf-8')
            h_lines = len(header_content.split('\n'))
            result['outputs'].append((h_file.name, h_lines))
            result['lines'] += h_lines

        result['success'] = True

    except SyntaxError as e:
        result['error'] = f"Python syntax error: {e}"
    except Exception as e:
        result['error'] = str(e)

    return result


def _convert_to_python(content: str, module_name: str, source_file: Path,
                       output_dir: Path, verbose: bool) -> dict:
    """Convert C++ to Python."""
    from ..core.cppy_converter import CppToPythonConverter
    import re

    result = {
        'success': False,
        'functions': 0,
        'classes': 0,
        'lines': 0,
        'outputs': [],
        'error': None
    }

    try:
        func_pattern = r'(?:static|inline|virtual|explicit|constexpr|\s)*\w+(?:<[^>]+>)?(?:\s*[*&])?\s+(\w+)\s*\([^)]*\)\s*(?:const)?\s*\{'
        class_pattern = r'class\s+(\w+)'
        struct_pattern = r'struct\s+(\w+)'

        result['functions'] = len(re.findall(func_pattern, content))
        result['classes'] = len(re.findall(class_pattern, content)) + len(re.findall(struct_pattern, content))

        converter = CppToPythonConverter()
        py_content = converter.convert(content, module_name)

        out_dir = output_dir if output_dir else source_file.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        py_file = out_dir / f"{module_name}.py"
        py_file.write_text(py_content, encoding='utf-8')
        py_lines = len(py_content.split('\n'))
        result['outputs'].append((py_file.name, py_lines))
        result['lines'] = py_lines

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)

    return result


def _convert_with_ai(content: str, module_name: str, source_file,
                     output_dir, no_header: bool, namespace: str,
                     verbose: bool, to_cpp: bool, no_ai_verbose: bool = False,
                     use_think: bool = False, use_think3: bool = False,
                     use_websearch: bool = False) -> dict:
    """AI-assisted code conversion with section-by-section processing."""
    from pathlib import Path
    from ..core.cppy_converter import (
        PythonToCppConverter, CppToPythonConverter,
        get_ai_assistant, AI_CONVERSION_RULEBASE
    )
    from ..core.ai_integration import get_ai_manager, get_verbose_output
    import ast
    import re

    # Get AI verbose output handler
    ai_verbose = get_verbose_output(enabled=not no_ai_verbose)
    mode_str = "Python -> C++" if to_cpp else "C++ -> Python"

    result = {
        'success': False,
        'functions': 0,
        'classes': 0,
        'lines': 0,
        'outputs': [],
        'error': None,
        'api_changes': [],
        'workarounds': [],
    }

    try:
        ai_verbose.start(f"AI Convert [{mode_str}]")
        ai_verbose.phase('init', 'Setting up AI-assisted conversion')
        ai_verbose.detail('Module', module_name)
        ai_verbose.detail('Mode', mode_str)
        ai_verbose.detail('Namespace', namespace)

        ai_assistant = get_ai_assistant()
        ai_manager = get_ai_manager()

        if not ai_manager.is_enabled():
            ai_verbose.warning("AI not enabled. Run: includecpp ai token <YOUR_API_KEY>")
            ai_verbose.phase('fallback', 'Using standard conversion')
            ai_verbose.end(success=True, message="Fallback to standard")
            if to_cpp:
                return _convert_to_cpp(content, module_name, source_file, output_dir, no_header, namespace, verbose)
            else:
                return _convert_to_python(content, module_name, source_file, output_dir, verbose)

        ai_verbose.detail('Model', ai_manager.get_model())

        mode = 'py_to_cpp' if to_cpp else 'cpp_to_py'
        source_lines = content.count('\n')

        ai_verbose.phase('analyzing', 'Analyzing source code structure')
        ai_verbose.context_info(
            files=1,
            lines=source_lines,
            tokens=source_lines * 4,
            model=ai_manager.get_model()
        )

        # Analyze source for complexity and workarounds needed
        analysis = ai_assistant.analyze_source(content, mode)

        ai_verbose.detail('Complexity', analysis['complexity'])
        ai_verbose.detail('Sections', str(len(analysis['sections'])))
        if analysis['workarounds_needed']:
            ai_verbose.detail('Workarounds', f"{len(analysis['workarounds_needed'])} needed")

        if verbose:
            click.echo(f"  Complexity:     {analysis['complexity']}")
            click.echo(f"  Sections:       {len(analysis['sections'])}")
            if analysis['workarounds_needed']:
                click.echo(f"  Workarounds:    {len(analysis['workarounds_needed'])} needed")

        ai_verbose.phase('planning', 'Building AI conversion prompt')
        if no_header:
            ai_verbose.detail('Header', 'disabled (--no-h)')

        # Build AI prompt with IncludeCPP-specific rulebase
        ai_prompt = _build_cppy_ai_prompt(content, mode, module_name, namespace, analysis, no_header)

        ai_verbose.phase('thinking', 'AI is converting code section by section')
        ai_verbose.api_call(endpoint='chat/completions', tokens_in=source_lines * 4 + len(ai_prompt) // 4)

        # Call AI with appropriate think level
        # Default: --think2, optional: --think or --think3
        # Use skip_tool_execution to prevent AI from writing files directly
        # We parse the response and write files ourselves to the correct location
        project_root = source_file.parent

        # Determine thinking mode
        think = use_think
        think_twice = not use_think and not use_think3  # Default to think2
        think_three = use_think3

        ai_mode_str = "--think" if think else ("--think3" if think_three else "--think2")
        ai_verbose.detail('Think Mode', ai_mode_str)
        if use_websearch:
            ai_verbose.detail('Web Search', 'enabled')

        success, response, _ = ai_manager.generate(
            task=ai_prompt,
            files={str(source_file): content},
            project_root=project_root,
            think=think,
            think_twice=think_twice,
            think_three=think_three,
            use_websearch=use_websearch,
            skip_tool_execution=True  # Don't write files - we do it ourselves
        )

        if not success:
            ai_verbose.warning(f"AI conversion failed: {response}")
            ai_verbose.phase('fallback', 'Falling back to standard conversion')
            ai_verbose.end(success=True, message="Fallback successful")
            if to_cpp:
                return _convert_to_cpp(content, module_name, source_file, output_dir, no_header, namespace, verbose)
            else:
                return _convert_to_python(content, module_name, source_file, output_dir, verbose)

        ai_verbose.api_call(endpoint='chat/completions', tokens_out=len(response) // 4)

        # Check if AI needs clarification on unconvertible modules
        if 'CLARIFICATION_NEEDED:' in response:
            ai_verbose.phase('clarification', 'AI needs clarification')
            clarification_match = re.search(r'CLARIFICATION_NEEDED:\n((?:- .+\n?)+)', response)
            if clarification_match:
                questions = clarification_match.group(1).strip()
                click.echo("\n" + "=" * 60)
                click.secho("AI NEEDS CLARIFICATION:", fg='yellow', bold=True)
                click.echo(questions)
                click.echo("=" * 60)
                user_input = click.prompt("Your response (or 'skip' to use defaults)")
                if user_input.lower() != 'skip':
                    # Re-run AI with user's clarification
                    clarified_prompt = ai_prompt + f"\n\nUSER CLARIFICATION:\n{user_input}\n\nNow convert with this clarification:"
                    success, response, _ = ai_manager.generate(
                        task=clarified_prompt,
                        files={str(source_file): content},
                        project_root=project_root,
                        think=think,
                        think_twice=think_twice,
                        think_three=think_three,
                        use_websearch=use_websearch,
                        skip_tool_execution=True
                    )
                    if not success:
                        ai_verbose.warning("Clarified conversion failed, using standard converter")
                        if to_cpp:
                            return _convert_to_cpp(content, module_name, source_file, output_dir, no_header, namespace, verbose)
                        else:
                            return _convert_to_python(content, module_name, source_file, output_dir, verbose)

        ai_verbose.phase('parsing', 'Extracting converted code from AI response')

        # Parse AI response
        parsed = ai_assistant.parse_ai_response(response)

        # Extract converted code from AI response
        converted_code = _extract_ai_converted_code(response, to_cpp, module_name, namespace)

        if not converted_code:
            ai_verbose.status("Using hybrid conversion (AI + standard)", phase='complete')
            # Fall back to standard conversion with AI enhancements
            if to_cpp:
                converter = PythonToCppConverter()
                cpp_content, header_content = converter.convert(content, module_name)
                converted_code = {'cpp': cpp_content, 'header': header_content}
            else:
                converter = CppToPythonConverter()
                py_content = converter.convert(content, module_name)
                converted_code = {'python': py_content}

        # Add pybind11 wrappers for unconvertible Python features
        if to_cpp and analysis['workarounds_needed']:
            ai_verbose.phase('wrapping', f"Adding pybind11 wrappers for {len(analysis['workarounds_needed'])} features")
            converted_code = _add_pybind11_wrappers(converted_code, analysis['workarounds_needed'], module_name)
            for w in analysis['workarounds_needed']:
                workaround_desc = f"{w['type']}: {w.get('suggestion', 'pybind11 wrapper')}"
                result['workarounds'].append(workaround_desc)
                ai_verbose.detail('Workaround', workaround_desc)

        ai_verbose.phase('writing', 'Writing output files')

        # Write output files
        out_dir = Path(output_dir) if output_dir else source_file.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        if to_cpp:
            cpp_content = converted_code.get('cpp', '')
            header_content = converted_code.get('header', '')

            # Ensure namespace is correct
            if namespace != 'includecpp':
                cpp_content = cpp_content.replace('namespace includecpp', f'namespace {namespace}')
                cpp_content = cpp_content.replace('} // namespace includecpp', f'}} // namespace {namespace}')
                header_content = header_content.replace('namespace includecpp', f'namespace {namespace}')
                header_content = header_content.replace('} // namespace includecpp', f'}} // namespace {namespace}')

            cpp_file = out_dir / f"{module_name}.cpp"
            cpp_file.write_text(cpp_content, encoding='utf-8')
            cpp_lines = len(cpp_content.split('\n'))
            result['outputs'].append((cpp_file.name, cpp_lines))
            result['lines'] += cpp_lines
            ai_verbose.file_operation('write', cpp_file.name, success=True)

            if not no_header and header_content:
                h_file = out_dir / f"{module_name}.h"
                h_file.write_text(header_content, encoding='utf-8')
                h_lines = len(header_content.split('\n'))
                result['outputs'].append((h_file.name, h_lines))
                result['lines'] += h_lines
                ai_verbose.file_operation('write', h_file.name, success=True)

            # Count functions/classes from generated code
            result['functions'] = len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*(?:const)?\s*\{', cpp_content))
            result['classes'] = len(re.findall(r'class\s+\w+', cpp_content)) + len(re.findall(r'struct\s+\w+', cpp_content))

        else:
            py_content = converted_code.get('python', '')
            py_file = out_dir / f"{module_name}.py"
            py_file.write_text(py_content, encoding='utf-8')
            py_lines = len(py_content.split('\n'))
            result['outputs'].append((py_file.name, py_lines))
            result['lines'] = py_lines
            ai_verbose.file_operation('write', py_file.name, success=True)

            result['functions'] = len(re.findall(r'def\s+\w+', py_content))
            result['classes'] = len(re.findall(r'class\s+\w+', py_content))

        # Collect API changes
        if parsed.get('api_changes'):
            result['api_changes'] = parsed['api_changes']
            for change in result['api_changes']:
                ai_verbose.warning(f"API Change: {change}")

        result['success'] = True

        ai_verbose.changes_summary([{
            'file': module_name,
            'changes': [f"{result['functions']} functions", f"{result['classes']} classes", f"{result['lines']} lines"]
        }])
        ai_verbose.end(success=True, message=f"Converted {module_name} ({result['lines']} lines)")

    except Exception as e:
        result['error'] = str(e)
        ai_verbose.error(str(e))
        ai_verbose.end(success=False, message=str(e)[:50])
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

    return result


def _get_includecpp_readme() -> str:
    """Load IncludeCPP README.md for AI context."""
    try:
        import importlib.resources
        import includecpp
        readme_path = Path(includecpp.__file__).parent.parent / 'README.md'
        if readme_path.exists():
            readme = readme_path.read_text(encoding='utf-8')
            # Truncate to first sections (keep it focused)
            sections = readme.split('# Changelog')[0]  # Everything before changelog
            return sections[:8000]  # Limit to ~8k chars
    except Exception:
        pass
    return ""

def _build_cppy_ai_prompt(source: str, mode: str, module_name: str, namespace: str, analysis: dict, no_header: bool = False) -> str:
    """Build AI prompt with IncludeCPP-specific instructions."""

    # Load README for AI context (dynamically, not hardcoded)
    readme_context = _get_includecpp_readme()
    includecpp_docs = ""
    if readme_context:
        includecpp_docs = f'''
=== INCLUDECPP DOCUMENTATION (from README.md) ===
{readme_context}
=== END DOCUMENTATION ===
'''

    # Critical file extension rules
    file_rules = f'''
CRITICAL FILE EXTENSION RULES:
- C++ implementation file MUST be: {module_name}.cpp (NOT .cp, NOT .cc, NOT .cxx)
- C++ header file MUST be: {module_name}.h (NOT .hpp, NOT .hh)
- Python file MUST be: {module_name}.py
FOLLOW THESE EXTENSIONS EXACTLY.
'''

    # Unconvertible module handling
    unconvertible_info = ""
    for item, reason, line in getattr(analysis.get('converter', None), 'unconvertible', []) if isinstance(analysis, dict) else []:
        unconvertible_info += f"- Line {line}: {item} ({reason})\n"

    unconvertible_guidance = ""
    if unconvertible_info:
        unconvertible_guidance = f'''
UNCONVERTIBLE MODULES DETECTED:
{unconvertible_info}

For unconvertible modules (tkinter, pygame, ursina, etc.):
1. COMMENT OUT: Add /* UNCONVERTIBLE: tkinter */ comment
2. ALTERNATIVE: Suggest C++ alternatives (Qt for GUI, SDL2 for games, etc.)
3. SKIP: Remove the code with explanation comment

If you need clarification, output:
CLARIFICATION_NEEDED:
- <what you need clarified>
'''

    if mode == 'py_to_cpp':
        direction = "Python to C++"
        source_lang = "python"
        target_lang = "cpp"

        # CRITICAL: No pybind11 - IncludeCPP handles bindings automatically
        includecpp_note = '''
**CRITICAL - IncludeCPP HANDLES BINDINGS AUTOMATICALLY:**
- DO NOT include pybind11 headers
- DO NOT write PYBIND11_MODULE macros
- DO NOT use py:: namespace or py::object
- Just write CLEAN C++ code in namespace includecpp
- IncludeCPP will auto-generate Python bindings via: includecpp plugin <name> <file.cpp>

The user runs:
1. includecpp cppy convert file.py --cpp  (generates .cpp)
2. includecpp plugin mymod file.cpp       (auto-generates pybind11 bindings)
3. includecpp rebuild                     (compiles to Python module)
'''

        if no_header:
            # No header mode - put everything in .cpp
            specific_rules = f'''
INCLUDECPP-SPECIFIC REQUIREMENTS:
1. ALL code MUST be wrapped in: namespace {namespace} {{ ... }}
2. **CRITICAL: DO NOT create a header file** - --no-h flag is set
3. Put ALL declarations AND implementations in the .cpp file only
4. NO separate .h file should be created
{includecpp_note}

{file_rules}

TYPE CONVERSIONS:
- int -> int
- float -> double
- str -> std::string
- bool -> bool
- List[T] -> std::vector<T>
- Dict[K,V] -> std::unordered_map<K,V>
- Set[T] -> std::unordered_set<T>
- Optional[T] -> std::optional<T>
- Callable -> std::function<R(Args...)>
- bytes -> std::vector<uint8_t>

GENERIC/TEMPLATE FUNCTIONS:
- For functions that accept any type (like choices), use C++ templates:
  template<typename T> T getRandomChoice(const std::vector<T>& choices);
- NOT: auto getRandomChoice(const std::vector<auto>& choices)  // INVALID!

{unconvertible_guidance}'''
        else:
            # Normal mode with header
            specific_rules = f'''
INCLUDECPP-SPECIFIC REQUIREMENTS:
1. ALL code MUST be wrapped in: namespace {namespace} {{ ... }}
2. Create BOTH .cpp implementation AND .h header file
3. Use #include "{module_name}.h" at top of .cpp file
4. Header guard: #ifndef {module_name.upper()}_H / #define / #endif
{includecpp_note}

{file_rules}

GENERIC/TEMPLATE FUNCTIONS:
- For functions that accept any type, use C++ templates:
  template<typename T> T getRandomChoice(const std::vector<T>& choices);
- NOT: auto getRandomChoice(const std::vector<auto>& choices)  // INVALID!

TEMPLATE EXAMPLE (for generic functions):
```cpp
// In header (.h):
template<typename T>
T getRandomChoice(const std::vector<T>& choices);

// In implementation (.cpp):
template<typename T>
T Manager::getRandomChoice(const std::vector<T>& choices) {{
    // implementation
}}
// Explicit instantiations for common types:
template int Manager::getRandomChoice<int>(const std::vector<int>&);
template double Manager::getRandomChoice<double>(const std::vector<double>&);
template std::string Manager::getRandomChoice<std::string>(const std::vector<std::string>&);
```

TYPE CONVERSIONS:
- int -> int
- float -> double
- str -> std::string
- bool -> bool
- bytes -> std::vector<uint8_t>
- List[T] -> std::vector<T>
- Dict[K,V] -> std::unordered_map<K,V>
- Set[T] -> std::unordered_set<T>
- Optional[T] -> std::optional<T>
- Callable -> std::function<R(Args...)>

{unconvertible_guidance}'''
    else:
        direction = "C++ to Python"
        source_lang = "cpp"
        target_lang = "python"
        specific_rules = '''
CONVERSION REQUIREMENTS:
1. Add proper type hints from typing module
2. Convert namespace content to module-level
3. Convert this-> to self.
4. Convert std::cout to print()
5. Convert templates to Generic[T] where possible

TYPE CONVERSIONS:
- int/long/short/size_t -> int
- float/double -> float
- std::string -> str
- bool -> bool
- std::vector<T> -> List[T]
- std::unordered_map<K,V> -> Dict[K,V]
- std::optional<T> -> Optional[T]
- std::function -> Callable
'''

    workarounds_info = ""
    if analysis['workarounds_needed']:
        workarounds_info = "\nPATTERNS NEEDING WORKAROUNDS:\n"
        for w in analysis['workarounds_needed']:
            workarounds_info += f"- Line {w.get('line', '?')}: {w['type']} -> {w.get('suggestion', 'needs workaround')}\n"

    # Build output format based on mode and no_header flag
    if mode == 'py_to_cpp':
        if no_header:
            output_format = f'''OUTPUT FORMAT (--no-h flag is set, NO HEADER FILE):
**CRITICAL**: Output ONLY a single .cpp file. NO .h file allowed.

Output the implementation file (extension MUST be .cpp):
```cpp
// {module_name}.cpp
#include <string>
#include <vector>
// ... other includes ...

namespace {namespace} {{

// All declarations AND implementations go here
// No forward declarations needed since everything is in one file

}} // namespace {namespace}
```

REMEMBER:
- File extension is .cpp (NOT .cp, NOT .cc)
- DO NOT create a .h header file
- Put ALL code in the single .cpp file'''
        else:
            output_format = f'''OUTPUT FORMAT (with header):
1. First output the implementation file (extension MUST be .cpp):
```cpp
// {module_name}.cpp
#include "{module_name}.h"
// ... implementations ...
```

2. Then output the header file (extension MUST be .h):
```cpp
// {module_name}.h
#ifndef {module_name.upper()}_H
#define {module_name.upper()}_H
// ... declarations ...
#endif // {module_name.upper()}_H
```

REMEMBER:
- Implementation file extension is .cpp (NOT .cp, NOT .cc)
- Header file extension is .h (NOT .hpp, NOT .hh)'''
    else:
        output_format = f'''OUTPUT FORMAT:
Output the Python file (extension MUST be .py):
```python
# {module_name}.py
<full python content>
```'''

    prompt = f'''Convert the following {direction}.
You are IncludeCPP's AI code converter. Follow all requirements precisely.
{includecpp_docs}
MODULE NAME: {module_name}
NAMESPACE: {namespace}
{specific_rules}
{workarounds_info}

SOURCE CODE ({source_lang}):
```{source_lang}
{source}
```

{output_format}

If you need clarification about how to convert specific modules or patterns:
CLARIFICATION_NEEDED:
- <specific question about conversion approach>

At the end, list any API changes:
API_CHANGES:
- <change description>

And list any warnings:
WARNINGS:
- <warning>

Convert now, ensuring ALL functionality is preserved:'''

    return prompt


def _extract_ai_converted_code(response: str, to_cpp: bool, module_name: str, namespace: str) -> dict:
    """Extract converted code from AI response."""
    import re

    result = {}

    if to_cpp:
        # Extract .cpp content
        cpp_pattern = rf'```cpp\n(?:// ?{module_name}\.cpp\n)?(.*?)```'
        cpp_matches = re.findall(cpp_pattern, response, re.DOTALL)
        if cpp_matches:
            result['cpp'] = cpp_matches[0].strip()

        # Extract header content (second cpp block or explicit .h)
        h_pattern = rf'```cpp\n(?:// ?{module_name}\.h\n)?(.*?)```'
        h_matches = re.findall(h_pattern, response, re.DOTALL)
        if len(h_matches) > 1:
            result['header'] = h_matches[1].strip()
        elif len(h_matches) == 1 and '#ifndef' in h_matches[0]:
            result['header'] = h_matches[0].strip()
            result['cpp'] = ''  # Need to re-extract

        # If we only got one block with both, split them
        if 'cpp' in result and 'header' not in result:
            if '#ifndef' in result['cpp'] and '#include' in result['cpp']:
                # Contains both, try to split
                parts = result['cpp'].split('#ifndef', 1)
                if len(parts) == 2:
                    result['cpp'] = parts[0].strip()
                    result['header'] = '#ifndef' + parts[1]
    else:
        # Extract Python content
        py_pattern = r'```python\n(.*?)```'
        py_matches = re.findall(py_pattern, response, re.DOTALL)
        if py_matches:
            result['python'] = py_matches[0].strip()

    return result


def _add_pybind11_wrappers(converted_code: dict, workarounds: list, module_name: str) -> dict:
    """Add pybind11 wrappers for Python features that can't be directly converted."""

    wrapper_header = '''
// ============================================================================
// PYBIND11 WRAPPERS - For Python features without direct C++ equivalent
// ============================================================================
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

'''

    wrapper_funcs = []

    for w in workarounds:
        w_type = w['type']

        if w_type == 'generator':
            wrapper_funcs.append(f'''
// Generator workaround: Use callback pattern
template<typename T, typename Func>
void iterate_generator(Func callback) {{
    // Call callback for each yielded value
    // Usage: iterate_generator<int>([](int val) {{ ... }});
}}
''')
        elif w_type == 'async_await':
            wrapper_funcs.append(f'''
// Async workaround: Use std::async
#include <future>
template<typename Func>
auto run_async(Func func) -> std::future<decltype(func())> {{
    return std::async(std::launch::async, func);
}}
''')
        elif w_type == 'context_manager':
            wrapper_funcs.append(f'''
// Context manager workaround: RAII wrapper
template<typename T>
class ScopedResource {{
public:
    explicit ScopedResource(T resource) : resource_(resource), active_(true) {{}}
    ~ScopedResource() {{ if (active_) release(); }}
    T& get() {{ return resource_; }}
    void release() {{ active_ = false; /* cleanup */ }}
private:
    T resource_;
    bool active_;
}};
''')
        elif w_type == 'list_comprehension':
            wrapper_funcs.append(f'''
// List comprehension helper
template<typename T, typename Container, typename Func>
std::vector<T> transform_to_vector(const Container& src, Func transform) {{
    std::vector<T> result;
    result.reserve(src.size());
    for (const auto& item : src) {{
        result.push_back(transform(item));
    }}
    return result;
}}
''')
        elif w_type == 'dict_comprehension':
            wrapper_funcs.append(f'''
// Dict comprehension helper
template<typename K, typename V, typename Container, typename KeyFunc, typename ValFunc>
std::unordered_map<K, V> transform_to_map(const Container& src, KeyFunc key_fn, ValFunc val_fn) {{
    std::unordered_map<K, V> result;
    for (const auto& item : src) {{
        result[key_fn(item)] = val_fn(item);
    }}
    return result;
}}
''')

    # Add wrappers to header
    if wrapper_funcs and 'header' in converted_code:
        # Find position after includes
        header = converted_code['header']
        include_end = header.rfind('#include')
        if include_end != -1:
            # Find end of that line
            line_end = header.find('\n', include_end)
            if line_end != -1:
                header = header[:line_end+1] + wrapper_header + '\n'.join(wrapper_funcs) + header[line_end+1:]
                converted_code['header'] = header

    return converted_code


@cppy.command(name='analyze')
@click.argument('files', nargs=-1, required=True)
@click.option('--json', 'as_json', is_flag=True, help='Output as JSON')
def cppy_analyze(files, as_json):
    """Analyze code structure without converting.

    Shows functions, classes, methods, fields extracted from source files.
    Useful for understanding what will be converted.

    Examples:
        includecpp cppy analyze math_utils.py
        includecpp cppy analyze utils.cpp --json
    """
    from pathlib import Path
    import ast
    import re
    import json as json_module

    project_root = Path.cwd()
    results = []

    for f in files:
        fp = Path(f)
        if not fp.is_absolute():
            fp = project_root / f

        if not fp.exists():
            click.secho(f"File not found: {fp}", fg='red', err=True)
            continue

        content = fp.read_text(encoding='utf-8', errors='replace')
        file_info = {
            'file': str(fp.name),
            'path': str(fp),
            'language': 'python' if fp.suffix == '.py' else 'cpp',
            'functions': [],
            'classes': [],
            'structs': [],
            'global_vars': []
        }

        if fp.suffix == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                        func_info = {
                            'name': node.name,
                            'params': [arg.arg for arg in node.args.args],
                            'returns': ast.dump(node.returns) if node.returns else None,
                            'decorators': [ast.dump(d) for d in node.decorator_list],
                            'line': node.lineno
                        }
                        file_info['functions'].append(func_info)
                    elif isinstance(node, ast.ClassDef):
                        class_info = {
                            'name': node.name,
                            'bases': [ast.dump(b) if not isinstance(b, ast.Name) else b.id for b in node.bases],
                            'methods': [],
                            'fields': [],
                            'line': node.lineno
                        }
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                class_info['methods'].append({
                                    'name': item.name,
                                    'params': [a.arg for a in item.args.args if a.arg != 'self'],
                                    'line': item.lineno
                                })
                            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                                class_info['fields'].append({
                                    'name': item.target.id,
                                    'line': item.lineno
                                })
                        file_info['classes'].append(class_info)
            except SyntaxError as e:
                file_info['error'] = f"Syntax error: {e}"
        else:
            func_pattern = r'(\w+(?:<[^>]+>)?(?:\s*[*&])?)\s+(\w+)\s*\(([^)]*)\)'
            class_pattern = r'class\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+(\w+))?'
            struct_pattern = r'struct\s+(\w+)'

            for match in re.finditer(func_pattern, content):
                ret_type = match.group(1).strip()
                name = match.group(2)
                params = match.group(3).strip()
                if name not in ('if', 'while', 'for', 'switch', 'catch', 'class', 'struct'):
                    file_info['functions'].append({
                        'name': name,
                        'return_type': ret_type,
                        'params': params
                    })

            for match in re.finditer(class_pattern, content):
                file_info['classes'].append({
                    'name': match.group(1),
                    'base': match.group(2)
                })

            for match in re.finditer(struct_pattern, content):
                file_info['structs'].append({'name': match.group(1)})

        results.append(file_info)

    if as_json:
        click.echo(json_module.dumps(results, indent=2))
    else:
        for info in results:
            click.echo("=" * 60)
            click.secho(f"File: {info['file']}", fg='cyan', bold=True)
            click.echo(f"Language: {info['language'].upper()}")
            click.echo()

            if info.get('error'):
                click.secho(f"Error: {info['error']}", fg='red')
                continue

            if info['functions']:
                click.secho("Functions:", fg='green', bold=True)
                for func in info['functions']:
                    params = func.get('params', '')
                    if isinstance(params, list):
                        params = ', '.join(params)
                    ret = func.get('return_type') or func.get('returns') or ''
                    click.echo(f"  {func['name']}({params}) -> {ret}")

            if info['classes']:
                click.secho("Classes:", fg='yellow', bold=True)
                for cls in info['classes']:
                    base = f" : {cls.get('base')}" if cls.get('base') else ""
                    click.echo(f"  {cls['name']}{base}")
                    for method in cls.get('methods', []):
                        params = ', '.join(method.get('params', []))
                        click.echo(f"    - {method['name']}({params})")
                    for field in cls.get('fields', []):
                        click.echo(f"    . {field['name']}")

            if info['structs']:
                click.secho("Structs:", fg='magenta', bold=True)
                for struct in info['structs']:
                    click.echo(f"  {struct['name']}")

            click.echo()


@cppy.command(name='types')
def cppy_types():
    """Show type mapping between Python and C++.

    Displays the conversion tables used for type conversion:
    - Python types -> C++ types
    - C++ types -> Python types
    """
    from ..core.cppy_converter import PY_TO_CPP_TYPES, CPP_TO_PY_TYPES

    click.echo("=" * 60)
    click.secho("CPPY Type Mapping Tables", fg='cyan', bold=True)
    click.echo("=" * 60)
    click.echo()

    click.secho("Python -> C++ Types:", fg='green', bold=True)
    click.echo("-" * 40)
    for py_type, cpp_type in sorted(PY_TO_CPP_TYPES.items()):
        click.echo(f"  {py_type:20} -> {cpp_type}")
    click.echo()

    click.secho("C++ -> Python Types:", fg='yellow', bold=True)
    click.echo("-" * 40)
    for cpp_type, py_type in sorted(CPP_TO_PY_TYPES.items()):
        click.echo(f"  {cpp_type:20} -> {py_type}")
    click.echo()
    click.echo("=" * 60)


# ============================================================================
# EXEC - Interactive Code Execution
# ============================================================================

@cli.command(name='exec')
@click.argument('lang', type=click.Choice(['py', 'cpp', 'python', 'c++', 'cssl']))
@click.argument('path', required=False, type=click.Path())
@click.option('--all', 'import_all', is_flag=True, help='Import all available modules')
def exec_repl(lang, path, import_all):
    """Execute code interactively for quick testing.

    Run Python, C++ or CSSL code snippets without creating files.
    Perfect for testing your IncludeCPP modules quickly.

    \b
    Usage:
      includecpp exec py              # Interactive Python
      includecpp exec cpp             # Interactive C++
      includecpp exec cssl            # Interactive CSSL
      includecpp exec py mymodule     # Auto-import mymodule
      includecpp exec py plugins/x.cp # Auto-import from plugin
      includecpp exec py --all        # Import all modules

    \b
    Controls:
      ENTER       = Add new line
      Empty line  = Execute code (press ENTER twice)
      CTRL+C      = Cancel

    \b
    Examples:
      $ includecpp exec py fast_math
      >>> x = fast_math.add(1, 2)
      >>> print(x)
      >>>
      3
    """
    import sys
    import subprocess
    import tempfile
    from pathlib import Path as PathLib

    # Normalize language
    is_python = lang in ('py', 'python')
    is_cssl = lang == 'cssl'
    lang_name = 'Python' if is_python else ('CSSL' if is_cssl else 'C++')

    # Build imports/includes
    imports = []
    includes = []

    if import_all:
        # Import all available modules
        try:
            from ..core.cpp_api import CppApi
            api = CppApi()
            modules = list(api.registry.keys())
            if is_python:
                for mod in modules:
                    imports.append(f'from includecpp import {mod}')
                if modules:
                    click.secho(f"Auto-importing {len(modules)} modules: {', '.join(modules)}", fg='cyan')
            else:
                for mod in modules:
                    includes.append(f'#include "{mod}.h"')
                if modules:
                    click.secho(f"Auto-including {len(modules)} headers", fg='cyan')
        except Exception:
            click.secho("Warning: Could not load module registry", fg='yellow')

    elif path:
        path_obj = PathLib(path)
        module_name = None

        # Check if it's a .cp plugin file
        if path.endswith('.cp') or f'{os.sep}plugins{os.sep}' in path or '/plugins/' in path:
            # Extract module name from plugin path
            module_name = path_obj.stem
        elif path_obj.exists():
            # It's a file path
            module_name = path_obj.stem
        else:
            # Assume it's a module name directly
            module_name = path

        if module_name:
            if is_python:
                imports.append(f'from includecpp import {module_name}')
                click.secho(f"Auto-importing: {module_name}", fg='cyan')
            else:
                includes.append(f'#include "{module_name}.h"')
                click.secho(f"Auto-including: {module_name}.h", fg='cyan')

    # Show header
    click.echo()
    click.secho(f"=== IncludeCPP {lang_name} REPL ===", fg='cyan', bold=True)
    click.echo("Enter code line by line. Press ENTER on empty line to execute.")
    click.echo("Press CTRL+C to cancel.")
    click.echo()

    # Show pre-loaded imports
    if imports:
        click.secho("Pre-loaded:", fg='green')
        for imp in imports:
            click.echo(f"  {imp}")
        click.echo()

    if includes:
        click.secho("Pre-loaded:", fg='green')
        for inc in includes:
            click.echo(f"  {inc}")
        click.echo()

    # Collect code lines
    lines = []
    prompt = '>>> ' if is_python else 'cssl> '
    continuation = '... ' if is_python else '    > '

    try:
        while True:
            try:
                # Determine prompt
                current_prompt = prompt if not lines else continuation
                line = input(current_prompt)

                # Empty line = execute
                if not line.strip():
                    if lines:
                        break
                    continue

                lines.append(line)

            except EOFError:
                break

    except KeyboardInterrupt:
        click.echo()
        click.secho("Cancelled.", fg='yellow')
        return

    if not lines:
        click.secho("No code entered.", fg='yellow')
        return

    # Build full code
    code_lines = imports + [''] + lines if imports else lines

    click.echo()

    if is_python:
        # Execute Python code
        import builtins
        full_code = '\n'.join(code_lines)
        try:
            # Use exec with captured output
            import io
            from contextlib import redirect_stdout, redirect_stderr

            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()

            # Create execution context
            exec_globals = {'__name__': '__main__'}

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                builtins.exec(full_code, exec_globals)

            stdout_val = stdout_capture.getvalue()
            stderr_val = stderr_capture.getvalue()

            if stdout_val:
                click.echo(stdout_val, nl=False)
            if stderr_val:
                click.secho(stderr_val, fg='red', nl=False)

            if not stdout_val and not stderr_val:
                click.secho("(no output)", fg='bright_black')

        except Exception as e:
            click.secho(f"Error: {e}", fg='red')

    elif is_cssl:
        # Execute CSSL code
        full_code = '\n'.join(lines)
        try:
            from ..core.cssl_bridge import CsslLang
            cssl_lang = CsslLang()
            result = cssl_lang.exec(full_code)

            # v4.8.6: Don't re-print output buffer - runtime.output() already prints to stdout
            # Just check if there was output for the "(no output)" message
            output = cssl_lang.get_output()
            had_output = bool(output)
            cssl_lang.clear_output()  # Clear buffer for next execution

            if result is not None:
                click.echo(result)

            if not had_output and result is None:
                click.secho("(no output)", fg='bright_black')

        except Exception as e:
            click.secho(f"Error: {e}", fg='red')

    else:
        # Execute C++ code
        # Build a complete C++ program
        cpp_code_lines = [
            '#include <iostream>',
            '#include <vector>',
            '#include <string>',
            '#include <algorithm>',
            '#include <cmath>',
            'using namespace std;',
            ''
        ]
        cpp_code_lines.extend(includes)
        cpp_code_lines.append('')
        cpp_code_lines.append('int main() {')

        # Indent user code
        for line in lines:
            cpp_code_lines.append('    ' + line)

        cpp_code_lines.append('    return 0;')
        cpp_code_lines.append('}')

        full_code = '\n'.join(cpp_code_lines)

        # Write to temp file and compile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
            f.write(full_code)
            cpp_file = f.name

        exe_file = cpp_file.replace('.cpp', '.exe' if sys.platform == 'win32' else '')

        try:
            # Compile
            compile_cmd = ['g++', '-std=c++17', '-o', exe_file, cpp_file]
            result = subprocess.run(compile_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                click.secho("Compilation Error:", fg='red')
                click.echo(result.stderr)
            else:
                # Run
                run_result = subprocess.run([exe_file], capture_output=True, text=True, timeout=10)
                if run_result.stdout:
                    click.echo(run_result.stdout, nl=False)
                if run_result.stderr:
                    click.secho(run_result.stderr, fg='red', nl=False)
                if not run_result.stdout and not run_result.stderr:
                    click.secho("(no output)", fg='bright_black')

        except subprocess.TimeoutExpired:
            click.secho("Execution timed out (10s limit)", fg='red')
        except FileNotFoundError:
            click.secho("Error: g++ not found. Install a C++ compiler.", fg='red')
        except Exception as e:
            click.secho(f"Error: {e}", fg='red')
        finally:
            # Cleanup temp files
            import os
            try:
                os.unlink(cpp_file)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)
            except Exception:
                pass


# ============================================================================
# CSSL - Hidden Command Group
# ============================================================================

@click.group(hidden=True)
def cssl():
    """CSSL scripting commands."""
    pass


@cssl.command(name='run')
@click.argument('path', required=False, type=click.Path())
@click.option('--code', '-c', type=str, help='Execute code directly')
@click.option('--python', '-p', is_flag=True, help='Force Python interpreter (full builtin support)')
def cssl_run(path, code, python):
    """Run/execute CSSL code or file."""
    _cssl_execute(path, code, force_python=python)


@cssl.command(name='exec')
@click.argument('path', required=False, type=click.Path())
@click.option('--code', '-c', type=str, help='Execute code directly')
@click.option('--python', '-p', is_flag=True, help='Force Python interpreter (full builtin support)')
def cssl_exec(path, code, python):
    """Execute CSSL code or file (alias for 'run')."""
    _cssl_execute(path, code, force_python=python)


def _cssl_execute(path, code, force_python=False):
    """Internal: Execute CSSL code or file.

    v4.8.7: Uses CSSLRuntime directly for consistent behavior.
    CsslLang is an extra API layer for users, not needed for CLI execution.
    """
    from pathlib import Path as PathLib

    try:
        from ..core.cssl.cssl_runtime import CSSLRuntime
    except ImportError as e:
        click.secho(f"CSSL runtime not available: {e}", fg='red')
        return

    # Determine source
    if code:
        source = code
    elif path:
        path_obj = PathLib(path)
        if not path_obj.exists():
            click.secho(f"File not found: {path}", fg='red')
            return
        source = path_obj.read_text(encoding='utf-8')
    else:
        # Interactive mode
        click.secho("=== CSSL REPL ===", fg='magenta', bold=True)
        click.echo("Enter CSSL code. Empty line to execute. CTRL+C to cancel.")
        click.echo()

        lines = []
        prompt = 'cssl> '

        try:
            while True:
                try:
                    line = input(prompt)
                    if not line.strip():
                        if lines:
                            break
                        continue
                    lines.append(line)
                except EOFError:
                    break
        except KeyboardInterrupt:
            click.echo()
            click.secho("Cancelled.", fg='yellow')
            return

        if not lines:
            click.secho("No code entered.", fg='yellow')
            return

        source = '\n'.join(lines)

    # Execute using CSSLRuntime directly
    # v4.9.1: Use execute_program for standalone scripts (not service format)
    try:
        runtime = CSSLRuntime()
        # v4.9.3: Set current file path for relative payload resolution
        if path:
            import os
            runtime._current_file_path = os.path.abspath(path)
            runtime._current_file = os.path.basename(path)
        # Auto-detect: service format starts with service-init/run/include
        stripped = source.lstrip()
        if stripped.startswith('service-init') or stripped.startswith('service-run') or stripped.startswith('service-include'):
            result = runtime.execute(source)
        else:
            result = runtime.execute_program(source)
    except Exception as e:
        error_msg = str(e)
        # v4.8.6: Handle Unicode encoding errors in error messages
        try:
            # Clean display - single CSSL Error: prefix with colorama
            click.echo(f"{Fore.RED}CSSL Error: {error_msg}{Style.RESET_ALL}")
        except UnicodeEncodeError:
            # Fallback: replace non-ASCII characters with placeholders
            safe_msg = error_msg.encode('ascii', 'replace').decode('ascii')
            click.echo(f"CSSL Error: {safe_msg}")


@cssl.command(name='makemodule')
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output path for .cssl-mod')
def cssl_makemodule(path, output):
    """Create a .cssl-mod module from Python/C++ file."""
    from pathlib import Path as PathLib
    import pickle
    import base64

    path_obj = PathLib(path)
    suffix = path_obj.suffix.lower()

    if suffix not in ('.py', '.cpp', '.cp', '.h'):
        click.secho(f"Unsupported file type: {suffix}", fg='red')
        click.echo("Supported: .py, .cpp, .cp, .h")
        return

    # Read source
    source = path_obj.read_text(encoding='utf-8')

    # Create module data
    module_data = {
        'name': path_obj.stem,
        'type': 'python' if suffix == '.py' else 'cpp',
        'source': source,
        'version': '1.0',
    }

    # Encode as base64 pickle
    encoded = base64.b64encode(pickle.dumps(module_data)).decode('utf-8')

    # Write .cssl-mod file
    out_path = PathLib(output) if output else path_obj.with_suffix('.cssl-mod')
    out_path.write_text(f"CSSLMOD1\n{encoded}", encoding='utf-8')

    click.secho(f"Created: {out_path}", fg='green')
    click.echo(f"  Name: {module_data['name']}")
    click.echo(f"  Type: {module_data['type']}")


# ============================================================================
# CSSL Documentation Category Helpers
# ============================================================================

def _show_doc_categories():
    """Show overview of all CSSL syntax categories."""
    click.secho("CSSL Syntax Categories", fg='cyan', bold=True)
    click.secho("=" * 60, fg='cyan')
    click.echo()

    categories = [
        ("--snapshots, -s", "%", "Captured variable snapshots", "yellow"),
        ("--references, -r", "&", "Function/variable references", "green"),
        ("--overrides, -o", "++, embedded, &<>", "Override/replacement syntax", "magenta"),
        ("--datatypes, -t", "string, int, ...", "Data types", "blue"),
        ("--keywords, -k", "if, for, class, ...", "All keywords", "cyan"),
        ("--operators", "<==, <<==, +, ...", "All operators", "yellow"),
        ("--containers, -c", "stack<T>, vector<T>, ...", "Container types", "green"),
        ("--globals", "@, global", "Global variables", "magenta"),
        ("--injection, -i", "<==, <<==, +<==", "Code injection", "red"),
        ("--open", "open, OpenFind", "Open parameters", "blue"),
        ("--embedded, -e", "embedded", "Function/class replacement", "magenta"),
        ("--classes", "class, extends, ...", "OOP syntax", "cyan"),
        ("--enums", "enum, Enum::Value", "Enumerated types", "yellow"),
        ("--exceptions, -x", "try, catch, throw", "Exception handling", "red"),
        ("--modifiers, -m", "const, private, ...", "Access/type modifiers", "blue"),
        ("--builtins, -b", "printl, json::, ...", "Built-in functions", "green"),
    ]

    for flag, symbols, desc, color in categories:
        click.echo(f"  {click.style(flag, fg=color, bold=True):30} ", nl=False)
        click.echo(f"{click.style(symbols, fg='white'):25} ", nl=False)
        click.echo(f"{desc}")

    click.echo()
    click.secho("Usage:", fg='cyan')
    click.echo("  includecpp cssl doc --snapshots    # Show % documentation")
    click.echo("  includecpp cssl doc --embedded     # Show embedded docs")
    click.echo("  includecpp cssl doc \"keyword\"      # Search documentation")


def _show_doc_snapshots():
    """Show % snapshot syntax documentation."""
    click.secho("% - Captured Variable Snapshots", fg='yellow', bold=True)
    click.secho("=" * 60, fg='yellow')
    click.echo()

    click.secho("Description:", fg='cyan')
    click.echo("  The % prefix captures the current value of a variable or function")
    click.echo("  at definition time. Used in embedded functions to preserve the")
    click.echo("  original function before replacement.")
    click.echo()

    click.secho("Syntax:", fg='cyan')
    click.echo("  %variable      - Captured value of 'variable'")
    click.echo("  %function()    - Call the original function (before embedding)")
    click.echo()

    click.secho("Examples:", fg='cyan')
    click.echo()
    click.secho("  // In embedded function, call original:", fg='white')
    click.echo("  embedded define MyPrint(text) &print {")
    click.echo("      %print(\"[LOG] \" + text);  // Call original print")
    click.echo("  }")
    click.echo()
    click.secho("  // Capture variable value:", fg='white')
    click.echo("  x = 10;")
    click.echo("  define test() {")
    click.echo("      captured = %x;  // Captures current value of x")
    click.echo("  }")
    click.echo()

    click.secho("Use Cases:", fg='cyan')
    click.echo("  - Wrapping built-in functions with logging")
    click.echo("  - Preserving original behavior while adding functionality")
    click.echo("  - Creating function decorators/middleware")


def _show_doc_references():
    """Show & reference syntax documentation."""
    click.secho("& - References", fg='green', bold=True)
    click.secho("=" * 60, fg='green')
    click.echo()

    click.secho("Description:", fg='cyan')
    click.echo("  The & prefix creates references to functions, variables, or")
    click.echo("  specifies the function being replaced in embedded definitions.")
    click.echo()

    click.secho("Syntax:", fg='cyan')
    click.echo("  &function         - Reference to function (for embedded)")
    click.echo("  &variable         - Reference to variable")
    click.echo("  &ClassName        - Reference to class")
    click.echo("  &$PyObject        - Reference to Python object")
    click.echo()

    click.secho("Examples:", fg='cyan')
    click.echo()
    click.secho("  // Embedded function replacement:", fg='white')
    click.echo("  embedded define Logger(msg) &printl {")
    click.echo("      %printl(\"[\" + timestamp() + \"] \" + msg);")
    click.echo("  }")
    click.echo()
    click.secho("  // Function reference:", fg='white')
    click.echo("  callback = &myFunction;")
    click.echo("  callback();  // Calls myFunction")
    click.echo()
    click.secho("  // In open param switch conditions:", fg='white')
    click.echo("  switch(Params) {")
    click.echo("      case error & !text:  // error exists AND text doesn't")
    click.echo("          handleError();")
    click.echo("  }")


def _show_doc_overrides():
    """Show override/replacement syntax documentation."""
    click.secho("Overrides - ++, embedded, &<>", fg='magenta', bold=True)
    click.secho("=" * 60, fg='magenta')
    click.echo()

    click.secho("1. embedded - Function/Class Replacement", fg='cyan')
    click.echo("-" * 40)
    click.echo("  Replaces an existing function or class with a new implementation.")
    click.echo()
    click.echo("  Syntax:")
    click.echo("    embedded define NewName(args) &OldFunc { ... }")
    click.echo("    embedded class NewClass &OldClass { ... }")
    click.echo("    embedded NewEnum &OldEnum { ... }  // Enum replacement")
    click.echo()
    click.echo("  Example:")
    click.echo("    embedded define SafePrint(text) &print {")
    click.echo("        if (text != null) {")
    click.echo("            %print(text);  // Call original")
    click.echo("        }")
    click.echo("    }")
    click.echo()

    click.secho("2. ++ - Constructor/Method Extension", fg='cyan')
    click.echo("-" * 40)
    click.echo("  Appends code to existing constructors or methods.")
    click.echo()
    click.echo("  Syntax:")
    click.echo("    ClassName::constr ++ { additional code }")
    click.echo("    ClassName::method ++ { additional code }")
    click.echo()
    click.echo("  Example:")
    click.echo("    Player::constr ++ {")
    click.echo("        this->initialized = true;")
    click.echo("        printl(\"Player created!\");")
    click.echo("    }")
    click.echo()

    click.secho("3. open embedded define - Open Parameter Wrapper", fg='cyan')
    click.echo("-" * 40)
    click.echo("  Create wrapper with flexible open parameters.")
    click.echo()
    click.echo("  Syntax:")
    click.echo("    open embedded define Name(open Params) &target { ... }")
    click.echo("    embedded open define Name(open Params) &target { ... }")
    click.echo()
    click.echo("  Example:")
    click.echo("    open embedded define SmartPrint(open Args) &printl {")
    click.echo("        text = OpenFind<string>(0);")
    click.echo("        error = OpenFind<string, \"error\">;")
    click.echo("        switch(Args) {")
    click.echo("            case error: %printl(\"ERROR: \" + error);")
    click.echo("            default: %printl(text);")
    click.echo("        }")
    click.echo("    }")


def _show_doc_datatypes():
    """Show data types documentation."""
    click.secho("Data Types", fg='blue', bold=True)
    click.secho("=" * 60, fg='blue')
    click.echo()

    click.secho("Primitive Types:", fg='cyan')
    click.echo("  string    - Text strings: \"hello\", 'world'")
    click.echo("  int       - Integers: 42, -10, 0x1F")
    click.echo("  float     - Floating point: 3.14, -0.5")
    click.echo("  bool      - Boolean: true, false")
    click.echo("  null      - Null value: null, None")
    click.echo("  dynamic   - Any type (type inference)")
    click.echo("  void      - No return value (functions)")
    click.echo()

    click.secho("Container Types:", fg='cyan')
    click.echo("  array<T>      - Fixed-size array")
    click.echo("  list<T>       - Dynamic list (alias: vector<T>)")
    click.echo("  stack<T>      - LIFO stack")
    click.echo("  vector<T>     - Dynamic array")
    click.echo("  map<K,V>      - Key-value dictionary")
    click.echo("  set<T>        - Unique elements set")
    click.echo("  combo<T>      - Combination container")
    click.echo("  iterator<T>   - Iterator object")
    click.echo("  datastruct<T> - Custom data structure")
    click.echo()

    click.secho("Special Types:", fg='cyan')
    click.echo("  json          - JSON object")
    click.echo("  regex         - Regular expression")
    click.echo("  callable      - Function reference")
    click.echo("  object        - Generic object")
    click.echo()

    click.secho("Type Declaration:", fg='cyan')
    click.echo("  string name = \"John\";")
    click.echo("  int count = 0;")
    click.echo("  dynamic value = getAny();")
    click.echo("  list<string> names = [\"a\", \"b\"];")
    click.echo("  map<string, int> scores = {\"a\": 10};")


def _show_doc_keywords():
    """Show all CSSL keywords."""
    click.secho("CSSL Keywords", fg='cyan', bold=True)
    click.secho("=" * 60, fg='cyan')
    click.echo()

    click.secho("Control Flow:", fg='yellow')
    click.echo("  if, elif, else       - Conditionals")
    click.echo("  for, foreach, while  - Loops")
    click.echo("  switch, case, default - Pattern matching")
    click.echo("  break, continue      - Loop control")
    click.echo("  return               - Function return")
    click.echo("  try, catch, finally  - Exception handling")
    click.echo("  throw                - Raise exception")
    click.echo()

    click.secho("Functions:", fg='yellow')
    click.echo("  define       - Define function: define name() { }")
    click.echo("  void         - No return type: void name() { }")
    click.echo("  shuffled     - Randomized function")
    click.echo("  open         - Open/variadic parameters")
    click.echo("  closed       - No variadic params")
    click.echo()

    click.secho("Classes:", fg='yellow')
    click.echo("  class        - Define class: class Name { }")
    click.echo("  struct       - Define struct")
    click.echo("  enum         - Define enum: enum Name { A, B }")
    click.echo("  interface    - Define interface")
    click.echo("  extends      - Inherit from class")
    click.echo("  overwrites   - Override parent class")
    click.echo("  constr       - Constructor")
    click.echo("  new          - Create instance: new ClassName()")
    click.echo("  this         - Current instance reference")
    click.echo("  super        - Parent class reference")
    click.echo()

    click.secho("Modifiers:", fg='yellow')
    click.echo("  embedded     - Replace existing function/class")
    click.echo("  global       - Global variable declaration")
    click.echo("  private      - Private member")
    click.echo("  protected    - Protected member")
    click.echo("  public       - Public member")
    click.echo("  static       - Static member")
    click.echo("  const        - Constant value")
    click.echo("  final        - Cannot be overridden")
    click.echo("  virtual      - Virtual method")
    click.echo("  abstract     - Abstract class/method")
    click.echo()

    click.secho("Special:", fg='yellow')
    click.echo("  payload      - Load payload file")
    click.echo("  include      - Include CSSL file")
    click.echo("  import       - Import module")
    click.echo("  bytearrayed  - Multi-return analysis")
    click.echo("  in           - Iteration/membership")
    click.echo("  range        - Number range")


def _show_doc_operators():
    """Show all CSSL operators."""
    click.secho("CSSL Operators", fg='yellow', bold=True)
    click.secho("=" * 60, fg='yellow')
    click.echo()

    click.secho("Arithmetic:", fg='cyan')
    click.echo("  +   Addition / String concatenation")
    click.echo("  -   Subtraction")
    click.echo("  *   Multiplication")
    click.echo("  /   Division")
    click.echo("  %   Modulo (also: captured variable prefix)")
    click.echo("  **  Power/exponentiation")
    click.echo("  ++  Increment / Constructor extension")
    click.echo("  --  Decrement")
    click.echo()

    click.secho("Comparison:", fg='cyan')
    click.echo("  ==  Equal")
    click.echo("  !=  Not equal")
    click.echo("  <   Less than")
    click.echo("  >   Greater than")
    click.echo("  <=  Less or equal")
    click.echo("  >=  Greater or equal")
    click.echo()

    click.secho("Logical:", fg='cyan')
    click.echo("  &&  Logical AND")
    click.echo("  ||  Logical OR")
    click.echo("  !   Logical NOT")
    click.echo("  &   Bitwise AND / Reference / Param condition AND")
    click.echo("  |   Bitwise OR")
    click.echo("  not Keyword NOT")
    click.echo()

    click.secho("Assignment:", fg='cyan')
    click.echo("  =   Assign")
    click.echo("  +=  Add and assign")
    click.echo("  -=  Subtract and assign")
    click.echo("  *=  Multiply and assign")
    click.echo("  /=  Divide and assign")
    click.echo()

    click.secho("Injection/Infusion:", fg='cyan')
    click.echo("  <==   BruteInjection (replace method body)")
    click.echo("  +<==  Append to method body")
    click.echo("  -<==  Prepend to method body")
    click.echo("  <<==  CodeInfusion (replace, preserves context)")
    click.echo("  +<<== Append with CodeInfusion")
    click.echo()

    click.secho("Access:", fg='cyan')
    click.echo("  .     Member access: obj.property")
    click.echo("  ->    Member access: this->property")
    click.echo("  ::    Namespace/static: Class::method, json::parse")
    click.echo("  @     Global variable: @globalVar")
    click.echo("  $     Shared object: $sharedName")
    click.echo("  %     Captured/snapshot: %originalFunc")
    click.echo("  &     Reference: &function, &variable")
    click.echo("  #$    Python interop: #$python_var")


def _show_doc_containers():
    """Show container types documentation."""
    click.secho("Container Types", fg='green', bold=True)
    click.secho("=" * 60, fg='green')
    click.echo()

    click.secho("stack<T> - LIFO Stack", fg='cyan')
    click.echo("-" * 30)
    click.echo("  stack<int> s;")
    click.echo("  s.push(10);")
    click.echo("  s.push(20);")
    click.echo("  x = s.pop();    // 20")
    click.echo("  y = s.peek();   // 10")
    click.echo("  n = s.size();   // 1")
    click.echo()

    click.secho("vector<T> / list<T> - Dynamic Array", fg='cyan')
    click.echo("-" * 30)
    click.echo("  vector<string> v = [\"a\", \"b\", \"c\"];")
    click.echo("  v.push(\"d\");")
    click.echo("  v.insert(0, \"start\");")
    click.echo("  x = v[1];       // \"a\"")
    click.echo("  v.remove(0);")
    click.echo("  for (item in v) { printl(item); }")
    click.echo()

    click.secho("map<K,V> - Dictionary", fg='cyan')
    click.echo("-" * 30)
    click.echo("  map<string, int> m = {\"score\": 100};")
    click.echo("  m[\"lives\"] = 3;")
    click.echo("  m.set(\"level\", 1);")
    click.echo("  x = m.get(\"score\");  // 100")
    click.echo("  if (m.has(\"lives\")) { ... }")
    click.echo("  keys = m.keys();")
    click.echo("  vals = m.values();")
    click.echo()

    click.secho("set<T> - Unique Set", fg='cyan')
    click.echo("-" * 30)
    click.echo("  set<int> s = {1, 2, 3};")
    click.echo("  s.add(4);")
    click.echo("  s.add(2);      // No duplicate")
    click.echo("  if (s.contains(3)) { ... }")
    click.echo("  s.remove(1);")
    click.echo()

    click.secho("array<T> - Fixed Array", fg='cyan')
    click.echo("-" * 30)
    click.echo("  array<int> a = [1, 2, 3, 4, 5];")
    click.echo("  x = a[0];")
    click.echo("  a[2] = 10;")
    click.echo("  n = a.length();")


def _show_doc_globals():
    """Show global variable documentation."""
    click.secho("@ - Global Variables", fg='magenta', bold=True)
    click.secho("=" * 60, fg='magenta')
    click.echo()

    click.secho("Description:", fg='cyan')
    click.echo("  Global variables are accessible from anywhere in the code.")
    click.echo("  Declare with 'global' keyword, access with '@' prefix.")
    click.echo()

    click.secho("Declaration:", fg='cyan')
    click.echo("  global version = \"1.0.0\";")
    click.echo("  global config = {\"debug\": true};")
    click.echo("  global counter = 0;")
    click.echo()

    click.secho("Access:", fg='cyan')
    click.echo("  printl(@version);        // \"1.0.0\"")
    click.echo("  @counter = @counter + 1;")
    click.echo("  if (@config[\"debug\"]) { ... }")
    click.echo()

    click.secho("In Payloads:", fg='cyan')
    click.echo("  // file.cssl-pl")
    click.echo("  global appName = \"MyApp\";")
    click.echo("  global settings = {")
    click.echo("      \"theme\": \"dark\",")
    click.echo("      \"lang\": \"en\"")
    click.echo("  };")
    click.echo()
    click.echo("  // main.cssl")
    click.echo("  payload(\"file.cssl-pl\");")
    click.echo("  printl(@appName);  // \"MyApp\"")
    click.echo()

    click.secho("Namespaced Globals:", fg='cyan')
    click.echo("  payload(\"engine.cssl-pl\", \"Engine\");")
    click.echo("  printl(@Engine::version);")


def _show_doc_injection():
    """Show code injection operators documentation."""
    click.secho("╔══════════════════════════════════════════════════════════════╗", fg='red', bold=True)
    click.secho("║           CODE INJECTION & FILTERING SYSTEM                  ║", fg='red', bold=True)
    click.secho("╚══════════════════════════════════════════════════════════════╝", fg='red', bold=True)
    click.echo()

    # ===== SECTION 1: BASIC OPERATORS =====
    click.secho("┌─────────────────────────────────────────────────────────────┐", fg='yellow')
    click.secho("│  1. BASIC INJECTION OPERATORS                               │", fg='yellow', bold=True)
    click.secho("└─────────────────────────────────────────────────────────────┘", fg='yellow')
    click.echo()

    click.secho("  <==  Replace (BruteInjection)", fg='cyan', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    target <== source;           // Replace target with source")
    click.echo("    myList <== { 1, 2, 3 };      // Replace list contents")
    click.echo("    Player::update <== { ... };  // Replace method body")
    click.echo()

    click.secho("  +<== Add/Append", fg='cyan', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    target +<== source;          // Add source to target")
    click.echo("    myList +<== { 4, 5, 6 };     // Append items to list")
    click.echo("    myDict +<== { \"key\" = val }; // Merge dict into target")
    click.echo("    printl +<<== { log(msg); };  // Add code to function")
    click.echo()

    click.secho("  -<== Remove/Subtract", fg='cyan', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    target -<== source;          // Remove source items from target")
    click.echo("    myList -<== { 2, 4, 6 };     // Remove specific items")
    click.echo("    myDict -<== { \"key\" };       // Remove keys from dict")
    click.echo()

    click.secho("  ==> Receive (Reverse Direction)", fg='cyan', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    source ==> target;           // Move source to target")
    click.echo("    source ==>+ target;          // Add source to target")
    click.echo("    source -==> target;          // Move & clear source")
    click.echo()

    # ===== SECTION 2: CODE INFUSION =====
    click.secho("┌─────────────────────────────────────────────────────────────┐", fg='yellow')
    click.secho("│  2. CODE INFUSION OPERATORS                                 │", fg='yellow', bold=True)
    click.secho("└─────────────────────────────────────────────────────────────┘", fg='yellow')
    click.echo()

    click.secho("  <<== CodeInfusion (Function Hooking)", fg='magenta', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    func <<== { code };          // Replace function body")
    click.echo("    func +<<== { code };         // Add code AFTER function")
    click.echo("    func -<<== { code };         // Add code BEFORE function")
    click.echo()
    click.echo("    Example - Hook into printl:")
    click.secho("      printl +<<== { log(\"Called printl\"); };", fg='green')
    click.secho("      printl(\"Hello\");  // Also triggers hook", fg='green')
    click.echo()

    click.secho("  ==>> Right-side Infusion", fg='magenta', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    { code } ==>> func;          // Infuse code into function")
    click.echo()

    # ===== SECTION 3: FILTERING =====
    click.secho("┌─────────────────────────────────────────────────────────────┐", fg='yellow')
    click.secho("│  3. INJECTION FILTERS [type::helper=value]                  │", fg='yellow', bold=True)
    click.secho("└─────────────────────────────────────────────────────────────┘", fg='yellow')
    click.echo()

    click.secho("  Filter Syntax:", fg='cyan', bold=True)
    click.echo("    target <==[filter] source;")
    click.echo("    target <==[f1][f2][f3] source;   // Chained filters")
    click.echo("    source ==>[filter] target;")
    click.echo()

    click.secho("  String Filters:", fg='green', bold=True)
    click.echo("    [string::where=VALUE]     // Exact match")
    click.echo("    [string::contains=SUB]    // Contains substring")
    click.echo("    [string::not=VALUE]       // Exclude matches")
    click.echo("    [string::length=N]        // Filter by length")
    click.echo("    [string::startswith=PRE]  // Starts with prefix")
    click.echo("    [string::endswith=SUF]    // Ends with suffix")
    click.echo()

    click.secho("  Integer/Number Filters:", fg='green', bold=True)
    click.echo("    [integer::where=N]        // Exact value match")
    click.echo("    [integer::gt=N]           // Greater than N")
    click.echo("    [integer::lt=N]           // Less than N")
    click.echo("    [integer::range=A,B]      // Between A and B")
    click.echo()

    click.secho("  Array/List/Vector Filters:", fg='green', bold=True)
    click.echo("    [array::index=N]          // Get element at index N")
    click.echo("    [array::length=N]         // Filter by length")
    click.echo("    [array::first]            // Get first element")
    click.echo("    [array::last]             // Get last element")
    click.echo("    [array::slice=A,B]        // Get slice [A:B]")
    click.echo("    [vector::where=VAL]       // Filter containing VAL")
    click.echo()

    click.secho("  JSON/Dict Filters:", fg='green', bold=True)
    click.echo("    [json::key=KEY]           // Extract value by key")
    click.echo("    [json::value=VAL]         // Filter by value")
    click.echo("    [json::keys]              // Get all keys")
    click.echo("    [json::values]            // Get all values")
    click.echo()

    click.secho("  Dynamic/Type Filters:", fg='green', bold=True)
    click.echo("    [dynamic::VarName=VAL]    // Filter by variable value")
    click.echo("    [type::string]            // Filter only strings")
    click.echo("    [type::int]               // Filter only integers")
    click.echo()

    click.secho("  Instance/Object Filters:", fg='green', bold=True)
    click.echo("    [instance::class]         // Get classes from object")
    click.echo("    [instance::method]        // Get methods from object")
    click.echo("    [instance::var]           // Get variables from object")
    click.echo("    [instance::all]           // Get all (categorized)")
    click.echo("    [instance::\"ClassName\"]   // Get specific class")
    click.echo()

    click.secho("  Name Filter:", fg='green', bold=True)
    click.echo("    [name::\"MyName\"]          // Filter by name attribute")
    click.echo()

    # ===== SECTION 4: CHAINED FILTERS =====
    click.secho("┌─────────────────────────────────────────────────────────────┐", fg='yellow')
    click.secho("│  4. CHAINED FILTERS (Multiple Filters)                      │", fg='yellow', bold=True)
    click.secho("└─────────────────────────────────────────────────────────────┘", fg='yellow')
    click.echo()

    click.echo("  Apply multiple filters in sequence:")
    click.echo()
    click.secho("    data <==[json::key=\"users\"][array::index=0] source;", fg='green')
    click.echo("    // Extract 'users' key, then get first element")
    click.echo()
    click.secho("    items <==[type::string][string::contains=\"error\"] logs;", fg='green')
    click.echo("    // Get strings containing 'error'")
    click.echo()
    click.secho("    nums <==[array::slice=0,10][integer::gt=5] data;", fg='green')
    click.echo("    // Get first 10 elements, then filter > 5")
    click.echo()

    # ===== SECTION 5: EMBEDDED REPLACEMENT =====
    click.secho("┌─────────────────────────────────────────────────────────────┐", fg='yellow')
    click.secho("│  5. EMBEDDED FUNCTION REPLACEMENT                           │", fg='yellow', bold=True)
    click.secho("└─────────────────────────────────────────────────────────────┘", fg='yellow')
    click.echo()

    click.secho("  embedded define - Replace & Wrap Functions:", fg='magenta', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    embedded define NewFunc(args) &oldFunc {")
    click.echo("        // Pre-processing")
    click.echo("        result = %oldFunc(args);  // Call original")
    click.echo("        // Post-processing")
    click.echo("        return result;")
    click.echo("    }")
    click.echo()

    click.secho("  Example - Logging Wrapper:", fg='green')
    click.echo("    embedded define Logger(msg) &printl {")
    click.echo("        timestamp = now();")
    click.echo("        %printl(\"[\" + timestamp + \"] \" + msg);")
    click.echo("    }")
    click.echo()

    click.secho("  Class Method Replacement:", fg='magenta', bold=True)
    click.echo("  ─────────────────────────────────")
    click.echo("    embedded define NewMethod() &Class::method {")
    click.echo("        // Replace Class::method")
    click.echo("    }")
    click.echo()

    # ===== SECTION 6: PRACTICAL EXAMPLES =====
    click.secho("┌─────────────────────────────────────────────────────────────┐", fg='yellow')
    click.secho("│  6. PRACTICAL EXAMPLES                                      │", fg='yellow', bold=True)
    click.secho("└─────────────────────────────────────────────────────────────┘", fg='yellow')
    click.echo()

    click.secho("  List Operations:", fg='cyan')
    click.echo("    list items = { 1, 2, 3, 4, 5 };")
    click.echo("    items +<== { 6, 7, 8 };       // [1,2,3,4,5,6,7,8]")
    click.echo("    items -<== { 2, 4, 6 };       // [1,3,5,7,8]")
    click.echo("    items <== { 10, 20 };         // [10,20] (replace)")
    click.echo()

    click.secho("  Dict/DataStruct Operations:", fg='cyan')
    click.echo("    datastruct<dynamic> data;")
    click.echo("    data +<== { \"name\" = \"John\" };")
    click.echo("    data +<== { \"age\" = 30 };")
    click.echo("    config <==[json::key=\"name\"] data;  // \"John\"")
    click.echo()

    click.secho("  Function Hooking:", fg='cyan')
    click.echo("    // Add logging to all printl calls")
    click.echo("    printl +<<== { logToFile(msg); };")
    click.echo()
    click.echo("    // Validate before function runs")
    click.echo("    saveData -<<== { validate(data); };")
    click.echo()

    click.secho("  Snapshot & Restore:", fg='cyan')
    click.echo("    list original = { 1, 2, 3 };")
    click.echo("    snapshot(original);")
    click.echo("    original +<== { 4, 5 };")
    click.echo("    printl(original);      // [1,2,3,4,5]")
    click.echo("    printl(%original);     // [1,2,3] (snapshot)")


def _show_doc_open():
    """Show open parameters documentation."""
    click.secho("open - Open/Variadic Parameters", fg='blue', bold=True)
    click.secho("=" * 60, fg='blue')
    click.echo()

    click.secho("Description:", fg='cyan')
    click.echo("  'open' allows functions to accept any number/type of arguments.")
    click.echo("  Use OpenFind to extract values by index or name.")
    click.echo()

    click.secho("Function Declaration:", fg='cyan')
    click.echo("  define myFunc(open Params) { ... }")
    click.echo("  open define wrapper(open Args) &target { ... }")
    click.echo()

    click.secho("OpenFind - Extract Arguments:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  // By index (positional args):")
    click.echo("  first = OpenFind<string>(0);   // 1st arg as string")
    click.echo("  second = OpenFind<int>(1);     // 2nd arg as int")
    click.echo()
    click.echo("  // By name (keyword args):")
    click.echo("  name = OpenFind<string, \"name\">;")
    click.echo("  count = OpenFind<int, \"count\">;")
    click.echo()

    click.secho("switch(Params) - Parameter Matching:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  switch(Params) {")
    click.echo("      case error & !text:     // error exists, text doesn't")
    click.echo("          handleError();")
    click.echo("          break;")
    click.echo("      case text & !error:     // text exists, error doesn't")
    click.echo("          printl(text);")
    click.echo("          break;")
    click.echo("      case name || id:        // name OR id exists")
    click.echo("          lookup();")
    click.echo("          break;")
    click.echo("      default:")
    click.echo("          printl(\"Unknown\");")
    click.echo("  }")
    click.echo()

    click.secho("Complete Example:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  open embedded define SmartLog(open Input) &printl {")
    click.echo("      msg = OpenFind<string>(0);")
    click.echo("      level = OpenFind<string, \"level\">;")
    click.echo("      switch(Input) {")
    click.echo("          case level:")
    click.echo("              %printl(\"[\" + level + \"] \" + msg);")
    click.echo("              break;")
    click.echo("          default:")
    click.echo("              %printl(msg);")
    click.echo("      }")
    click.echo("  }")
    click.echo()
    click.echo("  // Usage:")
    click.echo("  printl(\"Hello\");                    // Hello")
    click.echo("  printl(\"Warning!\", level=\"WARN\");   // [WARN] Warning!")


def _show_doc_embedded():
    """Show embedded function/class replacement documentation."""
    click.secho("embedded - Function/Class Replacement", fg='magenta', bold=True)
    click.secho("=" * 60, fg='magenta')
    click.echo()

    click.secho("Description:", fg='cyan')
    click.echo("  'embedded' replaces an existing function or class definition.")
    click.echo("  The original can be called via %originalName().")
    click.echo()

    click.secho("Function Replacement:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  embedded define NewImpl(args) &oldFunction {")
    click.echo("      // Your new implementation")
    click.echo("      %oldFunction(args);  // Call original if needed")
    click.echo("  }")
    click.echo()
    click.echo("  Example - Logging wrapper:")
    click.echo("    embedded define Logger(msg) &print {")
    click.echo("        timestamp = now();")
    click.echo("        %print(\"[\" + timestamp + \"] \" + msg);")
    click.echo("    }")
    click.echo("    print(\"Hello\");  // Now prints with timestamp")
    click.echo()

    click.secho("With Open Parameters:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  Both syntaxes work:")
    click.echo("    open embedded define Name(open P) &target { }")
    click.echo("    embedded open define Name(open P) &target { }")
    click.echo()
    click.echo("  Example:")
    click.echo("    open embedded define SafeDiv(open Args) &div {")
    click.echo("        b = OpenFind<int>(1);")
    click.echo("        if (b == 0) {")
    click.echo("            return 0;  // Prevent division by zero")
    click.echo("        }")
    click.echo("        return %div(OpenFind<int>(0), b);")
    click.echo("    }")
    click.echo()

    click.secho("Class Replacement:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  embedded class NewClass &OldClass {")
    click.echo("      // New implementation")
    click.echo("  }")
    click.echo()

    click.secho("Enum Replacement:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  embedded NewColors &Colors {")
    click.echo("      RED = \"#FF0000\",")
    click.echo("      GREEN = \"#00FF00\",")
    click.echo("      BLUE = \"#0000FF\"")
    click.echo("  }")
    click.echo()

    click.secho("Use Cases:", fg='cyan')
    click.echo("  - Add logging/debugging to existing functions")
    click.echo("  - Add validation/error handling")
    click.echo("  - Implement middleware/interceptors")
    click.echo("  - Mock functions for testing")
    click.echo("  - Extend built-in functions (print, error, etc.)")


def _show_doc_classes():
    """Show class/OOP documentation."""
    click.secho("Classes and OOP", fg='cyan', bold=True)
    click.secho("=" * 60, fg='cyan')
    click.echo()

    click.secho("Class Definition:", fg='yellow')
    click.echo("-" * 40)
    click.echo("  class Player {")
    click.echo("      string name;")
    click.echo("      int health = 100;")
    click.echo("      int score;")
    click.echo()
    click.echo("      constr Player(string n) {")
    click.echo("          this->name = n;")
    click.echo("          this->score = 0;")
    click.echo("      }")
    click.echo()
    click.echo("      void takeDamage(int amount) {")
    click.echo("          this->health -= amount;")
    click.echo("      }")
    click.echo("  }")
    click.echo()

    click.secho("Inheritance (extends):", fg='yellow')
    click.echo("-" * 40)
    click.echo("  class Enemy : extends Entity {")
    click.echo("      int damage;")
    click.echo()
    click.echo("      constr Enemy(string name, int dmg) {")
    click.echo("          super(name);  // Call parent constructor")
    click.echo("          this->damage = dmg;")
    click.echo("      }")
    click.echo()
    click.echo("      void attack(target) {")
    click.echo("          target.takeDamage(this->damage);")
    click.echo("      }")
    click.echo("  }")
    click.echo()

    click.secho("Override (overwrites):", fg='yellow')
    click.echo("-" * 40)
    click.echo("  class Boss : overwrites Enemy {")
    click.echo("      // Completely replaces Enemy class")
    click.echo("      int health = 1000;")
    click.echo()
    click.echo("      void attack(target) {")
    click.echo("          // New attack implementation")
    click.echo("          super::attack(target);  // Optional: call parent")
    click.echo("          target.takeDamage(this->damage * 2);")
    click.echo("      }")
    click.echo("  }")
    click.echo()

    click.secho("Instantiation:", fg='yellow')
    click.echo("-" * 40)
    click.echo("  player = new Player(\"Hero\");")
    click.echo("  enemy = new Enemy(\"Goblin\", 10);")
    click.echo()
    click.echo("  // Namespaced class:")
    click.echo("  engine = new Engine::GameEngine();")
    click.echo()

    click.secho("Constructor Extension (++):", fg='yellow')
    click.echo("-" * 40)
    click.echo("  Player::constr ++ {")
    click.echo("      // Additional initialization")
    click.echo("      this->initialized = true;")
    click.echo("      printl(\"Player \" + this->name + \" created!\");")
    click.echo("  }")
    click.echo()

    click.secho("Enums:", fg='yellow')
    click.echo("-" * 40)
    click.echo("  enum Direction {")
    click.echo("      UP = 0,")
    click.echo("      DOWN = 1,")
    click.echo("      LEFT = 2,")
    click.echo("      RIGHT = 3")
    click.echo("  }")
    click.echo()
    click.echo("  dir = Direction.UP;")
    click.echo("  if (dir == Direction.LEFT) { ... }")


def _show_doc_enums():
    """Show enum documentation."""
    click.secho("Enums - Enumerated Types", fg='yellow', bold=True)
    click.secho("=" * 60, fg='yellow')
    click.echo()

    click.secho("Basic Enum Definition:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  enum Direction {")
    click.echo("      UP = 0,")
    click.echo("      DOWN = 1,")
    click.echo("      LEFT = 2,")
    click.echo("      RIGHT = 3")
    click.echo("  }")
    click.echo()

    click.secho("Enum Access (EnumName::Value):", fg='cyan')
    click.echo("-" * 40)
    click.echo("  dir = Direction::UP;")
    click.echo("  // or")
    click.echo("  dir = Direction.UP;")
    click.echo()
    click.echo("  if (dir == Direction::LEFT) {")
    click.echo("      printl(\"Going left!\");")
    click.echo("  }")
    click.echo()

    click.secho("String Enums:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  enum Colors {")
    click.echo("      RED = \"#FF0000\",")
    click.echo("      GREEN = \"#00FF00\",")
    click.echo("      BLUE = \"#0000FF\"")
    click.echo("  }")
    click.echo()
    click.echo("  color = Colors::RED;  // \"#FF0000\"")
    click.echo()

    click.secho("Embedded Enum Replacement:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  // Replace existing enum")
    click.echo("  embedded NewColors &Colors {")
    click.echo("      RED = \"crimson\",")
    click.echo("      GREEN = \"lime\",")
    click.echo("      BLUE = \"navy\"")
    click.echo("  }")
    click.echo()

    click.secho("Enum with Expressions:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  base = 100;")
    click.echo("  enum Scores {")
    click.echo("      LOW = base,")
    click.echo("      MEDIUM = base * 2,")
    click.echo("      HIGH = base * 5")
    click.echo("  }")
    click.echo()

    click.secho("Enum Iteration:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  for (value in Direction) {")
    click.echo("      printl(value);")
    click.echo("  }")


def _show_doc_exceptions():
    """Show exception handling documentation."""
    click.secho("Exception Handling", fg='red', bold=True)
    click.secho("=" * 60, fg='red')
    click.echo()

    click.secho("try/catch/finally:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  try {")
    click.echo("      result = riskyOperation();")
    click.echo("      process(result);")
    click.echo("  } catch (e) {")
    click.echo("      printl(\"Error: \" + e);")
    click.echo("  } finally {")
    click.echo("      cleanup();")
    click.echo("  }")
    click.echo()

    click.secho("except (alias for catch):", fg='cyan')
    click.echo("-" * 40)
    click.echo("  try {")
    click.echo("      data = json::parse(input);")
    click.echo("  } except (err) {")
    click.echo("      printl(\"Parse error: \" + err);")
    click.echo("      data = {};")
    click.echo("  }")
    click.echo()

    click.secho("throw - Raise Exception:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  define divide(a, b) {")
    click.echo("      if (b == 0) {")
    click.echo("          throw \"Division by zero!\";")
    click.echo("      }")
    click.echo("      return a / b;")
    click.echo("  }")
    click.echo()
    click.echo("  try {")
    click.echo("      result = divide(10, 0);")
    click.echo("  } catch (e) {")
    click.echo("      printl(e);  // \"Division by zero!\"")
    click.echo("  }")
    click.echo()

    click.secho("Catching Python Exceptions:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  try {")
    click.echo("      // Python exceptions are also caught")
    click.echo("      list = [1, 2, 3];")
    click.echo("      x = list[10];  // IndexError")
    click.echo("  } catch (e) {")
    click.echo("      printl(\"Caught: \" + str(e));")
    click.echo("  }")
    click.echo()

    click.secho("Nested try/catch:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  try {")
    click.echo("      try {")
    click.echo("          innerOperation();")
    click.echo("      } catch (inner) {")
    click.echo("          throw \"Inner failed: \" + inner;")
    click.echo("      }")
    click.echo("  } catch (outer) {")
    click.echo("      printl(outer);")
    click.echo("  }")


def _show_doc_modifiers():
    """Show modifier keywords documentation."""
    click.secho("Modifiers - Access and Type Qualifiers", fg='blue', bold=True)
    click.secho("=" * 60, fg='blue')
    click.echo()

    click.secho("Access Modifiers:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  class MyClass {")
    click.echo("      private int secret = 42;     // Only in class")
    click.echo("      protected int data = 10;     // Class + subclasses")
    click.echo("      public string name;          // Anywhere (default)")
    click.echo("  }")
    click.echo()

    click.secho("const - Immutable Values:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  const PI = 3.14159;")
    click.echo("  const MAX_SIZE = 100;")
    click.echo("  const CONFIG = {\"debug\": true};")
    click.echo()
    click.echo("  // Cannot reassign:")
    click.echo("  PI = 3;  // Error!")
    click.echo()

    click.secho("static - Class-Level Members:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  class Counter {")
    click.echo("      static int count = 0;")
    click.echo()
    click.echo("      constr Counter() {")
    click.echo("          Counter::count += 1;")
    click.echo("      }")
    click.echo()
    click.echo("      static int getCount() {")
    click.echo("          return Counter::count;")
    click.echo("      }")
    click.echo("  }")
    click.echo()
    click.echo("  c1 = new Counter();")
    click.echo("  c2 = new Counter();")
    click.echo("  printl(Counter::getCount());  // 2")
    click.echo()

    click.secho("final - Cannot Override:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  class Base {")
    click.echo("      final void important() {")
    click.echo("          // Cannot be overridden in subclass")
    click.echo("      }")
    click.echo("  }")
    click.echo()

    click.secho("virtual - Override in Subclass:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  class Animal {")
    click.echo("      virtual void speak() {")
    click.echo("          printl(\"...\");")
    click.echo("      }")
    click.echo("  }")
    click.echo()
    click.echo("  class Dog : extends Animal {")
    click.echo("      void speak() {")
    click.echo("          printl(\"Woof!\");")
    click.echo("      }")
    click.echo("  }")
    click.echo()

    click.secho("abstract - Must Override:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  abstract class Shape {")
    click.echo("      abstract float area();  // Must implement")
    click.echo("  }")
    click.echo()
    click.echo("  class Circle : extends Shape {")
    click.echo("      float radius;")
    click.echo("      float area() {")
    click.echo("          return 3.14 * this->radius * this->radius;")
    click.echo("      }")
    click.echo("  }")
    click.echo()

    click.secho("readonly - Read After Init:", fg='cyan')
    click.echo("-" * 40)
    click.echo("  class Config {")
    click.echo("      readonly string path;")
    click.echo()
    click.echo("      constr Config(string p) {")
    click.echo("          this->path = p;  // OK in constructor")
    click.echo("      }")
    click.echo("  }")
    click.echo("  // cfg->path = \"x\";  // Error after construction")


def _show_doc_builtins():
    """Show built-in functions documentation."""
    click.secho("Built-in Functions", fg='green', bold=True)
    click.secho("=" * 60, fg='green')
    click.echo()

    click.secho("Output:", fg='cyan')
    click.echo("  print(x)         - Print without newline")
    click.echo("  printl(x)        - Print with newline")
    click.echo("  error(msg)       - Print error message")
    click.echo("  warn(msg)        - Print warning")
    click.echo("  debug(x)         - Debug print")
    click.echo()

    click.secho("Type Conversion:", fg='cyan')
    click.echo("  str(x)           - Convert to string")
    click.echo("  int(x)           - Convert to integer")
    click.echo("  float(x)         - Convert to float")
    click.echo("  bool(x)          - Convert to boolean")
    click.echo("  list(x)          - Convert to list")
    click.echo()

    click.secho("String Functions:", fg='cyan')
    click.echo("  len(s)           - Length of string/list")
    click.echo("  upper(s)         - Uppercase")
    click.echo("  lower(s)         - Lowercase")
    click.echo("  trim(s)          - Remove whitespace")
    click.echo("  split(s, d)      - Split by delimiter")
    click.echo("  join(list, d)    - Join with delimiter")
    click.echo("  replace(s,o,n)   - Replace occurrences")
    click.echo("  substr(s,i,l)    - Substring")
    click.echo("  contains(s,sub)  - Check if contains")
    click.echo("  startswith(s,p)  - Check prefix")
    click.echo("  endswith(s,p)    - Check suffix")
    click.echo()

    click.secho("Math:", fg='cyan')
    click.echo("  abs(x)           - Absolute value")
    click.echo("  min(a, b)        - Minimum")
    click.echo("  max(a, b)        - Maximum")
    click.echo("  floor(x)         - Round down")
    click.echo("  ceil(x)          - Round up")
    click.echo("  round(x)         - Round to nearest")
    click.echo("  sqrt(x)          - Square root")
    click.echo("  pow(x, y)        - Power")
    click.echo("  random()         - Random 0-1")
    click.echo("  randint(a, b)    - Random int in range")
    click.echo()

    click.secho("Collections:", fg='cyan')
    click.echo("  len(x)           - Length")
    click.echo("  append(l, x)     - Add to list")
    click.echo("  pop(l)           - Remove last")
    click.echo("  insert(l, i, x)  - Insert at index")
    click.echo("  remove(l, x)     - Remove first occurrence")
    click.echo("  sort(l)          - Sort list")
    click.echo("  reverse(l)       - Reverse list")
    click.echo("  range(a, b)      - Number range")
    click.echo("  keys(m)          - Map keys")
    click.echo("  values(m)        - Map values")
    click.echo()

    click.secho("JSON (json::):", fg='cyan')
    click.echo("  json::parse(s)   - Parse JSON string")
    click.echo("  json::stringify(x) - Convert to JSON")
    click.echo("  json::load(path) - Load JSON file")
    click.echo("  json::save(x,p)  - Save to JSON file")
    click.echo()

    click.secho("File I/O:", fg='cyan')
    click.echo("  read(path)       - Read file contents")
    click.echo("  write(path, s)   - Write to file")
    click.echo("  append(path, s)  - Append to file")
    click.echo("  exists(path)     - Check if file exists")
    click.echo()

    click.secho("Time:", fg='cyan')
    click.echo("  now()            - Current timestamp")
    click.echo("  timestamp()      - Formatted timestamp")
    click.echo("  sleep(ms)        - Wait milliseconds")
    click.echo()

    click.secho("Type Checking:", fg='cyan')
    click.echo("  type(x)          - Get type name")
    click.echo("  isinstance(x,t)  - Check instance")
    click.echo("  isstring(x)      - Is string?")
    click.echo("  isint(x)         - Is integer?")
    click.echo("  islist(x)        - Is list?")
    click.echo("  isnull(x)        - Is null?")
    click.echo("  iscallable(x)    - Is function?")


@cssl.command(name='doc')
@click.argument('search', required=False, default=None)
@click.option('--list', '-l', 'list_sections', is_flag=True, help='List all documentation sections')
@click.option('--get', '-g', 'show_categories', is_flag=True, help='Show all syntax categories')
@click.option('--snapshots', '--snapshot', '-s', 'cat_snapshots', is_flag=True, help='Show % snapshot syntax')
@click.option('--references', '--refs', '-r', 'cat_refs', is_flag=True, help='Show & reference syntax')
@click.option('--overrides', '--override', '-o', 'cat_overrides', is_flag=True, help='Show ++, embedded, &<> override syntax')
@click.option('--datatypes', '--types', '-t', 'cat_types', is_flag=True, help='Show all data types')
@click.option('--keywords', '-k', 'cat_keywords', is_flag=True, help='Show all keywords')
@click.option('--operators', '--ops', 'cat_operators', is_flag=True, help='Show all operators')
@click.option('--containers', '-c', 'cat_containers', is_flag=True, help='Show container types (stack, vector, map)')
@click.option('--globals', 'cat_globals', is_flag=True, help='Show @, global syntax')
@click.option('--injection', '--inject', '-i', 'cat_injection', is_flag=True, help='Show <==, <<==, +<== injection syntax')
@click.option('--open', 'cat_open', is_flag=True, help='Show open parameters and OpenFind')
@click.option('--embedded', '-e', 'cat_embedded', is_flag=True, help='Show embedded function/class replacement')
@click.option('--classes', 'cat_classes', is_flag=True, help='Show class, extends, overwrites syntax')
@click.option('--enums', 'cat_enums', is_flag=True, help='Show enum definitions and EnumName::Value')
@click.option('--exceptions', '--except', '-x', 'cat_exceptions', is_flag=True, help='Show try/catch/except/throw')
@click.option('--modifiers', '-m', 'cat_modifiers', is_flag=True, help='Show const, private, static, etc.')
@click.option('--builtins', '-b', 'cat_builtins', is_flag=True, help='Show built-in functions')
def cssl_doc(search, list_sections, show_categories, cat_snapshots, cat_refs, cat_overrides,
             cat_types, cat_keywords, cat_operators, cat_containers, cat_globals,
             cat_injection, cat_open, cat_embedded, cat_classes, cat_enums, cat_exceptions,
             cat_modifiers, cat_builtins):
    """Show CSSL documentation.

    \b
    Usage:
      includecpp cssl doc              # Show full documentation
      includecpp cssl doc "open"       # Search for 'open' keyword
      includecpp cssl doc --get        # Show syntax categories overview
      includecpp cssl doc --snapshots  # Show % snapshot documentation
      includecpp cssl doc --embedded   # Show embedded replacement docs
      includecpp cssl doc --list       # List all sections

    \b
    Categories:
      --get, -g          Overview of all syntax categories
      --snapshots, -s    % captured variable snapshots
      --references, -r   & function/variable references
      --overrides, -o    ++, embedded, &<> override syntax
      --datatypes, -t    Data types (string, int, float, bool, ...)
      --keywords, -k     All CSSL keywords
      --operators        All operators (+, -, *, /, <==, <<==, ...)
      --containers, -c   Container types (stack, vector, map, ...)
      --globals          @ global variables
      --injection, -i    Code injection (<==, <<==, +<==)
      --open             open parameters and OpenFind
      --embedded, -e     embedded function/class replacement
      --classes          class, extends, overwrites, constr
      --enums            enum definitions and EnumName::Value
      --exceptions, -x   try/catch/except/throw/finally
      --modifiers, -m    const, private, static, virtual, etc.
      --builtins, -b     Built-in functions (printl, len, json::, ...)
    """
    from pathlib import Path as PathLib
    import os
    import re

    # Find the documentation file in the cssl package directory
    cssl_dir = PathLib(__file__).parent.parent / 'core' / 'cssl'
    doc_path = cssl_dir / 'CSSL_DOCUMENTATION.md'

    if not doc_path.exists():
        # Try alternative locations
        alt_paths = [
            PathLib(__file__).parent.parent.parent / 'CSSL_DOCUMENTATION.md',
            PathLib(__file__).parent.parent / 'CSSL_DOCUMENTATION.md',
            PathLib(os.getcwd()) / 'CSSL_DOCUMENTATION.md',
        ]
        for alt in alt_paths:
            if alt.exists():
                doc_path = alt
                break

    if doc_path.exists():
        content = doc_path.read_text(encoding='utf-8')

        # List sections mode
        if list_sections:
            click.secho("CSSL Documentation Sections", fg='cyan', bold=True)
            click.secho("=" * 40, fg='cyan')
            sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
            for i, section in enumerate(sections, 1):
                click.echo(f"  {i:2d}. {section}")
            click.echo()
            click.echo("Use: includecpp cssl doc \"<keyword>\" to search")
            return

        # Category documentation mode
        if show_categories:
            _show_doc_categories()
            return

        if cat_snapshots:
            _show_doc_snapshots()
            return

        if cat_refs:
            _show_doc_references()
            return

        if cat_overrides:
            _show_doc_overrides()
            return

        if cat_types:
            _show_doc_datatypes()
            return

        if cat_keywords:
            _show_doc_keywords()
            return

        if cat_operators:
            _show_doc_operators()
            return

        if cat_containers:
            _show_doc_containers()
            return

        if cat_globals:
            _show_doc_globals()
            return

        if cat_injection:
            _show_doc_injection()
            return

        if cat_open:
            _show_doc_open()
            return

        if cat_embedded:
            _show_doc_embedded()
            return

        if cat_classes:
            _show_doc_classes()
            return

        if cat_enums:
            _show_doc_enums()
            return

        if cat_exceptions:
            _show_doc_exceptions()
            return

        if cat_modifiers:
            _show_doc_modifiers()
            return

        if cat_builtins:
            _show_doc_builtins()
            return

        # Search mode
        if search:
            click.secho(f"Searching for: '{search}'", fg='cyan', bold=True)
            click.secho("=" * 50, fg='cyan')
            click.echo()

            # Split into subsections (### headers) for focused results
            # Note: Allow optional leading whitespace since doc may be indented
            subsections = re.split(r'(?=^\s*### )', content, flags=re.MULTILINE)

            # Also split into main sections (## headers)
            main_sections = re.split(r'(?=^\s*## )', content, flags=re.MULTILINE)

            # Find matching subsections (### level) - most focused
            matching_subsections = []
            for subsection in subsections:
                if search.lower() in subsection.lower():
                    # Extract title (allow leading whitespace)
                    title_match = re.match(r'^\s*###\s+(.+)$', subsection, re.MULTILINE)
                    if title_match:
                        # Trim subsection to just the content until next ### or ##
                        lines = subsection.split('\n')
                        trimmed_lines = []
                        for line in lines:
                            stripped = line.lstrip()
                            if stripped.startswith('## ') and not stripped.startswith('### '):
                                break
                            trimmed_lines.append(line)
                        matching_subsections.append((title_match.group(1), '\n'.join(trimmed_lines)))

            if matching_subsections:
                click.secho(f"Found {len(matching_subsections)} matching subsection(s):", fg='green')
                click.echo()

                # Show focused subsections (limit output)
                for title, sub_content in matching_subsections[:5]:
                    click.secho(f"### {title}", fg='yellow', bold=True)
                    # Highlight search term in content
                    highlighted = re.sub(
                        f'({re.escape(search)})',
                        click.style(r'\1', fg='green', bold=True),
                        sub_content,
                        flags=re.IGNORECASE
                    )
                    # Limit lines per subsection
                    lines = highlighted.split('\n')
                    if len(lines) > 30:
                        click.echo('\n'.join(lines[:30]))
                        click.secho(f"  ... ({len(lines) - 30} more lines)", fg='cyan')
                    else:
                        click.echo(highlighted)
                    click.echo()
                    click.secho("-" * 40, fg='cyan')
                    click.echo()

                if len(matching_subsections) > 5:
                    click.secho(f"... and {len(matching_subsections) - 5} more subsections", fg='cyan')
                    click.echo("Use --list to see all sections")
            else:
                # Fall back to main section search (## level)
                found_sections = []
                for section in main_sections:
                    if search.lower() in section.lower():
                        title_match = re.match(r'^\s*##\s+(.+)$', section, re.MULTILINE)
                        if title_match:
                            found_sections.append((title_match.group(1), section))

                if found_sections:
                    click.secho(f"Found in {len(found_sections)} section(s):", fg='green')
                    for title, _ in found_sections:
                        click.echo(f"  - {title}")
                    click.echo()

                    # Show first matching section, trimmed
                    title, section = found_sections[0]
                    click.secho(f"## {title}", fg='yellow', bold=True)
                    highlighted = re.sub(
                        f'({re.escape(search)})',
                        click.style(r'\1', fg='green', bold=True),
                        section,
                        flags=re.IGNORECASE
                    )
                    lines = highlighted.split('\n')
                    if len(lines) > 40:
                        click.echo('\n'.join(lines[:40]))
                        click.secho(f"\n... ({len(lines) - 40} more lines in this section)", fg='cyan')
                    else:
                        click.echo(highlighted)
                else:
                    click.secho(f"No matches found for '{search}'", fg='yellow')
                    click.echo()
                    click.echo("Try searching for:")
                    click.echo("  - Keywords: class, function, define, open, global, shuffled")
                    click.echo("  - Syntax: $, @, ::, this->, <<==, <==, #$")
                    click.echo("  - Types: string, int, stack, vector, map, json")
                    click.echo()
                    click.echo("Or use: includecpp cssl doc --list")
        else:
            # Full documentation mode - output everything at once (no pager)
            # Replace Unicode characters that may not be supported on all terminals
            safe_content = content.replace('✓', '[OK]').replace('✗', '[X]').replace('→', '->').replace('←', '<-').replace('•', '*').replace('─', '-').replace('│', '|').replace('└', '+').replace('├', '+').replace('▸', '>').replace('▾', 'v')
            try:
                click.echo(safe_content)
            except UnicodeEncodeError:
                # Fallback: encode with errors='replace'
                click.echo(safe_content.encode('ascii', errors='replace').decode('ascii'))
    else:
        click.secho("Documentation file not found.", fg='yellow')
        click.echo("Looking for: CSSL_DOCUMENTATION.md")
        click.echo()
        click.echo("Quick Reference:")
        click.echo("  - Variables: string x = \"hello\"; int n = 42;")
        click.echo("  - Functions: void foo() { } or define bar() { }")
        click.echo("  - Loops: for (i in range(0, 10)) { } or for (int i = 0; i < 10; i++) { }")
        click.echo("  - Conditions: if (x) { } elif (y) { } else { }")
        click.echo("  - Containers: stack<T>, vector<T>, array<T>")
        click.echo("  - Globals: global x = value; @x")
        click.echo("  - Payloads: payload(\"file.cssl-pl\");")
        click.echo()
        click.echo("For full docs, see: https://github.com/liliassg/IncludeCPP")


@cssl.command(name='create')
@click.argument('name')
@click.option('--dir', '-d', type=click.Path(), default='.', help='Output directory')
def cssl_create(name, dir):
    """Create a new CSSL project with .cssl and .cssl-pl files."""
    from pathlib import Path as PathLib

    out_dir = PathLib(dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cssl_file = out_dir / f"{name}.cssl"
    payload_file = out_dir / f"{name}.cssl-pl"

    # Create .cssl file
    cssl_content = f'''// {name}.cssl - CSSL Application
// Created with: includecpp cssl create {name}

// Load payload (globals, injections, config)
payload("{name}.cssl-pl");

// Main application code
void main() {{
    printl("Hello from {name}!");
    printl("Version: " + @version);
}}

main();
'''

    # Create .cssl-pl payload file
    payload_content = f'''// {name}.cssl-pl - CSSL Payload
// Loaded via: payload("{name}.cssl-pl");

// ============================================================================
// Configuration & Variables
// ============================================================================
global version = "1.0.0";
global appName = "{name}";
global debug = false;

// ============================================================================
// Builtin Injections
// ============================================================================
// Inject cleanup code into exit()
exit() <<== {{
    if (@debug) {{
        printl("[DEBUG] {name} shutting down...");
    }}
}}

// ============================================================================
// Helper Functions (globally callable via @functionName)
// ============================================================================
void log(string message) {{
    if (@debug) {{
        printl("[LOG] " + message);
    }}
}}

void error(string message) {{
    printl("[ERROR] " + message);
}}
'''

    # Write files
    cssl_file.write_text(cssl_content, encoding='utf-8')
    payload_file.write_text(payload_content, encoding='utf-8')

    click.secho(f"Created CSSL project: {name}", fg='green', bold=True)
    click.echo()
    click.echo("Files created:")
    click.echo(f"  {cssl_file}  - Main application")
    click.echo(f"  {payload_file}  - Payload (globals, injections)")
    click.echo()
    click.echo("Run with:")
    click.secho(f"  includecpp cssl exec {cssl_file}", fg='cyan')
    click.echo()
    click.echo("Or from Python:")
    click.echo("  from includecpp import CSSL")
    click.echo(f"  CSSL.exec('{cssl_file}')")


@cssl.command(name='vscode')
def cssl_vscode():
    """Install VSCode extension for CSSL syntax highlighting."""
    from pathlib import Path as PathLib
    import shutil
    import os

    # Find VSCode extensions directory
    if os.name == 'nt':  # Windows
        vscode_ext_dir = PathLib(os.environ.get('USERPROFILE', '')) / '.vscode' / 'extensions'
    else:  # Linux/Mac
        vscode_ext_dir = PathLib.home() / '.vscode' / 'extensions'

    if not vscode_ext_dir.exists():
        # Try VSCode Insiders
        if os.name == 'nt':
            vscode_ext_dir = PathLib(os.environ.get('USERPROFILE', '')) / '.vscode-insiders' / 'extensions'
        else:
            vscode_ext_dir = PathLib.home() / '.vscode-insiders' / 'extensions'

    if not vscode_ext_dir.exists():
        click.secho("VSCode extensions directory not found.", fg='red')
        click.echo("Make sure VSCode is installed.")
        click.echo()
        click.echo("Expected locations:")
        if os.name == 'nt':
            click.echo(f"  %USERPROFILE%\\.vscode\\extensions")
        else:
            click.echo(f"  ~/.vscode/extensions")
        return

    # Find our bundled extension
    package_dir = PathLib(__file__).parent.parent
    source_ext_dir = package_dir / 'vscode' / 'cssl'

    if not source_ext_dir.exists():
        click.secho("CSSL extension files not found in package.", fg='red')
        return

    # Get version from package.json
    pkg_json = source_ext_dir / 'package.json'
    current_version = "1.1.0"
    if pkg_json.exists():
        try:
            pkg_data = json.loads(pkg_json.read_text(encoding='utf-8'))
            current_version = pkg_data.get('version', '1.1.0')
        except:
            pass

    target_dir = vscode_ext_dir / f'includecpp.cssl-{current_version}'

    try:
        # Check for existing installations
        existing_version = None
        for existing in vscode_ext_dir.glob('includecpp.cssl-*'):
            existing_version = existing.name.split('-')[-1]
            if existing_version != current_version:
                click.echo(f"Removing old version: {existing_version}")
                shutil.rmtree(existing)

        if target_dir.exists():
            shutil.rmtree(target_dir)

        shutil.copytree(source_ext_dir, target_dir)

        if existing_version and existing_version != current_version:
            click.secho(f"CSSL extension updated: v{existing_version} -> v{current_version}", fg='green', bold=True)
        else:
            click.secho(f"CSSL VSCode extension installed! (v{current_version})", fg='green', bold=True)
        click.echo()
        click.echo(f"Installed to: {target_dir}")
        click.echo()
        click.echo("Features:")
        click.echo("  - Syntax highlighting for .cssl, .cssl-pl, .cssl-mod files")
        click.echo("  - OOP support: class, constructor, this->member")
        click.echo("  - Injection operators: <== (brute), <<== (infuse)")
        click.echo("  - Type highlighting: int, string, stack<T>, instance<>")
        click.echo("  - Global references: @Name, r@Name, s@Name")
        click.echo("  - Shared objects: $Name")
        click.echo()
        click.secho("Restart VSCode to activate the extension.", fg='yellow')

    except PermissionError:
        click.secho("Permission denied. Try running as administrator.", fg='red')
    except Exception as e:
        click.secho(f"Installation failed: {e}", fg='red')


@cssl.command(name='sdk')
@click.argument('lang', required=False, default=None)
@click.option('--doc', is_flag=True, help='Show SDK documentation')
def cssl_sdk(lang, doc):
    """Generate SDK files for cross-language instance sharing.

    \b
    Usage:
      includecpp cssl sdk cpp        # Create C++ SDK in ./sdk/cpp/
      includecpp cssl sdk java       # Create Java SDK in ./sdk/java/
      includecpp cssl sdk csharp     # Create C# SDK in ./sdk/csharp/
      includecpp cssl sdk js         # Create JavaScript SDK in ./sdk/javascript/
      includecpp cssl sdk all        # Create all SDKs
      includecpp cssl sdk --doc      # Show SDK documentation

    \b
    Languages:
      cpp, c++      C++ header-only SDK
      java          Java SDK (com.includecpp.CSSL)
      csharp, c#    C# SDK (IncludeCPP.CSSL)
      js, javascript  JavaScript/Node.js SDK
      all           All languages

    \b
    Cross-Language Instance Sharing:
      Share instances from any language and access them in CSSL using
      the lang$InstanceName syntax:

      C++:    CSSL::share("Engine", &engine);  -> cpp$Engine
      Java:   CSSL.share("Service", svc);      -> java$Service
      C#:     CSSL.Share("Handler", hdl);      -> csharp$Handler
      JS:     CSSL.share('Processor', proc);   -> js$Processor
    """
    from pathlib import Path as PathLib
    import shutil

    # Show documentation if --doc flag is set
    if doc or lang == 'doc':
        _show_sdk_documentation()
        return

    if lang is None:
        # Show help
        click.secho("CSSL Multi-Language SDK Generator", fg='cyan', bold=True)
        click.echo()
        click.echo("Usage:")
        click.echo("  includecpp cssl sdk <lang>     Create SDK for language")
        click.echo("  includecpp cssl sdk --doc      Show documentation")
        click.echo()
        click.echo("Languages:")
        click.echo("  cpp, c++      C++ header-only SDK")
        click.echo("  java          Java SDK")
        click.echo("  csharp, c#    C# SDK")
        click.echo("  js, javascript  JavaScript SDK")
        click.echo("  all           All SDKs")
        return

    # Normalize language name
    lang_map = {
        'cpp': 'cpp', 'c++': 'cpp',
        'java': 'java',
        'csharp': 'csharp', 'c#': 'csharp', 'cs': 'csharp',
        'js': 'javascript', 'javascript': 'javascript',
        'all': 'all'
    }

    normalized = lang_map.get(lang.lower())
    if normalized is None:
        click.secho(f"Unknown language: {lang}", fg='red')
        click.echo("Supported: cpp, java, csharp, js, all")
        return

    # Find source SDK directory in package
    package_dir = PathLib(__file__).parent.parent
    source_sdk_dir = package_dir / 'sdk'

    # Target SDK directory
    target_sdk_dir = PathLib.cwd() / 'sdk'

    langs_to_create = ['cpp', 'java', 'csharp', 'javascript'] if normalized == 'all' else [normalized]

    click.secho("Creating CSSL SDK files...", fg='cyan', bold=True)
    click.echo()

    for lang_name in langs_to_create:
        _create_sdk_for_language(target_sdk_dir, lang_name)

    click.echo()
    click.secho("SDK created successfully!", fg='green', bold=True)
    click.echo()
    click.echo("Next steps:")
    click.echo("  1. Copy SDK file(s) to your project")
    click.echo("  2. Import and use CSSL.share() in your code")
    click.echo("  3. Access instances in CSSL via lang$InstanceName")
    click.echo()
    click.echo("Documentation: includecpp cssl sdk --doc")


def _create_sdk_for_language(target_dir, lang_name):
    """Create SDK files for a specific language."""
    from pathlib import Path as PathLib

    # SDK content for each language
    sdk_content = {
        'cpp': _get_cpp_sdk_content(),
        'java': _get_java_sdk_content(),
        'csharp': _get_csharp_sdk_content(),
        'javascript': _get_js_sdk_content(),
    }

    sdk_paths = {
        'cpp': ('cpp', 'includecpp.h'),
        'java': ('java/src/com/includecpp', 'CSSL.java'),
        'csharp': ('csharp', 'IncludeCPP.cs'),
        'javascript': ('javascript', 'includecpp.js'),
    }

    subdir, filename = sdk_paths[lang_name]
    target_subdir = target_dir / subdir
    target_subdir.mkdir(parents=True, exist_ok=True)

    target_file = target_subdir / filename
    target_file.write_text(sdk_content[lang_name], encoding='utf-8')

    lang_display = {'cpp': 'C++', 'java': 'Java', 'csharp': 'C#', 'javascript': 'JavaScript'}
    click.echo(f"  {lang_display[lang_name]}: {target_file}")


def _get_cpp_sdk_content():
    return '''/**
 * IncludeCPP CSSL SDK for C++ (v4.2.0)
 * Cross-language instance sharing between C++ and CSSL.
 *
 * USAGE:
 *     #include "includecpp.h"
 *
 *     class Engine { public: int power = 100; };
 *
 *     int main() {
 *         Engine engine;
 *         CSSL::share("Engine", &engine);
 *         // In CSSL: cpp = libinclude("c++"); engine = cpp$Engine;
 *         return 0;
 *     }
 */
#pragma once
#include <string>
#include <any>
#include <unordered_map>
#include <vector>
#include <mutex>

namespace includecpp { namespace cssl {
class Registry {
public:
    static Registry& instance() { static Registry r; return r; }
    void share(const std::string& n, std::any v) { std::lock_guard<std::mutex> l(_m); _i[n] = v; }
    template<typename T> void share(const std::string& n, T* p) { std::lock_guard<std::mutex> l(_m); _i[n] = static_cast<void*>(p); }
    std::any get(const std::string& n) { std::lock_guard<std::mutex> l(_m); auto it = _i.find(n); return it != _i.end() ? it->second : std::any{}; }
    template<typename T> T* get(const std::string& n) { std::lock_guard<std::mutex> l(_m); auto it = _i.find(n); if (it != _i.end()) try { return static_cast<T*>(std::any_cast<void*>(it->second)); } catch (...) {} return nullptr; }
    bool has(const std::string& n) { std::lock_guard<std::mutex> l(_m); return _i.count(n) > 0; }
    bool remove(const std::string& n) { std::lock_guard<std::mutex> l(_m); return _i.erase(n) > 0; }
    std::vector<std::string> list() { std::lock_guard<std::mutex> l(_m); std::vector<std::string> r; for (auto& p : _i) r.push_back(p.first); return r; }
    void clear() { std::lock_guard<std::mutex> l(_m); _i.clear(); }
private:
    Registry() = default;
    std::unordered_map<std::string, std::any> _i;
    std::mutex _m;
};
}}

namespace CSSL {
    template<typename T> inline void share(const std::string& n, T* i) { includecpp::cssl::Registry::instance().share(n, i); }
    inline void share(const std::string& n, std::any v) { includecpp::cssl::Registry::instance().share(n, v); }
    template<typename T> inline T* get(const std::string& n) { return includecpp::cssl::Registry::instance().get<T>(n); }
    inline bool has(const std::string& n) { return includecpp::cssl::Registry::instance().has(n); }
    inline bool remove(const std::string& n) { return includecpp::cssl::Registry::instance().remove(n); }
    inline std::vector<std::string> list() { return includecpp::cssl::Registry::instance().list(); }
    inline void clear() { includecpp::cssl::Registry::instance().clear(); }
}

#define CSSL_SHARE(name, instance) CSSL::share(#name, instance)
#define CSSL_GET(type, name) CSSL::get<type>(#name)
'''


def _get_java_sdk_content():
    return '''/**
 * IncludeCPP CSSL SDK for Java (v4.2.0)
 * Cross-language instance sharing between Java and CSSL.
 *
 * USAGE:
 *     import com.includecpp.CSSL;
 *
 *     MyService service = new MyService();
 *     CSSL.share("MyService", service);
 *     // In CSSL: java = libinclude("java"); svc = java$MyService;
 */
package com.includecpp;

import java.util.concurrent.ConcurrentHashMap;
import java.util.List;
import java.util.ArrayList;

public class CSSL {
    private static final ConcurrentHashMap<String, Object> instances = new ConcurrentHashMap<>();

    public static void share(String name, Object instance) { instances.put(name, instance); }
    @SuppressWarnings("unchecked")
    public static <T> T get(String name) { return (T) instances.get(name); }
    public static <T> T get(String name, Class<T> type) { Object o = instances.get(name); return type.isInstance(o) ? type.cast(o) : null; }
    public static boolean has(String name) { return instances.containsKey(name); }
    public static boolean remove(String name) { return instances.remove(name) != null; }
    public static List<String> list() { return new ArrayList<>(instances.keySet()); }
    public static void clear() { instances.clear(); }
    public static int size() { return instances.size(); }
}
'''


def _get_csharp_sdk_content():
    return '''/**
 * IncludeCPP CSSL SDK for C# (v4.2.0)
 * Cross-language instance sharing between C# and CSSL.
 *
 * USAGE:
 *     using IncludeCPP;
 *
 *     var service = new MyService();
 *     CSSL.Share("MyService", service);
 *     // In CSSL: cs = libinclude("c#"); svc = cs$MyService;
 */
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;

namespace IncludeCPP
{
    public static class CSSL
    {
        private static readonly ConcurrentDictionary<string, object> _instances = new();

        public static void Share(string name, object instance) => _instances[name] = instance;
        public static T Get<T>(string name) where T : class => _instances.TryGetValue(name, out var o) ? o as T : null;
        public static object Get(string name) => _instances.TryGetValue(name, out var o) ? o : null;
        public static bool Has(string name) => _instances.ContainsKey(name);
        public static bool Remove(string name) => _instances.TryRemove(name, out _);
        public static IReadOnlyList<string> List() => _instances.Keys.ToList().AsReadOnly();
        public static void Clear() => _instances.Clear();
        public static int Count => _instances.Count;
    }
}
'''


def _get_js_sdk_content():
    return '''/**
 * IncludeCPP CSSL SDK for JavaScript (v4.2.0)
 * Cross-language instance sharing between JavaScript and CSSL.
 *
 * USAGE:
 *     const { CSSL } = require('includecpp-cssl');
 *     // or: import { CSSL } from 'includecpp-cssl';
 *
 *     class DataProcessor { process(data) { return data.toUpperCase(); } }
 *     CSSL.share('DataProcessor', new DataProcessor());
 *     // In CSSL: js = libinclude("javascript"); proc = js$DataProcessor;
 */
const instances = new Map();

const CSSL = {
    share(name, instance) { instances.set(name, instance); },
    get(name) { return instances.get(name); },
    has(name) { return instances.has(name); },
    remove(name) { return instances.delete(name); },
    list() { return Array.from(instances.keys()); },
    clear() { instances.clear(); },
    get size() { return instances.size; }
};

if (typeof module !== 'undefined') { module.exports = { CSSL }; module.exports.default = CSSL; }
if (typeof window !== 'undefined') { window.CSSL = CSSL; }
export { CSSL };
export default CSSL;
'''


def _show_sdk_documentation():
    """Show detailed SDK documentation."""
    click.secho("=" * 70, fg='cyan')
    click.secho("  CSSL Multi-Language SDK Documentation (v4.2.0)", fg='cyan', bold=True)
    click.secho("=" * 70, fg='cyan')
    click.echo()

    click.secho("OVERVIEW", fg='yellow', bold=True)
    click.echo("  The CSSL SDK enables cross-language instance sharing between")
    click.echo("  C++, Java, C#, JavaScript and CSSL scripts.")
    click.echo()
    click.echo("  Share an instance from any language, then access it in CSSL")
    click.echo("  using the lang$InstanceName syntax.")
    click.echo()

    click.secho("HOW IT WORKS", fg='yellow', bold=True)
    click.echo("  1. In your language, call CSSL.share(name, instance)")
    click.echo("  2. In CSSL, load language support with libinclude()")
    click.echo("  3. Access instance via lang$InstanceName")
    click.echo()

    click.secho("C++ USAGE", fg='green', bold=True)
    click.echo('''
    #include "includecpp.h"

    class Engine {
    public:
        int power = 500;
        void start() { /* ... */ }
    };

    int main() {
        Engine engine;
        CSSL::share("Engine", &engine);

        // Alternative macro syntax:
        // CSSL_SHARE(Engine, &engine);

        return 0;
    }

    // In CSSL:
    // cpp = libinclude("c++");
    // engine = cpp$Engine;
    // printl(engine.power);  // 500
''')

    click.secho("JAVA USAGE", fg='green', bold=True)
    click.echo('''
    import com.includecpp.CSSL;

    public class Main {
        public static void main(String[] args) {
            MyService service = new MyService();
            CSSL.share("MyService", service);

            // Check if exists
            if (CSSL.has("MyService")) {
                MyService s = CSSL.get("MyService", MyService.class);
            }
        }
    }

    // In CSSL:
    // java = libinclude("java");
    // service = java$MyService;
    // service.doSomething();
''')

    click.secho("C# USAGE", fg='green', bold=True)
    click.echo('''
    using IncludeCPP;

    class Program {
        static void Main() {
            var handler = new DataHandler();
            CSSL.Share("DataHandler", handler);

            // List all shared
            foreach (var name in CSSL.List()) {
                Console.WriteLine(name);
            }
        }
    }

    // In CSSL:
    // cs = libinclude("c#");
    // handler = cs$DataHandler;
    // handler.Process(data);
''')

    click.secho("JAVASCRIPT USAGE", fg='green', bold=True)
    click.echo('''
    const { CSSL } = require('includecpp-cssl');
    // or: import { CSSL } from 'includecpp-cssl';

    class DataProcessor {
        process(data) {
            return data.toUpperCase();
        }
    }

    CSSL.share('DataProcessor', new DataProcessor());
    console.log(CSSL.list());  // ['DataProcessor']

    // In CSSL:
    // js = libinclude("javascript");
    // processor = js$DataProcessor;
    // result = processor.process("hello");
''')

    click.secho("CSSL SIDE (Complete Example)", fg='green', bold=True)
    click.echo('''
    // Load language support
    cpp = libinclude("c++");
    java = libinclude("java");
    cs = libinclude("c#");
    js = libinclude("javascript");

    // Access shared instances
    engine = cpp$Engine;
    service = java$MyService;
    handler = cs$DataHandler;
    processor = js$DataProcessor;

    // Use them
    printl("Engine power: " + engine.power);
    service.doSomething();
    handler.Process(data);
    result = processor.process("hello");

    // Cross-language inheritance
    class TurboEngine : extends cpp$Engine {
        int boost;

        constr TurboEngine(int b) {
            this->boost = b;
        }
    }
''')

    click.secho("API REFERENCE", fg='yellow', bold=True)
    click.echo('''
    Method             Description
    ---------------    ------------------------------------------
    share(name, obj)   Share an instance by name
    get(name)          Get a shared instance
    has(name)          Check if instance exists
    remove(name)       Remove a shared instance
    list()             Get all instance names
    clear()            Clear all instances
    size/Count         Number of shared instances
''')

    click.secho("GENERATE SDK FILES", fg='yellow', bold=True)
    click.echo('''
    includecpp cssl sdk cpp        # C++ SDK
    includecpp cssl sdk java       # Java SDK
    includecpp cssl sdk csharp     # C# SDK
    includecpp cssl sdk js         # JavaScript SDK
    includecpp cssl sdk all        # All SDKs
''')


@cssl.command(name='guimaker')
@click.argument('file', required=False, default='')
def cssl_guimaker(file):
    """Launch the visual CSSL GUI Builder.

    \b
    Usage:
      includecpp cssl guimaker              # New project
      includecpp cssl guimaker gui.cssl     # Open existing file
    """
    try:
        from includecpp.gui.guimaker import run_guimaker
        run_guimaker(file)
    except ImportError as e:
        click.secho(f"Failed to launch GUI Builder: {e}", fg='red')
        click.secho("Make sure PyQt6 is installed: pip install PyQt6", fg='yellow')


# Register hidden cssl command group
cli.add_command(cssl)


# ============================================================================
# VSCODE - Initialize/Update VSCode Configuration
# ============================================================================

@cli.command()
@click.option('--force', '-f', is_flag=True, help='Force overwrite existing files')
@click.option('--reinstall', '-r', is_flag=True, help='Reinstall extension (removes all versions first)')
@click.option('--stubs-only', is_flag=True, help='Only update stubs, skip extension files')
def vscode(force, reinstall, stubs_only):
    """Initialize or update VSCode configuration for IncludeCPP/CSSL.

    Installs CSSL extension globally and sets up project stubs.

    \b
    Usage:
      includecpp vscode             # Install/update extension + stubs
      includecpp vscode --force     # Force reinstall extension
      includecpp vscode --reinstall # Remove ALL versions & reinstall fresh
      includecpp vscode --stubs-only  # Only update stubs

    \b
    What it does:
      1. Installs CSSL extension globally (~/.vscode/extensions/)
      2. Creates .vscode/settings.json with file associations
      3. Creates .vscode/stubs/ with type hints for IDE support
    """
    from pathlib import Path as PathLib
    import os

    cwd = PathLib.cwd()
    vscode_dir = cwd / '.vscode'
    stubs_dir = vscode_dir / 'stubs'
    plugins_stubs_dir = stubs_dir / 'plugins'
    modules_stubs_dir = stubs_dir / 'modules'

    # Create directories
    vscode_dir.mkdir(exist_ok=True)
    stubs_dir.mkdir(exist_ok=True)
    plugins_stubs_dir.mkdir(exist_ok=True)
    modules_stubs_dir.mkdir(exist_ok=True)

    click.secho("=" * 60, fg='cyan')
    click.secho("IncludeCPP VSCode Configuration", fg='cyan', bold=True)
    click.secho("=" * 60, fg='cyan')
    click.echo()

    updated_count = 0
    created_count = 0

    # 1. Install CSSL extension GLOBALLY (unless stubs-only)
    if not stubs_only:
        click.secho("Installing CSSL extension globally...", fg='yellow')

        # Find source extension directory
        source_ext_dir = PathLib(__file__).parent.parent / 'vscode' / 'cssl'

        if source_ext_dir.exists():
            # Get version from package.json
            pkg_json = source_ext_dir / 'package.json'
            current_version = "1.1.0"
            if pkg_json.exists():
                try:
                    pkg_data = json.loads(pkg_json.read_text(encoding='utf-8'))
                    current_version = pkg_data.get('version', '1.1.0')
                except:
                    pass

            # Find global VSCode extensions directory
            if os.name == 'nt':  # Windows
                global_ext_dir = PathLib(os.environ.get('USERPROFILE', '')) / '.vscode' / 'extensions'
            else:  # Linux/Mac
                global_ext_dir = PathLib.home() / '.vscode' / 'extensions'

            if not global_ext_dir.exists():
                # Try VSCode Insiders
                if os.name == 'nt':
                    global_ext_dir = PathLib(os.environ.get('USERPROFILE', '')) / '.vscode-insiders' / 'extensions'
                else:
                    global_ext_dir = PathLib.home() / '.vscode-insiders' / 'extensions'

            if global_ext_dir.exists():
                target_dir = global_ext_dir / f'includecpp.cssl-{current_version}'

                # Check if already installed with same or older version
                needs_install = force or reinstall
                existing_version = None

                # Find existing installations
                for existing in global_ext_dir.glob('includecpp.cssl-*'):
                    existing_version = existing.name.split('-')[-1]
                    if reinstall:
                        # --reinstall: Remove ALL versions
                        click.echo(f"  Removing version: {existing_version}")
                        shutil.rmtree(existing)
                        needs_install = True
                    elif existing_version != current_version:
                        # Remove old version
                        click.echo(f"  Removing old version: {existing_version}")
                        shutil.rmtree(existing)
                        needs_install = True
                    elif not force:
                        click.echo(f"  Already installed: v{current_version}")
                        needs_install = False

                if not target_dir.exists():
                    needs_install = True

                if needs_install:
                    # Remove target if exists (force reinstall)
                    if target_dir.exists():
                        shutil.rmtree(target_dir)

                    # Copy extension to global directory
                    shutil.copytree(source_ext_dir, target_dir)
                    created_count += 1

                    if existing_version and existing_version != current_version:
                        click.secho(f"  Updated: v{existing_version} -> v{current_version}", fg='green')
                    else:
                        click.secho(f"  Installed: v{current_version}", fg='green')

                    click.echo(f"  Location: {target_dir}")
                    click.echo()

                    # Run npm install for vscode-languageclient dependency
                    click.secho("  Installing Node.js dependencies...", fg='cyan')
                    npm_path = shutil.which('npm')
                    if npm_path:
                        try:
                            # Use cwd instead of --prefix for better Windows compatibility
                            result = subprocess.run(
                                [npm_path, 'install'],
                                capture_output=True,
                                text=True,
                                timeout=120,
                                cwd=str(target_dir)
                            )
                            if result.returncode == 0:
                                click.secho("  Node.js dependencies installed", fg='green')
                            else:
                                click.secho("  Warning: npm install had issues", fg='yellow')
                                click.echo(f"  Run manually: cd \"{target_dir}\" && npm install")
                        except subprocess.TimeoutExpired:
                            click.secho("  Warning: npm install timed out", fg='yellow')
                        except Exception as e:
                            click.secho(f"  Warning: npm install failed: {e}", fg='yellow')
                            click.echo(f"  Run manually: cd \"{target_dir}\" && npm install")
                    else:
                        click.secho("  Note: npm not found - install Node.js for full LSP support", fg='yellow')

                    click.secho("  Restart VSCode to activate the extension!", fg='yellow', bold=True)
            else:
                click.secho("  VSCode extensions directory not found.", fg='red')
                click.echo("  Make sure VSCode is installed.")
        else:
            click.secho("  Warning: CSSL extension source not found", fg='yellow')

        # Install Python LSP dependencies
        click.echo()
        click.secho("Installing Language Server dependencies...", fg='yellow')
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pygls>=2.0.0', 'lsprotocol>=2025.0.0', '-q'],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                click.secho("  pygls and lsprotocol installed", fg='green')
            else:
                click.secho(f"  Warning: pip install had issues", fg='yellow')
                if result.stderr:
                    click.echo(f"  {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            click.secho("  Warning: pip install timed out", fg='yellow')
        except Exception as e:
            click.secho(f"  Warning: Could not install LSP dependencies: {e}", fg='yellow')
            click.echo("  Run manually: pip install pygls>=2.0.0 lsprotocol>=2025.0.0")

        # Test Language Server
        click.echo()
        click.secho("Testing Language Server...", fg='yellow')
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'includecpp.vscode.cssl.server', '--test'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                click.secho("  Language Server test passed!", fg='green')
                # Extract completion count from output
                for line in result.stdout.split('\n'):
                    if 'Completions:' in line:
                        click.echo(f"  {line.strip()}")
            else:
                click.secho("  Language Server test failed", fg='red')
                click.echo(f"  {result.stderr[:200] if result.stderr else result.stdout[:200]}")
        except subprocess.TimeoutExpired:
            click.secho("  Language Server test timed out", fg='yellow')
        except Exception as e:
            click.secho(f"  Could not test Language Server: {e}", fg='yellow')

        click.echo()

    # 2. Copy CSSL builtins stub
    click.secho("Updating type stubs...", fg='yellow')

    builtins_src = PathLib(__file__).parent.parent / 'core' / 'cssl' / 'cssl_builtins.pyi'
    builtins_dst = stubs_dir / 'cssl_builtins.pyi'

    if builtins_src.exists():
        if not builtins_dst.exists() or force:
            shutil.copy2(builtins_src, builtins_dst)
            created_count += 1
            click.echo(f"  Created: .vscode/stubs/cssl_builtins.pyi")
        else:
            # Check if source is newer
            if builtins_src.stat().st_mtime > builtins_dst.stat().st_mtime:
                shutil.copy2(builtins_src, builtins_dst)
                updated_count += 1
                click.echo(f"  Updated: .vscode/stubs/cssl_builtins.pyi")
            else:
                click.echo(f"  Up-to-date: .vscode/stubs/cssl_builtins.pyi")
    else:
        click.secho("  Warning: cssl_builtins.pyi not found in package", fg='yellow')

    # 3. Generate stubs for user plugins (.cp files)
    click.echo()
    click.secho("Scanning for plugins...", fg='yellow')

    plugins_dir = cwd / 'plugins'
    cp_files = []

    # Find all .cp files
    for pattern in ['*.cp', '**/*.cp']:
        cp_files.extend(cwd.glob(pattern))

    if plugins_dir.exists():
        cp_files.extend(plugins_dir.glob('**/*.cp'))

    # Deduplicate
    cp_files = list(set(cp_files))

    if cp_files:
        click.echo(f"  Found {len(cp_files)} plugin(s)")

        for cp_file in cp_files:
            stub_name = cp_file.stem + '.pyi'
            stub_path = plugins_stubs_dir / stub_name

            # Generate stub from .cp file
            stub_content = _generate_plugin_stub(cp_file)

            if stub_content:
                # Check if needs update
                needs_write = not stub_path.exists() or force
                if stub_path.exists() and not force:
                    existing = stub_path.read_text(encoding='utf-8')
                    if existing != stub_content:
                        needs_write = True
                        updated_count += 1
                        click.echo(f"  Updated: .vscode/stubs/plugins/{stub_name}")
                    else:
                        click.echo(f"  Up-to-date: .vscode/stubs/plugins/{stub_name}")
                else:
                    if needs_write:
                        created_count += 1
                        click.echo(f"  Created: .vscode/stubs/plugins/{stub_name}")

                if needs_write:
                    stub_path.write_text(stub_content, encoding='utf-8')
    else:
        click.echo("  No .cp plugins found")

    # 4. Generate stubs for modules in registry
    click.echo()
    click.secho("Scanning for modules...", fg='yellow')

    try:
        from ..core.cpp_api import CppApi
        api = CppApi()
        modules = list(api.registry.keys())

        if modules:
            click.echo(f"  Found {len(modules)} registered module(s)")

            for mod_name in modules:
                stub_name = mod_name + '.pyi'
                stub_path = modules_stubs_dir / stub_name

                # Generate stub from module
                stub_content = _generate_module_stub(api, mod_name)

                if stub_content:
                    needs_write = not stub_path.exists() or force
                    if stub_path.exists() and not force:
                        existing = stub_path.read_text(encoding='utf-8')
                        if existing != stub_content:
                            needs_write = True
                            updated_count += 1
                            click.echo(f"  Updated: .vscode/stubs/modules/{stub_name}")
                        else:
                            click.echo(f"  Up-to-date: .vscode/stubs/modules/{stub_name}")
                    else:
                        if needs_write:
                            created_count += 1
                            click.echo(f"  Created: .vscode/stubs/modules/{stub_name}")

                    if needs_write:
                        stub_path.write_text(stub_content, encoding='utf-8')
        else:
            click.echo("  No modules registered")

    except Exception as e:
        click.echo(f"  Could not scan modules: {e}")

    # 5. Create/update settings.json
    if not stubs_only:
        click.echo()
        click.secho("Configuring VSCode settings...", fg='yellow')

        settings_path = vscode_dir / 'settings.json'
        settings = {}

        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text(encoding='utf-8'))
            except:
                pass

        # Add CSSL settings
        cssl_settings = {
            "files.associations": {
                "*.cssl": "cssl",
                "*.cssl-pl": "cssl",
                "*.cssl-mod": "cssl",
                "*.cp": "cpp"
            },
            "python.analysis.extraPaths": [
                ".vscode/stubs"
            ],
            "python.autoComplete.extraPaths": [
                ".vscode/stubs"
            ]
        }

        # Merge settings
        for key, value in cssl_settings.items():
            if key not in settings:
                settings[key] = value
            elif isinstance(value, dict) and isinstance(settings[key], dict):
                settings[key].update(value)
            elif isinstance(value, list) and isinstance(settings[key], list):
                for item in value:
                    if item not in settings[key]:
                        settings[key].append(item)

        settings_path.write_text(json.dumps(settings, indent=4), encoding='utf-8')
        click.echo(f"  Updated: .vscode/settings.json")

    # Summary
    click.echo()
    click.secho("=" * 60, fg='cyan')
    click.secho("Summary", fg='cyan', bold=True)
    click.secho("=" * 60, fg='cyan')
    click.echo(f"  Created: {created_count} file(s)")
    click.echo(f"  Updated: {updated_count} file(s)")
    click.echo()
    click.secho("VSCode configuration complete!", fg='green', bold=True)
    click.echo()
    click.secho("Features enabled:", fg='cyan')
    click.echo("  - Syntax highlighting for .cssl, .cssl-mod, .cssl-pl")
    click.echo("  - Real-time diagnostics (errors in red, warnings in yellow)")
    click.echo("  - Autocomplete with 264+ completions (builtins, types, keywords)")
    click.echo("  - Hover documentation for functions and types")
    click.echo("  - Go-to-definition (Ctrl+Click or F12)")
    click.echo("  - Find references (Shift+F12)")
    click.echo()
    click.echo("Tips:")
    click.echo("  - Re-run 'includecpp vscode' after adding new plugins")
    click.echo("  - Use --force to overwrite all files")
    click.echo("  - Use --reinstall to completely reinstall the extension")
    click.echo("  - Use --stubs-only to only regenerate stubs")


def _generate_plugin_stub(cp_file: Path) -> str:
    """Generate a .pyi stub file from a .cp plugin file."""
    try:
        content = cp_file.read_text(encoding='utf-8')
    except:
        return ""

    lines = [
        f'"""',
        f'Type stubs for {cp_file.name}',
        f'Auto-generated by: includecpp vscode',
        f'"""',
        f'from typing import Any, Optional, List, Dict, Union',
        f'',
    ]

    # Parse function definitions from .cp file
    # Look for patterns like: type name(params) { or @export type name(params)
    func_pattern = re.compile(
        r'(?:@export\s+)?'
        r'(int|float|string|void|bool|auto|[A-Z]\w*)\s+'
        r'(\w+)\s*\(([^)]*)\)',
        re.MULTILINE
    )

    found_functions = set()

    for match in func_pattern.finditer(content):
        ret_type, func_name, params = match.groups()

        if func_name in found_functions:
            continue
        found_functions.add(func_name)

        # Convert C++ types to Python types
        py_ret = _cpp_to_python_type(ret_type)
        py_params = _parse_cpp_params(params)

        lines.append(f'def {func_name}({py_params}) -> {py_ret}:')
        lines.append(f'    """Function from {cp_file.name}"""')
        lines.append(f'    ...')
        lines.append(f'')

    if len(found_functions) == 0:
        lines.append(f'# No exported functions found in {cp_file.name}')
        lines.append(f'')

    return '\n'.join(lines)


def _generate_module_stub(api, module_name: str) -> str:
    """Generate a .pyi stub file from a registered module."""
    lines = [
        f'"""',
        f'Type stubs for module: {module_name}',
        f'Auto-generated by: includecpp vscode',
        f'"""',
        f'from typing import Any, Optional, List, Dict, Union',
        f'',
    ]

    try:
        module = api.registry.get(module_name)
        if not module:
            return ""

        # Get module functions
        funcs = getattr(module, '_functions', {})
        if not funcs and hasattr(module, '__dict__'):
            # Try to introspect
            for name, obj in module.__dict__.items():
                if callable(obj) and not name.startswith('_'):
                    lines.append(f'def {name}(*args: Any, **kwargs: Any) -> Any:')
                    lines.append(f'    """Function from {module_name}"""')
                    lines.append(f'    ...')
                    lines.append(f'')

        for func_name, func_info in funcs.items():
            ret_type = func_info.get('return_type', 'Any')
            params = func_info.get('params', [])

            py_ret = _cpp_to_python_type(ret_type)
            py_params = ', '.join([f'{p["name"]}: {_cpp_to_python_type(p.get("type", "Any"))}' for p in params]) if params else ''

            lines.append(f'def {func_name}({py_params}) -> {py_ret}:')
            lines.append(f'    """Function from {module_name}"""')
            lines.append(f'    ...')
            lines.append(f'')

    except Exception:
        lines.append(f'# Could not introspect module: {module_name}')
        lines.append(f'')

    return '\n'.join(lines)


def _cpp_to_python_type(cpp_type: str) -> str:
    """Convert C++ type to Python type annotation."""
    type_map = {
        'void': 'None',
        'int': 'int',
        'float': 'float',
        'double': 'float',
        'string': 'str',
        'bool': 'bool',
        'auto': 'Any',
        'char*': 'str',
        'const char*': 'str',
    }
    return type_map.get(cpp_type.strip(), 'Any')


def _parse_cpp_params(params_str: str) -> str:
    """Parse C++ parameter list to Python type annotations."""
    if not params_str.strip():
        return ''

    params = []
    for param in params_str.split(','):
        param = param.strip()
        if not param:
            continue

        # Parse "type name" or "type name = default"
        parts = param.split('=')[0].strip().split()
        if len(parts) >= 2:
            param_type = parts[-2]
            param_name = parts[-1].strip('&*')
            py_type = _cpp_to_python_type(param_type)
            params.append(f'{param_name}: {py_type}')
        elif len(parts) == 1:
            params.append(f'arg: Any')

    return ', '.join(params)


# ============================================================================
# HomeServer Commands
# ============================================================================

@cli.group()
def server():
    """HomeServer - Local storage for modules and projects.

    A lightweight background server for storing and sharing content.
    Default port: 2007
    """
    pass


@server.command()
def install():
    """Install and configure HomeServer for auto-start."""
    from ..core.homeserver import (
        HomeServerConfig, get_server_dir, setup_windows_autostart, start_server
    )

    config = HomeServerConfig()

    if config.is_installed():
        click.secho("HomeServer is already installed", fg='yellow')
        return

    # Create directories
    server_dir = get_server_dir()
    server_dir.mkdir(parents=True, exist_ok=True)

    # Mark as installed
    config.set_installed()

    # Set up auto-start on Windows
    if sys.platform == 'win32':
        if setup_windows_autostart():
            click.secho("Auto-start configured for Windows", fg='green')

    # Start the server
    success, port, message = start_server()
    if success:
        click.secho(f"HomeServer installed successfully", fg='green')
        click.secho(f"Running on port {port}", fg='cyan')
    else:
        click.secho(f"Installation complete but server failed to start: {message}", fg='yellow')


@server.command()
@click.option('--port', '-p', type=int, help='Port number to use')
def start(port):
    """Start the HomeServer."""
    from ..core.homeserver import start_server

    success, actual_port, message = start_server(port=port)

    if success:
        click.secho(message, fg='green')
    else:
        click.secho(message, fg='red')


@server.command()
def stop():
    """Stop the HomeServer."""
    from ..core.homeserver import stop_server

    success, message = stop_server()

    if success:
        click.secho(message, fg='green')
    else:
        click.secho(message, fg='yellow')


@server.command()
def status():
    """Check HomeServer status."""
    from ..core.homeserver import is_server_running, HomeServerConfig, format_size, HomeServerDB

    config = HomeServerConfig()
    running = is_server_running(config.port)

    click.secho(f"Port: {config.port}", fg='cyan')
    click.secho(f"Status: ", nl=False)

    if running:
        click.secho("Running", fg='green')

        # Show storage stats
        try:
            db = HomeServerDB()
            items = db.get_all_items()
            total_size = sum(i.get('size_bytes', 0) for i in items)
            click.secho(f"Items: {len(items)}", fg='cyan')
            click.secho(f"Storage: {format_size(total_size)}", fg='cyan')
        except:
            pass
    else:
        click.secho("Stopped", fg='red')

    click.secho(f"Auto-start: {'Enabled' if config.auto_start else 'Disabled'}", fg='cyan')


@server.command('list')
@click.option('--category', '-c', help='Filter by category')
def server_list(category):
    """List all stored items."""
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig, format_size

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()

        if category:
            items = client.get_items_by_category(category)
            click.secho(f"Category: {category}", fg='cyan', bold=True)
        else:
            items = client.list_items()

        if not items:
            click.secho("No items stored", fg='yellow')
            return

        click.secho(f"{'Name':<25} {'Type':<10} {'Category':<15} {'Size':<10}", fg='cyan', bold=True)
        click.secho("-" * 65, fg='white')

        for item in items:
            name = item['name'][:23] + '..' if len(item['name']) > 25 else item['name']
            item_type = item['item_type']
            cat = item.get('category') or '-'
            cat = cat[:13] + '..' if len(cat) > 15 else cat
            size = format_size(item.get('size_bytes', 0))
            click.echo(f"{name:<25} {item_type:<10} {cat:<15} {size:<10}")

        click.secho(f"\nTotal: {len(items)} items", fg='green')

        # Show categories summary
        if not category:
            categories = client.list_categories()
            if categories:
                click.secho(f"Categories: {', '.join(categories)}", fg='cyan')

    except ConnectionError as e:
        click.secho(str(e), fg='red')


@server.command()
@click.argument('name')
@click.argument('path', type=click.Path(exists=True))
@click.option('--project', '-p', is_flag=True, help='Upload as project (folder)')
@click.option('--category', '-c', help='Category to organize the item')
def upload(name, path, project, category):
    """Upload a file or project to HomeServer.

    NAME: Unique name for the item
    PATH: Path to file or folder
    """
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig, format_size

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    path_obj = Path(path)

    try:
        client = HomeServerClient()

        if project or path_obj.is_dir():
            if not path_obj.is_dir():
                click.secho("--project flag requires a directory", fg='red')
                return
            click.secho(f"Uploading project '{name}'...", fg='cyan')
            result = client.upload_project(name, path_obj, category=category)
        else:
            click.secho(f"Uploading file '{name}'...", fg='cyan')
            result = client.upload_file(name, path_obj, category=category)

        if result.get('success'):
            msg = f"Uploaded successfully: {name}"
            if category:
                msg += f" (category: {category})"
            click.secho(msg, fg='green')
            # Check if project path was auto-detected
            if not project and path_obj.suffix.lower() == '.py':
                saved_proj = client.get_project_path(name)
                if saved_proj:
                    click.secho(f"  Auto-detected project: {saved_proj}", fg='cyan')
                    click.echo("  This will be used automatically with 'server run'")
        else:
            click.secho(f"Upload failed: {result.get('error', 'Unknown error')}", fg='red')

    except ConnectionError as e:
        click.secho(str(e), fg='red')
    except Exception as e:
        click.secho(f"Error: {e}", fg='red')


@server.command()
@click.argument('name')
@click.argument('output', type=click.Path(), required=False)
def download(name, output):
    """Download a file or project from HomeServer.

    NAME: Name of the item to download
    OUTPUT: Output path - directory (ends with /) or file path (default: current directory)

    Examples:
        includecpp server download myfile.exe ./        # -> ./myfile.exe
        includecpp server download myfile.exe backup/   # -> backup/myfile.exe
        includecpp server download myfile.exe out.exe   # -> out.exe
    """
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()

        # Get item info first
        item = client.get_item(name)
        if not item:
            click.secho(f"Item '{name}' not found", fg='red')
            return

        # Determine output path and if it's a directory
        if output:
            # Check if user specified a directory (ends with separator or is existing dir)
            is_dir = output.endswith(('/', '\\', os.sep)) or Path(output).is_dir()
            output_path = Path(output.rstrip('/\\')) if is_dir else Path(output)
        else:
            # Default: current directory
            output_path = Path.cwd()
            is_dir = True

        click.secho(f"Downloading '{name}'...", fg='cyan')

        final_path = client.download_file(name, output_path, is_dir=is_dir)
        click.secho(f"Downloaded to: {final_path}", fg='green')

    except ConnectionError as e:
        click.secho(str(e), fg='red')
    except Exception as e:
        click.secho(f"Error: {e}", fg='red')


@server.command()
@click.argument('name')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
def delete(name, force):
    """Delete an item from HomeServer.

    NAME: Name of the item to delete
    """
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()

        # Check item exists
        item = client.get_item(name)
        if not item:
            click.secho(f"Item '{name}' not found", fg='red')
            return

        if not force:
            if not click.confirm(f"Delete '{name}'?"):
                return

        result = client.delete_item(name)

        if result.get('success'):
            click.secho(f"Deleted: {name}", fg='green')
        else:
            click.secho(f"Delete failed: {result.get('error', 'Unknown error')}", fg='red')

    except ConnectionError as e:
        click.secho(str(e), fg='red')


@server.command()
@click.argument('target')
@click.argument('args', nargs=-1)
@click.option('--project', '-p', type=click.Path(exists=True),
              help='IncludeCPP project path for module imports')
@click.option('--cwd', '-c', type=click.Path(exists=True),
              help='Working directory for execution')
def run(target, args, project, cwd):
    """Run a stored executable, script, or project file.

    TARGET: Item name, or name.path.to.file for project files

    Examples:
        includecpp server run MyApp              # Run single executable
        includecpp server run myproject.main    # Run myproject/main.py
        includecpp server run proj.src.app      # Run proj/src/app.py

        # With includecpp project for module imports:
        includecpp server run myscript -p /path/to/project
    """
    from ..core.homeserver import (
        is_server_running, HomeServerClient, HomeServerConfig,
        get_server_dir, HomeServerDB
    )
    import tempfile
    import subprocess

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()
        db = HomeServerDB()

        # Parse target: name or name.path.to.file
        parts = target.split('.')
        item_name = parts[0]
        file_path = '.'.join(parts[1:]) if len(parts) > 1 else None

        # Get item info
        item = client.get_item(item_name)
        if not item:
            click.secho(f"Item '{item_name}' not found", fg='red')
            return

        storage_path = Path(item['storage_path'])

        if item['item_type'] == 'project':
            # Project: find the file to run
            if file_path:
                # Convert dots to path separators
                rel_path = file_path.replace('.', os.sep)
                # Try with common extensions
                candidates = [
                    storage_path / rel_path,
                    storage_path / f"{rel_path}.py",
                    storage_path / f"{rel_path}.bat",
                    storage_path / f"{rel_path}.exe",
                    storage_path / f"{rel_path}.sh",
                ]
                run_file = None
                for c in candidates:
                    if c.exists():
                        run_file = c
                        break

                if not run_file:
                    click.secho(f"File not found: {file_path}", fg='red')
                    click.secho(f"Tried: {', '.join(str(c.relative_to(storage_path)) for c in candidates)}", fg='yellow')
                    return
            else:
                # Try to find main entry point
                for name in ['main.py', 'app.py', '__main__.py', 'run.py', 'main.bat', 'run.bat']:
                    candidate = storage_path / name
                    if candidate.exists():
                        run_file = candidate
                        break
                else:
                    click.secho(f"No entry point found in project. Use: server run {item_name}.<path.to.file>", fg='red')
                    # List available files
                    files = [str(f.relative_to(storage_path)) for f in storage_path.rglob('*')
                             if f.is_file() and f.suffix in ('.py', '.bat', '.exe', '.sh')][:10]
                    if files:
                        click.secho(f"Available files: {', '.join(files)}", fg='cyan')
                    return
        else:
            # Single file
            run_file = storage_path

        if not run_file.exists():
            click.secho(f"File not found: {run_file}", fg='red')
            return

        # Determine how to run the file
        suffix = run_file.suffix.lower()
        click.secho(f"Running: {run_file.name}", fg='cyan')

        # Set up environment for includecpp modules
        env = os.environ.copy()

        # Auto-detect project path from metadata if not explicitly provided
        effective_project = project
        if not effective_project:
            saved_project = client.get_project_path(item_name)
            if saved_project and Path(saved_project).exists():
                effective_project = saved_project
                click.secho(f"Using saved project: {saved_project}", fg='cyan')

        if effective_project:
            project_path = Path(effective_project).resolve()
            # Add project to PYTHONPATH so imports work
            pythonpath = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = f"{project_path}{os.pathsep}{pythonpath}" if pythonpath else str(project_path)
            # Set INCLUDECPP_PROJECT for the includecpp package to find modules
            env['INCLUDECPP_PROJECT'] = str(project_path)

        # Determine working directory
        if cwd:
            work_dir = Path(cwd)
        elif effective_project:
            work_dir = Path(effective_project)
        else:
            work_dir = storage_path.parent if item['item_type'] == 'file' else storage_path

        if suffix == '.py':
            cmd = [sys.executable, str(run_file)] + list(args)
        elif suffix == '.exe':
            cmd = [str(run_file)] + list(args)
        elif suffix == '.bat':
            cmd = ['cmd', '/c', str(run_file)] + list(args)
        elif suffix == '.sh':
            cmd = ['bash', str(run_file)] + list(args)
        elif suffix in ('.js', '.mjs'):
            cmd = ['node', str(run_file)] + list(args)
        else:
            # Try to execute directly
            cmd = [str(run_file)] + list(args)

        # Run the command
        try:
            result = subprocess.run(cmd, cwd=work_dir, env=env)
            if result.returncode != 0:
                click.secho(f"Process exited with code {result.returncode}", fg='yellow')
        except FileNotFoundError:
            click.secho(f"Cannot execute: {run_file.name}", fg='red')
        except PermissionError:
            click.secho(f"Permission denied: {run_file.name}", fg='red')

    except ConnectionError as e:
        click.secho(str(e), fg='red')
    except Exception as e:
        click.secho(f"Error: {e}", fg='red')


@server.command()
@click.argument('port_num', type=int)
def port(port_num):
    """Change the server port.

    PORT_NUM: New port number (1024-65535)
    """
    from ..core.homeserver import HomeServerConfig, is_server_running

    if port_num < 1024 or port_num > 65535:
        click.secho("Port must be between 1024 and 65535", fg='red')
        return

    config = HomeServerConfig()
    old_port = config.port

    if is_server_running(old_port):
        click.secho("Stop the server first before changing port", fg='yellow')
        click.secho("Use: includecpp server stop", fg='cyan')
        return

    config.port = port_num
    click.secho(f"Port changed from {old_port} to {port_num}", fg='green')


@server.command()
def deinstall():
    """Remove HomeServer completely."""
    from ..core.homeserver import (
        stop_server, remove_windows_autostart, get_server_dir, is_server_running,
        HomeServerConfig
    )

    if not click.confirm("This will delete all stored data. Continue?"):
        return

    config = HomeServerConfig()

    # Stop if running
    if is_server_running(config.port):
        stop_server()
        click.secho("Server stopped", fg='cyan')

    # Remove auto-start
    if sys.platform == 'win32':
        remove_windows_autostart()
        click.secho("Auto-start removed", fg='cyan')

    # Delete all data
    server_dir = get_server_dir()
    if server_dir.exists():
        shutil.rmtree(server_dir)
        click.secho("Data deleted", fg='cyan')

    click.secho("HomeServer deinstalled successfully", fg='green')


# Category management subcommand group
@server.group()
def categories():
    """Manage categories for organizing items."""
    pass


@categories.command('list')
def categories_list():
    """List all categories."""
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()
        cats = client.list_categories()

        if not cats:
            click.secho("No categories", fg='yellow')
            return

        click.secho("Categories:", fg='cyan', bold=True)
        for cat in cats:
            items = client.get_items_by_category(cat)
            click.echo(f"  {cat} ({len(items)} items)")

    except ConnectionError as e:
        click.secho(str(e), fg='red')


@categories.command('add')
@click.argument('name')
def categories_add(name):
    """Create a new category."""
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()
        result = client.add_category(name)

        if result.get('success'):
            click.secho(f"Category '{name}' created", fg='green')
        else:
            click.secho(f"Failed: {result.get('error', 'Unknown error')}", fg='red')

    except ConnectionError as e:
        click.secho(str(e), fg='red')


@categories.command('delete')
@click.argument('name')
def categories_delete(name):
    """Delete a category (items become uncategorized)."""
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()
        result = client.delete_category(name)

        if result.get('success'):
            click.secho(f"Category '{name}' deleted", fg='green')
        else:
            click.secho(f"Failed: {result.get('error', 'Unknown error')}", fg='red')

    except ConnectionError as e:
        click.secho(str(e), fg='red')


@categories.command('move')
@click.argument('item_name')
@click.argument('category')
def categories_move(item_name, category):
    """Move an item to a category.

    Use '-' as category to uncategorize.
    """
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    try:
        client = HomeServerClient()
        cat = None if category == '-' else category
        result = client.move_to_category(item_name, cat)

        if result.get('success'):
            if cat:
                click.secho(f"Moved '{item_name}' to category '{cat}'", fg='green')
            else:
                click.secho(f"Removed '{item_name}' from category", fg='green')
        else:
            click.secho(f"Failed: {result.get('error', 'Unknown error')}", fg='red')

    except ConnectionError as e:
        click.secho(str(e), fg='red')


@categories.command('download')
@click.argument('category')
@click.argument('output', type=click.Path(), required=False)
def categories_download(category, output):
    """Download all items in a category.

    CATEGORY: Category name to download
    OUTPUT: Output directory (default: current directory)
    """
    from ..core.homeserver import is_server_running, HomeServerClient, HomeServerConfig

    config = HomeServerConfig()
    if not is_server_running(config.port):
        click.secho("HomeServer is not running. Use 'includecpp server start' first.", fg='red')
        return

    output_path = Path(output) if output else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        client = HomeServerClient()
        items = client.get_items_by_category(category)

        if not items:
            click.secho(f"No items in category '{category}'", fg='yellow')
            return

        click.secho(f"Downloading {len(items)} items from '{category}'...", fg='cyan')

        downloaded = []
        for item in items:
            try:
                path = client.download_file(item['name'], output_path, is_dir=True)
                downloaded.append(item['name'])
                click.echo(f"  Downloaded: {item['name']}")
            except Exception as e:
                click.secho(f"  Failed: {item['name']} - {e}", fg='red')

        click.secho(f"\nDownloaded {len(downloaded)}/{len(items)} items to {output_path}", fg='green')

    except ConnectionError as e:
        click.secho(str(e), fg='red')


# ============================================================================
# Conditional Registration of Experimental Commands
# ============================================================================
# AI and CPPY commands are only available when experimental features are enabled
# Enable via: includecpp settings -> "Enable Experimental Features" checkbox

if _EXPERIMENTAL_ENABLED:
    cli.add_command(ai)
    cli.add_command(cppy)
    cli.add_command(project)


if __name__ == '__main__':
    cli()
