"""EcoBoard | Sustainability Analyzer – entry point.

Run with:  streamlit run app.py

Where to put your keys / links
------------------------------
* ANTHROPIC_API_KEY      -> .streamlit/secrets.toml   (see secrets.toml.example)
* Google Sheet CSV link  -> GOOGLE_SHEET_CSV_URL in utils.py (or in secrets.toml)
"""
import streamlit as st

from styles import inject_css
from utils import PAGE_DASH, PAGE_INPUT

st.set_page_config(
    layout="wide",
    page_title="EcoBoard | Sustainability Analyzer",
    page_icon="🌿",
    initial_sidebar_state="expanded",
)
inject_css()

pages = [
    st.Page(PAGE_INPUT, title="Product Input", icon=":material/edit_note:", url_path="product-input", default=True),
    st.Page(PAGE_DASH, title="Sustainability Dashboard", icon=":material/eco:", url_path="dashboard"),
]
page = st.navigation(pages)

with st.sidebar:
    st.html(
        """
        <div class="eb-side-card">
          <b>How scores work</b><br>
          Every score runs 0&ndash;100 &mdash; <b>higher is greener</b>. Material data is
          adjusted for your manufacturing process, then compared with industry averages
          and greener alternatives.
        </div>
        """
    )

page.run()
