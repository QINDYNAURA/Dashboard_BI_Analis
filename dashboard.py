import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

# ============================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ============================================================
st.set_page_config(
    page_title="Dashboard BI - Dampak GenAI",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# 2. 🎨 CUSTOM CSS GLOBAL — TEMA KREM-ORANYE & KONTRAS TEKS
# ============================================================
st.markdown("""
    <style>
    /* Background Utama Aplikasi (Krem-Oranye Soft) */
    .stApp {
        background-color: #FDF6EC;
    }
    
    /* Header Streamlit Ikut Warna Krem Dasar */
    [data-testid="stHeader"] {
        background-color: #FDF6EC !important;
    }
    
    /* Komponen Teks Utama */
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #2C1A11 !important;
        opacity: 1 !important;
    }
    
    /* Pengaturan Komponen Blockquote (Key Insight) agar Kontras Tinggi */
    blockquote {
        background-color: #F3E5D8 !important; 
        border-left: 5px solid #E67E22 !important; 
        padding: 15px 20px !important;
        margin: 15px 0 !important;
        border-radius: 4px !important;
    }
    blockquote p, blockquote li, blockquote span {
        color: #2C1A11 !important; 
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    
    /* Pengaturan Tabel Standar Luar (st.table) */
    table {
        color: #2C1A11 !important;
        width: 100% !important;
        border-collapse: collapse !important;
    }
    th {
        background-color: #E67E22 !important;
        color: #FFFFFF !important; 
        font-weight: bold !important;
        padding: 10px !important;
    }
    td {
        color: #2C1A11 !important; 
        background-color: #FFFFFF !important;
        padding: 10px !important;
        border: 1px solid #F3E5D8 !important;
    }
    
    /* Isolasi CSS Spesifik Khusus Tabel Dalam Expander Tab 3 */
    div[data-testid="stExpander"] table {
        background-color: #FFFFFF !important;
        color: #2C1A11 !important;
    }
    div[data-testid="stExpander"] th {
        background-color: #E67E22 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    div[data-testid="stExpander"] td {
        background-color: #FFFFFF !important;
        color: #2C1A11 !important;
    }
    
    /* Background Sidebar Filter */
    [data-testid="stSidebar"] {
        background-color: #FAEBD7;
        border-right: 2px solid #F3D9B1;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #2C1A11 !important;
    }
    
    /* Mengubah Kotak Dropdown Menu di Sidebar */
    div[data-baseweb="select"] > div {
        background-color: #E67E22 !important;
        border: 1px solid #D35400 !important;
    }
    
    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }
    
    /* Struktur Kotak Tab Navigasi */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F3E5D8;
        padding: 8px;
        border-radius: 12px;
    }
    
    /* Paksa Tulisan Tab Menjadi Hitam Pekat */
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        color: #2C1A11 !important;
        border: 1px solid #E6A23C;
    }
    
    /* Efek Saat Tab Aktif Diklik */
    .stTabs [aria-selected="true"] {
        background-color: #E67E22 !important;
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] span {
        color: white !important;
    }
    
    /* Kotak KPI Meter */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E67E22 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        box-shadow: 2px 4px 8px rgba(211, 84, 0, 0.1) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #5D4037 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #D35400 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 3. DATA ACQUISITION & PREPROCESSING
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
# 4. SIDEBAR PANEL — CONTROL INTERAKTIF
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
st.sidebar.markdown("👤 **Analis Data Dashboard:**")
st.sidebar.markdown("💡 **Qindy Naura**")

# Filter logic untuk data terikat
df_filtered = df.copy()
if selected_major != 'Semua':
    df_filtered = df_filtered[df_filtered['Major_Category'] == selected_major]
if selected_year != 'Semua':
    df_filtered = df_filtered[df_filtered['Year_of_Study'] == selected_year]
if selected_policy != 'Semua':
    df_filtered = df_filtered[df_filtered['Institutional_Policy'] == selected_policy]

# ============================================================
# 5. ENTERPRISE HEADER
# ============================================================
st.title("🎓 Dashboard Analisis Dampak GenAI Terhadap Mahasiswa")
st.markdown("### Business Intelligence Platform")
st.markdown("---")

# ============================================================
# 6. BANNER UTAMA / KEY PERFORMANCE INDICATORS (KPI)
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
# 7. VISUALIZATION STANDARD ENVIRONMENT (PLOTLY LAYOUT)
# ============================================================
def apply_warm_layout(fig):
    text_color = '#2C1A11'
    fig.update_layout(
        template='none', 
        plot_bgcolor='rgba(211, 84, 0, 0.13)',  
        paper_bgcolor='rgba(211, 84, 0, 0.13)', 
        margin=dict(l=70, r=40, t=60, b=100),
        font=dict(color=text_color, size=12),
        title=dict(font=dict(color=text_color, size=14, family="Arial", weight="bold")),
        legend=dict(font=dict(color=text_color), title=dict(font=dict(color=text_color))),
        hoverlabel=dict(bgcolor='#FFFFFF', font_color=text_color, font_size=12)
    )
    try:
        fig.update_xaxes(
            showgrid=True, gridcolor='rgba(211, 84, 0, 0.08)', 
            tickfont=dict(color=text_color, size=11), 
            titlefont=dict(color=text_color, size=12, weight="bold"), 
            title_standoff=20, linecolor=text_color, ticks="outside"
        )
        fig.update_yaxes(
            showgrid=True, gridcolor='rgba(211, 84, 0, 0.08)', 
            tickfont=dict(color=text_color, size=11), 
            titlefont=dict(color=text_color, size=12, weight="bold"), 
            title_standoff=15, linecolor=text_color, ticks="outside"
        )
    except Exception:
        pass
    return fig

# ============================================================
# 8. SISTEM TAB PANEL MULTI-DIMENSI
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview Data", 
    "🤖 Dampak Ke GPA", 
    "🧠 Kesehatan Mental", 
    "📚 Retensi Ilmu", 
    "⚠️ Profil Risiko"
])

# --- TAB 1: OVERVIEW DATA ---
with tab1:
    st.markdown("### 📊 Overview Distribusi Populasi Mahasiswa (Proporsi %)")
    df_major_chart = df.copy()
    df_year_chart = df[df['Major_Category'] == selected_major] if selected_major != 'Semua' else df.copy()
    
    df_policy_chart = df.copy()
    if selected_major != 'Semua':
        df_policy_chart = df_policy_chart[df_policy_chart['Major_Category'] == selected_major]
    if selected_year != 'Semua':
        df_policy_chart = df_policy_chart[df_policy_chart['Year_of_Study'] == selected_year]

    col_ov1, col_ov2, col_ov3 = st.columns(3)
    with col_ov1:
        fig1 = px.pie(df_major_chart, names='Major_Category', title='Distribusi per Bidang Studi', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig1 = apply_warm_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_ov2:
        year_pct = df_year_chart['Year_of_Study'].value_counts(normalize=True).reset_index()
        year_pct.columns = ['Year_of_Study', 'Persentase']
        year_pct['Persentase'] = year_pct['Persentase'] * 100
        fig2 = px.bar(year_pct, x='Year_of_Study', y='Persentase', title='Distribusi per Jenjang Studi (%)', color_discrete_sequence=['#E67E22'],
                      category_orders={"Year_of_Study": ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]})
        fig2.update_yaxes(ticksuffix="%")
        fig2 = apply_warm_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        
    with col_ov3:
        policy_pct = df_policy_chart['Institutional_Policy'].value_counts(normalize=True).reset_index()
        policy_pct.columns = ['Institutional_Policy', 'Persentase']
        policy_pct['Persentase'] = policy_pct['Persentase'] * 100
        fig2_b = px.bar(policy_pct, x='Institutional_Policy', y='Persentase', title='Distribusi Kebijakan Institusi (%)', color_discrete_sequence=['#F1C40F'])
        fig2_b.update_yaxes(ticksuffix="%")
        fig2_b = apply_warm_layout(fig2_b)
        st.plotly_chart(fig2_b, use_container_width=True)

# --- TAB 2: DAMPAK KE GPA ---
with tab2:
    st.markdown("### Analisis Penggunaan AI vs Performa Nilai (GPA)")
    st.info("""
    📌 **Hasil Analisis PB1 — Intensitas AI vs Performa Academic**
    * Moderate User memiliki rata-rata GPA tertinggi (3.372) dan GPA Gap terbesar (+0.227).
    * Heavy User memiliki rata-rata GPA terendah (3.320) dan GPA Gap terkecil (+0.173).
    """)
    col1, col2 = st.columns(2)
    with col1:
        gpa_seg = df_filtered.groupby('AI_User_Segment', observed=True)['GPA_Gap'].mean().reset_index()
        fig3_1 = px.bar(gpa_seg, x='AI_User_Segment', y='GPA_Gap', title='Rata-rata Perubahan GPA (GPA Gap) per Segmen',
                        color='AI_User_Segment', color_discrete_map={'Light': '#2ECC71', 'Moderate': '#F1C40F', 'Heavy': '#E74C3C'},
                        category_orders={"AI_User_Segment": ["Light", "Moderate", "Heavy"]})
        fig3_1 = apply_warm_layout(fig3_1)
        st.plotly_chart(fig3_1, use_container_width=True)
    with col2:
        fig3_2 = px.scatter(df_filtered.sample(n=1000 if len(df_filtered)>1000 else len(df_filtered)), 
                            x='Weekly_GenAI_Hours', y='Post_Semester_GPA', trendline='ols',
                            title='Scatter Plot: Durasi Belajar AI vs Post GPA (Sampel 1000 data)', color_discrete_sequence=['#E67E22'])
        fig3_2 = apply_warm_layout(fig3_2)
        st.plotly_chart(fig3_2, use_container_width=True)

# --- TAB 3: KESEHATAN MENTAL (FIX TABEL KONTINGENSI GELAP) ---
with tab3:
    st.markdown("### Hubungan Kebijakan Kampus dengan Tingkat Stress")
    st.info("""
    📌 **Hasil Analisis PB3 — Kebijakan Institusi vs Performa & Burnout**
    * Aturan Strictly Ban berkorelasi dengan nilai rata-rata GPA terendah (3.333) dan tingkat High Burnout tertinggi (29.8%).
    """)
    col1, col2 = st.columns(2)
    with col1:
        mental_pct = df_filtered.groupby(['Institutional_Policy', 'Burnout_Risk_Level']).size().reset_index(name='count')
        policy_totals = df_filtered['Institutional_Policy'].value_counts().reset_index()
        policy_totals.columns = ['Institutional_Policy', 'total_policy']
        mental_pct = pd.merge(mental_pct, policy_totals, on='Institutional_Policy')
        mental_pct['Persentase'] = (mental_pct['count'] / mental_pct['total_policy']) * 100
        fig4_1 = px.bar(mental_pct, x='Institutional_Policy', y='Persentase', color='Burnout_Risk_Level', 
                        title='Proporsi Risiko Burnout Berdasarkan Kebijakan Kampus (%)', barmode='group',
                        color_discrete_map={'Low': '#2ECC71', 'Medium': '#F1C40F', 'High': '#E74C3C'})
        fig4_1.update_yaxes(ticksuffix="%")
        fig4_1 = apply_warm_layout(fig4_1)
        st.plotly_chart(fig4_1, use_container_width=True)
    with col2:
        fig4_2 = px.box(df_filtered, x='Institutional_Policy', y='Anxiety_Level_During_Exams', title='Box Plot: Tingkat Kecemasan Ujian per Kebijakan Kampus', color_discrete_sequence=['#E67E22'])
        fig4_2 = apply_warm_layout(fig4_2)
        st.plotly_chart(fig4_2, use_container_width=True)

    st.markdown("---")
    with st.expander("🔬 Uji Statistik Formal: Chi-Square Test of Independence (Validasi Aturan AI vs Stres)"):
        st.markdown("#### **1. Tabel Kontingensi (Sebaran Jumlah Mahasiswa Riil)**")
        
        contingency_data = pd.DataFrame({
            "Kebijakan Kampus (Policy)": ["Allow With Restrictions", "Banned In Exams", "No Policy", "Strictly Ban"],
            "Low Risk": ["3,524", "4,122", "3,115", "2,841"],
            "Medium Risk": ["6,110", "7,255", "5,420", "4,890"],
            "High Risk": ["3,912", "4,054", "3,180", "4,188"]
        })
        
        # Menggunakan st.dataframe dengan menyembunyikan indeks bawaan agar tampilan bersih putih sesuai tema
        st.dataframe(contingency_data, use_container_width=True, hide_index=True)
        
        st.markdown("#### **2. Hasil Uji Hipotesis Chi-Square**")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric(label="Chi-Square Statistic (χ²)", value="153.15")
        with col_stat2:
            st.metric(label="P-Value", value="0.0000")
        st.error("**🚨 KEPUTUSAN STATISTIK:** **Tolak H0 (P-Value = 0.0000 < 0.05).** Hubungan Kebijakan Kampus dan Tingkat Burnout SANGAT SIGNIFIKAN.")

# --- TAB 4: RETENSI ILMU ---
with tab4:
    st.markdown("### Korelasi Ketergantungan AI dengan Daya Ingat")
    st.info("""
    📌 **Hasil Analisis PB2 — AI Dependency vs Skill Retention**
    * Skor dependensi tinggi (skor 8–10) menunjukkan penurunan rata-rata retensi ilmu ke angka 63–69.
    """)
    col1, col2 = st.columns(2)
    with col1:
        ret_dep = df_filtered.groupby('Perceived_AI_Dependency')['Skill_Retention_Score'].mean().reset_index()
        fig5_1 = px.line(ret_dep, x='Perceived_AI_Dependency', y='Skill_Retention_Score', title='Tren Penurunan Skill Retention', markers=True)
        fig5_1.update_traces(line_color='#E67E22')
        fig5_1 = apply_warm_layout(fig5_1)
        st.plotly_chart(fig5_1, use_container_width=True)
    with col2:
        fig5_2 = px.density_heatmap(df_filtered, x='Perceived_AI_Dependency', y='Skill_Retention_Score', title='Kepadatan Distribusi Dependency vs Retention', color_continuous_scale='YlOrRd')
        fig5_2 = apply_warm_layout(fig5_2)
        st.plotly_chart(fig5_2, use_container_width=True)

# --- TAB 5: PROFIL RISIKO (ROSE CHART DI KIRI & GAMBAR BESAR DI KANAN) ---
with tab5:
    st.markdown("### ⚠️ Segmentasi & Profil Risiko Burnout Mahasiswa")
    st.markdown("##### Framework Klasifikasi Berbasis *Decision Tree Classifier*")
    
    st.info("""
    📌 **Evaluasi Keandalan Klasifikasi Model:**
    * **Akurasi Global:** Model berhasil mengklasifikasikan tingkat burnout dengan akurasi **52%** pada data testing.
    * **Recall Tertinggi (63%):** Model paling andal dalam mengidentifikasi kelompok mahasiswa di zona **Medium Burnout**.
    """)
    
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.markdown("#### 📊 *Feature Importance (Rose Chart)*")
        
        df_importance = pd.DataFrame({
            "Fitur": [
                "Weekly_GenAI_Hours", 
                "Year_of_Study_Graduate", 
                "Institutional_Policy_Strict_Ban", 
                "Year_of_Study_Senior", 
                "Pre_Semester_GPA", 
                "Post_Semester_GPA", 
                "Perceived_AI_Dependency",
                "Anxiety_Level_During_Exams"
            ],
            "Nilai": [0.886175, 0.065356, 0.030942, 0.010440, 0.003067, 0.002522, 0.001500, 0.000000]
        })
        df_importance = df_importance.sort_values(by="Nilai", ascending=False)
        
        # Pembuatan Rose Chart / Polar Bar Chart
        fig_rose = px.bar_polar(
            df_importance, 
            r="Nilai", 
            theta="Fitur",
            color="Nilai",
            color_continuous_scale="YlOrRd",
            template="none"
        )
        fig_rose.update_layout(
            polar=dict(
                radialaxis=dict(showticklabels=True, ticks="outside", gridcolor="rgba(211, 84, 0, 0.1)"),
                angularaxis=dict(gridcolor="rgba(211, 84, 0, 0.1)", tickfont=dict(size=10, color="#2C1A11"))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=30, b=30),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_rose, use_container_width=True)
        
        # Tabel Referensi Nilai Mutlak
        df_table_show = df_importance.copy()
        df_table_show["Bobot (%)"] = (df_table_show["Nilai"] * 100).map("{:.2f}%".format)
        st.table(df_table_show[["Fitur", "Bobot (%)"]])

    with col_right:
        st.markdown("#### 🌲 Pohon Keputusan Klasifikasi (*Decision Tree*)")
        nama_gambar = 'pb5_decision_tree_final_kerangka.png'
        if os.path.exists(nama_gambar):
            image = Image.open(nama_gambar)
            st.image(image, caption="Struktur Aturan Split Decision Tree (Sweet Spot: Max Depth = 4)", use_container_width=True)
        else:
            st.warning(f"⚠️ Gambar '{nama_gambar}' belum ditemukan di direktori aktif.")

    st.markdown("---")
    st.markdown("#### 🔍 Karakteristik Profil Hasil Prediksi Model ")
    
    profil_risiko_table = pd.DataFrame({
        "Indikator / Karakteristik": [
            "Rata-rata Jam GenAI / Minggu", 
            "Rata-rata Jam Belajar Tradisional", 
            "Rata-rata Skor Anxiety Ujian", 
            "Fakultas / Jurusan Dominan", 
            "Tingkat Angkatan Terbanyak", 
            "Segmentasi Pengguna AI"
        ],
        "🟢 LOW RISK": ["1.87 Jam", "11.82 Jam", "3.80 / 10", "Business", "Junior", "Light User"],
        "🟡 MEDIUM RISK": ["6.59 Jam", "11.40 Jam", "4.05 / 10", "STEM", "Senior", "Moderate User"],
        "🔴 HIGH RISK": ["22.34 Jam", "9.97 Jam", "5.46 / 10", "STEM", "Freshman (Maba)", "Heavy User"]
    })
    st.table(profil_risiko_table)
    
    st.markdown("""
    > 💡 **Key Insight & Analisis Strategis Laporan BI:**
    > * **Lokomotif Utama Risiko:** Berdasarkan perhitungan matematika model, durasi pemakaian **`Weekly_GenAI_Hours` (88.62%)** adalah indikator tunggal yang mendominasi arah pembentukan stres mahasiswa dibandingkan faktor lainnya.
    > * **Anomali Transisi Maba STEM (High Risk):** Temuan krusial menunjukkan kelompok *High Risk* secara dominan diisi oleh mahasiswa baru (**Freshman**) di bidang **STEM** dengan durasi penggunaan GenAI yang sangat ekstrem (**22.34 jam/minggu**). Hal ini mengindikasikan adanya beban transisi kuliah teknik/sains yang berat, sehingga maba mengompensasikannya secara berlebihan dengan asisten AI yang justru memicu kecemasan ujian lebih tinggi (skor 5.46/10).
    """)
