"""
orquestador.py
--------------
Este es el ORQUESTADOR (el "jefe").
Ahora hace el FLUJO COMPLETO:
  1. Busca empresas candidatas (desambiguador).
  2. Te deja elegir la correcta.
  3. Analiza a fondo la empresa elegida (investigador), anclada a su sitio web.

La funcion correr_analisis() se queda enfocada en UNA cosa:
analizar una empresa ya confirmada. Asi sirve igual para la terminal
y, mas adelante, para Streamlit.
"""

from desambiguador import buscar_candidatos
from agente_investigador import investigar_marca


def correr_analisis(empresa, web=None, cuentas=None):
    """
    Analiza a fondo una empresa YA CONFIRMADA.
    - empresa: nombre de la empresa (texto)
    - web: sitio web, para anclar el analisis a la empresa correcta
    - cuentas: cuentas de redes sociales (lo usaremos despues)

    Devuelve un reporte final (texto).
    """

    print(f"Analizando a fondo: {empresa}...")

    # --- PASO 1: Agente investigador (web publica) ---
    investigacion = investigar_marca(empresa, web)

    # --- PASO 2: Agente de Instagram (aun no conectado) ---
    # Aqui, mas adelante: datos_redes = analizar_instagram(cuentas)
    datos_redes = "(El analisis de redes sociales se agregara mas adelante.)"

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
{datos_redes}
"""
    return reporte


def flujo_completo():
    """
    Flujo interactivo para la terminal:
    nombre -> candidatas -> elegir -> analisis.
    (Mas adelante, Streamlit hara estos mismos pasos pero con pantalla.)
    """

    # 1) Pedir el nombre
    nombre = input("Nombre de la empresa a analizar: ").strip()

    # 2) Buscar candidatas
    print("Buscando empresas que coincidan...")
    candidatos = buscar_candidatos(nombre)

    # 3) Si no hay candidatas, avisar y salir
    if not candidatos:
        print("No encontre empresas con ese nombre. Revisa la escritura e intenta de nuevo.")
        return

    # 4) Mostrar las candidatas numeradas
    print("\nEncontre estas empresas:")
    for i, c in enumerate(candidatos, start=1):
        print(f"  {i}. {c.get('nombre')} - {c.get('descripcion')} ({c.get('ubicacion')})")

    # 5) Pedir que elija una (con validacion sencilla)
    try:
        eleccion = int(input("\nElige el numero de la empresa correcta: "))
        elegida = candidatos[eleccion - 1]
    except (ValueError, IndexError):
        print("Eleccion no valida. Intenta de nuevo.")
        return

    # 6) Analizar la elegida, pasando su sitio web para anclar el analisis
    reporte = correr_analisis(elegida.get("nombre"), elegida.get("web"))
    print(reporte)


# Corre el flujo completo desde la terminal
if __name__ == "__main__":
    flujo_completo()