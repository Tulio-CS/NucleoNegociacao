import streamlit as st
import pandas as pd
import numpy as np

st.title("Random Data Table")

data = pd.DataFrame({
    "A": np.random.randn(10),
    "B": np.random.rand(10),
    "C": np.random.randint(0, 100, 10)
})

st.dataframe(data)
st.line_chart(data)
