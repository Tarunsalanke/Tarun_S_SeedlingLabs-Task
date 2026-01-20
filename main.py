from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from services.github_service import GitHubIssueFetcher
from services.llm_service import IssueAnalyzer
from models.schemas import IssueRequest, IssueAnalysis

load_dotenv()

app = FastAPI(
    title="AI-Powered GitHub Issue Assistant",
    description="Analyzes GitHub issues using LLMs",
    version="1.0.0"
)

github_fetcher = GitHubIssueFetcher(
    github_token=os.getenv("GITHUB_TOKEN")
)

issue_analyzer = IssueAnalyzer(
    api_key=os.getenv("GROQ_API_KEY")
)


@app.post("/analyze-issue", response_model=IssueAnalysis)
def analyze_issue(request: IssueRequest):
    try:
        issue_data = github_fetcher.fetch_issue(
            repo_url=str(request.repo_url),
            issue_number=request.issue_number
        )

        analysis = issue_analyzer.analyze(
            title=issue_data["title"],
            body=issue_data["body"],
            comments=issue_data["comments"]
        )

        return analysis

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
