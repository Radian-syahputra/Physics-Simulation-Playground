import pandas as pd
import streamlit as st


def render():
    st.header("Besaran & Satuan")
    st.info("Modul ini akan dikerjakan.")


KONFERSI = {
    "Panjang (SI : m)": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "inci": 0.0254,
        "kaki ": 0.3048,
        "mill": 1609.344,
    },
    "Massa (SI : kg)": {
        "mg": 1e-6,
        "g": 0.001,
        "kg": 1.0,
        "ton": 1000.0,
        "pon": 0.45359237,
        "ons": 0.028349523,
    },
    "Waktu (SI : s)": {
        "ms": 0.001,
        "s": 1.0,
        "menit": 60.0,
        "jam": 3600.0,
        "hari": 86400.0,
    },
}

SATUAN_SUHU = ["°C", "K", "°F"]

# TABEL BESARAN : nama, simbol, satuan, satuan SI, dimensi
BESARAN = [
    ("Panjang", "l", "meter (m)", "[L]"),
    ("Massa", "m", "kilogram (kg)", "[M]"),
    ("Waktu", "t", "secon (s)", "[T]"),
    ("Suhu", "T", "Kelvin (K)", "[Θ]"),
    ("Kecepatan", "v", "m/s", "[L][T]⁻¹"),
    ("Percepatan", "a", "m/s²", "[L][T]⁻²"),
    ("Gaya", "F", "newton (N)", "[M][L][T]⁻²"),
    ("Energi / Usaha", "E, W", "joule (J)", "[M][L]²[T]⁻²"),
    ("Daya", "P", "watt (W)", "[M][L]²[T]⁻³"),
    ("Tekanan", "p", "pascal (Pa)", "[M][L]⁻¹[T]⁻²"),
]

# DIMENSI DISIMPAN SEBAGAI PANGKAT (M, L, T) AGAR BISA DI CEK OTOMATIS
DIMENSI = {
    "Panjang (L)" : (0, 1, 0),
    "Massa (M)" : (1, 0, 0),
    "Waktu (T)" : (0, 0, 1),
    "Kecepatan (v)" : (0, 1, -1),
    "Percepatan (a)" : (0, 1, -2),
    "Gaya (F)" : (1, 1, -2),
    "Energi (E)" : (1, 2, -2),
    "Daya (P)" : (1, 2, -3),
    "Tekanan (p)" : (1, -1, -2)
}

# -------------------------------------------------------
# FUNGSI HITUNG DALAM FISIKA ANJAYYY
# -------------------------------------------------------

def konversi_biasa(nilai, dari, ke, tabel) :
    """Ubah ke SI dulu, lalu ke satuan tujuan."""
    dalam_si = nilai * tabel[dari]
    return dalam_si / tabel[ke]

def konversi_suhu(nilai, dari, ke) :
    """Suhu: ubah ke Kelvin dulu, lalu ke satuan tujuan."""
    if dari == "°C" :
        kelvin = nilai + 273.15
    elif dari == "°F" :
        kelvin = (nilai - 32) * 5 / 9 + 273.15
    else :
        kelvin = nilai


    if ke == "°C" :
        return kelvin - 273.15
    elif ke == "°F" :
        return (kelvin - 273.15) * 9 / 5 + 32
    return kelvin

def format_dimensi(d) :
    """Ubah (1, 1, -2) menjadi teks 'M¹ L¹ T⁻²'."""
    # Menngubah -0sampai9 menjadi pangkat kecil
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    bagian = []
    for huruf, pangkat in zip("MLT", d) :
        if pangkat != 0:
            bagian.append(f"{huruf}{str(pangkat).translate(sup)}")
        return " ".join(bagian) if bagian else "Tidak Berdimensi"

