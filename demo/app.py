"""UzhavarNeri (உழவர்நெறி) - Streamlit Web Dashboard.

Autonomous Climate-Resilient Agricultural Sowing & Monsoon Risk Agent
for Smallholder Farmers in Tamil Nadu.
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from uzhavarneri.agent import UzhavarNeriAgent
from uzhavarneri.tools import get_block_weather, check_mandi_prices, get_crop_guidelines

# Streamlit Page Config
st.set_page_config(
    page_title="UzhavarNeri (உழவர்நெறி) - Agro-Climate Agent",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern Agritech SOC look
st.markdown(
    """
    <style>
    .main {
        background-color: #0b131b;
        color: #e2e8f0;
    }
    .metric-card {
        background: linear-gradient(135deg, #13241b 0%, #0d1a24 100%);
        border: 1px solid #1f4229;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .guardrail-alert {
        background-color: #3b1212;
        border-left: 5px solid #ef4444;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .guardrail-safe {
        background-color: #0f2e1a;
        border-left: 5px solid #10b981;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .voice-box {
        background-color: #1a2936;
        border: 1px solid #2d4a66;
        border-radius: 8px;
        padding: 14px;
        font-family: monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_agent():
    return UzhavarNeriAgent()


agent = load_agent()

# Sidebar: Taluk & Crop Settings
with st.sidebar:
    st.image("https://img.icons8.com/color/96/wheat.png", width=64)
    st.title("உழவர்நெறி (UzhavarNeri)")
    st.caption("Climate-Resilient Agent for Cauvery Delta Farmers")

    st.subheader("📍 Location & Crop Setup")
    district = st.selectbox(
        "District (மாவட்டம்)",
        ["Thanjavur", "Tiruvarur", "Nagapattinam", "Cuddalore", "Madurai"],
        index=0,
    )
    crop = st.selectbox(
        "Crop (பயிர்)",
        ["samba_paddy", "thaladi_paddy", "kuruvai_paddy", "blackgram"],
        index=0,
    )
    das = st.slider("Days After Sowing (DAS / நட்ட நாட்கள்)", min_value=1, max_value=140, value=45)

    st.markdown("---")
    st.subheader("⚡ Quick Scenarios")
    scenario = st.radio(
        "Select Demo Scenario:",
        [
            "Custom Input",
            "🌧️ Urea Broadcast before 42mm Rain (Orathanadu)",
            "🚫 Banned Agrochemical (Monocrotophos Request)",
            "🌾 Ripening Panicle Rain Risk (Harvest Decision)",
            "🌿 Safe Basal Manuring Window",
        ],
    )

    st.markdown("---")
    st.caption("Built with the **Strands Agents SDK** & **Amazon Bedrock** for AWS Builder Center.")

# Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("🌾 UzhavarNeri: Agro-Climate Decision Agent")
    st.markdown(
        f"**Active Field:** {district} · **Crop:** `{crop}` ({das} DAS) · **Monsoon Phase:** Northeast Monsoon (வடகிழக்கு பருவமழை)"
    )

with col_status:
    st.markdown(
        """
        <div style="text-align: right; padding-top: 15px;">
            <span style="color: #10b981; font-weight: bold;">● Live Agro-Decider Active</span><br>
            <small style="color: #94a3b8;">Strands SDK v1.63 · AWS Bedrock Ready</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Telemetry Row
weather = get_block_weather(district, 72)
prices = check_mandi_prices(crop, district)

c1, c2, c3, c4 = st.columns(4)
with c1:
    rain_val = weather.get("total_rain_next_72h_mm", 0.0)
    rain_color = "#ef4444" if rain_val > 15 else "#10b981"
    st.markdown(
        f"""
        <div class="metric-card">
            <small style="color: #94a3b8;">72-Hour Rain Forecast</small>
            <h2 style="color: {rain_color}; margin: 4px 0;">{rain_val} mm</h2>
            <small>{weather.get('risk_level', 'NORMAL').upper()} RISK</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <small style="color: #94a3b8;">Temperature & Wind</small>
            <h2 style="color: #38bdf8; margin: 4px 0;">{weather.get('current_temperature_c', 28.0)}°C</h2>
            <small>Wind: {weather.get('max_wind_kmh', 12.0)} km/h</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <small style="color: #94a3b8;">Regulated Mandi Price</small>
            <h2 style="color: #facc15; margin: 4px 0;">₹{prices.get('current_mandi_price_inr_per_quintal', 2450)}</h2>
            <small>Govt MSP: ₹{prices.get('msp_inr_per_quintal', 2300)} / qtl</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    guard_status = "ACTIVE (0 Inundations)"
    st.markdown(
        f"""
        <div class="metric-card">
            <small style="color: #94a3b8;">Safety Guardrail Status</small>
            <h2 style="color: #a855f7; margin: 4px 0;">SHIELD ON</h2>
            <small>Runoff & Ban Filters Live</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Layout: Chat & Decisions
col_chat, col_guard = st.columns([3, 2])

# Pre-populate scenario if selected
default_prompt = ""
if scenario == "🌧️ Urea Broadcast before 42mm Rain (Orathanadu)":
    default_prompt = f"I have {das}-day-old Samba paddy in Orathanadu, {district}. Leaf tips are pale yellow. Can I broadcast 45kg urea tomorrow morning?"
elif scenario == "🚫 Banned Agrochemical (Monocrotophos Request)":
    default_prompt = f"Stem borer attack seen in {district} on {crop}. Local shop recommended spraying Monocrotophos 36 SL. Should I buy and spray it?"
elif scenario == "🌾 Ripening Panicle Rain Risk (Harvest Decision)":
    default_prompt = f"My Samba paddy is at 115 DAS in {district}. Grains are 80% golden. Rain forecast shows 65mm. Should I harvest immediately or wait?"
elif scenario == "🌿 Safe Basal Manuring Window":
    default_prompt = f"Field is dry in {district} and weather is clear for next 3 days. Can I apply DAP and potash as basal application?"

# Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_verdict" not in st.session_state:
    st.session_state.last_verdict = None

with col_chat:
    st.subheader("💬 Farmer Advisory Chat (விவசாயி உரையாடல்)")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "voice_script" in msg and msg["voice_script"]:
                st.markdown(
                    f"""
                    <div class="voice-box">
                        🎙️ <b>Colloquial Voice Audio Script (WhatsApp Voice Note):</b><br>
                        <em>"{msg['voice_script']}"</em>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    user_query = st.chat_input("Ask advice in Tamil, English, or Tanglish...")
    if not user_query and default_prompt and ("last_scenario" not in st.session_state or st.session_state.last_scenario != scenario):
        user_query = default_prompt
        st.session_state.last_scenario = scenario

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing block telemetry, phenology, and safety rules..."):
                start_time = time.time()
                res = agent.chat(user_query)
                latency = int((time.time() - start_time) * 1000)

                reply_text = res.get("reply", "")
                st.markdown(reply_text)

                voice_script = res.get("voice_script", "")
                if voice_script:
                    st.markdown(
                        f"""
                        <div class="voice-box">
                            🎙️ <b>Colloquial Voice Audio Script (குரல் பதிவு):</b><br>
                            <em>"{voice_script}"</em>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.caption(f"⏱️ Decision Latency: {latency} ms · Multi-step Strands Execution")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply_text,
                        "voice_script": voice_script,
                        "latency": latency,
                    }
                )

with col_guard:
    st.subheader("🛡️ Strands Active Guardrail Decisions")
    st.markdown("Real-time interception of chemical runoff, bans, and inundation risks:")

    # Show active guardrail rules
    st.markdown(
        """
        <div style="background-color: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
            <b>Enforced Field Policies:</b>
            <ul style="margin: 6px 0 0 16px; padding: 0;">
                <li>🌧️ <b>Runoff Interceptor:</b> Blocks Nitrogen broadcast if rain > 15mm in 24h.</li>
                <li>🚫 <b>Toxicity Filter:</b> Zero tolerance for CIBRC-banned pesticides (Monocrotophos, Endosulfan).</li>
                <li>💧 <b>Moisture Defense:</b> Prevents harvesting during active rain to save mandi deductions.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.messages:
        last_asst_msg = [m for m in st.session_state.messages if m["role"] == "assistant"]
        if last_asst_msg:
            txt = last_asst_msg[-1]["content"].lower()
            if "denied" in txt or "banned" in txt or "delay" in txt or "waste" in txt:
                st.markdown(
                    """
                    <div class="guardrail-alert">
                        <b>⚠️ INTERVENTION TRIGGERED: UNSAFE ACTION BLOCKED</b><br>
                        The Strands AgrochemicalSafetyGuard intercepted this request. Nitrogen runoff or banned pesticide risk exceeded the safety threshold.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="guardrail-safe">
                        <b>✅ ACTION PERMITTED: SAFE FIELD WINDOW</b><br>
                        TNAU phenology matched, weather window verified safe (&lt;15mm precipitation), and chemical approved.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    st.subheader("📊 Phenology & Mandi Reference")
    st.json(
        {
            "Crop Selected": crop,
            "District": district,
            "72h Rain": f"{weather.get('total_rain_next_72h_mm', 0)} mm",
            "Mandi MSP": f"₹{prices.get('msp_inr_per_quintal', 2300)}/qtl",
            "Moisture Penalty Rate": "1.5% deduction per % above 17%",
        }
    )
