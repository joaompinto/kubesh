import click
from .plugins import load_commands
from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    print("Do something", load_commands())
