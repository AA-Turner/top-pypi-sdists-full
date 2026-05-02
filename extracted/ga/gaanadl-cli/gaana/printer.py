"""
Pretty console output using Rich library.
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    DownloadColumn,
)
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
import pyfiglet

# Custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "track": "bold magenta",
    "album": "bold blue",
    "artist": "bold yellow",
})

console = Console(theme=custom_theme)


def print_banner():
    """Print ASCII art banner."""
    banner = pyfiglet.figlet_format("gaanadl", font="slant")
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("[dim]High-quality music downloader for Gaana[/dim]\n")


def info(message: str):
    """Print info message."""
    console.print(f"[info]ℹ[/info] {message}")


def success(message: str):
    """Print success message."""
    console.print(f"[success]✓[/success] {message}")


def warning(message: str):
    """Print warning message."""
    console.print(f"[warning]⚠[/warning] {message}")


def error(message: str):
    """Print error message."""
    console.print(f"[error]✗[/error] {message}")


def print_track_info(track: dict):
    """Print track information in a panel."""
    title = track.get("title", "Unknown")
    artists = track.get("artists", track.get("primary_artists", "Unknown"))
    album = track.get("album", track.get("album_seokey", "Unknown"))
    
    # Handle duration as string or int
    duration = track.get("duration", 0)
    try:
        duration = int(duration)
    except (ValueError, TypeError):
        duration = 0
    
    # Format duration
    minutes = duration // 60
    seconds = duration % 60
    duration_str = f"{minutes}:{seconds:02d}"
    
    content = Text()
    content.append("Title: ", style="dim")
    content.append(f"{title}\n", style="track")
    content.append("Artist: ", style="dim")
    content.append(f"{artists}\n", style="artist")
    content.append("Album: ", style="dim")
    content.append(f"{album}\n", style="album")
    content.append("Duration: ", style="dim")
    content.append(duration_str)
    
    panel = Panel(content, title="[bold]Track Info[/bold]", border_style="cyan")
    console.print(panel)


def print_album_info(album: dict):
    """Print album information."""
    title = album.get("title", "Unknown")
    artists = album.get("artists", "Unknown")
    track_count = album.get("track_count", 0)
    release_date = album.get("release_date", "Unknown")
    
    content = Text()
    content.append("Album: ", style="dim")
    content.append(f"{title}\n", style="album")
    content.append("Artist: ", style="dim")
    content.append(f"{artists}\n", style="artist")
    content.append("Tracks: ", style="dim")
    content.append(f"{track_count}\n")
    content.append("Released: ", style="dim")
    content.append(release_date)
    
    panel = Panel(content, title="[bold]Album Info[/bold]", border_style="blue")
    console.print(panel)


def print_playlist_info(playlist: dict):
    """Print playlist information."""
    title = playlist.get("title", playlist.get("name", "Unknown"))
    track_count = playlist.get("track_count", len(playlist.get("tracks", [])))
    play_count = playlist.get("play_count", "Unknown")
    favorite_count = playlist.get("favorite_count", "0")
    language = playlist.get("language", "Unknown")
    
    content = Text()
    content.append("Playlist: ", style="dim")
    content.append(f"{title}\n", style="bold magenta")
    content.append("Tracks: ", style="dim")
    content.append(f"{track_count}\n")
    content.append("Language: ", style="dim")
    content.append(f"{language}\n")
    content.append("Plays: ", style="dim")
    content.append(f"{play_count}  ")
    content.append("❤ ", style="red")
    content.append(f"{favorite_count}")
    
    panel = Panel(content, title="[bold]Playlist Info[/bold]", border_style="magenta")
    console.print(panel)


def print_search_results(results: dict, result_type: str = "songs"):
    """Print search results in a table."""
    items = results.get(result_type, [])
    
    if not items:
        warning(f"No {result_type} found.")
        return
    
    table = Table(title=f"Search Results - {result_type.capitalize()}")
    
    table.add_column("#", style="dim", width=4)
    table.add_column("Title/Name", style="track")
    table.add_column("Artist", style="artist")
    
    if result_type == "songs":
        table.add_column("Album", style="album")
    
    for idx, item in enumerate(items[:20], 1):
        # Handle different field names for different result types
        if result_type == "artists":
            title = item.get("name", "Unknown")
            artist = "-"
        else:
            title = item.get("title", "Unknown")
            # Try various artist field names
            artist = (
                item.get("primary_artists") or 
                item.get("artists") or 
                item.get("artist") or 
                "Unknown"
            )
        
        row = [str(idx), title, artist]
        
        if result_type == "songs":
            # Get album name from album_seokey or album field
            album = item.get("album") or item.get("album_seokey", "-")
            row.append(album)
        
        table.add_row(*row)
    
    console.print(table)



def create_download_progress():
    """Create a progress bar for downloads."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        DownloadColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def create_simple_progress():
    """Create a simple progress bar."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )


def print_tracks_list(tracks: list, title: str = "Tracks"):
    """Print a list of tracks in a table format."""
    if not tracks:
        warning("No tracks found.")
        return
    
    table = Table(title=title)
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="track")
    table.add_column("Artist", style="artist")
    table.add_column("Album", style="album")
    table.add_column("Duration", style="dim", justify="right")
    
    for idx, track in enumerate(tracks, 1):
        title_str = track.get("title", "Unknown")
        artist = track.get("artists", track.get("artist", "Unknown"))
        album = track.get("album", "-")
        duration_secs = int(track.get("duration", 0))
        duration = f"{duration_secs // 60}:{duration_secs % 60:02d}" if duration_secs else "-"
        
        table.add_row(str(idx), title_str, artist, album, duration)
    
    console.print(table)

