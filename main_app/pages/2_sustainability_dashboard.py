"""Page 2 – score, regulations and Claude greener-alternatives chat."""
from html import escape as esc

import plotly.graph_objects as go
import streamlit as st

from utils import (
    AUTO_PROMPT,
    AMBER,
    EMERALD,
    FOREST,
    LEAF,
    PAGE_INPUT,
    PLASTICS,
    REGULATIONS,
    compliance_readiness,
    get_sheet_url,
    load_material_data,
    rating_for,
    score_product,
    stream_reply,
    stretch,
    top_alternatives,
)

FONT = "Plus Jakarta Sans, Inter, sans-serif"

# ---------------------------------------------------------------- guard
product = st.session_state.get("product")
if not product:
    with st.container(key="card_empty"):
        st.html(
            '<div class="eb-card-title">No product yet</div>'
            '<p class="eb-sub" style="margin-top:.4rem">Fill in the product form first and '
            "we'll build your sustainability dashboard.</p>"
        )
        if st.button("Go to product form", type="primary", key="btn_to_form"):
            st.switch_page(PAGE_INPUT)
    st.stop()

# ---------------------------------------------------------------- data
df, source = load_material_data(get_sheet_url())
result = score_product(df, product["material"], product["process"])
reg = REGULATIONS[product["country"]]
readiness = compliance_readiness(result, product["country"], product["material"])


# ---------------------------------------------------------------- builders
def hero_html() -> str:
    label, colour = rating_for(result["overall"])
    return f"""
<div class="eb-hero">
  <div>
    <div class="eb-eyebrow">Product analysed</div>
    <h2 class="eb-hero-title">{esc(product['name'])}</h2>
    <div class="eb-meta">
      <div><div class="eb-meta-label">Material</div><div class="eb-meta-value">{esc(product['material'])}</div></div>
      <div><div class="eb-meta-label">Manufacturing</div><div class="eb-meta-value">{esc(product['process'])}</div></div>
      <div><div class="eb-meta-label">Sold in</div><div class="eb-meta-value">{esc(product['country'])}</div></div>
    </div>
  </div>
  <div class="eb-score-wrap">
    <div class="eb-score-label">Overall Sustainability Score</div>
    <div class="eb-score">{result['overall']}<small>/100</small></div>
    <span class="eb-badge" style="background:{colour}">↗ Eco Rating · {label}</span>
  </div>
</div>"""


def kpi_html() -> str:
    items = [
        ("Overall Score", result["overall"], result["overall"] - df["Overall_Score"].mean(), "Combined rating"),
        ("Carbon Impact", result["carbon"], result["carbon"] - df["Carbon_Score"].mean(), "Higher = lower footprint"),
        ("Recyclability", result["recyclability"], result["recyclability"] - df["Recyclability_Score"].mean(), "End-of-life recovery"),
        ("Resource Efficiency", result["resource"], result["resource"] - df["Resource_Efficiency"].mean(), "Water, energy & waste"),
    ]
    cells = ""
    for label, value, delta, sub in items:
        d = int(round(delta))
        cls, arrow = ("up", "↗") if d >= 0 else ("down", "↘")
        cells += (
            f'<div class="eb-kpi"><div class="eb-kpi-label">{label}</div>'
            f'<div class="eb-kpi-row"><span class="eb-kpi-value">{value}</span>'
            f'<span class="eb-delta {cls}">{arrow} {d:+d}</span></div>'
            f'<div class="eb-kpi-sub">{sub}</div></div>'
        )
    return f'<div class="eb-kpis">{cells}</div>'


def comparison_fig() -> go.Figure:
    alts = top_alternatives(df, product["material"], product["process"], 2)
    labels = ["Your product", "Industry average"] + [name for name, _ in alts]
    values = [result["overall"], int(round(df["Overall_Score"].mean()))] + [s for _, s in alts]
    colours = [FOREST, EMERALD, LEAF, LEAF]
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color=colours),
            text=values,
            textposition="outside",
            cliponaxis=False,
            textfont=dict(family=FONT, size=14, color=FOREST),
            hovertemplate="%{x}: %{y}/100<extra></extra>",
        )
    )
    try:  # rounded bars need a recent Plotly; harmless to skip on older ones
        fig.update_traces(marker_cornerradius=12)
    except Exception:
        pass
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=24, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        bargap=0.45,
        showlegend=False,
        font=dict(family=FONT, color="#4B5B52"),
        yaxis=dict(visible=False, range=[0, 112]),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=12)),
    )
    return fig


def gauge_fig(value: int) -> go.Figure:
    colour = LEAF if value >= 70 else AMBER
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number=dict(suffix="%", font=dict(size=38, color=FOREST, family=FONT)),
            gauge=dict(
                axis=dict(range=[0, 100], visible=False),
                bar=dict(color=colour, thickness=1),
                bgcolor="#E8EFE9",
                borderwidth=0,
            ),
        )
    )
    fig.update_layout(
        height=160,
        margin=dict(l=10, r=10, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT),
    )
    return fig


def rules_html() -> str:
    dots = [LEAF, EMERALD, FOREST, AMBER]
    is_plastic = product["material"] in PLASTICS
    rows = ""
    for i, (title, desc, plastics_only) in enumerate(reg["rules"]):
        chip = ""
        if plastics_only:
            chip = (
                '<span class="eb-chip hit">Applies to your material</span>'
                if is_plastic
                else '<span class="eb-chip miss">Plastics only</span>'
            )
        rows += (
            f'<li><span class="eb-dot" style="background:{dots[i % 4]}"></span>'
            f'<div><div class="eb-rule-title">{esc(title)}</div>'
            f'<div class="eb-rule-desc">{esc(desc)}</div>{chip}</div></li>'
        )
    return f'<ul class="eb-rules">{rows}</ul>'


# ---------------------------------------------------------------- layout
if st.button("← Analyze Another Product", key="btn_back"):
    st.switch_page(PAGE_INPUT)

left, right = st.columns([2.2, 1.1], gap="large")

with left:
    st.html(hero_html())

    with st.container(key="card_scores"):
        st.html('<div class="eb-card-head"><span class="eb-card-title">Sustainability score</span>'
                '<span class="eb-tag">0–100 · higher is better</span></div>')
        st.html(kpi_html())
        st.plotly_chart(
            comparison_fig(), theme=None, config={"displayModeBar": False}, **stretch(st.plotly_chart)
        )
        note = "" if result["known"] else " · material not in dataset, using the average"
        st.caption(
            f"Data source: {source}{note}. Badges show the difference from the average material in the dataset."
        )

with right:
    with st.container(key="card_regs"):
        st.html(f'<div class="eb-card-head"><span class="eb-card-title">Applicable regulations</span>'
                f'<span class="eb-tag">{esc(reg["short"])}</span></div>')
        st.plotly_chart(
            gauge_fig(readiness), theme=None, config={"displayModeBar": False}, **stretch(st.plotly_chart)
        )
        st.html('<div class="eb-gauge-cap">Compliance readiness · indicative estimate, not legal advice</div>'
                + rules_html())

    with st.container(key="card_chat"):
        st.html('<div class="eb-card-head"><span class="eb-card-title">Greener alternatives</span>'
                '<span class="eb-tag">Claude AI</span></div>')

        # A new submission (new id) resets the chat and queues the auto-prompt.
        if st.session_state.get("chat_sig") != product["submission_id"]:
            st.session_state["chat_sig"] = product["submission_id"]
            st.session_state["chat_messages"] = [
                {"role": "user", "content": AUTO_PROMPT.format(material=product["material"]), "hidden": True}
            ]
        messages = st.session_state["chat_messages"]

        chat_box = st.container(height=340, border=False)
        follow_up = st.chat_input("Ask follow-up questions...", key="chat_input_box")
        if follow_up:
            messages.append({"role": "user", "content": follow_up})

        with chat_box:
            for m in messages:
                if not m.get("hidden"):
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])
            # Last message is from the user (auto-prompt or follow-up) → ask Claude.
            if messages[-1]["role"] == "user":
                with st.chat_message("assistant"):
                    reply = st.write_stream(stream_reply(product, messages, df, result["overall"]))
                messages.append({"role": "assistant", "content": reply})
