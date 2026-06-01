import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&family=Outfit:wght@200;300;400&display=swap');
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0a0a !important;
    color: #f0f0f0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(220,38,38,0.12) 0%, transparent 60%),
        #0a0a0a !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 2rem 4rem 4rem !important; max-width: 1100px !important; margin: 0 auto; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 4rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    color: #dc2626;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 8vw, 7rem);
    line-height: 0.95;
    letter-spacing: 0.02em;
    color: #ffffff;
    margin-bottom: 0.4rem;
}
.hero-title span { color: #dc2626; }
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 1rem;
    color: #6b6b6b;
    letter-spacing: 0.02em;
    margin-top: 1rem;
}
.hero-divider {
    width: 48px;
    height: 2px;
    background: #dc2626;
    margin: 2rem auto 0;
}

/* ── Input section ── */
.input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #dc2626;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: block;
}

[data-testid="stTextInput"] input {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
    color: #f0f0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #dc2626 !important;
    box-shadow: 0 0 0 1px rgba(220,38,38,0.3) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3a3a3a !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    background: #dc2626 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2.5rem !important;
    cursor: pointer !important;
    transition: background 0.2s ease, transform 0.1s ease !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    background: #b91c1c !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Pipeline status cards ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #1a1a1a;
    border: 1px solid #1a1a1a;
    margin: 2.5rem 0;
}
.pipeline-card {
    background: #0d0d0d;
    padding: 1.2rem 1rem;
    text-align: center;
    position: relative;
    transition: background 0.3s ease;
}
.pipeline-card.active { background: #110000; }
.pipeline-card.done { background: #0d0d0d; }
.pipeline-card-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    display: block;
    opacity: 0.5;
    transition: opacity 0.3s ease;
}
.pipeline-card.active .pipeline-card-icon,
.pipeline-card.done .pipeline-card-icon { opacity: 1; }
.pipeline-card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3a3a3a;
    transition: color 0.3s ease;
}
.pipeline-card.active .pipeline-card-label { color: #dc2626; }
.pipeline-card.done .pipeline-card-label { color: #6b6b6b; }
.pipeline-card-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    margin-top: 0.3rem;
    color: #2a2a2a;
    transition: color 0.3s ease;
}
.pipeline-card.active .pipeline-card-status { color: #dc2626; }
.pipeline-card.done .pipeline-card-status { color: #3d3d3d; }
.pipeline-card.done::after {
    content: '✓';
    position: absolute;
    top: 8px; right: 10px;
    font-size: 0.65rem;
    color: #dc2626;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin: 2.5rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1a1a1a;
}
.section-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #dc2626;
    text-transform: uppercase;
    background: rgba(220,38,38,0.08);
    padding: 0.2rem 0.5rem;
    border: 1px solid rgba(220,38,38,0.2);
}
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.05em;
    color: #ffffff;
}

/* ── Content boxes ── */
.content-box {
    background: #0d0d0d;
    border: 1px solid #1e1e1e;
    border-left: 2px solid #dc2626;
    padding: 1.5rem 1.8rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 0.92rem;
    line-height: 1.75;
    color: #c0c0c0;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Score badge ── */
.score-badge {
    display: inline-block;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #dc2626;
    background: rgba(220,38,38,0.06);
    border: 1px solid rgba(220,38,38,0.25);
    padding: 0.2rem 1.2rem;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: #1a1a1a !important;
    border-radius: 0 !important;
}
[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #dc2626, #ef4444) !important;
    border-radius: 0 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #dc2626 !important; }

/* ── Error ── */
.err-box {
    background: rgba(220,38,38,0.06);
    border: 1px solid rgba(220,38,38,0.3);
    border-left: 3px solid #dc2626;
    padding: 1rem 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #f87171;
    margin-top: 1rem;
}

/* ── Footer ── */
.page-footer {
    text-align: center;
    margin-top: 5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #141414;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: #2a2a2a;
    text-transform: uppercase;
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.5s ease forwards; }

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.pulse { animation: pulse-dot 1.2s ease infinite; }
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero fade-up">
    <div class="hero-eyebrow">⬡ Multi-Agent Research AI System</div>
    <div class="hero-title">Agentic Research <span>Engine</span></div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<p style="font-family:\'Outfit\',sans-serif; font-size:0.85rem; letter-spacing:0.08em; color:#ffffff; text-align:center; font-weight:300; margin-bottom:1.2rem;">Hi! Whats in your mind today? Tell me what topic you want to research.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input("topic", placeholder="e.g. What is Retrieval-Augmented Generation?", label_visibility="collapsed")
with col2:
    run = st.button("Run")


# ── Pipeline stages helper ────────────────────────────────────────────────────
def render_pipeline(active: int):
    """active: 0=none, 1=search, 2=reader, 3=writer, 4=critic, 5=done"""
    stages = [
        ("🔍", "Search", "Tavily"),
        ("📄", "Reader", "Scraper"),
        ("✍️", "Writer", "LLM"),
        ("🎯", "Critic", "Evaluator"),
    ]
    cards = ""
    for i, (icon, label, sub) in enumerate(stages, start=1):
        cls = "active" if i == active else ("done" if i < active else "")
        status = "<span class='pulse'>running...</span>" if i == active else ("complete" if i < active else "waiting")
        cards += f"""
        <div class="pipeline-card {cls}">
            <span class="pipeline-card-icon">{icon}</span>
            <div class="pipeline-card-label">{label}</div>
            <div class="pipeline-card-status">{status}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-grid">{cards}</div>', unsafe_allow_html=True)


# ── Run ───────────────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.markdown('<div class="err-box">⚠ Please enter a research topic.</div>', unsafe_allow_html=True)
    else:
        progress_bar = st.progress(0)

        # Stage 1 — Search
        render_pipeline(1)
        progress_bar.progress(10)
        status_ph = st.empty()
        status_ph.markdown('<div class="err-box" style="border-color:#333;color:#666;background:#0d0d0d">Searching the web for reliable sources...</div>', unsafe_allow_html=True)

        try:
            from agents import build_search_agent
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            search_content = search_result['messages'][-1].content
            progress_bar.progress(30)
            status_ph.empty()

            # Stage 2 — Reader
            render_pipeline(2)
            status_ph.markdown('<div class="err-box" style="border-color:#333;color:#666;background:#0d0d0d">Scraping the most relevant page...</div>', unsafe_allow_html=True)

            from agents import build_reader_agent
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [(
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape the information.\n\n"
                    f"Search Results:\n{str(search_content)[:800]}"
                )]
            })
            scraped_content = reader_result['messages'][-1].content
            progress_bar.progress(55)
            status_ph.empty()

            # Stage 3 — Writer
            render_pipeline(3)
            status_ph.markdown('<div class="err-box" style="border-color:#333;color:#666;background:#0d0d0d">Drafting research report...</div>', unsafe_allow_html=True)

            from agents import writer_chain
            research_combined = (
                f"Search Results:\n{search_content}\n\n"
                f"Detailed Scraped Content:\n{scraped_content}\n\n"
            )
            report = writer_chain.invoke({"topic": topic, "research": research_combined})
            progress_bar.progress(80)
            status_ph.empty()

            # Stage 4 — Critic
            render_pipeline(4)
            status_ph.markdown('<div class="err-box" style="border-color:#333;color:#666;background:#0d0d0d">Evaluating report quality...</div>', unsafe_allow_html=True)

            from agents import critic_chain
            feedback = critic_chain.invoke({"report": report})
            progress_bar.progress(100)
            status_ph.empty()

            # Done
            render_pipeline(5)

            # ── Results ──────────────────────────────────────────────────────
            st.markdown("""
            <div class="section-header fade-up">
                <span class="section-tag">02</span>
                <span class="section-title">Research Report</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="content-box fade-up">{report}</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="section-header fade-up">
                <span class="section-tag">03</span>
                <span class="section-title">Critic Review</span>
            </div>
            """, unsafe_allow_html=True)

            # Extract score if present
            score_line = ""
            for line in feedback.split('\n'):
                if line.strip().lower().startswith("score"):
                    score_val = line.split(":")[-1].strip()
                    score_line = f'<div class="score-badge">{score_val}</div>'
                    break

            st.markdown(f'{score_line}<div class="content-box fade-up">{feedback}</div>', unsafe_allow_html=True)

        except Exception as e:
            render_pipeline(0)
            st.markdown(f'<div class="err-box">❌ Pipeline error: {e}</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
    ResearchMind · Powered by LangChain + Gemini · Multi-Agent Pipeline
</div>
""", unsafe_allow_html=True)