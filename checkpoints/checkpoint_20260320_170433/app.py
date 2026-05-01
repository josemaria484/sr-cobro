import re
import json
import os

ARCHIVO = "clientes.json"

# ==============================
# CARGAR / GUARDAR
# ==============================

def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = cargar_datos()

# ==============================
# NORMALIZAR
# ==============================

def normalizar(msg):
    msg = msg.lower().strip()

    disparadores = [
        "anotale","anotame","anotar",
        "agregame","agregale",
        "sumale","sumar",
        "ponele","poneme",
        "cargale","cargame"
    ]

    for d in disparadores:
        if d in msg:
            msg = msg.replace(d, "anotame")
            break

    return msg

# ==============================
# MONTO
# ==============================

def extraer_monto(msg):
    numeros = re.findall(r"\d+", msg)
    if not numeros:
        return None

    monto = int(numeros[0])

    if "luca" in msg:
        monto *= 1000

    return monto

# ==============================
# NOMBRE + ALIAS
# ==============================

def resolver_alias(nombre, alias):
    return alias.get(nombre, nombre)

def extraer_nombre(msg, alias):

    match = re.search(r"\ba\s+([a-z0-9]+)", msg)
    if match:
        return resolver_alias(match.group(1), alias)

    match = re.search(r"\bdebe\s+([a-z0-9]+)", msg)
    if match:
        return resolver_alias(match.group(1), alias)

    palabras = msg.split()

    ignorar = {"anotame","cuanto","debe","total","lista","borrar","reset","a"}

    for palabra in reversed(palabras):
        if palabra not in ignorar and not palabra.isdigit():
            return resolver_alias(palabra, alias)

    return None

# ==============================
# LISTA
# ==============================

def armar_lista(clientes):
    if not clientes:
        return "No hay deudas"

    texto = "📋 Deudas:\n"

    for nombre, deuda in clientes.items():
        texto += f"- {nombre.capitalize()}: ${deuda}\n"

    return texto.strip()

# ==============================
# RESPONDER (MULTI USUARIO)
# ==============================

def responder(msg, numero):
    global data

    print("ORIGINAL:", msg)

    msg = normalizar(msg)

    print("NORMALIZADO:", msg)

    # ==========================
    # CREAR USUARIO SI NO EXISTE
    # ==========================
    if numero not in data:
        data[numero] = {
            "clientes": {},
            "alias": {}
        }

    clientes = data[numero]["clientes"]
    alias = data[numero]["alias"]

    monto = extraer_monto(msg)

    # ==========================
    # ALIAS
    # ==========================
    if "alias" in msg:
        partes = msg.split()

        if len(partes) >= 3:
            alias_nombre = partes[1]
            real = partes[2]

            alias[alias_nombre] = real
            guardar_datos()

            return f"Alias guardado: {alias_nombre} → {real}"

        return "Uso: alias cabezon juan"

    # ==========================
    # LISTA
    # ==========================
    if "lista" in msg:
        return armar_lista(clientes)

    # ==========================
    # ALTA
    # ==========================
    if "anotame" in msg:

        if not monto:
            return "¿Cuánto anotamos?"

        cliente = extraer_nombre(msg, alias)

        if not cliente:
            return "¿A quién le anotamos?"

        clientes[cliente] = clientes.get(cliente, 0) + monto
        guardar_datos()

        return f"{cliente.capitalize()} ahora debe ${clientes[cliente]}"

    # ==========================
    # CONSULTA
    # ==========================
    if any(x in msg for x in ["cuanto", "debe", "total"]):

        cliente = extraer_nombre(msg, alias)

        if not cliente:
            return "¿De quién querés saber?"

        deuda = clientes.get(cliente, 0)

        return f"{cliente.capitalize()} debe ${deuda}"

    # ==========================
    # RESET
    # ==========================
    if any(x in msg for x in ["borrar", "reset"]):

        cliente = extraer_nombre(msg, alias)

        if not cliente:
            return "¿A quién querés borrar?"

        clientes[cliente] = 0
        guardar_datos()

        return f"Deuda de {cliente} reiniciada"

    return "No entendí el mensaje"
# ==============================
# 🌐 FUNCION PARA API / WHATSAPP
# ==============================

def procesar_mensaje(texto):
    try:
        texto = texto.lower().strip()

        # ejemplo básico (usa tu lógica real después)
        if "anotale" in texto:
            return "Anotado correctamente"

        if "cuanto debe" in texto:
            return "Debe consultar (lógica pendiente)"

        return "No entendí el mensaje"

    except Exception as e:
        return f"Error: {str(e)}"

