import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import dropbox
import time
import os
import sys
import requests


sys.stdout = sys.__stdout__

# Variáveis de ambiente
REFRESH_TOKEN = st.secrets["REFRESH_TOKEN"]
APP_KEY = st.secrets["APP_KEY"]
APP_SECRET = st.secrets["APP_SECRET"]
DROPBOX_PATH = '/logs/log.txt'  # Caminho onde o arquivo será salvo no Dropbox
LOG_FILE_PATH = 'log.txt'



chrome_driver_version = '120.0.6099.183'  # Versão compatível com o Chromium 120
# Inicializar o cliente Dropbox
dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN)


def inicializar_web_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita estouro de memória
    service = Service(ChromeDriverManager(chrome_driver_version).install())  # Removendo o argumento 'version'
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Função para enviar o arquivo para o Dropbox
def upload_to_dropbox():
    try:
        with open(LOG_FILE_PATH, 'rb') as f:
            file_content = f.read()
        dbx.files_upload(file_content, DROPBOX_PATH, mode=dropbox.files.WriteMode.overwrite)
        print(f"Arquivo {LOG_FILE_PATH} enviado para o Dropbox em {DROPBOX_PATH}")
    except Exception as e:
        print(f"Erro ao enviar o arquivo para o Dropbox: {e}")



driver = inicializar_web_driver()
# Interface do Streamlit (para entrada de URL e XPath)
st.title("Streamlit + Selenium: Monitoramento Contínuo")

while True:
    try:
            driver.get("https://www.mice.com")
            texto_capturado = driver.find_element(By.XPATH,'//*[@id="header-slogan"]').text


            with open(LOG_FILE_PATH, 'a') as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {texto_capturado}\n")
            upload_to_dropbox()
            time.sleep(10)

    except Exception as e:
            print(f"Erro durante a execução: {e}")
            if 'invalid session id' in str(e):
                print("Reinicializando o WebDriver...")
                try:
                    driver.quit()  # Tenta fechar o driver antigo
                except:
                     pass
                driver = inicializar_web_driver()
            time.sleep(10)

# Certifique-se de fechar o driver ao finalizar (isso pode não ser alcançado em execução contínua no Streamlit)
try:
    driver.quit()
except:
    pass