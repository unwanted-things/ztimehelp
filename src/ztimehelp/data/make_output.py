import json
from datetime import datetime
from typing import Dict, List


def generate_summary_markdown(data: Dict) -> str:
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    try:
        date_obj = datetime.fromisoformat(date_str)
        display_date = date_obj.strftime("%B %d, %Y")
    except ValueError:
        display_date = date_str

    md = f"# Activity Summary for {display_date}\n\n"

    md += "## GitHub\n\n"

    # Issues section
    issues = data.get("issues_created", {})
    issue_count = issues.get("total_count", 0)
    md += f"### Issues Created: {issue_count}\n\n"

    if issue_count > 0 and "items" in issues:
        for issue in issues.get("items", []):
            title = issue.get("title", "Untitled")
            url = issue.get("issue_url", "#")
            comments = issue.get("comments", 0)
            md += f"- {title} - {comments} comments ([Link]({url}))\n"
        md += "\n"

    # Pull Requests section
    prs = data.get("pull_requests_created", {})
    pr_count = prs.get("total_count", 0)
    md += f"### Pull Requests Created: {pr_count}\n\n"

    if pr_count > 0 and "items" in prs:
        for pr in prs.get("items", []):
            title = pr.get("title", "Untitled")
            url = pr.get("pull_request_url", "#")
            comments = pr.get("comments", 0)
            md += f"- {title} - {comments} comments ([Link]({url}))\n"
        md += "\n"

    commits = data.get("commits_made", {})
    commit_count = commits.get("total_count", 0)
    md += f"### Commits: {commit_count}\n\n"

    if commit_count > 0 and "items" in commits:
        repos = {}
        for commit in commits.get("items", []):
            repo_url = commit.get("repository_url", "")
            repo_name = repo_url.split("/")[-1] if repo_url else "Unknown"

            if repo_name not in repos:
                repos[repo_name] = []

            repos[repo_name].append(commit)

        for repo_name, repo_commits in repos.items():
            md += f"#### Repository: {repo_name}\n\n"
            for commit in repo_commits:
                message = commit.get("commit_message", "").split("\n")[
                    0
                ]  # Get first line
                url = commit.get("commit_url", "#")
                md += f"- {message} ([Link]({url}))\n"
            md += "\n"

    # Comments section
    comments = data.get("comments", {})
    comment_count = comments.get("total_count", 0)
    issue_comments = len(comments.get("items_issues", []))
    pr_comments = len(comments.get("items_pulls", []))

    md += f"### Comments: {comment_count}\n\n"
    md += f"- Issue Comments: {issue_comments}\n"
    md += f"- PR Comments: {pr_comments}\n\n"

    if issue_comments > 0:
        md += "#### Issue Comments\n\n"
        for comment in comments.get("items_issues", []):
            issue_url = comment.get("issue_url", "#")

            issue_parts = issue_url.split("/")

            if len(issue_parts) >= 5:
                repo_owner = issue_parts[-4]
                repo_name = issue_parts[-3]
                issue_num = issue_parts[-1]
                issue_title = f"{repo_owner}/{repo_name}#{issue_num}"
            else:
                issue_title = "Issue"

            body = comment.get("body", "").strip() if comment.get("body") else ""
            md += f"- {issue_title} ([Link]({issue_url}))\n"
            if body:
                md += f"```md\n{body}\n```\n"
        md += "\n"

    if pr_comments > 0:
        md += "#### PR Comments\n\n"
        for comment in comments.get("items_pulls", []):
            pr_url = comment.get("pull_request_url", "#")
            pr_parts = pr_url.split("/")
            if len(pr_parts) >= 5:
                repo_owner = pr_parts[-4]
                repo_name = pr_parts[-3]
                pr_num = pr_parts[-1]
                pr_title = f"{repo_owner}/{repo_name}#{pr_num}"
            else:
                pr_title = "Pull Request"

            body = comment.get("p", "").strip() if comment.get("body") else ""

            md += f"- {pr_title} ([Link]({pr_url}))\n"
            if body:
                md += f"```md\n{body}\n```\n"
        md += "\n"

    md += "## Summary\n\n"
    md += f"- **Issues Created:** {issue_count}\n"
    md += f"- **Pull Requests Created:** {pr_count}\n"
    md += f"- **Comments Made:** {comment_count}\n"
    md += f"- **Commits:** {commit_count}\n"

    return md


def save_to_file(content: str, filename: str) -> None:
    with open(filename, "w") as f:
        f.write(content)


def process_github_data(data: Dict, date, output_dir: str = "./") -> Dict:
    markdown = generate_summary_markdown(data)

    file_path = f"{output_dir}/time_entry_helper_{date}.md"

    save_to_file(markdown, file_path)

    return file_path
