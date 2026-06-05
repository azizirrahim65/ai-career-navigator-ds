import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import ast

# ================= 1. KONFIGURASI HALAMAN & TEMA =================
st.set_page_config(
    page_title="Job Market EDA Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS (Tema Sidebar Krem & Utama Abu Terang)
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Background Dashboard Utama (Abu Terang) */
    [data-testid="stAppViewContainer"] {
        background-color: #F1F5F9; 
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    /* Warna teks default utama */
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h3 {
        color: #1E293B; 
    }

    /* Background Sidebar (Krem) */
    [data-testid="stSidebar"] {
        background-color: #FFF8DC; 
    }
    
    /* Warna teks di Sidebar */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] .stWidgetLabel p {
        color: #1E293B !important;
    }

    /* Desain Kartu Insight */
    .insight-card {
        background-color: #FFFFFF; 
        border-left: 5px solid #0284c7;
        padding: 18px;
        border-radius: 8px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .question-title {
        color: #0369a1 !important;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .insight-text {
        color: #334155 !important;
        font-size: 15px;
        line-height: 1.5;
    }
    
    /* Teks Judul KPI / Info */
    .kpi-title {
        color: #0284c7;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 5px;
    }
    .kpi-subtitle {
        color: #475569;
        font-size: 13px;
        margin-bottom: 15px;
    }
    
    /* st.metric */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #0284C7 !important; 
    }
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important; 
    }
</style>
""", unsafe_allow_html=True)

sns.set_theme(style="whitegrid")
PALETTE_PRIMARY = ["#0284c7", "#38bdf8", "#0ea5e9", "#7dd3fc", "#bae6fd"]

# ================= 2. DATA LOADING & PREPROCESSING =================
@st.cache_data
def load_data():
    df = pd.read_csv('dataset/cleaned_dataset_job.csv')
    
    # Preprocessing kolom skills (mengubah string array menjadi list python asli)
    def parse_skills(skill_str):
        try:
            return ast.literal_eval(skill_str)
        except (ValueError, SyntaxError):
            return []
            
    df['parsed_skills'] = df['skills'].apply(parse_skills)
    
    # Standarisasi Kapitalisasi Kolom Teks
    if 'job_title' in df.columns:
        df['job_title'] = df['job_title'].str.title()
        
    return df

try:
    job_df = load_data()
except FileNotFoundError:
    st.error("Dataset 'cleaned_dataset_job.csv' tidak ditemukan! Pastikan file berada di folder yang sama.")
    st.stop()


# ================= 3. SIDEBAR CONTROLS (FILTER) =================
st.sidebar.image("img/logo.png", width=500)
st.sidebar.image("img/image.png", width=500)
st.sidebar.title("Control Panel")

df_filtered = job_df.copy()

# Filter Tingkat Pengalaman
if 'experience_level' in job_df.columns:
    st.sidebar.subheader("Tingkat Pengalaman")
    exp_levels = sorted([str(x) for x in job_df['experience_level'].dropna().unique()])
    selected_exp = st.sidebar.multiselect("Pilih Experience Level:", options=exp_levels)
    if selected_exp:
        df_filtered = df_filtered[df_filtered['experience_level'].isin(selected_exp)]

# Filter Tipe Pekerjaan
if 'job_type' in job_df.columns:
    st.sidebar.subheader("Tipe Pekerjaan")
    job_types = sorted([str(x) for x in job_df['job_type'].dropna().unique()])
    selected_type = st.sidebar.multiselect("Pilih Job Type:", options=job_types)
    if selected_type:
        df_filtered = df_filtered[df_filtered['job_type'].isin(selected_type)]


# ================= 4. MAIN HEADER =================
st.title("Career & Skills EDA Dashboard")
st.markdown("Analisis data lowongan pekerjaan terkini untuk memahami permintaan industri, distribusi peran (role), dan pemetaan keahlian spesifik yang paling dicari oleh perusahaan.")

# KPI Metrik Teratas
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
total_jobs = len(df_filtered)
unique_companies = df_filtered['company'].nunique() if 'company' in df_filtered.columns else 0
unique_titles = df_filtered['job_title'].nunique() if 'job_title' in df_filtered.columns else 0

# Hitung rasio full-time
full_time_pct = 0
if 'job_type' in df_filtered.columns and total_jobs > 0:
    full_time_count = len(df_filtered[df_filtered['job_type'].str.contains('Full Time', case=False, na=False)])
    full_time_pct = (full_time_count / total_jobs) * 100

kpi1.metric(label="Total Lowongan Kerja", value=f"{total_jobs:,}")
kpi2.metric(label="Total Perusahaan Aktif", value=f"{unique_companies:,}")
kpi3.metric(label="Variasi Posisi (Role)", value=f"{unique_titles:,}")
kpi4.metric(label="Rasio Pekerjaan Penuh Waktu", value=f"{full_time_pct:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ================= 5. INTERACTIVE TABS LAYOUT =================
tab1, tab2, tab3,tab4 = st.tabs([
    "Overview & Deskripsi Data", 
    "Distribusi Peran & Pengalaman", 
    "Pemetaan Keahlian (Skills)",
    "Roadmap Skill"
])

# ----- TAB 1: OVERVIEW DATA -----
with tab1:
    st.subheader("Preview Dataset Lowongan Pekerjaan")
    st.dataframe(df_filtered.drop(columns=['parsed_skills']), use_container_width=True, height=350)
    
    
    st.markdown(f"""
        <div class="insight-card" style="border-left-color: #14b8a6; margin-top:0;">
            <div class="question-title">Deskripsi Dataset</div>
            <div class="insight-text">
                Dataset lowongan pekerjaan (<i>Job Dataset</i>) ini berisi <b>{total_jobs} baris data</b> berdasarkan parameter Anda.<br><br>
                Data ini mencakup informasi mengenai <b>{unique_companies} perusahaan</b> yang sedang membuka peluang karir, beserta tingkat pengalaman yang dibutuhkan dan daftar *skill* teknis yang disyaratkan. Ini sangat krusial untuk pemodelan tren pasar tenaga kerja.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ----- TAB 2: PERAN & PENGALAMAN -----
with tab2:
    st.subheader("Analisis Distribusi Tingkat Pengalaman & Pekerjaan")
    st.markdown("### Bagaimana distribusi tingkat pengalaman pada lowongan kerja?")
    if df_filtered.empty:
        st.warning("Tidak ada data untuk ditampilkan. Sesuaikan filter di Sidebar.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'experience_level' in df_filtered.columns:
                fig1, ax1 = plt.subplots(figsize=(6, 4))
                order_exp = df_filtered['experience_level'].value_counts().index
                sns.countplot(data=df_filtered, y='experience_level', order=order_exp, ax=ax1, palette="viridis")
                ax1.set_title("Kebutuhan Tingkat Pengalaman (Experience Level)", weight='bold')
                ax1.set_xlabel("Jumlah Lowongan")
                ax1.set_ylabel("")
                st.pyplot(fig1)
                
                # Variabel Dinamis
                top_exp = order_exp[0] if len(order_exp) > 0 else "N/A"
            else:
                st.info("Kolom 'experience_level' tidak ditemukan.")
                top_exp = "N/A"
                
        with col2:
            if 'job_title' in df_filtered.columns:
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                df_filtered['job_title'].value_counts().head(10).sort_values().plot(kind='barh', ax=ax2, color="#0ea5e9")
                ax2.set_title("Top 10 Posisi Lowongan Terbanyak", weight='bold')
                ax2.set_xlabel("Frekuesnsi Lowongan")
                st.pyplot(fig2)
                
                # Variabel Dinamis
                top_job = df_filtered['job_title'].mode()[0] if not df_filtered['job_title'].empty else "N/A"
            else:
                st.info("Kolom 'job_title' tidak ditemukan.")
                top_job = "N/A"
                
        st.markdown(f"""
        <div class="insight-card">
            <div class="question-title">Target Demografi Industri Saat Ini</div>
            <hr style='margin: 10px 0; border: 0; border-top: 1px solid #e2e8f0;'>
            <div class="insight-text">💡 <b>Insight Eksploratif (Dinamis):</b> <br>
            Berdasarkan data yang disajikan, mayoritas lowongan saat ini ditargetkan untuk kalangan pekerja dengan tingkat pengalaman <b>{top_exp}</b>.<br><br>
            Posisi karir (Role) yang menempati peringkat tertinggi dalam permintaan industri (<i>High Demand</i>) adalah <b>{top_job}</b>. Tingginya kebutuhan pada peran tersebut mengindikasikan pergeseran tren atau kebutuhan massal industri di ranah tersebut. Profil pelamar sangat disarankan untuk mempersiapkan portofolio ke arah posisi top 10 di atas.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ----- TAB 3: PEMETAAN KEAHLIAN (SKILLS) -----
with tab3:
    st.subheader("Analisis Kebutuhan Keahlian Utama (Core Skills)")
    st.markdown("### Skill teknis apa yang paling sering muncul pada lowongan kerja?")
    if df_filtered.empty:
        st.warning("Tidak ada data untuk ditampilkan. Sesuaikan filter di Sidebar.")
    else:
        # Ekstraksi dan Perhitungan Frekuensi Skill
        all_skills_list = []
        for skills in df_filtered['parsed_skills']:
            if isinstance(skills, list):
                for skill in skills:
                    all_skills_list.append(str(skill).strip().lower())
                    
        if all_skills_list:
            col3, col4 = st.columns([3, 2])
            
            skill_counter = Counter(all_skills_list)
            top_20_skills = skill_counter.most_common(20)
            skills_df = pd.DataFrame(top_20_skills, columns=['Skill', 'Frekuensi Kemunculan'])
            
            with col3:
                fig3, ax3 = plt.subplots(figsize=(8, 6))
                sns.barplot(x='Frekuensi Kemunculan', y='Skill', data=skills_df, ax=ax3, palette="mako")
                ax3.set_title("Top 20 Keahlian Paling Dicari Perusahaan", weight='bold')
                st.pyplot(fig3)
                
            with col4:
                st.markdown("### Proporsi Tipe Lowongan (Job Type)")
                if 'job_type' in df_filtered.columns:
                    fig4, ax4 = plt.subplots(figsize=(5, 5))
                    job_type_counts = df_filtered['job_type'].value_counts()
                    ax4.pie(job_type_counts, labels=job_type_counts.index, autopct='%1.1f%%', startangle=90, colors=PALETTE_PRIMARY)
                    st.pyplot(fig4)
                
            # Mengambil top 3 skill untuk teks dinamis
            top_3_skills = [x.title() for x in skills_df['Skill'].head(3)]
            skills_str = ", ".join(top_3_skills)
            
            st.markdown(f"""
            <div class="insight-card">
                <div class="question-title">Kesenjangan Kompetensi dan Kebutuhan Teknis</div>
                <hr style='margin: 10px 0; border: 0; border-top: 1px solid #e2e8f0;'>
                <div class="insight-text"><b>Insight Eksploratif (Dinamis):</b> <br>
                Dari total ekstraksi ribuan data lowongan terfilter, tiga kompetensi paling dominan yang bersifat wajib dimiliki oleh pelamar adalah <b>{skills_str}</b>.<br><br>
                Keahlian-keahlian fundamental inilah yang sering kali menjadi filter utama <i>Applicant Tracking System (ATS)</i> yang digunakan perusahaan. Jika sistem <i>AI Career Navigator</i> digunakan pada data ini, sistem akan mengidentifikasi jika pengguna tidak memiliki {top_3_skills[0]} di profil mereka, lalu otomatis merekomendasikan kursus pembelajaran yang berkaitan dengan {top_3_skills[0]}.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Data kolom keahlian (skills) tidak tersedia pada data yang difilter.")
            
# ----- TAB 4: SKILL ROADMAP (ROLE SPESIFIK) -----
with tab4:
    st.markdown("### Skill apa yang perlu dipelajari user untuk mencapai role tertentu?")
    st.write("Silakan pilih target posisi (Role) idaman di bawah ini untuk melihat *mapping skill* spesifik yang wajib dikuasai.")
    
    if df_filtered.empty or 'job_title' not in df_filtered.columns:
        st.warning("⚠️ Data tidak mencukupi untuk analisis roadmap. Cek kembali filter Anda.")
    else:
        # Mengambil daftar role yang paling umum (minimal muncul lebih dari 1 kali)
        role_counts = df_filtered['job_title'].value_counts()
        valid_roles = role_counts[role_counts >= 1].index.tolist()
        
        if not valid_roles:
            st.info("Tidak ada role spesifik yang memenuhi syarat tampilan.")
        else:
            col_sel, _ = st.columns([2, 1])
            with col_sel:
                selected_role = st.selectbox("🎯 Pilih Target Karir (Role):", options=valid_roles)
                
            # Memfilter dataset HANYA untuk role yang dipilih
            role_df = df_filtered[df_filtered['job_title'] == selected_role]
            
            role_skills = []
            for skills in role_df['parsed_skills']:
                if isinstance(skills, list):
                    role_skills.extend([str(s).strip().title() for s in skills])
                    
            if role_skills:
                col_chart, col_insight = st.columns([3, 2])
                
                role_skill_counts = Counter(role_skills).most_common(12)
                r_skills_df = pd.DataFrame(role_skill_counts, columns=['Skill', 'Frekuensi Kebutuhan'])
                
                with col_chart:
                    fig_role, ax_role = plt.subplots(figsize=(8, 5))
                    sns.barplot(x='Frekuensi Kebutuhan', y='Skill', data=r_skills_df, ax=ax_role, palette="magma")
                    ax_role.set_title(f"Top 12 Skill Wajib untuk: {selected_role}", weight='bold')
                    st.pyplot(fig_role)
                    
                # Insight Text Khusus Role
                top_req_skills = ", ".join([x[0] for x in role_skill_counts[:5]])
                with col_insight:
                    st.markdown(f"""
                    <div class="insight-card" style="border-left-color: #8b5cf6;">
                        <div class="question-title">Roadmap Pembelajaran: {selected_role}</div>
                        <div class="insight-text">
                        <b>Analisis Kebutuhan Role:</b><br>
                        Untuk berhasil lolos menjadi seorang <b>{selected_role}</b>, seorang kandidat (user) sangat direkomendasikan untuk memprioritaskan pemelajaran pada pilar utama ini: <b>{top_req_skills}</b>.<br><br>
                        Grafik di samping menampilkan anatomi keahlian yang secara khusus di-*query* dari {len(role_df)} perusahaan yang membuka posisi ini. Menguasai skill teratas dari daftar ini (berada di bagian atas grafik batang) akan meminimalisasi *skill gap* secara signifikan saat berhadapan dengan HRD.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"Belum ada deskripsi spesifik mengenai skill untuk role {selected_role} pada data ini.")