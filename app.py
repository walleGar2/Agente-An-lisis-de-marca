"""
app.py
------
La LANDING en Streamlit. Es solo la "cara": llama a las funciones
que ya tienes (buscar_candidatos y correr_analisis) y muestra el resultado.

Flujo:
  1. Escribes el nombre y das "Buscar".
  2. Eliges la empresa correcta en un menu desplegable.
  3. Das "Analizar" y se muestra el reporte.

Concepto clave: Streamlit re-ejecuta TODO este archivo cada vez que tocas
un boton. Para no perder lo que encontramos, lo guardamos en st.session_state
(piensalo como una mochila que sobrevive entre clic y clic).
"""

import streamlit as st
from desambiguador import buscar_candidatos
from orquestador import correr_analisis

# Configuracion basica de la pagina
st.set_page_config(page_title="Analizador de marcas", layout="centered")

st.title("Analizador de marcas")
st.write("Escribe el nombre de una empresa de Guatemala para analizarla.")

# -------------------------------------------------------------------
# PASO 1: escribir el nombre y buscar candidatas
# -------------------------------------------------------------------
nombre = st.text_input("Nombre de la empresa")

if st.button("Buscar empresa"):
    if nombre.strip():
        with st.spinner("Buscando empresas que coincidan..."):
            # Guardamos las candidatas en la "mochila" para no perderlas
            st.session_state.candidatos = buscar_candidatos(nombre)
        # Si buscamos de nuevo, borramos un reporte viejo que hubiera
        st.session_state.pop("reporte", None)
    else:
        st.warning("Escribe un nombre primero.")

# -------------------------------------------------------------------
# PASO 2: si ya hay candidatas guardadas, dejar elegir una
# -------------------------------------------------------------------
if st.session_state.get("candidatos"):
    candidatos = st.session_state.candidatos

    # Armamos las opciones legibles para el menu
    opciones = [
        f"{c.get('nombre')} - {c.get('descripcion')} ({c.get('ubicacion')})"
        for c in candidatos
    ]

    # selectbox devuelve el INDICE elegido; mostramos el texto con format_func
    indice = st.selectbox(
        "Cual es la empresa correcta?",
        range(len(opciones)),
        format_func=lambda i: opciones[i],
    )

    # -------------------------------------------------------------------
    # PASO 3: analizar la empresa elegida
    # -------------------------------------------------------------------
    if st.button("Analizar esta empresa"):
        elegida = candidatos[indice]
        with st.spinner("Analizando a fondo... (esto puede tardar unos segundos)"):
            st.session_state.reporte = correr_analisis(
                elegida.get("nombre"),
                elegida.get("web"),
            )

elif "candidatos" in st.session_state:
    # Hubo busqueda pero la lista vino vacia
    st.warning("No encontre empresas con ese nombre. Revisa la escritura.")

# -------------------------------------------------------------------
# Mostrar el reporte (si ya existe en la mochila)
# -------------------------------------------------------------------
if "reporte" in st.session_state:
    st.subheader("Reporte")
    st.text(st.session_state.reporte)