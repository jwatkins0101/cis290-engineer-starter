"""
Guardrails Module

Safety checks and approval gates for the Lead Qualification Agent.
Students implement these in Week 7.

Guardrails include:
- Approval gates for high-risk actions
- Input validation and sanitization
- Output validation
- Rate limiting (Week 10)
"""

from .approval import check_approval, ApprovalCheck, request_approval
from .validators import validate_lead_input, sanitize_input

__all__ = [
    "check_approval",
    "ApprovalCheck",
    "request_approval",
    "validate_lead_input",
    "sanitize_input",
]
