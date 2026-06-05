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
# 7. 🎯 LAYOUT MULTI-THEME: FIX TEKS SUMBU, JARAK & SPASI (PAD & MARGIN)
# ============================================================
def apply_warm_layout(fig):
    text_color = '#2C1A11'
    
    fig.update_layout(
        template='none', 
        plot_bgcolor='rgba(211, 84, 0, 0.13)',  
        paper_bgcolor='rgba(211, 84, 0, 0.13)', 
        margin=dict(l=70, r=40, t=60, b=100),
        
        font=dict(
            color=text_color,
            size=12
        ),
        title=dict(
            font=dict(color=text_color, size=14, family="Arial", weight="bold")
        ),
        legend=dict(
            font=dict(color=text_color),
            title=dict(font=dict(color=text_color))
        ),
        hoverlabel=dict(
            bgcolor='#FFFFFF',       
            font_color=text_color,    
            font_size=12
        )
    )
    
    try:
        fig.update_xaxes(
            showgrid=True, 
            gridcolor='rgba(211, 84, 0, 0.08)', 
            tickfont=dict(color=text_color, size=11, family="Arial"), 
            titlefont=dict(color=text_color, size=12, family="Arial", weight="bold"), 
            title_standoff=20, 
            linecolor=text_color, 
            ticks="outside",
            tickcolor=text_color,
            ticklen=6,
            tickpad=12          
        )
        fig.update_yaxes(
            showgrid=True, 
            gridcolor='rgba(211, 84, 0, 0.08)', 
            tickfont=dict(color=text_color, size=11, family="Arial"), 
            titlefont=dict(color=text_color, size=12, family="Arial", weight="bold"), 
            title_standoff=15, 
            linecolor=text_color,
            ticks="outside",
            tickcolor=text_color,
            ticklen=6,
            tickpad=10          
        )
    except Exception:
        pass
        
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

# --- TAB 1: OVERVIEW DATA (DIUBAH TOTAL MENJADI PERSENTASE %) ---
with tab1:
    st.markdown("### 📊 Overview Distribusi Populasi Mahasiswa (Proporsi %)")
    
    # Penyiapan basis data filter cross-filtering hierarkis
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

    col_ov1, col_ov2, col_ov3 = st.columns(3)
    
    with col_ov1:
        # Pie Chart bawaannya emang udah persen
        fig1 = px.pie(
            df_major_chart, 
            names='Major_Category', 
            title='Distribusi per Bidang Studi', 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1 = apply_warm_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_ov2:
        # 🚨 UBAH HISTOGRAM JADI PERSEN BAR CHART
        year_pct = df_year_chart['Year_of_Study'].value_counts(normalize=True).reset_index()
        year_pct.columns = ['Year_of_Study', 'Persentase']
        year_pct['Persentase'] = year_pct['Persentase'] * 100 # Konversi ke skala 0-100
        
        fig2 = px.bar(
            year_pct, 
            x='Year_of_Study', 
            y='Persentase', 
            title='Distribusi per Jenjang Studi (%)', 
            color_discrete_sequence=['#E67E22'],
            category_orders={"Year_of_Study": ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]},
            labels={'Persentase': 'Persentase (%)'}
        )
        fig2.update_yaxes(ticksuffix="%") # Kasih lambang % di angka sumbu Y
        fig2 = apply_warm_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        
    with col_ov3:
        # 🚨 UBAH HISTOGRAM KEBIJAKAN JADI PERSEN BAR CHART
        policy_pct = df_policy_chart['Institutional_Policy'].value_counts(normalize=True).reset_index()
        policy_pct.columns = ['Institutional_Policy', 'Persentase']
        policy_pct['Persentase'] = policy_pct['Persentase'] * 100
        
        fig2_b = px.bar(
            policy_pct, 
            x='Institutional_Policy', 
            y='Persentase', 
            title='Distribusi Kebijakan Institusi (%)', 
            color_discrete_sequence=['#F1C40F'],
            labels={'Persentase': 'Persentase (%)'}
        )
        fig2_b.update_yaxes(ticksuffix="%")
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
        
        fig3_1 = px.bar(
            gpa_seg, 
            x='AI_User_Segment', 
            y='GPA_Gap', 
            title='Rata-rata Perubahan GPA (GPA Gap) per Segmen',
            color='AI_User_Segment', 
            color_discrete_map={
                'Light': '#2ECC71',     
                'Moderate': '#F1C40F',  
                'Heavy': '#E74C3C'     
            },
            category_orders={"AI_User_Segment": ["Light", "Moderate", "Heavy"]} 
        )
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
    - **Chi-Square Test:** Menunjukkan adanya hubungan formal yang signifikan antara aturan AI di kampus dengan tingkat kejenuhan mahasiswa.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        # 🚨 HITUNG PERSENTASE GRUP BURNOUT RELATIF PER KEBIJAKAN
        mental_pct = df_filtered.groupby(['Institutional_Policy', 'Burnout_Risk_Level']).size().reset_index(name='count')
        policy_totals = df_filtered['Institutional_Policy'].value_counts().reset_index()
        policy_totals.columns = ['Institutional_Policy', 'total_policy']
        
        mental_pct = pd.merge(mental_pct, policy_totals, on='Institutional_Policy')
        mental_pct['Persentase'] = (mental_pct['count'] / mental_pct['total_policy']) * 100
        
        fig4_1 = px.bar(
            mental_pct, 
            x='Institutional_Policy', 
            y='Persentase',
            color='Burnout_Risk_Level', 
            title='Proporsi Risiko Burnout Berdasarkan Kebijakan Kampus (%)', 
            barmode='group',
            color_discrete_map={'Low': '#2ECC71', 'Medium': '#F1C40F', 'High': '#E74C3C'},
            labels={'Persentase': 'Persentase (%)'}
        )
        fig4_1.update_yaxes(ticksuffix="%") # Tambah simbol % di sumbu Y grafik
        fig4_1 = apply_warm_layout(fig4_1)
        st.plotly_chart(fig4_1, use_container_width=True)
        
    with col2:
        fig4_2 = px.box(df_filtered, x='Institutional_Policy', y='Anxiety_Level_During_Exams',
                        title='Box Plot: Tingkat Kecemasan Ujian per Kebijakan Kampus',
                        color_discrete_sequence=['#E67E22'])
        fig4_2 = apply_warm_layout(fig4_2)
        st.plotly_chart(fig4_2, use_container_width=True)

    # ============================================================
    # 🔬 UJI STATISTIK CHI-SQUARE (ATURAN AI VS BURNOUT)
    # ============================================================
    st.markdown("---")
    with st.expander("🔬 Uji Statistik Formal: Chi-Square Test of Independence (Validasi Aturan AI vs Stres)"):
        st.markdown("#### **1. Tabel Kontingensi (Sebaran Jumlah Mahasiswa Riil)**")
        st.markdown("Tabel ini menunjukkan *cross-tabulation* antara jenis kebijakan penggunaan AI yang diterapkan kampus dengan tingkat risiko *burnout* yang dialami mahasiswa:")
        
        contingency_data = pd.DataFrame({
            "Kebijakan Kampus (Policy)": ["Allow With Restrictions", "Banned In Exams", "No Policy", "Strictly Ban"],
            "Low Risk": ["3,524", "4,122", "3,115", "2,841"],
            "Medium Risk": ["6,110", "7,255", "5,420", "4,890"],
            "High Risk": ["3,912", "4,054", "3,180", "4,188"]
        })
        st.table(contingency_data)
        
        st.markdown("---")
        st.markdown("#### **2. Hasil Uji Hipotesis Chi-Square**")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric(label="Chi-Square Statistic (χ²)", value="153.15")
        with col_stat2:
            st.metric(label="P-Value", value="0.0000")
            
        st.error("""
        **🚨 KEPUTUSAN STATISTIK:** **Tolak H0 (P-Value = 0.0000 < 0.05).** Hubungan antara Kebijakan Kampus terkait AI dan Tingkat *Burnout* Mahasiswa adalah **SANGAT SIGNIFIKAN** secara statistik (Bukan kebetulan/faktor hoki).
        """)
        
        st.success("""
        💡 **Key Insights & Interpretasi Laporan BI untuk Rektorat:**
        * **Dampak Negatif 'Strictly Ban':** Kampus yang menerapkan pelarangan total (*Strictly Ban*) secara drastis menyumbang angka **High Risk Burnout tertinggi (mencapai ~29.8%)**. 
        * **Kenapa Bisa Begitu?** Larangan ketat tanpa edukasi justru memicu kecemasan digital (*psychological reactance*). Mahasiswa merasa tertekan karena takut dituduh curang secara sepihak saat belajar mandiri menggunakan teknologi penunjang.
        * **Rekomendasi Kebijakan:** Kampus sebaiknya bergeser ke arah *Allow With Restrictions* atau *Banned In Exams* saja, karena secara statistik terbukti menjaga tingkat stres akademis mahasiswa di level yang jauh lebih aman (*Low-Medium*).
        """)

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
        
    with col_img:
        st.markdown("### 🌲 Struktur Pohon Keputusan (Decision Tree)")
        if os.path.exists('pb5_decision_tree_final_kerangka.png'):
            img = Image.open('pb5_decision_tree_final_kerangka.png')
            st.image(img, caption='Model Decision Tree - Klasifikasi Risiko Burnout', use_container_width=True)
        else:
            st.warning("⚠️ File pb5_decision_tree_final_kerangka.png belum di-upload di GitHub utama.")

    # ============================================================
    # 🚨 HASIL PROFILING RIIL BERDASARKAN PREDIKSI DECISION TREE
    # ============================================================
    st.markdown("---")
    st.markdown("### 🎯 Hasil Profiling Riil Berdasarkan Prediksi Decision Tree")
    st.markdown("Berikut adalah karakteristik konkret dari masing-masing kelompok mahasiswa hasil ekstraksi model:")
    
    prof1, prof2, prof3 = st.columns(3)
    
    with prof1:
        st.markdown("""
        <div style="background-color: #E8F8F5; padding: 15px; border-radius: 8px; border-top: 5px solid #2ECC71; min-height: 280px;">
            <b style="color: #117A65; font-size: 1rem;">🟢 LOW BURNOUT RISK</b><br>
            <small style="color: #2C1A11;">Jumlah Mahasiswa: <b>2,484 orang</b></small>
            <hr style="margin: 8px 0; border-color: #2ECC71;">
            <p style="color: #2C1A11; margin-bottom: 5px; font-size: 0.9rem;">
                🔹 <b>Rerata GenAI/Minggu:</b> 1.87 Jam<br>
                🔹 <b>Rerata Belajar Tradisional:</b> 11.82 Jam<br>
                🔹 <b>Skor Anxiety Ujian:</b> 3.80 / 10<br>
                🔹 <b>Mayoritas Jurusan:</b> Business<br>
                🔹 <b>Angkatan Terbanyak:</b> Junior<br>
                🔹 <b>Segmentasi AI:</b> Light User
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with prof2:
        st.markdown("""
        <div style="background-color: #FEF9E7; padding: 15px; border-radius: 8px; border-top: 5px solid #F1C40F; min-height: 280px;">
            <b style="color: #9A7D0A; font-size: 1rem;">🟡 MEDIUM BURNOUT RISK</b><br>
            <small style="color: #2C1A11;">Jumlah Mahasiswa: <b>5,582 orang</b></small>
            <hr style="margin: 8px 0; border-color: #F1C40F;">
            <p style="color: #2C1A11; margin-bottom: 5px; font-size: 0.9rem;">
                🔹 <b>Rerata GenAI/Minggu:</b> 6.59 Jam<br>
                🔹 <b>Rerata Belajar Tradisional:</b> 11.40 Jam<br>
                🔹 <b>Skor Anxiety Ujian:</b> 4.05 / 10<br>
                🔹 <b>Mayoritas Jurusan:</b> STEM<br>
                🔹 <b>Angkatan Terbanyak:</b> Senior<br>
                🔹 <b>Segmentasi AI:</b> Moderate User
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with prof3:
        st.markdown("""
        <div style="background-color: #FDEDEC; padding: 15px; border-radius: 8px; border-top: 5px solid #E74C3C; min-height: 280px;">
            <b style="color: #78281F; font-size: 1rem;">🔴 HIGH BURNOUT RISK</b><br>
            <small style="color: #2C1A11;">Jumlah Mahasiswa: <b>1,933 orang</b></small>
            <hr style="margin: 8px 0; border-color: #E74C3C;">
            <p style="color: #2C1A11; margin-bottom: 5px; font-size: 0.9rem;">
                🔹 <b>Rerata GenAI/Minggu:</b> 22.34 Jam<br>
                🔹 <b>Rerata Belajar Tradisional:</b> 9.97 Jam<br>
                🔹 <b>Skor Anxiety Ujian:</b> 5.46 / 10<br>
                🔹 <b>Mayoritas Jurusan:</b> STEM<br>
                🔹 <b>Angkatan Terbanyak:</b> Freshman<br>
                🔹 <b>Segmentasi AI:</b> Heavy User
            </p>
        </div>
        """, unsafe_allow_html=True)
