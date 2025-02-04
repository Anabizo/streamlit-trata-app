import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://trata-app-api-p5a1.onrender.com/ficha-fisioterapia"
EXERCICIOS_URL = "https://trata-app-api-p5a1.onrender.com/exercicio"

st.title("Ficha de Fisioterapia")

# Função para buscar fichas
def get_fichas():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados!")
        return []

# Função para buscar exercícios disponíveis
def get_exercicios():
    response = requests.get(EXERCICIOS_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar exercícios!")
        return []

# Formulário para criar nova ficha
st.subheader("Criar Nova Ficha")
professor_options = [
        "Kátia Tiemi",
    ]
professor = st.selectbox("Professor*", professor_options)
data = st.date_input("Data*")

caracteristicas_options = [
    "Animado", "Raivoso", "Calmo", "Violento", "Sonolento", "Um Pouco Agitado", "Agitado",
    "Ansioso", "Depressivo", "Impaciente", "Triste", "Consciente/normal", "Falante",
    "Sem sono", "Um pouco Falante", "Fala arrastada", "Alegre", "Muito calmo (quase sedado)"
]
caracteristicas = st.selectbox("Características*", caracteristicas_options)
spo_porcentagem = st.number_input("SPO Porcentagem*", min_value=0, max_value=100, step=1)
fc_bpm = st.number_input("Frequência Cardíaca (BPM)*", min_value=0, step=1)
pa_mm_hg = st.text_input("Pressão Arterial (mmHg)*")

estado_exaltacao_options = ["Ótimo", "Bom", "Regular", "Ruim", "Péssimo"]
estado_exaltacao = st.selectbox("Estado de Exaltação*", estado_exaltacao_options)

horario = st.time_input("Horário inicial*")

# Buscar exercícios e permitir múltipla seleção
exercicios_disponiveis = get_exercicios()
exercicios_nomes = [exercicio["nome"] for exercicio in exercicios_disponiveis]
exercicios_selecionados = st.multiselect("Exercícios Realizados", exercicios_nomes)

performace_options = ["Muito bom", "Satisfatório", "Insatisfatório"]
performace = st.selectbox("Performace durante o treino*", performace_options)
comentarios = st.text_area("Descrição")




if st.button("Enviar Ficha"):
    exercicios_ids = [exercicio["id"] for exercicio in exercicios_disponiveis if exercicio["nome"] in exercicios_selecionados]
    
    dados = {
        "professor": professor,
        "data": str(data),
        "horario": str(horario),
        "estado_exaltacao": estado_exaltacao_options.index(estado_exaltacao) + 1,
        "caracteristicas": [caracteristicas],
        "spo_porcentagem": spo_porcentagem,
        "fc_bpm": fc_bpm,
        "pa_mm_hg": pa_mm_hg,
        "comentarios": comentarios,
        "performace": performace,
        "exercicios": [exercicio_id for exercicio_id in exercicios_ids]
    }
    
    response = requests.post(API_URL, json=dados)
    if response.status_code == 201:
        st.success("Ficha enviada com sucesso!")
    else:
        st.error("Erro ao enviar ficha!")

# Exibição de gráficos
st.subheader("Evolução dos Sinais Vitais")
fichas = get_fichas()
if fichas:
    df = pd.DataFrame(fichas)
    df['data'] = pd.to_datetime(df['data'])
    
    opcao_y = st.selectbox("Selecionar métrica para o eixo Y", ["spo_porcentagem", "fc_bpm"], format_func=lambda x: "SPO²" if x == "spo_porcentagem" else "FC (BPM)")
    fig = px.line(df, x='data', y=opcao_y, title='Evolução dos Sinais Vitais', markers=True)
    st.plotly_chart(fig)

fichas = get_fichas()
for ficha in fichas:
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
                <p style="text-align: center; font-size: 20px; font-weight: bold; color: #4A148C;">Horário: {ficha['horario']}</p>
                <div style="background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px; text-align: center;">
                    {', '.join(ficha['caracteristicas'])}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("---")



