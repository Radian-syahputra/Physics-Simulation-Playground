import numpy as np
import plotly.graph_objects as go
import streamlit as st


def hitung_gaya(m, sudut, g):
    sudut_rad = np.radians(sudut)
    N = m * g * np.cos(sudut_rad)
    w_sejajar = m * g * np.sin(sudut_rad)

    return N, w_sejajar


def tentukan_gerak(w_sejajar, F_luar, N, mu, m):
    """Tentukan status balok, gaya gesek, dan percepatan."""
    gaya_bawah = w_sejajar - F_luar
    f_maks = mu * N

    if abs(gaya_bawah) <= f_maks:
        status = "Diam"
        f_gesek = abs(gaya_bawah)
        a = 0.0
    else:
        status = "Meluncur"
        f_gesek = f_maks
        arah = 1 if gaya_bawah > 0 else -1
        a = (gaya_bawah - arah * f_gesek) / m
    return status, f_gesek, a


def buat_data_kecepatan(a, durasi=5, jumlah_titik=100):
    t = np.linspace(0, durasi, jumlah_titik)
    v = a * t
    return t, v


def buat_grafik(t, v) :
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=v, mode="lines", name="Kecepatan"))
    fig.update_layout(
        xaxis_title = "Waktu (s)",
        yaxis_title = "Kecepatan (m/s)",
        title = "Kecepatan Balok Terhadap Waktu"
    )
    return fig


def render():
    st.header("Dinamika : Balok Di Bidang Miring")

    kiri, kanan = st.columns([1, 2])

    with kiri :
        m = st.slider("Massa Balok (Kg)", 1, 100, 10)
        sudut = st.slider("Sudut Bidang (°)", 0, 89, 30)
        mu = st.slider("Koefisien Gesek (μ)", 0.0, 1.0, 0.2, 0.05)
        F_luar = st.number_input("Gaya Luar Ke Atas Bidang (N)", min_value=0.0, value=0.0)
        g = st.number_input("Gravitasi (m/s²)", min_value=0.1, value=9.8)

    N , w_sejajar = hitung_gaya(m, sudut, g)
    status, f_gesek, a = tentukan_gerak(w_sejajar,F_luar, N, mu, m)
    t, v = buat_data_kecepatan(a)

    with kanan :
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Gaya Normal", f"{N:.2f} N")
        c2.metric("Gaya Gesek", f"{f_gesek:.2f} N")
        c3.metric("Percepatan", f"{a:.2f} m/s²")
        c4.metric("Status", status)

        st.plotly_chart(buat_grafik(t, v), use_container_width=True)
        

    