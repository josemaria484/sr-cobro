def procesar(texto):
    texto = texto.lower().strip()

    precio = ".000 contado"
    modelo = "respaldo modelo Canelón"

    # 🔹 Entrada típica: precio / hola
    if any(p in texto for p in ["hola","precio","cuanto","cuánto","info","consulta"]):
        return (
            "Hola 😊\n\n"
            "El respaldo modelo Canelón está en " + precio + ".\n"
            "Es uno de los más firmes y más pedidos.\n\n"
            "¿Lo buscás para 2 plazas?"
        )

    # 🔹 Medida
    if "2" in texto or "dos" in texto:
        return (
            "Perfecto 👍 queda muy bien en 2 plazas.\n\n"
            "Lo tenemos en varios colores y con muy buena terminación.\n\n"
            "¿Querés que te pase los colores o estás viendo para comprar ya?"
        )

    # 🔹 Interés alto
    if any(p in texto for p in ["si","sí","quiero","me interesa","comprar"]):
        return (
            "Buenísimo 👍\n\n"
            "Trabajamos con seña y lo hacemos a pedido.\n\n"
            "¿Sos de San Rafael o alrededores?"
        )

    # 🔹 Ubicación (recién acá)
    if any(p in texto for p in ["direccion","dirección","donde","ubicacion","ubicación"]):
        return (
            "Estamos en San Rafael.\n\n"
            "Si querés coordinamos así venís a verlo y elegís color tranquilo.\n\n"
            "Avisame y te paso la ubicación 📍"
        )

    return (
        "Hola 😊\n\n"
        "Tenemos respaldos en varios colores.\n"
        "El modelo Canelón está en " + precio + ".\n\n"
        "¿Lo buscás para 2 plazas?"
    )
