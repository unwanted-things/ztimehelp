import datetime
from ztimehelp.config import config
from ztimehelp.data.github import GitHubStats
from ztimehelp.data.utils import get_date_object
from ztimehelp.data.zoom import ZoomStats


token = config.get("GITHUB_TOKEN")
username = config.get("GITHUB_USERNAME")
organization = config.get("GITHUB_ORGANIZATION", "unwanted-things")

today = datetime.date.today()

github_stats = GitHubStats(token, username, today, organization)

# print(get_date_object(datetime.date.today())["start_date"].isoformat()+ "Z")

daily_summary = github_stats.get_daily_activity_summary(today)

print(f"GitHub Activity Summary for {today.isoformat()}:")
print(f"{daily_summary}")
