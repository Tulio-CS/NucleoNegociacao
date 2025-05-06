import streamlit as st

# Título principal
st.title("Meu App Simples com Sidebar")

# Sidebar
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Escolha a página:", ["Início", "Sobre", "Contato"])

# Conteúdo de cada página
if pagina == "Início":
    st.header("Bem-vindo!")
    st.write("Esta é a página inicial do app.")
elif pagina == "Sobre":
    st.header("Sobre")
    st.write("Este app foi feito com Streamlit.")
elif pagina == "Contato":
    st.header("Contato")
    st.write("Email: exemplo@site.com")
