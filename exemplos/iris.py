import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

st.title("Iris Flower Prediction")

iris = load_iris()
X = iris.data
y = iris.target

clf = RandomForestClassifier()
clf.fit(X, y)

sepal_length = st.slider("Sepal length", 4.0, 8.0, 5.1)
sepal_width = st.slider("Sepal width", 2.0, 4.5, 3.5)
petal_length = st.slider("Petal length", 1.0, 7.0, 1.4)
petal_width = st.slider("Petal width", 0.1, 2.5, 0.2)

prediction = clf.predict([[sepal_length, sepal_width, petal_length, petal_width]])
st.write(f"Predicted class: {iris.target_names[prediction][0]}")
