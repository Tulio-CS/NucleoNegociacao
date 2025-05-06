import streamlit as st

st.title("📈 Employee Performance Review")

employee = st.selectbox("Select Employee", ["Alice", "Bob", "Carlos", "Diana"])
rating = st.slider("Rating (1-5)", 1, 5, 3)
comments = st.text_area("Comments")

if st.button("Submit Review"):
    st.success(f"Review submitted for {employee} with rating {rating}")
