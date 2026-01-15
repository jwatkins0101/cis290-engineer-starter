"""
Lead Scoring Tool

Scores a lead using LLM-based evaluation against defined criteria.
Students implement this in Week 3.
"""

from typing import Optional
import json
import google.generativeai as genai
from models import LeadInput, ScoreResult
from config import settings, SCORING_WEIGHTS, REQUIRED_FIELDS


# System prompt for lead scoring
SCORING_SYSTEM_PROMPT = """You are a lead qualification assistant. Score incoming leads based on six criteria and return a structured JSON response.

## Scoring Criteria (100 points total)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Industry Fit | 20 | Target vertical match |
| Budget | 20 | Meets minimum threshold |
| Authority | 15 | Decision-maker or influencer |
| Need | 20 | Clear problem statement |
| Timeline | 15 | Urgency indicator |
| Company Size | 10 | SMB (10-200) vs Enterprise (200+) |

## Scoring Rules

- Score each criterion 0-100, then apply weight
- Missing data = 50 (neutral) unless required field
- Required fields: email, company, need, timeline
- If required field missing, set tier to "needs_info"

## Score Tiers

| Score | Tier | Action |
|-------|------|--------|
| 0-39 | reject | Requires human approval |
| 40-69 | nurture | Auto-create task, draft email |
| 70-100 | qualified | Full workflow, approval for enterprise |

## Output Format

Always respond with valid JSON:

{
  "score": 0-100,
  "tier": "reject" | "nurture" | "qualified" | "needs_info",
  "segment": "smb" | "enterprise",
  "criteria_scores": {
    "industry_fit": 0-100,
    "budget": 0-100,
    "authority": 0-100,
    "need": 0-100,
    "timeline": 0-100,
    "company_size": 0-100
  },
  "missing_fields": ["field1", "field2"],
  "confidence": "low" | "medium" | "high",
  "reasoning": "Brief explanation of score"
}"""


def score_lead(lead: LeadInput) -> ScoreResult:
    """
    Score a lead 0-100 with tier classification.

    Uses an LLM to evaluate the lead against predefined criteria
    and returns a structured score result.

    Args:
        lead: The lead data to score

    Returns:
        ScoreResult with score, tier, segment, and reasoning
    """
    # Check for missing required fields first
    missing_fields = _check_missing_fields(lead)
    if missing_fields:
        return ScoreResult(
            score=0,
            tier="needs_info",
            segment="smb",
            criteria_scores={k: 0 for k in SCORING_WEIGHTS.keys()},
            missing_fields=missing_fields,
            confidence="high",
            reasoning=f"Missing required fields: {', '.join(missing_fields)}"
        )

    # TODO: Implement LLM scoring in Week 3
    # For now, return placeholder
    # genai.configure(api_key=settings.GEMINI_API_KEY)
    # model = genai.GenerativeModel(settings.LLM_MODEL)
    # response = model.generate_content(...)

    return _placeholder_score(lead)


def _check_missing_fields(lead: LeadInput) -> list[str]:
    """Check for missing required fields."""
    missing = []
    lead_dict = lead.model_dump()
    for field in REQUIRED_FIELDS:
        if not lead_dict.get(field):
            missing.append(field)
    return missing


def _placeholder_score(lead: LeadInput) -> ScoreResult:
    """
    Placeholder scoring logic.

    Replace this with LLM-based scoring in Week 3.
    """
    # Simple heuristic scoring
    score = 50

    criteria_scores = {
        "industry_fit": 50,
        "budget": 50,
        "authority": 50,
        "need": 50,
        "timeline": 50,
        "company_size": 50,
    }

    # Adjust based on available data
    if lead.budget:
        budget_score = 70 if "$" in lead.budget else 50
        criteria_scores["budget"] = budget_score

    if lead.title:
        title_lower = lead.title.lower()
        if any(t in title_lower for t in ["ceo", "cto", "cfo", "owner", "founder"]):
            criteria_scores["authority"] = 90
        elif any(t in title_lower for t in ["vp", "director", "head"]):
            criteria_scores["authority"] = 75
        elif any(t in title_lower for t in ["manager"]):
            criteria_scores["authority"] = 60

    if lead.need and len(lead.need) > 20:
        criteria_scores["need"] = 70

    if lead.timeline:
        timeline_lower = lead.timeline.lower()
        if any(t in timeline_lower for t in ["immediate", "asap", "urgent", "this month"]):
            criteria_scores["timeline"] = 90
        elif any(t in timeline_lower for t in ["q1", "q2", "next quarter"]):
            criteria_scores["timeline"] = 70

    if lead.company_size:
        if lead.company_size > 200:
            criteria_scores["company_size"] = 80
        elif lead.company_size > 50:
            criteria_scores["company_size"] = 70

    # Calculate weighted score
    total_score = sum(
        criteria_scores[k] * (SCORING_WEIGHTS[k] / 100)
        for k in SCORING_WEIGHTS.keys()
    )

    # Determine tier
    if total_score < 40:
        tier = "reject"
    elif total_score < 70:
        tier = "nurture"
    else:
        tier = "qualified"

    # Determine segment
    segment = "enterprise" if lead.company_size and lead.company_size > 200 else "smb"

    return ScoreResult(
        score=int(total_score),
        tier=tier,
        segment=segment,
        criteria_scores=criteria_scores,
        missing_fields=[],
        confidence="low",
        reasoning="Placeholder scoring - implement LLM scoring in Week 3"
    )
