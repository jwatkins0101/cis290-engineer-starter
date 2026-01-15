# Engineer Track Sample: Lead Qualification Agent

> **For coders** — Python FastAPI + OpenAI SDK + structured tool calling

## Quick Start

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Add your API keys to .env

# 3. Start the stack
docker compose up

# 4. Test the API
curl http://localhost:8000/health

# 5. View API docs
open http://localhost:8000/docs
```

## What You'll Build

A Python FastAPI service that:
1. Exposes tool endpoints the agent can call
2. Implements the agent loop (observe → decide → act → stop)
3. Stores memory in Redis with TTL
4. Logs traces to PostgreSQL
5. Enforces guardrails before risky actions

## Project Structure

```
engineer-track/
├── README.md                 # This file
├── docker-compose.yml        # API + Postgres + Redis
├── .env.example              # Environment template
├── db/
│   └── init.sql              # Database schema
├── agent-api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py               # FastAPI app and routes
│   ├── agent.py              # Agent loop implementation
│   ├── config.py             # Settings and constants
│   ├── models.py             # Pydantic schemas
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── score_lead.py     # Lead scoring tool
│   │   ├── upsert_lead.py    # Sheet update tool
│   │   ├── create_task.py    # Task creation tool
│   │   ├── draft_email.py    # Email drafting tool
│   │   └── memory.py         # Company history tool
│   ├── guardrails/
│   │   ├── __init__.py
│   │   ├── approval.py       # Approval gate logic
│   │   └── validators.py     # Input validation
│   └── db/
│       ├── __init__.py
│       ├── postgres.py       # Trace logging
│       └── redis.py          # Memory/cache
├── eval/
│   ├── run_eval.py           # Eval runner script
│   ├── sample-leads.json     # 20 test cases
│   └── expected-outputs.json # Ground truth
└── data/
    └── traces/               # JSON trace files
```

## Starter Files vs. Student-Created

This sample project includes **starter code with placeholders**. Each file contains TODO comments showing what you need to implement.

### Provided Starters (ready to use)

| File | Purpose | Status |
|------|---------|--------|
| `docker-compose.yml` | Infrastructure (API + Postgres + Redis) | Ready to use |
| `.env.example` | Environment template | Copy and configure |
| `db/init.sql` | Database schema | Ready to use |
| `agent-api/Dockerfile` | Container build | Ready to use |
| `agent-api/requirements.txt` | Python dependencies | Ready to use |
| `agent-api/main.py` | FastAPI routes | Starter with endpoints |
| `agent-api/models.py` | Pydantic schemas | Complete |
| `agent-api/config.py` | Settings and constants | Complete |
| `eval/sample-leads.json` | 20 test cases | Ready to use |
| `eval/expected-outputs.json` | Expected results | Ready to use |

### Student-Implemented (replace TODO placeholders)

| File | Week | What You Implement |
|------|------|-------------------|
| `agent-api/agent.py` | 3-5 | Agent loop logic (observe → decide → act → stop) |
| `agent-api/tools/score_lead.py` | 3 | LLM-based lead scoring |
| `agent-api/tools/upsert_lead.py` | 4 | Database/Sheets upsert |
| `agent-api/tools/create_task.py` | 4 | Task creation logic |
| `agent-api/tools/draft_email.py` | 4 | LLM email drafting |
| `agent-api/tools/memory.py` | 5 | Redis get/set operations |
| `agent-api/db/postgres.py` | 4 | Trace logging to Postgres |
| `agent-api/db/redis.py` | 5 | Redis connection and operations |
| `agent-api/guardrails/approval.py` | 7 | Approval gate logic |
| `agent-api/guardrails/validators.py` | 11 | Input validation, prompt injection defense |
| `eval/run_eval.py` | 6 | Connect eval runner to your agent |

> **Note:** All tool and database files include working placeholder implementations that print debug messages. Replace the TODO sections with real implementations as you progress through the weeks.

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/lead` | Submit a lead for qualification |
| GET | `/lead/{lead_key}` | Get lead status |
| GET | `/memory/{domain}` | Get company history |
| POST | `/approve/{action_id}` | Approve pending action |
| GET | `/traces` | List recent traces |
| GET | `/health` | Health check |

## Tools (Python Functions)

```python
# tools/score_lead.py
def score_lead(lead: LeadInput) -> ScoreResult:
    """Score a lead 0-100 with tier classification."""

# tools/upsert_lead.py
def upsert_lead_row(lead_key: str, data: LeadRow) -> UpsertResult:
    """Create or update lead in tracking sheet."""

# tools/memory.py
def get_company_history(domain: str) -> CompanyHistory:
    """Retrieve previous interactions with company."""

def write_company_summary(domain: str, summary: str) -> bool:
    """Store company summary with 90-day TTL."""
```

## Agent Loop

```python
# agent.py
class LeadAgent:
    def run(self, lead: LeadInput) -> AgentResult:
        """Main agent loop."""

        # 1. Observe - gather context
        history = self.tools.get_company_history(lead.domain)

        # 2. Decide - score and classify
        score = self.tools.score_lead(lead)

        # 3. Check guardrails
        if self.requires_approval(score):
            return self.request_approval(score)

        # 4. Act - execute tools
        self.tools.upsert_lead_row(lead)
        self.tools.create_followup_task(lead, score)

        # 5. Stop - return result
        return AgentResult(score=score, actions_taken=[...])
```

## Guardrails Implementation

```python
# guardrails/approval.py
APPROVAL_REQUIRED = {
    "reject_decision": True,
    "enterprise_scheduling": True,
    "send_email": True,
    "mark_spam": True,
}

def check_approval(action: str, context: dict) -> ApprovalCheck:
    """Check if action requires human approval."""
    if action in APPROVAL_REQUIRED:
        return ApprovalCheck(
            required=True,
            reason=f"{action} requires human approval",
            context=context
        )
    return ApprovalCheck(required=False)
```

## Week-by-Week Deliverables

| Week | What to Build |
|------|---------------|
| 3 | `score_lead` tool + basic API endpoint |
| 4 | `upsert_lead_row` with idempotency |
| 5 | Memory tools with Redis TTL |
| 6 | `run_eval.py` script, baseline metrics |
| 7 | Approval gates in `guardrails/` |
| 9 | Multi-agent routing (enterprise specialist) |
| 10 | Cost tracking middleware |
| 11 | Input validation, prompt injection defense |
| 13 | Google Sheets/Calendar integration |
| 14 | Fix failures, regression tests |
| 15 | Final demo and documentation |

## Running Evals

```bash
# Run the eval suite
python eval/run_eval.py

# Output
Running 20 test cases...
✓ 16/20 passed (80% baseline)

Failures:
- Case 7: Expected tier=nurture, got tier=qualified
- Case 12: Missing approval request for enterprise
- Case 15: Incorrect score (expected 45, got 62)
- Case 18: Failed to detect missing timeline
```

## Demo Commands

```bash
# Lead 1: Missing fields
curl -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d '{"email": "test@company.com", "company": "Acme Corp"}'

# Lead 2: SMB Qualified
curl -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d '{
    "email": "buyer@smallbiz.com",
    "company": "SmallBiz Inc",
    "need": "Need CRM integration",
    "timeline": "Q1 2026",
    "company_size": 50,
    "title": "Operations Manager"
  }'

# Lead 3: Enterprise (requires approval)
curl -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cto@bigcorp.com",
    "company": "BigCorp Industries",
    "need": "Enterprise API integration",
    "timeline": "Immediately",
    "budget": "$50,000+",
    "company_size": 500,
    "title": "CTO"
  }'
```
