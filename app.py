def procesar(texto):
    texto = texto.lower().strip()

    precio = ".000 contado"
    modelo = "respaldo modelo Canelón"

    saludo = any(p in texto for p in ["hola", "buenas", "buen día", "buen dia", "buenas tardes", "buenas noches"])
    consulta_precio = any(p in texto for p in ["precio", "cuanto", "cuánto", "sale", "valor", "info", "consulta"])
    consulta_medida = any(p in texto for p in ["2 plazas", "dos plazas", "1.40", "140", "2", "dos"])
    interes_compra = any(p in texto for p in ["si", "sí", "quiero", "me interesa", "comprar", "encargar", "seña", "reservo"])
    consulta_ubicacion = any(p in texto for p in ["direccion", "dirección", "donde", "dónde", "ubicacion", "ubicación"])
    consulta_colores = any(p in texto for p in ["color", "colores", "tono", "tapizado"])
    consulta_envio = any(p in texto for p in ["envio", "envío", "mandan", "llevan", "entrega"])

    if consulta_ubicacion:
        return (
            "Estamos en San Rafael 📍\n\n"
            "Si querés, coordinamos para que vengas a verlo, elegir color y dejarlo reservado en el momento.\n\n"
            "Decime si sos de San Rafael o alrededores y te paso bien la ubicación."
        )

    if consulta_envio:
        return (
            "Sí, podemos coordinar la entrega según la zona 🚚\n\n"
            "Si me decís de dónde sos, te confirmo la mejor opción y seguimos con la reserva si te sirve."
        )

    if consulta_colores:
        return (
            "Lo tenemos en varios colores y con muy buena terminación 👌\n\n"
            "Si querés, te paso las opciones disponibles y vemos cuál te combina mejor.\n\n"
            "¿Lo estás buscando para 2 plazas?"
        )

    if interes_compra:
        return (
            "Buenísimo 👍\n\n"
            "Trabajamos con seña porque se hace a pedido, así te asegurás color y entrega.\n\n"
            "Si querés avanzar, decime de dónde sos y te explico cómo reservarlo."
        )

    if consulta_medida:
        return (
            "Perfecto, para 2 plazas queda muy bien 👍\n\n"
            f"El {modelo} está en {precio} y es uno de los más elegidos por la firmeza y la terminación.\n\n"
            "¿Querés que te pase colores o preferís que te explique cómo reservarlo?"
        )

    if saludo or consulta_precio:
        return (
            "Hola 😊\n\n"
            f"El {modelo} está en {precio}.\n"
            "Es un modelo muy pedido porque queda firme, prolijo y viste muchísimo la habitación.\n\n"
            "¿Lo buscás para 2 plazas o querés ver colores primero?"
        )

    return (
        "Hola 😊\n\n"
        f"Tenemos el {modelo} en varios colores, con muy buena terminación y a {precio}.\n\n"
        "Si querés, te ayudo a elegir rápido según la medida o te explico cómo reservarlo."
    )
