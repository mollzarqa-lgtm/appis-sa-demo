# APPIS-SA - نظام الذكاء التكيفي التنبئي للأدوية
# نسخة متطورة مع AI Explanation ومحاكاة حية

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# إعدادات الصفحة
st.set_page_config(page_title="APPIS-SA", page_icon="📊", layout="wide")

# عنوان رئيسي
st.markdown("""
<div style='text-align: center;'>
    <h1>🧠 APPIS-SA</h1>
    <p style='color: #8a8f99; font-size: 1.2rem;'>Adaptive Predictive Pharma Intelligence System</p>
    <p style='color: #5a5f6e;'>يكشف الطلب الدوائي قبل 21 يوماً من بيانات الوصفات</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ============================================
# 1. اختيار السيناريو (Scenario Selection)
# ============================================
col_scenario1, col_scenario2 = st.columns([2, 1])

with col_scenario1:
    scenario = st.selectbox(
        "🎯 اختر الفئة العلاجية / Select Therapeutic Category",
        ["Respiratory (أمراض التنفس)", "Allergy (الحساسية)", "Flu (الإنفلونزا)", "Pain Management (إدارة الألم)"]
    )

with col_scenario2:
    st.metric("📊 نظام الكشف", "نشط", delta="مراقبة 24/7")

st.markdown("---")

# ============================================
# توليد البيانات حسب السيناريو المختار
# ============================================
@st.cache_data
def generate_data(scenario_type):
    """توليد بيانات محاكاة حسب الفئة العلاجية"""
    days = 60
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    # معاملات حسب الفئة
    if "Respiratory" in scenario_type:
        search_peak, otc_peak, rx_peak = 52, 45, 38
        search_pct, otc_pct, engagement_pct = 22, 15, 31
        lead_time = 21
    elif "Allergy" in scenario_type:
        search_peak, otc_peak, rx_peak = 48, 42, 36
        search_pct, otc_pct, engagement_pct = 18, 12, 28
        lead_time = 18
    elif "Flu" in scenario_type:
        search_peak, otc_peak, rx_peak = 58, 50, 42
        search_pct, otc_pct, engagement_pct = 28, 20, 35
        lead_time = 24
    else:  # Pain Management
        search_peak, otc_peak, rx_peak = 35, 32, 28
        search_pct, otc_pct, engagement_pct = 14, 10, 22
        lead_time = 15
    
    search = []
    otc = []
    rx = []
    for i in range(days):
        s = 20 + (search_peak - 20) * (1 - ((i-30)/30)**2) if 10 < i < 50 else 20 + np.random.normal(0, 2)
        o = 15 + (otc_peak - 15) * (1 - ((i-40)/25)**2) if 20 < i < 55 else 15 + np.random.normal(0, 2)
        r = 10 + (rx_peak - 10) * (1 - ((i-50)/20)**2) if 35 < i < 60 else 10 + np.random.normal(0, 2)
        search.append(max(5, min(100, s)))
        otc.append(max(5, min(100, o)))
        rx.append(max(5, min(100, r)))
    
    return dates, search, otc, rx, search_pct, otc_pct, engagement_pct, lead_time

dates, search, otc, rx, search_pct, otc_pct, engagement_pct, lead_time = generate_data(scenario)

# ============================================
# عرض المؤشرات
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📈 إشارة الطلب المبكر", f"+{search_pct}%", "↑ عن خط الأساس")

with col2:
    st.metric("🎯 نسبة الثقة", f"{87 + (search_pct - 15)//2}%", "تحقق متعدد المصادر")

with col3:
    st.metric("⏱️ مهلة الاكتشاف", f"{lead_time} يوم", "قبل بيانات الوصفات")

with col4:
    st.metric("🌍 التغطية الجغرافية", "48 ولاية", "الولايات المتحدة")

# ============================================
# 3. زر Simulate Live Detection (مطور)
# ============================================
st.markdown("---")

if st.button("🚀 Run Live Detection", type="primary", use_container_width=True):
    with st.spinner("🔍 Analyzing real-time behavioral signals..."):
        time.sleep(1.5)
        st.success("✅ Signal detected successfully")
        
        # ============================================
        # 1. AI Explanation - Model Insight
        # ============================================
        st.markdown("### 🧠 Model Insight")
        st.info(f"""
        **APPIS-SA detected a behavioral convergence pattern matching historical demand spikes for {scenario}.**\n\n
        **Key drivers:**
        - Early surge in symptom-related search queries (+{search_pct}%)
        - Correlated increase in OTC purchases (+{otc_pct}%)
        - Non-linear engagement acceleration across health platforms (+{engagement_pct}%)\n
        **Pattern similarity score:** {85 + (search_pct - 10)}% vs historical outbreaks
        **Recommendation:** Initiate supply chain alignment within 48 hours.
        """)
        
        # تخزين حالة الكشف
        st.session_state.detection_run = True
else:
    st.session_state.detection_run = False

# ============================================
# الرسم البياني
# ============================================
st.markdown("### 📊 Behavioral Convergence Timeline")

fig = go.Figure()

fig.add_trace(go.Scatter(x=dates, y=search, name="🔍 Search Behavior", 
                         line=dict(color="#00d4ff", width=2.5),
                         fill='tozeroy', fillcolor='rgba(0,212,255,0.1)'))

fig.add_trace(go.Scatter(x=dates, y=otc, name="💊 OTC Activity", 
                         line=dict(color="#ff6b6b", width=2.5),
                         fill='tozeroy', fillcolor='rgba(255,107,107,0.08)'))

fig.add_trace(go.Scatter(x=dates, y=rx, name="📋 Prescription Data (Traditional)", 
                         line=dict(color="#ffd93d", width=2.5, dash='dash')))

# إضافة خطوط توضيحية
detection_point = 32
fig.add_vline(x=dates[detection_point], line_dash="dot", line_color="#00d4ff",
              annotation_text="🟢 APPIS-SA Detection", annotation_position="top left")

fig.update_layout(
    template="plotly_dark",
    title=f"{scenario} - Signal Progression Over Time",
    xaxis_title="Date",
    yaxis_title="Signal Intensity",
    height=450,
    legend=dict(x=0, y=1)
)

st.plotly_chart(fig, use_container_width=True)

# ============================================
# تفاصيل الإشارات
# ============================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔍 Search Uplift", f"+{search_pct}%", "Condition-related queries")

with col2:
    st.metric("💊 OTC Uplift", f"+{otc_pct}%", "OTC category purchases")

with col3:
    st.metric("💬 Engagement Uplift", f"+{engagement_pct}%", "Forums & health platforms")

# ============================================
# تذييل
# ============================================
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: space-between; text-align: center;'>
    <div style='flex:1'>
        <span style='color: #00d4ff; font-size: 1.2rem;'>✓ Cross-validated</span>
    </div>
    <div style='flex:1'>
        <span style='color: #00d4ff; font-size: 1.2rem;'>✓ Temporal correlation</span>
    </div>
    <div style='flex:1'>
        <span style='color: #00d4ff; font-size: 1.2rem;'>✓ Historical backtest</span>
    </div>
</div>
<div style='text-align: center; padding: 16px; margin-top: 16px;'>
    <span style='color: #5a5f6e;'>APPIS-SA · Market Timing Advantage</span>
</div>
""", unsafe_allow_html=True)
