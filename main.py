import streamlit as st
import pandas as pd
import random
import json

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
    
    avaliadores_disponiveis = df[df["Categoria"].isin(["Avaliador Experiente", "Avaliador Iniciante"])] ["Nome"].tolist()
    avaliadores_passados = historico["Avaliadores"].dropna().str.split(", ").explode().tolist()
    avaliadores_filtrados = [a for a in avaliadores_disponiveis if avaliadores_passados.count(a) == 0 or len(avaliadores_disponiveis) < 2]
    
    random.shuffle(participantes)
    mesas = [participantes[i:i+4] for i in range(0, len(participantes), 4) if len(participantes[i:i+4]) == 4]
    
    avaliadores = avaliadores_filtrados[:len(mesas) * 2] if len(avaliadores_filtrados) >= len(mesas) * 2 else avaliadores_filtrados
    
    if len(avaliadores) < len(mesas) * 2:
        st.warning("Não há avaliadores suficientes para todas as mesas.")
    
    if st.button("Salvar Debate"):
        if data and tema and participantes and len(mesas) > 0:
            novo_debate = pd.DataFrame({"Data": [data], "Tema": [tema], "Mesa": [json.dumps(mesas)], "Participantes": [", ".join(participantes)], "Avaliadores": [", ".join(avaliadores)], "Notas": [""]})
            historico = pd.concat([historico, novo_debate], ignore_index=True)
            salvar_dados()
            st.success("Debate criado!")

if menu == "Gerenciar Mesas":
    debate_escolhido = st.selectbox("Selecione um debate", historico["Tema"].tolist())
    debate = historico[historico["Tema"] == debate_escolhido].iloc[0]
    st.subheader(f"{debate['Data']} - {debate['Tema']}")
    
    try:
        mesas = json.loads(debate["Mesa"])
    except:
        st.error("Erro ao carregar as mesas.")
    avaliadores = debate["Avaliadores"].split(", ") if debate["Avaliadores"] else []
    
    for i, mesa in enumerate(mesas):
        st.markdown(f"### Mesa {i+1}")
        st.markdown(f"🎭 **Dupla A:** {', '.join(mesa[:2])}")
        st.markdown(f"🎭 **Dupla B:** {', '.join(mesa[2:])}")
        if len(avaliadores) >= (i+1)*2:
            st.markdown(f"📝 **Avaliadores:** {avaliadores[i*2]}, {avaliadores[i*2+1]}")
        st.markdown("---")
    
if menu == "Registrar Avaliação":
    debate_escolhido = st.selectbox("Selecione um debate", historico["Tema"].tolist())
    debate = historico[historico["Tema"] == debate_escolhido].iloc[0]
    st.subheader("Registro de Avaliações")
    participantes_debate = debate["Participantes"].split(", ") if debate["Participantes"] else []
    membro = st.selectbox("Selecione o membro", participantes_debate)
        
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
