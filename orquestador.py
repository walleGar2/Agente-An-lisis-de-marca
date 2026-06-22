"""
El ORQUESTADOR (el "jefe"). Hace el flujo completo:
  1. Busca empresas candidatas (desambiguador).
  2. Te deja elegir la correcta.
  3. La analiza a fondo: investigacion web + mapa de redes sociales.

Cada agente hace UNA cosa; el orquestador solo los coordina y junta el reporte.
"""

from desambiguador import buscar_candidatos
from agente_investigador import investigar_marca
from agente_redes import analizar_redes


def correr_analisis(empresa, web=None, cuentas=None):
    """
    Analiza a fondo una empresa YA CONFIRMADA.
    Devuelve un reporte final (texto).
    """

    print(f"Analizando a fondo: {empresa}...")

    # --- PASO 1: Investigacion web (noticias, reputacion, competidores) ---
    print("Investigando en internet...")
    investigacion = investigar_marca(empresa, web)

    # --- PASO 2: Redes sociales (UN solo agente coordina todo) ---
    print("Analizando redes sociales...")
    redes = analizar_redes(empresa, web)

    # --- PASO 3: Armar el reporte final ---
    reporte = f"""
========================================
   REPORTE DE ANALISIS DE MARCA
   Empresa: {empresa}
   Web: {web if web else "no especificada"}
========================================

--- INVESTIGACION WEB ---
{investigacion}

--- REDES SOCIALES ---
{redes}
"""
    return reporte


def flujo_completo():
    """Flujo interactivo para la terminal: nombre -> candidatas -> elegir -> analisis."""

    nombre = input("Nombre de la empresa a analizar: ").strip()

    print("Buscando empresas que coincidan...")
    candidatos = buscar_candidatos(nombre)

    if not candidatos:
        print("No encontre empresas con ese nombre. Revisa la escritura e intenta de nuevo.")
        return

    print("\nEncontre estas empresas:")
    for i, c in enumerate(candidatos, start=1):
        print(f"  {i}. {c.get('nombre')} - {c.get('descripcion')} ({c.get('ubicacion')})")

    try:
        eleccion = int(input("\nElige el numero de la empresa correcta: "))
        elegida = candidatos[eleccion - 1]
    except (ValueError, IndexError):
        print("Eleccion no valida. Intenta de nuevo.")
        return

    reporte = correr_analisis(elegida.get("nombre"), elegida.get("web"))
    print(reporte)


if __name__ == "__main__":
    flujo_completo()
