import streamlit as st
import pandas as pd

st.title("📋 Employee Directory")

# Example employee data
data = {
    "Name": ["Alice", "Bob", "Carlos", "Diana"],
    "Department": ["HR", "Finance", "IT", "Marketing"],
    "Email": ["alice@company.com", "bob@company.com", "carlos@company.com", "diana@company.com"]
}
df = pd.DataFrame(data)

# Filter by department
department = st.selectbox("Filter by Department", ["All"] + df["Department"].unique().tolist())

if department != "All":
    df = df[df["Department"] == department]

st.dataframe(df)