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

def detectar_cliente(msg):
    palabras = normalizar(msg).split()

    if "al" in palabras:
        idx = palabras.index("al")
        if idx + 1 < len(palabras):
            return palabras[idx + 1]

    return palabras[-1]

def listar_morosos(dias):
    filas = sheet.get_all_records()
    hoy = datetime.date.today()
    resultado = []

    for fila in filas:
        nombre = fila.get("nombre", "")
        deuda = int(float(fila.get("deuda_actual", 0)))
        ultimo_pago = fila.get("ultimo_pago", "")

        if deuda <= 0:
            continue

        if not ultimo_pago:
            resultado.append(f"{nombre} - debe ${deuda} - nunca pagó")
            continue

        try:
            fecha_pago = datetime.datetime.strptime(ultimo_pago, "%Y-%m-%d").date()
            diff = (hoy - fecha_pago).days

            if diff >= dias:
                if diff == 0:
                    estado = "pagó hoy"
                elif diff == 1:
                    estado = "hace 1 día"
                else:
                    estado = f"hace {diff} días"

                resultado.append(f"{nombre} - debe ${deuda} - {estado}")
        except:
            continue

    if not resultado:
        return "No hay morosos en ese rango"

    return "\n".join(resultado)

def responder(mensaje):
    msg = normalizar(mensaje)

    if msg in ("salir", "exit", "exit()", "quit", "quit()"):
        raise SystemExit

    if msg == "hoy":
        return listar_morosos(3)

    if "cuanto debe" in msg:
        cliente_query = detectar_cliente(msg)
        cliente, _ = buscar_cliente(cliente_query)
        if cliente:
            return f"{cliente['nombre']} debe ${cliente['deuda_actual']}"
        return "No encontré ese cliente"

    if "anotale" in msg or "agregale" in msg:
        monto = parsear_monto(msg)
        cliente_query = detectar_cliente(msg)

        cliente, fila = buscar_cliente(cliente_query)

        if not cliente or monto is None:
            return "Error en datos"

        deuda_actual = int(float(cliente["deuda_actual"]))
        nueva_deuda = deuda_actual + monto

        sheet.update_cell(fila, 5, nueva_deuda)
        sheet.update_cell(fila, 9, str(datetime.date.today()))

        return f"{cliente['nombre']} ahora debe ${nueva_deuda}"

    if "pago" in msg or "abono" in msg or "me dio" in msg:
        monto = parsear_monto(msg)
        cliente_query = detectar_cliente(msg)

        cliente, fila = buscar_cliente(cliente_query)

        if not cliente or monto is None:
            return "Error en datos"

        deuda_actual = int(float(cliente["deuda_actual"]))
        nueva_deuda = deuda_actual - monto

        sheet.update_cell(fila, 5, nueva_deuda)
        sheet.update_cell(fila, 9, str(datetime.date.today()))

        return f"{cliente['nombre']} pagó ${monto}. Debe ${nueva_deuda}"

    if msg.startswith("morosos"):
        partes = msg.split()
        if len(partes) >= 2 and partes[1].isdigit():
            return listar_morosos(int(partes[1]))
        return "Usá: morosos 7"

    return "No entendí el mensaje"

print("Sr Cobro listo")

while True:
    entrada = input(">> ")
    try:
        print(responder(entrada))
    except SystemExit:
        print("Saliendo...")
        break