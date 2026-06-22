"""
EL UNICO AGENTE DE REDES (el "chef").
Hacia afuera, el orquestador llama UNA sola funcion: analizar_redes().
Por dentro, coordina a sus ayudantes especializados:

  - mapeo por busqueda web (en que redes esta la empresa)  -> aqui mismo
  - YouTube (videos mas vistos y recientes, datos reales)  -> agente_youtube.py
  - Instagram (posts con likes/comentarios)                -> agente_instagram.py

"""

from google import genai
from google.genai import types
from config import GOOGLE_API_KEY

# Los ayudantes especializados
from agente_youtube import analizar_youtube
from agente_instagram import resumen_instagram

REDES = ["Instagram", "Facebook", "TikTok", "X", "YouTube", "LinkedIn"]


def _mapear_presencia(empresa, web=None):
    """Ayudante de mapeo: en que redes esta la empresa (por busqueda web)."""
    client = genai.Client(api_key=GOOGLE_API_KEY)
    config = types.GenerateContentConfig(
        tools=[{"google_search": {}}],
        system_instruction=(
            "Eres un analista de redes sociales del mercado guatemalteco. "
            "Trabajas SOLO con informacion publica encontrada al buscar. "
            "No inventas cuentas: si no encuentras una red, escribes 'Sin datos'."
        )
    )
    contexto_web = f" Su sitio web es {web}." if web else ""
    prompt = f"""
Investiga en internet la presencia en redes sociales de la marca {empresa} (Guatemala).{contexto_web}

Revisa estas redes: {", ".join(REDES)}.

Para CADA red, responde en una sola linea:
<Red>: usuario o enlace | tipo de contenido | actividad (alta / media / baja)

Reglas estrictas:
- Responde en espanol, una linea por red, en el orden listado.
- Si no encuentras una red, escribe: "<Red>: Sin datos".
- Se telegrafico, sin introducciones ni relleno.
"""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config
    )
    return response.text


def analizar_redes(empresa, web=None, usuario_instagram=None):
    """
    FUNCION UNICA que usa el orquestador.
    Junta: mapa de presencia + datos reales de YouTube + (opcional) Instagram.
    Devuelve un solo texto compacto.
    """

    # 1) Mapa de presencia en todas las redes
    mapa = _mapear_presencia(empresa, web)

    # 2) YouTube (datos reales). Si falla, no rompe lo demas.
    try:
        youtube = analizar_youtube(empresa)
    except Exception as e:
        youtube = f"YouTube no disponible: {e}"

    # 3) Instagram (opcional: solo si nos dan el usuario y hay token configurado)
    if usuario_instagram:
        try:
            instagram = resumen_instagram(usuario_instagram)
        except Exception as e:
            instagram = f"Instagram no disponible: {e}"
    else:
        instagram = "(No se indico usuario de Instagram; se omite.)"

    # 4) El chef junta todo en un solo resultado
    return f"""PRESENCIA EN REDES
{mapa}

YOUTUBE (datos reales)
{youtube}

INSTAGRAM
{instagram}"""


# Prueba rapida
if __name__ == "__main__":
    print(analizar_redes("Continental Motores"))
