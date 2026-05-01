from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import app

# ==============================
# 🔧 CONFIGURACIÓN CHROME
# ==============================

options = Options()
options.add_argument(r"--user-data-dir=C:\dev\sr_cobro\chrome_profile")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(r"C:\dev\sr_cobro\chromedriver.exe")

driver = webdriver.Chrome(
    service=service,
    options=options
)

# ==============================
# 🌐 ABRIR WHATSAPP
# ==============================

driver.get("https://web.whatsapp.com")

print("Escaneá QR si es la primera vez...")
time.sleep(25)

print("BOT WHATSAPP ACTIVO 🚀")

# ==============================
# 🔍 FUNCIONES
# ==============================

def leer_ultimo_mensaje():
    try:
        # SOLO mensajes que te mandan (cliente)
        mensajes = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")
        if mensajes:
            texto = mensajes[-1].text.strip()
            if texto != "":
                return texto
    except Exception as e:
        print("Error leyendo mensaje:", e)
    return None


def enviar_respuesta(texto):
    try:
        # caja de escritura real
        caja = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        caja.click()
        caja.send_keys(texto)
        caja.send_keys(Keys.ENTER)
    except Exception as e:
        print("Error enviando:", e)


# ==============================
# 🔁 LOOP PRINCIPAL
# ==============================

ultimo = ""

while True:
    try:
        msg = leer_ultimo_mensaje()

        if msg and msg != ultimo:
            print("Nuevo mensaje:", msg)

            respuesta = app.responder(msg)

            if respuesta:
                enviar_respuesta(respuesta)
                print("Respuesta enviada:", respuesta)

            ultimo = msg

        time.sleep(2)

    except Exception as e:
        print("Error en loop:", e)
        time.sleep(5)