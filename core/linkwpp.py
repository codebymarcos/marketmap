# abrir links do arquivo json
# procurar as partes <div class="form-group">
# <a href="https://chat.whatsapp.com/invite/LKIonV2tXBvEwtVrCFNbVl" class="btn btn-success btn-block" target="_blank">ENTRAR NO GRUPO</a></div>
# extrair o invite do link


import re
import json
from pathlib import Path
from typing import List

from core.utils.http import fetch_text
from core.utils.io import save_json


def extrair_link_invite(url, output, namedb):
    # 1) Buscar HTML
    status, html = fetch_text(url)
    if status != 200:
        return []

    # 2) Encontrar links de invite (aceita /invite/ID ou /ID)
    pattern = re.compile(r"https?://chat\.whatsapp\.com/(?:invite/)?(?P<id>[A-Za-z0-9_-]{10,})")
    ids = [m.group("id") for m in pattern.finditer(html)]
    if not ids:
        return []

    # Normaliza para um formato consistente
    invites = [f"https://chat.whatsapp.com/invite/{i}" for i in dict.fromkeys(ids)]  # dedupe mantendo ordem

    # 3) Mesclar com arquivo existente (se houver)
    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)
    db_path = out_dir / namedb

    try:
        if db_path.exists():
            with db_path.open("r", encoding="utf-8") as f:
                existing = json.load(f)
                if isinstance(existing, list):
                    # garantir que todos sejam strings
                    existing_list = [str(x) for x in existing]
                else:
                    existing_list = []
        else:
            existing_list = []
    except Exception:
        existing_list = []

    # merge mantendo ordem: existing primeiro, depois novos que não estejam presentes
    merged = list(dict.fromkeys(existing_list + invites))

    # 4) salvar
    save_json(merged, out_dir, namedb)

    # Retorna apenas os invites encontrados nesta página (não todo o arquivo)
    return invites
    
if __name__ == "__main__":
    url = "https://gruposdewhats.com.br/signo-de-virgem-1/"
    resultados = extrair_link_invite(url, "data", "invites.json")