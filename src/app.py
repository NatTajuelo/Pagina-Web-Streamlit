import streamlit as st
from pickle import load
import pandas as pd
import numpy as np

#Cargamos el modelo
model = load(open("../models/boosting_n_est-70_learn_rat-0_max_dep-44_gam-81_min_child-90_colsample-0_42.sav", "rb"))

class_dict = {
    "0": "Negativo",
    "1": "Positivo",
}

#Asignamos un nombre
st.image("https://www.ccomsuam.org/wp-content/uploads/2017/11/hospital-links-logo.png", width=400)
st.title("Test de diabetes - Diagnóstico")

left, right = st.columns(2)  # Retorna dos columnas: izquierda y derecha

# Cuadros de texto en la columna izquierda
with left:
    glucosa = st.text_input("Concentración de glucosa (2 horas antes del test)")
    presion = st.text_input("Presión arterial (mm Hg)")
    insulina = st.text_input("Nivel de insulina (µU/mL)")
    pliegue_cutaneo = st.text_input("Grosor del pliegue cutáneo del tríceps (mm)")

# Cuadros de texto en la columna derecha
with right:
    bmi = st.text_input("Índice de masa corporal (BMI)")
    edad = st.text_input("Edad")
    pedigri = st.text_input("Pedigrí de diabetes")
    embarazo = st.slider("Número de embarazos (0 = No embarazo)", min_value=0, max_value=10, step=1)

# Botón para procesar los datos
if st.button("Predecir"):
    if not glucosa or not presion or not insulina or not bmi or not edad or not pedigri or not pliegue_cutaneo:
        st.error("Por favor, complete todos los campos antes de continuar.")
    else:
    
        # Conversiones
        glucosa = float(glucosa)
        presion = float(presion)
        insulina = float(insulina)
        bmi = float(bmi)
        edad = float(edad)
        pliegue_cutaneo = float(pliegue_cutaneo)
        pedigri = float(pedigri)
        embarazo = float(embarazo)
        
        # Preparar datos para el modelo
        data = np.array([[glucosa, presion, insulina, pliegue_cutaneo, bmi, edad, pedigri, embarazo]])
        # Aquí puedes añadir la lógica para analizar los datos y predecir si tiene diabetes
        st.sucess("Datos ingresados correctamente. Procesando predicción...")
        prediction = str(model.predict([[glucosa, presion, insulina, pliegue_cutaneo, bmi, edad, pedigri, embarazo]])[0])
        pred_class = class_dict[prediction]
        st.write("Prediction:", pred_class)



