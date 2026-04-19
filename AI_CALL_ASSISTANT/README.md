<div align="center">

# 🤖 AI Call Intelligence Platform
### Autonomous Multi-Agent Enterprise System | Distributor → Vendor

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Zero human interaction. Fully autonomous. Sub-300ms resolution.**
> A production-grade, 7-agent AI pipeline that automatically processes distributor queries,
> generates solutions, creates action items, escalates priorities, and notifies distributors — all in real-time.

</div>

---

## 📌 Table of Contents

- [What This Project Does](#-what-this-project-does)
- [Live Demo Screenshots](#-live-demo-screenshots)
- [System Architecture](#-system-architecture)
- [The 7 AI Agents](#-the-7-ai-agents)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [How to Use](#-how-to-use)
- [Knowledge Base](#-knowledge-base)
- [Database Schema](#-database-schema)
- [Business Impact](#-business-impact)
- [Author](#-author)

---

## 🎯 What This Project Does

Most distributor-vendor communication systems require manual effort — a sales rep reads a query, finds a solution, writes a response, and creates follow-up tasks. This takes hours.

This platform **eliminates all of that**.

When a distributor submits any query or call transcript, the system:

1. **Automatically classifies** it into one of 8 business categories
2. **Analyses the emotional tone** (Positive / Neutral / Negative)
3. **Finds the best 3 solutions** from an intelligent Knowledge Base
4. **Generates action items** with owners and deadlines
5. **Escalates** if it detects urgency (P1/P2/P3 priority)
6. **Notifies the distributor** with a full resolution report

All within **under 300 milliseconds**.

---

## 🖥️ Live Demo Screenshots

### Overview Dashboard
```
╔══════════════════════════════════════════════════════════╗
║  🤖 AI Call Intelligence Platform    ● LIVE              ║
║  Distributor→Vendor | 7-Agent Pipeline | Real-time       ║
╠══════╦══════════╦═══════╦════════════╦════════════════╗  ║
║  15  ║    15    ║   0   ║     11     ║    296ms       ║  ║
║Total ║Resolved  ║Queue  ║Escalations ║ Avg Resolution ║  ║
║      ║ 100%     ║ Auto  ║  Attention ║ Near real-time ║  ║
╚══════╩══════════╩═══════╩════════════╩════════════════╝  ║
╚══════════════════════════════════════════════════════════╝
```

| Tab | What You See |
|---|---|
| 🏠 **Overview** | Live KPI cards, query feed, distributor notifications, health table |
| 🤖 **Agent Pipeline** | 7-step visual pipeline + real-time agent activity log |
| 📥 **Submit Query** | Full agent pipeline result in ~272ms |
| 📊 **Analytics** | Plotly charts — categories, sentiment, trends, escalations |
| 📋 **Query Logs** | Filterable log with expandable solutions + action items |
| 🔴 **Escalations** | Auto-detected P1/P2/P3 cards with assigned owners |
| 📢 **Distributor Portal** | Per-distributor self-service: queries, notifications, tasks |
| 🧠 **Knowledge Base** | Searchable 8-category × 20+ solution library |

---

## 🏗️ System Architecture

```
                    ┌─────────────────────────┐
                    │   Distributor Query      │
                    │   (Any Text / Transcript)│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    OrchestratorAgent     │  ◄── Master Controller
                    │  Manages full pipeline   │
                    └──┬──────────────────────┘
                       │
          ┌────────────┼────────────────────────────────┐
          │            │            │                    │
          ▼            ▼            ▼                    ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐       ┌──────────────┐
   │Classifier│ │Sentiment │ │ Solution │       │   Action     │
   │  Agent   │ │  Agent   │ │  Agent   │       │   Agent      │
   │ 8 cats   │ │ 0.0–1.0  │ │ KB match │       │ tasks+owners │
   └──────────┘ └──────────┘ └──────────┘       └──────────────┘
          │            │            │                    │
          └────────────┴────────────┴────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────┐          ┌──────────────────┐
          │  Escalation  │          │    Notifier      │
          │    Agent     │          │     Agent        │
          │  P1/P2/P3    │          │  push to dist.   │
          └──────────────┘          └──────────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │     SQLite Database      │
                    │ (7 tables, all persisted)│
                    └─────────────────────────┘
```

---

## 🤖 The 7 AI Agents

### 1. `OrchestratorAgent` — Master Controller
- Coordinates the full 6-agent downstream pipeline
- Logs every agent's action, input, output, and timing to the database
- Handles errors gracefully and marks query status (pending → completed/failed)
- Exposes `process_pending()` for autonomous batch processing

### 2. `ClassifierAgent` — Query Categoriser
- Multi-keyword scoring across **8 business categories**:  
  `pricing` · `onboarding` · `technical` · `support` · `logistics` · `compliance` · `enablement` · `partnership`
- Calculates per-category confidence score
- Returns top category + full score breakdown

### 3. `SentimentAgent` — Emotion Analyser
- Rule-based NLP with **negation handling** and **intensifier weighting**
- Detects `Positive`, `Neutral`, or `Negative` overall sentiment
- Extracts top 3 positive/negative context phrases
- Score range: 0.0 (very negative) → 1.0 (very positive)

### 4. `SolutionAgent` — Knowledge Base Matcher
- Scores all solutions in the KB using keyword overlap + classifier confidence
- Returns top 3 ranked solutions with:
  - Solution description
  - Matched resources
  - Estimated resolution time
  - Confidence score (0–100%)

### 5. `ActionAgent` — Task Generator
- Maps category to a set of 3 specific action templates
- Auto-calculates deadlines based on urgency (days offset from today)
- Assigns owners (e.g., Partner Manager, DevOps Team, Legal Team)
- Sets priority (`Critical` / `High` / `Medium` / `Low`)

### 6. `EscalationAgent` — Priority Judge
- Detects P1 keywords: `urgent`, `critical`, `asap`, `system down`, `emergency`
- Detects P2 keywords: `blocking`, `cannot`, `broken`, `no reply`, `overdue`
- Combines keyword hits with sentiment score for final P1/P2/P3 decision
- Logs escalation reason to database and notifies Support Manager

### 7. `NotifierAgent` — Distributor Relay
- Formats a rich, structured notification message
- Includes: query ID, top solution, next action item, owner, deadline, timestamp
- Logged to `notifications` table — visible in Distributor Portal instantly

---

## ✨ Features

### 🔄 Fully Autonomous Processing
- Submit any query → all 7 agents run instantly → full resolution logged
- 12 sample distributor queries auto-processed on first launch
- `process_pending()` method to drain queue autonomously

### 📊 Enterprise Business Intelligence
- Real-time Plotly charts: query category distribution, sentiment trends, escalation ratios
- Distributor health overview table with resolution % and avg sentiment
- AI-generated business insights with colour-coded alerts

### 🔴 Smart Escalation System
- Three-tier priority: **P1 Critical** → **P2 High** → **P3 Normal**
- Combined keyword + sentiment scoring for accurate escalation
- Auto-assigned to Support Manager with timestamp

### 📢 Distributor Self-Service Portal
- Each distributor gets their own filtered view
- Per-distributor: query history, notifications, action item table
- Sentiment badge on every query so distributors see their own health

### 🧠 Searchable Knowledge Base
- 8 categories, 20+ solutions
- Each solution has: description, keywords, resources, estimated resolution time
- Full-text search across solutions and descriptions

### ⚡ Near Real-Time Performance
- Average pipeline time: **~280–300ms**
- SQLite with thread-safe locking for concurrent access
- Streamlit's `@cache_resource` keeps agents hot-loaded

---

## 📁 Project Structure

```
AI_CALL_ASSISTANT/
│
├── app.py                          # 🖥️  Main Streamlit app — 8 premium dark-mode tabs
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py             # Master agent — runs full pipeline
│   ├── classifier_agent.py         # Keyword-scoring query classifier
│   ├── sentiment_agent.py          # NLP sentiment analyser (negation-aware)
│   ├── solution_agent.py           # KB-matching solution engine
│   ├── action_agent.py             # Action item generator with deadlines
│   ├── escalation_agent.py         # P1/P2/P3 priority evaluator
│   └── notifier_agent.py           # Distributor notification builder
│
├── database/
│   ├── __init__.py
│   └── db_manager.py               # SQLite manager — 7 tables, analytics, CRUD
│
├── knowledge_base/
│   ├── solutions.json              # 8 categories × 20+ solution entries
│   └── sample_queries.json         # 12 realistic test queries
│
├── ai_cl_intelligence/             # Legacy original module
│   ├── app.py
│   ├── customer_data.py
│   ├── distributor_to_vendor.py
│   ├── models.py
│   └── vendor_resources.json
│
├── data/                           # Auto-created — SQLite DB stored here
│   └── ai_call_assistant.db
│
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit (premium dark-mode CSS + Google Fonts Inter) |
| **Charts** | Plotly Express (pie, bar, area, horizontal bar) |
| **Data Processing** | Pandas |
| **Database** | SQLite3 (thread-safe, 7 tables) |
| **Agent Logic** | Pure Python — no external ML API required |
| **Knowledge Base** | JSON-based structured solution library |
| **Backend API** | FastAPI + Uvicorn (legacy module) |
| **Data Validation** | Pydantic (legacy module) |
| **Language** | Python 3.10+ |

> 🔑 **No OpenAI API key required.** All agents run 100% locally using intelligent rule-based NLP and keyword scoring.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Step 1 — Clone the Repository
```bash
git clone https://github.com/VISHVAPRASATHVS/AI-call-Assistant-Distributor-to-vendor-.git
cd AI-call-Assistant-Distributor-to-vendor-
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

**`requirements.txt` contents:**
```
streamlit
fastapi
uvicorn
python-dotenv
pydantic
plotly
pandas
```

### Step 3 — Run the Platform
```bash
streamlit run app.py --server.port 8502
```

### Step 4 — Open in Browser
```
http://localhost:8502
```

> On first launch, **12 sample queries** are automatically processed by all 7 agents. A progress bar will show while they load. This takes about 5–10 seconds.

---

## 💡 How to Use

### Submit a Query Manually
1. Go to **📥 Submit Query** tab
2. Enter the distributor name (e.g., `TechNova Solutions`)
3. Paste the query or call transcript in the text area
4. Click **🚀 Submit to Agent Pipeline**
5. See the full AI output in under 300ms:
   - Category + confidence
   - Sentiment score
   - Escalation priority (P1/P2/P3)
   - Top 3 matched solutions
   - 3 auto-generated action items with owners and deadlines
   - Distributor notification message

### View All Processed Queries
- Go to **📋 Query Logs** tab
- Filter by distributor, category, or status
- Expand any query to see its solutions, actions, and sentiment

### Monitor Escalations
- Go to **🔴 Escalations** tab
- See P1/P2/P3 breakdown with reasons and assigned owners

### Distributor Self-Service
- Go to **📢 Distributor Portal** tab
- Select any distributor from the dropdown
- View their query history, notifications, and action items

---

## 🧠 Knowledge Base

The Knowledge Base (`knowledge_base/solutions.json`) contains **20+ solutions** across **8 categories**:

| Category | Example Solution |
|---|---|
| 💰 **Pricing** | Share Comprehensive Pricing Tier Explainer Document |
| 💰 **Pricing** | Grant Instant Access to Real-Time Partner Pricing Portal |
| 🎓 **Onboarding** | Deliver Complete Digital Sales Rep Onboarding Pack |
| 🎓 **Onboarding** | Register Team for 3-Day Hands-On Product Bootcamp |
| 🔧 **Technical** | Deliver Full Technical Documentation & API Reference Kit |
| 🔧 **Technical** | Provision Dedicated Sandbox/Test Environment |
| 🆘 **Support** | Open Priority-1 Support Ticket with 4-Hour SLA Guarantee |
| 📦 **Logistics** | Expedite Shipment to Priority Fulfillment Queue |
| 📦 **Logistics** | Grant Real-Time Inventory Dashboard Access |
| ⚖️ **Compliance** | Deliver Full Compliance & Certification Documentation Bundle |
| 📣 **Enablement** | Send Complete Partner Enablement Kit (Slides + Videos) |
| 🤝 **Partnership** | Schedule Quarterly Business Review (QBR) with Executive Sponsors |

Each solution entry contains:
```json
{
  "solution": "Deliver Full Technical Documentation & API Reference Kit",
  "description": "Complete tech docs: API specs, Postman collections, integration guides...",
  "keywords": ["documentation", "docs", "api", "spec", "technical"],
  "resources": ["Technical Docs Portal", "API Reference", "Error Code Guide"],
  "estimated_time": "1 hour"
}
```

---

## 🗄️ Database Schema

The platform uses SQLite with **7 production tables**:

```sql
queries          → All incoming distributor queries with status tracking
solutions        → KB-matched solutions per query (with confidence score)
action_items     → Auto-generated tasks with owner, deadline, priority
sentiment_log    → Sentiment scores, positive/negative phrase extraction
escalations      → P1/P2/P3 escalation records with reason + assigned owner
notifications    → Rich distributor notification messages (auto-pushed)
agent_logs       → Full audit trail of every agent action with timing (ms)
```

---

## 📈 Business Impact

| Problem | Before | After |
|---|---|---|
| Query resolution time | Hours (manual) | **~300ms (autonomous)** |
| Human effort per query | 15–30 minutes | **Zero** |
| Solution consistency | Variable | **Standardised from KB** |
| Escalation detection | Manual judgement | **Automated P1/P2/P3** |
| Distributor visibility | Email / phone | **Real-time self-service portal** |
| Analytics | Spreadsheets | **Live Plotly dashboards** |
| Audit trail | None | **Full agent activity log** |

---

## 🌍 Scalability

- **Multi-distributor**: Platform handles any number of distributors simultaneously
- **Knowledge Base extensible**: Add new categories and solutions by editing `solutions.json`
- **No API costs**: Fully offline — no LLM API calls required
- **Database-backed**: All state persisted — restart the app and all data is intact
- **Concurrent-safe**: Thread-locked SQLite operations support parallel requests

---

## 📸 Demo Recording

A full video walkthrough of the platform is available in the repository under the `artifacts/` directory, showing all 8 tabs, autonomous query processing, and the live escalation detection system.

---

## 👨‍💻 Author

**VISHVAPRASATH V S**

- 🌐 GitHub: [@VISHVAPRASATHVS](https://github.com/VISHVAPRASATHVS)
- 📁 Original Project: [AI-call-Assistant-Distributor-to-vendor-](https://github.com/VISHVAPRASATHVS/AI-call-Assistant-Distributor-to-vendor-)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repo if it impressed you!**

*Built with ❤️ for global distributor-vendor intelligence*

</div>
