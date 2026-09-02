"""
CLI Banner utilities for InnoDay CLI

Provides lightweight banner functionality with graceful fallback for missing dependencies.
"""

import os


def show_cli_banner(
    component_name: str = "InnoDay CLI", show_full: bool = True
) -> None:
    """Show CLI banner with fallback for missing dependencies.

    Args:
        component_name: Name of the component to display
        show_full: Whether to show full banner or compact version
    """
    # Skip banner in quiet mode or CI environments
    if _should_skip_banner():
        return

    try:
        # Try to use the full banner from src.banner
        from src.banner import create_banner
        from src.version import get_display_version

        print(create_banner(component_name))
        print(f"\n🎉 Welcome to {component_name} {get_display_version()}!\n")

    except ImportError:
        # Fallback to simple banner if dependencies not available
        if show_full:
            _print_simple_banner(component_name)
        else:
            _print_compact_banner(component_name)

    except Exception:
        # Graceful degradation - just show component name
        print(f"\n🚀 {component_name}\n")


def show_welcome_banner() -> None:
    """Show welcome banner for first-time setup."""
    show_cli_banner("InnoDay CLI", show_full=True)


def show_version_banner() -> None:
    """Show compact banner for version display."""
    try:
        from src.version import get_display_version

        version = get_display_version()
        print("╔═══════════════════════════════════════╗")
        print("║            InnoDay CLI                ║")
        print(f"║{version:^39}║")
        print("╚═══════════════════════════════════════╝")

    except ImportError:
        print("InnoDay CLI")


def _should_skip_banner() -> bool:
    """Determine if banner should be skipped."""
    # Skip in CI environments
    ci_vars = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL", "TRAVIS"]
    if any(os.getenv(var) for var in ci_vars):
        return True

    # Skip if explicitly disabled
    if os.getenv("INNODAY_NO_BANNER", "").lower() in ["1", "true", "yes"]:
        return True

    # Skip if not a TTY (piped output)
    import sys

    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return True

    return False


def _print_simple_banner(component_name: str) -> None:
    """Simple ASCII banner without external dependencies."""
    try:
        from src.version import get_display_version

        version = get_display_version()
    except ImportError:
        version = ""

    border = "╔══════════════════════════════════════════════════════════════════════════════╗"

    print(f"""
{border}
║                                                                              ║
║                               {component_name:<27}                           ║
║                                                                              ║
║              🤖 AI-Powered Team Orchestration Platform                      ║
║                                                                              ║
║          Capture updates • Prepare SCRUM meetings • Direct workloads       ║
║           Organize releases • Connect people to information                 ║
║                                                                              ║
║       🚀 FastAPI Backend  📊 SQLModel ORM  🔗 Multi-platform Integration   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎉 Welcome to {component_name} {version}!
""")


def _print_compact_banner(component_name: str) -> None:
    """Compact banner for limited space scenarios."""
    try:
        from src.version import get_display_version

        version = get_display_version()
    except ImportError:
        version = ""

    print(f"""
╔══════════════════════════════════════════════╗
║              {component_name:<15}               ║
║           {version:^20}               ║
║                                              ║
║   🤖 AI-Powered Team Orchestration Platform ║
╚══════════════════════════════════════════════╝
""")


def get_banner_config() -> dict:
    """Get banner configuration from environment variables."""
    return {
        "show_banners": os.getenv("INNODAY_SHOW_BANNERS", "true").lower()
        in ["1", "true", "yes"],
        "banner_style": os.getenv("INNODAY_BANNER_STYLE", "full").lower(),
        "show_on_init": os.getenv("INNODAY_BANNER_ON_INIT", "true").lower()
        in ["1", "true", "yes"],
        "show_on_version": os.getenv("INNODAY_BANNER_ON_VERSION", "true").lower()
        in ["1", "true", "yes"],
        "show_on_help": os.getenv("INNODAY_BANNER_ON_HELP", "false").lower()
        in ["1", "true", "yes"],
    }
