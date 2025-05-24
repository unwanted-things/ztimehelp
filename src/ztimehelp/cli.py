"""Command-line interface for ZTimeHelp."""

import datetime
import click

from ztimehelp.config import config
from ztimehelp.data.github import GitHubStats
from ztimehelp.data.make_output import process_github_data


@click.group()
def main():
    """ZTimeHelp - Manage your time entries efficiently."""
    pass


@main.command()
@click.option("--date", help="Enter the date for the time entry (YYYY-MM-DD).")
@click.option("--output-dir", help="Directory to save the output files.")
def make_entry(date, output_dir):
    """Manage time entries."""

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    token = config.get("GITHUB_TOKEN")
    username = config.get("GITHUB_USERNAME")
    organization = config.get("GITHUB_ORGANIZATION")

    github_stats = GitHubStats(token, username, date_obj, organization)

    process_github_data(github_stats.get_daily_activity_summary(), date, output_dir)

    print(f"Time entry for {date} has been processed.")


if __name__ == "__main__":
    main()
