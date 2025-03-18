import subprocess
import sys

def install_playwright():
    try:
        print("Instalando o Playwright e os navegadores...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("Playwright e navegadores instalados com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro durante a instalação do Playwright: {e}")
        sys.exit(1)

def run_streamlit():
    try:
        print("Iniciando o Streamlit...")
        subprocess.run(["streamlit", "run", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao rodar o Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_playwright()  # Instala o Playwright e os navegadores
    run_streamlit()       # Executa o Streamlit
