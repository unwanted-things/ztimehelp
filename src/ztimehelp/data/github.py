import requests
import datetime
from typing import Dict, List, Optional, Union

from ztimehelp.data.utils import get_date_object


class GitHubStats:
    def __init__(
        self,
        token: str,
        username: str,
        date: datetime,
        organization: Optional[str] = None,
    ):
        self.token = token
        self.username = username
        self.organization = organization
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        dateobj = get_date_object(date)

        print(dateobj)

        self.start_date = self._format_date(dateobj["start_date"])
        self.end_date = self._format_date(dateobj["end_date"])

    def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Union[List, Dict]:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _format_date(self, date: datetime.datetime) -> str:
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _add_org_filter(self, query: str) -> str:
        if self.organization:
            return f"{query} org:{self.organization}"
        return query
    
    def _formate_large_string(self, text: str, length: int = 100) -> str:
        if len(text) > length:
            return text[:length] + "..."
        return text

    def get_issues_created(self) -> int:
        query = f"author:{self.username} type:issue created:{self.start_date}..{self.end_date}"
        query = self._add_org_filter(query)
        params = {"q": query, "per_page": 100}

        print(params)

        data = self._make_request("/search/issues", params)
        res = {"total_count": data["total_count"], "items": []}

        for item in data.get("items", []):
            res["items"].append(
                {
                    "issue_url": item["html_url"],
                    "comments": item["comments"],
                    "title": item["title"],
                }
            )

        return res

    def get_issue_comments(self) -> int:
        query = f"commenter:{self.username} created:{self.start_date}..{self.end_date} org:{self.organization}"
        params = {"q": query, "per_page": 100}

        print(params)

        data = self._make_request("/search/issues", params)
        res = {
            "total_count": data["total_count"],
            "items_issues": [],
            "items_pulls": [],
        }

        for item in data.get("items", []):
            itemData = {
                "body": self._formate_large_string(item.get("body", "")),
                "comments_url": item.get("comments_url", ""),
            }
            if "/pull/" in item["html_url"]:
                itemData["pull_request_url"] = item["html_url"]
                res["items_pulls"].append(itemData)
            else:
                itemData["issue_url"] = item["html_url"]
                res["items_issues"].append(itemData)

        return res

    def get_pull_requests_created(self) -> int:
        query = (
            f"author:{self.username} type:pr created:{self.start_date}..{self.end_date}"
        )
        query = self._add_org_filter(query)
        params = {"q": query, "per_page": 100}

        data = self._make_request("/search/issues", params)
        res = {"total_count": data["total_count"], "items": []}

        for item in data.get("items", []):
            res["items"].append(
                {
                    "pull_request_url": item["html_url"],
                    "comments": item["comments"],
                    "title": item["title"],
                }
            )

        return res

    def get_commits_made(self) -> int:
        query = (
            f"author:{self.username} committer-date:{self.start_date}..{self.end_date}"
        )
        if self.organization:
            query += f" org:{self.organization}"

        params = {"q": query, "per_page": 100}
        data = self._make_request("/search/commits", params)
        print(data,params)
        res = {"total_count": data["total_count"], "items": []}

        for item in data.get("items", []):
            res["items"].append(
                {
                    "commit_url": item["html_url"],
                    "repository_url": item["repository"]["html_url"],
                    "commit_message": self._formate_large_string(item["commit"]["message"]),
                }
            )

        return res

    def get_daily_activity_summary(self, date: Optional[datetime.date] = None) -> Dict:

        import concurrent.futures

        def fetch_data(func_name, func):
            try:
                return func_name, func()
            except Exception as e:
                return func_name, {"error": str(e), "total_count": 0, "items": []}

        tasks = [
            ("issues_created", self.get_issues_created),
            ("pull_requests_created", self.get_pull_requests_created),
            ("comments", self.get_issue_comments),
            ("commits_made", self.get_commits_made),
        ]

        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_task = {
                executor.submit(fetch_data, name, func): (name, func)
                for name, func in tasks
            }

            for future in concurrent.futures.as_completed(future_to_task):
                name, result = future.result()
                results[name] = result

        results["date"] = date

        return results
