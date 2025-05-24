"""Command-line interface for Time Entry Helper."""

import click

@click.group()
def main():
    """Time Entry Helper - Manage your time entries efficiently."""
    pass


@main.command()
@click.option("--start", is_flag=True, help="Start a time entry")
@click.option("--message", "-m", help="Description of the time entry")
def entry(start, message):
    """Manage time entries."""
    if start:
        click.echo(f"Starting a new time entry: {message}")
    else:
        click.echo("Use --start to begin a new time entry")


@main.command()
def report():
    """Generate time entry reports."""
    click.echo("Generating time entry report...")


if __name__ == "__main__":
    main()
