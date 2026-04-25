# remapd

> RL-inspired + Agentic AI dynamic redistricting engine

`remapd` makes redistricting analysis more transparent by combining:
- a multi-objective district optimizer,
- real Census-grounded data tooling,
- and a LangGraph-based explanation layer for non-technical users.

## The Problem

Redistricting is one of the most consequential and least transparent parts of U.S. democracy. In practice, districting can be manipulated through gerrymandering tactics that weaken fair and equitable representation. Communities that are already underrepresented are often most affected when district boundaries are engineered for political advantage.

## Our Solution

`remapd` improves redistricting with two core principles:

- **Transparency:** Every district plan is scored with clear, inspectable metrics.
- **Objectivity:** Every map is evaluated with the same weighted framework:
  fairness, population balance, compactness proxy, and voting-rights proxy.

### From Analysis to Action

`remapd` is built to help civic, legal, and policymaking teams act, not just observe.

Policy ideas often come from outside legislatures, including advocacy groups and organized coalitions. `remapd` helps those groups participate with credible, data-backed alternatives. It also helps policymakers present proposals with measurable evidence, making public communication more transparent and easier to trust.

With `remapd`, teams can:

- **Propose a model map early**  
  Submit a metrics-backed alternative before closed-door drafts control the process.

- **Strengthen lobbying and testimony**  
  Provide fast, defensible answers on fairness, population balance, and tradeoffs.

- **Support litigation strategy**  
  Produce consistent quantitative evidence that helps legal teams evaluate inequity signals.

- **Build public confidence in reforms**  
  Pair plain-language explanations with quantitative metrics so proposed changes are understandable, auditable, and easier to defend.

### Why This Matters

The goal is simple: move civic actors from being consulted to shaping the evidence itself.

`remapd` gives public-interest organizations technical capacity that has traditionally been expensive and hard to access.

Most importantly, this turns fair-mapping from a reactive conversation into proactive action: better draft maps, stronger testimony, clearer legal evidence, and policy proposals that are transparently backed by quantitative metrics.

## Who It’s For

- **Advocacy organizations** — propose fairer alternatives.
- **Civic and public-interest groups** — hold processes accountable.
- **Policy and legal teams** — build evidence-based arguments.
- **Policymakers and legislative staff** — present transparently scored proposals and communicate tradeoffs clearly to constituents.
- **Engaged citizens** — understand maps and demand measurable standards.

## Tech Stack

### Frontend
- **Next.js + React + TypeScript + shadcn/ui** for the web app, component system, and UI logic
- **D3 + TopoJSON (`us-atlas`)** for U.S. and state-level map rendering
- **Tailwind CSS** for styling
- **Recharts** for optimizer metrics visualization

### Backend
- **FastAPI + Uvicorn** for API endpoints and local server runtime
- **Pydantic + pydantic-settings** for typed request/response models and environment config
- **NumPy** for optimization math and scoring
- **LangGraph** for multi-agent orchestration (Engine, Civil Rights, Legislative, Liaison)
- **HTTPX** for Census API and model HTTP integrations
- **DuckDB** for local analytical data workflows

### Data & AI
- **U.S. Census Bureau ACS API** for demographic/economic grounding
- **Anthropic Claude API** for multi-agent reasoning and non-technical structured explanations
- **MCP-style tool layer** for Census fetch + audit/provenance verification

## Setup

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `backend/.env`:
```env
CENSUS_API_KEY=your_census_key
DUCKDB_PATH=data/remapd.duckdb
ANTHROPIC_API_KEY=your_anthropic_key
LIAISON_MODEL=claude-3-5-sonnet-20241022
```

Run backend:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Quickstart

Start backend:
```bash
cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000
```

Start frontend (new terminal):
```bash
cd frontend && npm run dev
```

Check backend health:
```bash
curl -s http://127.0.0.1:8000/api/agent/liaison/model
```