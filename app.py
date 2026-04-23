# APPIS-SA - نظام الذكاء التكيفي التنبئي للأدوية
# عرض توضيحي للمستثمرين

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="APPIS-SA", page_icon="📊", layout="wide")

st.markdown("""
<div style='text-align: center;'>
    <h1>APPIS-SA</h1>
    <p style='color: #8a8f99;'>نظام الذكاء التكيفي التنبئي للأدوية</p>
    <p style='color: #5a5f6e;'>يكشف الطلب الدوائي قبل 21 يوماً من بيانات الوصفات</p>
</div>
<hr>
""", unsafe_allow_html=True)

@st.cache_data
def generate_data():
    days = 60
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    search = []
    otc = []
    rx = []
    for i in range(days):
        search.append(20 + 30 * (1 - ((i-30)/30)**2) if 10 < i < 50 else 20 + np.random.normal(0, 3))
        otc.append(15 + 25 * (1 - ((i-40)/25)**2) if 20 < i < 55 else 15 + np.random.normal(0, 3))
        rx.append(10 + 20 * (1 - ((i-50)/20)**2) if 35 < i < 60 else 10 + np.random.normal(0, 2))
    return dates, search, otc, rx

dates, search, otc, rx = generate_data()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("📈 إشارة الطلب المبكر", "+18%")
with col2: st.metric("🎯 نسبة الثقة", "87%")
with col3: st.metric("⏱️ مهلة الاكتشاف", "21 يوم")
with col4: st.metric("🌍 التغطية الجغرافية", "48 ولاية")

if st.button("🚀 تشغيل نظام الكشف", type="primary", use_container_width=True):
    st.success("""
    ⚠️ **تم اكتشاف طلب ناشئ!**
    - الفئة: أمراض الجهاز التنفسي
    - تسارع الطلب: +18%
    - الإجراء: بدء تخصيص المخزون
    """)

fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=search, name="🔍 سلوك البحث", line=dict(color="#00d4ff", width=2)))
fig.add_trace(go.Scatter(x=dates, y=otc, name="💊 نشاط OTC", line=dict(color="#ff6b6b", width=2)))
fig.add_trace(go.Scatter(x=dates, y=rx, name="📋 بيانات الوصفات", line=dict(color="#ffd93d", width=2, dash='dash')))
fig.update_layout(template="plotly_dark", title="التقارب السلوكي - يظهر البحث والOTC الطلب قبل 2-3 أسابيع", height=400)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1: st.metric("🔍 زيادة البحث", "+22%")
with col2: st.metric("💊 زيادة OTC", "+15%")
with col3: st.metric("💬 تفاعل المرضى", "+31%")

st.markdown("---")
st.markdown("<p style='text-align: center;'>APPIS-SA · ميزة توقيت السوق</p>", unsafe_allow_html=True)