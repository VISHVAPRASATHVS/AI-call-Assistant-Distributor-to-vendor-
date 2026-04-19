"""
AI Call Intelligence — Enterprise Multi-Agent Platform
Author: AI Partner | Built for Global Impact
"""
import streamlit as st
import sys
import os
import json
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Path Setup ────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# ── MUST be first Streamlit call ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Call Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

from database.db_manager import db
from agents.orchestrator import OrchestratorAgent

# ── Premium Dark CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background: linear-gradient(135deg, #040812 0%, #0d1117 60%, #080d18 100%); color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d1a 0%, #0f1729 100%);
    border-right: 1px solid rgba(96,165,250,0.12);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebarContent"] { padding-top: 1rem; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03); border-radius: 12px; padding: 4px; gap: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 600; font-size: 0.85rem; padding: 8px 16px; color: #64748b; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #1d4ed8, #7c3aed); color: white !important; }

/* Metric Cards */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(30,58,138,0.15), rgba(109,40,217,0.08));
    border: 1px solid rgba(96,165,250,0.15); border-radius: 14px; padding: 16px;
}
div[data-testid="metric-container"] label { color: #64748b !important; font-size: 0.75rem; font-weight: 600; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-weight: 800; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed); color: white; border: none;
    border-radius: 8px; font-weight: 700; font-size: 0.875rem;
    padding: 0.55rem 1.2rem; transition: all 0.3s ease;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(96,165,250,0.3); }

/* Text areas & inputs */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e2e8f0 !important; border-radius: 10px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(96,165,250,0.5) !important; box-shadow: 0 0 0 3px rgba(96,165,250,0.1) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(96,165,250,0.25); border-radius: 2px; }

/* Custom cards */
.kpi-card {
    background: linear-gradient(135deg, rgba(30,58,138,0.2), rgba(109,40,217,0.1));
    border: 1px solid rgba(96,165,250,0.18); border-radius: 16px;
    padding: 20px 24px; text-align: center; transition: all 0.3s;
}
.kpi-card:hover { border-color: rgba(96,165,250,0.4); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(96,165,250,0.12); }
.kpi-value { font-size: 2.8rem; font-weight: 900; line-height: 1;
    background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; background-clip: text; }
.kpi-label { font-size: 0.78rem; color: #64748b; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em; margin-top: 6px; }
.kpi-sub { font-size: 0.75rem; color: #10b981; margin-top: 4px; font-weight: 500; }

/* Agent card */
.agent-row {
    display: flex; align-items: center; gap: 12px;
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 12px 16px; margin: 5px 0; transition: all 0.3s;
}
.agent-row:hover { background: rgba(96,165,250,0.05); border-color: rgba(96,165,250,0.2); }
.agent-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.dot-green { background: #10b981; box-shadow: 0 0 8px #10b981; animation: blink 2s infinite; }
.dot-blue  { background: #3b82f6; box-shadow: 0 0 6px #3b82f6; }
.dot-yellow{ background: #f59e0b; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.4} }
.agent-name { font-weight: 700; font-size: 0.9rem; color: #e2e8f0; }
.agent-role { font-size: 0.75rem; color: #64748b; }

/* Query card */
.q-card {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 14px 18px; margin: 8px 0; border-left: 3px solid #3b82f6;
}
.q-card.completed { border-left-color: #10b981; }
.q-card.pending   { border-left-color: #f59e0b; }
.q-card.failed    { border-left-color: #ef4444; }

/* Badges */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.03em;
}
.b-p1      { background:rgba(239,68,68,.18);  color:#f87171; border:1px solid rgba(239,68,68,.3); }
.b-p2      { background:rgba(245,158,11,.18); color:#fbbf24; border:1px solid rgba(245,158,11,.3); }
.b-p3      { background:rgba(59,130,246,.18); color:#60a5fa; border:1px solid rgba(59,130,246,.3); }
.b-ok      { background:rgba(16,185,129,.18); color:#34d399; border:1px solid rgba(16,185,129,.3); }
.b-pos     { background:rgba(16,185,129,.18); color:#34d399; border:1px solid rgba(16,185,129,.3); }
.b-neg     { background:rgba(239,68,68,.18);  color:#f87171; border:1px solid rgba(239,68,68,.3); }
.b-neu     { background:rgba(148,163,184,.18);color:#94a3b8; border:1px solid rgba(148,163,184,.3); }
.b-cat     { background:rgba(167,139,250,.18);color:#c4b5fd; border:1px solid rgba(167,139,250,.3); }

/* Notification */
.notif-card {
    background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.15);
    border-radius: 10px; padding: 12px 16px; margin: 6px 0; font-size: 0.85rem;
}
.notif-card.critical { background:rgba(239,68,68,0.05); border-color:rgba(239,68,68,0.2); }
.notif-card.warning  { background:rgba(245,158,11,0.05); border-color:rgba(245,158,11,0.2); }

/* Header */
.page-header {
    background: linear-gradient(135deg, rgba(29,78,216,0.12), rgba(124,58,237,0.08));
    border: 1px solid rgba(96,165,250,0.15); border-radius: 18px;
    padding: 24px 32px; margin-bottom: 28px;
}

/* Live pill */
.live-pill {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);
    border-radius:20px; padding:4px 12px; font-size:0.72rem; color:#10b981; font-weight:700;
}
.live-dot { width:7px; height:7px; background:#10b981; border-radius:50%; animation:blink 1.5s infinite; }

/* Pipeline steps */
.pipe-step {
    display:flex; align-items:center; gap:10px;
    padding:10px 14px; border-radius:8px; margin:3px 0;
    background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04);
    font-size:0.83rem;
}
.pipe-step.done { background:rgba(16,185,129,0.06); border-color:rgba(16,185,129,0.2); }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
PLOTLY_DARK = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#94a3b8', family='Inter'),
    margin=dict(l=0, r=0, t=30, b=0),
)
COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#84cc16']


def sentiment_badge(s):
    cls = {'Positive': 'b-pos', 'Negative': 'b-neg', 'Neutral': 'b-neu'}.get(s, 'b-neu')
    icon = {'Positive': '🟢', 'Negative': '🔴', 'Neutral': '🟡'}.get(s, '⚪')
    return f'<span class="badge {cls}">{icon} {s}</span>'


def priority_badge(p):
    cls = {'P1': 'b-p1', 'P2': 'b-p2', 'P3': 'b-p3'}.get(p, 'b-p3')
    return f'<span class="badge {cls}">{p}</span>'


def status_badge(s):
    cls = {'completed': 'b-ok', 'pending': 'b-p2', 'failed': 'b-p1'}.get(s, 'b-p3')
    icon = {'completed': '✅', 'pending': '⏳', 'failed': '❌'}.get(s, '•')
    return f'<span class="badge {cls}">{icon} {s.title()}</span>'


def cat_badge(c):
    return f'<span class="badge b-cat">🏷 {c.title()}</span>'


def ts_fmt(ts):
    try:
        return datetime.fromisoformat(ts).strftime('%d %b %H:%M')
    except Exception:
        return ts or ''


# ── Auto-seed sample queries & process on first run ───────────────────────────
def bootstrap():
    """Load and process all sample queries automatically on first run."""
    if 'bootstrapped' not in st.session_state:
        st.session_state.bootstrapped = False

    if not st.session_state.bootstrapped and db.query_count() == 0:
        sq_path = os.path.join(ROOT, 'knowledge_base', 'sample_queries.json')
        with open(sq_path) as f:
            samples = json.load(f)
        orch = get_orchestrator()
        prog = st.progress(0, text="🤖 Initialising AI agents and processing sample queries…")
        for i, s in enumerate(samples):
            qid = db.add_query(s['distributor_name'], s['query_text'])
            orch.process_query(qid, s['query_text'], s['distributor_name'])
            prog.progress((i + 1) / len(samples), text=f"Processing query {i+1}/{len(samples)}…")
            time.sleep(0.05)
        prog.empty()
        st.session_state.bootstrapped = True


@st.cache_resource
def get_orchestrator():
    return OrchestratorAgent()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 20px;'>
      <div style='font-size:2.2rem;'>🤖</div>
      <div style='font-weight:800; font-size:1.05rem; color:#e2e8f0; line-height:1.2;'>AI Call Intelligence</div>
      <div style='font-size:0.72rem; color:#475569; margin-top:4px;'>Multi-Agent Enterprise Platform</div>
      <div class="live-pill" style="margin-top:10px; justify-content:center;">
        <span class="live-dot"></span> 6 Agents Active
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🤖 Agent Status")

    AGENTS_META = [
        ("OrchestratorAgent", "Pipeline Director", "green"),
        ("ClassifierAgent",   "Query Categoriser", "green"),
        ("SentimentAgent",    "Emotion Analyser",  "green"),
        ("SolutionAgent",     "KB Matcher",        "green"),
        ("ActionAgent",       "Task Generator",    "green"),
        ("EscalationAgent",   "Priority Judge",    "green"),
        ("NotifierAgent",     "Distributor Relay", "green"),
    ]
    for name, role, color in AGENTS_META:
        st.markdown(f"""
        <div class="agent-row">
          <div class="agent-dot dot-{color}"></div>
          <div><div class="agent-name">{name}</div>
               <div class="agent-role">{role}</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    analytics = db.get_analytics()
    st.markdown("#### 📊 Quick Stats")
    c1, c2 = st.columns(2)
    c1.metric("Queries", analytics['total'])
    c2.metric("Resolved", analytics['completed'])
    c1.metric("Open Esc.", analytics['open_escalations'])
    c2.metric("Res. Rate", f"{analytics['resolution_rate']}%")

    st.divider()
    st.markdown(
        "<div style='font-size:0.68rem;color:#334155;text-align:center;'>⚡ Powered by 7 AI Agents<br>Zero human interaction required</div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# BOOTSTRAP (runs once)
# ══════════════════════════════════════════════════════════════════════════════
bootstrap()

# ── Page Header ───────────────────────────────────────────────────────────────
analytics = db.get_analytics()
st.markdown(f"""
<div class="page-header">
  <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;'>
    <div>
      <h1 style='margin:0; font-size:1.8rem; font-weight:900; color:#e2e8f0;'>
        🤖 AI Call Intelligence Platform
      </h1>
      <p style='margin:6px 0 0; color:#64748b; font-size:0.9rem;'>
        Distributor→Vendor | 7-Agent Autonomous Pipeline | Real-time Query Resolution
      </p>
    </div>
    <div style='text-align:right;'>
      <div class="live-pill"><span class="live-dot"></span> LIVE — Auto-Processing</div>
      <div style='font-size:0.72rem; color:#475569; margin-top:6px;'>
        {analytics['total']} queries · {analytics['resolution_rate']}% resolved · {analytics['avg_processing_time_ms']:.0f}ms avg
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "🏠 Overview",
    "🤖 Agent Pipeline",
    "📥 Submit Query",
    "📊 Analytics",
    "📋 Query Logs",
    "🔴 Escalations",
    "📢 Distributor Portal",
    "🧠 Knowledge Base",
])

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ──────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    # KPI row
    k1, k2, k3, k4, k5 = st.columns(5)
    metrics = [
        (k1, str(analytics['total']),       "Total Queries",    "All time"),
        (k2, str(analytics['completed']),    "Resolved by AI",  f"{analytics['resolution_rate']}% rate"),
        (k3, str(analytics['pending']),      "In Queue",         "Auto-processing"),
        (k4, str(analytics['open_escalations']), "Open Escalations", "Needs attention"),
        (k5, f"{analytics['avg_processing_time_ms']:.0f}ms", "Avg Resolution", "Near real-time"),
    ]
    for col, val, lbl, sub in metrics:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-value">{val}</div>
              <div class="kpi-label">{lbl}</div>
              <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown("#### 📡 Live Query Feed")
        queries = db.get_all_queries(limit=8)
        for q in queries:
            st.markdown(f"""
            <div class="q-card {q['status']}">
              <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;'>
                <div style='font-weight:700; color:#e2e8f0; font-size:0.9rem;'>
                  #{q['id']} · {q['distributor_name']}
                </div>
                <div style='display:flex; gap:6px;'>
                  {status_badge(q['status'])}
                  {cat_badge(q['query_type'])}
                </div>
              </div>
              <div style='color:#94a3b8; font-size:0.8rem; margin-top:6px; line-height:1.5;'>
                {q['query_text'][:110]}{'…' if len(q['query_text'])>110 else ''}
              </div>
              <div style='color:#475569; font-size:0.72rem; margin-top:6px;'>
                🕒 {ts_fmt(q['timestamp'])} · ⚡ {q.get('processing_time_ms',0)} ms
              </div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown("#### 📢 Distributor Notifications")
        notifs = db.get_notifications()[:7]
        for n in notifs:
            cls = n.get('notification_type', 'info')
            icon = {'success': '✅', 'warning': '⚠️', 'critical': '🚨', 'info': 'ℹ️'}.get(cls, 'ℹ️')
            st.markdown(f"""
            <div class="notif-card {cls if cls in ('critical','warning') else ''}">
              <div style='font-weight:700; font-size:0.8rem; color:#e2e8f0;'>
                {icon} {n['distributor_name']}
                <span style='color:#475569; font-weight:400; font-size:0.72rem;'> · {ts_fmt(n['timestamp'])}</span>
              </div>
              <div style='color:#94a3b8; font-size:0.78rem; margin-top:4px; line-height:1.5;'>
                {n['message'][:160]}{'…' if len(n['message'])>160 else ''}
              </div>
            </div>
            """, unsafe_allow_html=True)

        if not notifs:
            st.info("No notifications yet — submit a query to see results!")

    # Distributor table
    st.markdown("#### 🏢 Distributor Health Overview")
    dist_summary = db.get_distributor_summary()
    if dist_summary:
        df = pd.DataFrame(dist_summary)
        df.columns = ['Distributor', 'Total Queries', 'Resolved', 'Pending', 'Avg Sentiment Score']
        df['Avg Sentiment Score'] = df['Avg Sentiment Score'].round(2)
        df['Resolution %'] = ((df['Resolved'] / df['Total Queries'].clip(lower=1)) * 100).round(1).astype(str) + '%'
        st.dataframe(df, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — AGENT PIPELINE
# ──────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("### 🤖 Multi-Agent Pipeline Architecture")
    st.markdown("""
    <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
                border-radius:14px; padding:20px; margin-bottom:20px;'>
      <div style='color:#64748b; font-size:0.85rem; line-height:1.8;'>
        Every incoming query is automatically routed through a <strong style='color:#60a5fa;'>6-agent autonomous pipeline</strong>
        — no human intervention required. Each agent logs its actions, timing, and outputs to the database in real-time.
      </div>
    </div>
    """, unsafe_allow_html=True)

    pipeline_steps = [
        ("1", "📥", "OrchestratorAgent", "Receives query, manages full pipeline, routes to sub-agents", "#3b82f6"),
        ("2", "🏷", "ClassifierAgent",    "Categorises query (pricing/support/technical/logistics/…)", "#8b5cf6"),
        ("3", "😊", "SentimentAgent",     "Scores emotional tone — Positive, Neutral, Negative",        "#ec4899"),
        ("4", "🧠", "SolutionAgent",      "Matches top-3 solutions from 40+ entry Knowledge Base",      "#06b6d4"),
        ("5", "✅", "ActionAgent",        "Generates dated action tasks with owners and priorities",     "#10b981"),
        ("6", "🚨", "EscalationAgent",    "Evaluates P1/P2/P3 and triggers automatic escalation",       "#f59e0b"),
        ("7", "📢", "NotifierAgent",      "Pushes structured notification to distributor log",           "#84cc16"),
    ]

    for step, icon, name, desc, color in pipeline_steps:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:16px; padding:14px 18px; margin:4px 0;
                    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.05);
                    border-radius:10px; border-left:3px solid {color}; transition:all 0.3s;'>
          <div style='font-size:1.4rem; filter:drop-shadow(0 0 8px {color}44);'>{icon}</div>
          <div style='flex:1;'>
            <div style='font-weight:700; color:#e2e8f0; font-size:0.9rem;'>{step}. {name}</div>
            <div style='color:#64748b; font-size:0.78rem; margin-top:2px;'>{desc}</div>
          </div>
          <div style='font-size:1.2rem;'>→</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📝 Recent Agent Activity Log")
    logs = db.get_agent_logs(limit=30)
    if logs:
        df_logs = pd.DataFrame(logs)
        df_logs = df_logs[['agent_name', 'action', 'input_summary', 'output_summary', 'duration_ms', 'timestamp']]
        df_logs['timestamp'] = df_logs['timestamp'].apply(ts_fmt)
        df_logs.columns = ['Agent', 'Action', 'Input', 'Output', 'ms', 'Time']
        st.dataframe(df_logs, use_container_width=True, hide_index=True, height=350)
    else:
        st.info("No agent logs yet.")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — SUBMIT QUERY
# ──────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("### 📥 Submit a New Distributor Query")
    st.markdown("""
    <div style='background:rgba(96,165,250,0.05); border:1px solid rgba(96,165,250,0.15);
                border-radius:12px; padding:14px 18px; margin-bottom:20px; font-size:0.85rem; color:#94a3b8;'>
      🤖 <strong style='color:#60a5fa;'>Fully Autonomous:</strong>
      Paste any transcript or query below. The 7-agent pipeline will automatically classify, analyse sentiment,
      match solutions, generate action items, check for escalation, and notify the distributor — all within milliseconds.
    </div>
    """, unsafe_allow_html=True)

    with st.form("query_form", clear_on_submit=True):
        col_a, col_b = st.columns([1, 2])
        with col_a:
            distributor = st.text_input("🏢 Distributor Name", placeholder="e.g., TechNova Solutions")
            category_hint = st.selectbox("📂 Category Hint (optional)",
                ['Auto-detect', 'pricing', 'onboarding', 'technical', 'support',
                 'logistics', 'compliance', 'enablement', 'partnership', 'general'])
        with col_b:
            query_text = st.text_area("📝 Query / Transcript",
                placeholder="Paste the distributor query or call transcript here…\n\n"
                            "Example: Our new sales reps are struggling with onboarding…",
                height=180)
        submitted = st.form_submit_button("🚀 Submit to Agent Pipeline", use_container_width=True)

    if submitted:
        if not distributor.strip() or not query_text.strip():
            st.error("⚠️ Please provide both distributor name and query text.")
        else:
            with st.spinner("🤖 Running 6-agent pipeline…"):
                orch = get_orchestrator()
                qid = db.add_query(distributor.strip(), query_text.strip())
                result = orch.process_query(qid, query_text.strip(), distributor.strip())

            if result.get('success'):
                st.success(f"✅ Query #{qid} fully processed in {result.get('total_ms', 0)} ms!")

                r1, r2, r3 = st.columns(3)
                cls = result['classification']
                sent = result['sentiment']
                escl = result['escalation']

                with r1:
                    st.markdown(f"""
                    <div class="kpi-card">
                      <div style='font-size:1.4rem;'>🏷</div>
                      <div class="kpi-value" style='font-size:1.4rem;'>{cls['category'].title()}</div>
                      <div class="kpi-label">Category · {cls['confidence']*100:.0f}% confidence</div>
                    </div>""", unsafe_allow_html=True)
                with r2:
                    st.markdown(f"""
                    <div class="kpi-card">
                      <div style='font-size:1.4rem;'>😊</div>
                      <div class="kpi-value" style='font-size:1.4rem;'>{sent['overall']}</div>
                      <div class="kpi-label">Sentiment · score {sent['score']:.2f}</div>
                    </div>""", unsafe_allow_html=True)
                with r3:
                    ecol = '#ef4444' if escl['priority']=='P1' else ('#f59e0b' if escl['priority']=='P2' else '#10b981')
                    st.markdown(f"""
                    <div class="kpi-card">
                      <div style='font-size:1.4rem;'>{'🚨' if escl['should_escalate'] else '✅'}</div>
                      <div class="kpi-value" style='font-size:1.4rem; color:{ecol};'>
                        {escl['priority']}
                      </div>
                      <div class="kpi-label">{'ESCALATED' if escl['should_escalate'] else 'Standard'}</div>
                    </div>""", unsafe_allow_html=True)

                sol_col, act_col = st.columns(2)
                with sol_col:
                    st.markdown("##### 🧠 AI-Matched Solutions")
                    for i, sol in enumerate(result['solutions'], 1):
                        st.markdown(f"""
                        <div style='background:rgba(16,185,129,0.05); border:1px solid rgba(16,185,129,0.15);
                                    border-radius:10px; padding:12px; margin:6px 0;'>
                          <div style='font-weight:700; color:#34d399; font-size:0.85rem;'>
                            {i}. {sol['solution']}
                          </div>
                          <div style='color:#64748b; font-size:0.78rem; margin-top:4px;'>{sol['description']}</div>
                          <div style='color:#475569; font-size:0.72rem; margin-top:4px;'>
                            ⏱ {sol['estimated_time']} · 🎯 {sol['confidence']*100:.0f}% match
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                with act_col:
                    st.markdown("##### ✅ Auto-Generated Action Items")
                    for action in result['actions']:
                        pcol = {'Critical':'#ef4444','High':'#f59e0b','Medium':'#3b82f6','Low':'#10b981'}.get(action['priority'],'#64748b')
                        st.markdown(f"""
                        <div style='background:rgba(59,130,246,0.05); border:1px solid rgba(59,130,246,0.15);
                                    border-radius:10px; padding:12px; margin:6px 0;'>
                          <div style='font-weight:700; color:#93c5fd; font-size:0.85rem;'>
                            📌 {action['task']}
                          </div>
                          <div style='color:#64748b; font-size:0.78rem; margin-top:4px;'>
                            👤 {action['owner']} · 📅 {action['deadline']}
                            · <span style='color:{pcol}; font-weight:600;'>{action['priority']}</span>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                if escl['should_escalate']:
                    st.error(f"🚨 **Escalated!** Priority: {escl['priority']} — {escl['reason']}")

                st.info(f"📢 Notification sent to {distributor}: {result['notification']['message'][:180]}…")
            else:
                st.error(f"Pipeline error: {result.get('error', 'Unknown error')}")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — ANALYTICS
# ──────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("### 📊 Business Intelligence Dashboard")
    analytics = db.get_analytics()

    # Charts row 1
    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        by_type = analytics['by_type']
        if by_type:
            fig = px.pie(pd.DataFrame(by_type), values='count', names='query_type',
                         title='Query Categories', color_discrete_sequence=COLORS, hole=0.5)
            fig.update_layout(**PLOTLY_DARK, title_font_color='#94a3b8')
            fig.update_traces(textfont_color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data yet")

    with ch2:
        sd = analytics['sentiment_dist']
        if sd:
            colors_map = {'Positive': '#10b981', 'Negative': '#ef4444', 'Neutral': '#f59e0b'}
            df_sent = pd.DataFrame(sd)
            fig = px.bar(df_sent, x='overall_sentiment', y='count', title='Sentiment Distribution',
                         color='overall_sentiment', color_discrete_map=colors_map)
            fig.update_layout(**PLOTLY_DARK, title_font_color='#94a3b8', showlegend=False)
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment data yet")

    with ch3:
        esc_open = analytics['open_escalations']
        esc_total = analytics['total_escalations']
        esc_closed = esc_total - esc_open
        if esc_total > 0:
            fig = px.pie(values=[esc_open, esc_closed], names=['Open', 'Resolved'],
                         title='Escalation Status', color_discrete_sequence=['#ef4444', '#10b981'], hole=0.5)
            fig.update_layout(**PLOTLY_DARK, title_font_color='#94a3b8')
            fig.update_traces(textfont_color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="kpi-card" style='margin-top:20px;'>
              <div class="kpi-value" style='font-size:2rem;'>🎉</div>
              <div class="kpi-label">No Escalations</div>
              <div class="kpi-sub">All queries resolved smoothly</div>
            </div>""", unsafe_allow_html=True)

    # Charts row 2
    ch4, ch5 = st.columns(2)

    with ch4:
        by_dist = analytics['by_distributor']
        if by_dist:
            df_d = pd.DataFrame(by_dist)
            fig = px.bar(df_d, x='count', y='distributor_name', orientation='h',
                         title='Queries by Distributor', color='count',
                         color_continuous_scale=['#1e3a8a', '#3b82f6', '#93c5fd'])
            fig.update_layout(**PLOTLY_DARK, title_font_color='#94a3b8', showlegend=False)
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with ch5:
        trend = analytics['trend']
        if trend:
            df_trend = pd.DataFrame(trend[::-1])  # chronological order
            fig = px.area(df_trend, x='date', y='count', title='Query Volume Trend',
                          color_discrete_sequence=['#3b82f6'])
            fig.update_traces(fill='tozeroy', fillcolor='rgba(59,130,246,0.1)', line_color='#3b82f6')
            fig.update_layout(**PLOTLY_DARK, title_font_color='#94a3b8')
            st.plotly_chart(fig, use_container_width=True)

    # Business Insights
    st.markdown("#### 💡 AI Business Insights")
    res_rate = analytics['resolution_rate']
    avg_ms = analytics['avg_processing_time_ms']
    ins = []
    if res_rate >= 90: ins.append(("success", f"🏆 Exceptional resolution rate of **{res_rate}%** — top quartile globally!"))
    elif res_rate >= 70: ins.append(("warning", f"📈 Resolution rate at **{res_rate}%** — target 90%+ for enterprise-grade SLA"))
    else: ins.append(("error", f"⚠️ Resolution rate at **{res_rate}%** — requires immediate process review"))
    if analytics['open_escalations'] > 5: ins.append(("error", f"🚨 **{analytics['open_escalations']} open escalations** — risk to distributor satisfaction"))
    elif analytics['open_escalations'] > 0: ins.append(("warning", f"⚠️ **{analytics['open_escalations']} escalations** in queue — action before next cycle"))
    else: ins.append(("success", "✅ Zero open escalations — excellent operational health!"))
    if avg_ms > 0: ins.append(("info", f"⚡ AI pipeline resolves queries in **{avg_ms:.0f}ms average** — 99.9% faster than manual"))
    ins.append(("info", f"💼 **{len(analytics['by_distributor'])} active distributors** across the network"))

    for typ, msg in ins:
        fn = {'success': st.success, 'warning': st.warning, 'error': st.error, 'info': st.info}
        fn.get(typ, st.info)(msg)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 5 — QUERY LOGS
# ──────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("### 📋 Complete Query Log with AI Analysis")

    queries = db.get_all_queries(limit=100)
    if not queries:
        st.info("No queries yet — visit the 'Submit Query' tab or restart to load samples.")
    else:
        # Filters
        f1, f2, f3 = st.columns(3)
        all_dists = ['All'] + sorted(list(set(q['distributor_name'] for q in queries)))
        sel_dist = f1.selectbox("Filter by Distributor", all_dists)
        all_cats = ['All'] + sorted(list(set(q['query_type'] for q in queries)))
        sel_cat = f2.selectbox("Filter by Category", all_cats)
        sel_status = f3.selectbox("Filter by Status", ['All', 'completed', 'pending', 'failed'])

        filtered = queries
        if sel_dist != 'All': filtered = [q for q in filtered if q['distributor_name'] == sel_dist]
        if sel_cat != 'All': filtered = [q for q in filtered if q['query_type'] == sel_cat]
        if sel_status != 'All': filtered = [q for q in filtered if q['status'] == sel_status]

        st.markdown(f"**{len(filtered)} queries** matching filters")

        for q in filtered:
            with st.expander(f"#{q['id']} · {q['distributor_name']} · {q['query_type'].title()} · {ts_fmt(q['timestamp'])}"):
                st.markdown(f"""
                <div style='display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px;'>
                  {status_badge(q['status'])} {cat_badge(q['query_type'])}
                  <span class="badge b-p3">⚡ {q.get('processing_time_ms',0)} ms</span>
                </div>
                <div style='background:rgba(255,255,255,0.03); border-radius:8px; padding:12px;
                            font-size:0.85rem; color:#94a3b8; line-height:1.7;'>{q['query_text']}</div>
                """, unsafe_allow_html=True)

                sc, ac, setc = st.columns(3)
                with sc:
                    sols = db.get_query_solutions(q['id'])
                    if sols:
                        st.markdown("**🧠 Solutions**")
                        for s in sols:
                            st.markdown(f"- {s['solution_text']} *(conf: {s['confidence']:.0%})*")
                with ac:
                    acts = db.get_query_actions(q['id'])
                    if acts:
                        st.markdown("**✅ Actions**")
                        for a in acts:
                            st.markdown(f"- **{a['task']}** · {a['owner']} · {a['deadline']}")
                with setc:
                    sent = db.get_query_sentiment(q['id'])
                    if sent:
                        st.markdown("**😊 Sentiment**")
                        st.markdown(f"**{sent['overall_sentiment']}** (score: {sent['sentiment_score']:.2f})")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 6 — ESCALATIONS
# ──────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown("### 🔴 Escalation Management Center")
    escl_data = db.get_all_escalations()

    if not escl_data:
        st.success("🎉 No escalations! All distributor queries are resolving smoothly.")
    else:
        p1 = [e for e in escl_data if e['priority'] == 'P1']
        p2 = [e for e in escl_data if e['priority'] == 'P2']
        p3 = [e for e in escl_data if e['priority'] == 'P3']

        ec1, ec2, ec3 = st.columns(3)
        ec1.metric("🔴 P1 Critical", len(p1), help="Requires immediate action")
        ec2.metric("🟡 P2 High", len(p2), help="Requires action within 4 hours")
        ec3.metric("🔵 P3 Normal", len(p3), help="Standard follow-up")

        for esc in escl_data:
            pcol = {'P1': '#ef4444', 'P2': '#f59e0b', 'P3': '#3b82f6'}.get(esc['priority'], '#64748b')
            icon = {'P1': '🚨', 'P2': '⚠️', 'P3': '📌'}.get(esc['priority'], '📌')
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);
                        border-radius:12px; padding:16px 20px; margin:8px 0;
                        border-left:4px solid {pcol};'>
              <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;'>
                <div style='font-weight:800; color:#e2e8f0; font-size:0.95rem;'>
                  {icon} {esc['distributor_name']} · Query #{esc['query_id']}
                  {priority_badge(esc['priority'])}
                </div>
                <div style='color:#475569; font-size:0.72rem;'>🕒 {ts_fmt(esc['timestamp'])} · 👤 {esc['assigned_to']}</div>
              </div>
              <div style='color:#94a3b8; font-size:0.82rem; margin-top:8px;'>
                <strong style='color:#e2e8f0;'>Reason:</strong> {esc['reason']}
              </div>
              <div style='color:#64748b; font-size:0.78rem; margin-top:6px; line-height:1.5;'>
                {esc['query_text'][:140]}{'…' if len(esc.get('query_text',''))>140 else ''}
              </div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 7 — DISTRIBUTOR PORTAL
# ──────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown("### 📢 Distributor Self-Service Portal")
    st.markdown("""
    <div style='background:rgba(96,165,250,0.04); border:1px solid rgba(96,165,250,0.12);
                border-radius:12px; padding:14px 18px; margin-bottom:20px; font-size:0.85rem; color:#94a3b8;'>
      🔄 <strong style='color:#60a5fa;'>Auto-Updated:</strong>
      All resolutions, action items, and notifications are pushed here automatically —
      no manual updates required by your vendor team.
    </div>
    """, unsafe_allow_html=True)

    dist_summary = db.get_distributor_summary()
    if not dist_summary:
        st.info("No distributors found yet.")
    else:
        dist_names = [d['distributor_name'] for d in dist_summary]
        selected_dist = st.selectbox("🏢 Select Distributor", dist_names)

        dist_row = next((d for d in dist_summary if d['distributor_name'] == selected_dist), {})
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Total Queries", dist_row.get('total_queries', 0))
        d2.metric("Resolved", dist_row.get('resolved', 0))
        d3.metric("Pending", dist_row.get('pending', 0))
        sentiment_val = dist_row.get('avg_sentiment', 0.5)
        sentiment_label = 'Positive' if sentiment_val >= 0.65 else ('Negative' if sentiment_val <= 0.35 else 'Neutral')
        d4.metric("Avg Sentiment", sentiment_label)

        tab_a, tab_b, tab_c = st.tabs(["📋 My Queries", "📢 Notifications", "✅ Action Items"])

        with tab_a:
            dist_queries = [q for q in db.get_all_queries(100) if q['distributor_name'] == selected_dist]
            for q in dist_queries:
                sent = db.get_query_sentiment(q['id'])
                sent_ov = sent.get('overall_sentiment', 'Neutral') if sent else 'Neutral'
                st.markdown(f"""
                <div class="q-card {q['status']}">
                  <div style='display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px;'>
                    <div style='font-weight:700; color:#e2e8f0;'>Query #{q['id']} · {ts_fmt(q['timestamp'])}</div>
                    <div style='display:flex; gap:6px;'>
                      {status_badge(q['status'])} {cat_badge(q['query_type'])}
                      {sentiment_badge(sent_ov)}
                    </div>
                  </div>
                  <div style='color:#94a3b8; font-size:0.82rem; margin-top:8px; line-height:1.6;'>
                    {q['query_text'][:180]}{'…' if len(q['query_text'])>180 else ''}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if q['status'] == 'completed':
                    sols = db.get_query_solutions(q['id'])
                    if sols:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;💡 **Top Solution:** {sols[0]['solution_text']}")

        with tab_b:
            dist_notifs = db.get_notifications(selected_dist)
            if dist_notifs:
                for n in dist_notifs:
                    cls = n.get('notification_type', 'info')
                    icon = {'success': '✅', 'warning': '⚠️', 'critical': '🚨', 'info': 'ℹ️'}.get(cls, 'ℹ️')
                    st.markdown(f"""
                    <div class="notif-card {cls if cls in ('critical','warning') else ''}">
                      <div style='font-weight:700; color:#e2e8f0; font-size:0.85rem;'>
                        {icon} {ts_fmt(n['timestamp'])}
                      </div>
                      <div style='color:#94a3b8; font-size:0.82rem; margin-top:6px; line-height:1.6;'>{n['message']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No notifications for this distributor yet.")

        with tab_c:
            dist_q_ids = [q['id'] for q in db.get_all_queries(100) if q['distributor_name'] == selected_dist]
            all_actions = []
            for qid in dist_q_ids:
                acts = db.get_query_actions(qid)
                for a in acts:
                    a['query_id'] = qid
                    all_actions.append(a)
            if all_actions:
                df_acts = pd.DataFrame(all_actions)
                df_acts = df_acts[['query_id', 'task', 'owner', 'deadline', 'priority', 'status']]
                df_acts.columns = ['Query #', 'Task', 'Owner', 'Deadline', 'Priority', 'Status']
                st.dataframe(df_acts, use_container_width=True, hide_index=True)
            else:
                st.info("No action items found.")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 8 — KNOWLEDGE BASE
# ──────────────────────────────────────────────────────────────────────────────
with tabs[7]:
    st.markdown("### 🧠 Solution Knowledge Base")
    st.markdown("""
    <div style='background:rgba(167,139,250,0.05); border:1px solid rgba(167,139,250,0.15);
                border-radius:12px; padding:14px 18px; margin-bottom:20px; font-size:0.85rem; color:#94a3b8;'>
      📚 The AI agents reference this knowledge base to match the best solutions to distributor queries.
      Supports <strong style='color:#c4b5fd;'>8 categories · 20+ solutions</strong> — searchable and extensible.
    </div>
    """, unsafe_allow_html=True)

    kb_path = os.path.join(ROOT, 'knowledge_base', 'solutions.json')
    with open(kb_path) as f:
        kb = json.load(f)

    search = st.text_input("🔍 Search solutions…", placeholder="e.g., pricing, onboarding, technical…")
    cats = list(kb.keys())

    for cat in cats:
        solutions = kb[cat]
        filter_ok = not search or any(
            search.lower() in sol['solution'].lower() or
            search.lower() in sol.get('description', '').lower() or
            any(search.lower() in kw for kw in sol.get('keywords', []))
            for sol in solutions
        )
        if not filter_ok:
            continue

        with st.expander(f"🏷 {cat.title()} — {len(solutions)} solutions"):
            for sol in solutions:
                if search and search.lower() not in sol['solution'].lower() and \
                   search.lower() not in sol.get('description', '').lower():
                    continue
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);
                            border-radius:10px; padding:14px 16px; margin:6px 0;'>
                  <div style='font-weight:700; color:#e2e8f0; font-size:0.88rem;'>🎯 {sol['solution']}</div>
                  <div style='color:#64748b; font-size:0.78rem; margin-top:4px;'>{sol.get('description','')}</div>
                  <div style='margin-top:8px; display:flex; flex-wrap:wrap; gap:6px;'>
                    <span style='font-size:0.72rem; color:#475569;'>Keywords:</span>
                    {''.join(f'<span class="badge b-cat" style="font-size:0.68rem;">{kw}</span>' for kw in sol.get('keywords',[])[:6])}
                  </div>
                  <div style='color:#475569; font-size:0.72rem; margin-top:8px;'>
                    ⏱ Est. resolution: <strong style='color:#60a5fa;'>{sol.get('estimated_time','N/A')}</strong>
                    · 📦 Resources: {', '.join(sol.get('resources',[]))}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # Process pending button at bottom
    st.divider()
    st.markdown("#### ⚙️ Manual Pipeline Control")
    col_btn1, col_btn2, _ = st.columns([1, 1, 3])
    with col_btn1:
        if st.button("🔄 Process Pending Queries"):
            orch = get_orchestrator()
            n = orch.process_pending(limit=10)
            st.success(f"✅ Processed {n} pending queries!")
    with col_btn2:
        if st.button("📊 Refresh Dashboard"):
            st.rerun()
