import streamlit as st
from pickle import load
import numpy as np
import os
from gtts import gTTS

# Cargamos el modelo
model = load(open("./models/boosting_n_est-70_learn_rat-0_max_dep-44_gam-81_min_child-90_colsample-0_42.sav", "rb"))

Outcome = {
    "0": "Positivo",
    "1": "Negativo",
}

# CSS personalizado para accesibilidad
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
st.markdown(page_bg, unsafe_allow_html=True)

# Ponemos un título y logo
st.image("https://www.ccomsuam.org/wp-content/uploads/2017/11/hospital-links-logo.png", width=300)
st.title("Test de diabetes - Diagnóstico")

# **Instrucciones claras para usuarios**
st.markdown("""
### Instrucciones:
1. Ingrese sus datos en los cuadros proporcionados.
2. Ajuste los parámetros según sea necesario.
3. Presione el botón "Predecir" para ver el resultado.
""")

# **Soporte multilingüe**
language = st.radio("Seleccione un idioma:", ["Español", "Inglés"])

# Texto dinámico para adaptarse al idioma
if language == "Español":
    text_labels = {
        "glucose": "Concentración de glucosa (2 horas antes del test)",
        "pressure": "Presión arterial (mm Hg)",
        "insulin": "Nivel de insulina (µU/mL)",
        "thickness": "Grosor del pliegue cutáneo del tríceps (mm)",
        "bmi": "Índice de masa corporal (BMI)",
        "age": "Edad",
        "pedigree": "Pedigrí de diabetes",
        "pregnancies": "Número de embarazos (0 = No embarazo)",
        "predict": "Predecir",
        "success": "Datos ingresados correctamente. Procesando predicción...",
        "positive": "Positivo: Es posible que tenga diabetes.",
        "negative": "Negativo: Es poco probable que tenga diabetes.",
    }
elif language == "Inglés":
    text_labels = {
        "glucose": "Glucose concentration (2 hours before the test)",
        "pressure": "Blood pressure (mm Hg)",
        "insulin": "Insulin level (µU/mL)",
        "thickness": "Skin thickness of the triceps (mm)",
        "bmi": "Body Mass Index (BMI)",
        "age": "Age",
        "pedigree": "Diabetes pedigree",
        "pregnancies": "Number of pregnancies (0 = No pregnancies)",
        "predict": "Predict",
        "success": "Data successfully entered. Processing prediction...",
        "positive": "Positive: You may have diabetes.",
        "negative": "Negative: You are unlikely to have diabetes.",
    }

# **Control del tamaño de texto**
font_size = st.slider("Ajuste el tamaño del texto", min_value=12, max_value=32, value=16)
st.markdown(
    f"""
    <style>
    body, label, input, button {{
        font-size: {font_size}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Colocamos los campos de entrada en dos columnas
left, right = st.columns(2)
with left:
    Glucose = st.text_input(text_labels["glucose"])
    BloodPressure = st.text_input(text_labels["pressure"])
    Insulin = st.text_input(text_labels["insulin"])
    SkinThickness = st.text_input(text_labels["thickness"])
with right:
    BMI = st.text_input(text_labels["bmi"])
    Age = st.text_input(text_labels["age"])
    DiabetesPedigreeFunction = st.text_input(text_labels["pedigree"])
    Pregnancies = st.slider(text_labels["pregnancies"], min_value=0, max_value=10, step=1)

# Botón para predecir
if st.button(text_labels["predict"]):
    if not Glucose or not BloodPressure or not Insulin or not BMI or not Age or not DiabetesPedigreeFunction or not SkinThickness:
        st.error("Por favor, complete todos los campos antes de continuar.")
    else:
        # Procesamos los datos
        Glucose = float(Glucose)
        BloodPressure = float(BloodPressure)
        Insulin = float(Insulin)
        BMI = float(BMI)
        Age = float(Age)
        SkinThickness = float(SkinThickness)
        DiabetesPedigreeFunction = float(DiabetesPedigreeFunction)
        Pregnancies = float(Pregnancies)
        
        # Predicción
        data = np.array([[Glucose, BloodPressure, Insulin, SkinThickness, BMI, Age, DiabetesPedigreeFunction, Pregnancies]])
        st.info(text_labels["success"])
        prediction = str(model.predict(data)[0])
        result = text_labels["positive"] if prediction == "1" else text_labels["negative"]
        
        # Mostrar resultado con retroalimentación
        st.success(result)

# **Incluir audio para personas con discapacidad visual**
audio_text = "Bienvenido al test de diabetes. Por favor, complete todos los campos para continuar." if language == "Español" else "Welcome to the diabetes test. Please fill in all fields to continue."
tts = gTTS(audio_text, lang="es" if language == "Español" else "en")
tts.save("welcome.mp3")
audio_file = open("welcome.mp3", "rb")
st.audio(audio_file.read(), format="audio/mp3")

# **Imagen inclusiva al final**
st.image("https://www.semana.com/resizer/v2/YCZYGAJPVFG3HBY5C4HURENNEI.jpg?auth=c82cd58038203e50d842887194d373de616c79e7d13cd59a938228e7a5b48cf4&smart=true&quality=75&width=1280&height=720", use_container_width=True)
