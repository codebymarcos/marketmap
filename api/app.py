from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import json

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.__gruposnowhats__.run import run_all
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

# Criar DB consolidado — aceita GET e POST (GET útil para navegador)
@app.api_route("/generate-db", methods=["GET", "POST"])
async def create_db(
    background_tasks: BackgroundTasks,
    limit_links: int = None,
    limit_invites: int = None,
    max_pages: int = 5
):
    # Agendar em background (sem bloquear a requisição)
    background_tasks.add_task(run_all, limit_links, limit_invites, max_pages)
    return {"message": "Coleta consolidada iniciada (background)", "status": "running", "output": "data/consolidated_database.json"}

# Limpar dados — aceita GET e POST
@app.api_route("/clear-data", methods=["GET", "POST"])
async def clear_db(data_dir: str = "data"):
    try:
        # Rodar limpeza de forma síncrona — rápida
        clear_data(data_dir)
        return {"message": f"Pasta {data_dir} limpa", "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obter dados consolidados — aceita GET
@app.get("/database")
async def get_database():
    try:
        db_path = Path("data/consolidated_database.json")
        if not db_path.exists():
            raise HTTPException(status_code=404, detail="Database não encontrado. Execute /generate-db primeiro.")

        with db_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "database": data,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obter apenas invites — aceita GET
@app.get("/invites")
async def get_invites():
    try:
        db_path = Path("data/consolidated_database.json")
        if not db_path.exists():
            raise HTTPException(status_code=404, detail="Database não encontrado. Execute /generate-db primeiro.")

        with db_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "invites": data.get("invites", []),
            "total": len(data.get("invites", [])),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)