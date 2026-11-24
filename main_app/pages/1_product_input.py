"""Page 1 – simple product form. Saves inputs to st.session_state, then opens Page 2."""
import uuid

import streamlit as st

from utils import (
    COUNTRIES,
    PAGE_DASH,
    PROCESSES,
    get_sheet_url,
    index_of,
    load_material_data,
    stretch,
)

materials_df, _ = load_material_data(get_sheet_url())
materials = sorted(materials_df["Material"].tolist())
previous = st.session_state.get("product", {})

_, centre, _ = st.columns([1, 1.7, 1])
with centre:
    with st.container(key="card_form"):
        st.html(
            """
            <div class="eb-form-head">
              <span class="eb-tag">STEP 1 OF 2</span>
              <h2>Analyze a product</h2>
              <p>Tell us what it's made of and where it's sold. We'll score it, list the
              rules that apply and suggest greener alternatives.</p>
            </div>
            """
        )

        with st.form("product_form"):
            name = st.text_input(
                "Product Name",
                value=previous.get("name", ""),
                placeholder="Insulated Travel Tumbler",
                max_chars=80,
            )
            material = st.selectbox(
                "Material",
                materials,
                index=index_of(materials, previous.get("material"), index_of(materials, "Virgin Polypropylene")),
            )
            process = st.selectbox(
                "Manufacturing Process",
                PROCESSES,
                index=index_of(PROCESSES, previous.get("process")),
            )
            country = st.selectbox(
                "Country Sold In",
                COUNTRIES,
                index=index_of(COUNTRIES, previous.get("country")),
            )
            submitted = st.form_submit_button(
                "Analyze sustainability →", type="primary", **stretch(st.form_submit_button)
            )

        if submitted:
            if not name.strip():
                st.error("Please enter a product name.")
            else:
                st.session_state["product"] = {
                    "name": name.strip(),
                    "material": material,
                    "process": process,
                    "country": country,
                    "submission_id": uuid.uuid4().hex,  # lets Page 2 detect a *new* submission
                }
                st.switch_page(PAGE_DASH)
