# services/github_service.py

import requests
from urllib.parse import urlparse


class GitHubIssueFetcher:
    def __init__(self, github_token: str | None = None):
        self.base_url = "https://api.github.com"
        self.headers = {}

        if github_token:
            self.headers["Authorization"] = f"Bearer {github_token}"

    def parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """
        Extract owner and repo name from GitHub URL
        """
        try:
            path = urlparse(repo_url).path.strip("/")
            owner, repo = path.split("/")[:2]
            return owner, repo
        except Exception:
            raise ValueError("Invalid GitHub repository URL")

    def fetch_issue(self, repo_url: str, issue_number: int) -> dict:
        owner, repo = self.parse_repo_url(repo_url)

        issue_url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
        comments_url = f"{issue_url}/comments"

        issue_resp = requests.get(issue_url, headers=self.headers)
        comments_resp = requests.get(comments_url, headers=self.headers)

        if issue_resp.status_code != 200:
            raise ValueError("Issue not found or GitHub API error")

        issue_data = issue_resp.json()
        comments_data = comments_resp.json() if comments_resp.status_code == 200 else []

        return {
            "title": issue_data.get("title", ""),
            "body": issue_data.get("body", ""),
            "comments": [comment.get("body", "") for comment in comments_data]
        }
