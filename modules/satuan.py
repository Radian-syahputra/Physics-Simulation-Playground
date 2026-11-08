import pandas as pd
import streamlit as st

KONFERSI = {
    "Panjang (SI : m)": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "inci": 0.0254,
        "kaki": 0.3048,
        "mil": 1609.344,
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
    ("Waktu", "t", "sekon (s)", "[T]"),
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
    "Panjang (L)": (0, 1, 0),
    "Massa (M)": (1, 0, 0),
    "Waktu (T)": (0, 0, 1),
    "Kecepatan (v)": (0, 1, -1),
    "Percepatan (a)": (0, 1, -2),
    "Gaya (F)": (1, 1, -2),
    "Energi (E)": (1, 2, -2),
    "Daya (P)": (1, 2, -3),
    "Tekanan (p)": (1, -1, -2),
}

# -------------------------------------------------------
# FUNGSI HITUNG DALAM FISIKA ANJAYYY
# -------------------------------------------------------


def konversi_biasa(nilai, dari, ke, tabel):
    """Ubah ke SI dulu, lalu ke satuan tujuan."""
    dalam_si = nilai * tabel[dari]
    return dalam_si / tabel[ke]


def konversi_suhu(nilai, dari, ke):
    """Suhu: ubah ke Kelvin dulu, lalu ke satuan tujuan."""
    if dari == "°C":
        kelvin = nilai + 273.15
    elif dari == "°F":
        kelvin = (nilai - 32) * 5 / 9 + 273.15
    else:
        kelvin = nilai

    if ke == "°C":
        return kelvin - 273.15
    elif ke == "°F":
        return (kelvin - 273.15) * 9 / 5 + 32
    return kelvin


def format_dimensi(d):
    """Ubah (1, 1, -2) menjadi teks 'M¹ L¹ T⁻²'."""
    # Menngubah -0sampai9 menjadi pangkat kecil
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    bagian = []
    for huruf, pangkat in zip("MLT", d):
        if pangkat != 0:
            bagian.append(f"{huruf}{str(pangkat).translate(sup)}")
    return " ".join(bagian) if bagian else "Tidak Berdimensi"


#  TAMPILAN UNTUK WEBISTE NYA
def render():
    st.header("Besaran & Satuan")

    with st.expander("Konsep singkat"):
        st.write(
            "Besaran fisika selalu punya satuan. Konversi dilakukan lewat satuan SI "
            "sebagai perantara. Cek dimensi dipakai untuk menguji apakah sebuah rumus "
            "masuk akal: kedua ruas harus punya dimensi yang sama."
        )

    sub1, sub2, sub3 = st.tabs(
        ["Konverter Satuan", "Tabel Besaran", "Cek Dimensi Rumus"]
    )

    # -------------- KONVERTER --------------
    with sub1:
        kiri, kanan = st.columns([1, 1.3])

        with kiri:
            kategori = st.selectbox("Kategori", list(KONFERSI.keys()) + ["Suhu"])

            nilai = st.number_input("Nilai", value=1.0, format="%.6g")

            if kategori == "Suhu":
                daftar = SATUAN_SUHU
            else:
                daftar = list(KONFERSI[kategori].keys())

            dari = st.selectbox("Dari", daftar, index=0)
            ke = st.selectbox("Ke", daftar, index=min(1, len(daftar) - 1))

        with kanan:
            if kategori == "Suhu":
                hasil = konversi_suhu(nilai, dari, ke)
            else:
                hasil = konversi_biasa(nilai, dari, ke, KONFERSI[kategori])

            st.subheader("Hasil")
            st.metric(label=f"{nilai:g} {dari} =", value=f"{hasil:,.6g} {ke}")

            st.markdown("**Langkah Perhitungan**")
            if kategori == "Suhu":
                st.write("Suhu Di Ubah Ke Kelvin Dulu, Lalu ke Satuan Tujuan.")
                st.latex(r"T_K = T_C + 273{,}15 \qquad T_F = \tfrac{9}{5}T_C + 32")
            else:
                faktor = KONFERSI[kategori][dari] / KONFERSI[kategori][ke]
                st.latex(
                    rf"{nilai:g}\ \text{{{dari}}} \times {faktor:.6g} = "
                    rf"{hasil:.6g}\ \text{{{ke}}}"
                )

    # ------------ TABEL BESARAN ------------
    with sub2:
        st.write("Besaran Pokok Dan Turunan Beserta Dimensinya")
        df = pd.DataFrame(
            BESARAN, columns=["Besaran", "Simbol", "Satuan SI", "Dimensi"]
        )
        st.dataframe(df, width="stretch", hide_index=True)

    # ----------- CEK DIMENSI -------------
    with sub3:
        st.write(
            "Uji apakah sebuah rumus konsisten secara dimensi. "
            "Contoh: apakah **F = m · a** benar?"
        )
        c1, c2 = st.columns(2)
        with c1:
            ruas_kiri = st.selectbox("Ruas Kiri", list(DIMENSI.keys()), index=5)
        with c2:
            st.write("Ruas Kanan = Hasil Kali Dari : ")
            faktor1 = st.selectbox("Besaran 1", list(DIMENSI.keys()), index=1)
            faktor2 = st.selectbox("Besaran 2", list(DIMENSI.keys()), index=4)

        dim_kiri = DIMENSI[ruas_kiri]
        dim_kanan = tuple(a + b for a, b in zip(DIMENSI[faktor1], DIMENSI[faktor2]))

        st.write(f"Dimensi Ruas Kiri : **{format_dimensi(dim_kiri)}**")
        st.write(f"Dimensi Ruas Kanan : **{format_dimensi(dim_kanan)}**")

        if dim_kiri == dim_kanan:
            st.success("Dimensi Sama, Rumus Konsisten Secara Dimensi")
        else:
            st.error("Dimensi Berbedad, Rumus Ini Gak Mungkin Benar")
