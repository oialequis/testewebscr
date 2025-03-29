import streamlit as st
from playwright.sync_api import sync_playwright
import dropbox
import time
import os
import sys

sys.stdout = sys.__stdout__

# Variáveis de ambiente
REFRESH_TOKEN = st.secrets["REFRESH_TOKEN"]
APP_KEY = st.secrets["APP_KEY"]
APP_SECRET = st.secrets["APP_SECRET"]
DROPBOX_PATH = '/logs/log.txt'  # Caminho onde o arquivo será salvo no Dropbox
LOG_FILE_PATH = 'log.txt'

# Inicializar o cliente Dropbox
dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN)

# Função para enviar o arquivo para o Dropbox
def upload_to_dropbox():
    try:
        with open(LOG_FILE_PATH, 'rb') as f:
            file_content = f.read()
        dbx.files_upload(file_content, DROPBOX_PATH, mode=dropbox.files.WriteMode.overwrite)
        print(f"Arquivo {LOG_FILE_PATH} enviado para o Dropbox em {DROPBOX_PATH}")
    except Exception as e:
        print(f"Erro ao enviar o arquivo para o Dropbox: {e}")

# Interface do Streamlit (para entrada de URL e XPath)
st.title("Streamlit + Playwright: Monitoramento Contínuo")

def run_monitoring():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        while True:
            try:
                page.goto("https://www.mice.com")
                texto_capturado = page.locator('//*[@id="header-slogan"]').text_content()

                with open(LOG_FILE_PATH, 'a') as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {texto_capturado}\n")
                upload_to_dropbox()
                time.sleep(10)

            except Exception as e:
                print(f"Erro durante a execução: {e}")
                # Não é necessário reiniciar o browser/page no Playwright para este erro específico
                # O Playwright lida bem com a maioria das situações e pode continuar a usar a mesma instância.
                # Se houver um erro crítico, você pode considerar reiniciar o navegador ou a página.
                time.sleep(10)

        browser.close()

if __name__ == '__main__':
    run_monitoring()