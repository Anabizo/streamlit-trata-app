import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime
import os

load_dotenv()

EXERCICIOS_URL = os.getenv('EXERCICIOS_URL')
API_URL = os.getenv('API_URL')

st.set_page_config(page_icon='📃')

# Função para buscar fichas
def get_fichas():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados!")
        return []

# Exibição de gráficos
st.subheader("📈Evolução dos Sinais Vitais🫀")
fichas = get_fichas()
if fichas:
    df = pd.DataFrame(fichas)
    df['data'] = pd.to_datetime(df['data'])
    
    opcao_y = st.selectbox("Selecionar métrica para o eixo Y", ["spo_porcentagem", "fc_bpm"], format_func=lambda x: "SPO²" if x == "spo_porcentagem" else "FC (BPM)")
    fig = px.line(df, x='data', y=opcao_y, title='Evolução dos Sinais Vitais', markers=True)
    st.plotly_chart(fig)

fichas = get_fichas()
for ficha in fichas:
    data_obj = datetime.strptime(ficha['data'], "%Y-%m-%dT%H:%M:%S.%fZ")
    ficha['data'] = data_obj.strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(
        f"""
        <div style="border-radius: 10px; padding: 15px; background-color: #f8f9fa; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;">
        <h3 style="text-align: center; color: #4A148C;">Ficha</h3>
        <div style="background-color: #6D1B7B; padding: 5px; border-radius: 5px; text-align: center; color: white; font-weight: bold;">Performance</div>
        <p style="text-align: center; color: #4A148C;"><strong>Professor:</strong> {ficha['professor']}</p>
        <p style="text-align: center; color: #4A148C;"><strong>Data:</strong> {ficha['data']}</p>
        <p style="text-align: center; color: #4A148C;"><strong>Horário:</strong> {ficha['horario']}</p>
                <p style="text-align: center; color: #4A148C;"><strong>Estado de Exaltação:</strong> {ficha['estado_exaltacao']}</p>
                <h4 style="text-align: center; color: #333;">Sinais Vitais</h4>
                <div style="display: flex; justify-content: space-around;">
                    <span style="padding: 5px 10px; background-color: #00A8FF; border-radius: 5px;">SPO²: {ficha['spo_porcentagem']}%</span>
                    <span style="padding: 5px 10px; background-color: #FFEB3B; border-radius: 5px;">FC: {ficha['fc_bpm']} BPM</span>
                    <span style="padding: 5px 10px; background-color: #FF0000; border-radius: 5px;">P.A: {ficha['pa_mm_hg']}</span>
                </div>
                <div style="background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px; text-align: center;">
                    {', '.join(ficha['caracteristicas'])}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("---")