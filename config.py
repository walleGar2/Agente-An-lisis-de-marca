"""
Lee de forma SEGURA todas las llaves del proyecto, sin dejarlas escritas aqui.
Por eso este archivo se puede subir a GitHub sin riesgo.

  - LOCAL: del archivo .streamlit/secrets.toml (NO se sube a GitHub)
  - EN LA NUBE: del apartado "Secrets" de Streamlit Cloud
"""

import os


def _leer_secreto(nombre):
    """Busca un secreto por su nombre, primero en Streamlit y luego en variables de entorno."""
    try:
        import streamlit as st
        valor = st.secrets.get(nombre, "")
        if valor:
            return valor
    except Exception:
        pass
    return os.environ.get(nombre, "")


# Llave de Google (Gemini)
GOOGLE_API_KEY = _leer_secreto("GOOGLE_API_KEY")

# Llaves de Meta (Instagram)
META_ACCESS_TOKEN = _leer_secreto("META_ACCESS_TOKEN")
IG_BUSINESS_ACCOUNT_ID = _leer_secreto("IG_BUSINESS_ACCOUNT_ID")

# Llave de YouTube (Data API v3)
YOUTUBE_API_KEY = _leer_secreto("YOUTUBE_API_KEY")
