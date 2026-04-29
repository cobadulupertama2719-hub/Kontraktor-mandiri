# app.py - ARKI ESTIMATOR PRO (Streamlit Version)
# Simpan file ini dengan nama app.py

import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import json

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="ARKI ESTIMATOR PRO",
    page_icon="🏗️",
    layout="wide"
)

# ==================== CSS CUSTOM ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    .success-box {
        background: #22c55e20;
        color: #22c55e;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
    }
    .total-card {
        background: #1a3a5c;
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: #22c55e; margin:0;">🏗️ ARKI ESTIMATOR PRO</h1>
    <p style="color: #94a3b8; margin:5px 0 0 0;">20 Komponen Lengkap | Perhitungan Presisi</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR INPUT ====================
with st.sidebar:
    st.markdown("## 📐 INPUT DATA")
    
    st.markdown("### 🏠 Dimensi Bangunan")
    panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5)
    tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1)
    lantai = st.number_input("Jumlah Lantai", min_value=1, max_value=5, value=1, step=1)
    
    st.markdown("### 🛏️ Jumlah Ruangan")
    col1, col2 = st.columns(2)
    with col1:
        kamar = st.number_input("Kamar Tidur", min_value=0, max_value=10, value=3, step=1)
        ruang_tamu = st.number_input("Ruang Tamu", min_value=0, max_value=3, value=1, step=1)
    with col2:
        km = st.number_input("Kamar Mandi", min_value=0, max_value=5, value=2, step=1)
        dapur = st.number_input("Dapur", min_value=0, max_value=2, value=1, step=1)
    garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0, step=1)
    
    st.markdown("### 🔧 Material & Spek")
    col1, col2 = st.columns(2)
    with col1:
        jenis_atap = st.selectbox("Jenis Atap", ["metal", "tanah", "beton"], 
                                   format_func=lambda x: "Metal" if x=="metal" else "Tanah" if x=="tanah" else "Beton")
        rangka_atap = st.selectbox("Rangka Atap", ["baja", "kayu"],
                                    format_func=lambda x: "Baja Ringan" if x=="baja" else "Kayu")
    with col2:
        jenis_bata = st.selectbox("Jenis Bata", ["merah", "hebel"],
                                   format_func=lambda x: "Bata Merah" if x=="merah" else "Bata Ringan")
        ukuran_besi = st.selectbox("Ukuran Besi", [10, 13, 16], format_func=lambda x: f"Ø{x} mm")
    
    st.markdown("### 👷 Tenaga Kerja")
    col1, col2 = st.columns(2)
    with col1:
        upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000)
    with col2:
        upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000)
    
    st.markdown("### 🏡 Opsional")
    col1, col2 = st.columns(2)
    with col1:
        kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0, step=1)
    with col2:
        pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0, step=1)


# ==================== FUNGSI PERHITUNGAN ====================

def hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi):
    if lantai == 1:
        kp = math.ceil(panjang / 5.5) + 1
        kl = math.ceil(lebar / 5.5) + 1
        jumlah_titik = kp * kl
        ukuran = 0.5
        tebal = 0.2
        jarak = "5-6 meter (penghematan)"
    elif lantai == 2:
        kp = math.floor(panjang / 3) + 1
        kl = math.floor(lebar / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.7
        tebal = 0.25
        jarak = "3 meter (wajib)"
    else:
        kp = math.floor(panjang / 3) + 1
        kl = math.floor(lebar / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.9
        tebal = 0.3
        jarak = "3 meter"
    
    volume_per_titik = ukuran * ukuran * tebal
    volume_total = jumlah_titik * volume_per_titik
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    panjang_besi_per_titik = (ukuran * 4) * 10
    berat_besi = (panjang_besi_per_titik * jumlah_titik) * berat_per_meter
    batang_besi = math.ceil((panjang_besi_per_titik * jumlah_titik) / 12)
    
    return {
        'jumlah_titik': jumlah_titik, 'jarak': jarak,
        'ukuran_cm': ukuran * 100, 'tebal_cm': tebal * 100,
        'volume_m3': round(volume_total, 2),
        'semen_sak': math.ceil(volume_total * 8),
        'pasir_m3': round(volume_total * 0.65, 2),
        'split_m3': round(volume_total * 0.85, 2),
        'besi_kg': round(berat_besi, 1),
        'besi_batang': batang_besi
    }


def get_layout(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi):
    layout = []
    y = 0.5
    
    if kamar > 0:
        lebar_kt = (panjang - 1) / kamar
        for i in range(1, kamar + 1):
            layout.append({'nama': f'KT {i}', 'x': 0.5 + (i-1)*lebar_kt, 'y': y, 'w': lebar_kt, 'h': 3})
    
    y += 3.2
    if ruang_tamu > 0:
        layout.append({'nama': 'Ruang Tamu', 'x': 0.5, 'y': y, 'w': panjang/2, 'h': 3})
    if dapur > 0:
        layout.append({'nama': 'Dapur', 'x': panjang/2 + 0.5, 'y': y, 'w': panjang/2 - 1, 'h': 3})
    
    y += 3.2
    for i in range(1, km + 1):
        layout.append({'nama': f'KM {i}', 'x': 0.5 + (i-1)*2.5, 'y': y, 'w': 2, 'h': 2})
    
    if garasi > 0:
        layout.append({'nama': 'Garasi', 'x': panjang - 3.5, 'y': y, 'w': 3, 'h': 2.5})
    
    return layout


def hitung_dinding_presisi(layout, tinggi):
    sisi_dihitung = set()
    total_luas = 0
    jumlah_pintu = 0
    jumlah_jendela = 0
    
    for r in layout:
        kiri = r['x']; kanan = r['x'] + r['w']; atas = r['y']; bawah = r['y'] + r['h']
        
        sisi_kiri = f"kiri,{kiri},{atas},{bawah}"
        if sisi_kiri not in sisi_dihitung:
            total_luas += r['h'] * tinggi
            sisi_dihitung.add(sisi_kiri)
        
        sisi_kanan = f"kanan,{kanan},{atas},{bawah}"
        if sisi_kanan not in sisi_dihitung:
            total_luas += r['h'] * tinggi
            sisi_dihitung.add(sisi_kanan)
        
        sisi_atas = f"atas,{atas},{kiri},{kanan}"
        if sisi_atas not in sisi_dihitung:
            total_luas += r['w'] * tinggi
            sisi_dihitung.add(sisi_atas)
        
        sisi_bawah = f"bawah,{bawah},{kiri},{kanan}"
        if sisi_bawah not in sisi_dihitung:
            total_luas += r['w'] * tinggi
            sisi_dihitung.add(sisi_bawah)
        
        jumlah_pintu += 1
        if "KM" not in r['nama'] and "Garasi" not in r['nama']:
            jumlah_jendela += 1
    
    luas_pintu = jumlah_pintu * (0.9 * 2.1)
    luas_jendela = jumlah_jendela * (1.2 * 1.0)
    luas_bersih = total_luas - luas_pintu - luas_jendela
    
    return {
        'luas_kotor': round(total_luas, 2), 'luas_pintu': round(luas_pintu, 2),
        'luas_jendela': round(luas_jendela, 2), 'luas_bersih': round(luas_bersih, 2),
        'jumlah_pintu': jumlah_pintu, 'jumlah_jendela': jumlah_jendela,
        'bata': math.ceil(luas_bersih * 70),
        'semen_pasang': math.ceil(luas_bersih * 0.3),
        'pasir_pasang': round(luas_bersih * 0.04, 2),
        'semen_plester': math.ceil(luas_bersih * 2 * 0.2),
        'pasir_plester': round(luas_bersih * 2 * 0.025, 2),
        'acian': math.ceil(luas_bersih * 2 * 0.15)
    }


# ==================== MAIN PERHITUNGAN ====================
layout = get_layout(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi)
keliling = 2 * (panjang + lebar)
luas_bangunan = panjang * lebar
luas_total = luas_bangunan * lantai

# KOMPONEN 1: PONDASI
vol_pondasi = keliling * 0.6 * 0.8
komponen_pondasi = {
    'volume': round(vol_pondasi, 2),
    'batu_belah': round(vol_pondasi * 1.2, 2),
    'semen': math.ceil(vol_pondasi * 4.5),
    'pasir': round(vol_pondasi * 0.55, 2)
}

# KOMPONEN 2: SLOOF
vol_sloof = keliling * 0.2 * 0.25
komponen_sloof = {
    'volume': round(vol_sloof, 2),
    'semen': math.ceil(vol_sloof * 8),
    'pasir': round(vol_sloof * 0.65, 2),
    'split': round(vol_sloof * 0.85, 2),
    'besi_kg': round(vol_sloof * 120, 1)
}

# KOMPONEN 3: RING BALOK
vol_ring = keliling * 0.15 * 0.2
komponen_ring = {
    'volume': round(vol_ring, 2),
    'semen': math.ceil(vol_ring * 8),
    'pasir': round(vol_ring * 0.65, 2),
    'split': round(vol_ring * 0.85, 2),
    'besi_kg': round(vol_ring * 120, 1)
}

# KOMPONEN 4: TOTAL STRUKTUR
faktor = 1.3 if (lantai > 1 or jenis_atap != 'metal') else 1
total_beton = (vol_sloof + vol_ring) * faktor
komponen_struktur = {
    'beton': round(total_beton, 2),
    'semen': math.ceil(total_beton * 8),
    'pasir': round(total_beton * 0.65, 2),
    'split': round(total_beton * 0.85, 2),
    'besi_kg': round(total_beton * 120, 1),
    'besi_batang': math.ceil((total_beton * 120) / (12 * (13*13/162)))
}

# KOMPONEN 5: BEKISTING
luas_bekisting = (vol_sloof * 8) + (vol_ring * 6)
komponen_bekisting = {
    'triplek': math.ceil(luas_bekisting * 0.35),
    'kaso': math.ceil(luas_bekisting * 2.5),
    'paku': round(luas_bekisting * 0.2, 1)
}

# KOMPONEN 6: CAKAR AYAM
cakar = hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi)

# KOMPONEN 7: DINDING
dinding = hitung_dinding_presisi(layout, tinggi)

# KOMPONEN 8: ATAP
luas_atap = luas_bangunan * 1.3
genteng_per_m2 = {'metal': 16, 'tanah': 28, 'beton': 10}
genteng = math.ceil(luas_atap * genteng_per_m2[jenis_atap])

# KOMPONEN 9: RANGKA ATAP
if rangka_atap == 'baja':
    komponen_rangka = {
        'jenis': 'Baja Ringan',
        'kanal_c': math.ceil(luas_atap * 4.5),
        'reng': math.ceil(luas_atap * 2.5),
        'sekrup': math.ceil(luas_atap * 12)
    }
else:
    komponen_rangka = {
        'jenis': 'Kayu',
        'kuda2': math.ceil(panjang / 1.5) * 4,
        'gording': math.ceil(panjang * 3),
        'reng': math.ceil(luas_atap * 1.5)
    }

# KOMPONEN 10: PLAFON
komponen_plafon = {
    'gypsum': math.ceil(luas_bangunan * 0.35),
    'hollow': math.ceil(luas_bangunan * 0.8),
    'list': math.ceil(keliling * 1.2)
}

# KOMPONEN 11: KERAMIK
komponen_keramik = {
    'lantai': math.ceil(luas_bangunan * 1.05),
    'dinding_km': km * 6,
    'semen': math.ceil((luas_bangunan + km*6) * 0.3),
    'pasir': round((luas_bangunan + km*6) * 0.03, 2)
}

# KOMPONEN 12: LISTRIK
titik_lampu = len(layout) + 3
komponen_listrik = {
    'lampu': titik_lampu,
    'saklar': math.ceil(titik_lampu * 0.7),
    'kabel': titik_lampu * 8,
    'mcb': 6 if lantai >= 2 else 4
}

# KOMPONEN 13-20
komponen_km = {'closet': km, 'pipa': km * 8, 'wastafel': km}
komponen_dapur = {'kitchen_set': 1 if dapur > 0 else 0}
komponen_cat = {
    'tembok': math.ceil(dinding['luas_bersih'] * 0.12),
    'plafon': math.ceil(luas_bangunan * 0.1),
    'total': math.ceil((dinding['luas_bersih'] * 0.12) + (luas_bangunan * 0.1))
}
komponen_tenaga = {
    'tukang': max(2, math.ceil(luas_total / 25)),
    'kenek': math.ceil(max(2, math.ceil(luas_total / 25)) * 1.2),
    'hari': max(25, math.ceil(luas_total / 3)),
    'biaya': (max(2, math.ceil(luas_total / 25)) * upah_tukang + 
              math.ceil(max(2, math.ceil(luas_total / 25)) * 1.2) * upah_kenek) * max(25, math.ceil(luas_total / 3))
}

# TOTAL REKAP
total_semen = (komponen_pondasi['semen'] + komponen_struktur['semen'] + 
               cakar['semen_sak'] + dinding['semen_pasang'] + 
               dinding['semen_plester'] + komponen_keramik['semen'])

# TOTAL BIAYA
harga = {'semen':65000, 'pasir':300000, 'split':320000, 'bata':800, 'besi':15000,
         'triplek':180000, 'kaso':25000, 'paku':18000, 'genteng_metal':25000,
         'genteng_tanah':5000, 'genteng_beton':12000, 'keramik':90000, 'batu_belah':250000,
         'gypsum':45000, 'hollow':35000, 'list':8000, 'kabel':15000, 'saklar':25000,
         'lampu':45000, 'mcb':75000, 'pintu':500000, 'closet':800000, 'pipa':50000,
         'wastafel':300000, 'cat':35000, 'kitchen_set':3000000, 'kanopi':350000, 'pagar':850000}

total_biaya = (total_semen * harga['semen']) + \
              ((komponen_pondasi['pasir'] + komponen_struktur['pasir'] + cakar['pasir_m3'] + 
                dinding['pasir_pasang'] + dinding['pasir_plester'] + komponen_keramik['pasir']) * harga['pasir']) + \
              ((komponen_struktur['split'] + cakar['split_m3']) * harga['split']) + \
              (komponen_pondasi['batu_belah'] * harga['batu_belah']) + \
              ((komponen_struktur['besi_kg'] + cakar['besi_kg']) * harga['besi']) + \
              (komponen_bekisting['triplek'] * harga['triplek']) + (komponen_bekisting['kaso'] * harga['kaso']) + \
              (komponen_bekisting['paku'] * harga['paku']) + (dinding['bata'] * harga['bata']) + \
              (genteng * harga[f'genteng_{jenis_atap}']) + \
              ((komponen_keramik['lantai'] + komponen_keramik['dinding_km']) * harga['keramik']) + \
              (komponen_plafon['gypsum'] * harga['gypsum']) + (komponen_plafon['hollow'] * harga['hollow']) + \
              (komponen_plafon['list'] * harga['list']) + (komponen_listrik['lampu'] * harga['lampu']) + \
              (komponen_listrik['saklar'] * harga['saklar']) + (komponen_listrik['kabel'] * harga['kabel']) + \
              (komponen_listrik['mcb'] * harga['mcb']) + (dinding['jumlah_pintu'] * harga['pintu']) + \
              (km * harga['closet']) + (km*8 * harga['pipa']) + (km * harga['wastafel']) + \
              (komponen_cat['total'] * harga['cat']) + (komponen_dapur['kitchen_set'] * harga['kitchen_set']) + \
              (kanopi * harga['kanopi']) + (pagar * harga['pagar']) + komponen_tenaga['biaya']


# ==================== TAMPILAN ====================

st.markdown(f"""
<div style="display: flex; gap: 20px; margin-bottom: 20px;">
    <div class="total-card"><h3>{luas_bangunan} m²</h3><p>Luas Bangunan</p></div>
    <div class="total-card"><h3>{cakar['jumlah_titik']} titik</h3><p>Cakar Ayam</p></div>
    <div class="total-card"><h3>{komponen_tenaga['hari']} hari</h3><p>Estimasi Waktu</p></div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📋 20 KOMPONEN", "🏠 DENAH", "📊 RINGKASAN", "💾 EXPORT"])

with tab1:
    st.markdown("## 📋 20 KOMPONEN")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🪨 1. PONDASI BATU KALI", expanded=True):
            st.metric("Volume", f"{komponen_pondasi['volume']} m³")
            st.metric("Batu Belah", f"{komponen_pondasi['batu_belah']} m³")
            st.metric("Semen", f"{komponen_pondasi['semen']} sak")
            st.metric("Pasir", f"{komponen_pondasi['pasir']} m³")
        
        with st.expander("🏗️ 2. SLOOF"):
            st.metric("Volume", f"{komponen_sloof['volume']} m³")
            st.metric("Semen", f"{komponen_sloof['semen']} sak")
            st.metric("Pasir", f"{komponen_sloof['pasir']} m³")
            st.metric("Split", f"{komponen_sloof['split']} m³")
            st.metric("Besi", f"{komponen_sloof['besi_kg']} kg")
        
        with st.expander("🏗️ 3. RING BALOK"):
            st.metric("Volume", f"{komponen_ring['volume']} m³")
            st.metric("Semen", f"{komponen_ring['semen']} sak")
            st.metric("Pasir", f"{komponen_ring['pasir']} m³")
            st.metric("Split", f"{komponen_ring['split']} m³")
            st.metric("Besi", f"{komponen_ring['besi_kg']} kg")
        
        with st.expander("📦 4. TOTAL STRUKTUR"):
            st.metric("Beton", f"{komponen_struktur['beton']} m³")
            st.metric("Semen", f"{komponen_struktur['semen']} sak")
            st.metric("Besi", f"{komponen_struktur['besi_kg']} kg ({komponen_struktur['besi_batang']} batang)")
        
        with st.expander("🪵 5. BEKISTING"):
            st.metric("Triplek", f"{komponen_bekisting['triplek']} lembar")
            st.metric("Kaso", f"{komponen_bekisting['kaso']} batang")
            st.metric("Paku", f"{komponen_bekisting['paku']} kg")
    
    with col2:
        with st.expander("🦶 6. CAKAR AYAM", expanded=True):
            st.metric("Jumlah Titik", f"{cakar['jumlah_titik']} titik")
            st.caption(f"Jarak: {cakar['jarak']}")
            st.metric("Ukuran", f"{cakar['ukuran_cm']}x{cakar['ukuran_cm']} cm")
            st.metric("Volume", f"{cakar['volume_m3']} m³")
            st.metric("Semen", f"{cakar['semen_sak']} sak")
            st.metric("Besi", f"{cakar['besi_kg']} kg ({cakar['besi_batang']} batang)")
        
        with st.expander("🧱 7. DINDING"):
            st.metric("Luas Bersih", f"{dinding['luas_bersih']} m²")
            st.metric(f"Pintu ({dinding['jumlah_pintu']} bh)", f"-{dinding['luas_pintu']} m²")
            st.metric("Bata", f"{dinding['bata']:,} pcs")
            st.metric("Semen Pasang", f"{dinding['semen_pasang']} sak")
            st.metric("Semen Plester", f"{dinding['semen_plester']} sak")
        
        with st.expander("🏠 8. ATAP & RANGKA"):
            st.metric("Luas Atap", f"{luas_atap:.2f} m²")
            st.metric("Genteng", f"{genteng:,} pcs")
            st.markdown(f"**Rangka: {komponen_rangka['jenis']}**")
            if komponen_rangka['jenis'] == 'Baja Ringan':
                st.metric("Kanal C", f"{komponen_rangka['kanal_c']} kg")
                st.metric("Sekrup", f"{komponen_rangka['sekrup']:,} pcs")
        
        with st.expander("✨ 10. PLAFON"):
            st.metric("Gypsum", f"{komponen_plafon['gypsum']} lembar")
            st.metric("Hollow", f"{komponen_plafon['hollow']} batang")
        
        with st.expander("🪨 11. KERAMIK"):
            st.metric("Lantai", f"{komponen_keramik['lantai']} m²")
            st.metric("Dinding KM", f"{komponen_keramik['dinding_km']} m²")

with tab2:
    st.markdown("## 🏠 DENAH RUMAH")
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, panjang)
    ax.set_ylim(0, lebar)
    ax.set_facecolor('#f8fafc')
    warna = ['#fcd34d', '#86efac', '#67e8f9', '#fde047', '#c4b5fd', '#fdba74']
    for i, r in enumerate(layout):
        rect = patches.Rectangle((r['x'], r['y']), r['w'], r['h'], 
                                  linewidth=2, edgecolor='#1e293b', 
                                  facecolor=warna[i % len(warna)], alpha=0.8)
        ax.add_patch(rect)
        ax.text(r['x'] + r['w']/2, r['y'] + r['h']/2, r['nama'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
    ax.set_xlabel("Panjang (m)")
    ax.set_ylabel("Lebar (m)")
    ax.set_title(f"Denah Rumah ({panjang}m x {lebar}m)")
    ax.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig)

with tab3:
    st.markdown("## 📊 RINGKASAN")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Semen", f"{total_semen} sak")
        st.metric("Pasir", f"{komponen_pondasi['pasir'] + komponen_struktur['pasir'] + cakar['pasir_m3'] + dinding['pasir_pasang'] + dinding['pasir_plester'] + komponen_keramik['pasir']:.2f} m³")
        st.metric("Split", f"{komponen_struktur['split'] + cakar['split_m3']:.2f} m³")
    with col2:
        st.metric("Besi", f"{komponen_struktur['besi_kg'] + cakar['besi_kg']:.1f} kg")
        st.metric("Bata", f"{dinding['bata']:,} pcs")
        st.metric("Genteng", f"{genteng:,} pcs")
    with col3:
        st.metric("Keramik", f"{komponen_keramik['lantai'] + komponen_keramik['dinding_km']} m²")
        st.metric("Closet", f"{komponen_km['closet']} buah")
        st.metric("Wastafel", f"{komponen_km['wastafel']} buah")
    
    st.markdown("---")
    st.markdown("### 👷 TENAGA KERJA")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tukang", f"{komponen_tenaga['tukang']} orang")
    with col2:
        st.metric("Kenek", f"{komponen_tenaga['kenek']} orang")
    with col3:
        st.metric("Hari", f"{komponen_tenaga['hari']} hari")
    
    st.markdown("---")
    st.markdown(f"""
    <div class="success-box">
        <h2 style="margin:0;">Rp {total_biaya:,.0f}</h2>
        <p>💰 TOTAL RAB (Material + Upah)</p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("## 💾 EXPORT LAPORAN")
    
    laporan_txt = f"""
ARKI ESTIMATOR PRO - LAPORAN PERHITUNGAN
========================================
Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATA BANGUNAN:
- Panjang: {panjang} m
- Lebar: {lebar} m
- Tinggi: {tinggi} m
- Lantai: {lantai}
- Luas: {luas_bangunan} m²

HASIL PERHITUNGAN:
- Total Semen: {total_semen} sak
- Total Pasir: {komponen_pondasi['pasir'] + komponen_struktur['pasir'] + cakar['pasir_m3'] + dinding['pasir_pasang'] + dinding['pasir_plester'] + komponen_keramik['pasir']:.2f} m³
- Total Split: {komponen_struktur['split'] + cakar['split_m3']:.2f} m³
- Total Besi: {komponen_struktur['besi_kg'] + cakar['besi_kg']:.1f} kg
- Total Bata: {dinding['bata']:,} pcs
- Total Genteng: {genteng:,} pcs
- Total Keramik: {komponen_keramik['lantai'] + komponen_keramik['dinding_km']} m²

TOTAL RAB: Rp {total_biaya:,.0f}
    """
    
    st.download_button("📥 Download Laporan TXT", laporan_txt, f"laporan_{datetime.now().strftime('%Y%m%d')}.txt")
    
    st.download_button("📥 Download Laporan JSON", 
                       json.dumps({'total_biaya': total_biaya, 'tanggal': str(datetime.now())}, indent=2),
                       f"laporan_{datetime.now().strftime('%Y%m%d')}.json")
