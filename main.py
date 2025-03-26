import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import dropbox
import time
import os

# Variáveis de ambiente
REFRESH_TOKEN = st.secrets["REFRESH_TOKEN"]
APP_KEY = st.secrets["APP_KEY"]
APP_SECRET = st.secrets["APP_SECRET"]
DROPBOX_PATH = '/logs/log.txt'  # Caminho onde o arquivo será salvo no Dropbox
LOG_FILE_PATH = 'log.txt'

chrome_driver_version = '120.0.6099.183'  # Versão compatível com o Chromium 120

# Inicializar o cliente Dropbox
dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN)

# Função para inicializar o Selenium WebDriver
def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())  # Removendo o argumento 'version'
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Função para pegar o conteúdo do elemento
def get_element_by_xpath(driver, url, xpath):
    try:
        driver.get(url)
        element = driver.find_element(By.XPATH, xpath)
        return element.text
    except Exception as e:
        return f"Erro ao encontrar o elemento: {e}"

# Função para escrever no arquivo de log
def write_to_log(content):
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {content}\n")

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
st.title("Streamlit + Selenium: Monitoramento Contínuo")

# Entrada de URL
url = st.text_input("Digite a URL da página a ser monitorada:")

# Entrada de XPath
xpath = st.text_input("Digite o XPath do elemento a ser monitorado:")

st.info("O script irá coletar o conteúdo do elemento a cada 10 segundos e salvar em log.txt.")
st.info("O arquivo log.txt será enviado para o Dropbox.")

if url and xpath:
    st.success("Monitoramento iniciado. Verifique o log.txt local e o Dropbox.")

    # Inicializar o WebDriver fora do loop
    driver = initialize_webdriver()

    while True:
        content = get_element_by_xpath(driver, url, xpath)
        write_to_log(content)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Conteúdo coletado: {content}")

        # Enviar o arquivo para o Dropbox a cada minuto (opcional, ajuste conforme necessário)
        if time.time() % 60 < 10:  # Envia nos primeiros 10 segundos de cada minuto
            upload_to_dropbox()

        time.sleep(10)

    # Certifique-se de fechar o driver ao finalizar (isso pode não ser alcançado em execução contínua no Streamlit)
    driver.quit()
else:
    st.warning("Por favor, insira uma URL e um XPath válidos para iniciar o monitoramento.")