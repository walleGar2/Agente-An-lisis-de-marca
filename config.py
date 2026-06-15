"""
config.py
---------
Lee la API key de forma SEGURA, sin dejarla escrita aqui.
Por eso este archivo YA se puede subir a GitHub sin riesgo.
"""

import os


def _obtener_api_key():
    # 1) Streamlit: lee secrets.toml (local) o los Secrets (nube)
    try:
        import streamlit as st
        clave = st.secrets.get("GOOGLE_API_KEY", "")
        if clave:
            return clave
    except Exception:
        pass

    # 2) Variable de entorno (alternativa, por si corres sin streamlit)
    return os.environ.get("GOOGLE_API_KEY", "")


GOOGLE_API_KEY = _obtener_api_key()
