import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ============ FUNGSI HITUNG ===============


def hitung_komponen(v0, sudut):
    """Uraikan v0 menjadi komponen horizontal (vx) dan vertikal (vy)."""
    sudut_rad = np.radians(sudut)
    vx = v0 * np.cos(sudut_rad)
    vy = v0 * np.sin(sudut_rad)

    return vx, vy


def hitung_waktu_terbang(vy, h0, g):
    """Waktu sampai y = 0, akar positif dari h0 + vy*t - 0.5*g*t^2 = 0."""
    diskriminan = vy**2 + 2 * g * h0
    t_total = (vy + np.sqrt(diskriminan)) / g
    return t_total


def hitung_tinggi_maks(vy, h0, g):
    h_maks = h0 + vy**2 / (2 * g)
    return h_maks


def hitung_jarak_maks(vx, t_total):
    jarak = vx * t_total
    return jarak


def fungsi_buat_data_lintasan(vx, vy, h0, g, t_total, jumlah_titik=200):
    t = np.linspace(0, t_total, jumlah_titik)
    x = vx * t
    y = h0 + vy * t -0.5 * g * t**2
    return t, x, y

def buat_grafik(x, y) :
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Lintasan"))
    fig.update_layout(
        xaxis_title = "Jarak (m)",
        yaxis_title = "Tinggi (m)",
        title = "Lintasan Gerak Parabola"
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


# -------------------- TAMPILAN ----------------------

def render():
    st.header("Kinematika : Gerak Parabola")

    kiri, kanan = st.columns([1, 2])

    with kiri :
        v0 = st.slider("Kecepatan Awal (m/s)", 1, 100, 30)
        sudut = st.slider("Sudut Tembak (°)", 1, 89, 45)
        h0 = st.number_input("Ketinggian Awal (m)", min_value=0.0, value=0.0)
        g = st.number_input("Gravitasi (m/s²)", min_value=0.1, value=9.8, key="kinematika_g")

    vx, vy = hitung_komponen(v0, sudut)
    t_total = hitung_waktu_terbang(vy, h0, g)
    h_maks = hitung_tinggi_maks(vy, h0, g)
    jarak = hitung_jarak_maks(vx, t_total)
    t, x, y= fungsi_buat_data_lintasan(vx, vy, h0, g, t_total)

    with kanan :
        c1, c2, c3 = st.columns(3)
        c1.metric("Waktu terbang", f"{t_total:.2f} s")
        c2.metric("Tinggi maks", f"{h_maks:.2f} m")
        c3.metric("Jarak maks", f"{jarak:.2f} m")

        st.plotly_chart(buat_grafik(x, y), use_container_width=True)
