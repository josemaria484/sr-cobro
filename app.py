import json
from datetime import datetime, timezone
from pathlib import Path


QUEUE_PATH = Path(__file__).resolve().parent / "handoff_queue.jsonl"


def _encolar_handoff(motivo, texto):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "motivo": motivo,
        "mensaje": texto,
    }
    with QUEUE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def procesar(texto):
    texto = texto.lower().strip()

    precio = "170.000"
    modelo = "respaldo modelo Canelón"

    saludo = any(p in texto for p in ["hola", "buenas", "buen día", "buen dia", "buenas tardes", "buenas noches"])
    consulta_precio = any(p in texto for p in ["precio", "cuanto", "cuánto", "sale", "valor", "info", "consulta"])
    consulta_dos_plazas = any(p in texto for p in ["2 plazas", "dos plazas", "1.40", "140", "2", "dos"])
    consulta_una_plaza = any(p in texto for p in ["1 plaza", "una plaza", "0.90", "90", "1", "una"])
    consulta_ubicacion = any(p in texto for p in ["direccion", "dirección", "donde", "dónde", "ubicacion", "ubicación"])
    consulta_colores = any(p in texto for p in ["color", "colores", "tono", "tapizado"])
    consulta_envio = any(p in texto for p in ["envio", "envío", "mandan", "llevan", "entrega", "retiro", "retirar"])

    intencion_compra = any(p in texto for p in ["quiero", "me interesa", "comprar", "encargar", "seña", "sena", "reservo", "reservar", "lo llevo", "dale"])
    pago = any(p in texto for p in ["pago", "pagar", "transferencia", "transferir", "alias", "seña", "sena", "cuenta"])
    negociacion = any(p in texto for p in ["descuento", "mejor precio", "ultimo precio", "último precio", "rebaja"])
    objecion = any(p in texto for p in ["demora", "tarda", "confianza", "calidad", "garantia", "garantía", "otro vendedor", "más barato", "mas barato"])

    if pago:
        _encolar_handoff("pago", texto)
        return (
            "Perfecto, ya te ayudo a cerrarlo.\n\n"
            "Te paso con José para coordinar pago y reserva."
        )

    if negociacion:
        _encolar_handoff("negociacion", texto)
        return (
            "Dale, eso lo revisamos bien para darte la mejor opción.\n\n"
            "Te paso con José y lo ve con vos."
        )

    if objecion:
        _encolar_handoff("objecion", texto)
        return (
            "Entiendo. Eso te lo aclaro bien para que compres tranquilo.\n\n"
            "Te paso con José así lo ve con vos personalmente."
        )

    if intencion_compra:
        _encolar_handoff("cierre", texto)
        return (
            "Buenísimo 👍\n\n"
            "Ya te paso con José para cerrar reserva, entrega o retiro."
        )

    if consulta_ubicacion:
        return (
            "Estamos en San Rafael 📍\n\n"
            "Decime si sos de San Rafael o alrededores y te paso bien la ubicación."
        )

    if consulta_envio:
        return (
            "Sí, podemos coordinar entrega o retiro según la zona 🚚\n\n"
            "¿Sos de San Rafael o alrededores?"
        )

    if consulta_colores:
        return (
            "Lo tenemos en varios colores y con muy buena terminación 👌\n\n"
            "¿Lo buscás para 2 plazas o 1 plaza?"
        )

    if consulta_dos_plazas:
        return (
            "Perfecto, para 2 plazas queda muy bien 👍\n\n"
            f"El {modelo} está en ${precio} contado.\n\n"
            "¿Sos de San Rafael o alrededores?"
        )

    if consulta_una_plaza:
        return (
            "También lo hacemos de 1 plaza sin problema 👍\n\n"
            f"El {modelo} está en ${precio} contado.\n\n"
            "¿Querés que te pase colores o vemos entrega?"
        )

    if saludo or consulta_precio:
        return (
            "Hola 😊\n\n"
            f"El {modelo} está en ${precio} contado.\n"
            "Es el más firme y el más vendido.\n\n"
            "¿Lo buscás para 2 plazas o 1 plaza?"
        )

    return (
        "Tenemos el modelo Canelón, que es el más vendido.\n\n"
        "¿Lo buscás para 2 plazas o 1 plaza?"
    )
