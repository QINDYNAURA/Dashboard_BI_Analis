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
# 2. 🎨 CUSTOM CSS — FIX TOTAL TEKS TABEL, BLOCKQUOTE, & THEME KREM
# ============================================================
st.markdown("""
    <style>
    /* Background Utama Aplikasi (Krem-Oranye Soft) */
    .stApp {
        background-color: #FDF6EC;
    }
    
    /* FIX BAR HITAM ATAS: Paksa Header Streamlit Ikut Warna Krem Dasar */
    [data-testid="stHeader"] {
        background-color: #FDF6EC !important;
    }
    
    /* Semua tulisan reguler luar wajib Hitam/Cokelat Tua biar kontras */
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3 {
        color: #2C1A11 !important;
        opacity: 1 !important;
    }
    
    /* FIX UTAMA UNTUK BLOCKQUOTE (KUTIPAN DI BAWAH TABEL PROFIL RISIKO) */
    blockquote {
        background-color: #F3E5D8 !important; /* Kasih background biar kontras */
        border-left: 5px solid #E67E22 !important; /* Garis oranye di kiri */
        padding: 10px 15px !important;
        margin: 10px 0 !important;
        border-radius: 4px !important;
    }
    blockquote p {
        color: #2C1A11 !important; /* Paksa tulisan di dalam kutipan jadi hitam pekat */
        font-weight: 500 !important;
        opacity: 1 !important;
    }
    
    /* FIX UTAMA UNTUK WARNA TULISAN DI DALAM TABEL */
    table {
        color: #2C1A11 !important;
    }
    th {
        background-color: #E67E22 !important;
        color: white !important; /* Header tabel pakai tulisan putih di atas oranye biar kebaca */
        font-weight: bold !important;
    }
    td {
        color: #2C1A11 !important; /* Isi tabel paksa hitam pekat */
        background-color: #FFFFFF !important;
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
    
    /* FIX TEKS TAB: Paksa Tulisan Tab Menjadi Hitam Pekat */
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        color: #2C1A11 !important;
        border: 1px solid #E6A23C;
    }
    
    /* Efek Saat Tab Aktif Diklik (Warna Oranye, Tulisan Putih) */
    .stTabs [aria-selected="true"] {
        background-color: #E67E22 !important;
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] span {
        color: white !important;
    }
    
    /* Warna Judul Utama H1 */
    h1 {
        color: #A04000 !important;
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
# 3. LOAD DATA
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
# 4. SIDEBAR PANEL — FILTER INTERAKTIF
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
st.sidebar.markdown("*Divisi Riset & Kebijakan | Konsultan BI*")

# Proses Filtering Data Utama (Untuk KPI dan Tab 2-5)
df_filtered = df.copy()
if selected_major != 'Semua':
    df_filtered = df_filtered[df_filtered['Major_Category'] == selected_major]
if selected_year != 'Semua':
    df_filtered = df_filtered[df_filtered['Year_of_Study'] == selected_year]
if selected_policy != 'Semua':
    df_filtered = df_filtered[df_filtered['Institutional_Policy'] == selected_policy]

# ============================================================
# 5. HEADER DASHBOARD UTAMA
# ============================================================
st.title("🎓 Dashboard Analisis Dampak GenAI Terhadap Mahasiswa")
st.markdown("### Business Intelligence Platform | Divisi Riset & Kebijakan")
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
# 7. 🎯 LAYOUT MULTI-THEME: PAKSA TOTAL TEXT SUMBU MENJADI HITAM PEKAT
# ============================================================
def apply_warm_layout(fig):
    # Paksa warna teks dasar yang akan digunakan
    text_color = '#2C1A11'
    
    fig.update_layout(
        # Menggunakan template basic bawaan plotly agar tidak ditimpa font putih oleh Streamlit
        template='none', 
        # Mengubah latar belakang menjadi oranye transparan (Alpha = 0.15)
        plot_bgcolor='rgba(211, 84, 0, 0.15)',  
        paper_bgcolor='rgba(211, 84, 0, 0.15)', 
        margin=dict(l=50, r=40, t=60, b=60),
        
        # Paksa seluruh font global menjadi hitam pekat
        font=dict(
            color=text_color,
            size=12
        ),
        
        # Paksa Judul Grafik berwarna hitam pekat
        title=dict(
            font=dict(color=text_color, size=14, family="Arial", weight="bold")
        ),
        
        # Paksa Teks Legenda & Judul Legenda jadi item pekat
        legend=dict(
            font=dict(color=text_color),
            title=dict(font=dict(color=text_color))
        ),
        
        # Fix untuk popup hover teks
        hoverlabel=dict(
            bgcolor='#FFFFFF',       
            font_color=text_color,    
            font_size=12
        )
    )
    
    # 🚨 FIX TOTAL PROBLEM IMAGE_CF9B6B.PNG: Paksa warna komponen sumbu X dan Y ke hitam pekat
    try:
        fig.update_xaxes(
            showgrid=True, 
            gridcolor='rgba(211, 84, 0, 0.1)', 
            tickfont=dict(color=text_color, size=11, family="Arial"), # Huruf Freshman, Senior dll
            titlefont=dict(color=text_color, size=12, family="Arial", weight="bold"), # Label 'Year_of_Study'
            linecolor=text_color, # Garis sumbu dasar
            ticks="outside",
            tickcolor=text_color
        )
        fig.update_yaxes(
            showgrid=True, 
            gridcolor='rgba(211, 84, 0, 0.1)', 
            tickfont=dict(color=text_color, size=11, family="Arial"), # Angka 0, 50, 100 dsb
            titlefont=dict(color=text_color, size=12, family="Arial", weight="bold"), # Label 'count'
            linecolor=text_color,
            ticks="outside",
            tickcolor=text_color
        )
    except Exception:
        pass
        
    # Paksa anotasi teks tambahan di dalam chart (jika ada) biar ikutan hitam pekat
    try:
        fig.update_annotations(font=dict(color=text_color))
    except Exception:
        pass
        
    return fig

# ============================================================
# 8. SISTEM TAB MULTI-DIMENSI
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview Data", 
    "🤖 Dampak Ke GPA", 
    "🧠 Kesehatan Mental", 
    "📚 Retensi Ilmu", 
    "⚠️ Profil Risiko"
])

# --- TAB 1: OVERVIEW DATA (FIX CROSS-FILTERING HIERARKIS) ---
with tab1:
    st.markdown("### 📊 Overview Distribusi Populasi Mahasiswa (Pintar)")
    st.caption("💡 *Sistem Cross-Filtering aktif: Jenjang studi mengikuti filter Bidang Studi. Kebijakan mengikuti kedua filter.*")
    
    # --- LOGIKA FILTERING KHUSUS UNTUK TAB OVERVIEW ---
    df_major_chart = df.copy()
    
    if selected_major != 'Semua':
        df_year_chart = df[df['Major_Category'] == selected_major]
    else:
        df_year_chart = df.copy()
        
    df_policy_chart = df.copy()
    if selected_major != 'Semua':
        df_policy_chart = df_policy_chart[df_policy_chart['Major_Category'] == selected_major]
    if selected_year != 'Semua':
        df_policy_chart = df_policy_chart[df_policy_chart['Year_of_Study'] == selected_year]
    # -------------------------------------------------

    # Membuat 3 kolom sejajar
    col_ov1, col_ov2, col_ov3 = st.columns(3)
    
    with col_ov1:
        fig1 = px.pie(
            df_major_chart, 
            names='Major_Category', 
            title='Distribusi per Bidang Studi', 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1 = apply_warm_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_ov2:
        fig2 = px.histogram(
            df_year_chart, 
            x='Year_of_Study', 
            title='Distribusi per Jenjang Studi', 
            color_discrete_sequence=['#E67E22'],
            category_orders={"Year_of_Study": ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]}
        )
        fig2 = apply_warm_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        
    with col_ov3:
        fig2_b = px.histogram(
            df_policy_chart, 
            x='Institutional_Policy', 
            title='Distribusi Kebijakan Institusi', 
            color_discrete_sequence=['#F1C40F']
        )
        fig2_b = apply_warm_layout(fig2_b)
        st.plotly_chart(fig2_b, use_container_width=True)

# --- TAB 2: DAMPAK KE GPA ---
with tab2:
    st.markdown("### Analisis Penggunaan AI vs Performa Nilai (GPA)")
    
    st.info("""
    📌 **Hasil Analisis PB1 — Intensitas AI vs Performa Akademik**
    - **Korelasi Pearson:** r = -0.0186 (Sangat Lemah, Negatif, Signifikan)
    - **Regresi Linear:** R² = 0.0003 → setiap +1 jam/minggu AI, GPA berubah -0.0011 poin
    - **Moderate User** memiliki rata-rata GPA tertinggi **(3.372)** dan GPA Gap terbesar **(+0.227)**
    - **Heavy User** justru memiliki GPA terendah **(3.320)** dan GPA Gap terkecil **(+0.173)**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        gpa_seg = df_filtered.groupby('AI_User_Segment', observed=True)['GPA_Gap'].mean().reset_index()
        fig3_1 = px.bar(gpa_seg, x='AI_User_Segment', y='GPA_Gap', title='Rata-rata Perubahan GPA (GPA Gap) per Segmen',
                      color='AI_User_Segment', color_discrete_sequence=['#2ECC71', '#F1C40F', '#E74C3C'])
        fig3_1 = apply_warm_layout(fig3_1)
        st.plotly_chart(fig3_1, use_container_width=True)
    with col2:
        fig3_2 = px.scatter(df_filtered.sample(n=1000 if len(df_filtered)>1000 else len(df_filtered)), 
                            x='Weekly_GenAI_Hours', y='Post_Semester_GPA', trendline='ols',
                            title='Scatter Plot: Durasi Belajar AI vs Post GPA (Sampel 1000 data)',
                            color_discrete_sequence=['#E67E22'])
        fig3_2 = apply_warm_layout(fig3_2)
        st.plotly_chart(fig3_2, use_container_width=True)

# --- TAB 3: KESEHATAN MENTAL ---
with tab3:
    st.markdown("### Hubungan Kebijakan Kampus dengan Tingkat Stress")
    
    st.info("""
    📌 **Hasil Analisis PB3 — Kebijakan Institusi vs Performa & Burnout**
    - **Strictly_Ban** memiliki rata-rata GPA terendah **(3.333)** dan % High Burnout tertinggi **(29.8%)**
    - **Chi-Square:** χ² = 153.15, p-value = 0.000 → distribusi burnout berbeda signifikan antar kebijakan
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        fig4_1 = px.histogram(df_filtered, x='Institutional_Policy', color='Burnout_Risk_Level', 
                            title='Tingkat Risiko Burnout Berdasarkan Kebijakan Kampus', barmode='group',
                            color_discrete_map={'Low': '#2ECC71', 'Medium': '#F1C40F', 'High': '#E74C3C'})
        fig4_1 = apply_warm_layout(fig4_1)
        st.plotly_chart(fig4_1, use_container_width=True)
    with col2:
        fig4_2 = px.box(df_filtered, x='Institutional_Policy', y='Anxiety_Level_During_Exams',
                        title='Box Plot: Tingkat Kecemasan Ujian per Kebijakan Kampus',
                        color_discrete_sequence=['#E67E22'])
        fig4_2 = apply_warm_layout(fig4_2)
        st.plotly_chart(fig4_2, use_container_width=True)

# --- TAB 4: RETENSI ILMU ---
with tab4:
    st.markdown("### Korelasi Ketergantungan AI dengan Daya Ingat")
    
    st.info("""
    📌 **Hasil Analisis PB2 — AI Dependency vs Skill Retention**
    - **Korelasi Pearson:** r = -0.0843 (Sangat Lemah, Negatif, Signifikan)
    - Skor dependency 1–3 memiliki rata-rata retention **75–76**, skor 8–10 turun ke **63–69**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        ret_dep = df_filtered.groupby('Perceived_AI_Dependency')['Skill_Retention_Score'].mean().reset_index()
        fig5_1 = px.line(ret_dep, x='Perceived_AI_Dependency', y='Skill_Retention_Score', title='Tren Penurunan Skill Retention', markers=True)
        fig5_1.update_traces(line_color='#E67E22')
        fig5_1 = apply_warm_layout(fig5_1)
        st.plotly_chart(fig5_1, use_container_width=True)
    with col2:
        fig5_2 = px.density_heatmap(df_filtered, x='Perceived_AI_Dependency', y='Skill_Retention_Score',
                                    title='Kepadatan Distribusi Dependency vs Retention',
                                    color_continuous_scale='YlOrRd')
        fig5_2 = apply_warm_layout(fig5_2)
        st.plotly_chart(fig5_2, use_container_width=True)

# --- TAB 5: PROFIL RISIKO ---
with tab5:
    st.markdown("### Rekomendasi Profil Risiko & Variabel Penentu Burnout")
    
    st.info("""
    📌 **Hasil Analisis PB5 — Profiling Burnout Risk (Decision Tree Model)**
    - **Akurasi Model:** 52% | Berhasil mengklasifikasikan mahasiswa ke dalam 3 tingkatan risiko secara optimal.
    - 💡 **Kesimpulan Utama:** Durasi penggunaan AI per minggu (`Weekly_GenAI_Hours`) mutlak menjadi faktor penentu tunggal terbesar yang memicu kejenuhan atau stres akademis mahasiswa.
    """)
    
    col_table, col_img = st.columns([2, 3])
    
    with col_table:
        st.markdown("### 📊 Hasil Variabel Importance")
        st.markdown("Berikut adalah kontribusi masing-masing variabel dalam memprediksi tingkat risiko *burnout* mahasiswa:")
        
        importance_data = pd.DataFrame({
            "Nama Variabel / Fitur": ["Weekly_GenAI_Hours", "Major_Category", "Year_of_Study", "Variabel Lainnya"],
            "Bobot Pengaruh": ["88.6%", "6.2%", "4.1%", "1.1%"],
            "Tingkat Dampak": ["🚨 Sangat Tinggi (Kritis)", "🟡 Rendah", "🟡 Rendah", "⚪ Sangat Rendah"]
        })
        st.table(importance_data)
        
        st.markdown("""
        > 💡 **Key Takeaways untuk BI Report:**
        > * **Weekly GenAI Hours (88.6%):** Dominasi mutlak! Mahasiswa kategori *Heavy User* berisiko tinggi mengalami *burnout* akademis **3x lipat**.
        > * **Major & Year (10.3%):** Hanya memberikan pengaruh minor pada tingkat stres mahasiswa.
        """)
        
    with col_img:
        st.markdown("### 🌲 Struktur Pohon Keputusan (Decision Tree)")
        if os.path.exists('pb5_decision_tree_final_kerangka.png'):
            img = Image.open('pb5_decision_tree_final_kerangka.png')
            st.image(img, caption='Model Decision Tree - Klasifikasi Risiko Burnout', use_container_width=True)
        else:
            st.warning("⚠️ File pb5_decision_tree_final_kerangka.png belum di-upload di GitHub utama.")
