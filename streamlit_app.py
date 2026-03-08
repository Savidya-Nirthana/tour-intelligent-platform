import streamlit as st
import datetime
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Ceysaid · Travel Intelligence",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  STYLES
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300;1,500&family=Outfit:wght@300;400;500;600&display=swap');

:root {
  --ink:       #0E1117;
  --surface:   #141820;
  --card:      #1A1F2E;
  --border:    rgba(99,178,160,0.2);
  --teal:      #63B2A0;
  --teal-dim:  rgba(99,178,160,0.12);
  --teal-glow: rgba(99,178,160,0.35);
  --sand:      #D4B896;
  --sand-dim:  rgba(212,184,150,0.1);
  --text:      #E4DDD4;
  --muted:     rgba(228,221,212,0.45);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
  background: var(--ink) !important;
  font-family: 'Outfit', sans-serif;
  color: var(--text);
}

[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 50% at 15% 10%,  rgba(99,178,160,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 85% 90%,  rgba(212,184,150,0.06) 0%, transparent 55%);
  pointer-events: none;
  z-index: 0;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMainBlockContainer"] { position: relative; z-index: 1; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: rgba(14,17,23,0.97) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] p  { color: var(--muted) !important; font-size: 0.85rem !important; }
[data-testid="stSidebar"] li { color: var(--muted) !important; font-size: 0.83rem !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: 'Cormorant Garamond', serif !important;
  color: var(--text) !important;
}
[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

/* ── HERO ── */
.hero-wrap {
  display: flex;
  align-items: center;
  gap: 1.8rem;
  padding: 2.4rem 0 1.6rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
  animation: fadeUp 0.5s ease both;
}
.hero-icon {
  font-size: 3.6rem;
  line-height: 1;
  flex-shrink: 0;
  filter: drop-shadow(0 0 20px rgba(99,178,160,0.6));
  animation: pulseIcon 3s ease-in-out infinite;
}
@keyframes pulseIcon {
  0%,100% { filter: drop-shadow(0 0 14px rgba(99,178,160,0.45)); }
  50%      { filter: drop-shadow(0 0 30px rgba(99,178,160,0.85)); }
}
.hero-label {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: var(--teal);
  margin-bottom: 0.4rem;
}
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 600;
  line-height: 1.05;
  color: var(--text);
}
.hero-title span { color: var(--teal); font-style: italic; }
.hero-sub {
  margin-top: 0.5rem;
  font-size: 0.88rem;
  font-weight: 300;
  color: var(--muted);
  line-height: 1.5;
}
.hero-badges {
  display: flex;
  gap: 0.6rem;
  margin-top: 0.9rem;
  flex-wrap: wrap;
}
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: var(--teal-dim);
  border: 1px solid var(--border);
  color: var(--teal);
  font-size: 0.67rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0.28rem 0.7rem;
  border-radius: 4px;
}

/* ── QUERY TYPE CARDS ── */
.qt-row { display: flex; gap: 0.8rem; margin-bottom: 1.4rem; animation: fadeUp 0.5s 0.1s ease both; }
.qt-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  padding: 1.1rem 0.5rem;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  text-align: center;
}
.qt-card.active {
  background: var(--teal-dim);
  border-color: var(--teal);
  box-shadow: 0 0 22px rgba(99,178,160,0.15);
}
.qt-card .qt-icon  { font-size: 1.5rem; line-height: 1; }
.qt-card .qt-label {
  font-size: 0.7rem; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--muted);
}
.qt-card.active .qt-label { color: var(--teal); }
.qt-card .qt-desc { font-size: 0.7rem; color: var(--muted); font-weight: 300; line-height: 1.3; }

/* ── INPUT SHELL ── */
.input-shell {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem 1.7rem 1.3rem;
  box-shadow: 0 4px 30px rgba(0,0,0,0.35);
  margin-bottom: 0.5rem;
  animation: fadeUp 0.5s 0.2s ease both;
}
.input-shell-title {
  font-size: 0.67rem; font-weight: 600;
  letter-spacing: 0.28em; text-transform: uppercase;
  color: var(--teal); margin-bottom: 1rem;
  display: flex; align-items: center; gap: 0.5rem;
}
.input-shell-title::after { content:''; flex:1; height:1px; background: var(--border); }

/* Widget label overrides */
[data-testid="stTextArea"] > label {
  color: rgba(228,221,212,0.5) !important;
  font-size: 0.73rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}
[data-testid="stTextArea"] textarea {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(99,178,160,0.25) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 0.95rem !important;
  font-weight: 300 !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 3px rgba(99,178,160,0.1) !important;
  outline: none !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: rgba(228,221,212,0.22) !important; }

/* Submit button */
[data-testid="stFormSubmitButton"] button {
  background: linear-gradient(135deg, #63B2A0 0%, #4A9D8B 50%, #63B2A0 100%) !important;
  background-size: 200% !important;
  border: none !important;
  border-radius: 8px !important;
  color: #0E1117 !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.83rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  padding: 0.7rem 2rem !important;
  width: 100% !important;
  cursor: pointer !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(99,178,160,0.3) !important;
  animation: btnShimmer 3s ease infinite !important;
}
@keyframes btnShimmer {
  0%,100% { background-position: 0% 50%; }
  50%     { background-position: 100% 50%; }
}
[data-testid="stFormSubmitButton"] button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(99,178,160,0.45) !important;
}

/* Selector buttons — hidden visually, just for logic */
[data-testid="stButton"] button {
  background: transparent !important;
  border: none !important;
  color: rgba(99,178,160,0.6) !important;
  font-size: 0.72rem !important;
  font-family: 'Outfit', sans-serif !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  padding: 0.2rem 0 !important;
  cursor: pointer !important;
  width: 100% !important;
  font-weight: 500 !important;
}
[data-testid="stButton"] button:hover { color: var(--teal) !important; }

/* ── RESULT PANEL ── */
.result-wrap {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 8px 50px rgba(0,0,0,0.4);
  animation: fadeUp 0.45s cubic-bezier(0.16,1,0.3,1) both;
  margin-top: 1.2rem;
}
.result-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.9rem 1.5rem;
  background: rgba(99,178,160,0.07);
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap; gap: 0.5rem;
}
.result-header-left { display: flex; align-items: center; gap: 0.7rem; }
.result-title { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; font-weight: 600; color: var(--text); }
.result-badge {
  display: inline-flex; align-items: center; gap: 0.3rem;
  background: var(--teal-dim); border: 1px solid rgba(99,178,160,0.4);
  color: var(--teal); font-size: 0.63rem; font-weight: 600;
  letter-spacing: 0.18em; text-transform: uppercase;
  padding: 0.25rem 0.6rem; border-radius: 4px;
}
.result-meta { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.04em; }
.result-body { padding: 1.7rem 1.7rem 1.2rem; }
.result-footer {
  padding: 0.8rem 1.5rem;
  background: rgba(0,0,0,0.15);
  border-top: 1px solid var(--border);
  font-size: 0.7rem; color: var(--muted);
  font-style: italic; text-align: center;
}

/* Markdown result styling */
[data-testid="stMarkdownContainer"] h1 {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.6rem !important; font-weight: 600 !important;
  color: var(--text) !important;
  border-bottom: 1px solid var(--border) !important;
  padding-bottom: 0.4rem !important; margin-bottom: 1rem !important;
}
[data-testid="stMarkdownContainer"] h2 {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.25rem !important; color: var(--sand) !important;
  margin: 1.3rem 0 0.5rem !important;
}
[data-testid="stMarkdownContainer"] h3 {
  font-size: 0.98rem !important; font-weight: 600 !important;
  color: var(--teal) !important; letter-spacing: 0.04em !important;
  margin: 1rem 0 0.35rem !important;
}
[data-testid="stMarkdownContainer"] p {
  color: rgba(228,221,212,0.82) !important;
  line-height: 1.8 !important; font-weight: 300 !important;
  margin-bottom: 0.65rem !important;
}
[data-testid="stMarkdownContainer"] li {
  color: rgba(228,221,212,0.78) !important;
  line-height: 1.75 !important; font-weight: 300 !important;
  margin-bottom: 0.3rem !important;
}
[data-testid="stMarkdownContainer"] strong { color: var(--sand) !important; font-weight: 600 !important; }
[data-testid="stMarkdownContainer"] hr { border-color: rgba(99,178,160,0.18) !important; margin: 1.1rem 0 !important; }
[data-testid="stMarkdownContainer"] blockquote {
  border-left: 3px solid var(--teal) !important;
  background: var(--teal-dim) !important;
  padding: 0.75rem 1.1rem !important; border-radius: 0 8px 8px 0 !important;
  color: rgba(228,221,212,0.75) !important; font-style: italic !important;
  margin: 0.8rem 0 !important;
}
[data-testid="stMarkdownContainer"] table { border-collapse: collapse !important; width: 100% !important; margin: 1rem 0 !important; }
[data-testid="stMarkdownContainer"] th {
  background: var(--teal-dim) !important; color: var(--teal) !important;
  font-size: 0.73rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important;
  padding: 0.55rem 0.9rem !important; border: 1px solid var(--border) !important;
}
[data-testid="stMarkdownContainer"] td {
  padding: 0.5rem 0.9rem !important; border: 1px solid var(--border) !important;
  color: rgba(228,221,212,0.78) !important; font-size: 0.87rem !important;
}
[data-testid="stMarkdownContainer"] tr:hover td { background: rgba(99,178,160,0.05) !important; }

/* Error */
[data-testid="stAlert"] {
  background: rgba(224,112,112,0.08) !important;
  border: 1px solid rgba(224,112,112,0.3) !important;
  border-radius: 8px !important; color: #ff9999 !important;
}

/* Spinner */
[data-testid="stSpinner"] > div { border-top-color: var(--teal) !important; }

/* Hide chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: rgba(99,178,160,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,178,160,0.55); }

@keyframes fadeUp {
  from { opacity:0; transform: translateY(14px); }
  to   { opacity:1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
if "query_type"   not in st.session_state: st.session_state.query_type   = "tour"
if "last_answer"  not in st.session_state: st.session_state.last_answer  = None
if "last_query"   not in st.session_state: st.session_state.last_query   = ""
if "last_type"    not in st.session_state: st.session_state.last_type    = ""

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
## ✈ Ceysaid
### Travel Intelligence

All answers are sourced directly from the **Ceysaid website** — tours, packages, and visa information.

---

### 🗺 Tour Queries
- *"What tours are available in Kandy?"*
- *"Tell me about the Ella rock hiking tour"*
- *"What's included in the Cultural Triangle tour?"*
- *"5-day packages from Colombo"*

---

### 🛂 Visa Queries
- *"Do I need a visa to visit Sri Lanka?"*
- *"How do I apply for a Sri Lanka ETA?"*
- *"Visa requirements for UK nationals"*
- *"How long is a tourist visa valid?"*

---

### ℹ About
This assistant answers **only** from crawled Ceysaid.com content. It does not access external sources or real-time data.
""")

# ══════════════════════════════════════════════════════════════════
#  MAIN + RIGHT STRIP
# ══════════════════════════════════════════════════════════════════
main_col, info_col = st.columns([3, 1], gap="large")

with main_col:

    # ── HERO ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-icon">✈</div>
      <div>
        <div class="hero-label">Website Intelligence · Ceysaid.com</div>
        <div class="hero-title">Your Travel Companion</div>
        <div class="hero-sub">Ask anything about tours, packages &amp; visa requirements —<br>answered exclusively from Ceysaid's own website content.</div>
        <div class="hero-badges">
          <span class="badge">🗺 Tours &amp; Packages</span>
          <span class="badge">🛂 Visa Information</span>
          <span class="badge">🌿 Sri Lanka</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── QUERY TYPE SELECTOR ────────────────────────────────────────
    st.markdown('<div style="font-size:0.63rem;font-weight:600;letter-spacing:0.3em;text-transform:uppercase;color:rgba(99,178,160,0.6);margin-bottom:0.7rem;">Select query type</div>', unsafe_allow_html=True)

    tc, vc = st.columns(2, gap="small")
    with tc:
        ta = "active" if st.session_state.query_type == "tour" else ""
        st.markdown(f'<div class="qt-card {ta}"><div class="qt-icon">🗺</div><div class="qt-label">Tours &amp; Packages</div><div class="qt-desc">Destinations, itineraries &amp; inclusions</div></div>', unsafe_allow_html=True)
        if st.button("↳ Select Tours", key="sel_tour"):
            st.session_state.query_type = "tour"
            st.rerun()
    with vc:
        va = "active" if st.session_state.query_type == "visa" else ""
        st.markdown(f'<div class="qt-card {va}"><div class="qt-icon">🛂</div><div class="qt-label">Visa Information</div><div class="qt-desc">Entry requirements &amp; applications</div></div>', unsafe_allow_html=True)
        if st.button("↳ Select Visa", key="sel_visa"):
            st.session_state.query_type = "visa"
            st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── INPUT AREA ─────────────────────────────────────────────────
    qtype = st.session_state.query_type
    icon  = "🗺" if qtype == "tour" else "🛂"
    label = "Tour & Package Query" if qtype == "tour" else "Visa Information Query"
    placeholder = (
        "e.g. What 5-day tours are available from Colombo? What is included in the Sigiriya day trip?"
        if qtype == "tour"
        else "e.g. What visa do I need to visit Sri Lanka as a UK citizen? How do I apply for an ETA?"
    )

    st.markdown(f'<div class="input-shell"><div class="input-shell-title">{icon} &nbsp;{label}</div></div>', unsafe_allow_html=True)

    with st.form(key="query_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your question",
            placeholder=placeholder,
            height=110,
        )
        submit = st.form_submit_button("→  Search Ceysaid Knowledge Base")

    # ── HANDLE SUBMIT ──────────────────────────────────────────────
    if submit and user_input.strip():
        spinner_msg = "Searching tour database…" if qtype == "tour" else "Retrieving visa information…"
        with st.spinner(spinner_msg):
            try:
                response = requests.post(f"{BASE_URL}/query", json={"question": user_input}, timeout=30)
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                    st.session_state.last_answer = answer
                    st.session_state.last_query  = user_input
                    st.session_state.last_type   = qtype
                else:
                    st.error(f"⚠ Server error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("⚠ Cannot connect to backend at `localhost:8000`. Is the server running?")
            except requests.exceptions.Timeout:
                st.error("⚠ Request timed out. The server took too long to respond.")
            except Exception as e:
                st.error(f"⚠ Unexpected error: {e}")

    # ── RESULT ────────────────────────────────────────────────────
    if st.session_state.last_answer:
        rtype  = st.session_state.last_type
        ricon  = "🗺" if rtype == "tour" else "🛂"
        rlabel = "Tour Result" if rtype == "tour" else "Visa Result"
        now    = datetime.datetime.now().strftime("%d %b %Y · %H:%M")

        st.markdown(f"""
        <div class="result-wrap">
          <div class="result-header">
            <div class="result-header-left">
              <span style="font-size:1.3rem">{ricon}</span>
              <span class="result-title">Ceysaid Answer</span>
              <span class="result-badge">{rlabel}</span>
            </div>
            <span class="result-meta">ceysaid.com · {now}</span>
          </div>
          <div class="result-body">
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.last_answer)

        st.markdown("""
          </div>
          <div class="result-footer">
            ✈ &nbsp; Information sourced exclusively from Ceysaid website content.
            Confirm details directly with Ceysaid before booking.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  RIGHT INFO STRIP
# ══════════════════════════════════════════════════════════════════
with info_col:
    st.markdown("""
    <div style="padding-top:2.8rem; display:flex; flex-direction:column; gap:1rem;">

      <div style="background:rgba(99,178,160,0.07);border:1px solid rgba(99,178,160,0.2);
                  border-radius:10px;padding:1.2rem 1rem;">
        <div style="font-size:0.6rem;font-weight:600;letter-spacing:0.28em;text-transform:uppercase;
                    color:#63B2A0;margin-bottom:0.85rem;">🌿 Top Destinations</div>
        <div style="font-size:0.82rem;color:rgba(228,221,212,0.68);line-height:2.1;">
          📍 Sigiriya<br>📍 Ella<br>📍 Kandy<br>📍 Galle Fort<br>📍 Yala Safari<br>📍 Mirissa Beach
        </div>
      </div>

      <div style="background:rgba(212,184,150,0.06);border:1px solid rgba(212,184,150,0.18);
                  border-radius:10px;padding:1.2rem 1rem;">
        <div style="font-size:0.6rem;font-weight:600;letter-spacing:0.28em;text-transform:uppercase;
                    color:#D4B896;margin-bottom:0.85rem;">🛂 Visa Quick Facts</div>
        <div style="font-size:0.8rem;color:rgba(228,221,212,0.62);line-height:1.75;">
          Most nationals need an <strong style="color:#D4B896;">ETA</strong> before arrival.<br><br>
          Ask about your nationality for specific requirements.
        </div>
      </div>

      <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                  border-radius:10px;padding:1.1rem 1rem;">
        <div style="font-size:0.6rem;font-weight:600;letter-spacing:0.28em;text-transform:uppercase;
                    color:rgba(228,221,212,0.3);margin-bottom:0.7rem;">⚡ Data Source</div>
        <div style="font-size:0.75rem;color:rgba(228,221,212,0.38);line-height:1.65;font-style:italic;">
          Answers drawn exclusively from crawled Ceysaid.com content. No external data is used.
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)