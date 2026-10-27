import streamlit as st
from modules import satuan, kinematika, dinamika, energi, termodinamika

st.set_page_config(
    page_title="Physics Simulation Playground",
    page_icon="⚛️",
    layout="wide",
)

st.title("⚛️ Physics Simulation Playground")
st.caption("Simulasi Fisika Bermakna Anjayy")

tabs = st.tabs(["Satuan", "Kinematika", "Dinamika", "Energi", "Termodinamika"])

with tabs[0] :
    satuan.render()
with tabs[1] :
    kinematika.render()
with tabs[2] :
    dinamika.render()
with tabs[3] :
    energi.render()
with tabs[4] :
    termodinamika.render()