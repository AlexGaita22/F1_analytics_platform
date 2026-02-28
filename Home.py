"""
F1 Lap Times - Pagina principală
===============================
Rulează: py -m streamlit run Home.py

Pagină de intrare cu logo și prezentare.
"""

import streamlit as st
import base64
from pathlib import Path

# Configurația paginii
st.set_page_config(
    layout="wide",
    page_title="Lap Times",
    page_icon="🏎️",
    initial_sidebar_state="collapsed"
)

# Ascundem elementele implicite Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {
        background-color: transparent;
    }
    .stApp {
        margin-top: 0px;
        padding-top: 0px;
    }
    .stApp > div {
        padding-top: 0px;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Încărcăm fonturile personalizate din assets/fonts
font_css = ""
fonts_dir = Path("assets/fonts")
if fonts_dir.exists():
    font_files = {
        "Formula1-Regular": "Formula1-Regular-1.ttf",
        "Formula1-Bold": "Formula1-Bold_web.ttf",
        "Formula1-Black": "Formula1-Black.ttf"
    }
    
    font_css_parts = []
    for font_name, font_file in font_files.items():
        font_path = fonts_dir / font_file
        if font_path.exists():
            with open(font_path, "rb") as f:
                font_data = base64.b64encode(f.read()).decode()
            font_css_parts.append(f"""
            @font-face {{
                font-family: '{font_name}';
                src: url(data:font/truetype;charset=utf-8;base64,{font_data}) format('truetype');
                font-weight: normal;
                font-style: normal;
            }}
            """)
    font_css = "".join(font_css_parts)

# CSS pentru landing cu fonturile personalizate
landing_css = f"""
<style>
    {font_css}
    
    .landing-container {{
        min-height: auto;
        display: flex;
        align-items: center;
        padding: 1.25rem;
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }}
    
    .logo-container img {{
        max-width: 100%;
        height: auto;
    }}
    
    .text-container {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 1rem;
    }}
    
    .title-main {{
        font-family: 'Formula1-Bold', 'Formula1-Black', sans-serif;
        font-size: 3.6rem;
        font-weight: 700;
        color: #000000;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0;
        margin-bottom: 0.5rem;
    }}
    
    .subtitle {{
        font-family: 'Formula1-Regular', sans-serif;
        font-size: 1.05rem;
        color: #666666;
        margin: 0;
        margin-bottom: 1.5rem;
        letter-spacing: 0.05em;
    }}
    
    .start-button-container {{
        margin-top: 2rem;
    }}
</style>
"""

st.markdown(landing_css, unsafe_allow_html=True)

# Conținut landing - două coloane: logo stânga, text dreapta
col_left, col_right = st.columns([1, 1])

with col_left:
    # Afișăm logo-ul
    logo_path = Path("assets/f1 red on white.png")
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.error("Logo image not found: assets/f1 red on white.png")

with col_right:
    st.markdown("""
    <div class="text-container">
        <h1 class="title-main">LAP TIMES</h1>
        <p class="subtitle">POWERED BY MN</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Buton start
    if st.button("START", key="start_button", use_container_width=True, type="primary"):
        st.switch_page("pages/1_App.py")

# Style the Streamlit button
st.markdown("""
<style>
    div[data-testid="column"]:nth-of-type(2) button {
        background-color: #FF0000 !important;
        color: white !important;
        font-family: 'Formula1-Bold', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 1rem 4rem !important;
        margin-top: 2rem !important;
        box-shadow: 0 4px 15px rgba(255,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:nth-of-type(2) button:hover {
        background-color: #cc0000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255,0,0,0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Secțiune imagini tematice F1 (plasată imediat sub header, compact)
st.markdown("---")
st.subheader("Paddock vibe & Predictive tech")

img_col1, img_col2 = st.columns(2, gap="small")

with img_col1:
    pitwall_path = Path("assets/imagine1.png")
    if pitwall_path.exists():
        st.image(str(pitwall_path), caption="Pit wall & FastF1 analytics", use_container_width=True)
    else:
        st.info("Adaugă imaginea pit wall în `assets/imagine1.png`.")

with img_col2:
    telemetry_path = Path("assets/imagine3.png")
    if telemetry_path.exists():
        st.image(str(telemetry_path), caption="Predictive engine activ pe circuit", use_container_width=True)
    else:
        st.info("Adaugă imaginea predictive engine în `assets/imagine3.png`.")
