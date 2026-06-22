"""
AGENTE DE YOUTUBE. Trae datos REALES de cualquier canal publico (la empresa
o su competencia): suscriptores, los videos mas vistos y los mas recientes
(lanzamientos), con vistas, likes y comentarios.
"""

import requests
from config import YOUTUBE_API_KEY

BASE = "https://www.googleapis.com/youtube/v3"


def _get(endpoint, params):
    """Hace una llamada a la API y devuelve el JSON. Si hay error, avisa claro."""
    params["key"] = YOUTUBE_API_KEY
    respuesta = requests.get(f"{BASE}/{endpoint}", params=params)
    datos = respuesta.json()
    if "error" in datos:
        mensaje = datos["error"].get("message", "error desconocido")
        raise RuntimeError(mensaje)
    return datos


def _buscar_canal(nombre):
    """Busca un canal por nombre. Devuelve su id y titulo, o None si no lo halla."""
    datos = _get("search", {
        "part": "snippet",
        "q": nombre,
        "type": "channel",
        "maxResults": 1,
    })
    items = datos.get("items", [])
    if not items:
        return None
    snip = items[0]["snippet"]
    return {"channel_id": snip["channelId"], "titulo": snip["title"]}


def _videos(channel_id, orden, n=5):
    """
    Trae videos de un canal con sus estadisticas.
    orden = 'viewCount' (mas vistos) o 'date' (mas recientes).
    """
    # 1) Buscamos los videos del canal
    busqueda = _get("search", {
        "part": "snippet",
        "channelId": channel_id,
        "type": "video",
        "order": orden,
        "maxResults": n,
    })
    ids = [it["id"]["videoId"] for it in busqueda.get("items", []) if it.get("id", {}).get("videoId")]
    if not ids:
        return []

    # 2) Pedimos las estadisticas de esos videos
    detalle = _get("videos", {
        "part": "statistics,snippet",
        "id": ",".join(ids),
    })

    videos = []
    for it in detalle.get("items", []):
        stats = it.get("statistics", {})
        videos.append({
            "titulo": it["snippet"]["title"],
            "fecha": it["snippet"]["publishedAt"][:10],
            "vistas": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comentarios": int(stats.get("commentCount", 0)),
        })
    return videos


def analizar_youtube(nombre):
    """
    Funcion lista para el orquestador. Devuelve un TEXTO compacto con
    suscriptores, videos mas vistos y videos mas recientes.
    """
    try:
        canal = _buscar_canal(nombre)
        if not canal:
            return f"No encontre un canal de YouTube para '{nombre}'."

        stats = _get("channels", {"part": "statistics,snippet", "id": canal["channel_id"]})
        suscriptores = "oculto"
        if stats.get("items"):
            suscriptores = stats["items"][0].get("statistics", {}).get("subscriberCount", "oculto")

        mas_vistos = _videos(canal["channel_id"], "viewCount", 3)
        recientes = _videos(canal["channel_id"], "date", 3)

    except RuntimeError as e:
        return f"Error de YouTube: {e}"

    lineas = [
        f"Canal: {canal['titulo']}",
        f"Suscriptores: {suscriptores}",
        "",
        "Videos mas vistos:",
    ]
    for v in mas_vistos:
        lineas.append(f"  - {v['vistas']} vistas | {v['likes']} likes | {v['comentarios']} comentarios | {v['titulo'][:60]}")

    lineas.append("")
    lineas.append("Lanzamientos recientes:")
    for v in recientes:
        lineas.append(f"  - {v['fecha']} | {v['vistas']} vistas | {v['titulo'][:60]}")

    return "\n".join(lineas)


# Prueba rapida
if __name__ == "__main__":
    print(analizar_youtube("Continental Motores"))
