import streamlit as st
import pandas as pd
import random

# Carregar ou criar banco de dados
try:
    df = pd.read_csv("nucleo_negociacoes.csv")
    historico = pd.read_csv("historico_debates.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Nome", "Categoria", "Rapport", "Coerência", "Sintonia", "Linguagem Corporal", "Persuasão", "Média Avaliação"])
    historico = pd.DataFrame(columns=["Data", "Tema", "Mesa", "Participantes", "Avaliadores", "Notas"])

def salvar_dados():
    df.to_csv("nucleo_negociacoes.csv", index=False)
    historico.to_csv("historico_debates.csv", index=False)

# Interface
st.title("Núcleo de Negociações")

menu = st.sidebar.radio("Menu", ["Cadastrar Membro", "Criar Debate", "Gerenciar Mesas", "Registrar Avaliação", "Visualizar Evolução", "Histórico de Debates", "Lista de Membros"])

if menu == "Cadastrar Membro":
    st.header("Cadastro de Membros")
    nome = st.text_input("Nome do membro")
    categoria = st.selectbox("Categoria", ["Avaliador Experiente", "Avaliador Iniciante", "Participante"])
    if st.button("Cadastrar"):
        if nome and categoria:
            df.loc[len(df)] = [nome, categoria, 0, 0, 0, 0, 0, 0]
            salvar_dados()
            st.success("Membro cadastrado!")

elif menu == "Criar Debate":
    st.header("Criar Novo Debate")
    data = st.date_input("Data do Debate")
    tema = st.text_input("Tema do Debate")
    participantes = st.multiselect("Selecione os participantes", df["Nome"].tolist())
    
    avaliadores_disponiveis = df[df["Categoria"].isin(["Avaliador Experiente", "Avaliador Iniciante"])]["Nome"].tolist()
    avaliadores_passados = historico["Avaliadores"].dropna().str.split(", ").explode().tolist()
    avaliadores_filtrados = [a for a in avaliadores_disponiveis if avaliadores_passados.count(a) == 0 or len(avaliadores_disponiveis) < 2]
    
    random.shuffle(participantes)
    mesas = [f"{participantes[i]} x {participantes[i + 1]}" for i in range(0, len(participantes), 2) if i + 1 < len(participantes)]
    
    avaliadores = avaliadores_filtrados[:2] if len(avaliadores_filtrados) >= 2 else avaliadores_filtrados
    if len(avaliadores_filtrados) > 2:
        participantes.extend(avaliadores_filtrados[2:])
    
    if st.button("Salvar Debate"):
        if data and tema and participantes and len(avaliadores) == 2:
            novo_debate = pd.DataFrame({"Data": [data], "Tema": [tema], "Mesa": [", ".join(mesas)], "Participantes": [", ".join(participantes)], "Avaliadores": [", ".join(avaliadores)], "Notas": [""]})
            historico = pd.concat([historico, novo_debate], ignore_index=True)
            salvar_dados()
            st.success("Debate criado!")

elif menu == "Gerenciar Mesas":
    st.header("Mesas de Debates")
    st.dataframe(historico[["Data", "Tema", "Mesa", "Avaliadores"]])

elif menu == "Registrar Avaliação":
    st.header("Registro de Avaliações")
    membro = st.selectbox("Selecione o membro", df["Nome"].tolist())
    criterios = ["Rapport", "Coerência", "Sintonia", "Linguagem Corporal", "Persuasão"]
    notas = [st.slider(crit, 0, 3, 1) for crit in criterios]
    
    if st.button("Salvar Avaliação"):
        df.loc[df["Nome"] == membro, criterios] = notas
        df.loc[df["Nome"] == membro, "Média Avaliação"] = sum(notas) / len(notas)
        salvar_dados()
        st.success("Avaliação registrada!")

elif menu == "Visualizar Evolução":
    st.header("Evolução dos Membros")
    st.dataframe(df)

elif menu == "Histórico de Debates":
    st.header("Histórico de Debates")
    st.dataframe(historico)

elif menu == "Lista de Membros":
    st.header("Lista de Todos os Membros")
    st.dataframe(df[["Nome", "Categoria"]])
