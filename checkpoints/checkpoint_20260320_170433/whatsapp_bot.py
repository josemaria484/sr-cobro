from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import app

# ==============================
# 🔧 CONFIGURACIÓN CHROME
# ==============================

options = Options()
options.add_argument(r"--user-data-dir=C:\dev\sr_cobro\chrome_profile")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")

# FIX CRASH
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(r"C:\dev\sr_cobro\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# ==============================
# 🌐 ABRIR WHATSAPP
# ==============================

driver.get("https://web.whatsapp.com")

print("Esperando WhatsApp...")
time.sleep(25)

print("BOT WHATSAPP ACTIVO 🚀")

# ==============================
# 🔍 FUNCIONES
# ==============================

def abrir_chat_con_mensaje_nuevo():
    try:
        notificaciones = driver.find_elements(By.XPATH, "//span[@data-testid='icon-unread-count']")

        if notificaciones:
            try:
                chat = notificaciones[0].find_element(By.XPATH, "./ancestor::div[@role='listitem']")
                chat.click()
                time.sleep(2)
                print("📩 Chat abierto automáticamente")
                return True
            except StaleElementReferenceException:
                print("Reintentando apertura de chat...")
                return False

    except Exception as e:
        print("Error buscando chats:", e)

    return False


def obtener_mensajes_entrantes():
    """
    Devuelve todos los spans de texto de mensajes entrantes.
    """
    try:
        return driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'message-in')]//span[@dir='ltr']"
        )
    except Exception:
        return []


def leer_ultimo_mensaje():
    try:
        time.sleep(1)

        mensajes = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")

        if not mensajes:
            return None

        ultimo = mensajes[-1]
        texto = ultimo.text.strip()

        if not texto:
            return None

        # 🔥 CLAVE: solo última línea
        lineas = texto.split("\n")
        texto_limpio = lineas[-1].strip()

        return texto_limpio

    except:
        print("Reintentando lectura...")
        return None

def enviar_respuesta(texto):
    try:
        time.sleep(0.5)

        caja = driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
        caja.click()
        caja.send_keys(texto)
        time.sleep(0.3)
        caja.send_keys(Keys.ENTER)

    except Exception as e:
        print("Error enviando:", e)


def obtener_chat_actual():
    try:
        encabezado = driver.find_element(By.XPATH, "//header//span[@dir='auto']")
        nombre = encabezado.text.strip()
        return nombre
    except NoSuchElementException:
        return ""
    except Exception:
        return ""


# ==============================
# 🔁 LOOP PRINCIPAL
# ==============================

ultimo_texto = ""
ultimo_chat = ""

while True:
    try:
        abrir_chat_con_mensaje_nuevo()

        chat_actual = obtener_chat_actual()
        msg = leer_ultimo_mensaje()

        if msg:
            # solo procesa si cambió texto o cambió chat
            if msg != ultimo_texto or chat_actual != ultimo_chat:
                print("Nuevo mensaje:", msg)

                respuesta = app.responder(msg)

                if respuesta:
                    enviar_respuesta(respuesta)
                    print("Respuesta enviada:", respuesta)

                ultimo_texto = msg
                ultimo_chat = chat_actual

        time.sleep(2)

    except Exception as e:
        print("Error en loop:", e)
        time.sleep(5)