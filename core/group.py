# procurar grupos
# entrar na url "https://gruposdewhats.com.br/"
# extrair html da página
# adicionar o html em um arquivo .html

import requests
import re
import json
from pathlib import Path
from urllib.parse import urlparse
from core.utils.http import fetch_text
from core.utils.extractor import extract_links
from core.utils.io import save_json, save_html


def extrair_html(url, namedb: str = "gruposdewhats_extracao.json", out_path: str | Path = "data"):

    # Acessa a URL e retorna apenas as partes relevantes do HTML.
    status, html = fetch_text(url)
    if status != 200:
        return {"error": f"Erro ao acessar a página: {status}"}

    # procura padrões como: <a href="..." title="..."><h2>Texto</h2>
    pattern = re.compile(r'<a\s+[^>]*href="(?P<href>[^"]+)"[^>]*title="(?P<title>[^"]+)"[^>]*>(?:\s*<h2>(?P<h2>.*?)</h2>)?', re.IGNORECASE | re.DOTALL)
    matches = pattern.finditer(html)

    # evitar duplicatas usando um conjunto e filtrar links irrelevantes
    resultados = []
    vistos_endpoints = set()
    blacklist = ("blog", "minha conta", "contato", "sobre", "termos", "privacidade")
    blacklist_paths = ("/minha-conta", "/category/")

    for m in matches:
        href = (m.group('href') or '').strip()
        title = (m.group('title') or '').strip()
        h2 = (m.group('h2') or '').strip()
        text = h2 if h2 else title

        # filtros simples: href não vazio, não âncora local, não mailto/telefone/javascript
        if not href:
            continue
        low = href.lower()
        if low.startswith('#') or low.startswith('mailto:') or low.startswith('tel:') or low.startswith('javascript:'):
            continue

        # normaliza endpoint: host + path (ou apenas path se for relativo)
        parsed = urlparse(href)
        endpoint_key = (parsed.netloc + parsed.path) if parsed.netloc else parsed.path
        endpoint_key = endpoint_key.lower()

        # ignorar endpoints específicos (ex: /minha-conta) e itens com palavras irrelevantes
        if any(bp in endpoint_key for bp in blacklist_paths):
            continue
        if any(b in low for b in blacklist):
            continue

        # ignorar se já vimos este endpoint (mesmo path com queries diferentes)
        if endpoint_key in vistos_endpoints:
            continue
        vistos_endpoints.add(endpoint_key)

        resultados.append({"href": href, "title": title, "text": text})

    # grava resultados em JSON se namedb/out_path fornecidos
    try:
        arquivo_json = save_json(resultados, out_path, namedb)
        # se houver um html salvo temporário no diretório, remove-o (comportamento antigo)
        html_file = Path(out_path) / "gruposdewhats.html"
        if html_file.exists():
            html_file.unlink()
    except Exception:
        # se falhar na escrita, apenas retornamos os resultados
        pass

    return resultados

# teste
if __name__ == "__main__":
   url = "https://gruposdewhats.com.br/"
   namedb = "quick_extracao.json"
   out = "data"
   resultados = extrair_html(url, namedb=namedb, out_path=out)
   print(f"Extração rápida: {len(resultados)} itens (salvos em {out}/{namedb})")
