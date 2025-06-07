import datetime
import click

from ztimehelp.config import config
from ztimehelp.data.github import GitHubStats
from ztimehelp.data.make_output import process_github_data


@click.group()
def main():
    pass


@main.command()
@click.option("--date", help="Enter the date for the time entry (YYYY-MM-DD).")
@click.option("--output-dir", help="Directory to save the output files.")
def make_entry(date, output_dir):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    print(f"Processing time entry for {date_obj}...")

    token = config.get("GITHUB_TOKEN")
    username = config.get("GITHUB_USERNAME")
    organization = config.get("GITHUB_ORGANIZATION")

    github_stats = GitHubStats(token, username, date_obj, organization)

    file_patch = process_github_data(
        github_stats.get_daily_activity_summary(date), date, output_dir
    )

    print(f"Time entry for {date} has been processed at location: {file_patch}")


if __name__ == "__main__":
    main()
