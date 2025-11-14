import click

from dotlocker import core


@click.group()
def cli():
    """
    DotLocker - Configuration files backup and synchronization manager.
    
    Track, version, and sync your dotfiles across multiple machines using Git.
    """

    pass

@cli.command()
def init():
    """Initialize DotLocker repository and configuration."""
    
    core.init_dotlocker()

@cli.command()
def sync():
    """Synchronize with remote repository (push/pull changes)."""

    core.sync_remote()

def main():
    cli()


if __name__ == "__main__":
    main()

