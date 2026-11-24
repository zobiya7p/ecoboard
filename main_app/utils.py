"""EcoBoard shared helpers: configuration, data, scoring, regulations, Claude.

Both pages import from here so the logic lives in one place.
"""
from __future__ import annotations

import inspect
import os

import pandas as pd
import streamlit as st

# =====================================================================
# CONFIGURATION  –  the two places you need to edit
# =====================================================================
# 1) GOOGLE SHEET CSV LINK  (optional – the app runs on built-in sample
#    data while this is empty).
#    In Google Sheets: File → Share → "Anyone with the link: Viewer", then
#    use a link of this shape (swap in your sheet ID and tab gid):
#      https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv&gid=0
#    The first row must hold these headers:
#      Material, Overall_Score, Carbon_Score, Recyclability_Score,
#      Resource_Efficiency          (all scores 0-100, higher = greener)
#    You can paste it below OR set GOOGLE_SHEET_CSV_URL in
#    .streamlit/secrets.toml.
GOOGLE_SHEET_CSV_URL = ""

# 2) ANTHROPIC API KEY  – do NOT paste it in code. Add it to
#    .streamlit/secrets.toml (local) or the Secrets box on Streamlit
#    Community Cloud:
#      ANTHROPIC_API_KEY = "sk-ant-..."
#    Without a key, the chatbot shows a built-in offline answer.
ANTHROPIC_MODEL = "claude-sonnet-5-5"

# =====================================================================
# Constants
# =====================================================================
PAGE_INPUT = "pages/1_product_input.py"
PAGE_DASH = "pages/2_sustainability_dashboard.py"

FOREST, LEAF, EMERALD, AMBER = "#113825", "#73B843", "#387642", "#F5A623"

AUTO_PROMPT = "This product uses {material}. Suggest two greener alternatives and explain why."

REQUIRED_COLUMNS = [
    "Material",
    "Overall_Score",
    "Carbon_Score",
    "Recyclability_Score",
    "Resource_Efficiency",
]

# Illustrative sample scores (0-100, higher = greener). Replace with your sheet.
FALLBACK_DF = pd.DataFrame(
    [
        ("Virgin Polypropylene", 41, 35, 50, 45),
        ("PET Plastic", 52, 40, 72, 45),
        ("Recycled PET (rPET)", 71, 68, 74, 70),
        ("Recycled Aluminum", 91, 88, 95, 90),
        ("Virgin Aluminum", 52, 25, 90, 40),
        ("Stainless Steel", 70, 55, 88, 72),
        ("Bamboo Fiber", 74, 82, 55, 85),
        ("Organic Cotton", 61, 70, 60, 52),
        ("Glass", 64, 45, 85, 62),
        ("Cork", 79, 90, 60, 88),
    ],
    columns=REQUIRED_COLUMNS,
)

# Manufacturing process nudges: (carbon delta, resource-efficiency delta)
PROCESS_ADJUST = {
    "Injection Molding": (0, 3),
    "Cold Pressing": (6, 4),
    "CNC Machining": (-8, -10),
    "Extrusion": (-1, 2),
    "Blow Molding": (-1, 1),
    "Casting": (-6, -2),
    "Weaving & Knitting": (-2, -3),
}
PROCESSES = list(PROCESS_ADJUST)

COUNTRIES = ["United Arab Emirates", "European Union", "United States", "United Kingdom"]

PLASTICS = {"Virgin Polypropylene", "PET Plastic", "Recycled PET (rPET)"}
VIRGIN_PLASTICS = {"Virgin Polypropylene", "PET Plastic"}

# (title, one-line description, plastics_only)
REGULATIONS = {
    "United Arab Emirates": {
        "short": "UAE",
        "strictness": 4,
        "rules": [
            ("UAE Net Zero 2050", "National strategic initiative for net-zero emissions; favours low-carbon materials and processes.", False),
            ("Single-Use Plastic Ban", "Federal phase-out of disposable plastic bags and other single-use plastic items.", True),
            ("Emirates Conformity Assessment (ECAS)", "Regulated products need conformity certification and marking before sale.", False),
        ],
    },
    "European Union": {
        "short": "EU",
        "strictness": 10,
        "rules": [
            ("EU Green Deal", "Framework aiming for climate neutrality by 2050 and a circular economy.", False),
            ("Ecodesign for Sustainable Products (ESPR)", "Durability, repairability, recyclability and recycled-content requirements by product group.", False),
            ("Digital Product Passport", "Digital record of materials, origin and recyclability, phasing in by product category.", False),
            ("Single-Use Plastics Directive", "Restricts certain disposable plastic products and sets recycled-content targets.", True),
        ],
    },
    "United States": {
        "short": "US",
        "strictness": 2,
        "rules": [
            ("FTC Green Guides", "Federal rules on environmental marketing claims such as “recyclable” or “eco-friendly”.", False),
            ("State EPR packaging laws", "Producer-responsibility rules in states like California, Oregon and Colorado.", False),
            ("State plastic restrictions", "Bag, foam and single-use plastic limits vary by state and city.", True),
        ],
    },
    "United Kingdom": {
        "short": "UK",
        "strictness": 7,
        "rules": [
            ("Environment Act 2021", "Legal basis for waste-reduction and resource-efficiency targets.", False),
            ("Plastic Packaging Tax", "Applies to plastic packaging with under 30% recycled content.", True),
            ("Packaging EPR", "Producers pay for collecting and recycling the packaging they place on the market.", False),
            ("CMA Green Claims Code", "Environmental claims must be truthful, clear and backed by evidence.", False),
        ],
    },
}

WHY = {
    "Recycled Aluminum": "it is endlessly recyclable and needs far less energy than making virgin metal",
    "Recycled PET (rPET)": "it keeps existing plastic in circulation and cuts demand for virgin resin",
    "Bamboo Fiber": "bamboo regrows quickly with little water or pesticide and stores carbon while growing",
    "Cork": "it is harvested without felling the tree and has a very low carbon footprint",
    "Stainless Steel": "it is highly durable, so one item replaces many, and it is widely recycled",
    "Glass": "it is inert, reusable and recycled again and again without losing quality",
    "Organic Cotton": "it avoids synthetic pesticides and is biodegradable at end of life",
}


# =====================================================================
# Small helpers
# =====================================================================
def stretch(fn) -> dict:
    """Full-width kwargs that work on old (use_container_width) and new (width) Streamlit."""
    try:
        if "width" in inspect.signature(fn).parameters:
            return {"width": "stretch"}
    except (TypeError, ValueError):
        pass
    return {"use_container_width": True}


def index_of(options, value, default=0) -> int:
    try:
        return list(options).index(value)
    except ValueError:
        return default


def get_secret(name: str, default: str = "") -> str:
    """Read from st.secrets, falling back to an environment variable."""
    try:
        value = st.secrets[name]
    except Exception:  # no secrets file / key missing
        value = None
    return str(value).strip() if value else os.environ.get(name, default).strip()


def get_sheet_url() -> str:
    return (GOOGLE_SHEET_CSV_URL or get_secret("GOOGLE_SHEET_CSV_URL")).strip()


# =====================================================================
# Data + scoring
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def load_material_data(sheet_url: str) -> tuple[pd.DataFrame, str]:
    """Return (dataframe, source label). Falls back to built-in data on any problem."""
    if sheet_url:
        try:
            df = pd.read_csv(sheet_url)
            df.columns = [str(c).strip() for c in df.columns]
            missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            if missing:
                raise ValueError(f"missing columns: {', '.join(missing)}")
            df = df[REQUIRED_COLUMNS].copy()
            df["Material"] = df["Material"].astype(str).str.strip()
            for col in REQUIRED_COLUMNS[1:]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            df = df.dropna().drop_duplicates("Material").reset_index(drop=True)
            if df.empty:
                raise ValueError("sheet has no usable rows")
            return df, "Google Sheet"
        except Exception as exc:  # network, permissions, bad format ...
            return FALLBACK_DF.copy(), f"Built-in sample data (sheet unavailable: {type(exc).__name__})"
    return FALLBACK_DF.copy(), "Built-in sample data"


def _clamp(x: float) -> int:
    return int(max(0, min(100, round(x))))


def score_product(df: pd.DataFrame, material: str, process: str) -> dict:
    """Look up the material, then nudge carbon/resource scores for the process."""
    match = df[df["Material"].str.lower() == material.lower()]
    known = not match.empty
    base = match.iloc[0] if known else df[REQUIRED_COLUMNS[1:]].mean()
    carbon_d, resource_d = PROCESS_ADJUST.get(process, (0, 0))
    return {
        "known": known,
        "overall": _clamp(base["Overall_Score"] + (carbon_d + resource_d) / 2),
        "carbon": _clamp(base["Carbon_Score"] + carbon_d),
        "recyclability": _clamp(base["Recyclability_Score"]),
        "resource": _clamp(base["Resource_Efficiency"] + resource_d),
    }


def rating_for(score: int) -> tuple[str, str]:
    """(label, badge colour)"""
    if score >= 80:
        return "Excellent", LEAF
    if score >= 65:
        return "Good", LEAF
    if score >= 50:
        return "Fair", AMBER
    return "Needs work", AMBER


def top_alternatives(df: pd.DataFrame, material: str, process: str, n: int = 2) -> list[tuple[str, int]]:
    """Best-scoring other materials, scored with the same process."""
    others = [m for m in df["Material"] if m.lower() != material.lower()]
    scored = [(m, score_product(df, m, process)["overall"]) for m in others]
    return sorted(scored, key=lambda t: t[1], reverse=True)[:n]


def compliance_readiness(result: dict, country: str, material: str) -> int:
    """Indicative 0-100 estimate – a heuristic, not a legal assessment."""
    base = 0.5 * result["overall"] + 0.3 * result["recyclability"] + 0.2 * result["resource"]
    base -= REGULATIONS[country]["strictness"]
    if material in VIRGIN_PLASTICS:
        base -= 8
    return _clamp(base)


# =====================================================================
# Claude chatbot
# =====================================================================
NO_KEY_FOLLOWUP = (
    "Follow-up questions need an Anthropic API key. Add `ANTHROPIC_API_KEY` to "
    "`.streamlit/secrets.toml` and restart the app."
)


def fallback_alternatives(product: dict, df: pd.DataFrame) -> str:
    alts = top_alternatives(df, product["material"], product["process"], 2)
    lines = [f"Here are two greener options than **{product['material']}**, based on the built-in sustainability data:", ""]
    for i, (name, score) in enumerate(alts, 1):
        why = WHY.get(name, "it scores higher on carbon, recyclability and resource efficiency in the dataset")
        lines.append(f"{i}. **{name}** (score {score}/100): {why}.")
    lines += [
        "",
        "_Offline mode: add `ANTHROPIC_API_KEY` to `.streamlit/secrets.toml` for tailored "
        "suggestions and follow-up answers from Claude._",
    ]
    return "\n".join(lines)


def _system_prompt(product: dict, overall: int) -> str:
    return (
        "You are EcoBoard's sustainability assistant. "
        f"Product: {product['name']}. Material: {product['material']}. "
        f"Manufacturing process: {product['process']}. Sold in: {product['country']}. "
        f"Estimated sustainability score: {overall}/100. "
        "Answer in plain English, concisely (under 200 words unless asked for more), "
        "with short paragraphs or a short list. Be honest about trade-offs, mention "
        "relevant rules in the selling market where helpful, and do not invent "
        "certifications or statistics."
    )


def stream_reply(product: dict, messages: list[dict], df: pd.DataFrame, overall: int):
    """Generator yielding text chunks; pass it to st.write_stream."""
    first_turn = len(messages) == 1
    key = get_secret("ANTHROPIC_API_KEY")
    if not key:
        yield fallback_alternatives(product, df) if first_turn else NO_KEY_FOLLOWUP
        return
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=key)
        with client.messages.stream(
            model=ANTHROPIC_MODEL,
            max_tokens=700,
            system=_system_prompt(product, overall),
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as exc:
        note = f"⚠️ Couldn't reach Claude ({type(exc).__name__}). Check your API key and connection."
        yield (note + "\n\n" + fallback_alternatives(product, df)) if first_turn else note
