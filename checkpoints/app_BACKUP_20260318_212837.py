import gspread
from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode
import datetime
import re

CRED_FILE = r"C:\dev\sr_cobro\credenciales.json"
SHEET_KEY = "1g5aJuVDQHs5n7NmFGlbYSvtB2NT_COOYH-8sLF1KV2A"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(CRED_FILE, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(SHEET_KEY).worksheet("clientes")

def normalizar(texto):
    return unidecode(str(texto).lower().strip())

def buscar_cliente(query):
    q = normalizar(query)
    filas = sheet.get_all_records()

    for i, fila in enumerate(filas, start=2):
        nombre = normalizar(fila.get("nombre", ""))
        apodos = normalizar(fila.get("apodos", ""))

        print(f"[DEBUG buscar] q={q} | nombre={nombre} | apodos={apodos}")

        if q == nombre or q == apodos or q in nombre or q in apodos:
            return fila, i

    return None, None

def parsear_monto(texto):
    t = normalizar(texto)

    m = re.search(r"(\d+)\s*luca", t)
    if m:
        return int(m.group(1)) * 1000

    m = re.search(r"(\d+)\s*mil", t)
    if m:
        return int(m.group(1)) * 1000

    m = re.search(r"\d+", t)
    if m:
        return int(m.group())

    return None

def fecha_proximo_viernes():
    hoy = datetime.date.today()
    dias = (4 - hoy.weekday()) % 7
    if dias == 0:
        dias = 7
    return hoy + datetime.timedelta(days=dias)

def parsear_fecha(texto):
    t = normalizar(texto)

    if "hoy" in t:
        return datetime.date.today()

    if "manana" in t:
        return datetime.date.today() + datetime.timedelta(days=1)

    if "viernes" in t:
        return fecha_proximo_viernes()

    return None

def detectar_cliente(msg):
    palabras = normalizar(msg).split()

    if "al" in palabras:
        idx = palabras.index("al")
        if idx + 1 < len(palabras):
            return palabras[idx + 1]

    return palabras[-1]

def responder(mensaje):
    msg = normalizar(mensaje)

    if msg in ("salir", "exit", "exit()", "quit", "quit()"):
        raise SystemExit

    # CONSULTA
    if "cuanto debe" in msg:
        cliente_query = detectar_cliente(msg)
        print(f"[DEBUG consulta] cliente_query={cliente_query}")
        cliente, _ = buscar_cliente(cliente_query)

        if cliente:
            return f"{cliente['nombre']} debe ${cliente['deuda_actual']}"
        return "No encontré ese cliente"

    # ALTA DEUDA
    if "anotale" in msg or "agregale" in msg:
        monto = parsear_monto(msg)
        fecha = parsear_fecha(msg)
        cliente_query = detectar_cliente(msg)

        print(f"[DEBUG alta] cliente_query={cliente_query} | monto={monto} | fecha={fecha}")

        cliente, fila = buscar_cliente(cliente_query)

        if not cliente:
            return "Cliente no encontrado"

        if monto is None:
            return "No entendí el monto"

        deuda_actual = int(float(cliente["deuda_actual"]))
        nueva_deuda = deuda_actual + monto

        sheet.update_cell(fila, 5, nueva_deuda)

        hoy = datetime.date.today()
        sheet.update_cell(fila, 9, str(hoy))

        if fecha:
            sheet.update_cell(fila, 6, str(fecha))

        return f"Listo. Nueva deuda de {cliente['nombre']}: ${nueva_deuda}"

    # PAGO
    if "pago" in msg or "abono" in msg or "me dio" in msg:
        monto = parsear_monto(msg)
        cliente_query = detectar_cliente(msg)

        print(f"[DEBUG pago] cliente_query={cliente_query} | monto={monto}")

        cliente, fila = buscar_cliente(cliente_query)

        if not cliente:
            return "Cliente no encontrado"

        if monto is None:
            return "No entendí el monto"

        deuda_actual = int(float(cliente["deuda_actual"]))
        nueva_deuda = deuda_actual - monto

        sheet.update_cell(fila, 5, nueva_deuda)

        hoy = datetime.date.today()
        sheet.update_cell(fila, 9, str(hoy))

        if nueva_deuda > 0:
            return f"{cliente['nombre']} pagó ${monto}. Debe ahora ${nueva_deuda}"
        elif nueva_deuda == 0:
            return f"{cliente['nombre']} saldó la deuda ✅"
        else:
            return f"{cliente['nombre']} pagó ${monto}. Quedó a favor ${abs(nueva_deuda)}"

    return "No entendí el mensaje"

print("Sr Cobro listo")

while True:
    entrada = input(">> ")
    try:
        print(responder(entrada))
    except SystemExit:
        print("Saliendo...")
        break