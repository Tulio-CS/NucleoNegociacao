import streamlit as st

st.title("Hello, Streamlit!")

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name} 👋")

age = st.slider("Your age", 0, 100, 25)
st.write(f"You're {age} years old.")
