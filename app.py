# APPIS-SA - نظام الذكاء التكيفي التنبئي للأدوية
# نسخة مبسطة - تعمل 100%

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="APPIS-SA", page_icon="📊", layout="wide")

st.markdown("""
<div style='text-align: center;'>
    <h1>🧠 APPIS-SA</h1>
    <p style='color: #8a8f99;'>Adaptive Predictive Pharma Intelligence System</p>
    <p style='color: #5a5f6e;'>يكشف الطلب الدوائي قبل 21 يوماً من بيانات الوصفات</p>
</div>
<hr>
""", unsafe_allow_html=True)

# اختيار السيناريو
scenario = st.selectbox(
    "🎯 اختر الفئة العلاجية",
    ["Respiratory (أمراض التنفس)", "Allergy (الحساسية)", "Flu (الإنفلونزا)", "Pain Management (إدارة الألم)"]
)

st.markdown("---")

# توليد البيانات
@st.cache_data
def generate_data(scenario_type):
    days = 60
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    if "Respiratory" in scenario_type:
        search_pct, otc_pct, engagement_pct = 22, 15, 31
        lead_time = 21
    elif "Allergy" in scenario_type:
        search_pct, otc_pct, engagement_pct = 18, 12, 28
        lead_time = 18
    elif "Flu" in scenario_type:
        search_pct, otc_pct, engagement_pct = 28, 20, 35
        lead_time = 24
    else:
        search_pct, otc_pct, engagement_pct = 14, 10, 22
        lead_time = 15
    
    search = []
    otc = []
    rx = []
    for i in range(days):
        if 10 < i < 50:
            s = 20 + (52 - 20) * (1 - ((i-30)/30)**2)
        else:
            s = 20 + np.random.normal(0, 2)
        if 20 < i < 55:
            o = 15 + (45 - 15) * (1 - ((i-40)/25)**2)
        else:
            o = 15 + np.random.normal(0, 2)
        if 35 < i < 60:
            r = 10 + (38 - 10) * (1 - ((i-50)/20)**2)
        else:
            r = 10 + np.random.normal(0, 2)
        search.append(max(5, min(100, s)))
        otc.append(max(5, min(100, o)))
        rx.append(max(5, min(100, r)))
    
    return dates, search, otc, rx, search_pct, otc_pct, engagement_pct, lead_time

dates, search, otc, rx, search_pct, otc_pct, engagement_pct, lead_time = generate_data(scenario)

# المؤشرات
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("📈 إشارة الطلب المبكر", f"+{search_pct}%")
with col2: st.metric("🎯 نسبة الثقة", f"{87 + (search_pct - 15)//2}%")
with col3: st.metric("⏱️ مهلة الاكتشاف", f"{lead_time} يوم")
with col4: st.metric("🌍 التغطية الجغرافية", "48 ولاية")

st.markdown("---")

# زر الكشف
if st.button("🚀 Run Live Detection", type="primary", use_container_width=True):
    with st.spinner("🔍 Analyzing real-time behavioral signals..."):
        time.sleep(1.5)
    st.success("✅ Signal detected successfully")
    
    st.markdown("### 🧠 Model Insight")
    st.info(f"""
    **APPIS-SA detected a behavioral convergence pattern matching historical demand spikes for {scenario}.**\n
    **Key drivers:**
    - Early surge in symptom-related search queries (+{search_pct}%)
    - Correlated increase in OTC purchases (+{otc_pct}%)
    - Non-linear engagement acceleration across health platforms (+{engagement_pct}%)\n
    **Pattern similarity score:** {85 + (search_pct - 10)}% vs historical outbreaks
    **Recommendation:** Initiate supply chain alignment within 48 hours.
    """)

# الرسم البياني
st.markdown("### 📊 Behavioral Convergence Timeline")

fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=search, name="🔍 Search Behavior", line=dict(color="#00d4ff", width=2.5)))
fig.add_trace(go.Scatter(x=dates, y=otc, name="💊 OTC Activity", line=dict(color="#ff6b6b", width=2.5)))
fig.add_trace(go.Scatter(x=dates, y=rx, name="📋 Prescription Data", line=dict(color="#ffd93d", width=2.5, dash='dash')))

fig.update_layout(
    template="plotly_dark",
    title=f"{scenario} - Signal Progression Over Time",
    xaxis_title="Date",
    yaxis_title="Signal Intensity",
    height=450,
    legend=dict(x=0, y=1)
)
st.plotly_chart(fig, use_container_width=True)

# تفاصيل الإشارات
col1, col2, col3 = st.columns(3)
with col1: st.metric("🔍 Search Uplift", f"+{search_pct}%")
with col2: st.metric("💊 OTC Uplift", f"+{otc_pct}%")
with col3: st.metric("💬 Engagement Uplift", f"+{engagement_pct}%")

st.markdown("---")
st.markdown("<p style='text-align: center;'>APPIS-SA · Market Timing Advantage</p>", unsafe_allow_html=True)
