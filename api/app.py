from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from functs.gerardb import generate_db
from functs.cleardb import clear_data

app = FastAPI(title="MarketMap API")

# CORS para Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar DB em background — aceita GET e POST (GET útil para navegador)
@app.api_route("/generate-db", methods=["GET", "POST"])
async def create_db(
    background_tasks: BackgroundTasks,
    url: str = "https://gruposdewhats.com.br/",
    namedb: str = "quick_extracao.json",
    out: str = "data"
):
    # Agendar em background (sem bloquear a requisição)
    background_tasks.add_task(generate_db, url, namedb, out)
    return {"message": "DB iniciado (background)", "status": "running"}

# Limpar dados — aceita GET e POST
@app.api_route("/clear-data", methods=["GET", "POST"])
async def clear_db(data_dir: str = "data"):
    try:
        # Rodar limpeza de forma síncrona — rápida
        clear_data(data_dir)
        return {"message": f"Pasta {data_dir} limpa", "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)