import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# ============================================================
# KONFIGURASI HALAMAN (Simpel & Bersih)
# ============================================================
st.set_page_config(
    page_title="Dampak AI pada Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

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
# SIDEBAR — FILTER UTAMA
# ============================================================
st.sidebar.header("🔧 Filter Analisis")
st.sidebar.markdown("---")

major_options = ['Semua'] + sorted(df['Major_Category'].dropna().unique().tolist())
selected_major = st.sidebar.selectbox("📚 Bidang Studi", major_options)

year_options = ['Semua'] + ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
selected_year = st.sidebar.selectbox("🎓 Jenjang Studi", year_options)

policy_options = ['Semua'] + sorted(df['Institutional_Policy'].dropna().unique().tolist())
selected_policy = st.sidebar.selectbox("🏛️ Kebijakan Kampus", policy_options)

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
st.markdown("Oleh: **Qindy Naura** | Tugas Akhir BI & Analisis Data")
st.markdown("---")

# ============================================================
# KEY METRICS (KPI)
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
# TAB NAVIGASI (Hanya 5 Tab Sesuai Pertanyaan Bisnis)
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
        # VISUALISASI 1: Pie Jurusan
        fig1 = px.pie(df_filtered, names='Major_Category', title='Proporsi Mahasiswa per Jurusan', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        # VISUALISASI 2: Bar Angkatan
        fig2 = px.histogram(df_filtered, x='Year_of_Study', title='Jumlah Mahasiswa per Jenjang', color_discrete_sequence=['#4A90E2'])
        st.plotly_chart(fig2, use_container_width=True)

# TAB 2 — DAMPAK AI
with tab2:
    st.subheader("Analisis Penggunaan AI vs Performa Nilai (GPA)")
    st.write("Melihat apakah durasi penggunaan GenAI per minggu memengaruhi naik/turunnya IPK mahasiswa.")
    
    # VISUALISASI 3: Bar Segmen AI vs GPA Gap
    gpa_seg = df_filtered.groupby('AI_User_Segment', observed=True)['GPA_Gap'].mean().reset_index()
    fig3 = px.bar(gpa_seg, x='AI_User_Segment', y='GPA_Gap', title='Rata-rata Perubahan GPA (GPA Gap) Berdasarkan Segmen User',
                  color='AI_User_Segment', color_discrete_sequence=['#2ECC71', '#F1C40F', '#E74C3C'])
    st.plotly_chart(fig3, use_container_width=True)
    st.info("💡 **Insight:** Pengguna tingkat 'Moderate' (5-15 jam/minggu) menunjukkan tren kenaikan GPA yang paling optimal dibanding pengguna 'Heavy'.")

# TAB 3 — KESEHATAN MENTAL
with tab3:
    st.subheader("Hubungan Kebijakan Kampus dengan Tingkat Stress")
    
    # VISUALISASI 4: Bar Kebijakan vs Burnout
    fig4 = px.histogram(df_filtered, x='Institutional_Policy', color='Burnout_Risk_Level', 
                        title='Tingkat Risiko Burnout Berdasarkan Kebijakan Kampus', barmode='group',
                        color_discrete_map={'Low': '#2ECC71', 'Medium': '#F1C40F', 'High': '#E74C3C'})
    st.plotly_chart(fig4, use_container_width=True)
    st.info("💡 **Insight:** Kampus yang menerapkan 'Strict Ban' (pelarangan total) justru mencatat proporsi mahasiswa dengan High Burnout Risk paling tinggi.")

# TAB 4 — RETENSI PENGETAHUAN
with tab4:
    st.subheader("Korelasi Ketergantungan AI dengan Daya Ingat")
    
    # VISUALISASI 5: Line Chart AI Dependency vs Skill Retention
    ret_dep = df_filtered.groupby('Perceived_AI_Dependency')['Skill_Retention_Score'].mean().reset_index()
    fig5 = px.line(ret_dep, x='Perceived_AI_Dependency', y='Skill_Retention_Score', title='Tren Penurunan Skill Retention Berdasarkan Skor Ketergantungan AI', markers=True)
    fig5.update_traces(line_color='#E67E22')
    st.plotly_chart(fig5, use_container_width=True)
    st.info("💡 **Insight:** Grafik menunjukkan tren menurun. Semakin tinggi skor ketergantungan mahasiswa pada AI, ada kecenderungan skor retensi pemahaman materi kuliahnya melemah.")

# TAB 5 — PROFIL RISIKO
with tab5:
    st.subheader("Rekomendasi Profil Risiko (Hasil Model Pohon Keputusan)")
    st.write("Segmentasi kritis untuk mendeteksi mahasiswa yang rentan mengalami burnout akibat over-use GenAI.")
    
    # Menampilkan Gambar Decision Tree Utama Lu
    if os.path.exists('pb5_decision_tree_final_kerangka.png'):
        img = Image.open('pb5_decision_tree_final_kerangka.png')
        st.image(img, caption='Model Decision Tree - Klasifikasi Risiko Burnout', use_container_width=True)
    else:
        st.warning("⚠️ File pb5_decision_tree_final_kerangka.png belum di-upload di GitHub utama.")
