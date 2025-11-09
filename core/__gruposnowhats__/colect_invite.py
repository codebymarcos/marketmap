"""Extrai invites de cada página de grupo coletada (etapa final).

Esse módulo espera um JSON com objetos que contenham a chave `href` (por exemplo
gerado por `core.group.extrair_html`). Para cada URL, chama
`core.linkwpp.extrair_link_invite` e agrega os invites em um JSON final.

Uso:
    from core.__gruposnowhats__.colect_invite import etp1
    etp1(pages_json='data/quick_extracao.json', out='data')
"""
from pathlib import Path
import json
from typing import List, Iterable, Optional
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from colorama import Fore, init
    init(autoreset=True)
except Exception:
    class Fore:  # tipo stub quando colorama não estiver disponível
        GREEN = ""
        YELLOW = ""
        RED = ""

from core.linkwpp import extrair_link_invite
from core.utils.io import save_json


def etp1(pages_json: str = "data/quick_extracao.json", out: str = "data", invites_namedb: str = "invites.json", limit: Optional[int] = None) -> List[str]:
    """Percorre as URLs do arquivo JSON e extrai invites.

    Args:
        pages_json: caminho para o JSON com as páginas coletadas (lista de objetos com 'href').
        out: diretório de saída para salvar invites.
        invites_namedb: nome do arquivo de invites a salvar.
        limit: se setado, limita o número de URLs processadas (útil para testes).

    Retorna lista de invites extraídos (únicos, em ordem de descoberta).
    """
    pages_path = Path(pages_json)
    if not pages_path.exists():
        print(f"{Fore.RED}Arquivo de páginas não encontrado: {pages_path}")
        return []

    try:
        with pages_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"{Fore.RED}Erro ao ler {pages_path}: {e}")
        return []

    # Extrair hrefs
    urls: List[str] = []
    for item in data:
        if isinstance(item, dict):
            href = item.get("href") or item.get("url")
            if href:
                urls.append(href)
        elif isinstance(item, str):
            urls.append(item)

    if limit is not None:
        urls = urls[:limit]

    total = len(urls)
    print(f"{Fore.GREEN}Iniciando extração de invites: {total} páginas")

    all_invites: List[str] = []
    for i, page_url in enumerate(urls, start=1):
        print(f"{Fore.YELLOW}[{i}/{total}] Processando: {page_url}")
        try:
            invites = extrair_link_invite(page_url, out, invites_namedb)
            # extrair_link_invite já salva no arquivo, mas retornamos os encontrados nesta página
            for inv in invites:
                if inv not in all_invites:
                    all_invites.append(inv)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Interrompido pelo usuário. Salvando progresso...")
            break
        except Exception as e:
            print(f"{Fore.RED}Erro em {page_url}: {e}")
            continue

    # Salvar todos os invites únicos no arquivo final (garantia)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    save_json(all_invites, out_dir, invites_namedb)
    print(f"{Fore.GREEN}Invites extraídos: {len(all_invites)} itens salvos em {out_dir / invites_namedb}")
    return all_invites


if __name__ == "__main__":
    etp1(pages_json="data/gruposnowhats_links.json")
