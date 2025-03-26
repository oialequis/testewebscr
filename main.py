import streamlit as st
from playwright.sync_api import sync_playwright

# Função para inicializar o Playwright e pegar o conteúdo do elemento
def get_element_by_xpath(url, xpath):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url)
            element = page.locator(f'xpath={xpath}')
            content = element.text_content()
            return content if content else "Elemento não encontrado ou sem texto."
        except Exception as e:
            return f"Erro ao encontrar o elemento: {e}"
        finally:
            browser.close()

# Interface do Streamlit
st.title("Streamlit + Playwright: Buscar Elemento pelo XPath")

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
