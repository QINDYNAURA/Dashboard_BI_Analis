%%writefile dashboard.py
# ============================================================
# DASHBOARD BI — AI IMPACT ON STUDENTS
# Analisis Dampak Penggunaan AI Generatif terhadap
# Performa Akademik dan Kesejahteraan Mahasiswa
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="AI Impact on Students Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
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
# SIDEBAR — FILTER INTERAKTIF
# ============================================================
st.sidebar.markdown("## 🔧 Filter Data")
st.sidebar.markdown("---")

major_options = ['Semua'] + sorted(df['Major_Category'].dropna().unique().tolist())
selected_major = st.sidebar.selectbox("📚 Bidang Studi", major_options)

year_options = ['Semua'] + ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
selected_year = st.sidebar.selectbox("🎓 Jenjang Studi", year_options)

policy_options = ['Semua'] + sorted(df['Institutional_Policy'].dropna().unique().tolist())
selected_policy = st.sidebar.selectbox("🏛️ Kebijakan Institusi", policy_options)

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Dataset Info**")
st.sidebar.markdown(f"Total Records: **{len(df):,}**")
st.sidebar.markdown(f"Total Variabel: **{df.shape[1]}**")
st.sidebar.markdown("---")
st.sidebar.markdown("*Divisi Riset & Kebijakan*")
st.sidebar.markdown("*Konsultan Pendidikan Tinggi Internasional*")

# Apply Filter
df_filtered = df.copy()
if selected_major != 'Semua':
    df_filtered = df_filtered[df_filtered['Major_Category'] == selected_major]
if selected_year != 'Semua':
    df_filtered = df_filtered[df_filtered['Year_of_Study'] == selected_year]
if selected_policy != 'Semua':
    df_filtered = df_filtered[df_filtered['Institutional_Policy'] == selected_policy]

# ============================================================
# HEADER
# ============================================================
st.title("🎓 AI Impact on Students")
st.markdown("### Business Intelligence Dashboard")
st.markdown("**Divisi Riset & Kebijakan | Konsultan Pendidikan Tinggi Internasional**")
st.markdown("---")

# ============================================================
# KPI METRICS
# ============================================================
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_gpa = df_filtered['Post_Semester_GPA'].mean()
    avg_gpa_all = df['Post_Semester_GPA'].mean()
    st.metric(
        label="📈 Rata-rata Post GPA",
        value=f"{avg_gpa:.3f}",
        delta=f"{avg_gpa - avg_gpa_all:+.3f} vs total"
    )

with col2:
    avg_retention = df_filtered['Skill_Retention_Score'].mean()
    avg_retention_all = df['Skill_Retention_Score'].mean()
    st.metric(
        label="🧠 Rata-rata Skill Retention",
        value=f"{avg_retention:.2f}",
        delta=f"{avg_retention - avg_retention_all:+.2f} vs total"
    )

with col3:
    pct_high_burnout = (df_filtered['Burnout_Risk_Level'] == 'High').mean() * 100
    pct_high_burnout_all = (df['Burnout_Risk_Level'] == 'High').mean() * 100
    st.metric(
        label="🔥 High Burnout Risk",
        value=f"{pct_high_burnout:.1f}%",
        delta=f"{pct_high_burnout - pct_high_burnout_all:+.1f}% vs total",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="👥 Total Mahasiswa",
        value=f"{len(df_filtered):,}",
        delta=f"{len(df_filtered) - len(df):,} dari filter"
    )

st.markdown("---")

# ============================================================
# TAB NAVIGASI
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🤖 Dampak AI",
    "🧠 Kesehatan Mental",
    "📚 Retensi Pengetahuan",
    "📐 Pola AI per Major",
    "⚠️ Profil Risiko"
])

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================
with tab1:
    st.subheader("📊 Overview — Distribusi Mahasiswa")
    st.markdown(f"Menampilkan data **{len(df_filtered):,}** mahasiswa sesuai filter.")

    col1, col2 = st.columns(2)

    with col1:
        major_dist = df_filtered['Major_Category'].value_counts().reset_index()
        major_dist.columns = ['Major', 'Jumlah']
        fig_major = px.pie(
            major_dist, values='Jumlah', names='Major',
            title='Distribusi Mahasiswa per Bidang Studi',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_major.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_major, use_container_width=True)

    with col2:
        year_order = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
        year_dist = df_filtered['Year_of_Study'].value_counts().reindex(year_order).reset_index()
        year_dist.columns = ['Jenjang', 'Jumlah']
        fig_year = px.bar(
            year_dist, x='Jenjang', y='Jumlah',
            title='Distribusi Mahasiswa per Jenjang Studi',
            color='Jumlah', color_continuous_scale='Blues',
            text='Jumlah'
        )
        fig_year.update_traces(textposition='outside')
        fig_year.update_layout(showlegend=False)
        st.plotly_chart(fig_year, use_container_width=True)

    policy_dist = df_filtered['Institutional_Policy'].value_counts().reset_index()
    policy_dist.columns = ['Kebijakan', 'Jumlah']
    fig_policy = px.bar(
        policy_dist, x='Kebijakan', y='Jumlah',
        title='Distribusi Mahasiswa per Kebijakan Institusi',
        color='Kebijakan',
        color_discrete_sequence=px.colors.qualitative.Set1,
        text='Jumlah'
    )
    fig_policy.update_traces(textposition='outside')
    fig_policy.update_layout(showlegend=False)
    st.plotly_chart(fig_policy, use_container_width=True)

# ============================================================
# TAB 2 — DAMPAK AI
# ============================================================
with tab2:
    st.subheader("🤖 Dampak AI — GPA vs Intensitas Penggunaan AI")

    # Insight Box PB1
    st.info("""
    📌 **Hasil Analisis PB1 — Intensitas AI vs Performa Akademik**
    - **Korelasi Pearson:** r = -0.0186 (Sangat Lemah, Negatif, Signifikan)
    - **Regresi Linear:** R² = 0.0003 → setiap +1 jam/minggu AI, GPA berubah -0.0011 poin
    - **Moderate User** memiliki rata-rata GPA tertinggi **(3.372)** dan GPA Gap terbesar **(+0.227)**
    - **Heavy User** justru memiliki GPA terendah **(3.320)** dan GPA Gap terkecil **(+0.173)**
    - 💡 **Insight:** Ada titik optimal penggunaan AI di 5–15 jam/minggu yang justru mendukung performa akademik
    """)

    # Metric Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Korelasi (r)", "-0.0186", "Sangat Lemah")
    with col2:
        st.metric("R-squared", "0.0003")
    with col3:
        st.metric("GPA Terbaik", "Moderate (3.372)")

    segment_order = ['Light', 'Moderate', 'Heavy']
    gpa_segment = df_filtered.groupby('AI_User_Segment', observed=True).agg(
        Rata_rata_GPA=('Post_Semester_GPA', 'mean'),
        Rata_rata_GPA_Gap=('GPA_Gap', 'mean'),
        Jumlah=('Post_Semester_GPA', 'count')
    ).reindex(segment_order).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig_segment = px.bar(
            gpa_segment, x='AI_User_Segment', y='Rata_rata_GPA',
            title='Rata-rata Post GPA per Segmen Pengguna AI',
            color='AI_User_Segment',
            color_discrete_map={
                'Light': '#2ecc71',
                'Moderate': '#f39c12',
                'Heavy': '#e74c3c'
            },
            text=gpa_segment['Rata_rata_GPA'].round(3),
            labels={'AI_User_Segment': 'Segmen', 'Rata_rata_GPA': 'Rata-rata GPA'}
        )
        fig_segment.update_traces(textposition='outside')
        fig_segment.update_layout(showlegend=False, yaxis_range=[0, 4.5])
        st.plotly_chart(fig_segment, use_container_width=True)

    with col2:
        fig_gap = px.bar(
            gpa_segment, x='AI_User_Segment', y='Rata_rata_GPA_Gap',
            title='Rata-rata GPA Gap per Segmen Pengguna AI',
            color='AI_User_Segment',
            color_discrete_map={
                'Light': '#2ecc71',
                'Moderate': '#f39c12',
                'Heavy': '#e74c3c'
            },
            text=gpa_segment['Rata_rata_GPA_Gap'].round(3),
            labels={'AI_User_Segment': 'Segmen', 'Rata_rata_GPA_Gap': 'GPA Gap'}
        )
        fig_gap.update_traces(textposition='outside')
        fig_gap.update_layout(showlegend=False)
        st.plotly_chart(fig_gap, use_container_width=True)

    sample_size = min(5000, len(df_filtered))
    fig_scatter = px.scatter(
        df_filtered.sample(sample_size, random_state=42),
        x='Weekly_GenAI_Hours',
        y='Post_Semester_GPA',
        color='AI_User_Segment',
        color_discrete_map={
            'Light': '#2ecc71',
            'Moderate': '#f39c12',
            'Heavy': '#e74c3c'
        },
        title=f'Scatter Plot: Weekly GenAI Hours vs Post Semester GPA (sample {sample_size:,} data)',
        opacity=0.4,
        labels={
            'Weekly_GenAI_Hours': 'Weekly GenAI Hours',
            'Post_Semester_GPA': 'Post Semester GPA',
            'AI_User_Segment': 'Segmen'
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================
# TAB 3 — KESEHATAN MENTAL
# ============================================================
with tab3:
    st.subheader("🧠 Kesehatan Mental — Burnout & Anxiety per Kebijakan")

    # Insight Box PB3
    st.info("""
    📌 **Hasil Analisis PB3 — Kebijakan Institusi vs Performa & Burnout**
    - **Strictly_Ban** memiliki rata-rata GPA terendah **(3.333)** dan % High Burnout tertinggi **(29.8%)**
    - **Actively_Encouraged** dan **Allowed_With_Citation** memiliki GPA lebih tinggi **(3.353)**
    - **Chi-Square:** χ² = 153.15, p-value = 0.000 → distribusi burnout berbeda signifikan antar kebijakan
    - 💡 **Insight:** Kebijakan pelarangan AI justru berkorelasi dengan burnout lebih tinggi
    """)

    # Metric Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("High Burnout Strict Ban", "29.8%", "+6.0% vs lainnya", delta_color="inverse")
    with col2:
        st.metric("High Burnout Allowed", "23.8%")
    with col3:
        st.metric("High Burnout Encouraged", "23.8%")

    col1, col2 = st.columns(2)

    with col1:
        burnout_policy = pd.crosstab(
            df_filtered['Institutional_Policy'],
            df_filtered['Burnout_Risk_Level'],
            normalize='index'
        ).reset_index()

        burnout_melted = burnout_policy.melt(
            id_vars='Institutional_Policy',
            var_name='Burnout_Level',
            value_name='Persentase'
        )
        burnout_melted['Persentase'] = (burnout_melted['Persentase'] * 100).round(2)

        fig_burnout = px.bar(
            burnout_melted,
            x='Institutional_Policy', y='Persentase',
            color='Burnout_Level',
            title='Distribusi Burnout Risk Level per Kebijakan Institusi',
            barmode='group',
            color_discrete_map={
                'Low': '#2ecc71',
                'Medium': '#f39c12',
                'High': '#e74c3c'
            },
            labels={
                'Institutional_Policy': 'Kebijakan',
                'Persentase': 'Persentase (%)',
                'Burnout_Level': 'Burnout Level'
            }
        )
        st.plotly_chart(fig_burnout, use_container_width=True)

    with col2:
        # Bar chart GPA per kebijakan
        gpa_policy = df_filtered.groupby('Institutional_Policy').agg(
            Rata_rata_GPA=('Post_Semester_GPA', 'mean'),
            Rata_rata_GPA_Gap=('GPA_Gap', 'mean')
        ).round(3).reset_index()

        fig_gpa_policy = px.bar(
            gpa_policy,
            x='Institutional_Policy', y='Rata_rata_GPA',
            title='Rata-rata Post GPA per Kebijakan Institusi',
            color='Institutional_Policy',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text=gpa_policy['Rata_rata_GPA'].round(3),
            labels={
                'Institutional_Policy': 'Kebijakan',
                'Rata_rata_GPA': 'Rata-rata GPA'
            }
        )
        fig_gpa_policy.update_traces(textposition='outside')
        fig_gpa_policy.update_layout(showlegend=False, yaxis_range=[0, 4.5])
        st.plotly_chart(fig_gpa_policy, use_container_width=True)

    # Anxiety per kebijakan
    anxiety_policy = df_filtered.groupby('Institutional_Policy').agg(
        Rata_rata_Anxiety=('Anxiety_Level_During_Exams', 'mean')
    ).round(3).reset_index()

    fig_anxiety = px.bar(
        anxiety_policy,
        x='Institutional_Policy', y='Rata_rata_Anxiety',
        title='Rata-rata Anxiety Level per Kebijakan Institusi',
        color='Institutional_Policy',
        color_discrete_sequence=px.colors.qualitative.Set1,
        text=anxiety_policy['Rata_rata_Anxiety'].round(3),
        labels={
            'Institutional_Policy': 'Kebijakan',
            'Rata_rata_Anxiety': 'Rata-rata Anxiety Level'
        }
    )
    fig_anxiety.update_traces(textposition='outside')
    fig_anxiety.update_layout(showlegend=False)
    st.plotly_chart(fig_anxiety, use_container_width=True)

# ============================================================
# TAB 4 — RETENSI PENGETAHUAN
# ============================================================
with tab4:
    st.subheader("📚 Retensi Pengetahuan — Skill Retention vs AI Dependency")

    # Insight Box PB2
    st.info("""
    📌 **Hasil Analisis PB2 — AI Dependency vs Skill Retention**
    - **Korelasi Pearson:** r = -0.0843 (Sangat Lemah, Negatif, Signifikan)
    - **Korelasi Spearman:** ρ = -0.0516 (Sangat Lemah, Negatif, Signifikan)
    - Skor dependency 1–3 memiliki rata-rata retention **75–76**, skor 8–10 turun ke **63–69**
    - 💡 **Insight:** Semakin tinggi ketergantungan AI, semakin rendah retensi pengetahuan — meski hubungannya lemah
    """)

    # Metric Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Korelasi Pearson (r)", "-0.0843", "Negatif Lemah")
    with col2:
        st.metric("Korelasi Spearman (ρ)", "-0.0516", "Negatif Lemah")
    with col3:
        st.metric("Retention Dep.Score 1", "75.997", "vs Dep.10: 63.547")

    col1, col2 = st.columns(2)

    with col1:
        sample_size = min(5000, len(df_filtered))
        fig_retention = px.scatter(
            df_filtered.sample(sample_size, random_state=42),
            x='Perceived_AI_Dependency',
            y='Skill_Retention_Score',
            color='Burnout_Risk_Level',
            color_discrete_map={
                'Low': '#2ecc71',
                'Medium': '#f39c12',
                'High': '#e74c3c'
            },
            title='Perceived AI Dependency vs Skill Retention Score',
            opacity=0.4,
            labels={
                'Perceived_AI_Dependency': 'AI Dependency Score',
                'Skill_Retention_Score': 'Skill Retention Score',
                'Burnout_Risk_Level': 'Burnout Level'
            }
        )
        st.plotly_chart(fig_retention, use_container_width=True)

    with col2:
        retention_dep = df_filtered.groupby('Perceived_AI_Dependency').agg(
            Rata_rata_Retention=('Skill_Retention_Score', 'mean')
        ).round(3).reset_index()

        fig_ret_line = px.line(
            retention_dep,
            x='Perceived_AI_Dependency',
            y='Rata_rata_Retention',
            title='Rata-rata Skill Retention per Skor AI Dependency',
            markers=True,
            labels={
                'Perceived_AI_Dependency': 'AI Dependency Score (1-10)',
                'Rata_rata_Retention': 'Rata-rata Skill Retention'
            }
        )
        fig_ret_line.update_traces(
            line_color='steelblue',
            marker=dict(size=8, color='coral')
        )
        st.plotly_chart(fig_ret_line, use_container_width=True)

# ============================================================
# TAB 5 — POLA AI PER MAJOR (PB4)
# ============================================================
with tab5:
    st.subheader("📐 Pola AI per Major — GPA Gap & Use Case")

    # Insight Box PB4
    st.info("""
    📌 **Hasil Analisis PB4 — Pola AI per Bidang Studi**
    - **STEM** memiliki GPA Gap tertinggi **(+0.217)** dan dominan pakai **Debugging/Troubleshooting (51.7%)**
    - **Business** dominan pakai **Ideation (47.9%)** dengan GPA Gap **(+0.194)**
    - **Humanities** dominan pakai **Copywriting/Drafting (51.9%)** dengan GPA Gap **(+0.198)**
    - **Medical** dominan pakai **Summarizing_Reading (47.9%)** dengan GPA Gap **(+0.201)**
    - **STEM** memiliki proporsi Advanced prompt skill tertinggi **(33.7%)** vs major lain (~25%)
    - 💡 **Insight:** Cara penggunaan AI yang sesuai konteks jurusan berkorelasi dengan peningkatan GPA lebih tinggi
    """)

    col1, col2 = st.columns(2)

    with col1:
        # Bar Chart GPA Gap per Major
        gpa_gap_major = df_filtered.groupby('Major_Category').agg(
            Rata_rata_GPA_Gap=('GPA_Gap', 'mean'),
            Rata_rata_Post_GPA=('Post_Semester_GPA', 'mean')
        ).round(3).sort_values('Rata_rata_GPA_Gap', ascending=False).reset_index()

        fig_gpagap = px.bar(
            gpa_gap_major,
            x='Major_Category', y='Rata_rata_GPA_Gap',
            title='Rata-rata GPA Gap per Bidang Studi',
            color='Major_Category',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text=gpa_gap_major['Rata_rata_GPA_Gap'].round(3),
            labels={
                'Major_Category': 'Bidang Studi',
                'Rata_rata_GPA_Gap': 'Rata-rata GPA Gap'
            }
        )
        fig_gpagap.update_traces(textposition='outside')
        fig_gpagap.update_layout(showlegend=False)
        st.plotly_chart(fig_gpagap, use_container_width=True)

    with col2:
        # Distribusi Use Case per Major
        usecase_major = pd.crosstab(
            df_filtered['Major_Category'],
            df_filtered['Primary_Use_Case'],
            normalize='index'
        ).round(3) * 100

        fig_usecase = px.imshow(
            usecase_major,
            title='Distribusi Primary Use Case per Bidang Studi (%)',
            color_continuous_scale='Blues',
            text_auto='.1f',
            labels={
                'x': 'Primary Use Case',
                'y': 'Bidang Studi',
                'color': '%'
            }
        )
        fig_usecase.update_layout(
            xaxis_tickangle=-20
        )
        st.plotly_chart(fig_usecase, use_container_width=True)

    # Prompt Engineering Skill per Major
    prompt_major = pd.crosstab(
        df_filtered['Major_Category'],
        df_filtered['Prompt_Engineering_Skill'],
        normalize='index'
    ).round(3) * 100

    fig_prompt = px.bar(
        prompt_major.reset_index().melt(
            id_vars='Major_Category',
            var_name='Skill_Level',
            value_name='Persentase'
        ),
        x='Major_Category', y='Persentase',
        color='Skill_Level',
        title='Distribusi Prompt Engineering Skill per Bidang Studi (%)',
        barmode='group',
        color_discrete_map={
            'Beginner': '#e74c3c',
            'Intermediate': '#f39c12',
            'Advanced': '#2ecc71'
        },
        labels={
            'Major_Category': 'Bidang Studi',
            'Persentase': 'Persentase (%)',
            'Skill_Level': 'Skill Level'
        }
    )
    st.plotly_chart(fig_prompt, use_container_width=True)

# ============================================================
# TAB 6 — PROFIL RISIKO (PB5)
# ============================================================
with tab6:
    st.subheader("⚠️ Profil Risiko — Segmentasi AI Dependency & Burnout")

    # Insight Box PB5
    st.info("""
    📌 **Hasil Analisis PB5 — Profiling Burnout Risk (Decision Tree)**
    - **Akurasi Model:** 52% | Feature terpenting: **Weekly_GenAI_Hours (88.6%)**
    - **Low Burnout (2.484 mhs):** Rata-rata 1.87 jam AI/minggu, Light User, mayoritas Business, Junior
    - **Medium Burnout (5.582 mhs):** Rata-rata 6.59 jam AI/minggu, Moderate User, mayoritas STEM, Senior
    - **High Burnout (1.933 mhs):** Rata-rata 22.34 jam AI/minggu, Heavy User, mayoritas STEM, Freshman
    - 💡 **Insight:** Weekly GenAI Hours adalah prediktor burnout terkuat — mahasiswa Heavy User berisiko 3x lebih tinggi
    """)

    # Metric Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Low Burnout", "2.484 mhs", "Avg 1.87 jam AI/minggu")
    with col2:
        st.metric("Medium Burnout", "5.582 mhs", "Avg 6.59 jam AI/minggu")
    with col3:
        st.metric("High Burnout", "1.933 mhs", "Avg 22.34 jam AI/minggu", delta_color="inverse")

    col1, col2 = st.columns(2)

    with col1:
        heatmap_data = pd.crosstab(
            df_filtered['AI_User_Segment'],
            df_filtered['Burnout_Risk_Level']
        )
        fig_heatmap = px.imshow(
            heatmap_data,
            title='Heatmap: AI User Segment vs Burnout Risk Level',
            color_continuous_scale='RdYlGn_r',
            text_auto=True,
            labels={
                'x': 'Burnout Risk Level',
                'y': 'AI User Segment',
                'color': 'Jumlah'
            }
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col2:
        fig_box = px.box(
            df_filtered,
            x='Burnout_Risk_Level',
            y='Perceived_AI_Dependency',
            color='Burnout_Risk_Level',
            category_orders={'Burnout_Risk_Level': ['Low', 'Medium', 'High']},
            color_discrete_map={
                'Low': '#2ecc71',
                'Medium': '#f39c12',
                'High': '#e74c3c'
            },
            title='Distribusi AI Dependency per Burnout Risk Level',
            labels={
                'Burnout_Risk_Level': 'Burnout Risk Level',
                'Perceived_AI_Dependency': 'AI Dependency Score'
            }
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    # Bubble Chart
    risk_major = df_filtered.groupby('Major_Category').agg(
        Pct_High_Burnout=('Burnout_Risk_Level', lambda x: (x == 'High').mean() * 100),
        Avg_AI_Dependency=('Perceived_AI_Dependency', 'mean'),
        Avg_GPA=('Post_Semester_GPA', 'mean')
    ).round(3).reset_index()

    fig_risk = px.scatter(
        risk_major,
        x='Avg_AI_Dependency',
        y='Pct_High_Burnout',
        size='Avg_GPA',
        color='Major_Category',
        title='Profil Risiko per Bidang Studi (Bubble Chart)',
        labels={
            'Avg_AI_Dependency': 'Rata-rata AI Dependency',
            'Pct_High_Burnout': 'Persentase High Burnout (%)',
            'Major_Category': 'Bidang Studi',
            'Avg_GPA': 'Rata-rata GPA'
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
        size_max=40
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    # Feature Importance
    st.markdown("### 🌲 Feature Importance — Decision Tree")
    feature_importance = pd.DataFrame({
        'Fitur': [
            'Weekly_GenAI_Hours',
            'Year_of_Study_Graduate',
            'Institutional_Policy_Strict_Ban',
            'Year_of_Study_Senior',
            'Pre_Semester_GPA',
            'Post_Semester_GPA',
            'Perceived_AI_Dependency'
        ],
        'Importance': [0.886, 0.065, 0.031, 0.010, 0.003, 0.003, 0.002]
    })

    fig_importance = px.bar(
        feature_importance,
        x='Importance', y='Fitur',
        orientation='h',
        title='Feature Importance — Decision Tree Burnout Risk',
        color='Importance',
        color_continuous_scale='Reds',
        text=feature_importance['Importance'].round(3)
    )
    fig_importance.update_traces(textposition='outside')
    fig_importance.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_importance, use_container_width=True)

    # Decision Tree Image
    st.markdown("### 🌳 Visualisasi Pohon Keputusan")
    if os.path.exists('pb5_decision_tree_final_kerangka.png'):
        img = Image.open('pb5_decision_tree_final_kerangka.png')
        st.image(img, caption='Pohon Keputusan — Profiling Burnout Risk Mahasiswa', use_column_width=True)
    else:
        st.warning("⚠️ File gambar decision tree belum diupload ke repository!")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 0.85rem;'>
    📊 Dashboard BI — AI Impact on Students | 
    Divisi Riset & Kebijakan | 
    Konsultan Pendidikan Tinggi Internasional
    </div>
    """,
    unsafe_allow_html=True
)
