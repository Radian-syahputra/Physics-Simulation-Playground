import numpy as np
import plotly.graph_objects as go
import streamlit as st


def hitung_energy_awal(m, L, sudut0, g):
    """Tinggi awal dan energi mekanik total saat bandul dilepas."""
    sudut_radian = np.radians(sudut0)
    h0 = L * (1 - np.cos(sudut_radian))
    EM = m * g * h0
    return h0, EM


def hitung_kurva(m, L, sudut0, g, EM, hilang):
    """Energi di setiap posisi, dari titik lepas sampai titik terendah."""
    sudut0_rad = np.radians(sudut0)
    theta = np.linspace(sudut0_rad, 0, 100)
    porsi = (sudut0_rad - theta) / sudut0_rad
    EP = m * g * L * (1 - np.cos(theta))
    EM_arr = EM * (1 - hilang * porsi)
    EK = EM_arr - EP

    return np.degrees(theta), EP, EK, EM_arr


def hitung_kecepatan(EK_bawah, m):
    """Gunakan Rumus EK dan di ubah mencari v nya"""
    return np.sqrt(2 * EK_bawah / m)


def buat_grafik(sudut, EP, EK, EM_arr):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sudut, y=EP, mode="lines", name="Energi Potensial"))
    fig.add_trace(go.Scatter(x=sudut, y=EK, mode="lines", name="Energi Kinetik"))
    fig.add_trace(
        go.Scatter(
            x=sudut,
            y=EM_arr,
            mode="lines",
            name="Energi Mekanik",
            line=dict(dash="dash"),
        )
    )

    fig.update_layout(
        xaxis_title="Sudut Bandul (°)",
        yaxis_title="Energi (J)",
        title="Energi Bandul Dari Titik Lepas Ke Titik Terendah",
    )

    fig.update_xaxes(autorange="reversed")
    return fig


def render():
    st.header("Energi")

    kiri, kanan = st.columns([1, 2])

    with kiri:
        m = st.slider("Massa Bandul (Kg)", 1, 20, 2, key="energi_m")
        L = st.slider("Panjang Tali (m)", 0.5, 5.0, 1.0, 0.1, key="energi_L")
        sudut0 = st.slider("Sudut Awal (°)", 1, 89, 60, key="energi_sudut")
        g = st.number_input(
            "Gravitasi (m/s²)", min_value=0.1, value=9.8, key="energi_g"
        )
        hilang_persen = st.slider(
            "Energi Hilang AKibat Gesekan (%)", 0, 90, 0, key="energi_hilang"
        )

    hilang = hilang_persen / 100
    _, EM = hitung_energy_awal(m, L, sudut0, g)
    sudut, EP, EK, EM_arr = hitung_kurva(m, L, sudut0, g, EM, hilang)

    v_maks = hitung_kecepatan(EK[-1], m)

    with kanan:
        c1, c2, c3 = st.columns(3)
        c1.metric("Kecepatan maks", f"{v_maks:.2f} m/s")
        c2.metric("Energi mekanik awal", f"{EM:.2f} J")
        c3.metric("Energi hilang", f"{EM * hilang:.2f} J")

        st.latex(r"E_p = m g L (1 - \cos\theta)")
        st.latex(r"E_k = \tfrac{1}{2} m v^2")
        st.latex(rf"E_M = E_p + E_k = {EM:.2f} \ \text{{J}}")

        st.plotly_chart(buat_grafik(sudut, EP, EK, EM_arr), width="stretch")
