# limpar data

import sys
from pathlib import Path
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""

def clear_data(data_dir="data"):
    """Limpa a pasta de dados, removendo todos os arquivos."""
    try:
        data_path = Path(data_dir)
        if data_path.exists() and data_path.is_dir():
            for file_path in data_path.iterdir():
                if file_path.is_file():
                    file_path.unlink()
                    print(f"{Fore.YELLOW}Removido: {file_path}")
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    print(f"{Fore.YELLOW}Removido diretório: {file_path}")
            print(f"{Fore.GREEN}Pasta {data_dir} limpa.")
        else:
            print(f"{Fore.RED}Pasta {data_dir} não existe.")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Limpeza interrompida pelo usuário.")
        print(f"{Fore.RED}Saindo...")

if __name__ == "__main__":
    clear_data()
