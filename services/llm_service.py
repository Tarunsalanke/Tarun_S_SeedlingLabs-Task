from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import IssueAnalysis


class IssueAnalyzer:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):

        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert software engineering triage assistant. "
                    "Analyze GitHub issues and return ONLY valid JSON "
                    "that strictly matches the required schema."
                ),
                (
                    "human",
                    """
Analyze the following GitHub issue and respond ONLY with JSON.

Issue Title:
{title}

Issue Description:
{body}

Comments:
{comments}

Instructions:
- Classify the issue type correctly
- Assign a priority score from 1 to 5 with justification
- Suggest 2-3 relevant GitHub labels
- Describe the potential impact on users

Rules:
- Output ONLY valid JSON
- No markdown
- No explanations
- Type must be one of:
  bug, feature_request, documentation, question, other
"""
                ),
            ]
        )

        self.chain = self.prompt | self.llm.with_structured_output(IssueAnalysis)

    def analyze(self, title: str, body: str, comments: list[str]) -> IssueAnalysis:
        joined_comments = "\n".join(comments) if comments else "No comments"

        return self.chain.invoke(
            {
                "title": title,
                "body": body[:4000],
                "comments": joined_comments[:4000],
            }
        )
