# criar ambiente virtual
import sys
from pathlib import Path
import subprocess

def preparar_ambiente():
    """Prepara o ambiente virtual e instala as dependências."""
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
    else:
        print("Ambiente virtual já existe.")

    pip_executable = venv_path / "Scripts" / "pip.exe" if sys.platform == "win32" else venv_path / "bin" / "pip"
    print("Instalando dependências...")
    subprocess.run([str(pip_executable), "install", "-r", "requirements.txt"])
    print("Ambiente preparado com sucesso.")

if __name__ == "__main__":
    preparar_ambiente()
    print("!"*12)
    print(" ativa o ambiente .venv\\Scripts\\activate" )
    print(" testa a API mano --> python api\\app.py")
    print("le o arquivo api\\api.md pra tu ver as rotas")
    print("!"*12)