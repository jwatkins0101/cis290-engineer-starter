"""
Agent Loop Implementation

Students build this in Week 3-7.
The agent loop follows: observe -> decide -> act -> stop
"""

from typing import Optional
from models import LeadInput, ScoreResult, AgentResult
from tools.memory import get_company_history
from tools.score_lead import score_lead
from tools.upsert_lead import upsert_lead_row
from tools.create_task import create_followup_task
from guardrails.approval import check_approval, ApprovalCheck
import uuid
from datetime import datetime


class LeadAgent:
    """
    Lead Qualification Agent

    Implements the core agent loop for qualifying incoming leads.
    """

    def __init__(self):
        # TODO: Initialize connections (Week 5)
        # - Redis client for memory
        # - Postgres client for traces
        # - OpenAI client for scoring
        pass

    def run(self, lead: LeadInput) -> AgentResult:
        """
        Main agent loop.

        Steps:
        1. Observe - gather context (company history, existing data)
        2. Decide - score and classify the lead
        3. Check guardrails - determine if approval needed
        4. Act - execute appropriate actions
        5. Stop - return result with trace ID

        Args:
            lead: The incoming lead data

        Returns:
            AgentResult with score, actions taken, and trace ID
        """
        trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        actions_taken = []

        # --- Step 1: Observe ---
        # TODO: Implement in Week 5
        # history = get_company_history(self._extract_domain(lead.email))
        history = None

        # --- Step 2: Decide ---
        # TODO: Implement in Week 3
        # score_result = score_lead(lead)
        score_result = self._placeholder_score(lead)

        # --- Step 3: Check Guardrails ---
        # TODO: Implement in Week 7
        approval_check = self._check_guardrails(score_result)

        if approval_check.required:
            return AgentResult(
                lead_key=self._generate_lead_key(lead.email),
                score_result=score_result,
                actions_taken=actions_taken,
                approval_required=True,
                approval_reason=approval_check.reason,
                trace_id=trace_id
            )

        # --- Step 4: Act ---
        # TODO: Implement in Week 4
        # upsert_lead_row(lead_key, lead, score_result)
        # actions_taken.append("upsert_lead_row")

        # TODO: Implement in Week 4
        # create_followup_task(lead, score_result)
        # actions_taken.append("create_followup_task")

        # --- Step 5: Stop ---
        return AgentResult(
            lead_key=self._generate_lead_key(lead.email),
            score_result=score_result,
            actions_taken=actions_taken,
            approval_required=False,
            trace_id=trace_id
        )

    def _extract_domain(self, email: str) -> str:
        """Extract domain from email address."""
        return email.split("@")[-1].lower()

    def _generate_lead_key(self, email: str) -> str:
        """Generate unique lead key from email and week."""
        week = datetime.utcnow().strftime("%Y%W")
        return f"{email.lower()}_{week}"

    def _placeholder_score(self, lead: LeadInput) -> ScoreResult:
        """Placeholder scoring logic - replace with LLM call in Week 3."""
        missing = []
        if not lead.need:
            missing.append("need")
        if not lead.timeline:
            missing.append("timeline")

        if missing:
            return ScoreResult(
                score=0,
                tier="needs_info",
                segment="smb",
                criteria_scores={},
                missing_fields=missing,
                confidence="low",
                reasoning="Missing required fields"
            )

        # Basic placeholder scoring
        score = 50
        if lead.budget:
            score += 15
        if lead.title and any(t in lead.title.lower() for t in ["ceo", "cto", "vp", "director"]):
            score += 15
        if lead.company_size and lead.company_size > 200:
            score += 10

        tier = "nurture" if score < 70 else "qualified"
        segment = "enterprise" if lead.company_size and lead.company_size > 200 else "smb"

        return ScoreResult(
            score=score,
            tier=tier,
            segment=segment,
            criteria_scores={"placeholder": score},
            missing_fields=[],
            confidence="low",
            reasoning="Placeholder scoring - implement LLM scoring in Week 3"
        )

    def _check_guardrails(self, score_result: ScoreResult) -> ApprovalCheck:
        """Check if the action requires approval."""
        # TODO: Implement full guardrails in Week 7
        if score_result.tier == "reject":
            return ApprovalCheck(
                required=True,
                reason="Reject decisions require human approval"
            )
        if score_result.segment == "enterprise" and score_result.tier == "qualified":
            return ApprovalCheck(
                required=True,
                reason="Enterprise scheduling requires approval"
            )
        return ApprovalCheck(required=False)
