"""
desambiguador.py
----------------
Agente IDENTIFICADOR (barato y rapido).
Su trabajo: dado un nombre, buscar empresas reales que coincidan
y devolver una lista de candidatas, para que la persona confirme cual es.

Asi resolvemos dos problemas:
 - Si el nombre esta mal escrito, no aparecera su empresa (y se da cuenta).
 - Si hay varias empresas con el mismo nombre, las ve todas y escoge.
"""

import json
from google import genai
from google.genai import types
from config import GOOGLE_API_KEY


def buscar_candidatos(nombre):
    """
    Recibe un nombre (texto) y devuelve una LISTA de empresas candidatas.
    Cada candidata es un diccionario con: nombre, descripcion, ubicacion, web.
    """

    client = genai.Client(api_key=GOOGLE_API_KEY)

    config = types.GenerateContentConfig(
        tools=[{"google_search": {}}],
        system_instruction=(
            "Eres un asistente que identifica empresas reales a partir de un nombre. "
            "Usas la busqueda para confirmar que existen. No inventas empresas."
        )
    )

    # Le pedimos que conteste SOLO en formato JSON.
    # JSON es una forma ordenada de devolver datos que Python puede leer facil.
    prompt = f"""
Busca empresas reales cuyo nombre coincida o se parezca a: "{nombre}".
Prioriza empresas de Guatemala. Devuelve hasta 4 candidatas.

Responde UNICAMENTE con JSON, sin ningun texto antes o despues, con esta forma:
[
  {{"nombre": "nombre completo", "descripcion": "a que se dedica en pocas palabras", "ubicacion": "pais o ciudad", "web": "sitio web si lo encuentras"}}
]
Si no encuentras ninguna, devuelve una lista vacia: []
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config
    )

    # A veces el modelo envuelve el JSON en ```json ... ```. Lo limpiamos.
    texto = response.text.strip().replace("```json", "").replace("```", "").strip()

    # Intentamos convertir el texto en una lista de Python.
    # Si algo sale mal, devolvemos lista vacia en vez de que el programa se caiga.
    try:
        candidatos = json.loads(texto)
    except Exception:
        candidatos = []

    return candidatos


# Prueba rapida
if __name__ == "__main__":
    resultados = buscar_candidatos("Continental Motores")
    for i, empresa in enumerate(resultados, start=1):
        print(f"{i}. {empresa.get('nombre')} - {empresa.get('descripcion')} ({empresa.get('ubicacion')})")