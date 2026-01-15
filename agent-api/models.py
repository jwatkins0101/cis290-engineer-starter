"""
Pydantic Models

Data models for the Lead Qualification Agent.
These define the schema for inputs, outputs, and internal data structures.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# --- Enums ---

class Tier(str, Enum):
    """Lead qualification tiers."""
    REJECT = "reject"
    NURTURE = "nurture"
    QUALIFIED = "qualified"
    NEEDS_INFO = "needs_info"


class Segment(str, Enum):
    """Company size segments."""
    SMB = "smb"
    ENTERPRISE = "enterprise"


class Confidence(str, Enum):
    """Scoring confidence levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# --- Input Models ---

class LeadInput(BaseModel):
    """Input schema for lead submission."""
    email: EmailStr
    company: str
    need: Optional[str] = None
    timeline: Optional[str] = None
    budget: Optional[str] = None
    title: Optional[str] = None
    company_size: Optional[int] = Field(None, ge=1)
    industry: Optional[str] = None


# --- Output Models ---

class CriteriaScores(BaseModel):
    """Individual scoring criteria results."""
    industry_fit: int = Field(default=50, ge=0, le=100)
    budget: int = Field(default=50, ge=0, le=100)
    authority: int = Field(default=50, ge=0, le=100)
    need: int = Field(default=50, ge=0, le=100)
    timeline: int = Field(default=50, ge=0, le=100)
    company_size: int = Field(default=50, ge=0, le=100)


class ScoreResult(BaseModel):
    """Output schema for lead scoring."""
    score: int = Field(ge=0, le=100)
    tier: str  # Using str for flexibility, could use Tier enum
    segment: str  # Using str for flexibility, could use Segment enum
    criteria_scores: dict
    missing_fields: List[str] = []
    confidence: str  # Using str for flexibility, could use Confidence enum
    reasoning: str


class AgentResult(BaseModel):
    """Final agent response."""
    lead_key: str
    score_result: ScoreResult
    actions_taken: List[str]
    approval_required: bool
    approval_reason: Optional[str] = None
    trace_id: str


# --- Memory Models ---

class CompanyHistory(BaseModel):
    """Company interaction history from memory."""
    domain: str
    last_contact_date: Optional[datetime] = None
    last_outcome: Optional[str] = None
    notes_summary: Optional[str] = None
    total_leads_count: int = 0


# --- Database Models ---

class LeadRow(BaseModel):
    """Lead row for database/sheet storage."""
    lead_key: str
    email: str
    company: str
    score: int
    tier: str
    segment: str
    need: Optional[str] = None
    timeline: Optional[str] = None
    budget: Optional[str] = None
    title: Optional[str] = None
    company_size: Optional[int] = None
    industry: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "new"
    notes: Optional[str] = None


class TraceRecord(BaseModel):
    """Agent execution trace for debugging and evaluation."""
    trace_id: str
    lead_key: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    input_data: dict
    score_result: Optional[dict] = None
    actions_taken: List[str] = []
    approval_required: bool = False
    approval_reason: Optional[str] = None
    error: Optional[str] = None
    token_usage: Optional[dict] = None


# --- Approval Models ---

class ApprovalRequest(BaseModel):
    """Pending approval request."""
    action_id: str
    action_type: str
    lead_key: str
    reason: str
    context: dict
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, approved, rejected


class ApprovalResponse(BaseModel):
    """Approval decision."""
    action_id: str
    approved: bool
    decided_by: Optional[str] = None
    decided_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
