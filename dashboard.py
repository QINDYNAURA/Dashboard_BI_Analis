import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Dampak AI pada Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# 🎨 CUSTOM STYLE — THEMA ORANGE & KPI BOXING (SETELAN PREMIUM)
# ============================================================
st.markdown("""
    <style>
    /* Background Utama Krem-Oranye Soft */
    .stApp {
        background-color: #FDF6EC;
    }
    
    /* Background Sidebar Filter */
    [data-testid="stSidebar"] {
        background-color: #FAEBD7;
        border-right: 2px solid #F3D9B1;
    }
    
    /* Mempercantik Struktur Kotak Tab Navigasi */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F3E5D8;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        color: #D35400;
        border: 1px solid #E6A23C;
    }
    
    /* Efek Saat Tab Aktif Diklik */
    .stTabs [aria-selected="true"] {
        background-color: #E67E22 !important;
        color: white !important;
    }
    
    /* Warna Judul Utama H1 */
    h1 {
        color: #A04000 !important;
    }
    
    /* 📦 KUSTOMISASI KOTAK KPI BIAR DIKOTAK-KOTAKIN CONTRAST */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E67E22 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        box-shadow: 2px 4px 8px rgba(211, 84, 0, 0.1) !important;
    }
    
    /* Warna teks label KPI */
    [data-testid="stMetricLabel"] {
        color: #5D4037 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Warna teks nilai angka utama KPI */
    [data-testid="stMetricValue"] {
        color: #D35400 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('ai_student_final.csv')
    if 'AI_User_Segment' not in df.columns:
        df['AI_User_Segment'] = pd.cut(
            df['Weekly_GenAI_Hours'],
            bins=[-1, 5, 15, 40],
            labels=['Light', 'Moderate', 'Heavy']
        )
    if 'GPA_Gap' not in df.columns:
        df['GPA_Gap'] = df['Post_Semester_GPA'] - df['Pre_Semester_GPA']
    return df

df = load_data()

# ============================================================
# SIDEBAR — FILTER INTERAKTIF & IDENTITAS LU
# ============================================================
st.sidebar.header("🔧 Filter Analisis")
st.sidebar.markdown("---")

major_options = ['Semua'] + sorted(df['Major_Category'].dropna().unique().tolist())
selected_major = st.sidebar.selectbox("📚 Bidang Studi", major_options)

year_options = ['Semua'] + ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
selected_year = st.sidebar.selectbox("🎓 Jenjang Studi", year_options)

policy_options = ['Semua'] + sorted(df['Institutional_Policy'].dropna().unique().tolist())
selected_policy = st.sidebar.selectbox("🏛️ Kebijakan Kampus", policy_options)

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Dataset Info**")
st.sidebar.markdown(f"Total Records: **{len(df):,}**")
st.sidebar.markdown(f"Total Variabel: **{df.shape[1]}**")
st.sidebar.markdown("---")
# DI SINI TEMPAT NAMA LU SEKARANG, JIRR! RAPI DI AREA FILTER!
st.sidebar.markdown("👤 **Analis Data Dashboard:**")
st.sidebar.markdown("💡 **Qindy Naura**")
st.sidebar.markdown("*Divisi Riset & Kebijakan | Konsultan BI*")

# Jalankan Filter
df_filtered = df.copy()
if selected_major != 'Semua':
    df_filtered = df_filtered[df_filtered['Major_Category'] == selected_major]
if selected_year != 'Semua':
    df_filtered = df_filtered[df_filtered['Year_of_Study'] == selected_year]
if selected_policy != 'Semua':
    df_filtered = df_filtered[df_filtered['Institutional_Policy'] == selected_policy]

# ============================================================
# HEADER UTAMA
# ============================================================
st.title("🎓 Dashboard Analisis Dampak GenAI Terhadap Mahasiswa")
st.markdown("### Business Intelligence Platform | Divisi Riset & Kebijakan")
st.markdown("---")

# ============================================================
# KEY PERFORMANCE INDICATORS (KPI) — KOTAK TIMBUL
# ============================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📈 Rata-rata Post GPA", value=f"{df_filtered['Post_Semester_GPA'].mean():.3f}")
with col2:
    st.metric(label="🧠 Rata-rata Skill Retention", value=f"{df_filtered['Skill_Retention_Score'].mean():.2f}")
with col3:
    pct_burnout = (df_filtered['Burnout_Risk_Level'] == 'High').mean() * 100
    st.metric(label="🔥 High Burnout Risk", value=f"{pct_burnout:.1f}%")

st.markdown("---")

# ============================================================
# TAB NAVIGASI
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview Data", 
    "🤖 Dampak Ke GPA", 
    "🧠 Kesehatan Mental", 
    "📚 Retensi Ilmu", 
    "⚠️ Profil Risiko"
])

# TAB 1 — OVERVIEW
with tab1:
    st.subheader("Distribusi Profil Mahasiswa")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(df_filtered, names='Major_Category', title='Proporsi Mahasiswa per Jurusan', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.histogram(df_filtered, x='Year_of_Study', title='Jumlah Mahasiswa per Jenjang', color_discrete_sequence=['#E67E22'])
        st.plotly_chart(fig2, use_container_width=True)

# TAB 2 — DAMPAK AI
with tab2:
    st.subheader("Analisis Penggunaan AI vs Performa Nilai (GPA)")
    
    # BALIK KE ANALISIS BERBOBOT AWAL LU, JIRR!
    st.info("""
    📌 **Hasil Analisis PB1 — Intensitas AI vs Performa Akademik**
    - **Korelasi Pearson:** r = -0.0186 (Sangat Lemah, Negatif, Signifikan)
    - **Regresi Linear:** R² = 0.0003 → setiap +1 jam/minggu AI, GPA berubah -0.0011 poin
    - **Moderate User** memiliki rata-rata GPA tertinggi **(3.372)** dan GPA Gap terbesar **(+0.227)**
    - **Heavy User** justru memiliki GPA terendah **(3.320)** dan GPA Gap terkecil **(+0.173)**
    - 💡 **Insight:** Ada titik optimal penggunaan AI di 5–15 jam/minggu yang justru mendukung performa akademik secara maksimal.
    """)
    
    gpa_seg = df_filtered.groupby('AI_User_Segment', observed=True)['GPA_Gap'].mean().reset_index()
    fig3 = px.bar(gpa_seg, x='AI_User_Segment', y='GPA_Gap', title='Rata-rata Perubahan GPA (GPA Gap) Berdasarkan Segmen User',
                  color='AI_User_Segment', color_discrete_sequence=['#2ECC71', '#F1C40F', '#E74C3C'])
    st.plotly_chart(fig3, use_container_width=True)

# TAB 3 — KESEHATAN MENTAL
with tab3:
    st.subheader("Hubungan Kebijakan Kampus dengan Tingkat Stress")
    
    # BALIK KE ANALISIS BERBOBOT AWAL LU, JIRR!
    st.info("""
    📌 **Hasil Analisis PB3 — Kebijakan Institusi vs Performa & Burnout**
    - **Strictly_Ban** memiliki rata-rata GPA terendah **(3.333)** dan % High Burnout tertinggi **(29.8%)**
    - **Actively_Encouraged** dan **Allowed_With_Citation** memiliki GPA lebih tinggi **(3.353)**
    - **Chi-Square:** χ² = 153.15, p-value = 0.000 → distribusi burnout berbeda signifikan antar kebijakan
    - 💡 **Insight:** Kebijakan pelarangan AI secara total (Strict Ban) justru berkorelasi dengan tingkat burnout mahasiswa yang lebih tinggi.
    """)
    
    fig4 = px.histogram(df_filtered, x='Institutional_Policy', color='Burnout_Risk_Level', 
                        title='Tingkat Risiko Burnout Berdasarkan Kebijakan Kampus', barmode='group',
                        color_discrete_map={'Low': '#2ECC71', 'Medium': '#F1C40F', 'High': '#E74C3C'})
    st.plotly_chart(fig4, use_container_width=True)

# TAB 4 — RETENSI PENGETAHUAN
with tab4:
    st.subheader("Korelasi Ketergantungan AI dengan Daya Ingat")
    
    # BALIK KE ANALISIS BERBOBOT AWAL LU, JIRR!
    st.info("""
    📌 **Hasil Analisis PB2 — AI Dependency vs Skill Retention**
    - **Korelasi Pearson:** r = -0.0843 (Sangat Lemah, Negatif, Signifikan)
    - **Korelasi Spearman:** ρ = -0.0516 (Sangat Lemah, Negatif, Signifikan)
    - Skor dependency 1–3 memiliki rata-rata retention **75–76**, skor 8–10 turun ke **63–69**
    - 💡 **Insight:** Semakin tinggi ketergantungan mahasiswa pada tools AI, ada kecenderungan skor retensi pemahaman materi kuliahnya melemah.
    """)
    
    ret_dep = df_filtered.groupby('Perceived_AI_Dependency')['Skill_Retention_Score'].mean().reset_index()
    fig5 = px.line(ret_dep, x='Perceived_AI_Dependency', y='Skill_Retention_Score', title='Tren Penurunan Skill Retention Berdasarkan Skor Ketergantungan AI', markers=True)
    fig5.update_traces(line_color='#D35400')
    st.plotly_chart(fig5, use_container_width=True)

# TAB 5 — PROFIL RISIKO
with tab5:
    st.subheader("Rekomendasi Profil Risiko (Hasil Model Pohon Keputusan)")
    
    # BALIK KE ANALISIS BERBOBOT AWAL LU, JIRR!
    st.info("""
    📌 **Hasil Analisis PB5 — Profiling Burnout Risk (Decision Tree)**
    - **Akurasi Model:** 52% | Feature terpenting: **Weekly_GenAI_Hours (88.6%)**
    - **Low Burnout (2.484 mhs):** Rata-rata 1.87 jam AI/minggu, Light User, mayoritas Business, Junior
    - **Medium Burnout (5.582 mhs):** Rata-rata 6.59 jam AI/minggu, Moderate User, mayoritas STEM, Senior
    - **High Burnout (1.933 mhs):** Rata-rata 22.34 jam AI/minggu, Heavy User, mayoritas STEM, Freshman
    - 💡 **Insight:** Weekly GenAI Hours adalah prediktor burnout terkuat. Mahasiswa dalam kategori Heavy User memiliki risiko mengalami stress/burnout akademis 3x lipat lebih tinggi.
    """)
    
    if os.path.exists('pb5_decision_tree_final_kerangka.png'):
        img = Image.open('pb5_decision_tree_final_kerangka.png')
        st.image(img, caption='Model Decision Tree - Klasifikasi Risiko Burnout', use_container_width=True)
    else:
        st.warning("⚠️ File pb5_decision_tree_final_kerangka.png belum di-upload di GitHub utama.")
