"""
agente_investigador.py
-----------------------
Este es el AGENTE INVESTIGADOR.
Su unico trabajo: buscar informacion publica de una marca en internet
(usando Gemini + Google Search) y devolver un texto con lo que encontro.

Toda su logica vive dentro de una funcion: investigar_marca(empresa)
Asi el orquestador (el jefe) solo tiene que "llamarla".
"""

from google import genai
from google.genai import types
from config import GOOGLE_API_KEY


def investigar_marca(empresa, web=None):
    """
    Recibe el nombre de una empresa (texto) y, opcionalmente, su sitio web.
    Devuelve un reporte (texto) con informacion publica encontrada en internet.
    El sitio web sirve para "anclar" el analisis a la empresa correcta.
    """

    # 1) Nos conectamos a Gemini con nuestra llave
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # 2) Configuramos la personalidad del agente y le damos la busqueda de Google
    config = types.GenerateContentConfig(
        tools=[{"google_search": {}}],
        system_instruction=(
            "Eres un analista de marca especializado en el mercado guatemalteco. "
            "Trabajas SOLO con informacion publica que encuentres al buscar en internet "
            "(noticias, sitios web, comunicados, blogs). No inventas datos: si algo no "
            "aparece en tu busqueda, lo dices claramente."
        )
    )

    # 3) Le damos la tarea concreta (usamos el nombre de la empresa que nos pasaron)
    # Si nos dieron el sitio web, lo agregamos para anclar la busqueda a la empresa correcta
    contexto_web = f" Su sitio web oficial es {web}." if web else ""

    prompt = f"""
Investiga la marca {empresa} (Guatemala) usando informacion publica en internet.{contexto_web}

Entrega un resumen COMPACTO con estos puntos, en este formato exacto:

A que se dedica: (1 frase)
Noticias/campanas recientes: (maximo 2 vinetas, 1 linea cada una)
Percepcion publica: (1 frase)
Competidores en Guatemala: (solo nombres, separados por comas)
Recomendaciones: (maximo 3 vinetas, 1 linea cada una)

Reglas estrictas:
- Responde en espanol.
- Se telegrafico: solo datos clave, sin introducciones ni relleno.
- No repitas la pregunta ni agregues conclusiones.
- Si un dato no existe, escribe solo: "Sin datos".
"""

    # 4) Hacemos la consulta y devolvemos solo el texto de la respuesta
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config
    )

    return response.text


# Prueba rapida: solo corre si ejecutas ESTE archivo directamente
if __name__ == "__main__":
    print(investigar_marca("Continental Motores"))