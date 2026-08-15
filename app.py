import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os # <-- Adicione isso

def conectar_planilha():
    escopo = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Aqui mudamos para ler do ambiente (Variável que vamos criar no Google Cloud)
    credenciais_dict = json.loads(os.environ["GCP_CREDENTIALS"])
    
    credenciais = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, escopo)
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open('Solicitacoes_Laboratorio').sheet1
    return planilha

planilha = conectar_planilha()

# 2. Interface da Página
st.title("🔬 Solicitação de Atividades - Laboratório")
st.write("Preencha o formulário abaixo para registrar uma nova demanda.")

# 3. Formulário de Entrada
with st.form("form_solicitacao", clear_on_submit=True):
    nome_solicitante = st.text_input("Nome do Solicitante")
    tipo_atividade = st.selectbox("Tipo de Atividade", ["Análise de Amostra", "Manutenção de Equipamento", "Reserva de Bancada", "Outro"])
    descricao = st.text_area("Descrição da Atividade")
    data_desejada = st.date_input("Data Desejada")
    
    submit = st.form_submit_button("Enviar Solicitação")

    # 4. Ação ao enviar o formulário
    if submit:
        if nome_solicitante and descricao:
            # Adiciona uma nova linha na planilha do Google
            nova_linha = [nome_solicitante, tipo_atividade, descricao, str(data_desejada)]
            planilha.append_row(nova_linha)
            st.success("✅ Solicitação enviada com sucesso e salva na planilha!")
        else:
            st.warning("⚠️ Por favor, preencha o nome e a descrição.")
