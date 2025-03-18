import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Função para inicializar o Selenium WebDriver e pegar o conteúdo do elemento
def get_element_by_xpath(url, xpath):
    # Configurar as opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem abrir o navegador (modo invisível)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Inicializar o WebDriver do Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acessar a página desejada
        driver.get(url)
        
        # Encontrar o elemento pelo XPath
        element = driver.find_element(By.XPATH, xpath)
        
        # Retornar o texto do elemento
        return element.text
    except Exception as e:
        return f"Erro ao encontrar o elemento: {e}"
    finally:
        # Fechar o navegador
        driver.quit()

# Interface do Streamlit
st.title("Streamlit + Selenium: Buscar Elemento pelo XPath")

# Entrada de URL
url = st.text_input("Digite a URL da página:")

# Entrada de XPath
xpath = st.text_input("Digite o XPath do elemento:")

# Botão para buscar o conteúdo do elemento
if st.button("Buscar Elemento"):
    if url and xpath:
        content = get_element_by_xpath(url, xpath)
        st.write(f"Conteúdo do elemento: {content}")
    else:
        st.error("Por favor, insira uma URL e um XPath válidos.")
