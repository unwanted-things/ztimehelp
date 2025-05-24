"""Command-line interface for ZTimeHelp."""

import click


@click.group()
def main():
    """ZTimeHelp - Manage your time entries efficiently."""
    pass


@main.command()
@click.option("--date", help="Enter the date for the time entry (YYYY-MM-DD).")
def make_entry(date):
    """Manage time entries."""
    click.echo(f"Starting a new time entry for: {date}")


if __name__ == "__main__":
    main()
