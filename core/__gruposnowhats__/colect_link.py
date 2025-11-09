# coletar link dos grupos no WhatsApp
# https://gruposnowhats.com/?page={numero de 1 ate 100}

def etp1(max_pages: int = 1000):
    """Etapa 1 — coleta links de grupos do site gruposnowhats.

    Percorre páginas do site `https://gruposnowhats.com/?page=1..n`, busca anchors
    cujo conteúdo contenha 'Entrar no grupo' e extrai o href.

    Salva o JSON em `data/gruposnowhats_links.json` e imprime um log para cada link.
    """
    import re
    import time
    from urllib.parse import urljoin
    from core.utils.http import fetch_text
    from core.utils.io import save_json

    base = "https://gruposnowhats.com/"
    delay = 0.3  # segundos entre requests

    seen = set()
    results = []

    anchor_re = re.compile(r'<a[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<body>.*?)</a>', re.IGNORECASE | re.DOTALL)

    for page in range(1, max_pages + 1):
        page_url = f"{base}?page={page}"
        try:
            status, html = fetch_text(page_url)
        except Exception as e:
            print(f"Erro ao buscar {page_url}: {e}")
            continue

        if status != 200 or not html:
            # parar caso não existam mais páginas (site pode retornar 404/empty)
            print(f"Página {page} retornou status {status}; pulando.")
            time.sleep(delay)
            continue

        for m in anchor_re.finditer(html):
            href = m.group('href').strip()
            body = m.group('body') or ''
            if 'entrar no grupo' in body.lower():
                full = urljoin(base, href)
                if full in seen:
                    continue
                seen.add(full)
                results.append(full)
                print(f"[page {page}] coletado: {full}")

        time.sleep(delay)

    # salvar
    out_path = save_json(results, "data", "gruposnowhats_links.json")
    print(f"Coleta finalizada: {len(results)} links salvos em {out_path}")
    return results