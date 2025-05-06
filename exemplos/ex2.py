import streamlit as st

st.title("📝 New Employee Onboarding")

with st.form("onboarding_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    department = st.selectbox("Department", ["HR", "Finance", "IT", "Marketing", "Sales"])
    start_date = st.date_input("Start Date")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"Employee {name} from {department} added successfully!")