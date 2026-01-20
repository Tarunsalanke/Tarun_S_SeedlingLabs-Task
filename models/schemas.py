from pydantic import BaseModel, Field, HttpUrl
from typing import List


class IssueAnalysis(BaseModel):
    summary: str = Field(
        description="One-sentence summary of the user's problem or request"
    )
    type: str = Field(
        description="One of: bug, feature_request, documentation, question, or other"
    )
    priority_score: str = Field(
        description="Score from 1 (low) to 5 (critical) with brief justification"
    )
    suggested_labels: List[str] = Field(
        description="2-3 relevant GitHub labels"
    )
    potential_impact: str = Field(
        description="Impact on users if the issue is a bug"
    )


class IssueRequest(BaseModel):
    repo_url: HttpUrl
    issue_number: int
