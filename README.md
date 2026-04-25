# remapd

> Reward-guided redistricting optimizer + legislator-facing AI copilot.

`remapd` is a hackathon prototype that makes redistricting analysis more transparent by combining:
- a multi-objective district optimizer,
- Census-grounded data tooling,
- and a LangGraph-based explanation layer for non-technical policymakers.

---

## Brief Project Description

Redistricting is often treated like a technical black box. `remapd` turns it into an inspectable workflow:
1. Generate and improve county-to-district plans with a weighted optimization objective.
2. Measure fairness, population balance, compactness proxy, and voting-rights proxy.
3. Explain tradeoffs in plain language through specialized agents (engine, civil-rights, legislative).

The goal is not to replace legal counsel. The goal is to give stakeholders a clear, auditable baseline for discussion.

---

## Context

We built this project in the spirit of moving from technological adolescence to democratic maturity: AI should not just be powerful, it should be accountable.

In redistricting, opaque workflows can enable map designs that weaken representation through packing/cracking patterns and race-aware manipulation. Communities most in need of fair representation are often the first to lose it when process transparency is weak.

`remapd` responds to that gap with an explicit pipeline: optimize plans with measurable criteria, ground claims in Census-backed data, and present conclusions in language legislators and community advocates can use.

---

## Impact

`remapd` is designed to scale fair-process capacity, not partisan outcomes:
- **Strengthen democratic process:** make district tradeoffs visible instead of hidden in expert-only workflows.
- **Expand access:** give advocacy groups and public-interest teams interpretable, metric-backed alternatives.
- **Center dignity in evaluation:** explicitly score fairness and voting-rights signals instead of pretending all maps are equivalent.

---

## The Problem

Redistricting decisions are high-stakes and usually hard to audit in real time:
- Technical complexity blocks public scrutiny.
- Tradeoffs are explained inconsistently, if at all.
- Legal/fairness arguments can drift away from measurable evidence.

---

## Our Solution

`remapd` provides an end-to-end loop:
- **Optimize** a district plan under weighted social/legal objectives.
- **Compare** against a baseline with per-metric improvement.
- **Explain** outputs in structured, non-technical sections for legislators.
- **Ground** external claims using Census API tool calls with provenance metadata.

---

## Model and Optimization (What We Actually Run)

### Algorithm

Despite the class name `RLAgent`, the current MVP uses **reward-guided local search with simulated annealing behavior**, not PPO training.

- State representation: `assignment[county_fips] = district_id`
- Move: reassign one county to a different district
- Acceptance:
  - always accept better reward,
  - sometimes accept worse reward based on exploration + temperature to escape local optima.

### Reward Function

The optimizer maximizes:

\[
R = w_r S_r + w_p S_p + w_c S_c + w_v S_v
\]

Where:
- `S_r`: racial fairness proxy
- `S_p`: population equality
- `S_c`: compactness proxy (county-count balance)
- `S_v`: voting-rights proxy (opportunity district heuristic)

Default weights:
- `racial_weight = 0.35`
- `population_weight = 0.30`
- `compactness_weight = 0.20`
- `vra_weight = 0.15`

### Hyperparameters / Runtime Parameters

From `POST /api/agent/run`:
- `n_districts` - number of districts
- `n_steps` - iteration budget
- `ent_coef` - exploration rate
- component weights (`racial_weight`, `population_weight`, `compactness_weight`, `vra_weight`)

Internal annealing params include `temperature` and `cooling_rate`.

### What is optimized vs tuned

- **Optimized:** county-to-district assignments.
- **Tuned by user:** reward weights/hyperparameters.
- **Not in this MVP:** neural policy fine-tuning.

---

## Agents and LangGraph Backend

The backend uses a LangGraph workflow to make results easier for non-technical audiences.

### Agent roles

1. **Engine Agent**  
   Computes and validates the score vector from the proposed map.

2. **Civil Rights Advocate Agent**  
   Interprets equity and voting-rights implications (including opportunity-district signals).

3. **Legislative Agent**  
   Frames compliance and policy implications for decision-makers.

4. **Liaison Node (Synthesis)**  
   Produces final structured memo output:
   - Engine Agent
   - Civil Rights Advocate Agent
   - Legislative Agent
   - Summary

### Why this reduces hallucination risk

- Claims are anchored to structured model outputs and tool payloads.
- Census metrics come from a tool call path, not model memory.
- Provenance/audit metadata is attached for traceability.

---

## MCP-style Census Tooling

`backend/mcp_server.py` provides lightweight MCP-style tools:
- `fetch_census_metrics(...)` - calls Census ACS API
- `verify_audit_trail(...)` - validates call provenance

These tools are used by both the social impact agent flow and policy copilot flow to ground summaries in external data.

---

## API Surface (MVP)

Key backend routes:
- `POST /api/agent/run`
- `POST /api/agent/stop`
- `GET /api/agent/metrics`
- `GET /api/agent/all-plans`
- `GET /api/agent/liaison/model`
- `POST /api/agent/evaluate-liaison`
- `POST /api/agent/stream-evaluate-liaison`
- `GET /api/states/{state}/district-plan`
- `GET /api/states/{state}/demographics`
- `POST /api/policy/query`
- `POST /api/mcp/census`
- `POST /api/mcp/audit`

---

## Tech Stack

### Frontend
- Next.js (App Router) + React + TypeScript
- D3 + TopoJSON (`us-atlas`) for map rendering
- TailwindCSS
- Recharts for metrics panels

### Backend
- FastAPI + Uvicorn
- Pydantic + `pydantic-settings`
- NumPy
- LangGraph + LangChain Core message types
- HTTPX
- DuckDB (project-level data path configured in env)

### Data
- US Census Bureau ACS API (live calls)
- County TopoJSON from `frontend/public/counties-10m.json`

---

## Setup Instructions

### 1) Clone and install

```bash
git clone <your-repo-url>
cd remapd
```

### 2) Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env`:

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

### 3) Frontend

```bash
cd ../frontend
npm install
npm run dev
```

Open:
- Frontend: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`

### 4) Quick health checks

```bash
curl -s http://127.0.0.1:8000/api/agent/liaison/model
curl -s http://127.0.0.1:8000/api/states/MO/demographics
```

---

## Demo Video

Add your demo link here:

- **Demo URL:** `<paste-video-link>`

Suggested 3-minute flow:
1. Show baseline map and metrics.
2. Run optimizer and show improvement vs baseline.
3. Trigger liaison output and read the 4 sections.
4. Mention Census tool grounding + provenance.
