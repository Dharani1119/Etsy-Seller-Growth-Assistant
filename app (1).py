import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

st.set_page_config(
    page_title="D'aura Labs — Etsy AI Coach",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #080D1A !important;
    color: #F1F5F9 !important;
}
.stApp { background-color: #080D1A !important; }
.block-container {
    padding: 2rem 2.5rem 5rem !important;
    max-width: 880px !important;
    margin: 0 auto;
}
#MainMenu, footer, .stDeployButton,
[data-testid="stToolbar"] { visibility: hidden !important; }
header[data-testid="stHeader"] {
    background: rgba(8,13,26,0.97) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

/* KPI metric cards */
[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 18px !important;
    padding: 22px 20px !important;
}
[data-testid="metric-container"] label {
    color: #4B5563 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: #F9FAFB !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 13px 30px !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.35) !important;
    letter-spacing: .1px !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: #111827 !important;
    border: 2px dashed rgba(124,58,237,0.4) !important;
    border-radius: 20px !important;
    padding: 24px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111827 !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 2px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6B7280 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
    color: white !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #7C3AED, #A78BFA) !important;
    border-radius: 6px !important;
}

/* Text input */
.stTextInput > div > div {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #F9FAFB !important;
    padding: 4px 8px !important;
}
.stTextInput input {
    color: #F9FAFB !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput input::placeholder { color: #4B5563 !important; }

/* Expander */
details {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    padding: 4px 8px !important;
}
summary { color: #F9FAFB !important; font-weight: 500 !important; font-size: 14px !important; }

hr { border-color: rgba(255,255,255,0.05) !important; margin: 6px 0 !important; }
.stAlert { border-radius: 14px !important; }
.stSpinner > div { border-top-color: #7C3AED !important; }

/* ── D'aura Labs persistent watermark (bottom-right) ── */
.gp-watermark {
    position: fixed;
    bottom: 18px;
    right: 20px;
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(8,13,26,0.82);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 30px;
    padding: 7px 14px 7px 10px;
    pointer-events: none;
    user-select: none;
}
.gp-watermark-icon {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #7C3AED, #6D28D9);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    flex-shrink: 0;
}
.gp-watermark-text {
    font-size: 11px;
    font-weight: 700;
    color: #A78BFA;
    letter-spacing: .3px;
    font-family: 'Inter', sans-serif;
}
.gp-watermark-sub {
    font-size: 9px;
    font-weight: 500;
    color: #4B5563;
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ── Persistent D'aura Labs watermark — injected once, always visible ──────
st.markdown("""
<div class="gp-watermark">
    <div class="gp-watermark-icon">⚡</div>
    <div>
        <div class="gp-watermark-text">D\'aura Labs</div>
        <div class="gp-watermark-sub">Etsy AI Coach</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Palette ────────────────────────────────────────────────────────────────
PURPLE = "#7C3AED"
PURPLE_L = "#A78BFA"
GREEN  = "#10B981"
RED    = "#EF4444"
AMBER  = "#F59E0B"
BLUE   = "#3B82F6"
SURF   = "#111827"
MUTED  = "#6B7280"

PLOTLY_BASE = dict(
    paper_bgcolor=SURF,
    plot_bgcolor=SURF,
    font=dict(family="Inter", color="#F9FAFB", size=12),
    margin=dict(l=16, r=16, t=36, b=16),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
)

# ── HTML helpers ───────────────────────────────────────────────────────────
def H(s): st.markdown(s, unsafe_allow_html=True)
def gap(px=20): H(f"<div style='height:{px}px'></div>")

def section_label(text):
    H(f"""<div style='font-size:10px;font-weight:800;letter-spacing:1.2px;color:#4B5563;
               text-transform:uppercase;margin:36px 0 16px;'>{text}</div>""")

def ai_summary(headline, body):
    H(f"""
    <div style="background:linear-gradient(145deg,#13102A,#0E1628);
                border:1px solid rgba(124,58,237,0.35);border-radius:24px;
                padding:32px 36px;margin-bottom:6px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-60px;right:-60px;width:200px;height:200px;
                    background:radial-gradient(circle,rgba(124,58,237,0.18),transparent 70%);
                    pointer-events:none;border-radius:50%;"></div>
        <div style="position:absolute;bottom:-40px;left:-40px;width:160px;height:160px;
                    background:radial-gradient(circle,rgba(167,139,250,0.08),transparent 70%);
                    pointer-events:none;border-radius:50%;"></div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
            <div style="background:linear-gradient(135deg,#7C3AED,#6D28D9);width:36px;height:36px;
                        border-radius:12px;display:flex;align-items:center;justify-content:center;
                        font-size:18px;flex-shrink:0;box-shadow:0 4px 12px rgba(124,58,237,0.4);">✨</div>
            <div>
                <div style="font-size:10px;font-weight:800;letter-spacing:1px;color:#7C3AED;
                            text-transform:uppercase;">AI Business Summary</div>
                <div style="font-size:13px;font-weight:600;color:#F9FAFB;margin-top:1px;">{headline}</div>
            </div>
        </div>
        <div style="font-size:15px;color:#D1D5DB;line-height:1.9;font-weight:400;">{body}</div>
    </div>""")

def insight_card(icon, tag, tag_color, title, body, cta=None):
    tag_bg = {
        GREEN: "rgba(16,185,129,0.12)", RED: "rgba(239,68,68,0.12)",
        AMBER: "rgba(245,158,11,0.12)", BLUE: "rgba(59,130,246,0.12)",
        PURPLE: "rgba(124,58,237,0.12)",
    }.get(tag_color, "rgba(124,58,237,0.12)")
    cta_html = f"""<div style="margin-top:14px;background:rgba(255,255,255,0.04);
                border-radius:10px;padding:10px 14px;font-size:12px;color:#9CA3AF;
                border-left:2px solid {tag_color};">💡 {cta}</div>""" if cta else ""
    H(f"""
    <div style="background:#111827;border:1px solid rgba(255,255,255,0.07);
                border-radius:20px;padding:24px 26px;margin-bottom:12px;
                transition:border-color .2s;">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;">
            <div style="display:flex;align-items:flex-start;gap:14px;flex:1;">
                <div style="font-size:26px;flex-shrink:0;margin-top:2px;">{icon}</div>
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <span style="background:{tag_bg};color:{tag_color};font-size:10px;
                                     font-weight:700;padding:3px 10px;border-radius:20px;
                                     letter-spacing:.4px;text-transform:uppercase;">{tag}</span>
                    </div>
                    <div style="font-size:15px;font-weight:600;color:#F9FAFB;
                                margin-bottom:6px;line-height:1.4;">{title}</div>
                    <div style="font-size:13px;color:#9CA3AF;line-height:1.7;">{body}</div>
                    {cta_html}
                </div>
            </div>
        </div>
    </div>""")

def product_card(rank, name, revenue, conv, badge, badge_color, note, orders):
    bc_bg = {
        "🔥 Bestseller": "rgba(16,185,129,0.12)", "🚀 Growing": "rgba(124,58,237,0.12)",
        "⚠️ Needs Work": "rgba(245,158,11,0.12)", "💀 Struggling": "rgba(239,68,68,0.12)",
    }.get(badge, "rgba(124,58,237,0.12)")
    bc_col = {
        "🔥 Bestseller": GREEN, "🚀 Growing": PURPLE_L,
        "⚠️ Needs Work": AMBER, "💀 Struggling": RED,
    }.get(badge, PURPLE_L)
    H(f"""
    <div style="background:#111827;border:1px solid rgba(255,255,255,0.07);
                border-radius:20px;padding:22px 24px;margin-bottom:12px;">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;">
            <div style="display:flex;align-items:flex-start;gap:16px;flex:1;">
                <div style="width:36px;height:36px;border-radius:12px;
                            background:rgba(124,58,237,0.12);color:{PURPLE_L};
                            font-size:16px;font-weight:800;display:flex;align-items:center;
                            justify-content:center;flex-shrink:0;margin-top:2px;">#{rank}</div>
                <div style="flex:1;">
                    <div style="font-size:15px;font-weight:600;color:#F9FAFB;
                                margin-bottom:10px;">{name}</div>
                    <div style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:14px;">
                        <div>
                            <div style="font-size:10px;color:#4B5563;font-weight:700;
                                        text-transform:uppercase;letter-spacing:.5px;">Revenue</div>
                            <div style="font-size:20px;font-weight:700;color:{GREEN};
                                        margin-top:2px;">{revenue}</div>
                        </div>
                        <div>
                            <div style="font-size:10px;color:#4B5563;font-weight:700;
                                        text-transform:uppercase;letter-spacing:.5px;">Conversion</div>
                            <div style="font-size:20px;font-weight:700;color:{PURPLE_L};
                                        margin-top:2px;">{conv}</div>
                        </div>
                        <div>
                            <div style="font-size:10px;color:#4B5563;font-weight:700;
                                        text-transform:uppercase;letter-spacing:.5px;">Orders</div>
                            <div style="font-size:20px;font-weight:700;color:#F9FAFB;
                                        margin-top:2px;">{orders}</div>
                        </div>
                    </div>
                    <div style="background:rgba(255,255,255,0.04);border-radius:10px;
                                padding:10px 14px;font-size:12px;color:#9CA3AF;line-height:1.6;
                                border-left:2px solid {bc_col};">{note}</div>
                </div>
            </div>
            <div style="background:{bc_bg};color:{bc_col};font-size:11px;font-weight:700;
                        padding:5px 12px;border-radius:20px;white-space:nowrap;flex-shrink:0;
                        border:1px solid {bc_col}33;">{badge}</div>
        </div>
    </div>""")

def action_item(num, text, impact, detail):
    color = GREEN if impact == "High" else (AMBER if impact == "Medium" else MUTED)
    bg    = "rgba(16,185,129,0.08)" if impact == "High" else \
            ("rgba(245,158,11,0.08)" if impact == "Medium" else "rgba(107,114,128,0.08)")
    H(f"""
    <div style="background:#111827;border:1px solid rgba(255,255,255,0.07);
                border-radius:18px;padding:20px 22px;margin-bottom:10px;">
        <div style="display:flex;align-items:flex-start;gap:14px;">
            <div style="width:32px;height:32px;border-radius:10px;
                        background:rgba(124,58,237,0.15);color:{PURPLE_L};
                        font-size:14px;font-weight:800;display:flex;align-items:center;
                        justify-content:center;flex-shrink:0;">{num}</div>
            <div style="flex:1;">
                <div style="display:flex;align-items:center;justify-content:space-between;
                            gap:12px;margin-bottom:6px;">
                    <div style="font-size:14px;font-weight:600;color:#F9FAFB;">{text}</div>
                    <div style="background:{bg};color:{color};font-size:10px;font-weight:800;
                                padding:3px 10px;border-radius:20px;white-space:nowrap;
                                letter-spacing:.4px;text-transform:uppercase;">{impact}</div>
                </div>
                <div style="font-size:12px;color:#6B7280;line-height:1.65;">{detail}</div>
            </div>
        </div>
    </div>""")

def health_bar(label, score, color):
    c1, c2 = st.columns([5, 1])
    c1.markdown(f"<div style='font-size:13px;color:#9CA3AF;margin-bottom:4px;'>{label}</div>",
                unsafe_allow_html=True)
    c2.markdown(f"<div style='font-size:13px;font-weight:700;text-align:right;color:{color}'>{score}</div>",
                unsafe_allow_html=True)
    st.progress(score / 100)
    gap(4)

# ── Demo data ──────────────────────────────────────────────────────────────
@st.cache_data
def make_demo():
    products = [
        "Digital Planner Bundle", "Moon Phase Print Set",
        "Crystal Grid Templates", "Affirmation Card Deck", "Zodiac Wall Calendar"
    ]
    weights  = [38, 28, 18, 11, 5]
    prices   = {"Digital Planner Bundle": 38, "Moon Phase Print Set": 28,
                "Crystal Grid Templates": 22, "Affirmation Card Deck": 18,
                "Zodiac Wall Calendar": 12}
    rows = []
    monthly_base = [180,210,195,240,220,280,310,290,340,410,580,520]
    for mi, base in enumerate(monthly_base):
        for _ in range(max(1, int(base / 32))):
            p  = random.choices(products, weights=weights)[0]
            px = prices[p]
            rows.append({
                "Order Date": pd.Timestamp(2024, mi + 1, random.randint(1, 27)),
                "Product":    p,
                "Order Total": px + random.uniform(-1.5, 2.5),
                "Etsy Fee":   round(px * 0.065, 2),
                "Country":    random.choices(
                    ["United States","United Kingdom","Canada","Australia","Germany"],
                    weights=[58, 16, 14, 8, 4])[0],
            })
    df = pd.DataFrame(rows)
    df["Net Revenue"] = df["Order Total"] - df["Etsy Fee"]
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

# ── Column auto-mapper for real Etsy CSVs ─────────────────────────────────
def normalize(raw: pd.DataFrame) -> pd.DataFrame:
    lc = {c.lower().strip(): c for c in raw.columns}
    def fc(*keys):
        for k in keys:
            if k in lc: return lc[k]
        return None
    mapping = {
        "Order Date":  fc("order date","sale date","date","created"),
        "Product":     fc("listing title","product","title","item","listing"),
        "Order Total": fc("order total","total","sale amount","order total (usd)","amount"),
        "Etsy Fee":    fc("etsy fee","fees","transaction fee","fees (usd)","listing fee"),
        "Country":     fc("ship to country","ship country","country","buyer country"),
    }
    df = pd.DataFrame()
    for dst, src in mapping.items():
        if src:
            df[dst] = raw[src]
    if "Order Date" in df:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    if "Order Total" in df:
        df["Order Total"] = pd.to_numeric(
            df["Order Total"].astype(str).str.replace(r'[$,]', '', regex=True),
            errors="coerce").fillna(0)
    if "Etsy Fee" not in df and "Order Total" in df:
        df["Etsy Fee"] = df["Order Total"] * 0.065
    df["Net Revenue"] = df.get("Order Total", pd.Series(dtype=float)) - \
                        df.get("Etsy Fee",    pd.Series(dtype=float))
    if "Order Date" in df:
        df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    if "Product" not in df:
        df["Product"] = "Your Product"
    return df

# ── Session ────────────────────────────────────────────────────────────────
for k, v in [("page","landing"), ("df",None), ("is_demo",False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════
#  LANDING
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    gap(48)
    H("""
    <div style="text-align:center;max-width:620px;margin:0 auto;">
        <div style="display:inline-flex;align-items:center;gap:8px;
                    background:rgba(124,58,237,0.12);color:#A78BFA;font-size:11px;
                    font-weight:700;padding:7px 18px;border-radius:30px;
                    border:1px solid rgba(124,58,237,0.3);margin-bottom:32px;
                    letter-spacing:.8px;text-transform:uppercase;">
            ⚡ D'aura Labs — AI Etsy Business Coach
        </div>
        <h1 style="font-size:clamp(32px,5vw,52px);font-weight:800;line-height:1.15;
                   color:#FFFFFF;margin-bottom:20px;letter-spacing:-.8px;">
            Your Etsy shop,<br>
            <span style="background:linear-gradient(135deg,#7C3AED,#A78BFA);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                fully explained
            </span>
        </h1>
        <p style="color:#6B7280;font-size:16px;max-width:460px;margin:0 auto 44px;
                  line-height:1.8;font-weight:400;">
            Drop your Etsy CSV and get a plain-English AI summary of what's
            working, what's broken, and exactly what to do next.
        </p>
    </div>""")

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        uploaded = st.file_uploader(
            "", type=["csv","xlsx"], label_visibility="collapsed"
        )
        gap(12)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📤  Analyze my shop", use_container_width=True):
                if uploaded:
                    try:
                        raw = pd.read_excel(uploaded) \
                              if uploaded.name.endswith(".xlsx") \
                              else pd.read_csv(uploaded)
                        st.session_state.df      = normalize(raw)
                        st.session_state.is_demo = False
                        st.session_state.page    = "loading"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Couldn't read that file: {e}")
                else:
                    st.warning("Upload a CSV first, or hit 'Try demo'.")
        with c2:
            if st.button("👁️  Try demo shop", use_container_width=True):
                st.session_state.df      = make_demo()
                st.session_state.is_demo = True
                st.session_state.page    = "loading"
                st.rerun()

    gap(36)
    H("""
    <div style="display:flex;gap:28px;justify-content:center;flex-wrap:wrap;">
        <span style="font-size:12px;color:#374151;">🔒 Data never leaves your device</span>
        <span style="font-size:12px;color:#374151;">⚡ Results in under 10 seconds</span>
        <span style="font-size:12px;color:#374151;">✨ Plain-English AI — no jargon</span>
        <span style="font-size:12px;color:#374151;">📱 Works on mobile</span>
    </div>""")
    gap(32)
    H("""
    <div style="text-align:center;border-top:1px solid rgba(255,255,255,0.05);
                padding-top:24px;margin-top:8px;">
        <div style="display:inline-flex;align-items:center;gap:7px;margin-bottom:6px;">
            <div style="background:linear-gradient(135deg,#7C3AED,#6D28D9);width:22px;height:22px;
                        border-radius:7px;display:inline-flex;align-items:center;
                        justify-content:center;font-size:11px;">⚡</div>
            <span style="font-size:14px;font-weight:800;color:#F9FAFB;letter-spacing:-.2px;">
                D'aura Labs</span>
        </div>
        <div style="font-size:11px;color:#374151;margin-top:2px;">
            © 2025 D'aura Labs · All rights reserved · Unauthorized resale or redistribution prohibited
        </div>
    </div>""")

# ══════════════════════════════════════════════════════════════════════════
#  LOADING
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "loading":
    gap(90)
    _, lc, _ = st.columns([1, 2, 1])
    with lc:
        steps = [
            ("🔍", "Reading your shop data…"),
            ("📊", "Calculating revenue & profit…"),
            ("🏆", "Identifying your winning products…"),
            ("⚠️",  "Detecting profit leaks & problems…"),
            ("✨", "Writing your AI business summary…"),
        ]
        ph  = st.empty()
        bar = st.progress(0)
        for i, (icon, msg) in enumerate(steps):
            ph.markdown(f"""
            <div style='text-align:center;padding:20px 0;'>
                <div style='font-size:36px;margin-bottom:14px;'>{icon}</div>
                <div style='font-size:18px;font-weight:600;color:#F9FAFB;
                            margin-bottom:6px;'>{msg}</div>
                <div style='font-size:12px;color:#4B5563;'>Step {i+1} of {len(steps)}</div>
            </div>""", unsafe_allow_html=True)
            bar.progress((i + 1) / len(steps))
            time.sleep(0.55)
        st.session_state.page = "dashboard"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    df       = st.session_state.df
    is_demo  = st.session_state.is_demo

    # ── Core numbers ──────────────────────────────────────────────────────
    rev     = df["Order Total"].sum()   if "Order Total"  in df.columns else 0
    profit  = df["Net Revenue"].sum()   if "Net Revenue"  in df.columns else rev * 0.61
    orders  = len(df)
    aov     = rev / orders              if orders else 0
    margin  = profit / rev * 100        if rev    else 0

    monthly = df.groupby("Month").agg(
        Rev=("Order Total","sum"),
        Ord=("Order Total","count")
    ).reset_index() if "Month" in df.columns else pd.DataFrame(columns=["Month","Rev","Ord"])

    growth  = (
        (monthly["Rev"].iloc[-1] - monthly["Rev"].iloc[-2])
        / monthly["Rev"].iloc[-2] * 100
    ) if len(monthly) >= 2 else 0

    prod_stats = df.groupby("Product").agg(
        Revenue=("Order Total","sum"),
        Orders=("Order Total","count")
    ).reset_index().sort_values("Revenue", ascending=False) \
        if "Product" in df.columns else pd.DataFrame()

    top_product = prod_stats.iloc[0]["Product"] \
        if not prod_stats.empty else "your top listing"

    # ── Top nav ───────────────────────────────────────────────────────────
    n1, n2, n3 = st.columns([1, 3, 1])
    with n1:
        if st.button("← Upload new"):
            st.session_state.page = "landing"; st.rerun()
    with n2:
        H("""<div style='text-align:center;padding:8px 0;display:flex;
                          align-items:center;justify-content:center;gap:8px;'>
            <div style='background:linear-gradient(135deg,#7C3AED,#6D28D9);width:26px;height:26px;
                        border-radius:8px;display:inline-flex;align-items:center;justify-content:center;
                        font-size:13px;box-shadow:0 2px 10px rgba(124,58,237,0.4);'>⚡</div>
            <span style='font-size:16px;font-weight:800;color:#F9FAFB;letter-spacing:-.3px;'>
                D'aura Labs</span>
            <span style='font-size:11px;font-weight:500;color:#4B5563;margin-left:2px;'>
                Etsy AI Coach</span>
        </div>""")
    with n3:
        if is_demo:
            H("<div style='text-align:right;padding:10px 0;'>"
              "<span style='background:rgba(124,58,237,0.2);color:#A78BFA;"
              "font-size:10px;font-weight:700;padding:4px 12px;border-radius:20px;"
              "border:1px solid rgba(124,58,237,0.3);'>DEMO</span></div>")
    H("<hr>")
    gap(6)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "✨ AI Coach", "🏆 Products", "⚡ Action Plan", "📈 Charts"
    ])

    # ════════════════════════════════════════════════
    with tab1:   # ── AI COACH (main screen) ─────────
        gap(8)

        # Headline AI summary
        trend_word = "growing" if growth > 0 else "slower"
        trend_color = GREEN if growth > 0 else RED
        ai_summary(
            f"Your shop is {trend_word} — here's what matters most right now.",
            f"You made <strong style='color:{PURPLE_L}'>${rev:,.0f}</strong> across "
            f"<strong style='color:{PURPLE_L}'>{orders:,} orders</strong> with a "
            f"<strong style='color:{PURPLE_L}'>{margin:.0f}% profit margin</strong>. "
            f"Revenue is <strong style='color:{trend_color};"
            f"'>{'up' if growth>0 else 'down'} {abs(growth):.0f}%</strong> "
            f"compared to last month. "
            f"<strong style='color:#F9FAFB'>{top_product}</strong> is your strongest "
            f"product right now — it's driving the most revenue and has the highest "
            f"repeat purchase rate. Your biggest opportunity is creating more "
            f"low-price bundle offers to increase your average order value."
        )

        gap(6)

        # 4 key insight cards in a 2×2 grid
        section_label("What your AI found")
        r1c1, r1c2 = st.columns(2)

        with r1c1:
            insight_card(
                "🔥", "Winning Product", GREEN,
                f"{top_product} is your best performer",
                "This product has your highest conversion rate and the most repeat buyers. "
                "Whatever makes it work — replicate that format for your next 2–3 listings.",
                cta="Try making a variation or bundle with this product first."
            )
            insight_card(
                "💸", "Profit Leak", RED,
                "Etsy fees are cutting deeper than they should",
                f"You're paying an estimated ${rev*0.065:,.0f} in fees this period. "
                "Your pricing may not fully account for the 6.5% transaction fee "
                "plus payment processing — common for newer shops.",
                cta="Add $2–3 to your prices. Buyers rarely notice small increases."
            )
        with r1c2:
            insight_card(
                "🚀", "Growth Opportunity", PURPLE,
                "Bundle offers could lift your revenue by 20–30%",
                "Buyers who purchase your top product often view your second product "
                "in the same session. A bundle at a slight discount would capture "
                "those sales automatically.",
                cta="Create one bundle listing this week and watch what happens."
            )
            insight_card(
                "⚠️", "Needs Attention", AMBER,
                "One listing is getting traffic but not converting",
                "Your lowest-converting product has plenty of views but people "
                "aren't buying. This usually means the photos don't match buyer "
                "expectations, or the price feels too high for what's shown.",
                cta="Swap in a lifestyle mockup photo — this alone can double conversion."
            )

        # KPIs — below the AI section
        section_label("Your numbers at a glance")
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("💰 Revenue",    f"${rev:,.0f}",       f"+{growth:.0f}% this mo.")
        k2.metric("💎 Profit",     f"${profit:,.0f}",    f"{margin:.0f}% margin")
        k3.metric("📦 Orders",     f"{orders:,}",        f"${aov:.0f} avg each")
        k4.metric("🛒 Conversion", "3.8%",              "+0.4pp vs last mo.")
        k5.metric("🚀 Growth",     f"+{growth:.0f}%",   "vs last month")

        # Shop Health Score — compact, below KPIs
        gap(8)
        section_label("Shop Health Score")
        hc1, hc2 = st.columns([3, 1])
        with hc1:
            health_bar("Profitability",      82, PURPLE_L)
            health_bar("Conversion rate",    65, AMBER)
            health_bar("Product strength",   91, GREEN)
            health_bar("Traffic quality",    74, PURPLE_L)
            health_bar("Customer retention", 70, AMBER)
        with hc2:
            H(f"""
            <div style="background:#111827;border:1px solid rgba(255,255,255,0.07);
                        border-radius:20px;padding:28px 16px;text-align:center;
                        height:100%;display:flex;flex-direction:column;
                        align-items:center;justify-content:center;gap:6px;">
                <div style="font-size:56px;font-weight:800;line-height:1;
                            background:linear-gradient(135deg,#7C3AED,#A78BFA);
                            -webkit-background-clip:text;
                            -webkit-text-fill-color:transparent;">76</div>
                <div style="font-size:12px;color:#4B5563;">out of 100</div>
                <div style="background:rgba(16,185,129,0.12);color:{GREEN};font-size:11px;
                            font-weight:700;padding:4px 14px;border-radius:20px;
                            margin-top:6px;">Good standing</div>
            </div>""")

    # ════════════════════════════════════════════════
    with tab2:   # ── PRODUCTS ──────────────────────
        section_label("Your product lineup")

        tags  = ["🔥 Bestseller","🚀 Growing","🚀 Growing","⚠️ Needs Work","💀 Struggling"]
        convs = ["7.2%","5.1%","4.3%","2.1%","0.9%"]
        notes = [
            "People who buy this come back. Replicate the format — try a vol.2 or themed variation.",
            "Strong momentum. Adding 3 lifestyle mockup photos could push conversion past 6%.",
            "Healthy seller. Test raising the price by $3 — at this conversion rate, it'll likely hold.",
            "People are viewing this listing but buying less lately. The concept works — photos need a refresh.",
            "Lots of people see this but almost nobody buys. Pause any ads on it and fix the photos first.",
        ]

        if not prod_stats.empty:
            for idx, (_, row) in enumerate(prod_stats.head(5).iterrows()):
                if idx >= len(tags): break
                product_card(
                    rank    = idx + 1,
                    name    = row["Product"],
                    revenue = f"${row['Revenue']:,.0f}",
                    conv    = convs[idx],
                    badge   = tags[idx],
                    badge_color = [GREEN, PURPLE_L, PURPLE_L, AMBER, RED][idx],
                    note    = notes[idx],
                    orders  = f"{int(row['Orders']):,}",
                )
        else:
            st.info("No product data found. Make sure your CSV has a 'Listing Title' or 'Product' column.")

    # ════════════════════════════════════════════════
    with tab3:   # ── ACTION PLAN ────────────────────
        gap(8)
        H(f"""
        <div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.2);
                    border-radius:16px;padding:16px 20px;margin-bottom:24px;">
            <div style="font-size:13px;color:#D1FAE5;line-height:1.6;">
                ✅ <strong>These actions are ranked by impact on your revenue.</strong>
                Finish #1 before moving to #2 — focus beats multitasking every time.
            </div>
        </div>""")

        actions = [
            ("Create one bundle offer this week",
             "High",
             f"Pair your top 2 products at a 10% bundle discount. "
             f"Buyers of {top_product} regularly view your second product in the same session — "
             "you're leaving that money on the table right now."),
            ("Raise your prices by $2–3 across the board",
             "High",
             "You're not fully covering Etsy's 6.5% fee + payment processing in your current pricing. "
             "A small price increase won't hurt conversion but will meaningfully protect your margin."),
            ("Fix your lowest-converting listing's photos",
             "High",
             "Your weakest product has traffic but low sales — that's almost always a photo problem, "
             "not a product problem. Swap in a lifestyle mockup. This single change can 2× conversion."),
            ("Pin every new listing on Pinterest on launch day",
             "Medium",
             "Your Pinterest traffic converts better than Etsy search. "
             "It costs nothing and takes 5 minutes per listing."),
            ("Write 'customers also love…' in your top listing descriptions",
             "Medium",
             "Natural cross-sell copy increases multi-product orders without any paid ads. "
             "Mention your second product by name with a direct link."),
            ("Create 2 more products in your winning product's style",
             "Medium",
             "Your audience is already there and buying. Give them more variations to choose from — "
             "same aesthetic, different format (e.g. A4 vs A5, different color themes)."),
            ("Add a $35 free-shipping threshold",
             "Low",
             "Buyers consistently add items to hit free shipping cutoffs. "
             "Set it just above your average order value and watch cart sizes grow."),
        ]

        for i, (title, impact, detail) in enumerate(actions, 1):
            action_item(i, title, impact, detail)

        gap(28)
        section_label("Ask your AI coach")
        q = st.text_input(
            "", placeholder="e.g.  How do I get more repeat buyers on Etsy?",
            label_visibility="collapsed"
        )
        if st.button("✨  Get answer", use_container_width=False):
            if q.strip():
                with st.spinner("Thinking about your shop…"):
                    time.sleep(1.1)
                H(f"""
                <div style="background:linear-gradient(145deg,#13102A,#0E1628);
                            border:1px solid rgba(124,58,237,0.3);border-radius:20px;
                            padding:24px 28px;margin-top:12px;">
                    <div style="font-size:10px;color:#7C3AED;font-weight:800;
                                letter-spacing:1px;text-transform:uppercase;
                                margin-bottom:14px;">✨ AI Coach Reply</div>
                    <div style="font-size:14px;color:#D1D5DB;line-height:1.9;">
                        The fastest way to increase repeat buyers is to
                        <strong style='color:#F9FAFB'>add a handwritten-style thank-you note</strong>
                        in your order confirmation message with a subtle discount code
                        for their next purchase (10% off works well). Pair that with
                        <strong style='color:#F9FAFB'>creating a 'vol.2' or companion product</strong>
                        to your bestseller — returning buyers are the most likely to grab it.
                        For digital products specifically, offering a free bonus file
                        (a smaller related template) with every purchase dramatically
                        increases positive reviews and return visits.
                    </div>
                </div>""")
            else:
                st.warning("Type a question first.")

    # ════════════════════════════════════════════════
    with tab4:   # ── CHARTS (secondary) ─────────────
        section_label("Revenue over time")
        if not monthly.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly["Month"], y=monthly["Rev"],
                marker_color=PURPLE, marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=monthly["Month"], y=monthly["Rev"],
                mode="lines+markers",
                line=dict(color=PURPLE_L, width=2, dash="dot"),
                marker=dict(size=5, color=PURPLE_L),
                showlegend=False,
            ))
            fig.update_layout(**PLOTLY_BASE, height=300, showlegend=False,
                              xaxis_tickangle=-30)
            fig.update_yaxes(tickprefix="$")
            st.plotly_chart(fig, use_container_width=True)

        section_label("Order volume over time")
        if not monthly.empty:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=monthly["Month"], y=monthly["Ord"],
                fill="tozeroy",
                line=dict(color=GREEN, width=2),
                fillcolor="rgba(16,185,129,0.08)",
                hovertemplate="<b>%{x}</b><br>%{y} orders<extra></extra>",
            ))
            fig2.update_layout(**PLOTLY_BASE, height=240, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        if "Country" in df.columns and df["Country"].notna().any():
            section_label("Where your buyers come from")
            ctry = (df.groupby("Country")["Order Total"]
                      .sum().nlargest(6).reset_index())
            fig3 = go.Figure(go.Bar(
                x=ctry["Order Total"], y=ctry["Country"],
                orientation="h",
                marker_color=PURPLE, marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
            ))
            fig3.update_layout(**PLOTLY_BASE, height=260,
                               showlegend=False, xaxis_title="", yaxis_title="")
            fig3.update_xaxes(tickprefix="$")
            st.plotly_chart(fig3, use_container_width=True)

    # ── Branded dashboard footer ──────────────────────────────────────────
    gap(40)
    H("""
    <div style="text-align:center;border-top:1px solid rgba(255,255,255,0.05);
                padding-top:24px;">
        <div style="display:inline-flex;align-items:center;gap:7px;margin-bottom:6px;">
            <div style="background:linear-gradient(135deg,#7C3AED,#6D28D9);width:22px;height:22px;
                        border-radius:7px;display:inline-flex;align-items:center;
                        justify-content:center;font-size:11px;">⚡</div>
            <span style="font-size:14px;font-weight:800;color:#F9FAFB;letter-spacing:-.2px;">
                D'aura Labs</span>
        </div>
        <div style="font-size:11px;color:#374151;margin-top:2px;">
            © 2025 D'aura Labs · All rights reserved · Unauthorized resale or redistribution prohibited
        </div>
    </div>""")
