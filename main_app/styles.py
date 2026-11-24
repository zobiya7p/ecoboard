"""Custom CSS for EcoBoard (matches the Visualboard-style reference).

Cards are Streamlit containers with keys starting with `card_`, e.g.
    with st.container(key="card_scores"): ...
Streamlit adds a `st-key-card_scores` class to them, which the
`[class*="st-key-card"]` rule below styles as a white rounded card.
"""
import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root{
  --eb-forest:#113825; --eb-leaf:#73B843; --eb-emerald:#387642; --eb-amber:#F5A623;
  --eb-bg:#F4F6F5; --eb-sage:#EBF5EE; --eb-border:#EAEFEA; --eb-muted:#6B7A71; --eb-ink:#14261C;
}

/* ---------- Typography ---------- */
.stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp button, .stApp input, .stApp textarea, .stApp a,
[data-baseweb="select"] div, [data-testid="stSidebarNavLink"] span {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
}
[data-testid="stIconMaterial"], .material-symbols-rounded {
  font-family: "Material Symbols Rounded" !important;
}
.stApp { background: var(--eb-bg); color: var(--eb-ink); }
[data-testid="stHeader"] { background: transparent; }
.stHtml-empty { display: none; }
.block-container { padding-top: 2rem; max-width: 1400px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid var(--eb-border); }
[data-testid="stSidebarNavLink"] {
  border-radius: 12px; padding: .55rem .8rem; font-weight: 600; color: #4B5B52;
}
[data-testid="stSidebarNavLink"]:hover { background: #F4F8F5; }
[data-testid="stSidebarNavLink"][aria-current="page"] { background: var(--eb-sage); color: var(--eb-forest); }
.eb-side-card {
  margin-top: 1.5rem; padding: 1rem; border-radius: 14px;
  background: linear-gradient(180deg, #EBF5EE 0%, #F7FBF8 100%); border: 1px solid #DDEBE0;
  font-size: .82rem; line-height: 1.45; color: #3C5245;
}
.eb-side-card b { color: var(--eb-forest); font-size: .9rem; }
.eb-side-brand { font-weight: 800; font-size: 1.35rem; color: var(--eb-forest); letter-spacing: -.02em; }
.eb-side-brand span { color: var(--eb-leaf); }

/* ---------- White cards (any container whose key starts with "card") ---------- */
[class*="st-key-card"] {
  background: #FFFFFF; border: 1px solid var(--eb-border); border-radius: 16px;
  box-shadow: 0 2px 10px rgba(17, 56, 37, .06); padding: 1.25rem 1.4rem;
}
.eb-card-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:.9rem; }
.eb-card-title { font-weight: 700; font-size: 1.05rem; color: var(--eb-forest); }
.eb-tag {
  background: var(--eb-sage); color: var(--eb-emerald); font-size: .7rem; font-weight: 700;
  padding: .22rem .65rem; border-radius: 999px; letter-spacing: .02em;
}
.eb-sub { color: var(--eb-muted); font-size: .82rem; margin-top: -.5rem; margin-bottom: .8rem; }

/* ---------- Form page ---------- */
.eb-form-head h2 { margin: .6rem 0 .25rem; font-size: 1.6rem; font-weight: 800; color: var(--eb-forest); letter-spacing: -.02em; }
.eb-form-head p { color: var(--eb-muted); margin: 0 0 1rem; font-size: .92rem; }
[data-testid="stForm"] { border: 0; padding: 0; background: transparent; }
.stTextInput input, [data-baseweb="select"] > div {
  border-radius: 12px !important; border-color: #E1E9E2 !important; background: #FAFCFA !important;
}
.stTextInput input:focus { border-color: var(--eb-emerald) !important; box-shadow: 0 0 0 1px var(--eb-emerald) !important; }

/* ---------- Buttons ---------- */
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"],
button[kind="primary"], button[kind="primaryFormSubmit"] {
  background: var(--eb-forest) !important; color: #FFFFFF !important; border: 0 !important;
  border-radius: 12px !important; padding: .65rem 1.1rem !important; font-weight: 700 !important;
}
[data-testid="stBaseButton-primary"] p, [data-testid="stBaseButton-primaryFormSubmit"] p,
button[kind="primary"] p, button[kind="primaryFormSubmit"] p { color: #FFFFFF !important; font-weight: 700; }
[data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover,
button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover { background: #245B36 !important; }
[data-testid="stBaseButton-secondary"], button[kind="secondary"] {
  background: #FFFFFF; color: var(--eb-forest); border: 1px solid #E1E9E2; border-radius: 12px; font-weight: 600;
}
[data-testid="stBaseButton-secondary"]:hover, button[kind="secondary"]:hover {
  border-color: var(--eb-leaf); color: var(--eb-forest); background: #F7FBF8;
}

/* ---------- Hero banner ---------- */
.eb-hero {
  position: relative; overflow: hidden; display: flex; justify-content: space-between; align-items: center;
  gap: 1.5rem; flex-wrap: wrap; padding: 1.9rem 2.1rem; border-radius: 20px; color: #FFFFFF;
  background: linear-gradient(135deg, #113825 0%, #245B36 100%);
  box-shadow: 0 6px 20px rgba(17, 56, 37, .22);
}
.eb-hero::before {
  content: ""; position: absolute; right: -70px; top: -90px; width: 340px; height: 340px; border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, rgba(115,184,67,.55), rgba(115,184,67,0) 68%);
}
.eb-hero::after {
  content: ""; position: absolute; right: 140px; bottom: -110px; width: 240px; height: 240px; border-radius: 50%;
  background: radial-gradient(circle, rgba(245,166,35,.35), rgba(245,166,35,0) 70%);
}
.eb-hero > * { position: relative; z-index: 1; }
.eb-hero, .eb-hero h2, .eb-hero div, .eb-hero span { color: #FFFFFF; }
.eb-eyebrow { font-size: .78rem; font-weight: 600; opacity: .75; text-transform: uppercase; letter-spacing: .08em; }
.eb-hero-title { margin: .25rem 0 0; font-size: 2rem; font-weight: 800; line-height: 1.15; letter-spacing: -.02em; }
.eb-meta { display: flex; gap: 1.8rem; flex-wrap: wrap; margin-top: 1.1rem; }
.eb-meta-label { font-size: .7rem; opacity: .65; text-transform: uppercase; letter-spacing: .08em; }
.eb-meta-value { font-size: .98rem; font-weight: 600; margin-top: .1rem; }
.eb-score-wrap { text-align: right; min-width: 190px; }
.eb-score { font-size: 4.2rem; font-weight: 800; line-height: 1; letter-spacing: -.03em; }
.eb-score small { font-size: 1.1rem; font-weight: 600; opacity: .7; margin-left: .15rem; }
.eb-score-label { font-size: .8rem; opacity: .75; margin-bottom: .35rem; }
.eb-hero .eb-badge {
  display: inline-block; margin-top: .7rem; padding: .35rem .85rem; border-radius: 999px;
  font-size: .8rem; font-weight: 700; color: #0B2A1B;
}

/* ---------- KPI strip ---------- */
.eb-kpis { display: grid; grid-template-columns: repeat(4, 1fr); margin: .2rem 0 1.2rem; }
.eb-kpi { padding: 0 1.1rem; border-left: 1px solid var(--eb-border); }
.eb-kpi:first-child { border-left: 0; padding-left: 0; }
.eb-kpi-label { font-size: .8rem; font-weight: 600; color: var(--eb-muted); }
.eb-kpi-row { display: flex; align-items: center; gap: .5rem; margin-top: .25rem; flex-wrap: wrap; }
.eb-kpi-value { font-size: 1.7rem; font-weight: 800; color: var(--eb-forest); letter-spacing: -.02em; }
.eb-kpi-sub { font-size: .72rem; color: #8A978F; margin-top: .15rem; }
.eb-delta { font-size: .7rem; font-weight: 700; padding: .15rem .5rem; border-radius: 999px; }
.eb-delta.up { background: var(--eb-emerald); color: #FFFFFF; }
.eb-delta.down { background: var(--eb-amber); color: #3A2A00; }
@media (max-width: 900px) { .eb-kpis { grid-template-columns: repeat(2, 1fr); row-gap: 1rem; } .eb-kpi:nth-child(3) { border-left: 0; padding-left: 0; } }

/* ---------- Regulations ---------- */
.eb-gauge-cap { text-align: center; color: var(--eb-muted); font-size: .78rem; margin: -.4rem 0 .9rem; }
.eb-rules { list-style: none; margin: 0; padding: 0; }
.eb-rules li { display: flex; gap: .65rem; padding: .6rem 0; border-top: 1px solid #F0F4F0; align-items: flex-start; }
.eb-rules li:first-child { border-top: 0; }
.eb-dot { flex: 0 0 10px; height: 10px; border-radius: 50%; margin-top: .38rem; }
.eb-rule-title { font-weight: 700; font-size: .86rem; color: var(--eb-ink); }
.eb-rule-desc { font-size: .78rem; color: var(--eb-muted); line-height: 1.4; margin-top: .1rem; }
.eb-chip { display: inline-block; margin-top: .3rem; font-size: .66rem; font-weight: 700; padding: .1rem .5rem; border-radius: 999px; }
.eb-chip.hit { background: #FDEFD6; color: #9A5B00; }
.eb-chip.miss { background: #F0F4F0; color: #7B8A81; }

/* ---------- Chat ---------- */
[data-testid="stChatMessage"] { background: #F7FAF7; border-radius: 14px; padding: .6rem .8rem; }
[data-testid="stChatInput"] { border-radius: 14px; }
"""


def inject_css() -> None:
    st.html(f"<style>{CSS}</style>")
