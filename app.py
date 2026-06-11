import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA GELAP
# ==========================================
st.set_page_config(
    page_title="Diabetes Diagnosis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0b132b; color: #ffffff; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px !important; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #8ba0b4 !important; font-size: 14px !important; }
    .card-risk {
        background-color: #1c2541; padding: 20px; border-radius: 10px; 
        border-left: 5px solid #e63946; margin-bottom: 15px;
    }
    .card-normal {
        background-color: #1c2541; padding: 20px; border-radius: 10px; 
        border-left: 5px solid #2a9d8f; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI DATABASE LOKAL (CSV)
# ==========================================
DB_FILE = "db_pasien.csv"

# Fungsi untuk memuat data dari CSV
def load_database():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        # Membuat kerangka data baru jika file belum ada
        return pd.DataFrame(columns=[
            "Waktu Input", "ID Pasien", "Nama Pasien", "Usia", 
            "Gender", "BMI", "HbA1c", "Glukosa", "BP", "Diagnosis", "Probabilitas"
        ])

# Fungsi untuk menyimpan data baru ke CSV
def save_to_database(new_row):
    df = load_database()
    # Menggunakan pd.concat untuk menambahkan baris baru
    df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# ==========================================
# 3. SIDEBAR: FORM INPUT INTERAKTIF & TOMBOL SIMPAN
# ==========================================
with st.sidebar:
    st.markdown("### 👩‍⚕️ dr. Ryuwan W.D")
    st.caption("Mei 26, 2026")
    st.markdown("---")
    
    st.markdown("### 📝 INPUT DATA PASIEN")
    nama_pasien = st.text_input("Nama Pasien", value="John Smith")
    usia = st.number_input("Usia (Tahun)", min_value=1, max_value=120, value=54)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    id_pasien = st.text_input("ID Pasien", value="P12345")
    
    st.markdown("---")
    bmi = st.slider("Indeks Massa Tubuh (BMI)", min_value=10.0, max_value=50.0, value=30.8, step=0.1)
    hba1c = st.slider("Kadar HbA1c (%)", min_value=4.0, max_value=15.0, value=7.1, step=0.1)
    glukosa = st.slider("Fasting Glucose (mg/dL)", min_value=50, max_value=300, value=140)
    
    st.markdown("**Tekanan Darah (BP)**")
    col_bp1, col_bp2 = st.columns(2)
    sistolik = col_bp1.number_input("Sistolik", min_value=70, max_value=200, value=135)
    diastolik = col_bp2.number_input("Diastolik", min_value=40, max_value=130, value=88)

    # ==========================================
    # LOGIKA PREDIKSI & PROBABILITAS
    # ==========================================
    skor_risiko = 1
    if hba1c >= 6.5: skor_risiko += 1
    if glukosa >= 126: skor_risiko += 1
    if bmi >= 30.0: skor_risiko += 1
    if usia >= 45: skor_risiko += 1

    base_prob = (hba1c / 15.0) * 40 + (glukosa / 300.0) * 35 + (bmi / 50.0) * 25
    probabilitas = min(round(base_prob, 1), 100.0)
    is_high_risk = skor_risiko >= 3 or hba1c >= 6.5 or glukosa >= 126
    hasil_diagnosis = "HIGH RISK" if is_high_risk else "NORMAL"

    st.markdown("---")
    # TOMBOL SIMPAN DATA PASIEN
    if st.button("💾 Simpan Data Pasien", use_container_width=True, type="primary"):
        data_baru = {
            "Waktu Input": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ID Pasien": id_pasien,
            "Nama Pasien": nama_pasien,
            "Usia": usia,
            "Gender": gender,
            "BMI": bmi,
            "HbA1c": f"{hba1c}%",
            "Glukosa": f"{glukosa} mg/dL",
            "BP": f"{sistolik}/{diastolik}",
            "Diagnosis": hasil_diagnosis,
            "Probabilitas": f"{probabilitas}%"
        }
        save_to_database(data_baru)
        st.success(f"Sukses! Data {nama_pasien} berhasil disimpan ke database.")

# ==========================================
# 4. HEADER UTAMA DASBOR
# ==========================================
st.markdown("<h2 style='color:#ffffff; margin-bottom: 0;'>DIABETES DIAGNOSIS & MONITORING DASHBOARD | <span style='color:#4ea8de;'>ML MODEL</span></h2>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1.2, 1.2, 1.1])

# ==========================================
# KOLOM 1: PATIENT OVERVIEW & GLUCOSE TRENDS
# ==========================================
with col1:
    st.markdown("### PATIENT OVERVIEW")
    with st.container(border=True):
        sub_c1, sub_c2 = st.columns([3, 1])
        with sub_c1:
            st.image("https://w3schools.com", width=65)
        with sub_c2:
            st.markdown(f"<h4 style='margin:0;'>{nama_pasien}</h4>", unsafe_allow_html=True)
            st.caption(f"{usia}, {'M' if gender=='Laki-laki' else 'F'} | ID: {id_pasien}")
            
        st.markdown("---")
        m1, m2 = st.columns(2)
        m1.metric(label="BMI", value=f"{bmi}")
        m2.metric(label="HbA1c", value=f"{hba1c} %")
        m3, m4 = st.columns(2)
        m3.metric(label="Fasting Glucose", value=f"{glukosa} mg/dL")
        m4.metric(label="Blood Pressure", value=f"{sistolik}/{diastolik}")

    st.markdown("### GLUCOSE TRENDS (LAST 6 MONTHS)")
    bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    nilai_glukosa = [110, 105, 142, 100, 130, glukosa]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=bulan, y=nilai_glukosa, mode='lines+markers', line=dict(color='#4ea8de', width=3)))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=20), height=180, font=dict(color="white"),
        yaxis=dict(gridcolor='#1c2541'), xaxis=dict(gridcolor='#1c2541')
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# KOLOM 2: ML PREDICTION STATUS & RECOMMENDATIONS
# ==========================================
with col2:
    st.markdown("### MACHINE LEARNING PREDICTION STATUS")
    if is_high_risk:
        st.markdown(f"""
            <div class="card-risk">
                <span style="color:#8ba0b4; font-size:12px;">PREDICTION RESULT:</span><br>
                <strong style="color:#e63946; font-size:22px;">DIABETES RISK DETECTED</strong>
                <span style="background-color:#e63946; color:white; padding:2px 6px; border-radius:3px; font-size:10px; vertical-align:middle; margin-left:10px;">HIGH RISK</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="card-normal">
                <span style="color:#8ba0b4; font-size:12px;">PREDICTION RESULT:</span><br>
                <strong style="color:#2a9d8f; font-size:22px;">NO DIABETES RISK DETECTED</strong>
                <span style="background-color:#2a9d8f; color:white; padding:2px 6px; border-radius:3px; font-size:10px; vertical-align:middle; margin-left:10px;">NORMAL</span>
            </div>
        """, unsafe_allow_html=True)
    
    # PERBAIKAN: Menambahkan nilai range [min, max] untuk indikator gauge
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", 
        value = probabilitas,
        number = {'suffix': "%", 'font': {'color': "white", 'size': 40}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#4ea8de"}, 
            'bgcolor': "#1c2541",
            'steps': [
                {'range': [0, 50], 'color': '#2a9d8f'},    # Contoh: 0-50% Hijau
                {'range': [50, 100], 'color': '#e63946'}   # Contoh: 50-100% Merah
            ],
        }
    )) # PERBAIKAN: Memastikan tanda kurung go.Indicator() tertutup dengan benar
    
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10), height=180, font=dict(color="white"))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown(f"<p style='text-align:center; color:#8ba0b4; margin:0;'>Risk Score: <strong style='color:#f4a261; font-size:20px;'>{skor_risiko}/5</strong></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### RECOMMENDATIONS & ACTION ITEMS")
    if is_high_risk:
        st.markdown("🚨 **Schedule Endocrinologist consultation immediately**")
        st.markdown("🥗 **Initiate strict low-glycemic diet plan**")
    else:
        st.markdown("✅ **Maintain current balanced lifestyle**")
        st.markdown("📈 **Schedule routine annual physical check-up**")

# ==========================================
# KOLOM 3: TOP FACTORS & RECENT PATIENTS
# ==========================================
with col3:
    st.markdown("### TOP PREDICTION FACTORS")
    faktor = ['HbA1c', 'Glucose', 'BMI', 'Age', 'Family History']
    persentase = [22, 18, 16, 12, 10]
    
    fig_bar = go.Figure(go.Bar(x=faktor, y=persentase, text=[f"{p}%" for p in persentase], textposition='auto', marker_color='#4ea8de'))
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10), height=200, font=dict(color="white"), yaxis=dict(visible=False))
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # MENAMPILKAN RIWAYAT DATA YANG TERSIMPAN DI DATABASE
    st.markdown("### RECENT PATIENT RESULTS (DATABASE)")
    df_db = load_database()
    if not df_db.empty:
        # Hanya menampilkan beberapa kolom utama agar rapi di tabel samping
        st.dataframe(df_db[["Nama Pasien", "Diagnosis", "Probabilitas"]].head(5), hide_index=True, use_container_width=True)
    else:
        st.caption("Belum ada data pasien yang disimpan.")

# ==========================================
# 5. TABEL DATABASE LENGKAP DI BAGIAN BAWAH DASBOR
# ==========================================