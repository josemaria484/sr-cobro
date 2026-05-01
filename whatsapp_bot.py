from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import app

# ==============================
# 🔧 CONFIG CHROME
# ==============================

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(r"C:\dev\sr_cobro\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# ==============================
# 🌐 ABRIR WHATSAPP
# ==============================

driver.get("https://web.whatsapp.com")

print("Escaneá QR si es la primera vez...")

# Espera flexible
for _ in range(60):
    try:
        driver.find_element(By.XPATH, '//div[@id="pane-side"]')
        print("BOT WHATSAPP ACTIVO")
        break
    except:
        time.sleep(1)
else:
    print("❌ WhatsApp no cargó")

# ==============================
# 🔍 FUNCIONES
# ==============================

def obtener_input_mensaje():
    try:
        elementos = driver.find_elements(
            By.XPATH,
            '//footer//*[@contenteditable="true"][@role="textbox"]'
        )
        for el in elementos:
            if el.is_displayed():
                return el
        return None
    except:
        return None


def asegurar_chat_activo():
    return obtener_input_mensaje() is not None


def leer_mensaje_entrante():
    try:
        mensajes = driver.find_elements(
            By.XPATH,
            '//div[contains(@class,"message-in")]//span[@dir="ltr"]'
        )

        textos = [m.text.strip() for m in mensajes if m.text.strip()]

        if not textos:
            return None

        return textos[-1]

    except Exception as e:
        print("ERROR LEYENDO:", e)
        return None


def enviar_respuesta(texto):
    try:
        for _ in range(3):  # 🔥 reintentos por stale
            try:
                caja = obtener_input_mensaje()
                if not caja:
                    return False

                caja.click()
                time.sleep(0.2)

                caja.send_keys(Keys.CONTROL + "a")
                caja.send_keys(Keys.BACKSPACE)

                caja.send_keys(texto)
                time.sleep(0.1)
                caja.send_keys(Keys.ENTER)

                return True

            except:
                time.sleep(0.5)

        print("ERROR ENVIANDO: reintentos fallidos")
        return False

    except Exception as e:
        print("ERROR ENVIANDO:", e)
        return False


# 🔥 detectar chats con mensajes nuevos
def abrir_chat_con_nuevo_mensaje():
    try:
        chats = driver.find_elements(
            By.XPATH,
            '//div[@id="pane-side"]//div[@role="row"]'
        )

        for chat in chats:
            try:
                notif = chat.find_elements(By.XPATH, './/span[@aria-label]')
                if notif:
                    chat.click()
                    time.sleep(2)
                    print("📩 Chat abierto automáticamente")
                    return True
            except:
                continue

        return False

    except Exception as e:
        print("ERROR buscando chats:", e)
        return False


# ==============================
# 🔁 LOOP PRINCIPAL
# ==============================

ultimo_mensaje = None
ultimo_log = 0

while True:
    try:
        if not asegurar_chat_activo():
            if abrir_chat_con_nuevo_mensaje():
                continue

            if time.time() - ultimo_log > 5:
                print("Esperando mensajes...")
                ultimo_log = time.time()

            time.sleep(2)
            continue

        mensaje = leer_mensaje_entrante()

        if not mensaje or mensaje == ultimo_mensaje:
            time.sleep(1)
            continue

        print("[RECIBIDO]:", mensaje)

        respuesta = app.procesar_mensaje(mensaje)

        if not respuesta:
            respuesta = "No entendí el mensaje"

        print("[RESPUESTA]:", respuesta)

        if enviar_respuesta(respuesta):
            ultimo_mensaje = mensaje

        time.sleep(2)

    except KeyboardInterrupt:
        print("Bot detenido")
        break

    except Exception as e:
        print("ERROR LOOP:", e)
        time.sleep(3)