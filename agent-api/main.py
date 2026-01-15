"""
Lead Qualification Agent API

Engineer Track Sample Project
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import os

app = FastAPI(
    title="Lead Qualification Agent",
    description="Sample capstone project - Engineer Track",
    version="0.1.0"
)


# --- Models ---

class LeadInput(BaseModel):
    """Input schema for lead submission."""
    email: EmailStr
    company: str
    need: Optional[str] = None
    timeline: Optional[str] = None
    budget: Optional[str] = None
    title: Optional[str] = None
    company_size: Optional[int] = None
    industry: Optional[str] = None


class ScoreResult(BaseModel):
    """Output schema for lead scoring."""
    score: int
    tier: str  # reject, nurture, qualified, needs_info
    segment: str  # smb, enterprise
    criteria_scores: dict
    missing_fields: list[str]
    confidence: str  # low, medium, high
    reasoning: str


class AgentResult(BaseModel):
    """Final agent response."""
    lead_key: str
    score_result: ScoreResult
    actions_taken: list[str]
    approval_required: bool
    approval_reason: Optional[str] = None
    trace_id: str


# --- Endpoints ---

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/lead", response_model=AgentResult)
async def submit_lead(lead: LeadInput):
    """
    Submit a lead for qualification.

    The agent will:
    1. Check for missing required fields
    2. Score the lead based on criteria
    3. Apply guardrails (approval gates)
    4. Execute allowed actions
    5. Return results with trace ID
    """
    # TODO: Implement agent loop
    # See agent.py for the full implementation

    # Placeholder response
    return AgentResult(
        lead_key=f"{lead.email.lower()}_{datetime.utcnow().strftime('%Y%W')}",
        score_result=ScoreResult(
            score=0,
            tier="needs_info",
            segment="smb",
            criteria_scores={},
            missing_fields=["need", "timeline"] if not lead.need else [],
            confidence="low",
            reasoning="Placeholder - implement scoring logic"
        ),
        actions_taken=[],
        approval_required=False,
        trace_id=f"trace_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    )


@app.get("/lead/{lead_key}")
async def get_lead(lead_key: str):
    """Get lead status by key."""
    # TODO: Implement database lookup
    raise HTTPException(status_code=404, detail="Lead not found")


@app.get("/memory/{domain}")
async def get_company_history(domain: str):
    """Get company interaction history from memory."""
    # TODO: Implement Redis lookup
    return {
        "domain": domain,
        "last_contact_date": None,
        "last_outcome": None,
        "notes_summary": None,
        "total_leads_count": 0
    }


@app.post("/approve/{action_id}")
async def approve_action(action_id: str, approved: bool):
    """Approve or reject a pending action."""
    # TODO: Implement approval workflow
    return {
        "action_id": action_id,
        "approved": approved,
        "processed_at": datetime.utcnow().isoformat()
    }


@app.get("/traces")
async def list_traces(limit: int = 10):
    """List recent agent traces."""
    # TODO: Implement trace retrieval from Postgres
    return {"traces": [], "total": 0}


# --- Startup ---

@app.on_event("startup")
async def startup():
    """Initialize connections on startup."""
    print("Starting Lead Qualification Agent API...")
    print(f"Gemini API Key configured: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
    print(f"Database URL configured: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")
    print(f"Redis URL configured: {'Yes' if os.getenv('REDIS_URL') else 'No'}")
