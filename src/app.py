import streamlit as st
from pickle import load
import pandas as pd
import numpy as np
import time
from gtts import gTTS
import os

#Cargamos el modelo
model = load(open("./models/boosting_n_est-70_learn_rat-0_max_dep-44_gam-81_min_child-90_colsample-0_42.sav", "rb"))

Outcome = {
    "0": "Positivo",
    "1": "Negativo",
}

#Personalizamos el fondo, la tipología e imágenes
page_bg = """
<style>
/* Fondo de la página */
[data-testid="stAppViewContainer"] {
    background-color: #f0f8ff; /* Azul claro */
    color: #333333;           /* Texto gris oscuro */
}

/* Cuadros de texto */
[data-testid="stTextInput"] label {
    color: #0066cc; /* Texto azul */
    font-size: 18px;
    font-weight: bold;
}

[data-testid="stTextInput"] input {
    background-color: #e0f7fa; /* Fondo celeste claro */
    color: #003333;           /* Texto verde oscuro */
    font-size: 16px;
    border-radius: 5px;
}

/* Slider */
[data-testid="stSlider"] .st-de {
    color: #333333; /* Texto del slider */
    font-size: 16px;
}

/* Títulos */
h1, h2, h3 {
    color: #003366; /* Azul oscuro */
    font-family: Arial, sans-serif;
    text-align: center;
}

/* Resultados */
[data-testid="stMarkdownContainer"] p {
    font-size: 20px;
    font-weight: bold;
}
</style>
"""

# Incluir el CSS en la app
st.markdown(page_bg, unsafe_allow_html=True)

#Ponemos un título y logo
st.image("https://www.ccomsuam.org/wp-content/uploads/2017/11/hospital-links-logo.png", width=300)
st.title("Test de diabetes - Diagnóstico")
st.text("Descripción: Este test ayuda a diagnosticar diabetes basándose en parámetros médicos.")

left, right = st.columns(2)  # Devuelve dos columnas: izquierda y derecha

# Cuadros de texto en la columna izquierda
with left:
    Glucose = st.text_input("Concentración de glucosa (2 horas antes del test)")
    BloodPressure = st.text_input("Presión arterial (mm Hg)")
    Insulin = st.text_input("Nivel de insulina (µU/mL)")
    SkinThickness = st.text_input("Grosor del pliegue cutáneo del tríceps (mm)")

# Cuadros de texto en la columna derecha
with right:
    BMI = st.text_input("Índice de masa corporal (BMI)")
    Age = st.text_input("Edad")
    DiabetesPedigreeFunction = st.text_input("Pedigrí de diabetes")
    Pregnancies = st.slider("Número de embarazos (0 = No embarazo)", min_value=0, max_value=10, step=1)

# Botón para procesar los datos
if st.button("Predecir"):
    if not Glucose or not BloodPressure or not Insulin or not BMI or not Age or not DiabetesPedigreeFunction or not SkinThickness:
        st.error("Por favor, complete todos los campos antes de continuar.")
    else:
    
        # Conversiones
        Glucose = float(Glucose)
        BloodPressure = float(BloodPressure)
        Insulin = float(Insulin)
        BMI = float(BMI)
        Age = float(Age)
        SkinThickness = float(SkinThickness)
        DiabetesPedigreeFunction = float(DiabetesPedigreeFunction)
        Pregnancies = float(Pregnancies)
        
        # Mensaje de "procesando"
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Datos ingresados correctamente. Procesando predicción...")
        time.sleep(2)

        # Borrar mensaje temporal y mostrar el resultado final
        status_placeholder.empty()

        # Preparar datos para el modelo
        data = np.array([[Glucose, BloodPressure, Insulin, SkinThickness, BMI, Age, DiabetesPedigreeFunction, Pregnancies]])
        prediction = str(model.predict([[Glucose, BloodPressure, Insulin, SkinThickness, BMI, Age, DiabetesPedigreeFunction, Pregnancies]])[0])
        pred_class = Outcome[prediction]
        st.success(f"Resultado de la predicción: **{pred_class}**")

st.image(
    "https://www.semana.com/resizer/v2/YCZYGAJPVFG3HBY5C4HURENNEI.jpg?auth=c82cd58038203e50d842887194d373de616c79e7d13cd59a938228e7a5b48cf4&smart=true&quality=75&width=1280&height=720",
    use_container_width=True
)

#Vamos a hacer la página más inclusiva
font_size = st.slider("Ajuste el tamaño del texto", min_value=12, max_value=32, value=16)

st.markdown(
    f"""
    <style>
    body, label, input, button {{
        font-size: {font_size}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

#Crear archivo de audio
text = "Bienvenido al test de diabetes. Por favor, complete todos los campos para continuar."
tts = gTTS(text, lang='es')
tts.save("welcome.mp3")
#Reproducir el audio al cargar la página
audio_file = open("welcome.mp3", "rb")
st.audio(audio_file.read(), format="audio/mp3")

#Otros idiomas
language = st.radio("Seleccione un idioma:", ["Español", "Inglés"])
if language == "Español":
    st.title("Test de diabetes - Diagnóstico")
    st.text("Por favor, complete los campos a continuación.")
elif language == "Inglés":
    st.title("Diabetes Test - Diagnosis")
    st.text("Please fill out the fields below.")