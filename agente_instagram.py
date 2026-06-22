"""
AGENTE DE INSTAGRAM.
Trae datos publicos de una cuenta de Instagram de empresa usando la API
oficial de Meta (funcion "Business Discovery"): seguidores, y por cada
publicacion sus likes y comentarios.

Las llaves (token e ID) NO van escritas aqui: se leen desde config.py,
que a su vez las saca de los Secrets. Asi este archivo es seguro para GitHub.
"""

import requests
from config import META_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID

# Version de la API de Meta. Si algun dia da error de version, sube el numero.
API_VERSION = "v21.0"


def obtener_datos_instagram(usuario):
    """
    Pide a Meta los datos publicos de la cuenta 'usuario' (ej: "continentalmotores").
    Devuelve un diccionario con los datos, o None si hubo error.
    """
    url = f"https://graph.facebook.com/{API_VERSION}/{IG_BUSINESS_ACCOUNT_ID}"

    # Que datos queremos de esa cuenta
    campos = (
        f"business_discovery.username({usuario})"
        "{followers_count,media_count,media{caption,like_count,comments_count,timestamp}}"
    )

    parametros = {
        "fields": campos,
        "access_token": META_ACCESS_TOKEN,
    }

    respuesta = requests.get(url, params=parametros)
    datos = respuesta.json()

    # Si Meta devolvio un error, lo mostramos claro y devolvemos None
    if "error" in datos:
        print("Meta devolvio un error:")
        print(datos["error"].get("message", datos["error"]))
        return None

    return datos


def resumen_instagram(usuario):
    """
    Version lista para el orquestador: devuelve un TEXTO corto con
    seguidores y las publicaciones con mas likes.
    """
    datos = obtener_datos_instagram(usuario)

    if not datos:
        return "No se pudieron obtener datos de Instagram (revisa el usuario o el token)."

    info = datos["business_discovery"]
    publicaciones = info.get("media", {}).get("data", [])

    # Ordenamos las publicaciones por likes, de mayor a menor, y tomamos las 3 primeras
    publicaciones.sort(key=lambda p: p.get("like_count", 0), reverse=True)
    top = publicaciones[:3]

    lineas = [
        f"Usuario: @{usuario}",
        f"Seguidores: {info.get('followers_count', 'Sin datos')}",
        f"Publicaciones totales: {info.get('media_count', 'Sin datos')}",
        "Top publicaciones por likes:",
    ]
    for p in top:
        texto = (p.get("caption") or "(sin texto)")[:60]
        lineas.append(f"  - {p.get('like_count', 0)} likes | {p.get('comments_count', 0)} comentarios | {texto}")

    return "\n".join(lineas)


# Prueba rapida: corre solo si ejecutas ESTE archivo directamente
if __name__ == "__main__":
    print(resumen_instagram("continentalmotores"))
