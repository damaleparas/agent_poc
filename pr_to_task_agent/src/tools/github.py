from langchain.tools import tool
from github import Github
from urllib.parse import urlparse
import re

from src.config import settings

# Initialize the GitHub client
gh = Github(settings.GITHUB_TOKEN)

def parse_pr_url(pr_url: str) -> dict:
    """Helper to get repo name and PR number from URL."""
    path = urlparse(pr_url).path
    # /Org/Repo/pull/123
    parts = path.strip('/').split('/')
    if len(parts) >= 4 and parts[2] == 'pull':
        repo_name = f"{parts[0]}/{parts[1]}"
        pr_number = int(parts[3])
        return {"repo_name": repo_name, "pr_number": pr_number}
    raise ValueError("Invalid GitHub PR URL format")

@tool
def post_github_comment(pr_url: str, comment_body: str) -> str:
    """Posts a comment on a specific GitHub Pull Request given its URL."""
    print(f"\n--- TOOL: Posting GitHub Comment ---")
    print(f"PR: {pr_url}")

    try:
        parsed_url = parse_pr_url(pr_url)
        repo = gh.get_repo(parsed_url["repo_name"])
        pr = repo.get_pull(parsed_url["pr_number"])
        
        pr.create_issue_comment(comment_body)
        
        print("Comment posted successfully.")
        return "Successfully posted comment to GitHub."
    except Exception as e:
        print(f"Error posting GitHub comment: {e}")
        return f"Error: {e}"