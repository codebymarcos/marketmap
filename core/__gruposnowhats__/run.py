"""Executa as duas etapas automaticamente coletando de ambos os sites.

Uso:
    from core.__gruposnowhats__.run import run_all

    # Executar completo (pode demorar)
    run_all()

    # Executar com limites para teste
    run_all(limit_links=20, limit_invites=10, max_pages=2)

Parâmetros:
- limit_links: Limita o número total de links coletados de ambos os sites (opcional)
- limit_invites: Limita o número de invites extraídos (opcional - None = máximo possível)
- max_pages: Máximo de páginas a percorrer no gruposnowhats.com (padrão: 1000)

Resultado: Salva tudo em data/consolidated_database.json com links, invites e metadados.
"""

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


def run_all(limit_links: int = None, limit_invites: int = None, max_pages: int = 1000):
    """Executa as duas etapas automaticamente coletando de ambos os sites.

    Etapa 1: Coleta links dos grupos de DOIS sites:
        - gruposnowhats.com (usando colect_link.py)
        - gruposdewhats.com.br (usando generate_db)
    Etapa 2: Extrai invites de todos os links coletados

    Args:
        limit_links: Limita o número total de links coletados de ambos os sites (opcional).
        limit_invites: Limita o número de invites extraídos (opcional - None = máximo possível).
        max_pages: Número máximo de páginas a percorrer no gruposnowhats.com (padrão: 1000).
    """
    print(f"{Fore.GREEN}=== Iniciando execução automática das etapas ===")

    all_links = []

    # Etapa 1A: Coletar links do gruposnowhats.com
    print(f"{Fore.YELLOW}Coletando links do gruposnowhats.com (máx. {max_pages} páginas)...")
    try:
        from .colect_link import etp1 as collect_links
        links_nowhats = collect_links(max_pages=max_pages)
        all_links.extend(links_nowhats)
        print(f"{Fore.GREEN}Coletados {len(links_nowhats)} links do gruposnowhats.com")
    except Exception as e:
        print(f"{Fore.RED}Erro ao coletar do gruposnowhats.com: {e}")

    # Etapa 1B: Coletar links do gruposdewhats.com.br
    print(f"{Fore.YELLOW}Coletando links do gruposdewhats.com.br...")
    try:
        from functs.gerardb import generate_db
        resultados_dewhats, _ = generate_db()  # Só precisamos dos links, não dos invites ainda
        # Extrair apenas os hrefs dos resultados
        links_dewhats = [item.get("href") for item in resultados_dewhats if item.get("href")]
        all_links.extend(links_dewhats)
        print(f"{Fore.GREEN}Coletados {len(links_dewhats)} links do gruposdewhats.com.br")
    except Exception as e:
        print(f"{Fore.RED}Erro ao coletar do gruposdewhats.com.br: {e}")

    # Remover duplicatas
    unique_links = list(set(all_links))
    print(f"{Fore.GREEN}Total de links únicos coletados: {len(unique_links)}")

    # Aplicar limite se especificado
    if limit_links and len(unique_links) > limit_links:
        unique_links = unique_links[:limit_links]
        print(f"{Fore.GREEN}Links limitados a {len(unique_links)} itens.")

    # Etapa 2: Extrair invites de todos os links coletados
    print(f"{Fore.YELLOW}Extraindo invites de {len(unique_links)} links coletados...")
    try:
        from .colect_invite import etp1 as extract_invites
        # Criar um JSON temporário com todos os links coletados
        import json
        from pathlib import Path
        from datetime import datetime

        temp_data = [{"href": link} for link in unique_links]
        temp_json_path = Path("data/temp_all_links.json")
        temp_json_path.parent.mkdir(parents=True, exist_ok=True)
        with temp_json_path.open("w", encoding="utf-8") as f:
            json.dump(temp_data, f, ensure_ascii=False, indent=2)

        # Extrair invites usando o JSON temporário
        invites = extract_invites(pages_json=str(temp_json_path), limit=limit_invites)

        # Limpar arquivo temporário
        temp_json_path.unlink(missing_ok=True)

        # Salvar tudo em um único arquivo JSON consolidado
        consolidated_data = {
            "links": unique_links,
            "invites": invites,
            "metadata": {
                "total_links": len(unique_links),
                "total_invites": len(invites),
                "collected_at": datetime.now().isoformat(),
                "sources": ["gruposnowhats.com", "gruposdewhats.com.br"]
            }
        }

        output_path = Path("data/consolidated_database.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(consolidated_data, f, ensure_ascii=False, indent=2)

        print(f"{Fore.GREEN}Banco de dados consolidado salvo em: {output_path}")
        print(f"{Fore.GREEN}=== Execução concluída com sucesso! ===")
        print(f"{Fore.GREEN}Links coletados (total): {len(unique_links)}")
        print(f"{Fore.GREEN}Invites extraídos: {len(invites)}")
        return unique_links, invites
    except Exception as e:
        print(f"{Fore.RED}Erro na extração de invites: {e}")
        return unique_links, []


if __name__ == "__main__":
    # Executar completo (máximo possível - pode demorar muito!)
    run_all()
