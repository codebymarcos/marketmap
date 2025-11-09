# gerar o db

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from pathlib import Path
from core.group import extrair_html
from core.linkwpp import extrair_link_invite

try:
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        BLUE = ""

def load_config():
    config_path = Path(__file__).parent.parent / "cofig.json"
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_db(url="https://gruposdewhats.com.br/", namedb="quick_extracao.json", out="data"):
    """Gera o banco de dados extraindo links de grupos do WhatsApp e seus invites."""
    try:
        resultados = extrair_html(url, namedb=namedb, out_path=out)
        print(f"{Fore.GREEN}Extração rápida: {len(resultados)} itens (salvos em {out}/{namedb})")

        # executar o linkwpp.py em loop um por um com o json gerado e criar o json com os invites
        out_dir = Path(out)
        json_path = out_dir / namedb
        if json_path.exists():
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                urls = [item.get("href") for item in data if item.get("href")]
        else:
            urls = []

        invites_db = []
        total_urls = len(urls)
        for i, group_url in enumerate(urls, 1):
            print(f"{Fore.BLUE}[{i}/{total_urls}] Extraindo invites de: {group_url}")
            try:
                invites = extrair_link_invite(group_url, out, "invites.json")
                invites_db.extend(invites)
            except Exception as e:
                print(f"{Fore.RED}Erro ao extrair de {group_url}: {e}")
                continue

        # Salvar invites únicos em um novo JSON
        config = load_config()
        invites_file = config.get("invites_file", "data/invites.json")
        unique_invites = list(set(invites_db))
        invites_json_path = Path(invites_file)
        invites_json_path.parent.mkdir(parents=True, exist_ok=True)
        with invites_json_path.open("w", encoding="utf-8") as f:
            json.dump(unique_invites, f, ensure_ascii=False, indent=2)

        print(f"{Fore.GREEN}Invites extraídos: {len(unique_invites)} itens salvos em {invites_json_path}")

        return resultados, unique_invites
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Processo interrompido pelo usuário. Salvando progresso...")
        # Salvar o que foi extraído até agora
        if 'invites_db' in locals():
            config = load_config()
            invites_file = config.get("invites_file", "data/invites.json")
            unique_invites = list(set(invites_db))
            invites_json_path = Path(invites_file)
            invites_json_path.parent.mkdir(parents=True, exist_ok=True)
            with invites_json_path.open("w", encoding="utf-8") as f:
                json.dump(unique_invites, f, ensure_ascii=False, indent=2)
            print(f"{Fore.GREEN}Progresso salvo: {len(unique_invites)} invites em {invites_json_path}")
        print(f"{Fore.RED}Saindo...")
        return [], []

if __name__ == "__main__":
    generate_db()