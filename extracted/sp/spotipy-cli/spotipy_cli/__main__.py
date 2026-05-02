import click
import sys, tty, os, time, termios

from . import config
from . import webApi

pidFileName = '/tmp/spotipy-cli.pid'


@click.group()
@click.pass_context
def cli(ctx):
    """CLI client for Spotify using Web API"""
    cfg = config.Config()
    api = webApi.WebApi(cfg)
    ctx.obj = {
        'api': api
    }
    if not api.initialised:
        sys.exit('Exiting\n')


@cli.command()
@click.pass_context
def play(ctx):
    """Pause or resume playback"""
    ctx.obj['api'].play()


@cli.command()
@click.pass_context
def next(ctx):
    """Next song"""
    ctx.obj['api'].next()


@cli.command()
@click.pass_context
def prev(ctx):
    """Previous song"""
    ctx.obj['api'].prev()


@cli.command()
@click.pass_context
def next_list(ctx):
    """Switch to next playlist"""
    ctx.obj['api'].next_list()


@cli.command()
@click.pass_context
def prev_list(ctx):
    """Switch to previous playlist"""
    ctx.obj['api'].prev_list()


@cli.command()
@click.pass_context
def shuffle(ctx):
    """Toggle shuffle for playback"""
    ctx.obj['api'].shuffle()


@cli.command()
@click.pass_context
def interactive(ctx):
    """Interactive mode. Listen for commands from keyboard. Following commands are supported:\n
     * p - play/pause\n
     * n - next song\n
     * b - previous song\n
     * N - next playlist\n
     * B - previous playlist\n
     * s - toggle shuffle\n
     * q - quit
     """

    sys.stdout.write('''Waiting for commands. 'q' to exit\n''')
    char = _getch()
    api = ctx.obj['api']
    while not char == 'q':
        if char == 'p':
            sys.stdout.write('play/pause\n')
            api.play()
        elif char == 'n':
            sys.stdout.write('next song\n')
            api.next()
        elif char == 'b':
            sys.stdout.write('previous song\n')
            api.prev()
        elif char == 'N':
            sys.stdout.write('next list\n')
            api.next_list()
        elif char == 'B':
            sys.stdout.write('previous list\n')
            api.prev_list()
        elif char == 's':
            sys.stdout.write('toggle shuffle\n')
            api.shuffle()
        time.sleep(0.5)
        char = _getch()
    sys.stdout.write('Exiting...\n')


def _getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def main():
    if os.path.isfile(pidFileName):
        sys.exit('Already running, exiting\n')
    pid = str(os.getpid())

    file = open(pidFileName, 'w').write(pid)
    try:
        cli(obj={})
    finally:
        time.sleep(1)
        os.unlink(pidFileName)


if __name__ == "__main__":
    main()
