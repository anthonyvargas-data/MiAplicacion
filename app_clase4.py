import streamlit as st
import numpy as np

st.image("logo.png", width=100)

st.title("Listas e inputs")

valor = int(st.number_input("Ingrese un valor"))

lista = list(range(valor))

st.write(lista)

valor1 = st.slider("Seleccione un valor",1,20)

arreglo = np.arange(valor1)

st.write(arreglo)

