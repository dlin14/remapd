# remapd

> AI-powered redistricting analysis — optimizer + multi-agent explanation layer

`remapd` makes redistricting transparent and actionable by combining a multi-objective district optimizer with real Census data and a Claude-powered multi-agent analysis layer.

---

## The Problem

Redistricting is one of the most consequential and least transparent processes in U.S. democracy. District boundaries directly affect who gets represented — yet the process is often opaque, technically inaccessible, and vulnerable to political manipulation.

Communities that are already underrepresented are most affected when boundaries are engineered for partisan advantage.

## Our Solution

`remapd` gives civic, legal, and policy teams the tools to participate with credible, data-backed alternatives:

- **Optimizer** — simulated annealing search over county-to-district assignments, scored on four fairness dimensions
- **Real data** — Census ACS 5-year estimates for population and demographic composition
- **Multi-agent analysis** — Claude explains every plan through three specialist lenses (engine, civil rights, legislative) plus a plain-language summary
- **Interactive map** — D3-rendered U.S. and state maps show real 118th Congress boundaries vs. the optimized plan side by side

### Four Fairness Dimensions

| Metric | What it measures |
|---|---|
| **Racial Fairness** | How evenly minority share is distributed across districts vs. state average |
| **Population Equality** | How close each district is to the state's ideal population (one-person-one-vote) |
| **Compactness** | Geographic spread of counties within each district (RMS distance from district centroid, normalized by state extent) |
| **Voting Rights** | Fraction of districts where minority voters hold meaningful influence (≥ 45% share) |

All four are combined into a single weighted reward. Users can adjust weights in the UI before running the optimizer.

### From Analysis to Action

`remapd` is built for teams that need to act, not just observe:

- **Advocacy organizations** — propose fairer alternatives with quantitative backing
- **Policy and legal teams** — build measurable arguments for redistricting reform
- **Policymakers and legislative staff** — present transparently scored proposals
- **Civic groups** — hold closed-door processes accountable with public evidence

---

## Tech Stack

### Frontend
- **Next.js 15 + React + TypeScript** with shadcn/ui components
- **D3 + TopoJSON** for interactive U.S. and state-level map rendering
- **Tailwind CSS** for styling

### Backend
- **FastAPI + Uvicorn** — REST API and async server runtime
- **Pydantic** — typed request/response models and environment config
- **NumPy** — simulated annealing optimizer and scoring math
- **LangGraph** — multi-agent orchestration (Engine Agent, Civil Rights Agent, Legislative Agent, Liaison)
- **HTTPX** — async Census API integration
- **DuckDB** — local analytical data layer

### Data & AI
- **U.S. Census Bureau ACS 5-Year API** — real county-level population and demographic data
- **Anthropic Claude API** — structured four-section analysis per optimizer run
- **U.S. Census Bureau TopoJSON** — county and congressional district boundary geometry

---

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Census API key (free at [api.census.gov](https://api.census.gov/data/key_signup.html))
- Anthropic API key (for the multi-agent analysis panel)

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
CENSUS_API_KEY=your_census_key
ANTHROPIC_API_KEY=your_anthropic_key
LIAISON_MODEL=claude-3-5-sonnet-20241022
DUCKDB_PATH=data/remapd.duckdb
ALLOWED_ORIGINS=http://localhost:3000
```

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Verify

```bash
curl -s http://localhost:8000/api/agent/liaison/model | python3 -m json.tool
```

---

## How It Works

1. **Select a state** on the home map — click any state to open its detail page
2. **Adjust weights** — use the sliders to set how much the optimizer cares about each fairness dimension
3. **Ask the agent** — type a plain-language request ("prioritize minority voting rights") to get Claude's suggested parameter set with a three-section analysis
4. **Run the optimizer** — the simulated annealing search runs on the backend and streams progress to the UI
5. **Inspect results** — the map switches from official 118th Congress boundaries to the optimized county-level plan; the metrics panel shows before/after scores

---

## Deployment

- **Backend**: Railway (Procfile included — `uvicorn main:app --host 0.0.0.0 --port $PORT`)
- **Frontend**: Vercel — set `NEXT_PUBLIC_API_URL` to your Railway backend URL

---

## Disclaimer

`remapd` is a research and demonstration tool built for the Claude Hackathon 2025. Output maps are not legal redistricting plans. Any analysis produced by the agent is informational only and does not constitute legal advice. Formal legal and demographic review is required before any map is used in an official context.
