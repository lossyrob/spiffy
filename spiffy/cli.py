import click
from .playlist import create_playlist, download_playlist
from pathlib import Path

@click.group()
def cli():
    """Spiffy CLI tool."""
    pass

@cli.command("create-playlist")
@click.argument('csv_path', type=str)
@click.option("--name", "-n", default="Spiffy playlist")
@click.option("--dry-run", "-d", is_flag=True)
def create_playlist_cmd(csv_path: str, name: str, dry_run: bool) -> None:
    """Say hello to NAME."""
    p = Path(csv_path)
    if not p.exists():
        raise click.FileError(p, "File does not exist.")
    """Create a Spotify playlist from a CSV file."""
    print(f"Creating playlist {name} from {p}...")
    create_playlist(str(p.resolve(strict=True)), name, dry_run)

@cli.command("download")
@click.argument('playlist_name')
def download(playlist_name):
    """Download a Spotify playlist as a CSV file."""
    result = download_playlist(playlist_name)
    click.echo(result)

if __name__ == "__main__":
    cli(prog_name="spiffy")
