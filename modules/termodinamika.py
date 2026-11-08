import numpy as np
import plotly.graph_objects as go
import streamlit as st

R: float = 8.314
KALOR_JENIS: dict[str, int] = {
    "Air": 4186,
    "Es": 2100,
    "Aluminium": 900,
    "Besi": 450,
    "Tembaga": 385,
}

# Fungsi Anjayy
def hitung_kalor(m, c, T_awal, T_akhir) : 
    delta_T = T_akhir - T_awal
    Q =  m * c * delta_T
    return delta_T, Q


def grafik_fungsi_kalor(T_awal, T_akhir, m, c) :
    T = np.linspace(T_awal, T_akhir, 100)
    Q = m * c * (T - T_awal)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=T, y=Q, mode="lines", name="Q"))
    fig.update_layout(
        xaxis_title = "Suhu (°C)",
        yaxis_title = "Kalor Q (J)",
        title = "Kalor Terhadap Suhu"
    )
    return fig

def hitung_tekanan(n, T, V) :
    P = n * R * T / V
    return P

def grafik_pv(n, T, V) :
    V_arr = np.linspace(0.3*V, 3*V, 200)
    P_arr = n * R * T / V_arr
    P_now = hitung_tekanan(n, T, V)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=V_arr, y=P_arr, mode="lines", name="Isotermal"))
    fig.add_trace(go.Scatter(x=[V], y=[P_now], mode="markers", name="Keadaan Sekarang", marker=dict(size=12)))

    fig.update_layout(
        xaxis_title = "Volume (m³)",
        yaxis_title = "Tekanan (Pa)",
        title = "Grafik P-V Gas Ideal"
    )

    return fig

# Tampilan
def tampil_kalor() :
    kiri, kanan = st.columns([1, 2])
    
    with kiri :
        zat = st.selectbox("Zat", list(KALOR_JENIS.keys()), key="termo_zat")
        m = st.number_input("Massa (Kg)", min_value=0.01, value=1.0, key="termo_masa")
        T_awal = st.number_input("Suhu Awal (°C)", value=20.0, key="termo_T_awal")
        T_akhir = st.number_input("Suhu Akhir (°C)", value=80.0, key="termo_T_akhir")

    c = KALOR_JENIS[zat]
    delta_T, Q = hitung_kalor(m, c, T_awal, T_akhir)

    with kanan :
        c1, c2, c3 = st.columns(3)

        c1.metric("Kalor Jenis", f"{c} J/kg·K")
        c2.metric("Perubahan Suhu", f"{delta_T:.1f} °C")
        c3.metric("Kalor Q", f"{Q:,.0f} J")
        st.latex(r"Q = m \cdot c \cdot \Delta T")
        st.plotly_chart(grafik_fungsi_kalor(T_awal, T_akhir, m, c), width="stretch")


def tampil_gas() :
    kiri, kanan = st.columns([1, 2])

    with kiri :
        n = st.number_input("Jumlah Mol (n)", min_value=0.01, value=1.0, key="termo_n")
        T_celcius = st.slider("Suhu (°C)", -100, 1000, 27, key="termo_T")
        V = st.number_input("Volume (m³)", min_value=0.001, value=0.025, format="%.3f", key="termo_V")

    T = T_celcius + 273.15
    P = hitung_tekanan(n, T, V)

    with kanan :
        c1, c2 = st.columns(2)
        c1.metric("Suhu", f"{T:.2f} K")
        c2.metric("Tekanan", f"{P:.2f} Pa")
        st.latex(r"PV = nRT")
        st.plotly_chart(grafik_pv(n, T, V), width="stretch")
        
        

def render():
    st.header("Termodinamika")

    mode = st.radio("Pilih Mode", ["Kalor", "Gas Ideal"], horizontal=True, key="termo_mode")

    if mode == "Kalor" :
        tampil_kalor()
    else :
        tampil_gas()

