"""
Lead Upsert Tool

Creates or updates a lead row in the tracking system.
Students implement this in Week 4.
"""

from typing import Optional
from datetime import datetime
from models import LeadInput, ScoreResult, LeadRow


class UpsertResult:
    """Result of an upsert operation."""

    def __init__(self, success: bool, lead_key: str, created: bool, message: str = ""):
        self.success = success
        self.lead_key = lead_key
        self.created = created  # True if new, False if updated
        self.message = message


def upsert_lead_row(
    lead_key: str,
    lead: LeadInput,
    score_result: ScoreResult
) -> UpsertResult:
    """
    Create or update lead in tracking sheet/database.

    This tool is idempotent - calling it multiple times with the same
    lead_key will update the existing record rather than create duplicates.

    Args:
        lead_key: Unique identifier for the lead (email_YYYYWW)
        lead: The original lead input data
        score_result: The scoring result from score_lead

    Returns:
        UpsertResult indicating success and whether record was created/updated
    """
    # TODO: Implement in Week 4
    # Options:
    # 1. Google Sheets API (matches builder track)
    # 2. PostgreSQL database
    # 3. Both (sheets for visibility, DB for querying)

    # Build the lead row
    lead_row = LeadRow(
        lead_key=lead_key,
        email=lead.email,
        company=lead.company,
        score=score_result.score,
        tier=score_result.tier,
        segment=score_result.segment,
        need=lead.need,
        timeline=lead.timeline,
        budget=lead.budget,
        title=lead.title,
        company_size=lead.company_size,
        industry=lead.industry,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        status="new",
        notes=score_result.reasoning
    )

    # Placeholder implementation
    # TODO: Replace with actual database/sheets operation
    print(f"[PLACEHOLDER] Would upsert lead: {lead_key}")
    print(f"  Score: {score_result.score}, Tier: {score_result.tier}")

    return UpsertResult(
        success=True,
        lead_key=lead_key,
        created=True,  # Assume new for placeholder
        message="Placeholder - implement database upsert in Week 4"
    )


def get_lead_by_key(lead_key: str) -> Optional[LeadRow]:
    """
    Retrieve a lead by its key.

    Args:
        lead_key: The unique lead identifier

    Returns:
        LeadRow if found, None otherwise
    """
    # TODO: Implement in Week 4
    print(f"[PLACEHOLDER] Would lookup lead: {lead_key}")
    return None


def update_lead_status(lead_key: str, status: str, notes: Optional[str] = None) -> bool:
    """
    Update the status of an existing lead.

    Args:
        lead_key: The unique lead identifier
        status: New status (new, contacted, meeting, closed)
        notes: Optional notes to append

    Returns:
        True if updated successfully
    """
    # TODO: Implement in Week 4
    print(f"[PLACEHOLDER] Would update lead {lead_key} to status: {status}")
    return True
