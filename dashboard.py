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
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
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

    # Derived variables (jaga-jaga kalau belum ada)
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

# Filter Major
major_options = ['Semua'] + sorted(df['Major_Category'].dropna().unique().tolist())
selected_major = st.sidebar.selectbox("📚 Bidang Studi", major_options)

# Filter Year of Study
year_options = ['Semua'] + ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
selected_year = st.sidebar.selectbox("🎓 Jenjang Studi", year_options)

# Filter Institutional Policy
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
    delta_gpa = avg_gpa - avg_gpa_all
    st.metric(
        label="📈 Rata-rata Post GPA",
        value=f"{avg_gpa:.3f}",
        delta=f"{delta_gpa:+.3f} vs total"
    )

with col2:
    avg_retention = df_filtered['Skill_Retention_Score'].mean()
    avg_retention_all = df['Skill_Retention_Score'].mean()
    delta_retention = avg_retention - avg_retention_all
    st.metric(
        label="🧠 Rata-rata Skill Retention",
        value=f"{avg_retention:.2f}",
        delta=f"{delta_retention:+.2f} vs total"
    )

with col3:
    pct_high_burnout = (df_filtered['Burnout_Risk_Level'] == 'High').mean() * 100
    pct_high_burnout_all = (df['Burnout_Risk_Level'] == 'High').mean() * 100
    delta_burnout = pct_high_burnout - pct_high_burnout_all
    st.metric(
        label="🔥 High Burnout Risk",
        value=f"{pct_high_burnout:.1f}%",
        delta=f"{delta_burnout:+.1f}% vs total",
        delta_color="inverse"
    )

with col4:
    total_mahasiswa = len(df_filtered)
    st.metric(
        label="👥 Total Mahasiswa",
        value=f"{total_mahasiswa:,}",
        delta=f"{total_mahasiswa - len(df):,} dari filter"
    )

st.markdown("---")

# ============================================================
# TAB NAVIGASI
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🤖 Dampak AI",
    "🧠 Kesehatan Mental",
    "📚 Retensi Pengetahuan",
    "⚠️ Profil Risiko"
])

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================
with tab1:
    st.subheader("📊 Overview — Distribusi Mahasiswa")
    st.markdown(f"Menampilkan data **{len(df_filtered):,}** mahasiswa sesuai filter yang dipilih.")

    col1, col2 = st.columns(2)

    with col1:
        # Pie Chart per Major
        major_dist = df_filtered['Major_Category'].value_counts().reset_index()
        major_dist.columns = ['Major', 'Jumlah']
        fig_major = px.pie(
            major_dist, values='Jumlah', names='Major',
            title='Distribusi Mahasiswa per Bidang Studi',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_major.update_traces(textposition='inside', textinfo='percent+label')
        fig_major.update_layout(showlegend=True)
        st.plotly_chart(fig_major, use_container_width=True)

    with col2:
        # Bar Chart per Year of Study
        year_order = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
        year_dist = df_filtered['Year_of_Study'].value_counts().reindex(year_order).reset_index()
        year_dist.columns = ['Jenjang', 'Jumlah']
        fig_year = px.bar(
            year_dist, x='Jenjang', y='Jumlah',
            title='Distribusi Mahasiswa per Jenjang Studi',
            color='Jumlah',
            color_continuous_scale='Blues',
            text='Jumlah'
        )
        fig_year.update_traces(textposition='outside')
        fig_year.update_layout(showlegend=False, xaxis_title='Jenjang', yaxis_title='Jumlah')
        st.plotly_chart(fig_year, use_container_width=True)

    # Bar Chart per Kebijakan
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

    col1, col2 = st.columns(2)

    segment_order = ['Light', 'Moderate', 'Heavy']
    gpa_segment = df_filtered.groupby('AI_User_Segment', observed=True).agg(
        Rata_rata_GPA=('Post_Semester_GPA', 'mean'),
        Rata_rata_GPA_Gap=('GPA_Gap', 'mean'),
        Jumlah=('Post_Semester_GPA', 'count')
    ).reindex(segment_order).reset_index()

    with col1:
        # Bar Chart GPA per Segmen
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
            labels={
                'AI_User_Segment': 'Segmen',
                'Rata_rata_GPA': 'Rata-rata GPA'
            }
        )
        fig_segment.update_traces(textposition='outside')
        fig_segment.update_layout(showlegend=False, yaxis_range=[0, 4.5])
        st.plotly_chart(fig_segment, use_container_width=True)

    with col2:
        # Bar Chart GPA Gap per Segmen
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
            labels={
                'AI_User_Segment': 'Segmen',
                'Rata_rata_GPA_Gap': 'GPA Gap'
            }
        )
        fig_gap.update_traces(textposition='outside')
        fig_gap.update_layout(showlegend=False)
        st.plotly_chart(fig_gap, use_container_width=True)

    # Scatter Plot
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
        trendline='ols',
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

    col1, col2 = st.columns(2)

    with col1:
        # Distribusi Burnout per Kebijakan
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
            x='Institutional_Policy',
            y='Persentase',
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
        # Rata-rata Anxiety per Kebijakan
        anxiety_policy = df_filtered.groupby('Institutional_Policy').agg(
            Rata_rata_Anxiety=('Anxiety_Level_During_Exams', 'mean')
        ).round(3).reset_index()

        fig_anxiety = px.bar(
            anxiety_policy,
            x='Institutional_Policy',
            y='Rata_rata_Anxiety',
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

    col1, col2 = st.columns(2)

    with col1:
        # Scatter Plot
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
            trendline='ols',
            opacity=0.4,
            labels={
                'Perceived_AI_Dependency': 'AI Dependency Score',
                'Skill_Retention_Score': 'Skill Retention Score',
                'Burnout_Risk_Level': 'Burnout Level'
            }
        )
        st.plotly_chart(fig_retention, use_container_width=True)

    with col2:
        # Line Chart Retention per Dependency
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
# TAB 5 — PROFIL RISIKO
# ============================================================
with tab5:
    st.subheader("⚠️ Profil Risiko — Segmentasi AI Dependency & Burnout")

    col1, col2 = st.columns(2)

    with col1:
        # Heatmap
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
        # Boxplot
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

    # Bubble Chart Profil Risiko per Major
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
