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


# Inicializar o cliente Dropbox
dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN)
