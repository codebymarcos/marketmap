"""Pacote `core` — atalhos de importação para funções e utilitários principais.

Imports são feitos de forma tolerante para evitar falhas de import em ambientes
onde algum módulo ainda não está disponível (útil durante desenvolvimento).
"""

__all__ = []

try:
    from .group import extrair_html
except Exception:
    extrair_html = None
else:
    __all__.append("extrair_html")

try:
    from .linkwpp import extrair_link_invite
except Exception:
    extrair_link_invite = None
else:
    __all__.append("extrair_link_invite")

try:
    from . import utils
except Exception:
    utils = None
else:
    __all__.append("utils")

