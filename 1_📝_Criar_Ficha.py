import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

EXERCICIOS_URL = os.getenv('EXERCICIOS_URL')
API_URL = os.getenv('API_URL')

st.set_page_config(page_title='Apollo REAB', page_icon='🧑‍⚕️', layout='centered')

st.title("📃Ficha de Fisioterapia🧘‍♀️")

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

