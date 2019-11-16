import sys
import click
from . import __version__
from .plugins import load_commands
from .consoles import TerminalConsole, StdinConsole


@click.command()
@click.version_option(version=__version__)
def main():
    commands = load_commands()
    console = TerminalConsole if sys.stdin.isatty() else StdinConsole
    console.run()
